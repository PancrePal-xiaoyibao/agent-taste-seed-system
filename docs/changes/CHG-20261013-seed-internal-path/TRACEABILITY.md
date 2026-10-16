# TRACEABILITY-20261013 — 种子库部署收敛（美学大脑）

```yaml
change_id: CHG-20261013-seed-internal-path
spec_ref: SPEC.md
evidence_date: 2026-10-13
```

## 1. 需求 → 文件 → 证据 映射

| 需求 | 落实文件 | 落地证据 | 验证命令（可复制） | 证据类型 |
|---|---|---|---|---|
| FR-1 OpenClaw 落点改为 skill 内部 | `deploy/openclaw.md` | 落点章节写 `<workspace>/skills/taste/references/`；含迁移小节 | `grep -n "skills/taste/references" deploy/openclaw.md` 有命中 | grep 断言 |
| FR-2 通用 Agent 按端 skill 目录 | `deploy/generic-agents.md` | 情形 A 增"按端 skill 根取值表"；无 skill 机制兜底并声明"不得位于 workspace" | `grep -n "skill 根" deploy/generic-agents.md` 有命中 | grep 断言 |
| FR-3 `TASTE.md` 路径自适配段收敛 | `TASTE.md` | 文首只保留"skill 内部相对路径"单一说法 | `grep -c "taste/art-seeds.md" TASTE.md` 仅命中迁移/历史语境 | grep 断言 |
| FR-4 注入表同步 | `AGENT-INJECTION.md` | 部署说明表引用 skill 内部路径 | `grep -n "skills/taste" AGENT-INJECTION.md` 有命中 | grep 断言 |
| FR-5 README 一键指令改指 | `README.md` | 5 个一键块 + 手动部署表 + 文件清单统一 | `grep -rn "workspace根>/taste/" README.md` 无"推荐落点"命中 | grep 断言 |
| FR-6 `templates/SKILL.md` 声明相对引用 | `templates/SKILL.md` | 新增「种子库随 skill 安装」段 | `grep -n "相对" templates/SKILL.md` 有命中 | grep 断言 |
| FR-7 `claude-code.md` 补理由与验证 | `deploy/claude-code.md` | 新增「为什么装在 skill 内部」+ 验证命令 | `grep -n "为什么" deploy/claude-code.md` 有命中 | grep 断言 |
| FR-8 CHANGELOG v1.0.2 | `CHANGELOG.md` | 新增 v1.0.2 段 | `grep -n "v1.0.2" CHANGELOG.md` 有命中 | grep 断言 |
| FR-9 迁移与验证步骤 | `deploy/openclaw.md`、`deploy/generic-agents.md` | 迁移命令 + workspace 搬迁免疫性证明 | 手动执行 SPEC §4.4 命令 | 执行断言 |

## 2. PRD 验收标准 → 证据

| 验收标准（PRD §5） | 证据 |
|---|---|
| US-001 OpenClaw 装在 `<workspace>/skills/taste/references/` | `deploy/openclaw.md` 落点章节 + 结构树 |
| US-002 通用 Agent 有按端取值表 | `deploy/generic-agents.md` 表格 |
| US-003 workspace 搬走仍可用 | `deploy/openclaw.md` 验证节命令 |
| US-004 旧部署一条命令迁移不丢风味日志 | `deploy/openclaw.md` 迁移节（先备份 + 再覆盖 + 清旧） |
| US-005 全文落点描述一致 | 一致性 grep：`grep -rn "taste/art-seeds.md" --include=*.md .` 命中仅在迁移/历史语境 |

## 3. 一致性断言（交付前自检）

```bash
cd <repo>
# A1 不得存在"把种子库放 workspace 根 taste/"的推荐描述
! grep -rn "workspace根>/taste/\|workspace/taste/" --include=*.md . | grep -v "tasks/"
# A2 skill 内部相对引用存在（SKILL.md）
grep -q "references/" templates/SKILL.md
# A3 迁移节存在
grep -q "迁移" deploy/openclaw.md
```

## 4. 未覆盖 / 延后

| 项 | 说明 |
|---|---|
| 本机 taste skill 实际部署 | 属于部署动作（不在本仓库交付物内），交付后随 commit 一并执行 |
| 其他 agent（pi/gemini/kimi）实例化验证 | 无 skill 落点差异，按同一契约复用 |
| OpenClaw 人格文件语义 | 本 CHG 不触碰 |
