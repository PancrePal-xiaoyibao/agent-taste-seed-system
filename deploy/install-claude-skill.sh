#!/usr/bin/env bash
# install-claude-skill.sh — 把 taste 美学大脑装进本机 Claude Code（~/.claude/skills/taste/）
# 用法：bash deploy/install-claude-skill.sh   （在本仓库任意位置可执行，自动定位仓库根）
#
# 落点说明：种子库装在 skill 内部（~/.claude/skills/taste/references/），不在任何 workspace 里。
# 许多 agent 宿主集群的 workspace 自动清理会搬走 workspace 内文件——skill 内部不受影响。
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DST="${HOME}/.claude/skills/taste"

[[ -f "$SRC/SKILL.md" ]] || { echo "❌ 找不到 $SRC/SKILL.md，请在仓库内运行"; exit 1; }
[[ -f "$SRC/references/art-seeds.md" ]] || { echo "❌ 找不到 $SRC/references/art-seeds.md"; exit 1; }

mkdir -p "$DST"

# 重装保护：旧种子库含风味日志，先备份
if [[ -f "$DST/references/art-seeds.md" ]]; then
  BAK="$DST/references/art-seeds.md.bak-$(date +%Y%m%d-%H%M%S)"
  cp "$DST/references/art-seeds.md" "$BAK"
  echo "📦 已备份旧种子库（含风味日志）→ $BAK"
fi

cp "$SRC/SKILL.md" "$DST/SKILL.md"
# 决策层文档随 skill 走（属能力部件，不属人格部件）
cp "$SRC/TASTE.md" "$DST/TASTE.md"
# references/ 整目录覆盖拷贝（art-seeds 总库 + chapters/ + moods/ + code-genes/ 四层全量）
mkdir -p "$DST/references"
rm -rf "$DST/references/chapters" "$DST/references/moods" "$DST/references/code-genes"
cp -R "$SRC/references/." "$DST/references/"

echo "✅ taste 美学大脑已安装 → $DST"
echo "   ├─ SKILL.md                  （审美 OS + 四层查询路由）"
echo "   ├─ TASTE.md                  （决策层文档版）"
echo "   └─ references/"
echo "      ├─ art-seeds.md           （L1 总库速查，250+ 种子）"
echo "      ├─ moods/                 （L2a 10 份情绪选种档案）"
echo "      ├─ code-genes/            （L2b 12 张代码基因卡：CSS 变量+部署提示词）"
echo "      └─ chapters/              （L2c 24 章原文风格档）"
echo "📍 落点说明：种子库在 skill 内部（$DST/references/），不在任何 workspace 里——workspace 自动清理不会搬走它。"
echo "👉 下一步：把 deploy/claude-code.md 里的「薄注入片段」贴进 ~/.claude/CLAUDE.md，新会话生效。"
