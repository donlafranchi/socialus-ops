# Pipeline — how work moves

Five kinds of work. Each has its own path; only one goes through design. Everything that isn't listed here is one of these five, or it's a decision (`DECISIONS.md`).

| Kind | What it is | Opened by | Approval | Tracked as |
|---|---|---|---|---|
| **Scenario** | New feature or behavior a person experiences | Cowork, from IMAGINE or Don | Cowork approves the scenario; Don rules only on scope or a contested call | `planning/scenario-*.md` → Issues labeled `scenario` |
| **Change** | UX/UI polish, copy, layout, a small tweak to existing behavior | Anyone | User-facing copy: Don ([public-is-draft]). Otherwise none | Issue labeled `change` |
| **Bug** | Something built doesn't do what its scenario or the code intends | Anyone | None. `launch-blocking` label if it is | Issue labeled `bug` |
| **Process** | A change to this repo's structure, rules, or lint — or to a skill in `~/Projects/skills` | Cowork, Code or Don | Must name the failure with a dated example (`LESSONS.md`) | A PR in the repo that owns the file + a line in `LESSONS.md`. Cowork merges |
| **Chore** | Dependencies, config, deploy, tooling — nothing a member sees | Code | None unless it touches production ([production-asks-don]) | Issue labeled `chore` |

## Paths

- **Scenario:** `IMAGINE.md` → `planning/scenario-*.md` (draft) → Cowork review flips it to approved → Code opens an Issue with the architecture note and builds → all acceptance checks closed → `sync` deletes the scenario.
- **Change / Bug / Chore:** Issue → Code builds → PR closes it. No scenario, no handoff, no review file. Don sees a preview link, not a document.
- **Process:** name the failure, make the change on a branch, open the PR, log it. Cowork merges. Small fixes any time. A reorganisation of the tree is rare, in one session, with a git tag first.

## Rules of the road (guidelines)

