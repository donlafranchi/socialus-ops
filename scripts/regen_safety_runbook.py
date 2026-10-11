#!/usr/bin/env python3
"""Regenerates runbooks/staff-safety.md from the moderation rulings (F078, F100, F101, F102 in socialus-plan) so the runbook is
generated, not maintained. The steps are this script's template; every ruling it cites is read live and quoted, and a hash of
the cited rulings is stamped in the file. `--check` fails when a cited ruling has changed since the file was written.
Usage: python3 scripts/regen_safety_runbook.py [--check] [--no-write]"""
import hashlib, os, re, sys
from datetime import date
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from score_lib import PROJECTS, ROOT

PLAN = os.path.join(PROJECTS, 'socialus-plan')
OUT = os.path.join(ROOT, 'runbooks', 'staff-safety.md')


def clean(t):
    """This repo is public: no personal names. The rulings say Don; the runbook says the PM."""
    return re.sub(r"\bDon\b", 'the PM', re.sub(r"\bDon's\b", "the PM's", t))


def scenario(fid):
    return open(os.path.join(PLAN, 'planning', f'scenario-{fid}.md')).read()


def crit(fid, n):
    sec = scenario(fid).split('## Acceptance', 1)[1].split('\n## ', 1)[0]
    m = re.search(rf'^{n}\. (.*(?:\n(?!\d+\. ).*)*)', sec, re.M)
    if not m:
        raise SystemExit(f'{fid} criterion {n} not found')
    t = re.sub(r'\*\*|\*|`', '', m.group(1)).strip()
    return clean(re.sub(r'\s+', ' ', t))


def tiers():
    sec = scenario('F101').split('### The severity scale', 1)[1].split('\n###', 1)[0]
    return [tuple(c.strip() for c in l.strip('|').split('|')) for l in sec.split('\n') if re.match(r'\| [1-4] \|', l)]


def decision(prefix):
    for l in open(os.path.join(PLAN, 'DECISIONS.md')):
        if l.startswith('- **' + prefix):
            return clean(re.sub(r'\*\*|`|\[binds[^\]]*\]', '', l[2:]).strip())
    raise SystemExit(f'decision {prefix} not found')

CITED = [('F078', 5), ('F078', 8), ('F100', 12), ('F102', 9), ('F102', 10), ('F102', 14), ('F101', 13)]
rulings = {k: crit(*k) for k in CITED}
child = decision('2026-10-06 — Apparent child sexual abuse material')
stamp = hashlib.sha256(('\n'.join(rulings[k] for k in CITED) + child + str(tiers())).encode()).hexdigest()[:12]

if '--check' in sys.argv:
    cur = re.search(r'rulings-hash: (\w+)', open(OUT).read()).group(1) if os.path.exists(OUT) else None
    if cur != stamp:
        print(f'staff-safety.md is stale: rulings hash {cur} but the rulings now hash to {stamp}. Run regen_safety_runbook.py and re-read the steps.')
        sys.exit(1)
    print('staff-safety.md matches the rulings it cites.')
    sys.exit(0)

T = tiers()
q = lambda f, n: f'*{f} criterion {n}:* {rulings[(f, n)]}'
L = []
w = L.append
w('# Staff safety runbook')
w('')
w(f'<!-- generated {date.today().isoformat()} by scripts/regen_safety_runbook.py; rulings-hash: {stamp}; never hand-edited -->')
w('')
w(f'**Generated {date.today().isoformat()} from the moderation rulings (F078, F100, F101, F102 and the child-safety decision of 2026-10-06). Not legal advice; counsel reviews it before launch.** Read it on your phone: find the tier, do the numbered steps, stop.')
w('')
w('## Before anything')
w('')
w('- **You are never the last line of defence for your own wellbeing.** If an item upsets you, stop, step away, and come back later. Nothing here needs speed except tier 1, and tier 1 needs care more than speed.')
w('- **Hidden is already done.** The system hides reported content at once, tier 1 and threats regardless of any setting. Your job is the decision and the record, not the rescue.')
w('- **Never copy, download, screenshot, forward, message or post abusive material, even to report it.** Describe it in words in your report. (IFTAS, a nonprofit for social-web moderators, says to describe it, not store it; Thorn says never to share it even to report it.)')
w('- **If anyone is in danger right now, call 911.** The platform is not an emergency service.')
w('')
w('## The four tiers')
w('')
w('| Tier | Name | What lands here |')
w('|---|---|---|')
for t in T:
    w(f'| {t[0]} | {t[1]} | {t[2]} |')
