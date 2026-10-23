# Trademarks & Names Notice

**Scope**: every file in this repository — the seed library, chapter texts, code-gene cards, mood cards, documentation, and demo pages.

---

## One-sentence notice

Every third-party **trademark, brand name, work title, company name, and creator name** that appears in this repository is used **descriptively (nominative / descriptive use)** — to state art-history facts, to attribute a style movement, or to discuss technical characteristics of a visual style.

It does **not** constitute:

- any affiliation, sponsorship, endorsement, or license from the rights holder;
- any claim of any kind over a third-party trademark;
- any reproduction, derivative work, or redistribution of a copyrighted work (this repository contains **no** images of third-party works).

**All rights remain with their respective owners.** This repository's own name, logo, and visual identity use **no** third-party elements.

---

## Types of names that actually appear (ordered by risk, low to high)

| Type | Examples | Nature | Treatment |
|---|---|---|---|
| Deceased artists | Caravaggio, Ma Yuan, Ni Zan, Hokusai, Van Gogh, Böcklin | Art-history fact, public domain | No action needed; names are not copyrightable |
| Historical movements / techniques | Tenebrism, ukiyo-e, nishiki-e, Bauhaus | Generic art terminology | No action needed |
| Living creators | Rella, Yoneyama Mai, Loundraw, wlop, ASK, neco, etc. | Factual mention + personality-rights sensitivity | See dedicated section below |
| Company / studio styles | Studio Ghibli, Kyoto Animation, Trigger, Pixiv | Factual style attribution | See dedicated section below |
| Commercial trademarks | VOCALOID, Photoshop, Pixiv, Twitter/X, Weibo | Nominative use | See dedicated section below |
| Work titles | *Gu Dao*, *Blue Ocean Girl*, *Literature Girl*, *Dragon Ball*, *Evangelion*, etc. | Factual citation of a title | See dedicated section below |

**The distinction this notice rests on**: what this repository collects is **descriptive prose and generic English keyword phrases** (for example `Rella, VOCALOID, transparent, soft lighting, dreamy, pastel`) — **not** images, screenshots, source passages, or long paraphrases of any work.

---

## 1. Living creators (P0 concern)

`references/chapters/ch23-当代二次元插画师.md` covers the styles of several **living contemporary illustrators**.

**What this repository does, and does not do:**

1. **Factual style description only.** Entries describe publicly discussable visual traits — "known for transparency, soft light, and dreamy palettes" — not reproductions or derivatives of their work.
2. **Zero artwork images.** No image, screenshot, or derivative graphic by a living creator appears anywhere in this repository (see the self-check below).
3. **Zero quotation.** No interview, social-media post, or art-book text is quoted or paraphrased.
4. **Names point at people, not at partnerships.** A name identifies its owner; it never implies collaboration.

**⚠️ Red lines for downstream users:**

- ❌ Do **not** use "generate in the style of <artist name>" as a product claim or marketing pitch. A living artist's name plus commercial AI generation touches **personality rights, reputation, and unfair-competition** law — a topic the Japanese illustration community is especially sensitive to.
- ❌ Do **not** feed this repository's keywords to a model as a batch instruction to imitate a living creator for commercial output.
- ✅ Correct use: treat the keywords as **descriptions of visual traits** (transparency, soft light, pastel), applied to the **visual character you want** — not to "get XX's style".

> The relationship between generative AI and artists' rights is still evolving in law and ethics.
> This repository provides an **aesthetic decision method**, not a tool for **replicating living creators**.
> Users remain responsible for the compliance of whatever they generate.

---

## 2. Company / studio styles

Entries that name `Studio Ghibli`, `Kyoto Animation`, `Trigger`, or `Pixiv` are **style attribution** — they record who systematised a given visual character historically.

- Their presence does not imply partnership with the company;
- Their logos, characters, and artwork screenshots must **not** be used as branding for this project or any derivative.

---

## 3. Commercial trademarks

| Name | Rights holder (nominative) | Use in this repository |
|---|---|---|
| VOCALOID / Hatsune Miku | Yamaha / Crypton Future Media | Describing the source of an illustration subject |
| Pixiv / Twitter / Weibo | Respective platform owners | Describing where creators publish |
| Photoshop | Adobe | Describing a conventional toolchain (the software itself is not included) |
| EVA / Evangelion | khara | Describing an animation style reference |
| GeGeGe no Kitarō / Dragon Ball, etc. | Respective rights holders | Describing a visual-language reference |

All of the above is **nominative use**: the name is used to refer to the thing itself, not to borrow its goodwill.

---

## 4. Work titles

Titles appearing in 《book-title marks》 are **factual citations of a title**, used to name a style reference.

This repository contains **none** of the following:

- any passage, script, lyric, or dialogue from a work;
- any image, screenshot, or storyboard from a work;
- any plot summary of a work.

---

## Self-check: confirm there are no third-party assets

The commands below should return **empty** (except for this repository's own generated `demos/_assets/`):

```bash
# 1) No image / audio / video / binary assets
#    (demos/_assets holds this project's own rendered screenshots and font subsets)
git ls-files | grep -iE '\.(jpg|jpeg|png|gif|webp|bmp|tiff|pdf|mp3|mp4|wav|mov|psd|ai|eps)$' \
  | grep -v '^demos/_assets/'

# 2) No traces of transcription from external sources
#    The CJK pattern list stays in the Chinese edition (../TRADEMARKS.md, self-check section)
#    and is enforced in CI on every push by scripts/check_assets.sh.

# 3) No externally hosted images (demo pages only use local assets)
grep -rnoE 'https?://[^"'"'"' )]+\.(png|jpg|jpeg|gif|webp|svg)' --include='*.html' --include='*.md' .
```

All three checks run in CI (`.github/workflows/ci.yml`).

---

## If you believe this repository infringes your rights

Open an Issue (or contact the repository owner directly) stating:

1. the specific file and line numbers;
2. the right you assert (copyright / trademark / personality right);
3. the remedy you want (add attribution / reword / remove the content).

**We commit to responding within 72 hours**, and to preferring **take-down first, discuss second**.

---

*This document is a compliance notice, not legal advice. For specific commercial scenarios, consult a licensed attorney.*
