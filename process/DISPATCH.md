# Working with the PM through Dispatch

**As of 2026-11-02** · Source: hand-written · Maintained by: hand (set by tend-docs from the last commit date; the owner confirms on next edit)

*(the PM, 2026-10-06.)* Dispatch is the PM's phone-side agent. Its memory has been wiped before, so what it must do lives here, and memory is only a cache. These add to § Working with the PM in `PIPELINE.md`; nothing here repeats it.

1. **Modes.** The PM types **"phone"** or **"computer"**. In phone mode there are no desktop approvals and no terminal: pause anything that needs them, and still do merges, messages, reading and migrations. A migration from the phone: GitHub iOS app → Actions → apply → Run workflow → pick the branch → type `apply`. In computer mode, everything.
2. **Copy-paste goes inline.** Prompts, handoffs and commands go in the message as one code block, never in a file or an artifact. Each terminal command gets its own block. Prefer commands that report status, such as `gh run watch --exit-status`.
3. **Migrations.** Until the first real (non-builder) member signs up, agents apply them themselves with `gh workflow run apply.yml -R donlafranchi/socialus-web --ref <branch> -f confirm=apply`, strictly in order, confirming each in the database before the next and stopping on failure (the exception under `[production-asks-don]`, 2026-10-06). From then on the PM applies each one by branch name: give that command and the iOS steps from item 1.
4. **Reuse sessions.** Every new session or folder on the Mac costs the PM an approval prompt, so reuse an existing one there; a cloud session costs none. A Code session ends with its PR; nothing carries over.
5. **Folders.** Design files go in `~/Projects/socialus-design`; briefs and files in the repo they're about, never outside the repos (Don, 2026-11-01); repos keep the `socialus-*` naming.
6. **Deliverables are markdown, by PR,** in the right `socialus-*` repo. Never a Docs or Design artifact.
7. **Name the work, not its number.** Never refer to work by a ticket or Issue number alone: say what it is, the number in brackets.
8. **Scheduled runs.** The daily seed (3am), the monthly notifications review and the Sunday 8am disk cleanup. The 5am/5pm handoff and the 9pm merge pass were retired on 2026-10-27 *(the PM)*: a handoff runs when the PM asks ("catch me up"), and agents merge on green themselves. Dispatch messages the PM on events, not on timers.
9. **A weekly tidy of long agent-facing lists** (`PRINCIPLES.md`, `STATUS.md` and the like), sorted by topic and then newest first, when that helps agents decide. Superseded items stay out of the live file (`[newer-decision-wins]`) and history lives in git through `[replaces]` tags. There is no separate history file for the PM.

## Intake and the Code loop

*(the PM, 2026-10-06; lanes and shifts folded 2026-11-02, single-loop rewrite variant rewrite-1.)*

- **Every PM ask is filed, not acted on:** a `socialus-web` Issue labelled `area:<name>` and milestoned "Beta 10-30" or "After beta". Dispatch replies with one line: "Filed: <area> · <milestone> · Nth in that area". Only launch blockers and production breakage jump the line.
- **Areas:** `page-editing`, `sign-in-you`, `explore-map`, `create-posts`, `sharing-links`, `builders-seed`, `moderation`, `ops`. An area is a label for finding things, not a lane.
- **One Code loop per Issue** (`build-ticket`): a session, cloud or Mac, takes one Issue from ticket to merge, woken by the Issue or its PR's events or started by Dispatch, and ends with the PR. No area partition, no shifts, no handoff notes: the area lanes of 2026-10-06 partitioned work so three sessions could share one machine, and a cloud session shares nothing. Builds on the Mac still obey `PIPELINE.md` § Build rules. Small edits ship as their own loop; nothing is held for a batch.
- **The Issue is a hypothesis.** A loop may end by saying the Issue is wrong, on the Issue, instead of building it.
- **Research tangents** go to a separate research task and come back as one-at-a-time decisions (the PM queue).
- **The beta dashboard** is two outputs of one script (`scripts/dashboard.py` in the planning repo, reading `socialus-web` Issues and PRs), regenerated daily by `dashboard.yml` and on request: `DASHBOARD.md` in plain text, no colour (the PM reads it in the GitHub iOS app) and `dashboard/index.html` (self-contained, the only place with colour). Never a Claude artifact. A stage with no data shows `?`, not a guess. Under each area it logs the last day: PRs merged and opened, Issues filed and closed, migrations in merged PRs, decisions dated that day (`--since Nh` changes the window), so the PM catches up in one place per area without reading the PRs *(the PM, 2026-10-07)*.
