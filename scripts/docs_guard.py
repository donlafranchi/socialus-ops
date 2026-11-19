#!/usr/bin/env python3
"""A markdown file must earn its place: it is listed in docs.tsv, or it fails.

  docs_guard.py check [--root DIR]

docs.tsv: path<TAB>why it is a file and not a store record<TAB>review-by YYYY-MM-DD (or - for none)
Fails when a tracked .md is unlisted, a listed file is missing, or a review-by date has passed.
Content that lives in the knowledge store is deleted from the repo; it is not listed here.
"""
import datetime, os, subprocess, sys

def tracked(root):
    out = subprocess.run(['git', '-C', root, 'ls-files', '*.md'], capture_output=True, text=True).stdout.split('\n')
    return [p for p in out if p and '/fixtures/' not in '/' + p]

def check(root, today=None):
    today = today or datetime.date.today()
    fails, listed = [], {}
    p = os.path.join(root, 'docs.tsv')
    for line in open(p) if os.path.exists(p) else []:
        if line.startswith('#') or not line.strip():
            continue
        f = line.rstrip('\n').split('\t')
        if len(f) < 3 or not f[1].strip():
            fails.append(f'docs.tsv: "{f[0]}" needs a reason and a review-by (or -)')
            continue
        listed[f[0]] = f[2].strip()
    files = tracked(root) if os.path.isdir(os.path.join(root, '.git')) else sorted(
        os.path.relpath(os.path.join(d, n), root) for d, _, ns in os.walk(root) for n in ns if n.endswith('.md'))
    for f in files:
        if f not in listed:
            fails.append(f'{f} is not in docs.tsv: put it in the knowledge store, or list it with why it must be a file')
    for f, rb in listed.items():
        if f not in files:
            fails.append(f'docs.tsv lists {f}, which does not exist')
        elif rb != '-':
            try:
                if datetime.date.fromisoformat(rb) < today:
                    fails.append(f'{f}: review-by {rb} has passed: is it in the store yet?')
            except ValueError:
                fails.append(f'{f}: review-by "{rb}" is not YYYY-MM-DD or -')
    return fails

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] != 'check':
        print(__doc__); sys.exit(2)
    root = sys.argv[sys.argv.index('--root') + 1] if '--root' in sys.argv else '.'
    fs = check(root)
    for f in fs:
        print(f'docs: {f}')
    sys.exit(1 if fs else 0)
