"""Shared helpers for the score-* scripts. TRIAL (started 2026-10-10): thresholds are assumed until two weeks of readings exist."""
import json, os, subprocess, sys
from datetime import date, datetime, timedelta, timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
PROJECTS = os.environ.get('PROJECTS', os.path.expanduser('~/Projects'))
HISTORY = os.path.join(ROOT, 'scores', 'history.tsv')
WEB, PLAN, SKILLS, OPS = ('donlafranchi/socialus-web', 'donlafranchi/socialus-plan', 'donlafranchi/skills', 'donlafranchi/socialus-ops')
TRIAL_LINE = '> **TRIAL (started 2026-10-10).** Thresholds are assumed until two weeks of readings exist. Read-only; proposes nothing by itself.'


def sh(args):
    return subprocess.run(args, capture_output=True, text=True).stdout


def gh_json(args):
    out = sh(['gh', *args])
    try:
        return json.loads(out)
    except ValueError:
        return None


def since_iso(days):
    return (datetime.now(timezone.utc) - timedelta(days=days)).strftime('%Y-%m-%dT%H:%M:%SZ')


def band(value, green, amber):
    """Lower is better. green and amber are the inclusive upper limits."""
    return 'green' if value <= green else ('amber' if value <= amber else 'red')


def previous(skill, metric):
    if not os.path.exists(HISTORY):
        return None
    last = None
    for line in open(HISTORY):
        f = line.rstrip('\n').split('\t')
        if len(f) >= 5 and f[1] == skill and f[2] == metric and f[0] < date.today().isoformat():
            last = f
    return last


def record(skill, metric, value, b):
    os.makedirs(os.path.dirname(HISTORY), exist_ok=True)
    rows = []
    if os.path.exists(HISTORY):
        rows = [l for l in open(HISTORY) if not l.startswith(f'{date.today().isoformat()}\t{skill}\t{metric}\t')]
    rows.append(f'{date.today().isoformat()}\t{skill}\t{metric}\t{value}\t{b}\n')
    open(HISTORY, 'w').writelines(rows)


def trend(skill, metric, value):
    p = previous(skill, metric)
    if not p:
        return 'first reading'
    old = float(p[3])
    d = value - old
    return f'was {p[3]} on {p[0]} ({"worse" if d > 0 else "better" if d < 0 else "same"})'


def write_report(skill, body):
    d = os.path.join(ROOT, 'scores', skill)
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, date.today().isoformat() + '.md')
    open(p, 'w').write(body)
    return p
