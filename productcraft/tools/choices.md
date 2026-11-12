# Productcraft's tool list

The tools Productcraft uses, one pick per kind of work, with Sean's yes or no. Scouted on November 12, 2026 for today's best, not for what the last setup used. Each tool gets a mastery guide in this folder before the lead uses it on a job.

Sean said yes to the whole free list on November 12, 2026: use what's on the Mac, add parakeet, and open free Tally and Stripe accounts when a job first needs a test. Anything paid is asked about first, when a job needs it. Later that day, after a blind test of three researchers, Sean chose Claude plus Codex for research and took Gemini Deep Research and the discovery council off the list.

The short version: nothing new needs buying. The skills already installed cover the product methods (interviews, assumption maps, sizing, pricing, test analysis), so a separate "AI product manager" app would add nothing. What's missing is a few free accounts for real-world tests, each opened only when a job needs it.

A few words used below: a **skill** is a packaged set of instructions Claude loads for a kind of task; a **connector** links Claude to an app like Granola or Figma; a **demand test** checks whether people want something before it's built.

## The list

| Kind of work | The pick | Cost | Have it? | Sean's answer |
|---|---|---|---|---|
| Quick research with sources | Claude's own web search plus the research skill; the overnight researcher for anything that can wait until morning. | Free | Yes | Yes. |
| What people are saying right now | last30days, which reads the past month of Reddit, Hacker News, YouTube and more. | Free | Yes | Yes. |
| Research that changes a call | Two researchers on the same question: the lead in the session, and Codex with ChatGPT's live search as a second opinion. The lead checks every place they disagree. | Free, on the Claude and ChatGPT plans | Yes | Yes, after a blind test on November 12, 2026. |
| Finding products worth making | last30days for real complaints, then the two researchers to check what's found. | Free | Yes | Yes. |
| Market size and competitors | The market-sizing skill on free sources: company filings, Google Trends, Similarweb's free view, app store lookups. | Free | Yes | Yes. |
| The product methods | The installed product skills: interview scripts, assumption maps, opportunity trees, strategy and pricing, pre-mortems, test analysis. | Free | Yes | Yes. |
| Recording and transcribing calls | Granola's free plan for calls Sean may record, with its training switch off; parakeet-mlx on the Mac for anything sensitive, which never leaves the machine. | Free | Granola yes; parakeet is one command to add | Yes. |
| Making sense of interviews | The interview-summary skill plus Claude, with every quote checked against the transcript. Claude sends the text to Anthropic, so a sensitive transcript is summarized with a local Ollama model or after Sean's yes. | Free | Yes | Yes. |
| Surveys | Tally's free plan, which Claude can drive. | Free account | No | Yes. |
| Cheap demand tests | A page the lead builds, a Tally waitlist, and a Stripe payment link when it's time to ask for money. | Free; Stripe takes 2.9% plus 30¢ per payment | No (two free accounts) | Yes. |
| Clickable prototypes | Claude artifacts. | Free | Yes | Yes. |
| Reading numbers honestly | Google Sheets plus Python run through uv, with the A/B test and data-check skills. | Free | Yes | Yes. |
| Analytics for a live side product | PostHog, free up to a million events a month. Only once something is live. | Free | No | Yes. |
| Diagrams and docs | Mermaid for diagrams (already installed) plus Claude Docs or Google Docs. | Free | Yes | Yes. |

## Paid, only when a job needs it

- **Recruiting strangers to interview:** Respondent, about $40 to $80 a session plus the payment to the person, when a job needs business buyers Sean can't reach himself. Free channels come first. Runner-up: User Interviews, $49 a session plus payment.
- **Real search-volume numbers:** DataForSEO, about $50 once, if a job turns on how many people search for something.
- **A transcriber that labels speakers:** MacWhisper Pro, about $69 once, if parakeet's unlabelled transcripts get in the way.

## Runners-up and not now

- **Gemini Deep Research:** off the list. In the November 12 test it came last on both questions, with 7 wrong claims on one and mostly SEO blogs as sources, at about $2.80 a run. Codex came first and Claude a close second, both at no extra cost. `tools/codex-research.md` has the results.
- **The discovery council:** parked. Its backlog in the brain holds 13 open problems, mostly about cost: runs costing up to 3.7 times their estimate, and spend records that trip the daily cap early. Worth another look only once those are fixed.

- **Research:** Exa search, $10 free a month, its key already expected. Perplexity Max and ChatGPT Pro add a second big bill for little gain over what's here.
- **Interviews:** Dovetail, about $4,800 a year, built for research teams, not one person. Otter is weaker than Granola.
- **Surveys:** OpinionX's free plan for ranking and price questions; Typeform's free plan is too small.
- **Demand tests:** Carrd, $19 a year, if a page needs to live longer than a test. No paid ads until a free waitlist shows interest.
- **Prototypes:** Figma Make's free plan (its connector needs Sean to sign in). Paid v0, Lovable or Bolt only if Claude artifacts fall short.
- **Analytics:** Plausible, $9 a month, not before there's a product.
- **Data:** paid Crunchbase, Similarweb or Appfigures plans. The free views give rough ranges, enough for a first call.

## Privacy

Day-job material is the care point. Day-job jobs keep their folders in Sean's private work repo.

- **Only two things never leave the Mac:** the local Ollama models and parakeet-mlx. They're the choice for anything from the day job that mustn't go to an outside service.
- **Granola's free plan trains on anonymised notes unless the switch is off.** Whether his employer allows Granola on work calls is Sean's to check.
- **Claude's consumer plans can train on chats unless the setting is off.** Worth confirming it's off.
- **Stripe's connector can move money.** If it's ever connected, test mode first and approval on every action.

## Things to know

- **Search volume is hard to get free.** Google's Trends programming access is invite-only and the old scraper is broken; the Trends website still works by hand.
- **Reddit's own programming access closed to new applications on October 31,** reportedly. last30days reads it another way.
- **Free traffic and app numbers are rough ranges only.**

## More details

**Checked on this Mac, November 12, 2026, read-only:** Mermaid's renderer 11.15.0, uv 0.10.3, pandoc, ffmpeg, gh, sqlite3, jq, the Gemini and Codex command-line tools, Ollama with qwen3 models. Apps: Granola, Obsidian, Google Docs and Sheets, Numbers, Claude, ChatGPT, Ollama. Connectors working: Google Drive, Gmail, Google Calendar, Claude Docs. Waiting for sign-in: Granola, Figma, Slack, Hex, Amplitude, Atlassian. Not installed: any transcriber, DuckDB, Jupyter, the Python data libraries (fetched per run with `uv run --with pandas`).

**Prices** read from vendor pages on November 12, 2026, except these from third-party write-ups: Lovable, PostHog's free limit, MacWhisper, Perplexity and ChatGPT research limits. OpenAI's pricing page blocked the fetch.
