#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 book/ 下的 Markdown 排版成印刷版 PDF。

流程：Markdown -> HTML -> Chrome 打印 -> 合并封面/正文/封底
      -> 生成两级书签 -> 压缩图片 -> output/dark-gate.pdf
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path

import markdown
import pymupdf
from PIL import Image
from playwright.sync_api import sync_playwright

# ---------------------------------------------------------------- 基本配置

ROOT = Path(__file__).resolve().parents[2]
BOOK = ROOT / "book"
BUILD = BOOK / "build"
CACHE = BUILD / ".cache"
OUT_DIR = ROOT / "output"
OUT_PDF = OUT_DIR / "dark-gate.pdf"

TITLE = "暗门"
SUBTITLE = "黑客技术与安全原理"
AUTHOR = "Dr. Dezeming"
YEAR = "2026"

COVER_IMAGE = Path("E:/Study/0-logo/logo1.png")
BACK_IMAGE = Path("E:/Study/0-logo/logo15.png")

PAGE_W, PAGE_H = "170mm", "240mm"
MARGIN = {"top": "20mm", "bottom": "18mm", "left": "19mm", "right": "19mm"}

FONT_DIR = ROOT / "_private" / "fonts"

MAX_FILE_MB = 19.0
IMG_MAX_W = 1500
JPEG_QUALITY = 84


# ---------------------------------------------------------------- 字体

def font_css() -> str:
    """优先使用思源宋体/黑体，缺失时退回系统中文字体。"""
    faces = []
    serif_reg = FONT_DIR / "NotoSerifSC-Regular.otf"
    serif_bold = FONT_DIR / "NotoSerifSC-Bold.otf"
    sans_reg = FONT_DIR / "NotoSansSC-Regular.otf"
    sans_med = FONT_DIR / "NotoSansSC-Medium.otf"

    def url(p: Path) -> str:
        return p.resolve().as_uri()

    if serif_reg.exists():
        faces.append(
            '@font-face{font-family:"AnmenSerif";font-weight:400;'
            f'src:url("{url(serif_reg)}") format("opentype");}}')
    if serif_bold.exists():
        faces.append(
            '@font-face{font-family:"AnmenSerif";font-weight:700;'
            f'src:url("{url(serif_bold)}") format("opentype");}}')
    if sans_reg.exists():
        faces.append(
            '@font-face{font-family:"AnmenSans";font-weight:400;'
            f'src:url("{url(sans_reg)}") format("opentype");}}')
    if sans_med.exists():
        faces.append(
            '@font-face{font-family:"AnmenSans";font-weight:500;'
            f'src:url("{url(sans_med)}") format("opentype");}}')
        faces.append(
            '@font-face{font-family:"AnmenSans";font-weight:700;'
            f'src:url("{url(sans_med)}") format("opentype");}}')
    return "\n".join(faces)


# ---------------------------------------------------------------- 图片处理

IMAGE_RE = re.compile(r'src="((?:\.\./)+images/[^"]+)"')


def compress_image(src: Path, max_w: int = IMG_MAX_W, quality: int = JPEG_QUALITY) -> Path:
    """把插图转成压缩 JPEG，放进构建缓存。"""
    stat = src.stat()
    key = f"{src.name}-{stat.st_mtime_ns}-{max_w}-{quality}"
    digest = hashlib.md5(key.encode("utf-8")).hexdigest()[:16]
    out = CACHE / "img" / f"{digest}.jpg"
    if out.exists():
        return out
    out.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as im:
        im = im.convert("RGBA") if im.mode in ("RGBA", "LA", "P") else im.convert("RGB")
        if im.mode == "RGBA":
            bg = Image.new("RGB", im.size, (255, 255, 255))
            bg.paste(im, mask=im.split()[-1])
            im = bg
        if im.width > max_w:
            h = int(im.height * max_w / im.width)
            im = im.resize((max_w, h), Image.LANCZOS)
        im.save(out, "JPEG", quality=quality, optimize=True, progressive=True)
    return out


def rewrite_images(text: str, md_dir: Path, quality: int) -> str:
    def repl(m: re.Match) -> str:
        rel = m.group(1)
        src = (md_dir / rel).resolve()
        if not src.exists():
            print(f"  ! 缺少图片 {src}")
            return m.group(0)
        out = compress_image(src, quality=quality)
        return f'src="{out.as_uri()}"'

    return IMAGE_RE.sub(repl, text)


# ---------------------------------------------------------------- Markdown

def make_md() -> markdown.Markdown:
    return markdown.Markdown(
        extensions=[
            "codehilite",
            "extra",
            "sane_lists",
            "nl2br",
        ],
        extension_configs={
            "codehilite": {"guess_lang": False, "css_class": "highlight"},
        },
    )


