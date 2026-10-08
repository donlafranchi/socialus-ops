# Performance — the method

How a product keeps itself fast with a PM who does not read code (Don, 2026-10-08: "I want this as a system"). Nothing here belongs to one product; SocialUs is the first. Its pieces live in `socialus-web` (`evals/speed/`, `src/lib/speed/`, `.github/workflows/smoke-live.yml`).

## What "fast" means

A **tap** is timed three ways, on a mid-range phone (4x CPU slowdown) over 4G, from inside the page:

- **Feedback**: the first visible change after the tap.
- **URL change**: the address changes (the card moves but the page does not = feedback with no URL change, called a *stall*).
- **Content**: the new screen's main content is visible and usable.

Budgets, per screen, in `evals/speed/budgets.json`. Consumer: feedback 100 ms, content 1 s. Creator and editing: feedback 250 ms, content 2.5 s (they have more patience for their own pages).

## The layers

| Layer | What | How often | Where it runs | Cost |
|---|---|---|---|---|
| Unit guards | the verdict rules, budgets match the screens, a Page does not download the map library | every PR | CI, with the unit tests | none extra |
| Tap speed | every consumer tap, then creator taps, on production, read-only | nightly, after the live smoke; on demand from the Actions tab | `smoke-live` job (shares its install) | about 10 min |
| Re-benchmark | the tap suite and the load simulation, baseline re-recorded | when membership passes 100, 500, 1,000, 5,000 | on demand | a few runs |
| Load simulation | many people on one Page at once (phase 2, below) | before each checkpoint and before any launch push | local Docker stack, never production | free tools |

## Verdicts

Each tap reads 🟢, 🟠 or 🔴 (`src/lib/speed/verdict.ts`):

- 🔴 a consumer screen over budget with no filed issue; any screen more than 20% (and more than 50 ms) slower than its baseline; a stall; a screen that never shows; a tap with no feedback; a tap that could not be run.
- 🟠 over budget with an issue filed (`issue` in `baseline.json`), or a creator screen over budget. Seen, not shouting.
- 🟢 otherwise.

A red reading is measured twice more and the middle one is used, so one bad run is not a finding. Over-budget with no issue is red on purpose: a new slow screen cannot hide.

**Baseline** is `evals/speed/baseline.json`; `baseline-source.json` says where it was recorded. A baseline from a laptop only warns (the runner is a different machine). After the first nightly run, `npx tsx evals/speed/rebaseline.ts <that run's rows.jsonl>` records the CI baseline and turns the 20% rule on. Re-baseline the same way after a fix lands, when the summary lists screens "faster than baseline", and at each membership checkpoint (add the number to `checkpoints.json`).

## Where results go

- **Run page**: the table and the slowest ten, in the job summary.
- **History**: one JSON per night on the `perf-history` branch of the code repo (`history/YYYY-MM-DD.json`), not on `main`, so no deploy. `latest.json` there is the dashboard's feed: `red` is true only when a consumer screen is over budget or a tap could not be run; it also carries the slowest five and `rebenchmarkDue`.
- **Dashboard** reads `latest.json` and shows the slowest screens, the trend, and red only on `red`.
- **Issue**: on a red night the job opens (or comments on) `bug · live: taps are slower than budget`.

## Who acts

Agents. A red night is a bug: the next shift's fix loop picks up the issue, diagnoses from the table (requests, waterfall depth, long tasks, whether the route was prefetched, the slowest request and its cache and region), fixes or files the cause, and re-baselines. **Don is told about red only** (the dashboard, or a message from dispatch); amber and green are never a message. A change that makes a screen slower on purpose (a richer Page) is Don's call, as any trade-off is.

## Load simulation (phase 2)

Question Don asked: what happens when many people use the same Page at once, and what breaks first?

- **Tool**: k6 (free, open source, one binary, thresholds that fail a run). No paid tools. Playwright stays for browser-level timing under load (a handful of real browsers while k6 holds the crowd).
- **Target**: the local stack on Docker Desktop (Supabase and a production build of the app, seeded), never production. Production Supabase is on the free plan with rate limits and holds real members.
- **Scenarios**: 50, 200 and 1,000 concurrent viewers of one Page (signed out, then signed in); a burst of taps on the blue dot; a burst of reports. Ramp up, hold, ramp down.
- **Where it breaks first**: watch four things during each run and name the first to saturate: database (pg_stat_activity, slow queries, lock waits), connections (pool exhaustion), cold starts (first-hit versus warm latency in the server), rendering (CPU of the app process, response time under load).
- **Honest limit**: a laptop is not Vercel or Supabase's hosted tier. The run shows which layer saturates first and by how much, not production's absolute ceiling; the hosted plans' own limits (concurrent functions, database connections) are read from their docs and compared with the numbers.
- **Light production check**: at most 10 viewers for 60 seconds on two read-only addresses, outside busy hours; never the burst scenarios.
- **Output**: a short table per scenario (requests per second, p50 and p95, errors, first layer to break) saved as a check-in with the checkpoint, so the numbers can be compared at 100, 500, 1,000 and 5,000 members.

## Why it is built this way

The first tap-speed run on 2026-10-08 found the bug Don described within minutes: opening a Page took 2.2 s and the address only changed at 2.2 s, because the Page had no loading screen and every visitor downloaded a 480 KB map library through the owner's composer. Nothing in the existing checks could have seen it: they test what a screen shows, not how long a tap takes.
