# -*- coding: utf-8 -*-
"""第八章插图：浏览器多进程与沙箱边界，JIT 类型假设被打破。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def sandbox_model():
    fig, ax = setup(5.3, 3.5)
    box(ax, 24.0, 50.0, 52.0, 10.0, fc="white", ec=LINE)
    label(ax, 50.0, 56.8, "浏览器进程（broker）", fs=8.4, color=INK,
          weight="bold")
    label(ax, 50.0, 52.6, "持有文件句柄、网络与全部权限", fs=6.7, color=GREY)

    ax.plot([10.0, 90.0], [44.0, 44.0], color=ACCENT_2, lw=1.0, zorder=2)
    arrow(ax, (50.0, 49.8), (50.0, 44.2), color=ACCENT_2, lw=1.0, ms=7)
    label(ax, 3.0, 45.6, "IPC", fs=6.6, color=ACCENT_2, ha="left",
          weight="bold")

    kids = [("渲染进程", "站点 A", 2.0), ("渲染进程", "站点 B", 26.0),
            ("网络服务", "代收请求", 50.0), ("GPU 进程", "光栅与合成", 74.0)]
    for name, note, x in kids:
        rect(ax, x, 22.0, 21.5, 20.0, fc="#f7f8f6", ec=LINE, lw=0.8,
             zorder=1)
        box(ax, x + 1.6, 26.0, 18.3, 9.0, fc="white", ec=LINE)
        label(ax, x + 10.7, 32.4, name, fs=7.2, color=INK, weight="bold")
        label(ax, x + 10.7, 28.6, note, fs=6.4, color=GREY)
        arrow(ax, (x + 10.7, 43.8), (x + 10.7, 40.4), color=ACCENT_2, lw=0.9,
              ms=6)

    label(ax, 3.6, 38.4, "沙箱边界", fs=5.9, color=GREY, ha="left")

    box(ax, 2.0, 4.0, 94.0, 9.0, fc=PALE_2, ec="#dcd8cc")
    label(ax, 49.0, 8.5, "操作系统资源　文件、注册表、设备、其他进程",
          fs=7.2, color=SOFT)

    arrow(ax, (12.0, 21.6), (12.0, 14.4), color=WARN, lw=1.1,
          ls=(0, (4, 2.4)), ms=7)
    ax.plot([10.2, 13.8], [16.0, 19.6], color=WARN, lw=1.5, zorder=5)
    ax.plot([10.2, 13.8], [19.6, 16.0], color=WARN, lw=1.5, zorder=5)
    label(ax, 16.4, 18.0, "系统调用被内核拒绝", fs=6.6, color=WARN, ha="left")
    return save(fig, "08", "sandbox-model.png")


def jit_confusion():
    fig, ax = setup(5.3, 3.45)
    label(ax, 3.0, 60.4, "编译时的类型假设", fs=7.2, color=GREY, ha="left")
    label(ax, 56.0, 60.4, "同一数组后来的实际类型", fs=7.2, color=GREY,
          ha="left")

    box(ax, 3.0, 46.0, 41.0, 8.6, fc=PALE_BLUE, ec="#b6c4d2")
    label(ax, 23.5, 50.3, "PACKED_DOUBLE", fs=7.4, color=BLUE, weight="bold")
    box(ax, 56.0, 46.0, 41.0, 8.6, fc=PALE_WARN, ec="#dcc3b6")
    label(ax, 76.5, 50.3, "PACKED_ELEMENTS", fs=7.4, color=WARN,
          weight="bold")

    arrow(ax, (44.4, 50.3), (55.4, 50.3), color=ACCENT_2, lw=1.0, ms=7)
    label(ax, 49.9, 53.5, "类型提升", fs=6.4, color=GREY)

    left_cells = ["1.5", "2.5", "3.5"]
    right_cells = ["指向对象", "指向对象", "指向对象"]
    for i, (lc, rc) in enumerate(zip(left_cells, right_cells)):
        lx = 3.0 + i * 13.5
        rx = 56.0 + i * 13.5
        box(ax, lx, 33.0, 13.0, 9.0, fc="white", ec=LINE, lw=0.9)
        label(ax, lx + 6.5, 37.5, lc, fs=7.2, color=SOFT)
        box(ax, rx, 33.0, 13.0, 9.0, fc="white", ec=LINE, lw=0.9)
        label(ax, rx + 6.5, 37.5, rc, fs=6.5, color=SOFT)

    label(ax, 23.5, 29.0, "每格 8 字节，存浮点数", fs=6.7, color=GREY)
    label(ax, 76.5, 29.0, "每格 8 字节，存地址", fs=6.7, color=GREY)

    arrow(ax, (6.0, 32.8), (6.0, 21.4), color=ACCENT, lw=1.0, ms=7)
    arrow(ax, (94.0, 32.8), (94.0, 21.4), color=ACCENT, lw=1.0, ms=7)

    box(ax, 3.0, 8.0, 41.0, 13.0, fc="white", ec=LINE)
    label(ax, 23.5, 16.4, "按 double 读", fs=7.4, color=INK, weight="bold")
    label(ax, 23.5, 12.2, "地址被当成数值", fs=6.7, color=GREY)
    box(ax, 56.0, 8.0, 41.0, 13.0, fc="white", ec=LINE)
    label(ax, 76.5, 16.4, "按 double 写", fs=7.4, color=INK, weight="bold")
    label(ax, 76.5, 12.2, "数值被当成指针", fs=6.7, color=GREY)
    return save(fig, "08", "jit-confusion.png")


if __name__ == "__main__":
    sandbox_model()
    jit_confusion()
