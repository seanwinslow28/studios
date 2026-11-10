# Dan Carley's one-character fix with a 218-word explanation (2013)

## What it is

A single saved change (a "commit", the unit of change in Git, the tool most programmers use to track edits) to the code behind the UK government's main website. It changed one invisible character. Its attached note is 218 words long and tells how he found it.

Written by Dan Carley at the Government Digital Service on May 1, 2013. It became famous in 2019, when David Thompson, who also worked there, wrote a blog post calling it his favourite commit.

The problem: new automated tests failed with a baffling error, but only when run one way. After an hour he found a file with a space that wasn't a normal space. He swapped it for a plain one, and the tests passed.

Read the commit: https://github.com/alphagov/govuk-puppet/commit/63b36f93bf75a848e2125008aa1e880c5861cf46

Read the post: https://dhwthompson.com/2019/my-favourite-git-commit

**Best part to look at: the middle of the commit note,** where he shows each command he ran and what it printed, ending with the one that pinpointed the bad character by line and column. It's a short detective story you can retrace step by step.

## How it turned out

- **Hacker News front page twice.** Thompson's post drew 714 points and 398 comments in February 2024, and 229 points and 67 comments in March 2020. Hacker News is the main link-sharing forum for programmers; 700-plus points is a big hit.
- **Translated and reposted widely,** including a Russian translation on Habr, a large programming site, and a Korean news summary.
- **It started a real argument, which is useful.** In March 2025, Michael Lynch, a software writer, published "No Longer My Favorite Git Commit". He argued the note buries what the change does under the story, never explains why the file had that character, and mentions code without linking to it. His rewrite puts a one-paragraph summary first and moves the story under an optional "how I found this" heading.
- **Why it's believable:** the praise and the critique both come from named, working developers, and the commit itself is public, so anyone can check.

## What makes it good, measured

I pulled the commit's numbers from GitHub's records.

- **Change versus explanation:** 1 line changed in 1 file (a comment, so the fix couldn't alter behaviour). The note is 38 lines, 218 words, about 1,700 characters. Roughly 200 words of explanation for every word of change.
- **Title:** 41 characters, and it says the cause and the effect ("convert the template to plain ASCII text to fix an error").
- **Structure, in order:** what he was doing; the exact error text; what he ruled out; the command that reproduced it; how he found the one odd file; how he found the character; proof the file was clean afterwards; a one-line human sign-off about losing an hour.
- **Four commands with their output,** so a reader can learn the tools as well as the fix.
- **The exact error text is in the note,** so anyone who hits the same error later can find this fix by searching the project's history. Thompson calls that out as a main strength.
- **What's missing, per Lynch:** no summary up top and no root cause (how the odd space got there in the first place).

### Why it's here

It's the clearest example of a tiny fix whose explanation is the real product. For Devcraft, the lesson is to put the exact symptom, the steps that proved the cause, and the proof of the fix in the change note. Lynch's critique adds the second lesson: lead with one plain sentence on what changed. Read the two together.

## What Sean said about it

On the shelf Sean saw on November 10, 2026. He didn't single this one out; his pick was uv's design.

## More details

- Commit (repository is now archived, read-only): https://github.com/alphagov/govuk-puppet/commit/63b36f93bf75a848e2125008aa1e880c5861cf46
- David Thompson, "My favourite Git commit" (August 30, 2019): https://dhwthompson.com/2019/my-favourite-git-commit
- Hacker News threads, found through the Hacker News search service: 2024 (714 points) https://news.ycombinator.com/item?id=39217149 and 2020 (229 points) https://news.ycombinator.com/item?id=22519632. Counts read November 10, 2026.
- Michael Lynch, "No Longer My Favorite Git Commit" (March 19, 2025): https://mtlynch.io/no-longer-my-favorite-git-commit/
- Habr translation: https://habr.com/ru/post/472278
- The odd character was a non-breaking space (character code A0); I confirmed that from the change itself. On a Mac, Option+Space types one, which makes an accidental keystroke a likely cause. Lynch mentions a Hacker News commenter offering a keyboard explanation, but the commit doesn't say how it got there.
- My measurements: diff and message read from GitHub's commit record; words counted by splitting on spaces.
