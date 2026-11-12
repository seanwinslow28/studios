# Deciding what to build and when.

Read this when a job turns into "what goes next, and how much of it?": a roadmap, a quarter's plan, a side-product build, a pile of requests, or a goal. A good answer names the change it wants, puts a time limit on the work, cuts the work to fit, and says plainly what isn't happening. You can't do it all, so the craft is choosing what to leave out, early and in the open.

## Roadmaps built on outcomes.

A feature list on a calendar is a promise you'll probably break, about things you haven't tested. A roadmap built on outcomes promises problems to solve and the change you hope to see, and leaves the solution open until you know more.

C. Todd Lombardo, Bruce McCarthy and their co-authors make the case in *Product Roadmaps Relaunched*. The working shape:

- **Themes, not features.** A theme is a customer problem ("new users can't tell if their first setup worked"). Features sit under it as current guesses.
- **Every theme ties to a goal.** If it can't be linked to something the business or the user needs, it moves later or goes.
- **Broad time, not dates.** Now, next, later, or rough quarters. The further out, the less certain, and the roadmap says so. Exact dates belong in a release plan, for work already shaped.
- **Ask why before when.** When someone asks for a feature by a date, the master asks what problem it solves and what the date is for. Most requests are one person's guess at a fix.

John Cutler named what happens without this a "feature factory": teams judged by what they ship, with nobody checking whether it worked. His tell is lots of care in choosing what to build and almost none in checking afterwards.

Netflix's proxy metrics, on the shelf, show outcomes done well: each team owned a number it could move in weeks that predicted members staying.

## Appetite: decide the time first.

Most planning asks "how long will this take?" and gets a guess that grows. Ryan Singer's *Shape Up*, written from Basecamp's practice, turns it round: first decide how much time the idea is worth, then design something that fits. He calls that budget the appetite. Basecamp uses two sizes: a small batch of one or two weeks, and a big batch of six.

Fixed time, flexible scope:

- **The time doesn't move.** When the budget runs out, the work ships as it is or stops. Basecamp doesn't extend by default; work that missed goes back to be rethought, so a bad bet costs one cycle, not a quarter.
- **The scope does.** Inside the budget, the team keeps cutting what's nice to have so the core gets done well.
- **Compare down, not up.** "Is it good enough?" means better than what people have now, not as good as the ideal version.

Shaping is the work before the work: setting the edges of a problem and a rough solution at the right level, solid enough that it'll fit, loose enough that the people building it still design it. A shaped piece of work names what's out of scope as clearly as what's in, because careful people otherwise build the extras.

For a side product, appetite is the most useful single tool: "two weekends for a version people can pay for" forces cuts that "when it's ready" never does.

## Story maps: the thinnest useful slice.

Jeff Patton's *User Story Mapping* gives a picture for finding the smallest thing worth releasing. Lay out what a person does, left to right, as a series of steps: sign up, set up, do the main task, see the result, come back. Under each step, stack the ways it could be done, from bare-bones at the top to deluxe at the bottom.

Then draw a line across. Everything above the line is one release: a thin version of every step, end to end. That beats a deluxe version of step one with nothing after it, because the person can actually get through, and you learn whether the whole journey is worth having.

Patton's point is that you slice to an outcome. Before drawing the line, say who it's for and what they'll be able to do. Without that, "minimum" means something different to everyone.

Buffer, on the shelf, is a story map with the line drawn hard: it launched without account settings, password reset or editing queued posts, because none of those were needed for someone to schedule a post and pay.

## Working backwards from the announcement.

Colin Bryar and Bill Carr's *Working Backwards* describes Amazon's habit of writing the press release before building anything. It's written as if the product has launched, in plain words to the customer, with a list of hard questions and answers behind it.

It makes the benefit concrete before money is spent: if the announcement is dull to read, the product will be too. The questions are where risks and awkward truths come out. A first draft should take hours, not days.

The same book carries Jeff Bezos's split between one-way and two-way doors, from his 2015 letter to shareholders. A decision you can undo should be made fast, by a few people. One you can't undo deserves the slow, careful treatment. Most of a roadmap is two-way doors; treating it all as one-way is how teams freeze.

## Goals that are outcomes.

Objectives and key results, OKRs, are a goal format: one plain-words objective saying where you want to get, and a few numbers saying how you'll know you got there. Christina Wodtke, whose *Radical Focus* is the friendliest guide, keeps it strict:

