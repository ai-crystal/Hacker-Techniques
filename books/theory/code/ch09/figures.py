# -*- coding: utf-8 -*-
"""第九章插图：AEAD 的分工、ECDH 与子密钥派生。

画布宽度统一 5.3 英寸。图内不写标题，标题由图注承担。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def aead_roles():
    """nonce/AAD/密文/tag 在 AEAD 里的分工。"""
    fig, ax = setup(5.3, 3.05)

    box(ax, 3.0, 40.0, 16.0, 9.5, fc=PALE_2, ec=LINE)
    label(ax, 11.0, 44.75, "明文 P", fs=8.6, color=INK, weight="bold")

    box(ax, 24.5, 38.0, 25.0, 13.5, fc=PALE_BLUE, ec="#b6c4d2")
    label(ax, 37.0, 47.6, "AES-CTR", fs=9.4, color=BLUE, weight="bold")
    label(ax, 37.0, 42.6, "按 nonce 生成密钥流", fs=6.6, color=GREY)

    box(ax, 54.0, 40.0, 16.0, 9.5, fc=PALE_2, ec=LINE)
    label(ax, 62.0, 44.75, "密文 C", fs=8.6, color=INK, weight="bold")

    box(ax, 79.0, 40.0, 18.0, 9.5, fc=PALE_WARN, ec="#dcb9a8")
    label(ax, 88.0, 46.4, "AAD", fs=8.6, color=WARN, weight="bold")
    label(ax, 88.0, 43.0, "头部、序号", fs=6.8, color=GREY)

    box(ax, 26.0, 24.0, 22.0, 8.5, fc=PALE, ec=LINE)
    label(ax, 37.0, 28.25, "密钥 K", fs=8.4, color=INK)

    box(ax, 79.0, 18.0, 18.0, 10.5, fc=PALE_BLUE, ec="#b6c4d2")
    label(ax, 88.0, 25.4, "GHASH", fs=9.0, color=BLUE, weight="bold")
    label(ax, 88.0, 21.4, "H = E_K(0)", fs=6.8, color=GREY)

    box(ax, 79.0, 5.0, 18.0, 8.5, fc=PALE_WARN, ec="#dcb9a8")
    label(ax, 88.0, 9.25, "tag 128 位", fs=8.2, color=WARN, weight="bold")

    # 加密链
    arrow(ax, (19.0, 44.75), (24.5, 44.75))
    arrow(ax, (49.5, 44.75), (54.0, 44.75))
    arrow(ax, (37.0, 32.5), (37.0, 38.0))

    # 密文与 AAD 进入认证
    ax.plot([62.0, 62.0], [40.0, 23.25], color=ACCENT_2, lw=1.1,
            ls=(0, (4.5, 2.5)), zorder=2)
    arrow(ax, (62.0, 23.25), (79.0, 23.25), color=ACCENT_2, lw=1.1,
          ls=(0, (4.5, 2.5)))
    arrow(ax, (88.0, 40.0), (88.0, 28.5))

    # tag 输出
    arrow(ax, (88.0, 18.0), (88.0, 13.5))

    label(ax, 3.0, 15.0, "nonce 与计数器决定密钥流", fs=7.2, color=SOFT, ha="left")
    label(ax, 3.0, 10.5, "同一密钥下 nonce 不可重复", fs=7.2, color=SOFT, ha="left")
    label(ax, 3.0, 6.0, "AAD 只进 tag，不进密文", fs=7.2, color=SOFT, ha="left")

    return save(fig, "09", "aead-roles.png")


def ecdh_schedule():
    """ECDH 共享秘密与 HKDF 子密钥派生。"""
    fig, ax = setup(5.3, 3.3)

    box(ax, 2.0, 43.0, 26.0, 13.0, fc=PALE, ec=LINE)
    label(ax, 15.0, 52.2, "客户端", fs=9.0, color=INK, weight="bold")
    label(ax, 15.0, 48.0, "临时私钥 a", fs=7.0, color=SOFT)
    label(ax, 15.0, 44.8, "公钥 A = aG", fs=7.0, color=SOFT)

    box(ax, 72.0, 43.0, 26.0, 13.0, fc=PALE, ec=LINE)
    label(ax, 85.0, 52.2, "服务器", fs=9.0, color=INK, weight="bold")
    label(ax, 85.0, 48.0, "临时私钥 b", fs=7.0, color=SOFT)
    label(ax, 85.0, 44.8, "公钥 B = bG", fs=7.0, color=SOFT)

    arrow(ax, (28.0, 55.0), (72.0, 55.0), color=ACCENT)
    label(ax, 50.0, 57.4, "A = aG", fs=7.4, color=ACCENT)
    arrow(ax, (72.0, 50.5), (28.0, 50.5), color=ACCENT_2)
    label(ax, 50.0, 48.0, "B = bG", fs=7.4, color=ACCENT_2)

    box(ax, 32.0, 29.0, 36.0, 9.5, fc=PALE_BLUE, ec="#b6c4d2")
    label(ax, 50.0, 35.4, "abG", fs=9.6, color=BLUE, weight="bold")
    label(ax, 50.0, 31.6, "双方各算一次标量乘", fs=6.8, color=GREY)

    ax.plot([13.0, 13.0], [43.0, 33.75], color=LINE, lw=1.0, zorder=2)
    arrow(ax, (13.0, 33.75), (32.0, 33.75), color=LINE, lw=1.0)
    ax.plot([87.0, 87.0], [43.0, 26.0], color=LINE, lw=1.0, zorder=2)
    ax.plot([87.0, 60.0], [26.0, 26.0], color=LINE, lw=1.0, zorder=2)
    arrow(ax, (60.0, 26.0), (60.0, 29.0), color=LINE, lw=1.0)

    label(ax, 58.4, 26.2, "共享秘密", fs=6.6, color=GREY, ha="right")

    box(ax, 24.0, 14.0, 52.0, 9.5, fc=PALE_2, ec=LINE)
    label(ax, 50.0, 20.6, "HKDF", fs=9.2, color=INK, weight="bold")
    label(ax, 50.0, 16.6, "extract 出 PRK，再按 info 展开", fs=6.8, color=GREY)

    arrow(ax, (50.0, 29.0), (50.0, 23.5))
    ax.plot([50.0, 50.0], [14.0, 11.0], color=ACCENT_2, lw=1.1, zorder=2)
    ax.plot([25.0, 75.0], [11.0, 11.0], color=ACCENT_2, lw=1.1, zorder=2)
    arrow(ax, (25.0, 11.0), (25.0, 8.6), color=ACCENT_2, lw=1.1)
    arrow(ax, (75.0, 11.0), (75.0, 8.6), color=ACCENT_2, lw=1.1)

    box(ax, 6.0, 1.5, 38.0, 7.1, fc=PALE, ec=LINE)
    label(ax, 25.0, 5.05, "客户端→服务器 的密钥与 IV", fs=7.2, color=SOFT)
    box(ax, 56.0, 1.5, 38.0, 7.1, fc=PALE, ec=LINE)
    label(ax, 75.0, 5.05, "服务器→客户端 的密钥与 IV", fs=7.2, color=SOFT)

    return save(fig, "09", "ecdh-schedule.png")


if __name__ == "__main__":
    aead_roles()
    ecdh_schedule()
