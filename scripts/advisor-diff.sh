#!/usr/bin/env bash
# Diff a Supabase advisor export against accepted-risks/ (one file per finding).
# Prints only findings nobody has ruled on, plus any accepted entry whose
# review_by has passed. Exits 1 if either list is non-empty.
#
#   supabase inspect db lints --output json > /tmp/advisor.json   # or the dashboard export
#   bash scripts/advisor-diff.sh /tmp/advisor.json
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export ADVISOR="${1:-}"
export REGISTER="$ROOT/accepted-risks"

if [ -z "$ADVISOR" ] || [ ! -f "$ADVISOR" ]; then
  echo "usage: scripts/advisor-diff.sh <advisor-export.json>" >&2
  exit 2
fi

python3 - <<'PY'
import json, os, sys, datetime

import glob
reg = []
for path in sorted(glob.glob(os.path.join(os.environ["REGISTER"], "*.json"))):
    with open(path) as fh:
        reg.append(json.load(fh))
if not reg:
    print("advisor-diff: no entries in accepted-risks/ — every finding will read as unruled.", file=sys.stderr)
raw = json.load(open(os.environ["ADVISOR"]))
findings = raw.get("lints", raw) if isinstance(raw, dict) else raw

def norm(s):
    return (s or "").strip().lower()

keys = {norm(e["cache_key"]) for e in reg if e.get("cache_key")}
pairs = {(norm(e.get("lint")), norm(e.get("object"))) for e in reg}

def obj_of(f):
    # Advisor exports vary: an explicit object, or name + metadata.
    for k in ("object", "name", "title"):
        if f.get(k):
            return f[k]
    md = f.get("metadata") or {}
    if md.get("schema") and md.get("name"):
        return f"{md['schema']}.{md['name']}"
    return ""

unruled = []
for f in findings:
    ck = norm(f.get("cache_key"))
    lint = norm(f.get("lint") or f.get("rule") or f.get("name"))
    obj = norm(obj_of(f))
    if ck and ck in keys:
        continue
    if (lint, obj) in pairs:
        continue
    unruled.append((f.get("level") or f.get("severity") or "?", lint or "?", obj or "?", ck or "-"))

today = datetime.date.today().isoformat()
stale = [e for e in reg if (e.get("review_by") or "9999") < today]

if unruled:
    print(f"advisor-diff: {len(unruled)} finding(s) not in the register\n")
    for lvl, lint, obj, ck in sorted(unruled):
        print(f"  [{lvl.upper()}] {lint} — {obj}   cache_key={ck}")
    print("\nRule on each: a dated ruling in the doc it governs, then an entry here. Or fix it.")

if stale:
    print(f"\nadvisor-diff: {len(stale)} accepted entry/entries past review_by\n")
    for e in stale:
        print(f"  {e['object']} ({e['lint']}) — review_by {e['review_by']}, revisit_if: {e['revisit_if']}")
    print("\nRe-argue or delete. Renewing is a new dated line, not a quiet edit.")

if not unruled and not stale:
    print("advisor-diff: clean — every finding is ruled on, nothing past review.")
    sys.exit(0)
sys.exit(1)
PY
