# -*- coding: utf-8 -*-
"""第11章插图：Kerberos 三次交换、域内枚举的信息汇聚。

画布宽度统一 5.3 英寸，与版心一致；图内不写标题，标题交给图注。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def kerberos_flow():
    fig, ax = setup(5.3, 3.25)

    # 列标题
    label(ax, 12.0, 54.0, "发起方", fs=7.2, color=GREY, weight="bold")
    label(ax, 39.0, 54.0, "对端", fs=7.2, color=GREY, weight="bold")
    label(ax, 88.0, 54.0, "票据用哪把密钥加密", fs=7.2, color=GREY, weight="bold")

    rows = [
        (38.0, "客户端", "AS 服务（DC）", "AS-REQ ／ AS-REP",
         "TGT 用 krbtgt 的\n密钥加密，\n客户端解不开"),
        (23.0, "客户端", "TGS 服务（DC）", "TGS-REQ ／ TGS-REP",
         "服务票据用\n目标账号的密钥\n加密"),
        (8.0, "客户端", "SRV01 上的服务", "AP-REQ ／ AP-REP",
         "服务解密后\n校验 PAC，\n确认组 SID"),
    ]

    for y, left, right, msgs, note in rows:
        h = 9.0
        box(ax, 2.0, y, 20.0, h, fc=PALE, ec=LINE)
        label(ax, 12.0, y + h / 2, left, fs=7.8, color=INK)
        box(ax, 50.0, y, 24.0, h, fc=PALE_2, ec=LINE)
        label(ax, 62.0, y + h / 2, right, fs=7.8, color=INK)

        arrow(ax, (22.4, y + h / 2), (49.4, y + h / 2), color=ACCENT, ms=7,
              style="<|-|>")
        label(ax, 36.0, y + h / 2 + 3.0, msgs, fs=7.0, color=ACCENT)

        label(ax, 77.0, y + h / 2, note, fs=6.6, color=SOFT, ha="left")

    # 三段之间用淡色分隔，提示这是三次独立交换
    for y in (34.2, 19.2):
        ax.plot([2.0, 98.0], [y, y], color="#e2e2dc", lw=0.7, zorder=1)

    return save(fig, "11", "kerberos-flow.png")


def enum_funnel():
    fig, ax = setup(5.3, 3.4)

    label(ax, 12.0, 60.0, "采集来源", fs=7.2, color=GREY, weight="bold")
    label(ax, 44.0, 60.0, "按 SID 归并", fs=7.2, color=GREY, weight="bold")
    label(ax, 81.0, 60.0, "连成路径", fs=7.2, color=GREY, weight="bold")

    sources = [
        ("LDAP 查询", "用户、组、OU", 43.0),
        ("SPN 注册表", "setspn -Q */*", 31.0),
        ("SMB 会话", "谁在哪台机器上", 19.0),
        ("SYSVOL", "GPO 与登录脚本", 7.0),
    ]
    for title, note, y in sources:
        box(ax, 1.0, y, 22.0, 9.0, fc=PALE, ec=LINE)
        label(ax, 12.0, y + 5.8, title, fs=7.4, color=INK, weight="bold")
        label(ax, 12.0, y + 3.0, note, fs=6.4, color=GREY)
        arrow(ax, (23.6, y + 4.5), (28.4, y + 4.5), color=ACCENT_2, lw=1.0, ms=6)

    # 中间的表
    box(ax, 29.0, 7.0, 30.0, 50.0, fc=PALE_BLUE, ec="#b6c4d2", radius=1.2)
    label(ax, 44.0, 53.0, "统一对象表", fs=7.8, color=BLUE, weight="bold")
    ax.plot([31.0, 57.0], [50.0, 50.0], color="#b6c4d2", lw=0.8, zorder=3)
    label(ax, 30.6, 47.2, "对象", fs=6.2, color=BLUE, ha="left")
    label(ax, 46.4, 47.2, "SID 后缀", fs=6.2, color=BLUE)
    label(ax, 57.4, 47.2, "组", fs=6.2, color=BLUE, ha="right")
    ax.plot([31.0, 57.0], [44.8, 44.8], color="#c9d5e0", lw=0.7, zorder=3)
    rows = [("zhang.wei", "1105", "Staff", 41.4),
            ("svc_sql", "1106", "Staff", 37.4),
            ("SRV01$", "1109", "Servers", 33.4)]
    for name, rid, grp, y in rows:
        label(ax, 30.6, y, name, fs=6.1, color=SOFT, ha="left")
        label(ax, 46.4, y, rid, fs=6.1, color=SOFT)
        label(ax, 57.4, y, grp, fs=6.1, color=SOFT, ha="right")
    ax.plot([31.0, 57.0], [30.6, 30.6], color="#c9d5e0", lw=0.7, zorder=3)
    label(ax, 44.0, 24.0, "不同来源里的同一个人\n合并成一行")
    label(ax, 44.0, 13.4, "唯一的键是 SID", fs=6.8, color=BLUE, weight="bold")

    arrow(ax, (59.6, 47.0), (63.4, 47.0), color=ACCENT, lw=1.0, ms=6)

    # 右侧的路径
    nodes = [("你的账号", 44.0), ("IT 组", 31.0),
             ("SRV01 管理员", 18.0), ("Domain Admins", 5.0)]
    for name, y in nodes:
        fc = PALE_WARN if name == "Domain Admins" else PALE
        box(ax, 64.0, y, 27.0, 6.6, fc=fc, ec=LINE, radius=1.0)
        label(ax, 77.5, y + 3.3, name, fs=7.0,
              color=WARN if name == "Domain Admins" else INK)
    edges = [("成员", 37.5), ("本地管理员", 24.5), ("成员", 11.5)]
    for text, y in edges:
        arrow(ax, (76.0, y + 6.9), (76.0, y - 0.3), color=ACCENT, lw=1.0, ms=6)
        label(ax, 78.0, y + 3.3, text, fs=6.4, color=ACCENT, ha="left")

    return save(fig, "11", "enum-funnel.png")


if __name__ == "__main__":
    kerberos_flow()
    enum_funnel()
