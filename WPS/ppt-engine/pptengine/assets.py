# -*- coding: utf-8 -*-
"""素材生成器：用 PIL 程序化产出配图，避免依赖外部图床或截图。

调用 ensure_default_assets() 会在资源目录生成一批通用素材：
  背景、渐变横幅、竖条、圆环、箭头、热图/散点/细胞/网页截图示意图等。
生成的图片均为原创绘制，可直接商用替换。
"""
from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw

from . import paths


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ---------------- 基础图形 ----------------
def grad_bar(path, c1, c2, w=480, h=72, cut=0.22, dark_bottom=True):
    """渐变斜切横幅"""
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im, "RGBA")
    for x in range(w):
        c = lerp(c1, c2, x / (w - 1))
        d.line([(x, 0), (x, h)], fill=c + (255,))
    if dark_bottom:
        y0 = int(h * 0.78)
        for y in range(y0, h):
            t = (y - y0) / max(1, h - 1 - y0)
            for x in range(w):
                base = lerp(c1, c2, x / (w - 1))
                c = lerp(base, tuple(int(v * 0.72) for v in base), t)
                d.point((x, y), fill=c + (255,))
    ch = int(h * cut)
    d.polygon([(0, 0), (ch, 0), (0, h)], fill=(0, 0, 0, 0))
    d.polygon([(w, h), (w - ch, h), (w, 0)], fill=(0, 0, 0, 0))
    im.save(path)


def vertical_accent(path, c1=(58, 116, 190), c2=(24, 62, 140), w=40, h=120):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im, "RGBA")
    for y in range(h):
        d.line([(0, y), (w, y)], fill=lerp(c1, c2, y / max(1, h - 1)) + (255,))
    im.save(path)


def ring(path, d0=300, stroke=(150, 198, 116), fill=(255, 255, 255, 0), width=3.0):
    im = Image.new("RGBA", (d0, d0), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im, "RGBA")
    dr.ellipse([0, 0, d0 - 1, d0 - 1], fill=fill, outline=stroke, width=int(width))
    im.save(path)


