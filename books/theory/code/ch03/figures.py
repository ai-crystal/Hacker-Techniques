# -*- coding: utf-8 -*-
"""第三章插图：栈帧的逐字节布局、CFI 描述与栈展开。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def stack_frame():
    """一个带 64 字节缓冲区、三个保存寄存器的函数，栈上从上到下。"""
    fig, ax = setup(5.3, 3.6)

    rows = [
        (58.7, 6.0, "调用者的栈帧", "上一层的局部变量", "#f3f3ef"),
        (51.8, 6.0, "第 7 个及以后的参数", "由调用者压栈", PALE_2),
        (44.5, 6.4, "返回地址", "call 压入，ret 弹出", PALE_WARN),
        (37.2, 6.4, "保存的 rbp", "push rbp 的结果", PALE),
        (29.9, 6.4, "栈保护 canary", "fs:0x28 拷来的值", PALE_WARN),
        (15.0, 14.0, "局部变量与缓冲区", "偏移由编译器算定", PALE_BLUE),
        (9.5, 4.6, "对齐填充", "", "#f0f0ec"),
        (1.4, 7.2, "callee-saved", "rbx  r12–r15", PALE),
    ]

    x, w = 30.0, 40.0
    for y, h, name, note, fc in rows:
        box(ax, x, y, w, h, fc=fc, ec="#c9c9c3", lw=0.9)
        if note:
            label(ax, x + w / 2, y + h / 2 + 1.6, name, fs=6.9, color=INK)
            label(ax, x + w / 2, y + h / 2 - 1.8, note, fs=6.0, color=GREY)
        else:
            label(ax, x + w / 2, y + h / 2, name, fs=6.4, color=SOFT)

    marks = [(54.8, "rbp + 0x10 起"), (47.7, "rbp + 0x8"),
             (40.4, "rbp"), (33.1, "rbp − 0x8"),
             (22.0, "rbp − 0x10 到 −0x50"), (11.8, "对齐到 16 字节"),
             (1.6, "rsp")]
    for y, off in marks:
        label(ax, 28.6, y, off, fs=6.4, color=ACCENT, ha="right")

    ax.plot([70.6, 72.6], [33.1, 33.1], color=WARN, lw=1.0, zorder=2)
    label(ax, 73.6, 34.6, "溢出往高地址走", fs=6.0, color=WARN, ha="left")
    label(ax, 73.6, 31.8, "先撞 canary，再改返回地址", fs=6.0, color=WARN,
          ha="left")

    label(ax, 30.0, 66.4, "高地址", fs=6.0, color=GREY, ha="left")
    label(ax, 76.4, 6.2, "rsp 以下 128 字节是红区", fs=6.0, color=GREY,
          ha="left")
    label(ax, 76.4, 2.8, "低地址", fs=6.0, color=GREY, ha="left")
    return save(fig, "03", "stack-frame.png")


def unwind_cfi():
    """CFA 是怎么算出来的，展开器从哪两个位置读东西。"""
    fig, ax = setup(5.3, 3.4)

    label(ax, 4.0, 57.0, "高地址", fs=6.2, color=GREY, ha="left")

    box(ax, 6.0, 46.0, 39.0, 6.5, fc=PALE_WARN, ec="#c9c9c3", lw=0.9)
    label(ax, 25.5, 50.4, "返回地址", fs=6.8, color=INK)
    label(ax, 25.5, 47.6, "CFA − 8", fs=6.0, color=GREY)

    box(ax, 6.0, 39.5, 39.0, 6.5, fc=PALE, ec="#c9c9c3", lw=0.9)
    label(ax, 25.5, 43.9, "保存的 rbp", fs=6.8, color=INK)
    label(ax, 25.5, 41.1, "CFA − 16", fs=6.0, color=GREY)

    box(ax, 6.0, 24.0, 39.0, 15.5, fc=PALE_BLUE, ec="#c9c9c3", lw=0.9)
    label(ax, 25.5, 33.6, "本帧的局部变量", fs=6.8, color=INK)
    label(ax, 25.5, 30.4, "与寄存器溢出区", fs=6.0, color=GREY)
    label(ax, 25.5, 26.4, "rsp 停在这里", fs=6.0, color=GREY)

    ax.plot([4.0, 44.0], [52.5, 52.5], color=ACCENT, lw=1.0,
            ls=(0, (4, 2.2)), zorder=3)
    label(ax, 46.0, 52.5, "CFA", fs=7.0, color=ACCENT, ha="left")
    label(ax, 46.0, 49.8, "CFA = rbp + 16", fs=6.2, color=GREY, ha="left")

    ax.plot([5.0, 44.0], [39.5, 39.5], color=ACCENT_2, lw=1.0, zorder=3)
    label(ax, 46.0, 39.5, "rbp", fs=7.0, color=ACCENT_2, ha="left")

    box(ax, 46.0, 22.0, 50.0, 12.0, fc="white", ec=LINE)
    label(ax, 48.0, 31.0, "FDE 里的两条规则", fs=6.6, color=INK, ha="left")
    label(ax, 48.0, 27.4, "0x1136  CFA = rsp + 8", fs=6.2, color=SOFT, ha="left")
    label(ax, 48.0, 24.4, "0x1140  CFA = rbp + 16", fs=6.2, color=SOFT, ha="left")

    box(ax, 46.0, 4.0, 50.0, 14.0, fc=PALE_2, ec=LINE)
    label(ax, 48.0, 14.8, "展开器依次做", fs=6.6, color=INK, ha="left")
    label(ax, 48.0, 11.4, "按 PC 找到覆盖它的 FDE", fs=6.2, color=SOFT, ha="left")
    label(ax, 48.0, 8.4, "用当条规则算出 CFA", fs=6.2, color=SOFT, ha="left")
    label(ax, 48.0, 5.6, "读 CFA−8，得到调用者的 PC", fs=6.2, color=SOFT, ha="left")

    arrow(ax, (71.0, 21.7), (71.0, 18.3), color=ACCENT, lw=1.1)
    label(ax, 4.0, 19.0, "低地址", fs=6.2, color=GREY, ha="left")
    return save(fig, "03", "unwind-cfi.png")


if __name__ == "__main__":
    stack_frame()
    unwind_cfi()
