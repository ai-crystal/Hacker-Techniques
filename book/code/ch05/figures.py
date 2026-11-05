# -*- coding: utf-8 -*-
"""第五章插图：安全三目标、漏洞生命周期、利用链条。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                    PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label, rect,
                    save, setup)


def cia_triad():
    fig, ax = setup(5.3, 3.0)
    top = (50.0, 42.0)
    left = (16.0, 10.0)
    right = (84.0, 10.0)
    ax.plot([top[0], left[0], right[0], top[0]],
            [top[1], left[1], right[1], top[1]], color="#c9cfcd", lw=1.0)
    ax.plot([top[0]], [top[1]], "o", ms=6, color=ACCENT, zorder=4)
    label(ax, top[0], top[1] + 10.6, "机密性", fs=9.2, color=INK, weight="bold")
    label(ax, top[0], top[1] + 5.8, "只让该看的人看到", fs=7.0, color=GREY)
    for (x, y), name, note in [(left, "完整性", "不被非法改动"),
                               (right, "可用性", "需要时能用")]:
        ax.plot([x], [y], "o", ms=6, color=ACCENT, zorder=4)
        label(ax, x, y - 5.6, name, fs=9.2, color=INK, weight="bold")
        label(ax, x, y - 10.4, note, fs=7.0, color=GREY)
    label(ax, 50.0, 26.0, "安全", fs=10.5, color=ACCENT, weight="bold")
    label(ax, 50.0, 20.4, "三者此消彼长，很难同时拉满", fs=7.2, color=GREY)
    return save(fig, "05", "cia-triad.png")


def vuln_lifecycle():
    fig, ax = setup(5.3, 2.9)
    ax.plot([6.0, 94.0], [38.0, 38.0], color="#c4c9c7", lw=1.4, zorder=1)
    stages = [
        (12.0, "被发现", ("崩溃", "模糊测试")),
        (31.0, "确认与编号", ("厂商复现", "分配编号")),
        (50.0, "补丁发布", ("用户开始", "升级")),
        (69.0, "细节公开", ("可利用信息", "出现")),
        (88.0, "大规模利用", ("扫描器", "与蠕虫")),
    ]
    for x, name, notes in stages:
        ax.plot([x], [38.0], "o", ms=6, color=ACCENT, zorder=4)
        label(ax, x, 46.0, name, fs=8.0, color=INK, weight="bold")
        label(ax, x, 23.0, notes[0], fs=6.6, color=GREY)
        label(ax, x, 17.4, notes[1], fs=6.6, color=GREY)
    rect(ax, 49.6, 31.4, 19.8, 3.8, fc=PALE_WARN, ec="none", zorder=2)
    label(ax, 59.5, 33.3, "补丁窗口", fs=6.6, color=WARN, zorder=3)
    return save(fig, "05", "vuln-lifecycle.png")


def exploit_chain():
    fig, ax = setup(5.3, 2.6)
    steps = [("触发漏洞", "构造输入", PALE),
             ("获得原语", "稳定读写", PALE_2),
             ("劫持控制流", "改写返回地址", PALE_BLUE),
             ("落地与维持", "提权、持久化", PALE_WARN)]
    w, gap, y, h = 18.5, 8.0, 24.0, 14.0
    for i, (name, note, fc) in enumerate(steps):
        x = 2.0 + i * (w + gap)
        box(ax, x, y, w, h, fc=fc, ec=LINE)
        label(ax, x + w / 2, y + h - 5.0, name, fs=7.8, color=INK, weight="bold")
        label(ax, x + w / 2, y + 4.8, note, fs=6.6, color=GREY)
        if i < 3:
            arrow(ax, (x + w + 0.6, y + h / 2), (x + w + gap - 0.6, y + h / 2))
    label(ax, 50.0, 15.5, "任何一环断开，整条链就失效", fs=7.4, color=ACCENT)
    label(ax, 50.0, 8.0, "防守方因此在每一环上都布置了检查", fs=7.0, color=GREY)
    return save(fig, "05", "exploit-chain.png")


if __name__ == "__main__":
    cia_triad()
    vuln_lifecycle()
    exploit_chain()
