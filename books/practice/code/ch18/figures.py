# -*- coding: utf-8 -*-
"""第十八章插图：响应阶段与决策点、演练时间线。

画布宽度统一取 5.3 英寸，与版心宽度接近，图内不写标题。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def response_phases():
    """六个阶段，右侧标出阶段之间的决策点。"""
    fig, ax = setup(5.3, 3.5)

    phases = [
        ("准备", "资产清单、日志留存、联系方式", PALE),
        ("识别", "确认范围与入口，先不动现场", PALE),
        ("遏制", "断开扩散路径，保住可用数据", PALE_WARN),
        ("根除", "去掉持久化与凭据，补上入口", PALE_WARN),
        ("恢复", "分批上线，验证数据完整", PALE),
        ("复盘", "时间线、缺口、改进项与负责人", PALE_2),
    ]
    decisions = [
        "谁有权宣布事件",
        "范围：单机、网段、整站",
        "清理还是重建",
        "备份可信吗",
        "同类资产查完没有",
    ]

    x, w, h = 4.0, 46.0, 7.6
    ys = [56.0, 45.0, 34.0, 23.0, 12.0, 1.0]
    for (name, goal, fc), y in zip(phases, ys):
        box(ax, x, y, w, h, fc=fc, ec=LINE, lw=0.9)
        label(ax, x + 2.6, y + 5.1, name, fs=8.6, color=ACCENT, ha="left",
              weight="bold")
        label(ax, x + 2.6, y + 1.8, goal, fs=6.5, color=SOFT, ha="left")

    for y in ys[:-1]:
        arrow(ax, (x + 12.0, y - 0.4), (x + 12.0, y - 3.0), color=ACCENT,
              lw=1.0, ms=6.5)

    for (name, goal, fc), y, text in zip(phases, ys, decisions):
        mid = y + h + 1.7
        ax.plot([x + w, 55.0], [mid, mid], color=ACCENT_2, lw=0.7,
                ls=(0, (2.4, 2.0)), zorder=3)
        label(ax, 56.4, mid, text, fs=6.9, color=WARN, ha="left")

    return save(fig, "18", "response-phases.png")


def drill_timeline():
    """一场八小时的演练，两侧分别是攻防双方的动作。"""
    fig, ax = setup(5.3, 3.5)

    ax.plot([50.0, 50.0], [3.0, 57.0], color=LINE, lw=1.0, zorder=2)
    for t in range(10):
        y = 55.0 - t * 5.4
        ax.plot([49.0, 51.0], [y, y], color=LINE, lw=0.8, zorder=2)
    label(ax, 48.6, 57.3, "T+0", fs=5.9, color=GREY, ha="right")
    label(ax, 48.6, 4.0, "T+9h", fs=5.9, color=GREY, ha="right")

    reds = [
        (0.5, "T+0.5　投递钓鱼附件", "首台工作站执行"),
        (3.0, "T+3.0　转储凭据", "备份账号被读"),
        (6.0, "T+6.0　打包外传", "出网被代理拦下"),
    ]
    blues = [
        (2.0, "T+2.0　首个告警", "计划任务创建"),
        (5.0, "T+5.0　宣布事件", "隔离网段"),
        (7.5, "T+7.5　清除持久化", "重置凭据"),
    ]

    for t, title, note in reds:
        y = 55.0 - t * 5.4
        box(ax, 2.0, y - 3.5, 41.0, 7.0, fc=PALE_WARN, ec="#ddc4b8", lw=0.8)
        label(ax, 4.4, y + 1.5, title, fs=7.0, color=WARN, ha="left")
        label(ax, 4.4, y - 1.6, note, fs=6.0, color=GREY, ha="left")
        arrow(ax, (43.4, y), (49.4, y), color=WARN, lw=0.8, ms=5.5)

    for t, title, note in blues:
        y = 55.0 - t * 5.4
        box(ax, 58.0, y - 3.5, 40.0, 7.0, fc=PALE_BLUE, ec="#bdc9d6", lw=0.8)
        label(ax, 60.4, y + 1.5, title, fs=7.0, color=BLUE, ha="left")
        label(ax, 60.4, y - 1.6, note, fs=6.0, color=GREY, ha="left")
        arrow(ax, (50.6, y), (57.4, y), color=BLUE, lw=0.8, ms=5.5)

    label(ax, 22.0, 61.2, "攻击方", fs=7.6, color=WARN, weight="bold")
    label(ax, 78.0, 61.2, "防守方", fs=7.6, color=BLUE, weight="bold")
    label(ax, 50.0, 60.6, "演练计时", fs=6.2, color=GREY)

    return save(fig, "18", "drill-timeline.png")


if __name__ == "__main__":
    response_phases()
    drill_timeline()