- **The objective is words, not a number.** It should make people want to start.
- **Key results are measures of change, not tasks.** "Launch the new signup flow" is a task. "Half of new signups finish setup" is a result. If you can tick it off as done, it's a task.
- **Pitch them at even odds.** Her rule of thumb is a goal you have a roughly 50/50 chance of hitting. Certain success means the bar was too low.
- **Few of them.** One objective with about three results is something a team can remember.

For a side product, one objective a quarter is plenty.

## Saying no.

Every yes is a no to something else, and leaving the no unsaid is how plans quietly fail. Apple's 1997 cuts on the shelf are the clearest case: about 15 desktop models down to one, every printer dropped, five of six store chains dropped, all serving one diagnosis. Profit came back before the iMac shipped.

The master's moves:

- **Say no early and kindly,** with the reason. A request held in a backlog forever is a no that keeps costing attention.
- **Hold the no to the goal.** "Good idea, but not for this outcome" keeps the door open without derailing the work.
- **Name what will stop.** A new priority that drops nothing is a wish.
- **Don't keep a giant backlog.** Singer's view is that ideas worth doing come back on their own. A list of hundreds is a debt nobody pays.

## Prioritising without fake precision.

Scoring models that multiply reach by impact by confidence look rigorous, but the inputs are guesses, and multiplying guesses doesn't make them true. The master uses scoring to start the argument, never to end it.

- **Size in rough brackets.** Cutler's ladder of hours, days, weeks, months, quarters, years, each in ones to threes, is precise enough to compare and loose enough to be honest.
- **Ask the cost of waiting.** What gets worse if this slips a month? Often that sorts the list faster than any score.
- **Watch the usual distorters:** the loudest customer, the biggest deal, what a competitor just shipped, an executive's latest idea. Each is a signal to weigh, not an order to follow.

## Where it goes wrong.

- **A feature list with dates.** Fix: problems and hoped-for changes, in broad time frames.
- **"How long will it take?"** Fix: "how much is it worth?", then cut to fit.
- **Extending when time runs out.** Fix: ship what's done or stop and reshape.
- **One step built deluxe, the rest missing.** Fix: a thin version of every step, end to end.
- **Key results that are tasks.** Fix: ask whether it can be ticked off; if so, find the change it should cause.
- **A score treated as the answer.** Fix: treat it as the opening of the argument.

## Examples.

- **Apple's 1997 cuts:** saying no at scale, every cut serving one policy.
- **Buffer's two-page test:** the thinnest slice that could take money, with the essentials left out on purpose.
- **Netflix's proxy metrics:** outcomes a team could move in weeks.
- **ConvertKit's commit or quit:** choosing a narrower customer, which quietly said no to everyone else.

## What a strong product leader would notice.

- The roadmap lists features, not problems.
- There's an estimate but no appetite.
- Nothing says what's out of scope.
- The first release is deep in one step and missing others.
- A key result could be ticked off as done.
- A new priority was added and nothing was dropped.
- A precise-looking score is settling a judgement call.

## More details

- Shelf files: `productcraft/research/apple-1997-cuts.md`, `buffer-two-page-test.md`, `netflix-proxy-metrics.md`, `convertkit-commit-or-quit.md`.
- Books named: *Shape Up* (Ryan Singer, 2019, free at https://basecamp.com/shapeup); *Product Roadmaps Relaunched* (C. Todd Lombardo, Bruce McCarthy, Evan Ryan and Michael Connors, 2017); *User Story Mapping* (Jeff Patton, 2014); *Working Backwards* (Colin Bryar and Bill Carr, 2021); *Radical Focus* (Christina Wodtke, 2016). Private notes on them, and on Wodtke and Cutler, are in `productcraft/library/`.
- Shape Up's appetite and batch sizes checked against "Set Boundaries", https://basecamp.com/shapeup/1.2-chapter-03 , on November 12, 2026.
- PR/FAQ first draft in hours: https://workingbackwards.com/concepts/working-backwards-pr-faq-process/ , checked November 12, 2026.
- One-way and two-way doors: Amazon's 2015 shareholder letter, https://www.sec.gov/Archives/edgar/data/1018724/000119312516530910/d168744dex991.htm , checked November 12, 2026.
- Wodtke's objectives, key results and 50/50 confidence: "The Art of the OKR" (February 1, 2014), https://eleganthack.com/the-art-of-the-okr/ , checked November 12, 2026.
- Cutler's "12 Signs You're Working in a Feature Factory" (November 17, 2016), https://cutle.fish/blog/12-signs-youre-working-in-a-feature-factory .
