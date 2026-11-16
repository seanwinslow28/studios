# Honeycomb's Query Assistant: one prompt, no agent, and an honest scorecard (2023)

## What it is

A box in Honeycomb's product where a customer types a question in plain English and gets a working data query back. Honeycomb sells software that engineers use to see what their systems are doing. Honeycomb built the assistant in about a month, and Phillip Carter wrote two posts about it: how it was designed, and whether it worked.

- The design: "All the Hard Stuff Nobody Talks About when Building Products with LLMs". https://www.honeycomb.io/blog/hard-stuff-nobody-talks-about-llm
- The results: "So We Shipped an AI Product. Did it Work?" https://www.honeycomb.io/blog/we-shipped-ai-product

**Best part to look at:** the results post, where the team lists the goals it missed beside the ones it hit.

## How it turned out

- **Teams that used it kept using the product.** Six weeks on, 26.5% of new teams that had used the assistant were still writing queries by hand, against 4.5% of new teams that hadn't. 33% went on to build a complex query, against 15.7%.
- **It was cheap.** About $30 a month paid to the model provider.
- **The misses are published.** Free-plan teams used it far less than hoped (39%, against 82% on the top plans), one target number barely moved, and new users mostly stopped after about a week. The team believes they had learned to write queries themselves.
- **Thin spot:** every number is Honeycomb's own, and they show that users of the feature did better, not that the feature caused it. It's believable because a marketing team would have cut the misses.

## What makes it good, measured

- **One model call per question.** The team turned down a chain of steps and gave the sum: five steps that are each right 90% of the time are right together only about 59% of the time. The post adds that in practice the drop is less steep, and that speed was its main reason for one call.
- **No chat window, on purpose.** One box, one answer. Less to confuse a user, and less room for someone to talk the model into misbehaving, which people did try.
- **Nothing the model writes can break anything.** Its output is a query the user can see, edit and undo, in a tool they already know. The person is the check.
- **Only what's needed goes in.** Some customers have over 5,000 data fields, so only fields that received data in the past seven days are sent. Each request is small: about 1,800 tokens in and 100 out. (A token is a piece of a word; models are billed by the token.)
- **Daily limits per user** cap both cost and abuse.

### How it works, in plain steps

1. The user types a question in one box.
2. Ordinary code builds one prompt: the rules of the query language, the trimmed list of this customer's fields, a few worked examples, and any query already on screen.
3. One model call returns a draft query.
4. Ordinary code checks the draft and repairs common mistakes.
5. The query runs in the normal query builder, where the user sees it and can change it.

### What a weaker version would have done

Built a chat assistant with several chained steps and access to customer data: slower, less reliable at every added step, and open to being talked into leaking data.

### Side by side

Uber's QueryGPT (September 19, 2024, https://www.uber.com/blog/query-gpt/) solves the same problem with a chain of four model steps and a person in the middle: one step picks the business area, one proposes tables and waits for the user to confirm them, one trims columns, one writes the query. Uber reports about 300 daily users in a limited release, and 78% saying it saved time. Honeycomb kept to one step because its queries are simple and its users wanted speed. Uber accepted a chain because its tables are huge and picking the wrong table is the costly mistake, so it put a person exactly there.

### Why it's here

The clearest worked example of the first question in any design: does this need an agent at all? Here the answer was no, and the result was cheap, safe and measurable.

## What Sean said about it

Shown to him on November 16, 2026, on a page with the other eleven. He picked the long-job harness as the closest to what he wants, and said nothing about this one.

## More details

- Both pages now show only an "updated" date (the design post August 26, 2024; the results post October 2, 2023). The results post refers to a May launch. The original publication dates could not be confirmed.
- Some second-hand summaries give "15% against 36%" for complex queries. The post itself says 33% against 15.7%.
