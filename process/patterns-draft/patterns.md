# Patterns

**Short names Don can say instead of explaining himself.** When he names one ("that's well-worn", "one at a time", "agent vs human"), the agent applies it in full without asking what he meant. Each pattern is one line on what it does and why, then folded details: when it applies, what the agent does, and Don's own words.

**Proposed home:** `~/.claude/templates/patterns.md`, read by every agent in every project. Project-only patterns live in that project's `CLAUDE.md`.

## Deciding

**`well-worn` — find what established platforms do, pick the simplest fit, and decide without the PM; only new territory goes to him.** The PM's time is the scarcest resource.

<details><summary>Details</summary>

- **When:** any design, product or process choice.
- **Do:** name 2–3 precedents with links; pick the most relevant and elegant one. Clear pattern → build it, label `Path: well-worn`, list the precedents, tell the PM what was chosen. No clear pattern, conflicting precedents, or it touches a ruling, legal, privacy, money or member trust → `Path: new territory`, one A/B/C with a recommendation, before building. Unsure → say which in one line and lean toward deciding.
- **Don:** "I want to lessen the amount of time that I get in the way." "What seems the most elegant? Do that." (2026-10-04)

</details>

**`adapt, don't adopt` — a pattern built for human teams is a starting point, never a template; keep what still solves a problem and rebuild the rest for agents.** Most precedents predate agents and assume people who forget, can't rewrite cheaply and read top to bottom.

<details><summary>Details</summary>

- **When:** a precedent from `well-worn` was designed for people: Diátaxis, ADR logs, changelogs, handbooks, sprint rituals, approval chains, wikis.
- **Do:** state in one line what problem it solved for humans. Keep the part that still applies. Drop what agents make cheap (rewriting, regenerating, searching). Add what agents need: one home per fact, machine checks, size budgets, a stated why. Write it as "adapted from X: kept …, dropped …, added …".
- **Don:** "Diátaxis is pre-agent", so adapt it: keep only the what-and-why vs how split, keep it minimal (2026-10-12).

</details>

**`no speculative rulings` — rule only on what binds current work; prune the rest instead of asking.** Hypothetical decisions cost the PM time and age badly.

<details><summary>Details</summary>

- **When:** a doc or plan holds a decision about something not yet built or near.
- **Do:** delete it or move it to the ideas list. Never send it to the PM as A/B/C.
- **Don:** "I don't want to rule on things that aren't yet a concern." (2026-09-30)

</details>

**`[always]/[for now]` — every never / won't / always ruling carries one of two fixed tags.** Agents kept treating a one-version call as permanent and blocked later ideas with it.

<details><summary>Details</summary>

- **Do:** `[always]` = every version. `[for now]` = this version, reviewed in one pass at each release planning. Any condition goes in the sentence ("for now, until the entity forms"); no version names. When citing a ruling, say its scope. Unknown scope → mark it; never assume `[always]`.
- **Don:** "the no distance anywhere was a version decision not a global decision… any decision that has a never or won't needs a global or version or other clarifier." (2026-10-12)
- **Replaces** the 2026-09-30 wording rule ("currently…", the only allowed never is "never extractive"). See contradictions in the draft README.

</details>

**`newer wins` — when two recorded rulings conflict, the newer one holds and work continues.** Asking the PM to re-pick between his own rulings is the failure the record exists to stop.

<details><summary>Details</summary>

- **Do:** follow the newer ruling and update or delete the older one in the same change. Exception: when what the PM says in chat contradicts a recorded ruling, show him the record and confirm the change in one line, because chat may be a misremembering, not a new call.

</details>

## Working with the PM

**`one at a time` — bring the PM exactly one item per message: the next one.** He works fastest one by one.

<details><summary>Details</summary>

- **Do:** one decision (A/B/C + recommendation, one-line trade-offs) or one page to review (link + 3 phone steps). Hold the rest. "Next" = unblocks the most agent work soonest; nearest deadline breaks ties. Status may show counts ("3 more queued") and asks nothing.
- **Don:** "I work much faster when we go one by one… ensure it is the next thing and not just something that needs to be done before soft launch." (2026-10-05)

</details>

**`record every ruling` — the moment the PM decides, write it where it governs; search that record before asking him anything.** Chat is not a record; unrecorded calls came back to him as open questions.

<details><summary>Details</summary>

- **Do:** after each call, a comment on its Issue/PR and the ruling inline in the doc it governs. Before any question, search Issues, PRs and the rulings. Found → use it (see `newer wins`).
- **Don:** "we went over all of these, how did they not get recorded?" (2026-10-11)

</details>

**`save open threads` — during any back-and-forth, save his words, where we got to and the next step after each substantive message.** Chat can reset and lose hours.

<details><summary>Details</summary>

- **Do:** update a memory or state note as you go, quoting him verbatim where wording matters. Briefs to other sessions quote him verbatim. On restart, rebuild from memory and GitHub before asking anything.
- **Why:** 2026-10-12, a reset lost 5–8am of discussion and he had to start over.

