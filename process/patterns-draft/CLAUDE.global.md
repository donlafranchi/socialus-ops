# Global CLAUDE.md

## Decision rule — read first

For every agent, every project. Don wants agents to decide more and need him less.

```
DECISION RULE (2026-10-04, Don)
1. Look first: before designing or deciding anything, find what established platforms do for this exact use case. Name 2–3 precedents with links (e.g. Google, Apple HIG, Airbnb, Meetup, Yelp, Stripe, Linear).
2. Choose: pick the most relevant and elegant option for SocialUs, the simplest one that fits our rulings.
3. Well-worn path: if a clear, established pattern exists, decide and build it yourself. Label the Issue/PR "Path: well-worn", list the precedents, and don't wait for the PM.
4. New territory: if there's no well-worn path, the precedents conflict, or it touches a ruling, legal or privacy exposure, money, or member trust, label it "Path: new territory" and bring it to the PM as A/B/C with a recommendation before building.
5. When unsure which it is, say which in one line and lean toward deciding: the PM's time is the scarcest resource.
```

An absolute still outranks it: new user-facing copy and anything reaching production go to Don. Method detail: `~/Projects/socialus-ops/process/PIPELINE.md` § Decision rule.

## Patterns — Don names them, agents apply them

When Don says a pattern's name, apply it in full; don't ask what he meant. Full text, triggers and his words: `~/.claude/templates/patterns.md`. Read it at the start of any session that will decide, write a doc, or message Don.

- **well-worn** — precedents first; decide alone unless it's new territory (A/B/C to Don).
- **adapt, don't adopt** — a pattern built for human teams is a starting point; keep what still solves a problem, rebuild the rest for agents.
- **agent vs human** — pick the reader first: Don gets what and why (`PM doc`), agents get how (`agent doc`).
- **one at a time** — one decision or one review per message, the next one only.
- **record every ruling** — write each call where it governs; search the record before asking.
- **newer wins** — two recorded rulings conflict: the newer holds; confirm only when chat contradicts the record.
- **[always]/[for now]** — every never / won't / always ruling carries one.
- **no speculative rulings** — prune what isn't a current concern.
- **save open threads** — save his words, the state and the next step as a discussion goes.
- **do the mechanical work** · **Don directs, agents edit** · **say it once**
- **three-line report** · **copy-paste inline** · **phone / computer**
- **no manual prompts** · **cheapest that works** · **verified or not** · **earn the rule**
- **runs unattended** · **self-correct first** · **nothing gets lost** · **Now/Next/Considering/Later**
- **fewest docs** · **current + why**

## Where skills live

Skills live in **`~/Projects/skills`** — its own git repo, not inside any project repo.
`bash ~/Projects/skills/link.sh` symlinks each one into the repos that use it, under that
repo's gitignored `.claude/skills/`. `~/.claude/skills/` is deliberately empty: anything
there loads in every repo at once and defeats per-repo scoping.

To change a skill, edit it in `~/Projects/skills` and commit there. Adding one also needs
its `README.md` row, its `link.sh` entry, and a re-run of `link.sh`.

## The repos

Every repo's `CLAUDE.md` points back here. Push every repo that has a remote; never cross-commit.

| Folder (`~/Projects/…`) | Holds | Remote |
|---|---|---|
| `socialus-web` | SocialUs app code. Code agents. **Push to main deploys to production.** | pushed |
| `socialus-plan` | SocialUs principles, scenarios with their rulings, roadmap: what's next to build. Cowork. | pushed |
| `socialus-design` | SocialUs palette, screens, mockups and design research | none yet |
| `socialus-ops` | The method only: how agents build, the roles and what each can see, process absolutes, living-docs tooling, templates. Reusable for any project. (`~/Projects/ops-pattern` is an older second checkout of the same remote; work in `socialus-ops`.) | pushed |
| `socialus-legal` | Private: legal, entity, finance, tax. Never mixed into plan or ops. | pushed |
| `agent-temp` | Files with no home yet. Agents check it, move each file to where it belongs, and empty it. Untracked scratch. | none |
| `skills` | Skills, linked per repo (above) | pushed |

**Ignore `~/Projects/community`**: a retired checkout. Don't work in it, don't cite its docs.

## How projects run

The method is `socialus-ops` — start at its `CLAUDE.md`. The PM rules and judges whether a change is right; agents own whether it is correct and prove it with checks seen failing. Each project's own `CLAUDE.md` overrides anything here.

- **Tickets are Issues in the code repo**, never files. A scenario's state is its frontmatter; a shipped scenario is deleted.
- **There is no `JOURNAL.md`** and no hand-kept index. What is true now is the project's generated `STATUS.md`; why is its `PRINCIPLES.md` (principles only), and each dated ruling lives inline under `## Rulings` in the scenario or product doc it governs. Where each kind of thing goes: `socialus-ops/process/WHERE-THINGS-GO.md`.
- **Commits follow the project's naming** (SocialUs: `F060/T142: what`, `bug #36: what`, `docs: what`) and carry the `Co-Authored-By` line.

## This machine (Don's Mac)

- **Docker is Docker Desktop, never OrbStack** (Don, 2026-10-04). Before anything that needs Docker (`supabase start`, a container, a test stack), check `docker context show` prints `desktop-linux`. If it doesn't, if anything opens OrbStack, or if Docker errors: stop and tell Don. Don't switch contexts or start OrbStack yourself.
- Build, test and browser load: `socialus-ops/process/PIPELINE.md` § Build rules.

## Docs

Every doc has one reader. Don's docs (status, READMEs, briefs, messages over a few lines) use the `PM doc` pattern: bold bottom line, his one call, the picture, what changed, folded detail; no paths or commands. Agent docs use the `agent doc` pattern: one home per fact, current state plus why, a budget, a check. Both skeletons: `~/.claude/templates/patterns.md` § Docs.

## Output Style

- Keep all generated files concise — no verbose comments, no redundant documentation
- Prefer terse, self-documenting code over explanatory comments
- One-line comments only when logic isn't obvious
- No auto-generated docstrings unless explicitly requested
- Responses should be brief and direct

## Report shape

Default to a three-line report:

  Status: Done | Blocked | Question — <plain-English one-sentence summary>
  Next: <the ask, or "none" if nothing's pending>
  Want detail? Say "expand."

Rules:
- Withhold commit hashes, file lists, lane counts, item IDs, and per-step
  trace unless the user says "expand."
- Name items in plain English, not by ID. "the meta + housekeeping retirement,"
  not "reorg-04." If the ID matters, put it in parentheses after the name.
- Drop running narration. No "Now updating refs." No "Committing X." No
  "Starting BATCH B." The user follows along by reading the final report,
  not the play-by-play.
- Rule of thumb: if a fact wouldn't change the user's next move, withhold it.
- Applies to multi-step reports from build / orient / tidy / scope / review
  and to any Cowork response over ~50 words that reports completed work.
- "Expand" returns the full detail in priority order: ask → high-level
  outcomes → references → notes. Stop at each section; let the user say
  "more" to keep going.

## Safety

Never commit: `.env`, credentials, keys, tokens.
