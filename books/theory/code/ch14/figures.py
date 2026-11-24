# -*- coding: utf-8 -*-
"""第十四章插图：反馈式模糊测试的循环、覆盖率增长与高原。"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def fuzz_loop():
    fig, ax = setup(5.3, 3.12)

    box(ax, 6.0, 41.0, 36.0, 9.6, fc=PALE_BLUE, ec="#b6c4d2")
    label(ax, 24.0, 47.6, "种子队列", fs=9.2, color=INK, weight="bold")
    label(ax, 24.0, 43.6, "历史语料、格式样本", fs=7.0, color=BLUE)

    box(ax, 58.0, 41.0, 36.0, 9.6, fc=PALE, ec=LINE)
    label(ax, 76.0, 47.6, "变异", fs=9.2, color=INK, weight="bold")
    label(ax, 76.0, 43.6, "位翻转、插删、字典替换", fs=6.8, color=GREY)

    box(ax, 58.0, 17.0, 36.0, 9.6, fc=PALE, ec=LINE)
    label(ax, 76.0, 23.6, "执行", fs=9.2, color=INK, weight="bold")
    label(ax, 76.0, 19.6, "目标程序 + harness", fs=7.0, color=GREY)

    box(ax, 6.0, 17.0, 36.0, 9.6, fc=PALE_WARN, ec="#d8b7a8")
    label(ax, 24.0, 23.6, "反馈与筛选", fs=9.2, color=WARN)
    label(ax, 24.0, 19.6, "crash 留档，新覆盖入队", fs=6.8, color=WARN)

    arrow(ax, (42.4, 45.8), (57.6, 45.8))
    label(ax, 50.0, 48.8, "取一条", fs=7.0, color=SOFT)

    arrow(ax, (76.0, 40.8), (76.0, 26.8))
    label(ax, 72.0, 33.8, "喂进目标", fs=7.0, color=SOFT, ha="right")

    arrow(ax, (57.6, 21.8), (42.4, 21.8))
    label(ax, 50.0, 24.6, "执行路径", fs=7.0, color=SOFT)

    arrow(ax, (24.0, 26.8), (24.0, 40.8))
    label(ax, 28.0, 33.8, "回填", fs=7.0, color=SOFT, ha="left")

    label(ax, 50.0, 11.6, "只有带来新边的输入才值得留在队列里", fs=7.2, color=SOFT)
    label(ax, 50.0, 7.0, "同一条边命中多次会被计数桶折叠成少量档位", fs=7.2, color=GREY)
    return save(fig, "14", "fuzz-loop.png")


def coverage_plateau():
    fig, ax = setup(5.3, 2.94)

    x0, x1, y0, y1 = 16.0, 96.0, 10.0, 46.0
    ax.plot([x0, x1], [y0, y0], color=LINE, lw=1.0)
    ax.plot([x0, x0], [y0, y1], color=LINE, lw=1.0)
    label(ax, (x0 + x1) / 2, 5.4, "累计执行次数，对数刻度", fs=7.4, color=SOFT)
    label(ax, 6.6, (y0 + y1) / 2, "已覆盖的边数", fs=7.4, color=SOFT,
          rotation=90)

    def curve(base, amp, rate):
        pts = []
        n = 180
        for i in range(n + 1):
            t = i / n
            pts.append((x0 + t * (x1 - x0), base + amp * (1 - math.exp(-t * rate))))
        return pts

    good = curve(y0, 27.0, 4.4)
    poor = curve(y0, 15.5, 2.6)
    ax.plot([p[0] for p in good], [p[1] for p in good], color=ACCENT, lw=1.9,
            solid_capstyle="round", zorder=4)
    ax.plot([p[0] for p in poor], [p[1] for p in poor], color=WARN, lw=1.9,
            linestyle=(0, (5, 2)), zorder=4)

    # 图例放在左上角的空白处
    ax.plot([19.0, 27.0], [43.6, 43.6], color=ACCENT, lw=1.9, zorder=5)
    label(ax, 29.0, 43.6, "harness 打通了真实入口", fs=7.0, color=ACCENT,
          ha="left")
    ax.plot([19.0, 27.0], [39.8, 39.8], color=WARN, lw=1.9,
            linestyle=(0, (5, 2)), zorder=5)
    label(ax, 29.0, 39.8, "harness 只爬到外层解析", fs=7.0, color=WARN,
          ha="left")

    label(ax, 78.0, 43.4, "进入高原期", fs=7.6, color=INK)
    arrow(ax, (78.0, 41.6), (78.0, 37.0), color=GREY, lw=1.0, ms=7)
    return save(fig, "14", "coverage-plateau.png")


if __name__ == "__main__":
    fuzz_loop()
    coverage_plateau()
