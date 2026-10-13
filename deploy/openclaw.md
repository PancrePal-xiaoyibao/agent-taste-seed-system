# OpenClaw 部署 — 美学大脑

> OpenClaw 有 workspace（人格 + 规则文件）**与 skill 目录**（`<workspace>/skills/`）。本系统最初就是在 OpenClaw 工作站上提炼的。
>
> ⚠️ **落点铁律：种子库只装进 skill 内部（`<workspace>/skills/taste/references/`），绝不装进 workspace 根或 workspace 下的普通子目录。**
> 原因：许多 OpenClaw 宿主配置了 **workspace 自动清理**，会把 workspace 内的文件转移到 archive 类路径或直接删除。种子库一旦落在 workspace 普通目录里，被清理后注入提示词里写死的路径就会**永久失效且无任何报错**——龙虾每次都"查库"，每次都查不到，退化成 AI 味默认审美。
> 放进 `skills/` 内部的理由：`skills/` 的语义是「这个 agent 的能力集合」，清理策略针对的是人格工作区，不会动能力目录。**按语义分层，而不是按目录是否写保护分层。**

## 步骤

1. **放文件**（容器内可读路径，按你的挂载结构调整）。以下命令**在本仓库根目录执行**：

```bash
cd /path/to/agent-taste-seed-system   # 仓库根（clone 出来的目录）
WS=/path/to/workspace                 # ← 改成你的 OpenClaw workspace 根

mkdir -p "$WS/skills/taste/references"

# 决策层文档随 skill 走（TASTE 属能力部件，不属人格部件）
cp TASTE.md "$WS/skills/taste/TASTE.md"
cp templates/SKILL.md "$WS/skills/taste/SKILL.md"

# 旧部署且 skill 内 art-seeds.md 末尾已有风味日志时，先备份再覆盖：
cp -n "$WS/skills/taste/references/art-seeds.md" \
      "$WS/skills/taste/references/art-seeds.md.bak-$(date +%Y%m%d-%H%M%S)" 2>/dev/null || true

# 四层全库整目录覆盖拷贝
cp -R references/. "$WS/skills/taste/references/"
```

装完的结构（四层全库，全部在 skill 内部）：

```
<workspace>/skills/taste/SKILL.md         审美 OS（决策层 + 四层路由）
<workspace>/skills/taste/TASTE.md         审美 OS 文档版
<workspace>/skills/taste/references/
    ├── art-seeds.md                      L1 总库速查（末尾记风味日志）
    ├── moods/                            L2a 情绪档 ×10
    ├── code-genes/                       L2b 代码基因卡 ×12
    └── chapters/                         L2c 风格章档 ×24+后记
```

> **引用形式**：skill 内一切引用**相对 skill 根**（`references/art-seeds.md`、`references/moods/01-…`）。不要写 `<workspace>/taste/...` 这类 workspace 相对路径。

2. **注入提示词**：把 [`AGENT-INJECTION.md`](../AGENT-INJECTION.md) 里的注入提示词整段并入 workspace 的 `AGENTS.md` 或 `SOUL.md`（人格层规则）。注入片段里提到的种子库路径写成 **skill 内部相对路径** `skills/taste/references/art-seeds.md`（相对 workspace 根）——因为人格文件本身在 workspace 根，这是它唯一能写对的形式。

3. **重启/热载** workspace，验证：对龙虾说「画一张 XX 海报」，看它是否先报情绪关键词再动手。

## 从旧布局迁移（workspace 根 `taste/` → skill 内部）

旧版把种子库平铺进 `<workspace>/taste/`，处于清理策略的射程内。迁移是显式动作，**先备份风味日志再覆盖**：

```bash
WS=/path/to/workspace
OLD="$WS/taste"
NEW="$WS/skills/taste"

# 1) 备份旧风味日志（幂等：新落点已有日志则不覆盖）
if [ -f "$OLD/art-seeds.md" ] && [ ! -f "$NEW/references/art-seeds.md" ]; then
  mkdir -p "$NEW/references"
  cp -n "$OLD/art-seeds.md" "$NEW/references/art-seeds.md"
  echo "📦 已迁移风味日志 → $NEW/references/art-seeds.md"
fi

# 2) 补装四层全库（在仓库根执行）
mkdir -p "$NEW/references"
cp TASTE.md "$NEW/TASTE.md"; cp templates/SKILL.md "$NEW/SKILL.md"
cp -R references/. "$NEW/references/"

# 3) 清理旧落点（含旧的 workspace 根 TASTE.md）
rm -rf "$OLD"
rm -f "$WS/TASTE.md"        # 旧版把 TASTE.md 放在 workspace 根，一并清掉
```

## 验证（含 workspace 清理免疫性证明）

```bash
WS=/path/to/workspace
test -r "$WS/skills/taste/references/art-seeds.md" && echo "L1 OK"
test -d "$WS/skills/taste/references/moods"        && echo "L2a OK"
test -d "$WS/skills/taste/references/code-genes"   && echo "L2b OK"
test -d "$WS/skills/taste/references/chapters"     && echo "L2c OK"

# 免疫性证明：把 workspace 整体挪走后，种子库仍可读
mv "$WS" "$WS.moved" \
  && test -r "$WS.moved/skills/taste/references/art-seeds.md" && echo "IMMUNE OK" \
  && mv "$WS.moved" "$WS"
```

> 若宿主清理策略连 `skills/` 都覆盖（罕见），说明该宿主的 `skills/` 不是能力目录语义——改用 [`deploy/generic-agents.md`](generic-agents.md) 情形 A 的仓库路径兜底（clone 到主目录，不进 workspace）。

## 注意

- 多龙虾舰队（多项目）时，每个 workspace 独立放一份；**人格文件不要跨项目串**（工作助手与心理支持类项目的注入语义各自独立）。
- 风味日志记在各自 `<workspace>/skills/taste/references/art-seeds.md` 末尾；定期把好搭配同步回本仓库。
- 不推荐、也不再支持把种子库平铺到 `<workspace>/taste/`——该布局已被本版废弃（见 [`tasks/CHG-20261013-seed-internal-path/`](../tasks/CHG-20261013-seed-internal-path/)）。
