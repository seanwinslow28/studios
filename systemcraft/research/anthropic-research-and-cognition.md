# Anthropic's many-agent Research system, and Cognition's argument against it (2025 to 2026)

## What it is

Two rival companies, the same week, on opposite sides of one question: should a job be split among several agents?

- Anthropic, "How we built our multi-agent research system", June 13, 2025. The Research feature in Claude: a lead agent plans, sends out helper agents to search at the same time, and assembles a report with sources. https://www.anthropic.com/engineering/multi-agent-research-system
- Cognition, "Don't Build Multi-Agents", June 12, 2025. The makers of the Devin coding agent argue that split-up agents make clashing choices. https://cognition.com/blog/dont-build-multi-agents
- Both came back to it: Anthropic's guidance of January 23, 2026 (https://claude.com/resources/articles/building-multi-agent-systems-when-and-how-to-use-them) and Cognition's "Multi-Agents: What's Actually Working", April 22, 2026 (https://cognition.com/blog/multi-agents-working).

**Best part to look at:** the two 2026 follow-ups side by side. They end up much closer than they started.

## How it turned out

- **Anthropic's number:** the many-agent set-up scored 90.2% better than a single agent on its own research test. That is the maker's number on the maker's test.
- **The stronger evidence is what happened next.** Anthropic's 2026 guidance says one agent handles most work, and that teams have spent months on many-agent builds a better single prompt would have matched. Cognition's 2026 follow-up says its warning holds for agents writing at the same time, but that a few many-agent patterns now work in its own product. Two rivals reaching one rule from opposite ends is the believable part.
- **Where they ended up:** both now say start with one agent. Cognition adds a rule: many agents may read and think, but only one writes.

## What makes it good, measured

- **The cost is stated plainly.** An agent uses about 4 times the tokens of a chat; many agents about 15 times. (A token is a piece of a word; models are billed by the token.)
- **Effort rules are written into the lead agent's instructions.** A simple fact gets 1 agent and 3 to 10 tool calls; a comparison gets 2 to 4 helpers; hard research more than 10. Early versions sent 50 helpers at simple questions.
- **Searching at the same time beats searching in turn.** It cut research time by up to 90% on hard questions, against the same system searching one source at a time. Anthropic's 2026 guidance says the main gain from many agents is thoroughness, not speed, and that they often take longer overall.
- **Testing started small:** about 20 real questions and one automated grader with a checklist. People still caught what the grader missed, such as helpers favouring poor websites.
- **It says where it doesn't fit:** work where every part depends on every other part, which includes most coding.

### How it works, in plain steps

1. The user asks a question.
2. The lead agent makes a plan and saves it, so the plan survives a long job.
3. The lead hands each helper one clearly bounded task.
4. Helpers search the web at the same time, each with its own separate memory.
5. Each helper sends back a short finding.
6. The lead decides: enough, or send more helpers.
7. A separate step attaches each claim to its source.
8. The report goes to the user.

The helpers only read. They never write the shared result. No person is involved during a run.

### What a weaker version would have done

One agent reading everything in a single memory until it fills up. Or helpers given vague one-line tasks, which Anthropic says made them repeat each other and miss parts of the question.

### Side by side

- **Cognition's design for coding:** one agent, one continuous thread. Its example of failure is two helpers building halves of a game that don't match, because neither saw the other's choices. By April 2026 it reports two patterns that work: a reviewer agent that sees only the finished change (about 2 bugs found per change), and a manager agent that splits work among child agents. A third, a stronger model the main agent can consult, works only when both models are strong.
- **Google Research's study** (January 28, 2026, https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/) measured it: splitting work helped by about 81% on a task with independent parts, and hurt by 39% to 70% on a task where each step depends on the last.
- **Cursor's experiment** with hundreds of agents writing a web browser (January 14, 2026, https://cursor.com/blog/scaling-agents) was measured by volume, over a million lines. The Register reported an outside developer finding most of the project's own automated checks failing (January 22, 2026, https://www.theregister.com/2026/01/22/cursor_ai_wrote_a_browser/).

### Why it's here

The most argued choice in this craft, with its price on it: when splitting a job among agents pays, when it hurts, and what it costs.

## What Sean said about it

Shown to him on November 16, 2026, on a page with the other eleven. He picked the long-job harness as the closest to what he wants, and said nothing about this one.

## More details

- Google's summary says 180 set-ups were tested; the paper's April 2026 revision says 260. The direction of the findings is the same.
- Anthropic's 2026 guidance puts many agents at 3 to 10 times the cost of one agent on the same task.
