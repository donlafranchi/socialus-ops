# Review: LaunchDarkly against how we work

**As of 2026-11-10** · Source: launchdarkly.com/docs (home, the docs index, Releasing features, Guarded rollouts, Flag lifecycle settings, MCP server), read 2026-11-10; the pack draft of the same date · Maintained by: hand (research note, the first test of the F128 review steps; deleted at 30 days)

**Bottom line: LaunchDarkly's core idea, releasing separately from deploying behind a flag, is one we already claim and don't do. Its paid strengths (guarded rollouts with automatic rollback, experiments) need traffic and money we don't have yet. Worth taking: the release-behind-a-flag practice and flag cleanup, built small on our own stack.**

| # | LaunchDarkly practice | Against the pack |
|---|---|---|
| 1 | Release separately from deploy, behind feature flags | **Gap.** "Unfinished work hides behind a flag" is our stated rule, with no flag system behind it |
| 2 | Percentage rollouts to a fixed share of users | **Hold for now.** One metro, few members: a share of almost nobody |
| 3 | Progressive rollouts that raise the share automatically | **Hold for now,** same reason |
| 4 | Guarded rollouts: watch metrics, roll back automatically on a regression | **Opposite, for now.** We detect after deploy (deploy check, nightly smoke and speed) and roll back by hand; theirs needs an Enterprise plan with an add-on and enough traffic for statistics |
| 5 | Experiments comparing variations on metrics | **We do a small version on purpose:** shelf rotation with a weekly scoreboard (F121), because bandits need traffic we don't have |
| 6 | Prerequisite flags (one flag waits on another) | **We do this, wider:** conditions with parts gate decisions and features, not just code (F126) |
| 7 | Flag lifecycle: temporary flags, ready-to-remove and ready-to-archive checks | **Gap if we adopt flags;** matches our for-now review queue in spirit |
| 8 | Code references: find every flag in the code | **Gap if we adopt flags** |
| 9 | Approvals and release policies before a change goes live | **We do this:** the PM's look on human-review work and the manual migration apply |
| 10 | Change history and restoring an earlier flag version | **We do this** through git and the knowledge store's history |
| 11 | Observability: errors, logs, traces, session replay, alerts | **Partly:** deploy check, build alarm, nightly smoke and speed; no error tracking in place (a branch for it exists) |
| 12 | Versioned AI configs and prompts with evaluations and judges (AgentControl) | **Partly:** skills in git and a moderation eval; no evaluation per prompt change. Assess, if the product's own AI grows |
| 13 | An MCP server and an agent that manage flags in plain language | **Fits** our agents-first way of working |
| 14 | Pricing | Guarded rollouts need Enterprise plus the Guardian add-on (docs say so); other tiers not read. **Clashes** with "no new paid tool before beta unless it replaces PM time" |

## Recommendation

- **A. Make our flag rule real, small and on our own stack (recommended):** a few flags held in our database, on for builder accounts first, so unfinished work can merge dark and the PM sees it live before members do; each flag marked temporary and listed for removal. Trade-off: one build session; no rollout percentages or automatic rollback.
- **B. LaunchDarkly for flags only, on whatever tier fits:** a full flag interface and MCP tools at once. Trade-off: a new vendor and a bill before beta; the parts we'd value most later are Enterprise-only.
- **C. Nothing now:** keep holding unfinished work by not merging. Trade-off: the stated rule stays untrue, and big features wait on long-lived branches.

**How A would be measured:** time from a feature's first merge to the PM's first live look, and PRs labelled human-review that wait unmerged, before and after.

## What this review did not cover

LaunchDarkly's pricing page and free tier were not read. Vercel's own flag product was not compared, and it may be the cheaper path for option A. The pack had no line on traffic numbers or plan limits; the context block now carries them, and the F128 pack should too.
