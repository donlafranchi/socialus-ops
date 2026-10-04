# SocialUs agent patterns — draft

Read from `ops-pattern` @ `origin/main` `eddbf02` and `socialus-web` @ `origin/main` `aa491bb` on 2026-10-04, plus `~/Projects/skills` and the global `~/.claude/CLAUDE.md`. `~/.claude/templates/` could not be reached from this session and was not read. Paths with no repo prefix are in `ops-pattern`; `socialus-web/…` paths are in the app repo.

## Summary

SocialUs is built by agents working in two repos. `ops-pattern` is the planning repo: rulings, scenarios, generated status. `socialus-web` is the app repo: code, Issues, PRs and CI. A third repo, `~/Projects/skills`, holds the skills both repos symlink in. Don rules on product and judges whether things are right. Agents own whether things are correct, and they prove it with checks rather than prose. Four ideas carry the system. A fact lives once, inline, and anything that spans the project is generated from markers. Superseded text is deleted, so the newer ruling is the only one an agent ever sees. No check is trusted until it has been seen failing. Production changes go through narrow, guarded doors. Most of the planning-side patterns are enforced by lint. The weak spots are the human interface (how agents report to Don, how Dispatch routes work, the "Don, please look" PR block) and the merge gate. Those are convention only, and the merge gate is not binding because branch protection was unavailable when CI was written.

## Roles

| Role | Owns | Never | Source |
|---|---|---|---|
| **Don (PM)** | Rulings, judgement on whether something is *right*, domain facts. Previews `needs-don` PRs on a phone. Applies migrations. | Reads code; reads more than `STATUS.md` and `ROADMAP.md` unless he asks | `ops-pattern/CLAUDE.md` § Who does what; `process/PIPELINE.md` § Who checks what |
| **Dispatch** (PM agent, orchestrator) | Routes work to the long-lived sessions, relays rulings, tells the working agent to merge | Undocumented beyond passing mentions | `process/PIPELINE.md` ("Cowork via Dispatch"); `DECISIONS.md` 2026-09-16 merge ruling |
| **Cowork** (planning agent): `plan` `review` `sync` `trim` | `ops-pattern`: scenarios, `DECISIONS.md`, `ROADMAP.md`, `product/`. May open Issues in `socialus-web`. Reviews architecture notes. | Commits code; hand-edits generated files | `ops-pattern/CLAUDE.md`; `~/Projects/skills/README.md` |
| **Code** (build agent): `ticket` `build` `diagnose` `respond` `design-review` | `socialus-web`: architecture notes, Issues, TDD code, PRs, self-merge when green | Writes scenarios, rulings or `STATUS.md`; redesigns; rolls back | `socialus-web/CLAUDE.md`; `~/Projects/skills/build/SKILL.md` |
| **Evaluator** | No separate agent. Its work is split between CI (`socialus-web/.github/workflows/ci.yml` browser job: feature evals, screenshot matrix), the `verify` skill, and `[guards F###.N]` markers | — | `~/Projects/skills/verify/SKILL.md`; `socialus-web/evals/` |

Code is the architect. Any ticket that touches schema, RLS or routes starts with an architecture note of 20 lines or fewer in the Issue. Cowork reviews it, and Don sees it only if they disagree (`ops-pattern/CLAUDE.md`).

## Patterns

Status key: **Enforced** means a lint, CI job or structure fails when the pattern is broken. **Convention** means the pattern is written down but nothing checks it. **Aspirational** means it was ruled or described but is not yet in force.

### A. Truth and documents

**A1. Facts live inline; cross-cutting docs are generated from markers**
- **Rule:** A fact sits at the one place it is true. Anything that spans the project is generated from markers: open questions, guard coverage, which ruling binds which tier, gating, platform needs. That covers `STATUS.md`, `README.md`, `constraints/*.md` and `PLATFORM-*.md`. Hand-maintained indexes are banned.
- **Why:** REGISTRY, MAP, TRACE, STAGE-LEDGER, JOURNAL and `WHERE-IT-IS.md` each went stale and were believed anyway (`process/LESSONS.md` 2, 23, 32).
- **Enforced by:** `scripts/markers.py lint`, run from `scripts/lint.sh` in `.github/workflows/lint.yml`. The lint fails if a generated file has drifted or lacks its header. `.github/workflows/status.yml` regenerates on push, daily at 13:05 UTC, and from a phone. A workflow does this rather than a skill because the `status` skill was never installed and never ran (lesson 27).
- **Status:** Enforced.

