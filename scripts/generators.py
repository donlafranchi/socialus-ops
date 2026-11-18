#!/usr/bin/env python3
"""Generators declare themselves: what a script makes, why, who reads it, and when it is needed.

  generators.py check [--root DIR]    lint: fails on a bad declaration; warns on outputs nobody reads

A script that writes files carries five comment lines (each starting with `#`) in its first 60 lines:

  GENERATES: path, glob, ...     what it writes (prefix `socialus-web:` for a file in another repo; not checked here)
  WHY: ...                       what the output is for
  READ BY: ...                   who or what reads it (a person, a script, a workflow)
  NEEDED WHEN: ...               the condition that makes running it worthwhile
  REVIEW BY: YYYY-MM-DD          a date to re-ask whether it is still needed

Fails (exit 1) when:
  - a *.py in scripts/ that writes a file has no GENERATES line (an undeclared generator)
  - a declaration is missing one of the five fields
  - REVIEW BY has passed
  - a declared output that exists is not marked `linguist-generated=true` in .gitattributes
  - a declared *.md output has no "generated" in its first 15 lines

Warns (does not fail) when:
  - nobody outside the generator and its own outputs mentions the output (checked across this repo and sibling
    checkouts such as socialus-plan and socialus-web, when present): a candidate to delete
  - a file under scores/, reports/, audits/ or packs/ is covered by no declaration (an orphan output)

The declarations live in the scripts, not in an index, so there is nothing to keep in step: a script that
stops declaring itself fails.
"""
import datetime, fnmatch, glob, os, re, sys

FIELDS = ['GENERATES', 'WHY', 'READ BY', 'NEEDED WHEN', 'REVIEW BY']
LINE = re.compile(r'^\s*#\s*(GENERATES|WHY|READ BY|NEEDED WHEN|REVIEW BY):\s*(.+?)\s*$')
WRITES = re.compile(r'''open\([^)]*['"]w['"]''')
ORPHAN_DIRS = ('scores', 'reports', 'audits', 'packs')
READ_EXT = ('.md', '.py', '.sh', '.ts', '.tsx', '.yml', '.yaml', '.tsv', '.json', '.cjs')
SKIP_DIRS = {'.git', 'node_modules', 'fixtures', '__pycache__', '.next'}


def declarations(root):
    """{script path: {field: text}} for every script under <root>/scripts that declares anything."""
    out = {}
    for p in sorted(glob.glob(os.path.join(root, 'scripts', '*.py')) + glob.glob(os.path.join(root, 'scripts', '*.sh'))):
        d = {}
        for line in open(p, errors='replace').read().split('\n')[:60]:
            m = LINE.match(line)
            if m and m.group(1) not in d:
                d[m.group(1)] = m.group(2)
        if d:
            out[p] = d
    return out


def gitattributes(root):
    pats = []
    p = os.path.join(root, '.gitattributes')
    if os.path.exists(p):
        for line in open(p):
            parts = line.split('#')[0].split()
            if len(parts) >= 2 and 'linguist-generated=true' in parts[1:]:
                pats.append(parts[0])
            elif len(parts) >= 2 and 'linguist-generated' in parts[1:]:
                pats.append(parts[0])
    return pats


def matches(rel, pats):
    return any(fnmatch.fnmatch(rel, pat) or fnmatch.fnmatch(os.path.basename(rel), pat) for pat in pats)


def outputs(root, text):
    """Local output files named by a GENERATES line; foreign ones (`repo:`) are skipped."""
    files = []
    for item in re.split(r',\s*', text):
        item = item.strip().strip('`')
        if not item or re.match(r'^[a-z0-9-]+:', item) or item.startswith('('):
            continue
        hits = glob.glob(os.path.join(root, item))
        files += [os.path.relpath(h, root) for h in hits if os.path.isfile(h)]
    return files


def text_files(base):
    for dp, dn, fn in os.walk(base):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in fn:
            if f.endswith(READ_EXT):
                yield os.path.join(dp, f)


