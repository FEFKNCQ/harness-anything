# -*- coding: utf-8 -*-
"""示例：生成一个 2 页演示，演示引擎全部常用元素。

运行（在本目录下）：
    pip install -r ../requirements.txt
    python build_demo.py                 # 输出到 ./out/demo.pptx
    python build_demo.py --out D:/tmp    # 指定输出目录
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# 让示例可直接以脚本方式运行（无需 pip install）
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pptengine import Deck, el, verify                      # noqa: E402
from pptengine.assets import ensure_default_assets          # noqa: E402


def page1(deck):
    s = deck.add_slide()
    el.header(s, "1.1", "国家重大需求")
    el.rich(s, 16, 60, 928, 32,
            [("消化道恶性肿瘤疾病负担持续加重，", el.RED, True),
             ("治疗抵抗已成为肿瘤医学前沿重大科学命题", el.RED, True)], fs=19, align=1)
    el.gray_box(s, 16, 96, 928, 82, [
        [("肿瘤代谢重编程与免疫微环境之间存在复杂双向调控，其驱动恶性演进的因果链条尚未阐明", el.INK, False)],
        [("决定免疫细胞耗竭、肿瘤克隆选择及治疗抵抗的关键代谢节点尚缺乏系统解析", el.INK, False)],
    ])
    el.grad_bar(s, "bar_blue.png", 16, 186, 300, 32, "高发高致死疾病负担")
    el.grad_bar(s, "bar_teal.png", 330, 186, 290, 32, "免疫治疗获益受限")
    el.grad_bar(s, "bar_dark.png", 634, 186, 310, 32, "肿瘤异质性与演进")
    el.rich(s, 22, 226, 288, 78,
            [("2020年全球肿瘤死亡病例近1千万人\n中国占30.2%死亡率", el.RED, True)], fs=15, align=1)
    el.pic(s, "fig_heat.png", 30, 308, 272, 86)
    el.pill(s, 286, 236, 54, 26, "治疗抵抗", fs=12)
    el.pic(s, "fig_paper.png", 344, 226, 262, 172)
    el.pill(s, 590, 236, 54, 26, "内在根源", fs=12)
    el.pic(s, "fig_web.png", 648, 226, 282, 172)
    el.rich(s, 16, 424, 928, 28,
            [("面向肿瘤精准防治重大需求，揭示", el.INK, True),
             ("“代谢重塑—免疫逃逸—恶性演进”", el.RED, True),
             ("核心机制", el.INK, True)], fs=17, align=1)
    for i, (num, cap) in enumerate([("01", "国自然科学基金重点"),
                                    ("02", "国重点研发计划"),
                                    ("03", "山东省自然科学基金")]):
        x = 38 + i * 312
        el.num_circle(s, x, 460, 34, num, fs=13)
        el.rrect(s, x + 42, 460, 250, 34, fill=el.BLUE_L, line=(150, 182, 220), lw=0.9)
        el.txt(s, x + 42, 460, 250, 34, cap, fs=14, color=el.BLUE, bold=True, align=1)
    return s


def page2(deck):
    s = deck.add_slide()
    el.header(s, "3.4", "研究国际应用成果")
    el.rich(s, 16, 58, 928, 56,
            [("相关研究围绕肿瘤免疫代谢与恶性演进形成系统性原创成果，为国际同行理解代谢重编程介\n导免疫逃逸提供新的机制框架", el.INK, True)],
            fs=15, align=0)
    el.table_simple(
        s, 16, 122, 552, cols=[140, 412],
        header_row=["成果方向", "学术影响"],
        rows=[
            ("肿瘤免疫\n代谢图谱", [("建立单细胞与空间免疫代谢图谱，为解析", el.INK, False),
                                    ("肿瘤异质性和免疫治疗耐受", el.RED, True), ("提供研究基础", el.INK, False)]),
            ("免疫逃逸\n调控网络", [("构建", el.INK, False), ("“代谢重编—免疫耗竭—肿瘤演进”", el.RED, True),
                                    ("因果模型，提供新的理论框架", el.INK, False)]),
            ("多模型因果\n验证体系", [("建立临床样本、空间组学、类器官及人源化模型相互印证的机制研究范式", el.INK, False)]),
        ],
        hdr_h=32, row_h=78,
    )
    el.pic(s, "fig_web.png", 580, 122, 180, 210)
    el.pic(s, "fig_heat.png", 768, 122, 184, 210)
    el.rect(s, 580, 340, 180, 106, fill=(253, 250, 250), line=(214, 176, 176), lw=1.1)
    el.rich(s, 590, 348, 160, 90,
            [("该研究从代谢通讯角度\n深化了对肿瘤免疫逃逸\n机制的认识", el.RED, True)], fs=12.5, align=0)
    el.rrect(s, 16, 464, 928, 40, fill=el.RED, line=None)
    el.rich(s, 16, 464, 928, 40,
            [("形成", el.WHITE, True),
             ("“时空图谱发现—跨细胞代谢通讯—免疫耗竭机制—关键靶点干预”", el.WHITE, True),
             ("的系统性原创理论链条", el.WHITE, True)], fs=15, align=1)
    return s


def main():
    ap = argparse.ArgumentParser(description="pptengine 演示")
    ap.add_argument("--out", default=None, help="输出目录，默认 ./out")
    ap.add_argument("--assets", default=None, help="素材目录，默认 <包根>/assets")
    ap.add_argument("--no-visible", action="store_true", help="后台运行不显示 WPS 窗口")
    args = ap.parse_args()

    assets = ensure_default_assets(args.assets)
    bg = str(Path(assets) / "bg_page.png")

    deck = Deck(assets_dir=assets, bg=bg, visible=not args.no_visible)
    page1(deck)
    page2(deck)

    out_dir = Path(args.out).expanduser().resolve() if args.out else (Path.cwd() / "out")
    out_dir.mkdir(parents=True, exist_ok=True)
    pptx, pdf = deck.save(out_dir / "demo.pptx")
    if pdf:
        verify.verify_pdf(pdf)
    print("[done] 输出:", pptx)


if __name__ == "__main__":
    main()
