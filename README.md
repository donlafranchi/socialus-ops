# socialus-ops

The operating manual for building SocialUs: who does what, what triggers it, what it produces, and where it is broken. No product code here. `CLAUDE.md` holds the rules; this file is the map.

**Snapshot, 2026-10-10 (regenerated after the plan/build skills were built).** This file is a point-in-time picture, regenerated from the live repos, never hand-maintained (see [Docs are generated](#docs-are-generated)). Every claim carries **[V]** verified (read or run on the snapshot date, source named) or **[A]** assumed (not checked). **[P]** marks a proposal that does not exist yet.

## 1. The chain

```
request / story
  -> plan-feature (council: design + plan)  [V] skill, stops at the brief
  -> PM approves the brief                   [V] brief status: approved
  -> run-feature-pipeline, any feature, new or built:
       assess -> do first phase not done -> reassess, until all 9 phases are done
       (filed, planned, ticketed, built, reviewed, shipped, smoked, reported, PM looked)
  -> regen-feature-report (per feature)      [V] skill; no reports exist yet
  -> regen-capabilities (can / cannot do)    [V] skill; first run not done
  -> regen-dashboard (each phase counted alone) [V] dashboard.py
  -> record-pm-review (pm-reviewed / found-by-pm) [V] skill; labels exist
```

Every link now has a named skill or script, but the chain has not run once end to end. Open seams: `dashboard.py` does not yet read `capabilities.json`, and no build report exists to read.

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

### Feature intake council, run by `plan-feature`
- **Does:** turns "[who] can [outcome] when [situation]" into a Feature Brief: Stage 0 facts (verified/assumed), prerequisites, nine roles in parallel (Person, Maker, Money, Architect, Developer, Tester, Operator, Guardian, Scout) on a cheap model, a chair on the strongest, three build sizes.
- **Input:** one sentence plus PM context. **Output:** `socialus-plan/planning/briefs/YYYY-MM-DD-slug.md`, `status: awaiting-approval`, with binary `criteria`. **Trigger:** the PM asks.
- **Stops** at the brief. It may not create a scenario, Issue or code. The PM sets `status: approved` and `size`. [V] `skills/plan-feature/SKILL.md`; the council prompt is still V0 (`planning/council/feature-intake.md`, status `draft`).
- **Sibling:** the beta-scope council (`2026-10-07-beta-mvp.md`, roles in `process/council-roles.md`) decided what ships, once.

### Any feature, every phase: `run-feature-pipeline` and `regen-feature-report`
- **Input:** one feature: a brief, a scenario `F###`, or its Issues. Works on features already built, not only new ones.
- **Loop:** `regen-feature-report` marks each of 9 phases done / partly / open / failing / unknown with evidence; the pipeline runs the first phase not done (`write-tickets`, `build-ticket`, `diagnose-bug`, `review-pr-bundle`, `respond-to-review`), then reassesses. It stops at the PM's gates and after 2 fix loops on one phase.
- **Output:** `socialus-web/build-log/reports/<feature-id>.md`, regenerated whole each run. [V] skills written; no report exists yet.

### PM review, run by `record-pm-review`
The PM says "<thing> ok" or "<thing> broken: why" in one line. The skill resolves it to an Issue and applies `pm-reviewed` or `found-by-pm` plus a comment, and lists what is waiting for review by area. The dashboard's "PM looked" column reads `pm-reviewed`. [V] skill; both labels exist in `socialus-web`.

### Planning skills (Cowork, in `socialus-plan`)
| Skill | Does | Output |
|---|---|---|
| `scope-scenario` | Orient, scope a scenario, log a decision | Scenario, DECISIONS line |
| `review-draft-scenario` | Architecture/design pre-flight on a draft scenario | Verdict before `approved` |
| `sync-roadmap` | Reconcile shipped work into ROADMAP and scenario status | Updated tracking docs |
| `trim-product-docs` | Cut product docs that restate the code | Smaller docs |
| `write-launch-report` | Public "what you can do today" and private "not yet, and how close", built from `handoff/capabilities.md` | Two docs |
| `plan-feature` | Council to Feature Brief; stops for approval | `planning/briefs/` |
| `regen-capabilities` | What the app can and cannot do, from build reports, Issues, smoke | `handoff/capabilities.md` + `.json` |
| `regen-status`, `regen-dashboard`, `regen-decisions` | Regenerate the same-named doc | The doc |

`socialus-next-moves` was retired: it read claude.ai project docs and published Artifacts, against the rule that deliverables are markdown by PR. [V] `skills/*/SKILL.md`, `link.sh`, relinked 2026-10-10.

### Build skills (Code, in `socialus-web`)
`run-feature-pipeline` and `record-pm-review` (above), `write-tickets` (approved scenario or change -> Issues), `build-ticket` (Issue -> TDD -> PR), `diagnose-bug` (root cause before fixing), `respond-to-review` (act on review feedback), `review-live-design` (live visual QA), `review-pr-bundle` (reviewer's first pass from the CI `review-bundle` artifact; five reviewers by concern, or one for small PRs). Cross-cutting: `verify-before-done`, `author-skill`. [V]

### CI (`socialus-web`, 20 workflows) [V `gh workflow list`]
- **Gate a merge:** `ci`, `ci-docs-only`, `boundaries`, `issue-lint`, `review`, `migrations (check)`.
- **Deploy and health:** `deploy-health`, `apply` (migrations, manual), `smoke-live` (nightly), `signup hook readiness`.
- **Scheduled content/ops:** `builders-daily`, `builders-production`, `builder-content`, `content-origins-purge`, `page-purge`, `unclaimed-load`, `staff-roles`, `problem-reports` (+ heartbeat), `preview-on-label`.

### Living-doc and lint tooling (`socialus-ops/scripts`)
`lint.sh` (runs in CI on push/PR, proves each checker against bad fixtures), `markers.py` (open-question, guards, binds, platform, replaces, evidence, gates), `never.py` (the six absolutes), `risks-due.sh` (accepted-risk register; lint fails when overdue), `state.sh`/`status.sh`/`view.sh` (generated views), `advisor-diff.sh`. Plan repo vendors a copy. [V]

### Generated documents
| Doc | Generator | Trigger | State |
|---|---|---|---|
| `STATUS.md` | `status.sh` via `status.yml`; or `regen-status` | push + daily 13:05 UTC | Regenerated by hand 2026-10-10; workflow cannot start (billing) [V] |
| `README.md` (plan) | `view.sh` | `status.yml` | Same workflow [V] |
| `handoff/capabilities.md` | `regen-capabilities` | Friday, launches | Not yet run [V] |
| `DASHBOARD.md` + `dashboard/status-dashboard.html` | `dashboard.py` / `regen-dashboard` | Handoffs | Counts each phase alone (n/N per area); Smoke 0/88; many cells `?` [V] |
| `handoff/latest.md` | Dispatch `dispatch-handoff` | 5am/5pm | [A] not inspected |
| Launch reports | `write-launch-report` skill | Asked; Friday not yet scheduled | No schedule exists [V: no scheduled tasks] |
| `socialus-ops/README.md` | `regen-readme` | Process changes | This file |
| `CLAUDE.md`, `process/*` | none, by design | by hand | Authored rules, not snapshots |

## 5. Docs are generated

Rule: a top-level doc is a snapshot regenerated from live sources, not maintained. Authored rule files (`CLAUDE.md`, `process/ABSOLUTES.md`, `LESSONS.md`) stay hand-written; they are rules, not state. Everything that describes *state* gets a generator named after it. Generators now: `STATUS`, plan `README`, `DASHBOARD`, `DECISIONS` (prune only), `capabilities`, this README. `ROADMAP` stays under `sync`; `handoff/latest.md` is made by Dispatch's `dispatch-handoff` skill, which is not in the skills library [V].

## 6. Built 2026-10-10 (PM approved the design)

Skills PR: `donlafranchi/skills#4`; dashboard PR: `socialus-plan#59`. Not yet exercised: no brief, report or capabilities file exists, so none of the new skills has run on real work. [V]

**Naming:** verb-object for work, `regen-<doc>` for a document. On 2026-10-10 every skill was renamed to verb-object (`review-draft-scenario`, `review-pr-bundle`, `review-live-design` were three different things all called review). `skills/README.md` is the index. [V]

## 7. Gaps

### Verified
- **Plan-repo Actions cannot start.** `socialus-plan` is private; every run fails with "recent account payments have failed or your spending limit needs to be increased". This kills `status.yml`, plan `lint.yml` and any scheduled job there. `socialus-web` and `socialus-ops` are public and unaffected. [V annotation on run 38079310793]
- **`status.sh` was also broken** by an unescaped quote in the SETTLED banner, so fixing billing alone would not have worked. Fixed 2026-10-10. [V]
- **Nightly live smoke is red** (`socialus-web`, public, so a real failure, not billing). Which spec fails is not determined. [V `gh run list`; cause A]
- **Dashboard data holes.** Smoke 0/88; "Reviewed" counts a PR with no `Reviewed by:` section as passed (`·`), so 88/88 is not evidence. [V `dashboard.py`]
- **The new chain has never run.** No brief, no build report, no `capabilities.md`. [V]
- **Process contradiction:** `PIPELINE.md` says "Cowork merges" method PRs; `CLAUDE.md` says self-merge on green lint. Unresolved; practice has been self-merge. [V]
- **Stale names remain:** a duplicate `~/Projects/ops-pattern` checkout of this remote; `ops-pattern` in `~/.claude/CLAUDE.md`, `DISPATCH.md` and `PIPELINE.md` paths. [V]
- **`dashboard/index.html`** in `DISPATCH.md` vs real `dashboard/status-dashboard.html`. [V]
- **`dispatch-handoff` skill** is not in the library, so it cannot be versioned or regenerated. [V]
- **No scheduled tasks** exist in the desktop scheduler, so nothing runs the Friday report, `regen-capabilities` or `regen-dashboard`. [V]
- **`socialus-design`** has no remote. [V]

### Assumed (not checked)
- Timezone fix vs the 2026-11-01 DST change; AI first read shadow-only; Sentry DSN unset (beta-watch items from the previous README).
- Zip coverage is Sacramento only.
- Child-safety hash check for open beta unanswered.
- Many open Issues are done but never closed.
- The 5am/5pm handoff and 9pm queue actually fire; their scheduler was not inspected.

## 8. What the PM needs to do

1. Decide how plan-repo Actions get minutes: fix billing, or make the repo public (it holds private planning, so probably not), or run `regen-*` locally.
2. Run one real feature through `plan-feature` and `run-feature-pipeline` to prove the chain.
3. Schedule the Friday run of `regen-capabilities`, `regen-dashboard`, `write-launch-report`.

## 9. Commands

```
scripts/lint.sh                       # all checkers + fixtures
scripts/risks-due.sh                  # accepted risks coming due
python3 scripts/markers.py coverage   # guard coverage
./link.sh                             # in the skills repo, after any skill change
```

## 10. Changing the method

Branch `process-YYYY-MM-DD-slug`, commit `docs: what`, add a `LESSONS.md` line naming the dated failure, open a PR, merge when `lint` is green. This repo is public: nothing secret, legal or personal goes in it.
