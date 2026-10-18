---
name: human-ui-copy
description: Judge, transform and verify AI-written pages and copy. Judges copy perspective and structural evenness with must/judgement scales; transforms a template-shaped page into a specific one with a fixed seven-step procedure; verifies the result with a self-score and a mechanical checker. Includes remediation and delta modes, accessibility intersections, dynamic/SSR states, an explicit whitelist, and a walkthrough example.
license: MIT
---

# human-ui-copy

> Write about what the user gets. Never report what the code does.
> When it looks too even, break it once — without breaking the product, and without over-correcting.

Judging is only a third of the job. **Judge → Transform → Verify.**

**Details:** [`references/appendix.md`](references/appendix.md). **Report example:** [`references/audit-report.md`](references/audit-report.md). **Worked transformation:** [`examples/WALKTHROUGH.md`](examples/WALKTHROUGH.md). **Checker:** [`check.py`](check.py).

## TL;DR

Two layers of AI flavor:

1. **Copy** — the sentence takes the implementer's side instead of the user's.
2. **Structure** — the page is too *even* to have been made by a person.

Judge them, transform the page, then verify you did not over-correct.

## Scope, modes, environment

This is a **heuristic checklist with a transformation recipe — not a linter**. Never override the project's design system.

| Mode | Output |
|---|---|
| `prototype` | Copy rules only; structure may be rough |
| `delivery` | Full audit report, every page state |
| `remediation` | Report **plus a patch** plus a self-score — see below |
| `delta` | Only new or still-unfixed findings |

| Environment | Standard |
|---|---|
| Local / test page | `judgement` relaxed — check `must` only |
| Internal admin / internal docs | `judgement` score ≤ 1 is acceptable |
| Customer-facing page | `judgement` should reach 0 |

Marketing landing pages and kids'/entertainment products: copy rules only (see the appendix whitelist).

## Judgement scales

Every line is `must` (objective) or `judgement` (needs a reviewer).

**"Is the page too even?"** — 0: one section is visibly heavier, plus a project-only detail; 1: sections differ, but nothing project-specific; 2: all sections same shape, page swappable with another product's.

**"Does the copy sound human?"** — 0: every sentence actionable, none explains the build; 1: one or two sentences describe the implementation; 2: the page explains its own architecture to visitors.

