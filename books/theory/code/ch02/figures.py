# -*- coding: utf-8 -*-
"""第二章插图：ELF 文件与内存映射对照、PLT/GOT 的解析流程。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def elf_mapping():
    """左边是文件里的字节，右边是进程里的页。"""
    fig, ax = setup(5.3, 3.5)

    label(ax, 4.0, 63.0, "文件里的字节", fs=8.2, color=ACCENT, ha="left",
          weight="bold")
    label(ax, 56.0, 63.0, "进程里的地址", fs=8.2, color=ACCENT, ha="left",
          weight="bold")
    label(ax, 4.0, 59.4, "偏移从 0 开始", fs=6.6, color=GREY, ha="left")
    label(ax, 56.0, 59.4, "基址每次运行都不同", fs=6.6, color=GREY, ha="left")

    blocks = [
        (48.9, 8.0, ".bss", "未初始化数据", "RW，零填充", True),
        (35.6, 11.0, ".init_array  .got  .data", "可读写", "RW", False),
        (18.3, 15.0, ".init  .plt  .text  .rodata", "只读可执行", "R-X", False),
        (6.0, 10.0, "ELF 头  程序头表", "总在偏移 0", "R", False),
    ]

    for y, h, name, note, perm, empty in blocks:
        ec = "#b0b0aa" if empty else "#c9c9c3"
        fc = PALE_WARN if empty else PALE
        box(ax, 4.0, y, 40.0, h, fc=fc, ec=ec, lw=0.9,
            style="dashed" if empty else None)
        label(ax, 6.4, y + h / 2 + 1.9, name, fs=7.0, color=INK, ha="left")
        label(ax, 6.4, y + h / 2 - 2.2, note, fs=6.2, color=GREY, ha="left")

        rc = PALE_WARN if empty else PALE_BLUE
        box(ax, 56.0, y, 40.0, h, fc=rc, ec=ec, lw=0.9)
        label(ax, 58.4, y + h / 2 + 1.9, name, fs=7.0, color=INK, ha="left")
        label(ax, 58.4, y + h / 2 - 2.2, perm, fs=6.2, color=GREY, ha="left")

    for y, h, empty in [(6.0, 10.0, False), (18.3, 15.0, False),
                        (35.6, 11.0, False), (48.9, 8.0, True)]:
        ls = (0, (4, 2.4)) if empty else "-"
        arrow(ax, (44.6, y + h / 2), (55.4, y + h / 2), color=ACCENT_2,
              lw=1.0, ls=ls)

    label(ax, 50.0, 2.0, "mmap 只按段映射，段与段之间按页补空洞",
          fs=6.6, color=SOFT)
    return save(fig, "02", "elf-mapping.png")


def plt_got():
    """一次延迟绑定：call 到 PLT，跳到 GOT，再进解析器，最后回填。"""
    fig, ax = setup(5.3, 3.2)

    box(ax, 2.0, 46.0, 24.0, 10.0, fc="white", ec=LINE)
    label(ax, 14.0, 52.6, "调用点", fs=7.4, color=INK)
    label(ax, 14.0, 49.2, "call printf@plt", fs=6.8, color=GREY)

    box(ax, 30.0, 46.0, 26.0, 10.0, fc=PALE, ec=LINE)
    label(ax, 43.0, 52.6, ".plt 里的一项", fs=7.4, color=INK)
    label(ax, 43.0, 49.2, "jmp *GOT[n]", fs=6.8, color=GREY)

    box(ax, 60.0, 46.0, 36.0, 10.0, fc=PALE_BLUE, ec=LINE)
    label(ax, 78.0, 52.6, ".got 里的那一项", fs=7.4, color=INK)
    label(ax, 78.0, 49.2, "先指向 .plt[0]，之后是真实地址", fs=6.4, color=GREY)

    arrow(ax, (26.4, 51.0), (29.6, 51.0))
    arrow(ax, (56.4, 51.0), (59.6, 51.0))

    arrow(ax, (68.0, 46.0), (68.0, 38.2), color=GREY, lw=1.0)
    label(ax, 66.6, 42.0, "尚未解析", fs=6.2, color=GREY, ha="right")
    arrow(ax, (88.0, 38.4), (88.0, 46.0), color=ACCENT_2, lw=1.0,
          ls=(0, (4.5, 2.5)))
    label(ax, 86.6, 42.0, "填回地址", fs=6.2, color=ACCENT_2, ha="right")

    box(ax, 30.0, 26.0, 66.0, 12.0, fc="white", ec=LINE)
    label(ax, 63.0, 34.6, "_dl_runtime_resolve", fs=7.4, color=INK)
    label(ax, 63.0, 31.2, "取重定位索引，查出 printf 的地址", fs=6.6,
          color=GREY)
    label(ax, 63.0, 27.9, "把地址写回 GOT[n]，再跳过去", fs=6.6, color=GREY)

    arrow(ax, (58.0, 25.8), (58.0, 21.2))
    box(ax, 30.0, 10.0, 66.0, 11.0, fc=PALE_2, ec=LINE)
    label(ax, 63.0, 17.6, "printf 的代码", fs=7.4, color=INK)
    label(ax, 63.0, 13.8, "以后再调用，GOT 已经填好，不再进解析器", fs=6.4,
          color=GREY)

    box(ax, 2.0, 24.0, 24.0, 12.0, fc=PALE_WARN, ec="#d8c3b6", lw=0.8)
    label(ax, 14.0, 32.6, "解析器查的表", fs=6.8, color=WARN)
    label(ax, 14.0, 28.6, ".dynsym", fs=6.4, color=SOFT)
    label(ax, 14.0, 25.6, ".rela.plt", fs=6.4, color=SOFT)
    arrow(ax, (26.4, 29.0), (30.0, 31.0), color="#c0a595", lw=0.9,
          ms=7)

    label(ax, 2.0, 4.2,
          "第一次调用走三步，之后每次只剩两步；GOT 可写，改它一条等于改掉 printf 的入口。",
          fs=6.6, color=SOFT, ha="left")
    return save(fig, "02", "plt-got.png")


if __name__ == "__main__":
    elf_mapping()
    plt_got()
