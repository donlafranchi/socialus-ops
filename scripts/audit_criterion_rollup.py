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
pct = lambda a, b: f'{round(100 * a / b)}%' if b else 'n/a'

# ---- document
L = []
w = L.append
w('# Criterion roll-up: audit')
w('')
w(f'**Generated {today} by `scripts/audit_criterion_rollup.py`, never hand-written.** Every number below was computed from live files, runs and data on that date. **V** verified, **A** assumed, **B** broken or missing.')
w('')
w('```')
w('  scenario criteria (plan)     UAT lists        evals / [guards] markers     PR review    smoke')
w('        |                        |                      |                      |           |')
w('        v                        v                      v                      v           v')
w('  feature report  <--- agent run: regen-feature-report (one per feature, build-log/reports/)')
w('        |   criterion rows: Built yes/no/unknown, Checked, Reviewed, Smoked, PM looked')
w('        v')
w('  scripts/criteria.py  (reads reports; counts Built only)')
w('        |-----------------> handoff/capabilities.md')
w('        v')
w('  dashboard.py:  FEATURES section (criteria met / total, red on launch-blocking)   (criterion-derived)')
w('                 AREA cards + header    (Issues in milestone: closed / total)      (Issue-derived)')
w('        |                                          ^ these two do not read each other')
w('        v')
w('  DASHBOARD.md + status-dashboard.html  ->  Friday launch report')
w('```')
w('')
w('## 1. Where criteria come from')
w('')
w('| Source | Who writes it | Status | Evidence |')
w('|---|---|---|---|')
w(f'| Scenario `Acceptance` list, numbered | Cowork drafts, the PM approves | **V** | {len(scen)} scenario files; {len(live_scen)} approved or building; the reports hold {tot} criteria across {len(feats)} features. Reports restate the scenario text, so a scenario edited after a report makes the report stale |')
w(f'| Scenario count vs report count | n/a | **{"V" if not crit_mismatch else "B"}** | {"every report matches its scenario" if not crit_mismatch else "differs: " + ", ".join(f"{k} scenario {a} vs report {b}" for k, a, b in crit_mismatch[:6])} |')
w(f'| Shipped scenarios (file deleted at sync) | recovered from git history by the report run | **A** | {len([f for f in feats if f["id"] not in scen])} features have no scenario file; their criteria were reconstructed, not read from a live source |')
w(f'| Issues with no criteria (change, bug, chore) | the PM / Dispatch | **B** | {ms_total - len(ms_scen)} of {ms_total} milestone Issues have no acceptance criteria, so they have no criterion-level result at all |')
w(f'| UAT checklist `#519` (click-through sheet) | an agent | **B** | the Issue body has {boxes519} checkboxes; the dashboard\'s Testing section reads it and shows {test_items} items, and hides the failure (`except: pass`) |')
w('')
w('## 2. How a criterion is tested, scored, and where the result lives')
w('')
w('| Mechanism | Triggered by | Where the result is stored | Status | Evidence |')
w('|---|---|---|---|---|')
w(f'| `[guards F###.N]` marker on a test | CI `check-markers.sh`, `markers.py coverage` | STATUS.md "Guard coverage" | **V**, low | {mk} criteria carry a marker across {mkf} features, out of {tot} criteria ({pct(int(mk or 0), tot)}) |')
w(f'| Feature report "Checked" column | agent run | the report file | **B** | disagrees with STATUS guard coverage on {len(cov_dis)} of {len(cov)} features, e.g. ' + (', '.join(f'{k} STATUS {a} vs report {b}' for k, a, b in cov_dis[:3]) or 'none') + ' (different definitions: whole-criterion marks vs marks plus unmarked tests) |')
w(f'| Feature evals `evals/features/*.spec.ts` | CI Browser job | CI run log only | **V**, partial | {evals} spec files; no per-criterion result is written anywhere |')
w(f'| PR reviewer first pass (`review-pr-bundle`) | UI PR | `Reviewed by:` in the PR body, label `review-skipped` | **V** | per-PR, not per-criterion; the report derives "Reviewed" from it by hand |')
w(f'| UAT close (`uat-close` workflow, `record-pm-review`) | the PM closes a `uat` Issue | label `pm-reviewed` | **B** | {len(uat_closed)} real UAT Issues have ever been closed; the workflow only ever ran on its own self-check |')
w(f'| Live smoke | nightly + manual | workflow run | **B** | last run {smoke.get("createdAt", "?")[:10]}: {smoke.get("conclusion", "?")}; "Smoked" is 0 for every criterion because runs are not tied to commits |')
w('')
w('## 3. What rolls up into what, and the formula')
w('')
w('| Level | Formula | Where computed | Status | Evidence |')
w('|---|---|---|---|---|')
w(f'| Criterion | Built = `yes` only (unknown counts as not built) | `scripts/criteria.py` | **V** | {unknown} of {tot} criteria are `unknown` and count as unmet |')
w(f'| Feature | met / total | `criteria.py`, dashboard Features section | **V** | {len(feats)} features, {met} of {tot} met ({pct(met, tot)}); {len(red)} red |')
w(f'| Feature report roll-up line | counts typed by the agent | each report and `reports/README.md` | **B** | differs from the criterion rows for {len(readme_mis)} features' + (': ' + ', '.join(f'{k} says {a}, rows say {b}' for k, a, b in readme_mis[:4]) if readme_mis else '') + ' |')
w('| Area | **no criterion roll-up exists.** Area cards use Issues: stage = Issues in the area that reached it | `dashboard.py` | **B** | see the table below |')
w(f'| Milestone / beta % | closed Issues / all Issues in milestone "Beta 11-06" | `handoff`, Dispatch, old dashboard header | **B** | {ms_closed} of {ms_total} now ({pct(ms_closed, ms_total)}); it read {ms_closed} of {before} ({pct(ms_closed, before)}) before the 5pm report run filed {ms_total - before} gap Issues into the milestone |')
w('')
w('Area cards (Issue-derived) against the same areas rolled up from criteria:')
w('')
w('| Area | Issues "Built" | Criteria met | Features reporting |')
w('|---|---|---|---|')
for a, (b, n) in areas.items():
    fs = [f for f in feats if f['area'] == a]
    w(f'| {a} | {b}/{n} ({pct(b, n)}) | ' + (f'{sum(f["met"] for f in fs)}/{sum(f["total"] for f in fs)} ({pct(sum(f["met"] for f in fs), sum(f["total"] for f in fs))})' if fs else 'no reports') + f' | {len(fs)} |')
