# -*- coding: utf-8 -*-
"""第四章插图：chunk 的字段与它在堆段中的位置、free 的归属判定流程。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def chunk_layout():
    """左边放大的 chunk 字段，右边这一段堆里它所在的位置。"""
    fig, ax = setup(5.3, 3.8)

    # ---- 右：堆段（地址向上增长） ----
    x, w = 62.0, 30.0
    rows = [
        (8.0, 7.0, "已分配", "0x20 字节", PALE_BLUE, "#c3ccd6"),
        (16.0, 7.0, "已释放", "0x30 字节", PALE, LINE),
        (24.0, 12.0, "本块", "0x40 字节", PALE_WARN, "#dcc3b6"),
        (37.0, 7.0, "已释放", "0x50 字节", PALE, LINE),
        (45.0, 7.0, "top chunk", "堆的剩余部分", "#f1f1ec", LINE),
    ]
    for y, h, name, note, fc, ec in rows:
        box(ax, x, y, w, h, fc=fc, ec=ec, lw=0.9)
        label(ax, x + w / 2, y + h / 2 + 1.5, name, fs=6.8, color=INK)
        label(ax, x + w / 2, y + h / 2 - 2.1, note, fs=5.9, color=GREY)

    label(ax, x, 55.2, "高地址", fs=6.0, color=GREY, ha="left")
    label(ax, x, 4.6, "低地址", fs=6.0, color=GREY, ha="left")

    # ---- 左：放大的 chunk 字段 ----
    sx, sw = 4.0, 44.0
    fields = [
        (24.0, 8.0, "prev_size", "前一块空闲时才有效", PALE_2, LINE),
        (32.0, 8.0, "size", "低 3 位是标志", PALE_WARN, "#dcc3b6"),
        (40.0, 12.0, "用户数据", "空闲时前 16 字节是 fd / bk", PALE_BLUE, "#c3ccd6"),
        (52.0, 7.0, "下一块的 prev_size", "不在本块的账上", "#f1f1ec", LINE),
    ]
    for y, h, name, note, fc, ec in fields:
        box(ax, sx, y, sw, h, fc=fc, ec=ec, lw=0.9)
        label(ax, sx + sw / 2, y + h / 2 + 1.7, name, fs=6.9, color=INK)
        label(ax, sx + sw / 2, y + h / 2 - 2.2, note, fs=5.9, color=GREY)

    label(ax, sx + sw / 2, 61.0, "一个 chunk 的字节账", fs=7.2, color=SOFT)

    # 用户指针落在 size 与用户数据之间
    ax.plot([2.4, sx + sw + 1.4], [40.0, 40.0], color=ACCENT,
            lw=1.0, ls=(0, (3.4, 2.0)), zorder=5)

    # 本块 → 放大
    arrow(ax, (x - 1.0, 30.0), (sx + sw + 0.2, 44.0), color=ACCENT_2, lw=1.0,
          ms=7, rad=-0.12)

    # 底部说明
    label(ax, 4.0, 16.6, "chunk 大小 = (n + 8 + 15) & ~15", fs=6.3,
          color=SOFT, ha="left")
    label(ax, 4.0, 12.2, "size 已含头部，按 16 字节对齐", fs=6.3,
          color=SOFT, ha="left")
    label(ax, 4.0, 7.8, "PREV_INUSE 等三个标志占低 3 位", fs=6.3,
          color=SOFT, ha="left")
    label(ax, 4.0, 3.4, "虚线处就是用户指针 chunk + 16", fs=6.3,
          color=ACCENT, ha="left")
    return save(fig, "04", "chunk-layout.png")


def free_path():
    """一次 free 依次经过的关口，以及每个关口把它送到哪里。"""
    fig, ax = setup(5.3, 3.9)

    spine_x, spine_w = 6.0, 46.0
    nodes = [
        (62.0, 6.0, "free(p)：校验指针非空、对齐、size 合法", PALE, LINE),
        (51.0, 6.0, "大小 ≤ 0x410 且对应 tcache 未满？", PALE_2, LINE),
        (40.0, 6.0, "大小 ≤ global_max_fast（0x80）？", PALE_2, LINE),
        (29.0, 6.0, "IS_MMAPPED 置位？", PALE_2, LINE),
        (18.0, 6.0, "向后、向前合并相邻空闲块", PALE_WARN, "#dcc3b6"),
        (6.0, 6.4, "挂进 unsorted bin", PALE, LINE),
    ]
    for y, h, text, fc, ec in nodes:
        box(ax, spine_x, y, spine_w, h, fc=fc, ec=ec, lw=0.9)
        label(ax, spine_x + spine_w / 2, y + h / 2, text, fs=6.4, color=INK)

    # 主干向下
    for (y1, h1, *_), (y2, *_rest) in zip(nodes, nodes[1:]):
        arrow(ax, (spine_x + 12.0, y1 - 0.2), (spine_x + 12.0, y2 + h1 + 0.2),
              color=ACCENT_2, lw=1.0, ms=7)

    # 右侧去向
    outs = [
        (51.4, "进 tcache 单链", "上限 7 个，不合并", PALE_BLUE, "#c3ccd6", 54.0, "是"),
        (40.0, "进 fastbin 单链", "不合并，不清 P 位", PALE_BLUE, "#c3ccd6", 43.0, "是"),
        (29.4, "munmap", "整块还给系统", "#f1f1ec", LINE, 32.0, "是"),
        (6.0, "≥ 64 KB 时 systrim", "试把堆尾还给系统", PALE_WARN, "#dcc3b6", 9.2, ""),
    ]
    ox, ow = 62.0, 33.0
    for y, name, note, fc, ec, ay, tag in outs:
        box(ax, ox, y, ow, 6.4, fc=fc, ec=ec, lw=0.9)
        label(ax, ox + ow / 2, y + 4.2, name, fs=6.4, color=INK)
        label(ax, ox + ow / 2, y + 1.5, note, fs=5.7, color=GREY)
        arrow(ax, (spine_x + spine_w + 0.2, ay), (ox - 0.6, ay),
              color=WARN, lw=1.0, ms=7)
        if tag:
            label(ax, (spine_x + spine_w + ox) / 2, ay + 1.6, tag, fs=5.9,
                  color=WARN)

    label(ax, 6.0, 2.4, "只有走到最后两步的块才会触发双向链表的摘除检查（fd->bk == p）",
          fs=5.9, color=GREY, ha="left")
    return save(fig, "04", "free-path.png")


if __name__ == "__main__":
    chunk_layout()
    free_path()
