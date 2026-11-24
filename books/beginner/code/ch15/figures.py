# -*- coding: utf-8 -*-
"""第十五章插图：检测流水线、基率谬误算例、更新链上的注入点。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                    PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label, rect,
                    save, setup)


def av_pipeline():
    fig, ax = setup(5.3, 3.3)

    rect(ax, 2.0, 51.6, 92.4, 7.6, fc="#f2f4f3")
    label(ax, 48.2, 55.4, "输入同一份东西：磁盘上的文件、跑着的进程、内存、网络流量",
          fs=7.2, color=SOFT)

    stages = [
        ("特征码", "已知样本的\n固定字节串", PALE),
        ("静态启发", "结构可疑的\n混淆痕迹", PALE),
        ("沙箱", "放它跑一遍\n看改了什么", PALE_BLUE),
        ("模型打分", "按相似度\n给样本打分", PALE_BLUE),
        ("行为阻断", "内核里盯着\n每一步动作", PALE_WARN),
    ]
    w, gap = 15.6, 3.6
    x = 2.0
    xs = []
    for i, (name, note, fc) in enumerate(stages):
        box(ax, x, 30.0, w, 13.0, fc=fc, ec=LINE)
        label(ax, x + w / 2, 39.6, f"第 {i + 1} 代", fs=6.2, color=GREY)
        label(ax, x + w / 2, 34.4, name, fs=8.0, color=INK, weight="bold")
        label(ax, x + w / 2, 24.4, note, fs=6.4, color=SOFT)
        xs.append(x)
        if i:
            arrow(ax, (xs[i - 1] + w, 36.5), (x, 36.5), lw=1.0, ms=7)
        x += w + gap

    arrow(ax, (9.8, 51.4), (9.8, 43.2), lw=1.0, ms=7)
    label(ax, 11.4, 47.2, "逐个过一遍", fs=6.6, color=ACCENT, ha="left")

    label(ax, 50.0, 10.6, "每往后一代，补的是上一代的盲区，付的是速度和资源",
          fs=7.2, color=GREY)
    label(ax, 50.0, 4.8, "代价还有一层，能看见的东西越多，越容易被针对",
          fs=7.2, color=GREY)
    return save(fig, "15", "av-pipeline.png")


def base_rate():
    fig, ax = setup(5.3, 2.95)

    x0, limit = 20.0, 110.0
    span = 66.0
    sx = span / limit

    label(ax, 50.0, 50.6, "1 万台机器，10 台真中毒（0.1%），检测率 99%",
          fs=7.4, color=SOFT)

    ax.plot([x0, x0], [8.0, 44.0], color=GREY, lw=0.9)
    for v in (0, 50, 100):
        xx = x0 + v * sx
        ax.plot([xx, xx], [8.0, 7.2], color=GREY, lw=0.8)
        label(ax, xx, 4.6, str(v), fs=6.8, color=GREY)

    # 上一条：误报率 1%
    py, ph = 33.0, 8.4
    tp, fp = 9.9, 99.9
    box(ax, x0, py, tp * sx, ph, fc="#b9d2cb", ec="none", zorder=2)
    box(ax, x0 + tp * sx, py, fp * sx, ph, fc="#eceae4", ec="none", zorder=2)
    label(ax, (x0 + tp * sx) / 2, py + ph + 3.6, "真中毒 9.9", fs=6.6,
          color=ACCENT)
    label(ax, x0 + (tp + fp / 2) * sx, py + ph / 2, "误报 99.9", fs=7.0,
          color=SOFT)
    label(ax, 16.0, py + ph / 2, "误报率 1%", fs=7.2, color=INK, ha="right",
          weight="bold")
    label(ax, 16.0, py + ph / 2 - 5.4, "报警 109.8 台", fs=6.6, color=GREY,
          ha="right")
    label(ax, x0 + (tp + fp) * sx + 1.2, py + ph / 2, "9%", fs=9.4,
          color=WARN, ha="left", weight="bold")

    # 下一条：误报率 0.01%
    py2 = 15.0
    tp2, fp2 = 9.9, 1.0
    box(ax, x0, py2, tp2 * sx, ph, fc="#b9d2cb", ec="none", zorder=2)
    box(ax, x0 + tp2 * sx, py2, fp2 * sx, ph, fc="#eceae4", ec="none", zorder=2)
    label(ax, 16.0, py2 + ph / 2, "误报率 0.01%", fs=7.2, color=INK,
          ha="right", weight="bold")
    label(ax, 16.0, py2 + ph / 2 - 5.4, "报警 10.9 台", fs=6.6, color=GREY,
          ha="right")
    label(ax, x0 + (tp2 + fp2) * sx + 1.2, py2 + ph / 2, "91%", fs=9.4,
          color=ACCENT, ha="left", weight="bold")

    label(ax, 55.0, 27.2, "同样一批机器，误报率降两个数量级，报警里真中毒的比例从 9% 涨到 91%",
          fs=6.8, color=GREY)
    label(ax, 55.0, 1.2, "横轴为报警台数，深色块是其中真中毒的部分", fs=6.6,
          color=GREY)
    return save(fig, "15", "base-rate.png")


def supply_chain():
    fig, ax = setup(5.3, 3.0)

    rect(ax, 2.0, 43.4, 96.0, 7.2, fc="#f4f2ee")
    label(ax, 50.0, 47.0, "客户信任的是签名，签名由这条链一路传下来", fs=7.2,
          color=SOFT)

    stages = ["开发者", "源码仓库", "构建与签名", "更新服务器", "客户机器"]
    w, gap = 15.6, 3.8
    x = 3.4
    centers = []
    for name in stages:
        box(ax, x, 30.0, w, 8.4, fc=PALE, ec=LINE)
        label(ax, x + w / 2, 34.2, name, fs=7.6, color=INK, weight="bold")
        centers.append(x + w / 2)
        x += w + gap
    for i in range(len(stages) - 1):
        sx = 3.4 + i * (w + gap) + w
        arrow(ax, (sx, 34.2), (sx + gap, 34.2), lw=1.0, ms=7)

    marks = [(1, "xz-utils", "2024 年", ["维护者被长期社工", "源码里埋钩子"]),
             (2, "SolarWinds", "2020 年", ["构建环节被植入", "后门代码"]),
             (3, "CCleaner", "2017 年", ["厂商分发渠道", "被换成带毒版本"])]
    for idx, title, year, body in marks:
        cx = centers[idx]
        ax.plot([cx, cx], [29.6, 24.4], color=WARN, lw=0.9, ls=(0, (3, 2.2)))
        ax.plot([cx], [29.4], "o", ms=3.6, color=WARN, zorder=5)
        label(ax, cx, 21.8, title, fs=6.6, color=WARN, weight="bold")
        label(ax, cx, 18.0, year, fs=6.2, color=GREY)
        label(ax, cx, 14.0, body[0], fs=6.2, color=SOFT)
        label(ax, cx, 10.2, body[1], fs=6.2, color=SOFT)

    label(ax, 50.0, 4.6, "链上任何一环被动过，恶意代码都会带着正规签名进门",
          fs=7.2, color=GREY)
    return save(fig, "15", "supply-chain.png")


if __name__ == "__main__":
    av_pipeline()
    base_rate()
    supply_chain()
