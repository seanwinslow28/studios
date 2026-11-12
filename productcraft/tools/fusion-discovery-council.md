# fusion-discovery-council.

A paid skill that mines real complaints about a topic and turns them into a ranked list of product opportunities. It gathers fresh posts and articles, has a panel of AI models from different companies read them and propose pain points, throws out any pain point it can't trace to a quote on a page it actually fetched, and scores the rest. Read this before suggesting a run, and ask Sean before each one: every run costs money.

## What it's best at.

- **"What are people in this space complaining about, and which complaint is worth building for?"** Its core question.
- **Where competitors let their users down.** At the standard level and above it also mines review sites and competitors' weak spots.
- **Opportunities with receipts.** Each card leads with the real quote and its link, so the opportunity can be checked and the quote reused in interview questions.
- **Writing ideas.** A second mode ranks post angles for Substack instead of product opportunities.

Where something else beats it: a quick read of this month's chatter is last30days, free (this skill uses it as one of its feeds). A long cited report is Gemini Deep Research. Criticising a draft Sean already has is a different council tool. A simple lookup is a web search.

## Setup.

- **Where it lives:** the brain's council tool, `~/Code-Brain/SWCB/tools/llm-council`. It runs through uv and OpenRouter, a service that resells many companies' models under one key.
- **What it needs:** an OpenRouter key in `~/.config/swcb/secrets/openrouter-api-key`. Optional keys (Brave or Exa web search, ScrapeCreators, GitHub) widen what it gathers.
- **On the Mac Mini, November 12, 2026, no OpenRouter key was found,** and no spend has been recorded there. Until Sean adds one, it can't run on that machine. Adding the key is his to do.
- **The one command that proves it's ready,** free, calling no model:

```bash
cd ~/Code-Brain/SWCB/tools/llm-council && uv run python -m council.discovery --help && test -s ~/.config/swcb/secrets/openrouter-api-key && echo "key present"
```

## How a run works.

1. **Gather.** last30days for Reddit and Hacker News posts, Perplexity's article search, and a web search. Standard adds review sites and GitHub issues; deep adds Stack Exchange questions. Everything gathered keeps the link it came from.
2. **Read as a panel.** Several models propose pain points from the evidence. A judge model, always from a different company than the panel, merges them, so no model grades its own family's work.
3. **The gate.** Every proposed pain point must trace to a quote whose link is in the gathered evidence. If it can't, it's dropped or marked unverified, never kept quietly.
4. **Merge near-duplicates and score.** Each survivor gets a score out of 100: how much it hurts, how many people engaged and how recently, multiplied by confidence, which comes mostly from how many separate websites back it.
5. **Fill the gaps.** The report opens with a map of what the evidence missed. The session then searches for each gap itself, adds only word-for-word quotes from real pages, and a script re-fetches every page to confirm them. A gap with no honest answer stays marked "still open".

## The levels and the caps.

| Level | Panel | Judge | Most one run may reserve |
|---|---|---|---|
| quick | Gemini, Grok, DeepSeek | GPT | $3.25 |
| standard | GPT, Gemini, Grok | Claude Opus | $4.50 |
| deep | standard's three plus DeepSeek and Mistral | Claude Opus | $7.50 |

On top of each run's limit: **$30 a day and $100 a month** for this skill, plus a ceiling shared by all the council tools of $245 a day and $1,000 a month.

Two things the numbers hide:

- **The skill's own page is out of date.** It lists $0.50, $1.50 and $4.00 per run, and the deep level's confirmation prompt still says "up to $4.00". The code enforces the higher figures in the table, from its cap settings. Quote those to Sean.
- **The per-run limit checks an estimate, not the bill.** Cost swings with how much searching the panel does. The skill's notes record a standard run costing $2.74 when its limit was $1.50, and a deep run costing $0.99 the same day. The daily cap counts actual spend, so it's the real guard. A run that fails partway still records what OpenRouter billed.

Start with standard. Quick is for checking whether a topic has any evidence at all. Deep earns its price when standard's gap map says the evidence was thin in a way more sources could fix.

## Why claims without a source are dropped.

Ask a model what freelancers hate about invoicing and it will answer fluently, whether or not anyone ever said it. Plausible pain is the cheapest thing a model makes. The gate is what makes this research rather than invention: if no fetched page holds the quote, the pain point doesn't ship. A high drop count isn't a failure. It's the skill saying the evidence is thin, and it belongs in what Sean hears, beside the survivors.

## Getting the best out of it.

**Name an audience and a pain, in plain words.** "Freelance designers chasing late payments" beats "invoicing". If a broad topic returns the wrong crowd's complaints, the `--segment` option aims the gathering at one audience.

**Read the quote under every card, and ask "does it say that?"** The gate checks that the quote exists in the evidence. A second check, whether the quote actually supports the pain point, needs a small local model that isn't installed on the Mac Mini. Without it the gate checks words only, and the report says "substring-only" at the top. A real quote can still be stretched into a claim it doesn't make; that's the lead's to catch.

**Read the receipts line.** One website behind a card means single-source; two means corroborated; three or more, well corroborated. Ten posts on one site count as one site, by design. Freshness says how recent, not how true.

**Treat the proposed bet as a prompt.** Each card ends with a riskiest assumption and a cheapest test, labelled as a rule of thumb from the shape of the pain, with a blank for a person to fill in. It's a starting point, not a finding.

**Then go and test it.** A ranked complaint is a guess about demand, not demand. Take the top two or three to real buyers, Jason Cohen's ten people who'll pay, or to a cheap test like Buffer's two pages.

## Where it goes wrong.

- **A stretched quote.** Real words, bigger claim. Read the quote.
- **One loud site.** A high score from a single viral thread. Check the receipts line.
- **The gap map read as findings.** It's a list of what was missed, to investigate, never a list of things to build.
- **Running several topics in a day** and hitting the $30 cap halfway. Plan the day's runs.
- **Bypassing a limit.** `--force` skips the per-run limit and `--yes` skips the deep confirmation. Neither is used without Sean's yes for that run.

## Safety.

Every run spends money: ask Sean first, naming the level, the reserve figure, that the bill can land above or below it, and what's been spent today and this month. If the tool refuses on budget, show him the refusal and let him choose: wait, drop a level, or stop.

The topic goes to OpenRouter and through it to OpenAI, Google, xAI and Anthropic (plus DeepSeek and Mistral at deep), and to Perplexity and every site last30days searches. Keep day-job specifics out of it. The report lands in the brain's research scratch folder, which git ignores; Sean decides whether the brain keeps it, and the lead copies what the job needs into the job's folder, never this public repo.

## More details

- Skill: `~/.claude/skills/fusion-discovery-council/SKILL.md` (a link to `~/Code-Brain/SWCB/skills/fusion-discovery-council/`) and `references/run-template.md`.
- Code that sets the facts above, in `~/Code-Brain/SWCB/tools/llm-council/council/`: `discovery/tiers.py` (panels and judges), `discovery/__main__.py` (per-run reserves $3.25, $4.50, $7.50, and the deep prompt), `cap_policy.json` (discovery $30 a day and $100 a month; all tools $245 and $1,000), `secrets.py` (where keys are read).
- Output folder: `~/Code-Brain/SWCB/.runtime/research/`.
- The $2.74 and $0.99 run costs are the skill's own notes from June 21, 2026, not checked against a bill.
- Checked on the Mac Mini, November 12, 2026, read-only: no OpenRouter key, no local supporting-check model (only the narrator's model is in the brain's models folder), no spend records. Never run.
