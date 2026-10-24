#!/usr/bin/env python3
"""
组装仓库根 `LICENSE` —— 把三份官方许可正文与适用范围说明合并为单一权威文件。

## 为什么要用脚本而不是手写

`LICENSE` 里包含三份**官方许可全文**（MIT / CC BY 4.0 / SIL OFL 1.1），
共约 4 万字节。手写会带来两个问题：

  1. 复制粘贴极易出现缺行、错字——而许可正文**错一个字都是法律风险**；
  2. 日后更新许可版本时，没人能确认到底改了什么。

所以：官方正文原文放在 `scripts/license-sources/`（登记来源与抓取日期），
本脚本负责拼装。改动只需动素材或本节文字，重跑即可。

## 用法

    python3 scripts/build_license.py           # 重新生成仓库根 LICENSE
    python3 scripts/build_license.py --check   # 只校验当前 LICENSE 是否与素材同步

退出码：0 = 一致/生成成功；1 = --check 模式下发现不同步
"""

import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "scripts" / "license-sources"
OUT = ROOT / "LICENSE"

YEAR = "2026"
HOLDER = "hhx465453939"
PROJECT = "美学大脑 / aesthetic-brain"
REPO = "https://github.com/hhx465453939/agent-taste-seed-system"

RULE = "─" * 78
BAR = "=" * 78


def read_source(name: str) -> str:
    p = SRC / name
    if not p.is_file():
        sys.exit(f"❌ 缺少许可素材：{p}")
    return p.read_text(encoding="utf-8").rstrip()


def dispw(s: str) -> int:
    """显示宽度：CJK 与全角符号占 2 列。"""
    return sum(2 if ord(ch) > 0x2E80 else 1 for ch in s)


def build_font_table() -> str:
    """字体清单表（等宽对齐，供纯文本 LICENSE 阅读）。

    数据来自 demos/_src/check_font_licenses.py 可复核的 name 表读取结果。
    """
    rows = [
        ("NotoSansSC-*.woff2", "Noto Sans SC", "SIL OFL 1.1",
         "© 2014-2021 Adobe；保留字体名 Source（另有 Google 参与）"),
        ("NotoSerifSC-*.woff2", "Noto Serif SC", "SIL OFL 1.1", "© 2017-2024 Adobe"),
        ("PlayfairDisplay-*.woff2", "Playfair Display", "SIL OFL 1.1",
         "© 2017 The Playfair Display Project Authors；保留字体名 Playfair Display"),
        ("Cinzel-*.woff2", "Cinzel", "SIL OFL 1.1", "© The Cinzel Project Authors"),
        ("CormorantGaramond-*.woff2", "Cormorant Garamond", "SIL OFL 1.1",
         "© The Cormorant Project Authors"),
        ("EBGaramond-*.woff2", "EB Garamond", "SIL OFL 1.1",
         "© The EB Garamond Project Authors"),
        ("LibreBaskerville-*.woff2", "Libre Baskerville", "SIL OFL 1.1",
         "© 2012 Impallari Type"),
        ("Marcellus-*.woff2", "Marcellus", "SIL OFL 1.1",
         "© 2012 Brian J. Bonislawsky DBA Astigmatic；保留字体名 Marcellus"),
        ("Italiana-*.woff2", "Italiana", "SIL OFL 1.1",
         "© 2011 Brian J. Bonislawsky DBA Astigmatic"),
        ("YesevaOne-*.woff2", "Yeseva One", "SIL OFL 1.1",
         "© 2012 The Yeseva One Project Authors；保留字体名 Yeseva"),
        ("ArchivoBlack-*.woff2", "Archivo Black", "SIL OFL 1.1",
         "© 2017 The Archivo Black Project Authors（Omnibus-Type）"),
        ("BebasNeue-*.woff2", "Bebas Neue", "SIL OFL 1.1",
         "© 2019 The Bebas Neue Project Authors（Dharma Type）"),
        ("Oswald-*.woff2", "Oswald", "SIL OFL 1.1",
         "© 2016 The Oswald Project Authors"),
        ("Inter-*.woff2", "Inter", "SIL OFL 1.1", "© The Inter Project Authors"),
        ("JetBrainsMono-*.woff2", "JetBrains Mono", "Apache-2.0",
         "© 2020 The JetBrains Mono Project Authors"),
    ]
    header = ("输出文件（子集）", "上游字体", "上游许可", "版权与保留字体名")
    allrows = [header] + rows
    widths = [max(dispw(r[i]) for r in allrows) for i in range(4)]
    lines = []
    for r in allrows:
        cells = [c + " " * (widths[i] - dispw(c) + 2) for i, c in enumerate(r)]
        lines.append("  " + "".join(cells).rstrip())
    return "\n".join(lines)


