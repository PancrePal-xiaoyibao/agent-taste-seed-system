#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
seed_brain.py — 种子大脑无偏检索层（L-B / Equal-Access Retrieval）

把「人工写死的首选表」换成「全库等距平铺 + IDF 加权匹配 + 状态记忆」。

为什么需要它
------------
现状：SKILL.md 的「快速选种索引」只有 10~12 行、每行 1 个「首选」。
      全库 352 粒（美学）/ 178 条（数学）里约 95% 没有入口 ——
      不是作者故意偏，是「索引表」这个窄口子结构性地决定了只有最显眼那几粒被看见。

本脚本做三件事：
  1. build  : 解析 L1 总库 + L2 卡片 → 等距平铺索引（每粒种子同等可见，无隐含优先级）
  2. match  : 任务描述 → 全库扫描 → 字符 n-gram + IDF 加权 → 跨层均衡 top-K
  3. pick   : 记录使用 → 状态文件（时间衰减 + 次数惩罚，让「刚用过的」自然下沉）

两条刻意的设计选择
------------------
* 不用随机数。合适性由 IDF 决定（确定、可解释、可复现）；
  多样性由「状态记忆 + 时间衰减」产生 —— 同一任务隔几天再跑，
  会拿到不同的**同等合适**候选，而不是随机的**不合适**候选。
* 不用分词器。中文用 2~3 字 n-gram 覆盖任意表达变体（「霓虹」「赛博霓虹」都能命中），
  零依赖、零词表、可原样搬到新领域。

零第三方依赖；Windows / macOS / Linux 通用。

用法
----
  python3 scripts/seed_brain.py build
  python3 scripts/seed_brain.py match "科技感长图，深色底霓虹光效，讲 AI 创业融资"
  python3 scripts/seed_brain.py match "病态线性系统求解" --k 8
  python3 scripts/seed_brain.py pick cg-02-赛博霓虹 --score 5 --note "深底霓虹，一次过"
  python3 scripts/seed_brain.py stats
