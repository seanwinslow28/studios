# Research with sources.

Three free ways to find out what's true, each with every claim tied to where it came from. Claude's own web search answers a question in minutes. The research skill sends a helper off to dig while the lead keeps working. The brain's overnight researcher answers one question while Sean sleeps and hands back a brief in the morning. Read this before any job leans on a fact found on the web.

## What it's best at.

- **Claude's own web search, live:** a handful of facts, a price, a date, what a company says on its own site. Fastest, and the lead reads the pages itself.
- **The research skill:** a question that needs reading across many pages, such as how three competitors price or what a standard actually says. It starts a helper in the background, tells it to use primary sources (the maker's own page, the paper, the filing, the official docs) and to follow every claim back to the source that owns it, and has it write one file with each claim's source beside it.
- **The overnight researcher:** a question that can wait until morning and deserves depth. It works alone on the Mac Mini, searches and reads the web, and returns a short brief: a direct answer, findings, the gaps it couldn't fill, and the sources. Every claim rests on a quote that a separate checker fetches from the cited page and finds, word for word.

Where something else beats them: what people are saying this month belongs to last30days; a 20-source report needed today belongs to Gemini Deep Research, which costs money; finding products worth making belongs to fusion-discovery-council.

## Setup.

- **Web search and page fetch** come with Claude Code. Nothing to install, nothing to pay on Sean's plan. Search results are from the US only.
- **The research skill** is installed from Matt Pocock's skills. Ask for it by name ("research this") or let it load when a job says "research".
- **The overnight researcher** lives in the brain. A job reaches it as a work ticket: a short file holding one question as its title and a goal of a few sentences, written in a live session, saved to the brain's queue, and run only after Sean marks it ready. The night run picks up every ready ticket in turn. Each gets about 45 minutes, 80 turns and $8 of model time measured at API prices, though it runs on Sean's subscription. The brief sits in the morning queue, with a ruling from the checker on whether its quotes held up.

The one command that proves the overnight machinery works, with a stand-in model and stand-in pages, spending nothing:

```bash
cd ~/Code-Brain/SWCB/agents/researcher && uv run pytest -q
```

## Getting the best out of it.

**Primary over secondary.** A primary source is the thing itself: the company's pricing page, the founder's own write-up, the filing, the study. A secondary source is someone describing it. Use secondary only when no primary exists, and say so. The shelf shows why. Bing's ad headline win appears as "over $100 million a year" in the published article and as $120 million in one of Kohavi's talks. A blog that repeats the bigger number isn't lying, but it isn't the source either. Quote the article.

**Check the claim against the original, not the summary.** Claude's page fetch hands back a small model's reading of the page, not the page. A "quote" from it can be quietly reworded. When a quote matters, ask the fetch for the exact sentences, copied word for word, then check that the numbers, names and dates in the claim appear in them. The overnight researcher has a tool for this that runs the checker's own fetch and match, and a brief whose quotes don't match is stopped before Sean sees it.

**Never let a claim outgrow its source.** The usual ways a sentence says more than the page does:

- "Most" or "all" where the page says some, or speaks for one person.
- "Is" where it says "may be"; "launched" where it says "plans to launch".
- A cause or a count the page never gives.
- A detail from a different page folded into the sentence.

**Date every fact.** Write when the source said it, and prefer the newest primary source when two disagree. A price is a fact about a day. The shelf piece on Superhuman puts its revenue as "a reported $35 million a year" and the Grammarly purchase in July 2025. That tells the reader both the age of the number and that nobody has confirmed it.

**Keep measured results apart from opinion and marketing.** A study, a documented test or a filed number is evidence. A vendor's "most accurate data", a founder's own story and a review site's ranking are claims. Say which a finding is when it matters to the call. Jason Cohen's 30 people agreeing to pay $50 a month before WP Engine existed is his own account, with no second source; the shelf says so.

**Write the overnight question narrowly, with a goal that says why.** The researcher sees the question, the goal and today's date, and nothing else of Sean's. Put in the goal what would change the call and what to keep apart. A good one: "How do freelance bookkeepers in the US find new clients: which channels, what share come from referrals, and what they pay for software each month. Give each survey's year and sample, and keep survey results apart from vendor marketing." A weak one: "Research bookkeeping software." The first comes back as numbers with dates; the second comes back as a tour.

**Name the pages it can't read.** The checker fetches plainly: no JavaScript, no login, no PDFs, no paywalls. A claim resting on such a page comes back unconfirmed, and one unconfirmed citation keeps the whole brief from passing. If the answer lives in a PDF report, say so in the goal, or look it up live instead.

## Where it goes wrong.

- **A chain of copies.** Five articles agree because they all quote one press release. Count the original once.
- **A reworded quote.** The fetch "quoted" something the page never said. Check the exact words before they go in front of Sean.
- **An old fact dressed as new.** A 2023 survey cited as if current. Look for the date first, then the number.
- **The research file in the wrong place.** The research skill saves "where the repo keeps notes". In Productcraft that means the job's folder, outside the studios repo, which is public. Never a tracked file here.
- **An overnight ticket that's really two questions.** The researcher stops and asks Sean to pick a reading, and a night is gone. One question per ticket.
- **A brief with thin evidence, rounded up.** The researcher is told to say so in the answer when evidence is thin. Read the gaps section before the answer.

## Safety.

All three read the web and spend nothing beyond Sean's plan. They post, buy and sign in to nothing. What leaves the Mac is the search terms and, for the overnight researcher, the question and goal. Keep day-job specifics out of all three. An overnight ticket is open by default and becomes private when its background comes from day-job work or a private note. Private doesn't change where the text goes: the question and brief still go to Claude and to an OpenAI model that judges the result. Anything that must never leave the Mac doesn't go to the researcher at all, because it has no local-only setting. Ask Sean before marking any ticket ready; that step is his.

## More details

- Research skill: `~/.claude/plugins/cache/mattpocock/mattpocock-skills/1.3.1/skills/engineering/research/SKILL.md`.
- Overnight researcher: `~/Code-Brain/SWCB/agents/researcher/README.md` and `instructions.md`; the ticket kind, budget and checks in `~/Code-Brain/SWCB/queue/types/research-brief.md` (budget 45 minutes, 80 turns, $8; findings up to 3,000 words; answer up to 150 words; at least five sources; quotes 5 to 50 words). Night run and ticket terms: `~/Code-Brain/SWCB/CONTEXT.md`.
- The "US only" limit on search comes from Claude Code's own web search tool description, November 12, 2026.
- Shelf examples used: `productcraft/research/bing-headline-test.md`, `superhuman-fit-engine.md`, `cohen-ten-who-will-pay.md`.
- Read on the Mac Mini, November 12, 2026. The pytest command was not run.
