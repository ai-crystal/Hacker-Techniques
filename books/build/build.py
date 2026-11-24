#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""系列书构建脚本。

    python books/build/build.py --book beginner
    python books/build/build.py --book theory --no-opt
    python books/build/build.py --all

流程：Markdown → HTML → Chrome 打印 → 合并封面/正文/封底 →
      生成两级书签 → 压缩插图 → output/<册名>.pdf
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import time
from pathlib import Path

import markdown
import pymupdf
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
BOOKS = ROOT / "books"
COMMON = BOOKS / "common"
CACHE_ROOT = BOOKS / "build" / ".cache"
OUT_DIR = ROOT / "output"

PAGE_W, PAGE_H = "170mm", "240mm"
MARGIN = {"top": "20mm", "bottom": "18mm", "left": "19mm", "right": "19mm"}

MAX_FILE_MB = 19.0
IMG_MAX_W = 1500
JPEG_QUALITY = 84

DEFAULT_CFG = {
    "series": "黑客技术与安全原理",
    "author": "Dr. Dezeming",
    "year": "2026",
    "accent": "#0f5c5c",
    "accent_light": "#7fb0b2",
    "toc_sections": False,
    "cover_image": "E:/Study/0-logo/logo1.png",
    "back_image": "E:/Study/0-logo/logo15.png",
    "blurb": [],
}


class Book:
    """一册书的配置与路径。"""

    def __init__(self, name: str):
        self.name = name
        self.dir = BOOKS / name
        if not self.dir.is_dir():
            raise SystemExit(f"找不到分册目录：{self.dir}")
        cfg_path = self.dir / "book.json"
        cfg = dict(DEFAULT_CFG)
        if cfg_path.exists():
            cfg.update(json.loads(cfg_path.read_text(encoding="utf-8")))
        self.cfg = cfg
        self.title = cfg["title"]
        self.volume = cfg.get("volume", cfg["title"])
        self.subtitle = cfg.get("subtitle", "")
        self.pdf_name = cfg["pdf"]
        self.out_pdf = OUT_DIR / self.pdf_name
        self.cache = CACHE_ROOT / name
        self.structure = json.loads(
            (self.dir / "structure.json").read_text(encoding="utf-8"))

    def cover_uri(self, key: str, tag: str) -> str:
        src = Path(self.cfg.get(key, ""))
        if not src.exists():
            raise SystemExit(f"封面底图不存在：{src}")
        out = self.cache / f"{tag}-bg.jpg"
        out.parent.mkdir(parents=True, exist_ok=True)
        if not out.exists() or out.stat().st_mtime < src.stat().st_mtime:
            with Image.open(src) as im:
                im = im.convert("RGB")
                if im.width > 1500:
                    im = im.resize((1500, int(im.height * 1500 / im.width)),
                                   Image.LANCZOS)
                im.save(out, "JPEG", quality=86, optimize=True, progressive=True)
        return out.as_uri()


# ---------------------------------------------------------------- 字体与样式

sys.path.insert(0, str(COMMON))
import cover as cover_mod  # noqa: E402


def page_css(book: Book) -> str:
    base = (COMMON / "assets" / "book.css").read_text(encoding="utf-8")
    extra = (book.dir / "assets" / "book.css")
    if extra.exists():
        base += "\n" + extra.read_text(encoding="utf-8")
    return base


# ---------------------------------------------------------------- 图片

IMAGE_RE = re.compile(r'src="((?:\.\./)+images/[^"]+)"')


def compress_image(src: Path, cache: Path, max_w: int, quality: int) -> Path:
    stat = src.stat()
    key = f"{src}-{stat.st_mtime_ns}-{max_w}-{quality}"
    digest = hashlib.md5(key.encode("utf-8")).hexdigest()[:16]
    out = cache / "img" / f"{digest}.jpg"
    if out.exists():
        return out
    out.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as im:
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            bg = Image.new("RGB", im.size, (255, 255, 255))
            bg.paste(im, mask=im.split()[-1])
            im = bg
        else:
            im = im.convert("RGB")
        if im.width > max_w:
            im = im.resize((max_w, int(im.height * max_w / im.width)),
                           Image.LANCZOS)
        im.save(out, "JPEG", quality=quality, optimize=True, progressive=True)
    return out


