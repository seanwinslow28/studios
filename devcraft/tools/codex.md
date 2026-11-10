# Codex CLI.

Codex CLI is Devcraft's cold fresh check: a reviewer from a different maker, OpenAI, who never saw the build and reads the change with no stake in it. Read this before asking it to check anything.

## What it's best at.

- **A second pair of eyes that wasn't in the room.** It hasn't seen Claude's reasoning, so it isn't talked into the same mistakes. A different model family also has different blind spots, which is the point.
- **Reading a diff for bugs.** `codex review` reads a branch, a commit or uncommitted work and reports problems, without a chat and without changing files.
- **Scripted checks.** `codex exec` runs one task and exits, with the final answer on standard output and progress on standard error, so a script can save the answer cleanly.

Where another tool beats it:

- **Building.** Claude Code leads and builds; Codex checks. Swapping the two works too, if one is weaker on a job.
- **Facts a command can settle.** Whether the tests pass is a question for `just check`, not for a reviewer's opinion. Whether a package has a known hole is a question for pip-audit.
- **Taste.** It checks truth: does the code do what was claimed, and what breaks. It doesn't decide what Sean likes.

## Setup.

- **What's installed.** Codex CLI 0.163.0 at `~/.local/bin/codex` (OpenAI's standalone installer). The latest stable release is 0.167.0, from November 6, 2026. Paid for through Sean's existing plan.
- **A second copy.** Homebrew also holds an older Codex, 0.162.1. Your shell finds the standalone one first, but a scheduled job runs with a shorter search path and can pick up the other. In anything unattended, call it by its full path.
- **The command that proves it works:**

```bash
codex --version && codex doctor
```

- **Updates** come with `codex update`. Codex moves fast, with alpha builds most days; stay on stable releases, and recheck any flag in this guide with `--help` after an update.
- **Settings** live in `~/.codex/config.toml`. A project can add `.codex/config.toml`, which loads only once the project is trusted. `-c key=value` overrides one setting for one run.

## Getting the best out of it.

**The built-in review.** `codex review` takes exactly one target:

```bash
codex review --base main < /dev/null        # this branch against main
codex review --commit <sha> < /dev/null     # one commit
codex review --uncommitted < /dev/null      # staged, unstaged and new files
```

It can't take a target and custom instructions together. `codex review --base main "check the rollback"` stops with an error (checked on 0.163.0). Custom instructions alone, with no target flag, are allowed. For a saved, scriptable review, use the same command under `exec`, which adds an output file and a no-trace mode:

```bash
codex exec review --base main --ephemeral -o review.md < /dev/null
```

`-o` writes the final message to a file, and `--ephemeral` keeps no session files on disk.

**Give it the diff and the claim, nothing else.** A reviewer handed the builder's story tends to check the story. Hand it the change and one plain sentence of what the change is supposed to do, and ask whether the code does that:

```bash
git diff main...HEAD > change.diff
codex exec --sandbox read-only --ephemeral -o check.md \
  "Claim: every scheduled job now runs on uv's Python 3.14, and each can be put back. \
The diff is on stdin. Say whether the code does what the claim says. \
List each real bug with file and line and how to trigger it. Skip style." < change.diff
```

When a prompt is given and something is piped in, Codex treats the prompt as the instruction and the piped text as context. Leave out the pull request description, the chat, and anything that says why the builder thinks it works. The claim should be one checkable sentence; "improves the jobs" gives it nothing to test.

**Small changes get real reviews.** A reviewer reads a 60-line diff line by line and skims a 2,000-line one. Google's small-changes guide on the shelf makes the case for people; it holds for Codex too. Split a big job into pieces and check each.

**Sandbox and approvals.** The sandbox decides what Codex's own commands can touch: `read-only`, `workspace-write` (edits inside the project folder only), or `danger-full-access`. `codex exec` runs read-only by default. A fresh check never needs more, so say so anyway with `--sandbox read-only` on `exec` or `-c sandbox_mode="read-only"` on `review`, which has no sandbox flag of its own. The approval policy (`-a`, or `approval_policy` in settings) decides when it stops to ask: `on-request` lets it ask; `never` means it never asks and failures go straight back to it.

**Running it in the background.** `codex exec` reads standard input whenever it isn't a terminal. A background job, a launchd job, or a helper that starts Codex may leave input connected to something that never closes, and Codex sits waiting for input that never comes. Always end a background command with `< /dev/null`, or feed it a file as above.

**Reading the output.** For a script, `--json` turns standard output into one JSON event per line; `-o` alone is usually enough. Treat the report as a list of leads to check, not a ruling.

## Where it goes wrong.

- **It reviews the description, not the code.** Given a summary, it agrees with the summary. Give it the diff and the claim only, and ask for file and line for every finding; a finding with no line is a hint that it didn't look.
- **Style nitpicks.** Naming and formatting notes crowd out the one real bug. Tell it to skip style; Ruff already settles formatting.
- **False alarms.** It reports a race that can't happen, or a missing check that's done two files away. Reproduce each finding before acting on it: write the failing test, or run the case. A finding that can't be shown is set aside, with a note of why.
- **Missing what isn't in the diff.** It sees the lines that changed, not the scheduled job that also calls the changed function. When the risk is in a caller, say where to look in the claim.
- **A hung run.** A background Codex with no `< /dev/null` waits forever and looks like a slow review. If a check takes far longer than usual, check its input first.
- **Flags that changed.** A flag that worked last month may be gone or renamed. Check `codex review --help` and `codex exec --help` on the installed version before writing it into a script.
- **The wrong copy.** A scheduled job finds Homebrew's older Codex. Use the full path.

## Safety.

- **What it uploads.** Everything Codex reads goes to OpenAI to be processed: the diff, the prompt, and any file it opens. Never point it at secrets or private material. Keep the diff to the job.
- **What it can change.** In `read-only` it can read the project and run commands that only read; it can't edit. A reviewer stays there. `danger-full-access` and `--dangerously-bypass-approvals-and-sandbox` remove every fence; use them only inside a throwaway machine, never for a review.
- **Keys in scripts.** If a scripted run uses an API key, give it to that one command only, never to the whole environment of a job that also runs project code.
- **What it decides.** Nothing. Its findings go back to the lead, who checks them and fixes what's real. Ask Sean before anything big, costly or hard to undo, whatever Codex suggests.

Sources: [Codex releases](https://github.com/openai/codex/releases), [command reference](https://learn.chatgpt.com/docs/developer-commands?surface=cli), [non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode); flags checked against `codex --help`, `codex review --help` and `codex exec --help` on 0.163.0, November 10, 2026.
