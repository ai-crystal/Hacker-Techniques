# -*- coding: utf-8 -*-
"""全系列体检：结构、图片、图号、代码块、标题字符。

    python books/build/verify.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BOOKS = ROOT / "books"

CN = "零一二三四五六七八九十"


def cn_to_int(s: str) -> int:
    if s.isdigit():
        return int(s)
    if s == "十":
        return 10
    if s.startswith("十"):
        return 10 + CN.index(s[1])
    if "十" in s:
        a, b = s.split("十")
        return CN.index(a) * 10 + (CN.index(b) if b else 0)
    return CN.index(s)


class Checker:
    def __init__(self, book_dir: Path):
        self.dir = book_dir
        self.name = book_dir.name
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def err(self, msg: str) -> None:
        self.errors.append(f"[{self.name}] {msg}")

    def warn(self, msg: str) -> None:
        self.warnings.append(f"[{self.name}] {msg}")

    def check(self) -> None:
        cfg_path = self.dir / "book.json"
        struct_path = self.dir / "structure.json"
        if not cfg_path.exists():
            self.err("缺少 book.json")
            return
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        for key in ("title", "pdf", "volume_no"):
            if key not in cfg:
                self.err(f"book.json 缺少字段 {key}")
        struct = json.loads(struct_path.read_text(encoding="utf-8"))

        chapters = [i for i in struct if i.get("kind") == "chapter"]
        total_chapters = len(chapters)

        for item in struct:
            rel = item.get("path", "")
            if item.get("kind") == "toc":
                continue
            p = self.dir / rel
            if not p.exists():
                self.err(f"structure.json 指向不存在的文件 {rel}")
                continue
            if rel.endswith(".md"):
                self.check_md(p, total_chapters)

    def check_md(self, path: Path, total_chapters: int) -> None:
        text = path.read_text(encoding="utf-8")
        body = re.sub(r"```.*?```", "", text, flags=re.S)
        rel = path.relative_to(self.dir)

        # 代码块围栏配对
        if len(re.findall(r"^```", text, flags=re.M)) % 2:
            self.err(f"{rel}: 代码块围栏数量为奇数")
        if re.search(r"^````", text, flags=re.M):
            self.err(f"{rel}: 出现四反引号嵌套代码块")

        # 标题里的危险字符
        for m in re.finditer(r"^(#{1,4})\s+(.*)$", body, flags=re.M):
            title = m.group(2)
            if re.search(r"[`*_\[\]<>|]", title):
                self.err(f"{rel}: 标题含特殊字符 {title[:24]}")
            if not title.strip():
                self.err(f"{rel}: 空标题")

        # 图片存在性与重复
        imgs = re.findall(r'<img src="([^"]+)"', text)
        for src in imgs:
            if src.startswith("http"):
                continue
            if not (path.parent / src).resolve().exists():
                self.err(f"{rel}: 缺图 {src}")
        for a, b in zip(imgs, imgs[1:]):
            if a == b:
                self.err(f"{rel}: 相邻重复图片 {a}")

        # 图号与章号一致、连续
        m = re.search(r"^#\s+第([一二三四五六七八九十]+)章", body, flags=re.M)
        if m:
            ch = cn_to_int(m.group(1))
            nums = re.findall(r"<figcaption>图 (\d+)-(\d+)", text)
            for idx, (c, n) in enumerate(nums, start=1):
                if int(c) != ch:
                    self.err(f"{rel}: 图号 {c}-{n} 与章号 {ch} 不一致")
                if int(n) != idx:
                    self.err(f"{rel}: 图号不连续，第 {idx} 张写成 {c}-{n}")
            if ch > total_chapters:
                self.err(f"{rel}: 章号 {ch} 超过总章数 {total_chapters}")

        # 章节引用范围
        for m in re.finditer(r"第([一二三四五六七八九十]+)章", body):
            n = cn_to_int(m.group(1))
            if n > total_chapters:
                self.err(f"{rel}: 引用了不存在的第 {n} 章")

        # 未闭合的 figure
        if text.count("<figure>") != text.count("</figure>"):
            self.err(f"{rel}: figure 标签不配对")
        if "<figcaption></figcaption>" in text:
            self.err(f"{rel}: 空图注")


def main() -> bool:
    ok = True
    pdfs = {}
    for d in sorted(BOOKS.iterdir()):
        if not (d / "book.json").exists():
            continue
        c = Checker(d)
        c.check()
        cfg = json.loads((d / "book.json").read_text(encoding="utf-8"))
        pdf = cfg.get("pdf")
        if pdf in pdfs:
            c.err(f"输出文件名 {pdf} 与 {pdfs[pdf]} 重复")
        pdfs[pdf] = d.name
        for e in c.errors:
            print("ERROR " + e)
        for w in c.warnings:
            print("WARN  " + w)
        if c.errors:
            ok = False
    print("体检通过" if ok else "体检未通过")
    return ok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
