# An agent that brings your own files back while you write (2000)

## What it is

"Just-in-time information retrieval agents", by Bradley Rhodes and Pattie Maes of the MIT Media Lab, in the IBM Systems Journal, 2000. It tested the Remembrance Agent, which watches what you type and quietly shows a few of your own past documents that match, and Margin Notes, which annotates web pages the same way. https://www.bradleyrhodes.com/Papers/rhodes-jitir-agents-ibmsj-2000.pdf

**Best part to look at:** the usefulness results, where on-topic suggestions turn out to be already known.

## How it turned out

- **People preferred it.** 13 people writing essays had the agent, a search box and Margin Notes; 78.5% ranked the agent first (14 others had search only).
- **It surfaced things search didn't.** The agent group viewed about three times as many articles as the search-only group, and about two and a half times as many through the agent as through search. Search use didn't drop.
- **On topic isn't useful.** On another test, suggestions averaged only 2.7 out of 5 for usefulness. Every suggestion rated on topic but useless was turned down because the person already knew it, and 68% of those were things the person had written. That slice was small: about 4% of all suggestions.
- **Known can still help.** Some people rated a known suggestion useful as "a good reminder".
- **Margin Notes did poorly:** fewer than a third looked at any of its suggestions, because they appeared when nobody was looking.
- **It settled.** With one fixed window on what you'd typed, it kept showing the same suggestions.
- **Thin spot:** small groups and a 2000 setting. Believable for its honest reporting of where it didn't help.

## What makes it good, measured

- **A few suggestions, precision first.** The paper argues for showing only a few and filtering hard, because a wrong suggestion costs attention.
- **Relevance is necessary, not enough.** The useful ones were relevant and new to the person, or a timely reminder.
- **Timing matters.** Suggestions shown when the person isn't looking go unused.

### How it works, in plain steps

1. The person writes.
2. The agent compares the last words written with the person's own files.
3. It shows a few of the closest, briefly, at the edge of the screen.
4. The person opens one or ignores them.

### What a weaker version would have done

A search box the person has to think to use. They viewed far fewer of their own documents that way.

### Side by side

GitHub's Copilot memory (`github-copilot-memory.md`) brings back what it learned, checks it before use, and counts the work that got accepted, not the memories shown.

## What Sean said about it

He hasn't seen it on its own. It shaped two of the six things he agreed a good version of his past-reasons design does, on November 16, 2026: a few right ones, never a pile; and useful, not just on topic. His words on the six: "Yes, hold to these."

## More details

- Read in full and every number checked by the lead on November 16, 2026, for Systemcraft's first job. A second researcher found it independently.
