# -*- coding: utf-8 -*-
"""第二十三章插图：演练生命周期、指标链。

画布宽 5.3 英寸，图内不写标题。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def lifecycle():
    """六个阶段蛇形排布，末尾虚线回到起点。"""
    fig, ax = setup(5.3, 3.4)

    stages = [
        (6.0, 48.0, "定目标与指标", "先定口径，再定主题", PALE, ACCENT),
        (54.0, 48.0, "授权与范围", "三方签字，写清禁区", PALE, ACCENT),
        (54.0, 32.0, "素材与落地页", "页面只收一个比特", PALE_BLUE, BLUE),
        (6.0, 32.0, "分批投放", "限速、白名单、中止线", PALE_BLUE, BLUE),
        (6.0, 16.0, "收尾与销毁", "个人信息按期清掉", PALE_2, SOFT),
        (54.0, 16.0, "复盘与改进", "指标翻译成动作", PALE_2, SOFT),
    ]
    w, h = 42.0, 11.0
    for x, y, name, note, fc, tc in stages:
        box(ax, x, y, w, h, fc=fc, ec=LINE, lw=0.9)
        label(ax, x + w / 2, y + 7.0, name, fs=8.4, color=tc, weight="bold")
        label(ax, x + w / 2, y + 3.4, note, fs=6.4, color=GREY)

    arrow(ax, (48.4, 53.5), (53.6, 53.5), color=ACCENT, lw=1.0, ms=7)
    arrow(ax, (75.0, 47.6), (75.0, 43.4), color=ACCENT, lw=1.0, ms=7)
    arrow(ax, (53.6, 37.5), (48.4, 37.5), color=ACCENT, lw=1.0, ms=7)
    arrow(ax, (27.0, 31.6), (27.0, 27.4), color=ACCENT, lw=1.0, ms=7)
    arrow(ax, (48.4, 21.5), (53.6, 21.5), color=ACCENT, lw=1.0, ms=7)

    # 虚线回路：从复盘下方绕到定目标左侧
    ax.plot([75.0, 75.0], [15.6, 8.6], color=ACCENT_2, lw=0.9, ls=(0, (3, 2)),
            zorder=3)
    ax.plot([75.0, 3.0], [8.6, 8.6], color=ACCENT_2, lw=0.9, ls=(0, (3, 2)),
            zorder=3)
    ax.plot([3.0, 3.0], [8.6, 53.5], color=ACCENT_2, lw=0.9, ls=(0, (3, 2)),
            zorder=3)
    arrow(ax, (3.0, 53.5), (5.6, 53.5), color=ACCENT_2, lw=0.9, ms=6)

    label(ax, 46.0, 11.6, "本轮结论进入下一轮设计", fs=6.4, color=ACCENT_2)
    return save(fig, "23", "lifecycle.png")


def metric_chain():
    """六个环节两行蛇形，底部三条口径提醒。"""
    fig, ax = setup(5.3, 3.4)

    nodes = [
        (4.0, 50.0, "发送", "按名单分批发", PALE, ACCENT),
        (38.0, 50.0, "送达", "进收件箱才算", PALE, ACCENT),
        (72.0, 50.0, "打开", "像素被预取", PALE_BLUE, BLUE),
        (72.0, 30.0, "点击", "网关也会点一遍", PALE_BLUE, BLUE),
        (38.0, 30.0, "提交", "表单或按钮", PALE_WARN, WARN),
        (4.0, 30.0, "报告", "越高越好", PALE_WARN, WARN),
    ]
    w, h = 24.0, 11.0
    for x, y, name, note, fc, tc in nodes:
        box(ax, x, y, w, h, fc=fc, ec=LINE, lw=0.9)
        label(ax, x + w / 2, y + 7.0, name, fs=8.6, color=tc, weight="bold")
        label(ax, x + w / 2, y + 3.4, note, fs=6.3, color=GREY)

    arrow(ax, (28.4, 55.5), (37.6, 55.5), color=ACCENT, lw=1.0, ms=7)
    arrow(ax, (62.4, 55.5), (71.6, 55.5), color=ACCENT, lw=1.0, ms=7)
    arrow(ax, (84.0, 49.6), (84.0, 41.4), color=ACCENT, lw=1.0, ms=7)
    arrow(ax, (71.6, 35.5), (62.4, 35.5), color=ACCENT, lw=1.0, ms=7)
    arrow(ax, (37.6, 35.5), (28.4, 35.5), color=ACCENT, lw=1.0, ms=7)

    label(ax, 33.0, 58.4, "送达率", fs=6.3, color=GREY)
    label(ax, 67.0, 58.4, "打开率", fs=6.3, color=GREY)
    label(ax, 86.4, 45.5, "点击率", fs=6.3, color=GREY, ha="left")
    label(ax, 67.0, 38.2, "提交率", fs=6.3, color=GREY)
    label(ax, 33.0, 38.2, "报告率", fs=6.3, color=GREY)

    tips = [
        "打开率不可信，客户端的图片代理会替你打开",
        "点击率是上界，网关预取和误触都算在内",
        "报告率越高越好，其余几项越低越好",
    ]
    for i, s in enumerate(tips):
        label(ax, 4.0, 21.0 - i * 6.0, s, fs=6.4, color=GREY, ha="left")

    return save(fig, "23", "metric-chain.png")


if __name__ == "__main__":
    lifecycle()
    metric_chain()
