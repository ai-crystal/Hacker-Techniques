# -*- coding: utf-8 -*-
"""第十三章插图：符号执行的分支树、污点传播路径。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def symbolic_tree():
    fig, ax = setup(5.3, 3.42)

    # 根节点
    box(ax, 34.0, 53.5, 34.0, 8.6, fc=PALE_BLUE, ec="#b6c4d2")
    label(ax, 51.0, 59.2, "入口函数 f(x)", fs=9.2, color=INK, weight="bold")
    label(ax, 51.0, 55.7, "x 是符号量，不取具体值", fs=7.2, color=BLUE)

    # 第一层
    box(ax, 9.5, 37.0, 32.0, 8.6, fc=PALE, ec=LINE)
    label(ax, 25.5, 42.7, "x > 10 成立", fs=8.8, color=INK)
    label(ax, 25.5, 39.2, "约束 x > 10", fs=7.2, color=GREY)

    box(ax, 60.5, 37.0, 32.0, 8.6, fc=PALE, ec=LINE)
    label(ax, 76.5, 42.7, "x > 10 不成立", fs=8.8, color=INK)
    label(ax, 76.5, 39.2, "约束 x ≤ 10", fs=7.2, color=GREY)

    # 第二层：四个叶节点
    leaves = [
        (1.0, "x² = 36", "解得 x = 6 或 −6", "与前件冲突，剪枝", PALE_WARN, WARN),
        (26.0, "x² ≠ 36", "约束可满足", "继续向下派生", PALE_2, SOFT),
        (51.0, "x² = 36", "x = 6 或 −6", "可解，生成输入", PALE, ACCENT),
        (76.0, "x² ≠ 36", "约束可满足", "继续向下派生", PALE_2, SOFT),
    ]
    for x, t1, t2, t3, fc, c3 in leaves:
        box(ax, x, 18.6, 23.0, 11.4, fc=fc, ec=LINE, lw=0.9)
        label(ax, x + 11.5, 27.6, t1, fs=8.4, color=INK)
        label(ax, x + 11.5, 24.1, t2, fs=7.0, color=GREY)
        label(ax, x + 11.5, 21.1, t3, fs=6.8, color=c3)

    # 连线
    arrow(ax, (42.0, 53.3), (27.0, 45.9))
    arrow(ax, (60.0, 53.3), (75.0, 45.9))
    arrow(ax, (17.5, 36.8), (12.4, 30.2))
    arrow(ax, (33.0, 36.8), (36.9, 30.2))
    arrow(ax, (68.5, 36.8), (64.1, 30.2))
    arrow(ax, (84.0, 36.8), (88.4, 30.2))

    # 底部说明
    rect(ax, 1.0, 2.4, 98.0, 10.6, fc="#f7f8f6")
    label(ax, 4.0, 9.8, "路径条件（path condition）是沿途各分支条件的合取", fs=7.4,
          color=SOFT, ha="left")
    label(ax, 4.0, 5.3, "交给 SMT 求解器判定可满足性，不可满足的分支直接剪掉", fs=7.4,
          color=SOFT, ha="left")
    label(ax, 96.0, 9.8, "每多一层条件", fs=7.2, color=WARN, ha="right")
    label(ax, 96.0, 6.6, "路径数翻倍", fs=7.2, color=WARN, ha="right")
    return save(fig, "13", "symbolic-path-tree.png")


def taint_flow():
    fig, ax = setup(5.3, 3.02)

    box(ax, 32.0, 45.0, 36.0, 9.0, fc=PALE_BLUE, ec="#b6c4d2")
    label(ax, 50.0, 51.1, "source：外部输入", fs=9.0, color=INK, weight="bold")
    label(ax, 50.0, 47.2, "recv / argv / 表单字段", fs=7.2, color=BLUE)

    box(ax, 4.0, 29.0, 38.0, 9.6, fc=PALE, ec=LINE)
    label(ax, 23.0, 35.4, "HTML 转义函数", fs=8.6, color=INK)
    label(ax, 23.0, 31.6, "只滤掉 < > & 三个字符", fs=7.0, color=GREY)

    box(ax, 58.0, 29.0, 38.0, 9.6, fc=PALE, ec=LINE)
    label(ax, 77.0, 35.4, "直接拼进命令串", fs=8.6, color=INK)
    label(ax, 77.0, 31.6, "没有任何检查", fs=7.0, color=GREY)

    box(ax, 31.0, 11.0, 38.0, 9.6, fc=PALE_WARN, ec="#d8b7a8")
    label(ax, 50.0, 17.4, "sink：system / SQL 执行", fs=8.8, color=WARN)
    label(ax, 50.0, 13.5, "污点在这里被解释成语法", fs=7.0, color=WARN)

    arrow(ax, (41.0, 44.8), (25.0, 38.8))
    arrow(ax, (59.0, 44.8), (75.0, 38.8))
    arrow(ax, (25.0, 28.8), (43.0, 20.8))
    arrow(ax, (75.0, 28.8), (57.0, 20.8))

    label(ax, 5.0, 22.6, "转义规则与 sink 的", fs=7.0, color=WARN, ha="left")
    label(ax, 5.0, 19.4, "解析规则不一致", fs=7.0, color=WARN, ha="left")
    label(ax, 95.0, 22.6, "污点原样到达", fs=7.0, color=WARN, ha="right")

    rect(ax, 1.0, 2.0, 98.0, 5.6, fc="#f7f8f6")
    label(ax, 50.0, 4.8, "污点分析回答“数据能不能流过去”，不回答“流过去能不能被利用”",
          fs=7.2, color=SOFT)
    return save(fig, "13", "taint-flow.png")


if __name__ == "__main__":
    symbolic_tree()
    taint_flow()
