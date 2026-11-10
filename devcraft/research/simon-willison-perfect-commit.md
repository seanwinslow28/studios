# Simon Willison's "perfect commit": change, tests, notes and a link, together (2022)

## What it is

A short blog post setting out what one finished change should contain. Willison's answer is four things in a single saved change: the change itself, the tests that prove it works, the updated user instructions, and a link to a discussion page (an "issue") that holds the background. Squeeze them into one and anyone reading the history later sees the whole picture at once.

Written by Simon Willison on October 29, 2022. He co-created Django, a widely used web framework, and maintains dozens of small open-source tools. He links five of his own changes as examples, so the advice comes with proof.

Read the post: https://simonwillison.net/2022/Oct/29/the-perfect-commit/

**Best part to look at: the example change to sqlite-utils, his database tool,** linked from the post. Open it and scroll: three files, one each for the code, the tests and the instructions. Then open the linked issue to see where the "why" lives.

Example change: https://github.com/simonw/sqlite-utils/commit/ab8d4aad0c42f905640981f6f24bc1e37205ae62

## How it turned out

- **Hacker News:** 197 points and 219 comments the day it went up. A long thread for a post about habits rather than a product.
- **Willison's standing:** his blog is one of the most-read independent programming blogs. Django runs large sites, and his own tools have real users: sqlite-utils has about 2,200 stars on GitHub (a star is a public bookmark).
- **He practises it publicly.** sqlite-utils has 1,204 saved changes since July 2018, and the pattern shows up across them. Anyone can check whether he follows his own advice.
- **Thin spot:** I found no formal adoption, such as a company guide citing it by name. Its reach is through readers and the discussion it sparked.

## What makes it good, measured

I counted these from a copy of the sqlite-utils code and from GitHub's records.

- **The example change, by part:** 10 lines changed in the code, 57 lines changed in the tests, 5 lines added to the instructions. The tests are bigger than the change, by more than five to one.
- **Message length:** one line, 58 characters, ending in "closes #299". That number links to the issue and closes it automatically. The short note works because the issue holds the background.
- **The issue:** opened and closed within 9 minutes on the afternoon of July 24, 2021, California time. He wrote down the need, then did the work. A tiny issue still leaves a findable record.
- **The post's own structure:** eight short sections. The four parts, then three on judgement: an issue beats a long commit note, not every change needs to be perfect, and work rough on a side copy (a "branch"), then fold it into one clean change.
- **The whole tool, for scale:** about 11,250 lines of tool code, 807 test functions across 56 test files, and about 52,800 words of instructions. A small tool, documented like a big one.
- **The opposite choice to Dan Carley's commit,** also on this shelf: that one put 218 words in the commit note itself. Willison keeps the note to a line and puts the story in a linked issue. Both leave a full trail; they just store it in different places.

### Why it's here

It's a simple checklist Devcraft can hold every change to: did the change ship with its tests, its updated instructions and a record of why? For Sean, who'll read the result rather than the code, the docs-in-the-same-change rule matters most. The instructions can never be one change behind the tool.

## What Sean said about it

On the shelf Sean saw on November 10, 2026. He didn't single this one out; his pick was uv's design.

## More details

- Simon Willison, "The Perfect Commit" (October 29, 2022): https://simonwillison.net/2022/Oct/29/the-perfect-commit/
- Example change and issue: https://github.com/simonw/sqlite-utils/commit/ab8d4aad0c42f905640981f6f24bc1e37205ae62 and https://github.com/simonw/sqlite-utils/issues/299
- His other four examples (Datasette, shot-scraper, s3-credentials, datasette-gunicorn) are linked from the post's "Some examples" section.
- sqlite-utils repository: https://github.com/simonw/sqlite-utils
- Hacker News thread, 197 points and 219 comments: https://news.ycombinator.com/item?id=33387855 (read November 10, 2026).
- Willison as Django co-creator: https://en.wikipedia.org/wiki/Simon_Willison
- My measurements: per-file line counts from `git show --stat`; test functions counted as lines starting `def test_` in the tests folder (some run many times with different inputs, so the real number of checks is higher); words in the instructions counted across the docs folder.
