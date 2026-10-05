#!/usr/bin/env bash
# Fails on: missing `status` in planning/, any root .md outside the eight, any
# link to a path that doesn't exist, a scenario whose SPEC runs over 40 lines, a
# scenario section outside Story/Acceptance/Why/Not this, an absolute cited
# by a slug that no longer exists, or a marker the markers checker rejects. Run
# from the repo root.
#
# One script for both repos. In the method repo (ops-pattern) the project
# checks find nothing to check and the fixtures still prove the checkers; in a
# project repo (socialus-plan, which vendors this copy) everything runs. The
# process absolutes live in the method repo, so a project finds them there.
#
# `## Why` (added 2026-09-17) carries rationale — why this shape, what was
# rejected, how it relates to a neighbouring scenario. It exists because 12 of
# 37 scenarios already carried exactly that content under a dozen different
# ad-hoc headings, and deleting it to satisfy a linter would have destroyed the
# reasoning behind ratified decisions. It is NOT counted toward the 40 lines:
# the cap exists to keep a SPEC small enough to hold in your head, and rationale
# is not spec. A scenario whose Story + Acceptance + Not this exceeds 40 lines
# is still two scenarios, which is the rule PIPELINE.md states.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

fail=0

if [ -f process/ABSOLUTES.md ]; then
  METHOD="$ROOT"
else
  METHOD=""
  for c in "${METHOD_REPO:-}" "$ROOT/../ops-pattern" "$HOME/Projects/ops-pattern"; do
    [ -n "$c" ] && [ -f "$c/process/ABSOLUTES.md" ] && { METHOD="$(cd "$c" && pwd)"; break; }
  done
  [ -n "$METHOD" ] || { echo "lint: no ops-pattern checkout found — the process absolutes live there; set METHOD_REPO"; exit 1; }
fi
absolutes="$METHOD/process/ABSOLUTES.md"
[ -f product/ABSOLUTES.md ] && absolutes="$absolutes product/ABSOLUTES.md"