</details>

**`do the mechanical work` — anything that needs no judgement, do it with the tools at hand and report it.** Handing him instructions spends his time on what a tool could do.

<details><summary>Details</summary>

- **Do:** merges of approved or green PRs, env vars, Issues, labels, reruns, migrations while allowed. Before writing "run this", check whether a tool can.
- **Don:** "why aren't you automatically doing everything that doesn't require human judgement." (2026-10-04)

</details>

**`Don directs, agents edit` — he says what to change; agents change it.** He does not edit files.

<details><summary>Details</summary>

- **Do:** never ask him to edit, paste into a file or "edit freely". Ask what he wants changed, then do it.
- **Don:** "I don't edit anything. I tell you what to edit and how." (2026-10-05)

</details>

**`say it once` — name a real cost or collision once, plainly, then do what he asked.** Repeated pushback reads as resisting everything.

<details><summary>Details</summary>

- **Do:** one line on what it displaces or risks, no framing devices (deadlines, freezes, past rulings) used as a lever. Then build.
- **Why:** 2026-10-08 he rejected a freeze-based pushback with "nope".

</details>

## Talking to the PM

**`three-line report` — Status / Next / "Want detail? Say expand."** Facts that don't change his next move stay out.

<details><summary>Details</summary>

- **Do:** `Status: Done | Blocked | Question — one sentence.` `Next: the ask, or none.` Then the offer. No hashes, file lists or step traces until "expand"; expand goes ask → outcomes → references → notes. Name things in plain words, an ID in brackets only if it matters. End on the next action, not a recap.

</details>

**`copy-paste inline` — anything he will copy goes in the message as one fenced block.** Never a file or artifact for a copy job.

<details><summary>Details</summary>

- **Don:** "give me the handoff here to copy and never produce an artifact for a copy paste job." (2026-10-05)

</details>

**`phone` / `computer` — his one-word mode switch.** Don't hand him what he can't do from where he is.

<details><summary>Details</summary>

- **`phone` (and office days):** no desktop approvals, no terminal. Queue anything needing those; say so in one line. Phone-safe: merges, messages to running sessions, reading, links to review, GitHub iOS steps by branch name.
- **`computer`:** everything, including starting sessions and terminal commands.

</details>

## Running the work

**`no manual prompts` — tool-heavy work goes only to sessions that skip permission prompts.** Approvals stall work while he's away.

<details><summary>Details</summary>

- **Do:** route research and multi-tool work to an existing bypass Code session. Pure-chat work only in chats that may prompt. Reuse a running session within the day; start fresh ones at the start of the day in `computer` mode. Never assume a session's permission mode.
- **Don:** "I never want anything to be manual." "You're really pissing me off by requesting permissions again and again." (2026-10-09, 2026-10-01)

</details>

**`cheapest that works` — the least costly model, tool and plan that does the job; flag any new recurring cost first.** He is on a shoestring budget.

<details><summary>Details</summary>

- **Do:** always pass a model: Haiku for status, Sonnet for routine and docs, Opus for design and tricky builds; Fable only if he names it. No new paid tool unless it replaces his time. At most 2 builds at once; serialize browser and build work, parallelize network and model work.

</details>

**`verified or not` — every "done" names the check that ran, and a new check is first seen failing.** A claim is worth what the check behind it was worth.

<details><summary>Details</summary>

- **Do:** one line per PR: live DB, local DB, unit tests only, or not verified. Unverified → draft PR naming the missing check.

</details>

**`earn the rule` — a process change names the dated failure that earned it.** Rules without a failure accumulate and nobody knows which to drop.

<details><summary>Details</summary>

- **Do:** the rule's "because" line holds the date and what went wrong. No failure, no rule.

</details>

## Building the product

**`runs unattended` — design every flow to run while the PM is away (Tue–Thu); batch his items for Fri–Mon; prefer one global switch over item-by-item controls.** He runs this alone beside a day job.

<details><summary>Details</summary>

- **Do:** flag any design that adds recurring operator work. Item-level handling only for real members' content.
- **Don:** "highly highly critical" (2026-10-05).

</details>

**`self-correct first` — push a problem back to the person who can fix it before any staff work; escalate only on a repeat or a legal/safety must-have.** Don't take on work one person can't keep up with.

<details><summary>Details</summary>

- **Do:** notice → fix → retry; staff only on repeat. Safety floor still hides at once.
- **Don:** "I am one person with a day job and want to push back most issues to let people self correct before I have to do work. That's a standing rule until I get help." (2026-10-11) `[for now]`

</details>

**`nothing gets lost` — everything the PM approved stays visible with its test, and anything that disappears or loses its test is shown to him.** Agents change a lot fast; this is how a feature can't vanish quietly.

<details><summary>Details</summary>

- **Do:** a generated "lost since last look" list on the dashboard, diffed from approved criteria and tests.

</details>

**`Now/Next/Considering/Later` — four fixed roadmap lanes that never change.** He wants to see settled next steps apart from possibilities.

