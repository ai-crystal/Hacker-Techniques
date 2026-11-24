# -*- coding: utf-8 -*-
"""第一章插图：实验环境拓扑、快照与回滚决策流程。

画布宽度统一取 5.3 英寸，与版心宽度接近。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def lab_topology():
    fig, ax = setup(5.3, 3.4)

    # 真实网络
    box(ax, 6, 57, 88, 6.4, fc=PALE_WARN, ec=LINE)
    label(ax, 50, 60.2, "真实网络　家用路由器 192.168.1.1", fs=8.0, color=SOFT)

    # 隔离边界：虚线在标签处断开，文字不压线
    for x0, x1 in ((6, 66), (82, 94)):
        ax.plot([x0, x1], [54, 54], color=WARN, lw=1.0, ls=(0, (5, 2.5)),
                zorder=2)
    label(ax, 74, 54, "隔离边界", fs=7.2, color=WARN, weight="bold")

    # NAT 交换机
    arrow(ax, (50, 56.8), (50, 51.4))
    box(ax, 28, 43, 44, 8.2, fc=PALE_BLUE, ec="#b6c4d2")
    label(ax, 50, 48.6, "NAT 虚拟交换机", fs=8.4, color=BLUE, weight="bold")
    label(ax, 50, 45.4, "vmnet8 · 唯一出网路径", fs=6.8, color=BLUE)

    # 仅主机交换机
    box(ax, 6, 32, 88, 8.2, fc=PALE, ec=LINE)
    label(ax, 50, 37.6, "仅主机虚拟交换机 / 内部网络", fs=8.4, color=INK,
          weight="bold")
    label(ax, 50, 34.4, "10.10.10.0/24　攻击流量全部落在这一段", fs=6.8,
          color=GREY)

    # 三台虚拟机
    vms = [
        (6, "Kali", ["eth0 → NAT", "eth1 → 仅主机"], 10.0),
        (38, "Linux 靶机", ["10.10.10.20", "只有一块网卡"], None),
        (70, "Windows 靶机", ["10.10.10.30", "只有一块网卡"], None),
    ]
    for x, name, notes, _ in vms:
        box(ax, x, 4, 24, 16, fc="white", ec=LINE)
        label(ax, x + 12, 16.2, name, fs=8.6, color=INK, weight="bold")
        label(ax, x + 12, 11.6, notes[0], fs=7.0, color=SOFT)
        label(ax, x + 12, 7.6, notes[1], fs=7.0, color=GREY)
        arrow(ax, (x + 12, 20.4), (x + 12, 31.6))

    # 攻击机 eth0 绕到左侧，走上 NAT
    ax.plot([6, 2.5], [10, 10], color=ACCENT, lw=1.1, zorder=3,
            solid_capstyle="butt")
    ax.plot([2.5, 2.5], [10, 47], color=ACCENT, lw=1.1, zorder=3)
    ax.plot([2.5, 26], [47, 47], color=ACCENT, lw=1.1, zorder=3)
    arrow(ax, (26, 47), (27.8, 47))
    label(ax, 15, 49.8, "攻击机唯一出网路径", fs=6.6, color=ACCENT)

    label(ax, 50, 1.4, "靶机没有第二块网卡，也就没有第二条出路",
          fs=6.8, color=GREY)
    return save(fig, "01", "lab-topology.png")


def snapshot_decision():
    fig, ax = setup(5.3, 3.4)

    box(ax, 4, 55.5, 48, 7, fc=PALE, ec=LINE)
    label(ax, 28, 59, "动手之前，先想清楚这一步要不要撤回", fs=7.6, color=INK)

    gates = [
        (43, "这次改动需要事后回滚？", "否", "直接做，结束前打基线快照", "是"),
        (31, "快照链已经超过三层？", "是", "克隆全量副本，另开一条链", "否"),
        (19, "机器上有数据库或加密卷？", "是", "先停服务，再取关机快照", "否"),
    ]
    for y, text, hmark, side, vmark in gates:
        box(ax, 4, y, 48, 8, fc=PALE_BLUE, ec="#b6c4d2")
        label(ax, 28, y + 4, text, fs=7.6, color=BLUE)
        box(ax, 60, y, 36, 8, fc=PALE_2, ec=LINE)
        label(ax, 78, y + 4, side, fs=7.0, color=SOFT)
        arrow(ax, (52, y + 4), (59.8, y + 4))
        label(ax, 56, y + 5.8, hmark, fs=7.0, color=WARN)
        y_end = 14.4 if y < 20 else y - 3.6
        arrow(ax, (28, y - 0.4), (28, y_end))
        label(ax, 29.6, (y - 0.4 + y_end) / 2, vmark, fs=7.0, color=WARN,
              ha="left")

    box(ax, 4, 4, 48, 10, fc=PALE_WARN, ec="#d8b6a6")
    label(ax, 28, 10.6, "恢复之后校验三样", fs=7.6, color=WARN, weight="bold")
    label(ax, 28, 7.0, "网卡地址 · 服务状态 · 系统时钟", fs=7.0, color=SOFT)

    arrow(ax, (28, 55.1), (28, 51.4))
    label(ax, 29.6, 53.2, "是", fs=7.0, color=WARN, ha="left")

    label(ax, 50, 1.6, "每个节点都写进实验日志：时间、快照名、做了什么",
          fs=6.6, color=GREY)
    return save(fig, "01", "snapshot-decision.png")


if __name__ == "__main__":
    lab_topology()
    snapshot_decision()
