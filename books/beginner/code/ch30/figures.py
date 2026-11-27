# -*- coding: utf-8 -*-
"""第三十章插图：研究路径的选择与披露时间线。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def research_paths():
    """手里有什么，去哪，换来什么。"""
    fig, ax = setup(5.3, 3.2)

    heads = [(2.0, "手里有什么"), (36.0, "去哪"), (69.0, "换来什么")]
    for x, text in heads:
        label(ax, x, 55.4, text, fs=7.0, color=GREY, ha="left", weight="bold")

    rows = [
        (40.0, "只有时间", "没有具体目标",
         "靶场与 CTF", "题目有确定解",
         "可重复的环境", "知道自己错在哪"),
        (25.0, "在读某个项目", "想弄懂它的代码",
         "项目的 SECURITY.md", "私密报告渠道",
         "与作者直接对话", "公告里署你的名"),
        (10.0, "有明确的目标", "一家公司或产品",
         "赏金计划的规则页", "范围、禁区、报价",
         "奖金与公开记录", "信用与履历"),
    ]
    for y, a1, a2, b1, b2, c1, c2 in rows:
        box(ax, 2.0, y, 27.0, 11.0, fc=PALE_2, ec=LINE, lw=0.9)
        label(ax, 4.2, y + 7.4, a1, fs=7.2, color=INK, ha="left")
        label(ax, 4.2, y + 3.6, a2, fs=6.2, color=GREY, ha="left")

        box(ax, 36.0, y, 28.0, 11.0, fc=PALE_BLUE, ec="#b6c4d2", lw=0.9)
        label(ax, 38.2, y + 7.4, b1, fs=7.2, color=BLUE, ha="left")
        label(ax, 38.2, y + 3.6, b2, fs=6.2, color=GREY, ha="left")

        box(ax, 69.0, y, 29.0, 11.0, fc=PALE, ec=LINE, lw=0.9)
        label(ax, 71.2, y + 7.4, c1, fs=7.2, color=ACCENT, ha="left")
        label(ax, 71.2, y + 3.6, c2, fs=6.2, color=GREY, ha="left")

        arrow(ax, (29.4, y + 5.5), (35.6, y + 5.5), color=GREY, lw=0.9)
        arrow(ax, (65.6, y + 5.5), (68.6, y + 5.5), color=GREY, lw=0.9)

    label(ax, 2.0, 3.0, "三条路的共同入口是读授权，不是找漏洞",
          fs=7.0, color=SOFT, ha="left")
    return save(fig, "30", "research-paths.png")


def disclosure_timeline():
    """从报告到公开的甘特图。"""
    fig, ax = setup(5.3, 3.7)

    def dx(day):
        return 32.0 + day * (64.0 / 90.0)

    rows = [
        (51.2, "报告与分诊", "0–7 天", 0, 7, PALE_BLUE, "#b6c4d2"),
        (41.4, "确认与定级", "3–14 天", 3, 14, PALE_BLUE, "#b6c4d2"),
        (31.6, "修复开发", "14–45 天", 14, 45, PALE_BLUE, "#b6c4d2"),
        (21.8, "验证与上线", "45–55 天", 45, 55, PALE, LINE),
    ]
    for y, name, span, d0, d1, fc, ec in rows:
        label(ax, 29.5, y + 3.6, name, fs=7.0, color=INK, ha="right")
        label(ax, 29.5, y + 1.3, span, fs=6.2, color=GREY, ha="right")
        rect(ax, dx(d0), y, dx(d1) - dx(d0), 5.6, fc=fc, ec=ec, lw=0.9,
             zorder=2)

    # 用户打补丁的窗口
    y = 11.0
    label(ax, 29.5, y + 3.6, "用户打补丁", fs=7.0, color=WARN, ha="right")
    label(ax, 29.5, y + 1.3, "55–90 天", fs=6.2, color=GREY, ha="right")
    rect(ax, dx(55), y, dx(90) - dx(55), 5.6, fc=PALE_WARN, ec="#d8c3b8",
         lw=0.9, zorder=2)
    label(ax, (dx(55) + dx(90)) / 2, y + 2.8, "风险窗口", fs=6.6, color=WARN)

    # 时间轴
    ax.plot([32.0, 96.0], [8.0, 8.0], color=LINE, lw=1.0, zorder=1)
    for d, text in [(0, "0"), (30, "30"), (60, "60"), (90, "90 天")]:
        ax.plot([dx(d), dx(d)], [8.0, 6.8], color=LINE, lw=0.9, zorder=1)
        label(ax, dx(d), 4.6, text, fs=6.4, color=GREY)

    # 90 天披露期限
    ax.plot([dx(90), dx(90)], [8.0, 58.0], color=WARN, lw=0.9,
            ls=(0, (4, 2.4)), zorder=2)
    label(ax, 96.0, 61.0, "第 90 天，惯例上的披露期限", fs=6.6, color=WARN,
          ha="right")

    label(ax, 2.0, 66.4, "90 天是惯例不是法律，修复上线后可以提前公开",
          fs=6.8, color=GREY, ha="left")
    return save(fig, "30", "disclosure-timeline.png")


if __name__ == "__main__":
    research_paths()
    disclosure_timeline()
