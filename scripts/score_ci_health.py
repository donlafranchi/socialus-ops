#!/usr/bin/env python3
"""score-ci-health. TRIAL. Usage: python3 scripts/score_ci_health.py [--days 14] [--no-write]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from score_lib import *

days = 14
if '--days' in sys.argv:
    days = int(sys.argv[sys.argv.index('--days') + 1])
since = since_iso(days)
rows = []  # metric, value, unit, band, note


def counts(runs):
    c = {}
    for r in runs:
        c[r['conclusion']] = c.get(r['conclusion'], 0) + 1
    return c

ci = [r for r in (gh_json(['run', 'list', '-R', WEB, '-w', 'CI', '-L', '300', '--json', 'conclusion,createdAt']) or []) if r['createdAt'] >= since and r['conclusion'] in ('success', 'failure')]
fails = sum(1 for r in ci if r['conclusion'] == 'failure')
rate = round(100 * fails / len(ci), 1) if ci else 0.0
rows.append(('ci_fail_pct', rate, '%', band(rate, 10, 20), f'{fails} of {len(ci)} finished CI runs failed (cancelled excluded)'))

allruns = [r for r in (gh_json(['run', 'list', '-R', WEB, '-L', '500', '--json', 'workflowName,conclusion,createdAt,event']) or []) if r['createdAt'] >= since and r['event'] == 'schedule' and r['conclusion'] in ('success', 'failure')]
by = {}
for r in allruns:
    by.setdefault(r['workflowName'], []).append(r)
red = []
for name, rs in by.items():
    rs.sort(key=lambda r: r['createdAt'])
    if len(rs) >= 3 and all(r['conclusion'] == 'failure' for r in rs[-3:]):
        red.append(name)
rows.append(('scheduled_red', len(red), 'workflows', band(len(red), 0, 1), ', '.join(sorted(red)) or 'none: no scheduled workflow failed its last 3 runs'))

sm = by.get('smoke-live', [])
sfail = sum(1 for r in sm if r['conclusion'] == 'failure')
srate = round(100 * sfail / len(sm), 1) if sm else 0.0
rows.append(('smoke_red_pct', srate, '%', band(srate, 10, 30), f'{sfail} of {len(sm)} scheduled smoke runs failed'))

blocked = []
for repo in (PLAN, WEB, OPS, SKILLS):
    latest = gh_json(['run', 'list', '-R', repo, '-L', '1', '--json', 'databaseId,conclusion']) or []
    if latest and latest[0]['conclusion'] == 'failure':
        jobs = gh_json(['api', f'repos/{repo}/actions/runs/{latest[0]["databaseId"]}/jobs']) or {}
        for j in jobs.get('jobs', [])[:1]:
            ann = gh_json(['api', f'repos/{repo}/check-runs/{j["id"]}/annotations']) or []
            if any('payments have failed' in (a.get('message') or '') or 'spending limit' in (a.get('message') or '') for a in ann):
                blocked.append(repo.split('/')[1])
rows.append(('actions_blocked', len(blocked), 'repos', band(len(blocked), 0, 0), ', '.join(blocked) or 'none: Actions start in every repo'))

overall = 'red' if any(r[3] == 'red' for r in rows) else ('amber' if any(r[3] == 'amber' for r in rows) else 'green')
lines = ['# score-ci-health', '', TRIAL_LINE, '', f'as-of: {date.today().isoformat()} · window: {days} days · overall: **{overall}** (the worst metric)', '',
         '| Metric | Value | Band | Trend | Detail |', '|---|---|---|---|---|']
for m, v, u, b, note in rows:
    lines.append(f'| {m} | {v} {u} | {b} | {trend("score-ci-health", m, float(v))} | {note} |')
    if '--no-write' not in sys.argv:
        record('score-ci-health', m, v, b)
lines += ['', 'Sources: `gh run list` per repo; annotation of the latest failed run for the billing check. Thresholds [A]: CI fail % green ≤10, amber ≤20; smoke red % green ≤10, amber ≤30; scheduled-red and blocked-repo counts green 0.']
body = '\n'.join(lines) + '\n'
print(body)
if '--no-write' not in sys.argv:
    print('wrote', write_report('score-ci-health', body))
