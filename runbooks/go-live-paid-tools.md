# Go-live: paid tools review (a prompt)

**As of 2026-11-10** · Source: the LaunchDarkly review and the how-we-work pack draft of 2026-11-10 (socialus-ops `process/research/`, deleted at 30 days; git keeps them) · Maintained by: hand. Fires from the socialus-plan launch checklist at production launch.

*Paste the block below into a Claude Project, or a Claude Code session with the four repos, once the production launch date is set. It is written to be run as is; nothing in it is a price or a plan limit to trust, because those change.*

```
You are reviewing paid tools for SocialUs at go-live. Use the how-we-work
pack and the "review a method" steps in this project (or, in a session,
the knowledge store and socialus-ops process/). Follow the decision rule:
2 to 3 precedents, then A/B/C with a recommendation.

WHAT CHANGED SINCE BETA
- Beta rule: no new paid tool unless it replaced PM time. At go-live the
  PM will pay for services that help the platform perform as well as it
  can (the PM, 2026-11-10).
- Planned upgrades: Vercel from Hobby to a paid plan; possibly GitHub to a
  paid plan, so builds, previews and Actions minutes stop limiting how
  often we ship.
- Look up, don't assume: members and daily traffic now, how many metros,
  and the current Vercel, Supabase and GitHub plans and their limits.

WHAT THE BETA REVIEW FOUND (2026-11-10, LaunchDarkly docs)
- Their core idea, release separately from deploy behind a flag, was a rule
  we stated and did not do. Look up what we chose (own flags, LaunchDarkly,
  or nothing) and how it has gone.
- Held for traffic: percentage and progressive rollouts; guarded rollouts
  that watch metrics and roll back on their own (Enterprise plan plus an
  add-on, per their docs); experiments (we ran a small weekly scoreboard
  instead).
- Already ours, wider: prerequisites (conditions with parts), approvals
  (the PM's live look, manual migration apply), change history (git and the
  knowledge store).
- Gaps: flag cleanup and finding every flag in the code; error tracking;
  no evaluation per prompt change for the product's own AI.
- Not read then: LaunchDarkly's pricing and free tier; Vercel's own flags
  and rollout features.

DO THIS
1. Read the current pricing and plan pages for: LaunchDarkly; Vercel's paid
   plan (flags, rolling releases, previews, observability, firewall); and
   1 or 2 alternatives that cover the same gaps (flags, error tracking,
   session replay). Date every page you read.
2. For each gap and each held practice above, say whether go-live traffic
   and budget now make it worth doing, and which tool does it at what
   monthly cost.
3. Check what a Vercel upgrade alone already gives us before adding a
   vendor; one bill beats two when the cheaper one covers the need.
4. Say what a GitHub upgrade changes for our Actions and branch rules, and
   whether we need it at launch or can wait.

ANSWER IN THIS SHAPE
- One bold bottom line.
- A table: practice or gap | tool | monthly cost | do now, later, or never.
- A, B, C with one-line trade-offs and a monthly total each; recommend one.
- How the recommendation would be measured, before and after.
- What you did not read.
Bullets, one line each, plain words, no em dashes.
```
