# -*- coding: utf-8 -*-
"""第二章插图：TCP 连接时间线、探测工具选择。

画布宽度统一取 5.3 英寸，与版心宽度接近。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def tcp_timeline():
    fig, ax = setup(5.3, 3.0)

    cols = [
        (2, "正常建连", [("SYN", "out", "-"), ("SYN/ACK", "in", "-"),
                       ("ACK", "out", "-"), ("GET /", "out", "-"),
                       ("200 OK", "in", "-")],
         "三次握手之后才会有数据"),
        (35, "只发不收", [("SYN", "out", "-"), ("SYN 重传", "out", "--"),
                        ("SYN 重传", "out", "--"), ("SYN 重传", "out", "--")],
         "重传三次后放弃"),
        (68, "立刻被拒", [("SYN", "out", "-"), ("RST/ACK", "in", "-")],
         "端口没有进程监听"),
    ]

    for x0, title, steps, note in cols:
        xa, xb = x0 + 8, x0 + 24
        label(ax, x0 + 16, 51.8, title, fs=8.2, color=INK, weight="bold")
        ax.plot([xa, xa], [12, 48], color=LINE, lw=0.9, zorder=1)
        ax.plot([xb, xb], [12, 48], color=LINE, lw=0.9, zorder=1)
        y = 44
        for text, direction, ls in steps:
            if direction == "out":
                p1, p2 = (xa + 0.3, y), (xb - 0.3, y)
            else:
                p1, p2 = (xb - 0.3, y), (xa + 0.3, y)
            arrow(ax, p1, p2, color=ACCENT if direction == "out" else ACCENT_2,
                  lw=1.0, ls=ls, ms=7)
            label(ax, x0 + 16, y + 2.2, text, fs=7.2,
                  color=SOFT if direction == "out" else BLUE)
            y -= 7
        label(ax, x0 + 16, 7.2, note, fs=7.2, color=GREY)

    label(ax, 50, 2.0, "→ 客户端发出　　← 服务端发出", fs=7.4, color=INK)
    return save(fig, "02", "tcp-timeline.png")


def tool_choice():
    fig, ax = setup(5.3, 3.2)

    box(ax, 30, 50, 40, 7, fc=PALE, ec=LINE)
    label(ax, 50, 53.5, "先问清楚要回答什么", fs=8.0, color=INK, weight="bold")

    arrow(ax, (50, 49.8), (50, 47))
    ax.plot([13, 85], [47, 47], color=ACCENT, lw=1.0, zorder=3)

    items = [
        ("这台机器还活着吗", "nmap -sn\n--reason 看依据"),
        ("开了哪些端口", "-sS 需要 root\n-sT 不需要"),
        ("跑的是什么版本", "nmap -sV\n--version-all 更准"),
        ("包到底有没有到", "tcpdump 两端\n各抓一份再对"),
    ]
    for i, (q, tool) in enumerate(items):
        x = 2 + i * 24
        arrow(ax, (x + 11, 47), (x + 11, 43.2))
        box(ax, x, 34, 22, 9, fc=PALE_BLUE, ec="#b6c4d2")
        label(ax, x + 11, 38.5, q, fs=7.2, color=BLUE)
        box(ax, x, 18, 22, 11.5, fc=PALE_2, ec=LINE)
        label(ax, x + 11, 23.8, tool, fs=7.2, color=SOFT)
        arrow(ax, (x + 11, 33.8), (x + 11, 30))

    box(ax, 2, 5, 94, 8, fc=PALE_WARN, ec="#d8b6a6")
    label(ax, 50, 9, "结论要标依据，猜出来的不算结论", fs=7.6, color=WARN)
    return save(fig, "02", "tool-choice.png")


if __name__ == "__main__":
    tcp_timeline()
    tool_choice()
