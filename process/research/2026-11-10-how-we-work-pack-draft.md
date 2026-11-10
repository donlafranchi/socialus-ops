# How SocialUs works: the pack (hand-built draft)

**As of 2026-11-10** · Source: socialus-ops `CLAUDE.md`, `process/PIPELINE.md`, `PIPELINE-build.md`, `DISPATCH.md`, `PERFORMANCE.md`; socialus-web `CLAUDE.md` and `.github/workflows/`; socialus-plan scenarios F121, F125 to F129 · Maintained by: hand (research note; a draft of the F128 pack, which the knowledge store will write once F128 is built; deleted at 30 days)

*For a Claude Project. It holds only what judging a tool, process or method against our way of working needs. Each line: what we do, why, how strict (absolute, rule, guideline), and its ring (adopt, trial, assess, hold). Review steps: the companion file `2026-11-10-review-a-method.md`.*

## Context that decides most answers

- One metro in beta (Northern California), beta until April 2027, a handful of builder accounts and few real members: almost no traffic.
- Bootstrapped and member-funded; no outside capital. No new paid tool before beta unless it replaces PM time.
- One PM who decides ideas, what is in each version, and words and look; he does not read code and works mostly from his phone.
- Stack: Next.js on Vercel (Hobby plan), Supabase Postgres (Pro), GitHub Actions; agents build through Claude Code sessions in the cloud.
- Many models will build over time; nothing is written for one model.

## Deciding

- **Look first, then decide.** Name 2 to 3 established precedents; a well-worn path is decided by agents, new territory goes to the PM as A/B/C with a recommendation. Why: the PM's time is the scarcest resource. Rule · adopt.
- **The PM decides only ideas, version scope, and words and look.** Agents decide everything else by the platform's soul and defaults, record it and report it. Rule · adopt.
- **Every decision is dated, carries its why, and the newer one wins.** A replaced decision is kept as retired, pointing at the newer one. Why: two live rulings in conflict stalled work before. Rule · adopt (moving into the knowledge store, F125).
- **Decisions, patterns and philosophies live in one database with history,** queried by status and area instead of read as documents. Why: hundreds of files went stale and every agent read all of them. Rule · trial (stage 1 built 2026-11-10).
- **Things wait on conditions with parts,** so part of a capability can unlock part of the work (F126). Rule · trial.

## Planning

- **A scenario is the unit of a feature:** a story, binary acceptance checks, and a six-question value test (does it already live somewhere better, do only locals know it, does it get people together, does it stay fresh, who keeps it current, does it get better as people join). Spec under 40 lines. Rule · adopt.
- **Now, next, later, ranked, no dates on features.** A version is a plan of feature slices that can change, each change with its why (F127). Guideline · trial.
- **The Issue is a hypothesis.** A build loop may end by saying the Issue is wrong. Guideline · trial.

## Building

- **One build session per Issue, ticket to merge,** in the cloud or on the Mac; no long-lived lanes. Why: lanes existed to share one machine. Guideline · trial (2026-11-02).
- **Tests first, seen failing before they pass** ([guard-proves-itself]); every check that claims a criterion says so in a marker. Rule · adopt.
- **Push once when ready; stacks at most two deep.** Why: every push runs CI and costs minutes. Guideline · adopt.
- **Verify against rows a handler created, not the seed data.** Why: seeded rows looked right while real ones broke (a Page with no URL). Rule · adopt.

## Reviewing and the PM's look

- **A second session that did not write the code reviews any UI, server action or schema change,** as a GitHub review. Rule · adopt.
- **The PM looks at the running app after merge, not at code,** and only for words, look, scope or a real trade-off; everything else merges itself on green. Rule · adopt.
- **No screenshots per PR;** the full screenshot matrix runs on demand for a redesign. Guideline · adopt.

## Shipping and operations (DevOps)

- **Merge to main deploys to production on Vercel.** Previews are off to save build minutes. Rule · adopt.
- **CI gates every PR:** lint, types and build; unit tests; browser journeys; the visibility matrix (who sees what); migrations from scratch; no undocumented migrations. Rule · adopt.
- **Database migrations are applied by a person, one at a time, from a manual GitHub Action** that refuses a branch stacked on unmerged work, before the PR merges. Why: two migrations applied outside the migration files once left production and the files out of step. Rule · adopt.
- **After deploy:** a database-connection check on every deploy (written after every write was down for four months unnoticed), an alarm when a main build fails, a nightly read-only smoke test of what changed, and a nightly tap-speed test against budgets on a mid-range phone on 4G. A failure files an Issue. Rule · adopt.
- **Rollback is a revert merged forward, or Vercel's instant rollback by hand;** nothing rolls back on its own. Guideline · adopt.
- **"Unfinished work hides behind a flag"** is stated, but there is no flag system in the code: unfinished work is held back by not merging. Rule as written · not enforced (a gap).
- **Every change goes by branch and PR; history is never rewritten.** Absolute.

## Words

- **Say only what we must; no promises about the future;** state what is true now. "Never" only where the PM said it and it holds always. Rule · adopt.
- **The PM owns every word a member reads;** agents draft, the PM looks live. Rule · adopt.

## Agents and the method itself

- **One agent loop does the work; a separate context only for independent review or parallel exploration** (the single-agent-loop kit). Guideline · trial.
- **A rule carries its dated failure as its "because";** a rule with no failure behind it is not added. Rule · adopt.
- **A standard exists when a check enforces it,** not when a document says it. Rule · adopt.
- **A correction names a failure seen in agents' work, never which model made it,** and is retired when the failure stops. Guideline · trial.
- **Measure the method by cost and by learning:** Issue to merge time, pushes after first CI, PM looks, bugs per merged PR, and Issues rejected as wrong. Guideline · trial.
- **Known gap:** every agent acts on GitHub as the PM, so agent work and PM work can't be told apart there. Assess.
