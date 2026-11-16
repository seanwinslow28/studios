# Stripe's "Minions": coding agents on fixed rails (2026)

## What it is

Stripe's in-house system that takes a request from an engineer and returns a finished code change, with nobody steering in the middle. Stripe engineer Alistair Gray wrote it up in two posts.

- Part 1, February 9, 2026: https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents
- Part 2, February 19, 2026: https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2

**Best part to look at:** Part 2, which names the design: a flow that mixes fixed steps with agent steps.

## How it turned out

- **Over 1,000 merged code changes a week** written entirely by the system, per Part 1; over 1,300 ten days later, per Part 2. A person reviews every one before it's merged.
- **Thin spot:** the numbers are Stripe's own. It publishes no failure rate and no count of runs thrown away. They're still believable, because reviewed changes in a payments company's code are costly to get wrong.

## What makes it good, measured

- **The model is used only where judgement is needed.** Fixed steps (run the style checks, push the work) are plain code that always runs. Agent steps (write the change, fix a failing test) are the model's.
- **A hard stop: two rounds of the full tests, at most.** If the second round fails, a person takes over. Stripe says more rounds bring little.
- **A small kit, chosen for the job.** Nearly 500 tools exist, for Stripe's own systems and outside products; each run gets a short list.
- **Walls, so no permission prompts.** Each run happens in a fresh machine that starts in about 10 seconds and has no route to live systems or the internet. Inside it the agent is free.
- **Fast check before slow check.** Style checks take under five seconds and run first, ahead of tests picked from a set of over three million.

### How it works, in plain steps

1. An engineer asks in a chat thread, or presses a button on a ticket.
2. Ordinary code collects the thread and linked pages, so the agent starts informed.
3. A clean, sealed work machine starts.
4. Agent step: write the change.
5. Fixed step: run the style checks. The agent loops here until they pass.
6. Fixed step: push the work; the full tests run.
7. Agent step: fix what failed, once. Then a second test run.
8. Still failing: it goes back to the engineer. Passing: a person reviews it and decides.

Fixed code decides the order of the steps. The model decides only how to write and repair the code. The person is at the start and the end, never in the middle.

### What a weaker version would have done

Given one agent every tool and let it decide when to check, test and push. That agent sometimes skips a check, loops on the tests burning time and money, and needs a person approving each risky command.

### Side by side

- **Ramp's "Inspect"** (https://builders.ramp.com/post/why-we-built-our-background-agent, about January 2026) is a conversation, not a one-shot: people send follow-ups while it works, and the agent proves its work with screenshots and live previews. Ramp reported about 30% of its merged changes at first and 74% by October 27, 2026 (https://ramp.com/blog/introducing-inspect). Stripe bets on rails and a hard stop; Ramp on a rich workspace with a person nearby.
- **Spotify's "Honk"** (November 6 and December 9, 2025, https://engineering.atspotify.com/2025/12/feedback-loops-background-coding-agents-part-3) leaves the order of work to the agent and puts the checks at the exit: the agent can only read, edit and call "verify", and a second model blocks about a quarter of runs, most often for doing more than was asked.
- **Airbnb's test migration** (about March 2025, https://airbnb.tech/?p=366) went the other way: no agent at all. A fixed script with model calls and retry loops moved 3,500 files in six weeks; 75% were done in the first four hours, 97% after four days of tuning.
- **The nine-second deletion** (`nine-second-database-deletion.md`) is the same freedom without the walls.

### Why it's here

The best current example of mixing a fixed workflow with an agent: rails where the path is known, the model where judgement is needed, walls around all of it, and a person at both ends.

## What Sean said about it

Shown to him on November 16, 2026, on a page with the other eleven. He picked the long-job harness as the closest to what he wants, and said nothing about this one.

## More details

- Part 1 never uses the word "blueprint"; the fixed-step and agent-step design is named only in Part 2.
- Ramp's and Spotify's numbers are also their own. A March 2026 conference report says Spotify later removed its second-model check as models improved; Spotify's own posts don't confirm that.
- Airbnb's "a year and a half by hand" is an estimate, not a measured comparison.
