# The build pipeline: fifteen steps, intake to the PM's look

**As of 2026-10-10** · Source: hand-written · Maintained by: hand (set by tend-docs from the last commit date; the owner confirms on next edit)

*(The PM approved the 15-step shape, 2026-10-06. This section replaces § Paths in `process/PIPELINE.md`; everything else in that file stands. Facts below were read on 2026-10-06 from `socialus-web` main; anything assumed is marked as an assumption.)*

**The speed idea, in one line:** builds are the only thing the PM's machine has to do. Browser work moves to CI (`socialus-web` is public, so standard-runner Actions minutes are free), one capture run per area batch feeds every reviewer, reviewers run as parallel subagents that only find problems, the lane fixes everything in one pass, and the PM sees one area at a time.

**Model tiers.** *Top* (currently Opus): concept, new territory, scenarios with RLS or money, tricky builds, RLS review. *Mid* (currently Sonnet): routine builds, tickets, UX, copy and visibility reviews. *Light* (currently Haiku): intake, labels, a11y triage of machine output, smoke comparison, dashboard.

## (a) Overview

| # | Step | Owner · tier | Gate (pass/fail) | Enforced by | Target | Runs in parallel with |
|---|---|---|---|---|---|---|
| 1 | Intake | Dispatch · light | Issue has `Kind:`, `Scenario:`, `Path:`, one `area:*`, a milestone | issue-lint; dashboard shows `?` for unlabelled | 2 min | everything |
| 2 | Concept | Cowork plan · top | idea has a noun/verb/surface → spine; else stays in `IMAGINE.md` | plan `scripts/lint.sh` | 10 min | 3 |
| 3 | Research | research subagents · light/mid | `Path:` line + 2–3 linked precedents in the Issue | `check-path-line.cjs` via issue-lint | 15 min | all items at once |
| 4 | Decision | well-worn: lane · mid; new territory: the PM | well-worn: Issue body; new territory: dated ruling in its scenario + rationale | plan lint (`[binds]`, constraints fresh) | 5 min / PM queue | other items keep moving |
| 5 | Scenario | Cowork plan · mid (top if RLS/money) | ≤40 lines, value test, `[platform]`, binary acceptance, `status: approved` | plan lint + Cowork review | 20 min | 6 for other items |
| 6 | Tickets | Code lane · mid | `F### · T### · name`, architecture note for schema/RLS/routes, `Visibility:` line | issue-lint | 15 min | 5 for other items |
| 7 | Tests first (red) | Code lane · mid | each criterion has a `[guards F###.n]` test, seen failing | red commit before green; reviewer checks | part of 8 | network work only |
| 8 | Build | Code lane · mid (top if tricky) | Lint/types/build, Unit tests, Migrations applied: green | CI + ruleset | half a shift per batch | max 2 builds on the machine |
| 9 | Journey check | CI + light reader | area journeys finish, no new friction vs main | CI `journeys` step + `## Journey check` | 10 min (CI) | 10, 11 (same bundle) |
| 10 | Visibility review | CI + subagent · mid (top if RLS) | matrix test green + UI dump matches matrix and rulings | CI `visibility` test + `## Visibility review` via review check | 15 min | 9, 11 |
| 11 | UX/UI review | 3 subagents · mid/light | checklist ticked incl. tidy + verdict at 390/1280 | review check | 15 min | 9, 10 |
| 12 | Fix loop | Code lane · mid | only judgement calls remain, ≤2 loops | review check re-runs on edit | 30–45 min | other lanes' builds |
| 13 | Merge/migrate/deploy | Code lane · light | apply → `applied` green → auto-merge → deploy-health green | ruleset + deploy-health.yml | 15 min | other lanes |
| 14 | Live smoke | CI + light reader | changed screens load, as each persona, no error, no leak | `smoke-live.yml` | 10 min | next batch's build |
| 15 | PM review | the PM, via Dispatch | the PM's look, one area at a time | DASHBOARD.md + PM queue | his time, Fri–Mon | everything |

## (b) Step by step

