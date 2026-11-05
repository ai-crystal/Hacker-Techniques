# -*- coding: utf-8 -*-
"""第二章插图：地址空间、栈帧、堆块结构。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                    PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label, rect,
                    save, setup)


def address_space():
    fig, ax = setup(5.3, 4.75)
    items = [
        ("内核空间", 79.0, 7.0, "#e6e2dc", "用户态不可访问"),
        ("栈", 63.0, 13.0, PALE, "局部变量、返回地址，向下生长"),
        ("共享库", 46.0, 9.0, PALE_BLUE, "libc 等动态库映射在此"),
        ("堆", 27.0, 10.0, PALE_2, "malloc 分配的内存，向上生长"),
        (".bss", 19.0, 6.0, PALE, "未初始化的全局变量"),
        (".data", 12.0, 6.0, PALE, "已初始化的全局变量"),
        (".text", 3.0, 7.0, PALE_BLUE, "程序机器码，只读可执行"),
    ]
    for name, y, h, fc, note in items:
        box(ax, 18.0, y, 34.0, h, fc=fc, ec=LINE)
        label(ax, 35.0, y + h / 2, name, fs=8.6, color=INK, weight="bold")
        label(ax, 55.0, y + h / 2, note, fs=7.4, color=GREY, ha="left")

    # 生长方向
    arrow(ax, (13.0, 75.4), (13.0, 64.6), color=ACCENT_2, lw=1.0)
    arrow(ax, (13.0, 28.6), (13.0, 36.4), color=ACCENT_2, lw=1.0)
    label(ax, 10.6, 70.0, "向\n下", fs=6.4, color=ACCENT_2, ha="center")
    label(ax, 10.6, 32.5, "向\n上", fs=6.4, color=ACCENT_2, ha="center")
    return save(fig, "02", "address-space.png")


def stack_frame():
    fig, ax = setup(5.3, 4.1)
    rows = [
        ("调用者的栈帧", 62.0, 10.0, "#eceae4"),
        ("调用者压入的参数", 51.0, 9.0, PALE_2),
        ("返回地址", 41.0, 9.0, PALE_WARN),
        ("保存的 rbp", 32.0, 8.0, PALE_BLUE),
        ("局部变量与数组", 14.0, 17.0, PALE),
    ]
    for name, y, h, fc in rows:
        box(ax, 20.0, y, 34.0, h, fc=fc, ec=LINE)
        label(ax, 37.0, y + h / 2, name, fs=8.4, color=INK, weight="bold")

    # 高地址方向
    arrow(ax, (13.0, 9.0), (13.0, 71.0), color=GREY, lw=0.9, style="<|-|>", ms=7)
    label(ax, 9.8, 40.0, "地 址 增 长", fs=6.6, color=GREY, rotation=90)

    # 指针标注
    ax.plot([54.0, 60.0], [32.0, 32.0], color=ACCENT, lw=0.9)
    label(ax, 61.0, 32.0, "rbp 指向这里", fs=7.2, color=ACCENT, ha="left")

    ax.plot([54.0, 60.0], [41.0, 41.0], color=WARN, lw=0.9)
    label(ax, 61.0, 41.0, "ret 从这里取地址", fs=7.2, color=WARN, ha="left")

    ax.plot([54.0, 60.0], [14.0, 14.0], color=ACCENT_2, lw=0.9)
    label(ax, 61.0, 14.0, "rsp 指向栈顶", fs=7.2, color=ACCENT_2, ha="left")

    return save(fig, "02", "stack-frame.png")


def heap_chunk():
    fig, ax = setup(5.3, 2.5)
    # 三个块：已分配、已分配、空闲
    xs = [4.0, 34.0, 64.0]
    w_data = 25.0
    for i, x in enumerate(xs):
        box(ax, x, 30.0, 6.0, 16.0, fc=PALE_WARN if i < 2 else "#e4e8e4", ec=LINE)
        label(ax, x + 3.0, 38.0, "头", fs=7.4, color=SOFT)
        fc = PALE if i < 2 else "#eef1ee"
        box(ax, x + 6.0, 30.0, w_data, 16.0, fc=fc, ec=LINE)
        label(ax, x + 6.0 + w_data / 2, 38.0, ["数据\n已分配", "数据\n已分配", "空闲"][i],
              fs=7.6, color=SOFT)
    label(ax, 49.0, 51.0, "分配器通过头部信息找到前一块和后一块", fs=7.4, color=GREY)
    label(ax, 17.0, 23.0, "用户指针指向数据区起点", fs=7.0, color=ACCENT, ha="left")
    arrow(ax, (29.0, 25.4), (35.0, 29.2), color=ACCENT, lw=1.0, ms=7)
    label(ax, 49.0, 15.5, "头部被越界写入破坏后，合并与复用会跳到别处", fs=7.0, color=WARN)
    return save(fig, "02", "heap-chunk.png")


if __name__ == "__main__":
    address_space()
    stack_frame()
    heap_chunk()
