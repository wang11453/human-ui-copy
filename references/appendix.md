# Appendix — human-ui-copy

Long-form details, examples and language-specific fingerprints. [`../SKILL.md`](../SKILL.md) is the working checklist; this file is for humans and for reviewers who need the reasoning.

## Copy tells

| Where | ❌ Tell | ✅ Fix |
|---|---|---|
| Tool page | `生成在本地完成 - 内容不出浏览器` | `本地处理，秒出结果` |
| Empty state | `暂无数据（数据由后端 API 提供）` | `还没有内容，点右上角新建一个` |
| Error message | `请求失败：status=401` | `登录过期了，重新登录一下` |
| HTML | `<!-- 这里是生成按钮 -->` | remove |
| Shipped JS | `console.log('debug')` left in | remove |
| Code comment | `// 需求：实现导出（待办：加进度条）` | `// 导出走流式，避免大文件卡内存` |
| Meta line | `A · B · C` note row | one sentence, or a real list |
| Section note | `此功能由前端实现` | delete — the visitor never asked |

## Structure fingerprints

1. **Centered hero** — centered title, one-line subtitle, two buttons.
2. **Three-card grid** — icon + title + one sentence, always exactly three.
3. **Gradient + glass + big radius** — purple/blue, `rounded-2xl`, frosted panel, soft shadow.
4. **Emoji as icons** — 🚀 ✨ 🔒 ⚡.
5. **Meta note rows** — subject-less lines separated by `·`.
6. **Invented statistics** — `10k+`, `99.9%`, `24/7`, no source.
7. **FAQ accordion + closing CTA** — the hero's button again.
8. **Marketing filler** — 一站式 / 无缝 / 赋能 / 极致 / 丝滑.
9. **Motion without logic** — hover lift, `transition: all .3s`, where movement means nothing.
10. **Happy path only** — no empty, error, loading or long-input state.

**Structural judgement:** AI is even, people are lopsided. A human page has a heavier section, a colour that is *almost* consistent, a joke or a real screenshot, a 3px misalignment fixed by hand.

## Template justification and component libraries

Ask: is the count driven by content? Does deleting one lose information? Is each card self-standing? Is the count `map`/`v-for`-driven, or three near-identical blocks?

| Signals | Reading | Action |
|---|---|---|
| library component + data-driven + reused across the site | library shape | leave structure; audit copy, states, specifics |
| library component + hardcoded ×3 + only this page | generated pile | make data-driven, or cut to content |
| hand-written, three near-identical blocks | generated pile | apply asymmetry |

**The library owns the shape; you own the content, the states and the specifics.**

## Internationalization

- **Chinese** — `·` note rows; 一站式 / 无缝 / 赋能 / 极致; subject-less fragments; 「为你」 openings.
- **English** — seamless / empower / elevate / unlock / supercharge; Title Case body copy; em-dash-heavy sentences; `built with ❤️`; `Ready to get started?`.
- **Japanese** — excessive 敬語 in tool UI; です・ます mixed with 体言止め; ぜひ stacking.
- **All** — empty/error/loading states; one language having them while another does not *is* the tell.
- Also: long-string overflow (German, Finnish), RTL mirroring, numerals and dates.

## Public artifacts

Environment leakage — a public artifact written as if the author's machine were everyone's:

- Absolute paths (`C:\Users\me\project\…`, `/Users/me/…`, `D:\work\…`)
- Real usernames, hostnames, account IDs, e-mails in commands or screenshots
- Internal repo names, intranet IPs
- The author's tool names as if universal
- Single-platform assumptions (`⌘` only, `Ctrl` only, one shell)
- Pinned versions written as minimums

**Markdown tells** — "以下是…" openings; a summary after every section; all emoji ✅/❌ tables instead of a sentence; a TL;DR longer than the document; every list item the same length; every section with exactly three subsections.

**Code-block tells** — `// ... rest of code`; comments restating the code; pseudocode labelled runnable; hallucinated APIs; one example showing five unrelated features.

**Rules** — abstract the environment; no personal identifiers; no OS assumptions; concrete examples, generic defaults.

## Page states (SPA, SSR, SSG)

| State | Check |
|---|---|
| Empty | empty-state copy, and whether it exists |
| Loading | skeleton/spinner, no fake content presented as real |
| Error | result-first copy, retry path |
| Full / long | overflow, truncation, very long names |
| Offline / slow | degradation, cached state |

- **SPA** — focus management and document title on route change; accessible item counts in virtualized lists; a real loading state instead of a blank shell.
- **SSR / SSG** — audit the **pre-hydration shell** as its own state (copy and layout in the first HTML), the **hydration flash** (placeholder text or content jumping when JS takes over), and the **no-JS read-through**; SSG pages are the easiest place to ship a shell that says nothing.

## Over-correction

Applying this skill badly creates a new tell.

| ❌ Over-corrected | ✅ Intentional |
|---|---|
| Adding an in-joke nobody in the audience shares "for a project-only detail" | Using a real, specific number: `支持 200 MB 以内的 PDF，超过会提示` |
| A full-bleed banner added to "break the grid" that carries an image and no information | Replacing one section with a real screenshot and a paragraph, leaving the rest plain |
| Removing the object to sound casual: `点我` | `下载拆分后的 PDF` |
| Deleting real content to look hand-made | Keeping all content, but making one section deliberately heavy |
| Inventing numbers to look specific | Removing the number and stating a verifiable limit |
| Breaking the grid in every section | Exactly one grid break per page |

**Blind test** — after the fix, another reviewer looks without context. If they can say "this page was AI-edited", it was over-corrected.

## Accessibility notes