def build_ofl_notes() -> str:
    return """  SIL Open Font License 1.1 允许自由使用、研究、修改与再分发（含嵌入文档与网页、
  含商业用途），但有三条与本仓库直接相关的约束：

  ── 1. 保留字体名（Reserved Font Name, RFN）—— OFL §3 ──

    OFL 规定：修改版不得使用保留字体名。子集是 OFL 意义上的 Modified Version。

    本项目实测（各源字体 name 表 nameID 0）有以下字体声明了 RFN：

        Noto Sans SC        → Reserved Font Name 'Source'
        Playfair Display    → Reserved Font Name "Playfair Display"
        Yeseva One          → Reserved Font Name "Yeseva"
        Marcellus           → Reserved Font Name "Marcellus"

    处置：`demos/_src/build_fonts.py` 对所有子集统一重命名，家族名加 `AB ` 前缀
    （AB Noto Serif SC、AB Playfair Display …），并同步改写 name 表
    nameID 1/2/3/4/6/16/17。一条规则覆盖全部字体，不需要记忆例外。

    未声明 RFN 的字体虽然可以沿用原名，本项目同样改名 —— 子集顶着原名会误导使用者。

  ── 2. 版权与许可声明必须保留 —— OFL §1 ──

    处置：重命名时刻意不动 nameID 0（版权）与 nameID 13/14（许可与许可链接），
    因此每个 woff2 子集内部仍完整携带上游版权声明与 OFL 链接。

  ── 3. 字体不得单独售卖 —— OFL §5 ──

    处置：字体子集仅作为本仓库演示页的组成部分分发，不与任何形式的字体售卖捆绑。

  上述三条已由 `demos/_src/check_font_licenses.py` 在 CI 中自动校验。"""


def build_font_upstream() -> str:
    rows = [
        ("Noto Sans SC / Noto Serif SC", "https://github.com/notofonts/noto-cjk"),
        ("Playfair Display", "https://github.com/clauseggers/Playfair-Display"),
        ("Cinzel", "https://github.com/natanaelgama/Cinzel"),
        ("Cormorant Garamond", "https://github.com/CatharsisFonts/Cormorant"),
        ("EB Garamond", "https://github.com/octaviopardo/EBGaramond12"),
        ("Libre Baskerville", "https://github.com/impallari/Libre-Baskerville"),
        ("Marcellus / Italiana", "https://github.com/astigmatic/marcellus-font"),
        ("Yeseva One", "https://github.com/lemonad/yeseva"),
        ("Archivo Black", "https://github.com/Omnibus-Type/ArchivoBlack"),
        ("Bebas Neue", "https://github.com/dharmatype/Bebas-Neue"),
        ("Oswald", "https://github.com/googlefonts/OswaldFont"),
        ("Inter", "https://github.com/rsms/inter"),
        ("JetBrains Mono", "https://github.com/JetBrains/JetBrainsMono"),
    ]
    w = max(dispw(r[0]) for r in rows)
    return "\n".join(f"  {n}{' ' * (w - dispw(n) + 3)}{u}" for n, u in rows)


def build_font_why() -> str:
    return """  本项目的三个风格基因（中国画留白 / 哥特暗黑 / 巴洛克聚光）依赖中文衬线体。
  而常见 Linux 服务器上 `fc-match "Noto Serif SC"` 会回落到无衬线的
  DejaVu Sans / 文泉驿正黑 —— 中文衬线并不存在，渲染结果会静默退化成黑体，
  风格基因随之失效。

  因此本仓库选择内置字体子集（30 个字重、约 2 MB），把「渲染结果可复现」
  变成硬保证：任何人 clone 后断网也能得到与仓库截图一致的结果。

  子集只保留演示页实际出现的字形（由页面上所有可见文本扫描得出），
  因此体积远小于完整字体；原始 42 MB 源字体不随仓库分发。"""


