# A coding agent's memory that checks itself before use (2026)

## What it is

GitHub Copilot Memory: the coding agent and code review save facts about a repository as they work, and later sessions use them. Written up by GitHub's engineering team on January 15, 2026, updated since. https://github.blog/ai-and-ml/github-copilot/building-an-agentic-memory-system-for-github-copilot/ and the documentation at https://docs.github.com/en/copilot/concepts/agents/copilot-memory

**Best part to look at:** the design of each memory (a fact, its evidence, a reason) and the A/B results.

## How it turned out

- **The maker's own test, in production:** code changes from the coding agent were accepted (merged) 90% of the time with memory, against 83% without. Positive feedback on code review rose from 75% to 77%.
- **What they counted** was work accepted, not memories loaded.
- **What broke:** the documentation says facts from closed, never-merged changes can slip past the check. The write-up reports no production failures.
- **Thin spot:** only GitHub's own numbers, and the stored reason is the agent's, not a person's words.

## What makes it good, measured

- **Each memory carries its evidence.** A memory names the code it came from.
- **Checked when used, not trusted.** Before using a memory, the agent checks it against the current code. If the code disagrees, it saves a corrected one. A memory that checks out is saved again, which keeps it fresh.
- **Old memories expire.** After 90 days without being confirmed, a memory lapses. Being read doesn't reset the clock.
- **People can vote and fix.** Useful memories can be upvoted, wrong ones corrected.

### How it works, in plain steps

1. The agent works and notices a fact worth keeping.
2. It saves the fact with the code it came from and a reason.
3. A later session starts with the repository's recent memories.
4. Before relying on one, it checks the cited code.
5. It uses, corrects or re-saves the memory.

### What a weaker version would have done

Load every saved note at the start and trust it. Stale facts would steer the work, which is the failure memory benchmarks find hardest to avoid.

### Side by side

The Remembrance Agent (`remembrance-agent.md`) shows a person their own past files while they write, and found that on-topic isn't the same as useful.

## What Sean said about it

He hasn't seen it on its own. It shaped two of the six things he agreed a good version of his past-reasons design does, on November 16, 2026: his exact words with where they came from; and counted by whether he used it. His words on the six: "Yes, hold to these."

## More details

- Two researchers found it independently on November 16, 2026, and agreed on its numbers from the same page.
