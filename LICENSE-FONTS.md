# 字体许可 / Font Licensing

`demos/_assets/fonts/*.woff2` 是**开源字体的子集（subset）**，随本仓库分发以
保证演示页与截图**离线可复现**。这些文件**不是**本项目原创资产，
其权利归各自上游作者，本项目仅做字形裁剪与重命名。

> **一句话**：上表所有源字体均为 SIL OFL 1.1（另见下方说明），
> 允许嵌入、修改与再分发；我们已按 OFL 要求**改名**，并在此完整列明来源与许可。

---

## 字体清单

| 输出文件（子集） | 上游字体 | 许可 | 版权与保留字体名 |
|---|---|---|---|
| `NotoSansSC-*.woff2` | Noto Sans SC | SIL OFL 1.1 | © 2014-2021 Adobe；保留字体名 `Source`（另有 Google 参与） |
| `NotoSerifSC-*.woff2` | Noto Serif SC | SIL OFL 1.1 | © 2017-2024 Adobe |
| `PlayfairDisplay-*.woff2` | Playfair Display | SIL OFL 1.1 | © 2017 The Playfair Display Project Authors；保留字体名 `Playfair Display` |
| `Cinzel-*.woff2` | Cinzel | SIL OFL 1.1 | © The Cinzel Project Authors |
| `CormorantGaramond-*.woff2` | Cormorant Garamond | SIL OFL 1.1 | © The Cormorant Project Authors |
| `EBGaramond-*.woff2` | EB Garamond | SIL OFL 1.1 | © The EB Garamond Project Authors |
| `LibreBaskerville-*.woff2` | Libre Baskerville | SIL OFL 1.1 | © 2012 Impallari Type |
| `Marcellus-*.woff2` | Marcellus | SIL OFL 1.1 | © 2012 Brian J. Bonislawsky DBA Astigmatic；保留字体名 `Marcellus` |
| `Italiana-*.woff2` | Italiana | SIL OFL 1.1 | © 2011 Brian J. Bonislawsky DBA Astigmatic |
| `YesevaOne-*.woff2` | Yeseva One | SIL OFL 1.1 | © 2012 The Yeseva One Project Authors；保留字体名 `Yeseva` |
| `ArchivoBlack-*.woff2` | Archivo Black | SIL OFL 1.1 | © 2017 The Archivo Black Project Authors（Omnibus-Type） |
| `BebasNeue-*.woff2` | Bebas Neue | SIL OFL 1.1 | © 2019 The Bebas Neue Project Authors（Dharma Type） |
| `Oswald-*.woff2` | Oswald | SIL OFL 1.1 | © 2016 The Oswald Project Authors |
| `Inter-*.woff2` | Inter | SIL OFL 1.1 | © The Inter Project Authors |
| `JetBrainsMono-*.woff2` | JetBrains Mono | SIL OFL 1.1 | © 2020 The JetBrains Mono Project Authors |

> 表中信息由 `fontTools` 直接读取各源字体 `name` 表（nameID 0/13/14）得出，
> 可用以下命令复核：`python3 demos/_src/check_font_licenses.py`

---

## OFL 1.1 的合规要点与本项目的处置

SIL Open Font License 1.1 允许自由使用、研究、修改与再分发（含嵌入文档与网页、含商业用途），
但有三条与本仓库直接相关的约束：

### 1. 保留字体名（Reserved Font Name, RFN）—— OFL §3

OFL 规定：**修改版不得使用保留字体名**。子集是 OFL 意义上的 Modified Version。

本项目实测（`name` 表 nameID 0）有以下字体声明了 RFN：

```
Noto Sans SC        -> Reserved Font Name 'Source'
Playfair Display    -> Reserved Font Name "Playfair Display"
Yeseva One          -> Reserved Font Name "Yeseva"
Marcellus           -> Reserved Font Name "Marcellus"
```

**处置**：`demos/_src/build_fonts.py` 对所有子集**统一重命名**，
家族名加 `AB ` 前缀（`AB Noto Serif SC`、`AB Playfair Display` …），
并同步改写 name 表 nameID 1/2/3/4/6/16/17。
一条规则覆盖全部字体，不需要记忆「哪支有 RFN / 哪支没有」。

**未声明 RFN 的字体虽然可以沿用原名，本项目同样改名** —— 子集顶着原名会误导使用者。

### 2. 版权与许可声明必须保留 —— OFL §1

**处置**：重命名时**刻意不动** nameID 0（版权）与 nameID 13/14（许可与许可链接），
因此每个 woff2 子集内部仍完整携带上游版权声明与 OFL 链接。

### 3. 字体不得单独售卖 —— OFL §5

**处置**：字体子集仅作为本仓库演示页的**组成部分**分发，
不与任何形式的字体售卖捆绑，不构成「单独销售字体」。

---

## 第三方字体的原始许可文本

各字体的 OFL 1.1 原文（标准文本，各字体相同，仅版权行不同）：

- SIL OFL 1.1 全文：<https://openfontlicense.org/open-font-license-official-text/>
- 中文参考译文：<https://openfontlicense.org/open-font-license-official-text/zh/>

上游项目地址（获取完整字体、报告问题、查看完整版权文件）：

| 字体 | 上游 |
|---|---|
| Noto Sans SC / Noto Serif SC | <https://github.com/notofonts/noto-cjk> |
| Playfair Display | <https://github.com/clauseggers/Playfair-Display> |
| Cinzel | <https://github.com/natanaelgama/Cinzel> |
| Cormorant Garamond | <https://github.com/CatharsisFonts/Cormorant> |
| EB Garamond | <https://github.com/octaviopardo/EBGaramond12> |
| Libre Baskerville | <https://github.com/impallari/Libre-Baskerville> |
| Marcellus / Italiana | <https://github.com/astigmatic/marcellus-font> |
| Yeseva One | <https://github.com/lemonad/yeseva> |
| Archivo Black | <https://github.com/Omnibus-Type/ArchivoBlack> |
| Bebas Neue | <https://github.com/dharmatype/Bebas-Neue> |
| Oswald | <https://github.com/googlefonts/OswaldFont> |
| Inter | <https://github.com/rsms/inter> |
| JetBrains Mono | <https://github.com/JetBrains/JetBrainsMono> |

---

## 为什么必须内置中文字体

本项目的三个风格基因（**中国画留白 / 哥特暗黑 / 巴洛克聚光**）依赖**中文衬线体**。
而常见 Linux 服务器上 `fc-match "Noto Serif SC"` 会回落到无衬线的
DejaVu Sans / 文泉驿正黑 —— 中文衬线**并不存在**，渲染结果会静默退化成黑体，
风格基因随之失效。

因此本仓库选择**内置字体子集**（30 个字重、约 2 MB），把「渲染结果可复现」
变成硬保证：任何人 clone 后断网也能得到与仓库截图逐像素一致的结果。

子集只保留演示页实际出现的字形（由 `scan_charset()` 扫描 HTML 文本得出），
因此体积远小于完整字体；原始 42 MB 源字体不随仓库分发。

---

## 重新生成子集

```bash
# 源字体需自行获取（见 LICENSE-FONTS.md 上方上游地址表）
# 默认读取 ~/.cache/taste-seed-fonts/，也可用 SOURCE_DIR= 指定
python3 demos/_src/build_fonts.py
```

脚本会自动完成：字形裁剪 → 重命名（加 `AB ` 前缀）→ 保留版权与许可记录 → 生成 CSS。

---

*本文件是合规说明，不构成法律意见。若你要在自己的项目里复用这些字体子集，
请直接遵循上游字体的 OFL 条款（本文件可作为来源与合规路径的参考）。*
