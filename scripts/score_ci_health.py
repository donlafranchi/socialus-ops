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

ci = [r for r in (gh_json(['run', 'list', '-R', WEB, '-w', 'CI', '-L', '500', '--json', 'conclusion,createdAt,event,headBranch']) or []) if r['createdAt'] >= since and r['conclusion'] in ('success', 'failure')]
# Split (tuning 2026-10-10): main's CI health is the concern; a PR's first run failing is CI doing its job in a fix loop.
main_runs = [r for r in ci if r['headBranch'] == 'main']
fails = sum(1 for r in main_runs if r['conclusion'] == 'failure')
rate = round(100 * fails / len(main_runs), 1) if main_runs else 0.0
rows.append(('ci_main_fail_pct', rate, '%', band(rate, 5, 15), f'{fails} of {len(main_runs)} finished CI runs on main failed (cancelled excluded)'))

first = {}  # head branch -> its earliest finished pull_request run in the window
for r in sorted((r for r in ci if r['event'] == 'pull_request'), key=lambda r: r['createdAt']):
    first.setdefault(r['headBranch'], r)
pfails = sum(1 for r in first.values() if r['conclusion'] == 'failure')
prate = round(100 * pfails / len(first), 1) if first else 0.0
rows.append(('ci_pr_first_run_fail_pct', prate, '%', 'none', f'{pfails} of {len(first)} PR branches failed CI on their first run (reported, no band yet)'))

# Per workflow (tuning 2026-10-30): one 500-run list across every workflow held about five days of socialus-web
# runs (CI plus the daily seed), so a daily smoke counted 5 runs in a 14-day window and never reached MIN_SMOKE.
by = {}
for wf in (gh_json(['workflow', 'list', '-R', WEB, '--json', 'name,state']) or []):
    if wf.get('state') != 'active':
        continue
    rs = [r for r in (gh_json(['run', 'list', '-R', WEB, '-w', wf['name'], '-L', '100', '--json', 'workflowName,conclusion,createdAt,event']) or []) if r['createdAt'] >= since and r['event'] == 'schedule' and r['conclusion'] in ('success', 'failure')]
    if rs:
        by[wf['name']] = rs
red = []
for name, rs in by.items():
    rs.sort(key=lambda r: r['createdAt'])
    if len(rs) >= 3 and all(r['conclusion'] == 'failure' for r in rs[-3:]):
        red.append(name)
rows.append(('scheduled_red', len(red), 'workflows', band(len(red), 0, 1), ', '.join(sorted(red)) or 'none: no scheduled workflow failed its last 3 runs'))

sm = by.get('smoke-live', [])
sfail = sum(1 for r in sm if r['conclusion'] == 'failure')
srate = round(100 * sfail / len(sm), 1) if sm else 0.0
MIN_SMOKE = 7  # tuning 2026-10-10: 2 of 3 runs is not a rate; band only once the window holds 7 scheduled runs
if len(sm) >= MIN_SMOKE:
    rows.append(('smoke_red_pct', srate, '%', band(srate, 10, 30), f'{sfail} of {len(sm)} scheduled smoke runs failed'))
else:
    rows.append(('smoke_red_pct', srate, '%', 'none', f'{sfail} of {len(sm)} scheduled smoke runs failed; fewer than {MIN_SMOKE} runs, so no band yet'))

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

banded = [r for r in rows if r[3] != 'none']
overall = 'red' if any(r[3] == 'red' for r in banded) else ('amber' if any(r[3] == 'amber' for r in banded) else 'green')
lines = ['# score-ci-health', '', TRIAL_LINE, '', f'as-of: {date.today().isoformat()} · window: {days} days · overall: **{overall}** (the worst banded metric; `none` is reported, not banded)', '',
         '| Metric | Value | Band | Trend | Detail |', '|---|---|---|---|---|']
for m, v, u, b, note in rows:
    lines.append(f'| {m} | {v} {u} | {b} | {trend("score-ci-health", m, float(v))} | {note} |')
    if '--no-write' not in sys.argv:
        record('score-ci-health', m, v, b)
lines += ['', 'Sources: `gh run list` per repo; annotation of the latest failed run for the billing check. Thresholds [A]: CI main fail % green ≤5, amber ≤15; PR first-run fail % reported, no band; smoke red % green ≤10, amber ≤30 once the window holds 7 scheduled runs; scheduled-red and blocked-repo counts green 0.']
body = '\n'.join(lines) + '\n'
print(body)
if '--no-write' not in sys.argv:
    print('wrote', write_report('score-ci-health', body))
