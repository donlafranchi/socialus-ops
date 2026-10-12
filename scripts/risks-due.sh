#!/usr/bin/env bash
# Accepted risks whose revisit condition has fired, or is close.
#
# SILENT WHEN NOTHING IS DUE, deliberately. A list that prints every day is a
# list nobody reads, and these are the things most easily forgotten precisely
# because somebody already decided they were fine.
#
# What "due" means, and why it is only ever a DATE here:
#   · past      — review_by has passed. Argue it again or delete it.
#   · soon      — review_by is within 21 days.
#   · triggered — a revisit_if condition that is not a date has fired. A script
#                 cannot know whether "the first report of illegal content"
#                 has happened, so it never claims to. Those conditions are
#                 printed alongside the dated ones so a person can answer them.
#
#   bash scripts/risks-due.sh          # dated entries that are due or close
#   bash scripts/risks-due.sh --all    # every accepted risk, with its condition
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export RISKS_ALL="${1:-}"

python3 - <<'PY'
import datetime, glob, json, os, sys

SOON_DAYS = 21
today = datetime.date.today()
show_all = os.environ.get("RISKS_ALL") == "--all"

entries = []
for path in sorted(glob.glob("accepted-risks/*.json")):
    try:
        entries.append((path, json.load(open(path))))
    except Exception as e:
        print(f"risks-due: {path} is not valid JSON — {e}", file=sys.stderr)
        sys.exit(2)

def days_until(d):
    try:
        return (datetime.date.fromisoformat(d) - today).days
    except Exception:
        return None

rows = []
for path, e in entries:
    left = days_until(e.get("review_by") or "")
    if left is None:
        continue
    state = "past" if left < 0 else ("soon" if left <= SOON_DAYS else "later")
    if state == "later" and not show_all:
        continue
    rows.append((left, state, e))

if not rows:
    sys.exit(0)          # silent, and green

rows.sort(key=lambda r: r[0])
print("Accepted risks needing a look\n")
for left, state, e in rows:
    when = f"{-left}d overdue" if left < 0 else f"in {left}d"
    print(f"  [{state.upper()}] {e.get('object', '?')}")
    print(f"      review_by {e.get('review_by')} ({when})")
    if e.get("cost_if_forgotten"):
        print(f"      if forgotten: {e['cost_if_forgotten']}")
    print(f"      revisit if: {e.get('revisit_if', '—')}")
    print()

print("Re-argue or delete. Renewing is a new dated ruling, not a quiet edit.")
sys.exit(1)
PY
