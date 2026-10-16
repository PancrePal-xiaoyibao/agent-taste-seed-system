# 🖼️ demos — 十二风格样本墙（实时渲染）

这里是「美学大脑」的**可视化证据**：12 张真实浏览器渲染出来的完整页面，每张都代表一粒风格基因。

- 打开 [`index.html`](index.html) 看样本墙（含每张的风格说明）
- 点任意一张图 → 打开它的**可交互原始页面**
- 想自己重跑 → 见下方「复现」

> ⚠️ **在 GitHub 网页上看 `index.html` 只会看到源码**——GitHub 不渲染 HTML。
> 三种看法：① 直接看 [`_assets/shots/`](_assets/shots/) 里的高清截图；
> ② 把仓库 clone 下来，`python3 -m http.server 8000 --directory demos` 后访问 `http://127.0.0.1:8000/`；
> ③ 用 raw.githack.com / htmlpreview 之类的 GitHub HTML 预览服务打开 `index.html`。

---

## 十二张作品

| # | 风格基因（主 + 辅） | 情绪定位 | 场景 | 页面 | 高清截图 |
|---|---|---|---|---|---|
| 01 | 赛博霓虹 + 机器美学 | 科技酷感 | 暗色仪表盘 / 科技产品页 | [html](01-赛博霓虹.html) | [webp](_assets/shots/01-cyber-neon.webp) |
| 02 | 瑞士平面 + 蒙德里安网格 | 清晰理性 | 数据报告 / B 端信息页 | [html](02-瑞士平面.html) | [webp](_assets/shots/02-swiss-international.webp) |
| 03 | 中国画留白 + 计白当黑 | 东方古韵 | 文化产品页（茶） | [html](03-中国画留白.html) | [webp](_assets/shots/03-cixuan-chinese-whitespace.webp) |
| 04 | 吉卜力手绘 + 水彩淡彩 | 梦幻治愈 | 亲子教育 / 疗愈系 | [html](04-吉卜力手绘.html) | [webp](_assets/shots/04-ghibli-handdrawn.webp) |
| 05 | 浮世绘扁平 + 手作不规则边 | 东方古韵 | 展览专题 / 和风创意页 | [html](05-浮世绘扁平.html) | [webp](_assets/shots/05-ukiyoe-flat.webp) |
| 06 | 巴洛克聚光 + 金色细线 | 暗黑崇高 | 演出海报 / 人物故事页 | [html](06-巴洛克聚光.html) | [webp](_assets/shots/06-baroque-tenebrism.webp) |
| 07 | 洛可可粉彩 + 美人绘的柔 | 甜美容爱 | 甜品花店 / 少女向 | [html](07-洛可可粉彩.html) | [webp](_assets/shots/07-rococo-pastel.webp) |
| 08 | 极简主义 + Kelly 单色面 | 清晰理性 | 作品集 / 高端产品 hero | [html](08-极简主义.html) | [webp](_assets/shots/08-minimalism-gallery.webp) |
| 09 | 波普拼贴 + 沃霍尔复制 | 荒诞幽默 | 潮流品牌 / 传播图 | [html](09-波普拼贴.html) | [webp](_assets/shots/09-pop-collage.webp) |
| 10 | 构成主义海报 + 照片拼贴 | 热血冲击 | 活动 KV / 招募宣言 | [html](10-构成主义海报.html) | [webp](_assets/shots/10-constructivism-poster.webp) |
| 11 | 赛璐璐动漫 UI + 斜切动势 | 热血冲击 | 二次元产品 / 角色主站 | [html](11-赛璐璐动漫UI.html) | [webp](_assets/shots/11-cel-shading-anime-ui.webp) |
| 12 | 哥特暗黑 + 废墟崇高 | 暗黑崇高 | 恐怖悬疑游戏 / 史诗长图 | [html](12-哥特暗黑.html) | [webp](_assets/shots/12-gothic-dark.webp) |

每个 HTML 文件顶部都有一段注释，写明**选自哪粒种子、用了哪些激活词、守了哪几条纪律**。

## 为什么每张都不一样，而不是"换了配色"

每张都走完整决策链（见 [`../TASTE.md`](../TASTE.md)）：

