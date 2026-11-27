# -*- coding: utf-8 -*-
"""第二十七章插图：端到端加密的信封、三种路径的信任转移。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def e2ee_envelope():
    fig, ax = setup(5.3, 3.0)
    box(ax, 10.0, 10.0, 80.0, 42.0, fc="#fbfbf8", ec=LINE, lw=1.0)
    label(ax, 50.0, 56.0, "服务器能看到的", fs=7.4, color=INK, weight="bold")

    left = ["发件人", "收件人", "时间", "消息大小"]
    for i, text in enumerate(left):
        y = 44.0 - i * 7.0
        box(ax, 14.0, y - 4.6, 30.0, 6.2, fc=PALE_WARN, ec="#e2ccc0", lw=0.7)
        label(ax, 29.0, y - 1.5, text, fs=6.4, color=WARN)

    box(ax, 50.0, 16.0, 36.0, 30.0, fc="#e6ecec", ec="#b9c9c5", lw=0.9)
    label(ax, 68.0, 40.0, "正文与附件", fs=7.0, color=ACCENT, weight="bold")
    label(ax, 68.0, 34.0, "只有两端持有密钥", fs=6.2, color=GREY)
    label(ax, 68.0, 24.0, "服务器只转发密文", fs=6.2, color=GREY)

    label(ax, 50.0, 5.0, "这些可读字段合起来就是元数据，足以画出社交关系", fs=6.8,
          color=SOFT)
    return save(fig, "27", "e2ee-envelope.png")


def trust_shift():
    fig, ax = setup(5.3, 3.1)
    rows = [("直连", ["你", "运营商", "站点"], 46.0, "运营商看到目标域名"),
            ("VPN", ["你", "VPN 服务商", "站点"], 28.0, "服务商看到目标域名"),
            ("Tor", ["你", "入口", "中继", "出口", "站点"], 10.0, "没有单点能拼全路径")]
    for name, hops, y, note in rows:
        label(ax, 8.0, y + 4.0, name, fs=7.4, color=INK, weight="bold")
        w = 70.0 / len(hops)
        for i, hop in enumerate(hops):
            x = 18.0 + i * (w + 2.0)
            fc = PALE_BLUE if hop in ("你", "站点") else PALE
            box(ax, x, y, w, 8.0, fc=fc, ec=LINE, lw=0.8)
            label(ax, x + w / 2, y + 4.0, hop, fs=6.0, color=SOFT)
        label(ax, 90.0, y + 4.0, note, fs=5.8, color=GREY, ha="left")

    label(ax, 50.0, 2.0, "加密保护内容，路径决定谁仍然知道你在和谁说话", fs=6.8,
          color=SOFT)
    return save(fig, "27", "trust-shift.png")


if __name__ == "__main__":
    e2ee_envelope()
    trust_shift()
