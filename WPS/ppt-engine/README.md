# WPS/PPT 数据驱动生成引擎（pptengine）

用 **WPS 演示 COM 接口**在 Windows 上批量生成 PPT。代码里**没有任何机器相关的绝对路径**，克隆下来即可运行。

## 特性

| 特性 | 说明 |
|---|---|
| 路径无关 | 全部基于 `Path(__file__)` / 当前工作目录推导，可用环境变量覆盖 |
| 数据驱动 | 页面由 Python 数据或 JSON 描述，换内容不改引擎 |
| 素材自生成 | 渐变横幅、箭头、圆环、背景、科研示意图全部 PIL 程序化绘制，不依赖外部图床 |
| 可见生成 | WPS 窗口可见、逐页跳转，跑完默认不退出，便于人工查看 |
| 落盘校验 | 用 PyMuPDF 检查文本是否溢出画布 |

## 环境要求

- Windows + 已安装 **WPS Office**（COM ProgID `KWPP.Application`）
- Python 3.9+

```bash
pip install -r requirements.txt
```

## 快速开始

```bash
cd examples
python build_demo.py              # 输出 ./out/demo.pptx（含 PDF）
python build_from_json.py         # 用 slides.json 驱动，输出 ./out/from_json.pptx

python build_demo.py --out D:/tmp/myppt      # 指定输出目录
python build_demo.py --no-visible            # 后台生成，不弹 WPS 窗口
```

## 代码方式

```python
from pptengine import Deck, el
from pptengine.assets import ensure_default_assets

assets = ensure_default_assets()                  # 首次运行生成素材
deck = Deck(bg=str(assets / "bg_page.png"))       # 画布 960x540

s = deck.add_slide()
el.header(s, "1.1", "国家重大需求")               # 顶部章节标题栏
el.rich(s, 16, 60, 928, 32,
        [("引导句前半，", el.RED, True), ("后半句", el.INK, True)],
        fs=19, align=1)
el.grad_bar(s, "bar_blue.png", 16, 186, 300, 32, "栏目名")
el.pic(s, "fig_heat.png", 30, 226, 272, 120)
el.pill(s, 286, 236, 54, 26, "标签")
el.gray_box(s, 16, 96, 928, 82, [[("说明文字", el.INK, False)]])

deck.save("out/demo.pptx")                        # 同时导出 PDF
```

## 元素一览（`pptengine/elements.py`）

- **文字**：`txt`（单色）、`rich`（分段着色）
- **形状**：`rect` / `rrect` / `oval` / `arrow` / `hline` / `shape`
- **图片**：`pic`（按文件名，自动等比 fit 防溢出）
- **组合**：`header`（页面标题栏）、`grad_bar`（渐变横幅）、`gray_box`（编号说明框）、
  `pill`（胶囊标签）、`chip`（浅色卡片）、`num_circle`（圆形编号）、`table_simple`（表格）

## JSON 方式（换内容零改码）

`examples/slides.json` 描述页面，元素通过 `type` 路由：

```json
{ "type": "grad_bar", "box": [16, 186, 300, 32],
  "img": "bar_blue.png", "text": "栏目名" }
```

新增自定义元素：在 `build_from_json.py` 里加一个 `@route("你的类型")` 函数即可。

## 目录结构

```
ppt-engine/
├── pptengine/
│   ├── __init__.py      # 统一出口
│   ├── paths.py         # 路径解析（无绝对路径）
│   ├── wps.py           # COM 连接 + Deck
│   ├── elements.py      # 绘图原语与组合组件
│   ├── assets.py        # PIL 素材生成
│   └── verify.py        # PDF 溢出校验 / 渲染
├── examples/
│   ├── build_demo.py        # 代码驱动示例（2 页）
│   ├── build_from_json.py   # JSON 驱动示例
│   └── slides.json
├── assets/              # 运行时生成的图片
└── requirements.txt
```

## 环境变量

| 变量 | 作用 | 默认 |
|---|---|---|
| `PPTENGINE_ASSETS_DIR` | 素材目录 | `<包根>/assets` |
| `PPTENGINE_OUT_DIR` | 输出目录 | `<cwd>/out` |

## 已知坑（引擎已内置规避）

1. `Sp.Adjustments.Item(1) = x` 是 Python 语法错误，须写 `sp.Adjustments[1] = x`
2. `Bold` 只在 `True` 时赋值；赋 `False` 部分 WPS 版本会抛异常
3. `WordWrap=False` 与居中/右对齐同用会让文字跑出页面，引擎恒设 `True`
4. 多行 + 垂直居中在 WPS 会算错，引擎改顶对齐 + 手动下移
5. `AddTable` 的单元格边框 API 不稳定，表格改用矩形拼接
6. 生成前需 `taskkill` 释放 WPS 锁，否则 `SaveAs` 可能静默失败
7. 中文字体固定 `微软雅黑`，避免渲染成方块

## License

与本仓库保持一致。