- Anyone may open an Issue in `socialus-web`, including Cowork via Dispatch. Only Code commits code there.
- A scenario's **spec** is ≤40 lines across three sections: Story, Acceptance, Not this. If the spec needs more, it's two scenarios.
- **Every scenario from F103 on answers the value test in `## Why`** (Don, 2026-10-05; the six questions and a worked example: the project's `product/foundation/value-test.md`). One line each, led by its label: **Lives somewhere better?**, **Only locals know?**, **Gets people together?**, **Stays fresh on its own?**, **Who keeps it current?**, **Better as more people join?** `scripts/lint.sh` fails a new scenario missing any; F102 and earlier are grandfathered. It answers *should this exist here at all* before anyone writes acceptance criteria for it.
- A fourth section, **Why**, carries rationale — why this shape, what was rejected, how it relates to a neighbouring scenario. **It is not counted toward the 40 lines**, because the cap exists to keep a spec small enough to hold in your head and rationale is not spec. *(Added 2026-09-17: 12 of 37 scenarios already carried exactly this content under a dozen ad-hoc headings, which is what kept `scripts/lint.sh` red. Deleting it to satisfy a linter would have destroyed the reasoning behind ratified decisions; giving it one name makes it checkable.)*
- A scenario says what it needs from a native platform — push, a deep link, the camera or photos, location, background work, a native sign-in, a store review topic — with a `[platform …]` marker, or `[platform none]`. Required from 2026-09-29; `process/LIVING-DOCS.md` § Platform readiness. When `sync` deletes a shipped scenario, its markers move to the spine entry for what shipped.
- If a Change starts needing acceptance checks, it's a Scenario. If a Bug fix changes what a scenario promises, it's a Change to the scenario first.
- Launch-blocking work displaces everything else. When a new launch-blocker lands, `sync` names what moved to Next.
- When something arrives that fits none of the five, don't force it — log it in `LESSONS.md` as a gap and pick the nearest path for now.

## Verified or not

A claim that something works is worth what the check behind it was worth. So say which check ran.

- **Every PR states how it was verified**, in one line: `live DB`, `local Postgres`, `unit tests only`, or `not verified`. Security and migration work must say it; everything else should.
- **Unverified work opens as a draft PR**, with the missing check named at the top of the body and what would clear it. Ready-for-review means the check ran.
- "Tests pass" from a laptop is `unit tests only` until CI says otherwise. There is no test workflow yet — see `LESSONS.md` 19.

## Decision rule — look first, then decide

Word for word, as Don gave it. It applies to every agent and every decision, not only UI, and it is why most work never reaches the PM.

```
DECISION RULE (2026-10-04, Don)
1. Look first: before designing or deciding anything, find what established platforms do for this exact use case. Name 2–3 precedents with links (e.g. Google, Apple HIG, Airbnb, Meetup, Yelp, Stripe, Linear).
2. Choose: pick the most relevant and elegant option for SocialUs, the simplest one that fits our rulings.
3. Well-worn path: if a clear, established pattern exists, decide and build it yourself. Label the Issue/PR "Path: well-worn", list the precedents, and don't wait for the PM.
4. New territory: if there's no well-worn path, the precedents conflict, or it touches a ruling, legal or privacy exposure, money, or member trust, label it "Path: new territory" and bring it to the PM as A/B/C with a recommendation before building.
5. When unsure which it is, say which in one line and lean toward deciding: the PM's time is the scarcest resource.
```

- **How it lands in this method.** The `Path:` line goes on every Issue and PR in the code repo, and a lint there fails one without it ([guard-proves-itself]). The precedents and their links go beside it, in the Issue before building and in the PR body. The reviewer's first pass (below) checks the build against them, and an unexplained departure is a finding.
- **Beside the absolutes, not over them.** "Don't wait for the PM" does not reach new user-facing copy, which stays a draft until he approves it ([public-is-draft]), or anything else an absolute reserves for him ([production-asks-don], [don-decides]).
- "SocialUs" and "our rulings" in the rule mean the project the method is running.

## Who checks what

**Agents own whether a change is correct. Don owns whether it is right.** Correct is testable — it compiles, the tests pass, the migration applies, the rule is enforced. Right is a judgment about the product, and no test has an opinion about it.

Don does not read code, and nothing should ever ask him to. What he looks at is the running app on the preview link.

**He looks only at new territory and tone** *(Don, 2026-10-04, the decision rule above)*:

- **`Path: new territory`** — no well-worn path, conflicting precedents, or it touches a ruling, legal or privacy exposure, money or member trust. It reaches him as A/B/C with a recommendation *before* building, so the PR that follows rarely needs his eyes again
- **tone** — new or changed user-facing copy, which stays a draft until he says otherwise ([public-is-draft])
- **a deviation** from the scenario, or an acceptance criterion with a judgment word — *clear*, *easy*, *minimal fumbling*, the words only he can score

**`Path: well-worn` work that has passed the reviewer's first pass merges without him** — the PR opens "Don doesn't need to look" and lists the precedents.

**He does not look at:** migrations with no visible effect, tests, refactors, docs, infrastructure, dependency bumps.

### The mechanism

Every PR opens with one of exactly two things, before anything else in the body:

1. **"Don doesn't need to look."** — and one line saying why not.
2. **The preview link, three numbered steps, and what he should expect to see.** Label the PR `needs-don`. Only after the reviewer's first pass below, which the body lists.

The steps are written for someone holding a phone who has not read the ticket: *"Open the link, tap Create, choose Business."* Not *"navigate to the composer route."* No file paths, no function names, no ticket numbers, no jargon.

**If a change cannot be described that way, that is a signal it needs his eyes more, not less.** Say so in the PR and label it anyway — an agent that cannot explain a change in three plain steps has found something worth his attention, not an excuse to skip him.

### A reviewer's first pass, before the PM sees it

*(Don, 2026-10-04.)* **Before a UI PR merges or is labelled `needs-don`, a separate reviewer agent that did not write the code runs a first pass** (extended to every UI PR by the decision rule the same day). The PM then reviews judgement calls only, not rule violations: a broken rule that reaches him is a review that did not happen.

- **Who.** A fresh agent with no part in the build: a subagent or another session, never the build agent checking its own work. It reads the diff, the Issue and its recorded precedents, the cited scenario, `constraints/code.md` and the project's copy and design rules, and runs the preview.
- **Screenshots.** Every changed surface, as each persona it affects, at phone width (390) and laptop width (1280). In SocialUs the personas are `socialus-web/evals/personas.ts`, seeded locally.
- **Precedents.** The build is checked against the precedents listed beside the Issue's `Path:` line; an unexplained departure is fixed like a rule violation.
- **Rulings.** Copy and behaviour are checked against the live rulings that bind the change: the scenario's acceptance, `constraints/code.md`, the wording rules, the design language. A mismatch is a rule violation, not a question for the PM.
- **Fixes.** The reviewer fixes what it finds on the same branch, or sends it back to the build agent, and checks again. What it cannot settle by a rule is a judgement call, and only those go to the PM.
- **UX checklist** *(the PM, 2026-10-05)*. The reviewer ticks each line in the PR body, or writes why it doesn't apply:
  - [ ] **WCAG 2.1 AA:** contrast through the colour tokens; visible focus in a logical order; every control labelled and every image has alt text; tap targets at least 44px.
  - [ ] **Every state is present:** empty, loading, error, offline or slow, signed out.
  - [ ] **One primary action** per screen.
  - [ ] **Thumb reach on a phone:** the main action sits in the lower half or a fixed bar.
  - [ ] **No horizontal scroll at 390.**
  - [ ] **Copy follows the project's voice rules** (in SocialUs, `socialus-plan product/foundation/voice-and-tone.md`).
  - [ ] **A quick Nielsen pass:** the system's status is visible; there's a way back or an undo; it's consistent with the rest of the app; errors are prevented before they're explained.
  - [ ] **Images are optimised** (no raw `<img>` lint warnings added, sizes set).
- **In the PR body**, under the first block: `Reviewed by: <agent>`, the personas and widths it looked at, the UX checklist ticked, what it fixed, and the judgement calls left for the PM, one line each. A UI PR without that section has skipped the pass.
- **Never skipped silently.** If the pass can't run (no local stack, no browser), the PR is labelled `review-skipped` with the reason in the body, and the pass runs when it can. In SocialUs a check fails a UI PR that has neither a `Reviewed by:` section with the checklist nor that label, so an unattended merge can't take it.

**Why:** on 2026-10-04 the screenshot matrix captured every route as every persona on every PR, and no role owned looking at the pictures (`socialus-design/research/PATTERNS.md` § E2). Rule violations reached the PM as if they were judgement calls.

### When he merges without looking

Nothing blocks it, and nothing should — his plan has no protection rules, and a gate he can't bypass on his own repo is worse than the problem. Instead the `needs-don` label **stays on after merge**, so `is:merged label:needs-don` is the list of things that shipped without his eyes. It is a list to review, not an alarm.

## Working with the PM

*(the PM, 2026-10-05.)* Guidelines for every agent, in SocialUs and any project that adopts this method.

- **PM queue: one at a time.** When work needs the PM, send exactly one item per message: one decision (A/B/C with a recommendation) or one page to review (a link and three phone steps). Send the next only after he answers; every other item is held in the queue. "Next" is the item that unblocks the most agent work soonest, the nearest deadline breaking ties. Never send a list of everything needed before beta or production. A status list may show counts but asks nothing.
- **Operating constraint.** The PM is mostly unavailable Tuesday to Thursday, so the platform runs unattended. Batch PM items for Friday to Monday, and push back on recurring operator work. Prefer global one-switch operator actions; item-level handling is only for real members' content.
- **PRs open with `gh pr create` from a Code session.** The GitHub connector's create/update PR shows an approval card the PM never sees. Merging through the connector is fine once checks are green.
- **The PM directs; agents edit.** Never ask him to edit a file.
- **Do the mechanical work.** Merges, env vars, issues and reruns get done with the tools at hand. Only judgement goes to the PM.
- **No speculative rulings.** Prune decisions that are not a current concern and don't ask him to rule on them. Ruling wording: "currently", platform first and then members; the only approved "never" is "never extractive".
- **Repo boundaries.** plan = features, ops = method, web = code, legal = private legal, entity and anonymity work. Legal work never goes in plan or ops, and no personal names appear in a public repo (currently `socialus-web`); plan and ops keep them until they go public, when they are scrubbed.
- **Migrations.** The PM applies each one from the apply workflow by branch name, in order, and it is confirmed in the database before the next.

## Build rules — one machine's load

*(Don, 2026-10-04.)* Builds, tests and browsers share one machine. These keep it usable. Guidelines, with one condition on breaking them (the last line).

- **At most 2 changes building or testing at once.**
- **Playwright runs with `--workers=2`.**
- **One dev server port per change**, shut down when the change finishes.
- **Close headless browsers after every run.**
- **Persona reviews run as a serial background queue**, with at most 1 build alongside. The queue shares one dev server and one browser, with a separate browser session per persona, and reports per persona as each finishes.
- **Parallelize network- and model-bound work; serialize browser and build work.** Searches, API reads and subagent thinking can fan out; anything that starts a browser, a dev server or a build waits its turn.
- **If a rule would slow a deadline, flag it to the PM before breaking it**, naming the rule and why. Never break one silently.

### Economy

*(the PM, 2026-10-05.)* The plan's limits (CI minutes, deployments, model use) ran out in one day of heavy building. These keep the spend proportionate.

- **Push once, when a change is ready,** not after every commit: every push runs CI. **Keep stacks at most two PRs deep.**
- **Batch migrations.** Where several pending branches each add a migration, bundle them into fewer applies, one migration PR per milestone where practical, and keep them strictly ordered.
- **Match the model to the work.** A cheaper model for routine work: status, merges, doc sweeps, conflict catch-ups. The top model for design and tricky builds.
- **Restart long agent sessions daily,** with a handoff note (in SocialUs, `socialus-plan handoff/latest.md`), rather than carrying a day's context forward.
- **No new paid tools before beta** unless one replaces PM time.

Machine-specific rules (which container runtime, for instance) live in `~/.claude/CLAUDE.md`, not here.

## Accepted risk

A lint finding ruled acceptable gets recorded once and stops being re-argued. The ruling is the dated line in `DECISIONS.md`; `accepted-risks/` holds one JSON file per finding so an advisor run can be diffed against it — `bash scripts/advisor-diff.sh <export.json>` prints only what isn't already ruled on, plus anything past review.

- One file per finding, named for the finding (`<cache_key>.json`, else `<lint>__<object>.json`). Two agents ruling the same thing collide on the filename instead of writing two rulings.
- An entry needs a `decision` (the `DECISIONS.md` date it points at), a `revisit_if` (the observable condition that reopens it), a `review_by` date, and an `owner` — who argues it again. **`scripts/lint.sh` fails the day `review_by` passes**: an accepted risk nobody revisits is an inert guard.
- `revisit_if` is a fact about the world, not a feeling — "the view's WHERE clause changes", not "if we get worried".
- A past `review_by` is reported on every run. An entry nobody will re-argue is deleted, not renewed silently; renewing it is a new dated line.
- Never derive a `cache_key` from the naming pattern. A key that looks right but never matches stops suppressing silently; `null` falls back to `(lint, object)` and keeps working.

## Open questions

A question nobody has answered yet is marked **inline, where it was raised**, and nowhere else. There is no register — `DECISIONS.md` § Open was one, and on 2026-09-27 F080's detection question stood in it, in F080 and in #221 at once. **The index is generated**: `STATUS.md` § Open questions, by `python3 scripts/markers.py index`.

**The marker — copy this, without the backticks:**

`[open-question owner=don raised=2026-09-27] Where is a picture of a child detected — review before visible, or the uploader's word?`

- **`owner`** is who must answer: `don`, `cowork` or `code`. Not who asked.
- **`raised`** is the date it was first asked, never updated. The index sorts oldest first and shows the age, so a stale question is visible without anyone tending it.
- **The question follows on the same line.** Options, trade-offs and a recommendation go in the lines after it, as before — A/B/C, one line each.
- In a code or migration comment the marker follows the comment token: `-- [open-question owner=code raised=2026-09-27] …`.
- In backticks it is a mention, not a marker — which is how this section quotes it.

**Where it goes — one rule: in the file the answer will change.**

- The answer changes what a member experiences → **the scenario**, in `## Why`. No scenario yet → the spine entry in `product/`.
- The answer changes only how it is built → **the Issue body** in `socialus-web`. Code owns it.
- The answer changes one line of code or one migration and nothing above it → **a comment on that line**.
- **Never** in a PR description, a commit message or an Issue comment: none is scanned, and a merged PR or a commit cannot be edited, so the marker could never be closed. **Never** in `DECISIONS.md`, which holds answers. An Issue that restates a scenario's question points at the scenario instead.

**Who writes one.** Whoever raises a question they cannot answer and will not answer this session — Cowork in `plan` and `review`, Code in `ticket` and `build`. An agent that would otherwise write *"open"*, *"TBD"* or *"needs a ruling"* writes the marker.

**What closes one.**

- **`owner=don`:** the answer is a ruling, so it lands as a dated `DECISIONS.md` line first ([ruling-is-dated-line]). **The same commit** removes the marker and edits the text the answer changes. Whoever records the ruling removes the marker — Cowork, or Code when the ruling reached an Issue.
- **`owner=cowork` / `owner=code`:** the answer is the change itself. The commit that makes it removes the marker and says so in its message. A `DECISIONS.md` line only if it settles something that would otherwise be re-argued.
- **A marker is never deleted without an answer.** A question that became moot is closed by a commit message saying why. A scenario or Issue carrying a marker is not deleted or closed until the marker is answered or moved.

**What checks it.** `scripts/lint.sh` fails on a marker missing an owner, a date or a question, or sitting in `DECISIONS.md` — and first proves the checker rejects every line of its bad fixtures in `scripts/fixtures/markers/` ([guard-proves-itself]). The same checker runs the other markers — `process/LIVING-DOCS.md`. It runs in `.github/workflows/lint.yml`. `socialus-web` runs the same grammar in its own CI for code comments. Issue bodies are not gated; a malformed marker there is listed in the index as malformed.
