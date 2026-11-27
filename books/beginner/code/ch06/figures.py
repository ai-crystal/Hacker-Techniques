# -*- coding: utf-8 -*-
"""第六章插图：栈帧覆盖、控制流劫持、远程利用路径。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                    PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label, rect,
                    save, setup)


def stack_overwrite():
    fig, ax = setup(5.3, 3.3)
    regions = [
        ("调用者的栈帧", 55.0, 6.0, "#eeebe5", "高地址"),
        ("返回地址", 44.0, 9.0, PALE_WARN, "rbp + 8"),
        ("保存的 rbp", 34.0, 8.0, PALE_BLUE, "rbp"),
        ("buf[16]", 17.0, 15.0, PALE, "rbp - 16"),
    ]
    for name, y, h, fc, addr in regions:
        box(ax, 30.0, y, 30.0, h, fc=fc, ec=LINE)
        label(ax, 45.0, y + h / 2, name, fs=8.2, color=INK, weight="bold")
        label(ax, 62.0, y + h / 2, addr, fs=6.8, color=GREY, ha="left")

    label(ax, 14.5, 57.5, "写入的字节", fs=7.2, color=SOFT)
    seg = [(17.0, 15.0, "16 字节填充"), (34.0, 8.0, "8 字节覆盖"),
           (44.0, 9.0, "8 字节地址")]
    for y, h, text in seg:
        box(ax, 4.0, y, 21.0, h, fc="#f8f8f5", ec="#d6d6d0", lw=0.8)
        label(ax, 14.5, y + h / 2, text, fs=6.8, color=GREY)
        arrow(ax, (25.4, y + h / 2), (29.4, y + h / 2), color=ACCENT_2, lw=0.9,
              ms=6)

    label(ax, 45.0, 11.0, "复制 32 字节之后，返回地址已经不属于原程序", fs=7.2,
          color=WARN)
    label(ax, 45.0, 4.8, "函数执行到 ret 时，弹出的是攻击者写的那个地址", fs=7.0,
          color=GREY)
    return save(fig, "06", "stack-overwrite.png")


def control_flow_hijack():
    fig, ax = setup(5.3, 3.0)
    box(ax, 4.0, 44.0, 26.0, 11.0, fc=PALE, ec=LINE)
    label(ax, 17.0, 49.5, "main 调用 greet", fs=7.8, color=INK, weight="bold")
    box(ax, 38.0, 44.0, 26.0, 11.0, fc=PALE, ec=LINE)
    label(ax, 51.0, 49.5, "greet 执行", fs=7.8, color=INK, weight="bold")
    box(ax, 72.0, 44.0, 22.0, 11.0, fc=PALE_2, ec=LINE)
    label(ax, 83.0, 49.5, "ret 取地址", fs=7.8, color=INK, weight="bold")
    arrow(ax, (30.4, 49.5), (37.6, 49.5))
    arrow(ax, (64.4, 49.5), (71.6, 49.5))

    box(ax, 4.0, 18.0, 40.0, 12.0, fc="#eef2f1", ec=LINE)
    label(ax, 24.0, 27.0, "回到 main，正常结束", fs=7.6, color=ACCENT)
    box(ax, 56.0, 18.0, 38.0, 12.0, fc=PALE_WARN, ec="#e2ccc0")
    label(ax, 75.0, 27.0, "跳进 buf，执行 shellcode", fs=7.6, color=WARN)

    arrow(ax, (78.0, 43.4), (30.0, 30.6), color=GREY, rad=0.12, lw=0.9)
    label(ax, 30.0, 36.8, "返回地址未改动", fs=6.8, color=GREY)
    arrow(ax, (86.0, 43.4), (75.0, 30.6), color=WARN, lw=1.1)
    label(ax, 90.0, 36.8, "被改写", fs=6.8, color=WARN, ha="right")
    label(ax, 50.0, 9.0, "同一个 ret 指令，因为栈顶的值不同，走向两个结局", fs=7.2,
          color=SOFT)
    return save(fig, "06", "control-flow-hijack.png")


def remote_path():
    fig, ax = setup(5.3, 2.5)
    steps = [("攻击者", "构造字节流", 2.0, 19.0, PALE),
             ("网络", "TCP 数据", 25.0, 18.0, PALE_2),
             ("服务进程", "recv 到 buf", 47.0, 22.0, PALE_BLUE),
             ("栈帧被改写", "ret 跳到 buf", 73.0, 24.0, PALE_WARN)]
    y, h = 30.0, 15.0
    for name, note, x, w, fc in steps:
        box(ax, x, y, w, h, fc=fc, ec=LINE)
        label(ax, x + w / 2, y + h - 5.2, name, fs=7.8, color=INK, weight="bold")
        label(ax, x + w / 2, y + 5.0, note, fs=6.6, color=GREY)
    for x in (21.4, 43.4, 69.4):
        arrow(ax, (x, y + h / 2), (x + 3.2, y + h / 2))
    label(ax, 50.0, 20.0, "全程不需要接触目标机器，只需要能连上那个端口", fs=7.2,
          color=ACCENT)
    label(ax, 50.0, 12.0, "偏移量和地址要与目标程序的具体版本对齐", fs=7.0,
          color=GREY)
    return save(fig, "06", "remote-path.png")


def frame_compare():
    fig, ax = setup(5.3, 2.9)
    h, gap = 8.5, 1.8
    ys = [10.0 + i * (h + gap) for i in range(4)]

    left = [("buf[16]", PALE), ("保存的 rbp", PALE_2),
            ("返回地址", PALE_WARN), ("调用者的栈帧", "#f2f2ef")]
    right = [("保存的 x29", PALE_2), ("保存的 x30（LR）", PALE_WARN),
             ("buf[16]", PALE), ("调用者的栈帧", "#f2f2ef")]

    for x0, center, title, cells in ((2.0, 19.0, "x86-64", left),
                                     (54.0, 71.0, "AArch64", right)):
        label(ax, center, 52.0, title, fs=9.2, color=ACCENT, weight="bold")
        for y, (text, fc) in zip(ys, cells):
            box(ax, x0, y, 34.0, h, fc=fc, ec=LINE)
            label(ax, center, y + h / 2, text, fs=7.4, color=SOFT)

    # 左侧：从 buf 顶部一路写到返回地址
    y_buf_top = ys[0] + h
    y_ret_bottom = ys[2]
    ax.plot([36.0, 39.0], [y_buf_top, y_buf_top], color=WARN, lw=0.9)
    arrow(ax, (39.0, y_buf_top), (39.0, y_ret_bottom - 0.6), color=WARN, lw=1.1)
    label(ax, 42.4, (y_buf_top + y_ret_bottom) / 2, "越界写入", fs=6.8,
          color=WARN, rotation=90)

    # 右侧：溢出不经过保存的 x30，直接进入调用者的栈帧
    y_buf_top_r = ys[2] + h
    ax.plot([88.0, 91.0], [y_buf_top_r, y_buf_top_r], color=ACCENT_2, lw=0.9)
    arrow(ax, (91.0, y_buf_top_r), (91.0, ys[3] + h * 0.75), color=ACCENT_2, lw=1.1)
    label(ax, 94.4, (y_buf_top_r + ys[3] + h * 0.75) / 2, "越过整个帧",
          fs=6.8, color=ACCENT_2, rotation=90)

    label(ax, 19.0, 5.6, "向上写先到 rbp，再到返回地址", fs=6.6, color=GREY)
    label(ax, 71.0, 5.6, "x30 在缓冲区下方，向上写碰不到", fs=6.6, color=GREY)

    return save(fig, "06", "frame-compare.png")


if __name__ == "__main__":
    stack_overwrite()
    control_flow_hijack()
    remote_path()
    frame_compare()
