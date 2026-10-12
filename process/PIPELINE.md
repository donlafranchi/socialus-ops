# Pipeline — how work moves

**As of 2026-10-10** · Source: hand-written · Maintained by: hand (set by tend-docs from the last commit date; the owner confirms on next edit)

Five kinds of work, because bugs, UX changes and process fixes forced through the scenario pipeline fell outside it (2026-09-10). Each has its own path; only one goes through design. Everything that isn't listed here is one of these five, or it's a decision (`DECISIONS.md`).

| Kind | What it is | Opened by | Approval | Tracked as |
|---|---|---|---|---|
| **Scenario** | New feature or behavior a person experiences | Cowork, from IMAGINE or Don | Cowork approves the scenario; Don rules only on scope or a contested call | `planning/scenario-*.md` → Issues labeled `scenario` |
| **Change** | UX/UI polish, copy, layout, a small tweak to existing behavior | Anyone | User-facing copy: Don ([public-is-draft]). Otherwise none | Issue labeled `change` |
| **Bug** | Something built doesn't do what its scenario or the code intends | Anyone | None. `launch-blocking` label if it is | Issue labeled `bug` |
| **Process** | A change to this repo's structure, rules, or lint — or to a skill in `~/Projects/skills` | Cowork, Code or Don | Names the failure with a dated example, as the rule's "because" | A PR in the repo that owns the file. Cowork merges |
| **Chore** | Dependencies, config, deploy, tooling — nothing a member sees | Code | None unless it touches production ([production-asks-don]) | Issue labeled `chore` |

## Paths

The build pipeline, fifteen steps from intake to the PM's look, and which steps each kind of work runs, is `process/PIPELINE-build.md` (the PM approved the shape, 2026-10-06).

- **Process:** name the failure, make the change on a branch, open the PR. Cowork merges. Small fixes any time. A reorganisation of the tree is rare, in one session, with a git tag first, because six reorganisations May–September each left citations to the old layout.

## Rules of the road (guidelines)

