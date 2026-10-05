#!/usr/bin/env bash
# Writes STATUS.md. Never hand-edit STATUS.md — a hand-edit is lost on the next
# run. Re-run this, or trigger the `status` workflow.
#
# WHY THIS IS A SCRIPT AND NOT A SKILL. A skill was written for this job
# (`process/skills/status/SKILL.md`, deleted 2026-09-19) and never once ran: it
# was never installed into any `.claude/skills/`, and even installed, a skill
# only fires when somebody thinks to invoke it. The defect being fixed is
# precisely that nobody invoked it. So the judgement the skill described is
# encoded here instead, as rules the script cannot forget:
#
#   · Never invent progress. A commit naming a ticket is not proof the ticket
#     is done; `state.sh` surfaces those as *check these* and that framing is
#     carried through untouched.
#   · `status: building` in frontmatter is a claim, not evidence. Said so.
#   · Anything this run could not check goes under "What this run could not
#     verify", which is never empty by default.
#   · Open questions come from inline markers, never from the previous file.
#
# It answers *where is this project*, not *what tickets exist*. The ticket list
# is `gh issue list`, which is always right; this does not copy it in.
#
# Usage: bash scripts/status.sh [path-to-socialus-web]
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# Beta is for testing: a soft target, not a hard deadline (2026-10-05).
BETA=2026-10-30
FREEZE=2026-10-23
PRODUCTION="April–May 2027"

# Resolve the code repo. In CI it is checked out beside this one; locally it is
# usually ../socialus-web from the MAIN checkout, which is not ../ from a
# worktree — hence the candidate list rather than one hardcoded path.
CODE=""
for c in "${1:-}" "${CODE_REPO:-}" "$ROOT/../socialus-web" "$HOME/Projects/socialus-web"; do
  [ -n "$c" ] && [ -d "$c/.git" ] && CODE="$(cd "$c" && pwd)" && break
done

# Two things make the cross-repo half possible: a checkout to read, and a `gh`
# that can see a PRIVATE repo's issues. Either missing is reported, loudly and
# by name, rather than silently producing a thinner file that looks complete.
CROSS_OK=1
BLOCKED=""
if [ -z "$CODE" ]; then
  CROSS_OK=0
  BLOCKED="no \`socialus-web\` checkout was available to this run"
elif ! gh auth status >/dev/null 2>&1; then
  CROSS_OK=0
  BLOCKED="\`gh\` could not authenticate, so nothing about issues, PRs or CI could be read"
fi

STATE_OUT=""
if [ "$CROSS_OK" = 1 ]; then
  if ! STATE_OUT="$(bash scripts/state.sh "$CODE" 2>/tmp/state.err)"; then
    # state.sh exits non-zero when it has FLAGGED rows, which is not a failure.
    # It also exits 1 on a fatal guard rail, which is. Tell them apart by
    # whether it produced a document.
    if [ -z "$STATE_OUT" ]; then
      CROSS_OK=0
      BLOCKED="\`scripts/state.sh\` refused to run — $(head -1 /tmp/state.err 2>/dev/null || echo 'no reason given')"
    fi
  fi
fi

export STATUS_STATE="$STATE_OUT"
export STATUS_CROSS_OK="$CROSS_OK"
export STATUS_BLOCKED="$BLOCKED"
export STATUS_BETA="$BETA"
export STATUS_FREEZE="$FREEZE"
export STATUS_PRODUCTION="$PRODUCTION"
export STATUS_CODE="${CODE:-}"

# Composed to a temp file and moved into place, so a failed run leaves the
# previous STATUS.md intact.
TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

python3 - > "$TMP" <<'PY'
import datetime, glob, json, os, re, subprocess, sys

state   = os.environ["STATUS_STATE"]
cross   = os.environ["STATUS_CROSS_OK"] == "1"
blocked = os.environ["STATUS_BLOCKED"]
beta    = datetime.date.fromisoformat(os.environ["STATUS_BETA"])
freeze  = datetime.date.fromisoformat(os.environ["STATUS_FREEZE"])
prod    = os.environ["STATUS_PRODUCTION"]
today   = datetime.date.today()
out     = []
unverified = []

