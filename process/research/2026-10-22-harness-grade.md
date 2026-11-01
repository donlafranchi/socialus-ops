# Grading the SocialUs factory: idea to production and back

**As of 2026-10-22** · Source: socialus-ops, socialus-web and socialus-plan at main on 2026-10-22, the live GitHub PRs, Issues, check runs and dashboard, and the external sources in § 6 · Maintained by: hand (research note; delete or promote within 30 days)

*Research note for the PM. Not a ruling. Facts marked "observed" were read from the repos or GitHub today; anything else is a judgement and says so.*

## 0. The verdict in one screen

- **Grade: B minus (3.1 of 5).** A strong, fast engine wrapped in a management layer built for people.
- **The engine is good.** Binary scenarios under 40 lines, tests that must be seen failing, guards that prove themselves on bad fixtures, migrations checked three ways, RLS checked per persona, browser smoke on every PR, deploy health and live smoke after merge, 100 PRs merged in a fortnight with about 14 minutes from PR open to merge on the median PR.
- **The human layer is the bottleneck, and the system is making it worse.** 0 of 285 criteria have been looked at by the PM. 0 of 22 phone walk-throughs ticked. 29 to-dos and 12 "waiting on you" items on the dashboard. 10 copy PRs parked as drafts since 10-11, and 149 PRs merged under the human-review label with no recorded look. The handoff file is 11 days stale. The pipeline manufactures PM work faster than one person with a day job can clear it, so the gates that depend on him never close and the miss rate the experiments were designed to measure (found-by-pm) has 0 data points.
- **The ceremony is sized for a team.** 33 workflows, 24 check runs on one PR head, a 15-step pipeline doc, a 796-word PR template with five sections, shifts, lanes, handoffs, a weekly refine pass, a trial scoring layer with its own tuning notes, and 25,000 words of method. About a third of it checks text rather than code, and the repo's own tuning notes call most of the red scores false.
- **The fix is subtraction, not a new tool.** Keep every check that runs code. Delete every check that parses prose. Cut the method docs to what an agent must read in one session. Replace shifts and handoffs with triggers. Turn the PM's 29 to-dos into one question at a time, and make "look live" the only thing he does.

## 1. Grade card

Score 0 to 5. "Observed" is from the repos or GitHub today.

