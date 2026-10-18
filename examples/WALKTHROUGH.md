# Walkthrough: `template.html` → `human.html`

The goal of this file is to make the transformation **reproducible**, not tasteful. Same product, same content, two pages. Every step below is: what changed, why, and what to check afterwards.

Open both files side by side while reading. `check.py` gives 7 `must` on the template and 0 on the result.

## 0. Inventory before touching anything

List what the page actually contains:

```
hero (title + claim + 2 buttons)   stats (3 numbers)      cards (3 features)
meta note (1 line)                 faq (2 questions)     cta (repeat button)
footer
```

Mark each as **content** (the visitor needs it) or **decoration** (a slot that exists because templates have it). In the template: the hero is decoration-shaped, stats are invented, cards are generic, the FAQ repeats the hero, and the one thing a visitor came for (the file picker) is three scrolls down.

## 1. Give the page one heavy section, and make it the task

- **Changed:** centered hero with two buttons → left-aligned title with one action (the file picker) directly under it.
- **Why:** the visitor came to split a file. A centered hero with a "Get started" button makes them click to start doing what they already wanted to do.
- **Check:** is there exactly one section that is obviously bigger than the rest? If three sections are the same height, you are not done.

## 2. Turn invented numbers into checkable limits

- **Changed:** `10k+ users`, `99.9% uptime`, `24/7 support` → `PDF only. Up to 200 MB, up to 3000 pages.`
- **Why:** nobody can verify the first three. A limit is information: the visitor learns immediately whether their file qualifies.
- **Check:** can a visitor act on each number? If not, either source it or replace it with a limit.

## 3. Replace the feature grid with the mechanism

- **Changed:** three cards (`Lightning fast` / `Beautifully simple` / `Private by design`) → three numbered paragraphs about the page tree, why pages are copied instead of re-encoded, and how outlines are rewritten.
- **Why:** the cards say what every competitor says; the mechanism is specific to this tool, and it is what a careful user wants to know before handing over a file.
- **Check:** could this paragraph appear on a competitor's page? If yes, it is filler.

## 4. Add the missing states, visibly

- **Changed:** nothing existed → a "Recent" list with a written empty state.
- **Why:** the empty state is the first thing a new visitor sees, and it is the first thing a template forgets. Writing it out also proves the page was designed past the demo.
- **Check:** is there text a visitor sees when they have zero items? Is there something for a failed file?

## 5. Move or delete the meta note

- **Changed:** `Processing happens in your browser · files never leave your device · no upload required` → one footer line plus a real link.
- **Why:** it is a genuine claim in the wrong slot. In a corner it reads as an implementation note; in the footer next to a link it reads as a promise the visitor can follow.
- **Check:** every architecture or privacy claim sits in a commitment slot (hero, footer with link, privacy page), not in a separator row.

## 6. Keep one honest limitation

- **Changed:** nothing → a caveat block: scanned PDFs are images, so a split cannot add selectable text.
- **Why:** this is the strongest specificity signal available. It also prevents the most common support complaint, and it is information rather than decoration.
- **Check:** does the page admit at least one thing it cannot do?

## 7. Verify (this is the step that makes it reproducible)

Run the self-score before showing anyone:

```
Evenness (0–2)       0  — one heavy section, everything else subordinate
Copy sound human     0  — no sentence explains how it was built
Over-correction      none of: in-joke, invented number, deleted content, decoration for asymmetry
States               empty state visible; failure path mentioned
check.py             0 must
```

If any line fails, go back to the step that owns it. Do not add decoration to compensate — that is the over-correction failure mode.

## Diff shape (summary)

```
hero       centered, gradient, 2 buttons     → left, flat, 1 action
stats      removed                            → replaced by limits line
cards      3 equal, emoji icons               → 1 heavy ordered explanation
note       middot meta row                    → footer line + link
faq        removed (repeated the hero)        → replaced by a caveat block
added      —                                  → visible empty state
```

## What does not transfer

The result is specific to a **tool page for a local PDF splitter**. Applying the same moves to a marketing landing page would remove the thing that page exists to do. That is why the skill has a whitelist and a justification test: the recipe is for pages whose job is a task, not a pitch.
