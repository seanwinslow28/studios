# What it costs to run

Read this when a design has a shape, and again before it goes to Sean. A design without a price isn't finished. The price is more than the model's bill: it is money, waiting time, and the hours a person spends checking the output. A good design gives a range for each, says what would push it to the top of the range, and has a ceiling that holds even when everything goes wrong.

## What the bill is made of

Models are billed by the token, which is a piece of a word. A request costs what goes in plus what comes out, and the two are priced differently: what comes out usually costs several times more per token than what goes in. The price page says how much, and it changes, so read it at the start of every job.

Four things multiply the bill:

- **Tokens per call.** Everything the model is shown: instructions, tool descriptions, files, the conversation so far.
- **Calls per run.** One for a single prompt. Dozens or hundreds for an agent.
- **Runs per day.**
- **Checks.** Every judge, every test round, every retry is more calls.

An agent has a fifth multiplier that is easy to miss. On every turn it reads the whole conversation so far again. So a run twice as long costs much more than twice as much. Long runs are where bills surprise people.

## The shape sets the price

The biggest cost decision is made before any tuning: which shape. The shelf has the numbers.

- **One prompt.** Honeycomb's assistant sends about 1,800 tokens in and gets about 100 out per question. The whole feature cost about $30 a month.
- **An agent** uses about 4 times the tokens of a chat. **Several agents** use about 15 times.
- **A long-job harness.** One agent alone: 20 minutes and $9, and the main feature didn't work. With a planner, builder and checker: 6 hours and $200, and it worked.
- **A very large job.** The compiler built by 16 agents took nearly 2,000 sessions and just under $20,000.

None of these is too much or too little. Each is a price for a result. The design's job is to say which result is being bought and why a cheaper shape wouldn't deliver it.

## Price each stage

The long-job harness on the shelf publishes its cost by stage: planning $0.46, each round of checking about $3 to $4, and building the rest. That is the form a cost estimate should take.

For each stage, write down:

- tokens in and out for a usual call,
- how many calls in a usual run, and how many at the limit,
- what that stage is there to buy.

A stage that costs a lot and buys little stands out at once. So does a cheap stage that carries a lot of the design, like the checker at a few dollars a round.

## State a range, and make the worst case honest

One number is a guess presented as a fact. Give three:

- **The usual run.**
- **A bad run:** every retry used, the loop running to its limit, the checker failing the work twice.
- **The ceiling:** the most it can spend before something outside the model stops it.

Then multiply by runs per day for a monthly figure, with the same range.

A design whose sums only work in the usual case has a fault, not an optimistic forecast. If a bad night costs ten times a good one, that goes in front of Sean before he approves it.

The best evidence is a real run. A cheap sketch of the design, run a few times, gives measured tokens per stage. Past runs on the Mac give the same for work already being done. An estimate built from those beats one built from reasoning.

## Ceilings that don't depend on the model

A model can't be trusted to notice it is spending too much. The limits sit outside it:

- **A spending cap per run,** and a limit on turns.
- **A limit on rounds.** Stripe stops after two rounds of the full tests, and says more rounds bring little.
- **A daily limit per user,** as Honeycomb set, which caps cost and abuse together.
- **An account with a small limit** for anything experimental. The shelf's example is $5.

Loops are where money goes. One team that tried an overnight loop spent about $800 and found some features the agent had called done that didn't work. A loop needs a ceiling and a real test of "done", or it buys nothing at a high price.

## Where the savings are

In rough order of how much they save:

- **A simpler shape.** One prompt instead of a chain; one agent instead of several.
- **Showing the model less.** Honeycomb sends only the data fields used in the past seven days, out of more than 5,000. Fewer tools means fewer descriptions read on every turn.
- **Shorter runs.** A fresh start with a short note costs less than one endless conversation, because of the re-reading. Whether it works as well is a bet to test.
- **Shorter answers.** What comes out costs the most per token.
- **A smaller model for the easy steps.** Sorting, extracting and formatting rarely need the strongest model. The step that plans, or that must get a long chain right, does.
- **Keeping the front of the prompt the same.** Makers charge less for text they have seen recently, so instructions and reference material go first and stay unchanged, and the part that varies goes last.
- **Work that can wait.** Makers charge less for requests that don't need an answer straight away.

