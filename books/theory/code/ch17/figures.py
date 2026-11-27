# -*- coding: utf-8 -*-
"""第十七章插图：内联与常量传播前后的控制流。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def cfg_before_after():
    fig, ax = setup(5.3, 3.0)
    # 左：优化前
    label(ax, 24.0, 50.0, "优化前", fs=7.6, color=SOFT, weight="bold")
    box(ax, 8.0, 38.0, 32.0, 7.0, fc=PALE, ec=LINE, lw=0.8)
    label(ax, 24.0, 41.5, "p = get(buf)", fs=6.2, color=INK)
    box(ax, 8.0, 27.0, 32.0, 7.0, fc=PALE_WARN, ec="#e2ccc0", lw=0.8)
    label(ax, 24.0, 30.5, "if (p == NULL) return", fs=6.2, color=WARN)
    box(ax, 8.0, 16.0, 14.0, 7.0, fc=PALE_BLUE, ec=LINE, lw=0.8)
    label(ax, 15.0, 19.5, "return", fs=6.0, color=BLUE)
    box(ax, 26.0, 16.0, 14.0, 7.0, fc=PALE, ec=LINE, lw=0.8)
    label(ax, 33.0, 19.5, "*p = 0", fs=6.0, color=INK)
    arrow(ax, (24.0, 37.4), (24.0, 34.6), color=GREY, lw=0.8, ms=6)
    arrow(ax, (20.0, 26.4), (15.0, 23.6), color=GREY, lw=0.8, ms=6)
    arrow(ax, (28.0, 26.4), (33.0, 23.6), color=GREY, lw=0.8, ms=6)

    # 右：优化后
    label(ax, 76.0, 50.0, "优化后（UB 假设 p 非空）", fs=7.6, color=SOFT, weight="bold")
    box(ax, 60.0, 38.0, 32.0, 7.0, fc=PALE, ec=LINE, lw=0.8)
    label(ax, 76.0, 41.5, "p = get(buf)", fs=6.2, color=INK)
    box(ax, 60.0, 26.0, 32.0, 7.0, fc=PALE_WARN, ec="#e2ccc0", lw=0.8)
    label(ax, 76.0, 29.5, "检查被判定为恒假，删除", fs=6.2, color=WARN)
    box(ax, 60.0, 14.0, 32.0, 7.0, fc=PALE_BLUE, ec=LINE, lw=0.8)
    label(ax, 76.0, 17.5, "*p = 0", fs=6.2, color=BLUE)
    arrow(ax, (76.0, 37.4), (76.0, 33.6), color=GREY, lw=0.8, ms=6)
    arrow(ax, (76.0, 25.4), (76.0, 21.6), color=WARN, lw=1.0, ms=6,
          ls=(0, (3, 2)))

    ax.plot([50.0, 50.0], [12.0, 52.0], color="#e0e0da", lw=0.9, ls=(0, (4, 3)))
    label(ax, 50.0, 6.0, "编译器假设空指针解引用不会发生，于是检查成了死代码", fs=6.8,
          color=SOFT)
    return save(fig, "17", "cfg-before-after.png")


if __name__ == "__main__":
    cfg_before_after()
