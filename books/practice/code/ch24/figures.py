# -*- coding: utf-8 -*-
"""第二十四章插图：报告结构与读者、风险定级四象限。

画布宽 5.3 英寸，图内不写标题。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def report_readers():
    """六个段落，三类读者，实心必读、空心参考。"""
    fig, ax = setup(5.3, 3.4)

    cols = [(62.0, "决策层"), (76.0, "技术团队"), (90.0, "审计合规")]
    for x, name in cols:
        label(ax, x, 58.6, name, fs=7.4, color=SOFT, weight="bold")
    label(ax, 48.0, 58.6, "段落", fs=6.6, color=GREY, ha="right")

    rows = [
        (52.0, "摘要", (1, 0, 0)),
        (44.5, "范围与方法", (0, 1, 1)),
        (37.0, "发现", (0, 1, 0)),
        (29.5, "影响", (1, 0, 0)),
        (22.0, "修复建议", (0, 1, 0)),
        (14.5, "附录", (-1, 0, 1)),
    ]

    for y, name, marks in rows:
        label(ax, 48.0, y, name, fs=7.8, color=INK, ha="right")
        for (x, _n), m in zip(cols, marks):
            if m == 1:
                ax.plot([x], [y], marker="o", ms=6.2, mfc=ACCENT, mec=ACCENT,
                        zorder=5)
            elif m == 0:
                ax.plot([x], [y], marker="o", ms=6.2, mfc="white", mec=GREY,
                        mew=0.9, zorder=5)

    # 行分隔线
    for y, _name, _m in rows:
        ax.plot([52.5, 95.0], [y - 3.6, y - 3.6], color=LINE, lw=0.5,
                zorder=2)
    ax.plot([52.5, 95.0], [56.6, 56.6], color=LINE, lw=0.7, zorder=2)

    ax.plot([6.0], [52.0], marker="o", ms=6.2, mfc=ACCENT, mec=ACCENT)
    label(ax, 9.0, 52.0, "必读", fs=6.8, color=SOFT, ha="left")
    ax.plot([6.0], [46.0], marker="o", ms=6.2, mfc="white", mec=GREY,
            mew=0.9)
    label(ax, 9.0, 46.0, "参考", fs=6.8, color=SOFT, ha="left")

    label(ax, 4.0, 8.5, "摘要与影响两段被两类人同时需要", fs=6.4, color=GREY,
          ha="left")

    return save(fig, "24", "report-readers.png")


def risk_quadrant():
    """可利用性 × 资产重要性。"""
    fig, ax = setup(5.3, 3.4)

    x0, x1, y0, y1 = 16.0, 93.0, 12.0, 58.0
    xm, ym = 55.0, 35.0

    rect(ax, x0, ym, xm - x0, y1 - ym, fc=PALE_2)
    rect(ax, xm, ym, x1 - xm, y1 - ym, fc=PALE_WARN)
    rect(ax, x0, y0, xm - x0, ym - y0, fc=PALE)
    rect(ax, xm, y0, x1 - xm, ym - y0, fc=PALE_BLUE)

    ax.plot([xm, xm], [y0, y1], color=LINE, lw=0.6, zorder=2)
    ax.plot([x0, x1], [ym, ym], color=LINE, lw=0.6, zorder=2)

    # 坐标轴
    arrow(ax, (x0, y0), (x1 + 2.0, y0), color=SOFT, lw=0.9, ms=7)
    arrow(ax, (x0, y0), (x0, y1 + 3.0), color=SOFT, lw=0.9, ms=7)
    label(ax, 54.5, 8.0, "可利用性（越往右越容易）", fs=6.8, color=SOFT)
    label(ax, 9.6, 35.0, "资产重要性与影响", fs=6.8, color=SOFT, rotation=90)
    label(ax, x0, 5.4, "低", fs=6.2, color=GREY)
    label(ax, x1, 5.4, "高", fs=6.2, color=GREY)
    label(ax, 13.2, y1 - 1.0, "高", fs=6.2, color=GREY)
    label(ax, 13.2, y0 + 1.0, "低", fs=6.2, color=GREY)

    # 四象限结论
    label(ax, 89.0, 53.0, "立即修", fs=8.2, color=WARN, weight="bold",
          ha="right")
    label(ax, 19.0, 53.0, "排期修", fs=8.2, color=SOFT, weight="bold",
          ha="left")
    label(ax, 89.0, 16.5, "批量修", fs=8.2, color=BLUE, weight="bold",
          ha="right")
    label(ax, 19.0, 16.5, "记录，随版本迭代", fs=7.6, color=SOFT,
          weight="bold", ha="left")

    # 示例
    dots = [
        (76.0, 45.0, "未认证 RCE，公网边缘", WARN),
        (30.0, 46.5, "需域管凭据的提权", SOFT),
        (72.0, 26.0, "内网测试机的反射型 XSS", BLUE),
        (30.0, 26.0, "日志里的低危信息泄露", SOFT),
    ]
    for x, y, text, color in dots:
        ax.plot([x], [y], marker="o", ms=4.4, mfc=color, mec=color, zorder=5)
        label(ax, x, y - 2.6, text, fs=6.3, color=SOFT, ha="center")

    return save(fig, "24", "risk-quadrant.png")


if __name__ == "__main__":
    report_readers()
    risk_quadrant()
