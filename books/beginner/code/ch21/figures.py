# -*- coding: utf-8 -*-
"""第二十一章插图：2015-2026 时间轴、勒索产业的分工。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def timeline():
    """双列时间轴：左列 2016-2021，右列 2021-2024。"""
    fig, ax = setup(5.3, 3.4)
    left = [
        ("2016", "Mirai 源码公开，10 月打瘫 Dyn"),
        ("2017.5", "WannaCry，150 国 20 万台"),
        ("2017.6", "NotPetya 经会计软件更新"),
        ("2019", "LockerGoga 打瘫挪威海德鲁"),
        ("2020.12", "SolarWinds 事件披露"),
        ("2021.5", "Colonial Pipeline 停摆"),
    ]
    right = [
        ("2021.7", "Kaseya，约 1500 家企业"),
        ("2021.12", "Log4Shell 公开"),
        ("2023", "MOVEit，数千家组织"),
        ("2023", "3CX 供应链事件"),
        ("2024.3", "xz-utils 后门被发现"),
        ("2024", "Change Healthcare 事件"),
        ("2024", "Operation Cronos 打击 LockBit"),
    ]
    for spine, rows, top, step, dx in ((3.2, left, 54.0, 7.5, 36.5),
                                       (52.6, right, 54.0, 6.9, 36.5)):
        ys = [top - i * step for i in range(len(rows))]
        ax.plot([spine, spine], [ys[-1] - 2.8, ys[0] + 2.8], color=LINE,
                lw=1.0, zorder=1, solid_capstyle="butt")
        for (year, text), y in zip(rows, ys):
            ax.plot([spine], [y], marker="o", markersize=4.0, color=ACCENT_2,
                    zorder=4, markeredgewidth=0)
            label(ax, spine + 2.2, y, year, fs=6.9, color=ACCENT, ha="left",
                  weight="bold")
            label(ax, spine + 12.6, y, text, fs=6.8, color=INK, ha="left")

    label(ax, 26.0, 2.0, "2015 年之前，勒索的主要受害者是个人", fs=6.8,
          color=GREY)
    return save(fig, "21", "timeline-2015-2026.png")


def ransom_chain():
    """分工结构：四道工序、两个供给方、按比例分成。"""
    fig, ax = setup(5.3, 3.3)
    y_chain, h = 22.0, 14.0
    xs = [2.5, 27.5, 52.5, 77.5]
    w = 20.0
    steps = [
        ("初始访问", "卖入口\n凭据与漏洞"),
        ("运营方", "投放、加密\n索要赎金"),
        ("谈判", "定价\n定截止时间"),
        ("洗钱", "混币\n跨境转移"),
    ]
    for (title, note), x in zip(steps, xs):
        box(ax, x, y_chain, w, h, fc=PALE, ec=LINE)
        label(ax, x + w / 2, y_chain + h - 4.6, title, fs=8.0, color=INK,
              weight="bold")
        label(ax, x + w / 2, y_chain + 4.8, note, fs=6.5, color=GREY)

    for xa, xb in ((22.5, 27.5), (47.5, 52.5), (72.5, 77.5)):
        arrow(ax, (xa + 0.2, y_chain + h / 2), (xb - 0.2, y_chain + h / 2),
              color=ACCENT_2, lw=1.0, ms=7)

    box(ax, 27.5, 44.0, 20.0, 12.0, fc=PALE_BLUE, ec="#b6c4d2")
    label(ax, 37.5, 52.0, "开发者", fs=7.6, color=BLUE, weight="bold")
    label(ax, 37.5, 48.0, "加密器按订阅收费", fs=6.4, color=SOFT)
    arrow(ax, (37.5, 43.6), (37.5, 36.4), color=ACCENT_2, lw=1.0, ms=7)

    box(ax, 50.0, 4.0, 25.0, 12.0, fc=PALE_WARN, ec="#e0c4b6")
    label(ax, 62.5, 12.2, "受害组织", fs=7.6, color=WARN, weight="bold")
    label(ax, 62.5, 7.4, "加密并窃取数据", fs=6.6, color=SOFT)
    arrow(ax, (62.5, 16.4), (62.5, 21.6), color=WARN, lw=1.0, ms=7)
    label(ax, 64.2, 19.4, "赎金", fs=6.4, color=WARN, ha="left")

    label(ax, 22.0, 10.0, "分工越细，每一环\n的门槛越低", fs=6.8, color=GREY)
    label(ax, 50.0, 0.9, "赎金按事先约定的比例在各环节之间分成", fs=6.6,
          color=GREY)
    return save(fig, "21", "ransom-chain.png")


if __name__ == "__main__":
    timeline()
    ransom_chain()
