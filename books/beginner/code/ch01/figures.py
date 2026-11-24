# -*- coding: utf-8 -*-
"""第一章插图：处理器、抽象层次、进程空间、系统调用。

画布宽度统一取 5.3 英寸，与版心宽度接近，图内字号与正文字号基本一一对应。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                    PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label, rect,
                    save, setup)


def instruction_cycle():
    fig, ax = setup(5.3, 2.35)
    y0, h, w = 15, 14, 20.0
    stages = [("取指", "按 PC 读指令", 2.0), ("译码", "识别操作数", 27.0),
              ("执行", "运算或访存", 52.0), ("写回", "结果写回", 77.0)]
    for name, note, x in stages:
        box(ax, x, y0, w, h, fc=PALE, ec=LINE)
        label(ax, x + w / 2, y0 + h - 4.6, name, fs=10, color=INK, weight="bold")
        label(ax, x + w / 2, y0 + 4.2, note, fs=7.4, color=GREY)
    for x in (2.0, 27.0, 52.0):
        arrow(ax, (x + w + 0.4, y0 + h / 2), (x + w + 4.6, y0 + h / 2))

    box(ax, 2.0, 33.0, 30.0, 9.4, fc=PALE_BLUE, ec="#b6c4d2")
    label(ax, 17.0, 37.7, "内存：指令与数据", fs=8, color=BLUE)
    arrow(ax, (12.0, 32.6), (12.0, y0 + h + 0.4))

    box(ax, 72.0, 33.0, 26.0, 9.4, fc=PALE, ec=LINE)
    label(ax, 85.0, 37.7, "寄存器组", fs=8, color=SOFT)
    arrow(ax, (85.0, 32.6), (85.0, y0 + h + 0.4))

    # 回路走线放在方框下方，避免压到框内文字
    ax.plot([87.0, 87.0], [y0 - 0.6, 5.6], color=ACCENT_2, lw=1.1,
            ls=(0, (5, 2.5)), zorder=2)
    ax.plot([87.0, 12.0], [5.6, 5.6], color=ACCENT_2, lw=1.1,
            ls=(0, (5, 2.5)), zorder=2)
    arrow(ax, (12.0, 5.6), (12.0, y0 - 0.6), color=ACCENT_2, lw=1.1,
          ls=(0, (5, 2.5)))
    return save(fig, "01", "instruction-cycle.png")


def abstraction_layers():
    fig, ax = setup(5.3, 3.15)
    rows = [
        ("Python 程序", "解释器逐条执行", PALE_2),
        ("C 源代码", "编译器翻译", PALE),
        ("汇编指令", "汇编器翻译", PALE),
        ("机器码", "处理器直接识别", PALE_BLUE),
        ("晶体管与逻辑门", "电压变化", PALE_WARN),
    ]
    h, gap = 9.4, 2.4
    y = 0.8
    for name, note, fc in reversed(rows):
        box(ax, 1.5, y, 85.0, h, fc=fc, ec=LINE)
        label(ax, 4.5, y + h / 2, name, fs=8.8, color=INK, ha="left", weight="bold")
        label(ax, 84.0, y + h / 2, note, fs=7.6, color=GREY, ha="right")
        y += h + gap
    arrow(ax, (91.5, 57.0), (91.5, 2.6), color=ACCENT, lw=1.0)
    return save(fig, "01", "abstraction-layers.png")


def process_space():
    fig, ax = setup(5.3, 3.4)
    names = ["进程 A", "进程 B", "进程 C"]
    segs = [("栈", 9.6, PALE), ("堆", 7.0, PALE_2), ("数据", 6.2, PALE),
            ("代码", 7.0, PALE_BLUE)]
    w = 25.0
    for i, name in enumerate(names):
        x = 2.0 + i * 31.0
        label(ax, x + w / 2, 58.0, name, fs=9, color=ACCENT, weight="bold")
        top = 52.0
        for seg, sh, fc in segs:
            box(ax, x, top - sh, w, sh, fc=fc, ec="#d2d2cc", lw=0.8)
            label(ax, x + w / 2, top - sh / 2, seg, fs=7.8, color=SOFT)
            top -= sh + 0.9
        if i == 0:
            label(ax, x + w + 1.6, 49.0, "高地址", fs=6.2, color=GREY, ha="left")
            label(ax, x + w + 1.6, 16.0, "低地址", fs=6.2, color=GREY, ha="left")
    box(ax, 2.0, 5.4, 88.0, 8.6, fc="#dfe7e6", ec="#b7c6c4")
    label(ax, 46.0, 9.7, "操作系统内核：页表、调度、设备驱动", fs=8.2, color=ACCENT)
    label(ax, 91.0, 1.4, "物理内存由内核统一分配", fs=6.4, color=GREY, ha="right")
    return save(fig, "01", "process-space.png")


def user_kernel():
    fig, ax = setup(5.3, 3.32)
    rect(ax, 0, 34, 100, 28, fc="#fafbf9")
    rect(ax, 0, 0, 100, 33, fc="#eaf0ef")
    label(ax, 3.0, 58.5, "用户态", fs=8.6, color=SOFT, ha="left", weight="bold")
    label(ax, 3.0, 28.0, "内核态", fs=8.6, color=ACCENT, ha="left", weight="bold")

    box(ax, 12.0, 41.0, 46.0, 13.0, fc="white", ec=LINE)
    label(ax, 35.0, 50.2, "应用程序", fs=9.4, color=INK, weight="bold")
    label(ax, 35.0, 45.0, "没有特权，访存受限", fs=7.4, color=GREY)

    box(ax, 12.0, 7.0, 46.0, 14.0, fc="white", ec=LINE)
    label(ax, 35.0, 17.2, "内核", fs=9.4, color=ACCENT, weight="bold")
    label(ax, 35.0, 11.8, "检查参数：指针、长度、权限", fs=7.4, color=GREY)

    arrow(ax, (24.0, 40.4), (24.0, 21.6), color=WARN)
    arrow(ax, (43.0, 21.6), (43.0, 40.4), color=ACCENT)

    ax.plot([0, 100], [33, 33], color="#8fa3a1", lw=0.9, ls=(0, (4, 2)), zorder=4)
    label(ax, 78.0, 33.0, "特权级边界", fs=7.0, color="#5d7573",
          bbox=dict(fc="#f2f5f4", ec="none", pad=1.4))

    label(ax, 22.4, 28.4, "陷入指令", fs=7.2, color=WARN, ha="right",
          bbox=dict(fc="#eaf0ef", ec="none", pad=1.0))
    label(ax, 44.6, 28.4, "返回结果", fs=7.2, color=ACCENT, ha="left",
          bbox=dict(fc="#eaf0ef", ec="none", pad=1.0))

    label(ax, 63.0, 47.0, "跨边界的每个参数", fs=7.4, color=SOFT, ha="left")
    label(ax, 63.0, 42.0, "都要重新验证一次", fs=7.4, color=SOFT, ha="left")
    label(ax, 63.0, 17.4, "漏掉一个条件", fs=7.4, color=WARN, ha="left")
    label(ax, 63.0, 12.4, "就是内核漏洞", fs=7.4, color=WARN, ha="left")
    return save(fig, "01", "user-kernel.png")


if __name__ == "__main__":
    instruction_cycle()
    abstraction_layers()
    process_space()
    user_kernel()
