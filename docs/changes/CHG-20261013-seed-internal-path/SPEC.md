# SPEC-20261013 — 种子库部署收敛到 skill 内部路径（美学大脑）

```yaml
change_id: CHG-20261013-seed-internal-path
version: 1
status: approved
prd_ref: PRD.md
health_ref: HEALTH.md
supersedes: null
approved_by: user
approved_at: 2026-10-13
```

---

## 0. 阅读顺序

`CHANGE.md`（为什么做）→ `HEALTH.md`（现状债）→ `PRD.md`（产品契约）→ 本文件（工程契约）→ `TRACEABILITY.md`（追溯）。

---

## 1. 上下文、目标、非目标、约束、假设

### 1.1 上下文

本项目是纯文档型知识库仓库（无运行时代码，仅一个 bash 安装脚本）。种子库 = `references/` 下的四层文件（`art-seeds.md` + `moods/` + `code-genes/` + `chapters/`）。问题不在代码，而在**"种子库被装到哪"**这条部署链路上——见 `CHANGE.md` §1。

### 1.2 目标（工程视角）

* E1 定义一个**唯一合法落点**：`<agent skill 根>/taste/references/`。
* E2 定义**唯一合法引用形式**：skill 内文档相对 skill 根（`references/...`）；skill 外文档才允许绝对路径。
* E3 把该约定**同时**落到 8 个文档 + 1 个脚本 + 1 个模板，不留下自相矛盾的旧描述。
* E4 提供可执行验证，且验证不依赖"我记得它装在哪"。
* E5 提供旧态 → 新态的幂等迁移步骤。

### 1.3 非目标

同 PRD §4。工程侧额外明确：不引入 `link-checker` 等新工具（保持零依赖）；不把 `references/` 内容做任何重命名或移动；不动 OpenClaw 的人格文件（`SOUL.md`/`AGENTS.md` 仍留 workspace 根）。

### 1.4 约束

| ID | 约束 | 来源 |
|---|---|---|
| C1 | 迁移/重装先备份 `art-seeds.md`（含风味日志） | PRD 风险表 |
| C2 | 文档零真实敏感值，示例用 `~` 与 `<占位符>` | 开源脱敏铁律 |
| C3 | 相对引用在 skill 根下必须可解析 | PRD US-001 |
| C4 | 8 文档 + 脚本 + 模板一次性对齐 | 齐头并进铁律 |
| C5 | 迁移命令幂等（`cp -n`/`test -d` 守卫） | PRD FR-9 |

### 1.5 假设

* A1 OpenClaw workspace 存在 `skills/` 子目录（本机实测：存在）。若不存在，退化为情形 A。
* A2 各 agent 的 skill 根在会话内是已知常量，不需要运行时探测。
* A3 用户接受"OpenClaw 的 `TASTE.md` 也一并放进 `skills/taste/`"——因为它是决策层文档，属于能力部件而非人格部件。

---

## 2. 当前架构与债务影响

```
现状（三套说法并存，互不承认）
├── deploy/claude-code.md      → ~/.claude/skills/taste/references/     ✅ 安全
├── deploy/openclaw.md         → <workspace>/taste/                     ❌ 暴露于清理
├── deploy/generic-agents.md   → ~/agent-taste-seed-system/references/  ❌ 暴露于清理（若在 workspace 内）
├── TASTE.md 文首              → 并列两种说法（"本仓库为…，OpenClaw 部署在 taste/"）❌ 自相矛盾
└── README.md                  → 三种落点各写一遍                        ❌ 无权威
```

债务影响：D1/D2/D3（HEALTH §3）全部收敛到本 CHG 修；改造后 `TASTE.md` 与各 deploy 文档单点权威。

---

## 3. 选型与 ADR

### ADR-001：种子库落点在 skill 内部，而非 workspace

| 方案 | 描述 | 结论 |
|---|---|---|
| A. 保留 workspace 落点 + 加"请勿清理"豁免 | 依赖用户在清理策略里加白名单 | **否决**：把能力数据的存续押在别人的清理配置上，脆弱且不可移植 |
| B. 种子库进 skill 内部 | 每个 agent 的能力目录天然不被 workspace 清理策略覆盖 | **采纳** |
| C. 种子库存用户主目录固定路径（`~/agent-taste-seed-system/`）并让各 agent 引用 | 单一副本、易更新 | **部分采纳**：作为"无 skill 机制"的兜底（情形 A/B），但**必须显式声明不得位于任何 workspace 内**；有 skill 机制时优先 B |

**理由**：workspace 清理策略的语义是"整理人格工作区"，它没有义务保留能力数据。skill 目录的语义是"这个 agent 的能力集合"，清理策略天然不会动它。**按语义分层，而不是按目录是否写保护分层。**

**可逆性**：反向迁移成本同等（一条 `cp` + 一条 `rm`），且迁移脚本幂等。**后果**：agent 的 skill 目录会变大（taste 约 400KB），可接受。

### ADR-002：引用形式——skill 内用相对，skill 外用绝对

- skill 根下文档（`templates/SKILL.md`、以及注入到 skill 的说明）：一律 `references/xxx.md`。
- skill 根**之外**的文档（README 的一键指令、`deploy/generic-agents.md` 情形 A 的注入片段）：用该 agent 的 skill 根绝对路径（`~/.codex/skills/taste/references/art-seeds.md`）。

