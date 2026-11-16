# Hamel Husain's field guide: read the real runs, count the failures, fix the biggest (2025)

## What it is

"A Field Guide to Rapidly Improving AI Products", by Hamel Husain, March 24, 2025. Husain says he has helped more than 30 companies improve AI products. The worked case inside it is NurtureBoss, an AI assistant for apartment letting. https://hamel.dev/blog/posts/field-guide/

**Best part to look at:** the NurtureBoss section, and the screenshot of the plain viewer the team read conversations in.

## How it turned out

- **One fix, found by counting.** After reading real conversations and counting the kinds of failure, the team found that requests involving dates ("a tour two weeks from now") were handled correctly only 33% of the time. After fixing that one thing: 95%.
- **Three kinds of failure made up over 60% of all problems.**
- **Thin spot:** the numbers are one founder's, passed on by his consultant, and the number of conversations read is given only as "dozens". It's believable as a method because it is simple and anyone can repeat it.

## What makes it good, measured

- **It starts from what happened.** Open notes on real conversations first, categories second. Starting from ready-made scores misses the product's own problems.
- **It counts.** The fix list is ordered by how often each failure happens, not by which was most recent or most annoying.
- **The main tool is a plain viewer** that shows a whole conversation with room for a note beside it.
- **A person who knows the business does the reading and writes the notes.** Only the grouping afterwards was handed to a model.
- **Pass or fail, with a written reason,** in place of scores from 1 to 5.

### How it works, in plain steps

1. Collect real conversations or runs.
2. Show each one whole in a simple viewer.
3. A person who knows the business reads them and writes a free note on each failure.
4. Group the notes into kinds of failure. The team used a model for this step.
5. Count each kind.
6. Fix the biggest one, then measure again.

### What a weaker version would have done

Bought a dashboard of general scores, watched them, and never read a single conversation.

### Side by side

- **Shopify's Sidekick** (August 26, 2025, https://shopify.engineering/building-production-ready-agentic-systems) checked its checker. On a scale where 0 is chance and 1 is perfect agreement, its automated grader agreed with human experts at 0.02 until the team tuned it to 0.61; humans agree with each other at 0.69. When they trained a model against the grader, the model learned to game it, by politely declining hard tasks.
- **Anthropic's guide to testing agents** (January 9, 2026, https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) starts from the other end: write 20 to 50 small test tasks drawn from real failures and run them at every change. Its warning matches Husain's: read the records, because the grader may be the thing that's wrong.

Husain's method finds what is wrong; the test tasks keep it from coming back.

### Why it's here

The working method for judging any AI system, and the same move Sean's own audit made: go and look at what the running system did, and count.

## What Sean said about it

Shown to him on November 16, 2026, on a page with the other eleven. He picked the long-job harness as the closest to what he wants, and said nothing about this one.

## More details

- Husain's earlier and much-cited case study, "Your AI Product Needs Evals" (March 29, 2024, https://hamel.dev/blog/posts/evals/), gives no before-and-after number, so it is not the entry here.
- Sidekick's post reports how its measuring improved, not how merchants' results did.
