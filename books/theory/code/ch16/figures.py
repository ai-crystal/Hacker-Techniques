# -*- coding: utf-8 -*-
"""第十六章插图：精确率随基率变化、检测与规避的循环。"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)

X0, X1, Y0, Y1 = 17.0, 94.0, 13.0, 49.0
LO, HI = -6.0, -1.0


def _x(p):
    t = (math.log10(p) - LO) / (HI - LO)
    return X0 + t * (X1 - X0)


def _y(prec):
    return Y0 + prec * (Y1 - Y0)


def precision_vs_base_rate():
    fig, ax = setup(5.3, 3.3)

    ax.plot([X0, X1], [Y0, Y0], color=LINE, lw=1.0)
    ax.plot([X0, X0], [Y0, Y1], color=LINE, lw=1.0)
    ax.plot([X0, X1], [_y(0.5), _y(0.5)], color=LINE, lw=0.9,
            linestyle=(0, (3, 3)))

    def curve(fpr, color, dashed=False):
        pts = []
        n = 220
        for i in range(n + 1):
            p = 10 ** (LO + (HI - LO) * i / n)
            prec = 0.99 * p / (0.99 * p + fpr * (1 - p))
            pts.append((_x(p), _y(prec)))
        ax.plot([q[0] for q in pts], [q[1] for q in pts], color=color, lw=1.8,
                zorder=4, solid_capstyle="round",
                linestyle=(0, (5, 2)) if dashed else "-")

    curve(0.01, WARN, dashed=True)
    curve(0.001, ACCENT)

    for p, name in ((1e-6, "百万分之一"), (1e-4, "万分之一"), (1e-2, "百分之一")):
        ax.plot([_x(p), _x(p)], [Y0, Y0 - 1.2], color=LINE, lw=0.9)
        label(ax, _x(p), Y0 - 4.0, name, fs=6.6, color=SOFT)
    ax.plot([X1, X1], [Y0, Y0 - 1.2], color=LINE, lw=0.9)
    label(ax, X1, Y0 - 4.0, "十分之一", fs=6.6, color=SOFT)

    label(ax, X0 + 2.6, _y(0.5) + 2.4, "五成", fs=6.4, color=GREY, ha="left")
    label(ax, 5.6, (Y0 + Y1) / 2, "精确率", fs=7.4, color=SOFT, rotation=90)
    label(ax, (X0 + X1) / 2, 1.8, "攻击样本占全部样本的比例（对数刻度）", fs=7.2,
          color=SOFT)

    ax.plot([19.0, 26.0], [46.2, 46.2], color=ACCENT, lw=1.8, zorder=5)
    label(ax, 27.6, 46.2, "误报率 0.1%", fs=6.8, color=ACCENT, ha="left")
    ax.plot([19.0, 26.0], [42.8, 42.8], color=WARN, lw=1.8,
            linestyle=(0, (5, 2)), zorder=5)
    label(ax, 27.6, 42.8, "误报率 1%", fs=6.8, color=WARN, ha="left")
    label(ax, 27.6, 39.2, "两条曲线的命中率都是 99%", fs=6.8, color=SOFT,
          ha="left")
    return save(fig, "16", "precision-vs-base-rate.png")


def arms_race():
    fig, ax = setup(5.3, 3.2)

    box(ax, 5.0, 42.0, 35.0, 10.0, fc=PALE, ec=LINE)
    label(ax, 22.5, 48.6, "攻击者改样本", fs=8.6, color=INK, weight="bold")
    label(ax, 22.5, 44.8, "改编码、换写法、拆包", fs=6.8, color=GREY)

    box(ax, 60.0, 42.0, 35.0, 10.0, fc=PALE_BLUE, ec="#b6c4d2")
    label(ax, 77.5, 48.6, "检测方看到失败", fs=8.6, color=INK, weight="bold")
    label(ax, 77.5, 44.8, "样本被绕过，日志里留痕", fs=6.8, color=BLUE)

    box(ax, 60.0, 17.0, 35.0, 10.0, fc=PALE_BLUE, ec="#b6c4d2")
    label(ax, 77.5, 23.6, "加一条规则", fs=8.6, color=INK, weight="bold")
    label(ax, 77.5, 19.8, "人工分析，写签名或训练模型", fs=6.4, color=BLUE)

    box(ax, 5.0, 17.0, 35.0, 10.0, fc=PALE_WARN, ec="#d8b7a8")
    label(ax, 22.5, 23.6, "旧样本被抓住", fs=8.6, color=WARN, weight="bold")
    label(ax, 22.5, 19.8, "攻击者换一批没见过的样本", fs=6.4, color=WARN)

    arrow(ax, (40.4, 47.0), (59.6, 47.0), color=WARN)
    label(ax, 50.0, 49.6, "绕过成功", fs=6.8, color=WARN)
    arrow(ax, (77.5, 41.6), (77.5, 27.4))
    label(ax, 81.0, 34.5, "几小时到几周", fs=6.4, color=GREY, ha="left")
    arrow(ax, (59.6, 22.0), (40.4, 22.0))
    label(ax, 50.0, 19.6, "规则上线", fs=6.8, color=SOFT)
    arrow(ax, (22.5, 27.4), (22.5, 41.6), color=WARN)
    label(ax, 18.0, 34.5, "几分钟", fs=6.4, color=WARN, ha="right")

    label(ax, 50.0, 33.4, "每一圈", fs=7.0, color=SOFT)
    label(ax, 50.0, 29.8, "成本不对称", fs=7.0, color=INK)
    return save(fig, "16", "arms-race.png")


if __name__ == "__main__":
    precision_vs_base_rate()
    arms_race()
