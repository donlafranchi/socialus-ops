# Criterion roll-up: audit

**Generated 2026-10-10 by `scripts/audit_criterion_rollup.py`, never hand-written.** Every number below was computed from live files, runs and data on that date. **V** verified, **A** assumed, **B** broken or missing.

```
  scenario criteria (plan)     UAT lists        evals / [guards] markers     PR review    smoke
        |                        |                      |                      |           |
        v                        v                      v                      v           v
  feature report  <--- agent run: regen-feature-report (one per feature, build-log/reports/)
        |   criterion rows: Built yes/no/unknown, Checked, Reviewed, Smoked, PM looked
        v
  scripts/criteria.py  (reads reports; counts Built only)
        |-----------------> handoff/capabilities.md
        v
  dashboard.py:  FEATURES section (criteria met / total, red on launch-blocking)   (criterion-derived)
                 AREA cards + header    (Issues in milestone: closed / total)      (Issue-derived)
        |                                          ^ these two do not read each other
        v
  DASHBOARD.md + status-dashboard.html  ->  Friday launch report
```

## 1. Where criteria come from

| Source | Who writes it | Status | Evidence |
|---|---|---|---|
| Scenario `Acceptance` list, numbered | Cowork drafts, the PM approves | **V** | 47 scenario files; 26 approved or building; the reports hold 235 criteria across 29 features. Reports restate the scenario text, so a scenario edited after a report makes the report stale |
| Scenario count vs report count | n/a | **B** | differs: F059 scenario 10 vs report 12 |
| Shipped scenarios (file deleted at sync) | recovered from git history by the report run | **A** | 3 features have no scenario file; their criteria were reconstructed, not read from a live source |
| Issues with no criteria (change, bug, chore) | the PM / Dispatch | **B** | 94 of 123 milestone Issues have no acceptance criteria, so they have no criterion-level result at all |
| UAT checklist `#519` (click-through sheet) | an agent | **B** | the Issue body has 0 checkboxes; the dashboard's Testing section reads it and shows 0 items, and hides the failure (`except: pass`) |

## 2. How a criterion is tested, scored, and where the result lives

| Mechanism | Triggered by | Where the result is stored | Status | Evidence |
|---|---|---|---|---|
| `[guards F###.N]` marker on a test | CI `check-markers.sh`, `markers.py coverage` | STATUS.md "Guard coverage" | **V**, low | 64 criteria carry a marker across 11 features, out of 235 criteria (27%) |
| Feature report "Checked" column | agent run | the report file | **B** | disagrees with STATUS guard coverage on 7 of 11 features, e.g. F080 STATUS 1 vs report 3, F081 STATUS 1 vs report 3, F091 STATUS 3 vs report 4 (different definitions: whole-criterion marks vs marks plus unmarked tests) |
| Feature evals `evals/features/*.spec.ts` | CI Browser job | CI run log only | **V**, partial | 12 spec files; no per-criterion result is written anywhere |
| PR reviewer first pass (`review-pr-bundle`) | UI PR | `Reviewed by:` in the PR body, label `review-skipped` | **V** | per-PR, not per-criterion; the report derives "Reviewed" from it by hand |
| UAT close (`uat-close` workflow, `record-pm-review`) | the PM closes a `uat` Issue | label `pm-reviewed` | **B** | 0 real UAT Issues have ever been closed; the workflow only ever ran on its own self-check |
| Live smoke | nightly + manual | workflow run | **B** | last run 2026-10-10: failure; "Smoked" is 0 for every criterion because runs are not tied to commits |

## 3. What rolls up into what, and the formula

| Level | Formula | Where computed | Status | Evidence |
|---|---|---|---|---|
| Criterion | Built = `yes` only (unknown counts as not built) | `scripts/criteria.py` | **V** | 12 of 235 criteria are `unknown` and count as unmet |
| Feature | met / total | `criteria.py`, dashboard Features section | **V** | 29 features, 141 of 235 met (60%); 9 red |
| Feature report roll-up line | counts typed by the agent | each report and `reports/README.md` | **B** | differs from the criterion rows for 4 features: F045 says 3, rows say 2, F093 says 10, rows say 9, F077 says 2, rows say 1, F081 says 6, rows say 5 |
| Area | **no criterion roll-up exists.** Area cards use Issues: stage = Issues in the area that reached it | `dashboard.py` | **B** | see the table below |
| Milestone / beta % | closed Issues / all Issues in milestone "Beta 11-06" | `handoff`, Dispatch, old dashboard header | **B** | 69 of 123 now (56%); it read 69 of 92 (75%) before the 5pm report run filed 31 gap Issues into the milestone |

Area cards (Issue-derived) against the same areas rolled up from criteria:

