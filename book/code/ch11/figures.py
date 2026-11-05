# -*- coding: utf-8 -*-
"""第十一章插图：同源判断、SQL 注入的语法变形、存储型 XSS 数据流。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                    PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label, rect,
                    save, setup)


def same_origin():
    fig, ax = setup(5.3, 3.2)

    label(ax, 3.0, 57.0, "一个源由三项共同决定，任何一项不同就是跨源",
          fs=8.0, color=INK, ha="left")

    box(ax, 3.0, 45.0, 26.0, 9.0, fc=PALE, ec=LINE)
    label(ax, 16.0, 49.5, "协议 https", fs=7.6, color=SOFT)
    label(ax, 30.6, 49.5, "+", fs=8.0, color=GREY)
    box(ax, 32.6, 45.0, 30.0, 9.0, fc=PALE, ec=LINE)
    label(ax, 47.6, 49.5, "主机 shop.example.com", fs=6.6, color=SOFT)
    label(ax, 64.6, 49.5, "+", fs=8.0, color=GREY)
    box(ax, 66.6, 45.0, 22.0, 9.0, fc=PALE, ec=LINE)
    label(ax, 77.6, 49.5, "端口 443", fs=7.6, color=SOFT)

    ax.plot([3.0, 97.0], [41.5, 41.5], color=LINE, lw=0.9)

    rows = [
        ("https://shop.example.com/cart", "同源", ACCENT),
        ("http://shop.example.com/cart", "跨源，协议不同", WARN),
        ("https://shop.example.com:8443/", "跨源，端口不同", WARN),
        ("https://api.example.com/", "跨源，主机不同", WARN),
    ]
    y = 36.5
    for url, verdict, color in rows:
        label(ax, 6.0, y, url, fs=7.2, color=SOFT, ha="left")
        label(ax, 55.0, y, verdict, fs=7.2, color=color, ha="left")
        y -= 6.4

    rect(ax, 0, 0, 100, 12.0, fc=PALE_2)
    label(ax, 5.0, 8.0, "同源策略限制的是读取，不是发送。跨站请求照样发出，cookie 照样带上。",
          fs=6.9, color=SOFT, ha="left")
    label(ax, 5.0, 3.4, "表单、图片、脚本标签都能跨站加载，这正是 CSRF 的入口。",
          fs=6.9, color=SOFT, ha="left")

    return save(fig, "11", "same-origin.png")


def _tokens(ax, x, y, h, items, fs=7.6, pad=5.5, gap=1.8):
    """把一段 SQL 画成一串定宽小方块，返回每个方块的中心与左右边界。"""
    geo = []
    cx = x
    for text, fc, ec, color in items:
        w = len(text) * 1.195 + pad
        box(ax, cx, y, w, h, fc=fc, ec=ec, lw=0.9, radius=0.6)
        label(ax, cx + w / 2, y + h / 2, text, fs=fs, color=color)
        geo.append((cx, cx + w, cx + w / 2))
        cx += w + gap
    return geo


def _bracket(ax, x1, x2, y, text, color=GREY):
    ax.plot([x1, x1, x2, x2], [y + 1.4, y, y, y + 1.4], color=color, lw=0.9,
            zorder=3)
    label(ax, (x1 + x2) / 2, y - 2.4, text, fs=6.9, color=color)


def sql_injection():
    fig, ax = setup(5.3, 3.1)
    kw = (PALE, LINE, SOFT)
    val = (PALE_WARN, WARN, WARN)

    label(ax, 5.0, 52.0, "输入是 alice 时，拼出来的语句", fs=7.6, color=INK,
          ha="left")
    g1 = _tokens(ax, 8.0, 40.0, 8.0, [
        ("WHERE", PALE_BLUE, LINE, BLUE),
        ("name", *kw),
        ("=", *kw),
        ("'alice'", PALE_BLUE, LINE, BLUE),
    ])
    _bracket(ax, g1[0][0], g1[-1][1], 37.0, "一个条件")

    label(ax, 5.0, 27.0, "输入是 ' OR 1=1 -- 时，拼出来的语句", fs=7.6,
          color=INK, ha="left")
    g2 = _tokens(ax, 6.0, 15.0, 8.0, [
        ("WHERE", PALE_BLUE, LINE, BLUE),
        ("name", *kw),
        ("=", *kw),
        ("''", *val),
        ("OR", PALE_BLUE, LINE, BLUE),
        ("1=1", *val),
        ("--", PALE_BLUE, LINE, BLUE),
    ])
    tail = g2[-1][1] + 1.8
    box(ax, tail, 15.0, 8.0, 8.0, fc=PALE_2, ec=LINE, lw=0.9, radius=0.6)
    label(ax, tail + 4.0, 19.0, "……", fs=7.2, color=GREY)
    _bracket(ax, g2[0][0], g2[3][1], 12.0, "条件 A")
    _bracket(ax, g2[4][0], g2[6][1], 12.0, "条件 B，恒真", WARN)

    label(ax, 5.0, 4.0, "两组条件由 OR 连接，整体恒真，口令校验失去意义",
          fs=7.0, color=WARN, ha="left")

    return save(fig, "11", "sql-injection.png")


def xss_flow():
    fig, ax = setup(5.3, 2.6)

    label(ax, 4.0, 45.0, "提交时只是一段文字", fs=7.2, color=GREY, ha="left")
    label(ax, 61.0, 45.0, "渲染后变成代码", fs=7.2, color=GREY, ha="left")

    box(ax, 4.0, 31.0, 20.0, 11.0, fc=PALE_WARN, ec=WARN)
    label(ax, 14.0, 36.5, "攻击者", fs=8.0, color=WARN, weight="bold")
    box(ax, 33.0, 31.0, 22.0, 11.0, fc=PALE, ec=LINE)
    label(ax, 44.0, 36.5, "留言接口", fs=8.0, color=SOFT)
    box(ax, 61.0, 31.0, 26.0, 11.0, fc=PALE, ec=LINE)
    label(ax, 74.0, 36.5, "数据库", fs=8.0, color=SOFT)

    box(ax, 4.0, 6.0, 20.0, 11.0, fc=PALE_WARN, ec=WARN)
    label(ax, 14.0, 13.8, "cookie", fs=7.6, color=WARN, weight="bold")
    label(ax, 14.0, 9.6, "外发", fs=7.2, color=WARN)
    box(ax, 33.0, 6.0, 22.0, 11.0, fc=PALE_WARN, ec=WARN)
    label(ax, 44.0, 11.5, "脚本执行", fs=8.0, color=WARN)
    box(ax, 61.0, 6.0, 26.0, 11.0, fc=PALE, ec=LINE)
    label(ax, 74.0, 13.8, "受害者", fs=8.0, color=SOFT)
    label(ax, 74.0, 9.6, "打开页面", fs=7.2, color=GREY)

    arrow(ax, (24.4, 36.5), (32.6, 36.5))
    arrow(ax, (55.4, 36.5), (60.6, 36.5))
    arrow(ax, (74.0, 30.6), (74.0, 17.4))
    arrow(ax, (60.6, 11.5), (55.4, 11.5))
    arrow(ax, (32.6, 11.5), (24.4, 11.5))
    arrow(ax, (14.0, 17.4), (14.0, 30.6))

    label(ax, 76.6, 24.0, "数据库里的字符串\n被原样拼进 HTML", fs=6.8,
          color=GREY, ha="left")
    label(ax, 18.2, 24.0, "带着会话\ncookie", fs=6.8, color=GREY,
          ha="left")

    return save(fig, "11", "xss-flow.png")


if __name__ == "__main__":
    same_origin()
    sql_injection()
    xss_flow()
