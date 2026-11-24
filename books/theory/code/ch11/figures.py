# -*- coding: utf-8 -*-
"""第十一章插图：OAuth 授权码 + PKCE 时序、JWT 验签路径。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def oauth_pkce():
    fig, ax = setup(5.3, 3.4)
    lanes = [(14.0, "浏览器"), (40.0, "客户端"), (66.0, "授权服务器"), (90.0, "资源接口")]
    for x, name in lanes:
        ax.plot([x, x], [8.0, 56.0], color="#c8c8c2", lw=0.9)
        label(ax, x, 59.0, name, fs=7.4, color=INK, weight="bold")

    steps = [(50.0, 14.0, 40.0, "① 点击登录", ACCENT),
             (44.0, 40.0, 14.0, "② 跳转 + code_challenge", ACCENT),
             (38.0, 14.0, 66.0, "③ 用户授权", ACCENT_2),
             (32.0, 66.0, 14.0, "④ 携带 code 回调", ACCENT_2),
             (26.0, 14.0, 40.0, "⑤ 把 code 交给客户端", WARN),
             (20.0, 40.0, 66.0, "⑥ code + code_verifier 换令牌", WARN)]
    for y, x1, x2, text, color in steps:
        d = 1.2 if x2 > x1 else -1.2
        arrow(ax, (x1 + d, y), (x2 - d, y), color=color, lw=1.0, ms=7)
        mid = (x1 + x2) / 2
        label(ax, mid, y + 1.7, text, fs=6.2, color=color)

    label(ax, 50.0, 12.5, "code 在浏览器里可见，但没有 verifier 就换不到令牌", fs=6.8,
          color=SOFT)
    return save(fig, "11", "oauth-pkce.png")


def jwt_verify():
    fig, ax = setup(5.3, 3.0)
    parts = [("头部", "alg、typ", 3.0, 28.0, PALE_BLUE),
             ("载荷", "sub、exp、scope", 33.0, 34.0, PALE),
             ("签名", "对前两段的签名", 69.0, 28.0, PALE_WARN)]
    for name, note, x, w, fc in parts:
        box(ax, x, 40.0, w, 12.0, fc=fc, ec=LINE)
        label(ax, x + w / 2, 47.4, name, fs=7.8, color=INK, weight="bold")
        label(ax, x + w / 2, 43.4, note, fs=6.2, color=GREY)
        if x < 60:
            label(ax, x + w + 1.4, 46.0, ".", fs=12, color=SOFT)

    checks = [("头部声明的 alg 是否在允许列表内", 30.0, True),
              ("签名是否用声明的 alg 验证通过", 23.0, True),
              ("exp / nbf 是否在当前时间窗内", 16.0, True),
              ("aud 与 iss 是否是自己期望的值", 9.0, False)]
    for text, y, fatal in checks:
        label(ax, 3.0, y, "·", fs=11, color=WARN if fatal else GREY, ha="left")
        label(ax, 7.0, y, text, fs=6.8, color=SOFT, ha="left")
    label(ax, 50.0, 2.4, "前两项任一失败，后面的判断都没有意义", fs=6.6, color=GREY)
    return save(fig, "11", "jwt-verify.png")


if __name__ == "__main__":
    oauth_pkce()
    jwt_verify()
