#!/usr/bin/env bash
# Fails on: missing `status` in planning/, any root .md outside the eight, any
# link to a path that doesn't exist, a scenario whose SPEC runs over 40 lines, a
# scenario section outside Story/Acceptance/Why/Not this, a scenario from F103
# on that doesn't answer the value test, an absolute cited
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
#     the five allowed sections, in any subset. `## Why` (rationale), `## Rulings`
#     (the dated rulings that govern it, inline) and frontmatter are excluded from the count.
for f in planning/scenario-*.md; do
  [ -f "$f" ] || continue
  spec=$(awk 'NR==1 && /^---$/{fm=1; next} fm{if(/^---$/)fm=0; next} /^## (Why|Rulings)$/{skip=1; next} /^## /{skip=0} !skip' "$f" | wc -l | tr -d ' ')
  if [ "$spec" -gt 40 ]; then
    echo "lint: scenario spec over 40 lines ($spec, excluding ## Why and ## Rulings) — $f"
    fail=1
  fi
  bad=$(grep -E '^## ' "$f" | grep -Ev '^## (Story|Acceptance|Why|Not this|Rulings)$')
  if [ -n "$bad" ]; then
    echo "lint: scenario has a section outside Story/Acceptance/Why/Not this/Rulings — $f"
    echo "$bad" | sed 's/^/  /'
    fail=1
  fi
done

# 1c. The value test (Don, 2026-10-05): every scenario from F103 on answers its
#     six questions in `## Why`, one line each, led by these exact labels.
#     F102 and earlier are grandfathered — they were approved before the test.
VALUE_TEST_FROM=103
VALUE_TEST_LABELS=("Lives somewhere better?" "Only locals know?" "Gets people together?" "Stays fresh on its own?" "Who keeps it current?" "Better as more people join?")
value_test_missing() {
  local n why l
  n=$(basename "$1" | sed -nE 's/^scenario-F0*([0-9]+)\.md$/\1/p')
  [ -n "$n" ] && [ "$n" -ge "$VALUE_TEST_FROM" ] || return 0
  why=$(awk '/^## Why$/{on=1; next} /^## /{on=0} on' "$1")
  for l in "${VALUE_TEST_LABELS[@]}"; do
    printf '%s\n' "$why" | grep -qE "^- \*\*${l//\?/\\?}\*\* +[^ ]" || echo "$l"
  done
}
for f in planning/scenario-*.md; do
  [ -f "$f" ] || continue
  missing=$(value_test_missing "$f")
  if [ -n "$missing" ]; then
    echo "lint: scenario does not answer the value test in ## Why — $f"
    printf '%s\n' "$missing" | sed 's/^/  missing: /'
    fail=1
  fi
done
# It proves itself first ([guard-proves-itself]).
vt=scripts/fixtures/value-test
[ "$(value_test_missing "$vt/bad/scenario-F999.md" | wc -l | tr -d ' ')" -eq 2 ] ||
  { echo "lint: value-test check is inert — it should find 2 missing answers in the bad fixture"; fail=1; }
[ -z "$(value_test_missing "$vt/good/scenario-F999.md")" ] ||
  { echo "lint: value-test check rejects the good fixture"; fail=1; }
[ -z "$(value_test_missing "$vt/grandfathered/scenario-F050.md")" ] ||
  { echo "lint: value-test check does not grandfather a scenario before F$VALUE_TEST_FROM"; fail=1; }

# 2. Root .md files are only the five listed here, plus the generated ones —
#    README.md (scripts/view.sh), PLATFORM-*.md (scripts/markers.py platform) and
#    DASHBOARD.md (scripts/dashboard.py),
#    never hand-edited, so not link-checked below.
allowed="CLAUDE.md STATUS.md PRINCIPLES.md UNPLACED.md IMAGINE.md README.md PLATFORM-IOS.md PLATFORM-ANDROID.md DASHBOARD.md"
for f in *.md; do
  [ -f "$f" ] || continue
  case " $allowed " in
    *" $f "*) ;;
    *)
      echo "lint: root .md outside the five (+ generated README.md, PLATFORM-*.md, DASHBOARD.md) — $f"
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

