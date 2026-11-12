# Reading numbers and tests honestly.

Read this whenever a job leans on a number: choosing what to measure, reading a test, estimating something nobody has counted, or judging whether a small product is working. Honest reading means three things: measure what predicts the outcome you care about, distrust results that flatter you, and say how sure you are, above all when the sample is small.

## Metrics that predict what matters.

The number that matters most is usually slow. By the time yearly retention moves, the quarter is over and nobody can say which change did it. So good teams steer by faster numbers that predict the slow one.

- **A proxy metric** is a number a team can move in weeks that reliably predicts the slow outcome. Netflix under Gibson Biddle used "share of new members who do at least X within Y time": watched 15 minutes of streaming in their first month, or rated 50 films in their first two months.
- **Input metrics** are the handful of things a team works on directly, each feeding the guiding number.
- **One guiding metric,** often called a North Star metric, captures the value customers get and leads revenue rather than reporting it. John Cutler's test, from Amplitude's playbook: a team shouldn't be able to push it directly. If it can, it's really an input.

What makes a metric good:

- **It names who, how much and by when.** "Engaged users" means nothing. "New members who watched at least 15 minutes in their first 30 days" can be checked and argued with.
- **It's about value, not activity.** Sign-ups, page views and downloads rise for reasons unrelated to anyone being helped. These are vanity metrics.
- **It's hard to game.** Biddle's customer service team improved its number by hiding the phone number; the fix was to count it only when the number was easy to find. Any target gets pushed in its cheapest direction, so find that direction first.
- **Its link to the outcome is tested.** Netflix saw correlation first and proved cause later with a test. Until then a proxy is a guess.
- **It would stall if product work stopped.** If it would climb anyway, it's measuring the market.

## A/B tests that can be trusted.

An A/B test shows two versions to two random groups and compares them. Random assignment is what lets you say the change caused the difference. Ronny Kohavi, Diane Tang and Ya Xu's *Trustworthy Online Controlled Experiments* is the standard text. Four ideas do most of the work.

**Work out the sample size first.** Small effects need huge samples. A common rule of thumb for 80% power (the chance of catching a real effect of the size you care about) is about 16 times the variance divided by the square of the smallest effect worth finding, per group. On a 5% sign-up rate, catching a lift to 5.5% needs about 30,000 visitors in each group; catching a jump to 10% needs about 450 (the rule of thumb says 300, but it runs low for big jumps; `productcraft/tools/sheets-and-python.md` has the full calculation). So a small product can only test big changes. Test the bold version, not the button colour.

**Don't peek and stop when it looks good.** Checking often and stopping the first time the result crosses the line inflates false wins. Evan Miller's 2010 simulation of a change that did nothing found about a 26% false-win rate under constant peeking, against the 5% people think they're running. Fix the length in advance, at least a full week so weekdays and weekends both count, and read it once.

**Too good to be true usually is.** Bing's ad headline test set off an alert because revenue was too high, and the team hunted for a bug before believing a 12% rise. Kohavi's paper "A/B Testing Intuition Busters" picks apart a published test claiming a 337% lift from 82 and 75 visitors: at that size the test had about a 3% chance of detecting a realistic effect, so the "win" was far likelier luck than truth. A surprising result earns a rerun, not a launch.

**Guardrails.** Name in advance the numbers that must not get worse: speed, complaints, cancellations, revenue. A main-number win that hurts a guardrail isn't a win. Also check the groups came out the size you asked for; a lopsided split on a big sample means something is broken.

Expect most ideas to fail. Kohavi reports only about a third of tested ideas at Microsoft improved the number they aimed at. That's the case for testing at all.

## Measuring the seemingly unmeasurable.

Douglas Hubbard's *How to Measure Anything* widens what "measure" means: any observation that reduces uncertainty counts. You need enough to make the decision, not a precise number.

- **Give a range, not a point.** "Between 200 and 2,000 people would pay, and I'm 90% sure" beats "about 800". Most people's first 90% ranges are too narrow; practice on questions with known answers fixes that.
- **Measure only what could change the decision.** If every likely answer leads to the same choice, skip it. Teams often measure what's easy and ignore the one unknown that decides things.
- **A little data goes far when you know little.** Hubbard's rule of five: take five random samples from any group, and there's a 93.75% chance the group's middle value lies between the smallest and largest of them.
- **Break a big unknown into smaller ones** (how many have the problem, find you, pay) and combine the ranges.

