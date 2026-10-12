# Where things go

Read this every session, before you write anything down. **Each kind of thing has one home.** If two homes seem to fit, pick the first row that matches. If none fits, the item goes to the junk drawer. Paths mean the project's planning repo unless another repo is named. *Draft: rows marked (proposed) wait on a PM call.*

| Category | Home | Owner | Kept current by | Never goes there |
|---|---|---|---|---|
| Principle: the why behind the mission and the rulings | `DECISIONS.md`, 15–30 entries | PM rules; planning agent words it | Reworded in place when a ruling sharpens it; old wording pruned; "sharpened" date updated | Dated feature rulings, copy, criteria, process, provenance |
| Mission and pledges | `product/charter.md` | generated | `regen-charter` from charter-tagged principles | Hand edits |
| Never-break rules | `product/ABSOLUTES.md`; method: `process/ABSOLUTES.md` here | PM | Admitted only by the four-harms test | Preferences, feature rules |
| Dated feature ruling (with `[binds]`/`[replaces]`) | `RULINGS.md` (proposed; today `DECISIONS.md`) | PM rules; planning agent records | Superseded → deleted; shipped and stated in the spine or code → deleted | Rationale essays, copy strings, who-said-it narrative |
| What a thing is, and its status | `product/` spine: nouns, verbs, surfaces | planning agent | Fixed in the same session a mismatch with code is seen | A second description of the same thing |
| How a thing works (depth) | `product/systems/` | planning agent | Pruned with the spine | Whether it ships |
| Acceptance criteria | the scenario file | planning agent | Amended in place; scenario deleted when shipped | Rulings restating a criterion |
| Member-facing copy | rules: `product/foundation/voice-and-tone.md`; strings: the code | PM approves new copy | Strings change in code; a ruled string is a scenario criterion | `DECISIONS.md` |
| Research, precedents, options | `planning/research/<topic>-<date>.md`; options: `product/exploration/` | any agent | Deleted once ruled and the result has a home | Rulings |
| Not yet decided | `[open-question owner= raised=]` inline, where the answer lands | whoever raised it | Marker removed when answered; index generated in `STATUS.md` | A list of questions |
| Idea with no noun, verb or surface | `IMAGINE.md` | planning agent | Moves to the spine once it has a shape (moved, not copied) | Anything with a shape |
| What's true now / what's next | `STATUS.md` (generated); `ROADMAP.md` | scripts; planning agent | Workflow; sequencing by hand | Rulings, history |
| Work and PM calls on it | Issues in the code repo | code agent | Closed by PR | Ticket files |
| Accepted risk | `accepted-risks/*.json` | code agent | Lint fails on `review_by` | A ruling restating it |
| Legal, entity, securities | the legal repo | counsel track | Its own rules | Product repos, beyond the SETTLED banner |
| Palette, screens, mockups | the design repo | design | — | Product rulings |
| How agents work (method) | `process/` here; failures that earned a change: `process/LESSONS.md` | method | Prune, except LESSONS (append-only) | Anything product-specific |
| Shift state | `handoff/` | Dispatch | Overwritten each handoff | Rulings |
| **Junk drawer:** not yet placed | `UNPLACED.md` (proposed): one dated line with `[unplaced raised= owner=]`; loose files: `~/Projects/agent-temp` | whoever adds it | Drained at each handoff; lint fails after 14 days or 20 lines | Anything that has a home above |

**Leaving the junk drawer:** every item goes to its row above, an open-question marker, `IMAGINE.md`, an Issue, or is deleted. The line is then removed, never copied or annotated.

**Tests in order:** Is it why? Use a principle. Did the PM rule it on a date? Use a ruling. Does it have a noun, verb or surface? Use the spine. Is it a pass/fail line? Use the scenario. Is it words members read? Use copy. Is it how agents work? Use method. Still unsure? Use the junk drawer, and don't stall.
