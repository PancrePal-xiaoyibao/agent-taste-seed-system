# 🧪 Seed Brain · Unbiased Distribution Verification Evidence

> **Generated**: 2026-10-22 23:45 ｜ **Suite** `seedbrain verify` ｜ **Version** `v0.1.1`
> **Subject**: `references/seed-index.jsonl` (374 seeds)
> **Reproduce**: `seedbrain verify --profile profiles/taste.json --evidence <path>`

## Result: 28/28 checks passed

| # | Check | Measured | Threshold | Verdict |
|---|---|---|---|---|
| S1 | profile is valid | validate() passes | no exception | ✅ |
| S2 | layer prefixes present | 3 layers | every layer has a prefix | ✅ |
| T1a | unique IDs | 0 duplicates | 0 | ✅ |
| T1b | no empty fields | missing field / gram<3: 0 | 0 | ✅ |
| T1c | refs resolvable | 0 broken refs | 0 | ✅ |
| T1d | legacy-shelf samples valid | 0 invalid ids | 0 | ✅ |
| T2a | name self-recall@8 | 100.0% (0/374 missed) | >= 98% | ✅ |
| T2b | feature-word recall@8 | 100.0% (0 missed) | >= 60% | ✅ |
| T3a | hit Gini coefficient | 0.233 | < 0.8 | ✅ |
| T3b | seed reach ratio | 21.7% (81/374) | > 0 | ✅ |
| T4a | IDF monotonicity | df=1 "阿梗" 5.24 vs df=145 "第十" 1.27 | rare > common | ✅ |
| T4b | top1 baseline (IDF vs keyword) | 99.7% vs 35.3% | >= 32% (no regression) | ✅ |
| T5 | top1 diversity over 6 consecutive picks | 6 distinct | >= 4 | ✅ |
| T6a | layer starvation (stocked but unranked) | 0 times | 0 | ✅ |
| T6b | single-layer monopoly when multiple layers have candidates | 0/12 | 0 (upper bound 70%) | ✅ |
| T7a | boundary inputs raise no exception | 0/8 crashes | 0 | ✅ |
| T7b | missing state fields survive | still returns float | True | ✅ |
| T8 | two rankings are identical | identical | identical | ✅ |
| T9 | top1 lands outside the legacy shelf | 75.0% (9/12) | >= 50% | ✅ |
| T9b | top1 self-diversity | 11/12 distinct | no single-seed monopoly | ✅ |
| T10a | ID set equivalence | 374/374 | exact match | ✅ |
| T10b | ranking equivalence | positional comparison | exact match | ✅ |
| T10c | no unexpected ID collisions | 0 times | 0 | ✅ |
| T11a | incremental add recall | min 100.0% | >= 90% | ✅ |
| T11b | Gini drift (final/initial) | 0.261 → 0.221 (×0.85) | < 1.2× | ✅ |
| T12 | existing IDs never rewritten | 0 lost / renamed | 0 | ✅ |
| T13a | synonym alias detected | hit ch-matisse (1.00) | >= 0.75 | ✅ |
| T13b | genuinely new seed not misflagged | 0.07 | < 0.75 | ✅ |
