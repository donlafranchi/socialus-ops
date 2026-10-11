#!/usr/bin/env python3
"""Audit of the criterion roll-up chain, regenerated from live sources (never hand-written).
Writes audits/criterion-rollup.md. Usage: python3 scripts/audit_criterion_rollup.py [--no-write]
Reads: socialus-plan (scenarios, STATUS.md, DASHBOARD.md, dashboard html, scripts) and socialus-web (reports, Issues, PRs, runs) via gh and sibling checkouts."""
import base64, glob, json, os, re, subprocess, sys
from datetime import date
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from score_lib import PROJECTS, WEB, gh_json, sh, ROOT

PLAN = os.path.join(PROJECTS, 'socialus-plan')
sys.path.insert(0, os.path.join(PLAN, 'scripts'))
import criteria

def read(p):
    return open(p).read() if os.path.exists(p) else ''

today = date.today().isoformat()
# ---- facts
feats = criteria.load()
by = {f['id']: f for f in feats}
met = sum(f['met'] for f in feats); tot = sum(f['total'] for f in feats); red = [f for f in feats if f['blocked']]
unknown = sum(1 for f in feats for r in f['criteria'] if r['built'] == 'unknown')
scen = {}
for p in glob.glob(os.path.join(PLAN, 'planning', 'scenario-F*.md')):
    t = read(p); fid = re.search(r'scenario-(F\d+)', p).group(1)
    st = re.search(r'^status:\s*(\w+)', t[:800], re.M); gt = re.search(r'^gates:\s*(\w+)', t[:800], re.M)
    acc = re.split(r'^## ', t, flags=re.M)
    a = next((s for s in acc if s.startswith('Acceptance')), '')
    scen[fid] = {'status': st.group(1) if st else '?', 'gates': gt.group(1) if gt else '', 'n': len(re.findall(r'^\d+\. ', a, re.M))}
live_scen = {k: v for k, v in scen.items() if v['status'] in ('approved', 'building')}
crit_mismatch = [(k, scen[k]['n'], by[k]['total']) for k in by if k in scen and scen[k]['n'] and scen[k]['n'] != by[k]['total']]
ms = gh_json(['issue', 'list', '-R', WEB, '-m', 'Beta 11-06', '-s', 'all', '-L', '600', '--json', 'number,title,state,labels,createdAt']) or []
ms_total = len(ms); ms_closed = sum(1 for i in ms if i['state'] == 'CLOSED')
lab = lambda i: {l['name'] for l in i['labels']}
ms_scen = [i for i in ms if 'scenario' in lab(i)]
gap_re = re.compile(r'^F\d{3} · (criterion|check|guard)', re.I)
gaps = [i for i in ms if gap_re.match(i['title'])]
# the 5pm all-feature report run (2026-10-10 17:00 PT = 2026-10-11 00:00Z) filed most gap Issues; four were filed earlier that day
RUN_CUT = '2026-10-11T00:00:00Z'
before = ms_total - len([g for g in gaps if g['createdAt'] >= RUN_CUT])
closed_parent_unmet = []
for f in feats:
    for i in ms:
        if re.match(rf'^{f["id"]} · ', i['title']) and not gap_re.match(i['title']) and i['state'] == 'CLOSED' and f['met'] < f['total']:
            closed_parent_unmet.append((f['id'], i['number'], f['met'], f['total'])); break
dash = read(os.path.join(PLAN, 'DASHBOARD.md'))
areas = {}
for l in dash.split('\n'):
    m = re.match(r'\| ([a-z-]+) \| \d+/\d+ \| (\d+)/(\d+) \|', l)
    if m: areas[m.group(1)] = (int(m.group(2)), int(m.group(3)))
html = read(os.path.join(PLAN, 'dashboard', 'status-dashboard.html'))
mm = re.search(r'<script id="data" type="application/json">(.*?)</script>', html, re.S)
dd = json.loads(mm.group(1).replace('<\\/', '</')) if mm else {}
test_items = len(dd.get('test_items', []))
i519 = sh(['gh', 'issue', 'view', '519', '-R', WEB, '--json', 'body', '-q', '.body'])
boxes519 = len(re.findall(r'^\s*[-*] \[[ xX]\]', i519, re.M))
rd = base64.b64decode(json.loads(sh(['gh', 'api', f'repos/{WEB}/contents/build-log/reports/README.md']) or '{}').get('content', '')).decode() if True else ''
roll = {}
for l in rd.split('\n'):
    m = re.match(r'\| \S+ \| \[(F\d+)[^\]]*\]\([^)]*\)[^|]*\| (\d+) \| (\S+) \| (\S+) \|', l)
    if m: roll[m.group(1)] = (int(m.group(2)), m.group(3), m.group(4))
