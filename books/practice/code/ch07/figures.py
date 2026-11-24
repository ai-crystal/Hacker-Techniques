# -*- coding: utf-8 -*-
"""第七章插图：JWT 验签的判断顺序、口令重置流程里的信任点。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def jwt_path():
    fig, ax = setup(5.3, 3.6)

    rows = [
        ("① 解 header", "签名段没有任何人验过",
         "token 完全由自己编码生成", 54.4),
        ("② 读 alg", "算法由 header 指定，不是由服务端指定",
         "填 none 直接放过，或把 RS256 改成 HS256", 41.8),
        ("③ 验签", "用公钥当 HMAC 的密钥",
         "拿公开的公钥签一个 HS256 就通过", 29.2),
        ("④ 处理 kid", "kid 被拼进文件路径或 SQL 语句",
         "用户可控的 kid 指向另一把密钥", 16.6),
        ("⑤ 查 claim", "exp、aud、iss 一个都没校验",
         "旧 token 永久有效，或跨服务复用", 4.0),
    ]

    label(ax, 2.0, 65.6, "服务端的检查顺序", fs=7.6, color=GREY, ha="left")
    label(ax, 34.0, 65.6, "某一步写错时的表现", fs=7.6, color=GREY, ha="left")

    for name, flaw, effect, y in rows:
        box(ax, 2.0, y, 27.0, 9.0, fc=PALE, ec=LINE)
        label(ax, 15.5, y + 4.5, name, fs=8.4, color=INK, weight="bold")
        arrow(ax, (29.4, y + 4.5), (33.6, y + 4.5), lw=1.0)
        box(ax, 34.0, y, 64.0, 9.0, fc=PALE_WARN, ec="#dcc0b2", lw=0.9)
        label(ax, 35.8, y + 6.1, flaw, fs=7.2, color=WARN, ha="left")
        label(ax, 35.8, y + 2.7, effect, fs=7.0, color=GREY, ha="left")

    return save(fig, "07", "jwt-path.png")


def reset_trust():
    fig, ax = setup(5.3, 3.4)

    stages = [
        ("提交邮箱", "只要地址存在\n就进入下一步"),
        ("生成 token", "随机值入库\n有效期写死"),
        ("邮件链接", "域名取自\n请求的 Host 头"),
        ("提交新密码", "凭 token\n直接修改"),
    ]
    w, gap = 20.0, 5.4
    y0, h = 41.0, 15.0
    for i, (name, note) in enumerate(stages):
        x = 2.0 + i * (w + gap)
        box(ax, x, y0, w, h, fc=PALE, ec=LINE)
        label(ax, x + w / 2, y0 + h - 4.2, name, fs=8.4, color=INK,
              weight="bold")
        label(ax, x + w / 2, y0 + 4.9, note, fs=6.8, color=GREY)
        if i < 3:
            arrow(ax, (x + w + 0.4, y0 + h / 2), (x + w + gap - 0.4, y0 + h / 2),
                  lw=1.1)

    marks = [
        ("Host 头伪造", "重置链接指向\n攻击者的域名"),
        ("token 可猜", "时间戳加序号\n或被截断"),
        ("链接外泄", "Referer、日志\n与浏览器历史"),
        ("不校验旧口令", "拿到 token 就\n能改别人的密码"),
    ]
    for i, (title, note) in enumerate(marks):
        x = 2.0 + i * (w + gap)
        arrow(ax, (x + w / 2, y0 - 0.4), (x + w / 2, 31.4), color=WARN, lw=1.0)
        box(ax, x, 19.6, w, 11.4, fc=PALE_WARN, ec="#dcc0b2", lw=0.9)
        label(ax, x + w / 2, 27.4, title, fs=7.6, color=WARN, weight="bold")
        label(ax, x + w / 2, 22.6, note, fs=6.6, color=SOFT)

    label(ax, 2.0, 12.6, "流程里的每一次“相信”都要能说清依据", fs=7.4,
          color=ACCENT, ha="left")
    label(ax, 2.0, 7.8, "改密码是账号接管最短的一条路，比猜口令省力得多", fs=7.4,
          color=SOFT, ha="left")

    return save(fig, "07", "reset-trust.png")


if __name__ == "__main__":
    jwt_path()
    reset_trust()
