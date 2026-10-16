# CHANGE-20261013-seed-internal-path — 种子库部署收敛到 skill 内部路径

```yaml
change_id: CHG-20261013-seed-internal-path
title: 把种子库的部署落点从 agent workspace 收敛到 agent 自身 skill 内部路径，杜绝 workspace 自动清理导致的引用失效
status: INTENT_ALIGNED
owner: user
created_at: 2026-10-13
evidence_date: 2026-10-13
```

## 1. 问题（Problem）

本机（以及任何配置了 workspace 自动清理的 agent 宿主）存在一条**种子库被静默搬走、引用失效**的链路：

| 环节 | 现状 |
|---|---|
| 部署落点 | Claude Code 装 `~/.claude/skills/taste/`（安全）；**OpenClaw 装 `<workspace根>/taste/`**（危险）；Codex 等走 `~/agent-taste-seed-system/` 复制品的 `references/`（危险，且靠"原生布局"约定） |
| 宿主行为 | 很多 agent 在宿主机配置了 **workspace 自动清理**：把 workspace 内的文件转移到 `archive` 类路径，或直接删除 |
| 后果 | 种子库文件（`art-seeds.md` 总库、`moods/`、`code-genes/`、`chapters/`）被搬走后，注入提示词里写死的 `taste/art-seeds.md`、`~/agent-taste-seed-system/references/...` **指向不存在的路径** |
| 长期后果 | skill / 注入节形同虚设——agent 每次都"查库"，每次都查不到，退化成 AI 味默认审美；**且没有任何报错**，故障静默 |

**根本原因（根因）**：把「**能力部件**（种子库）」和「**人格/记忆部件**（workspace 里的 SOUL/AGENTS/记忆文件）」混在了同一个被清理策略覆盖的目录里。workspace 清理策略的语义是"整理这个人格的工作区"，它没有义务保留一份能力数据。

**对照证据**：同一个仓库的 Claude Code 分支已经做对了——种子库装进 `~/.claude/skills/taste/references/`，位于 skill 内部，不受任何 workspace 清理策略影响。本 CHG 就是把另外几条部署链路对齐到这个已经正确的形态。

## 2. 期望结果（Outcome）

1. **单一落点**：种子库（四层全库）在任何 agent 上都只装到**该 agent 自身的 skill / 能力目录内部**（如 `~/.codex/skills/taste/references/`、`~/.claude/skills/taste/references/`、OpenClaw workspace 的 `skills/taste/references/`）。
2. **零 workspace 依赖**：注入提示词与 skill 文档里的种子库引用**不再出现任何 workspace 相对路径**（例如不再写 `taste/art-seeds.md`）。
3. **相对引用优先**：skill 内部文档一律用**相对 skill 目录**的路径（`references/art-seeds.md`、`references/moods/01-...`）；只有全局规则文件（漏在 skill 之外）才允许写绝对路径。
4. **可验证**：给出可执行的验证命令，能证明「把 workspace 整个搬走/清空后，种子库仍在且可读」。
5. **可迁移**：已经按旧形态（workspace 内 `taste/`）部署过的 agent，文档给出**一条命令的原地迁移 + 清理**步骤，迁移不丢风味日志。

## 3. 当前行为（Current Behavior）

- `deploy/openclaw.md`：把四层全库平铺进 `<workspace根>/taste/`，并把 `TASTE.md` 放在 workspace 根。
- `deploy/generic-agents.md` 情形 A：让 agent `git clone` 仓库到 `~/agent-taste-seed-system`，注入片段写死 `~/agent-taste-seed-system/references/art-seeds.md`。
- `deploy/claude-code.md` / `install-claude-skill.sh`：**已经正确**（`~/.claude/skills/taste/references/`），本 CHG 只做措辞统一与显式声明，不改落点。
- `TASTE.md` 文首自我描述："本仓库为 `references/art-seeds.md`，OpenClaw workspace 部署在 `taste/art-seeds.md`"——把两种形态并列，等于承认存在危险形态。
- `README.md` 中 OpenClaw / 通用 Agent / 手动部署表格均引导用户使用 workspace 落点。

## 4. 非目标（Non-goals）

- 不改种子库**内容**（`references/**` 的 24 章 250+ 艺术家、10 情绪档、12 代码基因卡一个字不动）。
- 不改「注入 + 薄 skill + 厚 reference」框架与四层路由契约。
- 不改 `install-claude-skill.sh` 的落点（已正确）；只补文档声明与验证段。
- 不引入任何第三方依赖、不做 daemon、不做自动清理对抗（我们不和清理策略打仗，只是把种子库挪到清理策略够不着的地方）。
- 不动 OpenClaw 的人格/记忆文件语义（`SOUL.md`/`AGENTS.md` 仍留在 workspace 根）。

## 5. 约束（Constraints）

| ID | 约束 | 来源 |
|---|---|---|
| C1 | 不破坏已部署实例的风味日志（重装/迁移必须先备份 `art-seeds.md`） | 与 `install-claude-skill.sh` 既有行为一致 |
| C2 | 文档中不出现真实主机敏感信息（IP/域名/端口/用户名/绝对 home 路径） | 开源脱敏铁律 |
| C3 | 相对路径引用必须能在 skill 根目录下解析成功 | 本 CHG 验收核心 |
| C4 | 五端齐头并进：README / TASTE.md / AGENT-INJECTION.md / deploy 四份 / templates/SKILL.md / CHANGELOG 一次性对齐 | 齐头并进铁律 |
| C5 | 迁移脚本必须幂等，重复执行结果一致 | 可运维性 |

## 6. 成功信号（Success Signals）

- 在**任意**已部署 agent 上执行 `test -r <skill根>/references/art-seeds.md` 均返回 0。
- 把 OpenClaw workspace 目录**整体重命名/清空**后，`skills/taste/references/art-seeds.md` 仍可读，且注入节仍能指导 agent 找到它。
- 全仓库 `grep -rn "taste/art-seeds.md"` 在部署文档中不再作为**推荐做法**出现（历史形态仅在"迁移"一节作为被替换对象出现）。

## 7. 风险与假设

| 风险/假设 | 说明 | 处置 |
|---|---|---|
| R1 各 agent 的 skill 目录约定不同 | Codex 是 `~/.codex/skills/`，Claude 是 `~/.claude/skills/`，OpenClaw 是 workspace 内 `skills/` | 文档按 agent 逐一给准确落点，并给通用形式 `<该 agent 的 skill 根>/taste/references/` |
| R2 有的 agent 没有 skill 机制 | 例如纯 CLI 的规则文件型 agent | 情形 A 兜底：种子库仍放**仓库 clone 目录**（不受 workspace 清理影响），并在注入片段里注明"这是仓库目录，不要放进 workspace" |
| A1 OpenClaw workspace 有 `skills/` 子目录 | 本机实测存在（46 个 skill） | 若无，则退化为该 agent 的规则文件 + 仓库路径方案 |

## 8. 未决问题

- 无（用户已明确指令：种子库进 skill 内部，不动 workspace）。
