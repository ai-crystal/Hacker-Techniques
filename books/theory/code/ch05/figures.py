# -*- coding: utf-8 -*-
"""第五章插图：利用原语的分级与一次完整的泄漏加覆写链路。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def primitive_ladder():
    fig, ax = setup(5.3, 3.55)
    # 自下而上：每一级都比下一级多一分控制力
    rows = [
        ("1  越界读", "读出对象之外的内容", "看得见", PALE),
        ("2  越界写", "改写相邻对象的字段", "改得动", PALE),
        ("3  释放后使用", "对象归还了，指针还在", "时序", PALE_2),
        ("4  类型混淆", "一块内存被当成两种类型", "解释权", PALE_2),
        ("5  任意读写", "地址由输入决定", "指哪打哪", PALE_BLUE),
        ("6  控制流劫持", "下一条指令的地址被改写", "跳得出去", PALE_WARN),
    ]
    h, gap, x, w = 7.0, 4.0, 10.0, 56.0
    y = 2.6
    for name, note, gain, fc in rows:
        box(ax, x, y, w, h, fc=fc, ec=LINE)
        label(ax, x + 2.2, y + h / 2, name, fs=8.4, color=INK, ha="left",
              weight="bold")
        label(ax, x + w - 2.2, y + h / 2, note, fs=7.2, color=GREY, ha="right")
        label(ax, 69.0, y + h / 2, gain, fs=7.2, color=SOFT, ha="left")
        if y > 3.0:
            arrow(ax, (15.0, y - gap + 0.25), (15.0, y - 0.25), color=ACCENT_2,
                  lw=1.0, ms=7)
        y += h + gap
    return save(fig, "05", "primitive-ladder.png")


def leak_then_write():
    fig, ax = setup(5.3, 3.45)
    h = 11.0
    w = 24.0
    top_y, mid_y = 46.0, 22.0
    xs = [6.0, 38.0, 70.0]

    steps_top = [("漏洞一　越界读", "读到相邻对象的指针"),
                 ("减掉已知偏移", "文件里查得到"),
                 ("得到模块基址", "地址就此定下来")]
    for (title, note), x in zip(steps_top, xs):
        box(ax, x, top_y, w, h, fc=PALE_BLUE, ec="#b6c4d2")
        label(ax, x + w / 2, top_y + h - 3.7, title, fs=8.0, color=BLUE,
              weight="bold")
        label(ax, x + w / 2, top_y + 3.1, note, fs=6.7, color=GREY)
    arrow(ax, (30.4, top_y + h / 2), (37.6, top_y + h / 2), color=ACCENT_2)
    arrow(ax, (62.4, top_y + h / 2), (69.6, top_y + h / 2), color=ACCENT_2)

    # 拐弯：从右上角落到第二行右端
    ax.plot([82.0, 82.0], [top_y - 0.3, mid_y + h + 0.3], color=ACCENT_2,
            lw=1.1, ls=(0, (4, 2.4)), zorder=2)
    arrow(ax, (82.0, mid_y + h + 2.6), (82.0, mid_y + h + 0.2), color=ACCENT_2,
          lw=1.1, ms=7)

    steps_mid = [("函数指针被改写", "下一次调用就跳走"),
                 ("漏洞二　越界写", "写入算好的地址"),
                 ("基址加目标偏移", "算出要写的值")]
    for (title, note), x in zip(steps_mid, xs):
        box(ax, x, mid_y, w, h, fc=PALE_WARN, ec="#dcc3b6")
        label(ax, x + w / 2, mid_y + h - 3.7, title, fs=8.0, color=WARN,
              weight="bold")
        label(ax, x + w / 2, mid_y + 3.1, note, fs=6.7, color=GREY)
    arrow(ax, (69.6, mid_y + h / 2), (62.4, mid_y + h / 2), color=ACCENT_2)
    arrow(ax, (37.6, mid_y + h / 2), (30.4, mid_y + h / 2), color=ACCENT_2)

    box(ax, 6.0, 3.0, 56.0, 9.4, fc="white", ec=LINE)
    label(ax, 34.0, 7.7, "控制流落到选定的目标", fs=8.4, color=INK,
          weight="bold")
    arrow(ax, (18.0, mid_y - 0.25), (18.0, 12.8), color=ACCENT, lw=1.2)

    label(ax, 66.0, 8.6, "两步之间不能颠倒", fs=7.0, color=SOFT, ha="left")
    label(ax, 66.0, 4.6, "先知道地址，才敢写", fs=7.0, color=SOFT, ha="left")
    return save(fig, "05", "leak-then-write.png")


if __name__ == "__main__":
    primitive_ladder()
    leak_then_write()
