# -*- coding: utf-8 -*-
"""第二十一章插图：启动链的验证与度量、TEE 的信任边界。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)

STAGES = [
    ("Boot ROM", "CRTM", "PCR 0"),
    ("UEFI 固件", "DXE · BDS", "PCR 1–3"),
    ("引导器", "shim · GRUB", "PCR 4–5"),
    ("内核", "vmlinuz", "PCR 8–9"),
    ("init", "用户态", "PCR 10"),
]
XS = [1.0, 21.0, 41.0, 61.0, 81.0]
W = 17.0


def boot_chain():
    fig, ax = setup(5.3, 2.95)

    label(ax, 50.0, 52.0, "实线为验签（阻断），虚线为度量（只记录）",
          fs=6.4, color=GREY)

    box(ax, 1.0, 43.0, 97.0, 6.2, fc=PALE_WARN, ec="#dcc3b6")
    label(ax, 49.5, 46.1, "信任根　芯片内不可改写的 ROM 与熔丝中的公钥哈希",
          fs=7.4, color=WARN, weight="bold")

    for (title, sub, pcr), x in zip(STAGES, XS):
        box(ax, x, 23.0, W, 11.0, fc="white", ec=LINE)
        label(ax, x + W / 2, 30.2, title, fs=7.4, color=INK, weight="bold")
        label(ax, x + W / 2, 26.0, sub, fs=5.9, color=SOFT)
        box(ax, x, 11.0, W, 6.4, fc=PALE_BLUE, ec="#a8bccd")
        label(ax, x + W / 2, 14.2, pcr, fs=6.2, color=BLUE)
        arrow(ax, (x + W / 2, 22.8), (x + W / 2, 17.6), color=BLUE, lw=0.9,
              ls=(0, (2.2, 1.8)), ms=5)

    for x in XS[:-1]:
        arrow(ax, (x + W + 0.3, 28.5), (x + W + 2.7, 28.5), color=ACCENT,
              lw=1.2, ms=6)

    arrow(ax, (9.5, 42.7), (9.5, 34.3), color=WARN, lw=1.2, ms=7)

    label(ax, 50.0, 4.0, "度量值在重启前一直留在 PCR 里，一串值只对应一条扩展序列",
          fs=6.4, color=GREY)
    return save(fig, "21", "boot-chain.png")


def tee_boundary():
    fig, ax = setup(5.3, 3.5)

    rect(ax, 3.0, 3.0, 94.0, 6.0, fc="#f2f1ea")
    label(ax, 50.0, 6.0, "共享微架构：缓存、TLB、内存控制器、电源管理",
          fs=6.5, color=SOFT)

    label(ax, 3.0, 57.6, "普通世界（不可信）", fs=6.6, color=GREY, ha="left")

    box(ax, 3.0, 42.0, 38.0, 10.0, fc="white", ec=LINE)
    label(ax, 22.0, 48.6, "应用进程", fs=7.6, color=INK, weight="bold")
    label(ax, 22.0, 44.8, "业务逻辑，持有明文", fs=5.9, color=SOFT)

    box(ax, 3.0, 30.0, 38.0, 10.0, fc="white", ec=LINE)
    label(ax, 22.0, 36.4, "操作系统 / hypervisor", fs=7.4, color=INK,
          weight="bold")
    label(ax, 22.0, 32.6, "调度、页表、中断", fs=5.9, color=SOFT)

    box(ax, 3.0, 19.0, 38.0, 8.0, fc="white", ec=LINE)
    label(ax, 22.0, 24.6, "设备与 I/O", fs=7.4, color=INK, weight="bold")
    label(ax, 22.0, 21.4, "DMA、设备固件", fs=5.9, color=SOFT)

    # 共享内存
    box(ax, 44.2, 43.8, 11.6, 6.0, fc=PALE_2, ec=LINE)
    label(ax, 50.0, 46.8, "共享内存", fs=6.1, color=SOFT)

    # TEE
    ax.add_patch(__import__("matplotlib").patches.FancyBboxPatch(
        (55.0, 16.0), 42.0, 42.0,
        boxstyle="round,pad=0,rounding_size=0.9",
        linewidth=1.1, edgecolor=ACCENT, facecolor=PALE_BLUE,
        linestyle=(0, (4, 2)), zorder=1))
    label(ax, 57.0, 55.2, "TEE（TCB 之内）", fs=6.6, color=ACCENT, ha="left")

    for title, sub, y, h in (
            ("认可代码", "度量值由硬件报告", 44.0, 9.0),
            ("密封数据", "只有本 TEE 能解密", 32.0, 8.0),
            ("CPU 与内存加密", "MEE / TZASC", 20.0, 8.0)):
        box(ax, 58.0, y, 36.0, h, fc="white", ec="#a8bccd")
        label(ax, 76.0, y + h - 2.7, title, fs=7.4, color=INK, weight="bold")
        label(ax, 76.0, y + 2.2, sub, fs=5.9, color=SOFT)

    arrow(ax, (41.3, 47.0), (43.9, 47.0), color=ACCENT_2, lw=1.1, ms=6)
    arrow(ax, (56.1, 47.0), (57.7, 47.0), color=ACCENT_2, lw=1.1, ms=6)

    arrow(ax, (76.0, 28.3), (76.0, 31.7), color=ACCENT_2, lw=1.0, ms=6)

    arrow(ax, (41.3, 35.0), (54.6, 35.0), color=WARN, lw=1.0, ms=6,
          ls=(0, (2.4, 1.8)))
    label(ax, 48.0, 37.4, "缺页时序", fs=5.8, color=WARN)

    arrow(ax, (41.3, 23.0), (54.6, 23.0), color=WARN, lw=1.0, ms=6,
          ls=(0, (2.4, 1.8)))
    label(ax, 48.0, 25.3, "DMA", fs=5.8, color=WARN)

    arrow(ax, (88.0, 9.3), (88.0, 15.6), color=WARN, lw=1.0, ms=6,
          ls=(0, (2.4, 1.8)))
    label(ax, 86.0, 12.4, "侧信道", fs=5.8, color=WARN, ha="right")
    return save(fig, "21", "tee-boundary.png")


if __name__ == "__main__":
    boot_chain()
    tee_boundary()
