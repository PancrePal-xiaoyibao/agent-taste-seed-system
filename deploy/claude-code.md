# Claude Code 部署 — 美学大脑

> 方案：**薄全局注入（CLAUDE.md）+ 美学 skill 调用 + 厚实种子库 reference（四层：总库/情绪档/代码基因卡/风格章档）**。
> 日常会话只背 ~10 行薄注入；约 300KB 种子库躺在 skill 目录里按需查，不占上下文。

## 为什么装在 skill 内部（而不是 workspace / 主目录某个文件夹）

**因为很多 agent 宿主在宿主机配置了 workspace 自动清理**——定期把 workspace 内的文件转移到 archive 类路径，或直接删除。种子库一旦落在被清理策略覆盖的目录里，被搬走后注入提示词里写死的路径就**永久失效，而且没有任何报错**：agent 每次都"查库"，每次都查不到，静默退化成 AI 味默认审美。

`~/.claude/skills/taste/references/` 位于 skill 内部——`skills/` 的语义是「这个 agent 的能力集合」，清理策略针对的是人格/工作区，不会动能力目录。**按语义分层，而不是按目录是否写保护分层。**

## 方式 A：一键脚本（推荐）

```bash
git clone https://github.com/hhx465453939/agent-taste-seed-system.git
bash agent-taste-seed-system/deploy/install-claude-skill.sh
```

脚本做的事：建 `~/.claude/skills/taste/` → 拷入 `SKILL.md`（来自仓库根 `SKILL.md`）→ `references/` 整目录覆盖拷贝（art-seeds 总库 + moods/ + code-genes/ + chapters/ 四层全量，重装前预清理三个子目录）。已装过会先备份旧种子库（含风味日志）再覆盖。

## 方式 B：手动（在本仓库根目录执行）

```bash
SKILL_ROOT="$HOME/.claude/skills/taste"
mkdir -p "$SKILL_ROOT/references"
cp SKILL.md "$SKILL_ROOT/SKILL.md"
cp TASTE.md "$SKILL_ROOT/TASTE.md"
cp -R references/. "$SKILL_ROOT/references/"   # 整目录覆盖拷贝，四层全量
```

## 第二步：薄注入片段（必做，复制整段贴进 `~/.claude/CLAUDE.md` 末尾）

```markdown
## 🎨 美学大脑（Taste Seed System）

本机 Claude Code 已装备美学大脑：24 章 250+ 艺术家风格种子库 + 情绪档 + 代码基因卡（`~/.claude/skills/taste/`）。

- **触发**：任何涉及审美与视觉呈现的任务（长图/海报/PPT/图表/插画/UI/皮肤/封面/配图/配色/前端页面视觉/视频分镜/文生图提示词/Word 与文档排版/生活与社会关系审美咨询）——先调用 `taste` skill 再动手。
- **流程**：情绪定位（读者该感受什么，一个词）→ 按四层路由查种子（moods/ 情绪档 → code-genes/ 抄 CSS 参数 → chapters/ 深挖艺术家）选 1 主 + 1 辅基因 → 按媒介翻译成具体参数（HTML→CSS 变量 / PPT→版式 / Word→字体行距样式 / 生图→Prompt Keywords / 生活→材质色彩）→ 一句话自检 → 交付后记风味日志。
- **种子库落点**：全部在 skill 内部（`~/.claude/skills/taste/references/`），引用一律相对 skill 根（`references/art-seeds.md` 等）。**禁止把种子库放进任何 workspace 目录**——会被 workspace 自动清理搬走，导致引用永久失效。
- **激活词原理**：艺术家名/风格名是 LLM 预训练美学基因的激活锚点，prompt 直接点名（如「马远一角构图」）比形容词精准。
- **红线**：禁止"AI 味默认审美"（通用卡片/蓝紫渐变）；一组作品一个主基因，敢混搭只混一层；种子库按需查询、禁止全文注入上下文。
```

> 已有全局规则的项目（CLAUDE.md 内容很多）也只加这 ~10 行——种子库永远不进 CLAUDE.md。

## 第三步：验证

```bash
SKILL_ROOT="$HOME/.claude/skills/taste"
test -r "$SKILL_ROOT/references/art-seeds.md" && echo "L1 OK"
test -d "$SKILL_ROOT/references/moods"        && echo "L2a OK"
test -d "$SKILL_ROOT/references/code-genes"   && echo "L2b OK"
test -d "$SKILL_ROOT/references/chapters"     && echo "L2c OK"
```

新开一个 Claude Code 会话，说「给我做一张 XX 主题的海报」。合格表现：

1. 它先问/先定**情绪关键词**，再动手
2. 交付时能一句话说出「这张作品的风格基因是什么（主+辅）」
3. `~/.claude/skills/taste/references/art-seeds.md` 末尾出现新的风味日志条目

## 风味日志的回流

日志记在安装副本（`~/.claude/skills/taste/references/art-seeds.md` 末尾）。本仓库是上游：验证过的好搭配，定期把日志新条目同步回本仓库 `references/art-seeds.md`（重装脚本覆盖前也会自动备份旧日志）。重装后想找回旧日志看 `references/art-seeds.md.bak-*`。