"""

from __future__ import annotations

__version__ = "0.1.0"  # 两份拷贝（taste / math）应始终保持同版本；抽 SDK 时收敛为单一源

import argparse
import json
import math
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent

# ── 两套 profile：同一份脚本，两个领域 ───────────────────────────────────
PROFILES = {
    "math": {
        "label": "数学种子大脑",
        "sources": [
            {"kind": "table", "path": "references/math-seeds.md", "layer": "tool"},
            {"kind": "card", "dir": "references/scenarios", "layer": "scenario"},
            {"kind": "card", "dir": "references/recipes", "layer": "recipe"},
        ],
        "index_md": "references/SEED-INDEX.md",
        "index_jsonl": "references/seed-index.jsonl",
        "state": "references/.seed-usage.json",
        # top-K 跨层配额：防止「工具层 178 条」把 scenario / recipe 全挤掉
        "quota": {"tool": 0.50, "recipe": 0.28, "scenario": 0.22},
        "decay_tau_days": 14.0,
        "count_penalty": 0.5,
        "prefix": {"tool": "tl", "recipe": "rc", "scenario": "sc"},
    },
    "taste": {
        "label": "审美种子大脑",
        "sources": [
            {"kind": "table", "path": "references/art-seeds.md", "layer": "chapter"},
            {"kind": "card", "dir": "references/code-genes", "layer": "code-gene"},
            {"kind": "card", "dir": "references/moods", "layer": "mood"},
        ],
        "index_md": "references/SEED-INDEX.md",
        "index_jsonl": "references/seed-index.jsonl",
        "state": "references/.seed-usage.json",
        "quota": {"chapter": 0.42, "code-gene": 0.33, "mood": 0.25},
        "decay_tau_days": 14.0,
        "count_penalty": 0.5,
        "prefix": {"chapter": "ch", "code-gene": "cg", "mood": "md"},
    },
}


def detect_profile() -> str:
    """同一个脚本文件丢进任一仓库即可工作 —— 这就是 SDK 的最小原型。"""
    if (ROOT / "references" / "art-seeds.md").exists():
        return "taste"
    if (ROOT / "references" / "math-seeds.md").exists():
        return "math"
    raise SystemExit("✗ 无法识别领域：references/ 下既没有 art-seeds.md 也没有 math-seeds.md")


# ── 基础工具 ──────────────────────────────────────────────────────────────
EMOJI = re.compile(r"^[\U0001F300-\U0001FAFF\u2600-\u27BF]+\s*")
MD_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
MD_BOLD = re.compile(r"\*\*(.+?)\*\*")
CJK_RUN = re.compile(r"[\u4e00-\u9fff]+")
ASCII_WORD = re.compile(r"[A-Za-z][A-Za-z0-9'\-\+\.]{2,}")

# 这些词在任何领域都没有区分度，或会制造假命中（任务里的「AI」≠ 条目里的 `AI:` 提示词）
STOP = {
    "the", "and", "with", "for", "style", "art", "of", "in", "to", "an", "as",
    "is", "by", "on", "from", "that", "this", "ai", "www", "http", "https",
    "使用", "以及", "一个", "可以", "需要", "任务", "问题", "方法", "工具",
    "风格", "艺术", "作品", "进行", "通过", "如果", "因为", "所以", "我们",
}
TEMPLATE_PARTS = {
    "code-gene", "code gene", "code-recipe", "scenario", "recipe",
    "情绪选种档案", "情绪档", "美学大脑", "数学大脑", "场景档",
}


def clean(text: str) -> str:
    text = MD_LINK.sub(r"\1", text)
    text = MD_BOLD.sub(r"\1", text)
    text = text.replace("`", "").strip()
    return EMOJI.sub("", text).strip()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def slugify(text: str) -> str:
    text = clean(text)
    text = re.sub(r"[（）()《》「」【】\[\]：:；;，,。.、/\\|\"'’]", " ", text)
    text = re.sub(r"\s+", "-", text.strip())
    return re.sub(r"-{2,}", "-", text).strip("-").lower()


W2, W3 = 1.0, 0.35  # 3-gram 降权：中文无词边界，3 字常跨词（「信息密度」→「息密」）


def grams(text: str) -> dict[str, float]:
    """中文 2~3 字 n-gram + 英文词 → {gram: 权重}。不分词、零依赖、跨领域通用。"""
    out: dict[str, float] = {}
    for run in CJK_RUN.findall(text):
        for i in range(len(run) - 1):
            g = run[i:i + 2]
            if g not in STOP:
                out[g] = max(out.get(g, 0.0), W2)
        for i in range(len(run) - 2):
            g = run[i:i + 3]
            if g not in STOP:
                out[g] = max(out.get(g, 0.0), W3)
    for w in ASCII_WORD.findall(text):
        w = w.lower()
        if w not in STOP:
            out[w] = max(out.get(w, 0.0), W2)
    return out


def pick_name(h1: str, fallback: str) -> str:
    """卡片 H1 → 干净名字。跳过 `code-gene` / `情绪选种档案` 这类模板段。"""
    raw = clean(h1) if h1 else fallback
    # 只切「带空格的 ·」——中文名内部常见无空格「绢色·气口·印章」，不能切碎
    parts = [p.strip() for p in re.split(r"\s+·\s+", raw) if p.strip()]
    parts = [p for p in parts if p.lower() not in TEMPLATE_PARTS]
    return parts[0] if parts else fallback


# ── 解析器 A：单行速查总库 ────────────────────────────────────────────────
TASTE_ENT = re.compile(
    r"^🎨\s*\*\*(?P<name>[^*]+?)\*\*\s*(?:（(?P<years>[^）]*)）)?\s*·?\s*"
    r"(?P<tag>[^—]*?)\s*——\s*(?P<desc>.+?)\s*$"
)
TASTE_AI = re.compile(r"^`AI:\s*(?P<kw>.+?)`")
MATH_ENT = re.compile(
    r"^🧮\s*\*\*(?P<name>[^*]+?)\*\*\s*·\s*(?P<sub>[^—]+?)\s*——\s*"
    r"(?P<desc>.+?)\s*｜\s*信号：(?P<sig>.+?)\s*｜\s*锚：(?P<anchor>.+?)\s*$"
)
GROUP_HEAD = re.compile(r"^##\s+(?P<group>[^#].*?)\s*$")


def parse_table(path: Path, layer: str, profile: str, seq0: int = 0) -> list[dict]:
    if not path.exists():
        print(f"  ! 缺文件 {path}")
        return []
    seeds: list[dict] = []
    group = ""
    pending = None
    seq = seq0
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()

        if line.startswith("## "):
            m = GROUP_HEAD.match(line)
            if m:
                group = re.split(r"[（(]", clean(m.group("group")))[0].strip()
            continue

        if profile == "taste":
            if line.startswith("`AI:") and pending is not None:
                kw = TASTE_AI.match(line)
                if kw:
                    pending["text"] += " " + clean(kw.group("kw"))
                pending["ai_line"] = True
                pending = None
                continue
            if not line.startswith("🎨"):
                continue
            m = TASTE_ENT.match(line)
            if not m:
                continue
            name = clean(m.group("name"))
            tag = clean(m.group("tag"))
            desc = clean(m.group("desc"))
            years = (m.group("years") or "").strip()
            ascii_part = re.findall(r"[A-Za-z][A-Za-z0-9'\-\s\.]{2,}", name)
            if ascii_part:
                sid = slugify(ascii_part[0])
            else:
                seq += 1
                sid = f"{seq:03d}-{slugify(name)}"
            seed = {
                "id": sid,
                "name": name,
                "layer": layer,
                "group": group,
                "one_liner": desc[:80],
                "tag": tag,
                "years": years,
                "text": f"{name} {tag} {desc} {group}",
                "ref": rel(path),
            }
            seeds.append(seed)
            pending = seed
        else:
            if not line.startswith("🧮"):
                continue
            m = MATH_ENT.match(line)
            if not m:
                continue
            name = clean(m.group("name"))
            desc = clean(m.group("desc"))
            ascii_part = re.findall(r"[A-Za-z][A-Za-z0-9'\-\.]{1,}", name)
            seq += 1
            sid = slugify(ascii_part[0]) if ascii_part else f"{seq:03d}-{slugify(name)}"
            seeds.append({
                "id": sid,
                "name": name,
                "layer": layer,
                "group": group,
                "one_liner": desc[:80],
                "sub": clean(m.group("sub")),
                "anchor": clean(m.group("anchor")),
                "text": f"{name} {clean(m.group('sub'))} {desc} {m.group('sig')} {group}",
                "ref": rel(path),
            })
    return seeds


# ── 解析器 B：卡片 ────────────────────────────────────────────────────────
H1 = re.compile(r"^#\s+(?P<h>.+)$")
QUOTE_FIELD = re.compile(r"^>\s*\*\*(?P<k>[^*]+?)\*\*\s*[（(]?[^：:）)]*[）)]?\s*[：:]\s*(?P<v>.*)$")


def parse_cards(directory: Path, layer: str) -> list[dict]:
    if not directory.is_dir():
        print(f"  ! 缺目录 {directory}")
        return []
    seeds = []
    for path in sorted(directory.glob("*.md")):
        lines = path.read_text(encoding="utf-8").splitlines()
        h1, fields = "", {}
        cur = None
        for line in lines[:60]:
            if not h1:
                m = H1.match(line)
                if m:
                    h1 = m.group("h")
                    continue
            q = QUOTE_FIELD.match(line)
            if q:
                cur = clean(q.group("k"))
                val = clean(q.group("v"))
                fields[cur] = val
                continue
            # 列表型字段：`> **问题信号**：` 下面是 `> - 条目` 或 `> 1. 条目`
            if cur and re.match(r"^>\s*(?:[-*]|\d+\.)\s+", line.lstrip(" ")):
                item = clean(re.sub(r"^>\s*(?:[-*]|\d+\.)\s+", "", line.lstrip(" ")))
                fields[cur] = (fields[cur] + " / " + item) if fields.get(cur) else item
                continue
            if line.strip() and not line.lstrip().startswith(">"):
                cur = None
        text = " ".join([clean(h1)] + [f"{k} {v}" for k, v in fields.items()])
        one = ""
        for key in ("适用产物", "适用场景", "典型任务", "覆盖工具", "问题信号", "读者该感受到", "激活词"):
            if fields.get(key):
                one = fields[key]
                break
        seeds.append({
            "id": slugify(path.stem),
            "name": pick_name(h1, path.stem),
            "layer": layer,
            "group": directory.name,
            "one_liner": one[:90],
            "text": text,
            "ref": rel(path),
        })
    return seeds


# ── 构建索引 ──────────────────────────────────────────────────────────────
# ── 增量池：agent 运行时新增的种子（不动源文件，可审计、可回滚）─────────
ADDITIONS_REL = "references/seed-additions.jsonl"


def additions_path(cfg: dict) -> Path:
    return ROOT / ADDITIONS_REL


def load_additions(cfg: dict) -> list[dict]:
    """读增量池。文件缺失 / 单行损坏都不阻塞主流程——写入路径绝不能成为新的单点故障。"""
    p = additions_path(cfg)
    if not p.exists():
        return []
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except Exception:
            continue
        if not isinstance(rec, dict) or not rec.get("name"):
            continue
        rec.setdefault("layer", "tool")
        rec.setdefault("group", "增量区")
        rec.setdefault("signals", [])
        rec.setdefault("one_liner", "")
        rec.setdefault("ref", ADDITIONS_REL)
        rec["origin"] = "addition"
        out.append(rec)
    return out


def _seed_from_addition(rec: dict, cfg: dict) -> dict:
    """把一条增量记录补全成与源库同构的种子。"""
    layer = rec["layer"]
    sid = str(rec.get("id") or slugify(rec["name"]))
    prefix = cfg["prefix"].get(layer, layer)
    if not sid.startswith(f"{prefix}-"):
        sid = f"{prefix}-{slugify(sid)}"
    text = " ".join([rec["name"], " ".join(rec.get("signals", [])), rec.get("one_liner", "")])
    return {
        "id": sid,
        "name": rec["name"],
        "layer": layer,
        "group": rec.get("group", "增量区"),
        "one_liner": rec.get("one_liner", ""),
        "text": text,
        "grams": len(grams(text)),
        "ref": rec.get("ref", ADDITIONS_REL),
        "origin": "addition",
    }


def merge_seeds(base: list[dict], additions: list[dict]) -> tuple[list[dict], int]:
    """把增量并进基础库。

    两条硬约束（增量不能毁掉历史）：
      1. **已有 ID 绝不改写** —— 否则风味日志、状态记忆、外部引用全部断链；
      2. **新 ID 撞车自动加后缀，绝不静默覆盖** —— 宁可 ID 丑陋，不可数据丢失。
    """
    merged = {s["id"]: s for s in base}
    used = set(merged)
    collided = 0
    for a in additions:
        sid = a["id"]
        if sid in used:
            n = 2
            while f"{sid}-{n}" in used:
                n += 1
            a = dict(a, id=f"{sid}-{n}")
            sid = a["id"]
            collided += 1
        merged[sid] = a
        used.add(sid)
    return sorted(merged.values(), key=lambda s: (s["layer"], s["id"])), collided


def cmd_build(cfg: dict, profile: str) -> int:
    seeds: list[dict] = []
    for src in cfg["sources"]:
        if src["kind"] == "table":
            got = parse_table(ROOT / src["path"], src["layer"], profile)
        else:
            got = parse_cards(ROOT / src["dir"], src["layer"])
        print(f"  · {(src.get('path') or src.get('dir')):<36} {len(got):>4} 粒  [{src['layer']}]")
        seeds += got

    # 加层前缀，彻底消除跨层 ID 冲突；层内重名追加序号——绝不因重名丢种子
    for s in seeds:
        s["id"] = f"{cfg['prefix'][s['layer']]}-{s['id']}"
    used: Counter = Counter()
    for s in seeds:
        base = s["id"]
        used[base] += 1
        if used[base] > 1:
            s["id"] = f"{base}-{used[base]}"

    merged: dict[str, dict] = {}
    for s in seeds:
        cur = merged.get(s["id"])
        if cur is None or len(s["text"]) > len(cur["text"]):
            merged[s["id"]] = s
    dropped = len(seeds) - len(merged)
    seeds = sorted(merged.values(), key=lambda s: (s["layer"], s["id"]))

    # 合并运行时增量池（agent 用 `add` 写入；不改源文件）
    add_seeds = [_seed_from_addition(r, cfg) for r in load_additions(cfg)]
    seeds, collided = merge_seeds(seeds, add_seeds)
    n_added = sum(1 for s in seeds if s.get("origin") == "addition")

    for s in seeds:
        s["grams"] = len(grams_cached(s["text"]))  # 只存规模，索引保持轻量

    _write_jsonl(ROOT / cfg["index_jsonl"], seeds)
    _write_flat_index(ROOT / cfg["index_md"], cfg, seeds)

    layers = Counter(s["layer"] for s in seeds)
    groups = Counter(s["group"] for s in seeds)
    print(f"\n✓ 共 {len(seeds)} 粒种子平铺完成" + (f"（合并 {dropped} 条重名）" if dropped else ""))
    print(f"  分层：{dict(layers)}")
    if n_added:
        print(f"  增量：{n_added} 粒来自 {ADDITIONS_REL}" + (f"（{collided} 个 ID 撞车已加后缀）" if collided else ""))
    print(f"  分组：{len(groups)} 个（章 / 域 / 目录）")
    print(f"  → {cfg['index_jsonl']}")
    print(f"  → {cfg['index_md']}")
    return 0


def _write_jsonl(path: Path, seeds: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for s in seeds:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")


LAYER_LABEL = {
    "chapter": "风格章档", "code-gene": "代码基因卡", "mood": "情绪档",
    "tool": "工具条目", "recipe": "模板代码卡", "scenario": "场景档",
}
LAYER_REF = {
    "chapter": "art-seeds.md", "code-gene": "code-genes/", "mood": "moods/",
    "tool": "math-seeds.md", "recipe": "recipes/", "scenario": "scenarios/",
}
LAYER_ORDER = ["mood", "scenario", "code-gene", "recipe", "chapter", "tool"]


def _write_flat_index(path: Path, cfg: dict, seeds: list[dict]) -> None:
    by_layer: dict[str, list[dict]] = defaultdict(list)
    for s in seeds:
        by_layer[s["layer"]].append(s)

    out = [
        f"# 🗂️ 种子全景索引（等距平铺 · 全员同等可见）· {cfg['label']}",
        "",
        "> **这是什么**：全库种子的**等距平铺目录**——每粒一行、同等曝光、没有「首选 / 备选」的层级差。",
        "> **为什么不用旧的「按需查询」**：人工索引表只有 10~12 行，结构性地让 95% 的种子永远没入口。",
        "> **怎么用**：机器选 → `python3 scripts/seed_brain.py match \"<任务描述>\"`（IDF 加权 top-K）；",
        "> 人/LLM 通读 → 本文件全文，按信号词自行判断归属。",
        "> **排序**：按层、层内按 ID 字典序——**刻意不按重要性**，杜绝任何隐含优先级。",
        f"> **规模**：{len(seeds)} 粒 ｜ " + " ｜ ".join(
            f"{LAYER_LABEL.get(k, k)} {len(v)}" for k, v in by_layer.items()
        )
        + (f" ｜ 🌱 增量 {sum(1 for s in seeds if s.get('origin') == 'addition')} 粒"
           if any(s.get("origin") == "addition" for s in seeds) else ""),
        "> **🌱 增量区**：带 🌱 的条目来自 `references/seed-additions.jsonl`（agent 运行时用 `seed_brain.py add` 写入）。",
        "> 它们与源库种子**同权参与匹配**，不因「新」而优先，也不因「未回填源文件」而低一等。",
        "",
        "---",
        "",
    ]

    for layer in LAYER_ORDER:
        items = by_layer.get(layer)
        if not items:
            continue
        out.append(f"## {LAYER_LABEL.get(layer, layer)}（{len(items)} 粒）")
        out.append("")
        out.append(f"目录：[`{LAYER_REF.get(layer, layer)}`]({LAYER_REF.get(layer, layer)})")
        out.append("")
        out.append("| id | 名称 | 一句话 |")
        out.append("|---|---|---|")
        for s in items:
            one = s["one_liner"].replace("|", "／")
            mark = "🌱 " if s.get("origin") == "addition" else ""
            out.append(f"| `{s['id']}` | {mark}{s['name']} | {one} |")
        out.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


# ── 匹配 ──────────────────────────────────────────────────────────────────
def load_seeds(cfg: dict) -> list[dict]:
    p = ROOT / cfg["index_jsonl"]
    if not p.exists():
        raise SystemExit("✗ 索引不存在：先跑 `python3 scripts/seed_brain.py build`")
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def load_state(cfg: dict) -> dict:
    p = ROOT / cfg["state"]
    if not p.exists():
        return {"picks": {}}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {"picks": {}}  # 状态损坏时优雅退化，绝不阻塞主流程


def save_state(cfg: dict, state: dict) -> None:
    p = ROOT / cfg["state"]
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_idf(seeds: list[dict]) -> dict[str, float]:
    df: Counter = Counter()
    for s in seeds:
        df.update(grams_cached(s["text"]).keys())
    n = max(1, len(seeds))
    return {g: math.log(1 + n / (1 + c)) for g, c in df.items()}


def novelty(rec: dict | None, cfg: dict) -> float:
    """刚用过 → 下沉；久未用 → 回升；从未用 → 1.0。

    这是多样性的唯一来源，刻意不用随机数：
    合适性由 IDF 决定（确定、可解释、可复现），重复度由时间衰减决定（自然轮转）。
    """
    if not rec:
        return 1.0
    days = max(0.0, (time.time() - rec.get("last_ts", 0)) / 86400.0)
    recovery = 1.0 - math.exp(-days / cfg["decay_tau_days"])
    count_pen = 1.0 / (1.0 + cfg["count_penalty"] * math.log1p(rec.get("count", 0)))
    return max(0.15, recovery) * count_pen


MAX_HITS = 5


_GRAM_CACHE: dict[str, dict[str, float]] = {}


def grams_cached(text: str) -> dict[str, float]:
    """同一文本只切一次 gram。测试套件会反复扫描全库（374 粒 × N 次对照），
    没有这层缓存，T4 的证伪实验要跑半分钟以上。"""
    g = _GRAM_CACHE.get(text)
    if g is None:
        g = _GRAM_CACHE[text] = grams(text)
    return g


def score_seed(seed: dict, task_grams: dict[str, float],
               idf: dict[str, float] | None) -> tuple[float, list[tuple[str, float]]]:
    """idf=None 时退化为均匀权重（仅供测试对照：证明 IDF 确实提供了区分度）。"""
    sg = grams_cached(seed["text"])
    common = set(task_grams) & set(sg)
    if not common:
        return 0.0, []
    weights = sorted(
        ((g, (idf.get(g, 1.0) if idf else 1.0) * min(sg[g], task_grams[g])) for g in common),
        key=lambda x: -x[1],
    )[:MAX_HITS]
    raw = sum(w for _, w in weights)
    # 温和归一：只压一点点长文本优势。用 sqrt 会把 chapter 层（文本长）整体压死，
    # 反而摧毁「平等摊开」——长文本信息量大，理应更容易相关。
    norm = raw / (1.0 + math.log1p(seed.get("grams", 1)) / 10.0)
    return norm, weights


def rank(cfg: dict, task: str, k: int = 8, *, state: dict | None = None,
         seeds: list[dict] | None = None, idf: dict[str, float] | None = None,
         use_idf: bool = True) -> tuple[list[tuple], dict[str, int], int]:
    """纯函数版检索：CLI 与测试共用同一条代码路径（测试不得另写影子实现）。

    返回 (top_rows, quotas, 命中数)。top_rows 每项 = (total, seed, hits, novelty, base)。
    """
    seeds = seeds if seeds is not None else load_seeds(cfg)
    idf = idf if idf is not None else build_idf(seeds)
    picks = (state if state is not None else load_state(cfg)).get("picks", {})
    task_grams = grams(task)

    scored = []
    for s in seeds:
        base, hits = score_seed(s, task_grams, idf if use_idf else None)
        if base <= 0:
            continue
        nv = novelty(picks.get(s["id"]), cfg)
        scored.append((base * nv, s, hits, nv, base))
    scored.sort(key=lambda x: -x[0])

    # 配额是「下限」而不只是「上限」：
    # 旧实现只防「某层超配额」，却不保「某层有货却拿不到位」——
    # 按分数单次扫到底，弱层的候选常排在 K 之外，等于配了白配。
    # 现在两阶段：先按层保底（层内最优），再按全局分数补满 K。
    quotas = {L: max(1, math.floor(k * q)) for L, q in cfg["quota"].items()}
    while sum(quotas.values()) > k:
        biggest = max(quotas, key=lambda x: quotas[x])
        if quotas[biggest] <= 1:
            break
        quotas[biggest] -= 1

    taken, idx_taken = [], set()
    for layer, q in quotas.items():
        picked = 0
        for i, row in enumerate(scored):
            if i in idx_taken or row[1]["layer"] != layer:
                continue
            taken.append(row)
            idx_taken.add(i)
            picked += 1
            if picked >= q:
                break
    for i, row in enumerate(scored):
        if len(taken) >= k:
            break
        if i not in idx_taken:
            taken.append(row)
            idx_taken.add(i)
    taken.sort(key=lambda x: -x[0])
    return taken[:k], quotas, len(scored)


def cmd_match(cfg: dict, task: str, k: int) -> int:
    seeds = load_seeds(cfg)
    idf = build_idf(seeds)
    taken, quotas, n_hit = rank(cfg, task, k, seeds=seeds, idf=idf)

    print(f"\n任务：{task}")
    print(f"扫描 {len(seeds)} 粒全库 ｜ 命中 {n_hit} ｜ IDF 加权 ｜ 跨层配额 "
          + " ".join(f"{k2}<={v}" for k2, v in quotas.items())
          + f" ｜ 衰减 {cfg['decay_tau_days']:.0f}d\n")
    if not taken:
        print("  （零命中）该表述未覆盖任何种子文本 —— 换更具体的领域词，")
        print("   或直接通读 references/SEED-INDEX.md 的人工全景表。")
        return 0

    print(f"{'#':>2}  {'层':<10}{'得分':>7} {'新颖':>5}  {'id':<26} 命中 n-gram (idf)")
    print("─" * 104)
    for i, (total, s, hits, nv, base) in enumerate(taken, 1):
        # 去冗余展示：短 gram 若被同批命中的长 gram 包含则隐去（保留「条件数」隐去「件数」）
        hi = {g for g, _ in hits}
        disp = [(g, w) for g, w in hits if not any(g != h and g in h for h in hi)][:5]
        h = "  ".join(f"{g}·{w:.1f}" for g, w in disp)
        print(f"{i:>2}  {s['layer']:<10}{total:>7.1f} {nv:>5.2f}  {s['id'][:25]:<26} {h}")
        print(f"    └ {s['name']} ｜ {s['one_liner'][:62]}")
        print(f"      深挖 {s['ref']}")
    print("\n下一步：挑定一个 → 读 ref 深挖 → 交付后 `pick <id>` 记入状态")
    return 0


def find_duplicate(seeds: list[dict], cand: dict, threshold: float = 0.75) -> tuple[dict | None, float]:
    """同层内按**包含度**找最相似的已有种子（纯函数，供 cmd_add 与测试套件共用）。

    用包含度而不是 Jaccard：新种子通常只有名字 + 几个信号（短），
    已有卡片文本很长，Jaccard 会被并集惩罚到永远不告警。
    """
    cg = set(grams_cached(cand["text"]))
    best, best_j = None, 0.0
    for s in seeds:
        if s["layer"] != cand["layer"]:
            continue
        sg = set(grams_cached(s["text"]))
        j = len(cg & sg) / (min(len(cg), len(sg)) or 1)
        if j > best_j:
            best, best_j = s, j
    return (best if best_j >= threshold else None), best_j


def cmd_add(cfg: dict, args) -> int:
    """把一粒新种子写进增量池 —— agent 在会话中发现新工具/新风格时的唯一正确入口。

    为什么不直接改源文件：
      • 源库是人工策展产物（CONTRIBUTING.md 有分层与格式硬约束），脚本盲插会破坏格式；
      • 增量池可审计、可回滚、可批量审阅后再回填；
      • 回填后从增量池删除即可，build 结果不变（幂等）。
    """
    layer = args.layer
    if layer not in cfg["prefix"]:
        print(f"✗ 未知层：{layer}；本领域可选 {sorted(cfg['prefix'])}")
        return 1
    name = (args.name or "").strip()
    if not name:
        print("✗ --name 不能为空")
        return 1
    signals = [x.strip() for x in re.split(r"[,，、·/|]", args.signals or "") if x.strip()]
    if not signals:
        print("⚠ 未提供 --signals：新种子将只能靠名字命中，召回率会明显偏低。")

    # ref 存在性校验：agent 最容易猜错的就是「深挖路径」——
    # 存进索引后就是一条静默的断链（T1c 会报，但那时已污染库）。
    ref = (args.ref or "").strip() or ADDITIONS_REL
    if not (ROOT / ref).exists() and not args.force:
        print(f"✗ --ref 指向的文件不存在：{ref}")
        print("  深挖路径必须是仓库内已存在的文件（不要写猜测路径）；")
        print("  确实要留空引用请加 --force。")
        return 2

    rec = {
        "name": name,
        "layer": layer,
        "signals": signals,
        "one_liner": (args.one_liner or "").strip(),
        "ref": ref,
        "added_at": time.strftime("%Y-%m-%d"),
        "origin": "addition",
    }
    if args.id:
        rec["id"] = args.id
    cand = _seed_from_addition(rec, cfg)

    seeds = load_seeds(cfg) if (ROOT / cfg["index_jsonl"]).exists() else []
    if any(s["id"] == cand["id"] for s in seeds) and not args.force:
        print(f"✗ ID 已存在：{cand['id']}（确认要新增请加 --force，会自动加后缀）")
        return 2

    # 查重：只在同层内比，用**包含度**而非 Jaccard ——
    # 新种子通常只有名字 + 几个信号（短），已有卡片文本很长，
    # Jaccard 会被并集惩罚到永远不告警；包含度才是「这粒是不是已有那粒的别名」。
    if seeds:
        dup, sim = find_duplicate(seeds, cand)
        if dup and not args.force:
            print(f"⚠ 疑似重复：{dup['id']}（{dup['name']}）包含度={sim:.2f} ≥ 0.75")
            print("  确认是新种子请加 --force；否则先复用已有那粒。")
            return 2

    if layer == "code-gene" and not args.force:
        print("ℹ 注意：增量池里的 code-gene 只是「可检索条目」，不是合规的代码基因卡。")
        print("  要成为正式卡需满足 CONTRIBUTING.md §四：五基因齐备 + CSS 变量块 + 反模式清单")
        print("  + 配演示页并通过 qa_style.py 断言。（仍要继续写增量池请加 --force）")
        return 2

    if args.dry_run:
        print(json.dumps({**rec, "resolved_id": cand["id"]}, ensure_ascii=False, indent=2))
        print("\n(dry-run：未写入)")
        return 0

    p = additions_path(cfg)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"✓ 已写入增量池 {ADDITIONS_REL}")
    print(f"  {cand['id']} ｜ {name} ｜ layer={layer} ｜ signals={signals}")
    print("\n重建索引 …")
    return cmd_build(cfg, detect_profile())


def cmd_pick(cfg: dict, sid: str, score: int, note: str) -> int:
    seeds = {s["id"]: s for s in load_seeds(cfg)}
    if sid not in seeds:
        near = [k for k in seeds if sid in k or sid.split("-")[-1] in k][:6]
        print(f"✗ 未知 id：{sid}")
        print(f"  相近：{', '.join(near) if near else '无（先跑 match 拿 id）'}")
        return 1
    state = load_state(cfg)
    picks = state.setdefault("picks", {})
    rec = picks.setdefault(sid, {"count": 0, "last_ts": 0, "scores": []})
    rec["count"] += 1
    rec["last_ts"] = time.time()
    if score:
        rec["scores"] = (rec.get("scores", []) + [score])[-20:]
    if note:
        rec["note"] = note[:200]
    rec["name"] = seeds[sid]["name"]
    rec["layer"] = seeds[sid]["layer"]
    save_state(cfg, state)
    print(f"✓ 已记录 {sid}（{seeds[sid]['name']}）第 {rec['count']} 次")
    print(f"  → {cfg['state']} ｜ {cfg['decay_tau_days']:.0f}d 衰减窗口内会自然下沉")
    return 0


def cmd_stats(cfg: dict) -> int:
    seeds = load_seeds(cfg)
    picks = load_state(cfg).get("picks", {})
    total = len(seeds)
    used = [s for s in seeds if s["id"] in picks]

    print(f"\n{cfg['label']} · 覆盖率审计")
    print(f"全库 {total} 粒 ｜ 曾使用 {len(used)} 粒 ｜ 覆盖率 {100*len(used)/max(1,total):.1f}%")

    by_layer = defaultdict(lambda: [0, 0])
    for s in seeds:
        by_layer[s["layer"]][0] += 1
        if s["id"] in picks:
            by_layer[s["layer"]][1] += 1
    print("\n分层：")
    for L, (t, u) in sorted(by_layer.items()):
        print(f"  {L:<11}{u:>4}/{t:<4} {'█'*int(24*u/max(1,t)):<24} {100*u/max(1,t):>5.1f}%")

    by_group = defaultdict(lambda: [0, 0])
    for s in seeds:
        by_group[s["group"]][0] += 1
        if s["id"] in picks:
            by_group[s["group"]][1] += 1
    blind = [(g, t) for g, (t, u) in by_group.items() if u == 0]
    print(f"\n零使用分组：{len(blind)}/{len(by_group)}")
    for g, t in blind[:12]:
        print(f"  · {g[:44]}（{t} 粒，全未用过）")
    if len(blind) > 12:
        print(f"  … 还有 {len(blind)-12} 个")

    top = sorted(picks.items(), key=lambda kv: -kv[1].get("count", 0))[:8]
    if top:
        print("\n复用最多（警惕正反馈收敛）：")
        for sid, r in top:
            print(f"  {r.get('count',0):>2}× {sid:<28}{r.get('name','')[:30]}")
    return 0


# ── CLI ───────────────────────────────────────────────────────────────────
def main() -> int:
    ap = argparse.ArgumentParser(description="种子大脑无偏检索层")
    ap.add_argument("--profile", choices=sorted(PROFILES), help="默认自动识别")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build", help="解析总库 → 等距平铺索引")
    m = sub.add_parser("match", help="任务描述 → top-K 候选")
    m.add_argument("task")
    m.add_argument("--k", type=int, default=8)
    p = sub.add_parser("pick", help="记录一次使用")
    p.add_argument("id")
    p.add_argument("--score", type=int, default=0, choices=[0, 1, 2, 3, 4, 5])
    p.add_argument("--note", default="")
    sub.add_parser("stats", help="覆盖率审计")
    a = sub.add_parser("add", help="新增一粒种子到增量池（不改源文件）")
    a.add_argument("--name", required=True)
    a.add_argument("--layer", required=True,
                   help="美学：chapter|code-gene|mood；数学：tool|recipe|scenario")
    a.add_argument("--signals", default="", help="逗号/顿号分隔的触发信号（强烈建议给）")
    a.add_argument("--one-liner", dest="one_liner", default="")
    a.add_argument("--ref", default="", help="深挖路径（默认指向增量池自身）")
    a.add_argument("--id", default="", help="自定义 id（默认由名字生成）")
    a.add_argument("--force", action="store_true", help="跳过重复/重名告警")
    a.add_argument("--dry-run", dest="dry_run", action="store_true")

    args = ap.parse_args()
    profile = args.profile or detect_profile()
    cfg = PROFILES[profile]
    print(f"▸ seed_brain v{__version__}  profile={profile}  root={ROOT}")

    if args.cmd == "build":
        return cmd_build(cfg, profile)
    if args.cmd == "match":
        return cmd_match(cfg, args.task, args.k)
    if args.cmd == "pick":
        return cmd_pick(cfg, args.id, args.score, args.note)
    if args.cmd == "stats":
        return cmd_stats(cfg)
    if args.cmd == "add":
        return cmd_add(cfg, args)
    return 1


if __name__ == "__main__":
    sys.exit(main())
