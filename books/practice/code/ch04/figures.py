# -*- coding: utf-8 -*-
"""第四章插图：从公告到验证的判定流程、PoC 依赖条件清单。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def verify_flow():
    fig, ax = setup(5.3, 3.5)

    x, w = 5, 38
    cx = x + w / 2
    h, gap = 6.2, 4.8
    top = 63.0

    gates = [
        ("公告里写的受影响区间", PALE),
        ("目标组件的真实版本", PALE_2),
        ("补丁是否已被回移", PALE_2),
        ("配置是否开启相关功能", PALE_2),
        ("攻击者能否到达入口", PALE_2),
        ("最小验证　一条请求", PALE_WARN),
    ]
    exits = [
        None,
        ("版本不在区间　结束", GREY),
        ("补丁已打　结束", GREY),
        ("功能关闭　无法复现", WARN),
        ("网络不通　无法判断", WARN),
        None,
    ]

    ys = [top - (h + gap) * i for i in range(len(gates))]
    for (text, fc), y in zip(gates, ys):
        ec = LINE if fc != PALE_WARN else "#d8b6a6"
        box(ax, x, y - h, w, h, fc=fc, ec=ec)
        color = INK if fc != PALE_WARN else WARN
        label(ax, cx, y - h / 2, text, fs=7.6, color=color,
              weight="bold" if fc != PALE_WARN else "bold")

    for i in range(len(gates) - 1):
        y1 = ys[i] - h
        y2 = ys[i + 1]
        arrow(ax, (cx, y1 - 0.3), (cx, y2 + 0.3))

    for i, item in enumerate(exits):
        if item is None:
            continue
        text, color = item
        cy = ys[i] - h / 2
        arrow(ax, (x + w + 0.4, cy), (x + w + 5.4, cy), color=color, lw=1.0)
        label(ax, x + w + 6.6, cy, text, fs=6.6, color=color, ha="left")

    return save(fig, "04", "verify-flow.png")


def poc_deps():
    fig, ax = setup(5.3, 3.0)

    cards = [
        ("版本", PALE, INK, [
            "硬编码的偏移与地址",
            "libc 与内核版本假设",
            "依赖库的版本区间",
        ]),
        ("配置", PALE_BLUE, BLUE, [
            "可选模块是否开启",
            "默认参数与调试开关",
            "端点与路径是否存在",
        ]),
        ("权限", PALE_2, INK, [
            "是否需要已登录会话",
            "是否需要 root 或特权",
            "是否有可写的落地点",
        ]),
        ("网络位置", PALE_WARN, WARN, [
            "从哪个网段可以到达",
            "中间设备是否改写请求",
            "出站能否连到外部",
        ]),
    ]

    positions = [(4, 30), (54, 30), (4, 4), (54, 4)]
    cw, ch = 42, 22

    for (name, fc, color, items), (x, y) in zip(cards, positions):
        ec = LINE if name not in ("网络位置",) else "#d8b6a6"
        box(ax, x, y, cw, ch, fc=fc, ec=ec)
        label(ax, x + 3.4, y + ch - 4.4, name, fs=8.4, color=color,
              weight="bold", ha="left")
        ax.plot([x + 3.4, x + cw - 3.4], [y + ch - 7.6, y + ch - 7.6],
                color=ec, lw=0.8)
        for j, it in enumerate(items):
            label(ax, x + 3.4, y + ch - 11.2 - j * 4.1, "· " + it,
                  fs=6.6, color=SOFT, ha="left")

    return save(fig, "04", "poc-deps.png")


if __name__ == "__main__":
    verify_flow()
    poc_deps()
