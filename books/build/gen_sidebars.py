# -*- coding: utf-8 -*-
"""从配置生成侧栏与各册首页，保持站点与 structure.json 一致。

    python books/build/gen_sidebars.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BOOKS = ROOT / "books"
OUTPUT = ROOT / "output"

ORDER = ["beginner", "theory", "practice"]
LABEL = {"beginner": "入门篇", "theory": "理论篇", "practice": "实战篇"}
NL = "\n"


def h1_of(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^#\s+(.+)$", text, flags=re.M)
    return m.group(1).strip() if m else path.stem


def book_pages(name: str):
    cfg = json.loads((BOOKS / name / "book.json").read_text(encoding="utf-8"))
    pdf = OUTPUT / cfg["pdf"]
    if not pdf.exists():
        return None
    import pymupdf
    doc = pymupdf.open(pdf)
    pages = doc.page_count
    doc.close()
    return pages, pdf.stat().st_size / 1048576


def sidebar(book_dir: Path) -> str:
    struct = json.loads((book_dir / "structure.json").read_text(encoding="utf-8"))
    name = book_dir.name
    lines = [f"- [本册首页](books/{name}/README.md)", ""]
    for item in struct:
        if item["kind"] == "toc":
            continue
        p = book_dir / item["path"]
        title = h1_of(p) if p.exists() else Path(item["path"]).stem
        if item["kind"] == "part":
            lines.append(f"- **{title}**")
        elif item["kind"] in ("chapter", "appendix", "front"):
            lines.append(f"- [{title}](books/{name}/{item['path']})")
    return NL.join(lines) + NL


def readme(book_dir: Path) -> str:
    name = book_dir.name
    cfg = json.loads((book_dir / "book.json").read_text(encoding="utf-8"))
    struct = json.loads((book_dir / "structure.json").read_text(encoding="utf-8"))
    info = book_pages(name)
    out = [f"# {cfg['volume']}　{cfg.get('subtitle', '')}", ""]
    if info:
        out += [f"共 {info[0]} 页，PDF {info[1]:.1f} MB。", ""]
    for para in cfg.get("blurb", []):
        out += [para, ""]
    out += [f"[下载本册 PDF](output/{cfg['pdf']})", "", "## 目录", ""]
    for item in struct:
        if item["kind"] == "toc":
            continue
        p = book_dir / item["path"]
        title = h1_of(p) if p.exists() else Path(item["path"]).stem
        if item["kind"] == "part":
            out += ["", f"### {title}", ""]
        elif item["kind"] in ("chapter", "appendix"):
            out.append(f"- [{title}](books/{name}/{item['path']})")
        elif item["kind"] == "front" and "postscript" in item["path"]:
            out += ["", f"- [{title}](books/{name}/{item['path']})"]
    return NL.join(out) + NL


def series_readme() -> str:
    rows = ["| 册 | 内容 | 页数 | 阅读 | 下载 |",
            "| --- | --- | --- | --- | --- |"]
    for name in ORDER:
        cfg = json.loads((BOOKS / name / "book.json").read_text(encoding="utf-8"))
        info = book_pages(name)
        pages = str(info[0]) if info else "构建中"
        rows.append(
            f"| {LABEL[name]} | {cfg.get('subtitle', '')} | {pages} | "
            f"[在线阅读](books/{name}/README.md) | "
            f'<a class="pdf-link" href="output/{cfg["pdf"]}" target="_blank" '
            f'rel="noopener">PDF</a> |')
    body = [
        "# 黑客技术与安全原理",
        "",
        "一套讲攻防原理的中文技术书，共三册。每一册都能单独读，合起来是一条从概念到动手的路径。",
        "",
        *rows,
        "",
        "## 三册的分工",
        "",
        "入门篇讲全貌。从 1971 年第一只会自我复制的程序讲到今天的勒索产业，"
        "再把机器、内存、网络、漏洞、恶意软件、人的因素逐层铺开。读完知道这个领域长什么样，"
        "遇到新闻能判断危险发生在哪一层。",
        "",
        "理论篇讲为什么。指令怎么编码，堆分配器怎么记账，一个越界写怎样变成任意读写，"
        "TLS 1.3 的握手为什么这样设计，检测为什么在数学上就有天花板。读完能自己判断一篇漏洞分析写得对不对。",
        "",
        "实战篇讲怎么做。在自己的虚拟机里搭靶场，从侦察、验证、利用、提权、横向一路做到样本分析和应急响应。"
        "每一步都要求能解释清楚为什么这样做。",
        "",
        "## 怎么读",
        "",
        "刚入门从第一册读起；已经能写代码、想弄清楚机制的直接读第二册；"
        "需要动手的从第三册开始，遇到不懂的概念再回去查。",
        "",
        "三册的实验环境、术语与例子保持统一，跨册阅读不需要重新适应。",
    ]
    return NL.join(body) + NL


def series_sidebar() -> str:
    lines = ["- [首页](README.md)", ""]
    for name in ORDER:
        cfg = json.loads((BOOKS / name / "book.json").read_text(encoding="utf-8"))
        info = book_pages(name)
        pages = f"　{info[0]} 页" if info else ""
        lines.append(f"- **{LABEL[name]}　{cfg.get('subtitle', '')}{pages}**")
        lines.append(f"- [本册首页](books/{name}/README.md)")
        lines.append("")
    return NL.join(lines) + NL


def main() -> None:
    for book_dir in sorted(BOOKS.iterdir()):
        if not (book_dir / "structure.json").exists():
            continue
        (book_dir / "_sidebar.md").write_text(sidebar(book_dir), encoding="utf-8")
        (book_dir / "README.md").write_text(readme(book_dir), encoding="utf-8")
        print(f"  {book_dir.name}: sidebar + README")
    (ROOT / "README.md").write_text(series_readme(), encoding="utf-8")
    (ROOT / "_sidebar.md").write_text(series_sidebar(), encoding="utf-8")
    print("  根目录：README.md / _sidebar.md")


if __name__ == "__main__":
    main()
