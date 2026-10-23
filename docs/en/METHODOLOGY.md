# The Five-Gene Methodology

> This document answers one question: **how does "aesthetic judgement" — normally considered unverifiable — become an executable, reviewable engineering action?**
>
> This is the core methodology of **aesthetic-brain**. The seed library is its **material**, the decision layer is its **workflow**, and the demo pages are its **evidence**.

---

## 1. Starting point: why AI visual output always looks the same

Ask any large model to produce a poster, a deck, or a landing page, and it will most likely give you:

- a centred headline plus three evenly spaced cards
- blue-to-purple gradients / generic rounded corners / soft drop shadows
- a nameless "tech feel"

The model isn't too weak. **It isn't making decisions.** It is sampling the most common visual pattern in its training distribution — in other words, the average. The average has no taste, because **taste comes from explicit choices and explicit refusals**.

There are two real causes of missing taste:

1. **No emotion set first**: it starts placing elements without answering "what should the reader feel?"
2. **No style discipline**: it doesn't know what this style *forbids*, so it puts in everything that looks good on its own.

This project supplies those two missing pieces.

---

## 2. Core proposition: style is a genome

> **Style = colour × light × brushwork × composition × emotion**

These five dimensions are the **gene loci** of a style. Tuning a style means tuning these five loci — not changing a background colour.

| Gene locus | What it decides | What it becomes in code |
|---|---|---|
| **Colour** | which colours, how many hues, saturation level, maximum accent area | CSS variables: `--bg` / `--text` / `--accent` / `--line` |
| **Light** | where light comes from, how many sources, warm or cool shadow, highlight ratio | `radial-gradient` glow, `box-shadow`, contrast assertions |
| **Brushwork** | hard or soft edges, outlines, corner-radius range, texture | `border-radius` / `border` / stroke strategy / noise and grid textures |
| **Composition** | which corner the subject anchors, how much whitespace, symmetric or not, grid or whitespace partitioning | layout strategy, whitespace-ratio assertions, alignment rules |
| **Emotion** | what the reader should feel (**this word governs how the other four are tuned**) | not written as CSS directly; it is the constraint when choosing the other four |

**Why a genome rather than a template**: a template copies a finished artefact; a genome inherits a generative rule set. The same genome grows completely different artefacts in different contexts — which is exactly why the 12 demo pages look nothing alike, yet each one can explain why it is laid out the way it is.

---

## 3. Second proposition: an artist's name is an activation token

> **Artist names and style names are activation anchors for the aesthetic genome inside an LLM's pretraining.**

Compare:

```
❌ dim, dramatic, high-contrast classical oil-painting style
```

with:

```
✅ Caravaggio, Tenebrism, chiaroscuro, single candlelight source, deep shadow
```

The second is far more precise. The model's pretraining corpus contains **vast** amounts of work and commentary about Caravaggio, so the token "Caravaggio" activates a whole vector of visual traits that has already been discussed thousands of times. Adjectives are something you construct on the spot; an artist's name is **already anchored in the corpus**.

This repository's job therefore reduces to two things:

1. **Help you pick the right activation token** — route from emotion to the correct seed (`references/moods/`);
2. **Translate the activated aesthetic into executable parameters** — CSS variables, layout rules, prompt skeletons (`references/code-genes/`).

---

## 4. Decision workflow (five steps, none may be skipped)

```
┌─ Step 1  Locate the emotion ────────────────────────────┐
│   Answer first: what should the reader feel?             │
│   One word (awe / healing / tension / nostalgia / absurd)│
│   ❗ The order cannot be reversed. Emotion decides the    │
│     genes — not "pick a style, then justify it"          │
└──────────────────────────────────────────────────────────┘
                        ↓
┌─ Step 2  Pick genes ────────────────────────────────────┐
│   Look up the matching file in references/moods/         │
│   Choose 1 primary gene + at most 1 accent gene          │
│   (mixing is allowed — only one layer deep)              │
└──────────────────────────────────────────────────────────┘
                        ↓
┌─ Step 3  Translate genes by medium ─────────────────────┐
│   HTML / long image  → CSS variable block (copy from     │
│                        code-genes/)                      │
│   AI image           → prompt keywords + artist anchors  │
│   PPT / documents    → layout character: background,     │
│                        headline treatment, density,      │
│                        chart style                       │
│   Outfit / interior  → material and scene: palette       │
│                        logic, light, whitespace, ritual  │
└──────────────────────────────────────────────────────────┘
                        ↓
┌─ Step 4  One-sentence self-check ───────────────────────┐
│   "What is this piece's style genome (primary + accent)?"│
│   Can't answer = it wasn't thought through → back to 1   │
└──────────────────────────────────────────────────────────┘
                        ↓
┌─ Step 5  Log after delivery ────────────────────────────┐
│   Write the pairing and the feedback into                │
│   references/ART-SEEDS-LOG.md (the flavour log)          │
│   Mark ✅ reuse or ❌ avoid → the library keeps evolving │
└──────────────────────────────────────────────────────────┘
```

---

## 5. Five aesthetic laws

These five recur throughout Eastern and Western art history and form the **axiom layer** of every style decision in this project:

