# 通用智能体部署 — Codex / pi / workbuddy / codebuddy / Trae / Qoder / hermas 等

> 判据只有一个：**你的 Agent 会不会在开工前自动读某个规则文件？**（AGENTS.md / rules / 系统提示词配置）

## 情形 A：有全局规则文件（Codex 的 `~/.codex/AGENTS.md`、Trae/Qoder 的 rules、hermas/workbuddy/codebuddy 的全局指令文件等）

1. 把 `TASTE.md` 和 `references/art-seeds.md` 放到一个**固定绝对路径**（建议 `~/agent-taste-seed-system/`，直接 clone 本仓库即可）：

```bash
git clone https://github.com/hhx465453939/agent-taste-seed-system.git ~/agent-taste-seed-system
```

2. 把下面薄注入片段贴进全局规则文件（注意把路径换成上一步的实际路径）：

```markdown
## 🎨 美学大脑（Taste Seed System）

- **触发**：任何带视觉属性的任务（长图/海报/PPT/图表/插画/UI/皮肤/封面/配图/配色/前端页面视觉/视频分镜）——动手前先走美学决策流程。
- **流程**：情绪定位（读者该感受什么，一个词）→ 打开 `~/agent-taste-seed-system/references/art-seeds.md` 按情绪索引选 1 主 + 1 辅基因 → 五基因翻译成具体参数 → 一句话自检 → 交付后记风味日志。
- **红线**：禁止"AI 味默认审美"（通用卡片/蓝紫渐变）；一组作品一个主基因，敢混搭只混一层；种子库按需查询、禁止全文注入上下文。
- 决策流程全文见 `~/agent-taste-seed-system/TASTE.md`；注入提示词全文见 `~/agent-taste-seed-system/AGENT-INJECTION.md`。
```

## 情形 B：只有系统提示词 / 知识库（通用 ChatBot、自定义 Agent）

1. `TASTE.md` + `art-seeds.md` 全文作为**知识库文档 / 附件**上传
2. [`AGENT-INJECTION.md`](../AGENT-INJECTION.md) 的注入提示词整段放进**系统提示词**（或人格层）

> 上下文紧张的系统：只注入「注入提示词」部分（约 500 字），种子库留给检索（RAG / 文件读取）。

## 情形 C：有 skill / 工具机制的 Agent

参照 [`templates/SKILL.md`](../templates/SKILL.md) 的结构做一个触发器：视觉类任务自动先读 `TASTE.md`，再按需查种子库。
