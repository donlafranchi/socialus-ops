> **SETTLED — do not re-raise:** members are the investors and the only people paid out. "Ownership, not profit-share" is rejected. Legal/securities questions about this go to `socialus-legal` for counsel and never come back to the PM as a decision. SocialUs takes transaction income; any 'no fee' language is retired.

# ops-pattern — the method

How agents build a product with a PM who rules and does not read code. **This repo holds the method only; nothing here belongs to one product.** Which folder holds what: `~/.claude/CLAUDE.md` § The repos.

SocialUs is the first project run on it. Its planning repo is `socialus-plan`, its code `socialus-web`, its design `socialus-design`. The examples and dated failures below are SocialUs's because that is where the method was learned; the rules are not.

## Decision rule

Every agent, every decision. Word for word from Don; how it lands in this method is `process/PIPELINE.md` § Decision rule.

```
DECISION RULE (2026-10-04, Don)
1. Look first: before designing or deciding anything, find what established platforms do for this exact use case. Name 2–3 precedents with links (e.g. Google, Apple HIG, Airbnb, Meetup, Yelp, Stripe, Linear).
2. Choose: pick the most relevant and elegant option for SocialUs, the simplest one that fits our rulings.
3. Well-worn path: if a clear, established pattern exists, decide and build it yourself. Label the Issue/PR "Path: well-worn", list the precedents, and don't wait for the PM.
4. New territory: if there's no well-worn path, the precedents conflict, or it touches a ruling, legal or privacy exposure, money, or member trust, label it "Path: new territory" and bring it to the PM as A/B/C with a recommendation before building.
5. When unsure which it is, say which in one line and lean toward deciding: the PM's time is the scarcest resource.
```

## What is here

- `process/ABSOLUTES.md` — the process absolutes and the four-harms test that admits any absolute, process or product. A project keeps its member-facing absolutes in its own `product/ABSOLUTES.md`.
- `process/council-roles.md` — the roles, lens and word limits for a council (parallel cheap-model members, one strong chair) that puts an A/B/C to the PM.
- `process/PIPELINE.md` — the five kinds of work (scenario, change, bug, process, chore), who checks what, open questions, accepted risk.
- `process/PERFORMANCE.md` — how a product keeps itself fast: tap-speed budgets, nightly runs, baselines and checkpoints, the load simulation, who acts on red.
- `process/LIVING-DOCS.md` — facts inline, cross-cutting views generated from markers, authored docs pruned, git as the archive. Every marker kind and the failure it answers.
- `process/WHERE-THINGS-GO.md` — one table: each kind of thing, its one home, owner, how it stays current, what never goes there. Read every session; each project's `CLAUDE.md` points here.
- `scripts/` — the marker checker, lints and generated-view tooling. `scripts/lint.sh` runs here too: the project checks find nothing to check, and the fixtures still prove every checker ([guard-proves-itself]).
- `templates/` — a scenario and a decision line, in the grammar the lint enforces.

**Paths in `process/` that name `DECISIONS.md`, `STATUS.md`, `ROADMAP.md`, `IMAGINE.md`, `planning/`, `product/`, `constraints/` or `accepted-risks/` mean the project's planning repo**, not this one.

## Roles

| Who | Owns | Never |
|---|---|---|
| The PM (SocialUs: Don) | rulings, judgment on whether something is *right*, domain facts | reads code |
| Cowork — planning agent | the project's planning repo: scenarios, rulings, roadmap, the product model | commits code |
| Code — build agent and architect | the code repo: architecture notes, Issues, TDD code, PRs, self-merge when green | writes scenarios or rulings |

Agents own whether a change is correct; the PM owns whether it is right (`process/PIPELINE.md` § Who checks what). Each tier reads only its own `constraints/<tier>.md` and the files its role names; that is the firewall.

## Starting a project on it

1. A planning repo and a code repo, both with remotes, both pushed.
2. Copy `scripts/`, `.github/workflows/lint.yml` and `templates/` into the planning repo. The copy is vendored: a change to how a marker or lint works is made here first, then copied.
3. The planning repo's `CLAUDE.md` points back here for the absolutes and the pipeline, and at `~/.claude/CLAUDE.md` for the folder map. Its lint finds this repo as a sibling checkout (`METHOD_REPO` overrides).

## Changing the method

Process work: branch `process-YYYY-MM-DD-slug`, commit `docs: what`, PR, self-merge when `lint` is green, then copy any changed script into each project that vendors it. Sessions work in their own worktree at `../worktrees/ops-pattern/{branch}`, never the repo root, because a worktree rule scoped to branches left read-only sessions at the root to wedge each other's `index.lock` (2026-09-09). Use `git --no-optional-locks status` when not committing: plain `status` takes the lock, and a sandboxed session leaves it stale.

- **Name the failure, with a dated example, and put it in the rule as its short "because …".** No fixes for imagined failures. There is no lessons file: the rule carries its reason and git carries the history.
- **Prefer deleting a doc to adding a rule.** Prefer a frontmatter field to a directory, because state held in kanban folders needed the PM at the Mac to move files. Prefer a check against code to a check against a doc, because every early gate compared docs to docs and two Explore tickets were built after Explore was retired (2026-09-03).
- **A standard exists when lint or CI checks it**, not before (`process/LIVING-DOCS.md` § Hooks).
- **A procedure improvised once goes into a skill that session**, because the 2026-09-09 session improvised five (classifying work, splitting a scenario, folding reviews) and the next could repeat none.
