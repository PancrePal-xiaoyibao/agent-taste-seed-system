# Changelog

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
