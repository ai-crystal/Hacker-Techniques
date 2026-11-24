# -*- coding: utf-8 -*-
"""第二十章插图：动机迁移、三种传播方式的时间尺度。"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def motive_shift():
    """三个阶段：求名、求财、地缘，中间用箭头表示迁移。"""
    fig, ax = setup(5.3, 3.15)
    stages = [
        ("2000－2005", "求名与破坏", "用别人没见过的\n手法证明自己能做",
         "ILOVEYOU\nCode Red\nSlammer", PALE),
        ("2006－2012", "求财", "把被控机器当资源\n按小时出租",
         "僵尸网络\nConficker\nZeus", PALE_BLUE),
        ("2010－2014", "地缘与威慑", "长期潜伏，目标\n由买家指定",
         "Stuxnet\nFlame\nShamoon", PALE_WARN),
    ]
    w, h, y0 = 27.0, 50.0, 6.0
    xs = [1.5, 36.5, 71.5]
    for (years, motive, note, cases, fc), x in zip(stages, xs):
        box(ax, x, y0, w, h, fc=fc, ec=LINE)
        label(ax, x + w / 2, y0 + h - 5.0, years, fs=7.0, color=GREY)
        label(ax, x + w / 2, y0 + h - 13.0, motive, fs=9.6, color=ACCENT,
              weight="bold")
        label(ax, x + w / 2, y0 + h - 24.0, note, fs=6.8, color=SOFT)
        ax.plot([x + 4.0, x + w - 4.0], [y0 + 20.0, y0 + 20.0], color=LINE,
                lw=0.7, zorder=3)
        label(ax, x + w / 2, y0 + 12.0, cases, fs=6.8, color=INK)

    for xa, xb, tag in ((28.5, 36.5, "变现"), (63.5, 71.5, "升级")):
        arrow(ax, (xa + 0.4, y0 + h / 2), (xb - 0.4, y0 + h / 2),
              color=ACCENT_2, lw=1.1, ms=7)
        label(ax, (xa + xb) / 2, y0 + h / 2 + 3.6, tag, fs=6.4, color=GREY)

    label(ax, 50.0, 1.8, "同一套技术，三种目的，越往右需要的资源越多",
          fs=7.0, color=GREY)
    return save(fig, "20", "motive-shift.png")


def propagation_speed():
    """三条传播方式的对数量级对比，柱长只表示量级。"""
    fig, ax = setup(5.3, 2.95)
    x0, x1 = 30.0, 92.0
    ymax_log = 4.0
    scale = (x1 - x0) / ymax_log

    def pos(minutes):
        return x0 + math.log10(minutes) * scale

    rows = [
        ("邮件附件", "ILOVEYOU 2000", 1440, "一天，全球范围", PALE),
        ("扫漏洞的蠕虫", "Code Red 2001", 840, "14 小时，约 35.9 万台", PALE_2),
        ("单包 UDP 蠕虫", "Slammer 2003", 10, "10 分钟，约 7.5 万台", PALE_WARN),
    ]
    ys = [49.0, 36.0, 23.0]
    bh = 6.4
    for (kind, name, minutes, value, fc), y in zip(rows, ys):
        label(ax, 27.5, y + 1.9, kind, fs=7.2, color=INK, ha="right",
              weight="bold")
        label(ax, 27.5, y - 1.9, name, fs=6.6, color=GREY, ha="right")
        right = pos(minutes)
        rect(ax, x0, y - bh / 2, right - x0, bh, fc=fc, ec="#c9c6bd", lw=0.8,
             zorder=2)
        if right - x0 > 34.0:
            label(ax, right - 2.0, y, value, fs=6.6, color=SOFT, ha="right")
        else:
            label(ax, right + 2.0, y, value, fs=6.6, color=SOFT, ha="left")

    ax.plot([x0, x1 + 2.6], [12.0, 12.0], color=SOFT, lw=0.9, zorder=3)
    ticks = [(1, "1 分钟"), (60, "1 小时"), (1440, "1 天"), (10000, "约 7 天")]
    for m, text in ticks:
        x = pos(m)
        ax.plot([x, x], [11.2, 12.8], color=SOFT, lw=0.9, zorder=3)
        label(ax, x, 8.2, text, fs=6.5, color=GREY)

    label(ax, 61.0, 3.0, "达到规模所需的时间，横轴按对数划分", fs=6.6,
          color=GREY)
    return save(fig, "20", "propagation-speed.png")


if __name__ == "__main__":
    motive_shift()
    propagation_speed()
