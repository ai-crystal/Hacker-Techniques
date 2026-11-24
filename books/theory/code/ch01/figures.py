# -*- coding: utf-8 -*-
"""第一章插图：x86-64 指令编码字段、地址翻译与缓存查找路径。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def encoding_fields():
    """一条 x86-64 指令的字段排列，柱长表示该字段最多能占几个字节。"""
    fig, ax = setup(5.3, 3.2)

    rows = [
        ("遗留前缀", 4, PALE_2, "0–4"),
        ("REX 前缀", 1, PALE_WARN, "0–1"),
        ("操作码", 3, PALE_BLUE, "1–3"),
        ("ModRM", 1, PALE, "0–1"),
        ("SIB", 1, PALE, "0–1"),
        ("位移", 4, PALE_2, "0–4"),
        ("立即数", 8, PALE_2, "0–8"),
    ]

    y, step, h = 50.0, 6.6, 4.6
    x0 = 33.0
    for name, nb, fc, rng in rows:
        label(ax, 4.0, y + h / 2, name, fs=7.6, color=INK, ha="left")
        box(ax, x0, y + 1.0, nb * 6.2, 2.6, fc=fc, ec="#c9c9c3", lw=0.8)
        label(ax, 96.0, y + h / 2, rng, fs=7.2, color=GREY, ha="right")
        y -= step

    label(ax, 96.0, 57.2, "字节数", fs=6.8, color=GREY, ha="right")
    label(ax, 4.0, 4.2,
          "REX 与 ModRM 的内容决定后面跟不跟 SIB、位移与立即数，整条 1 到 15 字节。",
          fs=6.8, color=SOFT, ha="left")
    return save(fig, "01", "x86-encoding.png")


def address_path():
    """虚拟地址的四级查表，以及物理地址落到缓存层次上的路径。"""
    fig, ax = setup(5.3, 3.6)

    # 左栏：地址翻译
    label(ax, 2.0, 66.8, "地址翻译", fs=8.4, color=ACCENT, ha="left",
          weight="bold")

    segs = [("PML4", 10.1, "9 位"), ("PDPT", 10.1, "9 位"),
            ("PD", 10.1, "9 位"), ("PT", 10.1, "9 位"),
            ("页内偏移", 13.5, "12 位")]
    x = 2.0
    for name, w, bits in segs:
        fc = PALE_BLUE if name != "页内偏移" else PALE_2
        box(ax, x, 57.6, w, 7.4, fc=fc, ec="#c9c9c3", lw=0.8)
        label(ax, x + w / 2, 62.9, name, fs=6.6, color=BLUE)
        label(ax, x + w / 2, 60.2, bits, fs=6.0, color=GREY)
        x += w

    arrow(ax, (13.0, 57.4), (13.0, 55.5))
    box(ax, 2.0, 48.2, 54.0, 7.1, fc="white", ec=LINE)
    label(ax, 29.0, 52.8, "四级页表，每级 512 项，每项 8 字节",
          fs=7.2, color=INK)
    label(ax, 29.0, 50.1, "取出的页框基址成为下一级的表地址",
          fs=6.6, color=GREY)

    arrow(ax, (29.0, 48.0), (29.0, 44.6))
    box(ax, 2.0, 37.3, 54.0, 7.1, fc=PALE, ec=LINE)
    label(ax, 29.0, 41.9, "物理地址 = 页框号 40 位 : 页内偏移 12 位",
          fs=7.0, color=INK)
    label(ax, 29.0, 39.2, "低 12 位不参与查表，原样传下去",
          fs=6.6, color=GREY)

    label(ax, 2.0, 30.6, "页表缓存", fs=7.4, color=ACCENT, ha="left",
          weight="bold")
    for i, s in enumerate(["TLB 缓存最近用过的页表项",
                           "命中时跳过整个查表过程",
                           "权限按页裁定，粒度 4 KiB"]):
        label(ax, 2.0, 26.4 - i * 3.4, s, fs=6.8, color=SOFT, ha="left")
    label(ax, 2.0, 12.6, "越界的虚拟地址在查表阶段就失败，", fs=6.8,
          color=GREY, ha="left")
    label(ax, 2.0, 9.2, "而不是等到真正读内存才出错。", fs=6.8,
          color=GREY, ha="left")

    # 右栏：缓存层次
    label(ax, 60.0, 66.8, "缓存查找", fs=8.4, color=ACCENT, ha="left",
          weight="bold")

    arrow(ax, (56.4, 40.9), (60.0, 40.9), color=ACCENT_2)

    lv = [("L1d 32 KiB，8 路", "64 组，一组 8 行", 37.0, PALE_BLUE),
          ("L2 256 KiB", "每核独占", 26.0, PALE),
          ("L3 数 MiB", "全核共享", 15.0, PALE_2),
          ("主存", "整行 64 字节搬入", 4.0, "white")]
    for name, note, yy, fc in lv:
        box(ax, 60.0, yy, 37.0, 7.2, fc=fc, ec=LINE)
        label(ax, 78.5, yy + 4.8, name, fs=7.2, color=INK)
        label(ax, 78.5, yy + 2.2, note, fs=6.4, color=GREY)

    for yy in (36.8, 25.8, 14.8):
        arrow(ax, (78.5, yy), (78.5, yy - 3.4), color=GREY, lw=1.0)
        label(ax, 80.6, yy - 1.7, "未命中", fs=6.2, color=GREY, ha="left")
    return save(fig, "01", "address-path.png")


if __name__ == "__main__":
    encoding_fields()
    address_path()
