#!/usr/bin/env python3
"""
demos 布局质检（程序化代替肉眼，可复现）。

因为渲染环境看不到图像，这里用真实浏览器做几何校验，捕捉三类事故：
  1. 溢出    —— 页面被撑出声明的画布（设计稿失效）
  2. 越界    —— 元素矩形跑出画布外（内容被裁）
  3. 遮挡    —— 文本元素互相压叠（可读性事故）

用法：
  python3 demos/_src/qa_layout.py
  python3 demos/_src/qa_layout.py 06 12
"""

import os
import re
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

DEMOS = Path(__file__).resolve().parent.parent
DEFAULT_CHROME = "~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome"
CHROME = os.environ.get("CHROME", DEFAULT_CHROME)

# 允许的越界容差（px）：装饰元素常故意出血
TOL = 2

PROBE = r"""
(tol) => {
  const TOL = tol;
  const W = document.documentElement.clientWidth;
  const H = document.documentElement.clientHeight;
  const out = {canvas:[W,H], scroll:[document.documentElement.scrollWidth,
                                     document.documentElement.scrollHeight],
               outside:[], overlaps:[], tiny:[], lowcont:[]};
  const nodes = [...document.querySelectorAll('body *')];
  const vis = nodes.filter(n => {
    const cs = getComputedStyle(n);
    if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) return false;
    const r = n.getBoundingClientRect();
    return r.width > 0 && r.height > 0 && !n.closest('[data-qa-ignore]');
  });
  for (const n of vis) {
    const r = n.getBoundingClientRect();
    const tag = n.tagName.toLowerCase();
    const cls = (n.className && n.className.toString().slice(0,26)) || '';
    const own = [...n.childNodes].some(c => c.nodeType === 3 && c.textContent.trim());
    // 绝对定位的装饰（圆/波浪/渐变块）允许出血；仅当元素自身承载文本才报越界
    if (own && (r.left < -TOL || r.top < -TOL || r.right > W + TOL || r.bottom > H + TOL)) {
      out.outside.push({tag, cls, rect:[Math.round(r.left),Math.round(r.top),
                                        Math.round(r.right),Math.round(r.bottom)]});
    }
    // 字号过小：低于 9px 不可读
    if (own) {
      const fs = parseFloat(getComputedStyle(n).fontSize);
      if (fs < 9) out.tiny.push({tag, cls, fontSize:fs});
      // WCAG 对比度：取实际背景色（向上找第一个不透明背景），要求 ≥4.5（正文）/ ≥3（大字）
      const fg = getComputedStyle(n).color.match(/[\d.]+/g).map(Number);
      let el = n, bg = null;
      while (el && el !== document.documentElement) {
        const bc = getComputedStyle(el).backgroundColor.match(/[\d.]+/g).map(Number);
        if (bc.length >= 3 && (bc.length < 4 || bc[3] > 0.85)) { bg = bc; break; }
        el = el.parentElement;
      }
      if (bg) {
        const lin = c => { c /= 255; return c <= 0.03928 ? c/12.92 : Math.pow((c+0.055)/1.055, 2.4); };
        const L = c => 0.2126*lin(c[0]) + 0.7152*lin(c[1]) + 0.0722*lin(c[2]);
        const l1 = L(fg), l2 = L(bg);
        const ratio = (Math.max(l1,l2) + 0.05) / (Math.min(l1,l2) + 0.05);
        const big = fs >= 24 || (fs >= 18.66 && parseInt(getComputedStyle(n).fontWeight) >= 700);
        const need = big ? 3.0 : 4.5;
        if (ratio < need && n.textContent.trim().length > 1) {
          out.lowcont.push({tag, cls, ratio:+ratio.toFixed(2), need, fs:Math.round(fs)});
        }
      }
    }
  }
  // 文本元素两两遮挡（只查携带直接文本的、非嵌套包含关系）
  const texts = vis.filter(n => [...n.childNodes].some(c => c.nodeType===3 && c.textContent.trim()));
  for (let i=0;i<texts.length;i++) for (let j=i+1;j<texts.length;j++) {
    const a=texts[i], b=texts[j];
    if (a.contains(b) || b.contains(a)) continue;
    const da=getComputedStyle(a).display, db=getComputedStyle(b).display;
    // 同一块级父元素下的两个 inline 是同一行内格式化上下文的兄弟，
    // 实际绘制盒永远不会重叠（只是 boundingRect 会含多行并集）——跳过
    if (da === 'inline' && db === 'inline' && a.parentElement === b.parentElement) continue;
    const ra=a.getBoundingClientRect(), rb=b.getBoundingClientRect();
    const ox = Math.min(ra.right,rb.right) - Math.max(ra.left,rb.left);
    const oy = Math.min(ra.bottom,rb.bottom) - Math.max(ra.top,rb.top);
    if (ox > 6 && oy > 6) {
      const area = ox*oy, min = Math.min(ra.width*ra.height, rb.width*rb.height);
      if (area / min > 0.30) {
        out.overlaps.push({a:[a.tagName.toLowerCase(),
                             (a.className||'').toString().slice(0,26)],
                           b:[b.tagName.toLowerCase(),
                             (b.className||'').toString().slice(0,26)],
                           ratio:+(area/min).toFixed(2)});
      }
    }
  }
  return out;
}
"""


