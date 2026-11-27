# -*- coding: utf-8 -*-
"""第二十章插图：数据包路径与 netfilter 钩子、eBPF 的挂载位置。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def _hook(ax, x, y, w, h, title, subs, fs=7.4):
    """带优先级小字的钩子框。"""
    box(ax, x, y, w, h, fc=PALE_BLUE, ec="#a8bccd", lw=1.0)
    cy = y + h / 2
    step = 2.8
    n = len(subs)
    label(ax, x + w / 2, cy + step * n / 2, title, fs=fs, color=BLUE,
          weight="bold")
    for i, s in enumerate(subs):
        label(ax, x + w / 2, cy + step * n / 2 - step * (i + 1), s,
              fs=5.9, color=SOFT)


def packet_path():
    fig, ax = setup(5.3, 3.62)
    h_in, cy_in = 13.5, 52.25
    h_fw, cy_fw = 9.0, 31.5
    h_eg, cy_eg = 13.5, 11.25

    rect(ax, 0, cy_in - h_in / 2 - 1.8, 100, h_in + 3.6, fc="#f7f9f8")
    rect(ax, 0, cy_eg - h_eg / 2 - 1.8, 100, h_eg + 3.6, fc="#f7f9f8")

    label(ax, 1.5, cy_in + h_in / 2 + 3.2, "本机接收", fs=6.6, color=GREY,
          ha="left")
    label(ax, 1.5, cy_eg + h_eg / 2 + 3.2, "本机发送", fs=6.6, color=GREY,
          ha="left")
    label(ax, 41.0, cy_fw + 0.6, "转发", fs=6.4, color=GREY, ha="right")

    box(ax, 8.0, cy_in - h_in / 2, 14.0, h_in, fc="white", ec=LINE)
    label(ax, 15.0, cy_in + 3.8, "网卡与驱动", fs=7.4, color=INK,
          weight="bold")
    label(ax, 15.0, cy_in - 0.4, "DMA 写 RX 环", fs=5.9, color=SOFT)
    label(ax, 15.0, cy_in - 3.2, "NAPI 轮询", fs=5.9, color=SOFT)

    _hook(ax, 25.0, cy_in - h_in / 2, 20.0, h_in, "PREROUTING",
          ["defrag −400", "conntrack −200", "dnat −100"])

    box(ax, 48.0, cy_in - h_in / 2, 14.0, h_in, fc="white", ec=LINE)
    label(ax, 55.0, cy_in + 1.4, "路由判定", fs=7.4, color=INK,
          weight="bold")
    label(ax, 55.0, cy_in - 2.8, "查 FIB", fs=5.9, color=SOFT)

    _hook(ax, 65.0, cy_in - h_in / 2, 20.0, h_in, "LOCAL_IN",
          ["filter 0", "security 50"])

    box(ax, 88.0, cy_in - h_in / 2, 11.0, h_in, fc="white", ec=LINE)
    label(ax, 93.5, cy_in + 3.8, "应用", fs=7.0, color=INK, weight="bold")
    label(ax, 93.5, cy_in - 1.8, "收队列", fs=5.9, color=SOFT)

    _hook(ax, 48.0, cy_fw - h_fw / 2, 14.0, h_fw, "FORWARD", ["filter 0"],
          fs=7.0)

    box(ax, 8.0, cy_eg - h_eg / 2, 14.0, h_eg, fc="white", ec=LINE)
    label(ax, 15.0, cy_eg + 1.4, "本机进程", fs=7.2, color=INK,
          weight="bold")
    label(ax, 15.0, cy_eg - 2.8, "发出", fs=5.9, color=SOFT)

    _hook(ax, 25.0, cy_eg - h_eg / 2, 20.0, h_eg, "LOCAL_OUT",
          ["raw −300", "conntrack −200", "mangle −150"])

    box(ax, 48.0, cy_eg - h_eg / 2, 14.0, h_eg, fc="white", ec=LINE)
    label(ax, 55.0, cy_eg + 1.4, "路由判定", fs=7.4, color=INK,
          weight="bold")
    label(ax, 55.0, cy_eg - 2.8, "查 FIB", fs=5.9, color=SOFT)

    _hook(ax, 65.0, cy_eg - h_eg / 2, 20.0, h_eg, "POSTROUTING",
          ["mangle −150", "snat 100"])

    box(ax, 88.0, cy_eg - h_eg / 2, 11.0, h_eg, fc="white", ec=LINE)
    label(ax, 93.5, cy_eg + 1.4, "网卡", fs=7.2, color=INK, weight="bold")
    label(ax, 93.5, cy_eg - 2.8, "发出", fs=5.9, color=SOFT)

    for x1, x2 in ((22.0, 24.7), (45.0, 47.7), (62.0, 64.7), (85.0, 87.7)):
        arrow(ax, (x1, cy_in), (x2, cy_in), color=ACCENT_2, lw=1.1, ms=7)
        arrow(ax, (x1, cy_eg), (x2, cy_eg), color=ACCENT_2, lw=1.1, ms=7)

    arrow(ax, (55.0, cy_in - h_in / 2 - 0.2), (55.0, cy_fw + h_fw / 2 + 0.2),
          color=ACCENT_2, lw=1.1, ms=7)
    ax.plot([62.0, 74.0], [cy_fw, cy_fw], color=ACCENT_2, lw=1.1, zorder=3,
            solid_capstyle="butt")
    arrow(ax, (74.0, cy_fw - 0.1), (74.0, cy_eg + h_eg / 2 + 0.2),
          color=ACCENT_2, lw=1.1, ms=7)

    label(ax, 50.0, 65.5,
          "框内数字为注册优先级（NF_IP_PRI_*），越小越先执行",
          fs=6.3, color=GREY)
    return save(fig, "20", "packet-path.png")


def ebpf_hooks():
    fig, ax = setup(5.3, 3.30)
    BX, BW = 47.0, 51.0

    bands = [
        ("应用进程", "read() 与业务逻辑", 51.0, 7.0, PALE_2, LINE),
        ("套接字层", "sk_filter · cgroup · sockops", 39.0, 9.0, "white", LINE),
        ("协议栈", "ip_rcv → 路由 → tcp_v4_rcv", 24.0, 12.0, PALE_BLUE,
         "#a8bccd"),
        ("驱动与 NAPI", "已分配 sk_buff", 15.0, 7.0, "white", LINE),
        ("网卡", "只有 DMA 缓冲区", 6.0, 7.0, PALE_2, LINE),
    ]
    for title, sub, y, h, fc, ec in bands:
        box(ax, BX, y, BW, h, fc=fc, ec=ec)
        label(ax, BX + BW / 2, y + h / 2 + 1.5, title, fs=7.6, color=INK,
              weight="bold")
        label(ax, BX + BW / 2, y + h / 2 - 1.6, sub, fs=5.9, color=SOFT)

    points = [
        (49.5, "cgroup / LSM", ""),
        (43.5, "socket filter", ""),
        (37.5, "tc egress", ""),
        (31.0, "kprobe / tracepoint", "任意内核函数"),
        (23.0, "tc ingress", ""),
        (14.5, "XDP", "xdp_md，无 sk_buff"),
    ]
    for y, name, note in points:
        ax.plot([44.0, 46.4], [y, y], color=ACCENT, lw=1.4, zorder=5,
                solid_capstyle="butt")
        ax.plot([46.4], [y], marker="o", ms=3.4, color=ACCENT, zorder=6)
        label(ax, 43.2, y, name, fs=6.6, color=INK, ha="right")
        if note:
            label(ax, 43.2, y - 2.6, note, fs=5.6, color=GREY, ha="right")

    label(ax, 3.0, 2.6, "越靠下，包越原始，能绕过的代码越多，能做的判断越少",
          fs=6.3, color=GREY, ha="left")
    return save(fig, "20", "ebpf-hooks.png")


if __name__ == "__main__":
    packet_path()
    ebpf_hooks()
