# -*- coding: utf-8 -*-
"""第十章插图：TLS 1.3 握手、QUIC 连接迁移。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def tls13_handshake():
    fig, ax = setup(5.3, 3.4)
    lx, rx = 16.0, 84.0
    ax.plot([lx, lx], [6.0, 54.0], color="#c8c8c2", lw=1.0)
    ax.plot([rx, rx], [6.0, 54.0], color="#c8c8c2", lw=1.0)
    label(ax, lx, 57.0, "客户端", fs=8.4, color=INK, weight="bold")
    label(ax, rx, 57.0, "服务端", fs=8.4, color=INK, weight="bold")

    msgs = [(48.0, lx, rx, "ClientHello + key_share", ACCENT, 1),
            (41.0, rx, lx, "ServerHello + key_share", ACCENT, 2),
            (34.0, rx, lx, "EncryptedExtensions / Certificate / Finished", ACCENT_2, 3),
            (27.0, lx, rx, "Finished", ACCENT_2, 3)]
    for y, x1, x2, text, color, phase in msgs:
        arrow(ax, (x1 + (1 if x1 == lx else -1), y), (x2 - (1 if x2 == rx else -1), y),
              color=color, lw=1.1)
        label(ax, (lx + rx) / 2, y + 2.0, text, fs=6.4, color=color)

    rect(ax, 4.0, 43.5, 8.0, 9.0, fc=PALE_BLUE, ec="none")
    label(ax, 8.0, 48.0, "握手\n密钥", fs=6.2, color=BLUE)
    rect(ax, 4.0, 25.0, 8.0, 12.0, fc=PALE, ec="none")
    label(ax, 8.0, 31.0, "应用\n数据\n密钥", fs=6.2, color=ACCENT)
    label(ax, 50.0, 18.0, "第 1 次往返结束时双方都握有应用数据密钥", fs=7.0, color=SOFT)
    label(ax, 50.0, 11.0, "证书在第 3 条消息里，与握手认证一起被加密", fs=6.8, color=GREY)
    return save(fig, "10", "tls13-handshake.png")


def quic_migration():
    fig, ax = setup(5.3, 2.8)
    box(ax, 4.0, 36.0, 24.0, 12.0, fc=PALE, ec=LINE)
    label(ax, 16.0, 42.5, "手机（Wi-Fi）", fs=7.6, color=INK, weight="bold")
    label(ax, 16.0, 39.0, "203.0.113.7", fs=6.4, color=GREY)
    box(ax, 72.0, 36.0, 24.0, 12.0, fc=PALE_BLUE, ec=LINE)
    label(ax, 84.0, 42.5, "服务端", fs=7.6, color=INK, weight="bold")
    label(ax, 84.0, 39.0, "Connection ID: 7f3a", fs=6.4, color=GREY)

    arrow(ax, (28.4, 44.0), (71.6, 44.0), color=ACCENT, lw=1.1)
    label(ax, 50.0, 46.2, "数据流（Connection ID 不变）", fs=6.6, color=ACCENT)

    box(ax, 4.0, 16.0, 24.0, 12.0, fc=PALE_WARN, ec="#e2ccc0")
    label(ax, 16.0, 22.5, "手机（蜂窝）", fs=7.6, color=INK, weight="bold")
    label(ax, 16.0, 19.0, "198.51.100.24", fs=6.4, color=GREY)
    arrow(ax, (28.4, 24.0), (71.6, 24.0), color=WARN, lw=1.1, ls=(0, (4, 2.5)))
    label(ax, 50.0, 26.2, "换网后继续原连接", fs=6.6, color=WARN)

    ax.plot([50.0, 50.0], [34.0, 28.0], color="#d0d0ca", lw=0.9, ls=(0, (3, 3)))
    label(ax, 50.0, 8.0, "地址变了，连接没有断，靠的是连接标识而不是四元组", fs=7.0, color=SOFT)
    return save(fig, "10", "quic-migration.png")


if __name__ == "__main__":
    tls13_handshake()
    quic_migration()
