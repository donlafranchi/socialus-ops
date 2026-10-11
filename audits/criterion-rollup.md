# Criterion roll-up: audit

**Generated 2026-10-10 by `scripts/audit_criterion_rollup.py`, never hand-written.** Every number below was computed from live files, runs and data on that date. **V** verified, **A** assumed, **B** broken or missing. The five fixes from the first audit have shipped; each row says what is true now.

```
  scenario criteria (plan)     UAT lists        guards markers / evals       PR review    smoke
        |                        |                      |                      |           |
        v                        v                      v                      v           v
  feature report <--- agent run: regen-feature-report (one per feature, build-log/reports/)
        |   rows: Built, Reviewed per criterion; roll-up lines GENERATED from the rows
        v
  scripts/criteria.py: Checked = markers.py (same as STATUS); Smoked = green smoke after last merge;
        |             PM looked = pm-reviewed; stale = merged after the report
        |-----------------> handoff/capabilities.md
        v
  rollup(): criterion -> feature -> area -> milestone  (plain sums of criteria)
        v
  dashboard.py (every 6 h by workflow): header = criteria met / total; area cards; features; Issue count alongside
        v
  DASHBOARD.md + status-dashboard.html  ->  Friday launch report
```

## 1. Where criteria come from

| Source | Who writes it | Status | Evidence |
|---|---|---|---|
| Scenario `Acceptance` list, numbered | Cowork drafts, the PM approves | **V** | 47 scenario files; 26 approved or building; the reports hold 235 criteria across 29 features |
| Scenario count vs report count | n/a | **B** | differs: F059 scenario 10 vs report 12 |
| Shipped scenarios (file deleted at sync) | recovered from git history | **A** | 3 features have no scenario file; criteria reconstructed |
| Issues with no criteria (change, bug, chore) | the PM / Dispatch | **B** | 94 of 123 milestone Issues have no acceptance criteria and no criterion-level result (not addressed by the five fixes) |
| UAT checklist `#519` | an agent | **B** | the Issue has 0 checkboxes; the dashboard now says so loudly (V: notice shown), but the list is still empty |

## 2. How a criterion is tested, scored, and where the result lives

| Mechanism | Triggered by | Where the result is stored | Status | Evidence |
|---|---|---|---|---|
| Guards marker on a test | CI `check-markers.sh`, `markers.py coverage` | STATUS.md, and now `criteria.py` | **V**, low | 64 criteria carry a marker across 11 features, of 235 (27%) |
| Checked (one definition: a marker covers the whole criterion) | `criteria.py coverage()` = `markers.py` | dashboard, report roll-ups | **V** | STATUS vs criteria.py disagree on 0 of 11 features; 40 of 235 criteria checked |
| Reviewed per criterion | the report row (agent, from PR `Reviewed by:`) | report + dashboard | **V**, thin | 16 of 235 criteria reviewed |
| Feature evals `evals/features/*.spec.ts` | CI Browser job | CI log only | **V**, partial | 12 spec files; no per-criterion result is written |
| Smoked per criterion | a green smoke-live run after the feature's last merge | dashboard, report roll-ups | **V**, weak | 81 of 235; last green smoke 2026-10-08, latest run failure (smoke loads pages; it does not test criteria) |
| PM looked | `pm-reviewed` label (`record-pm-review`, closed UAT) | labels | **B** | 1 of 235 criteria; 0 real UAT Issues have ever been closed |

## 3. What rolls up into what, and the formula

| Level | Formula | Where computed | Status | Evidence |
|---|---|---|---|---|
| Criterion | Built = `yes` only (unknown is unmet); Checked, Reviewed, Smoked, PM looked each yes/no | `scripts/criteria.py` | **V** | 12 of 235 criteria are `unknown` and count as unmet |
| Feature | met / total, and the same for each phase | `criteria.py` | **V** | 29 features, 141 of 235 met (60%); 9 red |
| Report roll-up lines and README table | generated from the rows by `--rewrite-reports` | `criteria.py` | **V** | 29 of 29 reports carry a generated line; 0 disagree with their rows, 0 README rows disagree |
| Area | sum of criteria in the area (`rollup()`); red if any feature is red | `criteria.py`, `dashboard.py` | **V** | area cards lead with criteria; Issue stages are shown only for areas with no reports |
| Milestone / beta % | **criteria met / total**; Issues closed shown alongside | `dashboard.py` header | **V** | header: "# Beta 11-06 · 20 days to freeze · criteria met 141/235 (60%), checked 40, reviewed 16, smoked 81, PM looked 1 across 29 features, 9 red, 0 reports stale · Issues closed ..." |

