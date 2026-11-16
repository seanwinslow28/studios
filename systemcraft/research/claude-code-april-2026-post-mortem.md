# Why Claude Code got worse for a month, in its makers' own words (2026)

## What it is

Anthropic's write-up, published April 23, 2026, of why its coding agent felt worse to users for several weeks. The cause was three small changes to the harness, the set-up wrapped around the model. The model itself hadn't changed. A write-up like this is called a post-mortem: what broke, why, and what changes now.

- "An update on recent Claude Code quality reports", April 23, 2026: https://www.anthropic.com/engineering/april-23-postmortem
- An earlier one of the same kind, September 17, 2025: https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues

**Best part to look at:** the three changes with their dates, and the paragraph on how the second one got through every check.

## How it turned out

- **All three were undone or fixed by April 20, 2026,** and usage limits were reset for every subscriber on April 23.
- **Why it's believable:** it gives dates and version numbers, admits that two of the three got past the company's own tests, and that the first was shipped knowing it cost a little quality, a trade it now calls wrong.
- **Thin spot:** it is the company's own account, published after weeks of public complaints. No outside party has rebuilt the story.

## What it shows, measured

| The change | Live | What it did |
|---|---|---|
| Thinking effort lowered by default, to cut waiting | March 4 to April 7 | Users found it less capable. |
| A cost-saving step meant to clear old reasoning once, after an hour idle | March 26 to April 10 | By mistake it cleared it on every turn. The agent seemed forgetful and repeated itself. |
| New instructions capping replies at 25 words between steps and 100 at the end | April 16 to 20 | A wider test later showed a 3% drop in quality. |

- **The second change passed everything:** human review, automated review, the small tests, the full tests and in-house use. It still took over a week to trace.
- **Each was pinned down alone.** For the third, the team removed instruction lines one at a time on a wider test set until the drop showed.
- **The fixes are rules for the makers:** more staff use the exact build the public gets, every instruction change gets a wide test, and anything that trades away quality rolls out slowly.

### How the investigation worked, in plain steps

1. Users say the product feels worse.
2. The company's own tests say it's fine.
3. The reports keep coming, so an investigation opens.
4. The team traces the complaints to three separate changes made in the period.
5. The hardest to find is pinned down by removing instruction lines one at a time on a wider test.
6. Each change is undone or fixed.
7. New standing rules are written so the same kind of change is caught sooner.

### What a weaker version would have done

Trusted the green tests and told users nothing had changed. Or undone all three changes together without learning which one did the harm.

### Side by side

- **GitLab's database outage** (written up February 10, 2017, https://about.gitlab.com/blog/postmortem-of-database-outage-of-january-31/). The nightly backups had been failing. The system did send failure emails, but the receiving mail server rejected them, so nobody saw one. When an engineer deleted about 300 GB from the wrong database, the freshest usable copy was a snapshot taken by hand about six hours earlier. Claude Code's case is "the tests couldn't see the problem"; GitLab's is "the alarm rang in an empty room". An audit should ask both.
- **Sean's own audit** of his overnight agents found the second kind: the watchdog spotted the failure and wrote it to a file nobody reads. The readout is kept private; see the shelf's guide.

### Why it's here

The best published audit of a running AI system: the dials around the model are part of the design, and a check that says "fine" isn't proof.

## What Sean said about it

Shown to him on November 16, 2026, on a page with the other eleven. He picked the long-job harness as the closest to what he wants, and said nothing about this one.

## More details

- The September 2025 write-up has harder numbers: one fault touched about 0.8% of requests at first and 16% at its worst hour.
- The post doesn't lay its investigation out as steps; the list above is the lead's reading of it.
- GitLab lost roughly 5,000 projects, 5,000 comments and 700 new accounts, and was down about 18 hours.