def rewrite_images(text: str, md_dir: Path, cache: Path, opt: bool) -> str:
    def repl(m: re.Match) -> str:
        src = (md_dir / m.group(1)).resolve()
        if not src.exists():
            print(f"  ! 缺少图片 {src}")
            return m.group(0)
        if opt:
            return f'src="{compress_image(src, cache, IMG_MAX_W, JPEG_QUALITY).as_uri()}"'
        return f'src="{src.as_uri()}"'

    return IMAGE_RE.sub(repl, text)


# ---------------------------------------------------------------- Markdown

def make_md() -> markdown.Markdown:
    return markdown.Markdown(
        extensions=["codehilite", "extra", "sane_lists", "nl2br"],
        extension_configs={"codehilite": {"guess_lang": False,
                                          "css_class": "highlight"}},
    )


def split_heading(text: str) -> tuple[str, str]:
    text = re.sub(r"<[^>]+>", "", text).strip()
    m = re.match(
        r"^(第[一二三四五六七八九十百]+[章篇部]|附录\s*[A-Z]|序言|前言|后记|致谢)\s*(.*)$",
        text)
    if m and m.group(2):
        return m.group(1).strip(), m.group(2).strip()
    return "", text


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Section:
    def __init__(self, rel: str, kind: str):
        self.rel = rel
        self.kind = kind
        self.title = ""
        self.kicker = ""
        self.marker = ""
        self.html = ""
        self.level = 1


def render_section(book: Book, rel: str, kind: str, opt: bool) -> Section:
    sec = Section(rel, kind)
    path = book.dir / rel
    if not path.exists():
        raise FileNotFoundError(f"structure.json 里列出的文件不存在：{rel}")
    raw = path.read_text(encoding="utf-8")
    raw = rewrite_images(raw, path.parent, book.cache, opt)
    html = make_md().convert(raw)

    m = re.search(r"<h1>(.*?)</h1>", html, re.S)
    if m:
        kicker, title = split_heading(m.group(1))
        sec.kicker, sec.title = kicker, title
        inner = ""
        if kicker:
            inner += f'<span class="kicker">{esc(kicker)}</span>'
        inner += f'<span class="ct">{title}</span>'
        html = html[:m.start()] + "<h1>" + inner + "</h1>" + html[m.end():]

    sec.html = html
    return sec


# ---------------------------------------------------------------- 目录页

TOC_HTML = ('<section class="toc"><h1><span class="kicker">CONTENTS</span>'
            '<span class="ct">目　录</span></h1>\n%s\n</section>')


def build_toc(entries: list[Section], pages: dict[str, int], sections: bool) -> str:
    rows = []
    for sec in entries:
        if sec.kind == "part":
            rows.append(f'<div class="toc-part">{esc(sec.kicker)}　{sec.title}</div>')
            continue
        pg = pages.get(sec.marker)
        label = f"{sec.kicker}　{sec.title}" if sec.kicker else sec.title
        rows.append(
            '<div class="toc-item"><span class="t">%s</span>'
            '<span class="dots"></span><span class="pg">%s</span></div>'
            % (esc(label), pg if pg is not None else ""))
    return TOC_HTML % "\n".join(rows)


def page_shell(book: Book, body: str) -> str:
    return f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<title>{book.title}</title>
