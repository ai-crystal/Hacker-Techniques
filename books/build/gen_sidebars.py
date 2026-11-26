# -*- coding: utf-8 -*-
"""按 book.json / structure.json 生成系列侧栏，并刷新首页里的章数与页数。

    python books/build/gen_sidebars.py

侧栏是完全生成的，手改会被覆盖；首页 README 的正文是手写的，这里只替换
「共 N 章 · P 页」和表格里的页数、PDF 文件名，不动其余文字。
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BOOKS = ROOT / "books"
OUTPUT = ROOT / "output"
NL = "\n"

CN_NUM = "零一二三四五六七八九十"


def volume_order() -> list[dict]:
    items = []
    for d in BOOKS.iterdir():
        cfg_path = d / "book.json"
        if cfg_path.exists():
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
            cfg["_dir"] = d.name
            items.append(cfg)
    items.sort(key=lambda c: c.get("volume_no", 99))
    return items


def h1_of(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^#\s+(.+)$", text, flags=re.M)
    return m.group(1).strip() if m else path.stem


def chapter_title(path: Path, index: int) -> str:
    raw = h1_of(path)
    raw = re.sub(r"^第[一二三四五六七八九十百\d]+章[\s\u3000]*", "", raw)
    return f"第 {index} 章　{raw}"


def structure(book_dir: Path) -> list[dict]:
    return json.loads((book_dir / "structure.json").read_text(encoding="utf-8"))


def pdf_path(cfg: dict) -> str:
    return f"output/{cfg['pdf']}"


def root_sidebar(vols: list[dict]) -> str:
    lines = ["- [系列首页](/README.md)", ""]
    for cfg in vols:
        lines.append(f"- **{cfg['volume_no']:02d}　{cfg['volume']}**")
        lines.append(f"  - [本册首页](/books/{cfg['_dir']}/README.md)")
        lines.append(f'  - <a href="/{pdf_path(cfg)}" target="_blank" '
                     f'rel="noopener" data-router-ignore>下载 PDF</a>')
        lines.append("")
    return NL.join(lines).rstrip(NL) + NL


def book_sidebar(cfg: dict) -> str:
    name = cfg["_dir"]
    items = structure(BOOKS / name)
    lines = ["- [系列首页](/README.md)", f"- [本册首页](/books/{name}/README.md)", ""]
    prefaces = [i for i in items
                if i["kind"] == "front" and "preface" in i["path"]]
    if prefaces:
        for it in prefaces:
            lines.append(f"- [前言](/books/{name}/{it['path']})")
        lines.append("")
    idx = 0
    for it in items:
        if it["kind"] != "chapter":
            continue
        idx += 1
        p = BOOKS / name / it["path"]
        lines.append(f"- [{chapter_title(p, idx)}](/books/{name}/{it['path']})")
    lines.append("")
    apps = [i for i in items if i["kind"] == "appendix"]
    if apps:
        lines.append("- **附录**")
        for it in apps:
            lines.append(f"  - [{h1_of(BOOKS / name / it['path'])}]"
                         f"(/books/{name}/{it['path']})")
        lines.append("")
    lines.append(f'- <a href="/{pdf_path(cfg)}" target="_blank" '
                 f'rel="noopener" data-router-ignore>下载 PDF</a>')
    return NL.join(lines) + NL


def book_pages(cfg: dict) -> tuple[int, int, float] | None:
    pdf = OUTPUT / cfg["pdf"]
    if not pdf.exists():
        return None
    import pymupdf
    doc = pymupdf.open(pdf)
    pages = doc.page_count
    doc.close()
    ch = sum(1 for i in structure(BOOKS / cfg["_dir"]) if i["kind"] == "chapter")
    return ch, pages, pdf.stat().st_size / 1048576


def patch_root_readme(vols: list[dict]) -> None:
    path = ROOT / "README.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    for cfg in vols:
        info = book_pages(cfg)
        if not info:
            continue
        _, pages, _ = info
        name = cfg["_dir"]
        # 表格行：| 01 | [入门篇](books/beginner/README.md) | ... | 199 | ... |
        pattern = re.compile(
            r"(\|\s*\d{2}\s*\|\s*\[[^\]]+\]\(books/" + re.escape(name) +
            r"/README\.md\)[^\n]*?\|\s*)\d+(\s*\|)")
        text = pattern.sub(lambda m: f"{m.group(1)}{pages}{m.group(2)}", text)
        # 只在该册所在的行里改 PDF 名
        lines = text.split(chr(10))
        for idx, line in enumerate(lines):
            if line.startswith("|") and f"(books/{name}/README.md)" in line:
                lines[idx] = re.sub(r"output/v[0-9]+-[a-z]+[.]pdf",
                                    pdf_path(cfg), line)
        text = chr(10).join(lines)
    write(path, text)


def patch_book_readme(cfg: dict) -> None:
    path = BOOKS / cfg["_dir"] / "README.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    info = book_pages(cfg)
    if info:
        ch, pages, _ = info
        text = re.sub(r"共\s*\d+\s*章\s*·\s*\d+\s*页", f"共 {ch} 章 · {pages} 页", text)
    text = re.sub(r"\.\./\.\./output/v\d+-[a-z]+\.pdf",
                  f"../../{pdf_path(cfg)}", text)
    write(path, text)


def write(path: Path, text: str) -> None:
    """统一用 LF 写盘，避免 Windows 下产生 CRLF 差异。"""
    with open(path, "w", encoding="utf-8", newline=chr(10)) as fh:
        fh.write(text)


def main() -> None:
    vols = volume_order()
    write(ROOT / "_sidebar.md", root_sidebar(vols))
    for cfg in vols:
        d = BOOKS / cfg["_dir"]
        write(d / "_sidebar.md", book_sidebar(cfg))
        patch_book_readme(cfg)
        print(f"  {cfg['_dir']}: sidebar + README 计数")
    patch_root_readme(vols)
    print("  根目录：_sidebar.md + README 计数")


if __name__ == "__main__":
    main()
