# -*- coding: utf-8 -*-
"""第二十六章插图：账号接管的四条路径、二次验证的强弱阶梯。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def takeover_paths():
    fig, ax = setup(5.3, 3.2)
    paths = [("撞库", "别处泄露的\n口令对上", 46.0, PALE),
             ("短信劫持", "补卡或转发\n验证码", 34.0, PALE_WARN),
             ("会话令牌", "抓到 cookie\n直接复用", 22.0, PALE_BLUE),
             ("客服社工", "骗过重置\n流程", 10.0, PALE_2)]
    for name, note, y, fc in paths:
        box(ax, 3.0, y, 22.0, 11.0, fc=fc, ec=LINE)
        label(ax, 14.0, y + 7.9, name, fs=7.2, color=INK, weight="bold")
        label(ax, 14.0, y + 3.4, note, fs=5.8, color=GREY)

    box(ax, 40.0, 6.0, 22.0, 50.0, fc="white", ec=LINE)
    label(ax, 51.0, 52.0, "绕开的那道检查", fs=7.0, color=SOFT)
    checks = [("口令强度", 44.0), ("短信可达性", 33.0),
              ("登录状态", 22.0), ("身份核验", 11.0)]
    for text, y in checks:
        label(ax, 51.0, y, text, fs=6.4, color=GREY)

    for y in (45.0, 32.0, 19.0, 6.0):
        arrow(ax, (25.4, y + 5.5), (39.4, y + 5.5), color=GREY, lw=0.8, ms=6)

    box(ax, 72.0, 24.0, 25.0, 17.0, fc="#f0e2e2", ec="#dcc0c0")
    label(ax, 84.5, 35.0, "账号被接管", fs=7.6, color=WARN, weight="bold")
    label(ax, 84.5, 30.0, "口令本身没被破解", fs=6.2, color=GREY)
    for y in (50.0, 38.0, 26.0, 14.0):
        arrow(ax, (62.4, y), (71.4, 32.5), color=WARN, lw=0.8, ms=6, rad=0.08)
    return save(fig, "26", "takeover-paths.png")


def mfa_ladder():
    fig, ax = setup(5.3, 2.8)
    steps = [("短信验证码", "运营商流程\n与补卡", 4.0, 10.0, PALE_WARN),
             ("TOTP", "实时钓鱼\n代理", 30.0, 18.0, PALE),
             ("推送确认", "疲劳轰炸\n误点", 56.0, 26.0, PALE_BLUE),
             ("硬件密钥", "需要物理\n持有", 82.0, 34.0, "#e3efe6")]
    for name, note, x, h, fc in steps:
        box(ax, x, 12.0, 14.0, h, fc=fc, ec=LINE)
        label(ax, x + 7.0, 12.0 + h + 4.0, name, fs=6.8, color=INK, weight="bold")
        label(ax, x + 7.0, 12.0 + h - 4.0, note, fs=5.6, color=GREY)
    ax.plot([2.0, 97.0], [12.0, 12.0], color="#c8c8c2", lw=1.0)
    label(ax, 50.0, 6.0, "越往右，远程接管需要的条件越多", fs=6.8, color=SOFT)
    return save(fig, "26", "mfa-ladder.png")


if __name__ == "__main__":
    takeover_paths()
    mfa_ladder()
