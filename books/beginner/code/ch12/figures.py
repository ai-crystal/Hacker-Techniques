# -*- coding: utf-8 -*-
"""第十二章插图：加盐哈希、bcrypt 成本曲线。

bcrypt 那张是本书唯一的数据图，纵轴为对数刻度，数据直接来自算法定义
（迭代次数 = 2^cost），不是测量值。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                    PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label, rect,
                    save, setup)


def hash_salt():
    fig, ax = setup(5.3, 3.05)

    label(ax, 4.0, 53.0, "用户", fs=7.0, color=GREY, ha="left")
    label(ax, 20.0, 53.0, "盐", fs=7.0, color=GREY, ha="left")
    label(ax, 36.0, 53.0, "口令", fs=7.0, color=GREY, ha="left")
    label(ax, 56.0, 53.0, "存储的哈希", fs=7.0, color=GREY, ha="left")
    ax.plot([3.0, 97.0], [50.5, 50.5], color=LINE, lw=0.9)

    rows = [
        ("alice", "—", "123456", "e10adc3949ba", PALE_2, WARN),
        ("bob", "—", "123456", "e10adc3949ba", PALE_2, WARN),
        ("alice", "aX9", "123456", "8f14e45fceea", PALE, ACCENT),
        ("bob", "Qm2", "123456", "3c7bd5a1c0e9", PALE, ACCENT),
    ]
    tops = [41.0, 32.0, 21.0, 12.0]
    for (user, salt, pwd, digest, fc, color), top in zip(rows, tops):
        rect(ax, 3.0, top, 94.0, 8.0, fc=fc)
        label(ax, 6.0, top + 4.0, user, fs=7.4, color=SOFT, ha="left")
        label(ax, 20.0, top + 4.0, salt, fs=7.4, color=SOFT, ha="left")
        label(ax, 36.0, top + 4.0, pwd, fs=7.4, color=SOFT, ha="left")
        label(ax, 56.0, top + 4.0, digest, fs=6.9, color=color, ha="left")

    ax.plot([3.0, 97.0], [30.5, 30.5], color=LINE, lw=0.9)

    # 右侧括号：无盐两行相同，加盐两行不同
    ax.plot([74.5, 76.5, 76.5, 74.5], [48.6, 48.6, 32.4, 32.4], color=WARN,
            lw=0.9)
    label(ax, 78.0, 40.5, "无盐，完全相同", fs=6.6, color=WARN, ha="left")
    ax.plot([74.5, 76.5, 76.5, 74.5], [28.6, 28.6, 12.4, 12.4], color=ACCENT,
            lw=0.9)
    label(ax, 78.0, 20.5, "加盐，互不相同", fs=6.6, color=ACCENT, ha="left")

    label(ax, 3.0, 6.4, "无盐时同一口令得到同一哈希，一张彩虹表全部命中；加盐后每个账户都要单独算一遍。",
          fs=6.9, color=SOFT, ha="left")
    label(ax, 3.0, 2.2, "示意，哈希值经过截断", fs=6.0, color=GREY, ha="left")

    return save(fig, "12", "hash-salt.png")


def bcrypt_cost():
    fig, ax = setup(5.3, 2.6)
    ax.axis("on")

    costs = list(range(4, 17))
    iters = [2 ** c for c in costs]

    ax.set_yscale("log", base=2)
    ax.set_xlim(3.4, 16.8)
    ax.set_ylim(2 ** 3.4, 2 ** 17.6)

    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(LINE)
        ax.spines[spine].set_linewidth(0.9)

    ax.grid(axis="y", color=LINE, lw=0.6, ls=(0, (2, 3)), zorder=0)
    ax.set_axisbelow(True)

    ax.plot(costs, iters, color=ACCENT, lw=1.3, marker="o", ms=3.0,
            markerfacecolor="white", markeredgecolor=ACCENT,
            markeredgewidth=0.9, zorder=3)

    ax.set_xticks([4, 6, 8, 10, 12, 14, 16])
    ax.set_yticks([2 ** 4, 2 ** 8, 2 ** 12, 2 ** 16])
    ax.set_yticklabels(["16", "256", "4 096", "65 536"])
    ax.tick_params(axis="both", labelsize=6.8, colors=GREY, length=2.5,
                   width=0.8)
    for tick in ax.get_xticklabels() + ax.get_yticklabels():
        tick.set_color(SOFT)

    ax.set_xlabel("成本因子 cost", fontsize=7.4, color=SOFT, labelpad=2.5)
    ax.set_ylabel("迭代次数 2^cost", fontsize=7.4, color=SOFT, labelpad=3.5)

    ax.text(4.3, 2 ** 15.4, "每加 1，计算量翻倍", fontsize=6.9, color=ACCENT,
            ha="left", va="center")
    ax.plot([12.0, 12.0], [2 ** 3.6, 2 ** 12], color=LINE, lw=0.8,
            ls=(0, (3, 3)), zorder=1)
    ax.text(11.6, 2 ** 7.4, "常见取值 12", fontsize=6.6, color=GREY,
            ha="right", va="center")

    return save(fig, "12", "bcrypt-cost.png")


if __name__ == "__main__":
    hash_salt()
    bcrypt_cost()
