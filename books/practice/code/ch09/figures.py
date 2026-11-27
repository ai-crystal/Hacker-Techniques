# -*- coding: utf-8 -*-
"""第九章插图：UAF 的时序、tcache 链表被篡改前后、块大小与分配路径。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def uaf_timeline():
    fig, ax = setup(5.3, 3.2)

    stages = [
        ("分配", "buf", PALE, INK, [
            ("size 0x21", GREY),
            ("用户数据 24 字节", SOFT),
            ("属于 buf", INK),
        ]),
        ("释放", "buf（悬空）", PALE_2, INK, [
            ("size 0x21", GREY),
            ("next · key", SOFT),
            ("归分配器管", INK),
        ]),
        ("再分配", "buf / obj", PALE_BLUE, BLUE, [
            ("size 0x21", GREY),
            ("obj->data", SOFT),
            ("同一块地址", BLUE),
        ]),
        ("经旧指针写", "buf 仍在此处", PALE_WARN, WARN, [
            ("size 0x21", GREY),
            ("数据被覆盖", SOFT),
            ("obj 读到新值", WARN),
        ]),
    ]

    w, gap = 21.0, 3.0
    x0 = 3.5
    centers = []
    for i, (name, ptr, fc, color, lines) in enumerate(stages):
        cx = x0 + (w + gap) * i + w / 2
        centers.append(cx)
        label(ax, cx, 55.0, name, fs=7.4, color=color, weight="bold")

        box(ax, cx - 9.0, 32.6, 18.0, 5.4, fc="white", ec=LINE, lw=0.8)
        label(ax, cx, 35.3, ptr, fs=6.2, color=SOFT)

        arrow(ax, (cx, 32.2), (cx, 27.4), color=GREY, lw=0.9)

        ec = LINE if fc != PALE_WARN else "#d8b6a6"
        box(ax, cx - 9.5, 15.0, 19.0, 12.0, fc=fc, ec=ec, lw=0.9)
        for j, (text, col) in enumerate(lines):
            label(ax, cx, 24.2 - j * 3.1, text, fs=6.2, color=col)

    ax.plot([6.0, 94.0], [47.5, 47.5], color=LINE, lw=0.9, zorder=1)
    for cx in centers:
        ax.plot([cx], [47.5], marker="o", ms=3.2, color=ACCENT, zorder=3)

    label(ax, 50, 8.0,
          "两次分配返回同一个地址，写入权留在旧指针手里",
          fs=6.6, color=SOFT)
    return save(fig, "09", "uaf-timeline.png")


def tcache_poison():
    fig, ax = setup(5.3, 3.0)

    xs = [3.0, 27.0, 51.0, 75.0]
    w, h = 17.0, 9.0

    def row(y, cells, arrow_pairs, fs=6.4):
        for x, (title, sub, fc, color, dashed) in zip(xs, cells):
            ec = LINE if fc not in (PALE_WARN,) else "#d8b6a6"
            if dashed:
                ec = GREY
            p = box(ax, x, y, w, h, fc=fc, ec=ec, lw=0.9)
            if dashed:
                p.set_linestyle((0, (3, 2)))
            label(ax, x + w / 2, y + h / 2 + 1.9, title, fs=fs, color=color,
                  weight="bold")
            label(ax, x + w / 2, y + h / 2 - 2.0, sub, fs=fs - 0.4, color=SOFT)
        for i, j, col in arrow_pairs:
            x1 = xs[i] + w + 0.3
            x2 = xs[j] - 0.3
            arrow(ax, (x1, y + h / 2), (x2, y + h / 2), color=col, lw=1.0)

    label(ax, 3.0, 52.0, "篡改之前", fs=7.2, color=SOFT, ha="left")
    row(38.0, [
        ("tcache head", "entries[i]", PALE_2, INK, False),
        ("块 A", "next → B", PALE, INK, False),
        ("块 B", "next → NULL", PALE, INK, False),
        ("链尾", "0", "white", GREY, True),
    ], [(0, 1, ACCENT), (1, 2, ACCENT), (2, 3, ACCENT)])

    label(ax, 3.0, 28.0, "篡改之后", fs=7.2, color=WARN, ha="left")
    row(10.0, [
        ("tcache head", "entries[i]", PALE_2, INK, False),
        ("块 A", "next = target", PALE_WARN, WARN, False),
        ("伪造块", "在可控缓冲区里", PALE_WARN, WARN, False),
        ("块 B", "从链上掉出去", "white", GREY, True),
    ], [(0, 1, ACCENT), (1, 2, WARN)])

    label(ax, 50, 3.4,
          "2.32 之后 next 存的是 (块地址 >> 12) ^ 目标地址",
          fs=6.2, color=GREY)
    return save(fig, "09", "tcache-poison.png")


def size_classes():
    fig, ax = setup(5.3, 2.8)

    y, h = 16.0, 13.0
    segs = [
        (8.0, 27.0, "fastbin", "块 ≤ 0x80", PALE_2, SOFT),
        (27.0, 49.0, "smallbin", "块 < 0x400", PALE, SOFT),
        (49.0, 70.0, "largebin", "块 ≥ 0x400", PALE_BLUE, BLUE),
        (70.0, 92.0, "mmap", "请求 ≥ 0x20000", PALE_WARN, WARN),
    ]
    for x0, x1, name, sub, fc, color in segs:
        ec = "#d8b6a6" if fc == PALE_WARN else LINE
        box(ax, x0, y, x1 - x0, h, fc=fc, ec=ec, lw=0.9, radius=0)
        label(ax, (x0 + x1) / 2, y + h / 2 + 2.2, name, fs=7.2,
              color=color, weight="bold")
        label(ax, (x0 + x1) / 2, y + h / 2 - 2.4, sub, fs=6.6, color=SOFT)

    ticks = [(8.0, "0x20"), (27.0, "0x80"), (49.0, "0x400"), (70.0, "0x20000")]
    for x, text in ticks:
        ax.plot([x, x], [y - 0.4, y - 3.0], color=GREY, lw=0.7, zorder=3)
        label(ax, x, y - 5.0, text, fs=6.4, color=GREY)

    # tcache 命中区间：覆盖 fastbin、smallbin，并在 0x410 处结束
    ax.plot([8.0, 52.0], [34.0, 34.0], color=ACCENT, lw=1.0, zorder=3)
    for x in (8.0, 52.0):
        ax.plot([x, x], [34.0, 31.2], color=ACCENT, lw=1.0, zorder=3)
    label(ax, 30.0, 40.0,
          "tcache 优先命中：块 ≤ 0x410 且该尺寸未满 7 块",
          fs=6.9, color=ACCENT, weight="bold")
    label(ax, 53.6, 34.0, "0x410", fs=6.4, color=ACCENT, ha="left")

    label(ax, 50, 4.0,
          "块大小 = (请求 + 8 + 15) & ~15，最小 0x20",
          fs=6.4, color=GREY)
    return save(fig, "09", "size-classes.png")


if __name__ == "__main__":
    uaf_timeline()
    tcache_poison()
    size_classes()
