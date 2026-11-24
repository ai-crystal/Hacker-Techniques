# -*- coding: utf-8 -*-
"""第十七章插图：规则开发闭环、狩猎路径。

画布宽度统一取 5.3 英寸，与版心宽度接近，图内不写标题。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def rule_loop():
    """五步一环，顺时针。"""
    fig, ax = setup(5.3, 3.2)

    nodes = [
        (50.0, 48.8, "假设", "什么行为不该出现", PALE, ACCENT),
        (80.0, 31.8, "写规则", "选字段、定范围", PALE_BLUE, BLUE),
        (72.0, 12.8, "回放验证", "已知样本必须命中", PALE_2, SOFT),
        (28.0, 12.8, "误报收敛", "逐条看命中物", PALE_WARN, WARN),
        (20.0, 31.8, "上线与监控", "统计命中与漏报", PALE, ACCENT),
    ]
    w, h = 27.0, 9.6
    for cx, cy, name, note, fc, tc in nodes:
        box(ax, cx - w / 2, cy - h / 2, w, h, fc=fc, ec=LINE, lw=0.9)
        label(ax, cx, cy + 2.3, name, fs=8.8, color=tc, weight="bold")
        label(ax, cx, cy - 2.5, note, fs=6.6, color=GREY)

    arrow(ax, (63.5, 51.2), (78.0, 36.8), color=ACCENT, lw=1.0, ms=7)
    arrow(ax, (82.0, 26.6), (85.4, 17.8), color=ACCENT, lw=1.0, ms=7)
    arrow(ax, (58.2, 12.8), (41.8, 12.8), color=ACCENT, lw=1.0, ms=7)
    arrow(ax, (15.2, 17.8), (18.4, 26.6), color=ACCENT, lw=1.0, ms=7)
    arrow(ax, (21.0, 36.8), (36.8, 51.2), color=ACCENT, lw=1.0, ms=7)

    label(ax, 50.0, 23.4, "每条规则都有主人", fs=6.9, color=GREY)
    label(ax, 50.0, 20.1, "和一条退休日期", fs=6.9, color=GREY)
    return save(fig, "17", "rule-loop.png")


def hunt_path():
    """一条假设的四种去向。"""
    fig, ax = setup(5.3, 2.8)

    steps = [
        ("假设", "谁做了什么", PALE, ACCENT),
        ("数据检查", "字段与保留期", PALE, ACCENT),
        ("基线查询", "平时长什么样", PALE, ACCENT),
        ("异常子集", "偏离的那几条", PALE, ACCENT),
    ]
    w, h, y = 20.0, 12.0, 38.0
    for i, (name, note, fc, tc) in enumerate(steps):
        x = 1.0 + i * 26.0
        box(ax, x, y, w, h, fc=fc, ec=LINE, lw=0.9)
        label(ax, x + w / 2, y + 8.6, name, fs=8.4, color=tc, weight="bold")
        label(ax, x + w / 2, y + 3.7, note, fs=6.2, color=GREY)
    for i in range(3):
        x = 1.0 + i * 26.0 + w
        arrow(ax, (x + 0.4, y + 6.0), (x + 5.6, y + 6.0), color=ACCENT,
              lw=1.0, ms=7)

    # 汇聚到三个结论
    ax.plot([89.0, 89.0], [y - 0.4, 26.0], color=ACCENT, lw=1.0, zorder=3)
    ax.plot([16.0, 89.0], [26.0, 26.0], color=ACCENT, lw=1.0, zorder=3)
    for cx in (16.0, 50.0, 84.0):
        arrow(ax, (cx, 26.0), (cx, 16.4), color=ACCENT, lw=1.0, ms=7)

    outs = [
        (2.0, "假设成立", "有细节可复核", PALE_BLUE, BLUE),
        (36.0, "假设被推翻", "记录里找不到", PALE_2, SOFT),
        (70.0, "数据不足", "先补采集范围", PALE_WARN, WARN),
    ]
    for x, name, note, fc, tc in outs:
        box(ax, x, 4.0, 28.0, 12.0, fc=fc, ec=LINE, lw=0.9)
        label(ax, x + 14.0, 12.6, name, fs=8.4, color=tc, weight="bold")
        label(ax, x + 14.0, 7.4, note, fs=6.5, color=GREY)

    return save(fig, "17", "hunt-path.png")


if __name__ == "__main__":
    rule_loop()
    hunt_path()
