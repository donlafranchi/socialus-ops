# STATUS

> ## Generated 2026-10-03 · 17:10 UTC
>
> **Disposable. Regenerating replaces this file wholesale** — nothing here is
> hand-maintained, and a hand-edit is lost on the next run. `git log -p
> STATUS.md` is the history.
>
> **Refreshed by `.github/workflows/status.yml`** — on every push to `main`
> here, daily at 13:05 UTC, and on demand from the Actions tab (*status →
> Run workflow*), which works from a phone. It commits only when the content
> moved, so a new revision of this file is never a bare heartbeat. Locally:
> `bash scripts/status.sh`.
>
> **Derived from:** `scripts/state.sh` against `socialus-web` @ `origin/main`
> `aa491bb` (2026-10-02); `accepted-risks/*.json`;
> `planning/scenario-*.md` frontmatter; `ROADMAP.md`.
>
> **Answers "where is this project", not "what tickets exist."** The ticket
> list is `gh issue list`, which is always right; this is not a copy of it.

Launch **2026-10-30**, one metro. 27 days out.

**17 of 22 approved and building scenarios are unverified** — no check is marked as discharging any
of their criteria. Unmarked is unverified, not verified. § Guard coverage.

**Native apps: 7 gaps for iOS, 6 for Android** — `PLATFORM-IOS.md`, `PLATFORM-ANDROID.md`.

## Scenarios, by status

| approved | building | draft | deferred |
|---|---|---|---|
| 18 | 4 | 20 | 1 |

**Building:**
- F060 (Someone starts something without opening a shop)
- F061 (Someone creates a Page worth showing people)
- F069 (A non-business Page resolves everywhere, and holding several is ordinary)
- F070 (Every Page has a face, even without a photo)

**`building` is frontmatter, not evidence** — nothing checks it against a
branch or a commit.

## In the code repo

**66 issues open** in `socialus-web`, 5 launch-blocking:
- #220 F078 · Flagged content hides itself on the agent's call, and the poster is told why
- #221 F080 · No pictures of children, from anyone — detection point needs Don
- #222 F081 · One signup for everyone: four fields, and the zip sets the metro
- #223 F082 · One self-attestation before a first Page, selling and hosting alike
- #246 bug · What one member can read about another: the signed-in half of #241, and four member tables open to anyone

**63 PRs merged in the last fortnight.** The newest five:
- #322 2026-10-03 change #323: the apply workflow is apply.yml, "Apply migrations"; branches named by Issue number
- #319 2026-10-03 change #318: owners can delete their own posts
- #306 2026-10-02 chore #294: adopt the design tokens without colour
- #292 2026-10-01 chore #291: the migrations-applied check also runs on main
- #288 2026-10-02 change #285: tags on a live Page can be edited any time

### Needs a look — not a claim that anything is wrong

*A commit naming a ticket is not proof the ticket is done: partial work
counts. Each row needs a look, not a close.*

- **#84 open, but T159 appears on main** — chore · T159 is two different tickets — renumber one in ops-pattern
- **#53 open, but T156 appears on main** — F059 · T156 · Browse renders Pages
- **#51 open, but T154 appears on main** — F059 · T154 · Browse reads Pages, not Items
- **#30 open, but T149 appears on main** — chore · T149 · Retire vendor routes for real
- **#16 open, but T126 appears on main** — F056 · T126 · Edit shop — image, description, values
- **#15 open, but T125 appears on main** — F057 · T125 · You gains a producer state

### Still on main, meant to be gone

- `/following` still present — src/app/following/page.tsx
- `members.maker_mode_enabled` still in the schema

## The ontology — what is declared

- **13 link types declared**, 11 built. Registry schema 2.
- **Declared but not built (2)** - the relationship is named and nothing writes it yet:
  - a Member supports a Page
  - an Announcement is at a Location
