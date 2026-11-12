# Market sizing and competitors.

How big the prize is and who's already there, on free sources only. Two installed skills give the shape of the work: market-sizing and competitor-analysis, from the product market-research plugin. The numbers come from public filings, government counts, the Google Trends website, Similarweb's free view and app store lookups. Read this before putting a market size or a competitor's numbers in front of Sean.

## What it's best at.

- **A first call on "is there enough here?"** For a small product the question is rarely "is this a billion-dollar market". It's "are there a few hundred reachable people who'd pay, and who else is selling to them?"
- **A map of the rivals:** who they are, what they charge, roughly how much traffic or how many app ratings they have, and what their customers complain about.
- **Finding the assumption that matters.** A sizing done well ends with the one guess the whole number hangs on.

Where it's weak: free numbers are rough ranges, never precise. When a job turns on real search volumes, real traffic or real download counts, the paid options in the tool list (DataForSEO, paid Similarweb or Appfigures) are Sean's call.

## Setup.

- **The skills:** `pm-market-research:market-sizing` estimates three sizes, top-down and bottom-up, with assumptions and a confidence for each. `pm-market-research:competitor-analysis` picks five direct competitors and profiles each: product, pricing, strengths, weaknesses, and gaps to exploit. Both search the web as they go. Free, installed.
- **The sources:** all free websites. Similarweb's fuller free view needs a free account, which Sean would open.
- **The one command that proves the free lookups work,** Apple's public app search, no key:

```bash
curl -s "https://itunes.apple.com/search?term=notion&entity=software&country=us&limit=1"
```

On November 12, 2026 that returned Notion with 90,679 ratings, an average of 4.77, free to download, last updated November 10.

## Three sizes, in plain words.

- **TAM, the total market:** everyone with the problem, times what they'd spend on it in a year.
- **SAM, the part you could serve:** the slice your product, language, price and channels can reach.
- **SOM, the part you could win:** what you could realistically get in one to three years.

## Top-down and bottom-up.

**Top-down** starts from a big published figure ("the note-taking software market is $X billion") and takes slices off it. It's quick, and it's where sizing goes wrong. The big figure often comes from a research firm's press release selling a report, its method hidden. Then comes the slice: "if we get just 1%..." Nothing in that sentence says anyone will buy from you.

**Bottom-up** counts buyers. Number of people or businesses you can actually reach, times the price they'd pay, times how often. Each part can be checked, and each part is a question for a real conversation.

**For a small product, bottom-up from real buyers wins,** and the best bottom-up number is people who said yes to a price. Jason Cohen's rule on the shelf is that bar: ten people who say they'll pay. By his own account, 30 people agreed to $50 a month for WP Engine before it had a name: $1,500 a month, tiny, and worth more than any industry forecast because it's real. Sizing for a side product starts there and works outward: if ten said yes from fifty conversations, how many more people like them exist, and how would you reach them?

A made-up example of the shape: a government count says there are 40,000 businesses of the right kind in the US. Perhaps a third use software for this job. If interviews suggest one in twenty of those would switch at $20 a month, that's about 670 customers and about $160,000 a year. Every one of those guesses can be tested; "1% of $4 billion" can't.

Run both and compare. When top-down and bottom-up land ten times apart, the gap is the finding: one of the assumptions is wrong, and the job is to find out which.

## The free sources, and what each can and can't say.

**Company filings.** US public companies file annual reports with the SEC, and EDGAR's free full-text search covers filings since 2001. An annual report gives revenue, often by segment, sometimes customer counts, and describes the competition in its own words. Primary, dated and audited. Its limit: private companies, which is most small rivals, file nothing.

**Government counts.** The cleanest base for bottom-up. The Census Bureau's County Business Patterns counts businesses with employees by industry and county, once a year; its latest data year was 2023 when checked. The Bureau of Labor Statistics counts workers in about 830 occupations; its May 2026 release covers May 2025. A count of real buyers beats a forecast of market value.

