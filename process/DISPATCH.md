# Working with the PM through Dispatch

*(the PM, 2026-10-06.)* Dispatch is the PM's phone-side agent. Its memory has been wiped before, so what it must do lives here, and memory is only a cache. These add to § Working with the PM in `PIPELINE.md`; nothing here repeats it.

1. **Modes.** The PM types **"phone"** or **"computer"**. In phone mode there are no desktop approvals and no terminal: pause anything that needs them, and still do merges, messages, reading and migrations. A migration from the phone: GitHub iOS app → Actions → apply → Run workflow → pick the branch → type `apply`. In computer mode, everything.
2. **Copy-paste goes inline.** Prompts, handoffs and commands go in the message as one code block, never in a file or an artifact. Each terminal command gets its own block. Prefer commands that report status, such as `gh run watch --exit-status`.
3. **Migrations are named by branch.** Give the command `gh workflow run apply.yml -R donlafranchi/socialus-web --ref <branch> -f confirm=apply` and the iOS steps from item 1. Order and confirmation are in § Working with the PM.
4. **Reuse sessions.** Every new session or folder costs the PM an approval prompt, so reuse an existing one. One Code session holds a folder, so parallel lanes go in different repo folders. Start fresh Code sessions daily, on a cheaper model for routine lanes.
5. **Folders.** Design files go in `~/Projects/socialus-design`; files with no home yet in `~/Projects/agent-temp`; repos keep the `socialus-*` naming.
6. **Deliverables are markdown, by PR,** in the right `socialus-*` repo. Never a Docs or Design artifact.
7. **Name the work, not its number.** Never refer to work by a ticket or Issue number alone: say what it is, the number in brackets.
8. **Scheduled runs.** 5am handoff, 9pm overnight queue, Sunday 8am disk cleanup. Dispatch messages the PM on events, not on timers.
9. **A weekly tidy of long agent-facing lists** (`DECISIONS.md`, `STATUS.md`, `LESSONS.md` and the like), sorted by topic and then newest first, when that helps agents decide. Superseded items stay out of the live file (`[newer-decision-wins]`) and history lives in git through `[replaces]` tags. There is no separate history file for the PM.
