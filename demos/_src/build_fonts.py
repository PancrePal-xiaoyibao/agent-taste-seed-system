#!/usr/bin/env python3
"""
demos 字体子集化管线（可复现）。

作用：把演示页真正用到的字形，从源字体裁成 woff2 子集，输出
  demos/_assets/fonts/*.woff2
  demos/_assets/taste-fonts.css

为什么必须做：系统无中文衬线，且仓库不能带 40MB 源字体；
子集化后 12 个风格页共用一份约 2MB 字体资产，页面与截图都能在任何
机器上稳定复现（不依赖访问 Google Fonts）。

用法：
  python3 demos/_src/build_fonts.py                 # 默认扫 demos/*.html
  SOURCE_DIR=/path/to/ttf python3 .../build_fonts.py
"""

import html
import os
import re
import sys
from pathlib import Path

from fontTools.subset import Options, Subsetter
from fontTools.ttLib import TTFont

DEMOS = Path(__file__).resolve().parent.parent
ASSETS = DEMOS / "_assets"
FONT_OUT = ASSETS / "fonts"
CSS_OUT = ASSETS / "taste-fonts.css"

SOURCE_DIR = Path(os.environ.get(
    "SOURCE_DIR",
    str(Path(os.path.expanduser("~/.cache/taste-seed-fonts"))),
))
# 兼容备用落点（见 demos/README.md「复现」：源字体不进仓库）
SOURCE_FALLBACK = Path("/tmp/taste-fonts")

# 源字体文件名 -> (CSS 家族名, 字重, 是否需要中文字形)
# 输出家族名统一加 AB 前缀（见 rename_font）：
#   - 多数 OFL 字体声明了 Reserved Font Name（RFN），子集=修改版，沿用原名违反 OFL
#   - 即使未声明 RFN，子集顶着原名也会误导使用者
# 所以一律改名，一条规则覆盖全部，无需记忆例外。
FAMILY_PREFIX = "AB"

FACES = [
    ("NotoSerifSC-Regular.ttf", "Noto Serif SC", 400),
    ("NotoSerifSC-Bold.ttf", "Noto Serif SC", 700),
    ("NotoSansSC-Regular.ttf", "Noto Sans SC", 400),
    ("NotoSansSC-Medium.ttf", "Noto Sans SC", 500),
    ("NotoSansSC-Bold.ttf", "Noto Sans SC", 700),
    ("PlayfairDisplay-400.ttf", "Playfair Display", 400),
    ("PlayfairDisplay-700.ttf", "Playfair Display", 700),
    ("PlayfairDisplay-900.ttf", "Playfair Display", 900),
    ("Cinzel-400.ttf", "Cinzel", 400),
    ("Cinzel-700.ttf", "Cinzel", 700),
    ("CormorantGaramond-300.ttf", "Cormorant Garamond", 300),
    ("CormorantGaramond-400.ttf", "Cormorant Garamond", 400),
    ("CormorantGaramond-600.ttf", "Cormorant Garamond", 600),
    ("EBGaramond-400.ttf", "EB Garamond", 400),
    ("LibreBaskerville-400.ttf", "Libre Baskerville", 400),
    ("Marcellus-400.ttf", "Marcellus", 400),
    ("Italiana-400.ttf", "Italiana", 400),
    ("YesevaOne-400.ttf", "Yeseva One", 400),
    ("ArchivoBlack-400.ttf", "Archivo Black", 400),
    ("BebasNeue-400.ttf", "Bebas Neue", 400),
    ("Oswald-300.ttf", "Oswald", 300),
    ("Oswald-400.ttf", "Oswald", 400),
    ("Oswald-700.ttf", "Oswald", 700),
    ("Inter-300.ttf", "Inter", 300),
    ("Inter-400.ttf", "Inter", 400),
    ("Inter-600.ttf", "Inter", 600),
    ("Inter-700.ttf", "Inter", 700),
    ("Inter-900.ttf", "Inter", 900),
    ("JetBrainsMono-400.ttf", "JetBrains Mono", 400),
    ("JetBrainsMono-700.ttf", "JetBrains Mono", 700),
]

# 基础字符集：ASCII 可打印 + 常用标点/符号 + CJK 标点
BASE_EXTRA = (
    "！？。，、；：（）【】「」『』《》〈〉—…·～¥€£§¶†‡•‰°※→←↑↓↗↘✓✕✦★☆⚑丨"
    "␣  –’‘“”′″№©®™"
)


def scan_charset() -> set:
    """扫描 demos/*.html 里所有可见文本，得到需要保留的字符集合。"""
    chars = set(BASE_EXTRA)
    for p in sorted(DEMOS.glob("*.html")):
        raw = p.read_text(encoding="utf-8")
        raw = re.sub(r"<style[^>]*>.*?</style>", " ", raw, flags=re.S | re.I)
        raw = re.sub(r"<script[^>]*>.*?</script>", " ", raw, flags=re.S | re.I)
        raw = re.sub(r"<!--.*?-->", " ", raw, flags=re.S)
        text = html.unescape(re.sub(r"<[^>]+>", " ", raw))
        chars |= set(text)
    chars = {c for c in chars if c.strip() or c == " "}
    return chars


