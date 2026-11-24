# -*- coding: utf-8 -*-
"""第二十三章插图：供应链的三类注入点、一次事件的传播链。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def injection_points():
    fig, ax = setup(5.3, 3.0)

    names = ["源码仓库", "构建与发布", "分发通道", "下游组织"]
    xs = [1.0, 27.0, 53.0, 79.0]
    w = 20.5
    for name, x in zip(names, xs):
        box(ax, x, 22.0, w, 12.0, fc=PALE, ec=LINE)
        label(ax, x + w / 2, 28.0, name, fs=8.4, color=INK, weight="bold")
    for x in xs[:3]:
        arrow(ax, (x + w + 0.5, 28.0), (x + w + 4.6, 28.0))

    notes = ["xz-utils 2024", "SolarWinds 2020", "3CX 2023", "依赖混淆 2021"]
    for note, x in zip(notes, xs):
        label(ax, x + w / 2, 16.6, note, fs=6.8, color=GREY)

    marks = [
        (11.25, "A　源码投毒", "以维护者身份待了两年"),
        (50.25, "B　构建与更新劫持", "签名证书照常打上去"),
        (89.25, "C　依赖抢注", "内部包名被公开注册"),
    ]
    for x, title, note in marks:
        label(ax, x, 47.6, title, fs=7.6, color=WARN, weight="bold")
        label(ax, x, 44.0, note, fs=6.6, color=GREY)
        ax.plot([x, x], [42.6, 34.8], color=WARN, lw=0.9,
                ls=(0, (2.2, 2.2)), zorder=3)

    label(ax, 50.0, 5.4, "三个位置都在你收到的东西之前，等它到手时校验已经做完了",
          fs=7.4, color=SOFT)

    return save(fig, "23", "injection-points.png")


def propagation():
    fig, ax = setup(5.3, 3.2)

    rows = [
        (48.0, "源码仓库", "后门写进一个源文件，提交记录看起来正常"),
        (35.0, "构建与签名", "用厂商自己的证书，产物只大几十 KB"),
        (22.0, "更新分发", "客户在管理界面里点下“安装更新”"),
        (9.0, "下游组织", "约 1.8 万次下载，约 100 家被继续渗透"),
    ]
    for y, name, note in rows:
        box(ax, 2.0, y, 42.0, 8.0, fc=PALE, ec=LINE)
        label(ax, 6.0, y + 4.0, name, fs=8.6, color=INK, ha="left",
              weight="bold")
        label(ax, 48.0, y + 4.0, note, fs=7.0, color=SOFT, ha="left")

    for y in (48.0, 35.0, 22.0):
        arrow(ax, (23.0, y), (23.0, y - 4.8))

    box(ax, 2.0, 0.6, 96.0, 6.2, fc=PALE_WARN, ec="#dcc4b6")
    label(ax, 50.0, 3.7, "从植入到被发现约九个月，期间所有流量都像正常的升级检查",
          fs=7.4, color=WARN)

    return save(fig, "23", "propagation.png")


if __name__ == "__main__":
    injection_points()
    propagation()
