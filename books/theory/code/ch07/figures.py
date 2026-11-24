# -*- coding: utf-8 -*-
"""第七章插图：用户态到内核态的检查点，以及内核提权的三条路径。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def trust_boundary():
    fig, ax = setup(5.3, 3.55)
    rect(ax, 0, 46.5, 100, 19.5, fc="#fafbf9")
    rect(ax, 0, 0, 100, 46.5, fc="#eaf0ef")

    ax.plot([0, 100], [46.5, 46.5], color="#8fa3a1", lw=0.9,
            ls=(0, (4, 2)), zorder=4)
    label(ax, 96.0, 48.6, "特权级边界", fs=6.8, color="#5d7573", ha="right")

    box(ax, 26.0, 51.0, 48.0, 10.0, fc="white", ec=LINE)
    label(ax, 50.0, 57.4, "read(fd, buf, len)", fs=8.6, color=INK,
          weight="bold")
    label(ax, 50.0, 53.2, "buf 指向自己进程的缓冲区", fs=6.9, color=GREY)

    checks = [
        ("系统调用入口", "从用户栈换到内核栈", 36.4, PALE),
        ("指针与范围校验", "access_ok 判范围", 25.6, PALE),
        ("长度与类型检查", "溢出、截断、符号", 14.8, PALE),
        ("权限与生命周期", "capable 与引用计数", 4.0, PALE_WARN),
    ]
    for name, note, y, fc in checks:
        ec = "#d6c9bf" if fc == PALE_WARN else LINE
        box(ax, 26.0, y, 48.0, 7.0, fc=fc, ec=ec)
        label(ax, 28.6, y + 3.5, name, fs=7.6, color=INK, ha="left",
              weight="bold")
        label(ax, 71.4, y + 3.5, note, fs=6.5, color=GREY, ha="right")

    arrow(ax, (50.0, 50.8), (50.0, 43.4), color=WARN, lw=1.2)
    for y in (36.4, 25.6, 14.8):
        arrow(ax, (50.0, y - 0.2), (50.0, y - 3.8), color=ACCENT_2, lw=1.0,
              ms=7)

    notes = ["入口只此一处", "指针可能是假的", "长度可能被绕过", "权限可能给宽了"]
    for note, y in zip(notes, (39.9, 29.1, 18.3, 7.5)):
        label(ax, 78.0, y, note, fs=6.9, color=SOFT, ha="left")

    label(ax, 78.0, 57.6, "每个检查点", fs=6.9, color=GREY, ha="left")
    label(ax, 78.0, 54.0, "都对应一类漏洞", fs=6.9, color=GREY, ha="left")
    label(ax, 3.0, 61.0, "用户态", fs=8.0, color=SOFT, ha="left", weight="bold")
    label(ax, 3.0, 42.4, "内核态", fs=8.0, color=ACCENT, ha="left", weight="bold")
    return save(fig, "07", "trust-boundary.png")


def privesc_paths():
    fig, ax = setup(5.3, 3.2)
    box(ax, 2.0, 21.0, 24.0, 14.0, fc="white", ec=LINE)
    label(ax, 14.0, 30.6, "本地普通用户", fs=8.2, color=INK, weight="bold")
    label(ax, 14.0, 25.6, "已能执行代码", fs=6.8, color=GREY)

    lanes = [("逻辑漏洞", "条件判断写错，权限直接到手", 41.0, PALE_BLUE,
              "#b6c4d2", BLUE, 47.0, 36.0),
             ("内存破坏", "悬垂指针、越界写，改内核对象", 23.0, PALE,
              LINE, ACCENT, 28.5, 29.0),
             ("配置不当", "sudo 规则、挂载选项、权限位", 5.0, PALE_WARN,
              "#dcc3b6", WARN, 10.0, 22.5)]
    for name, note, y, fc, ec, color, cy, ey in lanes:
        box(ax, 36.0, y, 34.0, 12.0, fc=fc, ec=ec)
        label(ax, 53.0, y + 7.8, name, fs=8.2, color=color, weight="bold")
        label(ax, 53.0, y + 3.0, note, fs=6.5, color=GREY)
        arrow(ax, (26.4, 28.0), (35.6, cy), color=ACCENT_2, lw=1.0, ms=7)
        arrow(ax, (70.4, cy), (79.6, ey), color=ACCENT_2, lw=1.0, ms=7)

    box(ax, 80.0, 17.0, 18.0, 24.0, fc="white", ec=LINE)
    label(ax, 89.0, 34.0, "内核态", fs=8.0, color=INK, weight="bold")
    label(ax, 89.0, 28.5, "任意内存", fs=7.0, color=GREY)
    label(ax, 89.0, 24.5, "与设备", fs=7.0, color=GREY)
    return save(fig, "07", "privesc-paths.png")


if __name__ == "__main__":
    trust_boundary()
    privesc_paths()
