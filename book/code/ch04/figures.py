# -*- coding: utf-8 -*-
"""第四章插图：协议封装与 TCP 连接建立。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                    PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label, rect,
                    save, setup)


def encapsulation():
    fig, ax = setup(5.3, 3.3)
    rows = [
        ("链路层", 6.0, [("以太网头", 16.0, 13.0, PALE_WARN), ("IP 头", 29.0, 11.0, PALE_BLUE),
                     ("TCP 头", 40.0, 9.0, PALE_2), ("应用数据", 49.0, 41.0, PALE),
                     ("FCS", 90.0, 5.0, PALE_WARN)]),
        ("网络层", 18.0, [("IP 头", 29.0, 11.0, PALE_BLUE), ("TCP 头", 40.0, 9.0, PALE_2),
                      ("应用数据", 49.0, 41.0, PALE)]),
        ("传输层", 30.0, [("TCP 头", 40.0, 9.0, PALE_2), ("应用数据", 49.0, 41.0, PALE)]),
        ("应用层", 42.0, [("应用数据", 49.0, 41.0, PALE)]),
    ]
    for name, y, parts in rows:
        label(ax, 14.0, y + 5.0, name, fs=7.6, color=SOFT, ha="right")
        for text, x, w, fc in parts:
            box(ax, x, y, w, 10.0, fc=fc, ec=LINE)
            label(ax, x + w / 2, y + 5.0, text, fs=6.9, color=SOFT)
    label(ax, 53.0, 60.0, "每往下一层，就在前面加一个头部", fs=7.6, color=ACCENT, ha="left")
    return save(fig, "04", "encapsulation.png")


def tcp_handshake():
    fig, ax = setup(5.3, 3.7)
    lx, rx = 20.0, 80.0
    ax.plot([lx, lx], [2.0, 66.0], color="#c8c8c2", lw=1.0)
    ax.plot([rx, rx], [2.0, 66.0], color="#c8c8c2", lw=1.0)
    label(ax, lx, 69.0, "客户端", fs=8.2, color=INK, weight="bold")
    label(ax, rx, 69.0, "服务端", fs=8.2, color=INK, weight="bold")

    hs = [(58.0, lx + 1.0, rx - 1.0, "SYN　seq=x", ACCENT),
          (49.0, rx - 1.0, lx + 1.0, "SYN + ACK　seq=y, ack=x+1", ACCENT),
          (40.0, lx + 1.0, rx - 1.0, "ACK　ack=y+1", ACCENT)]
    for y, x1, x2, text, color in hs:
        arrow(ax, (x1, y), (x2, y), color=color, lw=1.2)
        label(ax, (lx + rx) / 2, y + 2.2, text, fs=7.0, color=color)

    label(ax, (lx + rx) / 2, 33.0, "连接建立，双方开始传输数据", fs=7.2, color=GREY)
    ax.plot([12.0, 88.0], [29.0, 29.0], color="#dcdcd6", lw=0.8, ls=(0, (3, 3)))

    cl = [(23.0, lx + 1.0, rx - 1.0, "FIN", WARN),
          (17.0, rx - 1.0, lx + 1.0, "ACK", GREY),
          (11.0, rx - 1.0, lx + 1.0, "FIN", WARN),
          (5.0, lx + 1.0, rx - 1.0, "ACK", GREY)]
    for y, x1, x2, text, color in cl:
        arrow(ax, (x1, y), (x2, y), color=color, lw=1.1)
        label(ax, (lx + rx) / 2, y + 1.9, text, fs=6.8, color=color)
    label(ax, 82.0, 14.0, "四次挥手", fs=6.8, color=GREY, ha="left")
    return save(fig, "04", "tcp-handshake.png")


if __name__ == "__main__":
    encapsulation()
    tcp_handshake()
