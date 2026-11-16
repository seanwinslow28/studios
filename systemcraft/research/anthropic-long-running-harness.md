# Anthropic's harness for long jobs: a planner, a builder and a separate checker (2025 to 2026)

## What it is

Two engineering posts from Anthropic on a set-up that lets a model build a whole web app over many hours and many separate sessions. A "harness" is everything wrapped around the model: its instructions, its tools, its memory, its checks, and the points where a person steps in.

- "Effective harnesses for long-running agents", Justin Young, November 26, 2025: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- "Harness design for long-running application development", Prithvi Rajasekaran, March 24, 2026: https://www.anthropic.com/engineering/harness-design-long-running-apps

**Best part to look at:** the second post's cost table, and the paragraph where the author takes parts back out.

## How it turned out

- **Alone: 20 minutes, $9, and the main feature didn't work.** One agent, working by itself on a brief for a retro game maker, finished fast with a broken play mode.
- **With the harness: 6 hours, $200, and it worked.**
- **A later, simpler harness on a newer model** built a music-making app in 3 hours 50 minutes for $124.70.
- **Thin spot:** it is the builder's own account. The $9 and $200 runs used the same brief, but the music app used a different brief and a newer model, so it can't be set beside the other two. The author says what stayed wrong: the checker missed deep bugs, and the music app was far from a professional program. The first post has almost no numbers at all.

## What makes it good, measured

The two posts describe two harnesses, a year's models apart.

**The second post's harness (March 2026), the one with the costs:**

- **The checker is a different agent from the builder,** because a model grading its own work is too kind to it. The checker opens the real running app in a browser and clicks through it like a customer.
- **Written pass marks.** The checker scores against four written criteria. Failing any one fails the round.
- **Parts were removed when a newer model no longer needed them.** It dropped the short sprints and the forced fresh starts the first design relied on, ran as one continuous session, and kept the two parts that still paid: the planner and the checker.
- **Cost per stage is published.** Planning cost $0.46; each checking round about $3 to $4; building was the rest.

**The first post's harness (November 2025), which had no checker:**

- **Memory between sessions was plain files:** a feature list of over 200 items that all start as "failing", a progress log, and the saved work. The builder may change only the pass or fail mark on the list, so it can't quietly rewrite the list to look finished.
- **Each new session started the same way:** read the notes, start the app, run one basic test to catch anything the last session broke, then pick one unfinished feature.

### How it works, in plain steps

The second post's harness:

1. A person writes a brief of one to four sentences.
2. The planner turns it into a full description of the product.
3. The builder builds.
4. The checker opens the running app and uses it.
5. The checker scores it against the four criteria and lists the faults.
6. Any score under its pass mark: the fault list goes back to the builder.
7. Everything passes: the person looks at the result.

### What a weaker version would have done

One agent, one long run, judging its own work: the $9 run. Or a to-do list in loose prose that the agent can rewrite to make itself look done.

### Side by side

- **A compiler built by 16 agents** (Nicholas Carlini, February 5, 2026, https://www.anthropic.com/engineering/building-c-compiler): nearly 2,000 sessions and just under $20,000 produced a 100,000-line compiler that passes 99% of most standard test sets. No planner and no checker agent: a very large set of existing tests did the checking, and the person's work was designing those tests. Where a hard test exists, let the test be the checker. Where quality is a matter of taste, use a separate judge with written criteria.
- **Vercel took parts away** (December 22, 2025, https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools): its data-question agent went from 17 special tools to 2 and got more right (4 of 5 became 5 of 5), about 3.5 times faster. Thin: five test questions. Both teams draw the same lesson: each part of a harness is a bet about what the model can't do alone, and the bet needs re-testing.
- **Karpathy's overnight loop** (March 2026, https://github.com/karpathy/autoresearch): the agent tries one change at a time for a fixed five minutes, and one measured number, from a file the agent is told not to edit, decides keep or throw away. Shopify's chief executive used a variant of it to cut one engine's processing time by 53% (https://simonwillison.net/2026/Mar/13/liquid/); a month later the change was still unmerged, with outside commenters pointing at failing automated checks.

### Why it's here

The closest worked example to a content or creative harness: a maker, a separate checker with written pass marks, and, from the earlier design, memory kept in plain files that the next session reads first.

## What Sean said about it

Shown to him on November 16, 2026, on a page with the other eleven. Asked which was closest to what he wants Systemcraft to do, he picked this one:

> "It fits what we've already been working on and it's worked as long as we provide the right tools and the right knowledge."

What the lead takes from that: he is choosing the shape he has already seen work, and he names the condition himself. A harness is only as good as the tools and the knowledge its agents are given. That is a taste rule to propose when the taste page is written, in his words.

## More details

- Vercel's headline says 80% of tools removed; its own code shows 17 cut to 2.
- Karpathy's project page reports no result numbers of its own, only the pace: about 12 experiments an hour.
