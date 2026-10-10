#!/usr/bin/env python3
"""Meta-layer trial health. TRIAL (started 2026-10-10).
Usage: python3 scripts/trial_health.py [--block] [--issue N]   --block prints the Friday report block; --issue N rewrites the health section of that socialus-ops Issue."""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from score_lib import *

TRACKER = 'https://github.com/donlafranchi/socialus-ops/issues/89'
BUILT = ['score-ci-health', 'score-doc-drift']
QUEUE = [  # next to build first
    ('score-gap-leakage', 'a few weeks of `build-log/reports/` feature reports (first batch lands 2026-10-10)'),
    ('score-review-coverage', 'a PR-label scan; can start any time, needs `record-pm-review` in use for the PM-look half'),
    ('score-rework', 'smoke tied to merge commits, so a follow-up bug can be traced to the PR that caused it'),
    ('score-pm-overrule', 'briefs recording rejected/resized, and `record-pm-review` writing `found-by-pm`; nothing to measure until the pipeline has run'),
]
REVIEW_DATE = date(2026, 10, 24)

rows = [l.rstrip('\n').split('\t') for l in open(HISTORY)] if os.path.exists(HISTORY) else []
rows = [r for r in rows if len(r) >= 5]

# 1. on schedule: each built score has a reading within 8 days
sched = []
for s in BUILT:
    ds = [r[0] for r in rows if r[1] == s]
    last = max(ds) if ds else None
    age = (date.today() - date.fromisoformat(last)).days if last else None
    sched.append((s, last, age, age is not None and age <= 8))
on_time = sum(1 for x in sched if x[3])

# 2. meta PRs
prs = []
for repo in (SKILLS, OPS):
    prs += gh_json(['pr', 'list', '-R', repo, '-l', 'meta-change', '-s', 'all', '-L', '100', '--json', 'number,state,mergedAt,labels']) or []
proposed = len(prs)
approved = sum(1 for p in prs if p['mergedAt'])
rejected = sum(1 for p in prs if p['state'] == 'CLOSED' and not p['mergedAt'])
open_ = sum(1 for p in prs if p['state'] == 'OPEN')

# 3. did any score move
moved = []
keys = sorted({(r[1], r[2]) for r in rows})
for s, m in keys:
    rs = sorted([r for r in rows if r[1] == s and r[2] == m], key=lambda r: r[0])
    if len(rs) >= 2 and rs[-1][3] != rs[-2][3]:
        moved.append(f'{s}/{m}: {rs[-2][3]} ({rs[-2][4]}) -> {rs[-1][3]} ({rs[-1][4]})')

today = date.today()
if on_time < len(BUILT):
    health = 'late'
elif not rows:
    health = 'not started'
else:
    health = 'on schedule'
nxt = QUEUE[0]
decision = ''
if today >= REVIEW_DATE:
    decision = f'**Trial review is due ({REVIEW_DATE.isoformat()}): keep, adjust or drop?**'
else:
    decision = f'Trial review: {REVIEW_DATE.isoformat()} ({(REVIEW_DATE - today).days} days).'

lines = [
    f'**Trial health: {health}.** {on_time} of {len(BUILT)} built scores read within the last 8 days: ' + '; '.join(f'{s} ({last or "never"})' for s, last, _, _ in sched) + '.',
    f'Meta PRs: {proposed} proposed, {approved} approved and merged, {rejected} rejected, {open_} open.',
    'Scores that moved: ' + ('; '.join(moved) if moved else 'none yet (needs two readings).'),
    f'Not built yet: ' + ', '.join(f'`{q}`' for q, _ in QUEUE) + f'. Next: `{nxt[0]}`, waiting on {nxt[1]}.',
    decision,
]
health_md = '\n\n'.join(lines)

if '--block' in sys.argv:
    print(f'### Meta-layer trial\n\nWhy: "stick with this and keep improving it" (trial started 2026-10-10). Tracker: {TRACKER}\n\n' + health_md)
elif '--issue' in sys.argv:
    n = sys.argv[sys.argv.index('--issue') + 1]
    body = sh(['gh', 'issue', 'view', n, '-R', OPS, '--json', 'body', '-q', '.body'])
    new = re.sub(r'<!-- trial-health:start -->.*?<!-- trial-health:end -->', lambda m: '<!-- trial-health:start -->\n' + health_md + f'\n\n*Updated {today.isoformat()} by `scripts/trial_health.py`.*\n<!-- trial-health:end -->', body, flags=re.S)
    if new == body:
        print('markers not found; nothing changed')
    else:
        open('/tmp/trial-body.md', 'w').write(new)
        sh(['gh', 'issue', 'edit', n, '-R', OPS, '--body-file', '/tmp/trial-body.md'])
        print(f'updated #{n}')
else:
    print(health_md)
