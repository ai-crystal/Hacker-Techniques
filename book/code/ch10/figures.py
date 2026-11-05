# -*- coding: utf-8 -*-
"""第十章插图：ARP 欺骗、TLS 握手、Heartbleed 越界读。

画布宽度统一取 5.3 英寸，与版心宽度接近。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                    PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label, rect,
                    save, setup)


def arp_spoof():
    fig, ax = setup(5.3, 3.2)

    # 上半：正常路径
    label(ax, 2.0, 56.0, "欺骗前", fs=8.6, color=GREY, ha="left", weight="bold")
    box(ax, 4.0, 38.0, 24.0, 12.0, fc=PALE, ec=LINE)
    label(ax, 16.0, 46.4, "受害者", fs=8.4, color=INK, weight="bold")
    label(ax, 16.0, 41.8, "192.168.1.20", fs=6.8, color=GREY)
    box(ax, 56.0, 38.0, 24.0, 12.0, fc=PALE, ec=LINE)
    label(ax, 68.0, 46.4, "网关", fs=8.4, color=INK, weight="bold")
    label(ax, 68.0, 41.8, "192.168.1.1", fs=6.8, color=GREY)
    arrow(ax, (28.4, 44.0), (55.6, 44.0))
    label(ax, 42.0, 47.0, "目的 MAC 是网关", fs=6.9, color=ACCENT)
    arrow(ax, (80.4, 44.0), (94.0, 44.0), color=ACCENT_2)
    label(ax, 87.0, 47.0, "外网", fs=6.9, color=ACCENT_2)

    # 下半：欺骗之后
    label(ax, 2.0, 30.0, "欺骗后", fs=8.6, color=GREY, ha="left", weight="bold")
    box(ax, 2.0, 12.0, 22.0, 12.0, fc=PALE, ec=LINE)
    label(ax, 13.0, 20.2, "受害者", fs=8.0, color=INK, weight="bold")
    label(ax, 13.0, 15.8, "192.168.1.20", fs=6.4, color=GREY)
    box(ax, 32.0, 12.0, 24.0, 12.0, fc=PALE_WARN, ec=WARN)
    label(ax, 44.0, 20.2, "攻击者", fs=8.0, color=WARN, weight="bold")
    label(ax, 44.0, 15.8, "开启 IP 转发", fs=6.6, color=WARN)
    box(ax, 66.0, 12.0, 24.0, 12.0, fc=PALE, ec=LINE)
    label(ax, 78.0, 20.2, "网关", fs=8.0, color=INK, weight="bold")
    label(ax, 78.0, 15.8, "192.168.1.1", fs=6.4, color=GREY)

    arrow(ax, (24.4, 18.0), (31.6, 18.0), color=WARN)
    label(ax, 28.0, 20.8, "改道", fs=6.4, color=WARN)
    arrow(ax, (56.4, 18.0), (65.6, 18.0), color=WARN)
    label(ax, 61.0, 20.8, "原样转发", fs=6.4, color=WARN)

    # 伪造应答：从攻击者底部绕回受害者底部
    ax.plot([44.0, 44.0, 13.0], [11.6, 6.0, 6.0], color=WARN, lw=1.0,
            ls=(0, (4, 2.4)), zorder=3)
    arrow(ax, (13.0, 6.0), (13.0, 11.6), color=WARN, lw=1.0,
          ls=(0, (4, 2.4)))
    label(ax, 28.0, 3.0, "伪造的 ARP 应答", fs=6.9, color=WARN)

    return save(fig, "10", "arp-spoof.png")


def tls_handshake():
    fig, ax = setup(5.3, 3.3)

    box(ax, 6.0, 52.0, 26.0, 9.0, fc=PALE_BLUE, ec=LINE)
    label(ax, 19.0, 56.5, "客户端", fs=8.8, color=BLUE, weight="bold")
    box(ax, 68.0, 52.0, 26.0, 9.0, fc=PALE, ec=LINE)
    label(ax, 81.0, 56.5, "服务器", fs=8.8, color=INK, weight="bold")

    for x in (19.0, 81.0):
        ax.plot([x, x], [51.4, 15.0], color=LINE, lw=0.9,
                ls=(0, (3, 2.6)), zorder=1)

    arrow(ax, (19.0, 46.0), (81.0, 46.0))
    label(ax, 50.0, 48.9, "ClientHello　随机数、密码套件、DH 份额",
          fs=7.0, color=ACCENT)
    arrow(ax, (81.0, 36.5), (19.0, 36.5))
    label(ax, 50.0, 39.4, "ServerHello　证书链　握手签名　Finished",
          fs=7.0, color=ACCENT)
    arrow(ax, (19.0, 27.0), (81.0, 27.0))
    label(ax, 50.0, 29.9, "Finished　握手校验值", fs=7.0, color=ACCENT)

    rect(ax, 0, 1.5, 100, 10.5, fc=PALE_2)
    label(ax, 4.0, 9.2, "证书校验　域名匹配、在有效期内、签名链走到受信任的根",
          fs=6.9, color=SOFT, ha="left")
    label(ax, 4.0, 4.4, "之后的数据用会话密钥做对称加密，非对称只在握手里用一次",
          fs=6.9, color=SOFT, ha="left")

    return save(fig, "10", "tls-handshake.png")


def heartbleed():
    fig, ax = setup(5.3, 2.75)

    label(ax, 3.0, 49.0, "客户端发出的心跳请求", fs=7.4, color=GREY, ha="left")
    box(ax, 3.0, 36.0, 16.0, 10.0, fc=PALE, ec=LINE)
    label(ax, 11.0, 41.0, "类型 1", fs=7.2, color=SOFT)
    box(ax, 21.0, 36.0, 22.0, 10.0, fc=PALE_WARN, ec=WARN)
    label(ax, 32.0, 41.0, "长度 65535", fs=7.2, color=WARN, weight="bold")
    box(ax, 45.0, 36.0, 14.0, 10.0, fc=PALE_BLUE, ec=LINE)
    label(ax, 52.0, 41.0, "1 字节", fs=7.2, color=BLUE)
    label(ax, 63.0, 41.0, "声称 65535，实际只发了 1", fs=7.0, color=WARN,
          ha="left")

    arrow(ax, (3.0, 30.0), (95.0, 30.0), color=WARN, lw=1.0, style="<|-|>",
          ms=7)
    label(ax, 49.0, 33.0, "回送多少，由长度字段决定", fs=7.0, color=WARN)

    label(ax, 95.0, 25.0, "示意图，段长不代表真实比例", fs=6.2, color=GREY,
          ha="right")
    box(ax, 3.0, 12.0, 10.0, 10.0, fc=PALE_BLUE, ec=LINE)
    label(ax, 8.0, 17.0, "1 B", fs=6.8, color=BLUE)
    box(ax, 13.0, 12.0, 16.0, 10.0, fc=PALE_WARN, ec=LINE)
    label(ax, 21.0, 17.0, "私钥", fs=7.2, color=SOFT)
    box(ax, 29.0, 12.0, 17.0, 10.0, fc=PALE_WARN, ec=LINE)
    label(ax, 37.5, 17.0, "会话密钥", fs=7.2, color=SOFT)
    box(ax, 46.0, 12.0, 19.0, 10.0, fc=PALE_WARN, ec=LINE)
    label(ax, 55.5, 17.0, "别人的口令", fs=7.2, color=SOFT)
    box(ax, 65.0, 12.0, 30.0, 10.0, fc=PALE, ec=LINE)
    label(ax, 80.0, 17.0, "……", fs=7.2, color=GREY)

    label(ax, 3.0, 9.0, "服务器进程内存", fs=7.0, color=GREY, ha="left")
    label(ax, 95.0, 9.0, "越界读到的内容原样发回客户端", fs=7.0, color=WARN,
          ha="right")

    return save(fig, "10", "heartbleed.png")


if __name__ == "__main__":
    arp_spoof()
    tls_handshake()
    heartbleed()
