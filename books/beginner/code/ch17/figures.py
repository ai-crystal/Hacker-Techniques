# -*- coding: utf-8 -*-
"""第十七章插图：跨气隙传播、四个案例的信任链断点。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                    PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label, rect,
                    save, setup)


def stuxnet_airgap():
    """从外部网络到离心机的六跳，中间隔着一条气隙。"""
    fig, ax = setup(5.3, 3.2)
    h = 13.0
    ya, yb = 40.0, 10.0

    nodes = [
        (1.0, ya, 27.0, "外部网络", "供应商与承包商", PALE),
        (36.0, ya, 27.0, "工程师笔记本", "被 U 盘感染", PALE),
        (73.0, ya, 25.0, "内网主机", "Windows · WinCC", PALE),
        (73.0, yb, 25.0, "四个 0 日漏洞", "提权、伪装、注入", PALE_WARN),
        (36.0, yb, 27.0, "S7-315/417 PLC", "输出频率被改写", PALE_BLUE),
        (1.0, yb, 27.0, "离心机", "约 1000 台受损", PALE_WARN),
    ]
    for x, y, w, name, note, fc in nodes:
        box(ax, x, y, w, h, fc=fc, ec=LINE)
        label(ax, x + w / 2, y + h - 4.6, name, fs=8.2, color=INK,
              weight="bold")
        label(ax, x + w / 2, y + 4.0, note, fs=6.9, color=GREY)

    arrow(ax, (28.0, ya + 6.5), (36.0, ya + 6.5))
    arrow(ax, (63.0, ya + 6.5), (73.0, ya + 6.5))
    arrow(ax, (85.5, ya - 0.4), (85.5, yb + h + 0.4))
    arrow(ax, (73.0, yb + 6.5), (63.0, yb + 6.5))
    arrow(ax, (36.0, yb + 6.5), (28.0, yb + 6.5))

    ax.plot([68.0, 68.0], [7.0, 57.0], color=ACCENT_2, lw=1.0,
            ls=(0, (4, 3)), zorder=1)
    label(ax, 68.0, 33.0, "气隙", fs=7.4, color=ACCENT,
          bbox=dict(fc="white", ec="none", pad=1.8))
    label(ax, 68.0, 49.8, "U 盘", fs=7.0, color=WARN,
          bbox=dict(fc="white", ec="none", pad=1.0))

    label(ax, 50.0, 3.0, "四个 0 日漏洞分别用于传播、提权和伪装",
          fs=7.0, color=GREY)
    return save(fig, "17", "stuxnet-airgap.png")


def trust_chain_cases():
    """四个案例各自击穿信任链的哪一环。"""
    fig, ax = setup(5.3, 3.0)
    cols = ["物理隔离", "更新通道", "代码实现", "运维补丁"]
    xs = [26.0, 44.5, 63.0, 81.5]
    w = 16.5
    h = 8.0

    box(ax, 1.0, 45.0, 23.0, 8.0, fc=PALE_2, ec=LINE)
    label(ax, 12.5, 49.0, "时间与事件", fs=7.4, color=SOFT)
    for c, x in zip(cols, xs):
        box(ax, x, 45.0, w, h, fc=PALE_2, ec=LINE)
        label(ax, x + w / 2, 49.0, c, fs=7.4, color=SOFT)

    rows = [
        ("Stuxnet", "2010", 0),
        ("WannaCry", "2017", 3),
        ("SolarWinds", "2020", 1),
        ("Log4Shell", "2021", 2),
    ]
    marks = {0: "U 盘带入", 3: "未打补丁", 1: "植入更新包", 2: "JNDI 查找"}
    ys = [35.0, 26.0, 17.0, 8.0]
    for (name, year, hit), y in zip(rows, ys):
        box(ax, 1.0, y, 23.0, h, fc="white", ec=LINE)
        label(ax, 3.6, y + h / 2 + 1.6, name, fs=7.6, color=INK, ha="left",
              weight="bold")
        label(ax, 3.6, y + h / 2 - 2.2, year, fs=6.6, color=GREY, ha="left")
        for i, x in enumerate(xs):
            if i == hit:
                box(ax, x, y, w, h, fc=PALE_WARN, ec=WARN, lw=0.9)
                label(ax, x + w / 2, y + h / 2, marks[i], fs=7.0, color=WARN)
            else:
                box(ax, x, y, w, h, fc="white", ec="#dedcd4", lw=0.7)

    rect(ax, 26.0, 2.2, 3.2, 2.6, fc=PALE_WARN, ec=WARN, lw=0.9)
    label(ax, 31.0, 3.5, "被击穿的那一环", fs=7.0, color=GREY, ha="left")
    return save(fig, "17", "trust-chain-cases.png")


if __name__ == "__main__":
    stuxnet_airgap()
    trust_chain_cases()
