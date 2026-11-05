# -*- coding: utf-8 -*-
"""第十三章插图：恶意程序谱系、蠕虫增长曲线、扫描-感染循环。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from common import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                    PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label, rect,
                    save, setup)


def malware_taxonomy():
    fig, ax = setup(5.3, 3.05)

    box(ax, 32.0, 47.0, 36.0, 9.0, fc="#dfe7e6", ec="#b7c6c4")
    label(ax, 50.0, 51.5, "恶意程序", fs=10.0, color=ACCENT, weight="bold")

    items = [
        ("病毒", "需要宿主文件\n随宿主一起运行", PALE),
        ("蠕虫", "独立程序\n自己找路传播", PALE_WARN),
        ("木马", "伪装成正常软件\n等人安装", PALE),
        ("后门", "潜伏的通道\n随时可以回来", PALE_BLUE),
        ("逻辑炸弹", "满足条件才发作\n平时完全无害", PALE_2),
    ]
    w, gap = 17.6, 2.2
    x = 1.6
    centers = []
    for name, note, fc in items:
        box(ax, x, 14.0, w, 21.0, fc=fc, ec=LINE)
        label(ax, x + w / 2, 30.0, name, fs=9.2, color=INK, weight="bold")
        label(ax, x + w / 2, 21.0, note, fs=7.0, color=SOFT)
        centers.append(x + w / 2)
        x += w + gap

    ax.plot([50.0, 50.0], [47.0, 43.0], color=GREY, lw=0.9, zorder=1)
    ax.plot([centers[0], centers[-1]], [43.0, 43.0], color=GREY, lw=0.9, zorder=1)
    for cx in centers:
        ax.plot([cx, cx], [43.0, 35.0], color=GREY, lw=0.9, zorder=1)

    label(ax, 50.0, 7.0, "同一样本常把几种手段叠加，分类看的是它靠什么活着、怎么到达下一台机器",
          fs=7.2, color=GREY)
    return save(fig, "13", "malware-taxonomy.png")


def worm_growth():
    fig, ax = setup(5.3, 3.15)
    x0, x1, y0, y1 = 15.0, 92.0, 12.0, 52.0

    # 坐标轴
    ax.plot([x0, x1], [y0, y0], color=GREY, lw=0.9)
    ax.plot([x0, x0], [y0, y1], color=GREY, lw=0.9)

    # 纵轴刻度（只标量程，不标无依据的测量点）
    for v in (0, 3, 6):
        yy = y0 + (y1 - y0) * v / 7.5
        ax.plot([x0 - 0.8, x0], [yy, yy], color=GREY, lw=0.8)
        label(ax, x0 - 2.2, yy, str(v), fs=7.0, color=GREY, ha="right")

    # 横轴刻度
    for t in (0, 2, 4, 6, 8, 10):
        xx = x0 + (x1 - x0) * t / 10.0
        ax.plot([xx, xx], [y0, y0 - 0.8], color=GREY, lw=0.8)
        label(ax, xx, y0 - 3.4, str(t), fs=7.0, color=GREY)

    label(ax, (x0 + x1) / 2, y0 - 7.8, "释放后经过的时间（分钟）", fs=7.4, color=SOFT)
    label(ax, x0 - 8.4, (y0 + y1) / 2, "累计感染\n（万台）", fs=7.4, color=SOFT,
          ha="center", rotation=90)

    # 曲线：按论文给出的早期倍增时间与十分钟总量还原形状
    t = np.linspace(0, 10, 400)
    k, t0 = 1.55, 4.1
    y = 7.5 / (1.0 + np.exp(-k * (t - t0)))
    xs = x0 + (x1 - x0) * t / 10.0
    ys = y0 + (y1 - y0) * y / 7.5
    ax.plot(xs, ys, color=ACCENT, lw=1.6, zorder=4,
            solid_capstyle="round")

    # 峰值位置
    ax.plot([xs[-1]], [ys[-1]], "o", ms=4.0, color=WARN, zorder=5)
    label(ax, x1 - 2.6, 44.6, "约 7.5 万台", fs=7.6, color=WARN, ha="right",
          weight="bold")

    # 指数段标注：文字放在曲线左上方的空白处
    it = int(2.2 / 10.0 * (len(t) - 1))
    label(ax, 16.5, 40.0, "每 8.5 秒翻一倍", fs=7.2, color=ACCENT_2, ha="left")
    arrow(ax, (24.0, 37.6), (xs[it] + 1.5, ys[it] + 2.8), color=ACCENT_2,
          lw=0.9, ms=6)

    label(ax, 58.0, 26.0, "易感主机被扫完，曲线走平", fs=7.2, color=SOFT, ha="left")
    return save(fig, "13", "worm-growth.png")


def worm_loop():
    fig, ax = setup(5.3, 2.85)

    w, h = 27.0, 11.0
    specs = [(5.0, 37.0, "① 扫描地址", "按地址空间挑候选"),
             (68.0, 37.0, "② 试探连接", "看端口是否有回应"),
             (68.0, 11.0, "③ 打进漏洞", "发送一段攻击载荷"),
             (5.0, 11.0, "④ 复制自身", "新机器成为扫描者")]
    for x, y, name, note in specs:
        box(ax, x, y, w, h, fc=PALE, ec=LINE)
        label(ax, x + w / 2, y + h - 3.9, name, fs=9.2, color=INK, weight="bold")
        label(ax, x + w / 2, y + 3.6, note, fs=7.0, color=GREY)

    arrow(ax, (32.0, 42.5), (68.0, 42.5))
    arrow(ax, (81.5, 37.0), (81.5, 22.0))
    arrow(ax, (68.0, 16.5), (32.0, 16.5))
    arrow(ax, (18.5, 22.0), (18.5, 37.0))

    label(ax, 50.0, 46.4, "找到活的地址", fs=7.0, color=ACCENT)
    label(ax, 85.2, 29.5, "利用成功", fs=7.0, color=ACCENT, ha="left")
    label(ax, 50.0, 13.4, "植入副本并启动", fs=7.0, color=ACCENT)
    label(ax, 14.8, 29.5, "循环继续", fs=7.0, color=ACCENT, ha="right")

    label(ax, 50.0, 33.0, "整个循环里", fs=8.0, color=SOFT)
    label(ax, 50.0, 27.6, "没有人的位置", fs=8.0, color=WARN, weight="bold")
    return save(fig, "13", "worm-loop.png")


if __name__ == "__main__":
    malware_taxonomy()
    worm_growth()
    worm_loop()