How much each of the last three saves is on the price page, and changes. Never quote a discount from memory.

## The cost of being cheap

Cutting cost can cut the thing being paid for, and it does so quietly.

- **Klarna** judged its assistant mostly on speed, volume and cost. Fifteen months later its chief executive said cost had weighed too heavily and quality had suffered.
- **Claude Code** got worse for a month through three changes. Two were made to save cost or waiting: the default thinking effort was lowered, and a step meant to clear old reasoning once ended up clearing it every turn. Users noticed before the tests did.

The rule the makers took from it is a good one for any design: a change that trades quality for cost goes out slowly, and is measured on quality, not only on the saving.

So a cost line always sits beside a quality line. A saving that isn't checked against quality is unproven.

## A person's time is part of the price

- **Reviewing.** If a person must look at every output, how many minutes each, and how many a day? A design that makes more than its reviewer can read has moved the cost onto the person.
- **Approving.** Every approval prompt costs attention, and people stop reading them.
- **Effort.** In the partner study on the shelf, the partner that asked questions kept people's ideas varied and their own, and people also found it harder work. That is a real cost, and sometimes worth it.
- **Waiting.** Six hours is fine overnight and useless in a conversation. Say which the design is for.

## A plan against pay-per-use

Sean's Claude plan covers Claude Code, including runs with nobody at the keyboard, up to the plan's limits. A design that runs as a standalone program is billed differently. So far that has meant a separate account billed by the token; whether the larger plans' credits cover it is not confirmed. Either way the sum changes completely, so a design says which it assumes. A plan's limits are also a ceiling of their own: a heavy overnight run can use up what the next morning's work needed.

## Where it goes wrong

- **No price at all.** Fix: a figure per stage, per run and per month.
- **One number.** Fix: usual, bad and ceiling.
- **A price from memory.** Fix: read the page today and date it.
- **The usual case only.** Fix: price the loop at its limit.
- **No ceiling outside the model.** Fix: caps on spend, turns and rounds.
- **Savings with no quality check.** Fix: measure both.
- **The reviewer's time left out.** Fix: count minutes per item.
- **The strongest model everywhere.** Fix: match the model to the step.
- **One endless conversation, never priced.** Fix: price it against fresh starts with a short note.

## Examples

All on the shelf. **Honeycomb's query assistant** is the small, priced, capped design. **The long-job harness** is cost published by stage, and the honest gap between $9 and $200. **Anthropic's Research system** is the price of splitting work among agents. **Klarna's walk-back** and **the Claude Code post-mortem** are what cost-cutting does when quality isn't watched.

## What a strong system designer would notice

- A design with no price on it.
- A single figure with no range.
- No answer to "what is the most this can spend in one night?"
- A loop with no test of "done".
- Every step on the strongest model.
- A saving claimed with no quality number beside it.
- More output than the reviewer could ever read.
- A price quoted without a date.

## More details

- Every figure above comes from the shelf entries in `systemcraft/research/`, which list their sources: `honeycomb-query-assistant.md`, `anthropic-research-and-cognition.md` (4 and 15 times), `anthropic-long-running-harness.md` (the $9 and $200 runs, cost by stage, the compiler), `stripe-minions.md`, `lethal-trifecta-and-camel.md` (the $5 account), `klarna-assistant-walk-back.md`, `claude-code-april-2026-post-mortem.md`, `question-asking-partner-study.md`. The $800 overnight loop is in `systemcraft/research/README.md`.
- What the Claude plan covers, and what needs a pay-per-use account, is in `systemcraft/tools/choices.md`, with Sean's answer of November 16, 2026.
- How to read a price page, do the sum and add up past runs is in `systemcraft/tools/price-pages-and-ccusage.md`.
- Fundamentals, in the studio's own words: Chip Huyen's *AI Engineering* (the chapters on inference and on architecture, for where cost and waiting time come from, and for cheaper rates on repeated and delayed work).
