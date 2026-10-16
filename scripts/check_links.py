#!/usr/bin/env python3
"""
Markdown / HTML 相对链接检查 —— 防止改名后留下断链。

为什么需要：这个项目的「路由」本身就是内容的一部分
（`moods/01-…` → `code-genes/02-…` → `chapters/ch22-…`）。
一次目录改名（例如 sources/ 剥离、tasks/ → docs/changes/）
就会在几十个文件里留下静默断链——使用者点进去是 404，
却没人会报错。所以把它变成 CI 断言。

用法：
  python3 scripts/check_links.py            # 检查全部
  python3 scripts/check_links.py README.md  # 只查指定文件
退出码：0 = 无断链；1 = 有断链
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SKIP_DIRS = {".git", "node_modules", "__pycache__", "sources"}
SKIP_SCHEMES = ("http://", "https://", "mailto:", "tel:", "data:", "#")

MD_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HTML_ATTR = re.compile(r'(?:href|src)="([^"]+)"')


def iter_files(only):
    if only:
        for o in only:
            yield ROOT / o
        return
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.suffix.lower() in (".md", ".html") or p.name == "LICENSE":
            yield p


def check_file(path: Path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    targets = MD_LINK.findall(text)
    if path.suffix.lower() == ".html":
        targets += HTML_ATTR.findall(text)
    broken = []
    for t in targets:
        t = t.strip()
        if not t or t.startswith(SKIP_SCHEMES):
            continue
        t = t.split("#", 1)[0].split("?", 1)[0]
        if not t:
            continue
        if Path(t).is_absolute():
            broken.append((t, "绝对路径（应改为仓库内相对路径）"))
            continue
        resolved = (path.parent / t).resolve()
        if not resolved.exists():
            broken.append((t, "目标不存在"))
    return broken


def main() -> int:
    files = [p for p in iter_files(sys.argv[1:]) if p.is_file()]
    total = bad = 0
    for p in sorted(files):
        rel = p.relative_to(ROOT)
        broken = check_file(p)
        total += 1
        if broken:
            bad += 1
            print(f"\033[31m✗\033[0m {rel}")
            for t, why in broken:
                print(f"      → {t}  ({why})")
    if bad == 0:
        print(f"\033[32m✓\033[0m {total} 个文件的相对链接全部有效")
        return 0
    print(f"\n\033[31m{total} 个文件中 {bad} 个存在断链。\033[0m")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