**A2. Prune, don't annotate: `[replaces …]`**
- **Rule:** A superseded ruling, clause or scenario is deleted. Its replacement names it in one `[replaces …]` tag so `git log -S` can find it.
- **Why:** On 2026-09-22 and 2026-09-23 two opposite rulings were "kept rather than struck", and readers had to re-derive which one held (lesson 33).
- **Enforced by:** The replaces checker in `scripts/markers.py` fails on a reversal that names nothing, and on a named thing that is still present. It proves itself against `scripts/fixtures/markers/replaces-bad/` on every run (`scripts/lint.sh` §5).
- **Status:** Enforced.

**A3. Newer decision wins: `[newer-decision-wins]`**
- **Rule:** When two rulings conflict, the newer one wins and work continues. The only case raised with Don is two *live* rulings that conflict where neither replaces the other. That goes in as an `[open-question owner=don]` marker, never as a blocking message. Agents never split the difference.
- **Why:** `socialus-web` #220 asked Don to confirm a 2026-09-14 ruling over a 2026-09-13 one. Don named this as a stop-and-ask he hits repeatedly.
- **Enforced by:** It is structural. `DECISIONS.md` holds live rulings only, and `constraints/code.md` is generated from those, so no conflict is visible to an agent. A2's lint backs this up. Defined in `process/ABSOLUTES.md`.
- **Status:** Enforced.