- Anyone may open an Issue in `socialus-web`, including Cowork via Dispatch. Only Code commits code there.
- A scenario's **spec** is ≤40 lines across three sections: Story, Acceptance, Not this. If the spec needs more, it's two scenarios.
- **Every scenario from F103 on answers the value test in `## Why`** (Don, 2026-10-05; the six questions and a worked example: the project's `product/foundation/value-test.md`). One line each, led by its label: **Lives somewhere better?**, **Only locals know?**, **Gets people together?**, **Stays fresh on its own?**, **Who keeps it current?**, **Better as more people join?** `scripts/lint.sh` fails a new scenario missing any; F102 and earlier are grandfathered. It answers *should this exist here at all* before anyone writes acceptance criteria for it, because business hours were built because they were possible, cluttered the Page and were hidden (2026-10-05).
- A fourth section, **Why**, carries rationale (why this shape, what was rejected, the neighbouring scenario). **It is not counted toward the 40 lines**: the cap keeps a spec small enough to hold in your head, and rationale is not spec.
- A scenario says what it needs from a native platform — push, a deep link, the camera or photos, location, background work, a native sign-in, a store review topic — with a `[platform …]` marker, or `[platform none]`. Required from 2026-09-29; `process/LIVING-DOCS.md` § Platform readiness. When `sync` deletes a shipped scenario, its markers move to the spine entry for what shipped.
- If a Change starts needing acceptance checks, it's a Scenario. If a Bug fix changes what a scenario promises, it's a Change to the scenario first.
- Launch-blocking work displaces everything else. When a new launch-blocker lands, `sync-roadmap` names what moved to Next.
- When something arrives that fits none of the five, don't force it: pick the nearest path for now and open a process PR naming the gap.

## Verified or not

A claim that something works is worth what the check behind it was worth. So say which check ran, because on 2026-09-09 a security PR passed only on a laptop, could not apply its migration, and had no way to say so.

- **Every PR states how it was verified**, in one line: `live DB`, `local Postgres`, `unit tests only`, or `not verified`. Security and migration work must say it; everything else should.
- **Unverified work opens as a draft PR**, with the missing check named at the top of the body and what would clear it. Ready-for-review means the check ran.
- "Tests pass" from a laptop is `unit tests only` until CI says otherwise.
- **A claim that something shipped answers "what calls it?"** A function whose only importer is its own test is substrate, not a feature: on 2026-09-20 three planning docs called browse nearly done while nothing called `browse_feed`.

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

Don does not read code, and nothing should ever ask him to. What he looks at is the running page on socialus.org after merge (from the freeze, the labelled preview).

**He looks only at new territory and tone** *(Don, 2026-10-04, the decision rule above)*:

- **`Path: new territory`** — no well-worn path, conflicting precedents, or it touches a ruling, legal or privacy exposure, money or member trust. It reaches him as A/B/C with a recommendation *before* building, so the PR that follows rarely needs his eyes again
- **tone** — new or changed user-facing copy, which stays a draft until he says otherwise ([public-is-draft])
- **a deviation** from the scenario, or an acceptance criterion with a judgment word — *clear*, *easy*, *minimal fumbling*, the words only he can score

**`Path: well-worn` work that has passed the reviewer's first pass merges without him** — the PR opens "Don doesn't need to look" and lists the precedents.

**He does not look at:** migrations with no visible effect, tests, refactors, docs, infrastructure, dependency bumps.

### The mechanism

Every PR opens with one of exactly two things, before anything else in the body:

1. **"Don doesn't need to look."** — and one line saying why not.
2. **The page on socialus.org (after merge; from the freeze, the labelled preview), three numbered steps, and what he should expect to see.** Label the PR `human-review`. Only after the reviewer's first pass below, which the body lists.

The steps are written for someone holding a phone who has not read the ticket: *"Open the link, tap Create, choose Business."* Not *"navigate to the composer route."* No file paths, no function names, no ticket numbers, no jargon.

**A change that cannot be described that way needs his eyes more, not less.** Say so in the PR and label it anyway.

### A reviewer's first pass, before the PM sees it

*(Don, 2026-10-04.)* **Before a UI PR merges or is labelled `human-review`, a separate reviewer agent that did not write the code runs a first pass** (extended to every UI PR by the decision rule the same day). The PM then reviews judgement calls only, not rule violations: a broken rule that reaches him is a review that did not happen.

- **Who.** A fresh agent with no part in the build: a subagent or another session, never the build agent checking its own work, because a gate judged by the party it constrains is waived (the self-declared accessibility review was marked N/A). It reads the diff, the Issue and its recorded precedents, the cited scenario, `constraints/code.md` and the project's copy and design rules, and runs the preview.
- **Screenshots.** Every changed surface, as each persona it affects, at phone width (390) and laptop width (1280). In SocialUs the personas are `socialus-web/evals/personas.ts`, seeded locally.
- **Precedents.** The build is checked against the precedents listed beside the Issue's `Path:` line; an unexplained departure is fixed like a rule violation.
- **Rulings.** Copy and behaviour are checked against the live rulings that bind the change: the scenario's acceptance, `constraints/code.md`, the wording rules, the design language. A mismatch is a rule violation, not a question for the PM.
- **Fixes.** The reviewer fixes what it finds on the same branch, or sends it back to the build agent, and checks again. What it cannot settle by a rule is a judgement call, and only those go to the PM.
- **UX checklist** *(the PM, 2026-10-05)*. The reviewer ticks each line in the PR body, or writes why it doesn't apply:
  - [ ] **WCAG 2.1 AA:** contrast through the colour tokens; visible focus in a logical order; every control labelled and every image has alt text; tap targets at least 44px.
  - [ ] **Every state is present:** empty, loading, error, offline or slow, signed out.
  - [ ] **One primary action** per screen.
  - [ ] **Thumb reach on a phone:** the main action sits in the lower half or a fixed bar.
  - [ ] **No horizontal scroll at 390**, including a control that renders one element per term of a vocabulary (pills, tabs, filters) once the list grows, because the browse pill row fit seven kinds and broke at twelve categories (2026-09-12).
  - [ ] **Copy follows the project's voice rules** (in SocialUs, `socialus-plan product/foundation/voice-and-tone.md`).
  - [ ] **A quick Nielsen pass:** the system's status is visible; there's a way back or an undo; it's consistent with the rest of the app; errors are prevented before they're explained.
  - [ ] **Images are optimised** (no raw `<img>` lint warnings added, sizes set).
  - [ ] **Tidy and contained** *(the PM, 2026-10-06)*: each group of related information sits in its own card or section with a clear header; one edit or action affordance per card, in the card header, never scattered inline; consistent spacing and alignment; long or rarely used content collapsed (accordion); nothing floats loose between sections. Precedents: Apple HIG grouped lists, Material cards, Google Business Profile editor.
  - [ ] **Tidiness verdict** *(the PM, 2026-10-06)*: the reviewer answers in one line, at 390 and 1280, "Is the information on this screen neat, tidy and organized? What's the one thing that looks most cluttered?" and fixes rule-level clutter before the PM sees it.
- **In the PR body**, under the first block: `Reviewed by: <agent>`, the personas and widths it looked at, the UX checklist ticked, what it fixed, and the judgement calls left for the PM, one line each. A UI PR without that section has skipped the pass.
- **Never skipped silently.** If the pass can't run (no local stack, no browser), the PR is labelled `review-skipped` with the reason in the body, and the pass runs when it can, because #380 merged on 2026-10-05 with the pass skipped and nothing recorded it. In SocialUs a check fails a UI PR that has neither a `Reviewed by:` section with the checklist nor that label, so an unattended merge can't take it.

**Why:** on 2026-10-04 CI captured every route as every persona and no role owned looking at the pictures, so rule violations reached the PM as judgement calls.

### When he merges without looking

Nothing blocks it: a gate the PM can't bypass on his own repo is worse than the problem. The `human-review` label **stays on after merge**, so `is:merged label:human-review` lists what shipped without his eyes: a list to review, not an alarm.

## Working with the PM

*(the PM, 2026-10-05.)* Guidelines for every agent, in SocialUs and any project that adopts this method.

- **PM queue: one at a time.** When work needs the PM, send exactly one item per message: one decision (A/B/C with a recommendation) or one page to review (a link and three phone steps). Send the next only after he answers; every other item is held in the queue. "Next" is the item that unblocks the most agent work soonest, the nearest deadline breaking ties. Never send a list of everything needed before beta or production. A status list may show counts but asks nothing.
- **Operating constraint.** The PM is mostly unavailable Tuesday to Thursday, so the platform runs unattended. Batch PM items for Friday to Monday, and push back on recurring operator work. Prefer global one-switch operator actions; item-level handling is only for real members' content.
- **PRs open with `gh pr create` from a Code session.** The GitHub connector's create/update PR shows an approval card the PM never sees. Merging through the connector is fine once checks are green.
- **The PM directs; agents edit.** Never ask him to edit a file.
- **Do the mechanical work.** Merges, env vars, issues and reruns get done with the tools at hand. Only judgement goes to the PM; anything the PM must do at the Mac is a process bug.
- **No speculative rulings.** Prune decisions that are not a current concern and don't ask him to rule on them. Ruling wording: "currently", platform first and then members; the only approved "never" is "never extractive".
- **Repo boundaries.** plan = features, ops = method, web = code, legal = private legal, entity and anonymity work. Legal work never goes in plan or ops, and no personal names appear in a public repo (currently `socialus-web`); plan and ops keep them until they go public, when they are scrubbed.
- **Migrations.** Each is applied from the apply workflow by branch name, in order, and confirmed in the database before the next. Until the first real (non-builder) member signs up, agents apply them (the time-boxed exception under `[production-asks-don]`, 2026-10-06); after that, the PM does.
- **Through Dispatch** (modes, copy-paste, scheduled runs, folders, the weekly tidy): `process/DISPATCH.md`.

## Build rules — one machine's load

*(Don, 2026-10-04.)* Builds, tests and browsers share one machine. These keep it usable. Guidelines, with one condition on breaking them (the last line).

- **At most 2 changes building or testing at once.**
- **Playwright runs with `--workers=2`.**
- **One dev server port per change**, shut down when the change finishes.
- **Close headless browsers after every run.**
- **Persona reviews run as a serial background queue**, with at most 1 build alongside. The queue shares one dev server and one browser, with a separate browser session per persona, and reports per persona as each finishes.
- **Parallelize network- and model-bound work; serialize browser and build work.** Searches, API reads and subagent thinking can fan out; anything that starts a browser, a dev server or a build waits its turn.
- **Worktrees are removed the day their branch merges** *(the PM, 2026-10-05)*: after a merge, the agent that merged it runs `git worktree remove` for that branch's worktree (when its tree is clean and nothing is unpushed) and then `git worktree prune`. Why: 136 stale worktrees used 78GB and filled the build machine's disk on 2026-10-05.
- **Dependencies and build output do not multiply per worktree** *(disk root-cause analysis, 2026-10-05)*: seed a worktree's `node_modules` with an APFS clone of the main checkout's (`cp -cR`), never a fresh `npm ci` per branch, and delete `.next` when a run finishes. At most 10 live worktrees per repo; a read-only or docs session reuses one.
- **No second clone of a repo under `~/Projects`.** A repo has one checkout and its worktrees. A retired checkout is removed once its untracked files (`.env`) are saved.
- **Weekly sweep, by whoever starts the week's first build session:** `docker builder prune --filter until=168h`, `npm cache verify`, and `git worktree prune` in each repo. Nothing is pruned that a running build is using.
- **If a rule would slow a deadline, flag it to the PM before breaking it**, naming the rule. Never break one silently.

### Economy

*(the PM, 2026-10-05.)* The plan's limits (CI minutes, deployments, model use) ran out in one day of heavy building. These keep the spend proportionate.

- **Push once, when a change is ready,** not after every commit: every push runs CI. **Keep stacks at most two PRs deep.**
- **Batch migrations.** Where several pending branches each add a migration, bundle them into fewer applies, one migration PR per milestone where practical, and keep them strictly ordered.
- **Match the model to the work.** A cheaper model for routine work: status, merges, doc sweeps, conflict catch-ups. The top model for design and tricky builds.
- **Restart long agent sessions daily,** with a handoff note, rather than carrying a day's context forward.
- **No new paid tools before beta** unless one replaces PM time.

Machine-specific rules live in `~/.claude/CLAUDE.md`.

## Generated files

*(Path: well-worn, 2026-10-11.)* Precedents: [trunk-based development](https://trunkbaseddevelopment.com/), GitHub Linguist's [`linguist-generated`](https://github.com/github-linguist/linguist/blob/main/docs/overrides.md) (generated files are marked, not reviewed), and the lockfile rule "regenerate, don't merge" ([npm `package-lock.json`](https://docs.npmjs.com/cli/v10/configuring-npm/package-lock-json)).

- **Feature PRs never commit generated files**: `DASHBOARD.md`, `STATUS.md`, `README.md`, `dashboard/status-dashboard.html`. Only the workflow or the 5am/5pm handoff regenerates them, on main, in a commit whose subject starts `docs: regenerate`. `scripts/lint.sh` fails a PR whose diff touches one otherwise.
- **Carve-out:** `constraints/` and `PLATFORM-*.md` stay with the PR that changes their markers; `markers.py` already fails a PR that leaves them stale.
- **A branch that falls behind main merges main in.** It does not rebase.
- **Manual edits to shared files** (e.g. `CLAUDE.md` milestones) go in their own small PR and merge fast.
- **main never waits for feature branches.**
- **A conflict in a generated file is resolved by regenerating it**, never by merging it.

## Accepted risk

A lint finding ruled acceptable gets recorded once and stops being re-argued, because the definer views were re-triaged from scratch on 2026-09-09 against comments that already explained them. The ruling is the dated line in `DECISIONS.md`; `accepted-risks/` holds one JSON file per finding so an advisor run can be diffed against it — `bash scripts/advisor-diff.sh <export.json>` prints only what isn't already ruled on, plus anything past review.

- One file per finding, named for the finding (`<cache_key>.json`, else `<lint>__<object>.json`). Two agents ruling the same thing collide on the filename instead of writing two rulings.
- An entry needs a `decision` (the date of its ruling), a `revisit_if` (the observable condition that reopens it), a `review_by` date, and an `owner` — who argues it again. **`scripts/lint.sh` fails the day `review_by` passes**: an accepted risk nobody revisits is an inert guard.
- `revisit_if` is a fact about the world: "the view's WHERE clause changes", not "if we get worried".
- A past `review_by` is reported on every run. An entry nobody will re-argue is deleted, not renewed silently; renewing it is a new dated line.
- Never derive a `cache_key` from the naming pattern. A key that looks right but never matches stops suppressing silently; `null` falls back to `(lint, object)` and keeps working.

## Open questions

A question nobody has answered yet is marked **inline, where it was raised**, and nowhere else, because on 2026-09-27 one question stood in `DECISIONS.md` § Open, its scenario and an Issue at once. **The index is generated**: `STATUS.md` § Open questions, by `python3 scripts/markers.py index`.

**The marker — copy this, without the backticks:**

`[open-question owner=don raised=2026-09-27] Where is a picture of a child detected — review before visible, or the uploader's word?`

- **`owner`** is who must answer: `don`, `cowork` or `code`. Not who asked.
- **`raised`** is the date it was first asked, never updated; the index sorts oldest first, so a stale question shows without tending.
- **The question follows on the same line;** A/B/C and a recommendation on the lines after it.
- In a code or migration comment the marker follows the comment token: `-- [open-question owner=code raised=2026-09-27] …`.
- In backticks it is a mention, not a marker.

**Where it goes — one rule: in the file the answer will change.**

- The answer changes what a member experiences → **the scenario**, in `## Why`. No scenario yet → the spine entry in `product/`.
- The answer changes only how it is built → **the Issue body** in `socialus-web`. Code owns it.
- The answer changes one line of code or one migration and nothing above it → **a comment on that line**.
- **Never** in a PR description, a commit message or an Issue comment (unscanned, and uneditable once merged, so it could never close), nor in `PRINCIPLES.md`, which holds answers. An Issue that restates a scenario's question points at the scenario.

**Who writes one.** Whoever raises a question they will not answer this session. An agent that would otherwise write *"open"*, *"TBD"* or *"needs a ruling"* writes the marker.

**What closes one.**

- **`owner=don`:** the answer is a ruling, so it lands as a dated ruling first ([ruling-is-dated-line]). **The same commit** removes the marker and edits the text the answer changes. Whoever records the ruling removes the marker — Cowork, or Code when the ruling reached an Issue.
- **`owner=cowork` / `owner=code`:** the answer is the change itself. The commit that makes it removes the marker and says so in its message. A dated ruling only if it settles something that would otherwise be re-argued.
- **A marker is never deleted without an answer.** A question that became moot is closed by a commit message saying why. A scenario or Issue carrying a marker is not deleted or closed until the marker is answered or moved.

**What checks it.** `scripts/lint.sh` fails on a marker missing an owner, a date or a question, or sitting in `PRINCIPLES.md` — and first proves the checker rejects every line of its bad fixtures in `scripts/fixtures/markers/` ([guard-proves-itself]). The same checker runs the other markers — `process/LIVING-DOCS.md`. It runs in `.github/workflows/lint.yml`. `socialus-web` runs the same grammar in its own CI for code comments. Issue bodies are not gated; a malformed marker there is listed in the index as malformed.
