#!/usr/bin/env python3
"""
字体子集许可合规检查 —— 把 OFL 1.1 §1/§3 变成 CI 断言。

背景：`demos/_assets/fonts/*.woff2` 是开源字体的**子集**，
子集是 OFL 意义上的 Modified Version，因此：

  §3  修改版不得使用「保留字体名」（Reserved Font Name）
  §1  必须随字体保留版权声明与许可声明

本项目实测：Noto Sans SC（保留名 'Source'）、Playfair Display、
Yeseva One、Marcellus 都在 nameID 0 里声明了保留字体名。
所以 `build_fonts.py` 对所有子集统一加 `AB ` 前缀，并刻意不动
nameID 0（版权）与 13/14（许可）。

本脚本就是验证「这两件事真的做到了」。

用法：
  python3 demos/_src/check_font_licenses.py
退出码：0 = 合规；1 = 违规
"""

import re
import sys
from pathlib import Path

from fontTools.ttLib import TTFont

FONT_DIR = Path(__file__).resolve().parent.parent / "_assets" / "fonts"
PREFIX = "AB "

# 源字体里声明过的保留字体名（用于反查子集是否误用）
RESERVED = ["Source", "Playfair Display", "Yeseva", "Marcellus"]


def main() -> int:
    fonts = sorted(FONT_DIR.glob("*.woff2"))
    if not fonts:
        print(f"找不到字体子集：{FONT_DIR}", file=sys.stderr)
        return 1

    fails = []
    for f in fonts:
        t = TTFont(str(f))
        names = {}
        for rec in t["name"].names:
            try:
                names.setdefault(rec.nameID, rec.toUnicode())
            except Exception:
                pass

        family = names.get(1, "")
        full = names.get(4, "")
        ps = names.get(6, "")
        typo = names.get(16, "")
        copy = names.get(0, "")
        lic = names.get(13) or names.get(14) or ""

        # ① 家族名必须带 AB 前缀（OFL §3：修改版不得沿用保留字体名）
        for label, val in (("nameID 1 (family)", family),
                           ("nameID 4 (full)", full),
                           ("nameID 6 (PS)", ps),
                           ("nameID 16 (typo family)", typo)):
            if not val:
                fails.append((f.name, f"{label} 缺失"))
            elif not val.lstrip().startswith(PREFIX.strip()):
                fails.append((f.name, f"{label}='{val}' 未带 '{PREFIX.strip()}' 前缀"))

        # ② 不得残留任何已知保留字体名（作为完整词，避免误伤 AB 前缀里的字母）
        for r in RESERVED:
            if re.search(r"(?<!AB )\b" + re.escape(r) + r"\b", family + " " + full):
                fails.append((f.name, f"仍含保留字体名 '{r}'"))

        # ③ 版权与许可声明必须保留（OFL §1）
        if not copy.strip():
            fails.append((f.name, "nameID 0 (版权声明) 被清空——违反 OFL §1"))
        if "OFL" not in lic and "openfontlicense" not in lic.lower() \
                and "scripts.sil.org" not in lic.lower():
            fails.append((f.name, f"nameID 13/14 未指向 OFL（值为 '{lic[:40]}'）"))

    if fails:
        print(f"\033[31m✗ {len(fails)} 项字体许可违规：\033[0m")
        for name, why in fails:
            print(f"      {name}: {why}")
        return 1

    print(f"\033[32m✓\033[0m {len(fonts)} 个字体子集全部合规："
          f"带 '{PREFIX.strip()}' 前缀 · 无保留字体名残留 · 保留版权与 OFL 声明")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
