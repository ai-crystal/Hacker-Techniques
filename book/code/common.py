# -*- coding: utf-8 -*-
"""插图公共样式与绘图小工具。

所有插图都用代码绘制，统一使用这里的配色、字号和坐标约定，
避免不同章之间的风格漂移。
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

# 显式登记系统中文字体，保证 bold 也有中文字形
for _f in ("msyh.ttc", "msyhbd.ttc", "simhei.ttf"):
    _path = Path("C:/Windows/Fonts") / _f
    if _path.exists():
        try:
            fm.fontManager.addfont(str(_path))
        except Exception:
            pass

# 配色
INK = "#1c1c1e"
SOFT = "#4a4f52"
GREY = "#767676"
LINE = "#b9b9b4"
ACCENT = "#0f5c5c"
ACCENT_2 = "#2f7f7a"
WARN = "#a8442a"
PALE = "#eef2f1"
PALE_2 = "#f6f5f0"
PALE_WARN = "#f6ece6"
PALE_BLUE = "#e8eef4"
BLUE = "#2b4f74"

FONT_SANS = ["Microsoft YaHei", "SimHei"]
FONT_SERIF = ["SimSun", "Noto Serif SC"]

ROOT = Path(__file__).resolve().parents[2]
IMAGES = ROOT / "book" / "images"


def setup(width: float = 6.6, height: float = 3.4, serif: bool = False) -> tuple:
    plt.rcParams.update({
        "font.family": FONT_SERIF if serif else FONT_SANS,
        "font.size": 9,
        "axes.unicode_minus": False,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "savefig.dpi": 220,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.06,
        "text.color": INK,
    })
    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100 * height / width)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, text="", fc=PALE, ec=LINE, lw=1.0, fs=9,
        color=INK, weight="normal", radius=0.8, zorder=2, va="center",
        ha="center", family=None, style=None):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        linewidth=lw, edgecolor=ec, facecolor=fc, zorder=zorder,
        mutation_aspect=1,
    )
    ax.add_patch(patch)
    if text:
        ax.text(x + w / 2 if ha == "center" else x + 1.6,
                y + h / 2 if va == "center" else y + h - 1.2,
                text, ha=ha, va=va, fontsize=fs, color=color,
                fontweight=weight, zorder=zorder + 1, linespacing=1.55,
                family=family, style=style)
    return patch


def rect(ax, x, y, w, h, fc=PALE, ec="none", lw=0, zorder=1, alpha=1.0):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec,
                           linewidth=lw, zorder=zorder, alpha=alpha))


def arrow(ax, p1, p2, color=ACCENT, lw=1.2, style="-|>", rad=0.0, ls="-",
          zorder=3, ms=8):
    ax.add_patch(FancyArrowPatch(
        p1, p2, arrowstyle=style, mutation_scale=ms, linewidth=lw,
        color=color, connectionstyle=f"arc3,rad={rad}", zorder=zorder,
        linestyle=ls, shrinkA=0, shrinkB=0,
        joinstyle="miter", capstyle="butt"))


def label(ax, x, y, text, fs=8.2, color=SOFT, ha="center", va="center",
          weight="normal", family=None, style=None, rotation=0, zorder=6,
          bbox=None):
    ax.text(x, y, text, fontsize=fs, color=color, ha=ha, va=va,
            fontweight=weight, family=family, style=style,
            rotation=rotation, zorder=zorder, linespacing=1.5, bbox=bbox)


def save(fig, chapter: str, name: str) -> Path:
    folder = chapter if chapter.startswith("ch") else f"ch{chapter}"
    out = IMAGES / folder / name
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)
    plt.close(fig)
    print(f"  {out.relative_to(ROOT)}")
    return out
