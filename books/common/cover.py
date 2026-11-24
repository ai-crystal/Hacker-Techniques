# -*- coding: utf-8 -*-
"""字体、封面与封底的 HTML 生成。

各册共用同一套版式，靠背景图与强调色区分，摆在书架上能看出是一套。
"""

from __future__ import annotations

from pathlib import Path

PAGE_W, PAGE_H = "170mm", "240mm"

FONT_DIR = Path(__file__).resolve().parents[2] / "_private" / "fonts"

CN_NUM = {1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "七", 8: "八"}
EN_NUM = {1: "ONE", 2: "TWO", 3: "THREE", 4: "FOUR", 5: "FIVE", 6: "SIX"}


def font_css() -> str:
    """优先用思源宋体/黑体，缺字体时退回系统中文字体。"""
    faces = []
    pairs = [
        ("AnmenSerif", 400, "NotoSerifSC-Regular.otf"),
        ("AnmenSerif", 700, "NotoSerifSC-Bold.otf"),
        ("AnmenSans", 400, "NotoSansSC-Regular.otf"),
        ("AnmenSans", 500, "NotoSansSC-Medium.otf"),
        ("AnmenSans", 700, "NotoSansSC-Medium.otf"),
    ]
    for family, weight, name in pairs:
        path = FONT_DIR / name
        if path.exists():
            faces.append(
                f'@font-face{{font-family:"{family}";font-weight:{weight};'
                f'src:url("{path.as_uri()}") format("opentype");}}')
    return "\n".join(faces)


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
    rgba(3,10,20,0.82) 0%%, rgba(3,10,20,0.36) 38%%,
    rgba(3,10,20,0.54) 62%%, rgba(3,10,20,0.93) 100%%); }
.cover .inner { position: absolute; inset: 0; padding: 20mm 16mm 18mm 16mm;
    display: flex; flex-direction: column; color: #f4f7f8; }
.cover .series { font-size: 7.4pt; letter-spacing: 0.34em; color: #c3d9da;
    text-transform: uppercase; }
.cover .volno { margin-top: 3.4mm; font-size: 7.2pt; letter-spacing: 0.3em;
    color: %(accent_light)s; }
.cover .rule-thin { width: 26mm; height: 0.9pt; background: %(accent_light)s;
    margin: 6mm 0 0 0; }
.cover .spacer { flex: 1; }
.cover .title { font-size: 54pt; font-weight: 700; letter-spacing: 0.16em;
    line-height: 1.05; margin-left: -1mm; color: #ffffff; }
.cover .subtitle { font-size: 13pt; font-weight: 400; letter-spacing: 0.24em;
    color: #dbe9e9; margin-top: 7mm; }
.cover .tagline { font-size: 8.4pt; letter-spacing: 0.16em; color: #9db3b5;
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
    text-shadow: 0 1px 6px rgba(0,0,0,0.5); margin-bottom: 9mm; }
.back .blurb p { font-family: "AnmenSerif", "Noto Serif SC", "SimSun", serif;
    font-size: 9.6pt; line-height: 2.05; text-indent: 0; color: #eef4f4;
    text-align: justify; margin-bottom: 4.6mm;
    text-shadow: 0 1px 6px rgba(0,0,0,0.55); }
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
    <div class="series">%(series)s</div>
    <div class="volno">%(volno)s</div>
    <div class="rule-thin"></div>
    <div class="spacer"></div>
    <div class="title">%(title)s</div>
    <div class="subtitle">%(subtitle)s</div>
    <div class="tagline">%(tagline)s</div>
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
      <div>%(meta1)s</div>
      <div>%(meta2)s</div>
    </div>
  </div>
</div></body></html>"""


def cover_html(cfg: dict, bg_uri: str, back: bool = False) -> str:
    css = COVER_CSS % {
        "w": PAGE_W, "h": PAGE_H,
        "accent_light": cfg.get("accent_light", "#7fb0b2"),
    }
    if back:
        blurb = "".join(f"<p>{p}</p>" for p in cfg["blurb"])
        return BACK_HTML % {
            "font": font_css(), "css": css, "bg": bg_uri,
            "blurb": blurb,
            "author": cfg["author"],
            "meta1": cfg.get("meta1", "常年与底层代码和二进制打交道，习惯把复杂系统拆开看。"),
            "meta2": cfg.get("meta2", "写给想把安全这件事想明白的读者。"),
        }
    no = cfg["volume_no"]
    volno = f"卷{CN_NUM.get(no, no)}　VOLUME {EN_NUM.get(no, no)}"
    return COVER_HTML % {
        "font": font_css(), "css": css, "bg": bg_uri,
        "series": cfg.get("series", ""),
        "volno": volno,
        "title": cfg["volume"],
        "subtitle": cfg["subtitle"],
        "tagline": cfg.get("tagline", ""),
        "author": cfg["author"],
        "year": cfg["year"],
    }
