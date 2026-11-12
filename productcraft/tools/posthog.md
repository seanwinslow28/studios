# PostHog.

PostHog is product analytics: it records what people do inside a live product (pages seen, buttons pressed, signups finished) and turns that into funnels, retention curves and tests. It is for a side product that real people are already using. No account gets opened until one is live. Read this when a product is about to launch, or when a question can only be answered by watching real use.

## What it's best at.

- **One free tool for the whole loop.** Analytics, funnels, retention, feature flags (switches that turn a feature on for some users and off for others), A/B tests, short surveys and session recordings, all in one place.
- **A generous free plan.** The first million events a month are free, which a small side product is unlikely to use up.
- **Privacy controls that work.** A cookieless mode, settings to drop IP addresses, and a hook to strip data before it leaves the browser.

Where another tool beats it: before launch, there is nothing to measure. Demand tests use a page, a Tally waitlist and a Stripe link (`demand-tests-and-stripe.md`). For a plain "how many visitors" count on a marketing page, Plausible is simpler, at $9 a month. For one-off exports, Sheets and Python do the analysis (`sheets-and-python.md`).

## Setup.

**Not yet.** Sean said yes to PostHog only once something is live. When that day comes, the lead asks Sean before opening the account; he signs up himself.

What the free plan includes, read from PostHog's pricing page on November 12, 2026:

- 1,000,000 analytics events a month.
- 1,000,000 feature flag requests a month, shared with experiments.
- 5,000 web session recordings and 1,500 survey responses a month.
- One project, one year of data kept, no credit card needed.

The pricing page doesn't say what happens when a free account goes over its allowance. Check before relying on it. Past the free million, the paid plan charges $0.00005 an event for the next million, so a second million costs about $50.

The check that proves it works, once installed: open the product in a browser, click through it, and watch the events appear in PostHog's live activity view within a minute.

## What to track first.

Tracking everything because it's free is the mistake. Autocapture records every click by default, and unnamed clicks answer no question. Start from the two or three questions the product has to answer, and name a handful of events that answer them.

For a typical side product:

- **Visited** the landing page.
- **Signed up.**
- **Did the core thing once:** the first invoice sent, the first habit logged, the first file converted.
- **Came back** and did it again within a week.
- **Paid.**

That's five events, and each one maps to a question: do people arrive, do they try it, do they get value, do they stay, will they pay. Name events in plain words, past tense, one style throughout ("signed up", "invoice sent"), and never rename one later, because history splits at the rename.

Netflix's proxy numbers on the shelf show the next step: pick one early action that predicts staying, in the shape "share of new users who do X within Y days". Netflix used watching at least 15 minutes in the first month. For a side product it might be "share of signups who send a first invoice within 3 days". That one number is worth more than any dashboard.

## Getting the best out of it.

**Funnels.** A funnel is the chain of steps from visit to payment, and the share of people who make it through each step. Build one from the five events and the biggest drop is usually the first thing worth fixing. Funnels need enough people to read: with 30 visitors, a step that lost 4 people tells you little. Look at the people, not the percentages, at that size.

**Retention.** A retention chart shows, of the people who signed up in a given week, how many came back in each later week. The shape matters more than any single number: a curve that flattens means some people found lasting value; a curve that slides to zero means nobody did, however good the signups look. Measure retention on the core action, not on logging in.

**Feature flags.** Ship a change to a few users first, or only to Sean, and switch it off without a redeploy if it breaks. For a side product the everyday use is safety, not testing.

**Experiments.** PostHog runs A/B tests on top of feature flags, and its results give the chance that one version beats the other. Its own minimums are low (50 people per version, and 5 conversions per version for funnel goals). Those are data-quality floors, not enough people for a confident call. Decide the main number and the sample size before launch, and don't stop the moment it looks good. Most side products lack the traffic for a meaningful test; talking to ten users often teaches more. The Bing headline story on the shelf is the reminder: a surprising win gets checked for a bug before anyone celebrates.

**Surveys.** PostHog can show a short in-product survey. Superhuman's survey on the shelf, which asks how disappointed people would be to lose the product, fits here once enough people use it.

## Privacy.

Treat every event as something that will sit on someone else's server for a year.

- **No personal data in events.** No emails, names, phone numbers or free text people typed. PostHog's own guidance warns against setting an email as a person property without consent. Use an anonymous ID; keep the link to a real person, if any, in the product's own database.
- **Strip what slips through.** The browser library's `before_send` hook can remove or blank fields, such as a URL that carries an email in it, before an event leaves the page.
- **Cookieless mode.** Setting `cookieless_mode: 'always'` stores nothing in the browser; PostHog counts visitors with a hash of the IP address, browser details, the site and a salt that changes daily, then deletes the salt. The trade-off: the same person counts as new each day, so weekly and monthly visitor counts run high, and per-person features like identifying users don't fit. The setting `'on_reject'` uses cookies only for people who accept them. Either way, the project setting for cookieless tracking must also be switched on, or those events are ignored.
- **Drop IP addresses.** A project setting discards IPs. Location is still worked out from the IP first, unless that step is switched off too.
- **Mask recordings.** If session recording is on at all, mask every input and every bit of text by default. Recordings of real people are the most sensitive thing PostHog holds; leave them off unless a question needs them.
- **Choose the region.** PostHog offers a US and an EU cloud; pick the one that fits where the users are.

Whether a product needs a cookie banner or a privacy policy depends on where its users live and what it collects. That's a question to raise with Sean, not something to settle in code.

## Where it goes wrong.

- **Tracking everything, answering nothing.** Autocapture on, no named events, no questions. Start from the questions.
- **Vanity numbers.** Pageviews and total signups only go up. Retention on the core action and paying users tell the truth.
- **Reading noise.** Small numbers swing wildly week to week. Wait for enough people, and show counts beside percentages.
- **Events renamed midstream,** which breaks every chart that spans the change.
- **Own visits counted.** Sean testing his own product inflates every early number. Filter out his account and test data from day one.
- **Personal data in properties,** usually by accident through a URL or a form field. Check the first week's raw events by eye.
- **Opening the account early.** A PostHog project with nothing live is a dashboard of zeros and a reason to fiddle instead of shipping.

## Safety.

PostHog sends usage data about the product's users to PostHog's servers, which is the point of it, so what's collected is a privacy choice. Ask Sean before opening the account, before turning on session recording, and before the free allowance is close to running out. No spending without his yes. Day-job products never go into Sean's personal PostHog.

## More details

- Free allowances, one project, one-year retention, no card, and paid per-event price: https://posthog.com/pricing.md, read November 12, 2026. The page doesn't say what happens to a free account that exceeds its allowance; unverified.
- Experiment statistics and the 50-exposure and 5-conversion minimums: https://posthog.com/docs/experiments/statistics
- `cookieless_mode`, `person_profiles`, `autocapture`, `capture_pageview`, `mask_all_text`, `disable_session_recording`: https://posthog.com/docs/libraries/js/config
- Cookieless hash inputs and daily salt: https://posthog.com/docs/privacy/cookieless-tracking (summarised via search; the page itself didn't load in full here).
- Personal data, `before_send`, IP discard and GeoIP: https://posthog.com/docs/privacy/data-collection
- Browser storage options: https://posthog.com/docs/libraries/js/persistence
- Plausible's price is from `productcraft/tools/choices.md`.
- Shelf examples: `productcraft/research/netflix-proxy-metrics.md`, `productcraft/research/bing-headline-test.md`, `productcraft/research/superhuman-fit-engine.md`.
