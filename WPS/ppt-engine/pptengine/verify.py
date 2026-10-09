# -*- coding: utf-8 -*-
"""落盘校验：用 PyMuPDF 渲染 PDF，检查文本块是否溢出画布 / 是否重叠。

依赖 fitz（PyMuPDF）。未安装时 verify_pdf 返回 None 并提示，不影响生成流程。
"""
from __future__ import annotations


def _iter_spans(page):
    for b in page.get_text("dict")["blocks"]:
        if b.get("type") != 0:
            continue
        for l in b.get("lines", []):
            for sp in l.get("spans", []):
                t = (sp.get("text") or "").strip()
                if t:
                    yield t, sp["bbox"]


def verify_pdf(pdf_path, width=960.0, height=540.0, tol=1.0, verbose=True):
    """返回 (溢出条数, [(页码, bbox, 文本), ...])"""
    try:
        import fitz
    except ImportError:
        print("[verify] 未安装 PyMuPDF（pip install pymupdf），跳过校验")
        return None, []

    doc = fitz.open(str(pdf_path))
    bad = []
    for pi, pg in enumerate(doc, 1):
        W = pg.rect.width or width
        H = pg.rect.height or height
        for t, (x0, y0, x1, y1) in _iter_spans(pg):
            if x0 < -tol or y0 < -tol or x1 > W + tol or y1 > H + tol:
                bad.append((pi, (x0, y0, x1, y1), t))
                if verbose:
                    print(f"  p{pi} 溢出 [{x0:.0f},{y0:.0f},{x1:.0f},{y1:.0f}] {t[:24]}")
    if verbose:
        print(f"[verify] 页数={doc.page_count} 溢出={len(bad)}")
    return len(bad), bad


def render_pages(pdf_path, out_dir, dpi=110):
    """把 PDF 逐页渲染成 PNG，便于人工目检"""
    import fitz
    from pathlib import Path
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(str(pdf_path))
    files = []
    for i, pg in enumerate(doc, 1):
        f = out / f"p{i:02d}.png"
        pg.get_pixmap(dpi=dpi).save(str(f))
        files.append(str(f))
    return files
