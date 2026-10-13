# PRD-20261013 — 种子库部署收敛到 agent skill 内部路径

```yaml
change_id: CHG-20261013-seed-internal-path
version: 1
status: APPROVED
owner: user
approved_by: user
approved_at: 2026-10-13
source_change: CHANGE.md
source_health: HEALTH.md
```

## 1. 一句话

把种子库的部署落点从「agent workspace / 用户主目录 clone」收敛到「agent 自身的 skill 能力目录内部」，让种子库在任何 workspace 清理策略下都不会被搬走。

## 2. 用户与场景

| 用户 | 场景 | 期望 |
|---|---|---|
| agent 主人（部署者） | 按 README 一键部署 | 照文档装，装完就是安全落点，不需要额外判断 |
| 装了 workspace 自动清理的 agent 宿主 | workspace 定期被归档/清空 | 种子库不受影响，技能持续可用 |
| 已按旧形态部署过的用户 | 想知道要不要搬家 | 文档给一条命令的迁移步骤，且风味日志不丢 |
| 未来的贡献者 | 新增一种 agent 的部署文档 | 有明确规则：种子库只进 skill 目录内部 |

## 3. 目标（Goals）

- G1 种子库单一落点：`<该 agent 的 skill 根>/taste/references/`（四层全库）。
- G2 所有 skill 内部文档使用**相对 skill 根**的引用（`references/xxx.md`）。
- G3 注入提示词（薄注入片段 / AGENT-INJECTION）里不出现 workspace 相对路径。
- G4 给出 workspace 级验证方法，证明清理后仍可用。
- G5 给出旧形态（workspace `taste/`）→ 新形态的迁移步骤。

## 4. 非目标

- 不改种子库内容；不改四层路由契约；不改 Claude Code 已正确的落点；不动 OpenClaw 的人格/记忆文件语义。

## 5. 用户故事与验收

| ID | 故事 | 验收标准 |
|---|---|---|
| US-001 | 作为部署者，按 OpenClaw 文档部署后，种子库在 workspace 的 `skills/taste/references/` 里 | 文件存在；`TASTE.md` 引用 `references/art-seeds.md`（相对 skill 根） |
| US-002 | 作为部署者，按通用 Agent 文档部署后，种子库在该 agent 的 skill 目录内 | 文档给出 `<skill 根>` 的按端取值表；无 skill 机制时退化为仓库目录并显式声明"不得位于 workspace" |
| US-003 | 作为运维者，我能验证"把 workspace 搬走后种子库还在" | 文档含可复制命令，执行输出可判定 |
| US-004 | 作为旧部署用户，我能一条命令迁移且不丢风味日志 | 迁移步骤含 `cp` 备份 + `rm -rf` 旧落点 + 验证 |
| US-005 | 作为读者，我在任何一份文档里看到的落点描述都一致 | 全仓库 grep 无冲突描述（`taste/art-seeds.md` 仅出现在迁移节） |

## 6. 功能需求

| ID | 需求 | 优先级 |
|---|---|---|
| FR-1 | `deploy/openclaw.md` 落点改为 `<workspace>/skills/taste/references/`，`TASTE.md` 放 `<workspace>/skills/taste/` | P0 |
| FR-2 | `deploy/generic-agents.md` 落点改为按端 skill 目录；给出按端取值表；无 skill 机制时退化为仓库目录 | P0 |
| FR-3 | `TASTE.md` 文首路径自适配段改为"skill 内部相对路径"单一说法 | P0 |
| FR-4 | `AGENT-INJECTION.md` 部署表同步新落点 | P0 |
| FR-5 | `README.md` 一键部署指令（Claude/OpenClaw/Codex/通用/手动部署表）全部改指 skill 内部路径 | P0 |
| FR-6 | `templates/SKILL.md` 增加"种子库随 skill 安装、引用一律相对 skill 根"的显式声明 | P1 |
| FR-7 | `deploy/claude-code.md` 补"为什么装在 skill 内部（vs workspace）"与验证命令 | P1 |
| FR-8 | `CHANGELOG.md` 新增 v1.0.2 记录本次部署形态变更 | P2 |
| FR-9 | 新增验证小节（可并入 claude-code.md / openclaw.md）：workspace 搬迁后仍可读的证明命令 | P1 |

## 7. 依赖与约束

- 依赖：各 agent 的 skill 根约定（Claude `~/.claude/skills/`、Codex `~/.codex/skills/`、OpenClaw `<workspace>/skills/`、pi/Kimi `~/.agents/skills/`）。
- 约束：见 `CHANGE.md` §5（C1–C5）。开源脱敏：文档不得写入真实 home 绝对路径与主机信息（示例统一用 `~` / `<placeholder>`）。

## 8. 风险

| 风险 | 影响 | 缓解 |
|---|---|---|
| 某 agent 无 skill 机制 | 无法"进 skill 内部" | 退化为仓库目录（不在 workspace 内），文档显式声明 |
| 用户已有 workspace 落点数据 | 迁移丢风味日志 | 迁移步骤强制先备份 `art-seeds.md` |
| 文档数量多、易漏 | 不一致残留 | TRACEABILITY 逐文件对账 |

## 9. 成功指标

- 全仓库一致性检查通过：`grep -rn "taste/art-seeds.md"` 命中仅出现在"迁移/历史形态"语境。
- 任意已部署形态下：`test -r <skill 根>/references/art-seeds.md` 返回 0。

## 10. Definition of Ready / Done

- **DoR**：CHANGE 已对齐（用户明确指令）；HEALTH 基线已有。
- **DoD**：FR-1..FR-9 全部落地；TRACEABILITY 全部映射到证据；无脱敏违规；CHANGELOG 更新。
