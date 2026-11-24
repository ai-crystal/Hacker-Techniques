# -*- coding: utf-8 -*-
"""第十六章插图：信任的转移、钓鱼链路。

画布宽度统一取 5.3 英寸，与版心宽度接近。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                    PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label, rect,
                    save, setup)


def trust_transfer():
    """三层证据：外观、域名、证书，各自能证明什么。"""
    fig, ax = setup(5.3, 3.05)
    rows = [
        ("外观", "另存真站首页，改掉表单地址", "只说明它看起来像"),
        ("域名", "注册形近域名或同形异码", "只说明拼写接近，不说明是谁"),
        ("证书", "免费签发，全自动完成", "只说明这条连接通向该域名"),
    ]
    h = 13.0
    for (name, how, what), y in zip(rows, [39.5, 23.5, 7.5]):
        box(ax, 1.0, y, 97.0, h, fc="white", ec=LINE, lw=1.0)
        rect(ax, 1.0, y, 2.2, h, fc=ACCENT, zorder=3)
        label(ax, 6.0, y + h / 2, name, fs=10, color=ACCENT, ha="left",
              weight="bold")
        label(ax, 20.0, y + h / 2, how, fs=7.4, color=SOFT, ha="left")
        label(ax, 60.0, y + h / 2, what, fs=7.4, color=INK, ha="left")

    label(ax, 20.0, 55.4, "攻击者怎么做", fs=7.0, color=GREY, ha="left")
    label(ax, 60.0, 55.4, "它真正证明的", fs=7.0, color=GREY, ha="left")
    return save(fig, "16", "trust-transfer.png")


def phishing_layers():
    """钓鱼从选目标到变现的五步。"""
    fig, ax = setup(5.3, 3.25)
    steps = [
        ("1", "选目标", "从公开渠道找姓名、职位、同事关系"),
        ("2", "造入口", "注册相似域名，配好证书与登录页"),
        ("3", "投递", "伪造发件人，正文只留一个链接"),
        ("4", "取凭据", "假登录页把账号密码原样转发给真站"),
        ("5", "变现", "用同一密码试别的系统，改密后潜伏"),
    ]
    h = 7.2
    gap = 3.2
    top = 56.5
    for num, name, note in steps:
        y = top - h
        box(ax, 1.5, y, 23.0, h, fc=PALE, ec=LINE)
        label(ax, 3.8, y + h / 2, num, fs=7.2, color=GREY, ha="left")
        label(ax, 7.4, y + h / 2, name, fs=8.6, color=INK, ha="left",
              weight="bold")
        label(ax, 28.0, y + h / 2, note, fs=7.4, color=SOFT, ha="left")
        if top < 56.4:
            arrow(ax, (13.0, top + gap - 0.2), (13.0, top + 0.2), lw=1.0)
        top -= h + gap
    label(ax, 1.5, 3.4, "五步里没有一步需要攻破某台机器的防护",
          fs=7.0, color=GREY, ha="left")
    return save(fig, "16", "phishing-layers.png")


if __name__ == "__main__":
    trust_transfer()
    phishing_layers()