- **7 object types declared**: Member (live), Page (live), Item (live), Location (live), Place (live), Announcement (live), Tag (live).
- **Rejected as nouns (6)** - named so they stay rejected: Person, Creator, Organizer, Follower, Patron, Vendor.
- **29 handlers, of which 18 write no declared link.**
  Not a fault on its own - a handler may legitimately touch no relationship -
  but an undeclared link lives here if it lives anywhere:
  - group.member_join
  - group.member_leave
  - group.post_delete
  - group.post_edit
  - item.publish
  - member.business_jurisdiction.remove
  - member.business_jurisdiction.set
  - member.create
  - member.interests.add
  - member.place_interest.add
  - member.place_interest.remove
  - member.saved_search.remove
  - member.saved_search.restore
  - metro.waitlist_join
  - metro.waitlist_join_anonymous
  - report.create
  - report.decide
  - report.reverse

## What CI last said

- **`deploy-health.yml`** — success, 2026-10-03
  - Database reachable from the deployment: success
  - Ontology declarations still match the code: success
- **`ci.yml`** — success, 2026-10-03
  - Unit tests: success
  - Migrations applied to production: success
  - Browser: success
  - Lint, types, build: success

## Measured, not estimated

- Copy: 584 strings across 118 files — source `docs/copy-inventory.md` on origin/main
- Routes on origin/main: 23
- Migrations on origin/main: 70

## Deferred on purpose — and therefore easy to forget

Ruled acceptable with a condition for looking again. The ruling itself is a
dated line in `DECISIONS.md`; the register is `accepted-risks/`.

**3 need a look now.**

- **observability: no error tracking in production** — **due in 13 days**
  - If forgotten: A runtime error for a real member is invisible. Nobody is paged, nothing is logged where anyone looks, and the first signal is a person giving up and not saying why. The DATABASE_URL outage went four months unnoticed for exactly this reason.
  - Look again if: ANY of: a member outside the team signs up; a bug is reported that nobody can reproduce; or 2026-10-16 passes with this still open.
- **ci: playwright suite exists but no workflow runs it** — **due in 13 days**
  - If forgotten: The end-to-end tests rot. Nobody runs them, they drift from the app, and the day someone needs them they no longer pass for reasons unrelated to the bug being chased — at which point they get deleted instead of fixed.
  - Look again if: ANY of: a regression reaches production that a browser test would have caught; the Playwright suite fails to run locally when someone next tries it; or 2026-10-16 passes with this still open.
- **storage: removed photo bytes stay fetchable by direct URL** — **due in 13 days**
  - If forgotten: A photo the operator removed stays downloadable, indefinitely, by anyone who has or can guess its storage URL. For ordinary bad content that is tolerable. For illegal content it is not, and 'we kept it so it could be reversed' is not a defensible answer to a regulator, a police request, or the person in the photo.
  - Look again if: ANY of: the first report of illegal content reaches the review queue; a member asks for their own photo to be actually deleted rather than taken down; a takedown demand arrives from outside the platform; or 2026-10-16 passes (two weeks before launch) with this still open.
- **data: two rows in public.places share the slug 'sacramento'** — review by 2026-11-30
  - If forgotten: A scoped link resolves to the wrong geography and nobody notices, because both answers look plausible. The heuristic makes it deterministic and therefore silent.
  - Look again if: ANY of: a member reports results from the wrong area; a third row appears with the same slug; a browse or scope read starts resolving places by SLUG rather than by id; or 2026-11-30 passes. (The T156 browse query rewrite landed 2026-09-19 and takes place and metro IDs, never slugs, deliberately — so that trigger did NOT fire and this stays a live tripwire for the next read that does.)
- **schema: reports.reviewed_at/reviewed_by_member_id/outcome duplicate report_decisions** — review by 2026-11-30
  - If forgotten: Two sources of truth drift. A write path that updates the decisions log and forgets the projection leaves a report invisible in the queue or double-counted against a reporter's cap, and the bug looks like a UI fault rather than a schema one.
  - Look again if: ANY of: a third writer of report_decisions appears; delegated reviewers land (more writers, more chances to drift); the queue shows a report whose status disagrees with its history; or 2026-11-30 passes.