| # | Dimension | Score | Evidence (observed) | What moves it to 5 |
|---|---|---|---|---|
| 1 | **Spec quality**: binary, small, filtered | 4 | Scenario spec capped at 40 lines, five fixed sections, value test on every scenario from F103, `[platform]` marker, lint-enforced. 60 scenarios, 61,600 words. | Delete shipped scenarios on time (the rule exists; 60 files is a lot of unshipped intent) |
| 2 | **Verification by code, not prose** | 3 | Strong: lint/types/build, unit (7.5 min), browser (5.5 min), migrations from scratch, applied to production, no undocumented migrations, visibility matrix, action-layer conformance, ontology links, deploy-health, smoke-live. Weak: `review` check reads PR body text for `Reviewed by:` and ten checklist words; `## Visibility review` and `## Journey check` are prose sections; PR #990's reviewer is "claims lane agent", the builder reviewing itself; 13 unit tests parse workflow YAML; `reports.yml` diffs JSON against markdown; 45 browser evals are quarantined (run, result discarded); the pgTAP tests never run. | A reviewer that is a separate agent run (CI job or a second session) posting a review the check verifies by author, not by the builder's text |
| 3 | **Human touchpoints only where judgement lives** | 2 | PM looked 0 of 285; 0 of 22 walk-throughs; 29 to-dos (8 are P1); 12 waiting; 10 draft copy PRs since 10-11; meta scripts need `pm-approved`; a new session needs a desktop approval; the build-log question waits on a ruling already made on 10-12. | A PM queue with one item, a 7-day age alarm, and nothing else routed to him |
| 4 | **Loop closure**: production teaches the next cycle | 2 | deploy-health and smoke-live exist and file Issues. `found-by-pm` label: 0 Issues. Review-setups experiment awaits "the PM's live review" that never came; scheduling experiment log table is empty. Miss rate unmeasured. | The PM's live look as the only review, each finding filed as `found-by-pm`, miss rate on the dashboard |
| 5 | **Context economy**: what an agent must read to act | 2 | ops process docs 24,700 words; PIPELINE.md 8,300 (40 rulings appended); PIPELINE-build 4,000; web CLAUDE.md 2,100; plan CLAUDE.md 2,200; PR template 800; decision rule copied in 3 files; INFRASTRUCTURE.md 5,200. | Under 5,000 words per role per session, one copy of every rule |
| 6 | **Throughput and latency** | 5 | 100 PRs merged in 14 days; CI about 8 minutes; PR open to merge about 14 minutes median (8 sampled: 7, 8, 8, 11, 17, 29 min, 4.6 h, 1 day). | Hold it |
| 7 | **Observability for the agent and the PM** | 3 | Generated STATUS, DASHBOARD, constraints, criterion roll-up, scores. But: doc-drift score 97 items "mostly false"; dashboard headline says 2 red while rollup says 8; handoff/state.md stale since 10-11; beta date is 10-30 in four places and 11-06 in two; freeze is 10-23 and 10-30. | One source for dates, one number per concern, delete scores that are mostly false |
| 8 | **Guards prove themselves** | 5 | Every lint and checker runs on bad fixtures first; `[guard-proves-itself]` is an absolute with three dated failures. Rare and excellent. | Hold it |
| 9 | **Doc rot resistance** | 3 | Prune-don't-annotate, newer-decision-wins, budgets, generated views, 30-day research notes. But 83% of 416 docs hand-written, 63 undated, build-log/ exists against the 10-12 ruling, pipeline-ticket skill describes file tickets that don't exist here. | Delete to the budget rather than refine to it |
| 10 | **Ceremony ratio**: process per unit of shipped change | 2 | 33 workflows (2,831 lines, 614 of them comments; the DB-URL step copied 17 times); 24 check runs per PR head; `ci-docs-only.yml` exists only to echo the four required check names; `migrations.yml` repeats two jobs CI already runs; 15 steps; 5 PR sections; shifts, lanes, handoffs, phone/computer modes, weekly tidy, Friday refine, trial scores, tuning notes, doc garden, council, pm-approved guard. ~17,600 lines of scripts and workflows across three repos for a 935-file app. | Half the workflows, one PR section, no shifts |

**3.1 of 5.** Dimensions 6 and 8 are the two things most factories never get right and this one has. Dimensions 3, 5 and 10 are the same problem seen three ways: the method was written as if a team would run it.

## 2. Backward walk: production to idea

Each gate, who holds it, what kind of check it is, and the call. "Code" runs the product or the schema. "Structure" checks shape (names, files, markers). "Prose" reads text a human or agent wrote about the work.

