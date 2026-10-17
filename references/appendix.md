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

## Contributing

- **Convertible to `must`** (enumerable, mechanical): missing states; leftover task notes / `console.log`; hardcoded paths; unsourced numbers; visual order ≠ DOM order; more than three hardcoded identical cards.
- **Stays `judgement`** (needs context): "sounds human"; "too even"; whether a project-specific detail is *useful*; whether a template shape is justified by the product.
- **Method**: replace a feeling with a countable fact. "Three or more cards with no data source" can be `must`; "this page feels generated" cannot.
