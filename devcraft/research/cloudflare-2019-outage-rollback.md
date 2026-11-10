# Cloudflare's write-up of its July 2, 2019 outage: the fix, the undo, and why the undo was slow

## What it is

A public account of how one bad rule took down a large share of the web for 27 minutes. Cloudflare sits in front of millions of websites to speed them up and block attacks. On July 2, 2019, an engineer added a new attack-blocking rule. It contained a pattern-matching formula (a "regular expression") that sent every server's processor to 100% busy. Sites behind Cloudflare stopped loading worldwide.

Written by John Graham-Cumming, then Cloudflare's chief technology officer, and published 10 days later, on July 12, 2019. It's long, about 5,900 words, with a minute-by-minute timeline, a list of everything that went wrong, the fixes promised with dates, and an appendix teaching how such a formula can spiral.

Read it: https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/

**Best part to look at: the "What went wrong" section.** It's an 11-item numbered list. Item 6 is the one for Devcraft: the normal way to undo a rule change meant rebuilding the whole rule set twice, which took too long. So the team used a blunter tool, a single switch that turned off that whole feature everywhere.

## How it turned out

- **Hacker News:** 698 points and 149 comments. That's a top-tier response on the main programmers' forum.
- **A model of a blameless review,** the practice of explaining a failure by its causes rather than by who to blame. It never names the engineer who wrote the rule, and it frames the outage as several causes lining up, most of them process gaps.
- **The promises were checkable.** It lists seven actions with status or due dates. The first (put back a missing safety limit) was already done; the rule audit was already finished.
- **Why it's believable:** the author was a senior executive putting his name to an embarrassing account, and the promised fixes had dates anyone could hold the company to.

## What makes it good, measured

I read the post and counted its parts.

- **Timeline, to the minute (UTC):** change merged 13:31; tests passed 13:37; automatic rollout began 13:42; first alert about 13:45; cause found 14:00; "turn it all off" proposed 14:02 and done 14:07; traffic normal 14:09; the feature switched back on, with the bad rule fixed, at 14:52.
- **Time to undo:** 25 minutes from rollout to the off switch, then 2 minutes to recover. Another 45 minutes of checking before switching the feature back on. They tested in one city first, checking that good traffic passed and attacks were still blocked.
- **The "preview" that wasn't safe.** The rule went out in a simulate mode that logs what it would block without blocking anything. It still crashed everything, because the costly matching ran either way. A dry run must not do the expensive or risky part.
- **Why the undo was slow, four reasons:** the internal sign-in tool was itself down; some engineers' unused credentials had been switched off automatically for security; the emergency bypass route was rarely practised; and the normal undo meant a long double rebuild.
- **Eleven causes, not one.** The list runs from the bad formula through a safety limit removed weeks earlier, tests that never measured processor use, and a rule process that allowed going worldwide in one step.
- **Seven promised fixes,** including a speed check for every rule in the test suite, and moving rule changes to gradual rollouts (a few machines first, then more), keeping the instant worldwide path only for active attacks.
- **Structure:** 9 sections, from the story of the day through how the system works to the fixes, plus the appendix.

### Why it's here

It shows what a real undo plan needs: a fast, rehearsed off switch and a clear check before turning things back on. A thorough undo that takes too long to run doesn't count. Devcraft's first job is a scheduled task that runs unattended overnight. This is the case for a one-line undo that's been tested, plus a preview that changes nothing.

## What Sean said about it

On the shelf Sean saw on November 10, 2026. He didn't single this one out; his pick was uv's design.

## More details

- The post: https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/
- Hacker News thread (698 points): https://news.ycombinator.com/item?id=20421538, read November 10, 2026.
- Cloudflare's short first note on the outage, linked from the post: https://blog.cloudflare.com/cloudflare-outage/
- John Graham-Cumming on Wikipedia: https://en.wikipedia.org/wiki/John_Graham-Cumming
- In the post's terms: the feature was the Web Application Firewall (WAF), the off switch was a "global terminate", and the target was cross-site scripting attacks. The rule set held 3,868 managed rules, all of which were checked by hand afterwards.
- The post doesn't state Graham-Cumming's job title; chief technology officer comes from Wikipedia.
- My measurements: word count from the post's paragraphs (it may include a few lines of page footer); section and list counts read by hand.
