# The tools it may use, and its permissions

Read this when a design gives the model anything to act with: a search, a file, a command, an inbox, a key. A tool is whatever the model can call to do something outside its own words. The design has two halves. The first is the kit: which tools, and how well each is made. The second is the reach: what those tools can touch, and what stops a mistake from being a big one. A good design gives the model enough to do the job and makes the worst possible mistake small.

## A small kit, chosen for the job

More tools is not more capable. Every tool's description sits in what the model reads on every turn, and every extra choice is a chance to choose wrong.

- Stripe has nearly 500 tools for its coding system. Each run gets a short list picked for that job.
- Vercel cut a data-question agent from 17 special tools to 2 general ones. On its five test questions it went from four right to five, and ran about 3.5 times faster.

So a design names the tools each step may use, step by step, and gives a reason for each. A helper that only searches gets search and nothing else.

## What makes a tool good

A model uses a tool the way a new colleague would: from its name and its description, with no chance to ask.

- **The name says what it does.** One job per tool.
- **The description is written for a newcomer:** when to use it, when not to, and what comes back.
- **The inputs are hard to get wrong.** Few of them, plainly named, with the allowed values listed. A model will fill a gap with a plausible guess.
- **What comes back is short and usable.** The answer the model needs, not a dump it has to dig through.
- **An error says what to do next.** "No such file; here are the three closest names" beats a bare failure.

One tool pattern has earned its own mention: **the required look-up.** In the shop on the shelf, the second phase had the shopkeeper agent check the real cost and delivery time before any quote, and the shop did clearly better. The authors' own lesson was that paperwork matters. Two cautions: the shop moved to a newer model at the same time, and the check was asked for in the instructions, not enforced. A design should go one better. When a decision depends on a fact, fetching the fact is a step that can't be skipped.

## Reading is cheap, writing is not

Sort every tool before anything else:

- **Does it only read, or does it change something?**
- **Can the change be undone?**
- **How far does it reach?** One file, one folder, one account, everything.
- **Does anything leave?** A message sent, a page posted, money spent.

A tool that reads inside the job's own folder needs little thought. A tool that deletes, sends, publishes or pays needs a brake that sits outside the model.

## Instructions are not a brake

This is the hardest lesson on the shelf. A coding agent on a routine task hit a login problem, found a stored key, and deleted a company's live database in about nine seconds. By the founder's account, its instructions told it not to. The key worked on everything, the delete had no undo by that route, and nothing outside the agent had a say.

What the hosting company shipped afterwards was an undo: every delete now waits 48 hours before it is final. Clearer limits on keys were promised. The full lesson is three brakes, and not one depends on the agent behaving better:

- **Narrow keys.** A key that works only on test systems, and expires.
- **An undo** for anything that deletes.
- **A person for anything that destroys.** The agent can't confirm that kind of action by itself.

Add a fourth from elsewhere on the shelf: **a cap on spending**, such as an account with a $5 limit.

A rule that must hold goes in the machinery: in what the key can do, in a fixed step of ordinary code, in the walls around the run. What is written in the instructions is a request. Models follow requests most of the time, and "most of the time" is the problem.

## Walls beat prompts

There are two ways to keep an agent safe. One is to ask a person before each risky step. The other is to build walls so that nothing inside them is risky.

Stripe chose walls. Each run happens in a fresh machine with no route to live systems or the internet. Inside it the agent is free, with no approval prompts at all. That is the same freedom the deleting agent had, with different walls.

Approval prompts fail quietly. The authors of the safety design on the shelf say it themselves: frequent requests wear people down until they approve everything. So a design keeps prompts for the rare, costly thing that can't be undone, and takes the ability away for everything else.

A run with nobody at the keyboard sharpens this. There is no one to answer a prompt, so the design must say what happens at every step that would ask: allowed in advance, blocked, or saved for a person to look at later. Left unsaid, the step may simply be refused while the run still reports success, which is a failure nobody sees.

## Text from outside

Any text the model reads that its owner didn't write can carry orders: a web page, an email, a file someone sent. The model may follow them as if they came from its owner.

