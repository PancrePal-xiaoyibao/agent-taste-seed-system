# OpenClaw 部署 — 美学大脑

> OpenClaw 有 workspace（人格 + 规则文件），是最贴合本系统原生设计的部署形态——本系统最初就是在 OpenClaw 工作站上提炼的。

## 步骤

1. **放文件**（容器内可读路径，按你的挂载结构调整）：

```bash
cp TASTE.md <workspace根>/TASTE.md
mkdir -p <workspace根>/taste
cp references/art-seeds.md <workspace根>/taste/art-seeds.md
```

2. **注入提示词**：把 [`AGENT-INJECTION.md`](../AGENT-INJECTION.md) 里的注入提示词整段并入 workspace 的 `AGENTS.md` 或 `SOUL.md`（人格层规则）。

3. **重启/热载** workspace，验证：对龙虾说「画一张 XX 海报」，看它是否先报情绪关键词再动手。

## 注意

- 多龙虾舰队（多项目）时，每个 workspace 独立放一份；**人格文件不要跨项目串**（工作助手与心理支持类项目的注入语义各自独立）。
- 龙虾产出的风味日志记在各自 workspace 的 `taste/art-seeds.md` 末尾；定期把好搭配同步回本仓库。
