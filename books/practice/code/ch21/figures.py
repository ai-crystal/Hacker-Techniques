# -*- coding: utf-8 -*-
"""第二十一章插图：Pod 到节点的信任边界、RBAC 的权限传递。

画布宽度统一取 5.3 英寸，与版心宽度接近，图内不写标题。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def pod_to_node():
    """左右两栏，中间一道边界，三个开关决定箭头能不能穿过去。"""
    fig, ax = setup(5.3, 3.6)

    rect(ax, 2.0, 3.0, 42.0, 60.0, fc=PALE_BLUE, ec="none", zorder=1)
    rect(ax, 56.0, 3.0, 42.0, 60.0, fc=PALE_2, ec="none", zorder=1)

    label(ax, 4.5, 60.4, "Pod 内", fs=6.8, color=BLUE, ha="left",
          weight="bold")
    label(ax, 4.5, 56.4, "namespace 与 cgroup 划的圈", fs=6.2, color=SOFT,
          ha="left")
    label(ax, 58.5, 60.4, "节点上", fs=6.8, color=SOFT, ha="left",
          weight="bold")
    label(ax, 58.5, 56.4, "内核只有一个，运行时是 root", fs=6.2, color=SOFT,
          ha="left")

    left = [(40.0, "容器进程", "root，但能力集被裁过"),
            (24.0, "挂载的卷", "来自 spec.volumes"),
            (8.0, "API 凭据", "挂进来的 token 或 socket")]
    right = [(40.0, "宿主内核", "设备、模块、全部 caps"),
             (24.0, "宿主文件系统", "kubelet 目录、容器层"),
             (8.0, "容器运行时", "socket 等于节点 root")]

    for y, name, note in left:
        box(ax, 4.0, y, 38.0, 12.0, fc="white", ec=LINE, lw=0.9)
        label(ax, 23.0, y + 7.6, name, fs=6.8, color=INK, weight="bold")
        label(ax, 23.0, y + 3.6, note, fs=5.9, color=SOFT)

    for y, name, note in right:
        box(ax, 58.0, y, 38.0, 12.0, fc="white", ec=LINE, lw=0.9)
        label(ax, 77.0, y + 7.6, name, fs=6.8, color=INK, weight="bold")
        label(ax, 77.0, y + 3.6, note, fs=5.9, color=SOFT)

    ax.plot([50.0, 50.0], [4.0, 53.0], color=WARN, lw=0.9,
            ls=(0, (3.2, 2.4)), zorder=2)
    label(ax, 50.0, 55.2, "边界", fs=6.2, color=WARN)

    for y, name in ((46.0, "privileged"), (30.0, "hostPath"),
                    (14.0, "docker.sock")):
        arrow(ax, (42.4, y), (57.6, y), color=WARN, lw=1.0, ms=6.5)
        label(ax, 50.0, y + 2.4, name, fs=5.9, color=WARN,
              bbox=dict(boxstyle="square,pad=0.12", fc="white", ec="none"))

    return save(fig, "21", "pod-to-node.png")


def rbac_chain():
    """一条链是规则怎么落地，另一条是 token 怎么被换成数据。"""
    fig, ax = setup(5.3, 3.3)

    box(ax, 2.0, 40.0, 19.0, 13.0, fc=PALE, ec=LINE, lw=0.9)
    label(ax, 11.5, 49.4, "ServiceAccount", fs=6.4, color=INK, weight="bold")
    label(ax, 11.5, 44.8, "命名空间内的身份", fs=6.0, color=SOFT)

    box(ax, 28.0, 40.0, 19.0, 13.0, fc=PALE, ec=LINE, lw=0.9)
    label(ax, 37.5, 49.4, "RoleBinding", fs=6.4, color=INK, weight="bold")
    label(ax, 37.5, 44.8, "把身份接到规则", fs=6.0, color=SOFT)

    box(ax, 54.0, 40.0, 19.0, 13.0, fc=PALE, ec=LINE, lw=0.9)
    label(ax, 63.5, 49.4, "Role / ClusterRole", fs=6.0, color=INK,
          weight="bold")
    label(ax, 63.5, 44.8, "动词 + 资源", fs=6.0, color=SOFT)

    box(ax, 80.0, 40.0, 18.0, 13.0, fc=PALE_2, ec=LINE, lw=0.9)
    label(ax, 89.0, 49.4, "资源", fs=6.4, color=INK, weight="bold")
    label(ax, 89.0, 44.8, "pods、secrets", fs=6.0, color=SOFT)

    arrows = ((21.4, 27.4, "绑定", 46.5), (47.4, 53.4, "规则", 46.5),
              (73.4, 79.4, "鉴权", 46.5))
    for x1, x2, name, y in arrows:
        arrow(ax, (x1, y), (x2, y), color=ACCENT, lw=1.0, ms=6.5)
        label(ax, (x1 + x2) / 2, y + 2.4, name, fs=5.9, color=GREY)

    box(ax, 2.0, 16.0, 19.0, 13.0, fc=PALE_BLUE, ec="#bdc9d6", lw=0.9)
    label(ax, 11.5, 25.4, "Pod", fs=6.6, color=BLUE, weight="bold")
    label(ax, 11.5, 20.8, "默认自动挂 token", fs=5.9, color=SOFT)

    box(ax, 28.0, 16.0, 21.0, 13.0, fc=PALE_BLUE, ec="#bdc9d6", lw=0.9)
    label(ax, 38.5, 25.4, "token 文件", fs=6.4, color=BLUE, weight="bold")
    label(ax, 38.5, 20.8, "/var/run/secrets/…", fs=5.9, color=SOFT)

    box(ax, 54.0, 16.0, 20.0, 13.0, fc=PALE_BLUE, ec="#bdc9d6", lw=0.9)
    label(ax, 64.0, 25.4, "apiserver", fs=6.4, color=BLUE, weight="bold")
    label(ax, 64.0, 20.8, "认出这个身份", fs=5.9, color=SOFT)

    box(ax, 81.0, 16.0, 17.0, 13.0, fc=PALE_WARN, ec="#ddc4b8", lw=0.9)
    label(ax, 89.5, 25.4, "Secret", fs=6.4, color=WARN, weight="bold")
    label(ax, 89.5, 20.8, "别的服务凭据", fs=5.9, color=SOFT)

    for x1, x2, name in ((21.4, 27.4, "读取"), (49.4, 53.4, "调用"),
                         (74.4, 80.4, "列出")):
        arrow(ax, (x1, 22.5), (x2, 22.5), color=BLUE, lw=1.0, ms=6.5)
        label(ax, (x1 + x2) / 2, 24.7, name, fs=5.9, color=GREY)

    arrow(ax, (11.5, 29.4), (11.5, 39.6), color=ACCENT, lw=1.0, ms=6.5)
    label(ax, 13.0, 34.5, "以 SA 身份", fs=5.9, color=GREY, ha="left")

    box(ax, 4.0, 2.0, 92.0, 8.6, fc=PALE_2, ec=LINE, lw=0.8)
    label(ax, 50.0, 6.3,
          "鉴权的三个输入是身份、动词、资源加命名空间；token 的价值等于它绑到的规则",
          fs=6.1, color=SOFT)

    return save(fig, "21", "rbac-chain.png")


if __name__ == "__main__":
    pod_to_node()
    rbac_chain()
