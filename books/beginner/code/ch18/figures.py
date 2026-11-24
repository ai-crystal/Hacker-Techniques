# -*- coding: utf-8 -*-
"""第十八章插图：分层防御与 3-2-1 备份。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                    PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label, rect,
                    save, setup)


def defense_layers():
    """攻击链的每一步都对应一个检查点。"""
    fig, ax = setup(5.3, 3.35)
    pairs = [
        ("1　收集信息", "不把学号、课表、宿舍号发在公开主页"),
        ("2　投递诱导", "邮件网关拦附件，禁用 Office 宏"),
        ("3　触发执行", "当天打补丁，删掉不用的插件"),
        ("4　提权横移", "最小权限、网络分段、硬件密钥"),
        ("5　取走数据", "3-2-1 备份，日志留到能追溯"),
    ]
    h = 8.0
    step = 11.5
    top = 60.0
    for name, control in pairs:
        y = top - h
        box(ax, 1.0, y, 25.0, h, fc=PALE_WARN, ec="#d8c3b8", lw=0.9)
        label(ax, 3.4, y + h / 2, name, fs=7.6, color=WARN, ha="left")
        ax.plot([26.0, 38.0], [y + h / 2, y + h / 2], color=LINE, lw=0.8,
                ls=(0, (3, 2.4)), zorder=1)
        ax.plot([32.0], [y + h / 2], marker="D", markersize=4.6,
                color=ACCENT, zorder=4)
        box(ax, 38.0, y, 59.0, h, fc=PALE, ec=LINE)
        label(ax, 40.0, y + h / 2, control, fs=7.4, color=INK, ha="left")
        top -= step
    label(ax, 1.0, 2.6, "菱形处为检查点，靠流程维持，不靠注意力",
          fs=7.0, color=GREY, ha="left")
    return save(fig, "18", "defense-layers.png")


def backup_321():
    """3-2-1 备份：三份数据、两种介质、一份异地。"""
    fig, ax = setup(5.3, 2.95)
    box(ax, 2.0, 21.0, 26.0, 14.0, fc=PALE_BLUE, ec="#b6c4d2")
    label(ax, 15.0, 30.4, "在用的数据", fs=8.6, color=BLUE, weight="bold")
    label(ax, 15.0, 25.4, "第 1 份", fs=7.0, color=GREY)

    targets = [
        (38.0, PALE_WARN, WARN, "#dcc4b8", "同机快照", "盘坏了一起消失，不算副本"),
        (21.0, PALE, INK, LINE, "外接硬盘", "第二种介质，平时断开"),
        (4.0, PALE, INK, LINE, "异地或云端", "第三个地点，火灾也带不走"),
    ]
    for y, fc, color, ec, name, note in targets:
        box(ax, 40.0, y, 46.0, 13.0, fc=fc, ec=ec, lw=0.9)
        label(ax, 42.4, y + 8.6, name, fs=8.2, color=color, ha="left",
              weight="bold")
        label(ax, 42.4, y + 4.0, note, fs=6.9, color=GREY, ha="left")

    arrow(ax, (28.4, 30.0), (39.6, 40.6), rad=-0.22, color=GREY, lw=1.0,
          ls=(0, (3, 2.2)))
    arrow(ax, (28.4, 28.0), (39.6, 27.5), lw=1.1)
    arrow(ax, (28.4, 25.0), (39.6, 9.6), rad=0.22, lw=1.1)

    label(ax, 50.0, 1.2, "3 份数据、2 种介质、1 份异地", fs=7.2, color=SOFT)
    return save(fig, "18", "backup-321.png")


if __name__ == "__main__":
    defense_layers()
    backup_321()