def region_contrast(png: bytes, rect) -> float:
    """（保留工具）区域亮度 P95−P5 极差。"""
    import io
    x0, y0, x1, y1 = rect
    img = Image.open(io.BytesIO(png)).convert("L")
    x0 = max(0, x0); y0 = max(0, y0)
    x1 = min(img.width, x1); y1 = min(img.height, y1)
    if x1 - x0 < 3 or y1 - y0 < 3:
        return 99.0
    px = sorted(img.crop((x0, y0, x1, y1)).getdata())
    n = len(px)
    return float(px[min(n - 1, int(n * 0.95))] - px[int(n * 0.05)])


def main() -> int:
    only = sys.argv[1:]
    pages = []
    for p in sorted(DEMOS.glob("*.html")):
        if only and not any(p.name.startswith(k) for k in only):
            continue
        head = p.read_text(encoding="utf-8")[:1200]
        m = re.search(r'data-canvas="(\d+)x(full|\d+)"', head)
        if not m:
            continue
        pages.append((p, int(m.group(1)), m.group(2)))

    chrome = Path(os.path.expanduser(CHROME))
    bad = 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=str(chrome),
                                     args=["--no-sandbox", "--font-render-hinting=none"])
        for path, w, hs in pages:
            page_h = 900 if hs == "full" else int(hs)
            ctx = browser.new_context(viewport={"width": w, "height": page_h},
                                      device_scale_factor=1, reduced_motion="reduce")
            page = ctx.new_page()
            errs = []
            page.on("pageerror", lambda e: errs.append(str(e)[:120]))
            page.on("console", lambda m: errs.append("console:" + m.text[:100])
                    if m.type == "error" else None)
            page.goto(path.as_uri(), wait_until="load")
            page.evaluate("document.fonts.ready")
            page.wait_for_function("document.fonts.status === 'loaded'")
            page.wait_for_timeout(300)
            r = page.evaluate(PROBE, TOL)
            issues = []
            if r["scroll"][0] > r["canvas"][0] + TOL and hs != "full":
                issues.append(f"横向溢出 scroll={r['scroll']} canvas={r['canvas']}")
            if r["scroll"][1] > r["canvas"][1] + TOL and hs != "full":
                issues.append(f"纵向溢出 scroll={r['scroll']} canvas={r['canvas']}")
            if r["outside"] and hs != "full":
                issues.append("越界 " + "; ".join(
                    f"{o['tag']}.{o['cls']}{o['rect']}" for o in r["outside"][:4]))
            if r["overlaps"]:
                issues.append("遮挡 " + "; ".join(
                    f"{o['a'][0]}.{o['a'][1]} × {o['b'][0]}.{o['b'][1]} ({o['ratio']})"
                    for o in r["overlaps"][:4]))
            if r["tiny"]:
                issues.append("字号过小 " + str(r["tiny"][:3]))
            if r["lowcont"]:
                issues.append("对比度不足(文字可能看不清) " + "; ".join(
                    f"{c['tag']}.{c['cls']} {c['ratio']}:1 (需{c['need']}, {c['fs']}px)"
                    for c in r["lowcont"][:4]))
            if errs:
                issues.append("JS错误 " + "; ".join(errs[:2]))
            if issues:
                bad += 1
                print(f"✗ {path.name}")
                for s in issues:
                    print(f"    {s}")
            else:
                print(f"✓ {path.name}")
            ctx.close()
        browser.close()
    print(f"\n{len(pages)} 页，{bad} 页有问题")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