Areas, Issue-derived against criterion-derived (the old and the new view side by side):

| Area | Issues "Built" | Criteria met | Features reporting |
|---|---|---|---|

**Double counting (still true, no longer the headline):**
- 35 of 123 milestone Issues are gap Issues auto-filed from criteria, so a criterion appears as a report row and as an Issue. The Issue count (69 of 123, was 69 of 92) is now shown alongside the criterion figure, not as the beta %.
- 6 scenario Issues are closed while their feature has unmet criteria, so the Issue-derived areas still count them done: F082 (#223, 7 of 9), F099 (#460, 12 of 13), F080 (#221, 3 of 5), F101 (#487, 12 of 15), F102 (#488, 9 of 14), F081 (#222, 5 of 9).

## 4. Which skill or script does each step, trigger, last run

| Step | Skill or script | Trigger | Last ran | Status |
|---|---|---|---|---|
| Write criteria | Cowork `scope-scenario`, PM approval | a scenario is written | per scenario | **V** |
| Score criteria per feature | `regen-feature-report` | one-time run 2026-10-10; Friday refresh scheduled; 0 reports are stale now | reports last committed 2026-10-10 | **V** |
| Parse and roll up | `scripts/criteria.py` | every dashboard run | with the dashboard | **V** |
| Capabilities doc | `criteria.py --capabilities`, `regen-capabilities` | Friday task | 2026-10-10 | **V** |
| Dashboard | `dashboard.yml` workflow every 6 hours (also handoffs, Friday) | schedule, dispatch | 2026-10-11; workflow success (2026-10-11T03:37) | **V** |
| STATUS (guard coverage) | `status.yml` | every push to main, daily | 2026-10-11 | **V** |
| Reports roll-up README | generated by `criteria.py --rewrite-reports` | the report run and the Friday refresh | 2026-10-10 | **V** |
| UAT close | `uat-close.yml` | `uat` Issue closed | 0 real runs | **B** |

## 5. How it lands on the dashboard

- **Header:** "# Beta 11-06 · 20 days to freeze · criteria met 141/235 (60%), checked 40, reviewed 16, smoked 81, PM looked 1 across 29 features, 9 red, 0 reports stale · Issues closed 69/123 (alongside, not the hea". **V**
- **Color ramp:** five steps, red to green, on criteria met / total, per feature and per area. **V**
- **Red rule:** a feature or area is red when an unmet criterion links an open `launch-blocking` Issue. **V**; 9 features red: F082, F076, F093, F058, F078, F100, F101, F102, F081.
- **Stale flag:** a feature whose last merged PR is newer than its report is flagged. **V**; 0 stale now.
- **Per criterion:** built, checked (T), reviewed (R), smoked (S), PM looked (P) on each criterion row, with links to its Issues and the full report. **V**
- **Coverage:** 29 features have criterion-level results, of 29 reportable. Only 29 of the 123 milestone items are scenario Issues (24%).
- **Headline numbers in circulation:** criteria met 141 of 235 (the beta %), Issues closed 69 of 123 (alongside), and `handoff/latest.md`'s own count (Dispatch-written, **A**).

## 6. What the five fixes changed, and what is still open

| Fix | Shipped | Evidence |
|---|---|---|
| 1. Criterion-based beta %, Issue count alongside | plan #71 | **V** header leads with criteria |
| 2. Area and milestone roll-ups from criteria | plan #71 | **V** `rollup()` feeds area cards and header |
| 3. One definition of Checked; generated roll-up lines | plan #72, web #661 | **V** STATUS vs criteria.py: 0 disagree; report lines vs rows: 0 disagree |
| 4. Reviewed, Smoked, PM looked per criterion; loud Testing; honest Reviewed | plan #73, web #662 | **V** reviewed 16, smoked 81, PM looked 1 of 235; Testing notice shown |
| 5. Timer and stale-report flag | plan #74, #75, #76 | **V** dashboard workflow last run success |

**Still open:**
1. **No PM review results.** 1 of 235 criteria are PM-looked; 0 real UAT Issues have been closed; `#519` has 0 checkboxes.
2. **Smoke is red** (last green 2026-10-08), so "Smoked" is a stale claim and no criterion is evidenced beyond page loads.
3. **94 of 123 milestone items have no criteria** (changes, bugs, chores).
4. **Checked is 17%** (40 of 235); most criteria have no marked test.
5. **Report text can still be stale or wrong**: the rows are agent-written once and refreshed on the Friday run; a row can be wrong until then (the stale flag only catches merges, not edits to a scenario).
