# Choosing the shape

Read this at the start of any design, before anything else is settled. The first question is how much of the work the model steers. Get this wrong and every later choice inherits it: the cost, the checks, where the person goes. A good answer is the simplest shape that does the job, with a reason for every part added on top.

## The four shapes

- **One prompt.** Ordinary code builds one request, the model answers once, and ordinary code checks the answer. The model decides nothing about what happens next.
- **A fixed workflow.** Several model calls, in an order that code decides. The model does the judging inside each step. The path is written down in advance.
- **An agent.** The model decides its own next step, in a loop, using tools, until it judges the job done. Nobody wrote the path down.
- **Several agents.** A lead agent hands pieces to helper agents, each with its own separate memory, and assembles what comes back.

Each step up buys freedom and pays for it in cost, time, and ways to go wrong. So start at the top of this list and move down only when a real failure, seen and counted, says the simpler shape can't do the job.

## The questions that decide

**Can the steps be written down in advance?** If they can, write them as code and call the model only where judgement is needed. Airbnb moved 3,500 test files in six weeks with no agent at all: a fixed script, model calls, and retries. An agent earns its place when the path can't be known ahead, because each step depends on what the last one found.

**How many steps hang on each other?** Errors multiply. Honeycomb gave the sum when it chose one call over a chain: five steps that are each right 90% of the time are right together about 59% of the time. It added that in practice the drop is less steep, and that speed was its main reason. The sum still points the right way: a chain needs a check between steps, or fewer steps.

**What does a mistake cost, and can it be undone?** Honeycomb's assistant writes a query the user can see, edit and undo, so the person is the check and nothing the model writes can break anything. When a mistake is costly and hard to see, the shape must put a check or a person exactly there. Uber's version of the same product stops for the user to confirm the tables, because the wrong table is its costly mistake.

**Is there a hard test?** Where a pass or fail can be measured by a machine, let the test be the checker and let the model loop against it. One team built a working compiler this way, and the person's real work was designing the tests. Where quality is a matter of taste, use a separate judge with written pass marks instead.

**Do the pieces depend on each other?** This decides whether to split work among agents. Splitting pays when the pieces are independent and mostly reading: searching ten sources at once. It hurts when each piece depends on the others, which includes most coding. Google's study measured both: about 81% better on a task with independent parts, and 39% to 70% worse on a task where each step depends on the last.

**What will it cost?** Anthropic's figures: an agent uses about 4 times the tokens of a chat, and several agents about 15 times. (A token is a piece of a word; models are billed by the token.) The extra has to buy something that can be named.

## Mixing fixed steps with an agent

Most good designs are a mix. Stripe's coding system is the model to copy. Code decides the order of the steps. The model decides only how to write the change and how to repair a failed test. Checks that must always run are plain code, so the model can't skip them. There is a hard stop: two rounds of tests at most, then a person takes over.

The rule of thumb: rails where the path is known, the model where judgement is needed, and a wall around all of it.

A few fixed shapes come up again and again, and are worth knowing by name:

- **A chain:** each call works on the last one's output, with a check between.
- **A router:** one call sorts the request, then sends it to the right specialist prompt.
- **Side by side:** the same job split into independent parts, or run several times and compared.
- **A lead and helpers:** one call breaks the job up, helpers do the parts, the lead assembles.
- **A maker and a checker:** one call makes, another judges against written criteria, and the work goes round until it passes or a limit is hit.

## The long-job shape

For work that runs for hours, the shelf's best example is Anthropic's: a planner, a builder, and a separate checker. Sean picked it as the closest to what he wants, and named its condition himself: it works as long as the agents are given the right tools and the right knowledge.

It was written up twice, a few months apart, and the two versions are different harnesses.

From the later one, which has the costs:

- **The checker is not the builder.** A model grading its own work is too kind to it. The checker uses the real thing, as a customer would.
- **The pass marks are written down:** four criteria, and failing any one fails the round.

From the earlier one, which had no checker:

- **Memory is plain files** that the next session reads first: what is done, what is not, what was tried.
- **The builder is told to change only the pass or fail mark** on the list it is marked against, never the list itself.

Alone, one agent finished the test job in 20 minutes for $9, and the main feature didn't work. With the later harness, in one continuous session, it took 6 hours and $200, and it worked. The author also says what stayed wrong: the checker missed deep bugs. That is the trade, stated honestly.

## Every part is a bet

Each part of a harness is a bet about what the model can't do alone. Models change, so the bets need testing again. Anthropic's later version took parts out, the short sprints and forced fresh starts, because a newer model no longer needed them, and kept the two that still paid. Vercel cut a data agent from 17 tools to 2 and it got more right, faster, on a test of five questions.

A design should say, for each part, what it is there to prevent. A part with no answer comes out.

## Several agents: the settled rule

Two rival companies argued this in public for a year and ended up close together. Both now say: start with one agent. Cognition adds a rule worth keeping: several agents may read and think at the same time, and only one writes. The failure to picture is two helpers each building half of something, and the halves not matching, because neither saw the other's choices.

When helpers are used, each gets one clearly bounded task, a stated amount of effort, and sends back a short finding. Vague one-line tasks made helpers repeat each other and miss parts of the question.

## Where it goes wrong

- **An agent where one prompt would do.** Fix: try the single prompt first and count its failures.
- **A long chain with no checks.** Fix: fewer steps, or a check between them.
- **Several agents writing at once.** Fix: many read, one writes.
- **A checker that is a copy of the maker.** In the shop on the shelf, the manager agent approved soft requests about eight times as often as it refused, because it was the same model with the same soft spots. Fix: the checker must differ in what it sees, what it is rewarded for, or by being a fixed rule.
- **A loop with no stop.** Fix: a limit on rounds, and a person after it.
- **Parts that were never taken out.** Fix: test the design again without each part when the model changes.
- **Size taken for success.** One team's hundreds of agents wrote over a million lines, and a news report had an outside developer finding most of the project's own checks failing. Fix: measure whether it works.

## Examples

All on the shelf. **Honeycomb's query assistant** is the case for one prompt. **Stripe's Minions** is the mix of fixed steps and agent steps. **Anthropic's long-job harness** is the planner, builder and checker. **Anthropic's Research system and Cognition's reply** settle when to split work. **Project Vend** shows a second agent that was no check at all.

## What a strong system designer would notice

- An agent proposed before anyone tried a single prompt.
- Steps the model chooses that could have been plain code.
- A chain of five calls and no check until the end.
- Two agents that both write to the same thing.
- A checker that sees exactly what the maker saw.
- No limit on rounds, turns or spend.
- A part nobody can say the purpose of.
- No price on the shape that was chosen.

## More details

- Every figure above comes from the shelf entries in `systemcraft/research/`, which list their sources: `honeycomb-query-assistant.md` (the 59% sum, Uber's confirm step), `stripe-minions.md` (fixed and agent steps, the two-round stop, Airbnb's migration), `anthropic-long-running-harness.md` (the $9 and $200 runs, parts removed, the compiler, Vercel's tools), `anthropic-research-and-cognition.md` (4 and 15 times the tokens, Google's study, one writer, the million-line browser), `project-vend.md` (the manager agent).
- The named fixed shapes follow Anthropic's "Building effective agents" (December 2024), in the studio's own words: https://www.anthropic.com/research/building-effective-agents
- Fundamentals, in the studio's own words: Chip Huyen's *AI Engineering* (the chapter on agents, for how errors multiply across steps) and Berryman and Ziegler's *Prompt Engineering for LLMs* (the chapters on agency and on workflows).
- Sean's words on the long-job harness are on its shelf entry, dated November 16, 2026.