| Stage (newest first) | Gate | Held by | Kind | Call |
|---|---|---|---|---|
| Production (Vercel, main only) | deploy-health: /api/health/db and /schema; main-build-alarm opens one Issue on a failed build | CI | Code | Keep |
| After merge | smoke-live: changed routes as each builder persona, read-only, files `bug · live:` | CI | Code | Keep |
| Merge | auto-merge squash on green; `human-review` label stays on after merge | Agent | — | Keep. The label is the only trace the PM never looked |
| Required checks (four, per `ci-docs-only.yml`) | Lint/types/build (tsc, eslint, next build, 4–6 min) · Unit tests (553 Vitest files against a Supabase built from all 138 migrations, 10–18 min) · Browser (Playwright on a production build with seeded personas, RLS visibility matrix, must-fail guard, 12–20 min) · Migrations applied to production (drift, 1 min) | CI | Code | Keep all four. Also keep, required or not: migrations from scratch, no undocumented migrations, action-layer and ontology checks (inside Unit tests), markers lint |
| Same PR head | `review` first-pass: body has `Reviewed by:` and ten checklist words, or a `review-skipped` reason | CI reads prose | Prose | **Cut.** It verifies that words exist. PR #990 passed it with the builder as reviewer |
| Same PR head | `## Visibility review`, `## Journey check` sections | Agent writes prose | Prose | **Cut the sections.** Keep `tests/visibility.test.ts` and the journeys spec, which are the real gate |
| Same PR head | build-preview (skipped), apply workflow (manual dispatch), issue-lint echo | CI | — | Fold: 24 check runs per head is noise; one CI workflow with named jobs |
| PR body | Template: "Don doesn't need to look" or "Review" block · Path + precedents · What this changes · Migration · Reviewer's first pass · Journey · Visibility · How verified · Closes | Agent | Prose | **Shrink to three lines**: look/no-look, Path, how verified. The rest is the diff |
| Build | Tests red before green (`test:` commit first), `[guards F###.n]` markers | Agent self-discipline; "reviewer checks the branch history" | Structure, unenforced | Make it a check: CI fails a scenario PR with no `[guards]` marker for a touched criterion (PIPELINE-build (e) item 11, deferred) |
| Ticket | Issue with Kind, Scenario, Level, Path, area label, milestone; issue-lint | CI | Structure | Keep Kind/Scenario/Path. Drop Level and the `needs-fix` label dance (8 open, nobody watches it) |
| Tickets from scenario | `pipeline-ticket` skill | Agent | — | **Fix or delete**: it reads `planning/scenarios/` and writes `development/tickets/`, neither of which this project has |
| Scenario | 40 lines, five sections, value test, platform marker, `status: approved` by Cowork | Lint + agent | Structure | Keep. Best part of the method |
| Decision | Well-worn: agent decides, lists precedents. New territory: A/B/C to the PM | Agent / PM | — | Keep. This is the right human gate |
| Precedents | 2 to 3 links, `Path:` line, `check-path-line.cjs` | Agent + CI | Structure | Keep |
| Concept | Spine entry or IMAGINE; one-place rule | Agent | Structure | Keep, but IMAGINE is 4,200 words with a 60-day idle rule nobody enforces |
| Intake | Dispatch files every ask as an Issue with area and milestone; replies "Filed: …" | Agent | — | Keep the filing. Drop areas, lanes, shifts (§ 4) |
| Idea | The PM, by phone | PM | — | Keep |