CN_NUM = "零一二三四五六七八九十"


def split_heading(text: str) -> tuple[str, str]:
    """把 '第一章　程序是怎样跑起来的' 拆成 ('第一章', '程序是怎样跑起来的')。"""
    text = re.sub(r"<[^>]+>", "", text).strip()
    m = re.match(r"^(第[一二三四五六七八九十百]+[章篇部]|附录\s*[A-Z]|序言|前言|后记|致谢)\s*(.*)$", text)
    if m and m.group(2):
        return m.group(1).strip(), m.group(2).strip()
    return "", text


def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


class Section:
    def __init__(self, path: Path, kind: str):
        self.path = path
        self.kind = kind            # part / chapter / front / appendix / toc / titlepage / copyright
        self.title = ""
        self.kicker = ""
        self.marker = ""
        self.html = ""
        self.level = 0

    @property
    def number(self) -> str:
        m = re.search(r"ch(\d+)", self.path.name)
        if m:
            return str(int(m.group(1)))
        m = re.search(r"a(\d+)", self.path.name)
        if m:
            return "A" if m.group(1) == "1" else f"A{m.group(1)}"
        return ""


def render_section(path: Path, kind: str, quality: int) -> Section:
    sec = Section(path, kind)
    raw = path.read_text(encoding="utf-8")
    raw = rewrite_images(raw, path.parent, quality)

    md = make_md()
    html = md.convert(raw)

    # 第一个 h1 拆成 kicker + 标题
    m = re.search(r"<h1>(.*?)</h1>", html, re.S)
    if m:
        kicker, title = split_heading(m.group(1))
        sec.kicker, sec.title = kicker, title
        inner = ""
        if kicker:
            inner += f'<span class="kicker">{esc(kicker)}</span>'
        inner += f'<span class="ct">{title}</span>'
        html = html[:m.start()] + "<h1>" + inner + "</h1>" + html[m.end():]

    # 二级标题编号（Markdown 里已经手写，这里只在缺失时补）
    num = sec.number
    if False and kind == "chapter" and num:
        counter = [0]

        def h2_repl(mm: re.Match) -> str:
            counter[0] += 1
            inner = mm.group(1)
            if re.match(r"^\s*<span class=\"secnum\">", inner):
                return mm.group(0)
            return (f'<h2><span class="secnum">{num}.{counter[0]}</span>'
                    f"{inner}</h2>")

        html = re.sub(r"<h2>(.*?)</h2>", h2_repl, html, flags=re.S)
    elif kind == "appendix" and num:
        counter = [0]
        label = "A" if num == "A" else num

        def h2a(mm: re.Match) -> str:
            counter[0] += 1
            return (f'<h2><span class="secnum">{label}.{counter[0]}</span>'
                    f"{mm.group(1)}</h2>")

        html = re.sub(r"<h2>(.*?)</h2>", h2a, html, flags=re.S)

    sec.html = html
    return sec


# ---------------------------------------------------------------- 封面