The check takes a minute. An agent can be made to leak when it has all three of these at once:

1. access to private information,
2. exposure to text written by outsiders,
3. a way to send things out.

The fix is to take one away, not to trust the model more. A filter that spots attacks doesn't count: one that stops 95% still fails, because the attacker tries again.

Ways to take one away, cheapest first:

- **Remove the ability.** The helper that reads the web has no private files and can't send anything.
- **Split the reader from the doer.** One model reads outside text and has no tools. Another plans and acts and never sees that text. Google DeepMind's design does this and labels every piece of information with where it came from. It finished 77% of a standard set of tasks against 84% unprotected, so safety cost about seven points.
- **Close the space.** A sealed place to run, accounts that touch only test systems, a spending cap. For a one-person system this is far the easiest.

Whatever comes back from a tool is information. It is never an instruction, and a design should say so in the place the model will read it. That helps, and it is still only a request, so the three-part check has to pass on its own.

## Checks the model can't skip

Anything that must always happen is ordinary code, not a line in the instructions.

- Stripe's style checks and test runs are fixed steps. The model can't decide to skip them.
- Spotify's coding agent, as Spotify described it in 2025, could only read, edit, and call "verify". The checks sat at the exit, and a second model blocked about a quarter of runs, most often for doing more than was asked.

A weaker cousin, for contrast: Anthropic's first long-job design tells the builder to change only the pass or fail mark on its feature list. That is a strongly worded request, not a wall.

The pattern: narrow what the model can do until the wrong move isn't available.

## Where it goes wrong

- **Every tool, every time.** Fix: a short list per step.
- **A special tool for each question.** Fix: a few general ones the model already knows how to use.
- **Vague inputs.** The model invents a value that looks right. Fix: list the allowed values, and check them in code.
- **One key for everything.** Fix: a key per job, test only, short-lived.
- **Safety by instruction.** Fix: move the rule into the key, a fixed step, or the wall.
- **An approval prompt on everything.** Fix: walls for the common case, a person for the rare one.
- **All three at once:** private data, outside text, a way out. Fix: take one away.
- **A guard that is the same model.** The shop's manager agent approved soft requests about eight times as often as it refused them. Fix: a fixed rule, or a checker that differs in what it knows.
- **No answer for the permission question at 3am.** Fix: decide each one in the design.

## Examples

All on the shelf. **The nine-second deletion** is why instructions are not a brake. **Stripe's Minions** is walls instead of prompts, and a short tool list per run. **The three-part rule and CaMeL** is the outside-text check and its honest price. **Project Vend** is the required look-up, and a guard that could be talked round. **The long-job harness** is the list the builder is asked not to rewrite: a request, where the others are walls.

## What a strong system designer would notice

- A tool list that is the same for every step.
- A tool that deletes or sends, with no undo and no person.
- A key that works on live systems when the job is on test.
- A safety rule that exists only as a sentence in the instructions.
- A step that reads the web and can also send email.
- Approval prompts so frequent that nobody would read them.
- No stated answer for what happens when a prompt appears and nobody is there.
- A tool whose error message would leave a newcomer stuck.

## More details

- Every figure above comes from the shelf entries in `systemcraft/research/`, which list their sources: `nine-second-database-deletion.md`, `stripe-minions.md` (the tool count, the sealed machine, Spotify's agent), `lethal-trifecta-and-camel.md` (the three-part rule, the 95% filter, the 77% and 84%, the $5 account, worn-down approvals), `project-vend.md` (the required look-up, the manager agent), `anthropic-long-running-harness.md` (the feature list, Vercel's tools).
- What a run with nobody at the keyboard does at a permission step is in `systemcraft/tools/choices.md`, from a test on November 16, 2026.
- Fundamentals, in the studio's own words: Berryman and Ziegler's *Prompt Engineering for LLMs* (the chapter on agency, for how a model reads a tool's name and description) and Chip Huyen's *AI Engineering* (the chapter on agents, for sorting tools by whether they read or write).
- The checklist that turns this brief into a few minutes' work on any design is in `systemcraft/tools/safety-checklist-and-sandbox.md`.
