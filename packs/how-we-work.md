# How we work

Written 2026-11-12 from the knowledge store. 99 live practices, about 5,102 tokens.

How to read it: each line is one live practice. Strictness is absolute (never broken), rule (broken only with
a recorded reason) or guideline. Ring is adopt (how we work), trial (being tried), assess (being looked at)
or hold (not now). The id after each line is its record in the knowledge store.

## Absolutes and principles everything rests on

- The PM decides ideas, what is in each version, and words and look-and-feel; a reversal of a prior ruling in any of those goes to the PM as options with a recommendation. Everything else agents decide by the soul and defaults, record, and report (`process/PIPELINE.md` § Decision rights, 2026-10-25); new territory that conflicts with the soul goes to the PM. (don-decides)
- **A check may not be relied on until it has been observed rejecting input that should be rejected.** Until then it is inert, and an inert guard counts as absent — not as weak, as *absent*. Green is not evidence: every guard below was green throughout. (guard-proves-itself)
- **When a newer decision contradicts an older one, the newer one wins and work continues.** Do not stop to ask Don which is true — he answered when he made the newer one. Build to the newer ruling. (newer-decision-wins)
- Anything that reaches production or can't be undone — deploy to main, destructive migration, deleting data, rewriting history — asks Don first. (production-asks-don)
- Anything public — user-facing copy, a published page, a claim about what the app does — is a draft until Don says otherwise. (public-is-draft)
- A ruling exists only as one dated line: a principle in `PRINCIPLES.md`, or under `## Rulings` in the doc it governs. The code says how; rulings say why; a doc that disagrees with either is the thing that's wrong. Record it at the scope the PM gave: a wider reading is labelled as a reading, because "the other side is patron", internal shorthand, was recorded as a user-facing rule that retired four others (2026-09-14). (ruling-is-dated-line)

## How we decide

- **Each ruling carries a binds tag, and each tier reads only its generated constraints file.** rule, adopt. Why: Rulings did not reach the agents they bound. (practice.binds-tags-per-tier)
- **The PM gives direction; agents research it into options; the PM decides.** rule, adopt. Why: Don's model for building the app. (practice.direction-then-options)
- **Before deciding anything, name 2 to 3 established precedents with links.** rule, adopt. Why: Most decisions were already made well elsewhere. (practice.look-first-precedents)
- **New territory (a ruling, legal, privacy, money or member trust) goes to the PM as A/B/C before building.** rule, adopt. Why: A wrong guess there costs members or trust. (practice.new-territory-goes-as-abc)
- **Every Issue and PR in the code repo carries a Path line, well-worn or new territory, with its precedents beside it.** rule, adopt. Why: It says who decides. (practice.path-line-on-every-issue-pr)
- **Settled ground (members are the investors and only payees) is not re-raised; legal goes to counsel.** rule, adopt. Why: Re-arguing spends PM time. (practice.settled-not-reraised)
- **On a well-worn path agents build the simplest fitting option; when unsure, lean toward deciding.** rule, adopt. Why: The PM's time is the scarcest resource. (practice.well-worn-decide-and-build)
- **Decisions and patterns live in one database with history, queried instead of read as files.** rule, trial. Why: Hundreds of files went stale. (practice.knowledge-store)
- **A ruling changed by member action carries an [evidence] tag; a judgement ruling carries none.** rule, assess. Why: Feedback's effect should be a scan. (practice.evidence-tag-on-member-driven-rulings)
- **PM items go one per message, the most unblocking first, batched for Friday to Monday; never a list.** guideline, adopt. Why: One clear ask gets answered; a list stalls. (practice.pm-queue-one-at-a-time)
- **A council of three cheap members and a strong chair, briefed with the PM's limits, returns one A/B/C.** guideline, trial. Why: Nine overlapping roles were trimmed. (practice.council-three-roles)

## How we plan