## Open questions

Every open-question marker, found by scanning — nobody maintains this list.
Oldest first. Rule and grammar: `process/PIPELINE.md` § Open questions.


**Waiting on Don** (16)

- 29d · "Neighbours, not strangers or creators" vs. "everyone who posts is a creator." A) the north star's refusal is scoped to the word "creator" as a label only —… — [product/foundation/role-language.md:34](product/foundation/role-language.md#L34)
- 26d · Promise 1 — what "surplus returns to the community" actually means. A) a fixed percentage, decided annually by the founder. B) a member vote or board process… — [product/foundation/goals.md:46](product/foundation/goals.md#L46)
- 26d · The flourishing thresholds (40 discretionary hours/week, 1.5× adequacy margin). A) adopt as the literal north-star targets everywhere. B) keep them illustrat… — [product/foundation/metrics.md:16](product/foundation/metrics.md#L16)
- 21d · What triggers the LLM pass, and who approves its output? A) a scheduled job, proposals landing in a queue Don reviews. B) on demand, run when someone looks.… — [planning/scenario-F071.md:37](planning/scenario-F071.md#L37)
- 20d · How does the search dictionary grow? A) from tags creators create — every new tag is a word a real person chose for their own thing. B) from logged zero-resu… — [planning/scenario-F071.md:41](planning/scenario-F071.md#L41)
- 18d · Where do the premise strings live, given Don expects to update them often? Copy is inline in the components today — roughly 458 user-facing strings across 50… — [planning/scenario-F083.md:37](planning/scenario-F083.md#L37)
- 17d · Which noun does the paused ontology spike model first — Item or Page? The spike lives outside this repo, at `../socialus-ontology-spike/INTENT.md`. — [product/foundation/nouns.md:254](product/foundation/nouns.md#L254)
- 14d · What makes a thing "free", now that the free-things lens has nowhere to read from? Surfaced by the browse query rewrite (`socialus-web` T156, 2026-09-19), wh… — [planning/scenario-F059.md:46](planning/scenario-F059.md#L46)
- 14d · Which ten names are the collections, and does the picker suggest from a Page's tags? *(Narrowed 2026-09-19 — Don ruled membership is owner-set, so what is le… — [product/ui/surfaces.md:61](product/ui/surfaces.md#L61)
- 4d · Are the store apps the site in a native shell, or native screens on the same database? A) A shell around the site (Capacitor-style): every screen and server… — [product/ui/surfaces.md:64](product/ui/surfaces.md#L64)
- 3d · When "near me" returns, how does finding by neighbourhood fit "local = the whole metro" and "no distance shown"? A) A place filter the member types, not a ra… — [planning/scenario-F095.md:28](planning/scenario-F095.md#L28)
- 3d · What does "sends traffic back" mean on a card? A) The card's main action opens the venue's own event page; SocialUs keeps the summary. B) A secondary "from t… — [planning/scenario-F096.md:30](planning/scenario-F096.md#L30)
- 3d · How is a member-shared event marked until claimed? A) "Shared by a neighbour, not yet confirmed by the venue", with no RSVP until claimed. B) The same, with… — [planning/scenario-F096.md:32](planning/scenario-F096.md#L32)
- 3d · Does imported content follow relationship-based visibility and the signed-out front door like any announcement? A) Yes, exactly: an imported event is a publi… — [planning/scenario-F096.md:34](planning/scenario-F096.md#L34)
- 3d · What does the platform do when imported content breaks the sensitive-content ask (children, animals and pets, anyone who can't fend for themselves)? A) Repor… — [planning/scenario-F096.md:36](planning/scenario-F096.md#L36)
- 1d · Address-with-pin, neighbourhood list, or both, as recommended? Nothing is built until Don confirms. — [#315](https://github.com/donlafranchi/socialus-web/issues/315)

**Cowork owes an answer** (1)

- 2d · Nothing opens an owner panel on Explore yet; what should, if anything? — [socialus-web src/components/browse/BrowseSurface.tsx:61](https://github.com/donlafranchi/socialus-web/blob/main/src/components/browse/BrowseSurface.tsx#L61)

## Guard coverage

**17 of 22 approved and building scenarios are unverified — no check is marked
as discharging any criterion of theirs, so a contradiction in them cannot surface here.** Unmarked
is unverified, not verified: nothing says a check exists, and under `[guard-proves-itself]` that
counts as absent. A **partial** criterion has checks that cover only part of it, named with what
they leave out; parts never add up to covered. Full map: `python3 scripts/markers.py coverage`.

- **F059** · 0 of 12 covered · **partial: 5** · unclaimed: 1, 2, 2b, 2c, 3, 4, 6, 7, 8, 9, 10
- **F080** · 1 of 5 covered · unclaimed: 1, 2, 3, 4
- **F081** · 1 of 8 covered · unclaimed: 1, 2, 3, 4, 5, 6, 8
- **F091** · 3 of 7 covered · **partial: 1, 7** · unclaimed: 5, 6
- **F093** · 4 of 12 covered · **partial: 4, 5, 6, 8, 9** · unclaimed: 10, 11, 12
- **Unverified — no marked check at all** (17): F056, F057, F058, F060, F061, F063, F064, F065, F069, F070, F072, F074, F076, F077, F078, F082, F092

## Is `building` backed by code?

Each scenario whose frontmatter says `building`, against what names it in `socialus-web`: commits
and files on main, and branches. Frontmatter is a claim; this is the evidence.

- **F060** · 0 commits on main · 5 files naming it · 0 branches
- **F061** · 0 commits on main · 12 files naming it · 0 branches
- **F069** · **nothing in the code names it** — no commit, file or branch
- **F070** · 6 commits on main · 14 files naming it · 0 branches

## Gating launch — does each have an Issue?

Every scenario whose frontmatter says `gates: launch`, against the `socialus-web` Issues
naming it. Five approved gating scenarios once had none, and nothing noticed.

- **F058** (approved) · #62 closed, #61 closed, #13 closed, #12 closed
- **F076** (approved) · #194 closed, #193 closed, #77 closed
- **F078** (approved) · #220 open
- **F080** (approved) · #221 open
- **F081** (approved) · #222 open
- **F082** (approved) · #223 open
- **F093** (approved) · #252 closed, #215 closed

**Rulings that bind code: 90.** Each names its Issue or scenario, or says it has nothing to build;
the lint fails one that does none of the three — the identity leaks sat eight days with no Issue.

- **Nothing to build** (13), by their own tag: 2026-10-02 Gatherings saved with the old 7-hour timezone error are thro…; 2026-10-01 Design tokens live in the app code as the single source of t…; 2026-10-01 We disclose member data only in response to valid legal proc…; 2026-09-30 Visibility currently defaults to social norms: what people w…; 2026-09-30 We are careful and supportive of our members, and we ask the…; 2026-09-30 The platform comes first, then its members, and every ruling…; 2026-09-30 Between members, we currently show a display name and avatar…; 2026-09-27 When a newer decision contradicts an older one, the newer on…; 2026-09-27 Cross-cutting documents are generated from inline markers, n…; 2026-09-27 Grep-built, never hand-kept: a fact lives inline where it is…; 2026-09-27 An open question is an inline marker where it was raised, no…; 2026-09-21 [guard-proves-itself] is the sixth process absolute: a check…; 2026-09-21 plainlanguage.gov governs user-facing copy, alongside voice.…

## What this run could not verify

- **The 20 drafts.** Status alone does not say which are waiting
  on Don and which are simply unfinished.

