# Price pages and ccusage

This is how Systemcraft works out what a design will cost to run. There are two sources. The model makers' own price pages say what a token costs today (a token is a piece of a word, and models are billed by the token). ccusage, a free tool, adds up how many tokens past Claude Code runs on this Mac really used. An estimate needs both. Read this before putting a cost figure in front of Sean. Facts were checked on November 16, 2026.

## What they're best at

- **The price pages: today's price, from the company that sends the bill.** Prices move monthly, so a number from memory is a guess.
- **ccusage: evidence.** It shows tokens in, tokens out and cached tokens by day, month, session and model. A sketch that ran last week beats a rule of thumb.

Where something else beats them: for one session or one run, Claude Code's own report is enough (see below). For a real bill, the maker's billing page is the only authority. Everything here is an estimate.

## Setup

Nothing to install or buy. The price pages:

- Anthropic: https://platform.claude.com/docs/en/about-claude/pricing for pay-per-use, and https://claude.com/pricing for the monthly plans.
- OpenAI: https://developers.openai.com/api/docs/pricing
- Google: https://aistudio.google.com/docs/pricing

ccusage runs with no install. The command that proves it works prints one row per day:

```bash
npx ccusage@latest claude daily --since 20261101
```

## How to read a price page

All three pages are built the same way. Look for seven things.

1. **Price per million tokens, in and out.** Two prices for each model. On every main model read today, a token out cost five times a token in. The model's private thinking is billed as tokens out.
2. **The cached rate.** Text the maker has kept from an earlier request is re-read for a tenth of the normal price or less. Storing it costs a little extra: at Anthropic, a quarter more than the normal price to keep it five minutes. An agent (a model that picks its own next step in a loop) sends its whole history again at every step, so this rate decides most of its bill.
3. **The batch discount.** Work sent in bulk and answered later costs about half at all three. It suits overnight jobs.
4. **Charges for long requests.** Some models cost more per token once a single request passes a size. Read today: OpenAI's main models past 272,000 tokens in, and Anthropic's smallest model past 100,000. Anthropic's larger models keep one rate up to a million.
5. **Built-in tools.** Web search is charged per search on top of the tokens: $10 per 1,000 searches at Anthropic and at OpenAI today. What a search brings back is then billed as tokens in.
6. **Faster or location-bound service.** Fast modes cost about double. Keeping the work inside one country adds a tenth.
7. **Dated changes.** Opening prices end. Read today: two of Google's newest models double in price on December 1, 2026.

**A plan against pay-per-use.** A Claude plan is a flat monthly fee with limits on use per five hours and per week. Systemcraft's sketches run on the plan, so they cost nothing extra. Pay-per-use bills every token at the page's rates, and whatever another studio builds from the design may run that way. Price the design at pay-per-use rates, and say which of the two the figure assumes.

## The sum a design needs

Six numbers, written into the design:

- tokens in and out for each step
- steps in a run
- runs in a day
- the share of the tokens in that is cached
- the worst case: retries, and a loop that runs to its cap
- the cost of the checks themselves

A made-up example: an agent that drafts replies to customer emails, 200 runs a day. A usual run takes 10 steps. Each step sends 20,000 tokens in, 15,000 of them cached, and gets 500 out. A separate checker reads each draft once: 6,000 in, 300 out.

Priced for Claude Sonnet 5.5 at rates read on November 16, 2026: $2 per million tokens in, $2.50 to store new text, $0.10 to re-read cached text, $10 out. **Read the page again before using these.**

- **Usual run:** about 2 cents a step, so 21 cents with the checker. The checker is 7% of it.
- **Worst run:** the loop reaches its cap of 30 steps, nothing is cached and the checker runs twice. That is $1.68, eight times the usual run.
- **A month** is 6,000 runs. All usual: about $1,230. One run in twenty reaching the cap: about $1,670. Every run reaching the cap: about $10,000.

So the answer to "what will this cost" has three parts: a run, a range for the month, and a ceiling with the thing that enforces it. Here: "about 21 cents a run, $1,200 to $1,700 a month, and never past $10,000 because the loop stops at 30 steps."

A figure that only holds in the best case is a fault in the design, not in the sum. If the worst case can't be afforded, the design needs a lower cap, a spending limit or a cheaper model on the common steps before Sean sees it.

Two yardsticks from the shelf. An agent uses about 4 times the tokens of a chat, and many agents about 15 times. Honeycomb's one-prompt assistant, at about 1,800 tokens in and 100 out for each request, cost about $30 a month.

## Getting the best out of ccusage

ccusage reads the session records Claude Code keeps on this Mac, and changes nothing.

