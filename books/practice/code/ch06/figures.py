# -*- coding: utf-8 -*-
"""第六章插图：SSRF 的可达面、上传文件的处理链路。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'common'))

from figstyle import (ACCENT, ACCENT_2, BLUE, GREY, INK, LINE, PALE, PALE_2,
                      PALE_BLUE, PALE_WARN, SOFT, WARN, arrow, box, label,
                      rect, save, setup)


def ssrf_path():
    fig, ax = setup(5.3, 3.5)

    box(ax, 1.5, 40.0, 17.0, 13.0, fc="white", ec=LINE)
    label(ax, 10.0, 49.4, "攻击者", fs=9.2, color=INK, weight="bold")
    label(ax, 10.0, 44.4, "只能访问 80", fs=7.2, color=GREY)

    box(ax, 26.0, 37.0, 25.0, 22.0, fc=PALE_WARN, ec="#d8b3a4")
    label(ax, 38.5, 55.0, "对外 Web 应用", fs=9.2, color=INK, weight="bold")
    label(ax, 38.5, 49.6, "url 参数直接", fs=7.4, color=SOFT)
    label(ax, 38.5, 45.6, "交给请求库", fs=7.4, color=SOFT)
    label(ax, 38.5, 40.6, "服务端发起连接", fs=7.2, color=WARN)

    arrow(ax, (18.9, 46.5), (25.6, 46.5))
    label(ax, 22.2, 49.6, "GET", fs=6.8, color=GREY)

    rect(ax, 57.0, 5.0, 41.5, 59.0, fc=PALE_2, ec="#dcdad2", lw=0.9)
    label(ax, 59.6, 60.6, "服务器所在的网络", fs=7.6, color=GREY, ha="left")

    targets = [
        ("云元数据 169.254.169.254", "实例角色凭据", 48.6, PALE_BLUE, BLUE),
        ("Redis 127.0.0.1:6379", "无口令时可直接写键", 36.0, PALE, SOFT),
        ("管理后台 :8080", "只监听回环", 23.4, PALE, SOFT),
        ("数据库 :3306", "信任来源 IP", 10.8, PALE, SOFT),
    ]
    ax.plot([51.4, 54.4], [48.0, 48.0], color=ACCENT_2, lw=1.2, zorder=3)
    for text, note, y, fc, col in targets:
        box(ax, 60.0, y, 36.0, 10.2, fc=fc, ec=LINE, lw=0.9)
        label(ax, 61.6, y + 6.4, text, fs=7.6, color=col, ha="left")
        label(ax, 61.6, y + 3.0, note, fs=6.8, color=GREY, ha="left")
        arrow(ax, (54.4, 48.0), (60.0, y + 5.1), lw=1.0)

    label(ax, 1.5, 30.4, "校验只比对字符串前缀", fs=7.2, color=WARN, ha="left")
    label(ax, 1.5, 26.4, "挡不住 302 跳转", fs=7.2, color=WARN, ha="left")
    label(ax, 1.5, 22.4, "也挡不住 DNS 重绑定", fs=7.2, color=WARN, ha="left")
    ax.plot([1.5, 47.0], [19.4, 19.4], color="#e0d3cb", lw=0.8)
    label(ax, 1.5, 15.4, "真正有效的是出口策略", fs=7.2, color=ACCENT, ha="left")
    label(ax, 1.5, 11.4, "与网络层的默认拒绝", fs=7.2, color=ACCENT, ha="left")

    return save(fig, "06", "ssrf-path.png")


def upload_chain():
    fig, ax = setup(5.3, 3.6)

    rows = [
        ("① 客户端", "文件名与 Content-Type 都能随手改", "声明成 image/png，内容另写"),
        ("② 网关", "按长度截断、按类型头粗筛", "分块传输，或多段表单里改名"),
        ("③ 应用校验", "查后缀黑名单、查文件头", "黑名单漏掉 .phtml，两份检查不一致"),
        ("④ 落盘", "改名后放进 uploads 目录", "目录带执行权，或能写 .htaccess"),
        ("⑤ 解析器", "按后缀决定交给谁执行", "多后缀与 PATH_INFO 走另一条规则"),
    ]
    h, x, w = 9.6, 1.5, 33.0
    y = 56.0
    for name, what, bypass in rows:
        box(ax, x, y, w, h, fc=PALE, ec=LINE)
        label(ax, x + 2.2, y + h / 2, name, fs=8.6, color=INK, ha="left",
              weight="bold")
        label(ax, 40.0, y + 6.3, what, fs=7.4, color=SOFT, ha="left")
        label(ax, 40.0, y + 2.9, "绕过点　" + bypass, fs=7.2, color=WARN,
              ha="left")
        y -= 12.0

    for i in range(4):
        top = 56.0 - i * 12.0
        arrow(ax, (18.0, top - 0.4), (18.0, top - 2.4), lw=1.0)

    label(ax, 1.5, 4.2, "判定顺序：先看最终由谁解析，再回头看每一道关的检查对象",
          fs=7.2, color=ACCENT, ha="left")

    return save(fig, "06", "upload-chain.png")


if __name__ == "__main__":
    ssrf_path()
    upload_chain()
