#!/usr/bin/env python3
"""score-gap-leakage. TRIAL (started 2026-10-10). Where does a known gap in a criterion fall out of sight?
Reads the criterion roll-up (socialus-plan scripts/criteria.py, which parses the criterion reports in socialus-web) and the Issues.
Usage: python3 scripts/score_gap_leakage.py [--no-write]"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from score_lib import *
sys.path.insert(0, os.path.join(PROJECTS, 'socialus-plan', 'scripts'))
import criteria
import glob, json
side = {}
for _p in glob.glob(os.path.join(PROJECTS, 'socialus-web', 'build-log', 'reports', '*', 'F*.json')):
    _d = json.load(open(_p))
    side[_d['feature']] = (bool(_d.get('retired')), {c['id']: c.get('status', 'active') for c in _d['criteria']})

feats = criteria.load()
issues = gh_json(['issue', 'list', '-R', WEB, '-s', 'all', '-L', '800', '--json', 'number,title,state']) or []
state = {i['number']: i['state'] for i in issues}
gap_re = re.compile(r'^F\d{3} · (criterion|check|guard)', re.I)

# 1. closed parent Issue, feature still has unmet criteria (the F081 / F082 pattern)
closed_unmet = []
retired_unmet = []
tracked_closed = []  # tuning 2026-10-23: parent closed, but every unmet active criterion has an open gap Issue (F059 with #587, #589, #828 ...): tracked, not leaking
for f in feats:
    for i in issues:
        if re.match(rf'^{f["id"]} · ', i['title']) and not gap_re.match(i['title']) and i['state'] == 'CLOSED' and f['met'] < f['total']:
            sts = side.get(f['id'], (False, {}))[1]
            loose = [r for r in f['criteria'] if r['built'] != 'yes' and sts.get(r['n'], 'active') == 'active' and not any(state.get(n) == 'OPEN' for n in r['issues'])]
            if side.get(f['id'], (False, {}))[0]:
                retired_unmet.append(f['id'])
            elif not loose:
                tracked_closed.append(f['id'])
            else:
                closed_unmet.append(f"{f['id']} (#{i['number']}: {f['met']} of {f['total']} met; loose: {', '.join(r['n'] for r in loose)})")
            break

# 2. unmet criterion with no OPEN Issue linked in its row: a gap nobody is tracking
untracked = []
spec_conflict = []
closed_only = []
for f in feats:
    for r in f['criteria']:
        st = side.get(f['id'], (False, {}))[1].get(r['n'], 'active')
        if r['built'] == 'yes' or st == 'retired':
            continue
        if st == 'spec-conflict':
            spec_conflict.append(f"{f['id']}.{r['n']}")
        elif not any(state.get(n) == 'OPEN' for n in r['issues']):
            untracked.append(f"{f['id']}.{r['n']}")
            if r['issues'] and all(state.get(n) == 'CLOSED' for n in r['issues']):
                closed_only.append(f"{f['id']}.{r['n']}")

# 3. built criterion with no marked check
built = [(f['id'], r) for f in feats for r in f['criteria'] if r['built'] == 'yes']
unchecked = [f"{fid}.{r['n']}" for fid, r in built if r['checked'] != 'yes']
pct = round(100 * len(unchecked) / len(built), 1) if built else 0.0

rows = [
    ('closed_parent_unmet', len(closed_unmet), 'features', band(len(closed_unmet), 0, 2), ('; '.join(closed_unmet[:6]) or 'none') + (f'; {len(retired_unmet)} retired-scenario features not counted' if retired_unmet else '') + (f'; {len(tracked_closed)} closed parents whose gaps all have open Issues not counted ({", ".join(tracked_closed)})' if tracked_closed else '')),
    ('closed_issue_unmet', len(closed_only), 'criteria', band(len(closed_only), 0, 3), ', '.join(closed_only[:10]) or 'none'),
    ('untracked_unmet', len(untracked), 'criteria', band(len(untracked), 2, 10), ', '.join(untracked[:10]) + (' ...' if len(untracked) > 10 else '') or 'none'),
    ('spec_conflict_open', len(spec_conflict), 'criteria', 'none', 'routed to scope-scenario; reported, not banded'),
    ('unchecked_built_pct', pct, '%', band(pct, 30, 60), f'{len(unchecked)} of {len(built)} built criteria have no marked check'),
]
overall = 'red' if any(r[3] == 'red' for r in rows) else ('amber' if any(r[3] == 'amber' for r in rows) else 'green')
L = ['# score-gap-leakage', '', TRIAL_LINE, '',
     f'as-of: {date.today().isoformat()} · {len(feats)} features, {sum(len(f["criteria"]) for f in feats)} criteria · overall: **{overall}** (the worst metric)', '',
     '| Metric | Value | Band | Trend | Detail |', '|---|---|---|---|---|']
for m, v, u, b, note in rows:
    L.append(f'| {m} | {v} {u} | {b} | {trend("score-gap-leakage", m, float(v))} | {note} |')
    if '--no-write' not in sys.argv:
        record('score-gap-leakage', m, v, b)
L += ['', 'Sources: the criterion roll-up (`socialus-plan/scripts/criteria.py` over `socialus-web/build-log/reports/`) and `gh issue list`. A criterion row links an Issue by `#N`; a PR number there is not an Issue, so a gap tracked only by a merged PR counts as untracked. SPEC-CONFLICT criteria (no Issue by design, they go to `scope-scenario`) also count as untracked here. Thresholds [A]: closed_parent_unmet green 0 / amber ≤2; untracked_unmet green ≤2 / amber ≤10; unchecked_built_pct green ≤30 / amber ≤60.']
body = '\n'.join(L) + '\n'
print(body)
if '--no-write' not in sys.argv:
    print('wrote', write_report('score-gap-leakage', body))
