> **SETTLED — do not re-raise:** members are the investors and the only people paid out. "Ownership, not profit-share" is rejected. Legal/securities questions about this go to `socialus-legal` for counsel and never come back to the PM as a decision. SocialUs takes transaction income; any 'no fee' language is retired.

# Process absolutes

How work is done, for any project run on this method. Each project keeps its
member-facing absolutes in its own `product/ABSOLUTES.md` (SocialUs:
`socialus-plan/product/ABSOLUTES.md`); the test below governs both files.

**The test.** A rule is absolute only if breaking it once causes harm the next
session can't undo. Four kinds of harm qualify: harm to a member, loss or
exposure of production data, a public act that can't be unpublished, a decision
made without Don. Everything not on these two pages is a guideline — break it
when justified and say why in the PR or the scenario. The test exists because
absolutes multiply on their own: by 2026-09 live docs held 1,650 must/never
words, each reasonable alone, and agents obeyed the wording, not the intent.

**Cite an absolute by its slug in brackets — `[production-asks-don]`, never
"rule 3".** Numbers renumber and citations to them rot silently; slugs do not.
`scripts/lint.sh` fails on any bracketed slug in the repo with no matching `###`
heading in one of these two files, so a rename breaks the build instead of
leaving a pointer that reads fine and means nothing.

## Production

### production-asks-don

Anything that reaches production or can't be undone — deploy to main,
destructive migration, deleting data, rewriting history — asks Don first.

**Time-boxed exception (2026-10-06, the PM).** Until SocialUs has live users,
agents apply migrations themselves via the apply workflow, strictly in order,
confirming each in the database before the next and stopping on failure.
Because there is no real member data at risk and hand-applying cost the PM
time. **It ends the day the first real (non-builder) member signs up;** from
then on, migrations ask the PM first again. Only migrations are covered:
deploys to main, deleting data and rewriting history still ask.

## Public

### public-is-draft

Anything public — user-facing copy, a published page, a claim about what the app
does — is a draft until Don says otherwise.

## Authority

### don-decides

The PM decides ideas, what is in each version, and words and look-and-feel; a
reversal of a prior ruling in any of those goes to the PM as options with a
recommendation. Everything else agents decide by the soul and defaults, record,
and report (`process/PIPELINE.md` § Decision rights, 2026-10-25); new territory
that conflicts with the soul goes to the PM.

### ruling-is-dated-line

A ruling exists only as one dated line: a principle in `PRINCIPLES.md`, or under
`## Rulings` in the doc it governs. The code says how; rulings say why; a doc that disagrees with either is the thing
that's wrong. Record it at the scope the PM gave: a wider reading is labelled
as a reading, because "the other side is patron", internal shorthand, was
recorded as a user-facing rule that retired four others (2026-09-14).

## Verification

### guard-proves-itself

**A check may not be relied on until it has been observed rejecting input that
should be rejected.** Until then it is inert, and an inert guard counts as
absent — not as weak, as *absent*. Green is not evidence: every guard below was
green throughout.

**What relying on it means:** citing it as the reason something is safe, letting
it gate a merge, or writing it into `CLAUDE.md` as a thing agents watch for.

**What discharges it.** A guard ships with a case that *makes it fail*, run by
the same job that runs the guard — a known-bad fixture the check must reject, so
the failure path executes on every run and not only on the day it matters. Where
that is genuinely impossible, the PR links a run where the guard actually
failed. **No link and no failing fixture means the guard is not yet a guard**,
and nothing may be built on it.

**The dated failures, all within two days, which is what makes this a category
rather than three bugs** *(2026-09-19 to 2026-09-21)*:

- **The migration preflight parser** never worked in CI at all. `supabase
  migration list` renders markdown when stdout is not a TTY, so every cell
  arrived backtick-wrapped and the parser required bare digits. It failed
  closed, correctly, every time — and **the first migration it ever guarded is
  the one it blocked.** Above it sat a green test asserting the script's *text*
  contained the right strings.
- **`migrations (check)`** was broken by an unpinned Supabase CLI. **Its absence
  is what let a merge land ahead of its migration and take production down on
  2026-09-21.**
- **`issue-lint`** could not match the `**Kind:**` its own template emits, and
  its labelling call returned 403, so **the `needs-fix` label agents were told
  to watch for was never once applied.**

**Which harm:** harm to a member, and production data. The 2026-09-21 outage is
the dated failure — members could not use the product, and no later session can
undo downtime that already happened. **A guideline did not prevent it**: the
first two instances were each written up as a lesson, and the third happened
anyway. Describing a pattern accurately does not stop it; a failing fixture in
the same job does.

## Adding an absolute

The count is a result, not a cap. A new absolute needs a dated failure that a guideline
demonstrably didn't prevent, and must name which of the four harms it falls
under. If it can't, it's a guideline. Prefer a precise permission to a broad
ban, because "Code never writes to the planning repo" broke the first session
it was tested and was replaced by "Code may open a PR there" (2026-09-09). Give it a slug, file it in whichever of the
two pages it belongs to, and cite it by that slug from its first use.
