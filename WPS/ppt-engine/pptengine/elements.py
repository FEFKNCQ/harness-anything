# -*- coding: utf-8 -*-
"""绘图原语：文字 / 形状 / 图片 / 组合组件。

所有坐标单位为 pt，画布默认 960x540（16:9）。
颜色统一用 (R, G, B) 元组，内部自行转成 WPS 需要的 BGR 整数。
"""
from __future__ import annotations

import os
from pathlib import Path

from . import paths
from PIL import Image

# ---------- 全局可调项 ----------
FONT = "微软雅黑"          # 中文字体，防方块
TITLE_FONT = "微软雅黑"    # 需要书法风时改成 "STXingkai" / "华文行楷"
_ASSETS_DIR = paths.assets_dir()

# 常用色板
INK = (32, 32, 38)
WHITE = (255, 255, 255)
BLUE = (16, 62, 140)
BLUE_M = (36, 92, 170)
BLUE_L = (214, 231, 248)
TEAL = (18, 104, 124)
RED = (192, 24, 24)
ORANGE = (232, 126, 34)
GRAY_BG = (243, 245, 248)
GRAY_TX = (88, 94, 104)


def set_assets_dir(p):
    global _ASSETS_DIR
    _ASSETS_DIR = Path(p).expanduser().resolve()


def get_assets_dir() -> Path:
    return _ASSETS_DIR


def h2b(c):
    """(R,G,B) -> WPS COM 需要的 BGR 整数"""
    return (c[2] << 16) | (c[1] << 8) | c[0]


# ---------------- 文字 ----------------
def txt(s, x, y, w, h, text, fs=13, color=INK, bold=False, align=1, anchor=3, font=None):
    """align: 0=左 1=中 2=右；anchor: 1=顶 3=垂直居中"""
    tb = s.Shapes.AddTextbox(1, x, y, w, h)
    tf = tb.TextFrame
    tf.WordWrap = True                       # 居中/右对齐必须 True，否则文字跑出页面
    try:
        tf.MarginLeft = 0; tf.MarginRight = 0
        tf.MarginTop = 0; tf.MarginBottom = 0
        tf.AutoSize = 0
        n = text.count("\n") + 1
        if n > 1 and anchor == 3:            # 多行垂直居中在 WPS 会算错，改顶对齐+手动下移
            anchor = 1
            tb.Top = y + max(0, (h - n * fs * 1.42) / 2)
        tf.VerticalAnchor = anchor
    except Exception:                         # noqa: BLE001
        pass
    tf.TextRange.Text = text
    f = tf.TextRange.Font
    f.Name = font or FONT
    f.Size = fs
    f.Color.RGB = h2b(color)
    if bold:
        f.Bold = True                         # 只在 True 时赋值；赋 False 部分版本会抛异常
    try:
        tf.TextRange.ParagraphFormat.Alignment = {0: 1, 1: 2, 2: 3}[align]
    except Exception:                         # noqa: BLE001
        pass
    return tb


def rich(s, x, y, w, h, parts, fs=13, align=0, anchor=3, font=None):
    """分段着色：parts = [(文字, 颜色, 是否加粗), ...]"""
    tb = txt(s, x, y, w, h, "".join(p[0] for p in parts),
             fs=fs, color=INK, bold=False, align=align, anchor=anchor, font=font)
    tf = tb.TextFrame
    pos = 1
    for t, c, b in parts:
        n = len(t)
        if n <= 0:
            continue
        try:
            rng = tf.TextRange.Characters(pos, n)
            rng.Font.Color.RGB = h2b(c)
            if b:
                rng.Font.Bold = True
        except Exception:                     # noqa: BLE001
            pass
        pos += n
    return tb


# ---------------- 图片 ----------------
def pic(s, name, x, y, w, h, fit=True, assets_dir=None):
    """按文件名从资源目录插入图片；fit=True 时等比缩放居中，防溢出。"""
    base = Path(assets_dir) if assets_dir else _ASSETS_DIR
    p = base / name
    if not os.path.exists(p):
        print(f"[pic] 缺失: {p}")
        return None
    try:
        iw, ih = Image.open(str(p)).size
    except Exception:                         # noqa: BLE001
        return None
    if fit and iw > 0 and ih > 0:
        sr, ir = w / h, iw / ih
        if ir > sr:
            nw, nh = w, int(w / ir)
        else:
            nh, nw = h, int(h * ir)
        x += (w - nw) // 2
        y += (h - nh) // 2
        w, h = nw, nh
    try:
        return s.Shapes.AddPicture(str(p), False, True, x, y, w, h)
    except Exception as e:                    # noqa: BLE001
        print(f"[pic] 插入失败: {e}")
        return None


# ---------------- 形状 ----------------
def shape(s, t, x, y, w, h, fill=None, line=None, lw=1.0):
    """常用 MsoShapeType：1 矩形 / 5 圆角矩形 / 9 椭圆 / 33 右箭头"""
    sp = s.Shapes.AddShape(t, x, y, w, h)
    if fill is not None:
        sp.Fill.ForeColor.RGB = h2b(fill)
    else:
        sp.Fill.Visible = 0
    if line is not None:
        sp.Line.ForeColor.RGB = h2b(line)
        sp.Line.Weight = lw
    else:
        sp.Line.Visible = 0
    return sp


def rect(s, x, y, w, h, fill=None, line=None, lw=1.0):
    return shape(s, 1, x, y, w, h, fill, line, lw)


