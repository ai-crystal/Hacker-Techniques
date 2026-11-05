# -*- coding: utf-8 -*-
"""第三章插图：权限位、setuid 程序的权限变化。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                    PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label, rect,
                    save, setup)


def permission_bits():
    fig, ax = setup(5.3, 2.9)
    chars = ["-", "r", "w", "-", "r", "-", "-", "r", "-", "-"]
    w, gap = 7.2, 1.2
    x0 = 12.0
    for i, c in enumerate(chars):
        x = x0 + i * (w + gap)
        fc = "#dfe7e6" if c != "-" else "white"
        box(ax, x, 34.0, w, 11.0, fc=fc, ec=LINE)
        label(ax, x + w / 2, 39.5, c, fs=11, color=ACCENT if c != "-" else "#a9a9a4")

    groups = [("所有者", 0, 3), ("同组用户", 3, 6), ("其他人", 6, 9)]
    for name, a, b in groups:
        xa = x0 + a * (w + gap) + 0.4
        xb = x0 + (b - 1) * (w + gap) + w - 0.4
        ax.plot([xa, xb], [31.0, 31.0], color=SOFT, lw=0.9)
        ax.plot([xa, xa], [31.0, 28.6], color=SOFT, lw=0.9)
        ax.plot([xb, xb], [31.0, 28.6], color=SOFT, lw=0.9)
        label(ax, (xa + xb) / 2, 25.2, name, fs=7.6, color=SOFT)

    # 文件类型说明
    label(ax, x0 + w / 2, 21.0, "文件类型", fs=6.6, color=GREY)
    ax.plot([x0 + w / 2, x0 + w / 2], [32.4, 22.6], color=GREY, lw=0.7,
            ls=(0, (2, 2)))

    label(ax, 12.0, 12.5, "- 普通文件　　d 目录　　l 符号链接　　　r 读　　w 写　　x 执行",
          fs=7.2, color=GREY, ha="left")
    label(ax, 12.0, 6.0, "对目录而言，x 表示可以进入，r 表示可以列出内容",
          fs=7.2, color=ACCENT, ha="left")
    return save(fig, "03", "permission-bits.png")


def setuid_flow():
    fig, ax = setup(5.3, 2.4)
    y, h = 20.0, 18.0
    steps = [
        ("alice 执行 passwd", 2.0, 24.0, PALE, "有效用户 1000"),
        ("进程启动", 30.0, 20.0, PALE_WARN, "有效用户变成 0"),
        ("写 /etc/shadow", 54.0, 22.0, PALE_BLUE, "只有 root 能写"),
        ("进程退出", 80.0, 18.0, PALE_2, "回到 1000"),
    ]
    for name, x, w, fc, note in steps:
        box(ax, x, y, w, h, fc=fc, ec=LINE)
        label(ax, x + w / 2, y + h - 6.0, name, fs=8.0, color=INK, weight="bold")
        label(ax, x + w / 2, y + 5.6, note, fs=6.8, color=GREY)
    for x1, x2 in [(26.4, 29.6), (50.4, 53.6), (76.4, 79.6)]:
        arrow(ax, (x1, y + h / 2), (x2, y + h / 2))
    label(ax, 50.0, 12.0, "s 位让进程临时拥有文件所有者的身份", fs=7.4, color=ACCENT)
    label(ax, 50.0, 5.6, "程序必须自己限制住这份权力能做的事", fs=7.2, color=WARN)
    return save(fig, "03", "setuid-flow.png")


if __name__ == "__main__":
    permission_bits()
    setuid_flow()