### 1 · Intake
- **Purpose:** every ask becomes one filed, findable thing; nothing is acted on from chat.
- **Owner:** Dispatch, light tier.
- **In → out:** the PM's message → a `socialus-web` Issue (`.github/ISSUE_TEMPLATE/work.md`) with `Kind:`, `Scenario: F###|none`, `Path:`, one `area:<name>`, milestone "Beta 10-30" or "After beta". Reply: "Filed: <area> · <milestone> · Nth in that area".
- **Gate:** issue-lint passes (Kind, Scenario, Path); `dashboard.py` shows an Issue with no area or milestone as `?`.
- **On failure:** `needs-fix` label; Dispatch edits the Issue the same hour.
- **Parallel:** fully; network only.

### 2 · Concept
- **Purpose:** decide whether the idea has a shape yet.
- **Owner:** Cowork plan session, top tier. **Only for new scenarios**; changes, bugs and chores skip it.
- **In → out:** the Issue → a spine entry in `product/` (has a noun, verb or surface) or an `IMAGINE.md` entry (has none; the Issue waits, labelled `after beta` unless the PM said otherwise).
- **Gate:** plan `scripts/lint.sh` green; the one-place rule (an entry moves, never copies).
- **On failure:** fix the doc in the same PR.

### 3 · Research and precedents
- **Purpose:** look first; most decisions are already made by someone else.
- **Owner:** one research subagent per item, light tier for well-known UI patterns, mid for anything touching privacy, money or moderation. All items in a batch fan out at once.
- **In → out:** the Issue → 2–3 precedents with links and a `Path: well-worn | new territory` line in the Issue body.
- **Gate:** `check-path-line.cjs` (issue-lint) passes. "New territory" is required when it touches a ruling, legal or privacy exposure, money or member trust.
- **On failure:** missing line → `needs-fix`. Unsure which path → say so in one line, lean well-worn.

### 4 · Decision
- **Purpose:** record the choice where the people bound by it read it.
- **Owner:** well-worn: the lane, mid tier. New territory: the PM, reached through the PM queue as A/B/C with a recommendation, one at a time.
- **In → out:** well-worn: the Issue body is the record (precedents + choice), no ruling unless it binds more than this Issue. New territory: a dated ruling under `## Rulings` in its scenario with `[binds …]`, ruling wording uses "currently", a rationale doc at `socialus-plan planning/research/<topic>.md`, `constraints/` regenerated.
- **Gate:** plan lint (constraints fresh, `[replaces]` present where it reverses).
- **On failure / waiting:** the item is held; the lane builds the rest of the batch. The PM is mostly unavailable Tuesday to Thursday, so new-territory items raised then land Friday to Monday.

### 5 · Scenario
- **Purpose:** a story and binary acceptance a test can discharge. **Scenarios only.**
- **Owner:** Cowork plan, mid tier; top when it touches RLS, money or moderation (`planning-filter` skill).
- **In → out:** spine entry + decision → `planning/scenario-F###.md`: Story, Acceptance, Not this (≤40 lines), `## Why` with the six value-test answers, `[platform …]`, `gates: launch` where it does. 5 Deadly Sins pass: one line under Why naming any sin found, or "none".
- **Gate:** plan lint (length, value test, platform marker); Cowork review flips `status: approved`. A criterion with a judgement word (*clear*, *easy*) is marked for the PM.
- **Ethos and pitch test:** the scenario names the soul line it serves and, if `PRINCIPLES.md` has `#pitch`, the `cap-n` it moves (or none). Extracting, or deciding where a choice would do, fails it; a soul conflict or a capability moved against the member goes to the PM. And: **does it need us in the loop? If so, why, and when do we step out?** [always]
- **On failure:** over 40 lines → two scenarios. A sin found → cut it before approval and name what left.

### 6 · Tickets
- **Purpose:** buildable slices, each one PR or less.
- **Owner:** Code lane, mid tier (`pipeline-ticket` skill).
- **In → out:** approved scenario → Issues `F### · T### · name`, inheriting area and milestone; ≤20-line architecture note when schema, RLS or routes move; **a new `Visibility:` line**: the matrix rows touched (`pages.select`, `posts.select as signedOut`) or `none`.
- **Gate:** issue-lint.
- **On failure:** `needs-fix`; the lane fixes it.

