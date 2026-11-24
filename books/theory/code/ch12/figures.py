# -*- coding: utf-8 -*-
"""第十二章插图：同源判定、CSP 对内联脚本的拦截。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def same_origin():
    fig, ax = setup(5.3, 3.0)
    rows = [("页面来源", "https://shop.example:443/app", PALE_BLUE),
            ("目标 A", "https://shop.example/api/user", PALE),
            ("目标 B", "http://shop.example/api/user", PALE_WARN),
            ("目标 C", "https://api.example/api/user", PALE_WARN),
            ("目标 D", "https://shop.example:8443/api", PALE_WARN)]
    y = 46.0
    for name, url, fc in rows:
        box(ax, 4.0, y, 18.0, 8.0, fc="#f3f3ef" if name == "页面来源" else "white",
            ec=LINE, lw=0.8)
        label(ax, 13.0, y + 4.0, name, fs=6.8, color=SOFT)
        box(ax, 24.0, y, 52.0, 8.0, fc=fc, ec=LINE, lw=0.8)
        label(ax, 26.0, y + 4.0, url, fs=6.2, color=INK, ha="left")
        y -= 9.5

    verdicts = [("同源", ACCENT), ("协议不同：跨源", WARN), ("主机不同：跨源", WARN),
                ("端口不同：跨源", WARN)]
    yy = 46.0 - 9.5
    for text, color in verdicts:
        label(ax, 79.0, yy + 4.0, text, fs=6.4, color=color, ha="left")
        yy -= 9.5
    label(ax, 50.0, 4.0, "三者全同才算同源，任何一项不同都重新按跨源处理", fs=6.8,
          color=SOFT)
    return save(fig, "12", "same-origin.png")


def csp_inline():
    fig, ax = setup(5.3, 2.8)
    box(ax, 3.0, 34.0, 26.0, 12.0, fc=PALE_BLUE, ec=LINE)
    label(ax, 16.0, 41.4, "服务器响应头", fs=7.4, color=INK, weight="bold")
    label(ax, 16.0, 37.4, "CSP: script-src 'self'", fs=6.0, color=GREY)

    box(ax, 38.0, 34.0, 26.0, 12.0, fc=PALE, ec=LINE)
    label(ax, 51.0, 41.4, "页面里的内联脚本", fs=7.2, color=INK, weight="bold")
    label(ax, 51.0, 37.4, "<script>alert(1)</script>", fs=6.0, color=GREY)

    box(ax, 72.0, 34.0, 24.0, 12.0, fc=PALE_WARN, ec="#e2ccc0")
    label(ax, 84.0, 41.4, "浏览器拒绝执行", fs=7.2, color=WARN, weight="bold")
    label(ax, 84.0, 37.4, "控制台报 CSP 违规", fs=6.0, color=GREY)

    arrow(ax, (29.4, 40.0), (37.4, 40.0), color=ACCENT, lw=1.0)
    arrow(ax, (64.4, 40.0), (71.4, 40.0), color=WARN, lw=1.0)

    label(ax, 16.0, 26.0, "放行条件", fs=6.6, color=SOFT)
    label(ax, 24.0, 20.0, "同源文件 + nonce 匹配 + hash 匹配", fs=6.6, color=ACCENT,
          ha="left")
    label(ax, 50.0, 12.0, "strict-dynamic 之后，脚本再插入的脚本不再检查来源", fs=6.6,
          color=GREY)
    return save(fig, "12", "csp-inline.png")


if __name__ == "__main__":
    same_origin()
    csp_inline()