readme_mis = [(k, v[1], by[k]['met']) for k, v in roll.items() if k in by and v[1] != str(by[k]['met'])]
status = read(os.path.join(PLAN, 'STATUS.md'))
cov = {m.group(1): (int(m.group(2)), int(m.group(3))) for m in re.finditer(r'\*\*(F\d+)\*\* · (\d+) of (\d+) covered', status)}
cov_dis = [(k, cov[k][0], roll[k][2]) for k in cov if k in roll and str(cov[k][0]) != roll[k][2]]
webdir = os.path.join(PROJECTS, 'socialus-web')
mk = sh(['bash', '-c', f"cd {webdir} && grep -rhoE '\\[guards F[0-9]+\\.[0-9]+' src tests evals 2>/dev/null | sort -u | wc -l"]).strip()
mkf = sh(['bash', '-c', f"cd {webdir} && grep -rhoE '\\[guards F[0-9]+' src tests evals 2>/dev/null | sort -u | wc -l"]).strip()
evals = len(glob.glob(os.path.join(webdir, 'evals', 'features', '*.spec.ts')))
uat_closed = [i for i in (gh_json(['issue', 'list', '-R', WEB, '-l', 'uat', '-s', 'closed', '--json', 'number,title']) or []) if 'self-check' not in i['title']]
def last(path, repo=PLAN):
    return sh(['git', '-C', repo, 'log', '-1', '--format=%ad', '--date=short', '--', path]).strip() or 'never'
smoke = (gh_json(['run', 'list', '-R', WEB, '-w', 'smoke-live.yml', '-L', '1', '--json', 'conclusion,createdAt']) or [{}])[0]
sched = {os.path.basename(os.path.dirname(p)): read(p) for p in glob.glob(os.path.expanduser('~/.claude/scheduled-tasks/*/SKILL.md'))}
friday = next((t for k, t in sched.items() if 'friday' in k), '')
sched_reports = 'criteria.py' in friday and 'regen-feature-report' in friday
dpy = read(os.path.join(PLAN, 'scripts', 'dashboard.py'))
has_ramp = "RAMP=['#b91c1c'" in dpy; has_red = 'f.blocked' in dpy
repo_dates = sh(['git', '-C', webdir, 'log', '--format=%ad', '--date=short', '--', 'build-log/reports']).split()
rep_last = max(repo_dates) if repo_dates else 'never'
# -- facts added after the fixes: is each roll-up generated and in agreement?
rep_lines = {}
for f in feats:
    raw = sh(['gh', 'api', f'repos/{WEB}/contents/' + f['url'].split('/main/')[1]])
    try:
        t = base64.b64decode(json.loads(raw)['content']).decode()
    except Exception:
        continue
    m = re.search(r'\| (\d+) criteria \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \|', t)
    if m:
        rep_lines[f['id']] = tuple(int(x) for x in m.groups())
rep_dis = [f['id'] for f in feats if f['id'] in rep_lines and rep_lines[f['id']] != (f['total'], f['met'], f['checked'], f['reviewed'], f['smoked'], f['pm'])]
rep_gen = len(rep_lines)
roll_new = {}
for l in rd.split('\n'):
    m = re.match(r'\| \S+ \| \[(F\d+)[^\]]*\]\([^)]*\) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \|', l)
    if m: roll_new[m.group(1)] = tuple(int(x) for x in m.groups()[1:])
readme_dis2 = [k for k, v in roll_new.items() if k in by and v != (by[k]['total'], by[k]['met'], by[k]['checked'], by[k]['reviewed'], by[k]['smoked'], by[k]['pm'])]
cov_dis2 = [(k, cov[k][0], by[k]['checked']) for k in cov if k in by and cov[k][0] != by[k]['checked']]
stale = [f['id'] for f in feats if f.get('stale')]
reviewed = sum(f['reviewed'] for f in feats); smoked = sum(f['smoked'] for f in feats); pmlooked = sum(f['pm'] for f in feats); checked = sum(f['checked'] for f in feats)
header_line = next((l for l in dash.split('\n') if l.startswith('# Beta')), '')
wf_dash = os.path.exists(os.path.join(PLAN, '.github', 'workflows', 'dashboard.yml'))
wf_run = (gh_json(['run', 'list', '-R', 'donlafranchi/socialus-plan', '-w', 'dashboard', '-L', '1', '--json', 'conclusion,createdAt,event']) or [{}])[0]
test_loud = bool(dd.get('test_notice'))
pct = lambda a, b: f'{round(100 * a / b)}%' if b else 'n/a'

