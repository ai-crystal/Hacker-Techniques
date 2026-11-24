# -*- coding: utf-8 -*-
"""第六章插图：32 位进程的随机化区域，以及 CFI 的合法目标集合。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def layout_32bit():
    fig, ax = setup(5.3, 3.4)
    x, w = 24.0, 26.0
    # name, addr, addr 靠上还是靠下, note, y, h, fill, edge
    bands = [
        ("内核", "0xC0000000", "bottom", "用户态无法访问",
         54.0, 9.6, "#e6e9e6", "#b0b6b0"),
        ("栈", "0xBFFFFFFF", "top", "基址随机 19 位",
         41.0, 11.0, PALE_BLUE, "#b6c4d2"),
        ("mmap 映射区", "0x55555000", "bottom", "基址随机 8 位",
         29.0, 11.0, PALE_BLUE, "#b6c4d2"),
        ("", "", "", "", 21.0, 7.0, "white", LINE),
        ("堆（brk）", "", "", "起始位置随之浮动",
         13.0, 7.0, PALE, LINE),
        ("代码与数据", "0x08048000", "bottom", "非 PIE 时固定",
         5.0, 7.0, PALE, LINE),
    ]
    for name, addr, pos, note, y, h, fc, ec in bands:
        box(ax, x, y, w, h, fc=fc, ec=ec, lw=0.9)
        if not name:
            label(ax, x + w / 2, y + h / 2, "未映射", fs=7.0, color=GREY,
                  style="italic")
        else:
            label(ax, x + w / 2, y + h / 2, name, fs=7.6, color=SOFT)
        if addr:
            ay = y + 2.0 if pos == "bottom" else y + h - 2.0
            label(ax, x - 2.4, ay, addr, fs=6.4, color=GREY, ha="right")
        if note:
            label(ax, x + w + 3.4, y + h / 2, note, fs=6.9, color=SOFT,
                  ha="left")
    return save(fig, "06", "layout-32bit.png")


def cfi_targets():
    fig, ax = setup(5.3, 3.2)
    box(ax, 4.0, 22.0, 26.0, 12.0, fc=PALE, ec=LINE)
    label(ax, 17.0, 30.6, "间接调用点", fs=8.4, color=INK, weight="bold")
    label(ax, 17.0, 25.8, "void (*)(int)", fs=7.0, color=GREY)

    targets = [("目标 A　签名一致", "允许跳转", 41.0, PALE_BLUE, "#b6c4d2", BLUE),
               ("目标 B　签名一致", "允许跳转", 25.0, PALE_BLUE, "#b6c4d2", BLUE),
               ("栈上的数据", "不在合法集合内", 8.0, PALE_WARN, "#dcc3b6", WARN)]
    for name, note, y, fc, ec, color in targets:
        box(ax, 46.0, y, 48.0, 11.0, fc=fc, ec=ec)
        label(ax, 70.0, y + 7.0, name, fs=7.8, color=color, weight="bold")
        label(ax, 70.0, y + 3.2, note, fs=6.8, color=GREY)

    arrow(ax, (30.4, 30.0), (45.6, 46.5), color=ACCENT_2, rad=-0.08)
    arrow(ax, (30.4, 27.4), (45.6, 30.5), color=ACCENT_2)
    arrow(ax, (30.4, 24.8), (38.0, 16.2), color=WARN, lw=1.1,
          ls=(0, (4, 2.4)), ms=7)

    # 拦截标记，落在断开的箭头与目标框之间的空白处
    ax.plot([39.4, 42.4], [14.4, 17.4], color=WARN, lw=1.5, zorder=5)
    ax.plot([39.4, 42.4], [17.4, 14.4], color=WARN, lw=1.5, zorder=5)
    label(ax, 41.0, 11.4, "拦截", fs=6.8, color=WARN)

    return save(fig, "06", "cfi-targets.png")


if __name__ == "__main__":
    layout_32bit()
    cfi_targets()
