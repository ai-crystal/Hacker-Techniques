# -*- coding: utf-8 -*-
"""第12章插图：一条 AD 攻击路径、AD CS 的签发链。

两图都只画关系与前提，不写具体利用步骤。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def attack_path():
    fig, ax = setup(5.3, 3.95)

    h, gap = 7.2, 7.0
    y0 = 6.0
    ys = [y0 + i * (h + gap) for i in range(5)][::-1]

    nodes = [
        ("zhang.wei　普通域用户", PALE, INK),
        ("Helpdesk 组", PALE, INK),
        ("SRV01 本地管理员", PALE, INK),
        ("it.admin 的凭据", PALE_2, INK),
        ("Domain Admins", PALE_WARN, WARN),
    ]
    for (text, fc, color), y in zip(nodes, ys):
        box(ax, 4.0, y, 42.0, h, fc=fc, ec=LINE)
        label(ax, 25.0, y + h / 2, text, fs=7.8, color=color)

    edges = [
        "写 member 属性，需对组有 GenericAll",
        "组嵌套，Helpdesk 在 SRV01 的本地管理员组",
        "从 LSASS 读会话，SRV01 上有 it.admin 的登录",
        "本来就是成员，it.admin 属于 Domain Admins",
    ]
    for text, y_top in zip(edges, ys[:-1]):
        y_bottom = y_top - gap
        arrow(ax, (25.0, y_top), (25.0, y_bottom), color=ACCENT, lw=1.1, ms=7)
        label(ax, 27.4, (y_top + y_bottom) / 2, text, fs=6.4, color=ACCENT, ha="left")

    label(ax, 4.0, 2.0, "同一处还有三条边可直达终点，RBCD、AD CS、DCSync，各自的前提不同。",
          fs=6.4, color=GREY, ha="left")

    return save(fig, "12", "attack-path.png")


def adcs_chain():
    fig, ax = setup(5.3, 3.6)

    rows = [
        ("根 CA", "离线保存，只签企业 CA 的证书", 54.0, PALE, INK),
        ("企业 CA", "按模板签发，4886 / 4887 留下记录", 41.5, PALE, INK),
        ("证书模板", "谁能注册、能否自填主体、用途含客户端认证", 29.0, PALE_WARN, WARN),
        ("签发的证书", "主体映射到账号，私钥在申请人手里", 16.5, PALE, INK),
        ("KDC 的 PKINIT", "验链并映射主体，签出该账号的 TGT", 4.0, PALE_2, INK),
    ]
    h = 9.0
    for title, note, y, fc, color in rows:
        box(ax, 2.0, y, 96.0, h, fc=fc, ec=LINE)
        label(ax, 6.0, y + h / 2, title, fs=8.0, color=color, ha="left")
        label(ax, 94.0, y + h / 2, note, fs=6.4, color=SOFT, ha="right")

    steps = [("签发", 54.0, 50.5), ("套用", 41.5, 38.0),
             ("注册", 29.0, 25.5), ("出示", 16.5, 13.0)]
    for text, y_top, y_bottom in steps:
        arrow(ax, (50.0, y_top), (50.0, y_bottom), color=ACCENT, lw=1.0, ms=6)
        label(ax, 52.0, (y_top + y_bottom) / 2, text, fs=6.2, color=ACCENT, ha="left")

    return save(fig, "12", "adcs-chain.png")


if __name__ == "__main__":
    attack_path()
    adcs_chain()
