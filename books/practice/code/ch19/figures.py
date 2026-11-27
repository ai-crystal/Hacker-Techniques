# -*- coding: utf-8 -*-
"""第十九章插图：WPA2 四次握手、无线到内网的路径。

画布宽度统一取 5.3 英寸，与版心宽度接近，图内不写标题。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def four_way_handshake():
    """四帧 EAPOL-Key 的往返，以及两处 nonce 的来源。"""
    fig, ax = setup(5.3, 3.5)

    x_sta, x_ap = 13.0, 87.0
    ax.plot([x_sta, x_sta], [11.0, 56.0], color=LINE, lw=0.9, zorder=1)
    ax.plot([x_ap, x_ap], [11.0, 56.0], color=LINE, lw=0.9, zorder=1)

    label(ax, x_sta, 58.0, "终端（STA）", fs=7.2, color=INK, weight="bold")
    label(ax, x_ap, 58.0, "AP（自有热点）", fs=7.2, color=INK, weight="bold")

    msgs = [
        (50.0, "AP", "①  ANonce，无 MIC", "AP 生成随机数，先递过去"),
        (38.0, "STA", "②  SNonce + MIC", "终端算 PTK，回一个随机数并自证"),
        (26.0, "AP", "③  GTK + MIC + 安装", "AP 也装 PTK，顺带下发组密钥"),
        (15.0, "STA", "④  MIC，开始加密", "不带密钥信息，只作确认"),
    ]

    for y, src, title, note in msgs:
        if src == "AP":
            arrow(ax, (x_ap - 0.6, y), (x_sta + 0.6, y), color=ACCENT, lw=1.1,
                  ms=7.5)
        else:
            arrow(ax, (x_sta + 0.6, y), (x_ap - 0.6, y), color=ACCENT_2,
                  lw=1.1, ms=7.5)
        label(ax, 50.0, y + 2.5, title, fs=7.2, color=INK)
        label(ax, 50.0, y - 2.6, note, fs=6.2, color=GREY)

    box(ax, 6.0, 0.6, 88.0, 9.6, fc=PALE_2, ec=LINE, lw=0.8)
    label(ax, 50.0, 5.4,
          "PMK = PBKDF2(HMAC-SHA1, 口令, SSID, 4096)\n"
          "PTK = PRF(PMK, ANonce, SNonce, 两端 MAC)",
          fs=6.2, color=SOFT)

    return save(fig, "19", "fourway-handshake.png")


def wireless_to_lan():
    """同一条无线链路，两个 SSID 落到两个 VLAN。"""
    fig, ax = setup(5.3, 3.5)

    box(ax, 1.5, 22.0, 17.0, 15.0, fc=PALE, ec=LINE, lw=0.9)
    label(ax, 10.0, 33.4, "终端", fs=7.4, color=INK, weight="bold")
    label(ax, 10.0, 29.4, "802.1X 客户端", fs=6.2, color=SOFT)
    label(ax, 10.0, 25.4, "证书 / 账号", fs=6.2, color=SOFT)

    box(ax, 27.0, 18.0, 18.0, 23.0, fc=PALE, ec=LINE, lw=0.9)
    label(ax, 36.0, 37.4, "AP", fs=7.4, color=INK, weight="bold")
    label(ax, 36.0, 33.4, "员工 SSID", fs=6.2, color=SOFT)
    label(ax, 36.0, 30.0, "访客 SSID", fs=6.2, color=SOFT)
    label(ax, 36.0, 24.0, "同一台设备", fs=6.0, color=GREY)
    label(ax, 36.0, 20.6, "两张逻辑网", fs=6.0, color=GREY)

    arrow(ax, (18.9, 29.5), (26.4, 29.5), color=ACCENT_2, lw=1.0, ms=7,
          ls=(0, (3.0, 2.2)))
    label(ax, 22.6, 27.0, "无线", fs=6.0, color=GREY)

    box(ax, 51.0, 16.0, 18.0, 27.0, fc=PALE_BLUE, ec="#bdc9d6", lw=0.9)
    label(ax, 60.0, 39.4, "二层交换机", fs=7.4, color=BLUE, weight="bold")
    label(ax, 60.0, 34.4, "VLAN 20", fs=6.4, color=SOFT)
    label(ax, 60.0, 31.2, "VLAN 99", fs=6.4, color=SOFT)
    label(ax, 60.0, 25.6, "端口隔离", fs=6.2, color=GREY)
    label(ax, 60.0, 22.4, "ARP 检查", fs=6.2, color=GREY)
    label(ax, 60.0, 19.2, "DHCP 嗅探", fs=6.2, color=GREY)

    arrow(ax, (45.4, 30.0), (50.4, 30.0), color=ACCENT, lw=1.0, ms=7)

    box(ax, 74.0, 34.0, 24.5, 11.0, fc=PALE_WARN, ec="#ddc4b8", lw=0.9)
    label(ax, 86.2, 41.4, "VLAN 20　办公网", fs=6.8, color=WARN, weight="bold")
    label(ax, 86.2, 37.2, "域控、文件服务器", fs=6.0, color=SOFT)

    box(ax, 74.0, 17.0, 24.5, 11.0, fc=PALE, ec=LINE, lw=0.9)
    label(ax, 86.2, 24.4, "VLAN 99　访客", fs=6.8, color=SOFT, weight="bold")
    label(ax, 86.2, 20.2, "只放行出网", fs=6.0, color=GREY)

    arrow(ax, (69.4, 39.0), (73.4, 39.0), color=WARN, lw=1.0, ms=7)
    arrow(ax, (69.4, 23.0), (73.4, 23.0), color=GREY, lw=1.0, ms=7)

    box(ax, 27.0, 48.0, 18.0, 11.0, fc=PALE_2, ec=LINE, lw=0.9)
    label(ax, 36.0, 55.4, "RADIUS", fs=6.8, color=SOFT, weight="bold")
    label(ax, 36.0, 51.2, "校验证书", fs=6.0, color=GREY)

    arrow(ax, (36.0, 41.4), (36.0, 47.6), color=ACCENT, lw=1.0, ms=7)
    label(ax, 37.8, 44.4, "802.1X", fs=6.0, color=GREY, ha="left")

    label(ax, 50.0, 6.5, "接入哪个 SSID，决定落在哪个 VLAN", fs=6.6,
          color=INK)
    return save(fig, "19", "wireless-to-lan.png")


if __name__ == "__main__":
    four_way_handshake()
    wireless_to_lan()
