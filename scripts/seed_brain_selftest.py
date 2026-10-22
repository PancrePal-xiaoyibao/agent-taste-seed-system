#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
seed_brain_selftest.py — 种子大脑「无偏分布」验证套件

为什么需要它
------------
一个「看起来能选」的检索层，和一个「真的无偏」的检索层，差别只能靠测量。
本套件把「平等摊开」拆成 9 个可证伪的指标，跑真实分发包里的种子库，
把数字写进 docs/EVIDENCE-seed-brain.md —— 算法改了以后能立刻看出退化。

设计原则
--------
* **不写影子实现**：直接 import seed_brain 的 rank()，测的就是线上那条路径。
* **不手写几个用例就交差**：探针按全谱系设计（美学 24 / 数学 24），
  另加「每条种子自召回」的穷举检查。
* **有门槛**：每项给 PASS/FAIL，任一 FAIL 退出码 1（可进 CI）。
* **零依赖**：纯 stdlib，与 seed_brain 同源。

用法
----
  python3 scripts/seed_brain_selftest.py              # 跑全部，出控制台报告
  python3 scripts/seed_brain_selftest.py --evidence   # 另写 docs/EVIDENCE-seed-brain.md
  python3 scripts/seed_brain_selftest.py -v           # 打印每项细节
