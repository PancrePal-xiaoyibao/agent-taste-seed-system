# HEALTH-20261013 — 项目健康基线（种子库部署路径改造前）

```yaml
change_id: CHG-20261013-seed-internal-path
baseline_date: 2026-10-13
scope: agent-taste-seed-system @ main (10e20ea)
method: 仓库内静态盘点 + 本机部署面实测
```

## 1. 构建 / 测试 / 静态检查

| 项 | 状态 | 证据 |
|---|---|---|
| 构建系统 | 无（纯文档 + 一个 bash 安装脚本） | 仓库无 package.json / Makefile / pyproject.toml |
| 自动化测试 | **无** | 无 tests/ 目录；`install-claude-skill.sh` 无自检 |
| shell 语法检查 | 通过 | `bash -n deploy/install-claude-skill.sh` |
| index 覆盖 | 399 节点 / 398 边（`fast` 模式）；`CHANGELOG.md` 与 `sources/*.docx` 按设计排除 | `index_repository` 报告 |
| Markdown 链接 | 未校验 | 无 link checker |

## 2. 部署面实测（本机）

| 目标 | 期望落点 | 实测 | 判定 |
|---|---|---|---|
| Claude Code | `~/.claude/skills/taste/references/art-seeds.md` | **不存在**（taste skill 未安装） | ⚠️ 缺口：需按本 CHG 部署 |
| Codex | `~/.codex/skills/taste/references/` | **不存在** | ⚠️ 缺口 |
| `~/.agents/skills/` | pi/Kimi 通用 skill 目录 | 是 `~/.claude/skills` 的符号链接 | ℹ️ 复用 Claude 落点即可 |
| OpenClaw workspace | `<workspace>/skills/taste/references/` | workspace 存在且含 `skills/`（46 项），无 taste | ⚠️ 缺口 |

> 注：本机当前**没有任何 taste 种子库部署**（`~/art-seeds.md` 全局查找为空）。因此本 CHG 的改造不涉及"抢救已在途数据"，只需保证首次/再次部署即正确。

## 3. 技术债清单（本项目自身）

| ID | 债 | 等级 | 归属 |
|---|---|---|---|
| D1 | 部署落点存在两个互相冲突的权威描述：`TASTE.md` 文首并列"仓库 `references/`"与"OpenClaw `taste/`" | 高 | 本 CHG 修 |
| D2 | `deploy/generic-agents.md` 把种子库路径指向 clone 目录 `~/agent-taste-seed-system/...`，未声明该目录不得位于任何被清理的 workspace | 高 | 本 CHG 修 |
| D3 | `deploy/openclaw.md` 推荐 workspace 落点，直接暴露于清理策略 | **严重** | 本 CHG 修 |
| D4 | 仓库无任何验证脚本，无法证明"workspace 搬走后种子库仍可用" | 中 | 本 CHG 部分修（新增验证步骤） |
| D5 | 安装脚本无 `--dry-run` / 无幂等自检输出 | 低 | 记入 backlog，不在本 CHG |

## 4. 与本次变更的关系

- **must fix（本 CHG 内）**：D1 / D2 / D3
- **should fix（本 CHG 顺手）**：D4（文档级验证命令）
- **after（本 CHG 外）**：D5

## 5. 变更前基线结论

项目结构简单（纯文档 + 一个安装脚本）、无运行时代码，**风险集中在文档权威性**：同一件事（种子库放哪）被三份文档说了三种话。本次改造属于**跨文档一致性修复 + 部署形态纠偏**，不需要架构级重构，适合单 CHG 一次交付。