**A4. Per-tier constraints**
- **Rule:** Every ruling ends with `[binds tiers=… surfaces=…]`. Each tier reads only its own generated `constraints/<tier>.md`. A ruling that binds code must name its Issue or `F###`, or carry `build=none`.
- **Why:** F076 forbade a pre-filled home, but the code kept `DEFAULT_HOME_PLACE_ID` (#205). Separately, the identity-leak ruling sat for eight days with no Issue.
- **Enforced by:** `markers.py constraints` and `markers.py gating`. `scripts/lint.sh` fails if a constraints file is stale or a code-binding ruling names no work. `STATUS.md` lists the `build=none` escape hatches.
- **Status:** Enforced. Rulings from before 2026-09-21 are untagged.

**A5. Open questions are inline markers**
- **Rule:** The marker is `[open-question owner=don|cowork|code raised=YYYY-MM-DD] question`. It goes in the file the answer will change, never in a PR, a commit or `DECISIONS.md`. A `don` question is closed by a dated ruling in the same commit that removes the marker.
- **Why:** F080's question lived in three places at once (lesson 31).
- **Enforced by:** `markers.py lint` in `ops-pattern`, and `socialus-web/scripts/check-markers.sh` in `socialus-web` CI. Both prove themselves on bad fixtures first.
- **Status:** Enforced. Issue bodies are scanned but not gated.

**A6. "We currently…" wording; only "never extractive"**
- **Rule:** A ruling states what we currently do, not a permanent refusal. The one approved "never" is "never extractive".
- **Why:** On 2026-09-30 Don ruled that "every ruling can be revisited" (`DECISIONS.md` line 73), and on 2026-10-01 that he doesn't like "never".
- **Enforced by:** `scripts/never.py` proves itself on `scripts/fixtures/never/`. But `scripts/lint.sh` only scans real documents when `NEVER_LINT=1`, which is off "until Don approves the rewording". The "never extractive" exception exists only in `scripts/never.py`'s docstring and the lint comment, not as a `DECISIONS.md` line. Authored docs, the CLAUDE.md files included, still use "never" heavily.
- **Status:** Aspirational. The checker is built but does not gate anything.

**A7. One concept, one place (the spine)**
- **Rule:** Nouns, verbs and surfaces live in `product/` and carry their own status. A future version of something is a status on the existing entry. `IMAGINE.md` holds only ideas with no shape yet. `product/systems/` says how something works, never whether it ships.
- **Enforced by:** `scripts/lint.sh` allows only eight root `.md` files and checks links. The rest is convention.
- **Status:** Partly enforced.

**A8. Slugs, not numbers, for absolutes**
- **Rule:** Cite an absolute as `[production-asks-don]`, never as "rule 3".
- **Why:** Three of five numbered rule sets had become dead pointers.
- **Enforced by:** `scripts/lint.sh` §4 fails on any slug with no matching heading.
- **Status:** Enforced (`DECISIONS.md` is exempt).

**A9. Accepted risks expire**
- **Rule:** One JSON file per finding in `accepted-risks/`, each with `owner`, `review_by` and `revisit_if`. `scripts/advisor-diff.sh` shows only the findings nobody has ruled on yet.
- **Why:** The same advisor findings were re-triaged from scratch every time (lesson 22).
- **Enforced by:** `scripts/lint.sh` fails the day a `review_by` passes, and proves itself on `fixtures/markers/risks-bad`.
- **Status:** Enforced.

**A10. Small, testable scenarios**
- **Rule:** A scenario has Story, Acceptance and Not this, at 40 lines or fewer, plus an uncounted `## Why`. Its frontmatter carries `status: draft → approved → building` and `gates: launch`. Scenarios approved from 2026-09-29 on must carry a `[platform …]` marker.
- **Enforced by:** `scripts/lint.sh` §1 and §1b; `markers.py gating` and `markers.py platform`.
- **Status:** Enforced. `building` is self-reported. `markers.py building` checks it against the code as a report, not a lint.

### B. Judgement and escalation

**B1. Don rules on A/B/C with a recommendation**
- **Rule:** Ask only when a fact only Don has is missing, or when the deadline is affected. Present A/B/C options, one line each, with a recommendation. Agents recommend; Don decides (`[don-decides]`). A ruling exists only as a dated line in `DECISIONS.md` (`[ruling-is-dated-line]`).
- **Enforced by:** The marker grammar is linted. Asking one question at a time is not written anywhere in either repo.
- **Status:** Convention. The dated-line half is effectively enforced through A4.

**B2. Escalate, don't improvise**
- **Rule:** A PR whose behaviour differs from its scenario's Acceptance stops and asks for a scenario change in `ops-pattern` (`socialus-web/CLAUDE.md`). A change or bug that starts needing acceptance checks becomes a scenario.
- **Enforced by:** `socialus-web/.github/workflows/issue-lint.yml` flags acceptance checkboxes on non-scenario Issues. The divergence rule itself is unchecked. Deviation markers were considered and not built (`process/LIVING-DOCS.md`).
- **Status:** Convention, with partial enforcement.

**B3. Speculative items go to Later, not to a ruling**
- **Rule:** Speculative ideas go to `ROADMAP.md` § Later or "Speculative, not ruled", or to `IMAGINE.md`. Don is not asked to rule on them. Examples: price on cards, a public member profile, an event Page without an organization (`DECISIONS.md` 2026-09-30 and 2026-10-01).
- **Status:** Convention. The rule is not stated as such anywhere.

**B4. Report format**
- **Rule:** `Status: Done | Blocked | Question — one sentence. Next: the ask.` Detail comes on "expand".
- **Enforced by:** Written only in `ops-pattern/CLAUDE.md` § How to talk to Don. Missing from `socialus-web/CLAUDE.md`.
- **Status:** Convention.

**B5. Process changes need a dated failure**
- **Rule:** A process change must name the failure it fixes, with a date, in `process/LESSONS.md`. A new absolute needs a failure that a guideline demonstrably did not prevent, filed under one of the four harms. A pattern whose problem has stopped happening is a candidate for deletion.
- **Enforced by:** `process/PIPELINE.md`, `process/ABSOLUTES.md`, `process/LESSONS.md` § Guardrails.
- **Status:** Convention.

### C. Verification

**C1. Every guard is seen failing first: `[guard-proves-itself]`**
- **Rule:** A check counts as absent until it has been observed rejecting bad input. It ships with a fixture that must fail, and that fixture runs on every run.
- **Why:** Three guards were inert within two days (2026-09-19 to 2026-09-21): the preflight parser, `migrations (check)` and `issue-lint`. The second one is why the 2026-09-21 outage happened.
- **Enforced by:**
  - `scripts/lint.sh` checks expected rejection counts against fixtures.
  - `socialus-web/scripts/check-markers.sh` runs a self-test.
  - `socialus-web/evals/_guard/must-fail.spec.ts` is in CI.
  - The apply guard's self-test runs in `socialus-web/.github/workflows/apply.yml`.
  - `socialus-web/tests/runnable-gate.test.ts` makes a suite that cannot run fail rather than skip.
- **Status:** Enforced wherever it has been applied, but nothing checks that it has been applied everywhere. Counter-examples:
  - `socialus-web/evals/personas.ts` cites `tests/personas-agree.test.ts`, which does not exist.
  - `socialus-web/scripts/builder-isolation-probe.sh` prints "PASS (vacuous)".

**C2. Guard coverage maps criteria to checks**
- **Rule:** Mark a check with `// [guards F093.4]`, or `[guards F093.4 partial: …]` if it covers only part of the criterion. An unmarked criterion counts as unverified, not as verified.
- **Enforced by:** `markers.py coverage` writes the map into `STATUS.md`.
- **Status:** Enforced as a report. `STATUS.md` currently says 17 of 22 approved and building scenarios are unverified.

**C3. Verify against production by calling it**
- **Rule:** Ask the running system directly rather than trusting the code. "It works on the seed" is evidence only about the seed: verify against a row that went through the handler (`socialus-web/CLAUDE.md` § The seeds are privileged). Every PR states how it was verified: `live DB · local Postgres · unit tests only · not verified`. Unverified work opens as a draft.
- **Why:** Writes were down for four months because `DATABASE_URL` was unset in Vercel and every check that runs before a deploy was blind to it (`socialus-web/.github/workflows/deploy-health.yml` header). Bug #175 survived because seeded rows looked right.
- **Enforced by:**
  - `socialus-web/.github/workflows/deploy-health.yml` hits `/api/health/db` after deploy.
  - `socialus-web/.github/workflows/ci.yml` `applied` asks production whether each migration exists.
  - `socialus-web/scripts/probe-anon-*.sh`, `socialus-web/scripts/probe-member-reads.sh` and `socialus-web/scripts/builder-isolation-probe.sh` read production as a stranger. These are manual and in no workflow.
  - The `verify` skill.
  - The PR verification line comes from the template only.
- **Status:** Partly enforced.

**C4. Status claims are backed by code**
- **Rule:** `STATUS.md` reports open Issues whose ticket appears on main, and things that are "still on main, meant to be gone". `socialus-web/tests/retired-routes.test.ts` covers retired routes.
- **Status:** Enforced as a report.

### D. Merges, migrations and production

**D1. Code merges itself when green; Don merges only `needs-don`**
- **Rule:** A PR that says "Don doesn't need to look" is merged by the agent that did the work, once checks are green. Whoever does the work merges it, in either repo (`DECISIONS.md` 2026-09-16).
- **Enforced by:** `.claude/settings.json` in `ops-pattern` allows `gh pr merge`. **Nothing blocks a red merge.** Branch protection returned 403 on the old plan (`socialus-web/.github/workflows/ci.yml` `applied` comment, #187), so green is on the honour system. There is no auto-merge.
- **Status:** Convention.

**D2. The first PR block routes Don's attention**
- **Rule:** The PR body opens with either "Don doesn't need to look." plus a reason, or "Don, please look" with a preview link, three phone-level steps and what he should see, plus the `needs-don` label. That label stays on after merge, so `is:merged label:needs-don` lists what shipped without his eyes.
- **Enforced by:** `socialus-web/.github/pull_request_template.md`. `socialus-web/.github/workflows/issue-lint.yml` checks only that the PR cites an Issue.
- **Status:** Convention.

**D3. Migrations: Don applies, one at a time, and the database goes first**
- **Rule:** A migration is applied to production from its own branch *before* merge, through `socialus-web/.github/workflows/apply.yml`. That workflow is manual, requires typing `apply`, uses the Supabase CLI and never the management API, and checks for drift before and after. One pending migration at a time. A stacked branch is refused.
- **Why:**
  - 2026-09-11: the management API caused silent drift.
  - 2026-09-21: a merge went out ahead of its migration and every Page URL 404'd.
  - 2026-09-30: three stacked PRs (#254, #255, #258) ran ahead of their code and signed-out Pages 404'd.
- **Enforced by:**
  - `socialus-web/scripts/migrations-apply-guard.sh` refuses a non-main base, a missing PR, or more than one pending migration. It self-tests in `socialus-web/.github/workflows/apply.yml`.
  - `socialus-web/.github/workflows/ci.yml` `applied` runs on PRs and main.
  - `socialus-web/.github/workflows/migrations.yml` checks from scratch and runs a daily pending check.
  - `socialus-web/tests/migrations-apply-guard.test.ts`.
  - Branches are now named by Issue number so the apply command is short (2026-10-02).
- **Status:** Enforced. "Don applies" is convention: any session with `gh` can dispatch the workflow. An uncommitted `socialus-web/.github/workflows/migrations-apply-production.yml` sits in the working tree, so work is in flight.

**D4. Fix forward, never roll back or rewrite history**
- **Enforced by:** `~/Projects/skills/build/SKILL.md`, both CLAUDE.md files and `[production-asks-don]`.
- **Status:** Convention.

**D5. Pinned toolchain**
- **Rule:** Runners are pinned to `ubuntu-24.04` and the Supabase CLI to `2.117.0`.
- **Why:** `latest` was rate-limited on 2026-09-21 and blinded the migrations check (#164).
- **Enforced by:** `socialus-web/tests/workflow-pins.test.ts`.
- **Status:** Enforced.

**D6. Every write goes through the action layer**
- **Rule:** Every write goes through a named, transactional handler that also writes its `*_events` row. The service-role key and raw `pg` stay inside `socialus-web/src/actions/_lib/**`.
- **Enforced by:** `socialus-web/eslint.config.mjs` (T051 Rule 1) and `socialus-web/scripts/check-action-layer-conformance.ts`.
- **Status:** Enforced.

### E. Seeing the app

**E1. Builder accounts on the live app**
- **Rule:** There is one login per persona, marked as a builder. A builder account has no text code and no legal name. Nothing a builder makes is shown to members or counted. The operator persona can moderate. Logins come from the `BUILDER_SEED` secret, and any account can be switched off.
- **Why:** Don asked for this on 2026-10-01 so agents can see every view.
- **Enforced by:**
  - `socialus-web/supabase/migrations/20261001100000_builder_accounts.sql`
  - `socialus-web/scripts/builders.ts`
  - `socialus-web/.github/workflows/builders-production.yml` (manual)
  - `socialus-web/tests/builder-isolation-db.test.ts` in CI
  - `socialus-web/scripts/builder-isolation-probe.sh` against production (manual, can pass vacuously)
- **Status:** Enforced locally. The production check is manual.

**E2. Personas and the screenshot matrix**
- **Rule:** `socialus-web/evals/personas.ts` defines 13 personas. CI seeds them into a throwaway stack. `socialus-web/evals/screens/matrix.spec.ts` captures every inventory route, as every persona, at 390, 744, 1024, 1280, 1440 and 1920px, and uploads the result as the `screenshots` artifact.
- **Enforced by:** The `socialus-web/.github/workflows/ci.yml` `browser` job.
- **Status:** Enforced for capture only. Gaps:
  - The matrix fails only on a 5xx or a page error. "The review happens on the pictures", but no role, skill or check owns that review.
  - 51 feature evals are quarantined (`socialus-web/evals/quarantine.ts`).
  - The personas still include `ownerEvent`, `ownerPlace` and others, but the 2026-10-01 ruling cut Page kinds to group, business and organization.

**E3. Design tokens are the single source**
- **Rule:** Tokens live in `socialus-web/src/app/globals.css`, and `product/ui/design-language.md` keeps only the reasons (`DECISIONS.md` 2026-10-01; chore #294).
- **Enforced by:** Nothing. There are 57 arbitrary `[Npx]` or hex values in `socialus-web/src/**/*.tsx`, and a second copy of the tokens remains at `ops-pattern/planning/research/design/socialus-tokens.css`.
- **Status:** Aspirational.

### F. Work routing and sessions

**F1. Two repos (three with skills)**
- **Rule:** `ops-pattern` is planning. `socialus-web` is code, and a merge there deploys. `skills/` is symlinked into each repo's `.claude/skills/`. Tickets exist only as Issues. Agents never cross-commit.
- **Why:** `web/` nested inside the planning checkout caused lock collisions (lesson 9).
- **Status:** Enforced by structure. Note that `ops-pattern` is pushed, not local-only as the global template says.

**F2. Five kinds of work**
- **Rule:** Every piece of work is a scenario, change, bug, process or chore, each with its own path (`process/PIPELINE.md`). Issue titles look like `F060 · T142 · plain name` or `bug · plain name`, and the body carries `Kind:` and `Scenario:`.
- **Enforced by:** `socialus-web/.github/workflows/issue-lint.yml` checks Kind, Scenario and checkboxes. It does not check the title.
- **Status:** Partly enforced.

**F3. Dispatch and long-lived sessions**
- **Rule:** Dispatch routes work to one build session per repo and one planning session, rather than spawning many.
- **Enforced by:** Nothing in either repo. `ops-pattern/CLAUDE.md` § Sessions governs worktrees only. Branch naming is explicitly designed so that "dozens of agents" can name branches without coordinating.
- **Status:** Convention, and undocumented.

**F4. Session hygiene**
- **Rule:** Every session works in its own worktree at `../worktrees/{repo}/{branch}`. Read-only sessions use `git --no-optional-locks`.
- **Why:** Lessons 9, 18 and 19.
- **Status:** Convention.

**F5. Merge-conflict-free build log**
- **Rule:** One file per ticket, at `socialus-web/build-log/YYYY-WNN/<ticket>-<slug>.md`.
- **Why:** A shared weekly file conflicted with every other open PR (chore #76).
- **Status:** Enforced by structure.

**F6. Ontology links live in code**
- **Rule:** `socialus-web/src/ontology/links.ts` and the generated `socialus-web/src/ontology/registry.json` are updated in the same PR as the ruling that changes a link.
- **Enforced by:** Conformance Rule 5 and a registry comparison test.
- **Status:** Enforced.

**F7. Markdown deliverables in the repo, not Claude artifacts**
- **Enforced by:** Nothing. It is not written in either repo, and `business/entity-structure/*.html` exists.
- **Status:** Convention, undocumented.

## End-to-end: one feature

1. **Idea:** Don or `IMAGINE.md` raises an idea. Cowork's `plan` writes `planning/scenario-F###.md` with `status: draft`, 40 lines or fewer, platform marker and `gates:` if it gates launch. Anything Cowork cannot answer becomes an open-question marker in `## Why`.
2. **Questions:** Don rules on A/B/C. Each answer becomes a dated `DECISIONS.md` line with `[binds …]` and, where something was superseded, `[replaces …]`. The same commit closes the marker. `markers.py constraints` regenerates `constraints/code.md`.
3. **Approval:** Cowork's `review` flips the scenario to `approved`. Don is involved only on scope or a contested call. `scripts/lint.sh` must pass in CI.
4. **Ticket:** Code's `ticket` opens an Issue titled `F### · T### · name`, with the architecture note if the work touches schema, RLS or routes. Cowork comments on the note.
5. **Build:** Code's `build` reads `constraints/code.md`, writes failing tests first, sees each one fail, then marks it `[guards F###.N]`. The branch is named by Issue number. A migration means one migration per PR.
6. **PR:** The body opens with the Don block, a "Migration" section and a "How it was verified" line. CI runs:
   - markers
   - lint, types and build
   - Vitest on a throwaway stack
   - the browser job: must-fail guard, evals and screenshot matrix
   - migrations from scratch
   - `applied`
7. **Migration (if any):** Don runs `gh workflow run apply.yml --ref <issue#> -f confirm=apply`. The guard refuses a stacked branch or more than one pending migration. Drift is checked before and after.
8. **Merge:** If "Don doesn't need to look", Code merges once green. If `needs-don`, Don previews on his phone and merges or says to. The merge deploys. `deploy-health` and `applied` run on main.
9. **Verify in production:** A probe or builder account checks the live result. `.github/workflows/status.yml` regenerates `STATUS.md`, including coverage and gating.
10. **Sync:** Cowork's `sync` deletes the shipped scenario, moves its platform markers to the spine, and updates `ROADMAP.md`.

## Gaps

### Convention-only patterns that carry real risk

- **The merge gate (D1):** Green is not binding.
- **The Don block (D2):** Nothing checks the PR's first block.
- **Dispatch and sessions (F3):** Undocumented.
- **Report format (B4):** Not in `socialus-web`.
- **Wording (A6):** The "never" lint is off.
- **Tokens (E3):** No check blocks one-off visual values.
- **Screenshots (E2):** The pictures are captured, but nobody reviews them.
- **Production probes (C3):** Manual.

### Contradictions between repos and docs

1. **`[production-asks-don]` vs self-merge.** `process/ABSOLUTES.md` says "deploy to main … asks Don first". `socialus-web/CLAUDE.md` and the 2026-09-16 ruling say agents self-merge, and a merge deploys. The absolute was never pruned to match ([newer-decision-wins] says the ruling holds).
2. **Branch naming.** `ops-pattern/CLAUDE.md` says `f060-t142-slug` and `bug-36-slug`. `socialus-web/CLAUDE.md` says Issue number only (2026-10-02).
3. **Global `~/.claude/CLAUDE.md` vs the project.**

   | Global file says | Project does |
   |---|---|
   | `JOURNAL.md` | Retired (lesson 2) |
   | `development/tickets/` | Tickets are Issues |
   | `product/products/` | Not used |
   | `feat:` commits with no co-author | `F###/T###:` commits that carry `Co-authored-by: Claude` |
   | Parent repo is local-only | `ops-pattern` is pushed and public |
   | Four agents | Three roles plus Dispatch |

4. **Stale pointers:**
   - `socialus-web/BUILD-LOG.md` says "use JOURNAL.md".
   - `~/Projects/skills/README.md` lists a `status` skill in `ops-pattern/process/skills/`, which was deleted on 2026-09-19.
   - `socialus-web/CLAUDE.md` cites `ops-pattern/PIPELINE.md`; the file is `process/PIPELINE.md`.
   - `socialus-web/evals/personas.ts` cites the nonexistent `tests/personas-agree.test.ts` and `scripts/seed-personas.sh` (the file is `.ts`).
5. **Public vs private.** The repos are public (`DECISIONS.md` 2026-10-01), but comments in `.github/workflows/status.yml`, `socialus-web/.github/workflows/apply.yml` and `socialus-web/scripts/check-markers.sh` still reason from "private".
6. **Repo docs that state the opposite of rulings.**
   - `ROADMAP.md` § Now says "pick a metro"; the 2026-09-30 ruling says nobody picks a metro.
   - `process/ABSOLUTES.md` and `product/ABSOLUTES.md` refer to "the rule admitting a seventh", but there are eight absolutes.
   - The `scripts/lint.sh` comment calls `DECISIONS.md` "append-never-edit"; A2 prunes it.

### Making it more agent-optimized

**1. Make green binding**
- **A (recommended):** Now that the repo is public, retry the ruleset that returned 403 under #187. Require `socialus-web/.github/workflows/ci.yml` (quality, test, browser, applied) and `socialus-web/.github/workflows/migrations.yml` on main, then turn on GitHub auto-merge so "merges itself when green" becomes literal.
- **B:** Keep the honour system and add a post-merge alarm when main goes red.
- **C:** Status quo.
- **Note:** That rulesets are now available is inferred from the 403 text ("Upgrade to GitHub Pro or make this repository public"). Verify it with the API first.

**2. Kill stale pointers by lint, not by cleanup**
- **A (recommended):** Add a cross-repo dead-reference lint: every path cited in a CLAUDE.md, a skill or a code comment must exist. Run it in both repos' CI, with a must-fail fixture. In the same pass, rewrite the global `~/.claude/CLAUDE.md` to point at `ops-pattern` instead of the old template.
- **B:** A one-off cleanup of the items listed under contradictions.
- **C:** Leave it.
- **Trade-off:** A holds; B rots again (lesson 2).

**3. Write down and check the human interface**
- **A (recommended):** Add Dispatch as a role in `ops-pattern/CLAUDE.md` § Who does what, covering long-lived sessions, one question at a time, report format, and that deliverables are markdown in the repo. Extend `socialus-web/.github/workflows/issue-lint.yml` to check the issue title format and that a PR's first heading is one of the two Don blocks, and that a "please look" PR carries `needs-don`.
- **B:** Docs only.
- **C:** A Dispatch skill. A skill fires only when it is invoked (lesson 27).

**4. Smaller gaps, one line each**
- **Tokens:** Add an ESLint rule banning arbitrary `[…px]` and hex values in `socialus-web/src/**/*.tsx`, with an exemptions file, and delete the `ops-pattern` token copy.
- **Wording:** Get Don's ruling on the "never" rewording, add "never extractive" as a `DECISIONS.md` line, then set `NEVER_LINT=1`.
- **Screenshots:** Assign the matrix review to `design-review` on `needs-don` PRs, or add visual diffs. Burn down the 51 quarantined evals and realign the personas to the 2026-10-01 Page kinds.
- **Probes:** Schedule `probe-anon-*` and `socialus-web/scripts/builder-isolation-probe.sh` in `socialus-web/.github/workflows/deploy-health.yml`. Make a vacuous pass fail.
- **Guards:** Add a meta-lint so that every file carrying `[guard-proves-itself]` names a fixture or a failing-run link.