| Area | Issues "Built" | Criteria met | Features reporting |
|---|---|---|---|
| page-editing | 21/23 (91%) | 7/13 (54%) | 2 |
| sign-in-you | 5/8 (62%) | 11/27 (41%) | 4 |
| explore-map | 7/17 (41%) | 49/83 (59%) | 10 |
| create-posts | 5/10 (50%) | 30/49 (61%) | 7 |
| sharing-links | 1/2 (50%) | no reports | 0 |
| builders-seed | 4/7 (57%) | no reports | 0 |
| moderation | 5/28 (18%) | 44/63 (70%) | 6 |
| ops | 18/26 (69%) | no reports | 0 |

**Double counting and inflation (V):**
- 35 of 123 milestone Issues are gap Issues auto-filed from criteria. A criterion now appears twice: once as a row in its report, once as an Issue with its own stages. The Issue-derived header and areas count both.
- 6 scenario Issues are closed while their feature still has unmet criteria, so they count as done in the numerator: F082 (#223, 7 of 9), F099 (#460, 12 of 13), F080 (#221, 3 of 5), F101 (#487, 12 of 15), F102 (#488, 9 of 14), F081 (#222, 5 of 9).

## 4. Which skill or script does each step, trigger, last run

| Step | Skill or script | Trigger | Last ran | Status |
|---|---|---|---|---|
| Write criteria | Cowork `scope-scenario`, PM approval | a scenario is written | per scenario | **V** |
| Score criteria per feature | `regen-feature-report` | one-time run 2026-10-10; Friday refresh is scheduled | reports last committed 2026-10-10 | **V** |
| Parse reports | `scripts/criteria.py` | only when `dashboard.py` or `--capabilities` runs | with the dashboard | **V** |
| Capabilities doc | `regen-capabilities` / `criteria.py --capabilities` | Friday task | 2026-10-10 | **V**, first run today |
| Dashboard | `regen-dashboard` / `dashboard.py` | Dispatch handoffs (5am, 5pm), Friday task | 2026-10-10 | **A**: no scheduler runs it; handoff-driven |
| STATUS (guard coverage) | `status.yml` | every push to main, daily 13:05 UTC | 2026-10-11 | **V** |
| Reports roll-up README | an agent | with the report run | 2026-10-10 | **B**: hand-assembled, disagrees with rows |
| UAT close | `uat-close.yml` | `uat` Issue closed | 0 real runs | **B** |

## 5. How it lands on the dashboard

- **Color ramp:** five steps, red to green, on criteria met / total per feature. **V**
- **Red rule:** a feature is red when an unmet criterion links an open `launch-blocking` Issue. **V**; 9 features are red now: F082, F076, F093, F058, F078, F100, F101, F102, F081. An unmet criterion with no linked Issue does not turn a feature red (**A**, no example found, but the rule allows it).
- **Links:** each feature links its full report; each criterion links its Issues. **V**
- **Coverage:** 29 features have criterion-level results, of 29 reportable. Only 29 of the 123 milestone items are scenario Issues (24%); the other 94 have no criteria.
- **Headline numbers in circulation:** "69 of 92" (Issues closed, before the 5pm run), "69 of 123" (now), the dashboard header ("123 beta items"), and the criterion figure (141 of 235). Four numbers, three formulas.

## 6. Biggest problems

1. **The headline beta % counts Issues, and Issues are not criteria.** Filing 31 gap Issues moved it from 75% to 56% with no real change in the product, and 6 closed Issues are counted done with unmet criteria.
2. **Two roll-ups that never meet.** Areas are Issue-derived, features are criterion-derived, and they disagree widely, for example sign-in-you 5/8 built by Issues vs criteria. There is no area or milestone roll-up from criteria.
3. **"Checked" is counted two ways** (STATUS guard coverage vs the reports) and disagrees on 7 of 11 features; the reports' own roll-up lines disagree with their rows on 4.
4. **Reviewed, Smoked and PM looked are not rolled up at criterion level.** Only Built is. Smoke is 0 everywhere, there are no real UAT results, and the Testing section is empty without saying so.
5. **The scoring is a snapshot with one manual trigger.** Reports were produced once; refresh is scheduled for the first time on the next Friday run; the dashboard has no scheduler of its own.

## 7. Recommended fix order (not started; waits for the PM)

1. Make the beta % criterion-based: criteria met / total across reporting features, shown beside the Issue count. Stops the inflation.
2. Add the missing roll-up levels computed by `criteria.py`: area and milestone from criteria; have the dashboard area cards and header read them.
3. One definition of Checked (marks only, per criterion) read by both STATUS and the reports; generate each report roll-up line from its rows.
4. Roll up Reviewed, Smoked and PM looked per criterion; tie smoke to merge commits; make the Testing section fail loudly.
5. Schedule: dashboard and criteria.py on a timer, report refresh on any merged PR that cites a feature.

