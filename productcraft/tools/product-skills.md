# The product skills.

Eight sets of product-method skills are installed: discovery, strategy, market research, execution, data analytics, go-to-market, marketing and growth, and a small toolkit. Together they hold about seventy skills. Most are a framework wrapped in a prompt: they give the right shape for a piece of product thinking and none of the facts. Read this before reaching for one, so the lead picks the few that earn their place and knows where each one goes thin.

## What they're best at.

- **A good first shape, fast.** An interview script with the right sections, an assumption list sorted by risk, an opportunity tree with one outcome on top. The skeleton is sound and takes seconds.
- **Coverage.** They remember the categories a tired person forgets: the usability risk, the team risk, the guard number on an A/B test.
- **Naming the method.** Each one says which idea it comes from (Teresa Torres, Rob Fitzpatrick, Alberto Savoia, Geoffrey Moore), so the lead can judge how far to trust it.

Where something else beats them: anything that needs real facts. They can't know what Sean's ten interviewees said, what a competitor charges today, or how many people search for a thing. For research, the research guides in this folder come first; for numbers, `sheets-and-python.md`. The skills are the frame you hang those facts on.

## Setup.

Nothing to install or pay for. They load as skills under names like `pm-product-discovery:interview-script`. Some sets also carry short commands that chain several skills, such as the discovery set's full "discover" cycle. The commands are fine for a first pass; on a real job, call the single skill you need so you control what goes in.

## The few worth reaching for.

**Interview scripts: `interview-script`, then `summarize-interview`.** The script follows Rob Fitzpatrick's idea that you ask about someone's past behaviour, never about your idea. Its strongest lines ask for the last time the problem happened and what they've already tried. Pair it with Jason Cohen's method from the shelf: write the guesses down first, then make every question test one of them, and count how many people say they'll pay. The summary skill gives a clean one-page record per call, but it never checks a quote against the transcript. Do that yourself, every time.

**Assumption maps: `identify-assumptions-new`, then `prioritize-assumptions`.** The first lists what must be true across eight kinds of risk (value, usability, viability, feasibility, ethics, go-to-market, strategy, team). The second sorts them by impact and risk and suggests a test for each one that matters. This pair is the best route to "what should we test first?", which is most of Productcraft's work. For a feature on a product that already exists, use `identify-assumptions-existing`, which sticks to the four core risks.

**Opportunity trees: `opportunity-solution-tree`.** One measurable outcome at the top, customer problems under it, several solutions under each problem, a cheap test under each solution. Worth it once there is real research to sort. Without interview notes it invents the problems, and the tree looks finished while holding nothing.

**Cheap tests for a new idea: `brainstorm-experiments-new`.** It frames a bet as "at least X% of Y will do Z" and suggests fake-door pages, waitlists, pre-orders and doing the service by hand. It leans on Savoia's point that only commitment (time, money, reputation) counts as evidence. That matches the studio's focus: Buffer's two-page test on the shelf is exactly this kind of experiment.

**Strategy and pricing: `value-proposition`, `pricing-strategy`, `beachhead-segment`.** The value-proposition skill works one customer group at a time and makes you name what they use today, which keeps it honest. The pricing skill is a solid checklist of models and tests. The beachhead skill helps pick the first narrow group to win. Treat its "capture 60 to 70% of the segment" line as a big-company idea, not a side-product target.

**Pre-mortems: `pre-mortem`, plus the execution set's strategy stress-test skill.** The pre-mortem imagines the launch failed and sorts the reasons into real threats, overblown worries and things nobody is saying. The stress-test skill is the sharper of the two: it finds the claims a plan can't survive losing, attacks the strongest version of each, and gives the cheapest test, the evidence to get this week and the point at which you'd stop. Use the stress-test on a strategy or a plan; use the pre-mortem shortly before something ships.

**Test analysis: `ab-test-analysis` and `cohort-analysis`.** Useful structure for reading results: lift, a confidence range, guard numbers, ship or extend or stop. Read `sheets-and-python.md` before trusting its sample-size advice (see below).

## Where they overlap.