COVER_CSS = """
@page { size: %(w)s %(h)s; margin: 0; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { width: %(w)s; height: %(h)s; overflow: hidden; }
.page { position: relative; width: %(w)s; height: %(h)s; overflow: hidden;
        background: #04101c; font-family: "AnmenSans", "Microsoft YaHei", sans-serif; }
.page img.bg { position: absolute; inset: 0; width: 100%%; height: 100%%;
               object-fit: cover; }
.shade { position: absolute; inset: 0; }
.cover .shade { background: linear-gradient(180deg,
    rgba(3,10,20,0.80) 0%%, rgba(3,10,20,0.34) 38%%,
    rgba(3,10,20,0.52) 62%%, rgba(3,10,20,0.92) 100%%); }
.cover .inner { position: absolute; inset: 0; padding: 22mm 16mm 18mm 16mm;
    display: flex; flex-direction: column; color: #f4f7f8; }
.cover .eyebrow { font-size: 7.6pt; letter-spacing: 0.36em; color: #9fc4c6;
    text-transform: uppercase; }
.cover .rule-thin { width: 26mm; height: 0.9pt; background: #6fb3b3;
    margin: 6mm 0 0 0; }
.cover .spacer { flex: 1; }
.cover .title { font-size: 62pt; font-weight: 700; letter-spacing: 0.22em;
    line-height: 1; margin-left: -2mm; }
.cover .subtitle { font-size: 13pt; font-weight: 400; letter-spacing: 0.34em;
    color: #d6e6e6; margin-top: 7mm; }
.cover .tagline { font-size: 8.4pt; letter-spacing: 0.2em; color: #8fa6a8;
    margin-top: 5mm; }
.cover .bottom { margin-top: 10mm; display: flex; align-items: flex-end;
    justify-content: space-between; }
.cover .author { font-size: 11pt; letter-spacing: 0.18em; }
.cover .year { font-size: 8pt; letter-spacing: 0.2em; color: #93a9ab; }

.back .shade { background:
    linear-gradient(180deg, rgba(3,12,18,0.88) 0%%, rgba(3,12,18,0.44) 46%%,
      rgba(3,12,18,0.34) 66%%, rgba(3,12,18,0.92) 100%%),
    linear-gradient(90deg, rgba(3,12,18,0.55) 0%%, rgba(3,12,18,0) 62%%); }
.back .inner { position: absolute; inset: 0; padding: 26mm 18mm 18mm 18mm;
    color: #e8eeee; display: flex; flex-direction: column; }
.back .kicker { font-size: 7.4pt; letter-spacing: 0.34em; color: #9ecfd0;
    text-shadow: 0 1px 6px rgba(0,0,0,0.5);
    margin-bottom: 9mm; }
.back .blurb p { font-family: "AnmenSerif", "Noto Serif SC", "SimSun", serif;
    font-size: 9.6pt; line-height: 2.05; text-indent: 0; color: #eef4f4;
    text-align: justify; margin-bottom: 4.6mm;
    text-shadow: 0 1px 6px rgba(0,0,0,0.55); }
.back .blurb p.first::first-letter { color: #ffffff; }
.back .spacer { flex: 1; }
.back .meta { font-size: 8.4pt; line-height: 2.1; color: #a8bcbe;
    border-top: 0.6pt solid rgba(180,210,210,0.35); padding-top: 5mm; }
.back .meta .name { color: #f2f6f6; font-size: 9.6pt; letter-spacing: 0.12em; }
"""

COVER_HTML = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<style>%(font)s</style><style>%(css)s</style></head><body>
<div class="page cover">
  <img class="bg" src="%(bg)s">
  <div class="shade"></div>
  <div class="inner">
    <div class="eyebrow">From Silicon to Botnet</div>
    <div class="rule-thin"></div>
    <div class="spacer"></div>
    <div class="title">暗门</div>
    <div class="subtitle">黑客技术与安全原理</div>
    <div class="tagline">一台机器如何被说服去做它本不该做的事</div>
    <div class="bottom">
      <div class="author">%(author)s 著</div>
      <div class="year">%(year)s</div>
    </div>
  </div>
</div></body></html>"""

BACK_HTML = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<style>%(font)s</style><style>%(css)s</style></head><body>
<div class="page back">
  <img class="bg" src="%(bg)s">
  <div class="shade"></div>
  <div class="inner">
    <div class="kicker">内容简介</div>
    <div class="blurb">
      %(blurb)s
    </div>
    <div class="spacer"></div>
    <div class="meta">
      <div class="name">%(author)s</div>
      <div>常年与底层代码和二进制打交道，习惯把复杂系统拆开看。</div>
      <div>本书写给刚接触计算机、又想把安全这件事想明白的读者。</div>
    </div>
  </div>
</div></body></html>"""


def cover_image(src: Path, tag: str) -> str:
    """封面底图单独压一遍，避免整张原图被塞进 PDF。"""
    out = CACHE / f"cover-bg-{tag}.jpg"
    if not out.exists() or out.stat().st_mtime < src.stat().st_mtime:
        out.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(src) as im:
            im = im.convert("RGB")
            if im.width > 1500:
                im = im.resize((1500, int(im.height * 1500 / im.width)), Image.LANCZOS)
            im.save(out, "JPEG", quality=86, optimize=True, progressive=True)
    return out.as_uri()


def cover_html(back: bool = False) -> str:
    css = COVER_CSS % {"w": PAGE_W, "h": PAGE_H}
    if back:
        blurb = (
            "<p class='first'>你每天使用的电脑和手机，本质上是一台只会照做指令的机器。"
            "它不会分辨指令来自谁，也不会判断这条指令该不该执行。所谓的入侵，"
            "往往就是想办法让它执行一段原本不属于它的指令。</p>"
            "<p>本书从晶体管、内存和系统调用讲起，一路走到栈溢出、中间人攻击、"
            "蠕虫传播和勒索软件，把黑客技术背后的原理摊开在读者面前。"
            "读完它，你不会立刻变成安全专家，但再看那些耸人听闻的新闻时，"
            "你能判断出危险究竟发生在哪一层。</p>"
        )
        return BACK_HTML % {
            "font": font_css(), "css": css, "author": AUTHOR, "year": YEAR,
            "bg": cover_image(BACK_IMAGE, "back"), "blurb": blurb,
        }
    return COVER_HTML % {
        "font": font_css(), "css": css, "author": AUTHOR, "year": YEAR,
        "bg": cover_image(COVER_IMAGE, "front"),
    }