**理由**：相对路径让 skill 整体可搬迁（换机器、改用户名、装到别的 skill 根都不需要改文档）；绝对路径只出现在"告诉别人去哪儿找"的少数几处。

---

## 4. 接口、数据、兼容、迁移、观测、回滚

### 4.1 部署接口（落点契约）

| Agent | skill 根 | 落点 |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `~/.claude/skills/taste/references/art-seeds.md` |
| Codex | `~/.codex/skills/` | `~/.codex/skills/taste/references/art-seeds.md` |
| OpenClaw | `<workspace>/skills/` | `<workspace>/skills/taste/references/art-seeds.md` |
| pi / Kimi | `~/.agents/skills/`（本机为 `~/.claude/skills` 符号链接） | `<agents skill 根>/taste/references/art-seeds.md` |
| 无 skill 机制的 agent | 仓库 clone 目录（**不得位于 workspace 内**） | `<clone 根>/references/art-seeds.md` |

### 4.2 迁移（旧 → 新）

```bash
# 定位旧落点（旧形态：workspace/taste/）
WS="${WORKSPACE:?请设为 OpenClaw workspace 根}"
OLD="${WS}/taste"
NEW="${WS}/skills/taste"

# 1) 先备份风味日志（幂等：目标已存在则不覆盖）
if [ -f "$OLD/art-seeds.md" ] && [ ! -f "$NEW/references/art-seeds.md" ]; then
  mkdir -p "$NEW/references"
  cp -n "$OLD/art-seeds.md" "$NEW/references/art-seeds.md"
  echo "📦 已迁移风味日志 → $NEW/references/art-seeds.md"
fi

# 2) 再用仓库四层全量覆盖（正式步骤见 deploy/openclaw.md）
# 3) 清理旧落点
rm -rf "$OLD"
```

> 正式迁移命令以 `deploy/openclaw.md` 的「迁移」小节为权威（含日志合并顺序）。

### 4.3 兼容性

- **旧部署不破坏**：迁移是显式动作，不做自动搬运。旧用户什么都不做仍然能用（直到 workspace 被清理）。
- **不需要改种子库内容**：`references/**` 零改动。

### 4.4 观测（验证）

```bash
# 断言种子库四层可读
SKILL_ROOT="${SKILL_ROOT:-$HOME/.claude/skills/taste}"
test -r "$SKILL_ROOT/references/art-seeds.md" && echo "L1 OK"
test -d "$SKILL_ROOT/references/moods"      && echo "L2a OK"
test -d "$SKILL_ROOT/references/code-genes" && echo "L2b OK"
test -d "$SKILL_ROOT/references/chapters"   && echo "L2c OK"

# workspace 清理免疫性证明（OpenClaw）：把 workspace 挪走后仍可读
WS="${WORKSPACE:?}"
mv "$WS" "$WS.moved" && \
  test -r "$WS.moved/skills/taste/references/art-seeds.md" && echo "IMMUNE OK" && \
  mv "$WS.moved" "$WS"
```

### 4.5 回滚

回滚 = 把 `references/` 从 skill 根复制回旧 workspace 落点（一条 `cp -R`），旧注入节恢复即可。因本 CHG 不改内容，回滚零数据损失。

---

## 5. 里程碑

| M | 依赖 | 涉及文件 | 验收 | 风险 |
|---|---|---|---|---|
| M1 权威定义 | — | `TASTE.md`（文首路径段） | 只有一种落点说法：skill 内部相对路径 | 低 |
| M2 部署文档对齐 | M1 | `deploy/openclaw.md`、`deploy/generic-agents.md`、`deploy/claude-code.md` | 三份文档落点一致；openclaw 给迁移节；claude-code 给"为什么"与验证节 | 中（openclaw 语义变化最大） |
| M3 注入与模板对齐 | M1 | `AGENT-INJECTION.md`、`templates/SKILL.md` | 注入表无 workspace 相对路径；SKILL.md 显式声明相对引用 | 低 |
| M4 README 与变更记录 | M2,M3 | `README.md`、`CHANGELOG.md` | 一键指令全指 skill 内部；CHANGELOG v1.0.2 | 低 |
| M5 追溯与验收 | M4 | `tasks/.../TRACEABILITY.md` | 逐 FR 有证据 | 低 |

---

## 6. Definition of Ready / Done

- **DoR**：CHANGE 对齐、HEALTH 基线、PRD 批准 ✅
- **DoD**：M1–M5 完成；一致性断言通过；无脱敏违规；TRACEABILITY 无空洞；CHANGELOG 更新。

---

## 7. 评审与交付 Gate

| Gate | 内容 | 授权 |
|---|---|---|
| G1 内容一致性 | 三套说法是否收敛为一套；grep 无冲突 | 自检 |
| G2 脱敏 | 无真实 home 绝对路径/主机信息 | 自检 |
| G3 验证可执行 | §4.4 命令在任一已部署落点可跑通 | 自检 |
| G4 commit | 需维护者授权 | 用户 |
| G5 push | 需维护者授权（本次用户已预授权"直接 commit push"） | 用户 |

---

## 8. 追溯与证据计划

见 `TRACEABILITY.md`：FR-1..FR-9 → 文件 → 验证命令 → 证据类型（grep 断言 / 文件断言）。
