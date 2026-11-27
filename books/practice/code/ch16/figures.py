# -*- coding: utf-8 -*-
"""第十六章插图：样本分析流程、行为观察点。

画布宽度统一取 5.3 英寸，与版心宽度接近，图内不写标题。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def analysis_flow():
    """从接收到结论的五个步骤，左侧标出静态与动态两段。"""
    fig, ax = setup(5.3, 3.5)

    # 两段底色
    rect(ax, 2.6, 27.2, 10.6, 37.2, fc="#eef3f2")
    rect(ax, 2.6, 1.4, 10.6, 24.2, fc="#f7f6f1")
    label(ax, 7.9, 45.8, "静态", fs=8.4, color=ACCENT, weight="bold",
          rotation=90)
    label(ax, 7.9, 13.5, "动态", fs=8.4, color=ACCENT_2, weight="bold",
          rotation=90)

    steps = [
        ("接收与登记", "SHA-256、来源主机、收到时间", "先算哈希，再拷副本"),
        ("隔离分析机", "断网、只读挂载、快照可回滚", "一次一机，机不混用"),
        ("静态分析", "文件类型、节表、导入表、字符串", "一行代码都不执行"),
        ("动态分析", "沙箱、API 监控、网络流量", "出网全部指向假服务"),
        ("结论与规则", "行为清单、YARA、分析报告", "每一句都能被别人复核"),
    ]
    x, w, h = 15.5, 46.0, 9.6
    ys = [54.0, 41.0, 28.0, 15.0, 2.0]
    for (title, note, side), y in zip(steps, ys):
        box(ax, x, y, w, h, fc="white", ec=LINE, lw=1.0)
        label(ax, x + 2.4, y + h - 3.0, title, fs=8.8, color=INK,
              ha="left", weight="bold")
        label(ax, x + 2.4, y + 2.9, note, fs=6.8, color=GREY, ha="left")
        label(ax, 65.5, y + h / 2, side, fs=6.9, color=SOFT, ha="left")

    for y in ys[:-1]:
        arrow(ax, (x + 12.0, y - 0.3), (x + 12.0, y - 3.1), color=ACCENT,
              lw=1.1, ms=7)

    return save(fig, "16", "analysis-flow.png")


def behavior_points():
    """四类观察点，各给出四个可落地的记录项。"""
    fig, ax = setup(5.3, 3.3)

    quads = [
        ("文件系统", PALE, [
            "落地路径与文件名",
            "释放的临时文件",
            "自删除与时间戳改动",
            "被加密文件的扩展名",
        ], 2.0, 32.6),
        ("注册表", PALE_2, [
            "Run 键与启动目录",
            "服务与驱动的注册",
            "文件关联被改写",
            "排除项与防护被关",
        ], 51.0, 32.6),
        ("网络", PALE_BLUE, [
            "解析过的域名",
            "硬编码的 IP 与端口",
            "心跳间隔与包长",
            "上传下载的体积比",
        ], 2.0, 3.0),
        ("进程", PALE_WARN, [
            "父子进程关系",
            "命令行里的参数",
            "被注入的目标进程",
            "加载的非系统模块",
        ], 51.0, 3.0),
    ]

    for name, fc, items, x, y in quads:
        box(ax, x, y, 47.0, 26.2, fc=fc, ec=LINE, lw=0.9)
        label(ax, x + 3.0, y + 21.4, name, fs=8.6, color=ACCENT, ha="left",
              weight="bold")
        ax.plot([x + 3.0, x + 44.0], [y + 18.6, y + 18.6], color=LINE,
                lw=0.7, zorder=3)
        for i, item in enumerate(items):
            label(ax, x + 3.4, y + 15.0 - i * 4.0, item, fs=7.2, color=SOFT,
                  ha="left")

    return save(fig, "16", "behavior-points.png")


def rva_map():
    """同一个节在内存与文件里的两组坐标。"""
    fig, ax = setup(5.3, 2.7)

    label(ax, 12.0, 43.0, "内存\nRVA", fs=7.2, color=SOFT, ha="right")
    label(ax, 12.0, 15.0, "文件\n偏移", fs=7.2, color=SOFT, ha="right")

    rect(ax, 14.0, 38.0, 82.0, 9.0, fc=PALE, ec=LINE, lw=0.9)
    rect(ax, 52.0, 38.0, 34.0, 9.0, fc=PALE_WARN, ec=LINE, lw=0.9)
    label(ax, 69.0, 42.5, ".text 节在内存", fs=7.2, color=WARN)

    rect(ax, 14.0, 10.0, 82.0, 9.0, fc=PALE, ec=LINE, lw=0.9)
    rect(ax, 38.0, 10.0, 34.0, 9.0, fc=PALE_WARN, ec=LINE, lw=0.9)
    label(ax, 55.0, 14.5, ".text 节在文件里", fs=7.2, color=WARN)

    label(ax, 14.0, 48.8, "0", fs=6.2, color=GREY, ha="center")
    label(ax, 14.0, 20.8, "0", fs=6.2, color=GREY, ha="center")

    arrow(ax, (62.0, 38.0), (48.0, 19.0), lw=1.0, ms=7)
    label(ax, 65.0, 27.0, "减 VirtualAddress\n加 PointerToRawData",
          fs=6.4, color=ACCENT, ha="left")

    label(ax, 14.0, 34.6, "VirtualAddress + Misc_VirtualSize",
          fs=5.4, color=SOFT, ha="left", family="monospace")
    label(ax, 96.0, 6.4, "PointerToRawData + SizeOfRawData",
          fs=5.4, color=SOFT, ha="right", family="monospace")

    return save(fig, "16", "rva-map.png")


if __name__ == "__main__":
    analysis_flow()
    behavior_points()
    rva_map()