## SaaS basics for small products.

SaaS means software sold by subscription. David Skok's writing is the clearest free source.

- **Retention:** the share still paying after a set time. Track it by cohort, the group who joined in the same month, so new sign-ups don't hide old ones leaving.
- **Churn:** the share who leave in a period. Customer churn and revenue churn can disagree: ten small accounts leaving may barely dent revenue, one big one can halve it. Report both.
- **Unit economics:** whether a customer is worth more than they cost to win. Lifetime value (roughly monthly margin divided by monthly churn) is set against acquisition cost. Skok's older guide was lifetime value above three times that cost, earned back within 12 months; he later loosened the payback figure. Treat both as rough, and say which lifetime-value formula you used, because the versions differ a lot.
- **Small churn compounds.** Losing 2% of revenue a month is about 22% a year.

## Small-sample honesty.

With ten customers, every number is loud. One cancellation is 10% churn. Three yeses out of ten reads as 30%, but the honest range runs from about 11% to 60%.

- **Show counts beside percentages.** "3 of 10" tells the reader how much weight it can bear.
- **Zero isn't zero.** No cancellations among ten customers still allows a high true rate; the exact 95% upper limit for none out of ten is about 26%. (The usual shortcut, three divided by the sample size, gives 30% and is rough below about 30 customers.)

At this size, behaviour beats statistics: ten interviews and ten real payments say more than a dashboard. Jason Cohen's bar of ten people who say they'll pay is a count, not a rate, which is why it works. Superhuman's score grows the idea up: the share of regular users who'd be very disappointed to lose the product, against a 40% bar set before measuring. With about 40 answers, its climb from 22% to 58% is well outside the noise; 38% to 42% wouldn't be.

## Where it goes wrong.

- **A vanity metric as the goal.** Fix: tie it to value with who, how much and by when.
- **A proxy nobody tested.** Fix: check it predicts the slow outcome before steering by it.
- **A test too small to see anything.** Fix: work out the sample first; if it's out of reach, test a bolder change or don't test.
- **Peeking.** Fix: set the length in advance and read it once.
- **Cheering a huge result.** Fix: hunt for the bug, then rerun.
- **One exact number with no range.** Fix: give the range and how sure you are.

## Examples.

- **Netflix's proxy metrics** (`productcraft/research/netflix-proxy-metrics.md`): fast numbers in one shape, a gamed metric caught, and cause proven by a later test.
- **Bing's ad headline test** (`productcraft/research/bing-headline-test.md`): guardrails, suspicion of good news, and repetition before trust.
- **Superhuman's fit engine** (`productcraft/research/superhuman-fit-engine.md`): a fuzzy question turned into one score, with the bar set in advance.

## What a strong product leader would notice.

- Whether the metric names who, how much and by when.
- Whether the team could push or game the guiding number directly.
- Whether the sample size was worked out before the test began.
- A big, surprising result nobody has tried to break.
- Which guardrails were set, and whether they held.
- A percentage on a tiny sample with no count beside it.
- A single exact estimate where a range belonged.

## More details

- Biddle on proxy metrics: https://askgib.substack.com/p/how-do-you-establish-product-metrics
- Amplitude's North Star playbook: https://amplitude.com/north-star
- Kohavi, Tang and Xu, *Trustworthy Online Controlled Experiments* (2020): sample-size rule of thumb, one week minimum, guardrails, split checks. Read through private book notes.
- Kohavi, Deng and Vermeer, "A/B Testing Intuition Busters" (KDD 2022): https://exp-platform.com/abtestingintuitionbusters/ . The 3% power figure is the paper's.
- Evan Miller, "How Not To Run an A/B Test" (April 18, 2010): https://www.evanmiller.org/how-not-to-run-an-ab-test.html . 26.1% is his worst case.
- Bing: https://hbr.org/2017/09/the-surprising-power-of-online-experiments
- Hubbard, *How to Measure Anything*: ranges, value of information, the rule of five (one minus two halves to the fifth power).
- Skok: https://www.forentrepreneurs.com/saas-metrics-2/ and https://www.forentrepreneurs.com/why-churn-is-critical-in-saas/
- Computed for this brief: sample sizes (30,400 and 304 per group), the 3-of-10 range (Wilson 95% interval, 10.8% to 60.3%). The zero-events shortcut is the "rule of three".
- Notes live in `productcraft/library/`, which git ignores.