### 7 · Tests first (red)
- **Purpose:** the test proves it can fail before the code makes it pass ([guard-proves-itself]).
- **Owner:** Code lane, same session as 8.
- **In → out:** failing Vitest/Playwright tests marked `// [guards F###.n]`; new matrix rows in `evals/visibility/matrix.ts`; first commit on the branch is `test:` and red locally.
- **Gate:** the reviewer checks the branch history has a red commit before the green one; after task 11 in (e), CI checks every criterion of the cited scenario is claimed.
- **On failure:** a criterion with no test is a finding in 12. Bugs: a failing regression test is required, always.

### 8 · Build
- **Purpose:** the smallest code that turns red to green.
- **Owner:** one Code lane per area (worktree `~/Projects/worktrees/area-<name>`), mid tier; top for RLS, migrations with data, or a failed second attempt.
- **In → out:** tickets → one PR per area batch (or a stack of at most 2), draft until verified, pushed once when ready. PR body per the template; `How it was verified`.
- **Gate:** `Lint, types, build`, `Unit tests`, `Migrations applied` green; required by the ruleset (task 2).
- **On failure:** fix forward on the branch. Never improvise around a scenario: a divergence stops and asks `socialus-plan` for a scenario change.
- **Parallel:** at most 2 builds or local test runs on the machine; up to 3 lanes, so the third lane is always in model or network work (tickets, reviews, fixes planned).

### 9 · Journey check
- **Purpose:** a builder persona does the real thing end to end, the way a person would.
- **Owner:** CI runs it; a light-tier reader turns the friction log into findings.
- **In → out:** on a ready PR, the CI browser job runs the area's builder journeys (`evals/builders/journey.spec.ts`, plus any area spec) against the throwaway local stack → `friction.md`, storyboard, diffed against main's last friction log.
- **Gate:** no journey halts, and no friction line that main doesn't have. The PR's `## Journey check` lists the journeys run and new friction, or "n/a: no flow changed".
- **On failure:** a halt is a bug fixed in 12; new friction is a finding.
- **Gap:** journeys exist today for create, edit, publish, post, follow, RSVP. A lane whose flow has no journey adds the steps in 7.

### 10 · Visibility review (new gate)
- **Purpose:** who sees what is right for signed out, member, owner, operator and builder, in the UI and in the database.
- **Owner:** CI for the database half; a separate subagent, mid tier, top when the diff touches policies, views, `security definer` functions or `supabase/migrations/`.
- **In → out:**
  - **Database half:** `tests/visibility.test.ts` runs every row of `evals/visibility/matrix.ts` (resource × persona → `none | own | parties | all`, plus withheld fields) against the local stack, signed in as each persona's JWT and as `anon`. It proves itself on a bad fixture: a deliberately open policy it must reject.
  - **UI half:** the subagent reads the capture bundle's per-persona text dumps and screenshots of each changed route, checks them against the matrix and against `constraints/code.md` rulings on surfaces `rls`, `visibility`, `signed-out`, `members` (currently: signed out sees the minimum and no map pins; You is visible to no one else; a transaction is visible only to its parties).
- **Gate:** CI `visibility` test green, and a `## Visibility review` section with `Reviewed by:`, personas checked, matrix rows touched, and a one-line verdict; the review check fails a PR touching `src/app`, `src/actions` or `supabase/` without it.
- **On failure:** a mismatch with a ruling is a rule violation, fixed in 12. A case no ruling covers is privacy, so it's `Path: new territory` and goes to the PM as A/B/C; the rest of the batch keeps moving.

### 11 · UX/UI review
- **Purpose:** the PM sees only judgement calls, never a broken rule.
- **Owner:** three subagents that did not write the code, all reading the same bundle, in parallel:
  - **Layout and tidy** (mid, vision): tidy and contained, one primary action, all states, thumb reach, no horizontal scroll at 390, precedent match, Nielsen pass, the one-line verdict "neat, tidy, organized? Most cluttered thing:" at 390 and 1280.
  - **Accessibility** (light; mid if axe finds anything): the bundle's axe-core results, focus-order screenshots, tap targets ≥44px, labels and alt text, WCAG 2.1 AA.
  - **Copy and voice** (mid): `voice-and-tone.md`; every new or changed member-facing string is listed for the PM's tone look ([public-is-draft]).
