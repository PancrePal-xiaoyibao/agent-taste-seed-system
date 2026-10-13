# 通用智能体部署 — Codex / pi / workbuddy / codebuddy / Trae / Qoder / hermas 等

> 判据只有一个：**你的 Agent 会不会在开工前自动读某个规则文件？**（AGENTS.md / rules / 系统提示词配置）
> 第二判据：**你的 Agent 有没有 skill 机制？**——有则种子库进 skill 内部；没有则退回"仓库 clone 目录"（**不得位于任何 workspace 内**）。

## 落点铁律（先读）

> **种子库只装进 agent 自身 skill 的内部目录（`<skill 根>/taste/references/`），绝不装进 workspace 根或 workspace 下的普通子目录。**
> 原因：很多 agent 宿主配置了 **workspace 自动清理**，会把 workspace 内的文件搬进 archive 或删除。种子库落在 workspace 普通目录里，被清理后注入提示词里写死的路径会**永久失效且无报错**。

**按端 skill 根取值表**：

| Agent | skill 根 | 种子库落点 |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `~/.claude/skills/taste/references/` |
| Codex | `~/.codex/skills/` | `~/.codex/skills/taste/references/` |
| OpenClaw | `<workspace>/skills/` | `<workspace>/skills/taste/references/` |
| pi / Kimi | `~/.agents/skills/`（本机为 `~/.claude/skills` 符号链接） | `<agents skill 根>/taste/references/` |
| 无 skill 机制 | 仓库 clone 目录（**不得位于任何 workspace 内**） | `<clone 根>/references/` |

---

## 情形 A：有 skill 机制（Codex / OpenClaw / pi 等）

1. clone 本仓库到主目录固定路径（不要在 workspace 内）：

```bash
git clone https://github.com/hhx465453939/agent-taste-seed-system.git ~/agent-taste-seed-system
```

2. 把四层种子库装进**你自己的 skill 目录**（以 Codex 为例）：

```bash
SKILL_ROOT="$HOME/.codex/skills/taste"        # ← 换成上表里你那一行的 skill 根
mkdir -p "$SKILL_ROOT/references"
cp ~/agent-taste-seed-system/templates/SKILL.md "$SKILL_ROOT/SKILL.md"
cp ~/agent-taste-seed-system/TASTE.md           "$SKILL_ROOT/TASTE.md"
cp -R ~/agent-taste-seed-system/references/.    "$SKILL_ROOT/references/"   # 四层全量
```

3. 把下面薄注入片段贴进全局规则文件（Codex 的 `~/.codex/AGENTS.md`、Trae/Qoder 的 rules、hermas/workbuddy/codebuddy 的全局指令文件等；已有同名节则跳过）：

```markdown
## 🎨 美学大脑（Taste Seed System）

- **触发**：任何涉及审美与视觉呈现的任务（长图/海报/PPT/图表/插画/UI/皮肤/封面/配图/配色/前端页面视觉/视频分镜/Word 与文档排版/生活与社会关系审美咨询）——动手前先走美学决策流程。
- **种子库落点**：本 agent 的 skill 内部 `<skill 根>/taste/references/`（如 ~/.codex/skills/taste/references/）。**引用一律相对 skill 根**：`references/art-seeds.md`、`references/moods/`、`references/code-genes/`、`references/chapters/`。禁止把种子库放进任何 workspace 目录（会被 workspace 自动清理搬走）。
- **流程**：情绪定位（读者该感受什么，一个词）→ 打开 `references/art-seeds.md` 按情绪索引选 1 主 + 1 辅基因 → 按媒介翻译成具体参数（HTML→CSS 变量 / PPT→版式 / Word→字体行距样式 / 生图→Prompt Keywords / 生活→材质色彩）→ 一句话自检 → 交付后记风味日志。
- **红线**：禁止"AI 味默认审美"（通用卡片/蓝紫渐变）；一组作品一个主基因，敢混搭只混一层；种子库按需查询、禁止全文注入上下文。
- 决策流程全文见 `<skill 根>/taste/TASTE.md`；注入提示词全文见 `~/agent-taste-seed-system/AGENT-INJECTION.md`。
```

---

## 情形 A'：有全局规则文件但**没有** skill 机制（pi / workbuddy / codebuddy / Trae / Qoder / hermas 等）

1. clone 本仓库到一个**不在任何 workspace 内**的固定绝对路径（建议 `~/agent-taste-seed-system/`）：

```bash
git clone https://github.com/hhx465453939/agent-taste-seed-system.git ~/agent-taste-seed-system
```

> ⚠️ 关键约束：这个目录**不得位于任何被 workspace 清理策略覆盖的路径下**。放进 workspace = 迟早被搬走。

2. 把下面薄注入片段贴进全局规则文件（注意把路径换成上一步的实际路径）：

```markdown
## 🎨 美学大脑（Taste Seed System）

- **触发**：任何涉及审美与视觉呈现的任务（长图/海报/PPT/图表/插画/UI/皮肤/封面/配图/配色/前端页面视觉/视频分镜/Word 与文档排版/生活与社会关系审美咨询）——动手前先走美学决策流程。
- **种子库落点**：`~/agent-taste-seed-system/references/`（仓库 clone 目录，**不得位于任何 workspace 内**；若本 agent 有 skill 机制，请改走上方「情形 A」把种子库装进 skill 内部）。
- **流程**：情绪定位（读者该感受什么，一个词）→ 打开 `~/agent-taste-seed-system/references/art-seeds.md` 按情绪索引选 1 主 + 1 辅基因 → 按媒介翻译成具体参数（HTML→CSS 变量 / PPT→版式 / Word→字体行距样式 / 生图→Prompt Keywords / 生活→材质色彩）→ 一句话自检 → 交付后记风味日志。
- **红线**：禁止"AI 味默认审美"（通用卡片/蓝紫渐变）；一组作品一个主基因，敢混搭只混一层；种子库按需查询、禁止全文注入上下文。
- 决策流程全文见 `~/agent-taste-seed-system/TASTE.md`；注入提示词全文见 `~/agent-taste-seed-system/AGENT-INJECTION.md`。
```

## 情形 B：只有系统提示词 / 知识库（通用 ChatBot、自定义 Agent）

1. `TASTE.md` + `art-seeds.md` 全文作为**知识库文档 / 附件**上传（四层全库能放目录就放整个 `references/`）
2. [`AGENT-INJECTION.md`](../AGENT-INJECTION.md) 的注入提示词整段放进**系统提示词**（或人格层）

> 上下文紧张的系统：只注入「注入提示词」部分（约 500 字），种子库留给检索（RAG / 文件读取）。

## 情形 C：有 skill / 工具机制的 Agent

参照 [`templates/SKILL.md`](../templates/SKILL.md) 的结构做一个触发器：视觉类任务自动先读 `TASTE.md`，再按需查种子库。种子库放在 skill 内部（`<skill 根>/taste/references/`），触发器内引用用相对路径（`references/art-seeds.md`）。

---

## 验证（部署后自检）

```bash
SKILL_ROOT="$HOME/.codex/skills/taste"     # 或本 agent 的实际路径
test -r "$SKILL_ROOT/references/art-seeds.md" && echo "L1 OK"
test -d "$SKILL_ROOT/references/moods"        && echo "L2a OK"
test -d "$SKILL_ROOT/references/code-genes"   && echo "L2b OK"
test -d "$SKILL_ROOT/references/chapters"     && echo "L2c OK"
```
