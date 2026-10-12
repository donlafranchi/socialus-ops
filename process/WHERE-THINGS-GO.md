# Where things go

Read this every session, before you write anything down. **Each kind of thing has one home.** Agent docs hold current understanding plus the why, never history: git is the history. Human docs are generated snapshots and are never hand-kept. Every maintained doc has a size budget. When a doc passes 80% of its budget, condense it in the same PR that adds to it. If two homes seem to fit, pick the first row that matches. If none fits, use the junk drawer. Paths mean the project's planning repo unless another repo is named. *Draft: rows marked (proposed) wait on a PM call.*

## Maintained: agent docs

| Category | Home | Owner | Kept current by (budget) | Never goes there |
|---|---|---|---|---|
| Principle: the why behind mission and rulings | `DECISIONS.md` | PM rules; planning agent words it | Reworded in place as rulings sharpen it; old wording pruned (15k) | Dated rulings, copy, criteria, process, history |
| Never-break rules | `product/ABSOLUTES.md`; method: `process/ABSOLUTES.md` here | PM | Four-harms test admits (3k) | Preferences, feature rules |
| Dated feature ruling with `[binds]` | `RULINGS.md` (proposed; today `DECISIONS.md`) | PM rules; planning agent records | Deleted when superseded, or once shipped and stated in the spine or code (40k) | Rationale essays, copy strings, who-said-it |
| What a thing is, and its status | `product/` spine: nouns, verbs, surfaces | planning agent | Fixed the session a mismatch is seen (30k each) | A second description |
| How a thing works | `product/systems/` | planning agent | `trim-product-docs` (10k each) | Whether it ships |
| Acceptance criteria | the scenario file | planning agent | Amended in place; deleted on ship (8k) | Restated rulings |
| Copy rules | `product/foundation/voice-and-tone.md`; strings live in the code | PM approves new copy | Ruled strings become a scenario criterion (10k) | `DECISIONS.md` |
| Idea with no noun, verb or surface | `IMAGINE.md` | planning agent | Moves to the spine once it has a shape; idle 60 days → deleted (15k) | Anything with a shape |
| Not yet decided | `[open-question owner= raised=]` inline, where the answer lands | whoever raised it | Removed when answered | A list of questions |
| Research, options, briefs | `planning/research/`, `product/exploration/`, `planning/briefs/` | any agent | Deleted once ruled and placed (30 days) | Rulings |
| Accepted risk | `accepted-risks/*.json` | code agent | Lint on `review_by` | A ruling restating it |
| How agents work (method) | `process/` here | method | The rule's own "because" holds the failure that earned it (20k each) | Product specifics, history |
| How to work in a repo | that repo's `CLAUDE.md` | repo's agent | Points here for routing (8k) | Routing tables, history |
| Skills | `~/Projects/skills/*/SKILL.md` | `author-skill` | Named verb-object, because three skills were all called review (10k) | Project facts |
| Shift state | `handoff/state.md` (proposed), one file | Dispatch | Overwritten each handoff | Anything dated |
| Legal, entity, securities | the legal repo | counsel track | Its own rules | Product repos, beyond the SETTLED banner |
| Palette, screens, mockups | the design repo | design | — | Product rulings |
| **Junk drawer** | `UNPLACED.md` (proposed): one dated line with `[unplaced raised= owner=]`; loose files go to `~/Projects/agent-temp` | whoever adds it | Drained at each handoff; lint fails after 14 days or 20 lines | Anything with a home |

## Generated: human docs, never edited

| Snapshot | Built by | When |
|---|---|---|
| **Where we are**: the dashboard | `regen-dashboard` | Each handoff; committed |
| **Where we're going**: the dashboard's Now / Next / Later section, from scenario `status` + `rank` and Issue milestones (replaces `ROADMAP.md`) | `scripts/dashboard.py` | With the dashboard |
| **App storyboard**: every screen at 390px, by area and persona; a copy storyboard is the same view narrowed to changed routes | `evals/screens` capture + `scripts/builders/storyboard.ts` (code repo) | On request or nightly CI artifact; never committed |
| `STATUS.md`, READMEs, `constraints/`, `PLATFORM-*.md`, `product/charter.md` | scripts, `regen-*` | Workflow or lint; committed |
| Capabilities, criterion reports, launch report | `regen-*` skills | On request; not committed |
| Build history | git and PR bodies | Never written as files |

## Refinement

- `scripts/budgets.py` (budgets in `scripts/budgets.tsv`; a doc's frontmatter `budget:` overrides). `report` lists docs at 80% or more. `check`, in `lint.sh`, fails when an over-budget doc grows, a dated note passes its age, or `UNPLACED.md` holds an item past 14 days or more than 20 items.
- The weekly `tend-docs` pass rewrites any doc over 80%, or touched 10 times since its last refine, into current understanding plus the why. It opens one PR per doc, and only judgement calls go to the PM.

**Leaving the junk drawer:** every item goes to its row above, an open-question marker, `IMAGINE.md`, an Issue, or is deleted. The line is then removed, never copied or annotated.

**Tests in order:** Is it why? Use a principle. Did the PM rule it on a date? Use a ruling. Does it have a noun, verb or surface? Use the spine. Is it a pass/fail line? Use the scenario. Is it words members read? Use copy. Is it how agents work? Use method. Is it for a human to look at? It is the dashboard or the storyboard, so generate it. Still unsure? Use the junk drawer, and don't stall.
