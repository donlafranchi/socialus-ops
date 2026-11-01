# Todo: read the single-loop rewrite against "design engineering, not a factory"

**As of 2026-11-01** · Source: Rob West, "The Agentic Software Factory is the Wrong Metaphor", 2026-09-19, https://robwest.info/articles/the-agentic-software-factory-is-the-wrong-metaphor/ (filed by the PM) · Maintained by: hand (research note; deleted once the single-loop rewrite has used it, 30 days)

*Not a ruling. A todo the PM filed for the single-loop work (`single-loop/PLAN.md`).*

## What the article says

- Writing code is design, not manufacturing (Reeves 1992, Fowler, Farley). The build pipeline is the factory we already have; agents work on the design side of it.
- A ticket is not an engineering drawing. Treating it as one hides the design work in the input, and the agent resolves the ambiguity with a confident guess.
- Variation is useful in design: several different attempts to compare beat one standardised station.
- Factory metrics (changes shipped, share automated) measure the line, not the product. Ask instead: how fast an assumption becomes evidence, how cheaply alternatives get explored, how fast we learn we were wrong.
- Build factories for the production parts only: builds, tests, upgrades, migrations, formatting, routine remediation.

## Where it touches our method

- The decision rule already treats agents as designers (look at precedents, choose, decide well-worn paths). The article supports keeping that, and widening it: an Issue is a hypothesis, not a work order.
- The baseline numbers proposed in `single-loop/PLAN.md` § Evals (Issue to merge hours, pushes after first CI, PM touches) are line metrics. Read them as cost, not as success.
- Where variation would pay: the council (parallel members, compared) and copy or UX alternatives, not routine tickets.

## Todo

- [ ] Before the main metric is agreed (PLAN.md § Status, step 1), add at least one learning measure beside the five line numbers, or say why none is measurable yet. (Owner: the session doing step 1.)
- [ ] In the scratch rewrite (worklist 5 and 6), keep the Issue as a hypothesis: the loop may report "the Issue is wrong" as a valid outcome instead of building the plausible guess. (Owner: the session doing the rewrite.)
