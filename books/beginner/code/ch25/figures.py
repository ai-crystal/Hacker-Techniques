# -*- coding: utf-8 -*-
"""第二十五章插图：页面加载的数据流向、指纹信号来源。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def page_flow():
    fig, ax = setup(5.3, 3.2)
    box(ax, 3.0, 40.0, 20.0, 11.0, fc=PALE, ec=LINE)
    label(ax, 13.0, 47.4, "你的浏览器", fs=7.6, color=INK, weight="bold")
    label(ax, 13.0, 43.4, "Cookie / 本地存储", fs=6.2, color=GREY)

    box(ax, 31.0, 40.0, 20.0, 11.0, fc=PALE_BLUE, ec=LINE)
    label(ax, 41.0, 47.4, "目标站点", fs=7.6, color=INK, weight="bold")
    label(ax, 41.0, 43.4, "第一方 Cookie", fs=6.2, color=GREY)

    box(ax, 59.0, 46.0, 20.0, 10.0, fc=PALE_2, ec=LINE)
    label(ax, 69.0, 51.0, "统计脚本", fs=7.2, color=SOFT)
    box(ax, 59.0, 34.0, 20.0, 10.0, fc=PALE_2, ec=LINE)
    label(ax, 69.0, 39.0, "广告脚本", fs=7.2, color=SOFT)
    box(ax, 59.0, 22.0, 20.0, 10.0, fc=PALE_2, ec=LINE)
    label(ax, 69.0, 27.0, "CDN", fs=7.2, color=SOFT)

    box(ax, 84.0, 40.0, 13.0, 11.0, fc=PALE_WARN, ec="#e2ccc0")
    label(ax, 90.5, 45.5, "数据\n聚合方", fs=6.6, color=WARN)

    arrow(ax, (23.4, 45.5), (30.4, 45.5), color=ACCENT, lw=1.0)
    for y in (51.0, 39.0, 27.0):
        arrow(ax, (51.4, 45.5), (58.4, y), color=GREY, lw=0.8, ms=6)
    arrow(ax, (79.4, 51.0), (83.4, 47.0), color=WARN, lw=0.8, ms=6)
    arrow(ax, (79.4, 39.0), (83.4, 44.0), color=WARN, lw=0.8, ms=6)

    label(ax, 13.0, 32.0, "同一个标识在下个站点再次出现", fs=6.4, color=GREY)
    ax.plot([13.0, 13.0], [39.4, 34.0], color=GREY, lw=0.8, ls=(0, (3, 2.5)))
    ax.plot([13.0, 40.0], [34.0, 34.0], color=GREY, lw=0.8, ls=(0, (3, 2.5)))
    arrow(ax, (40.0, 34.0), (40.0, 39.4), color=GREY, lw=0.8, ms=6,
          ls=(0, (3, 2.5)))

    label(ax, 50.0, 12.0, "第一方只能看到自己站点上的行为", fs=6.8, color=SOFT)
    label(ax, 50.0, 5.6, "第三方脚本能在很多站点上看到同一批人", fs=6.8, color=WARN)
    return save(fig, "25", "page-flow.png")


def fingerprint():
    fig, ax = setup(5.3, 2.9)
    items = ["User-Agent", "时区", "语言", "字体列表", "屏幕尺寸",
             "Canvas", "WebGL", "音频栈", "硬件并发", "插件", "触控", "时钟精度"]
    cols, w, h = 4, 21.0, 9.0
    for i, name in enumerate(items):
        r, c = divmod(i, cols)
        x = 4.0 + c * (w + 3.0)
        y = 44.0 - r * (h + 4.0)
        box(ax, x, y, w, h, fc=PALE if i % 3 else PALE_BLUE, ec=LINE, lw=0.8)
        label(ax, x + w / 2, y + h / 2, name, fs=6.4, color=SOFT)

    box(ax, 4.0, 4.0, 92.0, 8.0, fc="white", ec=LINE, lw=0.8)
    label(ax, 50.0, 8.0, "合成一个向量，跨站、跨会话对齐到同一台设备", fs=6.8,
          color=ACCENT)
    return save(fig, "25", "fingerprint.png")


if __name__ == "__main__":
    page_flow()
    fingerprint()
