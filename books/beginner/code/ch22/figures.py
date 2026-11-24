# -*- coding: utf-8 -*-
"""第二十二章插图：僵尸网络的招募路径、SIM 卡交换时序。

来源标注见各图图注，图内不写标题。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def botnet_path():
    fig, ax = setup(5.3, 3.1)

    stages = [
        ("① 扫描", "全自动", 44.0,
         "随机生成 IPv4 地址，逐个试探\n23 与 2323 端口（Telnet）"),
        ("② 登录", "无交互", 29.0,
         "照内置口令表逐条试，几十组\n用户名口令，覆盖同类白牌方案"),
        ("③ 植入", "无感知", 14.0,
         "复制自身，杀掉同机的其他恶意\n程序，回连控制端等待指令"),
    ]
    for name, tag, y, note in stages:
        box(ax, 2.0, y, 40.0, 11.0, fc=PALE, ec=LINE)
        label(ax, 6.0, y + 7.2, name, fs=9.2, color=INK, ha="left", weight="bold")
        label(ax, 38.0, y + 4.0, tag, fs=7.0, color=GREY, ha="right")
        label(ax, 46.5, y + 5.6, note, fs=7.2, color=SOFT, ha="left")

    arrow(ax, (22.0, 44.0), (22.0, 40.4))
    arrow(ax, (22.0, 29.0), (22.0, 25.4))

    box(ax, 2.0, 2.0, 96.0, 8.2, fc=PALE_WARN, ec="#dcc4b6")
    label(ax, 50.0, 6.1, "一条指令：几十万台设备同时向同一个目标发起请求",
          fs=8.4, color=WARN)
    arrow(ax, (22.0, 14.0), (22.0, 10.6), color=WARN)

    return save(fig, "22", "botnet-path.png")


def sim_swap():
    fig, ax = setup(5.3, 3.3)

    lanes = [("攻击者", 19.0, WARN), ("运营商客服", 50.0, ACCENT),
             ("受害者", 82.0, SOFT)]
    for name, x, color in lanes:
        box(ax, x - 14.0, 49.0, 28.0, 8.0, fc=PALE_2, ec=LINE)
        label(ax, x, 53.0, name, fs=8.4, color=color, weight="bold")
        ax.plot([x, x], [49.0, 9.0], color=LINE, lw=0.9,
                ls=(0, (3, 2.5)), zorder=1)

    steps = [
        (44.0, 1, "冒充本人报失", WARN, 19.0, 50.0),
        (36.0, 2, "旧卡注销", ACCENT, 50.0, 82.0),
        (28.0, 3, "新卡写号激活", WARN, 50.0, 19.0),
        (20.0, 4, "短信改投新卡", WARN, 19.0, 82.0),
        (12.0, 5, "重置邮箱与账号", WARN, 19.0, 82.0),
    ]
    for y, no, text, color, x1, x2 in steps:
        label(ax, 4.0, y, str(no), fs=7.6, color=GREY)
        arrow(ax, (x1, y), (x2, y), color=color)
        label(ax, 34.5, y + 3.0, text, fs=7.2, color=color,
              bbox=dict(fc="white", ec="none", pad=1.2))

    box(ax, 2.0, 0.6, 96.0, 7.2, fc=PALE_WARN, ec="#dcc4b6")
    label(ax, 50.0, 4.2, "核对身份靠的是“知道的信息”，而这些信息在网上都能凑齐",
          fs=7.6, color=WARN)

    return save(fig, "22", "sim-swap.png")


if __name__ == "__main__":
    botnet_path()
    sim_swap()
