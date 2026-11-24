# -*- coding: utf-8 -*-
"""第二十四章插图：AI 在攻击链上的作用点、提示注入的两条路径。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def attack_chain():
    fig, ax = setup(5.3, 3.05)

    label(ax, 2.0, 52.4, "阶段", fs=7.0, color=GREY, ha="left")
    label(ax, 26.0, 52.4, "模型替攻击者做的事", fs=7.0, color=GREY, ha="left")
    ax.plot([1.0, 99.0], [49.6, 49.6], color=LINE, lw=0.8)

    rows = [
        ("侦察", "从公开资料里批量提取人名、汇报关系、供应商"),
        ("准备", "钓鱼文案本地化，一人一稿，术语和口吻都对得上"),
        ("投递", "同一个剧本生成多语言、多平台的变体"),
        ("利用", "读代码、改脚本、写绕过检测的变体"),
        ("驻留", "把命令改写成系统自带工具的调用"),
        ("取数", "大量文本的自动摘要与筛选"),
    ]
    y = 42.0
    for idx, (name, note) in enumerate(rows):
        box(ax, 1.0, y, 21.0, 6.6, fc=PALE, ec=LINE, lw=0.8)
        label(ax, 11.5, y + 3.3, name, fs=8.2, color=INK, weight="bold")
        label(ax, 26.0, y + 3.3, note, fs=7.2, color=SOFT, ha="left")
        if idx < len(rows) - 1:
            ax.plot([1.0, 99.0], [y - 1.3, y - 1.3], color="#e2e2dc", lw=0.7)
        y -= 7.9

    return save(fig, "24", "attack-chain.png")


def prompt_injection():
    fig, ax = setup(5.3, 3.2)

    box(ax, 28.0, 44.0, 30.0, 8.6, fc=PALE_BLUE, ec="#b6c4d2")
    label(ax, 43.0, 48.3, "用户输入", fs=8.4, color=BLUE, weight="bold")

    box(ax, 26.0, 24.0, 34.0, 10.0, fc=PALE, ec=LINE)
    label(ax, 43.0, 31.2, "模型", fs=9.0, color=INK, weight="bold")
    label(ax, 43.0, 27.0, "指令与数据走同一条通道", fs=6.8, color=GREY)

    box(ax, 2.0, 8.0, 28.0, 10.0, fc=PALE_WARN, ec="#dcc4b6")
    label(ax, 15.0, 14.6, "网页、邮件、文档", fs=7.6, color=WARN)
    label(ax, 15.0, 11.2, "指令藏在正文里", fs=6.8, color=GREY)

    box(ax, 34.0, 8.0, 26.0, 10.0, fc=PALE, ec=LINE)
    label(ax, 46.5, 14.6, "拼进上下文", fs=7.6, color=SOFT)
    label(ax, 46.5, 11.2, "和用户的问题并列", fs=6.8, color=GREY)

    box(ax, 74.0, 24.0, 24.0, 10.0, fc=PALE_BLUE, ec="#b6c4d2")
    label(ax, 86.0, 31.2, "工具调用", fs=8.4, color=BLUE, weight="bold")
    label(ax, 86.0, 27.0, "读文件、发信、付款", fs=6.6, color=GREY)

    arrow(ax, (43.0, 44.0), (43.0, 34.2))
    label(ax, 45.0, 39.2, "直接注入", fs=7.2, color=WARN, ha="left")

    arrow(ax, (30.0, 13.0), (33.8, 13.0))
    arrow(ax, (47.0, 18.0), (47.0, 23.8))
    label(ax, 49.0, 20.9, "间接注入", fs=7.2, color=WARN, ha="left")

    arrow(ax, (60.0, 29.0), (73.8, 29.0))
    label(ax, 67.0, 31.4, "执行", fs=6.8, color=SOFT)

    label(ax, 62.0, 48.3, "攻击者不必碰到对话，", fs=7.2, color=SOFT, ha="left")
    label(ax, 62.0, 44.6, "只要让模型读到他的文字", fs=7.2, color=SOFT, ha="left")

    label(ax, 50.0, 2.8, "一次注入的后果，等于模型手里那些工具的权限之和",
          fs=7.4, color=SOFT)

    return save(fig, "24", "prompt-injection.png")


if __name__ == "__main__":
    attack_chain()
    prompt_injection()