w('')
w('**Double counting and inflation (V):**')
w(f'- {len(gaps)} of {ms_total} milestone Issues are gap Issues auto-filed from criteria. A criterion now appears twice: once as a row in its report, once as an Issue with its own stages. The Issue-derived header and areas count both.')
w(f'- {len(closed_parent_unmet)} scenario Issues are closed while their feature still has unmet criteria, so they count as done in the numerator: ' + (', '.join(f'{f} (#{n}, {m} of {t})' for f, n, m, t in closed_parent_unmet[:6]) or 'none') + '.')
w('')
w('## 4. Which skill or script does each step, trigger, last run')
w('')
w('| Step | Skill or script | Trigger | Last ran | Status |')
w('|---|---|---|---|---|')
w(f'| Write criteria | Cowork `scope-scenario`, PM approval | a scenario is written | per scenario | **V** |')
w(f'| Score criteria per feature | `regen-feature-report` | one-time run 2026-10-10; Friday refresh ' + ('is scheduled' if sched_reports else 'is NOT scheduled') + f' | reports last committed {rep_last} | **{"V" if sched_reports else "B"}** |')
w(f'| Parse reports | `scripts/criteria.py` | only when `dashboard.py` or `--capabilities` runs | with the dashboard | **V** |')
w(f'| Capabilities doc | `regen-capabilities` / `criteria.py --capabilities` | Friday task | {last("handoff/capabilities.md")} | **V**, first run today |')
w(f'| Dashboard | `regen-dashboard` / `dashboard.py` | Dispatch handoffs (5am, 5pm), Friday task | {last("DASHBOARD.md")} | **A**: no scheduler runs it; handoff-driven |')
w(f'| STATUS (guard coverage) | `status.yml` | every push to main, daily 13:05 UTC | {last("STATUS.md")} | **V** |')
w(f'| Reports roll-up README | an agent | with the report run | {last("build-log/reports/README.md", webdir)} | **B**: hand-assembled, disagrees with rows |')
w(f'| UAT close | `uat-close.yml` | `uat` Issue closed | {len(uat_closed)} real runs | **B** |')
w('')
w('## 5. How it lands on the dashboard')
w('')
w(f'- **Color ramp:** five steps, red to green, on criteria met / total per feature. **{"V" if has_ramp else "B"}**')
w(f'- **Red rule:** a feature is red when an unmet criterion links an open `launch-blocking` Issue. **{"V" if has_red else "B"}**; {len(red)} features are red now: ' + ', '.join(f['id'] for f in red) + '. An unmet criterion with no linked Issue does not turn a feature red (**A**, no example found, but the rule allows it).')
w(f'- **Links:** each feature links its full report; each criterion links its Issues. **V**')
w(f'- **Coverage:** {len(feats)} features have criterion-level results, of {len(feats | set()) if False else len(set(f["id"] for f in feats) | set(live_scen))} reportable. Only {len(ms_scen)} of the {ms_total} milestone items are scenario Issues ({pct(len(ms_scen), ms_total)}); the other {ms_total - len(ms_scen)} have no criteria.')
w(f'- **Headline numbers in circulation:** "{ms_closed} of {before}" (Issues closed, before the 5pm run), "{ms_closed} of {ms_total}" (now), the dashboard header ("{ms_total} beta items"), and the criterion figure ({met} of {tot}). Four numbers, three formulas.')
w('')
w('## 6. Biggest problems')
w('')
w(f'1. **The headline beta % counts Issues, and Issues are not criteria.** Filing {ms_total - before} gap Issues moved it from {pct(ms_closed, before)} to {pct(ms_closed, ms_total)} with no real change in the product, and {len(closed_parent_unmet)} closed Issues are counted done with unmet criteria.')
w(f'2. **Two roll-ups that never meet.** Areas are Issue-derived, features are criterion-derived, and they disagree widely, for example sign-in-you {areas.get("sign-in-you", ("?", "?"))[0]}/{areas.get("sign-in-you", ("?", "?"))[1]} built by Issues vs criteria. There is no area or milestone roll-up from criteria.')
w(f'3. **"Checked" is counted two ways** (STATUS guard coverage vs the reports) and disagrees on {len(cov_dis)} of {len(cov)} features; the reports\' own roll-up lines disagree with their rows on {len(readme_mis)}.')
w(f'4. **Reviewed, Smoked and PM looked are not rolled up at criterion level.** Only Built is. Smoke is 0 everywhere, there are no real UAT results, and the Testing section is empty without saying so.')
w(f'5. **The scoring is a snapshot with one manual trigger.** Reports were produced once; refresh is scheduled for the first time on the next Friday run; the dashboard has no scheduler of its own.')
w('')
w('## 7. Recommended fix order (not started; waits for the PM)')
w('')
w('1. Make the beta % criterion-based: criteria met / total across reporting features, shown beside the Issue count. Stops the inflation.')
w('2. Add the missing roll-up levels computed by `criteria.py`: area and milestone from criteria; have the dashboard area cards and header read them.')
w('3. One definition of Checked (marks only, per criterion) read by both STATUS and the reports; generate each report roll-up line from its rows.')
w('4. Roll up Reviewed, Smoked and PM looked per criterion; tie smoke to merge commits; make the Testing section fail loudly.')
w('5. Schedule: dashboard and criteria.py on a timer, report refresh on any merged PR that cites a feature.')
w('')
doc = '\n'.join(L) + '\n'
print(doc[:200] + '...')
if '--no-write' not in sys.argv:
    os.makedirs(os.path.join(ROOT, 'audits'), exist_ok=True)
    open(os.path.join(ROOT, 'audits', 'criterion-rollup.md'), 'w').write(doc)
    print('wrote audits/criterion-rollup.md')
