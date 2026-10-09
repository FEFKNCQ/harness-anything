# -*- coding: utf-8 -*-
"""pptengine —— 基于 WPS COM 的数据驱动 PPT 生成引擎（Windows）

用法：
    from pptengine import Deck, el
    from pptengine.assets import ensure_default_assets

    ensure_default_assets()              # 首次运行生成素材
    deck = Deck(bg="assets/bg_page.png")
    s = deck.add_slide()
    el.header(s, "1.1", "国家重大需求")
    el.rich(s, 16, 60, 928, 32, [("引导句", el.RED, True)], fs=19, align=1)
    deck.save("out/demo.pptx")

特点：
- 全部路径基于包位置/当前目录推导，无机器相关绝对路径
- 颜色统一 (R,G,B)；字号/坐标单位 pt；画布默认 960x540
- 生成过程 WPS 可见，跑完默认不退出，便于人工查看
"""
from __future__ import annotations

from .wps import Deck, connect_wps, WPSConnectionError
from . import elements as el
from . import paths
from . import verify
from .assets import ensure_default_assets

__all__ = [
    "Deck", "connect_wps", "WPSConnectionError",
    "el", "elements", "paths", "verify", "ensure_default_assets",
]
from . import elements  # noqa: E402