def w(s=""):
    out.append(s)

def section(name, text=state):
    """One `## ` block of state.sh's output, body only."""
    m = re.search(r"^## " + re.escape(name) + r"\s*$(.*?)(?=^## |\Z)",
                  text, re.M | re.S)
    if not m:
        return ""
    # state.sh's closing "> rows flagged above" note has no heading of its own,
    # so it lands inside whichever section is last. It is that script's sign-off,
    # not a fact about the section — drop every blockquote line.
    body = [l for l in m.group(1).splitlines() if not l.startswith(">")]
    return "\n".join(body).strip("\n")

def bullets(name):
    return [l for l in section(name).splitlines() if l.startswith("- ")]

# --------------------------------------------------------------------- header
sha = re.search(r"origin/main ([0-9a-f]+) \(([0-9-]+)\)", state)
w("# STATUS")
w()
w(f"> ## Generated {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d · %H:%M} UTC")
w(">")
w("> **Disposable. Regenerating replaces this file wholesale** — nothing here is")
w("> hand-maintained, and a hand-edit is lost on the next run. `git log -p")
w("> STATUS.md` is the history.")
w(">")
w("> **Refreshed by `.github/workflows/status.yml`** — on every push to `main`")
w("> here, daily at 13:05 UTC, and on demand from the Actions tab (*status →")
w("> Run workflow*), which works from a phone. It commits only when the content")
w("> moved, so a new revision of this file is never a bare heartbeat. Locally:")
w("> `bash scripts/status.sh`.")
w(">")
if cross and sha:
    w(f"> **Derived from:** `scripts/state.sh` against `socialus-web` @ `origin/main`")
    w(f"> `{sha.group(1)}` ({sha.group(2)}); `accepted-risks/*.json`;")
    w("> `planning/scenario-*.md` frontmatter; `ROADMAP.md`.")
else:
    w("> **Derived from this repo only** — `accepted-risks/*.json`,")
    w("> `planning/scenario-*.md` frontmatter and `ROADMAP.md`. Everything about")
    w("> the code repo is missing from this run; see the last section.")
w(">")
w("> **Answers \"where is this project\", not \"what tickets exist.\"** The ticket")
w("> list is `gh issue list`, which is always right; this is not a copy of it.")
w()
w(f"Beta **{beta:%Y-%m-%d}**, one metro — a soft target for testing, not a hard deadline. "
  f"{(beta - today).days} days out; feature freeze {freeze:%Y-%m-%d}, also soft. Production launch {prod}.")

# Headline counts from the markers, so what is unverified is a number up here and not silence below.
_code = ["--code", os.environ["STATUS_CODE"]] if os.environ.get("STATUS_CODE") else []
_cov = subprocess.run(["python3", "scripts/markers.py", "coverage", "--count"] + _code, capture_output=True, text=True)
if _cov.returncode == 0 and _cov.stdout.split():
    un, of = _cov.stdout.split()[:2]
    w()
    w(f"**{un} of {of} approved and building scenarios are unverified** — no check is marked as discharging any")
    w("of their criteria. Unmarked is unverified, not verified. § Guard coverage.")
else:
    unverified.append("**The unverified-scenario count** — `markers.py coverage --count` failed.")
_gaps = dict(l.split() for l in subprocess.run(["python3", "scripts/markers.py", "platform", "--gaps"],
                                               capture_output=True, text=True).stdout.splitlines() if l.strip())
if _gaps:
    w()
    w(f"**Native apps: {_gaps.get('ios', '?')} gaps for iOS, {_gaps.get('android', '?')} for Android** — "
      "`PLATFORM-IOS.md`, `PLATFORM-ANDROID.md`.")

# ------------------------------------------------------------------ scenarios
counts, building = {}, []
for f in sorted(glob.glob("planning/scenario-F*.md")):
    src = open(f).read()
    st = re.search(r"^status:\s*(\S+)", src, re.M)
    if not st:
        continue
    counts[st.group(1)] = counts.get(st.group(1), 0) + 1
    if st.group(1) == "building":
        ti = re.search(r"^title:\s*(.+)$", src, re.M)
        idm = re.search(r"^id:\s*(\S+)", src, re.M)
        building.append(f"{idm.group(1) if idm else '?'} ({ti.group(1).strip() if ti else '?'})")

