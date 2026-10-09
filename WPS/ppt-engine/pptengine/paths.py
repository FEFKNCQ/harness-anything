# -*- coding: utf-8 -*-
"""路径解析：全部基于本文件位置推导，不含任何机器相关的绝对路径。

约定：
- ENGINE_ROOT : 本包所在目录（pptengine/）
- PACKAGE_ROOT: 引擎项目根目录（pptengine/ 的上一级）
- 资源默认目录:  PACKAGE_ROOT/assets
- 输出默认目录:  当前工作目录/out

可通过环境变量或 Deck(assets_dir=...) / save(out_dir=...) 覆盖。
"""
from __future__ import annotations

import os
from pathlib import Path

ENGINE_ROOT = Path(__file__).resolve().parent
PACKAGE_ROOT = ENGINE_ROOT.parent

DEFAULT_ASSETS_DIR = PACKAGE_ROOT / "assets"
DEFAULT_OUT_DIR = Path.cwd() / "out"

ENV_ASSETS = "PPTENGINE_ASSETS_DIR"
ENV_OUT = "PPTENGINE_OUT_DIR"


def assets_dir() -> Path:
    """资源目录：环境变量 > 默认 <包根>/assets"""
    p = os.environ.get(ENV_ASSETS)
    return Path(p).expanduser().resolve() if p else DEFAULT_ASSETS_DIR


def out_dir() -> Path:
    """输出目录：环境变量 > 默认 <cwd>/out"""
    p = os.environ.get(ENV_OUT)
    return Path(p).expanduser().resolve() if p else DEFAULT_OUT_DIR


def ensure_dir(p) -> Path:
    p = Path(p).expanduser().resolve()
    p.mkdir(parents=True, exist_ok=True)
    return p


def asset(name: str, base=None) -> str:
    """按文件名取资源绝对路径（字符串，WPS COM 需要 str）"""
    base = Path(base) if base else assets_dir()
    return str(base / name)


def has_asset(name: str, base=None) -> bool:
    return os.path.exists(asset(name, base))
