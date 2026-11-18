> **SETTLED — do not re-raise:** SocialUs is built for the primary benefit of its members, the people who use it. Members are not investors, owners or payees, and no money return is promised; any future financial return is open, and its legal side goes to `socialus-legal` for counsel and never comes back to the PM as a decision (Don, 2026-11-18, replaces "members are the investors"). SocialUs takes transaction income; any 'no fee' language is retired.

# socialus-ops — the method

How agents build a product with a PM who rules and does not read code. This repo holds how SocialUs is built (`process/`) and how it is run (`operations/`). Its planning lives in `socialus-plan`, its code in `socialus-web`, its design in `socialus-design`.

## Where the rules are

Each rule has one home; this file points, it does not repeat.

| For | Read |
|---|---|
| How to talk to the PM, and how to decide (decision rule, decision rights, who checks what, the five kinds of work) | `process/PIPELINE.md` |
| What may never be broken, and the test for adding one | `process/ABSOLUTES.md` |
| Handling a report or incident, going live | `operations/` (the safety runbook, the go-live prompt) |
| Where each kind of thing goes, and its size budget | `process/WHERE-THINGS-GO.md` |
| How a living doc is kept current | `process/LIVING-DOCS.md` |
| What a generated file is, why it exists, who reads it, when it is still needed | the `GENERATES` block at the top of the script that writes it; `python3 scripts/generators.py check` |
| Speed, the PM's phone-side agent, councils | `process/PERFORMANCE.md`, `process/DISPATCH.md`, `process/council-roles.md` |

In those files, `PRINCIPLES.md`, `STATUS.md`, `IMAGINE.md`, `planning/`, `product/`, `constraints/` and `accepted-risks/` mean the project's planning repo.

## When to ask the store

The knowledge store is the MCP server at `socialus.org/api/knowledge/mcp` (tools: `live`, `search`, `get`, `history`, `as_of`, `precedents`, `why`, `concept`, `how`, `review_method`, `upkeep`, `propose`).

| When | Ask the store |
|---|---|
| Starting work in an area | `live` for each concern touched |
| Deciding something not covered | `precedents`, then `search`. No well-worn path means A/B/C. |
| Opening or merging a PR | `how` reviewing and `how` shipping |
| Planning, or writing a scenario or ticket | `how` planning |
| Writing or trimming docs | `how` docs |
| Two live records conflict | `get`, `history`, `why`. Build to the newer, then `propose` retiring the older with the reason so one remains. A refusal is kept as a flag for the PM. |
| "What did we decide back then", or how an idea changed | `as_of`, `concept` |
| Judging a new tool or method | `review_method` |

If the store can't be reached, say so and work from the repo docs.

## Changing the method

Branch `process-YYYY-MM-DD-slug`, commit `docs: what`, PR, self-merge when `lint` is green, then copy any changed script into each project that vendors it. To start a new project on the method, copy `scripts/`, `.github/workflows/lint.yml` and `templates/` into its planning repo.
