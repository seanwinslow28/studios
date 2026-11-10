# Google's "Small CLs" guide: why and how to keep each change small (2019)

## What it is

A short public guide from Google's engineering practices, on keeping each change small enough to review well. "CL" is Google's word for one self-contained change sent for review; most other places say "pull request" or "patch". The guide gives eight reasons small changes are better, a rough size to aim for, and five ways to split a big change into small ones.

Published by Google in September 2019 as part of its public code review guidelines. Max Kanat-Alexander, then a Google engineer and author of the book "Code Simplicity", made early changes to the public copy; most others are marked only as coming from Google. It's licensed for anyone to reuse.

Read it: https://google.github.io/eng-practices/review/developer/small-cls.html

**Best part to look at: the opening list, "Why Write Small CLs?".** Eight bold one-line reasons, each with two or three sentences. The last one, "simpler to roll back", is the one for Devcraft: a small change can be undone cleanly, while undoing a large one can drag other changes with it.

## How it turned out

- **About 23,300 stars and 2,300 copies on GitHub** for the collection it belongs to (a star is a public bookmark; a copy, or "fork", is someone taking their own version to adapt). Very high for a set of written guidelines rather than a tool.
- **It's what teams link to.** When a reviewer asks for a big change to be split up, this page is a common citation, and the fork count shows how many people took a copy to adapt for their own teams.
- **Why it's believable:** it comes from a company with one of the largest codebases in the world, and it's short, specific and free to reuse, which is why it spread.
- **Thin spot:** the page itself had only small Hacker News threads (25 points at most). Its reach is through daily use and links in team handbooks rather than a big launch moment. The "widely adapted" point rests on the fork count, not on a survey.

## What makes it good, measured

I counted these from Google's public copy of the guide.

- **Length:** about 2,000 words, a ten-minute read. Nine main sections and five subsections.
- **Eight reasons, all practical:** reviewed faster, reviewed more carefully, fewer bugs, less wasted work if the idea is rejected, easier to merge with other people's work, easier to design well, less waiting, simpler to undo.
- **A rough size, not a rule:** about 100 lines is usually a reasonable change and about 1,000 is usually too big. It adds that spreading a change across many files makes it bigger too: 200 lines in one file may be fine, but not across 50 files.
- **Five ways to split a change,** each with a short example: stack small changes on top of each other, split by file, split by layer (horizontally), split by feature (vertically), or both.
- **It says when a big change is fine:** deleting whole files, or changes a tool made automatically, where reviewing is quick anyway.
- **Two rules that pair with size.** Keep tidy-up work separate from behaviour changes, so the reviewer can see each clearly. Keep the tests in the same change as the code they test.
- **The reviewer may say no just for size,** and the guide says so plainly. It's easier to write small changes from the start than to split one later.

### Why it's here

It turns "small and easy to undo" from a nice idea into a habit with a rough number attached. Devcraft's first job could easily become one big change. This guide argues for splitting it: one change that fixes the scheduled job, a separate one that adds the safety check, each reviewable and undoable on its own.

## What Sean said about it

On the shelf Sean saw on November 10, 2026. He didn't single this one out; his pick was uv's design.

## More details

- The guide: https://google.github.io/eng-practices/review/developer/small-cls.html
- Its source and history: https://github.com/google/eng-practices (file `review/developer/small-cls.md`; the README explains Google's terms such as CL and LGTM, meaning "looks good to me")
- Companion page on writing change descriptions, about 1,300 words: https://google.github.io/eng-practices/review/developer/cl-descriptions.html
- Largest Hacker News thread for the page: "Send small PRs (Google eng-practices)", 25 points, October 2021, found through the Hacker News search service.
- Star and fork counts read from GitHub's API on November 10, 2026.
- Kanat-Alexander's part comes from the repository's commit history (user `mkanat`, 7 changes); his past role at Google and his book are from his public GitHub profile.
- My measurements: word count with `wc -w` on the source file; sections counted from its headings.
