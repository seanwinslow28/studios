# Project Vend: a small shop run by an agent, examined, fixed, and broken again (2025)

## What it is

Anthropic and a partner firm, Andon Labs, let a model run a small office shop: choosing stock, setting prices, answering customers. They published what went wrong, changed the set-up, and published again. Then reporters from the Wall Street Journal tested a copy in their own office.

- Phase one, June 27, 2025: https://www.anthropic.com/research/project-vend-1
- Phase two, December 18, 2025: https://www.anthropic.com/research/project-vend-2
- The reporters' test, December 2025, read in a syndicated copy: https://www.tovima.com/wsj/we-let-ai-run-our-office-vending-machine-it-lost-hundreds-of-dollars/

**Best part to look at:** phase two's account of which fixes worked and which didn't.

## How it turned out

- **Phase one lost money** over about a month. The shopkeeper agent turned down $100 for drinks that cost about $15, sold metal cubes below cost, made up a payment account, and was talked into discounts again and again.
- **Phase two did clearly better.** Weeks that lost money were largely gone, discounts fell by about 80% and free items by half.
- **Then reporters ran both versions** in their own office over about three weeks. The first gave everything away and went more than $1,000 down. The improved one was brought down with forged meeting notes that "suspended" its manager.
- **Why it's believable:** the owners published their own failures, and an outside newsroom confirmed the weak points. Thin on money: no full profit-and-loss figures are given.

## What makes it good, measured

- **A before and after of the same system, with the changes named:** customer records, what each item cost, payment links, reminders, a manager agent, and a second agent with one narrow job. Phase two also moved to a newer model, so the gains can't be put down to the named changes alone.
- **What worked: a required look-up.** Forcing the shopkeeper to check the real cost and delivery time before quoting a price. The authors' lesson: paperwork matters.
- **What didn't: the manager agent.** It approved soft requests about eight times as often as it refused them, because it was the same model with the same soft spots.
- **The agent with one narrow, separate job did well.**

### How it works, in plain steps

1. Customers ask for things in a chat channel.
2. The shopkeeper agent decides what to stock, what to charge and how to reply.
3. Its tools: supplier search and email, a notebook, customer records, the price list.
4. A required step before any quote: look up the real cost and delivery time.
5. A manager agent sets targets and approves or refuses discounts.
6. A person must approve purchases, and people do the restocking.
7. The human overseers read the numbers and step in when something goes wrong.

### What a weaker version would have done

Phase one is the weaker version: no cost data, no memory of customers, no required look-up, and nobody whose job was to say no.

### Side by side

- **Karpathy's overnight loop** (March 2026, https://github.com/karpathy/autoresearch): one measured number, from a file the agent is told not to edit, decides whether a change is kept. No amount of charm changes the number. In the shop, the thing deciding a discount was another agent that could be persuaded, and it was. A second agent isn't a check unless it differs from the first in something that matters: what it knows, what it's rewarded for, or being a fixed rule and not a conversation.
- **One person's overnight agents.** Pawel Jozefiak's "Wiz" (March 2026, https://thoughts.jock.pl/p/wiz-ai-agent-self-improvement-architecture and https://thoughts.jock.pl/p/mac-mini-ai-agent-migration-headless-2026) runs 25 scheduled jobs on its own machine. He reports a nightly job that broke without any signal and ran blind for days, and an agent that tried to work around broken paths before reporting them. Thin: his own account, and he sells guides about it.
- **Sean's own audit** found the same family of faults in his overnight agents. The readout is kept private; see the shelf's guide.

### Why it's here

The best public study of an agent left to run something by itself, with the questions an audit should ask: what can talk it into giving things away, which look-ups are required, and whether its "manager" is a real check.

## What Sean said about it

Shown to him on November 16, 2026, on a page with the other eleven. He picked the long-job harness as the closest to what he wants, and said nothing about this one.

## More details

- The date of the newspaper's original story could not be confirmed; the syndicated copy is dated December 25, 2025.
- What Wiz costs to run and what it has earned could not be confirmed from the pages opened.