for f in CLAUDE.md STATUS.md PRINCIPLES.md UNPLACED.md IMAGINE.md process/*.md planning/*.md templates/*.md; do
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
#    points at nothing.
slugs="$(grep -hoE '^### [a-z][a-z0-9-]+$' $absolutes | sed 's/^### //')"
for hit in $(grep -roE '\[[a-z][a-z0-9]*(-[a-z0-9]+)+\]' --include='*.md' --exclude-dir=fixtures . | sort -u); do
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
EXPECT_BAD=27 EXPECT_RISKS=4 EXPECT_REP=8 EXPECT_PLAT=10
got=$(mk lint "$fx/open-question-bad.md" "$fx/guards-bad.md" "$fx/binds-bad/PRINCIPLES.md" "$fx/binds-bad/scenario-F996.md" "$fx/gating-bad/scenario-F998.md" | grep -c '^markers:')
[ "$got" -eq "$EXPECT_BAD" ] || { echo "lint: marker checker is inert — rejected $got of $EXPECT_BAD bad fixture lines"; fail=1; }
got=$(mk risks "$fx/risks-bad" | grep -c '^markers:')
[ "$got" -eq "$EXPECT_RISKS" ] || { echo "lint: accepted-risk checker is inert — rejected $got of $EXPECT_RISKS bad fixtures"; fail=1; }
got=$(MARKERS_PLANNING="$fx/replaces-bad/planning" python3 scripts/markers.py lint "$fx/replaces-bad/PRINCIPLES.md" | grep -c '^markers:')
[ "$got" -eq "$EXPECT_REP" ] || { echo "lint: replaces/evidence checker is inert — rejected $got of $EXPECT_REP bad fixtures"; fail=1; }
MARKERS_PLANNING="$fx/replaces-good/planning" python3 scripts/markers.py lint "$fx/replaces-good/PRINCIPLES.md" >/dev/null ||
  { echo "lint: replaces/evidence checker rejects the good fixture"; fail=1; }
got=$(mk lint "$fx"/platform-bad/product/*.md "$fx"/platform-bad/planning/*.md | grep -c '^markers:')
[ "$got" -eq "$EXPECT_PLAT" ] || { echo "lint: platform marker checker is inert — rejected $got of $EXPECT_PLAT bad fixtures"; fail=1; }
mk lint "$fx"/platform-good/product/*.md "$fx"/platform-good/planning/*.md >/dev/null ||
  { echo "lint: platform marker checker rejects the good fixture"; fail=1; }
cov=$(MARKERS_SOURCES="$fx/good.md" mk coverage F999; MARKERS_SOURCES="$fx/good.md" mk coverage --summary F999)
echo "$cov" | grep -q '^- \*\*1\*\* — \[' && echo "$cov" | grep -q '^- \*\*2\*\* — \*\*partial\*\*' &&
  echo "$cov" | grep -q '1 of 2 covered · \*\*partial: 2\*\*' ||
  { echo "lint: coverage map is inert — it does not tell a partial claim from a full one"; fail=1; }
mk lint "$fx/good.md" "$fx/binds-good/PRINCIPLES.md" "$fx/binds-good/scenario-F997.md" >/dev/null && mk risks "$fx/risks-good" >/dev/null ||
  { echo "lint: marker checker rejects a good fixture"; fail=1; }
# Criterion reports (2026-10-10): the roll-up must refuse every broken sidecar and compute the good ones exactly.
cf=scripts/fixtures/criteria
cout=$(python3 scripts/criteria.py check "$cf/bad" 2>&1)
for want in 'F911-x.json: criterion 1: built is '"'"'partly' 'F912-x.json: criteria[0]: missing "reviewed"' \
  'F913-x.md: no F913-x.json' 'F914-x.md: generated block does not match' 'F915-x.json: criterion 1: kind' \
  'F916-x.json: sits in alpha/' 'F917-x.json: cannot read JSON' 'F918-x.json: criterion 1: built is no, so'; do
  echo "$cout" | grep -qF "$want" || { echo "lint: criteria checker is inert — it let through: $want"; fail=1; }
done
[ "$(echo "$cout" | grep -c '/F9')" -eq 8 ] || { echo "lint: criteria checker reports other than the 8 planted faults"; fail=1; }
ct=$(mktemp -d); cp -R "$cf/good/." "$ct"
if python3 scripts/criteria.py rollup "$ct" >/dev/null; then
  grep -qF '| **All** | 5 | 2/5 (1?) | 1/5 | 1/5 (1?) | 2/5 (1?) | 0/5 (3?) | 0/5 | 3 |' "$ct/README.md" ||
    { echo "lint: criteria roll-up miscounts the good fixture"; fail=1; }
else
  echo "lint: criteria checker rejects the good fixture"; fail=1
fi
rm -rf "$ct"
# The "never" lint (Don, 2026-09-30: the only approved "never" is "never extractive").
# The checker proves itself on every run; the scan of real docs is off until Don approves
# the rewording. Turn it on with NEVER_LINT=1.
got=$(python3 scripts/never.py scripts/fixtures/never/bad.md | grep -c '^never:')
[ "$got" -eq 3 ] || { echo "lint: never checker is inert — rejected $got of 3 bad fixture uses"; fail=1; }
python3 scripts/never.py scripts/fixtures/never/good.md >/dev/null || { echo "lint: never checker rejects the good fixture"; fail=1; }
if [ "${NEVER_LINT:-0}" = "1" ] && ! out="$(python3 scripts/never.py)"; then
  echo "$out" | sed 's/^/lint: /'; fail=1
fi
# PRINCIPLES.md holds principles only: the checker names the home of each planted non-principle.
got=$(python3 scripts/markers.py principles "$fx/principles-bad/PRINCIPLES.md" | grep -c '^markers:')
[ "$got" -eq 6 ] || { echo "lint: principles checker is inert — rejected $got of 6 planted non-principles"; fail=1; }
python3 scripts/markers.py principles "$fx/principles-good/PRINCIPLES.md" >/dev/null || { echo "lint: principles checker rejects the good fixture"; fail=1; }
if [ -f PRINCIPLES.md ] && ! out="$(python3 scripts/markers.py lint)"; then
  echo "$out" | sed 's/^/lint: /'
  fail=1
fi

# Doc budgets (process/WHERE-THINGS-GO.md): the checker proves itself on 4 planted faults, then checks this repo.
bf=scripts/fixtures/budgets
got=$(BUDGETS_BASE_DIR="$bf/bad-base" python3 scripts/budgets.py check --root "$bf/bad" | grep -c '^budgets:')
[ "$got" -eq 4 ] || { echo "lint: budget checker is inert — rejected $got of 4 bad fixtures"; fail=1; }
BUDGETS_BASE_DIR="$bf/good-base" python3 scripts/budgets.py check --root "$bf/good" >/dev/null || { echo "lint: budget checker rejects the good fixture"; fail=1; }
got=$(BUDGETS_MOVE=1 BUDGETS_BASE_DIR="$bf/bad-base" python3 scripts/budgets.py check --root "$bf/bad" | grep -c '^budgets:')
[ "$got" -eq 3 ] || { echo "lint: budget checker does not let a docs: move PR grow a doc (got $got of 3)"; fail=1; }
if [ -f scripts/budgets.tsv ] && ! out="$(python3 scripts/budgets.py check)"; then
  echo "$out" | sed 's/^/lint: /'; fail=1
fi

# TRIAL meta layer: the PM-approval guard proves itself, and the score scripts must compile.
node scripts/pm-approved-guard.cjs --self-test >/dev/null || { echo "lint: pm-approved guard is inert or wrong"; fail=1; }
for f in scripts/score_lib.py scripts/score_ci_health.py scripts/score_doc_drift.py scripts/trial_health.py; do
  python3 -m py_compile "$f" 2>/dev/null || { echo "lint: $f does not compile"; fail=1; }
done

# Generated files: a feature PR never commits them; only the regen (workflow or handoff, subject "docs: regenerate…") does.
# constraints/ and PLATFORM-*.md are not listed: markers.py already makes the PR that changes a marker carry them.
if [ -f STATUS.md ] && base=$(git merge-base origin/main HEAD 2>/dev/null) && [ "$base" != "$(git rev-parse HEAD)" ]; then
  gen=$(git diff --name-only "$base" HEAD -- DASHBOARD.md STATUS.md README.md dashboard/status-dashboard.html)
  if [ -n "$gen" ] && [ -n "$(git log --no-merges --format=%s "$base..HEAD" | grep -v '^docs: regenerate')" ]; then
    echo "$gen" | sed 's/^/lint: generated file in a feature PR (merge main in, never commit it) — /'; fail=1
  fi
fi

if [ "$fail" -ne 0 ]; then
  echo "lint: FAILED"
  exit 1
fi
echo "lint: clean"
