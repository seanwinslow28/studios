# Codex as the second researcher.

Codex runs ChatGPT's model with its live web search, on Sean's ChatGPT plan, from the command line. In Productcraft it answers the same research question the lead is answering, as a second opinion from a different maker. The lead then compares the two and checks every place they disagree. Read this before any job leans on researched facts that would change a call.

## Why two researchers.

Sean chose this setup on November 12, 2026, after a blind test. Claude in the session, Codex with search and Gemini Deep Research each answered the same two questions. Graders who didn't know which report was which then opened 12 cited sources per report.

- **Codex came first on both questions.** On a tools-and-prices question, 10 of 12 checked claims were fully backed, none was wrong, and almost every source was a vendor page or a paper. On a question about turning waitlists into paying customers, it had the most numbers taken from the makers' own words.
- **Claude came a close second.** It was as accurate on the first question and found the most extra evidence. On the second, it was the broadest, but its headline number was about ten times too high: it trusted an interview over the maker's own case study. Codex had that number right.
- **Gemini Deep Research came last both times,** with 7 wrong claims on the first question and mostly SEO blogs as sources, so it came off the list.

The lesson is the pairing, not the winner. Each strong researcher caught an error the other made, and both cost nothing beyond plans Sean already pays for.

## What it's best at.

- **Facts with a source of record:** prices, plan limits, dates, what a company says on its own pages. Codex leaned hardest on primary sources in the test.
- **A cold second read of the same question.** It never sees the lead's draft, so it can't be pulled toward the lead's answer.
- **Speed.** About 4 to 7 minutes per question in the test.

Where something else beats it: what people are saying this month belongs to last30days; a question that can wait until morning and needs every quote checked word for word belongs to the overnight researcher (see `research-with-sources.md`).

## Setup.

Codex CLI is already installed and signed in with Sean's ChatGPT account. Nothing to buy. Devcraft's guide, `devcraft/tools/codex.md`, covers installing, updating and the second copy Homebrew holds.

The one command that runs a research question, saving only the final answer:

```bash
codex --search exec -m gpt-6.1-sol -c model_reasoning_effort=high \
  --skip-git-repo-check --ephemeral -s read-only \
  -o answer.md "$(cat question.txt)"
```

- **`--search` goes before `exec`.** Put after it, Codex stops with a usage error (checked on 0.163.0).
- **`-s read-only`** keeps Codex from changing any file; research never needs more.
- **`--ephemeral`** leaves no saved session behind.
- **`-o`** writes the final answer alone to the file; progress goes to the screen.
- **Keep Codex current.** An older version refused `gpt-6.1-sol` on a ChatGPT account; a newer one serves it. If the model is refused, run `codex update` and try again.

Run it in the background while the lead researches, so the two finish at about the same time.

## Getting the best out of it.

**Same question, word for word.** Write the question once, in a file, and give both researchers that file. Paraphrasing it for one of them makes the comparison meaningless. Put the output rules in the question itself: a length limit, an inline link for every factual claim, a numbered source list at the end, "say plainly where the evidence is thin," and today's date.

**Ask for first-hand numbers kept apart.** "Keep the maker's own numbers separate from roundups and vendor marketing" is what made the difference on the waitlist question. Without it, a vendor's blog post reads like evidence.

**Compare claim by claim, not report by report.** Line up the numbers that would change the call. Three cases:

- **They agree and cite different primary sources.** Good enough to use.
- **They agree but cite the same page, or two pages copying one source.** That's one source, not two. Check it.
- **They disagree.** Open the primary source yourself and settle it. This is where the errors live. In the test, the two disagreed on the waitlist headline, and the maker's own case study showed Codex was right.

**Name the winner per claim, not per report.** Sean sees one answer with its sources, not two reports. Where a disagreement couldn't be settled, say so plainly and give both numbers.

**Date-stamp everything.** Prices and limits changed within weeks of each other in the test: one researcher missed a new ChatGPT tier that had arrived six weeks earlier. Write the date each fact was read.

## Where it goes wrong.

- **A usage error and no answer.** `--search` was put after `exec`. Move it before.
- **The model is refused.** Codex is out of date. Update it.
- **Both lean on the same roundup.** Agreement looks like confirmation but isn't. Check where each claim really comes from.
- **Pages it can't read.** Some sites block automated readers: Reddit, Indie Hackers, some OpenAI help pages. A claim resting on one of them comes back unconfirmed. Say so rather than rounding it up.
- **The lead stops researching.** Codex is the second opinion, not the researcher. If the lead just copies Codex, the cross-check is gone.

## Safety.

Codex reads the web and spends nothing beyond Sean's ChatGPT plan. It posts, buys and signs in to nothing, and `-s read-only` keeps it from touching files. The question text goes to OpenAI. Keep day-job specifics and Sean's private notes out of the question unless he says otherwise; for anything that must never leave the Mac, don't use either researcher. The answer file goes in the job's folder, never in this public repo.

## More details

- The test: November 12, 2026, two questions, three researchers, graded blind on 12 claims each. Reports, shuffled copies, letter key and grade sheets were kept in that session's scratchpad; the house review page was `docs/prototypes/house-look/docs/research-bakeoff/` in the brain. Times: Codex 413 and 232 seconds, Claude 433 and 687, Gemini 357 and 366.
- Codex CLI 0.163.0, `~/.local/bin/codex`. Flag order checked with `codex exec --help` and a failed run with `--search` after `exec`.
- The refused-model note is from Sean's notes on Codex and the Mac Mini, October 2026.
- Not yet tried: Claude Code's built-in deep-research workflow, which starts several helpers that check each other. Running it needs Sean's go-ahead, since it starts many helpers at once.