- **Three canvases say much the same thing.** The business-model canvas, lean canvas and startup canvas all fill boxes about customers, problem, channels and money. Pick one, usually the lean canvas for a side product, and never run all three.
- **Two ways to judge risk.** The pre-mortem and the stress-test skill cover the same ground from different ends. One is enough for most jobs.
- **Prioritising.** `prioritize-features`, `analyze-feature-requests` and `prioritization-frameworks` all score lists. For a one-person side product, the assumption pair above usually matters more than any scoring formula.
- **Segments and personas.** `market-segments`, `user-segmentation`, `user-personas` and `ideal-customer-profile` overlap heavily. Personas built without real research are fiction; skip them until there are interviews to build from.
- **Market sizing** lives in the market-research set and has its own guide, `market-sizing.md`.

Skip for Productcraft work: sprint planning, retros, user stories, OKRs, stakeholder maps, release notes and battlecards. They're team and day-job tools. The toolkit's privacy-policy and NDA drafts are a starting point that a person qualified in that area must check.

## Where the output goes generic.

The skills are confident by design. Every box gets filled, whether or not there's anything to fill it with. That's the main failure, and it shows up in a few recognisable ways.

- **Made-up customers.** Ask for an assumption map with no research attached and you get plausible people with plausible pains. Feed the skill Sean's real notes, quotes and numbers, or label every line a guess.
- **Example companies in place of evidence.** Canva, Slack and Basecamp turn up as illustrations. Fine for teaching, useless as proof that this idea works.
- **Big-company assumptions.** Several skills assume a trio of product manager, designer and engineer, budgets, sales teams and quarterly goals. Sean works alone on side products. Strip out team roles, owners and dates that don't apply.
- **Numbers with no source.** Pricing tiers, market sizes and conversion rates come out looking exact. Each one needs a source or a "guess" label before Sean sees it.
- **A pass bar left vague.** The test skills ask for a success threshold; check that one actually got set before the test runs. Cohen's "ten people who'll pay" is the model of a bar you can count.

**How a master uses them:** give the skill the real material (notes, transcripts, the Tally export), ask for one skill rather than a chained command, then cut the output by half. The useful part of an assumption map is usually three lines.

## Two faults in the skills themselves.

- **The interview script slips in questions it warns against.** Alongside the good past-tense questions, it includes "magic wand" and "what would you give up" prompts, which ask people to imagine rather than remember. Cut them, or move them to the very end where they can't colour the rest.
- **The A/B skill's sample-size formula leaves out power.** It drops the term for the chance of catching a real effect, so it suggests about half the people a standard calculation needs. Use the calculation in `sheets-and-python.md`.

## Examples.

- **Weak:** "Make an assumption map for a budgeting app for freelancers." Out comes forty generic risks across eight boxes.
- **Strong:** the same request with Sean's five interview summaries attached, and the instruction to mark which assumptions an interview already answered. Out come three untested beliefs that the whole idea rests on, each with a test Sean could run this week. That's the difference between a framework and a decision.

## Safety.

The skills run inside Claude and upload nothing on their own. A few (pricing, market sizing, competitor analysis) tell Claude to search the web, which sends the search words out but not Sean's files. Day-job material stays in Sean's private work repo, whichever skill is used. Nothing here spends money.

## More details

- Skill files read on November 12, 2026: `~/.claude/plugins/synced/*/pm-*/skills/*/SKILL.md`, across the sets pm-product-discovery, pm-product-strategy, pm-market-research, pm-execution, pm-data-analytics, pm-go-to-market, pm-marketing-growth and pm-toolkit. Author named in the set's own readme: Paweł Huryn, The Product Compass, MIT licence.
- The "magic wand" and "what would you give up" lines are in the discovery set's `interview-script`.
- The sample-size formula is in the data-analytics set's `ab-test-analysis`; it uses only the significance term, so for 80% power it gives about 49% of the standard figure.
- The "60 to 70% of the segment" line is in the go-to-market set's `beachhead-segment`.
- Shelf examples used: `productcraft/research/cohen-ten-who-will-pay.md`, `productcraft/research/buffer-two-page-test.md`.
