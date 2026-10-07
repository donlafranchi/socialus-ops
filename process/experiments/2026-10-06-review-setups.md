# Experiment: three review setups on the Page-editing batch

*(The PM, 2026-10-06.)* One screenshot capture, three ways of reviewing it, scored against each other. An experiment, not a ruling: the recommendation is the lane's, and the PM rules. A later check compares each setup's misses against what the PM finds in his live review of the same batch.

## What was reviewed
The Page-editing batch: PRs #418 (Edit Page as section cards), #419 (location with a map pin and neighborhood search) and #424 (Archive and Delete), on one integration branch (`423`, which already contains the other two). One capture, taken once on a throwaway local stack: 5 routes (`page`, `page-business`, `page-private`, `page-edit`, `you`) × 13 personas × 390 and 1280px = 130 pictures, 7.2 minutes on two workers. All three setups read the same pictures and the same brief (`socialus-web` source was readable too, so some findings come from code, not pictures).

## The three setups (same model tier for all: mid)
- **A. One reviewer** covering every concern, every persona.
- **B. Five reviewers in parallel, split by concern:** visibility, UX and tidiness, accessibility, copy and voice, precedent. Each covers every persona.
- **C. Five reviewers in parallel, split by persona:** signed out, member (stranger, follower, member, applicant, RSVP), owner (place, interest, event, family), operator, builder. Each covers every concern. *No builder persona is seeded locally, so the builder reviewer used the business and practice owners as stand-ins.*

## Results

| Measure | A: one | B: five by concern | C: five by persona |
|---|---|---|---|
| Wall time | 3.2 min | 5.4 min (slowest reviewer 5.3 min) | 2.7 min (slowest reviewer 2.4 min) |
| Tokens (visible, subagents) | 153k | 614k | 509k |
| Findings raised (lines) | 19 | 59 | 66 |
| Distinct findings (deduplicated across setups) | 18 | 40 | 35 |
| Real, plausible or judgement (not false positives) | 18 | 40 | 30 |
| False positives | 0 | 0 | 5 |
| Caught only by this setup (not noise) | 2 | 15 | 10 |
| Share of all 53 non-noise distinct findings caught | 34% | 75% | 57% |
| Tokens per distinct non-noise finding | 8.5k | 15.3k | 17.0k |

Across the three setups there are **58 distinct findings, 53 non-noise and 5 false positives** (all five from setup C). Scoring was done by the lane that ran the experiment, by reading each finding against the source and the rulings; two (K20 and K25) were checked in code and confirmed, K23 and K54 are plausible from source and need a test, and the rest were judged from the pictures and the brief. **A real finding here includes judgement calls the PM should look at**, marked in the table.

Wall time includes the lane's own overhead (a few seconds each). Cost is the subagents' visible tokens only; the lane's own scoring work is not counted.

### What each setup uniquely caught
- **A (one reviewer):** two plausible items no one else raised: the missing message after Delete (K9) and members seeing the founder's display name (K15). Otherwise A's findings were a subset of B's and C's. It missed the privacy finding (K20) and the contrast failure (K25).
- **B (by concern):** the most valuable unique findings. **K20** (picking a neighbourhood saves and publishes an exact address point) is a privacy bug, and only B's visibility reviewer found it, by reading `WhereFields.tsx` and `where-save.ts`. B also alone found the 1.3:1 switch contrast (K25), the keyboard and screen-reader gaps in the typeahead (K26), the archived-Page read paths (K22, K23) and the "visitors" copy rule break (K34).
- **C (by persona):** ten unique non-noise findings, mostly minor: the Private marker an owner doesn't see (K42), two competing signed-out CTAs (K44), the operator's missing path to its tools (K52) and a blank-date Deleted tile (K54) are the useful ones. It also produced all five false positives: dev-overlay and mid-load capture artifacts, an applicant behaviour that is expected because approval isn't built, and two unmeasured contrast and target-size guesses.

### What all three missed (a gap in the capture, not the reviewers)
Every reviewer said the same thing: the captures show the Edit screen with its groups collapsed, so **the expanded Location card and pin, the neighborhood typeahead, Page settings, the Delete sheet, the archived banner and tiles, and loading, error and offline states were never pictured.** Findings about them came from source only. The capture bundle (`PIPELINE-build.md` § (e) item 4) should open each state it can before reviewers start. This probably matters more than the choice of setup.