order = [k for k in ("approved", "building", "draft", "deferred", "superseded") if k in counts]
if order:
    w()
    w("## Scenarios, by status")
    w()
    w("| " + " | ".join(order) + " |")
    w("|" + "---|" * len(order))
    w("| " + " | ".join(str(counts[k]) for k in order) + " |")
    if building:
        w()
        w("**Building:**")
        for b in building:
            w(f"- {b}")
        w()
        w("**`building` is frontmatter, not evidence** — nothing checks it against a")
        w("branch or a commit.")

# ----------------------------------------------------------- the code repo
if cross:
    openb = bullets("To build — open issues")
    blocking = [b for b in openb if "LAUNCH-BLOCKING" in b]
    w()
    w("## In the code repo")
    w()
    w(f"**{len(openb)} issues open** in `socialus-web`"
      + (f", {len(blocking)} launch-blocking:" if blocking else ", none launch-blocking."))
    for b in blocking:
        w(b.replace("  **LAUNCH-BLOCKING**", "").rstrip())

    merged = bullets("Merged in the last 14 days")
    if merged:
        w()
        w(f"**{len(merged)} PRs merged in the last fortnight.** The newest five:")
        for b in merged[:5]:
            w(b)

    check = bullets("Check these — an open issue whose ticket number appears on main")
    if check:
        w()
        w("### Needs a look — not a claim that anything is wrong")
        w()
        w("*A commit naming a ticket is not proof the ticket is done: partial work")
        w("counts. Each row needs a look, not a close.*")
        w()
        for b in check:
            w(b)

    retire = bullets("To retire — residue still on main")
    if retire:
        w()
        w("### Still on main, meant to be gone")
        w()
        for b in retire:
            w(b)

    ont = section("The ontology — what is declared")
    if ont:
        w()
        w("## The ontology — what is declared")
        w()
        w(ont)

    ci = section("What CI last said in the code repo")
    if ci:
        w()
        w("## What CI last said")
        w()
        w(ci)

    meas = section("Measured, not estimated")
    if meas:
        w()
        w("## Measured, not estimated")
        w()
        w(meas)
else:
    unverified.append(
        "**Everything about `socialus-web`** — open issues, merges, the ontology\n"
        "  registry and CI's last word. " + blocked.capitalize() + ".")

# -------------------------------------------------------------- deferred risks
# Things ruled fine ON PURPOSE, which is exactly why they get forgotten.
# risks-due.sh is silent unless something is due, and that silence is right for
# a daily job and wrong here: a deferred risk nobody is reminded of is the
# failure mode. So the whole set is named, with the due ones marked.
risks = []
for path in sorted(glob.glob("accepted-risks/*.json")):
    try:
        e = json.load(open(path))
    except Exception:
        unverified.append(f"**`{path}`** is not valid JSON and was skipped.")
        continue
    if e.get("lint") != "project_accepted_risk":
        continue          # advisor findings; machine-diffed, nobody reads them
    try:
        left = (datetime.date.fromisoformat(e["review_by"]) - today).days
    except Exception:
        left = None
    risks.append((left if left is not None else 9999, left, e))

if risks:
    risks.sort(key=lambda r: r[0])
    due = [r for r in risks if r[1] is not None and r[1] <= 21]
    w()
    w("## Deferred on purpose — and therefore easy to forget")
    w()
    w("Ruled acceptable with a condition for looking again. The ruling itself is a")
    w("dated line in `DECISIONS.md`; the register is `accepted-risks/`.")
    w()
    if due:
        w(f"**{len(due)} need a look now.**")
        w()
    for _, left, e in risks:
        if left is None:
            mark = ""
        elif left < 0:
            mark = f" — **{-left} days overdue**"
        elif left <= 21:
            mark = f" — **due in {left} days**"
        else:
            mark = f" — review by {e['review_by']}"
        w(f"- **{e['object']}**{mark}")
        if e.get("cost_if_forgotten"):
            w(f"  - If forgotten: {e['cost_if_forgotten']}")
        w(f"  - Look again if: {e['revisit_if']}")

