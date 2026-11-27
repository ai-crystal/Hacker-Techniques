# -*- coding: utf-8 -*-
"""第十八章插图：happens-before 关系、无锁栈的 ABA。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def happens_before():
    fig, ax = setup(5.3, 3.0)
    lx, rx = 22.0, 72.0
    ax.plot([lx, lx], [10.0, 52.0], color="#c8c8c2", lw=1.0)
    ax.plot([rx, rx], [10.0, 52.0], color="#c8c8c2", lw=1.0)
    label(ax, lx, 55.0, "线程 1", fs=7.6, color=INK, weight="bold")
    label(ax, rx, 55.0, "线程 2", fs=7.6, color=INK, weight="bold")

    box(ax, 8.0, 44.0, 28.0, 6.0, fc=PALE, ec=LINE, lw=0.7)
    label(ax, 22.0, 47.0, "写 x = 1", fs=6.2, color=INK)
    box(ax, 8.0, 34.0, 28.0, 6.0, fc=PALE_WARN, ec="#e2ccc0", lw=0.7)
    label(ax, 22.0, 37.0, "store release flag", fs=6.2, color=WARN)

    box(ax, 58.0, 34.0, 28.0, 6.0, fc=PALE_WARN, ec="#e2ccc0", lw=0.7)
    label(ax, 72.0, 37.0, "load acquire flag", fs=6.2, color=WARN)
    box(ax, 58.0, 24.0, 28.0, 6.0, fc="#f0e2e2", ec="#dcc0c0", lw=0.7)
    label(ax, 72.0, 27.0, "读 x（与左侧写 x 竞争）", fs=5.8, color=WARN)

    arrow(ax, (36.4, 37.0), (57.4, 37.0), color=ACCENT, lw=1.0)
    label(ax, 47.0, 39.0, "synchronizes-with", fs=6.0, color=ACCENT)

    ax.plot([22.0, 22.0], [43.4, 40.6], color=GREY, lw=0.8)
    ax.plot([72.0, 72.0], [33.4, 30.6], color=GREY, lw=0.8)
    label(ax, 50.0, 5.0, "竖线内是程序顺序，横线建立跨线程的可见性；没有连线的访问就是数据竞争",
          fs=6.4, color=SOFT)
    return save(fig, "18", "happens-before.png")


def aba():
    fig, ax = setup(5.3, 2.9)
    stages = [("初始", "A → B → C", 3.0),
              ("线程 1 读到 A、B 后挂起", "A → B → C", 27.0),
              ("线程 0 弹出 A、B，释放 B，压回 A", "A → C", 51.0),
              ("线程 1 的 CAS 成功", "B → C（已释放）", 75.0)]
    for title, stack, x in stages:
        box(ax, x, 34.0, 21.0, 12.0, fc=PALE, ec=LINE, lw=0.8)
        label(ax, x + 10.5, 42.0, title, fs=5.8, color=SOFT)
        label(ax, x + 10.5, 37.0, stack, fs=6.6, color=INK, weight="bold")

    for x in (24.4, 48.4, 72.4):
        arrow(ax, (x, 40.0), (x + 2.6, 40.0), color=ACCENT, lw=0.9, ms=6)

    label(ax, 50.0, 26.0, "栈顶地址没变，CAS 认为没人动过，于是把已经释放的 B 装了回去",
          fs=6.6, color=WARN)
    label(ax, 50.0, 18.0, "防护：带版本号的指针（双字 CAS）、危险指针、纪元回收", fs=6.4,
          color=SOFT)
    return save(fig, "18", "aba.png")


if __name__ == "__main__":
    happens_before()
    aba()
