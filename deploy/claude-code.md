# Claude Code 部署 — 美学大脑

> 方案：**薄全局注入（CLAUDE.md）+ 美学 skill 调用 + 厚实种子库 reference（四层：总库/情绪档/代码基因卡/风格章档）**。
> 日常会话只背 ~10 行薄注入；约 400KB 种子库躺在 skill 目录里按需查，不占上下文。

## 方式 A：一键脚本（推荐）

```bash
git clone https://github.com/hhx465453939/agent-taste-seed-system.git
bash agent-taste-seed-system/deploy/install-claude-skill.sh
```

脚本做三件事：建 `~/.claude/skills/taste/` → 拷入 `SKILL.md`（来自 `templates/SKILL.md`）→ 拷入 `references/art-seeds.md`。已装过会先备份旧种子库再覆盖。

## 方式 B：手动

```bash
mkdir -p ~/.claude/skills/taste/references
cp templates/SKILL.md ~/.claude/skills/taste/SKILL.md
cp references/art-seeds.md ~/.claude/skills/taste/references/art-seeds.md
```

## 第二步：薄注入片段（必做，复制整段贴进 `~/.claude/CLAUDE.md` 末尾）

```markdown
## 🎨 美学大脑（Taste Seed System）

本机 Claude Code 已装备美学大脑：24 章 250+ 艺术家风格种子库 + 情绪档 + 代码基因卡（`~/.claude/skills/taste/`）。

- **触发**：任何带视觉属性的任务（长图/海报/PPT/图表/插画/UI/皮肤/封面/配图/配色/前端页面视觉/视频分镜）——先调用 `taste` skill 再动手。
- **流程**：情绪定位（读者该感受什么，一个词）→ 按四层路由查种子（moods/ 情绪档 → code-genes/ 抄 CSS 参数 → chapters/ 深挖艺术家）选 1 主 + 1 辅基因 → 五基因翻译成具体参数 → 一句话自检 → 交付后记风味日志。
- **激活词原理**：艺术家名/风格名是 LLM 预训练美学基因的激活锚点，prompt 直接点名（如「马远一角构图」）比形容词精准。
- **红线**：禁止"AI 味默认审美"（通用卡片/蓝紫渐变）；一组作品一个主基因，敢混搭只混一层；种子库按需查询、禁止全文注入上下文。
```

> 已有全局规则的项目（CLAUDE.md 内容很多）也只加这 ~10 行——种子库永远不进 CLAUDE.md。

## 第三步：验证

新开一个 Claude Code 会话，说「给我做一张 XX 主题的海报」。合格表现：

1. 它先问/先定**情绪关键词**，再动手
2. 交付时能一句话说出「这张作品的风格基因是什么（主+辅）」
3. `~/.claude/skills/taste/references/art-seeds.md` 末尾出现新的风味日志条目

## 风味日志的回流

日志记在安装副本（`~/.claude/skills/taste/references/art-seeds.md` 末尾）。本仓库是上游：验证过的好搭配，定期把日志新条目同步回本仓库 `references/art-seeds.md`（重装脚本覆盖前也会自动备份旧日志）。重装后想找回旧日志看 `references/art-seeds.md.bak-*`。
