# -*- coding: utf-8 -*-
"""第十九章插图：1969-1999 时间轴、早期病毒的三条传播路径。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def timeline():
    """竖排时间轴：年份在左，事件在右，单列九行。"""
    fig, ax = setup(5.3, 3.4)
    events = [
        ("1969", "ARPANET 连起四个节点"),
        ("1971", "Creeper 在机器间跳转，Reaper 追着删"),
        ("1983", "Cohen 演示自我复制，Adleman 命名 virus"),
        ("1986", "Brain 感染 PC 引导扇区"),
        ("1988", "Morris 蠕虫，约 6000 台机器"),
        ("1989", "AIDS Trojan 索要 189 美元"),
        ("1995", "Concept，第一个 Word 宏病毒"),
        ("1998", "CIH 覆盖 BIOS；Back Orifice 发布"),
        ("1999", "Melissa 借通讯录群发"),
    ]
    x_spine = 16.5
    ys = [52.0 - i * 5.9 for i in range(len(events))]

    ax.plot([x_spine, x_spine], [ys[-1] - 3.0, ys[0] + 3.4], color=LINE,
            lw=1.1, zorder=1, solid_capstyle="butt")
    arrow(ax, (x_spine, ys[0] + 8.0), (x_spine, ys[0] + 3.8), color=GREY,
          lw=1.0, ms=7)
    label(ax, x_spine + 0.4, ys[0] + 10.4, "时间", fs=6.8, color=GREY,
          ha="left")

    for (year, text), y in zip(events, ys):
        ax.plot([x_spine], [y], marker="o", markersize=4.2, color=ACCENT_2,
                zorder=4, markeredgewidth=0)
        label(ax, x_spine - 2.4, y, year, fs=8.0, color=ACCENT, ha="right",
              weight="bold")
        label(ax, x_spine + 3.2, y, text, fs=7.4, color=INK, ha="left")
    return save(fig, "19", "timeline-1969-1999.png")


def three_paths():
    """三条传播路径：载体、落点、代表样本。"""
    fig, ax = setup(5.3, 3.3)
    heads = [(2.0, 28.0, "载体"), (34.0, 32.0, "落点"), (70.0, 28.0, "代表")]
    for x, w, name in heads:
        label(ax, x + w / 2, 55.0, name, fs=8.0, color=SOFT, weight="bold")

    rows = [
        ("软盘拷贝", "引导扇区", "先于系统执行", "Brain，1986"),
        ("交换程序", "可执行文件", "用户双击才触发", "CIH，1998"),
        ("传阅文档", "文档里的宏", "打开文档就运行", "Concept 1995\nMelissa 1999"),
    ]
    ys = [38.0, 23.0, 8.0]
    h = 12.0
    for (src, dst, note, case), y in zip(rows, ys):
        box(ax, 2.0, y, 28.0, h, fc=PALE, ec=LINE)
        label(ax, 16.0, y + h / 2, src, fs=7.8, color=INK, weight="bold")

        box(ax, 34.0, y, 32.0, h, fc=PALE_WARN, ec="#e0c4b6")
        label(ax, 50.0, y + h / 2 + 1.9, dst, fs=7.8, color=WARN, weight="bold")
        label(ax, 50.0, y + h / 2 - 2.4, note, fs=6.7, color=SOFT)

        box(ax, 70.0, y, 28.0, h, fc=PALE_2, ec=LINE)
        label(ax, 84.0, y + h / 2, case, fs=6.9, color=SOFT)

        arrow(ax, (30.4, y + h / 2), (33.6, y + h / 2), color=ACCENT_2, lw=1.0,
              ms=7)
        arrow(ax, (66.4, y + h / 2), (69.6, y + h / 2), color=ACCENT_2, lw=1.0,
              ms=7)

    label(ax, 50.0, 2.2, "三条路径都要借一次用户的正常操作完成跨越",
          fs=7.0, color=GREY)
    return save(fig, "19", "three-paths.png")


if __name__ == "__main__":
    timeline()
    three_paths()
