# socialus-ops

The operating manual for building SocialUs: who does what, what triggers it, what it produces, and where it is broken. No product code here. `CLAUDE.md` holds the rules; this file is the map.

**Snapshot, 2026-10-10.** This file is a point-in-time picture, regenerated from the live repos, never hand-maintained (see [Docs are generated](#docs-are-generated)). Every claim carries **[V]** verified (read or run on the snapshot date, source named) or **[A]** assumed (not checked). **[P]** marks a proposal that does not exist yet.

## 1. The chain

```
request / story
  -> intake council (design + plan)        [V] prompt only, no skill
  -> Feature Brief (3 sizes)
  -> PM approval                            [V] by convention, nothing enforces it
  -> scenario (<=40 lines) -> Issues        [V] plan, review, ticket skills
  -> build (TDD) -> PR                      [V] build skill, 20 CI workflows
  -> reviewer first pass -> merge           [V] review-bundle skill, review.yml
  -> deploy health, live smoke              [V] deploy-health.yml, smoke-live.yml
  -> review report                          [A] PR "Reviewed by:" section; no roll-up
  -> features-and-functionality report      [V] launch-report skill, manual only
  -> dashboard                              [V] dashboard.py, reads Issues/PRs, not reports
  -> PM review (Fri-Mon)
```

The chain exists end to end only by hand. Seams: the council is not a skill (section 4), approval is not a gate, review output is not collected, and the capability report does not feed the dashboard.

## 2. Repos

| Repo | Holds | Works there |
|---|---|---|
| `socialus-ops` | The method: `process/`, lint `scripts/`, `templates/` | Process work |
| `socialus-plan` | Scenarios, `DECISIONS`, `STATUS`, `ROADMAP`, `DASHBOARD`, `handoff/`, `accepted-risks/`, `planning/council/` | Cowork |
| `socialus-web` | Product code, Issues, 20 CI workflows | Code |
| `skills` | Skill library; `link.sh` symlinks into each repo's ignored `.claude/skills/` | Anyone, by PR |
| `socialus-design`, `socialus-legal` | Local folders only; no GitHub remote found | Not part of the chain |

[V] sources: `git remote -v` per folder; `gh repo view donlafranchi/socialus-design` fails. `~/Projects/ops-pattern` is a second checkout of this same remote [V].

## 3. Roles

| Role | Owns | Never |
|---|---|---|
| PM | Rulings, whether a thing is *right* | Reads code |
| Cowork | Planning repo: scenarios, decisions, roadmap | Commits code |
| Code | Web repo: Issues, TDD, PRs, merge on green | Writes scenarios or rulings |
| Dispatch | PM's phone-side intake and shift handoffs; files every ask as an Issue with an `area:` label | Acts on an ask directly |

Shifts 5am-5pm and 5pm-5am, at most 3 area lanes (areas: page-editing, sign-in-you, explore-map, create-posts, sharing-links, builders-seed, moderation, ops), 2 build slots. [V] `process/DISPATCH.md`.

## 4. Systems, one by one

### Decision rule
Look first (2-3 precedents), choose the simplest, label the work `Path: well-worn` (build it) or `Path: new territory` (bring A/B/C to the PM). Input: any design question. Output: a labelled Issue/PR. Trigger: every decision. [V] `CLAUDE.md`.

### Feature intake council (the "committee")
- **Does:** turns "[who] can [outcome] when [situation]" into a Feature Brief: Stage 0 facts (verified/assumed), prerequisites, nine roles in parallel (Person, Maker, Money, Architect, Developer, Tester, Operator, Guardian, Scout) on a cheap model, a chair on the strongest, three build sizes.
- **Input:** one sentence plus PM context (dates, hours, runway, what leaves scope). **Output:** a Feature Brief using `feature-brief-template.md`. **Trigger:** manual.
- **State:** V0, status `draft`, a prompt and a template, two worked runs. No skill, no script, no approval step, no record of runs beyond the worked-runs file. [V] `socialus-plan/planning/council/`.
- **Sibling:** the beta-scope council (`2026-10-07-beta-mvp.md`, roles in `process/council-roles.md`) decides what ships, once. Its MVP list is the first input to `launch-report`.

### Planning skills (Cowork, in `socialus-plan`)
| Skill | Does | Output |
|---|---|---|
| `plan` | Orient, scope a scenario, log a decision | Scenario, DECISIONS line |
| `review` | Architecture/design pre-flight on a draft scenario | Verdict before `approved` |
| `sync` | Reconcile shipped work into ROADMAP and scenario status | Updated tracking docs |
| `trim` | Cut product docs that restate the code | Smaller docs |
| `socialus-next-moves` | Next-phase planning | Phone-readable summary |
| `launch-report` | Regenerate two docs from scratch: public "what you can do today", private "not yet, and how close" | Two docs (Docs tool; fallback `handoff/`) |

[V] `skills/*/SKILL.md`, `link.sh`. `launch-report` is in `link.sh` but not yet symlinked on this machine until `link.sh` is re-run [V: `ls socialus-plan/.claude/skills`].

### Build skills (Code, in `socialus-web`)
`ticket` (approved scenario or change -> Issues), `build` (Issue -> TDD -> PR), `diagnose` (root cause before fixing), `respond` (act on review feedback), `design-review` (live visual QA), `review-bundle` (reviewer's first pass from the CI `review-bundle` artifact; five reviewers by concern, or one for small PRs). Cross-cutting: `verify` (evidence before "done"), `author` (writing skills). [V]

### CI (`socialus-web`, 20 workflows) [V `gh workflow list`]
- **Gate a merge:** `ci`, `ci-docs-only`, `boundaries`, `issue-lint`, `review`, `migrations (check)`.
- **Deploy and health:** `deploy-health`, `apply` (migrations, manual), `smoke-live` (nightly), `signup hook readiness`.
- **Scheduled content/ops:** `builders-daily`, `builders-production`, `builder-content`, `content-origins-purge`, `page-purge`, `unclaimed-load`, `staff-roles`, `problem-reports` (+ heartbeat), `preview-on-label`.

### Living-doc and lint tooling (`socialus-ops/scripts`)
`lint.sh` (runs in CI on push/PR, proves each checker against bad fixtures), `markers.py` (open-question, guards, binds, platform, replaces, evidence, gates), `never.py` (the six absolutes), `risks-due.sh` (accepted-risk register; lint fails when overdue), `state.sh`/`status.sh`/`view.sh` (generated views), `advisor-diff.sh`. Plan repo vendors a copy. [V]

### Generated documents
| Doc | Generator | Trigger | State |
|---|---|---|---|
| `STATUS.md` | `status.sh` via `status.yml` | push + daily 13:05 UTC | **Stale**: header says 2026-10-07; last runs failed [V] |
| `README.md` (plan) | `view.sh` | `status.yml` | Same workflow [V] |
| `DASHBOARD.md` + `dashboard/status-dashboard.html` | `dashboard.py` (reads `socialus-web` Issues and PRs via `gh`) | Manual, at handoffs | Regenerated 2026-10-10; shows "0 of 88 done", many stage cells `?` [V] |
| `handoff/latest.md` | Dispatch `dispatch-handoff` | 5am/5pm | [A] not inspected |
| Launch reports | `launch-report` skill | Asked; Friday not yet scheduled | No schedule exists [V: no scheduled tasks] |
| `socialus-ops/README.md` | **none** | by hand | This file |
| `CLAUDE.md`, `process/*` | **none** | by hand | Authored rules, not snapshots |

## 5. Docs are generated

Rule: a top-level doc is a snapshot regenerated from live sources, not maintained. Authored rule files (`CLAUDE.md`, `process/ABSOLUTES.md`, `LESSONS.md`) stay hand-written; they are rules, not state. Everything that describes *state* gets a generator named after it. Today only `STATUS`, plan `README` and `DASHBOARD` have one.

## 6. Proposed design (nothing below exists; Phase 2 builds it on approval)

### (a) Split the committee into two skills **[P]**
- **`feature-plan`** (Cowork, plan repo). Input: the one-sentence request. Runs Stage 0 and the nine roles, writes `planning/briefs/YYYY-MM-DD-slug.md` with status `awaiting-approval`, then **stops**. It may not create a scenario, an Issue or code. Approval is the PM flipping `status: approved` (and choosing size S/M/L) in the brief; the skill refuses to proceed without it.
- **`feature-build`** (Code, web repo). Input: an `approved` brief. Runs `ticket` -> `build` -> `review-bundle` as one chain, then writes `build-log/reports/<brief-id>.md`: what was built, which acceptance criteria are met (each verified by a named check), what is not, PR links, reviewer findings. It stops at merge-ready; deploy health and smoke append to the same report.
- **Handoff contract:** the brief's frontmatter (`id`, `status`, `size`, `criteria[]`) is the only interface. Neither skill reads the other's internals.
- **Why two:** different repos and roles; the stop for approval becomes structural instead of a habit.

### (b) `features-and-functionality` skill **[P]**
Regenerates "what the app can and can't do" from scratch each run. Inputs: all `build-log/reports/*.md`, open and closed Issues, scenario criteria, latest smoke. Output: one doc with **Can do** (criteria met and smoke-verified), **Partly**, **Can't yet** (wanted, not built), **Gaps in evidence** (closed but no report). Writes `planning/CAPABILITIES.md` and a `capabilities.json` that `dashboard.py` reads, replacing its `?` cells with report-backed stages. `launch-report` becomes a thin view of this file (public bullets and private table) instead of its own research pass. Scheduled Fridays.

### (c) One regenerate-skill per top-level doc **[P]**
A generator named after the doc, each with the same three steps: regenerate from live sources, prune what no longer applies, label verified/assumed. Proposed set: `regen-readme` (this file), `regen-status`, `regen-dashboard` (wraps `dashboard.py`), `regen-roadmap`, `regen-decisions` (prune superseded lines, keep git as the archive), `regen-handoff`. One shared template in `author` so adding a doc means adding a row, not inventing a pattern. Existing scripts stay; the skills call them.

## 7. Gaps

### Verified
- **STATUS.md is 3 days stale.** Header 2026-10-07; the `status` workflow failed on its last 4 runs, each in 4 seconds. The cause is unknown (logs expired). [V `gh run list`]
- **Nightly live smoke is red** for 2026-10-10 (3 runs). The guard spec failing is by design; which real spec failed was not determined. [V `gh run list`; cause A]
- **Dashboard cannot tell progress.** "0 of 88 done" and `?` in most stage cells because stages come from labels, not reports. [V `DASHBOARD.md`]
- **Council has no skill, no approval gate, no run log.** [V `planning/council/`, `skills/`]
- **No review roll-up.** Reviewer output lives in each PR body only. [V `process/PIPELINE.md` § reviewer pass]
- **Process contradiction:** `PIPELINE.md` says "Cowork merges" method PRs; `CLAUDE.md` says self-merge on green lint. [V]
- **Stale names:** `skills/README.md` and `link.sh` say `ops-pattern`; a duplicate `~/Projects/ops-pattern` checkout exists. [V]
- **`dashboard/index.html`** in `DISPATCH.md` vs real `dashboard/status-dashboard.html`. [V]
- **Docs without a generator:** this README, `ROADMAP`, `DECISIONS`, `handoff/latest.md`. [V]
- **No scheduled launch report**; no scheduled tasks exist in the desktop scheduler. [V `list_scheduled_tasks`]
- **Missing repos:** `socialus-design` has no remote. [V]

### Assumed (not checked)
- Timezone fix vs the 2026-11-01 DST change; AI first read shadow-only; Sentry DSN unset (beta-watch items from the previous README).
- Zip coverage is Sacramento only.
- Child-safety hash check for open beta unanswered.
- Many open Issues are done but never closed.
- The 5am/5pm handoff and 9pm queue actually fire; their scheduler was not inspected.

## 8. What the PM needs to do

1. Approve or amend section 6 so Phase 2 can start.
2. Say which repo owns method-PR merges (the contradiction above).

## 9. Commands

```
scripts/lint.sh                       # all checkers + fixtures
scripts/risks-due.sh                  # accepted risks coming due
python3 scripts/markers.py coverage   # guard coverage
./link.sh                             # in the skills repo, after any skill change
```

## 10. Changing the method

Branch `process-YYYY-MM-DD-slug`, commit `docs: what`, add a `LESSONS.md` line naming the dated failure, open a PR, merge when `lint` is green. This repo is public: nothing secret, legal or personal goes in it.
