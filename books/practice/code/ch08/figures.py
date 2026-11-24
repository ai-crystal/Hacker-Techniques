# -*- coding: utf-8 -*-
"""第八章插图：payload 与栈帧的对应、ROP 链的执行顺序。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def payload_layout():
    fig, ax = setup(5.3, 3.4)

    stack = [
        ("buf[64]", "read 往这里写", 8.0, 20.0, PALE, SOFT),
        ("saved rbp", "覆盖掉也无所谓", 28.0, 8.0, PALE, SOFT),
        ("返回地址", "谁在这里，谁决定去哪", 36.0, 8.0, PALE_WARN, WARN),
        ("调用者的帧", "溢出走到这里就崩了", 44.0, 8.0, PALE_2, GREY),
    ]
    for name, note, y, h, fc, col in stack:
        box(ax, 3.0, y, 33.0, h, fc=fc, ec=LINE, lw=0.9)
        label(ax, 4.6, y + h / 2 + 2.0, name, fs=8.0, color=col, ha="left",
              weight="bold")
        label(ax, 4.6, y + h / 2 - 2.2, note, fs=6.6, color=GREY, ha="left")

    label(ax, 3.0, 55.8, "栈（向下生长）", fs=7.4, color=GREY, ha="left")

    payload = [
        ("A × 72", "填满 64 字节加 8 字节", 8.0, 28.0, PALE_BLUE, BLUE),
        ("pop rdi; ret", "第一条 gadget", 36.0, 8.0, PALE, ACCENT),
        ("/bin/sh 地址", "被 pop 进 rdi", 44.0, 8.0, PALE, ACCENT),
        ("system 地址", "gadget 返回到这里", 52.0, 8.0, PALE, ACCENT),
    ]
    for name, note, y, h, fc, col in payload:
        box(ax, 56.0, y, 41.0, h, fc=fc, ec=LINE, lw=0.9)
        label(ax, 57.6, y + h / 2 + 2.0, name, fs=8.0, color=col, ha="left",
              weight="bold")
        label(ax, 57.6, y + h / 2 - 2.2, note, fs=6.6, color=GREY, ha="left")

    label(ax, 56.0, 62.6, "payload（按写入顺序）", fs=7.4, color=GREY, ha="left")

    for y in (36.0, 28.0):
        arrow(ax, (36.6, y + 4.0), (55.6, y + 4.0), color=ACCENT_2, lw=1.0,
              ls=(0, (4, 2)))

    label(ax, 3.0, 3.4, "写入从 buf 底部开始往高地址走，第一个被踩到的是 saved rbp，"
                        "第二个就是返回地址。", fs=7.2, color=ACCENT, ha="left")

    return save(fig, "08", "payload-layout.png")


def rop_order():
    fig, ax = setup(5.3, 3.2)

    cells = [
        ("pop rdi; ret", 7.0),
        ("/bin/sh 地址", 18.0),
        ("system 地址", 29.0),
        ("返回后的地址", 40.0),
    ]
    for name, y in cells:
        box(ax, 52.0, y, 45.0, 9.0, fc=PALE, ec=LINE, lw=0.9)
        label(ax, 74.5, y + 4.5, name, fs=7.8, color=INK)

    label(ax, 52.0, 51.4, "地址高", fs=7.2, color=GREY, ha="left")
    label(ax, 97.0, 51.4, "地址低，也是栈顶", fs=7.2, color=GREY, ha="right")

    steps = [
        ("① ret 弹出栈顶并跳过去", 7.0, "去执行 pop rdi"),
        ("② pop rdi 拿走 8 字节", 18.0, "rdi 现在是 /bin/sh"),
        ("③ 再 ret，跳进 system", 29.0, "参数已就位，起 shell"),
        ("④ system 返回后的落点", 40.0, "填 exit，或者干脆不管"),
    ]
    for text, y, note in steps:
        label(ax, 2.0, y + 5.6, text, fs=7.4, color=INK, ha="left")
        label(ax, 2.0, y + 2.4, note, fs=6.6, color=ACCENT, ha="left")
        arrow(ax, (45.0, y + 4.5), (51.4, y + 4.5), lw=1.0)

    label(ax, 2.0, 2.6, "每一格都被当成地址，弹栈的顺序就是从下往上。",
          fs=7.2, color=ACCENT, ha="left")

    return save(fig, "08", "rop-order.png")


if __name__ == "__main__":
    payload_layout()
    rop_order()
