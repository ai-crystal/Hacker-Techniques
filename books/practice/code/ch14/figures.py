# -*- coding: utf-8 -*-
"""第14章插图：凭据形态与复用路径、NTLM 中继的时序与前提。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def cred_reuse():
    fig, ax = setup(5.3, 3.2)

    label(ax, 12.0, 56.6, "凭据形态", fs=6.8, color=GREY, weight="bold")
    label(ax, 40.5, 56.6, "怎么用", fs=6.8, color=GREY, weight="bold")
    label(ax, 79.0, 56.6, "能落到哪里", fs=6.8, color=GREY, weight="bold")

    rows = [
        ("明文口令", "直接登录、net use", "该账号能碰的全部服务", PALE),
        ("NT 哈希", "NTLM 应答（PtH）", "接受 NTLM 的成员服务器", PALE),
        ("Kerberos 票据", "提交 TGT 或服务票据", "票据指向的那一个服务", PALE_2),
        ("访问令牌", "同机进程模拟", "本机，进程身份即上限", PALE_2),
    ]
    h = 8.8
    ys = [45.0, 34.4, 23.8, 13.2]
    for (name, how, where, fc), y in zip(rows, ys):
        box(ax, 1.5, y, 21.0, h, fc=fc, ec=LINE)
        label(ax, 12.0, y + h / 2, name, fs=7.0, color=INK)
        box(ax, 27.0, y, 27.0, h, fc=PALE_BLUE, ec=LINE)
        label(ax, 40.5, y + h / 2, how, fs=6.4, color=BLUE)
        box(ax, 59.0, y, 39.5, h, fc=PALE_2, ec=LINE)
        label(ax, 78.7, y + h / 2, where, fs=6.4, color=SOFT)

        arrow(ax, (23.0, y + h / 2), (26.5, y + h / 2), color=ACCENT_2, lw=0.9, ms=5)
        arrow(ax, (54.5, y + h / 2), (58.5, y + h / 2), color=ACCENT_2, lw=0.9, ms=5)

    arrow(ax, (86.0, 12.4), (14.0, 12.4), color=ACCENT, lw=1.0, ms=6, rad=-0.13)
    label(ax, 50.0, 2.4, "下一台主机上再抓一次，同样的四行重来一遍",
          fs=6.2, color=GREY)

    return save(fig, "14", "cred-reuse.png")


def relay_timing():
    fig, ax = setup(5.3, 3.6)

    lifelines = [
        (18.0, "受害主机", "10.10.10.31", PALE),
        (50.0, "攻击者", "10.10.10.50 中继", PALE_WARN),
        (82.0, "目标服务", "10.10.10.20 无签名", PALE),
    ]
    for x, name, addr, fc in lifelines:
        box(ax, x - 13.0, 57.0, 26.0, 10.4, fc=fc, ec=LINE)
        label(ax, x, 63.6, name, fs=7.2, color=INK)
        label(ax, x, 60.0, addr, fs=6.0, color=SOFT)
        ax.plot([x, x], [19.0, 56.4], color=LINE, lw=0.8, ls=(0, (4, 3)), zorder=1)

    steps = [
        (53.0, 18.0, 50.0, "① 触发一次回连"),
        (46.0, 50.0, 82.0, "② 转发 NEGOTIATE"),
        (39.0, 82.0, 50.0, "③ 拿回 CHALLENGE"),
        (32.0, 50.0, 18.0, "④ 原样交给受害者"),
        (25.0, 18.0, 50.0, "⑤ 受害者算出应答"),
        (21.0, 50.0, 82.0, "⑥ 转发，认证通过"),
    ]
    for y, x1, x2, text in steps:
        arrow(ax, (x1, y), (x2, y), color=ACCENT, lw=1.0, ms=6)
        label(ax, (x1 + x2) / 2, y + 2.4, text, fs=6.0, color=SOFT)

    conds = [
        ("目标接受 NTLM", ["SMB、LDAP、HTTP 各有开关"]),
        ("没有签名与绑定", ["否则最后一步被拒掉"]),
        ("攻击者位于路径上", ["能触发回连，也能改解析"]),
    ]
    for i, (head, body) in enumerate(conds):
        x = 1.5 + i * 33.0
        box(ax, x, 2.0, 31.0, 12.4, fc=PALE_2, ec=LINE)
        label(ax, x + 15.5, 10.8, head, fs=6.4, color=INK)
        label(ax, x + 15.5, 6.2, body[0], fs=5.7, color=GREY)

    return save(fig, "14", "relay-timing.png")


if __name__ == "__main__":
    cred_reuse()
    relay_timing()
