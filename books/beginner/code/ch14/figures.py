# -*- coding: utf-8 -*-
"""第十四章插图：勒索加密流程、C2 架构对比、攻击链阶段。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                    PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label, rect,
                    save, setup)


def ransom_flow():
    fig, ax = setup(5.3, 3.45)

    steps = [
        "① 生成一个随机对称密钥 K",
        "② 用 K 逐块加密文件，改扩展名",
        "③ 用攻击者公钥加密 K，得到 K′",
        "④ 删掉本机的 K 与卷影副本",
        "⑤ 显示勒索页面与付款地址",
    ]
    h, gap = 8.4, 2.6
    top = 52.6
    for i, text in enumerate(steps):
        y = top - i * (h + gap)
        fc = PALE_WARN if i == 3 else PALE
        box(ax, 2.6, y, 45.0, h, fc=fc, ec=LINE)
        label(ax, 25.1, y + h / 2, text, fs=7.0, color=INK)
        if i < len(steps) - 1:
            arrow(ax, (25.1, y - 0.15), (25.1, y - gap + 0.15), lw=1.0, ms=7)

    rect(ax, 51.4, 8.0, 45.6, 54.6, fc="#f7f4ef")
    ax.plot([51.4, 51.4], [8.0, 62.6], color="#ddd8cd", lw=0.8)
    label(ax, 54.6, 57.2, "没有私钥会怎样", fs=8.4, color=WARN, ha="left",
          weight="bold")
    lines = [(52.0, "文件内容已是密文，"),
             (46.4, "和原文没有可算的关系。"),
             (39.8, "K 只以 K′ 留在本机，"),
             (34.2, "K′ 要用私钥才能解开。"),
             (27.6, "2048 位私钥无法穷举，"),
             (22.0, "换杀毒软件也读不出。"),
             (16.8, "例外只有一处，"),
             (11.6, "没被加密的离线备份。")]
    for ly, text in lines:
        label(ax, 54.6, ly, text, fs=7.0, color=SOFT, ha="left")
    return save(fig, "14", "ransom-flow.png")


def c2_topology():
    fig, ax = setup(5.3, 3.15)

    panels = [(1.5, "① 集中式 C2"), (34.4, "② P2P"), (67.3, "③ DGA 域名")]
    for x, _ in panels:
        rect(ax, x, 4.0, 31.2, 46.0, fc="#f8f8f5")
    for x, title in panels:
        label(ax, x + 15.6, 46.2, title, fs=8.0, color=INK, weight="bold")

    # 集中式
    box(ax, 6.0, 36.6, 22.2, 6.2, fc=PALE_BLUE, ec="#b6c4d2")
    label(ax, 17.1, 39.7, "攻击者", fs=7.4, color=BLUE)
    box(ax, 6.0, 25.4, 22.2, 6.2, fc=PALE, ec=LINE)
    label(ax, 17.1, 28.5, "C2 服务器", fs=7.4, color=INK)
    arrow(ax, (17.1, 36.6), (17.1, 31.6), lw=1.0, ms=7)
    label(ax, 17.1, 34.1, "×", fs=12, color=WARN, ha="center", va="center",
          bbox=dict(fc="#f8f8f5", ec="none", pad=0.4))
    for bx in (5.0, 12.4, 19.8):
        box(ax, bx, 8.4, 7.6, 5.6, fc="white", ec=LINE, lw=0.8)
        label(ax, bx + 3.8, 11.2, "肉鸡", fs=6.4, color=GREY)
        arrow(ax, (bx + 3.8, 14.0), (17.1, 25.4), lw=0.9, ms=6,
              color=ACCENT_2)
    label(ax, 17.1, 5.4, "查封一台，全网失联", fs=6.6, color=GREY)

    # P2P
    nodes = [(36.5, 11.0), (52.5, 11.0), (36.5, 33.0), (52.5, 33.0)]
    for nx, ny in nodes:
        box(ax, nx, ny, 9.6, 6.0, fc="white", ec=LINE, lw=0.8)
        label(ax, nx + 4.8, ny + 3.0, "节点", fs=6.6, color=INK)
    arrow(ax, (46.1, 36.0), (52.5, 36.0), lw=0.9, ms=6, color=ACCENT_2,
          style="<|-|>")
    arrow(ax, (46.1, 14.0), (52.5, 14.0), lw=0.9, ms=6, color=ACCENT_2,
          style="<|-|>")
    arrow(ax, (41.3, 33.0), (41.3, 17.0), lw=0.9, ms=6, color=ACCENT_2,
          style="<|-|>")
    arrow(ax, (57.3, 33.0), (57.3, 17.0), lw=0.9, ms=6, color=ACCENT_2,
          style="<|-|>")
    label(ax, 49.3, 25.0, "无中心", fs=6.8, color=GREY)
    label(ax, 49.3, 5.4, "抓掉谁都不影响其余节点", fs=6.6, color=GREY)

    # DGA
    box(ax, 70.4, 34.4, 25.0, 6.2, fc=PALE, ec=LINE, lw=0.8)
    label(ax, 82.9, 37.5, "日期 + 种子算域名", fs=6.8, color=INK)
    names = [("a7dk2.net", False), ("q9xz4.org", True),
             ("m2pr8.biz", False), ("k4vt6.info", True)]
    y = 26.6
    for name, hit in names:
        fc = "#e4eeec" if hit else "white"
        ec = ACCENT_2 if hit else LINE
        box(ax, 72.4, y, 21.0, 4.4, fc=fc, ec=ec, lw=0.8)
        label(ax, 82.9, y + 2.2, name, fs=6.4,
              color=ACCENT if hit else GREY)
        y -= 5.4
    label(ax, 82.9, 5.4, "每天换一批，注册其中几个", fs=6.6, color=GREY)
    return save(fig, "14", "c2-topology.png")


def kill_chain():
    fig, ax = setup(5.3, 2.7)

    stages = [
        ("侦察", "TA0043", "找暴露的端口\n和用人的弱点"),
        ("初始访问", "TA0001", "钓鱼邮件或\n一个没补的洞"),
        ("执行", "TA0002", "脚本落地\n解释器跑起来"),
        ("持久化", "TA0003", "注册表、服务\n计划任务"),
        ("横向移动", "TA0008", "偷来的凭据\n换一台机器"),
        ("影响", "TA0040", "加密文件\n或把数据带走"),
    ]
    w, gap = 13.4, 3.2
    x = 1.8
    for name, tid, note in stages:
        box(ax, x, 26.0, w, 15.0, fc=PALE, ec=LINE)
        label(ax, x + w / 2, 37.2, tid, fs=6.0, color=GREY)
        label(ax, x + w / 2, 32.2, name, fs=7.6, color=INK, weight="bold")
        label(ax, x + w / 2, 19.4, note, fs=6.4, color=SOFT)
        x += w + gap
    for i in range(len(stages) - 1):
        sx = 1.8 + i * (w + gap)
        arrow(ax, (sx + w, 33.5), (sx + w + gap, 33.5), lw=1.0, ms=7)

    label(ax, 50.0, 9.0, "越往后，留下的痕迹越多，可用的时间越少",
          fs=7.2, color=GREY)
    return save(fig, "14", "kill-chain.png")


if __name__ == "__main__":
    ransom_flow()
    c2_topology()
    kill_chain()