def check(root, today=None):
    today = today or datetime.date.today()
    fails, warns = [], []
    decl = declarations(root)
    covered = []

    # undeclared generators: a *.py that writes a file and declares nothing
    for p in sorted(glob.glob(os.path.join(root, 'scripts', '*.py'))):
        src = open(p, errors='replace').read()
        if WRITES.search(src) and 'GENERATES' not in decl.get(p, {}):
            fails.append(f'{os.path.relpath(p, root)} writes files but declares no GENERATES (an undeclared generator)')

    gattr = gitattributes(root)
    sibling_roots = [os.path.abspath(root)]
    parent = os.path.dirname(os.path.abspath(root))
    for name in ('socialus-ops', 'socialus-plan', 'socialus-web'):
        cand = os.path.join(parent, name)
        if os.path.isdir(cand) and os.path.abspath(cand) not in sibling_roots:
            sibling_roots.append(os.path.abspath(cand))

    for p, d in decl.items():
        rel = os.path.relpath(p, root)
        if 'GENERATES' not in d:
            continue  # only comments that happen to look like fields; not a generator
        for f in FIELDS:
            if f not in d:
                fails.append(f'{rel} declares GENERATES but not {f}')
        rb = d.get('REVIEW BY')
        if rb:
            try:
                if datetime.date.fromisoformat(rb[:10]) < today:
                    fails.append(f'{rel}: REVIEW BY {rb[:10]} has passed: is it still needed?')
            except ValueError:
                fails.append(f'{rel}: REVIEW BY "{rb}" is not a YYYY-MM-DD date')
        outs = outputs(root, d['GENERATES'])
        covered += outs
        for o in outs:
            if not matches(o, gattr):
                fails.append(f'{o} (from {rel}) is not marked linguist-generated=true in .gitattributes')
            if o.endswith('.md'):
                head = '\n'.join(open(os.path.join(root, o), errors='replace').read().split('\n')[:15])
                if not re.search(r'generated', head, re.I):
                    fails.append(f'{o} (from {rel}) has no "generated" line in its first 15 lines')
        # does anyone read it? (warn only)
        names = set()
        for i in re.split(r',\s*', d['GENERATES']):
            i = i.strip().strip('`')
            if not i or re.match(r'^[a-z0-9-]+:', i):
                continue
            # a glob is found by its folder's name (reports/doc-garden/*.md -> doc-garden); a file by its own name
            names.add(os.path.basename(os.path.dirname(i)) if '*' in i else os.path.basename(i))
        names = {n for n in names if n}
        skip = {os.path.abspath(p)} | {os.path.abspath(os.path.join(root, o)) for o in outs}
        for n in sorted(names):
            seen = False
            for sr in sibling_roots:
                for tf in text_files(sr):
                    a = os.path.abspath(tf)
                    if a in skip or os.path.relpath(a, sr).split(os.sep)[0] in ORPHAN_DIRS:
                        continue
                    try:
                        if n in open(tf, errors='replace').read():
                            seen = True
                            break
                    except OSError:
                        continue
                if seen:
                    break
            if not seen and len(sibling_roots) > 1:
                warns.append(f'{n} (from {rel}) is mentioned nowhere else: a candidate to delete')

    # orphan outputs
    for top in ORPHAN_DIRS:
        for dp, dn, fn in os.walk(os.path.join(root, top)):
            for f in fn:
                r = os.path.relpath(os.path.join(dp, f), root)
                if r not in covered:
                    warns.append(f'{r} is covered by no GENERATES declaration (an orphan output)')
    return fails, warns


def main(argv):
    if not argv or argv[0] != 'check':
        print(__doc__)
        return 2
    root = '.'
    if '--root' in argv:
        root = argv[argv.index('--root') + 1]
    fails, warns = check(root)
    for f in fails:
        print(f'generators: {f}')
    if '--quiet' not in argv:
        for w in warns[:40]:
            print(f'generators (warning): {w}', file=sys.stderr)
        if len(warns) > 40:
            print(f'generators (warning): ... and {len(warns) - 40} more', file=sys.stderr)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
