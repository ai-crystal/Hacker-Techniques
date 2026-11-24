# -*- coding: utf-8 -*-
"""第五章插图：注入前后语句结构的变化、XSS 的数据流。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)

SYNTAX = ("语法", PALE_2, INK, LINE)
DATA = ("数据", PALE_BLUE, BLUE, "#b6c4d2")
EVIL = ("注入", PALE_WARN, WARN, "#d8b6a6")


def strip(ax, x, y, h, tokens, fs=6.2, gap=0.8):
    for text, kind, w in tokens:
        if kind == "dead":
            box(ax, x, y, w, h, fc="white", ec=GREY, lw=0.8, radius=0.4)
            label(ax, x + w / 2, y + h / 2, text, fs=fs, color=GREY)
            ax.plot([x + 1.2, x + w - 1.2], [y + h / 2, y + h / 2],
                    color=GREY, lw=0.8, ls=(0, (2, 2)))
        else:
            _, fc, color, ec = {"syn": SYNTAX, "dat": DATA, "bad": EVIL}[kind]
            box(ax, x, y, w, h, fc=fc, ec=ec, lw=0.8, radius=0.4)
            label(ax, x + w / 2, y + h / 2, text, fs=fs, color=color,
                  weight="bold" if kind == "bad" else "normal")
        x += w + gap
    return x - gap


def sqli_tokens():
    fig, ax = setup(5.3, 3.2)

    head = [("SELECT", "syn", 10.5), ("*", "syn", 4.8), ("FROM", "syn", 9.5),
            ("u", "syn", 4.8), ("WHERE", "syn", 10.0), ("n", "syn", 4.8),
            ("=", "syn", 4.8)]

    label(ax, 5, 52.6, "输入 alice", fs=6.6, color=SOFT, ha="left")
    row_a = head + [("'alice'", "dat", 12.5), ("AND a=1", "syn", 12.0)]
    strip(ax, 5, 43.0, 7.4, row_a)

    label(ax, 5, 38.4,
          "引号里的内容是一个值，整条语句的结构由开发者决定",
          fs=6.4, color=GREY, ha="left")

    label(ax, 5, 30.6, "输入 ' OR 1=1 -- -", fs=6.6, color=WARN, ha="left")
    row_b = head + [("' OR 1=1", "bad", 13.0), ("-- -", "bad", 7.5),
                    ("AND a=1", "dead", 12.0)]
    strip(ax, 5, 21.0, 7.4, row_b)

    label(ax, 5, 16.4,
          "引号闭合了字面量，后面的词成了语法，末尾的条件被注释吞掉",
          fs=6.4, color=GREY, ha="left")

    legend = [("开发者写的语法", SYNTAX, 5.0),
              ("用户输入的值", DATA, 33.0),
              ("被当成语法的输入", EVIL, 60.0)]
    for text, (_, fc, color, ec), x in legend:
        box(ax, x, 4.6, 3.4, 3.4, fc=fc, ec=ec, lw=0.8, radius=0.4)
        label(ax, x + 5.0, 6.3, text, fs=6.4, color=SOFT, ha="left")
    return save(fig, "05", "sqli-tokens.png")


def xss_flow():
    fig, ax = setup(5.3, 2.6)

    stages = [
        ("用户输入", "反射 · 存储 · DOM", "三种形态的差别在前两步", PALE, INK),
        ("拼接进页面", "输出编码", "按输出上下文选字符集", PALE_2, INK),
        ("浏览器解析", "CSP", "不给内联脚本留口子", PALE_2, INK),
        ("脚本执行", "HttpOnly", "只挡住读 cookie 这一条路", PALE_WARN, WARN),
    ]

    x, w = 3.0, 34.0
    h, gap = 7.0, 4.8
    top = 44.0

    for i, (name, key, note, fc, color) in enumerate(stages):
        y = top - (h + gap) * i
        ec = LINE if fc != PALE_WARN else "#d8b6a6"
        box(ax, x, y - h, w, h, fc=fc, ec=ec)
        label(ax, x + w / 2, y - h / 2, name, fs=7.8, color=color,
              weight="bold")
        label(ax, x + w + 4.0, y - h / 2 + 2.4, key, fs=7.0, color=color,
              ha="left", weight="bold")
        label(ax, x + w + 4.0, y - h / 2 - 2.2, note, fs=6.4, color=SOFT,
              ha="left")
        if i:
            arrow(ax, (x + w / 2, y + gap - 0.2), (x + w / 2, y + 0.2))

    return save(fig, "05", "xss-flow.png")


if __name__ == "__main__":
    sqli_tokens()
    xss_flow()