**Google Trends, by hand on the website.** It shows interest over time on a scale of 0 to 100, relative to all searches in that place and time, from a sample. It is not search volume. Only popular terms show at all; low-volume terms show as zero, and Google adds noise that's most visible on small terms, so a spike there may mean nothing. Good for "is interest in this rising or falling?" and "which of these two words do people use?" Compare terms in one chart, since each chart is scaled on its own.

**Similarweb's free view.** Estimated monthly visits, visit length, pages per visit and where traffic comes from, for the last few months, with daily lookups limited. Similarweb says that sites with too little traffic show "Not enough data", and that estimates for small sites vary more. Use it to tell a rival with thousands of visits a month from one with millions; never quote it to the nearest thousand.

**App stores.** Apple's free search gives the rating count, average rating, price, category and last update for any app, but no downloads. Google Play's page shows a download band like "100K+", which is a floor, not a count. A rating count is a rough sign of size; any ratio to turn ratings into downloads is a guess, so don't.

**Rivals' own pages.** Pricing pages, changelogs and help docs are primary sources for what a competitor charges and ships. Date every price; the Internet Archive's Wayback Machine shows what a page said before.

## Getting the best out of the skills.

- **Give the skill the bottom-up numbers.** Left alone it will reach for an industry figure. Hand it the buyer count, the price from interviews and the source of each, and ask it to build from those.
- **Ask for ranges, not points.** Its template has a table with single numbers. Ask for a low and a high, with the source and date beside each.
- **Make it label each number** as measured, estimated or a vendor's claim. Its own guidance says to keep estimates and data apart; hold it to that.
- **For competitors, add the complaints.** The skill profiles strengths and weaknesses from websites. Feed it what last30days and review sites say customers hate; that's where the opening usually is.
- **Read the assumptions list first.** The confidence beside each tells you which one to test.

## Where it goes wrong.

- **A forecast treated as fact.** A report seller's projection, quoted as if measured. Strike it, or label it plainly.
- **The 1% slice.** A share of a huge market, with no buyer behind it.
- **Everyone with the problem counted as a buyer.** Many people live with a problem and pay nothing to fix it.
- **Revenue and users mixed.** "2 million users" is not a market worth $X until you know how many pay, and how much.
- **False precision.** $4,237,000 built from rough free numbers. Round, and give a range.
- **Small rivals measured with Similarweb.** "Not enough data" isn't zero traffic; it's no estimate.
- **A stale price.** A rival's pricing from last year. Check the page today.

## Safety.

Everything here is free and reads public data. What leaves the Mac is search terms, so keep day-job names and plans out of them. Opening a Similarweb account, or paying for any data, is Sean's call. Apple's search allows about 20 lookups a minute; keep scripted lookups well under that.

## More details

- Skills: `~/.claude/plugins/synced/<id>/pm-market-research/skills/market-sizing/SKILL.md` and `.../competitor-analysis/SKILL.md`.
- EDGAR full-text search (filings since 2001): https://www.sec.gov/edgar/search/
- County Business Patterns (latest data year 2023): https://www.census.gov/programs-surveys/cbp.html
- Occupational Employment and Wage Statistics (about 830 occupations; May 2025 data released May 15, 2026): https://www.bls.gov/oes/
- How Google Trends scales its data: https://support.google.com/trends/answer/4365533
- Similarweb's free features (vendor article dated June 13, 2024; the daily limit it gives is unclear): https://www.similarweb.com/blog/marketing/marketing-strategy/similarweb-free/ and "Not enough data": https://support.similarweb.com/hc/en-us/articles/207698639-What-does-Not-enough-data-mean
- Apple's search (about 20 calls a minute): https://performance-partners.apple.com/search-api. The rating fields aren't documented there; the lookup above shows them.
- Google Play's download bands: no official explanation found; that the shown figure is a floor comes from third-party write-ups.
- All read November 12, 2026. The WP Engine figures are Jason Cohen's own claim, per `productcraft/research/cohen-ten-who-will-pay.md`.