# 1. Every planning/*.md carries a status field.
for f in planning/*.md; do
  [ -f "$f" ] || continue
  if ! grep -q '^status:' "$f"; then
    echo "lint: missing 'status:' frontmatter — $f"
    fail=1
  fi
done

# 1b. Every planning/scenario-*.md keeps its SPEC under 40 lines and uses only
#     the four allowed sections, in any subset. `## Why` is rationale and is
#     excluded from the count — see the note at the top of this file.
for f in planning/scenario-*.md; do
  [ -f "$f" ] || continue
  spec=$(awk '/^## Why$/{skip=1; next} /^## /{skip=0} !skip' "$f" | wc -l | tr -d ' ')
  if [ "$spec" -gt 40 ]; then
    echo "lint: scenario spec over 40 lines ($spec, excluding ## Why) — $f"
    fail=1
  fi
  bad=$(grep -E '^## ' "$f" | grep -Ev '^## (Story|Acceptance|Why|Not this)$')
  if [ -n "$bad" ]; then
    echo "lint: scenario has a section outside Story/Acceptance/Why/Not this — $f"
    echo "$bad" | sed 's/^/  /'
    fail=1
  fi
done

# 2. Root .md files are only the five listed here, plus the generated ones —
#    README.md (scripts/view.sh) and PLATFORM-*.md (scripts/markers.py platform),
#    never hand-edited, so not link-checked below.
allowed="CLAUDE.md STATUS.md ROADMAP.md DECISIONS.md IMAGINE.md README.md PLATFORM-IOS.md PLATFORM-ANDROID.md"
for f in *.md; do
  [ -f "$f" ] || continue
  case " $allowed " in
    *" $f "*) ;;
    *)
      echo "lint: root .md outside the five (+ generated README.md, PLATFORM-*.md) — $f"
      fail=1
      ;;
  esac
done

# 3. Every relative markdown link in root docs and planning/*.md resolves
#    to a file that exists.
check_links() {
  local f="$1"
  local dir
  dir="$(dirname "$f")"
  grep -oE '\]\([^) ]+\)' "$f" | sed -E 's/^\]\((.*)\)$/\1/' | while read -r link; do
    case "$link" in
      http://*|https://*|mailto:*|\#*) continue ;;
    esac
    link="${link%%#*}"
    [ -z "$link" ] && continue
    target="$dir/$link"
    if [ ! -e "$target" ]; then
      echo "lint: broken link in $f -> $link"
      echo "__FAIL__"
    fi
  done
}

for f in CLAUDE.md STATUS.md ROADMAP.md DECISIONS.md IMAGINE.md process/*.md planning/*.md templates/*.md; do
  [ -f "$f" ] || continue
  out="$(check_links "$f")"
  if [ -n "$out" ]; then
    echo "$out" | grep -v '__FAIL__'
    fail=1
  fi
done

# 4. Every bracketed absolute-slug citation resolves to a heading in one of the
#    two ABSOLUTES files. This is the point of slugs: a renamed or deleted
#    absolute breaks the build instead of leaving a citation that reads fine and
#    points at nothing. DECISIONS.md is exempt: its older lines cite absolutes
#    by number, and the 2026-09-16 line there maps those numbers to these slugs.
slugs="$(grep -hoE '^### [a-z][a-z0-9-]+$' $absolutes | sed 's/^### //')"
for hit in $(grep -roE '\[[a-z][a-z0-9]*(-[a-z0-9]+)+\]' --include='*.md' --exclude=DECISIONS.md --exclude-dir=fixtures . | sort -u); do
  slug="${hit##*:[}"; slug="${slug%]}"
  if ! printf '%s\n' "$slugs" | grep -qx "$slug"; then
    echo "lint: [$slug] cites an absolute that does not exist — ${hit%%:*}"
    fail=1
  fi
done

# 5. Markers (process/LIVING-DOCS.md in ops-pattern): open
#    questions, guard claims (full or partial), decision bindings and whether a
#    code-binding ruling names its work, platform needs, accepted-risk dates, and
#    the generated files they build. The checker proves itself first, every run
#    ([guard-proves-itself]): it must reject every bad fixture and pass every
#    good one, or it is inert and this lint fails rather than reporting a clean
#    repo it never really checked.
fx=scripts/fixtures/markers
mk() { MARKERS_PLANNING="$fx/planning" python3 scripts/markers.py "$@"; }
EXPECT_BAD=26 EXPECT_RISKS=4 EXPECT_REP=8 EXPECT_PLAT=10
got=$(mk lint "$fx/open-question-bad.md" "$fx/guards-bad.md" "$fx/binds-bad/DECISIONS.md" "$fx/gating-bad/scenario-F998.md" | grep -c '^markers:')
[ "$got" -eq "$EXPECT_BAD" ] || { echo "lint: marker checker is inert — rejected $got of $EXPECT_BAD bad fixture lines"; fail=1; }
got=$(mk risks "$fx/risks-bad" | grep -c '^markers:')
[ "$got" -eq "$EXPECT_RISKS" ] || { echo "lint: accepted-risk checker is inert — rejected $got of $EXPECT_RISKS bad fixtures"; fail=1; }
got=$(MARKERS_PLANNING="$fx/replaces-bad/planning" python3 scripts/markers.py lint "$fx/replaces-bad/DECISIONS.md" | grep -c '^markers:')
[ "$got" -eq "$EXPECT_REP" ] || { echo "lint: replaces/evidence checker is inert — rejected $got of $EXPECT_REP bad fixtures"; fail=1; }
MARKERS_PLANNING="$fx/replaces-good/planning" python3 scripts/markers.py lint "$fx/replaces-good/DECISIONS.md" >/dev/null ||
  { echo "lint: replaces/evidence checker rejects the good fixture"; fail=1; }
got=$(mk lint "$fx"/platform-bad/product/*.md "$fx"/platform-bad/planning/*.md | grep -c '^markers:')
[ "$got" -eq "$EXPECT_PLAT" ] || { echo "lint: platform marker checker is inert — rejected $got of $EXPECT_PLAT bad fixtures"; fail=1; }
mk lint "$fx"/platform-good/product/*.md "$fx"/platform-good/planning/*.md >/dev/null ||
  { echo "lint: platform marker checker rejects the good fixture"; fail=1; }
cov=$(MARKERS_SOURCES="$fx/good.md" mk coverage F999; MARKERS_SOURCES="$fx/good.md" mk coverage --summary F999)
echo "$cov" | grep -q '^- \*\*1\*\* — \[' && echo "$cov" | grep -q '^- \*\*2\*\* — \*\*partial\*\*' &&
  echo "$cov" | grep -q '1 of 2 covered · \*\*partial: 2\*\*' ||
  { echo "lint: coverage map is inert — it does not tell a partial claim from a full one"; fail=1; }
mk lint "$fx/good.md" "$fx/binds-good/DECISIONS.md" >/dev/null && mk risks "$fx/risks-good" >/dev/null ||
  { echo "lint: marker checker rejects a good fixture"; fail=1; }
# The "never" lint (Don, 2026-09-30: the only approved "never" is "never extractive").
# The checker proves itself on every run; the scan of real docs is off until Don approves
# the rewording. Turn it on with NEVER_LINT=1.
got=$(python3 scripts/never.py scripts/fixtures/never/bad.md | grep -c '^never:')
[ "$got" -eq 3 ] || { echo "lint: never checker is inert — rejected $got of 3 bad fixture uses"; fail=1; }
python3 scripts/never.py scripts/fixtures/never/good.md >/dev/null || { echo "lint: never checker rejects the good fixture"; fail=1; }
if [ "${NEVER_LINT:-0}" = "1" ] && ! out="$(python3 scripts/never.py)"; then
  echo "$out" | sed 's/^/lint: /'; fail=1
fi
if [ -f DECISIONS.md ] && ! out="$(python3 scripts/markers.py lint)"; then
  echo "$out" | sed 's/^/lint: /'
  fail=1
fi

if [ "$fail" -ne 0 ]; then
  echo "lint: FAILED"
  exit 1
fi
echo "lint: clean"
