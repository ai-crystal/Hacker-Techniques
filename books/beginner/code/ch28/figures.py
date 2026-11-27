# -*- coding: utf-8 -*-
"""第二十八章插图：企业网络分区与一条入侵路径。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def network_zones():
    """分层：互联网 / 边界 / DMZ / 内网。"""
    fig, ax = setup(5.3, 3.6)

    # 互联网
    box(ax, 20.0, 52.0, 60.0, 8.5, fc=PALE_2, ec=LINE)
    label(ax, 22.0, 57.2, "互联网", fs=8.4, color=INK, ha="left",
          weight="bold")
    label(ax, 22.0, 54.2, "任何地址都能主动发起连接", fs=6.8, color=GREY,
          ha="left")

    # 边界
    box(ax, 20.0, 39.0, 60.0, 8.5, fc=PALE_BLUE, ec="#b6c4d2")
    label(ax, 22.0, 44.2, "边界", fs=8.4, color=BLUE, ha="left",
          weight="bold")
    label(ax, 31.6, 44.2, "防火墙与 VPN 网关", fs=7.0, color=BLUE, ha="left")
    label(ax, 22.0, 41.2, "默认拒绝，只放行登记过的端口与账号", fs=6.8,
          color=GREY, ha="left")

    # DMZ
    box(ax, 20.0, 26.0, 60.0, 8.5, fc=PALE_WARN, ec="#d8c3b8")
    label(ax, 22.0, 31.2, "DMZ", fs=8.4, color=WARN, ha="left", weight="bold")
    label(ax, 30.4, 31.2, "对外 Web、邮件网关、反向代理", fs=7.0, color=WARN,
          ha="left")
    label(ax, 22.0, 28.2, "设计前提是它会被攻破，所以朝内的一侧必须窄",
          fs=6.8, color=GREY, ha="left")

    # 内网
    box(ax, 20.0, 2.5, 60.0, 16.5, fc="#f7f9f8", ec=LINE, lw=0.9)
    label(ax, 22.0, 16.0, "内网", fs=8.4, color=ACCENT, ha="left",
          weight="bold")
    label(ax, 30.0, 16.0, "分区之间默认不通，跨区要经检查点", fs=6.8,
          color=GREY, ha="left")

    zones = [(21.8, "办公网", "终端最多"),
             (41.0, "生产网", "可用性优先"),
             (60.2, "运维网", "权限最高")]
    for x, name, note in zones:
        box(ax, x, 4.4, 18.0, 7.6, fc=PALE, ec=LINE, lw=0.9)
        label(ax, x + 9.0, 9.5, name, fs=7.4, color=INK, weight="bold")
        label(ax, x + 9.0, 6.7, note, fs=6.4, color=GREY)

    # 纵向流程
    arrow(ax, (50.0, 51.9), (50.0, 47.7), lw=1.2)
    arrow(ax, (50.0, 38.9), (50.0, 34.7), lw=1.2)

    # DMZ 到内网：禁止
    ax.plot([50.0, 50.0], [25.9, 19.1], color=GREY, lw=1.0,
            ls=(0, (3, 2.4)), zorder=2)
    label(ax, 50.0, 22.5, "×", fs=11.0, color=WARN, weight="bold")
    label(ax, 52.6, 22.5, "未经登记的流量一律拒绝", fs=6.6, color=WARN,
          ha="left")

    # VPN 隧道：绕开 DMZ 直进内网
    ax.plot([80.0, 92.5, 92.5, 83.5], [43.25, 43.25, 14.5, 14.5],
            color=ACCENT_2, lw=1.0, ls=(0, (4, 2.2)), zorder=2)
    arrow(ax, (83.6, 14.5), (80.0, 14.5), color=ACCENT_2, lw=1.0)
    label(ax, 86.3, 44.9, "VPN", fs=6.8, color=ACCENT_2)

    label(ax, 20.0, 63.2, "实线为已登记的访问方向，虚线为被终止的路径",
          fs=6.8, color=GREY, ha="left")
    return save(fig, "28", "network-zones.png")


def intrusion_path():
    """五个阶段与各自的断点。"""
    fig, ax = setup(5.3, 3.5)
    label(ax, 4.0, 57.2, "五个阶段是串联的，断开任意一处，后面都要重来",
          fs=7.2, color=GREY, ha="left")

    line_x = 26.0
    ax.plot([line_x, line_x], [10.0, 52.0], color=LINE, lw=1.0, zorder=1)

    stages = [
        ("外网入口", "VPN、邮件、Web 应用",
         "入口设备当公网资产对待，打补丁、上 MFA"),
        ("边缘一台", "打印机、NAS、测试机",
         "资产台账加分区，让边缘机器摸不到别的机器"),
        ("拿到凭据", "浏览器、配置、共享盘",
         "凭据进保险库，机器上不留可复用的密码"),
        ("横向移动", "RDP、SMB、WMI",
         "最小权限，横向移动要能触发告警"),
        ("域控与备份", "全部账号、恢复能力",
         "一份离线备份，删得掉数据删不掉副本"),
    ]

    ys = [48.0, 38.6, 29.2, 19.8, 10.4]
    for (name, note, block), y in zip(stages, ys):
        ax.plot([line_x], [y], marker="o", markersize=5.2, markerfacecolor="white",
                markeredgecolor=ACCENT, markeredgewidth=1.1, zorder=4)
        label(ax, 23.0, y + 1.9, name, fs=7.8, color=INK, ha="right",
              weight="bold")
        label(ax, 23.0, y - 1.9, note, fs=6.3, color=GREY, ha="right")
        box(ax, 32.0, y - 3.8, 66.0, 7.6, fc=PALE, ec=LINE, lw=0.9)
        label(ax, 34.2, y, "断点", fs=6.6, color=WARN, ha="left",
              weight="bold")
        label(ax, 41.0, y, block, fs=6.7, color=INK, ha="left")

    return save(fig, "28", "intrusion-path.png")


if __name__ == "__main__":
    network_zones()
    intrusion_path()
