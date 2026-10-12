#!/usr/bin/env python3
"""Doc budgets (process/WHERE-THINGS-GO.md): no doc grows past its budget unrefined.

  budgets.py report [--root DIR]   docs at >=80% of their size budget, or past their age
  budgets.py check  [--root DIR]   lint: fails when an over-budget doc grew against the base,
                                   a dated note is past its age budget, or UNPLACED.md has an
                                   item older than 14 days, a line without its marker, or >20 items

Config: <root>/scripts/budgets.tsv (or <root>/budgets.tsv), `glob<TAB>KB<TAB>age-days`, first
match wins, `-` for none. A doc's frontmatter `budget: <KB>` overrides the size.
Base for "grew": $BUDGETS_BASE_DIR (a directory of base copies, for fixtures), else
`git merge-base origin/main HEAD` (HEAD~1 on main itself). No base: over budget only warns.
"""
import datetime, fnmatch, os, re, subprocess, sys

UNPLACED_DAYS, UNPLACED_MAX = 14, 20
DATE = re.compile(r'(20\d\d-\d\d-\d\d)')


def config(root):
    for p in (os.path.join(root, 'scripts', 'budgets.tsv'), os.path.join(root, 'budgets.tsv')):
        if os.path.exists(p):
            rows = []
            for line in open(p):
                line = line.rstrip('\n')
                if not line.strip() or line.startswith('#'):
                    continue
                g, kb, age = (line.split('\t') + ['-', '-'])[:3]
                rows.append((g, None if kb == '-' else float(kb), None if age == '-' else int(age)))
            return rows
    sys.exit(f'budgets: no budgets.tsv under {root}')


def tracked(root):
    try:
        out = subprocess.run(['git', 'ls-files', '*.md'], cwd=root, capture_output=True, text=True, check=True).stdout.split()
        if out:
            return out
    except Exception:
        pass
    return [os.path.relpath(os.path.join(d, f), root) for d, _, fs in os.walk(root) for f in fs if f.endswith('.md')]


def base_size(root, path):
    bd = os.environ.get('BUDGETS_BASE_DIR')
    if bd:
        p = os.path.join(bd, path)
        return os.path.getsize(p) if os.path.exists(p) else 0
    git = lambda *a: subprocess.run(['git', *a], cwd=root, capture_output=True, text=True)
    head = git('rev-parse', 'HEAD').stdout.strip()
    mb = git('merge-base', 'origin/main', 'HEAD').stdout.strip()
    if not head or not mb:
        return None
    base = 'HEAD~1' if mb == head else mb
    r = git('cat-file', '-s', f'{base}:{path}')
    return int(r.stdout) if r.returncode == 0 else 0


def budget_for(rows, path, text):
    m = re.search(r'^budget:\s*([\d.]+)\s*$', text[:600], re.M)
    for g, kb, age in rows:
        if fnmatch.fnmatch(path, g):
            return (float(m.group(1)) if m else kb), age
    return (float(m.group(1)) if m else None), None


def unplaced(path, today):
    errs, items = [], 0
    for n, line in enumerate(open(path), 1):
        if not line.startswith('- '):
            continue
        items += 1
        m = re.search(r'\[unplaced raised=(20\d\d-\d\d-\d\d) owner=[a-z-]+\]', line)
        if not m:
            errs.append(f'{path}:{n}: an item needs its [unplaced raised=YYYY-MM-DD owner=…] marker')
        elif (today - datetime.date.fromisoformat(m.group(1))).days > UNPLACED_DAYS:
            errs.append(f'{path}:{n}: unplaced for more than {UNPLACED_DAYS} days — place it, make it an open question, IMAGINE.md, an Issue, or delete it')
    if items > UNPLACED_MAX:
        errs.append(f'{path}: {items} items, over {UNPLACED_MAX} — drain it')
    return errs


def run(mode, root):
    rows, today = config(root), datetime.date.today()
    fails, warns = [], []
    for path in sorted(tracked(root)):
        if '/fixtures/' in f'/{path}' and root == '.':
            continue
        full = os.path.join(root, path)
        if not os.path.exists(full):
            continue
        if os.path.basename(path) == 'UNPLACED.md':
            fails += unplaced(full, today)
            continue
        text = open(full, errors='replace').read()
        kb, age = budget_for(rows, path, text)
        size = os.path.getsize(full)
        if age is not None and (d := DATE.search(os.path.basename(path))):
            days = (today - datetime.date.fromisoformat(d.group(1))).days
            if days > age:
                fails.append(f'{path}: dated note is {days} days old, past its {age}-day budget — delete it once its result has a home')
        if kb is None:
            continue
        pct = size / (kb * 1000)
        if pct >= 1:
            b = base_size(root, path)
            msg = f'{path}: {size/1000:.0f}k of a {kb:g}k budget ({pct:.0%})'
            (fails if b is not None and size > b else warns).append(msg + (' and it grew — condense it in this PR' if b is not None and size > b else ''))
        elif pct >= .8:
            warns.append(f'{path}: {size/1000:.0f}k of a {kb:g}k budget ({pct:.0%})')
    if mode == 'report':
        for m in fails + warns:
            print(m)
        return 0
    for m in fails:
        print(f'budgets: {m}')
    return 1 if fails else 0


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or a[0] not in ('report', 'check'):
        sys.exit(__doc__)
    root = a[a.index('--root') + 1] if '--root' in a else '.'
    sys.exit(run(a[0], root))
