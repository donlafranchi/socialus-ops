# Bug triage from members, and mutation testing: what we found and what we would do

*Research note, 2026-10-06 (the PM). Not a ruling and not built: nothing here changes the method until the PM rules. Facts about Vercel, Anthropic's dedupe bot and Sentry are as reported to the PM that day and were not re-checked here.*

## 1. Vercel's agent offerings do not fit our plan

- **"eve"** is an open-source agent framework from Vercel, a library we would host and run ourselves, not a service that triages bugs for us.
- **Vercel Agent** (their hosted code-review and investigation agent) needs the Pro plan. We are on Hobby, and Pro is a separate cost question (the previews ruling already says to revisit Pro before production).
- Neither fits Hobby, so neither is the answer for now.

## 2. Recommended member bug-report pipeline

A member's report becomes a fixed bug with the PM seeing only what needs a human.

1. **In-app "Report a problem."** One control, reachable from every screen.
2. **Full report to a private Supabase table.** The whole report, including who sent it and what they typed, stays here, readable by the operator only. Nothing from this table is public.
3. **A scrubbed public Issue** in `socialus-web`, opened from the report: route, role (not who), build SHA, browser, scrubbed console errors, and the report ID that links back to the private row. No member data. It carries the Kind, Scenario and Path lines that `issue-lint` requires.
4. **A Claude Code GitHub Action** reads the new Issue: labels `area:*`, sets the milestone, and checks for duplicates. It runs a **heartbeat check**, because Anthropic's own dedupe bot silently stopped working for two months without anyone noticing: if the Action has not run for a day, something posts to the PM queue.
5. **Reproduce.** The Action writes a failing Playwright test for the report ([guard-proves-itself]: the test is seen failing before any fix).
6. **Draft a fix PR** against that test.
7. **Only `human-review` reaches the PM** (the label that replaced `needs-don`), per the decision rule: judgement calls, new copy, new territory. Everything else merges on green.

Privacy is the load-bearing part: the public Issue must never carry member data, so step 3 is a scrub with its own test, and the private table is the only place the full report lives.

## 3. Sentry as an option

Sentry's free tier covers about 5,000 errors a month and includes a user-feedback widget, which could stand in for step 1 and add error capture for free. Its AI fixer, Seer, costs about $40 a month and is **skipped**. This sits beside the pipeline above as an option; the choice between the in-app control and Sentry's widget is the PM's.

## 4. Mutation testing

Stryker is already configured (`stryker.config.mjs`, `npm run mutate`) and not scheduled anywhere. The plan:

- **Nightly incremental run** (see `PIPELINE-build.md` § Day and night) on the critical slice only: auth, admin and hidden-for, the reports queue, reason codes, safe-next, signup policy, and the visibility helpers.
- **Report-only for a week**, to see the baseline score and the noise.
- **Then break the build below 60%.** Raise the bar only when the score supports it.
- **First fix five stale tests (T069).** They make the baseline meaningless, so they go before the schedule starts.

## What is not decided

Whether to build the pipeline at all before beta, whether to use Sentry's widget, and the threshold after the first week. Each goes to the PM one at a time when it is the next thing blocking work.
