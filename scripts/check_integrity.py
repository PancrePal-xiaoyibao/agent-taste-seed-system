#!/usr/bin/env python3
"""
内容完整性断言 —— 防止「有人 PR 时误删了一部分种子库」这类静默退化。

为什么需要它：本项目的价值全在文件齐备性上。少一章分章、少一张基因卡，
功能不会报错，但使用者会在某个情绪档上查到空结果，然后默默退回默认审美——
这正是整个项目要消灭的那件事。

所以这里把「齐备」变成 CI 里的可判定断言。

用法：
  python3 scripts/check_integrity.py
退出码：0 = 齐备；1 = 有缺失或退化
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 每个种子目录的预期条目数（同时作为内容量的下限断言）
EXPECTED = {
    "references/code-genes": 12,
    "references/moods": 10,
    "references/chapters": 25,
}

# 关键文件的体积下限（KB）——防止被替换成占位文件
MIN_KB = {
    "references/art-seeds.md": 60,
    "TASTE.md": 3,
    "README.md": 6,
}

LEGAL_FILES = [
    "LICENSE",
    "LICENSE-CODE.md",
    "LICENSE-CONTENT.md",
    "LICENSE-FONTS.md",
    "CITATION.cff",
    "CONTRIBUTING.md",
    "docs/TRADEMARKS.md",
    "docs/ATTRIBUTION.md",
    "docs/METHODOLOGY.md",
]


class Report:
    def __init__(self) -> None:
        self.fail = 0

    def ok(self, msg: str) -> None:
        print(f"  \033[32m✓\033[0m {msg}")

    def bad(self, msg: str) -> None:
        print(f"  \033[31m✗\033[0m {msg}")
        self.fail += 1


def check_counts(r: Report) -> None:
    print("\n\033[1m1. 种子库条目数\033[0m")
    for rel, expect in EXPECTED.items():
        d = ROOT / rel
        if not d.is_dir():
            r.bad(f"{rel} 目录不存在")
            continue
        files = sorted(p for p in d.glob("*.md") if p.is_file())
        if len(files) == expect:
            r.ok(f"{rel}  {len(files)} 份")
        else:
            r.bad(f"{rel}  期望 {expect} 份，实际 {len(files)} 份"
                  f"（缺：{ {p.name for p in files} ^ set() } 或有多余文件）")


def check_min_size(r: Report) -> None:
    print("\n\033[1m2. 关键文件体积下限\033[0m")
    for rel, min_kb in MIN_KB.items():
        p = ROOT / rel
        if not p.is_file():
            r.bad(f"{rel} 不存在")
            continue
        kb = p.stat().st_size / 1024
        if kb >= min_kb:
            r.ok(f"{rel}  {kb:.0f} KB（下限 {min_kb} KB）")
        else:
            r.bad(f"{rel} 仅 {kb:.0f} KB，低于下限 {min_kb} KB——可能被截断")


def check_chapter_headers(r: Report) -> None:
    print("\n\033[1m3. 分章免责头\033[0m")
    miss = []
    for p in sorted((ROOT / "references/chapters").glob("ch*.md")):
        txt = p.read_text(encoding="utf-8")[:800]
        if "CC BY-NC-SA" not in txt:
            miss.append(p.name)
    if miss:
        r.bad(f"{len(miss)} 份分章缺少许可/商标免责头：{miss[:4]}")
    else:
        r.ok("25 份分章均带许可与商标免责头")


def check_legal(r: Report) -> None:
    print("\n\033[1m4. 许可与合规文件\033[0m")
    for rel in LEGAL_FILES:
        p = ROOT / rel
        if p.is_file() and p.stat().st_size > 200:
            r.ok(rel)
        elif p.is_file():
            r.bad(f"{rel} 存在但内容过短（<200 字节）")
        else:
            r.bad(f"{rel} 缺失")


def check_demos(r: Report) -> None:
    print("\n\033[1m5. 演示页与截图配对\033[0m")
    demos = ROOT / "demos"
    if not demos.is_dir():
        r.bad("demos/ 不存在")
        return
    pages = {}
    for p in sorted(demos.glob("*.html")):
        head = p.read_text(encoding="utf-8")[:1500]
        if 'data-shots="skip"' in head:
            continue
        m = re.search(r'data-slug="([a-z0-9-]+)"', head)
        if m:
            pages[m.group(1)] = p
    missing = [s for s in pages
               if not (demos / "_assets/shots" / f"{s}.webp").is_file()]
    if missing:
        r.bad(f"{len(missing)} 张演示页缺少对应截图：{missing[:3]}")
    else:
        r.ok(f"{len(pages)} 张演示页与截图一一配对")

    # CSS 里声明的字体文件必须真实存在（防止改了名却没重建子集）
    css = demos / "_assets/taste-fonts.css"
    if not css.is_file():
        r.bad("demos/_assets/taste-fonts.css 不存在")
        return
    refs = re.findall(r"fonts/([A-Za-z0-9_.-]+\.woff2)", css.read_text(encoding="utf-8"))
    gone = [f for f in refs if not (demos / "_assets/fonts" / f).is_file()]
    if gone:
        r.bad(f"CSS 引用了 {len(gone)} 个不存在的字体文件：{gone[:3]}")
    else:
        r.ok(f"CSS 引用的 {len(refs)} 个字体子集全部存在")

    # 子集家族名必须带 AB 前缀（OFL 保留字体名合规，见 LICENSE-FONTS.md）
    bad_fam = re.findall(r"font-family:'(?!AB )([^']+)'", css.read_text(encoding="utf-8"))
    if bad_fam:
        r.bad(f"{len(bad_fam)} 个 @font-face 家族名未加 'AB ' 前缀（违反 OFL §3）："
              f"{sorted(set(bad_fam))[:3]}")
    else:
        r.ok("所有 @font-face 家族名均带 'AB ' 前缀（OFL 命名合规）")


def main() -> int:
    r = Report()
    check_counts(r)
    check_min_size(r)
    check_chapter_headers(r)
    check_legal(r)
    check_demos(r)
    if r.fail == 0:
        print("\n\033[32m完整性检查通过。\033[0m")
    else:
        print(f"\n\033[31m完整性检查未通过：{r.fail} 项。\033[0m")
    return 1 if r.fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
