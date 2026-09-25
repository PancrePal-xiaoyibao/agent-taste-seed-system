# Changelog

## v1.0.1 · 2026-09-25

部署路径一致性修复（OpenClaw 实际部署反馈发现，经多路对抗核查补全）。

**路径自适配**
- `TASTE.md` 路径适配各部署形态：种子库引用不再写死仓库布局路径，文首标注「仓库 = `references/`、OpenClaw workspace = `taste/`」，并给出按文件名 `art-seeds.md` 定位的兜底方式；速查说明补入 `moods/`/`code-genes/`/`chapters/` 深挖层（标注"部署了全库时"）。
- 种子库侧导航同步自适配：`references/art-seeds.md` 头部「四层知识库导航」不再写死 `../TASTE.md`（该路径在 Claude Code skill 形态必失效），改为按部署形态定位 + 按文件名兜底；`references/chapters/` 全部 25 个文件头部注释同步修正。
- 修复 `TASTE.md` 决策流程 Step 5 的日志位置残留 `taste/log.md`（该文件在任何部署形态都不存在）→ 统一为「种子库 `art-seeds.md` 末尾风味日志」，与全部部署文档及实际约定一致。

**部署文档修正**
- `deploy/openclaw.md` 升级为四层全库部署：`references/` 目录内容平铺进 workspace `taste/`（旧两文件部署重跑命令即可补齐），新增覆盖前自动备份风味日志的步骤、装后结构说明与「在仓库根目录执行」前提。
- `deploy/claude-code.md`：手动方式（方式 B）由只拷两个文件改为 `references/` 整目录覆盖拷贝（原方式装完 `moods/`/`code-genes/`/`chapters/` 三层缺失，四层路由会落空）；一键脚本描述修正为与脚本实际行为一致（脚本内注释同步对齐）；补方式 B 的目录前提；种子库体积口径 400KB → 约 300KB。
- `AGENT-INJECTION.md` 部署说明表按形态拆行：原表把 OpenClaw / Claude Code / Codex 压成一行 OpenClaw 式指令，与三份权威部署文档冲突（Claude Code 走 skill 方案、Codex 走 clone 原样布局），现各自指向对应部署文档。
- `README.md` 一键指令、文件清单、「部署成功的标准」同步以上约定；新增无文件写入形态（ChatBot 附件/知识库）的验收豁免口径。

**口径杂项**
- `chapters/` 实为 24 章 + 后记（25 个文件）——原 `ch00-前言.md` 正文即全书后记，错名已纠正为 `ch25-后记.md`，各处计数标注统一；TASTE.md 艺术家数量口径 200+ → 250+（与全仓一致）；百科章系枚举补漏「样式主义」；TASTE.md「原文由编制者自留」旧说法改为指向仓库内 `references/chapters/` 与 `sources/`；版本戳更新。

## v1.0.0 · 2026-09-24

首个公开发布版本。

- 收录《艺术风格百科大全》全量提炼三件套：`TASTE.md`（审美 OS）、`references/art-seeds.md`（24 章 250+ 艺术家全量种子库）、`AGENT-INJECTION.md`（通用注入提示词），内容与 OpenClaw 工作站原始版本一致（零删减）。
- **四层知识库建档**（重 agent 按需加载）：
  - `references/chapters/` ×24+1：《艺术风格百科大全》docx 原文逐章拆分，零删减（源 docx 归档于 `sources/`）；
  - `references/moods/` ×10：情绪选种档案（科技酷感/梦幻治愈/热血冲击/庄重典雅/甜美容爱/孤独诗意/荒诞幽默/暗黑崇高/清晰理性/东方古韵），每份含主推种子五基因详解 + 媒介适配 + 混种配方 + 翻车清单；
  - `references/code-genes/` ×12：代码基因卡（瑞士平面/赛博霓虹/中国画留白/极简/吉卜力/浮世绘/巴洛克聚光/洛可可粉彩/波普/构成主义/赛璐璐/哥特暗黑），每张含激活词 + 可直接生效的部署提示词 + CSS 变量块 + 反模式。
- **激活词原理**写入 skill：艺术家名/风格名是 LLM 预训练美学基因的激活锚点，prompt 点名 > 形容词。
- 相对原始工作站版本的适配（仅路径与分发说明，内容未动）：
  - `TASTE.md` 中种子库路径 `taste/art-seeds.md` → `references/art-seeds.md`（适配本仓库布局）；
  - 原始 README（系统总览）内容并入本仓库 `README.md` 并扩写为部署矩阵入口。
- 新增部署层：Claude Code skill 方案（`templates/SKILL.md` 四层路由版 + `deploy/install-claude-skill.sh` 整目录同步 + CLAUDE.md 薄注入）、OpenClaw workspace 方案、通用规则文件/系统提示词方案。