def render() -> str:
    cc = read_source("cc-by-4.0-legalcode.txt")
    ofl = read_source("ofl-1.1.txt")
    mit = read_source("mit.txt").replace("hhx465453939", HOLDER)

    return f"""{PROJECT} — 许可 (Licensing)
{BAR}

Copyright (c) {YEAR} {HOLDER}
SPDX-License-Identifier: MIT AND CC-BY-4.0 AND OFL-1.1

本项目按**资产类型**适用三种不同许可。本文件是唯一权威许可见证：
前三节是速览与适用范围，后三节是三份许可的**官方完整正文**（逐字未改）。


{RULE}
零 · 30 秒速览
{RULE}

  你的资产                          适用许可                     完整正文
  ---------------------------------------------------------------------------
  代码（脚本 / CI / 部署）           MIT                          §二
  内容（种子库 / 文档 / 截图）        CC BY 4.0                    §三
  字体子集（demos/_assets/fonts/）   SIL OFL 1.1 / Apache-2.0     §四

  一句话版：

    内容（种子库/文档/截图）：  CC BY 4.0         署名；可商用，无需附加限制
    代码（脚本/CI/部署）：      MIT               可商用，保留版权声明
    字体（woff2 子集）：        上游 OFL/Apache   随包可分发，已按 OFL 改名


{RULE}
一 · 适用范围（逐路径对照）
{RULE}

  §二 MIT —— 代码资产
      demos/_src/*.py        字体子集化 · 实时渲染 · 布局质检 · 风格校验 · 字体许可检查
      scripts/*.py           build_license · check_integrity · check_links ·
                             check_shots_freshness
      scripts/*.sh           check_assets
      deploy/*.sh            各 agent 形态的部署脚本
      .github/**             CI 工作流与配置

  §三 CC BY 4.0 —— 文本与视觉资产
      LICENSE（本文件） · CITATION.cff · CONTRIBUTING.md · .gitignore
      README*.md · CHANGELOG.md · SKILL.md · TASTE.md · AGENT-INJECTION.md
      AGENTS.md · CLAUDE.md
      docs/**                METHODOLOGY · ATTRIBUTION · TRADEMARKS · changes/**
      references/**          art-seeds.md · ART-SEEDS-LOG.md · code-genes/ · moods/ · chapters/
      deploy/*.md            部署文档
      demos/*.html           十二张演示页
      demos/README.md
      demos/_assets/taste-fonts.css
      demos/_assets/shots/** 演示截图

  §四 OFL 1.1 / Apache-2.0 —— 字体子集
      demos/_assets/fonts/*.woff2            （除 JetBrains Mono 外适用 OFL 1.1）
      demos/_assets/fonts/JetBrainsMono-*    （Apache-2.0）

  §五 例外 —— 许可正文自身
      scripts/license-sources/**             三份官方许可正文原文（供生成本文件）
      这些文本本身不受著作权保护，随本文件一并分发，不适用 §三。

  ── 边界规则（防止新增文件掉进缝里）──

  1. 默认规则：位于 demos/_src/、scripts/、deploy/、.github/ 下的
     .py / .sh / .yml 文件 → §二 MIT；其余一切文件 → §三 CC BY 4.0。
     本项由 scripts/check_integrity.py 自动守卫，新增文件无需手工登记。

  2. 一个文件里既有代码又有说明文字：以该文件的主要用途判定。
     脚本的主要用途是执行 → MIT；
     文档、种子卡、演示页的主要用途是传递文本表达 → CC BY 4.0。

  3. 字体文件例外：demos/_assets/fonts/** 的权利不属于本项目，归各自上游作者，
     适用其上游许可（见 §四）。本项目只做字形裁剪与重命名。


{RULE}
二 · MIT License（代码资产完整正文）
{RULE}

{mit}


{RULE}
三 · CC BY 4.0（内容资产）
{RULE}

  完整名称：Creative Commons Attribution 4.0 International
  中文名称：知识共享 署名 4.0 国际
  SPDX    ：CC-BY-4.0

  官方中文法律条款（权威文本的官方译本）：
      https://creativecommons.org/licenses/by/4.0/legalcode.zh-Hans
  人类可读摘要：
      https://creativecommons.org/licenses/by/4.0/

  ⚠️ 依 Creative Commons 官方立场，英文版为权威文本，中文版为官方译本。
     下方「三·附 官方完整法律条款」一节逐字收录英文全文，作为本仓库的权威依据。

  ── 你可以做什么 ──

    · 共享 —— 以任何媒介或格式复制、发行本作品
    · 演绎 —— 修改、转换、基于本作品进行创作
    · 任何目的，**包括商业目的** —— 本许可不含 NonCommercial 限制
    · 上述自由无需额外授权、无需付费

    许可方不能撤回这些自由，只要使用者遵守许可条款。

  ── 必须遵守的条件 ──

    署名 BY        必须给出适当署名，提供指向本许可的链接，并说明是否作了修改。
                   可以任何合理方式署名，但不得暗示许可方为你或你的使用背书。
    无附加限制     不得适用法律条款或技术措施，从而限制他人做本许可允许的事。

    完整条件以「三·附」的官方正文为准（CC BY 4.0 §2）。

  ── 补录内容怎么授权 ──

    CC BY 4.0 没有 ShareAlike：你补录进种子库的新内容可以用任何条款发布，
    包括专有条款；基于本仓库内容的演绎作品同样可以另行授权。
    前提是保留署名、许可链接与修改说明，并且不对他人的 CC BY 权利附加限制。

  ── 推荐署名格式（把尖括号内换成你的实际信息）──

      本作品使用了「{PROJECT}」（作者 {HOLDER}），
      依据 CC BY 4.0 许可使用。
      来源：{REPO}
      修改说明：<例如「仅使用 code-genes/02 赛博霓虹，未作修改」>

    机器可读格式见 CITATION.cff；更多模板见 docs/ATTRIBUTION.md。


{RULE}
三·附 · 官方完整法律条款（CC BY 4.0，英文权威文本，逐字未改）
{RULE}

{cc}


{RULE}
四 · SIL Open Font License 1.1（字体子集）
{RULE}

  demos/_assets/fonts/*.woff2 是开源字体的子集（subset），随本仓库分发
  以保证演示页与截图离线可复现。这些文件不是本项目原创资产，
  其权利归各自上游作者。本项目只做字形裁剪与重命名。

  JetBrains Mono 适用 Apache License 2.0，其余全部适用 SIL OFL 1.1。

  ── 字体清单 ──

{build_font_table()}

  上表信息由 fontTools 直接读取各源字体 name 表（nameID 0/13/14）得出，
  可用 demos/_src/check_font_licenses.py 复核。

{build_ofl_notes()}

  ── 上游项目地址 ──

{build_font_upstream()}

  ── 为什么必须内置中文字体 ──

{build_font_why()}


{RULE}
四·附 · 官方完整正文（SIL Open Font License 1.1，逐字未改）
{RULE}

{ofl}


{RULE}
五 · 附录
{RULE}

  ── 商标、作品名与在世创作者 ──

    本项目正文会事实性提及第三方商标、作品名、公司名与在世创作者姓名。
    这些名称仅用于风格描述与溯源，不构成关联、背书或授权关系，
    一切权利归各自所有者。完整声明见 docs/TRADEMARKS.md。

    ⚠️ 对外使用红线：不得把「用 XX 画师名字生成」作为产品卖点或宣传话术。
       在世艺术家姓名 + 商业 AI 生成涉及人格权与不正当竞争争议。
       本项目提供的是审美决策方法，不是「复刻在世创作者」的工具。

  ── 出处与 AI 使用披露 ──

    出处：由《艺术风格百科大全》（24 章 250+ 艺术家/风格）提炼而成。
          底稿不随仓库分发。
    AI  ：百科内容为编者执笔为主 + AI 辅助结构化整理；
          演示页与脚本由 AI 生成（pi agent × DeepSeek V4.1 Flash）。
    详见 docs/ATTRIBUTION.md。

  ── 无担保声明 ──

    本作品按「原样」提供，不附带任何形式的明示或默示担保，包括但不限于
    对适销性、特定用途适用性及不侵权的担保。作者不对因使用本作品而产生的
    任何索赔、损害或其他责任负责。（各许可正文中另有详尽的免责条款，
    均为其组成部分。）

  ── 许可变更史 ──

    v3.0.0（2026-10-24）  内容许可由 CC BY-NC-SA 4.0 改为 CC BY 4.0：去掉
                          非商业（NC）与相同方式共享（SA）两条限制，全仓库
                          成为完全开源（代码 MIT、字体 OFL/Apache 不变）。
                          v2.x 及更早版本继续按其原始许可。
    v2.0.1（2026-10-16）  三份分拆许可文件（LICENSE-CODE / LICENSE-CONTENT /
                          LICENSE-FONTS）合并为本单一 LICENSE；
                          三份官方正文固化进 scripts/license-sources/，
                          本文件改由 scripts/build_license.py 生成。
    v2.0.0（2026-10-16）  建立三许可分治结构。

{BAR}
{PROJECT}
{REPO}
{BAR}
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="只校验 LICENSE 是否与素材同步，不写文件")
    args = ap.parse_args()

    content = render()
    if args.check:
        if not OUT.is_file():
            print("❌ LICENSE 不存在")
            return 1
        if OUT.read_text(encoding="utf-8") != content:
            print("❌ LICENSE 与 scripts/license-sources/ 不同步")
            print("   处理：python3 scripts/build_license.py")
            return 1
        print(f"✅ LICENSE 与素材同步（{len(content)} 字节 / "
              f"{len(content.splitlines())} 行）")
        return 0

    OUT.write_text(content, encoding="utf-8")
    print(f"✅ 写出 {OUT.relative_to(ROOT)}  "
          f"{len(content)} 字节 / {len(content.splitlines())} 行")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
