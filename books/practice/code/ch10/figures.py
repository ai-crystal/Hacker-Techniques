# -*- coding: utf-8 -*-
"""第十章插图：提权链路的阶段、内核日志关键行的解读。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def priv_flow():
    fig, ax = setup(5.3, 3.3)

    stages = [
        ("一个低权限的本地 shell", "id · 能不能执行命令", PALE, INK),
        ("内核版本落在公告区间", "uname -r · 发行版 changelog", PALE_2, INK),
        ("配置与防护允许触发", "USER_NS · SMEP/SMAP · dmesg_restrict", PALE_2, INK),
        ("触发一次，看结果", "dmesg 里有没有新行", PALE_2, INK),
        ("拿到 root", "停在这里，不做持久化", PALE_WARN, WARN),
    ]

    x, w = 3.0, 38.0
    cx = x + w / 2
    h, gap = 7.0, 5.0
    top = 57.0

    for i, (name, note, fc, color) in enumerate(stages):
        y = top - (h + gap) * i
        ec = LINE if fc != PALE_WARN else "#d8b6a6"
        box(ax, x, y - h, w, h, fc=fc, ec=ec)
        label(ax, cx, y - h / 2, name, fs=7.6, color=color, weight="bold")
        label(ax, x + w + 4.6, y - h / 2, note, fs=6.2, color=SOFT, ha="left")
        if i:
            arrow(ax, (cx, y + gap - 0.2), (cx, y + 0.2))

    return save(fig, "10", "priv-flow.png")


def klog_lines():
    fig, ax = setup(5.3, 3.6)

    rows = [
        ("BUG: unable to handle page fault for address: 0000deadbeef",
         "地址不合法，先怀疑自己算出来的指针"),
        ("#PF: supervisor write access in kernel mode",
         "内核态在写，出现 user 字样时先想到 SMAP"),
        ("RIP: 0010:do_ioctl+0x2a/0x60",
         "崩在 do_ioctl 偏移 0x2a 处，用 vmlinux 定位"),
        ("CR4: 0x00000000003506e0",
         "第 20 位 SMEP，第 21 位 SMAP，置位就是开着"),
        ("Kernel Offset: 0x1a000000",
         "KASLR 偏移，有它才能把符号算回真实地址"),
    ]

    y0, step, h = 58.0, 12.5, 6.6
    for i, (line, note) in enumerate(rows):
        y = y0 - step * i
        box(ax, 2.0, y, 96.0, h, fc=PALE_2, ec=LINE, lw=0.8, radius=0.5)
        label(ax, 5.0, y + h / 2, line, fs=5.6, color=INK, ha="left",
              family="monospace")
        label(ax, 6.0, y - 2.6, note, fs=6.0, color=SOFT, ha="left")

    return save(fig, "10", "klog-lines.png")


if __name__ == "__main__":
    priv_flow()
    klog_lines()
