# The "lethal trifecta" rule, and a design that enforces it (2025)

## What it is

A three-part safety rule for agents, and a design from Google DeepMind that builds the rule in. The danger is prompt injection: text inside a web page, email or file that gives the model orders, which the model may follow as if they came from its owner.

- Simon Willison, "The lethal trifecta for AI agents", June 16, 2025: https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
- Debenedetti and nine co-authors, "Defeating Prompt Injections by Design", March 24, 2025, revised June 24, 2025: https://arxiv.org/abs/2503.18813
- Willison's plain account of that paper, April 11, 2025: https://simonwillison.net/2025/Apr/11/camel/

**Best part to look at:** Willison's first post. The rule fits in three lines.

## How it turned out

- **The rule:** an agent can be made to leak data when it has all three of these at once: access to private information, exposure to text written by outsiders, and a way to send things out.
- **It keeps turning up.** Willison lists 17 well-known products where researchers showed it worked.
- **The design's price is measured.** DeepMind's design, called CaMeL, finished 77% of a standard set of tasks with its protections on, against 84% for an unprotected system. Safety cost about seven points.
- **Thin spot:** no sign of CaMeL running in a product people use. It is a proven design, not a proven product. Its authors say the problem isn't fully solved, and that frequent approval requests wear people down until they approve everything.

## What makes it good, measured

- **Three items, checkable in a minute** for any agent.
- **It doesn't rely on a filter that tries to spot attacks.** Willison's point: a filter that stops 95% still fails, because the attacker tries again.
- **The fix is to take one of the three away,** not to trust the model more.

### How it works, in plain steps

1. The person makes a request.
2. A planner model writes a step-by-step plan. It never sees outside text.
3. A runner carries out the plan one step at a time.
4. When a step must read outside text, a second reader model does it. The reader has no tools.
5. Every piece of information carries a label saying where it came from.
6. Before any step that sends something out, a rule checks the labels.
7. Allowed: it goes. Not allowed: the person is asked.

### What a weaker version would have done

One agent that reads email, holds private files and can send messages, guarded by a filter. Or the same agent with an approval pop-up on everything, which people learn to click through.

### Side by side

Willison's "Designing agentic loops" (September 30, 2025, https://simonwillison.net/2025/Sep/30/designing-agentic-loops/) is the cheap version of the same idea: don't track the information, limit the damage. Run the agent in a closed-off space, give it accounts that only touch test systems, and cap its spending; his example is an account with a $5 limit. CaMeL keeps the ability and controls the flow; the loop advice removes the ability. For a one-person system the second is far easier.

### Why it's here

A safety check any design can pass or fail in a minute, with the honest cost of building it in.

## What Sean said about it

Shown to him on November 16, 2026, on a page with the other eleven. He picked the long-job harness as the closest to what he wants, and said nothing about this one.

## More details

- The 77% and 84% are on AgentDojo, a public test set for agent security.