- Screen readers follow semantics and DOM order, not visual order. `order`/`grid-area` used for visual asymmetry breaks both keyboard and reading order.
- Link lists are read out of context — `更多` ten times is unusable.
- Error copy: result first, action second.
- Decorative emoji icons, stickers and duplicate oversized numbers: `aria-hidden="true"`.
- `prefers-reduced-motion` applies to intentional animation too.
- Contrast and hit areas are defects, never style.

## The checker (`check.py`)

Mechanical `must` items get a script so the same audit can be re-run and compared:

```
python check.py <file-or-dir>          # human-readable
python check.py <file-or-dir> --json   # machine-readable
python tests/run_tests.py              # regression against tests/fixtures
```

What it checks: `console.*` residue, `debugger`, middot note rows in prose, absolute paths, numbers without a visible source (warn only), and whether any empty/loading/error state exists at all (warn only).

Scoping rules worth knowing:

- `.md` files never fail — documentation has to quote the tells it bans, so findings there are notes.
- Inline code and 「…」-quoted spans are ignored for prose rules.
- `tests/` and `examples/` are skipped on directory scans (they contain deliberate tells); point the script at a file inside them to see it work.
- It reports counts, not judgements. "395 SVGs" is a count; "fix the icon-only buttons first" is the audit.

## The checker (`check.py`)

Mechanical items get a script so the same audit can be re-run and compared:

```
python check.py <file-or-dir>                          # generic
python check.py <file-or-dir> --profile game|tool|marketing
python check.py <file-or-dir> --json
python tests/run_tests.py                              # regression against tests/fixtures
```

Profiles exist because the whitelist has to reach the script:

| Profile | Separators | Numeric claims | Structural musts |
|---|---|---|---|
| `generic` | must | warn | enforced |
| `tool` | must | warn | enforced |
| `marketing` | warn | warn | skipped |
| `game` | warn | skipped | enforced (states still matter) |

What it checks: `console.*` residue, `debugger`, middot separators in prose, and absolute paths. Numeric claims are **opt-in** (`--claims`), because content that states real numbers has no "source" to cite.

Scoping rules worth knowing:

- `.md` files never fail — documentation has to quote the tells it bans.
- Inline code and 「…」-quoted spans are ignored for prose rules; so are tag attributes and `<script>`/`<style>` blocks.
- Lines longer than 400 characters are treated as bundled code and skipped; `*.min.js` / `*.min.css` are never scanned.
- `tests/` and `examples/` are skipped on directory scans (they contain deliberate tells).
- Any line can be exempted with a `hui-check: ignore` comment.

**A green run is not a pass.** What the checker cannot see, on purpose or by limitation:

- `console["log"]`, `console?.log`, or a log bundled into a line over 400 characters
- `&middot;` / `&#183;` entities, and any separator produced at runtime
- UNC paths (`\\server\share`) and `file:///` URLs
- text built in JS, CSS-in-JS, or template literals
- every state that only exists after the page runs: empty, loading, error, offline
- anything the profile deliberately downgrades

So the division of labour is: the script counts four patterns, the **agent judges** everything else. A silent run means "no mechanical finding", not "this page is fine". Never report a green run as an approval.

**False-positive policy (measured).** Nine pages of a live hand-written site — home, game index, tool index, one calculator, the lab, docs, feedback, the team page, a user page — produce **0 must and 0 warn**. The demo pages that are supposed to fail still produce 7 and 6. The target is that a clean page says nothing at all; a checker that cries wolf gets ignored.

**Measured false-positive history (2026-10-18):** a 1737-line game page produced 96 musts under `generic` (all table separators) and 0 under `game`; a real page with a bundled library produced 2 more (minified `console.warn`); SVG filter attributes produced 4 more (`x="-50%" width="200%"`). All four classes are fixed, and each one is listed above so the fix is auditable.

## Game and entertainment products (whitelist)

Games are full of things this skill would otherwise flag. These are conventions, not AI flavor:

- **Flavor copy** — world-building text, item descriptions, NPC lines. Length and rhythm are intentional.
- **Ceremony** — staged reveals, unskippable intros, victory screens.
- **Feedback animation** — shake, flash, pop, because the action needs to feel like something.
- **Rule explanations** — dense how-to-play text that a marketing page would never ship.
- **Achievement toasts and progress bars** — celebration by design.
- **Exaggerated statistics** — a "-90% damage" badge is a game number, not a claim.

Still applies: empty/error states (a dead lobby with no message is still a bug), link and button text, focus order.

Game state checklist: **first play** (before any save), **end state** (win/lose/credits), **bankrupt/spent** (zero currency, no items), **return visit** (save exists, but days later).

## Component-library default looks

Independent of structure, some pages read as generated because they kept a library's default skin:

| Default look | What it signals | Fix |
|---|---|---|
| shadcn defaults, untouched | "generated dashboard" | change the tokens (radius, shadow, spacing scale) |
| Tailwind's default blue (`blue-500/600`) | "no decision was made" | one brand accent, neutral greys elsewhere |
| Inter everywhere, no type scale | "template" | pick a pairing or a scale with contrast |
| Lucide/Feather icons at default 24px | "starter kit" | adjust optical size and stroke, or draw one icon |
| Uniform `rounded-xl` on every surface | "AI polish" | vary by hierarchy: inputs sharper, cards softer |

The library owns the shape; the tokens, the type scale and the one bespoke detail are yours.

## Contributing

- **Convertible to `must`** (enumerable, mechanical): missing states; leftover task notes / `console.log`; hardcoded paths; unsourced numbers; visual order ≠ DOM order; more than three hardcoded identical cards.
- **Stays `judgement`** (needs context): "sounds human"; "too even"; whether a project-specific detail is *useful*; whether a template shape is justified by the product.
- **Method**: replace a feeling with a countable fact. "Three or more cards with no data source" can be `must`; "this page feels generated" cannot.