### 1. Set the emotion before choosing the genes
The order cannot be reversed. Skipping emotion and picking a style directly lets visual form dictate content — a common starting point for design failure.

### 2. One primary gene per piece
Klimt's gold plus Mondrian's grid is a hash. A single piece may carry **one dominant gene plus at most one accent gene**. "Mixing is allowed — only one layer deep" is a hard boundary.

### 3. Four hues maximum; one corner radius and one stroke style throughout
Uncontrolled colour count is the primary source of cheapness. Inconsistent corner radii and stroke styles make a page look assembled from three different projects.

### 4. Whitespace and restraint are universal sophistication
Ma Yuan's "one corner, half a view", Ni Zan's sparseness, Newman's zip, Agnes Martin's grid, Nordic emptiness — **East and West independently prove the same thing**: "less" projects more confidence than "more".

### 5. Eastern genes are a differentiation weapon
Whitespace, ink wash, line drawing, breathing gaps — rare in Western design vocabulary, native to a Chinese-speaking context. Cross-cultural hybrids (the James Jean / Wu Guanzhong route) are the easiest way to build recognisability.

---

## 6. Verifiability: turning aesthetic discipline into assertions

**This is the most fundamental difference between this project and "a pile of style description documents".**

Discipline alone is not enough — it must be decidable, otherwise it is just adjectives. So each gene card's hard discipline is translated into **pixel-level assertions over the rendered result**:

| Style gene | Discipline (natural language) | Assertion (decidable) |
|---|---|---|
| Chinese painting whitespace | whitespace should dominate; cinnabar only as a dot | `whitespace ≥62%` · `coloured pixels ≤6%` · `hues ≤3` |
| Baroque tenebrism | one light source only; darkness must occupy the frame | `shadow ≥45%` · `highlight ≤12%` |
| Minimalism | whitespace is the point; one solid accent block | `whitespace ≥46%` · `hues ≤2` |
| Gothic dark | the materiality of lead and ash; no pure black | `shadow ≥58%` · `hues ≤3` |

Implementation: [`../../demos/_src/qa_style.py`](../../demos/_src/qa_style.py) **infers** luminance, shadow ratio, whitespace ratio, distinct hue count, and coloured-pixel ratio directly from the screenshot, then compares each against the thresholds above.

Meanwhile [`../../demos/_src/qa_layout.py`](../../demos/_src/qa_layout.py) blocks a different class of accident: overflow, out-of-bounds elements, overlaps, undersized type, and **insufficient WCAG contrast** (computed against the actual background: 4.5:1 for body text, 3:1 for large text).

**Result**: 12 pieces, 34 style assertions, 13 layout checks — all reproducible, all regression-testable.

> Why this matters: once discipline is decidable, "having taste" stops being a subjective judgement and becomes **an engineering property that can pass a regression test**. Run it in CI and you know whether it degraded.

---

## 7. The boundaries of this method (stated honestly)

| It **can** | It **cannot** |
|---|---|
| Free output from the "default AI aesthetic" | Replace a designer's originality |
| Turn style decisions into a reproducible, reviewable process | Guarantee that the output is "sophisticated" (that is a human judgement) |
| Provide style activation tokens and executable parameters for 250+ artists | Replicate a living creator's personal style (see [`TRADEMARKS.md`](TRADEMARKS.md)) |
| Make style discipline regression-testable | Cover every visual medium (code-gene cards currently focus on web pages and long images) |
| Make taste transferable and cumulative within a team | Absolve you of responsibility for the compliance of what you generate |

**On living artists**: this repository contains **factual style descriptions and generic keywords**. It offers an aesthetic decision method, **not a tool for replicating living creators**. Selling "generate in the style of <artist>" as a product claim touches personality rights and unfair-competition law — please hold that line.

---

## 8. How to take part in evolving the method

The methodology is not fixed. The most effective contribution is **writing back real results**:

```markdown
- YYYY-MM-DD piece: <primary gene> × <accent gene>, key parameters → outcome ✅ / ⚠️ / ❌
```

Honest **failure records are worth more than success records** — they tell us which discipline needs reinforcing.

See [`../../CONTRIBUTING.md`](../../CONTRIBUTING.md).

---

## Further reading

| If you want to know | Go to |
|---|---|
| What this is overall, and how to deploy it | [`../../README.md`](../../README.md) |
| A quick-reference version of the workflow | [`../../SKILL.md`](../../SKILL.md) |
| Which seed to pick for a given emotion | [`../../references/moods/`](../../references/moods/) |
| How to translate a style into CSS | [`../../references/code-genes/`](../../references/code-genes/) |
| A detailed write-up of an artist | [`../../references/chapters/`](../../references/chapters/) |
| Real-world pairing records | [`../../references/ART-SEEDS-LOG.md`](../../references/ART-SEEDS-LOG.md) |
| Licensing, attribution, trademarks | [`../../LICENSE`](../../LICENSE) · [`ATTRIBUTION.md`](ATTRIBUTION.md) · [`TRADEMARKS.md`](TRADEMARKS.md) |

---

*This document explains a methodology; it is not legal advice.* 🎨