def rrect(s, x, y, w, h, fill=None, line=None, lw=1.0):
    return shape(s, 5, x, y, w, h, fill, line, lw)


def oval(s, x, y, w, h, fill=None, line=None, lw=1.0):
    return shape(s, 9, x, y, w, h, fill, line, lw)


def arrow(s, x, y, w, h, fill=BLUE_M, direction="right"):
    """方向箭头；direction='left' 时旋转 180 度"""
    sp = shape(s, 33, x, y, w, h, fill=fill)
    if direction == "left":
        try:
            sp.Rotation = 180
        except Exception:                     # noqa: BLE001
            pass
    return sp


def hline(s, x, y, w, color, wt=1.0):
    ln = s.Shapes.AddLine(x, y, x + w, y)
    ln.Line.ForeColor.RGB = h2b(color)
    ln.Line.Weight = wt
    return ln


# ---------------- 组合组件 ----------------
def num_circle(s, x, y, d, label, fill=BLUE_M, fs=12, color=WHITE):
    """圆形编号徽标"""
    oval(s, x, y, d, d, fill=fill)
    return txt(s, x, y, d, d, label, fs=fs, color=color, bold=True, align=1)


def grad_bar(s, img_name, x, y, w, h, text, fs=15, color=WHITE, assets_dir=None):
    """渐变横幅图 + 居中白字（比纯色矩形更有层次）"""
    pic(s, img_name, x, y, w, h, fit=False, assets_dir=assets_dir)
    return txt(s, x, y, w, h, text, fs=fs, color=color, bold=True, align=1)


def gray_box(s, x, y, w, h, rows, fs=14, numbered=True, fill=GRAY_BG):
    """浅灰说明框；rows = [[(文字,色,粗), ...], ...] 一行一个"""
    rect(s, x, y, w, h, fill=fill, line=(210, 217, 226), lw=0.9)
    outs = []
    rh = h / max(1, len(rows))
    for i, parts in enumerate(rows):
        ry = y + i * rh
        if numbered:
            num_circle(s, x + 14, ry + rh / 2 - 11, 22, str(i + 1), fill=(70, 122, 190), fs=12)
            txt(s, x + 44, ry + rh / 2 - 9, 18, 18, "\u25b6", fs=11, color=(60, 112, 182), align=0)
            outs.append(rich(s, x + 66, ry + 4, w - 82, rh - 8, parts, fs=fs, align=0))
        else:
            outs.append(rich(s, x + 18, ry + 4, w - 30, rh - 8, parts, fs=fs, align=0))
    return outs


def pill(s, x, y, w, h, text, fs=12.5, fill=RED, color=WHITE, rounded=True):
    """胶囊标签"""
    (rrect if rounded else rect)(s, x, y, w, h, fill=fill, line=None)
    return txt(s, x, y, w, h, text, fs=fs, color=color, bold=True, align=1)


def chip(s, x, y, w, h, parts, fs=12.5, fill=(249, 250, 252), line=(206, 214, 224)):
    """浅色圆角小卡片"""
    rrect(s, x, y, w, h, fill=fill, line=line, lw=0.9)
    return rich(s, x + 8, y + 2, w - 16, h - 4, parts, fs=fs, align=1)


def header(s, sec, title, logo="像素答辩", width=960,
           fs=25, color=BLUE, line_color=(96, 148, 210), assets_dir=None):
    """页面顶部章节标题栏：左竖条 + 「1.1 章节名」+ 右上 logo + 分隔线"""
    pic(s, "accent_bar.png", 18, 12, 7, 30, assets_dir=assets_dir)
    rich(s, 32, 10, width - 330, 34,
         [(sec + "  ", color, True), (title, color, True)], fs=fs, align=0)
    rrect(s, width - 88, 14, 22, 22, fill=BLUE_M, line=None)
    txt(s, width - 88, 14, 22, 22, "P", fs=13, color=WHITE, bold=True, align=1)
    txt(s, width - 62, 14, 62, 22, logo, fs=14, color=BLUE_M, bold=True, align=0)
    hline(s, 18, 48, width - 36, line_color, 2.0)
    hline(s, 18, 51, 160, BLUE_M, 2.5)


def table_simple(s, x, y, w, cols, header_row, rows,
                 hdr_h=32, row_h=66, header_fill=(32, 84, 160),
                 hdr_fs=14, cell_fs=11, alt_fill=(238, 244, 252),
                 left_bold_color=BLUE):
    """用矩形拼的简易表格（WPS AddTable 的边框 API 不稳定，这样更可靠）。

    cols        : 各列宽（pt）
    header_row  : [str, ...]
    rows        : [[第0列文本, [(文本,色,粗), ...]], ...]
    """
    rect(s, x, y, w, hdr_h, fill=header_fill)
    cx = x
    for i, t in enumerate(header_row):
        txt(s, cx, y, cols[i], hdr_h, t, fs=hdr_fs, color=WHITE, bold=True, align=1)
        cx += cols[i]
    ry = y + hdr_h
    for i, (cap, body) in enumerate(rows):
        rect(s, x, ry, w, row_h, fill=alt_fill if i % 2 == 0 else WHITE)
        hline(s, x, ry, w, (196, 208, 224), 0.9)
        txt(s, x + 10, ry, cols[0], row_h, cap, fs=12, color=left_bold_color, bold=True, align=1)
        rich(s, x + cols[0] + 10, ry + 5, cols[1] - 20, row_h - 10, body, fs=cell_fs, align=0)
        ry += row_h
    hline(s, x, ry, w, (196, 208, 224), 0.9)