<details><summary>Details</summary>

- **Now:** being built. **Next:** settled and approved. **Considering:** possible, not approved. **Later:** eventual. An idea not yet ruled on can only be Considering or Later. Generated from the plan, never hand-ordered.

</details>

## Docs

**`agent vs human` — decide the reader before writing: the PM gets what and why; agents get how.** Never one doc for both.

<details><summary>Details</summary>

- **Do:** PM docs follow the `PM doc` pattern and are generated snapshots; agent docs follow the `agent doc` pattern and are maintained. A message or brief to the PM is a PM doc.
- **Don:** "I need to know what we do and why, not how, that is for agents." (2026-10-12)

</details>

**`fewest docs` — never propose a new hand-kept doc; each kind of thing has one home.** The decisions log hit 267k characters and agents re-asked settled questions.

<details><summary>Details</summary>

- **Do:** route by the project's where-things-go map. Every maintained doc has a size budget; past 80%, condense it in the same change. Human docs are generated, never hand-kept. A junk drawer is fine only if every item has a way out.

</details>

**`current + why` — agent docs say what is true now and why, never the history.** Git is the history.

<details><summary>Details</summary>

- **Do:** reword in place; delete superseded text; no dated logs, changelogs or "previously" notes. Push back on any brief that appends history instead of refining.
- **Don:** "No long history lists: only current understanding and the rationale for why." (2026-10-12)

</details>

### `PM doc` — summary first, a mental model, skippable detail

**Built so a PM can scan one phone screen and leave with a working picture: what it is, how the parts fit, what changed, and the one thing asked of him.**

<details><summary>Details</summary>

Precedents, and what we change:

| Precedent | Kept | Changed for agent-led work |
|---|---|---|
| [BLUF](https://en.wikipedia.org/wiki/BLUF_(communication)) / [inverted pyramid](https://en.wikipedia.org/wiki/Inverted_pyramid_(journalism)) | Conclusion first, every section | Also the first line of every section, not just the doc |
| [Minto pyramid](https://www.barbaraminto.com/) | Answer, then the few supporting groups | The groups become "the picture": the 3–5 parts and how they connect, so he builds a mental model, not a reading list |
| [Progressive disclosure](https://www.nngroup.com/articles/progressive-disclosure/), GitHub [collapsed sections](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections) | Detail folded until needed | All folds closed must fit about one phone screen |
| [README vs AGENTS.md](https://agents.md) | People and agents read different files | The PM file is generated from the agent files, never hand-kept |
| [Diátaxis](https://diataxis.fr) (pre-agent) | Only the "explanation vs how-to" split | No quadrants, no tutorials; the how lives only in agent docs |
| Pre-agent status reports and changelogs | "What changed" | A generated diff since his last look, not a log |

Rules: plain words, IDs in brackets; no scripts, paths or commands; one ask at most, at the end, as A/B/C or yes/no with a recommendation.

```
# <Name>

**<Bottom line: what this is and why it matters, 1–2 bold lines.>**

**Your call:** <one yes/no or A/B/C with a recommendation — or "none">

## The picture
**<The 3–5 parts and how they connect, one bold line.>**
<details><summary>Details</summary> <one line per part; a small diagram if it helps> </details>

## What changed since you last looked
**<The one change that matters most.>**
<details><summary>Details</summary> <the rest, newest first; anything lost, flagged> </details>

## <Topic>
**<What we do and why, 1–3 lines, key phrase bold.>**
<details><summary>Details</summary> <only what he may want to look up> </details>
```

</details>

### `agent doc` — one home per fact, current state plus why, checkable

**Built so an agent can find the rule, act on it, and prove it, without asking anyone what the doc meant.**

<details><summary>Details</summary>

Precedents, and what we change:

| Precedent | Kept | Changed |
|---|---|---|
| [AGENTS.md](https://agents.md), [Claude Code memory](https://docs.anthropic.com/en/docs/claude-code/memory) | One instruction file per repo, short, specific, imperative | Points to the routing map instead of holding tables |
| [ADR](https://adr.github.io) | Decision + context + consequences | No numbered log: the decision lives inline where it governs and is replaced in place |
| Diátaxis how-to / reference | Task steps and lookup tables | Every rule carries its "because" (the failure), its inputs, outputs and check |
| Docs-as-code | Docs in git, reviewed in PRs | Size budgets, lints, and a refine pass instead of human gardeners |

Rules: one home per fact (link, never restate); current understanding plus the why, no history; a size budget, condensed at 80%; ruling tags `[always]`/`[for now]`; open questions as inline markers with owner and date; every pass/fail criterion binary.

```
# <Name>
<One line: what this doc is the single home for.> Budget: <n>k.

## <Task or rule>
<The rule, one imperative line.> Because: <the dated failure it prevents>.
- Inputs: <what it reads> · Outputs: <what it writes> · Check: <test or lint that proves it>
- <Steps or reference, only as long as needed.>

## Rulings
- **<date> — <ruling>.** [always|for now] [binds …]
```

</details>
