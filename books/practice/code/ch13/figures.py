# -*- coding: utf-8 -*-
"""第13章插图：Linux 提权检查清单的结构、Windows 服务权限的三处错误。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def linux_checklist():
    fig, ax = setup(5.3, 3.6)

    cards = [
        ("①", "身份与授权", ["sudo -l、/etc/sudoers.d", "docker、lxd、disk 组"], PALE),
        ("②", "可执行属性", ["SUID / SGID 位", "capabilities"], PALE),
        ("③", "定时与自启", ["cron、systemd timer", "开机与登录脚本"], PALE_2),
        ("④", "服务与套接字", ["可写的单元文件", "ExecStart 指向的路径"], PALE_2),
        ("⑤", "内核与驱动", ["版本对照 CVE", "发行版有没有回补"], PALE_WARN),
        ("⑥", "文件与凭据", ["可写的 /etc/passwd", "私钥与配置里的口令"], PALE_WARN),
    ]
    w, h = 47.0, 16.0
    for i, (num, title, items, fc) in enumerate(cards):
        col, row = i % 2, i // 2
        x = 1.5 + col * 50.0
        y = 47.0 - row * 19.5
        box(ax, x, y, w, h, fc=fc, ec=LINE)
        label(ax, x + 5.0, y + 11.4, num, fs=7.6, color=ACCENT)
        label(ax, x + 9.0, y + 11.4, title, fs=7.8, color=INK, ha="left")
        for j, item in enumerate(items):
            label(ax, x + 9.0, y + 7.0 - j * 4.0, item, fs=6.2, color=SOFT, ha="left")

    label(ax, 50.0, 3.0, "前四类只读配置，第五类要实际触发并承担崩溃风险",
          fs=6.4, color=GREY)

    return save(fig, "13", "linux-checklist.png")


def win_service_acl():
    fig, ax = setup(5.3, 3.4)

    label(ax, 10.5, 58.0, "看什么", fs=7.0, color=GREY, weight="bold")
    label(ax, 40.0, 58.0, "怎么错的", fs=7.0, color=GREY, weight="bold")
    label(ax, 79.5, 58.0, "最后得到什么", fs=7.0, color=GREY, weight="bold")

    rows = [
        ("服务的 DACL", "Users 有 SERVICE_CHANGE_CONFIG",
         "改 binPath，重启即生效", 40.0),
        ("ImagePath", "含空格、未引号、上级可写",
         "Windows 依次尝试 Program.exe", 24.0),
        ("文件 ACL", "exe 目录对 Users 可写",
         "替换 exe，下次启动生效", 8.0),
    ]
    h = 11.0
    for name, problem, result, y in rows:
        box(ax, 1.5, y, 18.0, h, fc=PALE_2, ec=LINE)
        label(ax, 10.5, y + h / 2, name, fs=6.8, color=INK)
        box(ax, 23.0, y, 34.0, h, fc=PALE_WARN, ec=LINE)
        label(ax, 40.0, y + h / 2, problem, fs=6.3, color=WARN)
        box(ax, 61.0, y, 37.5, h, fc=PALE, ec=LINE)
        label(ax, 79.7, y + h / 2, result, fs=6.3, color=INK)

        arrow(ax, (19.9, y + h / 2), (22.6, y + h / 2), color=ACCENT_2, lw=0.9, ms=5)
        arrow(ax, (57.4, y + h / 2), (60.6, y + h / 2), color=ACCENT_2, lw=0.9, ms=5)

    label(ax, 50.0, 2.4, "改完之后能不能让服务重新加载，是这三条路共同的最后一道门",
          fs=6.4, color=GREY)

    return save(fig, "13", "win-service-acl.png")


if __name__ == "__main__":
    linux_checklist()
    win_service_acl()
