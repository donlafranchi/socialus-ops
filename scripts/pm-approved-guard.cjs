#!/usr/bin/env node
// TRIAL (started 2026-10-10). A PR that changes how the pipeline judges itself needs the repo owner's `pm-approved` label,
// applied after the last commit. Usage: node scripts/pm-approved-guard.cjs --self-test
// LIMIT, stated plainly: agents here act with the owner's own token, so a label applied by an agent also reads as the owner.
// This is a tripwire and an audit trail (who, when), not a lock. A separate agent identity is the real fix.
const PROTECTED = [/^score-[^/]+\//, /^review-pipeline\//, /^scripts\/pm-approved-guard\.cjs$/, /^scripts\/score_[^/]+\.py$/, /^scripts\/trial_health\.py$/, /^\.github\/workflows\/pm-approved-guard\.yml$/]

function needsApproval(files, labels, baseHas = () => true) {
  if (labels.includes('meta-change')) return true
  return files.some((f) => PROTECTED.some((p) => p.test(f)) && baseHas(f))
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
    ['score file', needsApproval(['score-ci-health/SKILL.md'], []), true],
    ['reviewer', needsApproval(['review-pipeline/SKILL.md'], []), true],
    ['score formulas', needsApproval(['scripts/score_ci_health.py'], []), true],
    ['trial health', needsApproval(['scripts/trial_health.py'], []), true],
    ['guard itself', needsApproval(['scripts/pm-approved-guard.cjs'], []), true],
    ['meta label', needsApproval(['README.md'], ['meta-change']), true],
    ['plain docs', needsApproval(['README.md', 'plan-feature/SKILL.md'], []), false],
    ['guard file new in this PR', needsApproval(['scripts/pm-approved-guard.cjs'], [], () => false), false],
    ['no label', approvalProblem([], 'o', '2026-01-01T00:00:00Z') !== null, true],
    ['by agent', approvalProblem([ev('labeled', 'bot', '2026-01-02T00:00:00Z')], 'o', '2026-01-01T00:00:00Z') !== null, true],
    ['before last commit', approvalProblem([ev('labeled', 'o', '2026-01-01T00:00:00Z')], 'o', '2026-01-02T00:00:00Z') !== null, true],
    ['removed', approvalProblem([ev('labeled', 'o', '2026-01-02T00:00:00Z'), ev('unlabeled', 'o', '2026-01-03T00:00:00Z')], 'o', '2026-01-01T00:00:00Z') !== null, true],
    ['approved', approvalProblem([ev('labeled', 'o', '2026-01-02T00:00:00Z')], 'o', '2026-01-01T00:00:00Z') === null, true],
  ]
  let fail = 0
  for (const [name, got, want] of cases) if (got !== want) { console.log(`pm-approved-guard: wrong on "${name}"`); fail++ }
  if (fail) process.exit(1)
  console.log('pm-approved-guard: self-test ok')
}

if (require.main === module && process.argv[2] === '--self-test') selfTest()
module.exports = { needsApproval, approvalProblem }