1. **情绪定位** —— 读者该感受到什么（一个词）
2. **选基因** —— 从 `references/moods/` 对应情绪档选 **1 主 + 1 辅**
3. **基因翻译** —— 五基因位（色彩 / 光线 / 笔触 / 构图 / 情绪）→ CSS 变量
4. **一句话自检** —— 这张作品的风格基因是什么
5. **记档** —— 结果写回 `references/art-seeds.md` 末尾风味日志

## 两道自动闸门（审美纪律可判定）

```bash
python3 _src/qa_layout.py    # 布局：溢出 / 越界 / 遮挡 / 字号 / WCAG 对比度
python3 _src/qa_style.py     # 风格：亮度 / 暗部 / 留白 / 色相 / 饱和度
```

`qa_style.py` 把每粒基因卡的硬纪律变成断言。例如：

| 页面 | 断言 | 依据 |
|---|---|---|
| 03 中国画留白 | 留白 ≥62%、色彩像素 ≤6%、色相 ≤3 | 绢色+墨+朱砂，气口必须占大头 |
| 06 巴洛克聚光 | 暗部 ≥45%、亮部 ≤12%、金色只做线 | Tenebrism 只有一个光源 |
| 08 极简主义 | 留白 ≥46%、色相 ≤2 | 留白与克制是普适高级感 |
| 12 哥特暗黑 | 暗部 ≥58%、色相 ≤3 | 铅与烬的物质感，不用正黑 |

当前状态：**13 页布局检查（溢出/越界/遮挡/字号/对比度）0 问题 · 12 张图共 34 条基因纪律断言全部通过**。

## 复现（约 40 秒）

```bash
# 1. 字体子集化：从源字体裁出页面真正用到的字形 → _assets/fonts/*.woff2
#    （仓库不带 42MB 源字体，只带约 2MB 子集；断网也能渲染出同样的图）
python3 _src/build_fonts.py

# 2. 逐张实时渲染：真实 Chromium、2× 设备像素比、无损 WebP
python3 _src/render_shots.py

# 3. 质检
python3 _src/qa_layout.py
python3 _src/qa_style.py
```

依赖：`playwright`（含 Chromium）· `fonttools` + `brotli` · `Pillow`。
`_src/build_fonts.py` 默认从 `~/.cache/taste-seed-fonts/` 读源字体（该目录内有 `SOURCES.txt` 记明每支字体的获取方式），可用 `SOURCE_DIR=` 覆盖；源字体共约 42MB，**不进仓库**。

渲染环境：headless Chromium 143，`--force-color-profile=srgb`，`--font-render-hinting=none`。
截图尺寸 **2880 × 1800**（1440 × 900 逻辑画布 × 2 倍像素比）；长页面用 `data-canvas="宽度xfull"`。

## 字体许可

`_assets/fonts/` 内的 woff2 均为**开源字体的子集**，随仓库分发：

| 字体 | 许可 | 用途 |
|---|---|---|
| Noto Serif SC / Noto Sans SC | SIL OFL 1.1 | 中文正文与标题（本机无中文衬线，必须随包） |
| Playfair Display · Cormorant Garamond · EB Garamond · Libre Baskerville · Cinzel · Marcellus · Italiana · Yeseva One | SIL OFL 1.1 | 巴洛克/洛可可/哥特的衬线气质 |
| Archivo Black · Bebas Neue · Oswald · Inter | SIL OFL 1.1 | 瑞士平面 / 构成主义 / 波普的无衬线骨架 |
| JetBrains Mono | Apache License 2.0 | 数据与代码的等宽字 |

子集化只保留演示页实际出现的字形；完整字体请从各自上游获取。

## 架构说明（这个目录不是种子库的一部分）

```
demos/
├── index.html              样本墙（展示页，不产截图）
├── 01..12-*.html           十二张作品
├── _assets/
│   ├── taste-fonts.css     由 build_fonts.py 生成
│   ├── fonts/*.woff2       字体子集（开源字体，随仓库分发）
│   └── shots/*.webp        高清截图（README 与样本墙使用）
└── _src/
    ├── build_fonts.py      字体子集化
    ├── render_shots.py     实时渲染截图
    ├── qa_layout.py        布局质检
    └── qa_style.py         风格基因纪律校验
```

`demos/` 只依赖仓库根目录的 `references/` 做风格决策，**不修改种子库本体**；
各 agent 的部署脚本（`deploy/`）只搬运 `references/` 与 `TASTE.md`，因此新增本目录不影响任何已部署实例。
