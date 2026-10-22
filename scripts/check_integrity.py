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

import fnmatch
import re
import subprocess
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

# 许可与合规文件（三份官方正文已并入单一 LICENSE，见 scripts/build_license.py）
LEGAL_FILES = [
    "LICENSE",
    "CITATION.cff",
    "CONTRIBUTING.md",
    "docs/TRADEMARKS.md",
    "docs/ATTRIBUTION.md",
    "docs/METHODOLOGY.md",
    "scripts/build_license.py",
    "scripts/license-sources/cc-by-nc-sa-4.0-legalcode.txt",
    "scripts/license-sources/ofl-1.1.txt",
    "scripts/license-sources/mit.txt",
]

# LICENSE §一「适用范围」里声明的三块分区（用于反向校验许可覆盖无盲区）
LICENSE_ZONES = {
    "MIT": ("demos/_src/*.py", "scripts/*.py", "scripts/*.sh",
            "deploy/*.sh", ".github/**"),
    "FONT": ("demos/_assets/fonts/**",),
    "EXEMPT": ("scripts/license-sources/**",),
}


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
        # 下限断言：允许 agent 在运行时增量新增（不改源文件），
        # 但绝不允许多于原数的「变少」——那是删了内容或被截断。
        if len(files) >= expect:
            extra = len(files) - expect
            r.ok(f"{rel}  {len(files)} 份（下限 {expect}" + (f"，新增 {extra}" if extra else "") + "）")
        else:
            r.bad(f"{rel}  期望至少 {expect} 份，实际 {len(files)} 份（可能被误删）")


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

    # 子集家族名必须带 AB 前缀（OFL 保留字体名合规，见 LICENSE）
    bad_fam = re.findall(r"font-family:'(?!AB )([^']+)'", css.read_text(encoding="utf-8"))
    if bad_fam:
        r.bad(f"{len(bad_fam)} 个 @font-face 家族名未加 'AB ' 前缀（违反 OFL §3）："
              f"{sorted(set(bad_fam))[:3]}")
    else:
        r.ok("所有 @font-face 家族名均带 'AB ' 前缀（OFL 命名合规）")


def check_license_zones(r: Report) -> None:
    """许可覆盖守卫 —— 防「新增文件掉进许可的缝里」。

    本文件里最有价值的一项。LICENSE 里写的是**模式**（scripts/*.py），
    仓库里却是**具体文件**，两者会悄悄地脱节：
      · 新增 scripts/foo.py，但 LICENSE 只写了 scripts/*.sh → 该文件无人认领
      · 把某份文档挪进 _src/ → 它被 MIT 覆盖了，作者却以为是 CC

    所以做双向断言：
      1. 代码扩展名的文件必须落在 MIT 区
      2. 内容扩展名的文件不能落在 MIT 区
      3. LICENSE 里必须真实声明这些模式（代码改了、许可文档没跟上就报错）
    """
    print("\n\033[1m6. 许可覆盖守卫（防新增文件掉进缝里）\033[0m")
    out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT,
                         capture_output=True, text=True, encoding="utf-8").stdout
    tracked = [p for p in (out or "").split("\0") if p]
    if not tracked:
        r.bad("git ls-files 返回空——无法核验许可覆盖")
        return

    def match(path: str, pat: str) -> bool:
        if pat.endswith("/**"):
            base = pat[:-3]
            return path == base or path.startswith(base + "/")
        return fnmatch.fnmatch(path, pat)

    def zone_of(path: str) -> str:
        for zone, pats in LICENSE_ZONES.items():
            if any(match(path, p) for p in pats):
                return zone
        return "CONTENT"          # 默认区：其余一切文件

    CODE_EXT = {".py", ".sh", ".yml", ".yaml"}
    CONTENT_EXT = {".md", ".html", ".css", ".cff", ".txt", ".jpg", ".png"}

    miszoned = []
    for p in tracked:
        ext = Path(p).suffix.lower()
        zone = zone_of(p)
        if zone == "MIT" and ext in CONTENT_EXT and not p.startswith("scripts/license-sources/"):
            miszoned.append((p, f"内容扩展名 {ext} 落在 MIT 区"))
        if zone == "CONTENT" and ext in CODE_EXT:
            miszoned.append((p, f"代码扩展名 {ext} 却落在 CONTENT 兜底区"))

    if miszoned:
        r.bad(f"{len(miszoned)} 个文件的许可分区与类型不符：")
        for p, why in miszoned[:6]:
            print(f"        {p} —— {why}")
    else:
        r.ok(f"{len(tracked)} 个跟踪文件全部落在预期许可分区")

    lic_path = ROOT / "LICENSE"
    if not lic_path.is_file():
        r.bad("LICENSE 不存在")
        return
    lic = lic_path.read_text(encoding="utf-8")
    missing = []
    for zone, pats in LICENSE_ZONES.items():
        for pat in pats:
            core = pat.replace("/**", "").replace("*.py", "").replace("*.sh", "").rstrip("/")
            if core and core not in lic:
                missing.append(f"{zone}:{pat}")
    if missing:
        r.bad(f"LICENSE 未声明以下分区（代码与许可文档脱节）：{missing}")
    else:
        r.ok("LICENSE §一 已声明全部分区模式")


def check_license_sync(r: Report) -> None:
    """LICENSE 必须能由 scripts/license-sources/ 重跑生成（否则素材与产物脱节）。"""
    print("\n\033[1m7. LICENSE 与素材同步\033[0m")
    script = ROOT / "scripts" / "build_license.py"
    if not script.is_file():
        r.bad("缺少 scripts/build_license.py")
        return
    out = subprocess.run([sys.executable, str(script), "--check"],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    if out.returncode == 0:
        r.ok((out.stdout or "").strip().replace("✅ ", ""))
    else:
        r.bad("LICENSE 与 scripts/license-sources/ 不同步")
        print("        处理：python3 scripts/build_license.py")


def main() -> int:
    r = Report()
    check_counts(r)
    check_min_size(r)
    check_chapter_headers(r)
    check_legal(r)
    check_demos(r)
    check_license_zones(r)
    check_license_sync(r)
    if r.fail == 0:
        print("\n\033[32m完整性检查通过。\033[0m")
    else:
        print(f"\n\033[31m完整性检查未通过：{r.fail} 项。\033[0m")
    return 1 if r.fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
