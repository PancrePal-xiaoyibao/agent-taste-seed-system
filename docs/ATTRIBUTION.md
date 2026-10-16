# 出处、署名与 AI 使用披露 / Attribution & AI Disclosure

本文档说明三件事：**这东西从哪来**、**你要引用该怎么写**、**哪些内容是 AI 参与的**。

---

## 一、出处（Provenance）

| 项 | 内容 |
|---|---|
| 项目名 | **美学大脑 / aesthetic-brain**（仓库原名 `agent-taste-seed-system`） |
| 仓库 | <https://github.com/hhx465453939/agent-taste-seed-system> |
| 作者 | hhx465453939 |
| 首次建立 | 2026-09-24 |
| 内容来源 | 《艺术风格百科大全》（2026-06-20 编制，24 章 250+ 艺术家/风格全览） |
| 内容形态 | 纯文本（Markdown）。**不含任何图片、音视频或第三方作品复制品** |
| 许可 | 文本资产 CC BY-NC-SA 4.0 · 代码资产 MIT（见 [`../LICENSE`](../LICENSE)） |

### 内容是怎么变成现在这样的

```
《艺术风格百科大全》（编者自著底稿，24 章 250+ 艺术家）
        │  编者执笔 + AI 辅助结构化整理
        ▼
references/chapters/    25 份分章原文（含免责头）
references/art-seeds.md  L1 全量速查总表（单行种子卡）
references/moods/       L2a 情绪档 ×10（把种子按「读者该感受到什么」重新编排）
references/code-genes/  L2b 代码基因卡 ×12（把风格翻译成可抄的 CSS 变量）
        │
        ▼
TASTE.md / SKILL.md   L0 决策层：情绪定位 → 选基因 → 翻译参数 → 自检 → 记档
        │
        ▼
demos/                  12 张真实渲染的成品页（验收材料）
```

**底稿 docx 不随仓库分发**——仓库只保留结构化后的 Markdown 产物。

---

## 二、AI 使用披露（Disclosure）

诚实披露是开源许可体系与多平台实践的基本要求，本仓库明确声明：

| 环节 | 是否使用 AI | 说明 |
|---|---|---|
| 百科内容撰写 | **编者执笔为主** | 章节正文、艺术家条目、风格描述由编者撰写 |
| 结构化整理 | **AI 辅助** | 分章切分、单行种子卡提炼、情绪档归类、CSS 变量翻译、英文关键词补全 |
| 决策层文档 | 编者执笔 + AI 辅助 | 审美观五条、决策流程、四层路由结构 |
| 演示页代码 | **AI 生成**（pi agent） | `demos/*.html` 与 `demos/_src/*.py` 由编码智能体生成 |
| 演示截图 | 机器渲染 | headless Chromium 实时渲染，非 AI 生图 |

**演示材料的生产者**：

```
生成者         pi agent（终端里的编码智能体）
驱动模型       DeepSeek V4.1 Flash
渲染           headless Chromium 143 · 2× 设备像素比 · 无损 WebP
风格决策依据   本仓库 references/ 四层种子库
```

> **重要**：本项目的核心价值主张是**「让 Agent 按明确的审美纪律产出，而不是按默认审美」**。
> 演示页是这套方法论的**证据**，不是 AI 自由发挥的产物——
> 每一张的风格纪律（留白比例、暗部占比、色相数量、饱和度）都由程序断言，见 [`../demos/README.md`](../demos/README.md)。

---

## 三、怎么署名（Citation）

### 3.1 学术引用

使用 [`CITATION.cff`](../CITATION.cff)（GitHub 会自动生成「Cite this repository」按钮）。

APA 格式示例：

```
hhx465453939. (2026). 美学大脑 / aesthetic-brain: 面向 AI Agent 的审美决策系统与风格种子库
(Version 2.0.0) [Computer software]. https://github.com/hhx465453939/agent-taste-seed-system
```

### 3.2 在作品 / 产品中署名

**推荐格式**（把尖括号内容换成你的实际信息）：

```
本作品使用了「美学大脑 / aesthetic-brain」（作者 hhx465453939），
依据 CC BY-NC-SA 4.0 许可使用。
来源：https://github.com/hhx465453939/agent-taste-seed-system
修改说明：<例如「仅使用 code-genes/02 赛博霓虹，未作修改」>
```

**最小格式**（空间受限时，如页脚）：

```
风格决策：美学大脑 (aesthetic-brain) · CC BY-NC-SA 4.0
```

### 3.3 只在代码里用了脚本

脚本走 MIT，只需保留版权声明：

```
Portions of this software use aesthetic-brain's build/QA scripts
(MIT License, Copyright (c) 2026 hhx465453939)
https://github.com/hhx465453939/agent-taste-seed-system
```

---

## 四、署名必须说明的两件事

CC BY-NC-SA 4.0 的署名条款要求（BY 条件）：

1. **说明是否作了修改**
   「未作修改」/「仅使用其中 X 号基因卡」/「在 X 基础上扩展了 Y」——都行，但必须说。
2. **不得暗示背书**
   不要写成「本项目由 aesthetic-brain 官方支持/认证」——除非你确实获得了授权。

---

## 五、再分发的两条硬规则

| 规则 | 依据 |
|---|---|
| 你补录进种子库的新内容，**必须以 CC BY-NC-SA 4.0 分发** | SA（相同方式共享）条件 |
| **不得用于商业目的**；商用请先开 Issue 洽谈单独许可 | NC（非商业性）条件 |

想回馈种子库？见 [`../CONTRIBUTING.md`](../CONTRIBUTING.md)。

---

*本文件是合规说明，不是法律意见。*
