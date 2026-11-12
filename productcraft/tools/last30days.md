# last30days.

A skill that reads what people have posted about a topic in the past month, across Reddit, Hacker News, YouTube, GitHub, Polymarket, the web and, when set up, X and TikTok. It groups what it finds into stories, scores them by how many people engaged and on how many sites, and writes a brief with links. Read this before using it to judge what people want, hate or are switching to.

## What it's best at.

- **What's being said right now.** A new tool's launch reaction, complaints about a product, what people recommend when someone asks "what do you use for X?".
- **The words people actually use.** Top comments, quoted with their vote counts. Gold for interview questions and for the copy on a demand-test page.
- **Spotting movement.** Who switched, what's newly annoying, which complaint keeps coming back across sites.
- **Comparisons.** "A vs B" gets its own layout: a quick call, each side, head to head.

Where something else beats it: facts with a source of record (prices, dates, what a company says) belong to a web search or the overnight researcher. A long cited report is Gemini Deep Research. Turning complaints into ranked opportunities is fusion-discovery-council, which uses last30days as one of its feeds.

## Setup.

- **Installed:** version 3.26.0, from October 1, 2026, as a Claude Code plugin. It needs Python 3.12 or newer (the Mac Mini has 3.15). Ask for it with `/last30days <topic>`.
- **What works on the Mac Mini with no keys:** Reddit, Hacker News, Polymarket, YouTube (through the yt-dlp program, installed), GitHub (through the gh tool, signed in) and Claude's own web search. It has been used: about 64 saved briefs sit in `~/Documents/Last30Days`.
- **What isn't set up:** X, TikTok and Instagram. No settings file exists at `~/.config/last30days/.env`. TikTok and Instagram need a ScrapeCreators key (10,000 free calls, then pay as you go). Every way into X uses either Sean's own X login or a paid key, so turning it on is his call.
- **The one command that proves it works,** a health check that lists each source as working, on but unproven, broken, or available but off. When there's no recent run it makes a short free test of the keyless sources; it never touches paid ones:

```bash
python3 ~/.claude/plugins/cache/last30days-skill/last30days/3.26.0/skills/last30days/scripts/last30days.py doctor
```

## How to ask.

**Ask in the words people post in.** The skill searches posts, and posts don't sound like article titles. Its own checks catch the usual traps before running:

- **Tutorial phrasing.** "How to use Notion" matches blog titles. "Notion setup" or "Notion workflow" matches what people write.
- **A single common noun.** "Coffee" or "headphones" is a sea. Name the angle: "pour-over grinders under $200".
- **A number that collides.** "42" pulls in jersey numbers and Douglas Adams. Drop the number unless it's part of the name.

**Ask about pain, not the product idea.** "Freelancers chasing late invoices" finds people describing the problem. "An app that chases invoices" finds other apps' marketing.

**Choose the depth.** `--quick` takes about 8 to 12 items per source; the default more; `--deep` up to 50 to 70 from Reddit. `--days=7` narrows to a week, `--days=90` widens. Runs take a few minutes.

## How to weigh loud voices.

A post with 4,000 upvotes is one person's view that many people saw. Engagement measures reach, not truth, and not buyers. The craft is to count distinct people with something at stake.

- **Trust the cluster, not the post.** The skill marks a story found on one site only as "single-source" and a story with weak items as "thin-evidence". A complaint that turns up on Reddit, Hacker News and YouTube from different people outranks one viral rant.
- **First-hand beats hearsay.** For recommendations the skill ranks by signal: "I use X, here's why, here's my setup" counts most; a named expert switching and a specific number come next; a passing mention barely counts; course promotions and "comment CODE" posts count for nothing. Do the same with complaints: "I cancelled because the export broke twice" beats "this app is trash".
- **Separate what exists from what's recommended.** A tool mentioned forty times is famous, not loved. Lead with the change this month, not the incumbent everyone names.
- **Remember who doesn't post.** The people who post are not a fair sample of the people who'd pay, and the annoyed have more reason to write than the content. The bookkeeper who'd pay for a fix may never write a word online. Treat what you find as guesses to test with real buyers, Jason Cohen's ten people who'll pay, not as demand.
- **Read the top comments.** The most-upvoted reply often corrects the post. The skill quotes them with vote counts for that reason.
- **Prediction-market odds are rarely the point.** The skill treats Polymarket odds as strong evidence, which fits elections and launches. For a small product question, skip them.

## The Reddit caveat.

Reddit is the skill's richest source and its most fragile. It reads Reddit with no key, through Reddit's public site search, subreddit listings and top-comment pages, plus a third-party archive called arctic-shift. Reddit's RSS feeds switch off on November 13, 2026; version 3.26.0 already stopped relying on them.

Reading Reddit without logging in is rate-limited, and Reddit refuses some pages to data-center addresses. When that happens the skill falls back to the archive, or reports Reddit as rate-limited. That's why each brief has a partial-coverage section. A source marked partial, rate-limited, timed out or unreachable didn't come back empty; it wasn't heard. Never tell Sean "nobody on Reddit is talking about this" from a partial run. After a thin run, `doctor --postmortem` says what broke.

## Where it goes wrong.

- **A doomed query.** Article-style wording returns noise after five minutes. Reword before running.
- **Loud mistaken for many.** One viral thread becomes "users hate X". Count people and sites.
- **Silence mistaken for absence.** A blocked source read as "nobody cares". Check the partial-coverage section.
- **The wrong thing with the same name.** Two products called the same. The skill tries to pin down which one; check its pick before trusting the brief.
- **Old news in the window.** A post from this month about a year-old problem since fixed. Check whether replies say it's solved.

## Safety.

It reads public posts and posts nothing, likes nothing, changes nothing. The topic goes out as search terms to every source it reads, so keep day-job specifics out of it. Briefs save to `~/Documents/Last30Days`, outside every repo. Three things need Sean first: letting it read his browser's X login, adding any paid key, and its option to publish a feed of briefs to a public website, which is public unless password-protected. Don't use that option.

## More details

- Skill: `~/.claude/plugins/cache/last30days-skill/last30days/3.26.0/skills/last30days/SKILL.md` (setup guide, keyword-trap checks, the weighting rules under "Judge Agent" and "RECOMMENDATIONS", doctor states, and "Security & Permissions"). Changelog for 3.26.0 (the RSS change): `~/.claude/plugins/marketplaces/last30days-skill/CHANGELOG.md`.
- Source repository: https://github.com/mvanhorn/last30days-skill
- Checked on the Mac Mini, November 12, 2026, read-only: no `~/.config/last30days/.env`; yt-dlp, gh (signed in) and node present; Python 3.15. The doctor command was not run, and no search was run.