# ---------------------------------------------------------------- 组装

def read_order() -> list[str]:
    lines = []
    for line in (BUILD / "order.txt").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        lines.append(line)
    return lines


def classify(rel: str) -> str:
    name = Path(rel).name
    if name.startswith("part"):
        return "part"
    if name == "titlepage.md":
        return "titlepage"
    if name == "copyright.md":
        return "copyright"
    if rel.startswith("chapters/"):
        return "chapter"
    if rel.startswith("appendix/"):
        return "appendix"
    return "front"


TOC_HTML = """<section class="toc"><h1><span class="kicker">CONTENTS</span><span class="ct">目　录</span></h1>
%s
</section>"""


def build_toc(entries: list[Section], pages: dict[str, int]) -> str:
    rows = []
    for sec in entries:
        if sec.kind == "part":
            rows.append(f'<div class="toc-part">{esc(sec.kicker)}　{sec.title}</div>')
        else:
            pg = pages.get(sec.marker)
            label = f"{sec.kicker}　{sec.title}" if sec.kicker else sec.title
            rows.append(
                '<div class="toc-item"><span class="t">%s</span>'
                '<span class="dots"></span><span class="pg">%s</span></div>'
                % (esc(label), pg if pg is not None else ""))
    return TOC_HTML % "\n".join(rows)


def page_shell(css: str, body: str, extra_css: str = "") -> str:
    return f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<title>{TITLE}</title>
