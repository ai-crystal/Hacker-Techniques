# -*- coding: utf-8 -*-
"""第七章插图：ret2libc 栈布局、ROP 链、推测执行的时间差。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                    PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label, rect,
                    save, setup)


def nx_ret2libc():
    fig, ax = setup(5.3, 3.5)
    slots = [
        ("system 的地址", 54.0, 8.0, PALE_WARN, "ret 最终弹到这里"),
        ("\"/bin/sh\" 的地址", 44.0, 8.0, PALE_BLUE, "被 gadget 弹进 rdi"),
        ("gadget 地址", 34.0, 8.0, PALE_2, "pop rdi; ret"),
        ("填充 24 字节", 17.0, 13.0, PALE, "走到返回地址为止"),
    ]
    for name, y, h, fc, note in slots:
        box(ax, 24.0, y, 30.0, h, fc=fc, ec=LINE)
        label(ax, 39.0, y + h / 2, name, fs=7.6, color=INK, weight="bold")
        label(ax, 56.0, y + h / 2, note, fs=6.6, color=GREY, ha="left")

    label(ax, 18.0, 56.0, "②", fs=9, color=ACCENT)
    label(ax, 18.0, 37.0, "①", fs=9, color=ACCENT)
    label(ax, 8.0, 46.0, "执行顺序", fs=6.4, color=GREY, rotation=90)

    label(ax, 39.0, 9.0, "栈不可执行，但 libc 一直是可执行的", fs=7.2, color=ACCENT)
    label(ax, 39.0, 3.2, "于是攻击者把返回地址指向已有的函数", fs=7.0, color=GREY)
    return save(fig, "07", "nx-ret2libc.png")


def rop_chain():
    fig, ax = setup(5.3, 3.0)
    gadgets = [(4.0, "pop rdi; ret"), (33.0, "pop rsi; ret"), (62.0, "syscall")]
    for x, name in gadgets:
        box(ax, x, 40.0, 26.0, 8.0, fc=PALE_2, ec=LINE)
        label(ax, x + 13.0, 44.0, name, fs=7.4, color=INK, weight="bold")

    arrow(ax, (30.6, 44.0), (32.4, 44.0), color=ACCENT, lw=1.0, ms=7)
    arrow(ax, (59.6, 44.0), (61.4, 44.0), color=ACCENT, lw=1.0, ms=7)

    slots = [(4.0, "gadget 1", PALE_WARN), (20.0, "参数 1", PALE),
             (36.0, "gadget 2", PALE_WARN), (52.0, "参数 2", PALE),
             (68.0, "gadget 3", PALE_WARN)]
    for x, name, fc in slots:
        box(ax, x, 22.0, 14.0, 9.0, fc=fc, ec=LINE)
        label(ax, x + 7.0, 26.5, name, fs=6.6, color=SOFT)
    label(ax, 8.0, 17.0, "栈上的布局", fs=6.8, color=GREY, ha="left")

    # 连接栈槽与 gadget
    ax.plot([11.0, 11.0], [31.4, 39.4], color=ACCENT_2, lw=0.8, ls=(0, (2, 2)))
    ax.plot([43.0, 43.0], [31.4, 39.4], color=ACCENT_2, lw=0.8, ls=(0, (2, 2)))
    ax.plot([75.0, 75.0], [31.4, 39.4], color=ACCENT_2, lw=0.8, ls=(0, (2, 2)))

    label(ax, 50.0, 11.0, "每个 gadget 执行完立刻 ret，跳到栈上的下一格", fs=7.2,
          color=ACCENT)
    label(ax, 50.0, 4.6, "全部指令都来自程序自身的可执行段", fs=7.0, color=GREY)
    return save(fig, "07", "rop-chain.png")


def spectre_timing():
    fig, ax = setup(5.3, 3.0)
    steps = [("推测执行", "越过边界读 array1", 2.0, 27.0, PALE),
             ("缓存被污染", "array2 的某一块留在缓存", 32.0, 30.0, PALE_BLUE),
             ("逐块测量", "访问时间最短的一块", 65.0, 33.0, PALE_WARN)]
    y, h = 42.0, 12.0
    for name, note, x, w, fc in steps:
        box(ax, x, y, w, h, fc=fc, ec=LINE)
        label(ax, x + w / 2, y + h - 4.6, name, fs=7.6, color=INK, weight="bold")
        label(ax, x + w / 2, y + 4.4, note, fs=6.5, color=GREY)
    arrow(ax, (29.4, y + h / 2), (31.6, y + h / 2), color=ACCENT, lw=1.0, ms=7)
    arrow(ax, (62.4, y + h / 2), (64.6, y + h / 2), color=ACCENT, lw=1.0, ms=7)

    label(ax, 8.0, 33.0, "时间", fs=6.8, color=GREY, ha="left")
    rect(ax, 8.0, 22.0, 34.0, 7.0, fc=PALE, ec="none")
    label(ax, 10.0, 25.5, "命中缓存", fs=6.6, color=ACCENT, ha="left")
    rect(ax, 8.0, 12.0, 76.0, 7.0, fc="#eeece6", ec="none")
    label(ax, 10.0, 15.5, "未命中", fs=6.6, color=GREY, ha="left")
    label(ax, 50.0, 4.6, "条的长度表示访问耗时，差值就是被偷出来的信息", fs=7.0,
          color=GREY)
    return save(fig, "07", "spectre-timing.png")


if __name__ == "__main__":
    nx_ret2libc()
    rop_chain()
    spectre_timing()
