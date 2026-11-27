# -*- coding: utf-8 -*-
"""第十九章插图：虚拟机与容器的隔离边界、逃逸路径的三类来源。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)

BLUE_EDGE = "#b6c4d2"
WARM_EDGE = "#d8b7a8"


def isolation_boundary():
    fig, ax = setup(5.3, 3.6)

    # 列标题
    label(ax, 25.0, 63.6, "虚拟机", fs=10.2, color=INK, weight="bold")
    label(ax, 25.0, 60.2, "每台虚拟机一套内核", fs=6.6, color=GREY)
    label(ax, 75.0, 63.6, "容器", fs=10.2, color=INK, weight="bold")
    label(ax, 75.0, 60.2, "所有容器共用宿主内核", fs=6.6, color=GREY)

    rows = (
        (50.0, 8.5),
        (36.5, 9.5),
        (21.0, 9.5),
        (7.0, 9.0),
    )

    left = (
        ("用户进程", "见到的是一台完整机器", PALE_2, LINE, None),
        ("Guest 内核", "独立的内核副本，自己管页表", PALE, LINE, None),
        ("Hypervisor", "截获敏感指令，管第二层翻译", PALE_BLUE, BLUE_EDGE, None),
        ("CPU · 内存 · 设备", "", PALE_2, LINE, None),
    )
    right = (
        ("用户进程", "见到的是一个根目录和几个数字", PALE_2, LINE, None),
        ("容器", "namespace 给视图，cgroup 给配额", PALE, ACCENT_2, (0, (4, 2.4))),
        ("宿主内核", "sys_call_table 只有一份", PALE_BLUE, BLUE_EDGE, None),
        ("CPU · 内存 · 设备", "", PALE_2, LINE, None),
    )

    for (y, h), (t1, t2, fc, ec, dash) in zip(rows, left):
        p = box(ax, 5.0, y, 40.0, h, fc=fc, ec=ec, lw=1.0)
        if dash:
            p.set_linestyle(dash)
        if t2:
            label(ax, 25.0, y + h * 0.63, t1, fs=8.8, color=INK, weight="bold")
            label(ax, 25.0, y + h * 0.28, t2, fs=6.6, color=GREY)
        else:
            label(ax, 25.0, y + h / 2, t1, fs=7.8, color=SOFT)

    for (y, h), (t1, t2, fc, ec, dash) in zip(rows, right):
        p = box(ax, 55.0, y, 40.0, h, fc=fc, ec=ec, lw=1.0)
        if dash:
            p.set_linestyle(dash)
        if t2:
            label(ax, 75.0, y + h * 0.63, t1, fs=8.8, color=INK, weight="bold")
            label(ax, 75.0, y + h * 0.28, t2, fs=6.6, color=GREY)
        else:
            label(ax, 75.0, y + h / 2, t1, fs=7.8, color=SOFT)

    # 左侧：硬件强制的边界
    ax.plot([5.0, 45.0], [30.5, 30.5], color=ACCENT, lw=2.6, zorder=5,
            solid_capstyle="butt")
    label(ax, 5.0, 33.4, "越界只能走 VM exit，由 CPU 强制", fs=6.5, color=ACCENT,
          ha="left")

    # 右侧：没有可跨越的边界
    label(ax, 75.0, 34.5, "虚线只是同一层内核里的一个分支", fs=6.5, color=WARN,
          ha="center")

    return save(fig, "19", "isolation-boundary.png")


def escape_paths():
    fig, ax = setup(5.3, 3.0)

    box(ax, 68.0, 9.0, 28.0, 46.0, fc=PALE_WARN, ec=WARM_EDGE)
    label(ax, 82.0, 48.0, "宿主机", fs=9.6, color=WARN, weight="bold")
    ax.plot([72.0, 92.0], [43.4, 43.4], color=WARM_EDGE, lw=0.9)
    for y, t in ((38.0, "读写任意文件"), (32.0, "看到所有进程"),
                 (26.0, "控制其他容器"), (20.0, "改内核参数")):
        label(ax, 82.0, y, t, fs=7.0, color=WARN)

    lanes = (
        (44.0, "配置类", "privileged、hostPath、挂 docker.sock",
         "前提是 Pod 拿到了写宿主目录的权限", 48.5),
        (28.5, "内核类", "共用内核里的一次越界写或逻辑漏洞",
         "前提是版本范围内有可触发的漏洞", 33.0),
        (13.0, "运行时类", "runc、containerd、CRI-O 自身的漏洞",
         "前提是容器进程能左右运行时的行为", 17.5),
    )

    for y, t1, t2, cond, cy in lanes:
        box(ax, 5.0, y, 51.0, 9.0, fc=PALE, ec=LINE, lw=1.0)
        label(ax, 8.0, y + 6.0, t1, fs=8.8, color=INK, weight="bold", ha="left")
        label(ax, 8.0, y + 2.6, t2, fs=6.6, color=GREY, ha="left")
        label(ax, 6.0, y - 2.7, cond, fs=6.4, color=SOFT, ha="left")
        arrow(ax, (56.2, cy), (67.6, cy), color=ACCENT)

    return save(fig, "19", "escape-paths.png")


if __name__ == "__main__":
    isolation_boundary()
    escape_paths()
