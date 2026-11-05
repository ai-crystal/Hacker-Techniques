# -*- coding: utf-8 -*-
"""第八章插图：竞态时间线、TOCTOU 符号链接、锁的范围。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                    PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label, rect,
                    save, setup)


def race_timeline():
    fig, ax = setup(5.3, 3.4)
    box(ax, 40.0, 12.0, 20.0, 44.0, fc="#f2f6f8", ec="#bcc9d2")
    label(ax, 50.0, 52.5, "count", fs=7.6, color=BLUE)
    label(ax, 50.0, 47.5, "100", fs=7.6, color=BLUE)
    label(ax, 50.0, 17.5, "101", fs=7.6, color=BLUE)

    ax.plot([22.0, 22.0], [50.0, 14.0], color="#c8c8c2", lw=1.0)
    ax.plot([78.0, 78.0], [50.0, 14.0], color="#c8c8c2", lw=1.0)
    label(ax, 22.0, 55.0, "进程 A", fs=8.0, color=INK, weight="bold")
    label(ax, 78.0, 55.0, "进程 B", fs=8.0, color=INK, weight="bold")

    steps = [(44.0, 22.0, 39.4, "读 100"),
             (37.0, 78.0, 60.6, "读 100"),
             (30.0, 22.0, 39.4, "写 101"),
             (23.0, 78.0, 60.6, "写 101")]
    for y, x1, x2, text in steps:
        arrow(ax, (x1, y), (x2, y), color=ACCENT, lw=1.1, ms=7)
        label(ax, (x1 + x2) / 2, y + 1.9, text, fs=6.8, color=SOFT)

    label(ax, 50.0, 6.4, "两次加一，只留下一次效果", fs=7.4, color=WARN)
    return save(fig, "08", "race-timeline.png")


def toctou_symlink():
    fig, ax = setup(5.3, 2.7)
    steps = [("access 检查", "普通文件", 2.0, 21.0, PALE),
             ("攻击者替换", "改成符号链接", 27.0, 22.0, PALE_WARN),
             ("fopen 打开", "跟着链接走", 53.0, 22.0, PALE_BLUE),
             ("以 root 写入", "/etc/shadow", 79.0, 19.0, "#f0e2e2")]
    y, h = 34.0, 16.0
    for name, note, x, w, fc in steps:
        box(ax, x, y, w, h, fc=fc, ec=LINE)
        label(ax, x + w / 2, y + h - 5.4, name, fs=7.4, color=INK, weight="bold")
        label(ax, x + w / 2, y + 5.4, note, fs=6.4, color=GREY)
    for x in (23.4, 49.4, 75.4):
        arrow(ax, (x, y + h / 2), (x + 3.2, y + h / 2))
    label(ax, 50.0, 24.0, "缝隙就在这两步之间", fs=7.2, color=WARN)
    label(ax, 50.0, 15.0, "攻击者反复尝试，直到正好插进这个窗口", fs=7.0, color=GREY)
    label(ax, 50.0, 6.0, "修法：用 O_CREAT|O_EXCL 一步完成创建与打开", fs=7.0, color=ACCENT)
    return save(fig, "08", "toctou-symlink.png")


def lock_scope():
    fig, ax = setup(5.3, 2.6)
    steps = ["读 count", "加一", "写回"]
    rows = [("正确的锁范围", 3, ACCENT, 34.0), ("错误的锁范围", 1, WARN, 12.0)]
    for text, covered, color, y in rows:
        for i, name in enumerate(steps):
            x = 26.0 + i * 24.0
            fc = PALE if i < covered else PALE_WARN
            box(ax, x, y, 18.0, 10.0, fc=fc, ec=LINE)
            label(ax, x + 9.0, y + 5.0, name, fs=7.4, color=SOFT)
        xa = 25.4
        xb = 25.4 + covered * 24.0 - 6.6
        ax.plot([xa, xb], [y - 3.4, y - 3.4], color=color, lw=1.2)
        ax.plot([xa, xa], [y - 3.4, y - 0.4], color=color, lw=1.2)
        ax.plot([xb, xb], [y - 3.4, y - 0.4], color=color, lw=1.2)
        label(ax, 22.0, y + 5.0, text, fs=6.8, color=color, ha="right")
    label(ax, 50.0, 3.0, "锁只保护了读取，另外两步仍可被插入", fs=7.0, color=WARN)
    return save(fig, "08", "lock-scope.png")


if __name__ == "__main__":
    race_timeline()
    toctou_symlink()
    lock_scope()
