# -*- coding: utf-8 -*-
"""第九章插图：格式化字符串的取参顺序、注入的通用结构。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                    PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label, rect,
                    save, setup)


def format_string():
    fig, ax = setup(5.3, 3.0)
    box(ax, 3.0, 44.0, 40.0, 10.0, fc=PALE_WARN, ec="#e2ccc0")
    label(ax, 23.0, 49.0, "printf(buf)  buf = \"%x %x %x\"", fs=7.2, color=WARN)

    slots = [("rsi", 36.0), ("rdx", 30.0), ("rcx", 24.0), ("r8", 18.0),
             ("栈上参数", 12.0)]
    for name, y in slots:
        box(ax, 40.0, y, 18.0, 5.2, fc=PALE, ec=LINE)
        label(ax, 49.0, y + 2.6, name, fs=6.8, color=SOFT)
        box(ax, 60.0, y, 16.0, 5.2, fc="white", ec="#dcdcd6", lw=0.8)
        label(ax, 68.0, y + 2.6, "值", fs=6.6, color=GREY)

    label(ax, 49.0, 43.4, "printf 认为参数在这里", fs=6.6, color=GREY)
    for i, y in enumerate([38.6, 32.6, 26.6, 20.6]):
        label(ax, 36.0, y, "%x", fs=6.6, color=ACCENT, ha="right")
        arrow(ax, (37.2, y), (39.4, y), color=ACCENT, lw=0.8, ms=6)

    label(ax, 49.0, 7.0, "格式符多于实际参数时，printf 继续往栈上取", fs=7.2,
          color=WARN)
    label(ax, 49.0, 1.6, "取到的内容会被原样打印出来", fs=7.0, color=GREY)
    return save(fig, "09", "format-string.png")


def taint_boundary():
    fig, ax = setup(5.3, 3.2)
    box(ax, 3.0, 40.0, 26.0, 14.0, fc=PALE, ec=LINE)
    label(ax, 16.0, 49.6, "外部输入", fs=8.0, color=INK, weight="bold")
    label(ax, 16.0, 44.6, "用户名、文件名、请求体", fs=6.4, color=GREY)

    box(ax, 70.0, 40.0, 27.0, 14.0, fc=PALE_WARN, ec="#e2ccc0")
    label(ax, 83.5, 49.6, "解释器", fs=8.0, color=WARN, weight="bold")
    label(ax, 83.5, 44.6, "SQL、shell、反序列化", fs=6.4, color=GREY)

    ax.plot([34.0, 66.0], [47.0, 47.0], color="#c9cfcd", lw=1.0, ls=(0, (4, 2)))
    label(ax, 50.0, 50.4, "边界", fs=6.8, color=GREY)

    paths = [("直接拼接", 33.0, WARN), ("转义不完整", 26.0, WARN), ("参数化传递", 19.0, ACCENT)]
    for text, y, color in paths:
        arrow(ax, (30.4, y), (69.6, y), color=color, lw=1.0,
              ls="-" if color == ACCENT else (0, (3, 2)))
        label(ax, 50.0, y + 1.8, text, fs=6.6, color=color,
              bbox=dict(fc="white", ec="none", pad=0.8))

    label(ax, 50.0, 12.0, "线上是语法，线下是内容，跨过去就出事", fs=7.2, color=ACCENT)
    label(ax, 50.0, 5.6, "参数化的意义是把两者分开传，而不是靠过滤字符", fs=6.8, color=GREY)
    return save(fig, "09", "taint-boundary.png")


if __name__ == "__main__":
    format_string()
    taint_boundary()
