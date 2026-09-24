# 🎨 agent-taste-seed-system — 给任何 AI Agent 装上美学大脑

> 一套可移植的「审美操作系统 + 风格种子库」，让 Claude Code / Codex / OpenClaw / pi / workbuddy / codebuddy / Trae / Qoder / hermas 等任何智能体，在视觉创作上摆脱"AI 味默认审美"。
> 来源：编制者自藏《艺术风格百科大全》（24 章 250+ 艺术家/风格）→ 提炼为可执行的审美决策体系。v1.0 · 2026-09-24

## 这是什么

核心思想：**风格即基因** —— 色彩 × 光线 × 笔触 × 构图 × 情绪，五个基因位。
任何视觉产出前，先选基因、再动手：

```
创作任务 → 情绪定位 → 查种子选基因（1主+1辅）→ 基因翻译成参数 → 一句话自检 → 交付 → 用户反馈 → 风味日志 → 种子库进化 → 下次更好
```

## 文件清单

| 文件 | 作用 |
|------|------|
| [`AGENT-INJECTION.md`](AGENT-INJECTION.md) | ⭐ 通用注入提示词 + 部署说明（最小接入看这个） |
| [`TASTE.md`](TASTE.md) | 审美操作系统入口：审美观 5 条 + 决策流程 + 情绪→种子索引 |
| [`references/art-seeds.md`](references/art-seeds.md) | L1 总库速查：全量种子单行表（250+ 艺术家，按需查询勿全文注入） |
| [`references/moods/`](references/moods/) | L2a 情绪档 ×10：每情绪主推种子的五基因详解 + 媒介适配 + 翻车清单 |
| [`references/code-genes/`](references/code-genes/) | L2b 代码基因卡 ×12：写代码出图直接抄的部署提示词 + CSS 变量块 + 反模式 |
| [`references/chapters/`](references/chapters/) | L2c 风格章档 ×24：《艺术风格百科大全》原文全量，每艺术家 2-3 句细述 |
| [`sources/`](sources/) | 源文档归档（docx 原始百科） |
| [`templates/SKILL.md`](templates/SKILL.md) | Claude Code skill 文件（四层路由版，安装脚本直接拷贝用） |
| [`deploy/`](deploy/) | 各类智能体的部署文档 + 一键脚本 |

## 知识库分层架构（重 agent 按需加载，禁止全文注入）

```
L0  TASTE.md                      决策层：情绪定位 → 该查哪层
│
├─ L2a moods/（10 份）            知道情绪时第一落点
│    每情绪 2-3 粒主推种子 · 五基因详解 · 媒介适配 · 翻车清单
│
├─ L2b code-genes/（12 张）       写代码出图（网页/长图/dashboard）
│    部署提示词 + CSS 变量块 + 激活词 + 反模式，直接抄参数
│
├─ L2c chapters/（24 章）         深挖某艺术家/流派
│    原文零删减 · 每艺术家 2-3 句细述 + AI Prompt Keywords
│
└─ L1 art-seeds.md                全量单行速查总表（关键词全局搜）
```

**激活词原理**：艺术家名/风格名是 LLM 预训练美学基因的激活锚点——prompt 里直接点名「马远一角构图」「卡拉瓦乔 Tenebrism」比任何形容词都精准。本系统的职责：帮你选对激活词 + 把激活出的审美翻译成可执行参数。

## 30 秒部署矩阵（找你的 Agent）

| 你的 Agent | 方式 | 文档 |
|-----------|------|------|
| **Claude Code** | skill + CLAUDE.md 薄注入（推荐，一条命令） | [`deploy/claude-code.md`](deploy/claude-code.md) |
| **OpenClaw** | workspace 放置 + SOUL/AGENTS 注入 | [`deploy/openclaw.md`](deploy/openclaw.md) |
| **Codex / pi / workbuddy / codebuddy / Trae / Qoder / hermas** 等读规则文件的 | 全局规则文件薄注入 | [`deploy/generic-agents.md`](deploy/generic-agents.md) |
| 通用 ChatBot / 自定义 Agent（无文件机制） | 系统提示词整段注入 | [`deploy/generic-agents.md`](deploy/generic-agents.md) |

## 最快接入（任何 Agent，3 步）

1. 把 [`TASTE.md`](TASTE.md) 和 [`references/art-seeds.md`](references/art-seeds.md) 放进智能体可读取的工作区（建议目录结构：`TASTE.md` 在根，`references/art-seeds.md` 在旁）
2. 把 [`AGENT-INJECTION.md`](AGENT-INJECTION.md) 里的注入提示词整段复制进系统提示词 / 规则文件
3. 完成。下次视觉任务它会自动：情绪定位 → 查种子 → 翻译基因 → 自检 → 记档

## Claude Code 一行部署

```bash
git clone https://github.com/hhx465453939/agent-taste-seed-system.git \
  && bash agent-taste-seed-system/deploy/install-claude-skill.sh
```

装完后把 [`deploy/claude-code.md`](deploy/claude-code.md) 里的「薄注入片段」贴进 `~/.claude/CLAUDE.md` 即可。

## 使用原则

1. **种子库按需查询，不注入上下文**——创作时按情绪/章节/关键词检索需要的种子卡即可，90KB 全文进上下文是浪费
2. **风味日志是系统的灵魂**——每次交付后把搭配与反馈记进种子库末尾，定期同步回本仓库，越陈越香
3. **本仓库是活文档**——新风格、新配方、新混种，欢迎 PR 补录

## License

MIT
