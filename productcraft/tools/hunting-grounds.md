# Hunting grounds.

Where the explore-first hunt looks for pain, and how to read each place well. The hunt has four kinds of place, one hunter each: where people complain, where they already pay, bad reviews of paid tools, and pain they don't see yet. Read your part before hunting. The method is on the front-door page; this guide is the places.

## What it's best at.

- **Finding pain from several directions at once.** One deep search finds what one kind of place says. Four hunters on four kinds of place find the pains that show up everywhere, and a pain that shows up as a complaint, a paid job post and a bad review is far stronger than any one of them.
- **Getting past what a normal research pass sees.** A web search lands on articles and vendor pages. These places hold people describing their own week: the review they wrote after cancelling, the $40 they offered a stranger to fix a sheet, the routine they don't know is strange.
- **Spotting who pays.** Job posts and paid templates show money already changing hands, which is the closest the hunt gets to the ten who'd buy.

Where something else beats it: once Sean has picked a pain, checking how big it is and who sells against it is step 2's work, with the two researchers (`research-with-sources.md`, `codex-research.md`) and `market-sizing.md`.

## Setup.

Nothing to buy. Each place is read one of three ways, and which one works was checked on November 13, 2026:

- **A plain read** from the Mac (a fetch or a short script): the Apple App Store's review feed, Google Play's app pages, the Shopify app store's review pages, the Stack Exchange question search, the US Federal Register's search, Hacker News search, the Reddit archive `last30days` falls back on, the Etsy community forums, the BiggerPockets forums, forums built on Discourse (many software tools run one), and Wellfound's job listings.
- **Sean's Chrome,** through the browser extension, for sites that refuse plain reads: G2's software reviews and Upwork's job search both read cleanly there. Capterra, Trustpilot, Fiverr, Indie Hackers, Quora, Medium and Indeed refuse plain reads and haven't been tried in Chrome yet; try them there and note what works.
- **`last30days`** for Reddit, X, YouTube, TikTok and Hacker News together. Its own guide (`last30days.md`) covers setup, wording and its free-call limit.

Reddit's own site refuses reads from here, so Reddit comes through `last30days` and its archive, never directly.

The one check that the plain reads still work: fetch the Apple review feed for any app (`https://itunes.apple.com/us/rss/customerreviews/id=<app id>/sortBy=mostRecent/json`) and see reviews come back.

## Getting the best out of it.

**Where people complain.** Run `last30days` in the words people post in, about the pain rather than any product ("landlords chasing late rent", not "rent collection app"). Then go where the group talks shop, which is rarely Reddit alone: landlords on BiggerPockets, sellers on the Etsy forums, tool users on that tool's own forum, technical people on Stack Exchange. A trade forum's top threads of the year are often a ready-made list of what hurts. Read the replies: the top reply often says the pain is already solved.

**Where they already pay.** Search freelance job posts for the chore, not the solution: "clean up spreadsheet", "organize Google Drive", "reconcile orders". Every post is someone who tried, gave up and offered money; the budget is a price they already accept. Count how many different posters ask for the same thing in a month, and skip agencies reposting jobs. Paid templates and planners on Etsy show the same thing from the seller's side: a template with thousands of sales is a pain people pay to have tidied.

**Bad reviews of paid tools.** Read the newest one- to three-star reviews of the tools the group already uses. Two- and three-star reviews are the gold: the reviewer still uses the tool and says exactly what's missing ("the only thing I wish it did..."). One-star reviews spike after a price change or an outage, so check the date before calling a pain lasting. G2 marks each review's source; some reviews are gathered with rewards, so weigh "Organic" ones more. For phone apps, Apple's feed returns the most recent reviews with their stars; for shop owners, the Shopify app store's reviews are a direct line to small sellers.

**Pain they don't see yet.** Three ways in:

- **Routines described as normal.** Search for people sharing their system: "my workflow", "here's how I track", "every week I". Someone proudly describing a 40-step Monday routine is in pain they've stopped noticing.
- **Job ads for repeat work.** A small company hiring someone mainly to copy, check or chase is paying a salary for a chore. Wellfound's listings read plainly; bigger job boards need Chrome.
- **Changes coming.** New rules with a start date (the Federal Register's search lists US rules and their comment periods), price jumps and tools announced as shutting down. The people it will hit often haven't heard yet. Date every change and say who it hits.

**For every hunter.** Hand back pains, not ideas. Keep each quote word for word with its link and date. Count distinct people, not posts or upvotes. Name every place you couldn't read.

## Where it goes wrong.

- **The planted question.** Many "what tool do you wish existed?" threads are posted by people hunting for something to build, and their replies are pitches. Lean on first-hand stories with a number or a name.
- **A pain tied to one company.** A price jump or an outage at one vendor makes loud, real pain that may fade when the vendor backs down. Say so beside the pain.
- **Loud mistaken for many.** One viral thread is one person many people saw. A pain needs several people, on several sites, ideally in several kinds of place.
- **A blocked page read as silence.** A site that refused, timed out or showed a bot check wasn't heard. Write it down as not heard.
- **Old pain.** A review from two years ago about a bug long fixed. Check dates and later replies.

## Safety.

The hunt only reads. In Chrome: never sign in, apply, message, follow, buy or click anything that acts; read the page and close the tab when done. Sean's sign-ins are his, and a place behind one, such as a group he belongs to, is read only with his yes for that place. If a site shows a bot check, stop there and note it as not heard; never get past it. Keep day-job specifics out of every search, since search words leave the Mac. Quotes stay in the job's folder, and real people's names stay out of anything published.

## More details

- Checked November 13, 2026, with a plain read and Claude's page fetch, then Sean's Chrome for the ones refused. Plain reads worked for every place listed under Setup. G2 and Upwork refused both plain reads and Claude's fetch, and read cleanly in Chrome. Product Hunt worked through Claude's fetch. Reddit's own site refused; its archive worked. Google Trends refused a plain read.
- Apple's review feed returns up to 50 recent reviews per page for one country; change `us` in the address for another.