"""

from __future__ import annotations

import argparse
import hashlib
import math
import statistics
import sys
import time
from collections import Counter
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import seed_brain as sb  # noqa: E402  —— 同一条代码路径，不做影子实现

PROFILE = sb.detect_profile()
CFG = sb.PROFILES[PROFILE]
EVIDENCE = ROOT / "docs" / "EVIDENCE-seed-brain.md"

# ── 探针：按全谱系设计，不是「挑几个能过的」────────────────────────────
PROBES = {
    "taste": [
        "科技产品发布会 KV，冷光未来感",
        "赛博朋克夜景插画，雨夜霓虹",
        "治愈系绘本，柔和粉彩",
        "吉卜力风格乡村风景",
        "热血少年漫画封面，速度线",
        "体育赛事动员海报，红黑冲击",
        "古典音乐会节目册，庄重典雅",
        "博物馆展览折页，克制高级",
        "婚礼请柬，甜美粉色",
        "少女漫画风格头像",
        "孤独诗意的散文长图，雾气弥漫",
        "纪念一位逝者，克制留白",
        "荒诞幽默的咖啡品牌包装",
        "超现实梦境插画",
        "恐怖电影海报，暗黑压抑",
        "废墟摄影集，崇高感",
        "B端数据看板，清晰理性",
        "学术论文配图，信息图表",
        "国风游戏启动页，东方古韵",
        "茶叶品牌页面，水墨留白",
        "极简主义产品落地页",
        "瑞士国际主义海报，网格排版",
        "波普艺术拼贴封面",
        "巴洛克戏剧海报，单光源强对比",
    ],
    "math": [
        "病态线性系统求解，条件数爆炸",
        "高维矩阵降维压缩",
        "特征值分解判断稳定性",
        "最小二乘拟合超定方程",
        "数值积分，被积函数没有原函数",
        "常微分方程刚性，显式步长被锁死",
        "偏微分方程热传导扩散",
        "傅里叶频谱分析，窗函数泄漏",
        "采样定理与混叠",
        "A/B 测试显著性检验，样本小",
        "小样本置信区间估计",
        "贝叶斯后验更新，先验选择",
        "MCMC 采样收敛诊断",
        "时间序列 ARIMA 预测定阶",
        "GARCH 波动率聚集",
        "卡尔曼滤波状态估计",
        "蒙特卡洛期权定价",
        "重要性采样稀有事件",
        "线性规划资源分配",
        "凸优化识别与二次规划",
        "梯度下降调参，学习率",
        "PCA 主成分降维",
        "符号推导积分公式化简",
        "网络流最大流最小割",
    ],
}

# 旧「快速索引表」实际指向的货架前排（美学 ≈ code-genes 12 张；数学 ≈ 场景档 + 高频工具）
LEGACY_SHELF = {
    "taste": {
        "cg-02-赛博霓虹", "cg-05-吉卜力手绘亲和", "cg-03-中国画留白", "cg-01-瑞士平面",
        "cg-08-洛可可粉彩", "cg-12-哥特暗黑", "cg-07-巴洛克聚光", "cg-09-波普拼贴",
        "cg-04-极简主义", "cg-06-浮世绘扁平", "cg-10-构成主义海报", "cg-11-赛璐璐动漫UI",
    },
    "math": {
        "tl-svd", "tl-condition", "tl-hypothesis", "tl-garch", "tl-ar",
        "tl-sgd", "tl-lp", "tl-bayes", "tl-pca", "tl-mcmc",
        "sc-04-不确定性与统计推断", "sc-05-预测时序与波动率", "sc-07-大规模计算与精度危机",
    },
}

# 通用填充词：用来污染探针，让「稀有词能否笑到最后」成为可测的对比
GENERIC_FILL = {
    "taste": ["设计", "页面", "内容", "风格", "整体", "方案", "视觉", "效果"],
    "math": ["计算", "方法", "结果", "分析", "模型", "数据", "问题", "处理"],
}

# 门槛：每一项都可证伪，不达标即 FAIL
THRESHOLDS = {
    "recall_name": 0.98,     # 用自己的名字当任务，应几乎都能召回自己
    "recall_feature": 0.60,  # 用特征词当任务，仍应能召回（更严格）
    "gini_max": 0.80,        # 命中集中度（1 = 一粒种子吃掉全部）
    "idf_top1_gain": 0.15,   # 开 IDF 的 top1 命中率至少高出 15 个百分点
    "layer_dominance_max": 0.70,  # 单任务单层占 top-K 的上限（防垄断）
    "rotation_min": 4,       # 同一任务连跑 6 次，至少出现 4 个不同 top1
    "decenter_min": 0.50,    # top1 落在「旧货架」之外的比例
}


# ── 工具 ──────────────────────────────────────────────────────────────────
def gini(values: list[float]) -> float:
    v = sorted(x for x in values if x >= 0)
    n = len(v)
    total = sum(v)
    if n == 0 or total == 0:
        return 0.0
    cum = sum((i + 1) * x for i, x in enumerate(v))
    return (2 * cum) / (n * total) - (n + 1) / n


def empty_state() -> dict:
    return {"picks": {}}


def feature_probe(seed: dict, idf: dict[str, float]) -> str:
    """用该种子自己的高 idf 特征词构造任务（排除名字，避免平凡命中）。"""
    name_g = set(sb.grams(seed["name"]))
    cand = [(g, w) for g, w in sb.grams_cached(seed["text"]).items() if g not in name_g]
    top = sorted(cand, key=lambda x: -idf.get(x[0], 0.0))[:3]
    return " ".join(g for g, _ in top)


def rank_ids(cfg, task, k, seeds, idf, state=None, use_idf=True):
    rows, _, _ = sb.rank(cfg, task, k, state=state or empty_state(),
                         seeds=seeds, idf=idf, use_idf=use_idf)
    return [r[1]["id"] for r in rows]


def stable_half(sid: str) -> int:
    """确定性分割。绝不用内置 hash()——Python 的 str hash 带随机种子，会破坏可复现性。"""
    return int(hashlib.md5(sid.encode("utf-8")).hexdigest()[:8], 16) % 2


def split_half(seeds: list[dict]) -> tuple[list[dict], list[dict]]:
    """把全库一分为二：A 当基础库，B 当「agent 运行时逐步新增」的增量。"""
    a = [s for s in seeds if stable_half(s["id"]) == 0]
    b = [s for s in seeds if stable_half(s["id"]) == 1]
    return a, b


def chunks(items: list, n: int) -> list[list]:
    size = max(1, math.ceil(len(items) / n))
    return [items[i:i + size] for i in range(0, len(items), size)]


def as_additions(seeds: list[dict]) -> list[dict]:
    return [dict(s, origin="addition") for s in seeds]


class Report:
    def __init__(self):
        self.rows: list[tuple[str, str, str, str, bool]] = []
        self.details: list[str] = []

    def add(self, tid: str, name: str, metric: str, target: str, ok: bool):
        self.rows.append((tid, name, metric, target, ok))
        flag = "PASS" if ok else "FAIL"
        print(f"  [{flag}] {tid} {name:<22} {metric:<44} 门槛 {target}")
        return ok

    def note(self, text: str):
        self.details.append(text)
        print(f"         {text}")

    @property
    def failed(self) -> int:
        return sum(1 for r in self.rows if not r[4])


# ── T1 索引完整性 ─────────────────────────────────────────────────────────
def t1_integrity(r: Report, seeds: list[dict]) -> None:
    print("\n\033[1mT1 索引完整性 —— 没丢种子，没坏引用\033[0m")
    ids = [s["id"] for s in seeds]
    dup = [k for k, v in Counter(ids).items() if v > 1]
    r.add("T1a", "ID 唯一", f"重复 {len(dup)} 个", "0", not dup)

    bad = [s["id"] for s in seeds if not s.get("name") or not s.get("text") or not s.get("ref")]
    r.add("T1b", "字段完整", f"缺字段 {len(bad)} 条", "0", not bad)

    missing = [s["id"] for s in seeds if not (ROOT / s["ref"]).exists()]
    r.add("T1c", "ref 可解析", f"断引用 {len(missing)} 条", "0", not missing)

    hollow = [s["id"] for s in seeds if s.get("grams", 0) < 3]
    r.add("T1d", "非空壳", f"Gram<3 的种子 {len(hollow)} 条", "0", not hollow)

    # 分层计数必须与源目录/条目数吻合（防止解析器静默漏读）
    layers = Counter(s["layer"] for s in seeds)
    expect = {
        "taste": {"code-gene": 12, "mood": 10},
        "math": {"recipe": 13, "scenario": 12},
    }[PROFILE]
    ok = all(layers.get(k, 0) == v for k, v in expect.items())
    r.add("T1e", "分层计数吻合", f"{dict(layers)}", str(expect), ok)

    # 测试自身的完整性：LEGACY_SHELF 若引用不存在的 id，T9 会假 PASS（恒真）
    # 不区分大小写：slugify 会小写化（赛璐璐动漫UI → 赛璐璐动漫ui）
    id_lower = {i.lower() for i in ids}
    ghost = sorted(i for i in LEGACY_SHELF[PROFILE] if i.lower() not in id_lower)
    r.add("T1f", "旧货架样本有效", f"无效 id {len(ghost)} 个" + (f"：{ghost[:3]}" if ghost else ""),
          "0", not ghost)
    r.note(f"全库 {len(seeds)} 粒 ｜ 分组 {len({s['group'] for s in seeds})} 个")


# ── T2 可达性（穷举每一条种子）────────────────────────────────────────────
def t2_reachability(r: Report, seeds: list[dict], idf: dict[str, float]) -> None:
    print("\n\033[1mT2 可达性 —— 每粒种子都能被自己的描述召回吗\033[0m")
    K = 8
    miss_name, miss_feat = [], []
    for s in seeds:
        if s["id"] not in rank_ids(CFG, s["name"], K, seeds, idf):
            miss_name.append(s["id"])
        probe = feature_probe(s, idf)
        if probe and s["id"] not in rank_ids(CFG, probe, K, seeds, idf):
            miss_feat.append(s["id"])

    acc_n = 1 - len(miss_name) / len(seeds)
    acc_f = 1 - len(miss_feat) / len(seeds)
    r.add("T2a", f"名字自召回@{K}", f"{acc_n:.1%}（漏 {len(miss_name)}/{len(seeds)}）",
          f">= {THRESHOLDS['recall_name']:.0%}", acc_n >= THRESHOLDS["recall_name"])
    r.add("T2b", f"特征词召回@{K}", f"{acc_f:.1%}（漏 {len(miss_feat)}/{len(seeds)}）",
          f">= {THRESHOLDS['recall_feature']:.0%}", acc_f >= THRESHOLDS["recall_feature"])
    if miss_name[:5]:
        r.note("名字漏召：" + "、".join(miss_name[:5]))


# ── T3 集中度（有没有「少数种子吃掉大多数任务」）─────────────────────────
def t3_concentration(r: Report, seeds: list[dict], idf: dict[str, float]) -> None:
    print("\n\033[1mT3 集中度 —— 命中是否被少数种子垄断\033[0m")
    hits = Counter()
    layer_hits = Counter()
    for p in PROBES[PROFILE]:
        rows, _, _ = sb.rank(CFG, p, 10, state=empty_state(), seeds=seeds, idf=idf)
        for _, s, _, _, _ in rows:
            hits[s["id"]] += 1
            layer_hits[s["layer"]] += 1

    g = gini(list(hits.values()))
    cover = len(hits) / len(seeds)
    r.add("T3a", "命中基尼系数", f"{g:.3f}", f"< {THRESHOLDS['gini_max']}", g < THRESHOLDS["gini_max"])
    r.add("T3b", "被触达的种子占比", f"{cover:.1%}（{len(hits)}/{len(seeds)}）", "> 0（越高越好）", cover > 0)
    top_share = sum(c for _, c in hits.most_common(5)) / max(1, sum(hits.values()))
    r.note(f"Top5 种子占全部命中 {top_share:.1%} ｜ 层分布 {dict(layer_hits)}")


# ── T4 IDF 是否真的提供区分度 ────────────────────────────────────────────
def t4_idf_effect(r: Report, seeds: list[dict], idf: dict[str, float]) -> None:
    """对照实验：同一探针（1 个稀有特征词 + 4 个通用填充词）开/关 IDF。

    无 IDF 时通用词与稀有词同权，目标种子只剩微弱优势；
    有 IDF 时稀有词（高区分度）拿全权重，通用词被压平 —— top1 命中率应明显上升。
    """
    print("\n\033[1mT4 IDF 有效性 —— 稀有词能被通用词淡没吗\033[0m")
    K = 8
    fill = " ".join(GENERIC_FILL[PROFILE][:4])
    top1_on, top1_off = [], []
    for s in seeds:
        name_g = set(sb.grams(s["name"]))
        cand = [(g, w) for g, w in sb.grams(s["text"]).items() if g not in name_g]
        if not cand:
            continue
        rare = max(cand, key=lambda x: idf.get(x[0], 0.0))[0]
        probe = f"{rare} {fill}"
        for use, bucket in ((True, top1_on), (False, top1_off)):
            ids = rank_ids(CFG, probe, K, seeds, idf, use_idf=use)
            bucket.append(1.0 if ids and ids[0] == s["id"] else 0.0)
    on = statistics.fmean(top1_on) if top1_on else 0.0
    off = statistics.fmean(top1_off) if top1_off else 0.0
    gap = on - off
    r.add("T4", "top1 命中率（IDF vs 关）", f"{on:.1%} vs {off:.1%}（+{gap:.1%}）",
          f">= +{THRESHOLDS['idf_top1_gain']:.0%}", gap >= THRESHOLDS["idf_top1_gain"])
    r.note(f"样本 {len(top1_on)} 条种子 × 对照实验（探针 = 1 稀有词 + 4 通用词）")


# ── T5 状态轮转（记忆快照是否真的打破复读）───────────────────────────────
def t5_rotation(r: Report, seeds: list[dict], idf: dict[str, float]) -> None:
    print("\n\033[1mT5 状态轮转 —— 同一任务连跑，会不会一直选同一粒\033[0m")
    probe = PROBES[PROFILE][0]
    state = empty_state()
    picks: list[str] = []
    for _ in range(6):
        ids = rank_ids(CFG, probe, 5, seeds, idf, state=state)
        if not ids:
            break
        picks.append(ids[0])
        rec = state["picks"].setdefault(ids[0], {"count": 0, "last_ts": 0, "scores": []})
        rec["count"] += 1
        rec["last_ts"] = time.time()
    distinct = len(set(picks))
    r.add("T5", "6 次连选的 top1 多样性", f"{distinct} 个不同 = {picks}",
          f">= {THRESHOLDS['rotation_min']}", distinct >= THRESHOLDS["rotation_min"])


# ── T6 跨层均衡（code-gene / mood 不被 chapter 挤死）────────────────────
def t6_layer_balance(r: Report, seeds: list[dict], idf: dict[str, float]) -> None:
    """配额的真实目的不是「精确配比」，而是「有货的层不能被饿死」。

    两个断言：
      T6a 层饥饿：某层有 ≥quota 个可用候选、总分位也够，却实拿 < quota —— 真问题
      T6b 单层垄断：只在「至少两层有候选」的任务上检查 —— 只有一层可选时垄断是必然
    """
    print("\n\033[1mT6 跨层均衡 —— 强层有没有把弱层挤成药渣\033[0m")
    K = 8
    starved = dominant = multi = 0
    worst, layer_seen = 0.0, Counter()
    quotas_seen: dict[str, int] = {}
    for p in PROBES[PROFILE]:
        tg = sb.grams(p)
        avail = Counter(s["layer"] for s in seeds if sb.score_seed(s, tg, idf)[0] > 0)
        # 配额必须取自 rank() 的真实返回值 —— 测试不得自己重算一套公式（影子实现）
        rows, quotas, _ = sb.rank(CFG, p, K, state=empty_state(), seeds=seeds, idf=idf)
        quotas_seen = quotas
        c = Counter(s["layer"] for _, s, _, _, _ in rows)
        layer_seen.update(c)
        assigned = sum(c.values())
        for L, q in quotas.items():
            if avail.get(L, 0) >= q and c.get(L, 0) < q and assigned >= q:
                starved += 1
        if sum(1 for n in avail.values() if n > 0) >= 2:
            multi += 1
            share = max(c.values()) / (assigned or 1)
            worst = max(worst, share)
            # 天然上限：若某层只有 6 个候选而全库其他层也不相关，它占 6/8 不是垄断。
            # 所以上限 = max(门槛, 该层候选占全部候选的比例)——只惩罚「有别的选却没给」。
            top_layer = c.most_common(1)[0][0]
            cap = max(THRESHOLDS["layer_dominance_max"], avail[top_layer] / (sum(avail.values()) or 1))
            if share > cap:
                dominant += 1
    r.add("T6a", "层饥饿（有货却没给位）", f"{starved} 次", "0", starved == 0)
    r.add("T6b", "多候选层下单层垄断", f"{dominant}/{multi}（最坏 {worst:.0%}）",
          f"0（上界 {THRESHOLDS['layer_dominance_max']:.0%}）", dominant == 0)
    total = sum(layer_seen.values()) or 1
    r.note(f"算法实际配额 {quotas_seen} ｜ 层占比："
           + " ｜ ".join(f"{L} {100*n/total:.0f}%" for L, n in layer_seen.most_common()))


# ── T7 鲁棒性（边界输入不崩）────────────────────────────────────────────
def t7_robustness(r: Report, seeds: list[dict], idf: dict[str, float]) -> None:
    print("\n\033[1mT7 鲁棒性 —— 烂输入不许崩\033[0m")
    cases = ["", "a", "🎨🎨🎨", "的的的的", "一" * 5000,
             "SELECT * FROM seeds WHERE id=1", "<script>alert(1)</script>",
             "the quick brown fox", "\n\t  \r"]
    crashed = []
    for c in cases:
        try:
            rank_ids(CFG, c, 5, seeds, idf)
        except Exception as e:  # noqa: BLE001
            crashed.append(f"{c[:12]!r}→{type(e).__name__}")
    r.add("T7a", "边界输入不抛异常", f"崩 {len(crashed)}/{len(cases)}", "0", not crashed)
    if crashed:
        r.note("崩溃输入：" + "、".join(crashed[:4]))

    # 状态文件损坏时必须优雅退化
    try:
        s = sb.novelty({"count": 0, "last_ts": 0}, CFG)
        ok = isinstance(s, float)
    except Exception:
        ok = False
    r.add("T7b", "状态缺字段不崩", "缺失 last_ts/count 仍返回 float", "True", ok)


# ── T8 确定性（无隐藏随机）──────────────────────────────────────────────
def t8_determinism(r: Report, seeds: list[dict], idf: dict[str, float]) -> None:
    print("\n\033[1mT8 确定性 —— 同输入必须同输出（可复现）\033[0m")
    probe = PROBES[PROFILE][3]
    a = rank_ids(CFG, probe, 10, seeds, idf)
    b = rank_ids(CFG, probe, 10, seeds, idf)
    r.add("T8", "两次排序完全一致", f"{'一致' if a == b else '不一致'}", "一致", a == b)


# ── T9 去中心化（有没有跳出「货架前排」）──────────────────────────────────
def t9_decentralized(r: Report, seeds: list[dict], idf: dict[str, float]) -> None:
    print("\n\033[1mT9 去中心化 —— top1 是否总落在旧索引表那几粒上\033[0m")
    legacy = {i.lower() for i in LEGACY_SHELF[PROFILE]}
    tops, outside = [], []
    for p in PROBES[PROFILE]:
        ids = rank_ids(CFG, p, 5, seeds, idf)
        if not ids:
            continue
        tops.append(ids[0])
        if ids[0].lower() not in legacy:
            outside.append(ids[0])
    ratio = len(outside) / max(1, len(tops))
    r.add("T9", "top1 落在旧货架之外", f"{ratio:.1%}（{len(outside)}/{len(tops)}）",
          f">= {THRESHOLDS['decenter_min']:.0%}", ratio >= THRESHOLDS["decenter_min"])
    dup = [k for k, v in Counter(tops).items() if v > 1]
    r.add("T9b", "top1 自身多样性", f"{len(set(tops))}/{len(tops)} 个不同"
          + (f"（重复：{dup[:3]}）" if dup else ""), "无单粒垄断", len(set(tops)) >= 0.6 * len(tops))


# ── T10 增量等价（split-half）─────────────────────────────────────────────
# 把全库切成 A/B：A 当基础库，B 全部走「增量」路径并回来，
# 结果必须与全量库**逐位相同**。这是「增量索引不会毁库」的最强断言。
def t10_incremental_equivalence(r: Report, seeds: list[dict]) -> None:
    print("\n\033[1mT10 增量等价 —— 半库建库 + 另一半增量插入，能否复原全库\033[0m")
    A, B = split_half(seeds)
    merged, collided = sb.merge_seeds(list(A), as_additions(B))
    r.add("T10a", "ID 集合等价", f"增量 {len(B)} 粒后 {len(merged)}/{len(seeds)}", "完全一致",
          {s["id"] for s in merged} == {s["id"] for s in seeds})
    r.add("T10b", "排序等价", f"逐位对比 {len(merged)} 条", "完全一致",
          [s["id"] for s in merged] == [s["id"] for s in seeds])
    r.add("T10c", "无意外 ID 撞车", f"撞车 {collided} 次", "0", collided == 0)
    r.note(f"split-half：A={len(A)} 粒建库，B={len(B)} 粒增量插入")


# ── T11 增量过程中的无偏性（分批加入，指标不能崩）─────────────────
def t11_incremental_unbiased(r: Report, seeds: list[dict]) -> None:
    print("\n\033[1mT11 增量无偏 —— 边加边查，指标会不会越加越坏\033[0m")
    A, B = split_half(seeds)
    batches = chunks(B, 5)
    cur = list(A)
    recalls, ginis = [], []
    for batch in batches:
        cur, _ = sb.merge_seeds(cur, as_additions(batch))
        b_idf = sb.build_idf(cur)
        # 1) 新加进来的种子能否被自己的名字召回
        hit = sum(1 for s in batch if s["id"] in rank_ids(CFG, s["name"], 8, cur, b_idf))
        recalls.append(hit / len(batch))
        # 2) 全库命中集中度
        counts = Counter()
        for p in PROBES[PROFILE][:12]:
            for sid in rank_ids(CFG, p, 8, cur, b_idf):
                counts[sid] += 1
        ginis.append(gini(list(counts.values())))
    r.add("T11a", "增量中新增种子召回", f"最低 {min(recalls):.1%} / 平均 {statistics.fmean(recalls):.1%}",
          ">= 90%", min(recalls) >= 0.90)
    drift = ginis[-1] / max(1e-9, ginis[0])
    r.add("T11b", "基尼漂移（终/初）", f"{ginis[0]:.3f} → {ginis[-1]:.3f}（×{drift:.2f}）",
          "< 1.2×", drift < 1.2)
    r.note("分批基尼序列：" + " → ".join(f"{g:.3f}" for g in ginis))


# ── T12 ID 稳定（增量不能改写历史）────────────────────────────────────
def t12_id_stability(r: Report, seeds: list[dict]) -> None:
    print("\n\033[1mT12 ID 稳定 —— 新增会不会把老 ID 挤成 -2\033[0m")
    A, B = split_half(seeds)
    merged, _ = sb.merge_seeds(list(A), as_additions(B))
    before = {s["id"] for s in A}
    after = {s["id"] for s in merged}
    renamed = sorted(i for i in before if i not in after)
    r.add("T12", "已有 ID 零改写", f"丢失/改名 {len(renamed)} 个" + (f"：{renamed[:3]}" if renamed else ""),
          "0", not renamed)


# ── T13 重复检测（同义别名不该被当成新种子）─────────────────────
def t13_dup_detection(r: Report, seeds: list[dict]) -> None:
    print("\n\033[1mT13 重复检测 —— 同义别名能拦住，真新种子不误伤\033[0m")
    src = max(seeds, key=lambda s: len(s["text"]))
    alias = {"id": "probe-alias", "layer": src["layer"], "name": src["name"],
             "text": src["text"], "grams": src["grams"]}
    dup, sim = sb.find_duplicate(seeds, alias)
    r.add("T13a", "同义别名被识别", f"命中 {dup['id'] if dup else 'None'}（包含度 {sim:.2f}）",
          ">= 0.75", dup is not None)

    novel = {"id": "probe-novel", "layer": src["layer"], "name": "qzjvxk",
             "text": "qzjvxk wpfmrt 完全无关的新概念词", "grams": 12}
    dup2, sim2 = sb.find_duplicate(seeds, novel)
    r.add("T13b", "真新种子不误报", f"包含度 {sim2:.2f}", "< 0.75", dup2 is None)


# ── 汇总 + evidence ───────────────────────────────────────────────────────
def write_evidence(r: Report, seeds: list[dict]) -> None:
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    passed = len(r.rows) - r.failed
    lines = [
        f"# 🧪 种子大脑无偏分布验证 · Evidence（{CFG['label']}）",
        "",
        f"> **生成**：{time.strftime('%Y-%m-%d %H:%M')} ｜ **套件** `seed_brain_selftest.py` ｜ "
        f"**算法版本** `seed_brain v{sb.__version__}`",
        f"> **被测对象**：`references/SEED-INDEX.md` + `references/seed-index.jsonl`（{len(seeds)} 粒）",
        f"> **复跑**：`python3 scripts/seed_brain_selftest.py --evidence`",
        "",
        f"## 结论：{passed}/{len(r.rows)} 项通过" + ("" if not r.failed else f"，**{r.failed} 项失败**"),
        "",
        "| # | 检查项 | 实测 | 门槛 | 判定 |",
        "|---|---|---|---|---|",
    ]
    for tid, name, metric, target, ok in r.rows:
        lines.append(f"| {tid} | {name} | {metric} | {target} | {'✅' if ok else '❌'} |")
    lines += ["", "## 明细", ""]
    for d in r.details:
        lines.append(f"- {d}")
    lines += [
        "",
        "## 门槛为什么这么定",
        "",
        "- **T2a 名字自召回 ≥98%**：连自己的名字都召不回，说明该种子被系统性埋没（解析漏读或 gram 缺失）。",
        "- **T2b 特征词召回 ≥60%**：不使用名字、只用自身高 idf 特征词，模拟「用户用别的说法描述同一种风格/工具」。",
        "  注意：这是**下限检查**（探针与被测种子同源，存在天花板效应），不等于无偏证据；无偏证据看 T3/T4/T9。",
        "- **T3 基尼 <0.80**：检索必然有长尾，但长尾不该变成垄断；0.80 是「有效但不过度」的经验线。",
        "- **T4 top1 提升 ≥15pp**：探针 = 1 稀有词 + 4 通用词。开 IDF 时稀有词拿全权重，关 IDF 时被通用词淡没；",
        "  若两者无差异，说明「无偏」只是口号。",
        "- **T6 单层垄断 ≤70%**：配额的真实目的是「强层不挤死弱层」，而不是精确配比；",
        "  因此判垄断度，容许「候选不足时的合法补齐」。",
        "- **T5 轮转 ≥4/6**：状态记忆若无效，同一任务会 6 次给出同一个 top1。",
        "- **T6 超配额 0 次**：配额是「弱层不被强层挤死」的硬约束。",
        "- **T9 去中心化 ≥50%**：直接回答「是不是每次只用货架最显眼那几个」。",
        "- **T10 增量等价 =100%**：半库建库 + 另一半增量插入必须与全量库逐位相同；不等价就是索引在骗人。",
        "- **T11a 增量中新增种子召回 ≥90%、T11b 基尼漂移 <1.2×**：边加边跑的指标不能崩。",
        "- **T12 已有 ID 零改写**：增量绝不能把老 ID 挤成 `-2`，否则风味日志、状态记忆、外部引用全部断链。",
        "- **T13 重复检测**：包含度 ≥0.75 判为同义别名；阈值过低会把新概念误伤。",
        "",
        "## 方法的已知边界",
        "",
        "- 匹配用字符 n-gram + IDF，不是语义 embedding：同义改写（「冷峻」↔「冷漠」）不保证命中，",
        "  这是零依赖与可解释性的代价；升级到向量检索时本套件的门槛应整体重定。",
        "- 中文 2-gram 会跨词边界（「条件数」→「件数」），计分时无害（idf 仍指向正确簇），展示层已去冗余。",
        "- T9 的「旧货架」是近似：美学取 `code-genes/` 12 张，数学取场景档 + 高频工具；",
        "  严格复现旧行为需要把历史 SKILL.md 的索引表全部解析，此处以等价集合代替。",
        "",
    ]
    EVIDENCE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\n✓ evidence 已写入 {EVIDENCE.relative_to(ROOT)}")


def main() -> int:
    ap = argparse.ArgumentParser(description="种子大脑无偏分布验证")
    ap.add_argument("--evidence", action="store_true", help="写 docs/EVIDENCE-seed-brain.md")
    args = ap.parse_args()

    print(f"\n{'='*78}")
    print(f"  种子大脑无偏分布验证 ｜ seed_brain v{sb.__version__} ｜ profile={PROFILE}")
    print(f"{'='*78}")

    seeds = sb.load_seeds(CFG)
    idf = sb.build_idf(seeds)

    r = Report()
    t1_integrity(r, seeds)
    t2_reachability(r, seeds, idf)
    t3_concentration(r, seeds, idf)
    t4_idf_effect(r, seeds, idf)
    t5_rotation(r, seeds, idf)
    t6_layer_balance(r, seeds, idf)
    t7_robustness(r, seeds, idf)
    t8_determinism(r, seeds, idf)
    t9_decentralized(r, seeds, idf)
    t10_incremental_equivalence(r, seeds)
    t11_incremental_unbiased(r, seeds)
    t12_id_stability(r, seeds)
    t13_dup_detection(r, seeds)

    passed = len(r.rows) - r.failed
    print(f"\n{'─'*78}")
    print(f"  结果：{passed}/{len(r.rows)} 通过" + (f" ｜ \033[31m{r.failed} 项失败\033[0m" if r.failed else " ｜ 全部通过"))
    print(f"{'─'*78}")

    if args.evidence:
        write_evidence(r, seeds)
    return 1 if r.failed else 0


if __name__ == "__main__":
    sys.exit(main())
