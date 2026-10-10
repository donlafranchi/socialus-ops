# socialus-ops

The operating manual for building SocialUs: who does what, what triggers it, what it produces, and where it is broken. No product code here. `CLAUDE.md` holds the rules; this file is the map.

**Snapshot, 2026-10-10 (regenerated after the plan/build skills were built).** This file is a point-in-time picture, regenerated from the live repos, never hand-maintained (see [Docs are generated](#docs-are-generated)). Every claim carries **[V]** verified (read or run on the snapshot date, source named) or **[A]** assumed (not checked). **[P]** marks a proposal that does not exist yet.

## 1. The chain

Three layers: build (1), observe (2a), improve the pipeline (2b, proposed, section 7).

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

## 7. Meta layer: skills that review and improve the pipeline (**TRIAL**, started 2026-10-10)

The pipeline has three layers. > **TRIAL.** The PM's instruction: *stick with this and keep improving it.* Three pieces are built (guard, `score-ci-health`, `score-doc-drift`); four scores and the reviewer are not. Tracker, health and next step: pinned Issue [#89](https://github.com/donlafranchi/socialus-ops/issues/89). Trial review **2026-10-24**: keep, adjust or drop.

Layer 1 builds the product. Layer 2a describes what is true. Layer 2b judges the pipeline itself and proposes changes to it. Layers 2a and 2b never build product.

```
L1  build      plan-feature, run-feature-pipeline, scope-scenario, write-tickets, build-ticket, review-*, ...
L2a observe    dashboard, STATUS, feature reports, capabilities, launch report, retrospective     [exists]
L2b improve    score-* skills -> review-pipeline -> PRs to skills / process docs -> PM approves    [P]
```

### Today's skills by layer [V: `skills/`, `scripts/`, `process/`]

| Layer | What | Notes |
|---|---|---|
| **2a observe (meta, exists)** | `regen-dashboard` / `dashboard.py` | counts each phase on its own |
| | `regen-status` / `status.sh` | STATUS.md |
| | `regen-feature-report` | criterion-level truth per feature |
| | `regen-capabilities` | what the app can and cannot do |
| | `write-launch-report` | public and private launch docs |
| | `regen-readme`, `regen-decisions`, `sync-roadmap`, `trim-product-docs` | keep docs matching live state |
| | the 2026-10-10 retrospective by area | one-off; no skill, not repeatable |
| **Guards (meta, exists, not skills)** | `scripts/lint.sh`, `markers.py`, `never.py`, `risks-due.sh`, `advisor-diff.sh`, `issue-lint`, `review`, `uat-close` | enforce rules; none reports on whether a rule is working |
| **2b improve (partial)** | `author-skill`, `process/LESSONS.md` | manual: a person notices a failure and writes it down. No scoring, no cadence |
| **Layer 1 (builds product)** | everything else | |

Observation exists. **Nothing scores the pipeline or proposes a change from a score.** That is the whole gap.

### Proposed layer 2b: six scoring skills and one reviewer

Each `score-*` skill is read-only: it computes one number from live sources, with a window, a green / amber / red threshold, and a trend against the previous run. Thresholds are [A] until two weeks of baseline exist.

| Skill | Signal (scored) | Source | Reading today | Can propose changes to |
|---|---|---|---|---|
| `score-rework` (not built) | Share of merged PRs needing a fix loop or a follow-up bug within 14 days; Issues reopened | `gh` PRs, Issues, `bug - live:` titles | 7 live bugs filed in 14 days against 157 merged PRs [V] | `build-ticket`, `write-tickets`, `respond-to-review` |
| `score-pm-overrule` (not built) | How often the PM overrules a plan: briefs rejected or resized, `[replaces]` of an agent-made decision, UAT boxes left unticked, `found-by-pm` per `pm-reviewed` | briefs, `DECISIONS.md`, UAT Issues, labels | Not measurable: 0 `found-by-pm` Issues exist and no brief has been run [V]. `record-pm-review` must write these first | `plan-feature`, `scope-scenario`, the council prompts |
| `score-ci-health` (**trial, built**) | Failed CI runs; red scheduled workflows; smoke red share; repos whose Actions cannot start | `gh run list` | 2026-10-10: CI fail 27.9% (red), smoke 66.7% red (red), plan-repo Actions blocked (red) [V, `scores/`] | `build-ticket`, CI workflows, `diagnose-bug` |
| `score-doc-drift` (**trial, built**) | Docs older than their generator cadence; skills dirs, `link.sh` and README table disagreeing; README claims vs `gh`; approved scenarios whose Issues are all closed | file dates, `gh`, `ls` | 2026-10-10: 11 drift items (red): 9 approved scenarios with every Issue closed, 1 skill missing from the table, workflow count off by one [V, `scores/`] | `regen-*` skills, `sync-roadmap`, workflows |
| `score-gap-leakage` (not built) | Closed Issues whose criteria are unbuilt or unchecked (the F081 and F082 pattern); share of built criteria with no marked check | feature reports | F081 closed with 3 of 9 unbuilt; F082 closed with 1 unmet and 4 unchecked [V] | `write-tickets`, `verify-before-done`, `build-ticket` |
| `score-review-coverage` (not built) | Share of PRs merged with the review skipped; `human-review` PRs merged with no PM look; PM queue age | PR labels and bodies | 39 of 157 merged PRs were `review-skipped`; 65 `human-review` PRs have no `pm-reviewed` [V, 14 days from 2026-09-26] | `review-pr-bundle`, `record-pm-review`, `run-feature-pipeline` |

Considered and left out until there is data: cycle time per phase (needs the report timestamps), cost per feature (needs usage data, [A] available), skill-fit from session transcripts ([A] searchable). Add one only with a source named.

### The reviewer: `review-pipeline` (not built; after three scores have two weeks of readings)

- **Input:** the latest score from each `score-*` skill, the previous run, and `process/LESSONS.md`.
- **Does:** ranks signals by how far they are from green and by trend, picks at most three, and for each reads the skills that signal can change.
- **Output:** one PR per proposed change, to `skills` or `socialus-ops`, each with: the signal and its number, a dated failure example (the `LESSONS.md` format), the exact diff, a predicted effect on the score, and how the next run will show whether it worked. Label `meta-change`.
- **Trigger:** weekly, after `regen-capabilities` and `regen-dashboard`; or when a score turns red.
- **Output on a good week:** a short report saying nothing changed and why. No PR for the sake of a PR.

### Governance: nothing edits itself

1. **PM approval is the only merge path for meta PRs.** Docs PRs self-merge on green lint; a `meta-change` PR does not. The PM approves by applying the label `pm-approved` (from the phone, in the GitHub app).
2. **A guard enforces it** (**trial, built**: `.github/workflows/pm-approved-guard.yml` and `scripts/pm-approved-guard.cjs` in both repos; the script proves itself and lint runs the self-test): a workflow fails any PR that touches a `score-*` or `review-pipeline` path, or carries `meta-change`, unless `pm-approved` was applied by the repo owner after the last commit. **Limit:** agents act with the owner's own token, so a label applied by an agent also reads as the owner. It is a tripwire and an audit trail, not a lock; a separate agent identity is the real fix. [V]
3. **No self-edits.** `review-pipeline` may not propose a change to its own `SKILL.md`, to a `score-*` formula or threshold, or to the guard. Those changes are authored by a person or a separate session and need the same approval.
4. **Scores are read-only on the product.** `score-*` skills write one report file and nothing else; they never open Issues, relabel, or touch code.
5. **One change per PR, reversible.** Each PR names the previous behaviour so reverting is one click, and the next run reports the effect or says it cannot yet tell.
6. **Same method as everything else.** The proposing session classifies the change (`Path: well-worn` or `new territory`), cites precedents, and adds the `LESSONS.md` line.

### Where it sits in the chain

```
L1 chain runs  ->  L2a reports (dashboard, feature reports, capabilities)
                        |
                 score-* x6 read the same sources  ->  score file (dated, with trend)
                        |
                 review-pipeline  ->  up to 3 meta-change PRs  ->  PM applies pm-approved  ->  merge
                        |
                 next week's scores show whether it helped
```

### How the trial reminds the PM

- **Every Friday** the launch report and the dashboard carry a "Meta-layer trial" block (`scripts/trial_health.py --block`): the tracker link, trial health, the next score to build.
- **Trial health** = built scores read within 8 days, meta PRs proposed / approved / rejected, and whether any score moved. `late` is printed in the block.
- **2026-10-24:** that day's report asks keep, adjust or drop.
- Readings live in `scores/` (`history.tsv` plus a dated report per score); the scripts are `scripts/score_*.py`.

### What must exist first [P]
1. `record-pm-review` writes `found-by-pm`, and `plan-feature` writes `rejected` / `resized` onto briefs, so `score-pm-overrule` has data.
2. Smoke tied to merge commits, so `score-ci-health` and the dashboard stop reading 0/88.
3. A `reports/` folder in `socialus-web/build-log` with at least a few weeks of feature reports for `score-gap-leakage` to trend.
4. The `pm-approved` guard.

## 8. Gaps

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
- **No layer 2b.** Nothing scores the pipeline or proposes a change from a score; `found-by-pm` has never been used (0 Issues). [V]

### Assumed (not checked)
- Timezone fix vs the 2026-11-01 DST change; AI first read shadow-only; Sentry DSN unset (beta-watch items from the previous README).
- Zip coverage is Sacramento only.
- Child-safety hash check for open beta unanswered.
- Many open Issues are done but never closed.
- The 5am/5pm handoff and 9pm queue actually fire; their scheduler was not inspected.

## 9. What the PM needs to do

1. Decide how plan-repo Actions get minutes: fix billing, or make the repo public (it holds private planning, so probably not), or run `regen-*` locally.
2. Run one real feature through `plan-feature` and `run-feature-pipeline` to prove the chain.
3. Schedule the Friday run of `regen-capabilities`, `regen-dashboard`, `write-launch-report`.

## 10. Commands

```
scripts/lint.sh                       # all checkers + fixtures
scripts/risks-due.sh                  # accepted risks coming due
python3 scripts/markers.py coverage   # guard coverage
./link.sh                             # in the skills repo, after any skill change
```

## 11. Changing the method

Branch `process-YYYY-MM-DD-slug`, commit `docs: what`, add a `LESSONS.md` line naming the dated failure, open a PR, merge when `lint` is green. This repo is public: nothing secret, legal or personal goes in it.