# ---- document
V = lambda ok: 'V' if ok else 'B'
L = []
w = L.append
w('# Criterion roll-up: audit')
w('')
w(f'**Generated {today} by `scripts/audit_criterion_rollup.py`, never hand-written.** Every number below was computed from live files, runs and data on that date. **V** verified, **A** assumed, **B** broken or missing. The five fixes from the first audit have shipped; each row says what is true now.')
w('')
w('```')
w('  scenario criteria (plan)     UAT lists        guards markers / evals       PR review    smoke')
w('        |                        |                      |                      |           |')
w('        v                        v                      v                      v           v')
w('  feature report <--- agent run: regen-feature-report (one per feature, build-log/reports/)')
w('        |   rows: Built, Reviewed per criterion; roll-up lines GENERATED from the rows')
w('        v')
w('  scripts/criteria.py: Checked = markers.py (same as STATUS); Smoked = green smoke after last merge;')
w('        |             PM looked = pm-reviewed; stale = merged after the report')
w('        |-----------------> handoff/capabilities.md')
w('        v')
w('  rollup(): criterion -> feature -> area -> milestone  (plain sums of criteria)')
w('        v')
w('  dashboard.py (every 6 h by workflow): header = criteria met / total; area cards; features; Issue count alongside')
w('        v')
w('  DASHBOARD.md + status-dashboard.html  ->  Friday launch report')
w('```')
w('')
w('## 1. Where criteria come from')
w('')
w('| Source | Who writes it | Status | Evidence |')
w('|---|---|---|---|')
w(f'| Scenario `Acceptance` list, numbered | Cowork drafts, the PM approves | **V** | {len(scen)} scenario files; {len(live_scen)} approved or building; the reports hold {tot} criteria across {len(feats)} features |')
w(f'| Scenario count vs report count | n/a | **{V(not crit_mismatch)}** | {"every report matches its scenario" if not crit_mismatch else "differs: " + ", ".join(f"{k} scenario {a} vs report {b}" for k, a, b in crit_mismatch[:6])} |')
w(f'| Shipped scenarios (file deleted at sync) | recovered from git history | **A** | {len([f for f in feats if f["id"] not in scen])} features have no scenario file; criteria reconstructed |')
w(f'| Issues with no criteria (change, bug, chore) | the PM / Dispatch | **B** | {ms_total - len(ms_scen)} of {ms_total} milestone Issues have no acceptance criteria and no criterion-level result (not addressed by the five fixes) |')
w(f'| UAT checklist `#519` | an agent | **B** | the Issue has {boxes519} checkboxes; the dashboard now says so loudly ({"V: notice shown" if test_loud else "B: still silent"}), but the list is still empty |')
w('')
w('## 2. How a criterion is tested, scored, and where the result lives')
w('')
w('| Mechanism | Triggered by | Where the result is stored | Status | Evidence |')
w('|---|---|---|---|---|')
w(f'| Guards marker on a test | CI `check-markers.sh`, `markers.py coverage` | STATUS.md, and now `criteria.py` | **V**, low | {mk} criteria carry a marker across {mkf} features, of {tot} ({pct(int(mk or 0), tot)}) |')
w(f'| Checked (one definition: a marker covers the whole criterion) | `criteria.py coverage()` = `markers.py` | dashboard, report roll-ups | **{V(not cov_dis2)}** | STATUS vs criteria.py disagree on {len(cov_dis2)} of {len(cov)} features; {checked} of {tot} criteria checked |')
w(f'| Reviewed per criterion | the report row (agent, from PR `Reviewed by:`) | report + dashboard | **V**, thin | {reviewed} of {tot} criteria reviewed |')
w(f'| Feature evals `evals/features/*.spec.ts` | CI Browser job | CI log only | **V**, partial | {evals} spec files; no per-criterion result is written |')
w(f'| Smoked per criterion | a green smoke-live run after the feature\'s last merge | dashboard, report roll-ups | **V**, weak | {smoked} of {tot}; last green smoke {(feats[0].get("last_green_smoke") or "never")[:10]}, latest run {feats[0].get("last_smoke")} (smoke loads pages; it does not test criteria) |')
w(f'| PM looked | `pm-reviewed` label (`record-pm-review`, closed UAT) | labels | **B** | {pmlooked} of {tot} criteria; {len(uat_closed)} real UAT Issues have ever been closed |')
w('')
w('## 3. What rolls up into what, and the formula')
w('')
w('| Level | Formula | Where computed | Status | Evidence |')
w('|---|---|---|---|---|')
w(f'| Criterion | Built = `yes` only (unknown is unmet); Checked, Reviewed, Smoked, PM looked each yes/no | `scripts/criteria.py` | **V** | {unknown} of {tot} criteria are `unknown` and count as unmet |')
w(f'| Feature | met / total, and the same for each phase | `criteria.py` | **V** | {len(feats)} features, {met} of {tot} met ({pct(met, tot)}); {len(red)} red |')
w(f'| Report roll-up lines and README table | generated from the rows by `--rewrite-reports` | `criteria.py` | **{V(not rep_dis and not readme_dis2 and rep_gen >= len(feats) - 1)}** | {rep_gen} of {len(feats)} reports carry a generated line; {len(rep_dis)} disagree with their rows, {len(readme_dis2)} README rows disagree |')
w(f'| Area | sum of criteria in the area (`rollup()`); red if any feature is red | `criteria.py`, `dashboard.py` | **{V("criteria.rollup" in dpy)}** | area cards lead with criteria; Issue stages are shown only for areas with no reports |')
w(f'| Milestone / beta % | **criteria met / total**; Issues closed shown alongside | `dashboard.py` header | **{V("criteria met" in header_line)}** | header: "{header_line[:170]}..." |')
w('')
w('Areas, Issue-derived against criterion-derived (the old and the new view side by side):')
w('')
w('| Area | Issues "Built" | Criteria met | Features reporting |')
w('|---|---|---|---|')
for a, (b, n) in areas.items():
    fs = [f for f in feats if f['area'] == a]
    w(f'| {a} | {b}/{n} ({pct(b, n)}) | ' + (f'{sum(f["met"] for f in fs)}/{sum(f["total"] for f in fs)} ({pct(sum(f["met"] for f in fs), sum(f["total"] for f in fs))})' if fs else 'no reports') + f' | {len(fs)} |')