<style>{font_css()}</style>
<style>{css}</style>
<style>{extra_css}</style>
</head><body>
{body}
</body></html>"""


# ---------------------------------------------------------------- 渲染

def launch_browser(pw):
    """优先用系统里的 Chrome，退回 Playwright 自带的 Chromium 或 Edge。"""
    args = ["--font-render-hinting=none", "--disable-lcd-text",
            "--allow-file-access-from-files"]
    for kwargs in ({"channel": "chrome"}, {"channel": "msedge"}, {}):
        try:
            return pw.chromium.launch(args=args, **kwargs)
        except Exception:
            continue
    raise RuntimeError("找不到可用的 Chrome/Chromium，请先安装 Google Chrome，"
                       "或运行 python -m playwright install chromium")


def render_pdf(page, html_text: str, out: Path, *, full_bleed: bool = False,
               footer: bool = True) -> Path:
    tmp = CACHE / "html" / (out.stem + ".html")
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(html_text, encoding="utf-8")
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
    """markers: marker -> 标题；返回 marker -> 页码（从 1 开始）。"""
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
            for r in page.search_for(m):
                rects.append(r)
        if not rects:
            continue
        for r in rects:
            page.add_redact_annot(r, fill=None)
        page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE)


# ---------------------------------------------------------------- 主流程

def build(quality: int = JPEG_QUALITY, verbose: bool = True) -> Path:
    t0 = time.time()
    CACHE.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    css = (BUILD / "assets" / "book.css").read_text(encoding="utf-8")

    order = read_order()
    sections = []
    for rel in order:
        if rel == "@toc":
            continue
        path = BOOK / rel
        if not path.exists():
            raise FileNotFoundError(f"order.txt 里列出的文件不存在: {rel}")
        sections.append(render_section(path, classify(rel), quality))

    bookmarkable = [s for s in sections
                    if s.kind in ("part", "chapter", "front", "appendix")]
    for i, sec in enumerate(bookmarkable, start=1):
        sec.marker = f"@@B{i:03d}@@"
        sec.html = sec.html.replace(
            "<h1>", f'<h1><span class="bmk">{sec.marker}</span>', 1)
        sec.level = 1 if sec.kind in ("part", "front", "appendix") else 2

    preface = [s for s in sections if s.kind == "front" and "preface" in s.path.name]
    front_secs = [s for s in sections if s.kind in ("titlepage", "copyright")] + preface
    body_secs = [s for s in sections if s not in front_secs]

    def wrap(sec: Section) -> str:
        cls = {"part": "part", "chapter": "chapter", "front": "front",
               "appendix": "appendix", "titlepage": "titlepage",
               "copyright": "copyright"}[sec.kind]
        lead = ""
        if sec.kind == "part":
            num = "".join(ch for ch in sec.path.stem if ch.isdigit())
            lead = f'<div class="part-lead">PART {int(num):02d}</div>'
        return (f'<section class="{cls}" data-src="{sec.path.name}">'
                f'{lead}{sec.html}</section>')

    body_html = page_shell(css, "\n".join(wrap(s) for s in body_secs))
    front_html = page_shell(css, "\n".join(wrap(s) for s in front_secs))
    toc_entries = [s for s in body_secs
                   if s.kind in ("part", "chapter", "appendix", "front")]

    with sync_playwright() as pw:
        browser = launch_browser(pw)
        page = browser.new_page(viewport={"width": 900, "height": 1200})
        page.emulate_media(media="print")

        cover_pdf = render_pdf(page, cover_html(False), CACHE / "cover.pdf",
                               full_bleed=True)
        back_pdf = render_pdf(page, cover_html(True), CACHE / "back.pdf",
                              full_bleed=True)
        body_pdf = render_pdf(page, body_html, CACHE / "body.pdf")
        body_doc = pymupdf.open(body_pdf)
        body_pages = find_pages(body_doc, {s.marker: s.title for s in toc_entries})

        toc_block = build_toc(toc_entries, body_pages)
        front_pdf = render_pdf(page, front_html.replace("</body>", toc_block + "</body>"),
                               CACHE / "front.pdf", footer=False)
        browser.close()

    doc = pymupdf.open()
    doc.insert_pdf(pymupdf.open(cover_pdf))
    doc.insert_pdf(pymupdf.open(front_pdf))
    body_start = doc.page_count + 1
    doc.insert_pdf(body_doc)
    doc.insert_pdf(pymupdf.open(back_pdf))

    abs_pages = find_pages(doc, {s.marker: s.title for s in bookmarkable})
    toc = []
    for sec in sections:
        if sec.kind not in ("part", "chapter", "front", "appendix"):
            continue
        pg = abs_pages.get(sec.marker, 1)
        label = f"{sec.kicker}　{sec.title}" if sec.kicker else sec.title
        toc.append([sec.level, label, pg])

    strip_markers(doc, [s.marker for s in bookmarkable])
    doc.set_toc(toc)
    doc.set_metadata({
        "title": f"{TITLE}：{SUBTITLE}",
        "author": AUTHOR,
        "subject": "黑客技术的原理与攻防逻辑",
        "keywords": "网络安全, 漏洞, 恶意软件, 密码学, 科普",
        "creator": f"{TITLE} build script",
        "producer": "Chrome / PyMuPDF",
    })

    tmp_out = OUT_DIR / "dark-gate.tmp.pdf"
    doc.save(tmp_out, garbage=4, deflate=True, clean=True)
    doc.close()
    if OUT_PDF.exists():
        OUT_PDF.unlink()
    shutil.move(tmp_out, OUT_PDF)

    export_cover_images()

    size_mb = OUT_PDF.stat().st_size / 1024 / 1024
    if verbose:
        pages = pymupdf.open(OUT_PDF).page_count
        print(f"  页数 {pages}，正文起始第 {body_start} 页，"
              f"书签 {len(toc)} 条，体积 {size_mb:.2f} MB，"
              f"用时 {time.time() - t0:.1f}s")
    return OUT_PDF


def export_cover_images() -> None:
    """把封面和封底导出成 JPEG，供在线站点与仓库首页使用。"""
    doc = pymupdf.open(OUT_PDF)
    for idx, name in ((0, "cover.jpg"), (doc.page_count - 1, "backcover.jpg")):
        pix = doc[idx].get_pixmap(dpi=150)
        out = BOOK / "images" / name
        pix.save(out, jpg_quality=88)
    doc.close()
    # 站点封面用的底图（不带书名文字），避免与网页标题重复
    bg = BOOK / "images" / "cover-bg.jpg"
    with Image.open(COVER_IMAGE) as im:
        im = im.convert("RGB")
        if im.width > 1600:
            im = im.resize((1600, int(im.height * 1600 / im.width)), Image.LANCZOS)
        im.save(bg, "JPEG", quality=85, optimize=True, progressive=True)


def main() -> int:
    quality = JPEG_QUALITY
    for _ in range(4):
        out = build(quality)
        size_mb = out.stat().st_size / 1024 / 1024
        if size_mb <= MAX_FILE_MB:
            print(f"OK  {out}  ({size_mb:.2f} MB)")
            return 0
        quality = max(58, quality - 8)
        print(f"  体积 {size_mb:.2f} MB 超过 {MAX_FILE_MB} MB，"
              f"以 JPEG 质量 {quality} 重新生成")
    print("仍然超出体积上限，请检查插图尺寸")
    return 1


if __name__ == "__main__":
    sys.exit(main())
