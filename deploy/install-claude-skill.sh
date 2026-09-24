#!/usr/bin/env bash
# install-claude-skill.sh — 把 taste 美学大脑装进本机 Claude Code（~/.claude/skills/taste/）
# 用法：bash deploy/install-claude-skill.sh   （在本仓库任意位置可执行，自动定位仓库根）
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DST="${HOME}/.claude/skills/taste"

[[ -f "$SRC/templates/SKILL.md" ]] || { echo "❌ 找不到 $SRC/templates/SKILL.md，请在仓库内运行"; exit 1; }
[[ -f "$SRC/references/art-seeds.md" ]] || { echo "❌ 找不到 $SRC/references/art-seeds.md"; exit 1; }

mkdir -p "$DST"

# 重装保护：旧种子库含风味日志，先备份
if [[ -f "$DST/references/art-seeds.md" ]]; then
  BAK="$DST/references/art-seeds.md.bak-$(date +%Y%m%d-%H%M%S)"
  cp "$DST/references/art-seeds.md" "$BAK"
  echo "📦 已备份旧种子库（含风味日志）→ $BAK"
fi

cp "$SRC/templates/SKILL.md" "$DST/SKILL.md"
# references/ 整目录同步（art-seeds 总库 + chapters/ + moods/ + code-genes/ 四层全量）
mkdir -p "$DST/references"
rm -rf "$DST/references/chapters" "$DST/references/moods" "$DST/references/code-genes"
cp -R "$SRC/references/." "$DST/references/"

echo "✅ taste 美学大脑已安装 → $DST"
echo "   ├─ SKILL.md                  （审美 OS + 四层查询路由）"
echo "   └─ references/"
echo "      ├─ art-seeds.md           （L1 总库速查，250+ 种子）"
echo "      ├─ moods/                 （L2a 10 份情绪选种档案）"
echo "      ├─ code-genes/            （L2b 12 张代码基因卡：CSS 变量+部署提示词）"
echo "      └─ chapters/              （L2c 24 章原文风格档）"
echo "👉 下一步：把 deploy/claude-code.md 里的「薄注入片段」贴进 ~/.claude/CLAUDE.md，新会话生效。"
