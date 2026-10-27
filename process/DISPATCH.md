# Working with the PM through Dispatch

**As of 2026-10-07** · Source: hand-written · Maintained by: hand (set by tend-docs from the last commit date; the owner confirms on next edit)

*(the PM, 2026-10-06.)* Dispatch is the PM's phone-side agent. Its memory has been wiped before, so what it must do lives here, and memory is only a cache. These add to § Working with the PM in `PIPELINE.md`; nothing here repeats it.

1. **Modes.** The PM types **"phone"** or **"computer"**. In phone mode there are no desktop approvals and no terminal: pause anything that needs them, and still do merges, messages, reading and migrations. A migration from the phone: GitHub iOS app → Actions → apply → Run workflow → pick the branch → type `apply`. In computer mode, everything.
2. **Copy-paste goes inline.** Prompts, handoffs and commands go in the message as one code block, never in a file or an artifact. Each terminal command gets its own block. Prefer commands that report status, such as `gh run watch --exit-status`.
3. **Migrations.** Until the first real (non-builder) member signs up, agents apply them themselves with `gh workflow run apply.yml -R donlafranchi/socialus-web --ref <branch> -f confirm=apply`, strictly in order, confirming each in the database before the next and stopping on failure (the exception under `[production-asks-don]`, 2026-10-06). From then on the PM applies each one by branch name: give that command and the iOS steps from item 1.
4. **Reuse sessions.** Every new session or folder costs the PM an approval prompt, so reuse an existing one. One Code session holds a folder, so parallel lanes go in different repo folders. Start fresh Code sessions daily, on a cheaper model for routine lanes.
5. **Folders.** Design files go in `~/Projects/socialus-design`; files with no home yet in `~/Projects/agent-temp`; repos keep the `socialus-*` naming.
6. **Deliverables are markdown, by PR,** in the right `socialus-*` repo. Never a Docs or Design artifact.
7. **Name the work, not its number.** Never refer to work by a ticket or Issue number alone: say what it is, the number in brackets.
8. **Scheduled runs.** The daily seed (3am), the monthly notifications review and the Sunday 8am disk cleanup. The 5am/5pm handoff and the 9pm merge pass were retired on 2026-10-27 *(the PM)*: a handoff runs when the PM asks ("catch me up"), and agents merge on green themselves. Dispatch messages the PM on events, not on timers.
9. **A weekly tidy of long agent-facing lists** (`PRINCIPLES.md`, `STATUS.md` and the like), sorted by topic and then newest first, when that helps agents decide. Superseded items stay out of the live file (`[newer-decision-wins]`) and history lives in git through `[replaces]` tags. There is no separate history file for the PM.

## Intake and area lanes

*(the PM, 2026-10-06.)*

- **Every PM ask is filed, not acted on:** a `socialus-web` Issue labelled `area:<name>` and milestoned "Beta 10-30" or "After beta". Dispatch replies with one line: "Filed: <area> · <milestone> · Nth in that area". Only launch blockers and production breakage jump the line.
- **Areas:** `page-editing`, `sign-in-you`, `explore-map`, `create-posts`, `sharing-links`, `builders-seed`, `moderation`, `ops`.
- **Area lanes.** One Code session per area, each in its own permanent worktree folder (`~/Projects/worktrees/area-<name>`), at most 3 at once, sharing the 2-build limit (§ Build rules). Areas that touch the same screens don't run together. Each lane batches its area into one PR (or a stack of at most 2), and the PM reviews the area once, live.
- **Small edits are held** until an area has enough for a substantial lane (about half a shift of work), unless a beta deadline needs them sooner.
- **Shifts** are 5am–5pm and 5pm–5am. Lanes write a handoff note in their PR and stop at the handoff. Dispatch starts the next shift's lanes (each needs a desktop approval, so in phone mode the current lanes keep running). Migrations are serialized through Dispatch.
- **At each handoff** Dispatch recommends which areas get lanes, by what is furthest behind for beta, and opens with "Beta: X of Y done, Z days left, behind: <areas>".
- **Research tangents** go to a separate research task and come back as one-at-a-time decisions (the PM queue).
- **The beta dashboard** is two outputs of one script (`scripts/dashboard.py` in the planning repo, reading `socialus-web` Issues and PRs), both regenerated at each 5am and 5pm handoff and committed by PR: `DASHBOARD.md` in plain text, no colour (the PM reads it in the GitHub iOS app) and `dashboard/index.html` (self-contained, the only place with colour, opened in a browser on the Mac). Never a Claude artifact. A stage with no data shows `?`, not a guess.
- **The dashboard also logs the past shift** *(the PM, 2026-10-07)*: under each area, everything since the last handoff (12h): PRs merged and opened, Issues filed and closed, migrations in merged PRs, and decisions dated that day (`--since Nh` changes the window). It is regenerated at every 5am and 5pm handoff, and the log is how the PM catches up on a shift without reading the PRs. Because the PM wants one place per area to see what moved, not a hunt through GitHub.
- **Fresh lane sessions at each daily handoff** *(the PM, 2026-10-07)*: Dispatch starts fresh Code sessions for the day's lanes, one per area worktree folder, so the PM can set bypass permissions on each new session. The previous day's lane sessions are wrapped up first, each with a handoff note. Because fresh sessions daily is the economy rule (item 4), and permission mode is chosen per new session, so it is set once at each start.
