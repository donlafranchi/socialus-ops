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

# a2. the handoff snapshot and the roadmap (limits [A], tuned in the Friday notes)
_st = sorted(f for f in os.listdir(os.path.join(PROJECTS, 'socialus-plan', 'handoff', 'state')) if re.match(r'\d{4}-\d{2}-\d{2}\.md$', f)) if os.path.isdir(os.path.join(PROJECTS, 'socialus-plan', 'handoff', 'state')) else []
if not _st:
    items.append(('doc-age', 'socialus-plan/handoff/state: no snapshot'))
else:
    _h = (date.today() - date.fromisoformat(_st[-1][:10])).days
    if _h > 2:
        items.append(('doc-age', f'newest handoff snapshot ({_st[-1][:10]}) is {_h} days old (limit 2)'))
_rm = sh(['git', '-C', os.path.join(PROJECTS, 'socialus-plan'), 'log', '-1', '--format=%cs', '--', 'ROADMAP.md']).strip()
if _rm:
    _r = (date.today() - date.fromisoformat(_rm)).days
    if _r > 30:
        items.append(('doc-age', f'socialus-plan/ROADMAP.md last changed {_r} days ago (limit 30)'))

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

# f. socialus-web's committed doc inventory (docs/DOC-INVENTORY.md, rebuilt weekly by regen-doc-inventory)
import base64
inv = gh_json(['api', 'repos/' + WEB + '/contents/docs/DOC-INVENTORY.md'])
inv_text = base64.b64decode(inv['content']).decode() if inv and inv.get('content') else None
if inv_text is None:
    items.append(('doc-inventory', 'socialus-web docs/DOC-INVENTORY.md is missing; run regen-doc-inventory'))
else:
    am = re.search(r'\*\*As of (\d{4}-\d{2}-\d{2})\.\*\*', inv_text)
    inv_age = (date.today() - date.fromisoformat(am.group(1))).days if am else None
    if inv_age is None or inv_age > 8:
        items.append(('doc-inventory', f'docs/DOC-INVENTORY.md is {inv_age} days old (limit 8)' if inv_age is not None else 'docs/DOC-INVENTORY.md has no as-of date'))
    for title, label in [('Needs review', 'needs review'), ('Undated', 'undated'), ('Stale or aging', 'stale or aging'),
                         ('Broken links', 'has a broken link'), ('Dead references', 'has a dead reference')]:
        sec = re.search(r'^## ' + title + r'\n\n(.*?)(?=^## |\Z)', inv_text, re.M | re.S)
        for line in (sec.group(1).splitlines() if sec else []):
            if line.startswith('- '):
                path = line[2:].split(' (')[0].split(':')[0].strip('`')
                items.append(('doc-inventory', f'socialus-web {path} {label}' if label.startswith('has') else f'socialus-web {path} is {label}'))

# g. the cross-repo doc gardening (tend-docs): the counts it wrote to scores/tend-docs/latest.json. Thresholds [A], tuned in the Friday notes.
import json as _json
_td = os.path.join(PROJECTS, 'socialus-ops', 'scores', 'tend-docs', 'latest.json')
tend = _json.load(open(_td)) if os.path.exists(_td) else None
if tend is None:
    items.append(('tend-docs', 'scores/tend-docs/latest.json is missing; run tend-docs'))
else:
    _a = (date.today() - date.fromisoformat(tend['as_of'])).days
    if _a > 8:
        items.append(('tend-docs', f'the tend-docs reading is {_a} days old (limit 8)'))
    for _k, _lim, _what in [('duplicates', 0, 'duplicate or overlapping docs'), ('undated', 10, 'docs with no date'), ('non_conforming', 25, 'docs without the standard header'), ('superseded', 0, 'superseded docs not yet removed'), ('broken_links', 0, 'broken links')]:
        if tend[_k] > _lim:
            items.append(('tend-docs', f'{tend[_k]} {_what} (limit {_lim})'))
    if tend['hand_written_share'] > 0.85:
        items.append(('tend-docs', f"hand-written share {tend['hand_written_share']:.0%} of {tend['in_scope']} in-scope docs (limit 85%); derivable: {tend['derivable']}"))

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
lines += ['Checks: generated-doc age vs cadence; skills dirs vs `link.sh` vs `skills/README.md`; README mentions every skill; README workflow count vs `gh`; approved/building scenarios whose Issues are all closed; socialus-web `docs/DOC-INVENTORY.md` age and the docs it lists. tend-docs counts (duplicates, undated, non-conforming, superseded, broken links, hand-written share) from `scores/tend-docs/latest.json`. Thresholds [A]: green ≤2, amber ≤6.']
body = '\n'.join(lines) + '\n'
print(body)
if '--no-write' not in sys.argv:
    record('score-doc-drift', 'drift_items', n, b)
    print('wrote', write_report('score-doc-drift', body))