def rename_font(font: TTFont, family: str, weight: int) -> None:
    """把子集字体重命名为「AB <原家族名>」，并同步 name 表的全部相关记录。

    为什么要做：子集是 OFL 意义上的 Modified Version。多数 OFL 字体在 nameID 0 里
    声明了 Reserved Font Name（本例实测 Noto Sans SC / Playfair Display /
    Yeseva One / Marcellus 均有），OFL 1.1 §3 规定修改版不得继续使用保留字体名。
    未声明 RFN 的字体虽可沿用原名，但子集顶着原名同样会误导使用者——统一改名。

    重要：nameID 0（版权）与 13/14（许可）必须原样保留，这是 OFL 的强制要求。
    """
    styled = {300: "Light", 400: "", 500: "Medium", 600: "SemiBold",
              700: "Bold", 800: "ExtraBold", 900: "Black"}.get(weight, str(weight))
    fam = f"{FAMILY_PREFIX} {family}"
    full = f"{fam} {styled}".strip()
    ps = full.replace(" ", "")
    # (nameID, 值, 是否覆盖已有记录)
    plan = {
        1: fam,      # Font Family
        2: "Regular" if styled else "Regular",
        3: f"{ps};subset",   # Unique identifier
        4: full,     # Full name
        6: ps,       # PostScript name
        16: fam,     # Typographic Family
        17: styled or "Regular",
    }
    name = font["name"]
    for nid in list(plan):
        name.removeNames(nameID=nid)
    for nid, value in plan.items():
        name.setName(value, nid, 3, 1, 0x409)   # Windows / Unicode BMP / en-US
        name.setName(value, nid, 1, 0, 0)       # Mac / Roman / en


def subset(src: Path, dst: Path, chars: set, family: str, weight: int) -> None:
    font = TTFont(str(src), lazy=False)
    opts = Options()
    opts.layout_features = ["*"]
    opts.name_IDs = ["*"]
    opts.notdef_outline = True
    opts.recalc_bounds = True
    opts.drop_tables += ["DSIG"]
    opts.flavor = "woff2"
    sub = Subsetter(options=opts)
    # 未在文本中出现的 CJK 字符大量裁掉；拉丁/符号同理
    sub.populate(text="".join(sorted(chars)))
    sub.subset(font)
    rename_font(font, family, weight)
    dst.parent.mkdir(parents=True, exist_ok=True)
    font.save(str(dst))
    font.close()


def main() -> int:
    global SOURCE_DIR
    if not SOURCE_DIR.is_dir() and SOURCE_FALLBACK.is_dir():
        SOURCE_DIR = SOURCE_FALLBACK
    if not SOURCE_DIR.is_dir():
        print(f"源字体目录不存在：{SOURCE_DIR}（可用 SOURCE_DIR=... 指定）", file=sys.stderr)
        return 1
    chars = scan_charset()
    cjk = sum(1 for c in chars if ord(c) > 0x2E80)
    print(f"字符集：{len(chars)} 个（其中 CJK {cjk} 个）")

    FONT_OUT.mkdir(parents=True, exist_ok=True)
    rules, missing, total = [], [], 0
    for filename, family, weight in FACES:
        src = SOURCE_DIR / filename
        if not src.is_file():
            missing.append(filename)
            continue
        target = FONT_OUT / (src.stem + ".woff2")
        subset(src, target, chars, family, weight)
        size = target.stat().st_size
        total += size
        rules.append(
            "@font-face{font-family:'%s %s';font-style:normal;font-weight:%d;"
            "font-display:block;src:url('fonts/%s') format('woff2');}"
            % (FAMILY_PREFIX, family, weight, target.name)
        )
        print(f"  {target.name:<34} {size / 1024:7.1f} KB  ->  {FAMILY_PREFIX} {family} {weight}")

    CSS_OUT.write_text(
        "/* 由 demos/_src/build_fonts.py 生成，请勿手改。\n"
        "   子集来源字体与完整许可：见仓库根目录 LICENSE-FONTS。\n"
        "   家族名统一加 'AB ' 前缀：OFL 字体多有 Reserved Font Name，\n"
        "   子集（修改版）按 OFL 1.1 §3 不得沿用保留字体名。*/\n"
        + "\n".join(rules)
        + "\n",
        encoding="utf-8",
    )
    print(f"\n共 {len(rules)} 个字重，合计 {total / 1048576:.2f} MB")
    print(f"写出 {CSS_OUT.relative_to(DEMOS.parent)}")
    if missing:
        print("缺失源字体（跳过）：" + ", ".join(missing), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
