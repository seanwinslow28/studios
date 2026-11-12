# Gemini Deep Research.

Google's research agent: give it one question and it searches, reads and cross-checks dozens of pages for up to an hour, then writes a long report with citations. The brain's gemini-deep-research skill runs it, keeps a tally of the spend and refuses to go over the caps. It costs real money every run, so read this before suggesting one, and ask Sean every time.

## What it's best at.

- **A wide question needed today.** Twenty or more sources, cross-referenced, recent, in one sitting. A landscape of every tool in a space, a matrix of prices and features across eight competitors, due diligence on a market before a call.
- **Structure across many things at once.** It's good at "for each of these, find the same five facts". A person doing that by hand loses an afternoon.
- **Charts, when asked.** It draws visuals only when the question requests them.

Where something else beats it: a single fact is a live web search. What people are saying this month is last30days. Anything that can wait until morning goes to the overnight researcher, free, with every quote checked against its page by a checker. Deep Research's report has no such checker; the checking is the lead's job.

## The two levels.

| | Standard | Max |
|---|---|---|
| Google's estimate per run | about $1 to $3 | about $3 to $7 |
| Time | 5 to 20 minutes | 20 to 60 minutes |
| Searching, by Google's own example | about 80 searches | up to about 160 |
| Built for | speed | the most thorough sweep |

Standard is the default, and most product questions fit it. Max earns its price when the question is a matrix across many things and a gap in one cell would change the call. If standard came back thin on exactly the part that matters, rerunning a sharper question at standard usually beats paying for Max on the same vague one. Google caps any run at 60 minutes and says most finish within 20.

## Setup.

- **What it needs:** a paid-tier Gemini API key from Google AI Studio, with billing turned on, saved as one line in `~/.config/swcb/secrets/gemini-api-key` (or set as `GEMINI_API_KEY`). The helper fetches its one Python package through uv on first run.
- **On the Mac Mini, November 12, 2026, no key was found in either place,** and no run has been recorded this month. Until Sean adds one, the skill can't run there. Adding the key is Sean's to do.
- **The one command that proves the setup,** without calling Google or spending anything:

```bash
uv run ~/Code-Brain/SWCB/skills/gemini-deep-research/scripts/gemini_dr.py --query "test" --tier dr --dry-run
```

It prints the level, the predicted cost, the month's spend so far and where the report would land. It doesn't check the key; a real run fails at once without one.

## The caps, and what they actually count.

The helper refuses a run that would break any of three caps, set in the skill's `budget.json`:

- **$7 for one run.**
- **$20 in a day.**
- **$50 in a calendar month,** resetting on the first.

The catch: Google's answer carries no dollar figure, so the helper records a prediction, not the bill. It counts every standard run as $2.80 and every Max run as $7.00 (the midpoint, padded by 40%). So $50 buys about 17 standard runs or 7 Max runs before the helper says no, whatever Google actually charged. The real bill lives in Google's billing page. Raising a cap is Sean's yes, never the lead's.

## Getting the best out of it.

**Write the question like a brief, not a topic.** The agent does exactly what the words ask, at length. The skill's own advice is a question that is specific, can be proven wrong, has a time window and invites citations. In practice:

- **Name who, what and when.** The audience, the thing, the years that count.
- **Say the shape you want back.** A table with named columns pulls the same facts for every row; prose lets it skip the awkward ones.
- **Say what counts as a source.** "The vendor's own pricing page", "the company's annual filing", "a survey with its year and sample". Otherwise press releases about forecast market sizes creep in as facts.
- **Ask it to label each finding** as measured, estimated or claimed by a vendor, and to date every number.
- **Ask for a chart only if Sean will look at one.**

The difference, on the same money:

- Weak: "Tell me about the AI note-taking market."
- Strong: "For solo therapists in the US in 2025 and 2026: which note-taking tools do they use, what does each cost per month, and which complaints recur in public reviews? A table with tool, monthly price from the vendor's own pricing page with the date, the review sites used, and the top three complaints with a link to each. Keep survey data apart from vendor claims. Say plainly where no source was found."

The weak one comes back as twenty pages of market forecasts. The strong one comes back as a table the lead can check row by row.

**Check its citations before anything rests on them.** Google itself recommends reviewing the citations to verify the sources. Three things to know:

- **The helper saves only the report's text.** The structured citation data Google returns beside it is skipped. Whatever links the text itself carries are what there is to check.
- **Check every number the call turns on,** not a sample. Open the cited page, find the number, note the date, and ask whether the page is the source or a copy of it. One wrong price in a pricing matrix can flip a call.
- **A missing source is a finding.** If a key number has no link, or the link doesn't say it, mark it unverified and say so to Sean once.

## Where it goes wrong.

- **A vague question, an expensive tour.** Long, confident, and no closer to a call. Fix the question, not the level.
- **Forecasts presented as facts.** "The market will reach $X billion by 2032" from a report seller's press release. Ask for primary sources up front and strike these.
- **Old pages as current.** A 2023 price quoted as today's. The date column catches it.
- **Paying for a question that could wait.** If nobody needs it before tomorrow, the overnight researcher does it free, with every quote checked.
- **Trusting the cap as the bill.** The tally is a padded guess; Google's billing page is the truth.

## Safety.

Every run spends money. Ask Sean before each one, at either level: say the level, the expected cost, the time, and what's been spent this month. The skill itself insists on that question only for Max and lets standard run on its own when there's room under the cap; Sean's answer for Productcraft is to be asked every time, so ask.

The question goes to Google. On the paid tier Google says it doesn't use prompts or answers to improve its products, but logs them for a limited time to catch misuse, and its search grounding stores prompts, context and output for 30 days. Keep day-job specifics out of the question. The helper sends only the question, never files.

The report lands in the brain's research scratch folder, which git ignores. Sean decides whether to keep it in the brain; the lead copies what the job needs into the job's folder, never into this public repo.

## More details

- Skill: `~/.claude/skills/gemini-deep-research/SKILL.md` (a link to `~/Code-Brain/SWCB/skills/gemini-deep-research/`), `decision-table.md`, `scripts/gemini_dr.py`, `scripts/budget.json` (per run $7, daily $20, monthly $50; predictions $2 and $5 times 1.4). Reports go to `~/Code-Brain/SWCB/.runtime/research/<date>-<slug>.md`; the month's tally to `~/Code-Brain/SWCB/.runtime/gemini/spend/gemini-spend-<YYYY-MM>.json`.
- Agents named in the helper: `deep-research-preview-04-2026` and `deep-research-max-preview-04-2026`, both preview.
- Google's guide (prices, searches, 60-minute limit, citations advice, visuals only on request): https://aistudio.google.com/docs/deep-research, read November 12, 2026. Prices there are estimates "subject to change".
- Google's terms for paid and unpaid use, and the 30-day storage for search grounding: https://aistudio.google.com/docs/terms, read November 12, 2026.
- Never run while writing this guide. The dry-run command was not run either.
