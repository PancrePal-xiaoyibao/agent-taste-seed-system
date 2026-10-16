# 变更档案 / Change Records

本目录保存**已完成的变更**的过程文档（CHANGE / HEALTH / PRD / SPEC / TRACEABILITY）。

## 阅读须知

- 档案记录的是**当时的状态与当时使用的路径**，不做追溯性修改。
  项目在 **v2.0.0（2026-10-16）** 做过一次开源合规改名与结构收敛：
  - 仓库/项目名：`agent-taste-seed-system` → **美学大脑 / aesthetic-brain**
  - `templates/SKILL.md` → 仓库根 `SKILL.md`
  - `tasks/` → `docs/changes/`
  - `sources/`（底稿 docx）从版本库剥离

  因此本目录中的旧路径引用（如 `templates/SKILL.md`、`tasks/...`）**属于历史记录，不是当前结构**。
  当前结构见仓库根 [`README.md`](../../README.md)。
- 档案中的断言命令同样反映当时状态，不一定能在当前结构上直接复跑。

## 现有档案

| 档案 | 主题 |
|---|---|
| `CHG-20261013-seed-internal-path/` | 种子库落点从 agent workspace 收敛到 skill 内部，隔离 workspace 自动清理 |