w('')
w('Tier is the highest among a row\'s open reports. You see it as a badge on the **Posts** page (operators only). Thumbnails for tiers 1 to 3 are blurred until pressed and held.')
w('')
w('## Tier 1: child safety or illegal (apparent child sexual abuse material, CSAM)')
w('')
w('**What the system did for you:** hid it at any bar, stopped all AI processing of it (suspected tier 1 is never sent to an AI provider), checked any image against known-CSAM hashes first, and sent you a text. It never restores itself and never goes back to the poster for an answer.')
w('')
w('1. **Do not open it unless you must.** The text and the row tell you why it is here. View only as much as you need to decide that it is apparent child abuse, once, then stop. Do not zoom, save, or show anyone.')
w('2. **Do not delete it.** The law requires keeping reported content, in a secure place with limited access, for a year after you report it (18 U.S.C. 2258A, law.cornell.edu/uscode/text/18/2258A). Leave it hidden where it is. If it is not already hidden, hide it (Remove), then do not touch it again.')
w('3. **Report it to NCMEC as soon as reasonably possible. Do not wait for the Friday batch.** During beta, use NCMEC\'s public CyberTipline form at **report.cybertip.org**, or call **1-800-THE-LOST (1-800-843-5678)**, 24 hours. The public form cannot take images or video: write what it is, the account, the page address, and the times, in words.')
w('4. **Write down the report number** NCMEC gives you on the row, with the date and time. Keep that record.')
w('5. **Do not contact the poster, the reporter or anyone else about it.** Do not investigate, try to identify anyone, or confront anyone.')
w('6. **Never Approve it.** Approving tier 1 takes an extra confirm on purpose; if you are unsure, do not approve.')
w('7. **Look after yourself.** Take a break before the next row.')
w('')
w('*Rulings this comes from:*')
w(f'- {child}')
w(f'- {q("F100", 12)}')
w(f'- {q("F078", 8)}')
w(f'- {q("F102", 14)}')
w(f'- {q("F101", 13)}')
w('')
w('**Changes at entity setup and at production launch** (a dated reminder is on the dashboard\'s launch checklist and in the Friday report): register SocialUs with the CyberTipline, switch off the manual form, enable Cloudflare CSAM scanning. Entity specifics live in `socialus-legal`, not here.')
w('')
w('## Tier 2: threats and harassment')
w('')
w('**What the system did for you:** a threat of harm hides regardless of any bar and texts you at once. Harassment and violence hide at the current bar and wait in the batch.')
w('')
w('1. **If someone may be in danger now, call 911 first**, then come back.')
w('2. **Read the row:** the content, who reported it and why, the AI suggestion (shown beside it; it changes nothing in beta), and the poster\'s answer if there is one.')
w('3. **Decide with one tap:** Remove keeps it down; Approve restores it. A threat of harm is not approved without a good reason written on the row.')
w('4. **For a credible threat, keep the record:** leave the content preserved, note the account and the times, and tell the PM. Whether to contact police is a judgement for the PM and counsel; do not promise anyone a result.')
w('5. **Do not message the poster yourself.** The poster is told the category and the reporter\'s reason in the app, and gets one answer (fix and repost, or say the report is wrong).')
w('')
w('*Rulings:*')
w(f'- {q("F078", 5)}')
w(f'- {q("F102", 9)}')
w(f'- {q("F102", 10)}')
w('')
w('## Tier 3: sensitive or adult')
w('')
w('1. **Open the row; the picture is blurred until you press and hold.**')
w('2. **Judge against the rules:** nudity, and sensitive content such as animals and pets or anyone who cannot fend for themselves.')
w('3. **Remove or Approve.** One tap or one swipe (right approves, left removes). Undo is there for five seconds.')
w('4. **If you see anything that looks like a child in a sensitive situation, stop and treat it as tier 1.**')
w('')
w('## Tier 4: spam and other')
w('')
w('1. **Skim, then Approve or Remove.** These are the quickest rows.')
w('2. **Beta only:** the system restores a tier 4 row by itself, but only when the poster answered, both AI reads say approve at 95% or more, nothing looks like coordinated reporting, and the test set has cleared its targets. Anything else waits for you.')
w('')
w('## Tuesday to Thursday')
w('')
w('Nobody is expected midweek. Tiers 2 to 4 stay hidden and wait for the Friday to Monday batch. **Only tier 1 and a threat of harm text you.** Even then the expectation is care, not same-day heroics, except that a tier 1 report to NCMEC should not wait for the batch.')
w('')
w('## Not decided here')
w('')
w('- **Counsel review:** whether the plan\'s own reporting target meets "as soon as reasonably possible", and whether the preservation steps hold up. The public ruling already says counsel is asked.')
w('- **Not verified in this runbook:** NCMEC\'s current provider registration steps (its page would not load for the research; confirm with NCMEC), and an official "do not forward" wording from NCMEC or the Department of Justice (the closest official line is NCMEC\'s Take It Down FAQ, which tells people not to download or share explicit images).')
w('- **Planned:** a link to this page from the admin reports page.')
w('')
doc = '\n'.join(L) + '\n'
print(doc[:160] + '...')
if '--no-write' not in sys.argv:
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w').write(doc)
    print('wrote runbooks/staff-safety.md, rulings-hash', stamp)