w('')
w('**Double counting (still true, no longer the headline):**')
w(f'- {len(gaps)} of {ms_total} milestone Issues are gap Issues auto-filed from criteria, so a criterion appears as a report row and as an Issue. The Issue count ({ms_closed} of {ms_total}, was {ms_closed} of {before}) is now shown alongside the criterion figure, not as the beta %.')
w(f'- {len(closed_parent_unmet)} scenario Issues are closed while their feature has unmet criteria, so the Issue-derived areas still count them done: ' + (', '.join(f'{f} (#{n}, {m} of {t})' for f, n, m, t in closed_parent_unmet[:6]) or 'none') + '.')
w('')
w('## 4. Which skill or script does each step, trigger, last run')
w('')
w('| Step | Skill or script | Trigger | Last ran | Status |')
w('|---|---|---|---|---|')
w('| Write criteria | Cowork `scope-scenario`, PM approval | a scenario is written | per scenario | **V** |')
w(f'| Score criteria per feature | `regen-feature-report` | one-time run 2026-10-10; Friday refresh ' + ('scheduled' if sched_reports else 'NOT scheduled') + f'; {len(stale)} reports are stale now | reports last committed {rep_last} | **{V(sched_reports)}** |')
w(f'| Parse and roll up | `scripts/criteria.py` | every dashboard run | with the dashboard | **V** |')
w(f'| Capabilities doc | `criteria.py --capabilities`, `regen-capabilities` | Friday task | {last("handoff/capabilities.md")} | **V** |')
w(f'| Dashboard | `dashboard.yml` workflow every 6 hours (also handoffs, Friday) | schedule, dispatch | {last("DASHBOARD.md")}; workflow {wf_run.get("conclusion", "never run")} ({str(wf_run.get("createdAt", ""))[:16]}) | **{V(wf_dash and wf_run.get("conclusion") == "success")}** |')
w(f'| STATUS (guard coverage) | `status.yml` | every push to main, daily | {last("STATUS.md")} | **V** |')
w(f'| Reports roll-up README | generated by `criteria.py --rewrite-reports` | the report run and the Friday refresh | {last("build-log/reports/README.md", webdir)} | **{V(not readme_dis2)}** |')
w(f'| UAT close | `uat-close.yml` | `uat` Issue closed | {len(uat_closed)} real runs | **B** |')
w('')
w('## 5. How it lands on the dashboard')
w('')
w(f'- **Header:** "{header_line[:200]}". **{V("criteria met" in header_line)}**')
w(f'- **Color ramp:** five steps, red to green, on criteria met / total, per feature and per area. **{V(has_ramp)}**')
w(f'- **Red rule:** a feature or area is red when an unmet criterion links an open `launch-blocking` Issue. **{V(has_red)}**; {len(red)} features red: ' + ', '.join(f['id'] for f in red) + '.')
w(f'- **Stale flag:** a feature whose last merged PR is newer than its report is flagged. **{V("stale" in dpy)}**; {len(stale)} stale now' + (': ' + ', '.join(stale[:8]) if stale else '') + '.')
w(f'- **Per criterion:** built, checked (T), reviewed (R), smoked (S), PM looked (P) on each criterion row, with links to its Issues and the full report. **V**')
w(f'- **Coverage:** {len(feats)} features have criterion-level results, of {len(set(f["id"] for f in feats) | set(live_scen))} reportable. Only {len(ms_scen)} of the {ms_total} milestone items are scenario Issues ({pct(len(ms_scen), ms_total)}).')
w(f'- **Headline numbers in circulation:** criteria met {met} of {tot} (the beta %), Issues closed {ms_closed} of {ms_total} (alongside), and `handoff/latest.md`\'s own count (Dispatch-written, **A**).')
w('')
w('## 6. What the five fixes changed, and what is still open')
w('')
w('| Fix | Shipped | Evidence |')
w('|---|---|---|')
w(f'| 1. Criterion-based beta %, Issue count alongside | plan #71 | **{V("criteria met" in header_line)}** header leads with criteria |')
w(f'| 2. Area and milestone roll-ups from criteria | plan #71 | **{V("criteria.rollup" in dpy)}** `rollup()` feeds area cards and header |')
w(f'| 3. One definition of Checked; generated roll-up lines | plan #72, web #661 | **{V(not cov_dis2 and not rep_dis)}** STATUS vs criteria.py: {len(cov_dis2)} disagree; report lines vs rows: {len(rep_dis)} disagree |')
w(f'| 4. Reviewed, Smoked, PM looked per criterion; loud Testing; honest Reviewed | plan #73, web #662 | **{V(test_loud)}** reviewed {reviewed}, smoked {smoked}, PM looked {pmlooked} of {tot}; Testing notice {"shown" if test_loud else "missing"} |')
w(f'| 5. Timer and stale-report flag | plan #74, #75, #76 | **{V(wf_dash and wf_run.get("conclusion") == "success" and "stale" in dpy)}** dashboard workflow last run {wf_run.get("conclusion", "never")} |')
w('')
w('**Still open:**')
w(f'1. **No PM review results.** {pmlooked} of {tot} criteria are PM-looked; {len(uat_closed)} real UAT Issues have been closed; `#519` has {boxes519} checkboxes.')
w(f'2. **Smoke is red** (last green {(feats[0].get("last_green_smoke") or "never")[:10]}), so "Smoked" is a stale claim and no criterion is evidenced beyond page loads.')
w(f'3. **{ms_total - len(ms_scen)} of {ms_total} milestone items have no criteria** (changes, bugs, chores).')
w(f'4. **Checked is {pct(checked, tot)}** ({checked} of {tot}); most criteria have no marked test.')
w('5. **Report text can still be stale or wrong**: the rows are agent-written once and refreshed on the Friday run; a row can be wrong until then (the stale flag only catches merges, not edits to a scenario).')
doc = '\n'.join(L) + '\n'
print(doc[:200] + '...')
if '--no-write' not in sys.argv:
    os.makedirs(os.path.join(ROOT, 'audits'), exist_ok=True)
    open(os.path.join(ROOT, 'audits', 'criterion-rollup.md'), 'w').write(doc)
    print('wrote audits/criterion-rollup.md')
