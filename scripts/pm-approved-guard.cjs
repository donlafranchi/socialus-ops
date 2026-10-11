#!/usr/bin/env node
// TRIAL (started 2026-10-10; trimmed 2026-10-11, PM-approved). A PR that touches how the pipeline judges itself is one of two kinds:
//   meta-change       what a score measures or its target changes. Needs the repo owner's `pm-approved` label after the last commit,
//                     and the PR body says in plain words what the score measured before and after.
//   meta-bookkeeping  renames, lists, counts, wording. Merges on green; the PM never sees it.
// A protected-file PR with neither label fails until the agent picks one. Usage: node scripts/pm-approved-guard.cjs --self-test
// LIMIT, stated plainly: agents act with the owner's token, so a label applied by an agent also reads as the owner, and an agent
// could call a real change bookkeeping. This is a tripwire and an audit trail (which label, who, when); trial_health.py counts
// bookkeeping merges so the Friday review can read them. A separate agent identity is the real fix.
const PROTECTED = [/^score-[^/]+\//, /^review-pipeline\//, /^scripts\/pm-approved-guard\.cjs$/, /^scripts\/pm-approved-check\.cjs$/, /^scripts\/score_[^/]+\.py$/, /^scripts\/trial_health\.py$/, /^\.github\/workflows\/pm-approved-guard\.yml$/]
const UNLABELLED = 'protected files, no label. Add `meta-change` (what a score measures or its target changes; the PM approves) or `meta-bookkeeping` (renames, lists, counts; merges on green)'

// 'change' needs the PM; 'bookkeeping' merges on green; 'unlabelled' fails until labelled; 'plain' is not a meta PR.
function metaKind(files, labels, baseHas = () => true) {
  if (labels.includes('meta-change')) return 'change'
  if (!files.some((f) => PROTECTED.some((p) => p.test(f)) && baseHas(f))) return 'plain'
  return labels.includes('meta-bookkeeping') ? 'bookkeeping' : 'unlabelled'
}

// events: issue events, oldest first. Returns null when approved, else the reason.
function approvalProblem(events, owner, lastCommitAt) {
  let last = null
  for (const e of events) {
    if (e.label?.name !== 'pm-approved') continue
    if (e.event === 'labeled') last = e
    else if (e.event === 'unlabeled') last = null
  }
  if (!last) return 'no `pm-approved` label'
  if (last.actor?.login !== owner) return `\`pm-approved\` was applied by ${last.actor?.login}, not the repo owner`
  if (new Date(last.created_at) < new Date(lastCommitAt)) return '`pm-approved` was applied before the last commit; re-approve what changed'
  return null
}

function selfTest() {
  const ev = (event, login, at) => ({ event, label: { name: 'pm-approved' }, actor: { login }, created_at: at })
  const cases = [
    ['score file, unlabelled', metaKind(['score-ci-health/SKILL.md'], []), 'unlabelled'],
    ['reviewer, unlabelled', metaKind(['review-pipeline/SKILL.md'], []), 'unlabelled'],
    ['score formulas, unlabelled', metaKind(['scripts/score_ci_health.py'], []), 'unlabelled'],
    ['trial health, unlabelled', metaKind(['scripts/trial_health.py'], []), 'unlabelled'],
    ['guard itself, unlabelled', metaKind(['scripts/pm-approved-guard.cjs'], []), 'unlabelled'],
    ['by-hand check, unlabelled', metaKind(['scripts/pm-approved-check.cjs'], []), 'unlabelled'],
    ['score file, bookkeeping', metaKind(['score-ci-health/SKILL.md'], ['meta-bookkeeping']), 'bookkeeping'],
    ['score file, change', metaKind(['scripts/score_ci_health.py'], ['meta-change']), 'change'],
    ['both labels', metaKind(['scripts/score_ci_health.py'], ['meta-bookkeeping', 'meta-change']), 'change'],
    ['meta label on plain file', metaKind(['README.md'], ['meta-change']), 'change'],
    ['bookkeeping label on plain file', metaKind(['README.md'], ['meta-bookkeeping']), 'plain'],
    ['plain docs', metaKind(['README.md', 'plan-feature/SKILL.md'], []), 'plain'],
    ['guard file new in this PR', metaKind(['scripts/pm-approved-guard.cjs'], [], () => false), 'plain'],
    ['no label', approvalProblem([], 'o', '2026-01-01T00:00:00Z') !== null, true],
    ['by agent', approvalProblem([ev('labeled', 'bot', '2026-01-02T00:00:00Z')], 'o', '2026-01-01T00:00:00Z') !== null, true],
    ['before last commit', approvalProblem([ev('labeled', 'o', '2026-01-01T00:00:00Z')], 'o', '2026-01-02T00:00:00Z') !== null, true],
    ['removed', approvalProblem([ev('labeled', 'o', '2026-01-02T00:00:00Z'), ev('unlabeled', 'o', '2026-01-03T00:00:00Z')], 'o', '2026-01-01T00:00:00Z') !== null, true],
    ['approved', approvalProblem([ev('labeled', 'o', '2026-01-02T00:00:00Z')], 'o', '2026-01-01T00:00:00Z') === null, true],
  ]
  let fail = 0
  for (const [name, got, want] of cases) if (got !== want) { console.log(`pm-approved-guard: wrong on "${name}": got ${got}`); fail++ }
  if (fail) process.exit(1)
  console.log('pm-approved-guard: self-test ok')
}

if (require.main === module && process.argv[2] === '--self-test') selfTest()
module.exports = { metaKind, approvalProblem, UNLABELLED }
