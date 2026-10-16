#!/usr/bin/env bash
# 开源资产扫描 —— 确认仓库不含高版权权重资产、外部抄录痕迹与敏感信息。
#
# 为什么需要它：本项目的卖点是「纯文本、零第三方资产」。
# 这个前提一旦被无意破坏（有人贴了张图、抄了段百科、提交里带了私钥），
# 项目的合规基础就塌了。所以把它变成 CI 里每次提交都跑的硬闸门。
#
# 用法：  bash scripts/check_assets.sh
# 退出码：0 = 干净；1 = 发现问题（CI 会 fail）

set -uo pipefail
cd "$(dirname "$0")/.." || exit 2

FAIL=0
ok()   { printf '  \033[32m✓\033[0m %s\n' "$*"; }
bad()  { printf '  \033[31m✗\033[0m %s\n' "$*"; FAIL=1; }
head_() { printf '\n\033[1m%s\033[0m\n' "$*"; }

# ── 1. 媒体 / 二进制资产 ──────────────────────────────────────────
# demos/_assets/ 是本项目自产的演示截图（自己渲染的 HTML）与开源字体子集，
# 属于本仓库原创或合规可分发内容，予以豁免；其余一律不允许。
head_ "1. 媒体与二进制资产"
MEDIA=$(git ls-files \
  | grep -iE '\.(jpg|jpeg|png|gif|webp|bmp|tiff|tif|pdf|mp3|mp4|wav|mov|avi|mkv|psd|ai|eps|sketch|fig)$' \
  | grep -v '^demos/_assets/' || true)
if [ -n "$MEDIA" ]; then
  bad "发现未豁免的媒体资产（可能是第三方作品图，不能进库）："
  printf '      %s\n' $MEDIA
else
  ok "无第三方媒体资产（demos/_assets/ 为本项目自产截图与开源字体子集）"
fi

# ── 2. 文档归档 / 压缩包 ──────────────────────────────────────────
# 原始底稿（docx）属于私有资产层：体积大、含完整未结构化内容，
# 开源后会让使用者直接整书复制，也让「结构化产物」的价值归零。
head_ "2. 文档归档与压缩包"
ARCH=$(git ls-files | grep -iE '\.(docx|doc|xlsx|xls|pptx|ppt|zip|tar|tgz|gz|bz2|xz|7z|rar)$' || true)
if [ -n "$ARCH" ]; then
  bad "发现归档/二进制文档（底稿与压缩包不应随包发布）："
  printf '      %s\n' $ARCH
else
  ok "无归档文件（底稿 docx 未随仓库分发）"
fi

# ── 3. 外部抄录痕迹 ──────────────────────────────────────────────
# 内容必须源自本项目自著底稿。出现「转载自 / 百度百科 / 知乎」等字样，
# 意味着可能混入了受第三方著作权保护的文本。
head_ "3. 外部来源与抄录痕迹"
TRACE=$(grep -rnE '百度百科|维基百科|wikipedia\.org|知乎|豆瓣|简书|CSDN|公众号|转载自|原文链接|版权所有' \
  --include='*.md' --include='*.html' . 2>/dev/null \
  | grep -viE 'LICENSE|docs/ATTRIBUTION|docs/TRADEMARKS|check_assets' || true)
if [ -n "$TRACE" ]; then
  bad "发现疑似外部来源痕迹（需人工确认是否属自著内容）："
  printf '      %s\n' "$TRACE"
else
  ok "无外部抄录痕迹"
fi

# ── 4. 外部媒体外链 ──────────────────────────────────────────────
# 演示页必须完全自包含（离线可复现）；引外站图片会同时带来可用性与授权风险。
#
# ⚠️ 徽章服务豁免：shields.io / badgen.net 这类徽章**由文本参数生成**，
#    不含任何第三方作品图像，是开源项目 README 的标准做法
#    （否则每个项目的徽章都会把自己的 CI 卡死）。
#    白名单只放徽章/覆盖率服务，不放任何图库或 CDN。
head_ "4. 外部媒体外链"
EXTLINK=$(grep -rnoE 'https?://[^"'"'"' )>]+\.(png|jpg|jpeg|gif|webp|svg|mp4)' \
  --include='*.html' --include='*.md' --include='*.css' . 2>/dev/null \
  | grep -vE 'shields\.io|badgen\.net|badge\.fury\.io|codecov\.io|coveralls\.io|api\.netlify\.com|/actions/workflows/.*/badge\.svg' || true)
if [ -n "$EXTLINK" ]; then
  bad "发现外部媒体引用（应改为本地资产；徽章服务除外）："
  printf '      %s\n' "$EXTLINK"
else
  ok "无外部媒体引用（演示页自包含；shields.io 等文本生成的徽章已豁免）"
fi

# ── 5. 敏感信息（路径 / 主机 / 凭据） ─────────────────────────────
# 127.0.0.1 与 localhost 是本地示例，不是环境泄漏，豁免。
head_ "5. 敏感信息与内部线索"
SECRET=$(grep -rnE '/home/[a-z0-9_-]+|/Users/[A-Za-z0-9_-]+|C:\\\\Users|[0-9]{1,3}(\.[0-9]{1,3}){3}|BEGIN [A-Z ]*PRIVATE KEY|(api[_-]?key|token|password|passwd|secret)[[:space:]]*[:=][[:space:]]*[^[:space:]]{6,}' \
  --include='*.md' --include='*.py' --include='*.sh' --include='*.yml' --include='*.yaml' \
  --include='*.html' --include='*.cff' --include='*.css' . 2>/dev/null \
  | grep -vE '127\.0\.0\.1|0\.0\.0\.0|check_assets|LICENSE|# |<!--' || true)
if [ -n "$SECRET" ]; then
  bad "发现疑似敏感信息（绝对路径 / 内网地址 / 凭据）："
  printf '      %s\n' "$SECRET"
else
  ok "无敏感信息（绝对路径 / 内网地址 / 凭据均未出现）"
fi

# ── 6. 许可文件齐备性 ────────────────────────────────────────────
head_ "6. 许可与合规文件"
for f in LICENSE LICENSE-CODE.md LICENSE-CONTENT.md LICENSE-FONTS.md \
         CITATION.cff CONTRIBUTING.md docs/TRADEMARKS.md docs/ATTRIBUTION.md; do
  [ -f "$f" ] && ok "$f" || bad "缺少 $f"
done

# ── 结论 ─────────────────────────────────────────────────────────
if [ "$FAIL" -eq 0 ]; then
  printf '\n\033[32m资产扫描通过：仓库可安全公开发布。\033[0m\n'
else
  printf '\n\033[31m资产扫描未通过，请先处理上述问题再发布。\033[0m\n'
fi
exit "$FAIL"