- **A change or bug that needs acceptance checks is a scenario, written before it is ticketed.** rule, adopt. Why: Otherwise it ships unapproved. (practice.acceptance-checks-mean-scenario)
- **A ticket touching schema, RLS or routes opens with a short architecture note and its visibility rows.** rule, adopt. Why: Code is the architect. (practice.architecture-note-first)
- **A concept lives once, in the product spine with its status; systems docs never say what ships.** rule, adopt. Why: Two descriptions failed before. (practice.concept-in-one-place)
- **A scenario names the soul line and pitch capability it serves, and when we step out of the loop.** rule, adopt. Why: Extracting from members fails the soul. (practice.ethos-and-pitch-test)
- **Work is classed as scenario, change, bug, process or chore first; a misfit takes the nearest path.** rule, adopt. Why: Non-scenario work fell outside the pipeline. (practice.five-kinds-of-work)
- **A beta-gating scenario says gates: launch, and a code-binding ruling names its Issue or build=none.** rule, adopt. Why: Gating work sat with no Issue. (practice.gates-launch-frontmatter)
- **Ideas with no noun, verb or surface wait in IMAGINE.md and move out, never copied.** rule, adopt. Why: A parallel library becomes a second description. (practice.imagine-is-waiting-room)
- **Every PM ask is filed as an Issue with area and milestone; only launch blockers jump the line.** rule, adopt. Why: Asks acted on from chat get lost. (practice.intake-files-not-acts)
- **Issues, branches and commits use fixed names that carry the scenario or Issue number.** rule, adopt. Why: git finds everything. (practice.issue-and-commit-naming)
- **Don's model.md says what the product is; product docs that disagree are fixed that session.** rule, adopt. Why: Docs drift without one authority. (practice.model-md-is-authority)
- **A scenario marks its native platform needs, or [platform none]; store views are generated.** rule, adopt. Why: Hand-kept inventories would drift. (practice.platform-marker)
- **A scenario spec is at most 40 lines of Story, Acceptance and Not this; more is two scenarios.** rule, adopt. Why: A spec must fit in one head. (practice.scenario-spec-40-lines)
- **Scenario state is frontmatter, ticket state an Issue label; no bridge document.** rule, adopt. Why: A bridge doc went wrong. (practice.state-in-frontmatter-and-labels)
- **Every scenario from F103 on answers six value questions in its Why.** rule, adopt. Why: Should it exist here at all? (practice.value-test)
- **Work waits on conditions with parts, so part of a capability can unlock part of the work.** rule, trial. Why: A single blocker hid which piece was actually ready. (practice.conditions-with-parts)
- **A scenario changed after 2026-11-11 names its concept in frontmatter.** rule, trial. Why: Links it to the idea it grew from. (practice.scenario-names-concept)
- **An Issue is a hypothesis: a loop may end by saying the Issue is wrong.** guideline, trial. Why: Agents otherwise guess confidently. (practice.issue-is-hypothesis)
- **Features are ranked now, next, later with no dates; version plans change with a why.** guideline, trial. Why: Dates become false promises. (practice.now-next-later-no-dates)

## How we build