**What the walk shows.** Everything from the required checks down to production is code checking code and it works. Everything between "build" and "merge" that was added on 2026-10-04 to 10-06 (reviewer's first pass, visibility section, journey section, review check, 15-step doc) is prose checking prose, and the one PR sampled passed it with a self-review. Everything above "scenario" is sound.

## 3. Forward walk, as an agent would run it

The loop with no team metaphors. Each line is one trigger, one actor, one check.

1. **Ask arrives** (phone, Issue, or a live-look finding). Agent files one Issue: Kind, Scenario, Path. Nothing else.
2. **Agent classifies.** Well-worn: go. New territory (money, legal, privacy, trust, a ruling): one A/B/C to the PM queue, build everything else meanwhile.
3. **Agent writes or amends the scenario** (≤40 lines, binary criteria, value test). Cowork approves. The PM sees it only if it is new territory.
4. **Agent writes the failing test, then the code.** One PR. Body: look or no-look, Path, how verified.
5. **CI runs code against code**: build, unit, browser, migrations three ways, visibility matrix, markers. A second agent run (not the builder) reviews the diff and screenshots and posts a review. Nothing reads the PR body.
6. **Green merges itself.** Deploy health, then live smoke. A failure files an Issue, back to step 1.
7. **Dashboard regenerates** on merge. One line per feature: built, checked, live, looked.
8. **The PM looks live**, one screen, one question, when he has five minutes. What he finds is an Issue labelled `found-by-pm`. That label is the whole quality metric.

**Where the human adds value** (keep, and make each one cheap):

- **Taste on the live app.** The one thing no check has. Today it happens zero times because it is queued behind 29 to-dos. Make it the only queue.
- **New territory.** Money, legal, privacy, member trust, scope. A/B/C with a recommendation. Already right.
- **What to cut.** The value test and the 5 Deadly Sins are his lens; agents apply it, he overrules.
- **Domain facts.** Sacramento, local businesses, what a neighbour would actually do.
- **Being the first real member.** His own signup, Page and posts are worth more than the whole screenshot matrix.

**Where the human is in the way** (each inherited from a role a team would staff):

| Inherited role | How it shows up here | Cost today (observed) | Replace with |
|---|---|---|---|
| Copy editor | New copy is a draft until he approves | 10 draft copy PRs since 10-11; copy is the most common `human-review` reason | Ship under the voice rules, he edits live; or a copy lint |
| Release manager | Migrations "go to Don, in order" | Already waived until the first real member; the waiver is the right default | Keep the waiver permanently; alarm on drift instead |
| Change advisory board | `pm-approved` on score and skill changes | A manual check because Actions can't run in `skills` (billing) | Delete the guard; scores are not production |
| Checklist ticker | "PM looked" per criterion, 22 journeys on #519 | 0 ticked after 2 weeks | One `found-by-pm` label on Issues; "looked" is inferred from his Issues |
| Shift manager | 5am/5pm handoffs, lanes per area, phone/computer modes, approvals per session | handoff/state.md stale since 10-11; the dispatch skill carries the wrong beta date | PR events and scheduled tasks wake agents; no shifts, no handoff file |
| Bookkeeper | Rulings as dated lines with `[binds]`, `[replaces]`, `[always]`/`[for now]`, `[evidence]`, `[platform]`, `[unplaced]` | A grammar of eight marker kinds and 3,700 lines of checker; a ruling he already made (no build-log, 10-12) is back as a question | Keep the open-question, guards and binds markers. Retire the rest when their failure stops happening (LIVING-DOCS already says to) |
| Dashboard reader | 29 to-dos, 12 waiting, two tripwire questions, "answer the 18 items" | He has not; the queue is the blocker | One item, age-alarmed; the rest held by the agent and decided by default after 7 days where the decision rule allows |
| Build host | His Mac runs builds, browsers, worktrees, Docker; 136 stale worktrees once used 78 GB | Rules about ports, workers, APFS clones, weekly sweeps | Cloud sessions and CI do the building; the Mac is a phone with a keyboard |

## 4. Bloat: what to delete, fold or freeze

Ordered by words saved per minute of work. Each cut names the rule that already allows it.

| Cut | Size | Why it is safe | Rule that allows it |
|---|---|---|---|
| **PIPELINE.md § Rulings** (40 dated lines) out of ops, into the plan repo where rulings live | ~3,000 words | Ops holds the method; rulings are product history. The 10-12 ruling says rulings sit where they govern | WHERE-THINGS-GO row 3 |
| **PIPELINE-build.md** down to one table of gates that exist in CI | 4,000 → ~600 words | Estimate tables, day/night plan, speed plan and the (e) build list are a plan, not a method; several items are built, several are not, the doc can't tell you which | "A standard exists when lint or CI checks it" |
| **PR template** to three lines | 796 → ~120 words | Sections that a regex checks for words are the "doc checks doc" failure the method itself names (2026-09-03) | Prefer a check against code |
| **`review` workflow + check-review.cjs** | 1 workflow, 1 script | Verifies prose exists; the sampled PR self-reviewed through it | guard-proves-itself: a guard that cannot reject a self-review is inert |
| **build-log/2026-W42/** (32 per-ticket files; `build-log/reports/` is a live generated report and stays) | 32 files | Ruled out on 2026-10-12; one test even cites a build-log file that doesn't exist. Delete, don't ask | newer-decision-wins |
| **Trial meta layer**: scores/, tuning/, doc garden, pm-approved-guard, trial_health, score_* | ~1,500 lines + 3 workflows | Its own 10-16 tuning note: doc-drift "mostly false", 97 items of which 63 are build-log double counts. Freeze until after beta; keep two numbers | 10-11 ruling already trimmed it to two PM numbers |
| **experiments/** scheduling (empty log) and review-setups (K-table) | 2 files | Keep one line each in PIPELINE: "split reviewers by concern; capture expanded states first" | 30-day research budget |
| **INFRASTRUCTURE.md** to the env-var table and launch checklist | 5,200 → ~1,200 words | Vendor "why" sections are research; the code and Vercel are the truth | "If the code can answer it, read the code" |
| **TEST-CHECKLIST.md**, **docs/DOC-INVENTORY.md** + judgments.json + doc-inventory.ts + regen-docs.ts | 3 docs, 2 scripts, 1 test | Manual smoke is what CI does; the inventory is stale since 10-16, never runs in CI, duplicates tend-docs and disagrees with it | one home per thing |
| **Orphan scripts and dead gates in web** | ~15 files | `t049/t050/t052-sandbox-check.mjs` (one-off copies of tests), `001-create-tables.sql` and `seed-folsom-coffee.sql` (legacy schema), six `probe-*.sh` nobody runs, `supabase/tests/*.sql` (pgTAP, never run), `db:push` and `mutate` npm scripts (unused), 18 dated `unclaimed/makers-*.json` piling up in `scripts/` | prune, don't annotate |
| **Duplicate CI jobs** | 2 workflows | `migrations.yml` `verify` repeats the Unit tests stack start; its `pending` repeats `applied` on main; the path-line self-test runs in both `ci.yml` and `issue-lint.yml`; `ci-docs-only.yml` is four `echo` jobs | one check per thing |
| **Quarantine list** | 45 evals | Evals that run while their results are thrown away cost browser minutes and prove nothing; delete or fix each | guard-proves-itself |
| **DISPATCH.md** shifts, lanes, modes, folders | 900 → ~200 words | Human rituals; agents wake on events | "Dispatch messages the PM on events, not on timers" (its own item 8) |
| **pipeline-ticket skill** | 1 skill | Describes a file-based ticket system this project doesn't use | prune, don't annotate |
| **Decision rule** in three files | 2 copies | Import one | one place |
| **Dates** (beta, freeze) in six files | — | One `dates.json` the dashboard and docs read | generated, never hand-kept |
| **Marker kinds** beyond open-question, guards, binds | ~1,000 lines of checker | Each pattern "whose problem has stopped happening is a candidate for deletion" | LIVING-DOCS opening paragraph |

Rough total: method docs from ~25,000 to ~8,000 words; web workflows from 33 to about 15; scripts down by a third; one PR section instead of five.

## 5. The nimble version, on one page

**Docs an agent reads** (per session, by role):
- Code: `CLAUDE.md` (≤1,500 words), `constraints/code.md`, the Issue, the scenario. Nothing else.
- Planning: `CLAUDE.md`, `PRINCIPLES.md`, the spine entry, the scenario.
- Method: `ABSOLUTES.md` (8 slugs), `PIPELINE.md` (≤2,000 words: five kinds, decision rule, who checks what, the gate table), `WHERE-THINGS-GO.md`.

**Checks that gate a merge** (all run code): build · unit · browser · migrations from scratch · migrations applied · no undocumented migrations · visibility matrix · action-layer and ontology · markers lint · a second-agent review posted as a GitHub review.

**After merge**: deploy-health · smoke-live · dashboard regenerate.

**The PM's surface**: one page, three numbers (main green, criteria met, items waiting on you with the oldest age), one item in the queue, one `found-by-pm` label. He never sees a PR.

**Triggers, not shifts**: PR events wake the builder (`/loop` or cloud Auto-fix); a failed main build opens one Issue; a scheduled task regenerates the dashboard; a 7-day-old PM item pings once; unattended hours run under a deny floor (no force-push, no data deletion, no new paid service) rather than a queue.

**The grade card as a check**: if this rubric is worth keeping, the five numbers that can be computed go in one script and the rest is deleted: PR open to merge (median), main red minutes, PM items older than 7 days, `found-by-pm` Issues per 10 merged PRs, words an agent must read per role.

## 6. What others do, and what to take

Sources read today (URLs in the footnotes). "Verified" means the primary page was read; the rest comes from write-ups quoting it and should be re-checked before anyone quotes a sentence.

**Anthropic (verified, code.claude.com and anthropic.com)**
- **REVIEW.md** is a repo-root file of review-only rules (what to flag, at what severity, what to skip, "evidence as file:line before posting"). The hosted Claude Code Review (GA 15 Oct 2026, Team/Enterprise) reads it from the default branch; the local `/code-review` reads CLAUDE.md, not REVIEW.md. It never approves or blocks a PR. **Take:** replace the prose "Reviewer's first pass" with a real second-agent review: `/code-review` in a separate session or the hosted review, rules in one REVIEW.md, the check verifying a review exists from a non-author.
- **Harness design for long-running apps (Mar 2026):** planner, generator and a *separate skeptical evaluator*; "Claude out of the box is a weak QA agent"; tuning a standalone evaluator beats self-critique. **This is the exact failure in PR #990**: builder and reviewer were one agent.
- **Effective harnesses (Nov 2025):** a JSON feature list where the agent may only flip `passes`, one feature per fresh session, verify end to end in a browser because unit tests and curl missed failures. SocialUs already has the criterion roll-up and browser job; what it lacks is the one-feature-per-fresh-context discipline that lanes and shifts replaced.
- **Best practices page:** "Would removing this line cause Claude to make mistakes? If not, cut it." Hooks for things that must happen every time; skills for on-demand knowledge; a verification gate escalating from prompt to `/goal` to a Stop hook to a subagent. **Take:** run that question over every line of the 25,000 words.
- **`/goal`:** a separate small-model evaluator re-checks the done condition after every turn. **`/loop`:** session-scoped maintenance with a built-in prompt "tend to the current branch's PR: review comments, failed CI, merge conflicts." **Cloud Auto-fix PR** watches CI and review comments without a machine. **Take:** these replace the 5am/5pm handoff, the lanes, and the Mac as build host.
- **Auto permission mode** is now the default (classifier blocks merging a PR no human approved, prod deploys, migrations, force-push; 17% false-negative on overeager actions, Anthropic's own number). **Take:** stop paying a desktop approval per session; set auto once, keep the four hard gates in CI.
- **Anthropic's own numbers (Deputy CISO, Jul 2026):** Claude authors about 80% of merged code; human review reserved for regulated or critical code with risk-weighted sampling of the rest; the hard gate is CI, not a pre-tool prompt. Source control post (Oct 2026): humans "examine the intent of the change as opposed to reading every line." **Take:** the PM reading three phone steps per PR was already right; make it a sample, not a queue.

**OpenAI "Harness engineering" (Feb 2026, secondary):** 1M lines, 1,500 PRs, no hand-written code. They tried one big instruction file and dropped it: "too much guidance becomes non-guidance, it rots instantly." A 100-line AGENTS.md as a table of contents; architectural invariants as custom linters whose failure text is the fix; a doc-gardening agent that opens PRs; observability the agent can query. **Take:** the method's `tend-docs` and `guard-proves-itself` are this. The 8,300-word PIPELINE.md is the thing they deleted.

**Steve Yegge (secondary):** Gas Town (coordinator, disposable workers, one merge-queue agent, human as "Overseer") and Beads (tasks as JSONL in git). By Aug 2026 he said his own setup failed because agents kept tinkering with the orchestration instead of the application, and that "even with unlimited tokens, the bottleneck is people"; budget no more than about 3 hours a day of human supervision. **Take:** the trial scoring layer, tuning notes and doc garden are agents tinkering with orchestration two weeks before a beta. Freeze them.

**Ralph Wiggum loop (verified, Huntley and the Claude Code plugin):** a bash loop restarting a fresh agent per task; "backpressure via tests, typechecks, lints, builds that reject unacceptable work"; "when Ralph fails a specific way, add a sign"; `--max-iterations` as the safety. **Take:** the method's "named failure with a dated example" is the sign rule. The fix-loop cap of 2 is the max-iterations rule. Both already here.

**Practitioners (mostly secondary):** Hashimoto: each agent mistake becomes a lint plus one AGENTS.md line; the reality is one agent 10 to 20% of the day, not fleets. Ronacher: delete automations nobody uses; plain compiler errors beat LSP noise. Willison: red/green TDD, or the test never exercises the code. Cherny (Claude Code's creator): one shared CLAUDE.md, a line per mistake, "give Claude a way to verify its own work" is the most important tip, a PostToolUse hook that auto-formats so CI never fails on style. Karpathy's autoresearch: the agent may edit one file, five-minute budget, keep or discard by one number. **Take:** one number per loop; the agent keeps or discards on it.

**Spec-driven tooling (secondary):** Spec Kit (constitution → specify → plan → tasks → implement, human reviews each phase), Kiro (requirements in EARS form, each task linked to a requirement, hooks on save), Factory (spec mode read-only, then autonomy by per-command risk), Devin (knowledge pinned to the repo, playbooks), Cursor (rules under 500 lines). SocialUs's scenario grammar is as strong as any of these and stricter than most. Where they differ: every one of them has the human approve a *document* before build; SocialUs rightly moved that approval to the live app.

**Rubrics (secondary):** DORA 2025 names seven capabilities (clear AI stance, version control, small batches, user-centric focus, quality platform, data) and a "verification tax" J-curve. Swarmia's five levels: "if you can't describe done unambiguously, you're at L2." Osmani's L5: "managed by exception, agent factories." Thoughtworks Radar v34 (Apr 2026): "coding agents on a leash", feedback sensors wired so failures self-correct before human review, and "re-evaluate the need for SDD tooling as models improve." By those ladders SocialUs is at L4 heading for L5 on the build loop, and at L2 on the human loop because the human part has not been exercised.

**Failure modes everyone names, and which ones are here:**
- Monolithic instruction file rots: **here** (PIPELINE.md, INFRASTRUCTURE.md).
- Agents gaming the check: **here in miniature**; a checklist the author ticks is a check that rewards ticking. The research answer is to change what the check rewards, not to add "don't cheat" prose.
- Humans reviewing what they can't judge: **designed out**, correctly ("Don doesn't read code").
- Orchestration eating the work: **here** (trial layer, 17,600 lines of tooling, 33 workflows).
- Verification tax on the human: **here** (29 to-dos, 0 looks).
- Unbounded loops: **absent**; fix loop capped at 2.
- Perception gap (feels faster, isn't): **unmeasured**; found-by-pm has no data.

**Hermes Agent (Nous Research; verified from the repo at commit dc0fe3e today).** MIT, Python, about 256k stars, launched 2026-02-25, $90M Series B on 2026-10-07. A personal assistant first and a coding harness second, which is why it is worth looking at: its harness is general and small. What it does that SocialUs does not:
- **Bounded memory with hard caps.** `MEMORY.md` is 2,200 characters and `USER.md` 1,375; an over-limit write errors and the agent must consolidate before it can write. SocialUs has budgets in kilobytes and a weekly refine pass; Hermes makes the cap bite at write time. **Take:** make the budget check fail the PR that grows a doc, not the Friday pass.
- **Lessons, not logs.** The agent saves a skill when it worked out a multi-step flow, got past an error, or was corrected; a curator moves unused skills to stale, then archived, never deleted; "PR numbers and dates are not skill content." **Take:** the 32 build-log files are logs; the rule in `ops-pattern` ("a procedure improvised once goes into a skill that session") is the lesson rule. Keep the rule, delete the logs, add the curator.
- **Quality gates before judgement.** `/goal` runs deterministic shell commands that must exit 0 *before* any model judge sees the work. **Take:** this is "a standard exists when lint checks it" made literal: the reviewer agent should not even start until the four CI checks are green.
- **Headless denies by default.** Anything unattended (cron, webhook, quiet mode) denies dangerous actions and fails closed on timeout; deny-globs such as `git push --force*` sit below every autonomy mode. **Take:** the Tuesday-to-Thursday unattended window should run with a deny floor, not with a PM queue.
- **Staged writes for learned rules.** Agent-proposed memory and skill changes queue for a human diff (`/memory pending`, `/skills diff`) instead of auto-committing. **Take:** this is what the `pm-approved` guard was reaching for, done at the right layer and without a workflow.
- **Handoff metadata on every card:** changed files, verification, residual risk. **Take:** that is the whole PR body. Three fields, not five sections.
- **Role profiles with per-role model pins** (frontier reviewer, cheap implementer) and a Kanban where "PR completion contracts" read GitHub's required checks before a card can close. SocialUs's model tiers in PIPELINE-build are the same idea, as prose.
- **Where it is weaker than Claude Code for this job:** subagents start blind (only the goal and AGENTS.md), checkpoints are off by default, no first-class PR-event subscription or CI-log tooling beyond `gh`, and reviewers rank it below Claude Code on safety. Don't switch; steal the seven items above.

**Across all of them, four ideas repeat and all four point the same way.** A separate skeptical evaluator (Anthropic, Hermes `/review`, Yegge's Refinery). Checks as backpressure, prose as nothing (Ralph, Hashimoto, Thoughtworks, Hermes quality gates). One small instruction file plus progressive disclosure (OpenAI, Cursor, Hermes context chain, Anthropic's "would removing this line cause mistakes"). Humans by exception and by sample, never as a queue (Anthropic's 80% with risk-weighted sampling, Osmani L5, Yegge's 3 hours a day).

**Footnotes.** Anthropic: code.claude.com/docs/en/code-review-customize, /code-review-local, /best-practices, /goal, /scheduled-tasks, /permission-modes, /claude-code-on-the-web; anthropic.com/research/harness-design-long-running-apps, /effective-harnesses-for-long-running-agents, /effective-context-engineering-for-ai-agents, /claude-code-auto-mode, /redesigning-source-control; claude.com/blog/how-anthropic-secures-its-ai-native-software-development-lifecycle. OpenAI: openai.com/index/harness-engineering. Yegge: steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04; newsletter.pragmaticengineer.com/p/steve-yegge-on-ai-agents-and-the. Ralph: github.com/ghuntley/how-to-ralph-wiggum; github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum. Hashimoto: mitchellh.com/writing/my-ai-adoption-journey. Ronacher: lucumr.pocoo.org/2025/7/30/things-that-didnt-work. Willison: simonwillison.net/guides/agentic-engineering-patterns. Cherny: gist.github.com/eldermoraes/9bc426c67410081e1881b1b5127764b5. Karpathy: github.com/karpathy/autoresearch. Spec Kit: github.com/github/spec-kit. Kiro: kiro.dev/docs/specs/concepts. Factory: docs.factory.ai/cli/user-guides/auto-run. Cursor: cursor.com/docs/context/rules. DORA: dora.dev/dora-report-2025. Swarmia: swarmia.com/blog/five-levels-ai-agent-autonomy. Osmani: addyosmani.com/blog/agentic-autonomy-levels. Thoughtworks: thoughtworks.com Radar vol 34.

## 7. Next action

- **This week (before freeze):** delete build-log/, the review workflow and the three prose sections; shrink the PR template. Half a day, no behaviour change, all already ruled.
- **Clear the human queue:** merge the 10 copy drafts under the voice rules and let the PM edit live; close the 29 to-dos down to one.
- **After beta:** fold PIPELINE-build into PIPELINE, move rulings to plan, freeze the trial layer, replace shifts with triggers (`/loop`, cloud Auto-fix, scheduled tasks, auto permission mode), add a REVIEW.md and make the reviewer a second agent, and promote this grade card to one script if it earns its keep.
- **The one decision for the PM:** A) do the "this week" cuts now, before the freeze (recommended: no behaviour changes, all already ruled, frees agent time for beta bugs); B) freeze the method as is until beta ships and cut on 11-07; C) cut only the human-queue items now and leave the docs.
