#!/usr/bin/env node
// TRIAL (started 2026-10-10). Runs the pm-approved guard by hand for one PR, for repos where Actions cannot start
// (donlafranchi/skills is private and its Actions are blocked on billing). An agent MUST run this before merging any PR there.
// Usage: node scripts/pm-approved-check.cjs <owner/repo> <pr-number>      exit 0 = may merge, 1 = needs the PM or a label
const { execFileSync } = require('child_process')
const { metaKind, approvalProblem, UNLABELLED } = require('./pm-approved-guard.cjs')
const gh = (args) => JSON.parse(execFileSync('gh', args, { encoding: 'utf8', maxBuffer: 1 << 26 }))
const [slug, num] = process.argv.slice(2)
if (!slug || !num) { console.log('usage: pm-approved-check.cjs <owner/repo> <pr>'); process.exit(2) }
const owner = slug.split('/')[0]
const pr = gh(['api', `repos/${slug}/pulls/${num}`])
const files = gh(['api', '--paginate', '--slurp', `repos/${slug}/pulls/${num}/files?per_page=100`]).flat().map((f) => f.filename)
const labels = pr.labels.map((l) => l.name)
const baseHas = (f) => { try { execFileSync('gh', ['api', `repos/${slug}/contents/${f}?ref=${pr.base.sha}`], { stdio: 'ignore' }); return true } catch { return false } }
const kind = metaKind(files, labels, baseHas)
if (kind === 'plain') { console.log(`#${num}: not a meta change; may merge.`); process.exit(0) }
if (kind === 'bookkeeping') { console.log(`#${num}: meta-bookkeeping (renames, lists, counts); may merge on green without the PM.`); process.exit(0) }
if (kind === 'unlabelled') { console.log(`#${num}: DO NOT MERGE. ${UNLABELLED}.`); process.exit(1) }
const events = gh(['api', '--paginate', '--slurp', `repos/${slug}/issues/${num}/events?per_page=100`]).flat()
const commit = gh(['api', `repos/${slug}/commits/${pr.head.sha}`])
const problem = approvalProblem(events, owner, commit.commit.committer.date)
if (problem) { console.log(`#${num}: DO NOT MERGE. Meta change needs the PM: ${problem}.`); process.exit(1) }
console.log(`#${num}: pm-approved by ${owner} after the last commit; may merge.`)