- **Ask for Claude Code only:** `npx ccusage@latest claude daily`. Without the word `claude`, it mixes in every coding tool it finds on the Mac.
- **The reports** are `daily`, `weekly`, `monthly`, `session` (one row for each conversation) and `blocks` (five-hour windows, the unit the plan's limits use).
- **Each row** shows the models, then tokens in, out, stored and re-read, and a cost in dollars. A made-up row: `2026-11-03 | sonnet-5-5 | 4,100 in | 96,000 out | 1,200,000 stored | 31,000,000 re-read | $14.20`. The re-read column dwarfs the rest. That is normal for an agent.
- **Useful flags:** `--since` and `--until` take dates such as `20261101`. `--breakdown` adds a row for each model. `--instances` groups by project folder and `--project` keeps one. `--json` gives the same numbers to a script.
- **The dollar figure means "what this would have cost on pay-per-use".** On the plan nobody was charged it.
- **Use it as evidence.** Run the sketch a few times, then list those sessions with `npx ccusage@latest claude session --since 20261116 --json`. Take the token counts and price them yourself from today's page. The middle run is the usual case. The largest run is the least the worst case can be.
- **Run it offline.** By default ccusage downloads a public price list from GitHub. With `--offline` it uses the list packed inside it and makes no network call.

**When Claude Code's own report is enough.** Inside a session, `/usage` shows that session's tokens for each model, a dollar estimate, and how much of the plan's limits are used. A run with nobody at the keyboard, started with `--output-format json`, ends by reporting `total_cost_usd` and tokens for each model, and `--max-budget-usd` stops it at a cap. For one run, that is enough. ccusage earns its place across many runs or days.

## Where it goes wrong

- **A price from memory.** Every figure in a design carries the date its page was read.
- **Counting only the usual run.** The cap sets the ceiling. A checker that calls a model is a cost on every run too.
- **Forgetting the history.** Step 10 of an agent sends steps 1 to 9 again. Measure a real run; don't multiply the first step.
- **Counting on the cache.** After a pause longer than the cache lasts, or a change near the start of the prompt, the whole history is billed at full price again.
- **Trusting ccusage's dollars.** They come from a price list a third party keeps, which can lag a price change. Its site says web search charges aren't counted.
- **Records that are gone.** Claude Code deletes session records after 30 days unless a setting says otherwise. Runs on another Mac stay there.
- **Counts from another model.** Anthropic's page says its newer models turn the same text into about 30% more tokens than its older ones.

## Safety

- **What goes out:** none of the records. ccusage reads local files, and its site says usage data never leaves the computer. Its one network call is the price-list download, which `--offline` stops. `npx` fetches the tool itself from npm.
- **What it shows is private.** The reports hold project folder names, session IDs, dates and how much Sean works. None of that goes on a public page or into a public repo. Examples in a design use made-up numbers.
- **What it spends:** nothing. A sketch on the plan uses up plan limits, not money.
- **Ask Sean first** before anything that would start pay-per-use billing. He has said not now.

## More details

- **Run on this Mac, November 16, 2026:** ccusage 20.0.51 through `npx ccusage@latest` (Node 22.22.2), Claude Code 2.1.325. The reports `claude daily`, `monthly`, `session` and `blocks --recent` ran, as tables and with `--json`. So did `--breakdown`, `--instances`, `--project` and `--id`.
- **Network test:** with the network blocked by `sandbox-exec`, ccusage still printed costs. With `LOG_LEVEL=4` it warned that it could not fetch LiteLLM's price list (a file on raw.githubusercontent.com) and was using the one packed inside it. With `--offline` there was no warning.
- **Claude Code's own report:** one tiny run with `claude -p`, `--output-format json` and `--max-budget-usd 0.25` returned `total_cost_usd`, `usage`, `modelUsage`, `num_turns` and `duration_ms`. `/usage` and the 30-day clean-up (the setting is `cleanupPeriodDays`) are described at https://code.claude.com/docs/en/costs, which calls its dollar figures estimates.
- **Price pages** were read through the session's fetch tool on November 16, 2026. None shows a "last updated" date. https://openai.com/api/pricing/ refused the tool, so OpenAI's developer page was read. Google's old address, ai.google.dev/gemini-api/docs/pricing, forwards to the one above.
- **ccusage sources:** its help text and the README inside the package, https://ccusage.com/guide/, https://ccusage.com/guide/cost-modes and https://github.com/ccusage/ccusage.
- **Shelf figures** are from `research/anthropic-research-and-cognition.md` and `research/honeycomb-query-assistant.md`. `research/anthropic-long-running-harness.md` has a cost published stage by stage.
- **That the plan covers runs with nobody at the keyboard** is from `choices.md`. The test run here had no pay-per-use key set.
- **Not confirmed:** how close ccusage's dollar figure comes to a real pay-per-use bill; whether it counts helper agents' tokens in full; and what the API credits listed on the plans page for the larger plans can be spent on.
