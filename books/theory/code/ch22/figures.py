# -*- coding: utf-8 -*-
"""第二十二章插图：构建链的五个环节与注入点、依赖树的形状。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)

STAGES = [
    ("编译", "gcc / rustc", ["构建脚本", "编译器后门"]),
    ("链接", "ld / lld", ["依赖投毒", "RPATH 劫持"]),
    ("打包", "deb / rpm", ["安装脚本", "多余文件"]),
    ("签名", "GPG / KMS", ["密钥泄露", "流程被绕"]),
    ("分发", "镜像站 / CDN", ["镜像替换", "更新劫持"]),
]
XS = [1.0, 20.5, 40.0, 59.5, 79.0]
W = 17.0


def build_chain():
    fig, ax = setup(5.3, 2.9)

    for x in XS[:-1]:
        arrow(ax, (x + W + 0.3, 36.5), (x + W + 2.0, 36.5), color=ACCENT_2,
              lw=1.1, ms=5)

    for (title, tool, notes), x in zip(STAGES, XS):
        box(ax, x, 30.0, W, 13.0, fc="white", ec=LINE)
        label(ax, x + W / 2, 38.6, title, fs=7.8, color=INK, weight="bold")
        label(ax, x + W / 2, 34.4, tool, fs=5.9, color=SOFT)
        arrow(ax, (x + W / 2, 29.6), (x + W / 2, 25.4), color=WARN, lw=0.9,
              ls=(0, (2.2, 1.8)), ms=5)
        label(ax, x + W / 2, 22.4, notes[0], fs=6.1, color=WARN)
        label(ax, x + W / 2, 18.8, notes[1], fs=6.1, color=WARN)

    # 括号
    def bracket(x1, x2, y, text):
        ax.plot([x1, x1, x2, x2], [y - 1.6, y, y, y - 1.6], color=ACCENT,
                lw=1.0, zorder=4)
        label(ax, (x1 + x2) / 2, y + 2.9, text, fs=6.3, color=ACCENT,
              weight="bold")

    bracket(1.0, 57.0, 48.0, "可复现构建：重建并比对")
    bracket(59.5, 96.0, 48.0, "透明日志：签名可检索")

    label(ax, 50.0, 5.0, "编译器把源码变成产物，这一步没有留下可验证的痕迹",
          fs=6.4, color=GREY)
    return save(fig, "22", "build-chain.png")


def dependency_tree():
    fig, ax = setup(5.3, 2.65)

    box(ax, 40.0, 2.0, 20.0, 7.0, fc=PALE_BLUE, ec="#a8bccd")
    label(ax, 50.0, 5.5, "你的项目", fs=7.6, color=BLUE, weight="bold")

    directs = [("直接依赖 A", 4.0), ("直接依赖 B", 39.0), ("直接依赖 C", 74.0)]
    origins = [44.0, 50.0, 56.0]
    for (name, x), ox in zip(directs, origins):
        box(ax, x, 17.0, 22.0, 7.0, fc="white", ec=LINE)
        label(ax, x + 11.0, 20.5, name, fs=7.2, color=INK)
        arrow(ax, (ox, 9.2), (x + 11.0, 16.7), color=ACCENT_2, lw=0.9, ms=5)
        arrow(ax, (x + 11.0, 24.2), (x + 11.0, 30.7), color=ACCENT_2, lw=0.9,
              ms=5)

    rect(ax, 2.0, 31.0, 96.0, 8.0, fc=PALE_WARN)
    ax.plot([2.0, 98.0], [31.0, 31.0], color="#dcc3b6", lw=0.9, ls=(0, (3, 2)))
    ax.plot([2.0, 98.0], [39.0, 39.0], color="#dcc3b6", lw=0.9, ls=(0, (3, 2)))

    n, w, gap = 14, 4.0, 2.6
    start = 50.0 - (n * w + (n - 1) * gap) / 2
    for i in range(n):
        x = start + i * (w + gap)
        fc = WARN if i == 8 else "white"
        ec = WARN if i == 8 else "#d6c9bf"
        rect(ax, x, 33.5, w, 3.0, fc=fc, ec=ec, lw=0.9, zorder=3)

    label(ax, 28.0, 43.6, "传递依赖：几十到几百个，版本由别人选", fs=6.3,
          color=SOFT)
    ax.plot([59.9, 59.9], [36.4, 41.6], color=WARN, lw=0.9, zorder=4)
    label(ax, 61.6, 41.6, "被投毒的一格", fs=6.1, color=WARN, ha="left")
    return save(fig, "22", "dependency-tree.png")


if __name__ == "__main__":
    build_chain()
    dependency_tree()
