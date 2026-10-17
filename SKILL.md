---
name: human-ui-copy
description: Remove "AI flavor" from pages and copy, without over-correcting. Covers visitor-facing copy (perspective, punctuation, placement) and structure (template symmetry, centered hero, three-card grids, invented stats, missing states), plus judgement scales, accessibility intersections, dynamic/SSR states, and an explicit whitelist. Details, examples, i18n fingerprints and a sample audit report live in appendix.md and examples/.
license: MIT
---

# human-ui-copy

> Write about what the user gets. Never report what the code does.
> When it looks too even, break it once — without breaking the product, and without over-correcting.

**Full details:** [`references/appendix.md`](references/appendix.md) · **Sample output:** [`references/audit-report.md`](references/audit-report.md)

## TL;DR

Two layers of AI flavor:

1. **Copy** — the sentence takes the implementer's side instead of the user's.
2. **Structure** — the page is too *even* to have been made by a person.

Fix the first by rewriting from the user's side. Fix the second with a *small* asymmetry. Then check you did not over-correct.

## Scope, modes, environment

This is a **heuristic checklist, not a linter**. Never override the project's design system. Marketing landing pages and kids'/entertainment products: apply the copy rules only.

| Mode | Run |
|---|---|
| `prototype` | Copy rules only; structure may be rough |
| `delivery` | Everything, in **every page state** |

| Environment | Standard |
|---|---|
| Local / test page | `judgement` relaxed — check `must` only |
| Internal admin / internal docs | `judgement` score ≤ 1 is acceptable |
| Customer-facing page | `judgement` should reach 0 |

## Judgement scales

Every audit line is `must` (objective) or `judgement` (needs a reviewer). Anchors:

**"Is the page too even?"** — 0: one section is visibly heavier, plus a project-only detail · 1: sections differ, but nothing project-specific · 2: all sections same shape, page swappable with another product's.

**"Does the copy sound human?"** — 0: every sentence actionable, none explains the build · 1: one or two sentences describe the implementation · 2: the page explains its own architecture to visitors.

Boundary: `1` is fine internally; on customer-facing pages push to 0. Reduce disagreement by **anchoring on evidence**, two-pass blind review, the **delete test** (removing the sentence changes nothing for the visitor → it was leakage) and the **swap test** (replace the product name with a competitor's).

## Copy rules

1. **Perspective** — user-side benefit, not implementation proof.
   `Runs locally. Results in a second.` ✅ · `Generation is completed locally - content never leaves the browser` ❌
2. **Punctuation** — no `·` / `•` separators inside prose; no subject-less fragments.
3. **Placement** — architecture and security claims only in commitment slots (hero, privacy page, onboarding), never in corner notes.

More tells (including code comments and shipped JS): [appendix#copy-tells](references/appendix.md#copy-tells).

## Structure rules

Ten fingerprints: centered hero · three cards, always three · gradient + glass + big radius · emoji icons · `·` note rows · invented stats · FAQ + closing CTA · marketing filler · motion without logic · happy path only.

**Before calling any of these a problem, run the justification test:**

1. Is the count driven by content? (Deleting one should lose information.)
2. Is each unit self-standing, or is it one claim split three ways?
3. Hardcoded, or `map`/`v-for`/CMS-driven?
4. Does it come from a component library? (origin + site-wide reuse + data-driven = library shape → leave it alone.)

**Fixes** — delete half · one accent color · break the grid exactly once, in decoration · keep one project-only detail with real information · add the missing states.

**Red lines** — never trade usability for personality; contrast, hit areas, focus order and keyboard reachability come first; a second "special" element cancels the first.

## Accessibility intersections

- Colloquial ≠ readable: keep the object (`下载报告`, not `点我`).
- Link and button text must stand alone (screen readers list links out of context).
- Error copy: result first, action second.
- **Visual order must equal DOM order** — asymmetry in decoration only.
- Decorative extras get `aria-hidden="true"`.
- `prefers-reduced-motion` still applies to intentional animation.
- Contrast and hit areas are defects, never "flavor".

## Page states

Audit **every state**, not the demo: empty · loading · error · full/long · offline. A page that only looks finished at 100% data has not been audited.

- **SPA** — route changes need focus management and document title updates; virtualized lists need accessible counts.
- **SSR / SSG** — also audit the pre-hydration shell (initial HTML), the hydration flash (placeholder replaced or content jumping), and the no-JS read-through.

Details: [appendix#states](references/appendix.md#page-states-spa-ssr-ssg).

## Over-correction

Applying this skill badly creates a new tell: manufactured in-jokes, clutter for asymmetry's sake, casual copy that dropped its object, deleted content, invented numbers to look specific, a grid break in every section.

**Blind test:** another reviewer should not be able to say "this page was AI-edited". **One asymmetry point per page; every personality element must carry information.**

Examples: [appendix#over-correction](references/appendix.md#over-correction)

## Not AI flavor (whitelist)

Component-library shapes (data-driven, reused) · accessibility attributes · a product that genuinely has three features · template layout in `prototype` mode · marketing conventions · statistics with a real source · consistent design-system radii and spacing · minimalism because the product is small.

## Agent usage

> 使用 human-ui-copy，模式 = `delivery`。输出审计报告：`must` 项逐条 是/否 + 证据（引用原文或选择器）；`judgement` 项 0–2 分 + 引用片段 + 依据哪个锚点；结尾给建议清单（`must` 优先）。**不要自动修改 `judgement` 相关的内容** —— 只出报告，人来决定。

- `must` items may be fixed directly.
- `judgement` items are advisory only — never rewrite copy style or layout on your own.
- Every finding cites evidence; "too even" alone is not a finding.
- Propose one asymmetry point, not a redesign.
- Report the mode and the states audited.

## Audit before delivery

**Copy** — `must`: no leftover task notes / requirement text / `console.log` · no `·` note rows · no architecture claim outside a commitment slot · no author environment in public artifacts · link text stands alone. `judgement`: comments explain why, not what · "sounds human" = 0.

**Structure** — `must`: all page states exist · every number sourced · visual order = DOM order · at most one grid break, decoration only · decorative extras `aria-hidden` · no over-correction tells. `judgement`: "too even" = 0 (external) / ≤1 (internal) · grid shapes pass the justification test · library components left alone.

**i18n** — `must`: states exist in every shipped language. `judgement`: filler removed per language, not translated from one list.
