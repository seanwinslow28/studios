# Demand tests and Stripe.

A demand test checks whether people want something before it's built, by watching what they do instead of asking what they think. Three cheap parts: a page the lead builds, a Tally waitlist, and a Stripe payment link when it's time to ask for money. Read this before planning a demand test or taking anyone's money.

## What each part is best at.

- **The page** says who it's for, the problem, what it does and what it costs, with one action to take. The lead writes it as a plain page. Putting it online is publishing, so it needs Sean's yes. Carrd, $19 a year, is the runner-up when a page needs to outlive a test. Link out to the form and the payment link rather than embedding them; plain links work anywhere.
- **The Tally waitlist** measures interest: an email plus a question about intent. See `tally.md`.
- **The Stripe payment link** measures willingness to pay, the strongest signal short of a product. It's a checkout page Stripe hosts, made in Stripe's dashboard without code, shared as a link.

## The ladder of signals.

From weakest to strongest: a compliment, a visit, an email, an answer to an intent question, a click on a price, a payment. Each rung costs the visitor more, so each means more. Buffer's two-page test on the shelf added one rung, a pricing page before the email, and learned about price as well as interest. Jason Cohen's bar on the shelf is the top rung: ten people who'll pay.

Pick the lowest rung that answers the job's question, and write the pass bar before anything goes live: who you're reaching, through which channels, how many visitors, what counts as a pass, and the end date, when the link gets switched off. Bing's headline test on the shelf shows why: a number decided afterwards can be argued into anything.

A middle rung worth knowing is a "fake door": a buy button that leads to "not ready yet, join the waitlist". It counts clicks on a price without taking money. Weaker than a payment, but honest and free.

## Setup.

The Stripe account isn't open yet. Sean has already said yes to opening it, free, when a job first needs to ask for money. Confirm with him when that moment comes; he signs up himself. Taking live payments means Stripe verifies the business and a bank account for payouts; Sean enters those details himself.

**Cost, from Stripe's US pricing page:**

- No setup or monthly fee.
- 2.9% plus 30¢ per successful domestic card payment; 1.5% more for international cards; 1% more when currency conversion is needed.
- Payment links cost nothing extra.
- Issuing a refund is free, but the original fee isn't returned.
- A dispute (a buyer asking their bank to reverse a charge) costs $15.

So a $20 pre-order costs 88¢ in fees. Refund it and the buyer gets $20 back while Sean is out 88¢. Ten refunded pre-orders cost $8.80, a cheap price for real evidence.

**Test before going live.** A Stripe sandbox is a separate test copy of the account where no money moves and card networks aren't involved. The test card for a successful US payment is 4242 4242 4242 4242, with any future date and any three-digit code. The check that proves the setup works: in the sandbox, make the payment link, pay it with the test card, see the confirmation page, then refund it. Only then build the live version. The link's view and sales numbers don't appear in a sandbox.

## Getting the best out of it.

**The page.**

- **Show the price.** A page without one measures curiosity, not demand.
- **Say it plainly:** who it's for, the problem in their words, what it does, the price, one button.
- **Go where the people already are,** and record where each visitor came from. Tally's hidden fields and Stripe's payment links both accept tracking tags in the link. No paid ads until a free waitlist shows interest.

**The payment link.**

- **Name it honestly:** "Pre-order: founding member" with a plain line saying it isn't built yet and when it's expected.
- **Cap the number of payments.** A link can deactivate itself after a set number of sales, with a custom message for anyone who arrives late. A real cap, such as 20 founding places, is honest scarcity.
- **Write the confirmation message.** After paying, Stripe shows a thank-you page you can rewrite, or sends the buyer to your own page. Use it to say what happens next and repeat the refund promise.
- **One custom question at most,** such as a dropdown for what they'd use it for. Stripe allows text, number and dropdown fields, and warns against collecting sensitive information in them.
- **Let people choose the price** when the price is the question. A link can let customers pay what they want, with an optional suggested amount and a minimum and maximum. It can't be a subscription.
- **Read views against sales.** Each link's analytics show views, sales and revenue. They can lag by up to 18 hours, so don't judge a test on its first evening.