Boundary: `1` is fine internally; on customer-facing pages push to 0. Reduce disagreement by **anchoring on evidence**, two-pass blind review, the **delete test** (removing the sentence changes nothing for the visitor → it was leakage) and the **swap test** (replace the product name with a competitor's).

## Judge — must items

**Copy** — `must`: no leftover task notes / requirement text / `console.log`; no new `·` note rows; no architecture claim outside a commitment slot; no author environment in public artifacts; link text stands alone.

**Structure** — `must`: all page states exist; visual order = DOM order; at most one grid break, decoration only; decorative extras `aria-hidden`; no over-correction tells.

Run [`check.py`](check.py) for the mechanical ones instead of eyeballing; quote its output. Pass a **profile** so the whitelist reaches the script: `--profile game` downgrades separators and skips prize numbers, `--profile marketing` skips structural musts, `--profile tool` keeps both.

**Known limit:** on a well-built game page the default profile reports ~100 false positives (odds tables are full of `·`). Always set the profile before quoting a count. On nine pages of a clean site the checker reports nothing at all — that is the intended behaviour, not a failure to find something.

**A green run is not a pass.** The checker only knows four patterns. Regex misses what it was never written for — `console["log"]`, `&middot;`, UNC paths, text generated at runtime, states that only exist after JS runs. When the checker is silent, the review still has to happen; the agent judges, the script merely counts.

Ten structural fingerprints (centered hero, always-three cards, gradient + glass, emoji icons, meta rows, invented stats, FAQ + closing CTA, marketing filler, motion without logic, happy path only) are listed with examples in [appendix#fingerprints](references/appendix.md#structure-fingerprints).

## Transform — the recipe

Use this after judging, when the page is a **task page** (a tool, a dashboard, a document view). Full worked example: [`examples/WALKTHROUGH.md`](examples/WALKTHROUGH.md).

1. **Inventory** — list sections; mark each as content or decoration.
2. **One heavy section** — make it the task itself, and put the action in it. Exactly one section should be visibly bigger.
3. **Checkable specifics** — replace invented numbers with limits or sourced numbers.
4. **Mechanism over features** — replace the feature grid with how it actually works, in numbered prose.
5. **Visible states** — write the empty state out; mention the failure path.
6. **Claims into commitment slots** — move or delete corner notes; keep the claim where a promise belongs.
7. **One honest limitation** — say what the page cannot do.

Do not add decoration to compensate. Each step must reduce the page's symmetry, not increase its ornament.

## Verify — self-score

Before delivering a transformed page, score your own result and report the numbers:

```
Evenness        0 / 1 / 2   (target: 0 on customer-facing pages)
Copy sound human 0 / 1 / 2  (target: 0)
Over-correction none of: in-joke, invented number, deleted content, ornament for asymmetry
States          empty state visible; failure path mentioned
check.py        0 must
```

Any failure sends you back to the step that owns it. A self-score reported honestly is worth more than a page that "feels better".

## `remediation` mode

A report alone is not a fix. When asked to act on an audit, produce all three parts and stop at the human gate:

1. **Restate the authorization.** Which `must` items may be changed? Which `judgement` items, if any?
2. **Fix every `must` item**, with a one-line diff summary each.
3. **Propose the transformation as a patch** — a unified diff or a step-by-step edit plan, never applied silently. Exactly one asymmetry point per round.
4. **Self-score** the proposed result (see Verify), including the over-correction lines.
5. **Wait for confirmation**, then apply.

`judgement` changes are always delivered as a patch for a human to accept, never applied on your own initiative.

## Accessibility intersections

- Colloquial ≠ readable: keep the object (`下载报告`, not `点我`).
- Link and button text must stand alone (screen readers list links out of context).
- Error copy: result first, action second.
- **Visual order must equal DOM order** — asymmetry in decoration only.
- Decorative extras get `aria-hidden="true"` (plus `focusable="false"`). Never do this to an icon that is a control's only name; fix the control with `aria-label` instead.
- `prefers-reduced-motion` still applies to intentional animation.
- Contrast and hit areas are defects, never "flavor".

## Page states

Audit **every state**, not the demo: empty, loading, error, full/long, offline.

- **SPA** — focus management and document title on route change; accessible counts in virtualized lists.
- **SSR / SSG** — also audit the pre-hydration shell, the hydration flash, and the no-JS read-through.

Details: [appendix#states](references/appendix.md#page-states-spa-ssr-ssg).

## Auditing an existing site

1. **Group by class, not by occurrence.** Thirty near-identical cards are one finding.
2. **Order by blast radius** — shared templates and components first.
3. **Report the count once per class**, then the fix for the class. A number alone is not a finding.
4. **Run `check.py` first**, then review what it cannot see (states, originality, copy perspective).

## Over-correction

Manufactured in-jokes, clutter for asymmetry's sake, casual copy that dropped its object, deleted content, invented numbers to look specific, a grid break in every section.

**Blind test:** another reviewer should not be able to say "this page was AI-edited". **One asymmetry point per page; every personality element must carry information.**

## Not AI flavor (whitelist)

Component-library shapes (data-driven, reused); accessibility attributes; a product that genuinely has three features; template layout in `prototype` mode; marketing conventions; statistics with a real source; consistent design-system radii and spacing; minimalism because the product is small; game/entertainment conventions (flavor copy, ceremony, feedback animation, rule explanations, achievement toasts).

## Agent usage

> 使用 human-ui-copy，模式 = `delivery`。输出审计报告：`must` 项逐条 是/否 + 证据；`judgement` 项 0–2 分 + 引用片段 + 依据哪个锚点；结尾给建议清单（`must` 优先）。**不要自动修改 `judgement` 相关的内容** —— 只出报告，人来决定。

- `must` items may be fixed directly; `judgement` items are advisory only, delivered as a patch.
- Every finding cites evidence; "too even" alone is not a finding.
- Propose one asymmetry point, not a redesign.
- Report the mode and the states audited.
- For `remediation`, report the self-score; an unverified rewrite is not a deliverable.

**i18n** — `must`: states exist in every shipped language. `judgement`: filler removed per language, not translated from one list.
