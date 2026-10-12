# PM and agents: who needs what

**The PM reads what we do and why; agents read how.** Keeping the two apart lets the PM steer without wading through mechanics, and lets agents work without re-asking the PM what a page meant.

<details><summary>Details</summary>

The split borrows four patterns, each adapted for agent-led work:

- **README for people, AGENTS.md for agents** ([agents.md](https://agents.md)). Our `CLAUDE.md` files play the AGENTS.md role. **No AGENTS.md symlink for now:** only Claude Code agents work here, and the repos avoid symlinks so a Windows machine needs no special setup (`socialus-plan/process/SETUP.md`). If another agent tool joins, rename each `CLAUDE.md` to `AGENTS.md` and leave a one-line `CLAUDE.md` that imports it (`@AGENTS.md`, [Claude Code memory](https://docs.anthropic.com/en/docs/claude-code/memory)).
- **Diátaxis, adapted (pre-agent)** ([diataxis.fr](https://diataxis.fr), written for human readers from about 2017). We keep only its split: PM docs explain what and why; agent docs hold the how-to and the reference. No quadrants, no tutorials.
- **Bottom line up front** ([BLUF](https://en.wikipedia.org/wiki/BLUF_(communication)), [inverted pyramid](https://en.wikipedia.org/wiki/Inverted_pyramid_(journalism))). Every section opens with its conclusion.
- **Progressive disclosure** ([NN/g](https://www.nngroup.com/articles/progressive-disclosure/)), using GitHub's [collapsed sections](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections): detail is folded away until someone needs it.

</details>

## The one safety view: nothing gets lost

**Everything the PM approved stays on the dashboard with its test, and anything that disappears or loses its test is shown to the PM.** Agents change a lot of code fast. This is how a feature can't quietly vanish under them.

<details><summary>Details</summary>

- **Criterion roll-up:** every approved scenario's pass/fail criteria are scored as built, checked by a test, reviewed, smoked and looked at by the PM.
- **Nothing closes half-built:** an Issue that closes with an unmet criterion is counted and flagged (the gap-leakage score, the pipeline health alarms).
- **Lost since last look:** each dashboard compares its criteria with the last one and lists any criterion that left, stopped being built, or lost its test.
- **A deleted scenario can't take its rulings with it:** the lint blocks it until they move to the product doc.

</details>

## Who reads what

**One concern, two views: a generated what-and-why for the PM, and one agent home per role for the how.**

<details><summary>Details</summary>

| Concern | PM view (generated) | Product | Planner | Council | Ticket-writer | Builder | Reviewer | Ops | Kept current by |
|---|---|---|---|---|---|---|---|---|---|
| Why we exist | Charter | `PRINCIPLES.md` | `PRINCIPLES.md` | `PRINCIPLES.md` | — | constraints | constraints | — | PM rules; planner rewords |
| What we build | dashboard: where we're going | spine (`product/`) | scenarios | feature brief | scenario criteria | Issue + constraints | Issue + criteria | — | planner; sync-roadmap |
| Rulings | dashboard decisions; `[for now]` review list | spine `## Rulings` | scenario `## Rulings` | constraints | constraints | `constraints/code.md` | `constraints/code.md` | `process/PIPELINE.md` `## Rulings` | the agent who records the ruling |
| Is it working | dashboard: where we are, lost since last look | — | criterion reports | — | — | tests (`[guards]`) | review, storyboard | scores | roll-up scripts |
| How it looks and reads | app storyboard | voice-and-tone | scenario criteria | brief | — | code strings | storyboard | — | PM approves copy |
| Safety | safety runbook | moderation doc | moderation scenarios | — | — | code + tests | review | runbook generator | rulings drive the generator |
| How we work | ops README | — | `CLAUDE.md` | `council-roles.md` | `write-tickets` | `CLAUDE.md`, `PIPELINE-build.md` | `review-pr-bundle` | `process/` | ops agent; weekly refine pass |
| Where things go | ops README | `WHERE-THINGS-GO.md` | same | same | same | same | same | same | ops agent |

</details>

## Skeletons

**PM docs open each section with the what and why; agent docs open with what to do.**

<details><summary>Details</summary>

PM view, every section:

```
## <Section>

**<Key phrase: what we do and why, one or two plain lines.>** <One line on why agents need it: what goes wrong without it.>

<details><summary>Details</summary>

<Only what the PM may need to look up. No scripts, paths or commands.>

</details>
```

Agent doc, every section:

```
## <Task or rule>

<The rule, one line, imperative.> <Because: the failure it prevents.>

- Inputs: <files it reads>  · Outputs: <files it writes>  · Check: <the test or lint that proves it>
- <Steps or reference, only as long as needed.>
```

</details>
