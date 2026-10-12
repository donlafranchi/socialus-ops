# Don's patterns: draft

**A library of 25 short pattern names, so Don can say "well-worn" or "one at a time" instead of explaining himself, plus two doc patterns: one for the PM and one for agents.** It was built from all 35 Dispatch memories, the global and repo instructions, and the method docs.

**Your call:** apply the global changes, yes or no? *Recommend yes.* Yes means: `patterns.md` becomes `~/.claude/templates/patterns.md`, `CLAUDE.global.md` replaces `~/.claude/CLAUDE.md` (the diff is `global.diff`), and you paste `app-preferences.md` into the Claude app yourself. Nothing global has changed yet.

## The picture

**Four files: the library, the global instructions that point to it, a short app profile, and this summary.**

<details><summary>Details</summary>

- **`patterns.md`:** each pattern is a bold line (what and why), then folded detail: when, what to do, Don's words. It ends with the two doc patterns and their skeletons.
- **`CLAUDE.global.md`:** today's global file plus a one-line-per-pattern list (so every session sees the names), a short Docs section, and a corrected repo table.
- **`app-preferences.md`:** the same names, short enough to paste into the app profile.
- **`global.diff`:** what changes in the global file, line by line.

</details>

## What the patterns are

**Six groups: deciding, working with the PM, talking to him, running the work, building the product, and docs.**

<details><summary>Details</summary>

- **Deciding:** well-worn · adapt, don't adopt · no speculative rulings · [always]/[for now] · newer wins
- **Working with the PM:** one at a time · record every ruling · save open threads · do the mechanical work · Don directs, agents edit · say it once
- **Talking to him:** three-line report · copy-paste inline · phone / computer
- **Running the work:** no manual prompts · cheapest that works · verified or not · earn the rule
- **Building the product:** runs unattended · self-correct first · nothing gets lost · Now/Next/Considering/Later
- **Docs:** agent vs human · fewest docs · current + why · `PM doc` · `agent doc`

Merged: "reuse sessions" and "fresh sessions daily" became one rule in *no manual prompts* (reuse within the day, start fresh each morning). "Search before asking" and "quote Don verbatim" folded into *record every ruling* and *save open threads*. "A/B/C with a recommendation" lives inside *well-worn* and *one at a time*.

</details>

## The two doc patterns

**`PM doc`: a bold bottom line, your one call, the picture (the 3–5 parts and how they fit), what changed since you last looked, then folded detail.** **`agent doc`: one home per fact, what's true now plus why, a size budget, a check that proves it.**

<details><summary>Details</summary>

- **What's new for agent-led work, on the PM side:** the picture section exists for your mental model, not a reading list; PM docs are generated from agent docs, never hand-kept; "what changed" is a diff, not a log; all folds closed fit about one phone screen.
- **Agent side:** decision records live inline where they govern and are replaced in place (no numbered log); every rule carries the failure that earned it; budgets and a weekly refine pass replace human gardening.
- **Precedents:** BLUF, inverted pyramid, Minto pyramid, progressive disclosure, README vs AGENTS.md, Diátaxis (pre-agent, adapted), ADRs, docs-as-code. Links and skeletons are in `patterns.md`.

</details>

## Contradictions found

**Three real conflicts; the newer ruling wins in each, and one leaves a stale lint behind.**

<details><summary>Details</summary>

1. **"The only allowed never is never extractive" (2026-09-30) vs [always]/[for now] (2026-10-12).** The principles file already uses "never" a dozen times with tags. The newer tag rule wins. The old "never" lint (`scripts/never.py`, off by default, 117 hits) and the wording line in the pipeline doc are stale; retiring them is a follow-up method change after your yes.
2. **"Newer ruling wins, don't ask" vs "show the recorded ruling and confirm."** Both stand: newer wins between two recorded rulings; a one-line confirm only when what you say in chat contradicts the record.
3. **"Reuse sessions" vs "start sessions fresh daily."** Reuse within the day, fresh each morning in computer mode.

</details>

## SocialUs only, and stale

**Kept out of the global library: rules that are about SocialUs or expire on a date.** They stay in SocialUs's own instructions and memory.

<details><summary>Details</summary>

- **SocialUs only:** members are the investors (settled); data serves members, easy opt-out; member-to-member privacy strict, staff open; every business Page gets photos, labeled sample posts, working links; Find and Discover; legal work only in socialus-legal, no personal name in repos; SocialUs work lives in its repos, never Claude artifacts; Launch Coach is people-time only; build rules (Docker Desktop, 2 builds); the value test for scenarios.
- **Dated or time-boxed:** no freeze reminders until 2026-10-23; agents apply migrations until the first real member (then Don applies by branch from GitHub iOS); previews off until 10-23; the Dispatch state snapshot of 10-11.
- **Stale references fixed in the proposed global file:** the repo table named `ops-pattern` (now `socialus-ops`), said plan wasn't pushed yet, and had no `socialus-legal` row. The pipeline doc still points at `DECISIONS.md`, now `PRINCIPLES.md`: a follow-up.

</details>