def arrow_img(path, w, h, direction="right",
              c1=(108, 190, 78), c2=(58, 148, 44), head=0.16):
    """渐变箭头：direction = 'right' | 'left'"""
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im, "RGBA")
    for x in range(w):
        d.line([(x, 0), (x, h)], fill=lerp(c1, c2, x / max(1, w - 1)) + (255,))
    hw, bh = int(w * head), h // 2
    if direction == "right":
        d.polygon([(w - 1, bh - h // 2), (w - 1, bh + h // 2), (w - hw, bh)], fill=c2 + (255,))
    else:
        d.polygon([(0, bh - h // 2), (0, bh + h // 2), (hw, bh)], fill=c2 + (255,))
    im.save(path)


def page_bg(path, w=960, h=540, top=(252, 253, 254), bottom=(246, 248, 250)):
    im = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(im)
    for y in range(h):
        d.line([(0, y), (w, y)], fill=lerp(top, bottom, y / max(1, h - 1)))
    im.save(path)


def deco_circle(path, d=200, outer=(210, 228, 246), inner=(228, 240, 252), alpha=90):
    im = Image.new("RGBA", (d, d), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im, "RGBA")
    dr.ellipse([0, 0, d - 1, d - 1], fill=outer + (alpha,))
    m = int(d * 0.12)
    dr.ellipse([m, m, d - 1 - m, d - 1 - m], fill=inner + (alpha,))
    im.save(path)


# ---------------- 科研示意图（占位用，可替换为真实素材）----------------
def fig_heat(path, w, h, palette, cell=10, seed=None):
    rng = random.Random(seed)
    im = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(im)
    cols = [lerp(palette[0], palette[1], i / max(1, len(palette) - 1)) for i in range(len(palette))]
    for y in range(0, h, cell):
        for x in range(0, w, cell):
            d.rectangle([x, y, x + cell - 1, y + cell - 1], fill=rng.choice(cols))
    im.save(path)


def fig_scatter(path, w, h, colors, n=240, seed=None):
    rng = random.Random(seed)
    im = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(im)
    for _ in range(n):
        cx, cy = rng.uniform(10, w - 10), rng.uniform(10, h - 10)
        c = rng.choice(colors)
        r = rng.uniform(2, 6)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
    im.save(path)


def fig_cells(path, w, h, n=26, seed=None, cols=None):
    rng = random.Random(seed)
    cols = cols or [(150, 200, 130), (90, 160, 200), (200, 150, 190), (230, 200, 90)]
    im = Image.new("RGB", (w, h), (252, 252, 252))
    d = ImageDraw.Draw(im, "RGBA")
    for _ in range(n):
        cx, cy = rng.uniform(w * 0.08, w * 0.92), rng.uniform(h * 0.1, h * 0.92)
        rx, ry = rng.uniform(w * 0.04, w * 0.12), rng.uniform(h * 0.06, h * 0.16)
        c = rng.choice(cols)
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=c + (150,), outline=(80, 80, 90), width=2)
        d.ellipse([cx - rx * 0.45, cy - ry * 0.5, cx + rx * 0.1, cy - ry * 0.05],
                  fill=(255, 255, 255, 90))
    im.save(path)


def fig_web(path, w, h, lines=22, seed=None):
    rng = random.Random(seed)
    im = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w, int(h * 0.06)], fill=(210, 60, 50))
    d.rectangle([0, int(h * 0.06), w, int(h * 0.13)], fill=(240, 240, 240))
    d.rectangle([int(w * 0.03), int(h * 0.02), int(w * 0.4), int(h * 0.045)], fill=(255, 255, 255))
    y = int(h * 0.16)
    for _ in range(lines):
        wl = rng.uniform(0.55, 0.94)
        d.rectangle([int(w * 0.04), y, int(w * (0.04 + wl)), y + max(2, int(h * 0.016))],
                    fill=(190, 195, 205))
        y += int(h * 0.055)
        if y > h * 0.94:
            break
    im.save(path)


def fig_paper(path, w, h, seed=None):
    rng = random.Random(seed)
    im = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(im)
    d.rectangle([int(w * 0.1), int(h * 0.04), int(w * 0.9), int(h * 0.12)], fill=(30, 30, 30))
    y = int(h * 0.16)
    while y < h * 0.94:
        wl = rng.uniform(0.5, 0.95)
        d.rectangle([int(w * 0.08), y, int(w * (0.08 + wl)), y + max(2, int(h * 0.018))],
                    fill=(150, 155, 165))
        y += int(h * 0.05)
    hy = rng.uniform(0.35, 0.6)
    d.rectangle([int(w * 0.08), int(h * hy), int(w * 0.9), int(h * (hy + 0.07))], fill=(220, 90, 80))
    im.save(path)


# ---------------- 一键生成默认素材 ----------------
def ensure_default_assets(target_dir=None, force=False) -> Path:
    """生成通用素材到资源目录（已存在则跳过，force=True 强制重画）"""
    base = Path(target_dir).expanduser().resolve() if target_dir else paths.assets_dir()
    base.mkdir(parents=True, exist_ok=True)

    def done(name):
        return (base / name).exists()

    def gen(name, fn):
        if force or not done(name):
            fn(str(base / name))

    gen("bg_page.png", lambda p: page_bg(p))
    gen("bar_blue.png", lambda p: grad_bar(p, (58, 116, 190), (24, 62, 140)))
    gen("bar_teal.png", lambda p: grad_bar(p, (36, 150, 160), (18, 96, 118)))
    gen("bar_red.png", lambda p: grad_bar(p, (232, 78, 62), (176, 24, 24)))
    gen("bar_dark.png", lambda p: grad_bar(p, (40, 88, 160), (16, 44, 110)))
    gen("accent_bar.png", lambda p: vertical_accent(p))
    gen("deco_circle.png", lambda p: deco_circle(p))
    gen("ring.png", lambda p: ring(p))
    gen("arrow_green.png", lambda p: arrow_img(p, 690, 34, "right"))
    gen("arrow_orange.png", lambda p: arrow_img(p, 420, 30, "left",
                                                (244, 158, 62), (226, 116, 32)))
    gen("fig_heat.png", lambda p: fig_heat(p, 360, 200, [(240, 200, 190), (180, 60, 50), (90, 20, 20)], 9, seed=1))
    gen("fig_scatter.png", lambda p: fig_scatter(p, 360, 200, [(80, 120, 200), (200, 120, 160)], seed=2))
    gen("fig_cells.png", lambda p: fig_cells(p, 470, 420, n=26, seed=3))
    gen("fig_web.png", lambda p: fig_web(p, 420, 240, seed=4))
    gen("fig_paper.png", lambda p: fig_paper(p, 420, 230, seed=5))
    return base