- **Build agents use per-persona builder accounts that never count in numbers, seed the app daily, and one switch hides or deletes their content.** rule, adopt. Why: Agents must see every view as a persona. (practice.builder-accounts)
- **A PR that differs from its scenario stops and asks for a scenario change first.** rule, adopt. Why: Otherwise it ships what was not approved. (practice.divergence-stops-and-asks)
- **If a rule would slow a deadline, tell the PM which one before breaking it.** rule, adopt. Why: A silent break hides a trade-off the PM owns. (practice.flag-before-breaking-rule)
- **A test discharging a criterion carries a guards marker naming the criterion; covered means one check claims all of it.** rule, adopt. Why: An unmarked scenario is unverified, not verified. (practice.guards-marker-coverage)
- **On the Mac at most 4 builds at once, 4 Playwright workers, one dev port each, Docker Desktop only; cloud sessions are not capped.** rule, adopt, for now. Why: One machine is shared. (practice.mac-build-limits)
- **Worktrees are removed the day their branch merges, at most 10 per repo, with a weekly disk sweep.** rule, adopt, for now. Why: Stale worktrees filled the disk. (practice.mac-disk-hygiene)
- **Links between nouns live in code with their ruled date, updated in the ruling's PR.** rule, adopt. Why: Relationships lived implicitly in foreign keys, and a hand document called REGISTRY died. (practice.ontology-in-code)
- **Every PR states how it was verified; unverified work is a draft; shipped means something calls it.** rule, adopt. Why: A security PR passed only on a laptop and could not say so. (practice.pr-states-how-verified)
- **Push once when ready, not per commit, and keep PR stacks at most two deep.** rule, adopt. Why: Every push runs CI. (practice.push-once-when-ready)
- **Tests come first: a failing test per criterion, and a failing regression test for every bug.** rule, adopt. Why: A test that never failed proves nothing. (practice.tests-first-red)
- **Verify against a row a handler created from a form, not against seed data.** rule, adopt. Why: Seeds look right while member rows break (bug #175). (practice.verify-on-handler-rows)
- **Each session works in its own worktree beside the repo and reads status without taking the lock.** rule, adopt. Why: Sessions at the root wedged index.lock. (practice.worktree-per-session)
- **One build session takes one Issue from ticket to merge and ends with its PR.** guideline, trial. Why: Lanes existed only to share one machine. (practice.one-loop-per-issue)

## How we review

- **Builder journeys run end to end in CI; a halt or new friction is a finding.** rule, adopt. Why: Unit tests miss whole flows. (practice.journeys-in-ci)
- **Whoever does the work merges it on green; the PM is held only for what he must judge.** rule, adopt. Why: Waiting on him parks finished work. (practice.merge-on-green-self)
- **A PR changing what the reviewer checks needs the PM's pm-approved label; bookkeeping merges.** rule, adopt. Why: The review must not loosen itself. (practice.meta-change-needs-pm-approved)
- **The PM never reads code; he looks at the live app after merge, only for words, look, scope or trade-offs.** rule, adopt. Why: Agents own correct; the PM owns right. (practice.pm-looks-at-running-app)
- **Every PR opens with 'Don doesn't need to look' and why, or three phone steps and human-review.** rule, adopt. Why: The PM reads from a phone and has not read the ticket. (practice.pr-opens-look-or-not)
- **The reviewer fixes rule violations in at most two loops; only judgement calls reach the PM.** rule, adopt. Why: A broken rule that reaches the PM is a missed review. (practice.reviewer-checks-rules-pm-gets-judgement)
- **A UI, action or schema PR gets a GitHub review from a second session; a skipped one is labelled.** rule, adopt. Why: A gate judged by the party it constrains is waived. (practice.second-session-review)
- **Who sees what is tested in CI per resource and persona, and the test proves itself on an open policy.** rule, adopt. Why: Leaks are invisible to screen tests. (practice.visibility-matrix)
- **No screenshots per PR; the full screenshot matrix runs on demand for a UX redesign.** guideline, adopt. Why: Per-PR pictures were looked at once. (practice.screenshots-on-demand)

## How we ship

- **An accepted lint finding is one file with an owner and review-by date, and the lint fails when it lapses.** rule, adopt. Why: Accepted risks were re-argued, then forgotten. (practice.accepted-risk-expires)
- **Until the first real member signs up, agents apply migrations themselves, in order, confirming each.** rule, adopt, for now. Why: No member data at risk; it saves PM time. (practice.agents-apply-migrations-until-first-member)
- **Every change goes by branch and PR, history is never rewritten, and main deploys to production.** rule, adopt. Why: main requires its checks, and rewritten history cannot be undone. (practice.branch-and-pr-always)
- **CI gates every ready PR (lint, types, build, unit, browser, migrations); heavy suites run nightly.** rule, adopt. Why: Merges were once green with no test executing. (practice.ci-gates-every-pr)
- **Each deploy checks the database connection, and a failed main build opens an Issue within minutes.** rule, adopt. Why: Writes were down for months unnoticed. (practice.deploy-health-check)
- **After deploy a read-only smoke opens changed screens per persona and files bugs.** rule, adopt. Why: What passed locally can fail live. (practice.live-smoke-read-only)
- **Migrations are batched and applied one at a time from a manual workflow, in order, before merge.** rule, adopt. Why: A merge ahead of its migration broke production. (practice.migrations-manual-in-order)
- **Assume no outside capital, and no new paid tool before beta unless it replaces PM time.** rule, adopt, for now. Why: Bootstrapped and member-funded. (practice.no-new-paid-tools)
- **Previews are off and only main builds; one variable switches to previews for PRs labelled human-review.** rule, adopt, for now. Why: The Hobby plan's 100 deployments a day ran out. (practice.previews-off)
- **The code repo is public: secrets only in Actions and Vercel, no pull_request_target, no personal names.** rule, adopt, for now. Why: A fork's PR must never see a secret. (practice.public-repo-secrets)
- **Nightly, a mid-range phone on 4G taps production against budgets; a red night is a bug.** rule, adopt. Why: Checks tested content, not tap time. (practice.tap-speed-budgets)
- **Member problem reports are triaged by a cheap model in Actions under a hard spend cap.** rule, trial. Why: Takes triage off the PM. (practice.bug-triage-agent)
- **Unfinished work merges dark behind our own database flags, builders first, each with a removal date.** rule, trial. Why: The flag rule had no flags behind it. (practice.flags-of-our-own)
- **Before production in 2027, a staging site with its own database takes migrations first.** rule, hold, for now. Why: Nothing is built for beta. (practice.staging-before-production)
- **Rollback is a revert merged forward or Vercel's rollback by hand, asking the PM.** guideline, adopt. Why: Auto rollback needs traffic. (practice.rollback-by-revert)
- **Re-benchmark at member checkpoints and load-test with free tools locally, never on production.** guideline, assess. Why: Production holds real members. (practice.load-sim-and-checkpoints)

## How we write

- **Rulings cover current concerns, and 'never' or 'always' carries [always] or [for now].** rule, adopt. Why: Absolute words outlive their reason. (practice.always-or-for-now)
- **Say only what is true now, no promises; 'never' only where the PM said it holds always.** rule, adopt. Why: Promises go stale and mislead members. (practice.say-only-what-is-true-now)
- **Messages to the PM are plain one-line bullets, Status first, next ask last, commands inline.** rule, adopt. Why: He reads on a phone with little time. (practice.talk-to-don-format)
- **Language is pro-competition and for all Americans, and UI labels translate durable schema names.** guideline, adopt. Why: The product's voice is part of what it is. (practice.pro-competition-language)

## How the agents run

- **A new absolute needs a dated failure a guideline missed and one of four harms.** rule, adopt. Why: Absolutes multiply: live docs held 1,650 must/never words by 2026-09. (practice.absolute-needs-four-harms)
- **The PM directs; agents do the mechanical work and open PRs with gh pr create.** rule, adopt, for now. Why: Only judgement should cost PM time. (practice.pm-directs-agents-edit)
- **Method changes go on a dated process branch, merge on green lint, and are vendored the same session.** rule, adopt. Why: Every branch needs a unique name without a central counter. (practice.process-work-dated-branch)
- **The PM rules; the planning agent never commits code; only the build agent commits code.** rule, adopt. Why: Each tier reads only its own constraints and files. (practice.roles-and-firewall)
- **A rule names the dated failure that earned it as its 'because'; no fixes for imagined failures.** rule, adopt. Why: Git carries the history. (practice.rule-carries-dated-failure)
- **A standard exists when lint or CI checks it; a rule with no hook is a wish.** rule, adopt. Why: F044 and F045 shipped unreviewed under a 'mandatory' rule. (practice.standard-exists-when-checked)
- **Dispatch messages the PM on events, not timers; handoffs run when he asks.** guideline, adopt. Why: Scheduled handoffs found little new. (practice.events-not-timers)
- **A procedure improvised once goes into a skill that same session.** guideline, adopt. Why: The next session could repeat none. (practice.improvised-procedure-becomes-skill)
- **Use a light or mid model for routine work and the top model for design, money, RLS and tricky builds.** guideline, adopt. Why: Most work is routine. (practice.match-model-to-work)
- **Prefer deleting a doc to adding a rule, and a check against code to one against a doc.** guideline, adopt. Why: Doc-to-doc gates missed real drift. (practice.prefer-delete-and-check-code)
- **A correction names a seen failure, never a model, and is retired when it stops.** guideline, trial. Why: Many models will build. (practice.correction-names-failure-not-model)
- **Hard limits live in checks or deny rules, not prose, and skills carry no 'Act as' persona lines.** guideline, trial. Why: A remembered limit can be forgotten. (practice.hard-limits-in-checks)
- **Measure the method by cost and learning: Issue to merge, pushes, PM looks, bugs, Issues rejected.** guideline, trial. Why: Line metrics miss learning. (practice.measure-cost-and-learning)
- **One regen skill lists the generator scripts; a weekly tend-docs pass is the runner.** guideline, trial. Why: Wrapper skills tended the method. (practice.one-regen-skill)
- **One loop does the work; a separate context only for independent review or exploration.** guideline, trial. Why: Routing added glue, not judgement. (practice.single-loop-separate-context)
- **Agent and PM work should be distinguishable on GitHub; the review gate returns with a reviewer identity.** guideline, assess. Why: Every agent posts as the PM. (practice.agent-identity-separate)

## How we keep docs

- **A doc that must stay current is regenerated by a workflow, committing only on change.** rule, adopt. Why: A generator whose trigger is a person remembering has no trigger. (practice.current-docs-get-workflow)
- **The PM reads generated what-and-why views, a daily phone-text dashboard with ? for missing data.** rule, adopt, for now. Why: A guess on the dashboard is a false claim. (practice.dashboard-plain-and-honest)
- **Docs hold current understanding and why within a size budget, refined weekly; history is git.** rule, adopt. Why: Docs that only grew buried what was true. (practice.doc-budgets)
- **Files and deliverables live only in the PM's repos, as markdown by PR.** rule, adopt, for now. Why: Files elsewhere are lost or leak. (practice.files-only-in-repos)
- **Feature PRs never commit generated files, and a branch behind main merges main in.** rule, adopt. Why: Avoids conflicts and stale views. (practice.generated-files-not-in-feature-prs)
- **Anything spanning the project is generated from inline markers and never hand-edited.** rule, adopt. Why: Hand-kept indexes went stale at once. (practice.generated-from-markers)
- **No hand-kept index people read for truth; a script-compared data file is fine.** rule, adopt. Why: Five hand-kept registers rotted. (practice.no-hand-maintained-indexes)
- **Everything the PM approved stays on the dashboard with its test; anything lost is shown to him.** rule, adopt. Why: Features can vanish under fast changes. (practice.nothing-gets-lost)
- **Each kind of thing has one home; with none, a dated line in UNPLACED.md, drained in 14 days.** rule, adopt. Why: Two homes become two descriptions. (practice.one-home-per-kind)
- **An unanswered question is an open-question marker where its answer lands, removed when answered.** rule, adopt. Why: One question stood in three places at once. (practice.open-question-marker)
- **A doc derived from the pitch carries [derives pitch@date]; the lint fails it once the pitch moves.** rule, adopt. Why: The pitch was copied into five docs. (practice.pitch-derived-docs)
- **A superseded ruling is deleted, and its replacement names it in a [replaces] tag.** rule, adopt. Why: Annotated docs hid which half was current. (practice.prune-with-replaces-tag)
