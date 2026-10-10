#!/usr/bin/env python3
"""score-doc-drift. TRIAL. Counts places where a document disagrees with live state. Usage: python3 scripts/score_doc_drift.py [--no-write]"""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from score_lib import *

items = []  # (check, what)


def read(*p):
    f = os.path.join(PROJECTS, *p)
    return open(f).read() if os.path.exists(f) else None


def age(text, pattern):
    m = re.search(pattern, text or '')
    return (date.today() - date.fromisoformat(m.group(1))).days if m else None

# a. generated documents against their cadence
for label, text, pat, limit in [
    ('socialus-plan/STATUS.md', read('socialus-plan', 'STATUS.md'), r'Generated (\d{4}-\d{2}-\d{2})', 2),
    ('socialus-plan/DASHBOARD.md', read('socialus-plan', 'DASHBOARD.md'), r'updated (\d{4}-\d{2}-\d{2})', 2),
    ('socialus-ops/README.md', read('socialus-ops', 'README.md'), r'Snapshot, (\d{4}-\d{2}-\d{2})', 8)]:
    a = age(text, pat)
    if a is None:
        items.append(('doc-age', f'{label}: no generated date found'))
    elif a > limit:
        items.append(('doc-age', f'{label} is {a} days old (limit {limit})'))

# b. skills library: directories vs link.sh vs the README table
sk = os.path.join(PROJECTS, 'skills')
dirs = {d for d in os.listdir(sk) if os.path.exists(os.path.join(sk, d, 'SKILL.md'))}
link = read('skills', 'link.sh') or ''
linked = set(re.findall(r'[a-z][a-z0-9-]+', ' '.join(re.findall(r'^(?:PLAN|METHOD|WEB)="([^"]*)"', link, re.M))))
table = set(re.findall(r'^\| `([a-z0-9-]+)`', read('skills', 'README.md') or '', re.M))
table |= set(re.findall(r'`([a-z0-9-]+)`', ' '.join(l for l in (read('skills', 'README.md') or '').splitlines() if l.startswith('| `regen-status`'))))
for d in sorted(dirs - linked):
    items.append(('skill-link', f'{d} is in skills/ but not in link.sh'))
for d in sorted(linked - dirs):
    items.append(('skill-link', f'link.sh names {d}, which is not in skills/'))
for d in sorted(dirs - table):
    items.append(('skill-table', f'{d} has no row in skills/README.md'))

# c. the ops README mentions every skill
readme = read('socialus-ops', 'README.md') or ''
for d in sorted(dirs):
    if f'`{d}`' not in readme:
        items.append(('readme-skill', f'{d} is not mentioned in socialus-ops/README.md'))

# d. the workflow count the README states against the live count
m = re.search(r'(\d+) (?:CI )?workflows', readme)
wf = gh_json(['workflow', 'list', '-R', WEB, '-L', '200', '--json', 'name,state']) or []
live = sum(1 for w in wf if w['state'] == 'active')
if m and live and int(m.group(1)) != live:
    items.append(('workflow-count', f'README says {m.group(1)} workflows; socialus-web has {live} active'))

# e. an approved or building scenario whose Issues are all closed
iss = gh_json(['issue', 'list', '-R', WEB, '-s', 'all', '-L', '600', '--json', 'title,state']) or []
st = {}
for i in iss:
    f = re.match(r'^(F\d{3})\b', i['title'])
    if f:
        st.setdefault(f.group(1), set()).add(i['state'])
pdir = os.path.join(PROJECTS, 'socialus-plan', 'planning')
if os.path.isdir(pdir):
    for fn in sorted(os.listdir(pdir)):
        m = re.match(r'scenario-(F\d{3})\.md$', fn)
        if not m:
            continue
        head = open(os.path.join(pdir, fn)).read(800)
        s = re.search(r'^status:\s*(\w+)', head, re.M)
        if s and s.group(1) in ('approved', 'building') and st.get(m.group(1)) == {'CLOSED'}:
            items.append(('scenario-status', f'{m.group(1)} is {s.group(1)} but every Issue for it is closed'))

n = len(items)
b = band(n, 2, 6)
by = {}
for c, w in items:
    by.setdefault(c, []).append(w)
lines = ['# score-doc-drift', '', TRIAL_LINE, '', f'as-of: {date.today().isoformat()} · drift items: **{n}** · band: **{b}** · {trend("score-doc-drift", "drift_items", float(n))}', '']
for c, ws in by.items():
    lines.append(f'**{c}** ({len(ws)})')
    lines += [f'- {w}' for w in ws]
    lines.append('')
if not items:
    lines.append('No drift found.')
lines += ['Checks: generated-doc age vs cadence; skills dirs vs `link.sh` vs `skills/README.md`; README mentions every skill; README workflow count vs `gh`; approved/building scenarios whose Issues are all closed. Thresholds [A]: green ≤2, amber ≤6.']
body = '\n'.join(lines) + '\n'
print(body)
if '--no-write' not in sys.argv:
    record('score-doc-drift', 'drift_items', n, b)
    print('wrote', write_report('score-doc-drift', body))
