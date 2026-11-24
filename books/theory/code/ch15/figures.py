# -*- coding: utf-8 -*-
"""第十五章插图：Spectre 式攻击的两步、瞬态执行攻击的家族分类。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def spectre_two_steps():
    fig, ax = setup(5.3, 3.5)

    label(ax, 2.0, 60.0, "第一步　让处理器投机地读一次", fs=8.4, color=ACCENT,
          ha="left", weight="bold")
    top = [
        (2.0, "分支预测器", "被训练成跳进去"),
        (37.0, "推测执行越过边界", "把 array[x] 读进寄存器"),
        (72.0, "数据还在寄存器里", "就当下标再访存"),
    ]
    for x, t1, t2 in top:
        box(ax, x, 44.0, 26.0, 10.0, fc=PALE, ec=LINE, lw=0.9)
        label(ax, x + 13.0, 50.3, t1, fs=7.4, color=INK)
        label(ax, x + 13.0, 46.4, t2, fs=6.6, color=GREY)
    arrow(ax, (28.4, 49.0), (36.6, 49.0))
    arrow(ax, (63.4, 49.0), (71.6, 49.0))
    label(ax, 32.5, 51.8, "猜对", fs=6.4, color=GREY)
    label(ax, 67.5, 51.8, "带秘密", fs=6.4, color=GREY)

    ax.plot([2.0, 98.0], [39.0, 39.0], color=LINE, lw=0.9, ls=(0, (4, 3)))

    label(ax, 2.0, 34.4, "第二步　用时间把缓存状态读出来", fs=8.4, color=WARN,
          ha="left", weight="bold")
    bottom = [
        (2.0, "先清空 probe", "按 64 字节冲掉"),
        (37.0, "逐个槽计时", "看哪条命中 L1"),
        (72.0, "最快的那个槽", "下标即秘密字节"),
    ]
    for x, t1, t2 in bottom:
        box(ax, x, 18.4, 26.0, 10.0, fc=PALE_WARN, ec="#d8b7a8", lw=0.9)
        label(ax, x + 13.0, 24.7, t1, fs=7.4, color=INK)
        label(ax, x + 13.0, 20.8, t2, fs=6.6, color=WARN)
    arrow(ax, (28.4, 23.4), (36.6, 23.4), color=WARN)
    arrow(ax, (63.4, 23.4), (71.6, 23.4), color=WARN)

    rect(ax, 2.0, 3.4, 96.0, 11.2, fc="#f7f8f6")
    label(ax, 5.0, 10.6, "两次读之间有数据依赖，处理器不会打乱顺序", fs=7.2,
          color=SOFT, ha="left")
    label(ax, 5.0, 6.2, "提交阶段发现越界并把结果丢掉，缓存里的那一行却留下了", fs=7.2,
          color=SOFT, ha="left")
    return save(fig, "15", "spectre-two-steps.png")


def transient_taxonomy():
    fig, ax = setup(5.3, 3.62)

    box(ax, 26.0, 59.0, 48.0, 8.6, fc=PALE_BLUE, ec="#b6c4d2")
    label(ax, 50.0, 64.6, "瞬态执行攻击", fs=9.4, color=INK, weight="bold")
    label(ax, 50.0, 61.0, "被取消的指令也在缓存里留下了痕迹", fs=6.6, color=BLUE)

    box(ax, 3.0, 44.5, 44.0, 9.4, fc=PALE_WARN, ec="#d8b7a8")
    label(ax, 25.0, 50.2, "越权访问，异常报得晚", fs=7.8, color=WARN, weight="bold")
    label(ax, 25.0, 46.6, "权限检查在提交阶段才做", fs=6.6, color=WARN)

    box(ax, 53.0, 44.5, 44.0, 9.4, fc=PALE, ec=LINE)
    label(ax, 75.0, 50.2, "推测方向错了", fs=7.8, color=ACCENT, weight="bold")
    label(ax, 75.0, 46.6, "预测器把执行带到不该走的路上", fs=6.6, color=ACCENT_2)

    arrow(ax, (44.0, 58.8), (26.0, 54.2), color=WARN)
    arrow(ax, (56.0, 58.8), (74.0, 54.2), color=ACCENT)

    left = [
        ("Meltdown", "CVE-2017-5754　读内核映射"),
        ("L1TF", "CVE-2018-3615　读物理页"),
        ("MDS", "CVE-2018-12126　读填充缓冲"),
    ]
    ys = [33.6, 23.6, 13.6]
    ax.plot([6.0, 6.0], [44.3, 17.1], color="#c8b6ad", lw=1.0)
    for (name, note), y in zip(left, ys):
        box(ax, 9.0, y, 38.0, 7.2, fc="white", ec="#d8b7a8", lw=0.8)
        label(ax, 11.0, y + 4.9, name, fs=7.0, color=WARN, ha="left")
        label(ax, 11.0, y + 2.3, note, fs=6.3, color=GREY, ha="left")
        arrow(ax, (6.0, y + 3.6), (8.6, y + 3.6), color="#c8b6ad", lw=0.9, ms=6)

    right = [
        ("Spectre v1", "CVE-2017-5753　边界检查绕过"),
        ("Spectre v2", "CVE-2017-5715　分支目标注入"),
        ("Spectre v3a", "CVE-2018-3640　读系统寄存器"),
        ("Spectre v4", "CVE-2018-3639　推测存储绕过"),
    ]
    ry = [35.0, 26.0, 17.0, 8.0]
    ax.plot([94.0, 94.0], [44.3, 11.6], color="#b9c8c6", lw=1.0)
    for (name, note), y in zip(right, ry):
        box(ax, 53.0, y, 38.0, 7.2, fc="white", ec=LINE, lw=0.8)
        label(ax, 55.0, y + 4.9, name, fs=7.0, color=ACCENT, ha="left")
        label(ax, 55.0, y + 2.3, note, fs=6.3, color=GREY, ha="left")
        arrow(ax, (94.0, y + 3.6), (91.4, y + 3.6), color="#b9c8c6", lw=0.9,
              ms=6)
    return save(fig, "15", "transient-taxonomy.png")


if __name__ == "__main__":
    spectre_two_steps()
    transient_taxonomy()