- **In → out:** findings only, one line each, into the PR's `## Reviewer's first pass`. **Reviewers don't edit the branch**, so three of them never collide.
- **Gate:** the review check: every checklist line ticked or `n/a` with a reason, including the two tidy lines.
- **On failure:** findings go to 12.

### 12 · Fix loop
- **Purpose:** clear every rule-level finding in one pass.
- **Owner:** the Code lane, mid tier.
- **In → out:** the findings from 9–11 → one fix commit set, one push; CI re-captures only the changed routes; each reviewer re-checks only its failed lines.
- **Gate:** the PR's `Judgement calls for the PM:` holds only items no rule settles; the review check is green.
- **On failure:** after 2 loops, a finding still open is either a judgement call (to the PM) or a non-blocking follow-up `bug ·` Issue in the same area. Never a third loop.

### 13 · Merge, migrate, deploy
- **Purpose:** the database goes first, then the code, and the deploy proves itself.
- **Owner:** the Code lane, light tier; migrations serialized through Dispatch.
- **Order:** apply the batch's one migration with `gh workflow run apply.yml -R donlafranchi/socialus-web --ref <branch> -f confirm=apply` and confirm it in the database (agents do this until the first real member signs up; then the PM does) → `Migrations applied` turns green → `gh pr merge --auto --squash` → Vercel deploys main → deploy-health green → `git worktree remove` for any per-branch worktree, `.next` deleted.
- **Gate:** required checks (ruleset), deploy-health (`/api/health/db`, `/api/health/schema`).
- **On failure:** `applied` red → apply first. deploy-health red → a fix-forward PR labelled `launch-blocking`, which displaces everything. A production rollback asks the PM ([production-asks-don]).

### 14 · Live smoke check (new gate)
- **Purpose:** confirm on socialus.org that what passed locally works live.
- **Owner:** CI (`smoke-live.yml`, after deploy-health succeeds); a light-tier reader compares.
- **In → out:** the changed routes from every PR merged since the last smoke × builder accounts (signed out, stranger, member, owner of the affected kind, operator) at 390 and 1280, **read-only** (opens and taps, never creates) → screenshots and text dumps; the reader compares them with the same screens in the PR's bundle → a comment on the PR, `Live smoke: pass` or a list.
- **Gate:** every screen loads with no error and no console error, and no persona sees text the matrix denies it. A must-fail spec (a route that doesn't exist, asserted to load) runs first.
- **On failure:** a `bug · live: <screen>` Issue in the area, `launch-blocking` if a screen errors or anything leaks; fix forward.

### 15 · PM review
- **Purpose:** the PM judges whether it is right, once per area.
- **Owner:** the PM; Dispatch queues it.
- **In → out:** an area whose batch passed 14 shows "ready for your look" in `DASHBOARD.md`. Dispatch sends one area at a time: the page on socialus.org, three phone steps, the judgement calls and new copy, Friday to Monday. His feedback is filed as new Issues (back to 1), never fixed from chat.
- **Gate:** when `PREVIEWS_MODE` is `labelled`, a `human-review` PR (judgement calls or new copy) gets his look on its preview **before** 13; everything else is unchanged.

## (c) By change type

✓ runs · – skipped · ½ runs in part

| Step | Scenario | Change: UI | Change: copy only | Bug | Migration only | Chore | Docs only | Process (ops repo) |
|---|---|---|---|---|---|---|---|---|
| 1 Intake | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – (no Issue; dated branch) |
| 2 Concept | ✓ | – | – | – | – | – | – | – |
| 3 Research | ✓ | ✓ | – | – | ½ if new shape | – | – | name the failure (the rule's because) |
| 4 Decision | ✓ | ½ new territory only | – | – | ½ arch note | – | – | ½ if the PM rules |
| 5 Scenario | ✓ | – | – | – | – | – | – | – |
| 6 Tickets | ✓ | – (the Issue is the ticket) | – | – | ✓ arch note | – | – | – |
| 7 Tests first | ✓ | ½ if behaviour changes | – | ✓ regression test | ✓ | – | – | ✓ bad fixture for any new lint |
| 8 Build | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ (CI skips) | ✓ |
| 9 Journey | ✓ | ½ if a flow changes | – | ½ if a flow broke | – | – | – | – |
| 10 Visibility | ✓ | ½ UI half | – | ½ if who-sees-what | ✓ DB half (policies/views/functions) | – | – | – |
| 11 UX/UI | ✓ all 3 | ✓ all 3 | ½ copy reviewer | ½ touched surface | – | – | – | – |
| 12 Fix loop | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | – | – |
| 13 Merge/deploy | ✓ | ✓ | ✓ | ✓ | ✓ apply first | ✓ | ✓ | ✓ Cowork merges |
| 14 Live smoke | ✓ | ✓ | ½ text check | ✓ the fixed screen | ½ deploy-health only | ½ if runtime deps/env | – | – |
| 15 PM review | ✓ | ½ if judgement calls | ✓ tone, always | – unless visible | – | – | – | – |

**What each shortcut risks:**
- **Change skips 2, 5, 6:** a change that grows acceptance checks is a scenario in disguise. issue-lint already flags checkboxes on a non-scenario.
- **Copy only skips 9–10:** a string that reveals something (a count, a name) leaks with nobody looking at visibility. The copy reviewer flags any string carrying data, which promotes it to "Change: UI".
- **Bug skips 2–6:** a fix that changes what a scenario promises ships unapproved. The rule stands: that's a change to the scenario first.
- **Migration only skips 11 and 15:** a policy change has visible effects. The DB half of 10 is mandatory for exactly that reason.
- **Chore skips reviews:** a dependency bump that changes rendering (Next, Tailwind) is invisible until live. Chores touching `package.json` runtime dependencies run 14.
- **Docs only skips CI on PRs:** main runs it all after merge; a doc that a lint reads (markers, `[binds]`) can still break main, and the lane fixes forward.

## (d) Speed plan

**What makes it fast:**
1. **Browser work leaves the PM's machine.** Capture, journeys, visibility and smoke run on GitHub runners (free on the public `socialus-web`, assumed up to 20 jobs at once on the Free plan). The machine's 2 build slots do builds and local unit runs only, so the 2-build limit stops being the bottleneck for review.
2. **Capture once, review many.** One CI run per push produces `review-bundle`: changed routes × affected personas × 390/1280, every state the route has a fixture for, axe results, per-persona text dumps. Steps 9, 10 and 11 read it; nobody starts a browser to review.
3. **Reviewers find; one lane fixes.** Five reviewers in parallel (journey reader, visibility, layout, accessibility, copy), no branch edits, so no conflicts and one fix pass.
4. **Batch by area.** One PR (or a stack of 2), one migration, one capture, one fan-out, one apply, one smoke, one PM look per area batch.
5. **New territory never stalls a lane.** It's held in the PM queue; the batch ships without it, and it rides the next batch.
6. **Skip by change type** per (c).

**A typical area batch, estimated** (assumed: 1 well-worn scenario with ~6 criteria, 4 changes, 2 bugs, 1 migration):

| Phase | Steps | Wall clock |
|---|---|---|
| Plan | 2–6, items in parallel | 45–75 min |
| Build | 7–8, one lane, one build slot | 3–4 h |
| CI + capture | 8–10 automated | ~20 min |
| Review fan-out | 9–11 | ~15 min |
| Fix loop | 12, one loop + re-capture | 45–60 min |
| Ship | 13 | ~15 min |
| Live smoke | 14 | ~10 min |
| **Agent total** | | **about 5½–7 h: one batch per lane per shift, with room** |

Across a 12-hour shift with 3 lanes sharing 2 build slots, expect about 3–4 area batches a shift, limited by build slots. The PM's look (15) is outside this clock and batched Friday to Monday.

## Day and night

*(The PM, 2026-10-06.)* Part of the pipeline runs overnight, so the day is spent building and the heavy checks arrive ready.

**Day, per push:** only build, tests, lint, the capture bundle for the changed screens (step 9–11's input), and the quick reviewer pass. Nothing slow.

**Night:** scheduled GitHub Actions on `socialus-web`'s free minutes, plus Code lanes, run the heavy and slow work, with results ready for the 5am handoff:
- full builder journeys (step 9, every area);
- the full visibility matrix across all personas (step 10);
- a full-app screenshot sweep, with the five-reviewer pass over it (step 11);
- the live smoke check of everything merged that day (step 14);
- dependency and advisor checks;
- the dashboard refresh (`DASHBOARD.md` and `dashboard/index.html`).

A failure found overnight is a finding in the next shift's fix loop (step 12), filed as a `bug ·` Issue in its area. The nightly cron for each job is set by whoever builds it: items 4, 6, 8, 9 and 10 in (e).

## (e) What to build, in order

Each is a `chore ·` Issue in `area:ops` unless noted; times are estimates.

1. **Fix the tidy drift (verified today):** the PM's 2026-10-06 tidy items are in `PIPELINE.md` but not in `socialus-web/.github/pull_request_template.md` or `scripts/check-review.cjs`'s `CHECKLIST`, so the tidy rule is unenforced. Add both, plus a bad fixture. *30 min.* Same PR in ops: `PIPELINE.md` says `needs-don` and "preview link" where `socialus-web` now uses `human-review` and socialus.org after merge.
2. **Ruleset on `socialus-web` main:** require Lint/types/build, Unit tests, Migrations applied, review, issue-lint, with admin bypass on. Possible now the repo is public (the 403 in `ci.yml`'s note on #187 predates that). Prove it by watching a bad PR get blocked. *30 min.*
3. **End the CI diet for the public repo:** the browser job runs on every ready PR touching `src/` or `supabase/`, not only labelled ones; drop the "2,000 a month" comments. *30 min.*
4. **Capture bundle:** `scripts/changed-routes.ts` (diff → routes → affected personas) and a Playwright `capture` project that writes screenshots, state fixtures, axe results (`@axe-core/playwright`, free and open source) and text dumps to a `review-bundle` artifact. *Half a day.*
5. **Reviewer skill:** `review-pr-bundle` in `~/Projects/skills`, linked by `link.sh`: downloads the artifact with `gh run download`, fans out the five reviewers with fixed prompts, writes the PR sections. *2–3 h.*
6. **Visibility matrix:** `evals/visibility/matrix.ts`, `tests/visibility.test.ts` running each row as `anon` and each persona's JWT, a bad-fixture policy it must reject, and a `builder` persona in `evals/personas.ts` and its seed. *Half a day to a day.*
7. **PR template and review check:** `## Journey check` and `## Visibility review` sections; `check-review.cjs` requires the visibility section on PRs touching `src/app`, `src/actions` or `supabase/`; fixtures. *1–2 h.*
8. **`smoke-live.yml`:** `workflow_run` after deploy-health, read-only spec with builder accounts, must-fail guard first, comment on the PR or open a `bug · live:` Issue. *Half a day.*
9. **Journeys in PR CI:** run the area's builder journeys against the local stack in the browser job; diff `friction.md` against main's last artifact. *2–3 h.*
10. **Dashboard stages:** `dashboard.py` columns for Scenario approved, Built, Reviewed, Shipped, Smoke, PM looked (steps 5, 8, 11, 13, 14, 15); `?` where no data. *1–2 h.*
11. **Guard coverage check (can wait until after beta):** CI fails a scenario PR whose cited scenario has a criterion no `[guards]` marker claims. *Half a day.*

## (f) Choices for the PM

None currently. Everything above is a well-worn path inside existing rulings: CI on a public repo is free, required checks with admin bypass match the `socialus-plan` ruleset, smoke is read-only, rollback still asks the PM, and visibility cases no ruling covers already route to him as new territory.
