# -*- coding: utf-8 -*-
"""第二十章插图：云上的信任关系、从 SSRF 到临时凭据的路径。

画布宽度统一取 5.3 英寸，与版心宽度接近，图内不写标题。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def cloud_trust():
    """两道门：信任策略决定谁能进来，权限策略决定进来能干什么。"""
    fig, ax = setup(5.3, 3.2)

    rect(ax, 2.0, 50.0, 96.0, 7.6, fc=PALE_BLUE, ec="none", zorder=1)
    label(ax, 50.0, 53.8,
          "扮演成功后拿到 STS 临时凭据，有效权限是所有策略的交集",
          fs=6.3, color=BLUE)

    box(ax, 1.5, 27.0, 18.0, 16.0, fc=PALE, ec=LINE, lw=0.9)
    label(ax, 10.5, 39.4, "调用方", fs=7.4, color=INK, weight="bold")
    label(ax, 10.5, 34.6, "用户 / 实例角色", fs=6.2, color=SOFT)
    label(ax, 10.5, 31.0, "外部账号", fs=6.2, color=SOFT)

    box(ax, 27.0, 27.0, 18.0, 16.0, fc=PALE_WARN, ec="#ddc4b8", lw=0.9)
    label(ax, 36.0, 39.4, "信任策略", fs=7.4, color=WARN, weight="bold")
    label(ax, 36.0, 34.6, "谁能扮演", fs=6.2, color=SOFT)
    label(ax, 36.0, 31.0, "绑在角色上", fs=6.2, color=SOFT)

    box(ax, 52.5, 27.0, 18.0, 16.0, fc=PALE, ec=LINE, lw=0.9)
    label(ax, 61.5, 39.4, "权限策略", fs=7.4, color=INK, weight="bold")
    label(ax, 61.5, 34.6, "进来能做什么", fs=6.2, color=SOFT)
    label(ax, 61.5, 31.0, "绑在身份上", fs=6.2, color=SOFT)

    box(ax, 78.0, 27.0, 20.5, 16.0, fc=PALE_2, ec=LINE, lw=0.9)
    label(ax, 88.2, 39.4, "资源", fs=7.4, color=INK, weight="bold")
    label(ax, 88.2, 34.6, "S3 / KMS", fs=6.2, color=SOFT)
    label(ax, 88.2, 31.0, "Secrets / EC2", fs=6.2, color=SOFT)

    for x1, x2, num in ((19.9, 26.2, "①"), (45.4, 51.7, "②"), (70.9, 77.2, "③")):
        arrow(ax, (x1, 35.0), (x2, 35.0), color=ACCENT, lw=1.1, ms=7.5)
        label(ax, (x1 + x2) / 2, 38.4, num, fs=7.4, color=ACCENT)

    box(ax, 6.0, 12.0, 88.0, 9.4, fc=PALE_2, ec=LINE, lw=0.8)
    label(ax, 50.0, 18.0,
          "① 信任策略放行　　② 权限策略求值　　③ 资源策略再判一次",
          fs=6.3, color=SOFT)
    label(ax, 50.0, 14.6,
          "任何一道拒绝，请求就以 AccessDenied 结束", fs=6.3, color=WARN)

    return save(fig, "20", "cloud-trust.png")


def ssrf_to_creds():
    """从公网请求到临时凭据的四步，以及 IMDSv2 在第三步前拦下的地方。"""
    fig, ax = setup(5.3, 3.6)

    box(ax, 2.0, 44.0, 20.0, 14.0, fc=PALE, ec=LINE, lw=0.9)
    label(ax, 12.0, 54.4, "公网请求", fs=7.2, color=INK, weight="bold")
    label(ax, 12.0, 49.6, "图片抓取", fs=6.2, color=SOFT)
    label(ax, 12.0, 46.6, "URL 预览", fs=6.2, color=SOFT)

    box(ax, 28.0, 44.0, 30.0, 14.0, fc=PALE_WARN, ec="#ddc4b8", lw=0.9)
    label(ax, 43.0, 54.4, "Web 应用", fs=7.2, color=WARN, weight="bold")
    label(ax, 43.0, 49.6, "服务端替用户取 URL", fs=6.2, color=SOFT)
    label(ax, 43.0, 46.6, "不校验目标地址", fs=6.2, color=SOFT)

    box(ax, 64.0, 44.0, 34.0, 14.0, fc=PALE_BLUE, ec="#bdc9d6", lw=0.9)
    label(ax, 81.0, 54.4, "169.254.169.254", fs=7.2, color=BLUE, weight="bold")
    label(ax, 81.0, 49.6, "实例元数据服务", fs=6.2, color=SOFT)
    label(ax, 81.0, 46.6, "只对实例自身开放", fs=6.2, color=SOFT)

    box(ax, 64.0, 18.0, 34.0, 14.0, fc=PALE_WARN, ec="#ddc4b8", lw=0.9)
    label(ax, 81.0, 28.4, "临时凭据", fs=7.2, color=WARN, weight="bold")
    label(ax, 81.0, 23.6, "AccessKeyId / SecretKey", fs=6.2, color=SOFT)
    label(ax, 81.0, 20.6, "外带 SessionToken", fs=6.2, color=SOFT)

    box(ax, 28.0, 18.0, 30.0, 14.0, fc=PALE, ec=LINE, lw=0.9)
    label(ax, 43.0, 28.4, "云 API", fs=7.2, color=INK, weight="bold")
    label(ax, 43.0, 23.6, "枚举存储与密钥", fs=6.2, color=SOFT)
    label(ax, 43.0, 20.6, "权限够大就能建后门", fs=6.2, color=SOFT)

    arrow(ax, (22.6, 51.0), (27.4, 51.0), color=ACCENT, lw=1.1, ms=7.5)
    arrow(ax, (58.6, 51.0), (63.4, 51.0), color=ACCENT, lw=1.1, ms=7.5)
    arrow(ax, (81.0, 43.4), (81.0, 32.6), color=ACCENT, lw=1.1, ms=7.5)
    arrow(ax, (63.4, 25.0), (58.6, 25.0), color=ACCENT, lw=1.1, ms=7.5)

    label(ax, 25.0, 54.0, "①", fs=7.4, color=ACCENT)
    label(ax, 61.0, 54.0, "②", fs=7.4, color=ACCENT)
    label(ax, 79.2, 38.2, "③", fs=7.4, color=ACCENT, ha="right")
    label(ax, 61.0, 28.0, "④", fs=7.4, color=ACCENT)

    box(ax, 2.0, 2.0, 96.0, 11.0, fc=PALE_2, ec=LINE, lw=0.8)
    label(ax, 50.0, 9.4,
          "IMDSv2 要求先 PUT /latest/api/token 取令牌，再带 X-aws-ec2-metadata-token 发 GET",
          fs=6.2, color=SOFT)
    label(ax, 50.0, 5.4,
          "只能发 GET 的 SSRF 到第三步就断了；IMDSv1 没这一步",
          fs=6.2, color=WARN)

    return save(fig, "20", "ssrf-to-creds.png")


if __name__ == "__main__":
    cloud_trust()
    ssrf_to_creds()