<style>{cover_mod.font_css()}</style>
<style>{page_css(book)}</style>
<style>:root {{ --accent: {book.cfg['accent']}; --accent-ink: {book.cfg.get('accent_ink', '#14312f')}; --accent-soft: {book.cfg.get('accent_soft', '#b9c9c5')}; }}</style>
</head><body>
{body}
</body></html>"""


# ---------------------------------------------------------------- 渲染

def launch_browser(pw):
    args = ["--font-render-hinting=none", "--disable-lcd-text",
            "--allow-file-access-from-files"]
    for kwargs in ({"channel": "chrome"}, {"channel": "msedge"}, {}):
        try:
            return pw.chromium.launch(args=args, **kwargs)
        except Exception:
            continue
    raise RuntimeError("找不到可用的 Chrome/Chromium，请先安装 Google Chrome，"
                       "或运行 python -m playwright install chromium")


def render_pdf(page, book: Book, html_text: str, name: str, *,
               full_bleed: bool = False, footer: bool = True) -> Path:
    tmpdir = book.cache / "html"
    tmpdir.mkdir(parents=True, exist_ok=True)
    tmp = tmpdir / f"{name}.html"
    tmp.write_text(html_text, encoding="utf-8")
    out = book.cache / f"{name}.pdf"
    opts = dict(path=str(out), print_background=True,
                width=PAGE_W, height=PAGE_H, prefer_css_page_size=False)
    if full_bleed:
        opts.update(margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
                    display_header_footer=False)
    else:
        opts.update(margin=MARGIN, display_header_footer=footer,
                    header_template="<div></div>")
        if footer:
            opts["footer_template"] = (
                '<div style="width:100%;text-align:center;font-family:Georgia,serif;'
                'font-size:8pt;color:#6a6a6e;"><span class="pageNumber"></span></div>')
    page.goto(tmp.as_uri(), wait_until="load")
    page.wait_for_timeout(300)
    page.pdf(**opts)
    return out


def find_pages(doc, markers: dict) -> dict:
    found = {}
    pending = dict(markers)
    for i, page in enumerate(doc):
        if not pending:
            break
        text = page.get_text()
        for m in [k for k in pending if k in text]:
            found[m] = i + 1
            pending.pop(m)
    for m in pending:
        print(f"  ! 未定位书签 {m} {markers[m]}")
    return found


def strip_markers(doc, markers: list) -> None:
    for page in doc:
        rects = []
        for m in markers:
            rects.extend(page.search_for(m))
        if not rects:
            continue
        for r in rects:
            page.add_redact_annot(r, fill=None)
        page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE)


def export_cover_images(book: Book) -> None:
    doc = pymupdf.open(book.out_pdf)
    for idx, name in ((0, "cover.jpg"), (doc.page_count - 1, "backcover.jpg")):
        pix = doc[idx].get_pixmap(dpi=150)
        pix.save(book.dir / "images" / name, jpg_quality=88)
    doc.close()
    # 站点封面用的无字底图
    src = Path(book.cfg["cover_image"])
    if src.exists():
        with Image.open(src) as im:
            im = im.convert("RGB")
            if im.width > 1600:
                im = im.resize((1600, int(im.height * 1600 / im.width)),
                               Image.LANCZOS)
            im.save(book.dir / "images" / "cover-bg.jpg", "JPEG",
                    quality=85, optimize=True, progressive=True)


# ---------------------------------------------------------------- 主流程

def build(book: Book, opt: bool = True) -> Path:
    t0 = time.time()
    book.cache.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    sections: list[Section] = []
    toc_at = None
    for i, item in enumerate(book.structure):
        rel, kind = item["path"], item["kind"]
        if kind == "toc":
            toc_at = len(sections)
            continue
        sections.append(render_section(book, rel, kind, opt))
    if toc_at is None:
        toc_at = 0

    bookmarkable = [s for s in sections
                    if s.kind in ("part", "chapter", "front", "appendix")]
    for i, sec in enumerate(bookmarkable, start=1):
        sec.marker = f"@@B{i:03d}@@"
        sec.html = sec.html.replace(
            "<h1>", f'<h1><span class="bmk">{sec.marker}</span>', 1)
        sec.level = 1 if sec.kind in ("part", "front", "appendix") else 2

    head_kinds = ("titlepage", "copyright", "front")
    head = [s for s in sections[:toc_at] if s.kind in head_kinds]
    body = [s for s in sections[toc_at:] if s.kind in
            ("part", "chapter", "front", "appendix")]

    def wrap(sec: Section) -> str:
        cls = {"part": "part", "chapter": "chapter", "front": "front",
               "appendix": "appendix", "titlepage": "titlepage",
               "copyright": "copyright"}[sec.kind]
        lead = ""
        if sec.kind == "part":
            num = "".join(ch for ch in Path(sec.rel).stem if ch.isdigit())
            lead = f'<div class="part-lead">PART {int(num or 0):02d}</div>'
        return (f'<section class="{cls}" data-src="{sec.rel}">'
                f'{lead}{sec.html}</section>')

    body_html = page_shell(book, "\n".join(wrap(s) for s in body))
    head_html = page_shell(book, "\n".join(wrap(s) for s in head))
    toc_entries = [s for s in body
                   if s.kind in ("part", "chapter", "appendix", "front")]

    with sync_playwright() as pw:
        browser = launch_browser(pw)
        page = browser.new_page(viewport={"width": 900, "height": 1200})
        page.emulate_media(media="print")

        cover_pdf = render_pdf(
            page, book,
            cover_mod.cover_html(book.cfg, book.cover_uri("cover_image", "cover")),
            "cover", full_bleed=True)
        back_pdf = render_pdf(
            page, book,
            cover_mod.cover_html(book.cfg, book.cover_uri("back_image", "back"),
                                 back=True),
            "back", full_bleed=True)
        body_pdf = render_pdf(page, book, body_html, "body")
        body_doc = pymupdf.open(body_pdf)
        body_pages = find_pages(body_doc, {s.marker: s.title for s in toc_entries})

        toc_block = build_toc(toc_entries, body_pages, book.cfg["toc_sections"])
        front_pdf = render_pdf(
            page, book, head_html.replace("</body>", toc_block + "</body>"),
            "front", footer=False)
        browser.close()

    doc = pymupdf.open()
    doc.insert_pdf(pymupdf.open(cover_pdf))
    doc.insert_pdf(pymupdf.open(front_pdf))
    body_start = doc.page_count + 1
    doc.insert_pdf(body_doc)
    doc.insert_pdf(pymupdf.open(back_pdf))

    abs_pages = find_pages(doc, {s.marker: s.title for s in bookmarkable})
    toc = []
    for sec in bookmarkable:
        pg = abs_pages.get(sec.marker, 1)
        label = f"{sec.kicker}　{sec.title}" if sec.kicker else sec.title
        toc.append([sec.level, label, pg])

    strip_markers(doc, [s.marker for s in bookmarkable])
    doc.set_toc(toc)
    doc.set_metadata({
        "title": f"{book.title}·{book.volume}" if book.volume != book.title
                 else book.title,
        "author": book.cfg["author"],
        "subject": book.subtitle,
        "keywords": book.cfg.get("keywords", ""),
        "creator": "books/build/build.py",
        "producer": "Chrome / PyMuPDF",
    })

    tmp_out = OUT_DIR / (book.pdf_name + ".tmp")
    doc.save(tmp_out, garbage=4, deflate=True, clean=True)
    doc.close()
    if book.out_pdf.exists():
        book.out_pdf.unlink()
    shutil.move(tmp_out, book.out_pdf)

    export_cover_images(book)
    size = book.out_pdf.stat().st_size / 1024 / 1024
    pages = pymupdf.open(book.out_pdf).page_count
    print(f"  [{book.name}] {pages} 页，书签 {len(toc)} 条，"
          f"{size:.2f} MB，用时 {time.time() - t0:.1f}s")
    return book.out_pdf


def verify_series() -> bool:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import verify
    return verify.main()


def main() -> int:
    ap = argparse.ArgumentParser(description="构建系列中的一册或全部")
    ap.add_argument("--book", help="分册目录名，如 beginner")
    ap.add_argument("--all", action="store_true", help="构建全部")
    ap.add_argument("--no-opt", action="store_true", help="跳过图片压缩")
    ap.add_argument("--no-verify", action="store_true", help="跳过体检")
    args = ap.parse_args()

    names = ([p.name for p in sorted(BOOKS.iterdir())
              if (p / "book.json").exists()] if args.all
             else [args.book] if args.book else [])
    if not names:
        ap.error("需要 --book <名称> 或 --all")

    if not args.no_verify and not verify_series():
        print("体检未通过，已停止构建")
        return 1

    failed = []
    for name in names:
        book = Book(name)
        try:
            out = build(book, opt=not args.no_opt)
            size = out.stat().st_size / 1024 / 1024
            if size > MAX_FILE_MB:
                print(f"  ! {name} 体积 {size:.2f} MB 超过上限，请继续压图")
                failed.append(name)
        except Exception as e:  # noqa: BLE001
            print(f"  ! {name} 构建失败：{e}")
            failed.append(name)
    if failed:
        print("失败：", ", ".join(failed))
        return 1
    print("完成：", ", ".join(f"{n} → output/" for n in names))
    return 0


if __name__ == "__main__":
    sys.exit(main())
