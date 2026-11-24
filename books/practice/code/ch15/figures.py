# -*- coding: utf-8 -*-
"""第15章插图：C2 的组件与通信路径、检测面与规避代价的权衡。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def c2_components():
    fig, ax = setup(5.3, 3.6)

    nodes = [
        ("操作员", "看结果、发指令", "动作在这里排队"),
        ("团队服务器", "会话与任务队列", "唯一记录真实状态"),
        ("重定向器", "只做转发", "真实地址藏在后面"),
        ("植入体", "定时醒来", "执行并回传结果"),
    ]
    xs = [1.5, 27.5, 53.5, 79.5]
    fcs = [PALE, PALE_BLUE, PALE_BLUE, PALE_WARN]
    w, h, y = 19.0, 11.0, 42.0
    for (name, a1, a2), x, fc in zip(nodes, xs, fcs):
        box(ax, x, y, w, h, fc=fc, ec=LINE)
        label(ax, x + w / 2, y + h / 2, name, fs=7.2, color=INK)
        label(ax, x + w / 2, 27.6, a1, fs=5.7, color=SOFT)
        label(ax, x + w / 2, 24.2, a2, fs=5.7, color=GREY)

    gaps = [(20.8, 27.2), (46.8, 53.2), (72.8, 79.2)]
    for x1, x2 in gaps:
        arrow(ax, (x1, 58.0), (x2, 58.0), color=ACCENT, lw=1.0, ms=6)
        arrow(ax, (x2, 36.6), (x1, 36.6), color=ACCENT_2, lw=1.0, ms=6)

    label(ax, 50.0, 61.4, "任务下发，植入体下次醒来时取走", fs=6.0, color=SOFT)
    label(ax, 50.0, 33.0, "结果回传，走的是同一条连接", fs=6.0, color=SOFT)

    rect(ax, 1.5, 6.0, 97.0, 9.6, fc=PALE_2, ec=LINE, lw=0.8, zorder=1)
    label(ax, 50.0, 12.9, "信标周期只有一个参数，却同时决定操作手感与流量的规律性",
          fs=6.2, color=INK)
    label(ax, 50.0, 8.8, "植入体只往外连，不在目标上开监听端口",
          fs=5.8, color=GREY)

    return save(fig, "15", "c2-components.png")


def detect_tradeoff():
    fig, ax = setup(5.3, 3.4)

    ax.plot([12.0, 94.0], [9.0, 9.0], color=LINE, lw=1.0, zorder=1)
    ax.plot([12.0, 12.0], [9.0, 58.0], color=LINE, lw=1.0, zorder=1)
    arrow(ax, (11.6, 9.0), (95.0, 9.0), color=GREY, lw=0.8, ms=5)
    arrow(ax, (12.0, 8.6), (12.0, 59.5), color=GREY, lw=0.8, ms=5)

    label(ax, 47.0, 4.6, "隐蔽性（越往右越难被规则命中）", fs=6.2, color=GREY)
    label(ax, 5.4, 33.0, "可用性（带宽、时延、交互程度）", fs=6.2, color=GREY,
          rotation=90)

    pts = [
        (30.0, 50.0, "直连 IP + 自签证书", "left"),
        (62.0, 40.0, "走 CDN 的 HTTPS 信标", "left"),
        (56.0, 28.0, "内网 SMB 命名管道", "left"),
        (44.0, 15.0, "DNS 隧道", "left"),
    ]
    for x, y0, text, ha in pts:
        ax.plot([x], [y0], marker="o", ms=4.6, color=ACCENT, zorder=5,
                markeredgecolor="white", markeredgewidth=0.6)
        dx = 2.8 if ha == "left" else -2.8
        label(ax, x + dx, y0, text, fs=6.2, color=INK, ha=ha, va="center")

    ax.plot([85.0], [50.0], marker="x", ms=5.4, color=GREY, zorder=5,
            markeredgewidth=1.1)
    label(ax, 85.0, 45.4, "域名前置（已失效）", fs=6.2, color=GREY)

    label(ax, 36.0, 56.0, "越靠右上，工程与基础设施成本越高", fs=6.0, color=SOFT)
    label(ax, 52.0, 21.5, "越靠左下，越依赖耐性与手工", fs=6.0, color=SOFT)

    return save(fig, "15", "detect-tradeoff.png")


if __name__ == "__main__":
    c2_components()
    detect_tradeoff()
