# Experiment: how to schedule the pipeline for an area batch

*(The PM, 2026-10-06.)* Three ways of running `PIPELINE-build.md` for one area batch, one mode per batch, measured the same way. An experiment, not a ruling: nothing here changes the method until the PM rules on the result.

## The three modes

1. **Day.** Every check, the heavy ones included, runs on every push.
2. **Day/night split.** Quick checks per push (build, tests, lint, the capture bundle and quick reviewer pass for the changed screens); the heavy checks run overnight on schedule (`PIPELINE-build.md` § Day and night).
3. **Straight through.** One lane runs the whole pipeline end to end for its batch as soon as the build is green, heavy checks included, without waiting for night.

## Assignment

| Next area batch | Mode | Why this pairing |
|---|---|---|
| Page-editing finish (#412, #413, #423, #410) | **2 Day/night split** | The largest and most UI-heavy batch, so it shows whether the split keeps the day light without delaying review. |
| Builders & seed (#388, #353) | **3 Straight through** | Two items, mostly data and operator pages: few screens, so running everything at once is cheap and shows the fastest possible path. |
| Sharing & links (#409, #411, #422) | **1 Day** | Small and shallow, so running every heavy check on every push costs the least here and still shows what mode 1 spends. |

**Caveat.** The batches differ in size and in how much UI they carry, so this is a comparison with confounds, not a controlled test. Read each measure per item, and note any batch that was unusual. A second round can rotate the modes across the next three batches.

## The measures

| Measure | How it is taken |
|---|---|
| **Hours to ready** | First commit on the batch's first branch to the moment the dashboard shows the batch "ready for PM review" (steps 1–14 passed). Wall clock, minus any time the batch waited on the PM. |
| **Actions minutes** | Sum of billable job minutes for the batch's PRs and the nightly runs that covered it (`gh run list`, `gh api repos/…/actions/runs/<id>/timing`). Free on the public repo, still counted, because the plan may change. |
| **Mac load** | Hours the 2 build slots were busy for the batch (builds, local test runs), from the lane's own start and stop times. |
| **Caught before the PM** | Findings from tests, CI, reviewers and the live smoke that were fixed before the PM saw it, counted once each. |
| **Found by the PM** | Problems the PM raised in his live review of the batch (filed as Issues, labelled `found-by-pm`), each noted with the step that should have caught it. |

The last two give the miss rate: found by the PM ÷ (caught before + found by the PM).

## The log

Each lane copies this into its PR body at handoff and appends a row per event to the table below in the same file's PR (or the batch's Issue). Times are PT.

```
Batch:            <area batch>            Mode: <1|2|3>
First commit:     <time>                  Ready for PM review: <time>   Hours: <n>
Actions minutes:  <n>   (PRs <n>, nightly <n>)
Mac load:         <n> h of build-slot time
Caught before the PM: <n>   (by: tests <n>, CI <n>, reviewers <n>, smoke <n>, nightly <n>)
Found by the PM:  <n>   (Issues: #…, with the step that should have caught each)
Notes:            <anything unusual: a blocker, a flaky check, a lane that waited>
```

| Date | Batch | Mode | Event | Time | Note |
|---|---|---|---|---|---|
| | | | | | |

## Reading the result

After the three batches and the PM's live reviews, compare per item: hours to ready, minutes, Mac load and the miss rate. Prefer the mode with the shortest hours to ready among those whose miss rate is not worse; Actions minutes and Mac load break ties. The PM rules; the recommendation and the numbers go in a dated section at the end of this file.
