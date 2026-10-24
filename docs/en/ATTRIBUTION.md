# Attribution & AI Disclosure

This document answers three questions: **where this came from**, **how to cite it**, and **which parts involved AI**.

---

## 1. Provenance

| Item | Value |
|---|---|
| Project | **aesthetic-brain** (repository name `agent-taste-seed-system`) |
| Repository | <https://github.com/hhx465453939/agent-taste-seed-system> |
| Author | hhx465453939 |
| First created | 2026-09-24 |
| Source material | *Encyclopedia of Art Styles* (compiled 2026-06-20; 24 chapters, 250+ artists/styles) |
| Content form | Plain text (Markdown). **Contains no images, audio, video, or copies of third-party works** |
| License | Text assets CC BY 4.0 · Code assets MIT (see [`../../LICENSE`](../../LICENSE)) |

### How the content reached its current form

```
Encyclopedia of Art Styles (author's own manuscript, 24 chapters, 250+ artists)
        │  author-written + AI-assisted structuring
        ▼
references/chapters/    25 chapter texts (each with a notice header)
references/art-seeds.md L1 full quick-reference table (one-line seed cards)
references/moods/       L2a mood files ×10 (seeds reorganised by "what the reader should feel")
references/code-genes/  L2b code-gene cards ×12 (styles translated into copy-pasteable CSS variables)
        │
        ▼
TASTE.md / SKILL.md     L0 decision layer: locate emotion → pick genes → translate to parameters → self-check → log
        │
        ▼
demos/                  12 real rendered pages (acceptance material)
```

**The source .docx manuscript is not distributed with this repository** — only the structured Markdown output is.

---

## 2. AI Disclosure

Honest disclosure is a baseline requirement of open licensing and of most platform policies. This repository states plainly:

| Stage | AI used? | Detail |
|---|---|---|
| Encyclopedia writing | **Mostly author-written** | Chapter bodies, artist entries, and style descriptions were written by the author |
| Structuring | **AI-assisted** | Chapter splitting, one-line seed-card extraction, mood classification, CSS variable translation, English keyword completion |
| Decision-layer docs | Author-written + AI-assisted | The five aesthetic rules, the decision workflow, the four-layer routing structure |
| Demo page code | **AI-generated** (pi agent) | `demos/*.html` and `demos/_src/*.py` were produced by a coding agent |
| Demo screenshots | Machine-rendered | Rendered live in headless Chromium; not AI-generated images |

**Producers of the demo material:**

```
Generator        pi agent (a terminal coding agent)
Driver model     DeepSeek V4.1 Flash
Rendering        headless Chromium 143 · 2× device pixel ratio · lossless WebP
Style decisions  this repository's four-layer seed library under references/
```

> **Important**: the core claim of this project is **"make an agent produce work under explicit aesthetic discipline, instead of falling back to its default taste"**.
> The demo pages are **evidence** for that methodology, not free-form AI output — every page's style discipline (whitespace ratio, shadow ratio, hue count, saturation) is asserted by program; see [`../../demos/README.md`](../../demos/README.md).

---

## 3. How to cite

### 3.1 Academic citation

Use [`../../CITATION.cff`](../../CITATION.cff) (GitHub renders a "Cite this repository" button from it).

APA example:

```
hhx465453939. (2026). aesthetic-brain: an aesthetic decision system and style seed
library for AI agents (Version 3.0.0) [Computer software].
https://github.com/hhx465453939/agent-taste-seed-system
```

### 3.2 Attribution inside a work or product

**Recommended form** (replace the angle-bracketed parts with your own details):

```
This work uses aesthetic-brain (author: hhx465453939),
licensed under CC BY 4.0.
Source: https://github.com/hhx465453939/agent-taste-seed-system
Changes: <e.g. "used code-genes/02 Cyber Neon unmodified">
```

**Minimal form** (where space is tight, e.g. a footer):

```
Style decisions: aesthetic-brain · CC BY 4.0
```

### 3.3 Using only the scripts

The scripts are MIT-licensed; keep the copyright notice:

```
Portions of this software use aesthetic-brain's build/QA scripts
(MIT License, Copyright (c) 2026 hhx465453939)
https://github.com/hhx465453939/agent-taste-seed-system
```

---

## 4. Two things attribution must state

The BY condition of CC BY 4.0 requires:

1. **State whether you made changes** — "unmodified", "used only gene card no. X", "extended Y on top of X" all work, but you must say it.
2. **Do not imply endorsement** — do not write "officially supported / certified by aesthetic-brain" unless you actually hold authorisation.

---

## 5. Two hard rules for redistribution

| Rule | Basis |
|---|---|
| New content you add to the seed library **may be distributed under any terms**, including proprietary ones — there is no ShareAlike requirement | CC BY 4.0 has no SA condition |
| **Commercial use needs no separate licence**, but you must keep the attribution, the licence link, and a note of changes | BY (Attribution); there is no NC condition |

Want to give back to the seed library? See [`../../CONTRIBUTING.md`](../../CONTRIBUTING.md).

---

*This document is a compliance notice, not legal advice.*