## Recommendation (the lane's; the PM rules)
1. **Use B (split by concern) for UI PRs that touch who-sees-what, forms or lifecycle changes.** It found the most (75% of distinct findings) and all of the high-value ones, at about 4 times A's tokens and about 1.7 times A's wall time. Its visibility reviewer is the one that must not be dropped.
2. **Use A for small, low-risk UI changes** (copy-only, one component, no new state): about a quarter of the cost, and it caught 34%.
3. **Do not run C as the main setup.** It was fastest and caught real persona-specific items, but it raised all the false positives, found less per token, and each reviewer repeated the same Edit-page findings five times over. **Keep two persona checks as part of B's visibility reviewer** (signed out, and operator), since those are the ones C's lens added.
4. **Fix the capture first:** open the sheets, expand the groups, and capture the archived and error states, then rerun the best setup on the same batch to see how much the gap hid.
5. Treat this as one batch, one run each, scored by the same lane that ran it. It is a lead, not a measurement.

## The findings
Real = confirmed or clearly right; plausible = reasonable from source, needs a test; judgement = a call for the PM; false positive = not a defect. Which setup caught it is ticked.

| ID | Finding | Verdict | A | B | C |
|---|---|---|---|---|---|
| K1 | The read-only Link card floats loose under the collapsed "Tags and links" header, outside any group | real | ✓ | ✓ | ✓ |
| K2 | Location, Contact, Tags and links start collapsed, hiding their one-line summaries (the address needs a tap) | real | ✓ | ✓ | ✓ |
| K3 | Group says "Location", its card and sheet say "Where" | real | ✓ | ✓ |  |
| K4 | Em dash in the owner bar ("Your Page — only you see this"), against the no-em-dash rule | real | ✓ | ✓ |  |
| K5 | Owner Page: full inline announcement composer plus an Announce button; several primary-weight actions | real | ✓ | ✓ | ✓ |
| K6 | Per-post Edit and Delete links far under the 44px tap size, side by side | real | ✓ | ✓ | ✓ |
| K7 | The location pin map has no keyboard way to move the pin | real | ✓ | ✓ |  |
| K8 | "Drop a pin" starts at a fixed Sacramento point with no confirm step | real | ✓ | ✓ |  |
| K9 | After Delete the owner lands on You with no message or restore date | plausible | ✓ |  |  |
| K10 | Delete stays disabled unless the typed name matches exactly, with no hint why | real | ✓ | ✓ | ✓ |
| K11 | New draft copy for the PM's tone look (Archive, Delete, Restore, Where sheet, cards) | real | ✓ | ✓ | ✓ |
| K12 | Summaries like "Offer a service or teach · Listed as Social group" read as jargon or contradiction | real | ✓ | ✓ |  |
| K13 | You: the Your Pages tile is oversized and repeats the owner's Page under Following | real | ✓ | ✓ | ✓ |
| K14 | "Next event" repeats the first announcement on the same Page | real | ✓ |  | ✓ |
| K15 | Members and applicants see the founder's display name on a Page | plausible | ✓ |  |  |
| K16 | Private-Page refusal for non-members conflicts with the 2026-09-30 ruling (a doc conflict for the PM) | real | ✓ | ✓ | ✓ |
| K17 | Signed out on the Edit URL gets no sign-in route | real | ✓ | ✓ | ✓ |
| K18 | Done is only at the top of a long Edit page, out of thumb reach | judgement | ✓ | ✓ |  |
| K20 | Picking a neighbourhood sets a pin but never `areaOnly`, so a reverse-geocoded address point is saved and published (verified in source) | real |  | ✓ |  |
| K21 | A private Page's composer defaults to "Who sees this: Anyone" (already Issue #337) | real |  | ✓ |  |
| K22 | "Only you can see this" is wrong for an archived Page that its managers also see | plausible |  | ✓ |  |
| K23 | Archived Pages may still surface through `venue_hosted_items` and `discoverable_items`, which filter only `dissolved_at` (plausible from source, needs a test) | plausible |  | ✓ |  |
| K24 | The operator cannot open an archived or deleted Page during the 14 days | real |  | ✓ | ✓ |
| K25 | The "Show only my neighbourhood" switch's off state is about 1.3:1 against white, under 3:1 (verified: #e5e3dd on white) | real |  | ✓ |  |
| K26 | The neighbourhood typeahead announces no result count or error to screen readers | real |  | ✓ |  |
| K27 | Map zoom buttons are about 29px | judgement |  | ✓ |  |
| K28 | Heading order skips a level on Edit Page | judgement |  | ✓ |  |
| K29 | About ten duplicate-named region landmarks on Edit Page | judgement |  | ✓ |  |
| K30 | In-page links ("Add a date", "Add to calendar") are small tap targets | real |  | ✓ | ✓ |
| K31 | You: Start something, More, Sign out links and the LIVE chip are small | real |  | ✓ | ✓ |
| K33 | British spellings (neighbourhood, centre) in a US-only product | judgement |  | ✓ |  |
| K34 | "Visitors" used as a category of people in the Where sheet | real |  | ✓ |  |
| K35 | "Finish that answer" error is form jargon | judgement |  | ✓ |  |
| K36 | "You must be signed in." is blunt | judgement |  | ✓ |  |
| K37 | Archive fires on one tap with no confirm or undo | judgement |  | ✓ | ✓ |
| K38 | Archive and Delete buttons sit in the card body and under a bare accordion, not a card header or a separate place | judgement |  | ✓ | ✓ |
| K39 | Neighbourhood is a hidden mode switch, not one typeahead | judgement |  | ✓ |  |
| K40 | The literal placeholder "a location" shows as an address (already Issue #339) | real |  | ✓ | ✓ |
| K41 | An applicant (join not confirmed) sees a private Page and "Joined"; approval is not built, so likely expected | false positive |  |  | ✓ |
| K42 | The owner of a private Page sees nothing marking it Private | real |  |  | ✓ |
| K43 | The refusal screen has no app header or tab bar and no way back to the Page | real |  | ✓ | ✓ |
| K44 | Signed-out Page: two competing CTAs ("Sign up to join" and "Sign in to see what's happening") | judgement |  |  | ✓ |
| K45 | The signed-out Announcements teaser is inset and unboxed | judgement |  |  | ✓ |
| K46 | Share and "..." icon target size (unconfirmed from the picture) | false positive |  |  | ✓ |
| K47 | Secondary text contrast "near 4.5:1" (not measured) | false positive |  |  | ✓ |
| K48 | The wordmark repeats above the You card | judgement |  |  | ✓ |
| K49 | You captured mid-load ("Loading your Pages...") | false positive |  |  | ✓ |
| K50 | You Settings rows: "Password: Sign in without an email" and an unclear single "Set or change" | judgement |  |  | ✓ |
| K51 | The dev overlay ("N", "1 Issue") covers content in the shots | false positive |  |  | ✓ |
| K52 | The operator's You has no entry to the operator tools | judgement |  |  | ✓ |
| K53 | Loose unlabeled lines under the Page title and unboxed sections | real |  | ✓ | ✓ |
| K54 | A Deleted tile renders "restore until " with a blank date if `deleteAfter` is null | plausible |  |  | ✓ |
| K56 | Contact group absent and summaries identical across owner kinds | judgement |  |  | ✓ |
| K57 | At 1280 the edit column is a narrow strip in a mostly empty page | judgement |  |  | ✓ |
| K58 | Five "Edit" text buttons in a column; the About group is five thin cards | judgement |  | ✓ | ✓ |
| K60 | "Sign out" appears twice on You at 1280 | judgement |  |  | ✓ |
| K62 | Card summaries are truncated | judgement |  | ✓ | ✓ |
| K64 | The Link card explains a limit in the Page's own voice | judgement |  | ✓ |  |

## Later check (PM's live review)
When the PM reviews this batch live, file each problem he finds as an Issue labelled `found-by-pm`, and note here which setup's finding it matched or whether all three missed it. That gives the miss rate per setup that this one run cannot.

## Handed to the build lane
The non-noise findings above, by area, were posted as a comment on PRs #418, #419 and #424 after scoring (not before).
