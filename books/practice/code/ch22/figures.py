# -*- coding: utf-8 -*-
"""第二十二章插图：fuzzing 闭环、crash 分诊流程。

画布宽 5.3 英寸，图内不写标题。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def fuzz_loop():
    """左侧四步循环，右侧崩溃样本的去向。"""
    fig, ax = setup(5.3, 3.4)

    label(ax, 50.0, 58.6, "每一轮的取舍都由边覆盖位图决定", fs=7.4, color=GREY)

    cyc = [
        (3.0, 40.0, "种子与字典", "每种结构一份", PALE, ACCENT),
        (33.0, 40.0, "变异并执行", "位翻、拼接、注入", PALE_BLUE, BLUE),
        (33.0, 20.0, "覆盖有新增？", "与历史并集比较", PALE_2, SOFT),
        (3.0, 20.0, "入队", "成为下一轮种子", PALE, ACCENT),
    ]
    w, h = 22.0, 9.0
    for x, y, name, note, fc, tc in cyc:
        box(ax, x, y, w, h, fc=fc, ec=LINE, lw=0.9)
        label(ax, x + w / 2, y + 5.9, name, fs=8.4, color=tc, weight="bold")
        label(ax, x + w / 2, y + 2.9, note, fs=6.3, color=GREY)

    arrow(ax, (25.4, 44.5), (32.6, 44.5), color=ACCENT, lw=1.0, ms=7)
    arrow(ax, (44.0, 39.6), (44.0, 29.4), color=ACCENT, lw=1.0, ms=7)
    arrow(ax, (32.6, 24.5), (25.4, 24.5), color=ACCENT, lw=1.0, ms=7)
    arrow(ax, (14.0, 29.4), (14.0, 39.6), color=ACCENT, lw=1.0, ms=7)

    label(ax, 29.0, 26.6, "是", fs=6.4, color=ACCENT)
    label(ax, 46.4, 34.4, "是", fs=6.4, color=ACCENT)

    # 没有新覆盖就丢弃
    ax.plot([44.0, 44.0], [19.6, 16.2], color=GREY, lw=0.9, zorder=3)
    arrow(ax, (44.0, 16.2), (44.0, 14.2), color=GREY, lw=0.9, ms=6)
    label(ax, 46.0, 15.0, "否，丢弃", fs=6.2, color=GREY, ha="left")

    # 右侧：崩溃样本
    out = [
        (62.0, 40.0, "崩溃与挂起", "文件名带 id 与信号", PALE_WARN, WARN),
        (62.0, 24.0, "去重", "按 SUMMARY 与栈顶合并", PALE_WARN, SOFT),
        (62.0, 8.0, "分诊", "可复现？可控？可达？", PALE_WARN, SOFT),
    ]
    for x, y, name, note, fc, tc in out:
        box(ax, x, y, 34.0, 9.0, fc=fc, ec=LINE, lw=0.9)
        label(ax, x + 17.0, y + 5.9, name, fs=8.4, color=tc, weight="bold")
        label(ax, x + 17.0, y + 2.9, note, fs=6.1, color=GREY)

    arrow(ax, (55.4, 44.5), (61.6, 44.5), color=WARN, lw=1.0, ms=7)
    arrow(ax, (79.0, 39.6), (79.0, 33.4), color=WARN, lw=1.0, ms=7)
    arrow(ax, (79.0, 23.6), (79.0, 17.4), color=WARN, lw=1.0, ms=7)

    label(ax, 31.0, 8.0, "确认后的样本回填种子库，下一轮命中更快", fs=6.4,
          color=GREY, ha="center")

    return save(fig, "22", "fuzz-loop.png")


def triage_flow():
    """四道筛子，每道一个岔口。"""
    fig, ax = setup(5.3, 3.4)

    gates = [
        (54.0, "五次重放栈帧一致？", "排除竞态与环境巧合"),
        (41.0, "是越界写吗？", "写、读、释放后使用、未定义"),
        (28.0, "数据与长度来自输入？", "看崩溃点与输入的关系"),
        (15.0, "真实入口走得到？", "协议、认证、前置校验"),
    ]
    w, h = 44.0, 8.4
    for y, name, note in gates:
        box(ax, 2.0, y, w, h, fc=PALE, ec=LINE, lw=0.9)
        label(ax, 24.0, y + 5.5, name, fs=8.2, color=ACCENT, weight="bold")
        label(ax, 24.0, y + 2.6, note, fs=6.2, color=GREY)

    outs = [
        (54.0, "存疑样本", "换机器再试，别急着分析", PALE_2, SOFT),
        (41.0, "读越界或未定义", "多半是健壮性，低优先级", PALE_2, SOFT),        (28.0, "内部逻辑错误", "数据不可控，降级处理", PALE_2, SOFT),
        (15.0, "记录，暂不按漏洞报", "路径需要额外前提", PALE_WARN, WARN),
    ]
    for y, name, note, fc, tc in outs:
        box(ax, 53.0, y, 45.0, h, fc=fc, ec=LINE, lw=0.9)
        label(ax, 75.5, y + 5.5, name, fs=8.0, color=tc, weight="bold")
        label(ax, 75.5, y + 2.6, note, fs=6.1, color=GREY)

    # 向下的"继续"箭头与向右的"否"箭头
    for i, (y, _name, _note) in enumerate(gates):
        arrow(ax, (46.4, y + 4.2), (52.6, y + 4.2), color=GREY, lw=0.9, ms=6)
        label(ax, 49.4, y + 6.2, "否", fs=6.0, color=GREY)
        if i < len(gates) - 1:
            arrow(ax, (24.0, y - 0.4), (24.0, y - 4.6), color=ACCENT,
                  lw=1.0, ms=7)
            label(ax, 26.0, y - 2.6, "是", fs=6.0, color=ACCENT, ha="left")

    # 结论
    box(ax, 2.0, 2.0, 44.0, 8.4, fc=PALE_BLUE, ec=LINE, lw=0.9)
    label(ax, 24.0, 7.5, "写报告，附最小复现", fs=8.2, color=BLUE,
          weight="bold")
    label(ax, 24.0, 4.6, "版本、构建、输入、期望与实际", fs=6.2, color=GREY)
    arrow(ax, (24.0, 14.6), (24.0, 10.8), color=ACCENT, lw=1.0, ms=7)
    label(ax, 26.0, 12.7, "是", fs=6.0, color=ACCENT, ha="left")

    return save(fig, "22", "triage-flow.png")


if __name__ == "__main__":
    fuzz_loop()
    triage_flow()
