# -*- coding: utf-8 -*-
"""第二十九章插图：CVSS 向量与公告研判流程。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def cvss_vector():
    """CVSS 3.1 基础向量的六个格子。"""
    fig, ax = setup(5.3, 3.5)
    label(ax, 2.0, 62.0, "八个度量描述的是漏洞本身，暴露面和数据价值不在其中",
          fs=7.0, color=GREY, ha="left")
    label(ax, 2.0, 57.8, "同一份向量在不同环境里，风险可以差一个数量级",
          fs=6.8, color=GREY, ha="left")

    cells = [
        (2.0, 32.0, "AV", "攻击途径",
         ["N 网络　A 相邻", "L 本地　P 物理"]),
        (35.5, 32.0, "AC", "攻击复杂度",
         ["L 低，稳定可复现", "H 高，需特定条件"]),
        (69.0, 32.0, "PR", "所需权限",
         ["N 无　L 普通用户", "H 管理员"]),
        (2.0, 5.0, "UI", "用户交互",
         ["N 不需要交互", "R 需要受害者点一下"]),
        (35.5, 5.0, "S", "影响范围",
         ["U 不越界", "C 越界（逃逸类）"]),
        (69.0, 5.0, "CIA", "三要素",
         ["C 机密　I 完整　A 可用", "H 全失　L 部分　N 无"]),
    ]
    for x, y, abbr, name, lines in cells:
        box(ax, x, y, 30.0, 21.5, fc=PALE, ec=LINE, lw=0.9)
        label(ax, x + 2.2, y + 16.8, abbr, fs=8.0, color=ACCENT, ha="left",
              weight="bold")
        label(ax, x + 9.4 if len(abbr) < 3 else x + 10.2, y + 16.8, name,
              fs=7.0, color=INK, ha="left")
        for i, text in enumerate(lines):
            label(ax, x + 2.2, y + 10.8 - i * 5.4, text, fs=6.3, color=SOFT,
                  ha="left")

    return save(fig, "29", "cvss-vector.png")


def triage_flow():
    """四道门：从公告到结论。"""
    fig, ax = setup(5.3, 3.6)
    gates = [
        (50.0, "①　我们用这个组件吗", "不受影响，留档"),
        (39.0, "②　版本在受影响区间吗", "版本不在区间，注意 backport"),
        (28.0, "③　配置前提成立吗", "条件不成立，记下证据"),
        (17.0, "④　网络与权限够得着吗", "打不到，记为不可达"),
    ]
    for y, question, answer in gates:
        box(ax, 6.0, y, 44.0, 8.2, fc=PALE_BLUE, ec="#b6c4d2", lw=0.9)
        label(ax, 8.0, y + 4.1, question, fs=7.2, color=BLUE, ha="left")
        box(ax, 56.0, y + 0.8, 40.0, 6.6, fc=PALE_WARN, ec="#d8c3b8", lw=0.9)
        label(ax, 58.0, y + 4.1, answer, fs=6.5, color=WARN, ha="left")
        arrow(ax, (50.0, y + 4.1), (55.6, y + 4.1), color=GREY, lw=0.9)
        label(ax, 52.8, y + 6.4, "否", fs=6.2, color=GREY)

    for y_top, y_bot in [(50.0, 47.4), (39.0, 36.4), (28.0, 25.4)]:
        arrow(ax, (28.0, y_top), (28.0, y_bot), lw=1.0)
        label(ax, 30.2, (y_top + y_bot) / 2, "是", fs=6.2, color=GREY,
              ha="left")

    arrow(ax, (28.0, 17.0), (28.0, 11.7), lw=1.0)
    label(ax, 30.2, 14.3, "是", fs=6.2, color=GREY, ha="left")

    box(ax, 6.0, 3.4, 90.0, 8.3, fc=PALE, ec=LINE, lw=1.0)
    label(ax, 8.2, 9.4, "处置强度看暴露面和数据", fs=7.4, color=INK,
          ha="left", weight="bold")
    label(ax, 8.2, 5.9, "公网可达且有敏感数据　→　今晚；仅内网可达　→　本周期；"
                        "隔离环境　→　排期", fs=6.6, color=SOFT, ha="left")

    return save(fig, "29", "triage-flow.png")


if __name__ == "__main__":
    cvss_vector()
    triage_flow()
