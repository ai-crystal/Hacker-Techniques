# -*- coding: utf-8 -*-
"""第三章插图：侦察的两条路径、资产表字段结构。

画布宽度统一取 5.3 英寸，与版心宽度接近。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def recon_paths():
    fig, ax = setup(5.3, 3.3)

    box(ax, 30, 54, 40, 6.5, fc=PALE, ec=LINE)
    label(ax, 50, 57.2, "一个域名，或者一个网段", fs=8.0, color=INK,
          weight="bold")

    arrow(ax, (50, 53.8), (50, 51.6))
    ax.plot([23, 79], [51.6, 51.6], color=ACCENT, lw=1.0, zorder=3)
    for x in (23, 79):
        arrow(ax, (x, 51.6), (x, 50.2))

    box(ax, 2, 36, 40, 14, fc=PALE_2, ec=LINE)
    label(ax, 22, 47.2, "被动收集　不向目标发包", fs=7.8, color=INK,
          weight="bold")
    label(ax, 22, 43.2, "证书透明日志 · DNS 记录", fs=7.0, color=SOFT)
    label(ax, 22, 39.2, "搜索引擎 · 公开代码仓库", fs=7.0, color=SOFT)

    box(ax, 58, 36, 40, 14, fc=PALE_BLUE, ec="#b6c4d2")
    label(ax, 78, 47.2, "主动扫描　会留下日志", fs=7.8, color=BLUE,
          weight="bold")
    label(ax, 78, 43.2, "主机发现 · 端口状态", fs=7.0, color=SOFT)
    label(ax, 78, 39.2, "服务指纹 · 版本推断", fs=7.0, color=SOFT)

    arrow(ax, (42.4, 42.6), (57.6, 42.6))
    label(ax, 50, 44.6, "决定范围", fs=6.8, color=WARN)

    box(ax, 16, 18, 68, 13, fc=PALE_WARN, ec="#d8b6a6")
    label(ax, 50, 27.2, "资产表", fs=9.0, color=WARN, weight="bold")
    label(ax, 50, 22.4, "主机名 · IP · 端口 · 服务版本 · 来源 · 置信度",
          fs=6.8, color=SOFT)

    arrow(ax, (22, 35.8), (32, 31.4))
    arrow(ax, (78, 35.8), (68, 31.4))

    box(ax, 24, 4, 52, 8.5, fc="white", ec=LINE)
    label(ax, 50, 8.2, "下一步　版本与公告比对", fs=7.6, color=INK)
    arrow(ax, (50, 17.8), (50, 12.8))
    return save(fig, "03", "recon-paths.png")


def asset_fields():
    fig, ax = setup(5.3, 2.7)

    cols = [("主机名", 21), ("IP 地址", 17), ("端口", 9),
            ("服务与版本", 24), ("来源", 12), ("置信度", 13)]
    x0, top, hh, rh = 2, 44, 6.5, 7.0

    # 前三列是去重键，整列打底
    rect(ax, x0, top - hh - rh * 3, 47, hh + rh * 3, fc="#f4f7fa")

    rows = [
        ("www.lab.local", "10.10.10.20", "80", "nginx 1.24", "证书日志", "高"),
        ("api.lab.local", "10.10.10.20", "8080", "Tomcat 9.0", "主动扫描", "中"),
        ("mail.lab.local", "10.10.10.25", "25", "Postfix 3.7", "DNS MX", "高"),
    ]

    x = x0
    for name, w in cols:
        box(ax, x, top - hh, w, hh, fc=PALE, ec=LINE, lw=0.8, radius=0)
        label(ax, x + w / 2, top - hh / 2, name, fs=7.0, color=INK,
              weight="bold")
        x += w

    for i, row in enumerate(rows):
        y = top - hh - rh * (i + 1)
        x = x0
        for (name, w), cell in zip(cols, row):
            box(ax, x, y, w, rh, fc="none", ec=LINE, lw=0.8, radius=0)
            color = SOFT if name in ("主机名", "IP 地址", "端口") else GREY
            label(ax, x + w / 2, y + rh / 2, cell, fs=6.8, color=color)
            x += w

    ax.plot([x0, x0 + 47], [14.6, 14.6], color=ACCENT, lw=1.0)
    ax.plot([x0, x0], [14.6, 15.8], color=ACCENT, lw=1.0)
    ax.plot([x0 + 47, x0 + 47], [14.6, 15.8], color=ACCENT, lw=1.0)
    label(ax, 25.5, 11.4, "去重键　三列相同即视为同一条资产", fs=7.0,
          color=ACCENT)

    label(ax, 74, 11.4, "来源记出处，置信度记可信程度", fs=7.0, color=GREY)
    return save(fig, "03", "asset-fields.png")


if __name__ == "__main__":
    recon_paths()
    asset_fields()