# ------------------------------------------------------------ open questions
# Generated from inline `[open-question]` markers. Until 2026-09-27 this was a
# Waiting-on-Don list carried forward verbatim and never re-verified — a
# register, and it had gone stale. The marker's owner=don rows replace it.
code_arg = ["--code", os.environ["STATUS_CODE"]] if os.environ.get("STATUS_CODE") else []
for mode, title in (("index", "Open questions"), ("coverage", "Guard coverage"), ("building", "Is `building` backed by code?"), ("gating", "Gating launch")):
    r = subprocess.run(["python3", "scripts/markers.py", mode] + code_arg + (["--summary"] if mode == "coverage" else []),
                       capture_output=True, text=True)
    w()
    if r.returncode == 0 and r.stdout.strip():
        w(r.stdout.rstrip("\n"))
    else:
        w(f"## {title}")
        w()
        w(f"`python3 scripts/markers.py {mode}` failed this run.")
        unverified.append(f"**{title}** — the section did not generate.")

# ---------------------------------------------------------- docs by review age
# An authored doc goes stale quietly: on 2026-10-05 the member journey still
# described maker profiles four days after "no public member profile" was ruled.
# So every authored doc shows its age: frontmatter `reviewed:`, else its last
# commit (which counts any edit as a review, and says so). Precedent: GOV.UK's
# tech-docs template, `last_reviewed_on` plus `review_in`.
STALE_DAYS = 30
docs = []
for path in sorted(glob.glob("product/**/*.md", recursive=True) + glob.glob("planning/**/*.md", recursive=True)):
    head = open(path, encoding="utf-8").read(2000)
    m = re.search(r"^reviewed:\s*(\d{4}-\d{2}-\d{2})", head, re.M) if head.startswith("---") else None
    if m:
        when, how = m.group(1), "reviewed"
    else:
        r = subprocess.run(["git", "log", "-1", "--format=%cs", "--", path], capture_output=True, text=True)
        when, how = r.stdout.strip(), "last commit"
    try:
        age = (today - datetime.date.fromisoformat(when)).days
    except ValueError:
        continue
    docs.append((age, path, when, how))
if docs:
    docs.sort(reverse=True)
    old = [d for d in docs if d[0] > STALE_DAYS]
    w()
    w("## Docs by review age")
    w()
    unreviewed = sum(1 for d in docs if d[3] != "reviewed")
    w(f"{len(docs)} authored docs in `product/` and `planning/`; **{len(old)} not reviewed in {STALE_DAYS} days**, "
      f"and **{unreviewed} carry no `reviewed:` date** (their age is their last commit, which any edit resets).")
    w("Reviewing one means reading it against `DECISIONS.md` and setting `reviewed:` in its frontmatter.")
    w()
    for age, path, when, how in docs[:10]:
        w(f"- `{path}` — {age} days ({how} {when})")

# ------------------------------------------------------- could not verify
# Never empty by default. If a run really did verify everything, it says so.
w()
w("## What this run could not verify")
w()
if counts.get("draft"):
    unverified.append(
        f"**The {counts['draft']} drafts.** Status alone does not say which are waiting\n"
        "  on Don and which are simply unfinished.")
if not unverified:
    w("Nothing. Every claim above came from a source this run read.")
else:
    for u in unverified:
        w(f"- {u}")

print("\n".join(out).rstrip() + "\n")
PY

rc=$?
if [ "$rc" -ne 0 ] || [ ! -s "$TMP" ]; then
  echo "status: composing STATUS.md failed (exit $rc) — STATUS.md left untouched" >&2
  exit "${rc:-1}"
fi
mv "$TMP" STATUS.md
echo "wrote STATUS.md"
[ "$CROSS_OK" = 1 ] || echo "status: cross-repo facts were unavailable — $BLOCKED" >&2
exit 0
