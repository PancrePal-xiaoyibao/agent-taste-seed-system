#!/usr/bin/env python3
"""
demos 实时渲染截图管线（可复现）。

用真实 Chromium 打开 demos/*.html，等字体与渲染彻底稳定后按 2 倍
设备像素比截图，再转成高清 WebP 供 README 展示。

每张演示页在 <html data-canvas="WxH" data-slug="..."> 里声明画布尺寸，
保证截图与设计稿像素一致（不依赖窗口大小）。写成 data-canvas="1440xfull"
则按整页内容高度截图（用于样本墙这类长页面）。

用法：
  python3 demos/_src/render_shots.py            # 全部
  python3 demos/_src/render_shots.py 03 07      # 只渲染前缀匹配的几张
  CHROME=/path/to/chrome python3 ...
  SCALE=1 python3 demos/_src/render_shots.py    # 降低像素密度（长图用）
  OUT_DIR=/tmp/shots python3 demos/_src/render_shots.py   # 输出到别处（CI 比对用）
"""

import os
import re
import sys
import tempfile
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

from _browser import launch_kwargs

DEMOS = Path(__file__).resolve().parent.parent
SHOTS = Path(os.environ.get("OUT_DIR") or (DEMOS / "_assets" / "shots"))
SCALE = int(os.environ.get("SCALE", "2"))  # 设备像素比：2 倍 = 高清

# 浏览器路径由 _browser 自适应解析（本机快照 ≠ 通用事实，写死路径会让 CI 永久红）
APPEARANCE = ["--no-sandbox", "--font-render-hinting=none", "--force-color-profile=srgb"]


def to_webp(png: Path, out: Path, cap_kb: int = 700) -> tuple:
    """无损优先；文件过大时退回高质量有损（文字仍锐利）。"""
    img = Image.open(png).convert("RGB")
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "WEBP", method=6, quality=100, lossless=True)
    mode = "lossless"
    if out.stat().st_size > cap_kb * 1024:
        img.save(out, "WEBP", method=6, quality=92)
        mode = "q92"
    return img.size, out.stat().st_size, mode


def main() -> int:
    only = sys.argv[1:]
    pages = []
    for p in sorted(DEMOS.glob("*.html")):
        if only and not any(p.name.startswith(k) for k in only):
            continue
        head = p.read_text(encoding="utf-8")[:1200]
        if 'data-shots="skip"' in head:
            print(f"跳过（data-shots=skip，展示页不产图）：{p.name}")
            continue
        m = re.search(r'data-canvas="(\d+)x(full|\d+)"', head)
        if not m:
            print(f"跳过（未声明 data-canvas）：{p.name}")
            continue
        # 输出文件名用 ASCII slug：中文文件名在 GitHub 的图片 URL 里会被转义，易碎
        sm = re.search(r'data-slug="([a-z0-9-]+)"', head)
        slug = sm.group(1) if sm else p.stem
        pages.append((p, int(m.group(1)), m.group(2), slug))

    if not pages:
        print("没有可渲染的页面", file=sys.stderr)
        return 1

    SHOTS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch(**launch_kwargs(APPEARANCE))
        for path, w, hs, slug in pages:
            full = hs == "full"
            h = 900 if full else int(hs)
            ctx = browser.new_context(
                viewport={"width": w, "height": h},
                device_scale_factor=SCALE,
                reduced_motion="reduce",
            )
            page = ctx.new_page()
            page.goto(path.as_uri(), wait_until="load")
            page.evaluate("document.fonts.ready")
            page.wait_for_function("document.fonts.status === 'loaded'")
            page.wait_for_timeout(700)  # 留时间给动画/字体二次布局落定
            if full:
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(300)
                page.evaluate("window.scrollTo(0, 0)")
                page.wait_for_timeout(200)
            with tempfile.TemporaryDirectory() as td:
                png = Path(td) / (path.stem + ".png")
                if full:
                    page.screenshot(path=str(png), full_page=True)
                else:
                    page.screenshot(path=str(png),
                                    clip={"x": 0, "y": 0, "width": w, "height": h})
                size, nbytes, mode = to_webp(png, SHOTS / (slug + ".webp"))
            print(f"{slug + '.webp':<34} {size[0]}x{size[1]}  {nbytes / 1024:7.0f} KB  ({mode})")
            ctx.close()
        browser.close()
    try:
        shown = SHOTS.relative_to(DEMOS.parent)
    except ValueError:
        shown = SHOTS
    print(f"\n截图输出目录：{shown}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
