# OpenClaw 部署 — 美学大脑

> OpenClaw 有 workspace（人格 + 规则文件），是最贴合本系统原生设计的部署形态——本系统最初就是在 OpenClaw 工作站上提炼的。

## 步骤

1. **放文件**（容器内可读路径，按你的挂载结构调整）。以下命令**在本仓库根目录执行**：

```bash
cd /path/to/agent-taste-seed-system   # 仓库根（clone 出来的目录）
mkdir -p <workspace根>/taste
cp TASTE.md <workspace根>/TASTE.md
# 旧部署且 taste/art-seeds.md 末尾已有风味日志时，先备份再覆盖：
cp <workspace根>/taste/art-seeds.md <workspace根>/taste/art-seeds.md.bak-$(date +%Y%m%d-%H%M%S) 2>/dev/null || true
cp -R references/. <workspace根>/taste/
```

装完的 workspace 结构（四层全库）：

```
<workspace根>/TASTE.md            审美 OS（决策层）
<workspace根>/taste/art-seeds.md  L1 总库速查（末尾记风味日志）
<workspace根>/taste/moods/        L2a 情绪档 ×10
<workspace根>/taste/code-genes/   L2b 代码基因卡 ×12
<workspace根>/taste/chapters/     L2c 风格章档 ×24+后记
```

> 旧版只装了 `TASTE.md` + `taste/art-seeds.md` 的 workspace：重跑上面命令即可补齐四层；风味日志有备份，不会丢。

2. **注入提示词**：把 [`AGENT-INJECTION.md`](../AGENT-INJECTION.md) 里的注入提示词整段并入 workspace 的 `AGENTS.md` 或 `SOUL.md`（人格层规则）。

3. **重启/热载** workspace，验证：对龙虾说「画一张 XX 海报」，看它是否先报情绪关键词再动手。

## 注意

- 多龙虾舰队（多项目）时，每个 workspace 独立放一份；**人格文件不要跨项目串**（工作助手与心理支持类项目的注入语义各自独立）。
- 龙虾产出的风味日志记在各自 workspace 的 `taste/art-seeds.md` 末尾；定期把好搭配同步回本仓库。
