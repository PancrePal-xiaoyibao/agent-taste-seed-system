#!/usr/bin/env python3
"""
截图新鲜度检查 —— 「改了页面但忘了重渲染截图」是静默故障。

## 为什么不能直接 git diff

最直白的做法是重渲染后 `git diff --quiet`。但这条路在 CI 上**必然误报**：

- CI 的 Chromium 版本与本机不同
- 字体栅格化后端（FreeType / Skia）在不同 Ubuntu 版本上断字位置有微差
- 无损 WebP 编码器版本差异

结果是「内容完全正确，像素有 ±2 的抖动」，严格比对会把好的 PR 卡死。
假阴性（放过真故障）比假阳性（卡死好 PR）危害更大——所以这里不比字节，比**结构指纹**：

  1. 尺寸必须完全一致         —— 抓「页面高度/宽度变了」
  2. 均值亮度差 ≤ TOL_LUM     —— 抓「整页变亮/变暗」
  3. 16×16 灰度指纹最大差 ≤ TOL_SIG  —— 抓「某块区域被换了内容」
  4. 显著色相数必须一致       —— 抓「配色被改」
  5. 暗部/留白占比差 ≤ TOL_PCT —— 抓「风格纪律被破坏」

前四项容忍渲染抖动，第五项直接复用 qa_style 的指标口径。

用法：
  python3 scripts/check_shots_freshness.py <新渲染目录> <仓库内的截图目录>
退出码：0 = 新鲜；1 = 落后（需重渲染后提交）
"""

import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("需要 Pillow：pip install pillow", file=sys.stderr)
    raise SystemExit(2)

TOL_LUM = 4.0      # 均值亮度容差（0-255）
TOL_SIG = 26       # 16×16 灰度指纹单格最大差
TOL_PCT = 3.0      # 暗部/留白占比容差（百分点）


def fingerprint(path: Path):
    img = Image.open(path).convert("RGB")
    g = img.convert("L")
    px = list(g.getdata())
    mean = sum(px) / len(px)
    tiny = g.resize((16, 16), Image.BILINEAR)
    sig = list(tiny.getdata())

    hsv = img.convert("HSV")
    hp = hsv.load()
    dark = light = 0
    n = 0
    bins = [0] * 12
    for y in range(0, img.height, 4):
        for x in range(0, img.width, 4):
            h, s, v = hp[x, y]
            n += 1
            if v < 48:
                dark += 1
            elif v > 205:
                light += 1
            if s > 51 and v > 46:
                bins[(h * 12) // 256] += 1
    return {
        "size": img.size,
        "mean": mean,
        "sig": sig,
        "dark": dark * 100 / max(n, 1),
        "light": light * 100 / max(n, 1),
        "hue_n": sum(1 for c in bins if c / max(n, 1) > 0.008),
    }


def compare(name: str, a: Path, b: Path):
    """返回问题列表（空 = 通过）"""
    fa, fb = fingerprint(a), fingerprint(b)
    issues = []

    if fa["size"] != fb["size"]:
        issues.append(f"尺寸不一致：新渲染 {fa['size']} vs 仓库 {fb['size']}")

    d_lum = abs(fa["mean"] - fb["mean"])
    if d_lum > TOL_LUM:
        issues.append(f"均值亮度差 {d_lum:.1f} > {TOL_LUM}（整页明暗变了）")

    d_sig = max(abs(p - q) for p, q in zip(fa["sig"], fb["sig"]))
    if d_sig > TOL_SIG:
        issues.append(f"指纹单格最大差 {d_sig} > {TOL_SIG}（某块区域内容变了）")

    if fa["hue_n"] != fb["hue_n"]:
        issues.append(f"显著色相数 {fa['hue_n']} vs {fb['hue_n']}（配色变了）")

    for key, label in (("dark", "暗部占比"), ("light", "留白占比")):
        d = abs(fa[key] - fb[key])
        if d > TOL_PCT:
            issues.append(f"{label}差 {d:.1f} 百分点 > {TOL_PCT}"
                          f"（{fa[key]:.1f}% vs {fb[key]:.1f}%）")

    return issues


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    new_dir, old_dir = Path(sys.argv[1]), Path(sys.argv[2])

    if not new_dir.is_dir():
        print(f"新渲染目录不存在：{new_dir}", file=sys.stderr)
        return 1

    shots = sorted(old_dir.glob("*.webp"))
    if not shots:
        print(f"仓库内无截图：{old_dir}", file=sys.stderr)
        return 1

    stale, ok = [], 0
    for old in shots:
        new = new_dir / old.name
        if not new.is_file():
            stale.append((old.name, ["新渲染未产出该文件"]))
            continue
        issues = compare(old.name, new, old)
        if issues:
            stale.append((old.name, issues))
        else:
            ok += 1

    if stale:
        print(f"\033[31m✗ 截图落后于页面（{len(stale)}/{len(shots)}）：\033[0m")
        for name, issues in stale:
            print(f"    {name}")
            for i in issues:
                print(f"        · {i}")
        print("\n  处理：本地跑 `python3 demos/_src/render_shots.py` 后提交新截图。")
        return 1

    print(f"\033[32m✓ {ok} 张截图与页面内容一致"
          f"（容忍渲染抖动：亮度 ±{TOL_LUM}、指纹 ±{TOL_SIG}、占比 ±{TOL_PCT}pt）\033[0m")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