## Honesty with people who pay.

Taking money for something not built yet is fine when the buyer knows exactly what they're buying.

- **Say it before they pay.** On the page, in the product description and on the confirmation: not built yet, the expected date, and a full refund any time before it ships.
- **When the test fails or the date slips, refund promptly and unasked.** In the dashboard, Payments, then the menu beside a payment, then Refund payment; full by default, partial if you enter an amount. Several full refunds can go at once. A refund takes about 5 to 10 business days to show on the buyer's statement; one issued soon after the charge may instead appear as the charge simply vanishing.
- **Know the US rule for goods.** The FTC's rule for orders of merchandise by mail, phone or internet says ship within the time you stated, or 30 days if you stated none. If you can't, offer the buyer a choice between waiting and a prompt refund. It covers goods, not services, and its fit for software is unclear. The safe habit is the same either way: state a date, and refund when it's missed unless the buyer chooses to wait. If real money builds up, that's a moment for proper advice.
- **Never** invent scarcity, testimonials or a launch date, and never go quiet on someone who paid.

A refund doesn't erase the evidence. The signal is that they paid.

## Where it goes wrong.

- **Emails counted as payments.** Interest and payment are different rungs. Report each separately.
- **No pass bar set beforehand.** Any result then looks like success. Check the bar is written down before launch.
- **Friends as the audience.** They pay to be kind.
- **A test in live mode by mistake,** so a real card is charged. The dashboard shows which environment you're in; check it before every payment.
- **Disputes from confused buyers,** at $15 each. A clear product name, a plain description and prompt refunds head off most of them.

## Safety.

- **Stripe moves real money.** Confirming the account is wanted now, going live, creating or sharing a live link, and every refund each need Sean's yes.
- **Claude never enters card numbers, bank details or identity information.** Sean does. The 4242 test card is used only in a sandbox.
- **The Stripe connector can move money.** Stripe's official connector can create payment links, prices, customers, invoices, subscriptions and refunds, and its money-movement tools can send funds. Refunds and money transfers ask for a human to approve them in Stripe's dashboard first; most other actions don't. Signing in lets you grant access per environment, live or sandbox, with different permissions for each. Stripe advises turning on the client's own tool-approval setting and taking care when other connectors are active, since text from another tool can try to steer the AI. If it's ever connected: sandbox only at first, live access only when a job needs it, and Sean approves every action. Never paste a Stripe key into chat. From December 2026 the connector accepts only sign-in or Stripe's special agent keys, not full-access secret keys.
- **Buyers' names and emails stay out of this public repo.** They live in the job's folder.

## More details

- Fees, refunds and disputes: https://stripe.com/pricing, read November 12, 2026. Matches `choices.md`'s 2.9% plus 30¢.
- Payment links: https://docs.stripe.com/payment-links, https://docs.stripe.com/payment-links/create (pay-what-you-want, minimum and maximum), https://docs.stripe.com/payment-links/customize (payment limits, custom fields, deactivation message), https://docs.stripe.com/payment-links/post-payment (confirmation page, analytics and their 18-hour lag, refund timing).
- Sandboxes and the test card: https://docs.stripe.com/sandboxes and https://docs.stripe.com/testing
- Refunds, reversals and timing: https://docs.stripe.com/refunds
- Stripe's connector, its tools, which actions need human approval, and the key change: https://docs.stripe.com/mcp
- FTC rule for merchandise orders: https://www.ftc.gov/business-guidance/resources/business-guide-ftcs-mail-internet-or-telephone-order-merchandise-rule. A summary, not legal advice.
- Account verification for live payments is general Stripe practice and wasn't checked against a specific page. No account was opened.
- Shelf: `productcraft/research/buffer-two-page-test.md`, `cohen-ten-who-will-pay.md`, `bing-headline-test.md`.
