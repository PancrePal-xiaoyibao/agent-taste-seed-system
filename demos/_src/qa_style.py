#!/usr/bin/env python3
"""
demos 风格基因像素级校验（把审美纪律变成可判定断言）。

为什么需要：审美验收通常靠肉眼，但渲染环境里没人看图。这里直接从
截图像素反推风格指标，检验每张作品是否守住了自己基因卡里的硬纪律
（例：哥特暗黑要求黑暗 ≥60%，极简主义要求留白 ≥45%，
浮世绘/中国画要求色相 ≤3 种）。

指标：
  lum        平均亮度 0-255
  dark%      暗像素（亮度<48）占比
  light%     亮像素（亮度>205）占比 —— 留白的代理指标
  hue_n      显著色相数（占比 >0.8% 的色相桶），灰/白/黑不计
  sat%       彩色像素（HSV S>51 且 V>46）占比

用法：
  python3 demos/_src/qa_style.py                # 需要先跑 render_shots.py
  python3 demos/_src/qa_style.py 06 09   # 按编号前缀挑几页
"""

import sys
from pathlib import Path

from PIL import Image

DEMOS = Path(__file__).resolve().parent.parent
SHOTS = DEMOS / "_assets" / "shots"

# 每页的基因纪律断言（依据 references/code-genes/*.md 与 moods/*.md）
# 键 = 文件名前缀；值 = [(指标, 比较符, 阈值, 依据说明)]
RULES = {
    "01": [("light%", "<=", 26, "暗底基因：亮部（自发光）必须克制"),
           ("dark%", ">=", 52, "深蓝黑底要占主导"),
           ("sat%", "<=", 10, "荧光只给边/线/数字，面积 ≤15%"),
           ("hue_n", "<=", 4, "荧光青+品红双色纪律，禁紫渐变")],
    "02": [("light%", ">=", 45, "瑞士平面：白/浅灰是底"),
           ("sat%", "<=", 12, "灰阶为主，强调色不铺面"),
           ("hue_n", "<=", 3, "唯一强调色，面积 ≤10%")],
    "03": [("light%", ">=", 62, "留白（绢色）必须占大头"),
           ("sat%", "<=", 6, "整体饱和度压低，朱砂只一点"),
           ("hue_n", "<=", 3, "绢色+墨色+朱砂，色相三色封顶")],
    "04": [("light%", ">=", 52, "治愈系要亮、要留白"),
           ("sat%", "<=", 22, "饱和度整体压一档，禁荧光"),
           ("hue_n", "<=", 5, "米白+草木绿+天空蓝+暖黄")],
    "05": [("sat%", ">=", 6, "平涂大色块，饱和度不能低"),
           ("hue_n", "<=", 4, "一版一色：全图色相 ≤3（留 1 给反锯齿）")],
    "06": [("dark%", ">=", 45, "Tenebrism：黑暗要占画面"),
           ("light%", "<=", 12, "只有一个光源，禁满屏亮部"),
           ("sat%", "<=", 14, "金色只做线，不做面")],
    "07": [("light%", ">=", 60, "粉白底 + 留白 40%+"),
           ("sat%", "<=", 16, "马卡龙：明度高、饱和度中低"),
           ("hue_n", "<=", 5, "粉/婴蓝/鹅黄/玫瑰金，禁止跨色渐变")],
    "08": [("light%", ">=", 46, "极简：留白 ≥50% 是本基因的命"),
           ("hue_n", "<=", 2, "无彩 + 一个 Kelly 式点睛色块"),
           ("sat%", "<=", 32, "点睛色限一个整块（约占 1/4 画面），不many色铺满")],
    "09": [("sat%", ">=", 18, "波普：原色平涂，饱和度全开"),
           ("light%", ">=", 22, "亮白底 + 原色块，不能变暗调"),
           ("hue_n", "<=", 5, "红/黄/蓝/黑，色相 ≤4")],
    "10": [("sat%", ">=", 8, "宣传鼓动的红要有存在感"),
           ("hue_n", "<=", 3, "红 + 黑 + 米白，三色封顶")],
    "11": [("sat%", ">=", 16, "动漫基因要明快，禁高级灰低饱和"),
           ("light%", ">=", 24, "白底面板 + 明快色板")],
    "12": [("dark%", ">=", 58, "铅与烬：暗部统治画面"),
           ("sat%", "<=", 10, "骨白+铅灰，点睛色只一点"),
           ("hue_n", "<=", 3, "点睛色二选一，全局统一")],
}


def metrics(img: Image.Image) -> dict:
    small = img.convert("RGB")
    total = small.width * small.height
    hsv = small.convert("HSV")
    hp = hsv.load()
    rgb = small.load()
    dark = light = sat = 0
    hue_bins = [0] * 12
    lum_sum = 0
    step = 2  # 隔点采样：统计足够稳，速度快 4 倍
    n = 0
    for y in range(0, small.height, step):
        for x in range(0, small.width, step):
            r, g, b = rgb[x, y]
            h, s, v = hp[x, y]
            lum = (r * 299 + g * 587 + b * 114) // 1000
            lum_sum += lum
            n += 1
            if lum < 48:
                dark += 1
            elif lum > 205:
                light += 1
            if s > 51 and v > 46:           # HSV 0-255 标度：S>0.20 = 肉眼可辨的彩色
                sat += 1
                hue_bins[(h * 12) // 256] += 1
    hue_n = sum(1 for c in hue_bins if c / max(n, 1) > 0.008)
    return {
        "lum": round(lum_sum / max(n, 1), 1),
        "dark%": round(dark * 100 / max(n, 1), 1),
        "light%": round(light * 100 / max(n, 1), 1),
        "sat%": round(sat * 100 / max(n, 1), 1),
        "hue_n": hue_n,
        "px": total,
    }


def main() -> int:
    only = sys.argv[1:]
    shots = [p for p in sorted(SHOTS.glob("*.webp"))
             if not only or any(p.name.startswith(k) for k in only)]
    if not shots:
        print(f"没有截图，先跑 render_shots.py（目录：{SHOTS}）", file=sys.stderr)
        return 1

    bad = 0
    for p in shots:
        m = metrics(Image.open(p))
        key = p.name[:2]  # 文件名前缀仍是 01..12，规则键不受 slug 化影响
        print(f"{p.name[:18]:<20} lum={m['lum']:>5}  dark={m['dark%']:>5}%  "
              f"light={m['light%']:>5}%  sat={m['sat%']:>5}%  hue={m['hue_n']}")
        for rule in RULES.get(key, []):
            name, op, thr = rule[0], rule[1], rule[2]
            why = rule[3] if len(rule) > 3 else ""
            val = m[name] if isinstance(m[name], (int, float)) else 0
            ok = (val <= thr) if op == "<=" else (val >= thr)
            if not ok:
                bad += 1
                print(f"    ✗ {name} {op} {thr} 不满足（实测 {val}）— {why}")
    print(f"\n{len(shots)} 张，{bad} 条基因纪律未通过")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
