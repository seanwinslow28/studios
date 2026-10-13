# The wall

The machine layer of Devcraft's never-do list ([`devcraft/CLAUDE.md`](../CLAUDE.md), rule 9): the sandbox and permission settings every seat pass runs under, the guard hook on top of them, and the git hooks on every build worktree. Built on the Devcraft build map's **Build the never-do hooks and sandbox config** ticket (2026-10-11), from the never-do ticket's wall column and that day's probes of both vendors.

The order of trust is fixed. **The OS sandbox is the wall**; the permission deny rules sit beside it; **the guard only adds sight** the first two lack (which seat is running, a path after `~` and links are resolved, a wrapped `sh -c`, a plan-named exception). A hook fails open on a timeout or a mistyped path, so nothing here relies on the guard alone, and every seat contract still states every item. The after-check is [the diff check](../diffcheck/README.md), which the pre-push hook runs.

| File | What it is |
|---|---|
| [`policy.py`](policy.py) | The rules as data: seats and their write zones, controls, credentials, records, snapshot flags, the machine-local lists. One copy, read by everything below and by [the diff check](../diffcheck/README.md) |
| [`guard.py`](guard.py) | The PreToolUse hook, one script for both vendors. Exit 2 with a reason refuses; every decision is appended to the pass's guard log |
| [`shellparse.py`](shellparse.py) | Splits a command line into the simple commands the guard judges: `sh -c`, `$(…)`, `env`, `cd`, redirects, heredocs |
| [`gitcheck.py`](gitcheck.py), [`git/`](git/) | pre-commit, commit-msg and pre-push for a build worktree |
| [`seat.py`](seat.py) | The coordinator's tool: writes a pass's seat context, its Claude settings or Codex pass profile, the Codex seat home, a worktree's git hooks; launches a pass under its caps; freezes a diff; runs the model check and the preflight |
| [`tests/`](tests/) | The seeded cases (must refuse, must pass) beside the hooks, the Codex sandbox matrix, and `live.py` |

## How a pass is walled

1. **Open** installs the worktree's git hooks: `seat.py worktree <worktree> --engagement <eng>`. It sets `core.hooksPath` for that worktree only (`extensions.worktreeConfig`), so Sean's own checkout never runs them.
2. **Before each pass** the coordinator writes the seat context, copying every plan-named exception from the plan gate's frozen "Exceptions on the record" table and nowhere else: `seat.py context --seat <seat> --worktree <wt> --engagement <eng> --pass NN --branch <branch> [--test-path P] [--ops-path P] [--grant-read F] [--grant-control F] [--host H] [--cap-minutes N] [--cap-tool-calls N] [--cap-budget-usd N] [--effort xhigh --escalation <record>]`. It lands in `<eng>/trace/logs/pass-NN.context.json`, written once, with the pass's caps: the seat's defaults (the Builder 60 minutes and 200 tool calls, the Codex gates 20 and 80, the Claude seats and the security pass 30 minutes and $15) unless the Open changed them with a stated reason. It holds no employer paths. A Codex pass runs at effort `high`; **the Builder's escalated repair** takes the one step above it, `--effort xhigh`, only with `--escalation` naming the record that calls it: the gate findings whose FAIL sent the redraft up (`audits/<gate>[-rN].md`, its verdict a FAIL), or the ledger entry (`dNN-<slug>.md`) that names `xhigh` for another trigger. Any other effort (never `ultra` or `max`), a gate, a Claude seat or a record outside the engagement folder stops at `context`; the record's hash goes in the context, `launch` refuses if it has changed since, and the launch record carries the effort and the record (SWCB #135).
3. **The wall files** hold the machine's employer paths, so they are written once to `~/.config/devcraft/passes/<engagement>/` (`$DEVCRAFT_PASSES` for tests), outside every repo; the pass record keeps their path and hash, never their content. **Claude seat or the security pass:** `seat.py claude-settings <context>` writes `pass-NN.settings.json`: sandbox on and failing closed, no escape hatch, network limited to the plan's hosts, `denyRead` and `Read` denies for credentials, employer paths and (for all but the Verifier) `held-out/`, `Edit` denies for controls, records, the shared references and everything outside the seat's zone as the worktree stands, git writes only to the build branch's own refs, and the guard on `PreToolUse` and `SessionStart`. The security pass is a gate on Opus 5.5, so it runs read-only: the worktree is in its `Edit` denies and it gets no write tools. **Codex seat or gate:** `seat.py codex-pass <context>` writes `pass-NN.codex-layer.toml` and links the seat home's `<eng>-pass-NN.config.toml` to it, since Codex reads a profile only from its home: the Builder's extends `:workspace` with test paths, Release's ops paths and every control (present or not) read-only, a test or ops path meaning every match of a floor pattern at any depth as the worktree stands when the layer is written, plus each glob-free pattern's top-level path even when absent (a match created later elsewhere, such as a new nested `tests/`, is the guard's, the commit hook's and the diff check's); a gate's extends `:read-only`; both deny credentials, employer paths and `held-out/`, keep the engagement folder read-only and the network off, and mark the worktree untrusted so a repo's own `.codex/` config never loads.
4. **Launch** with `seat.py launch <context> --prompt-file <f> [--output artifacts/<file>] --run`: a scrubbed environment (no tokens, stdin closed), `--setting-sources ""` for Claude, `-p <profile>` and no `--sandbox` for Codex. The forms are in [the bench README](../bench/README.md#launch-forms). A Codex pass, and a read-only Claude pass, names its artifact with `--output` (in `artifacts/` or `audits/`, written once): Codex writes its final message there with `-o`, and the launcher files a read-only Claude pass's final answer there. The launcher watches the live log (`trace/logs/pass-NN.jsonl`, stderr beside it) and **kills the pass's whole process group at 100% of a cap** (wall clock, or tool calls counted from the log), because Codex has no budget, turn or time flag and macOS has no `timeout`; Claude stops itself at `--max-budget-usd`. Either stop is filed `Blocked: budget` with what the pass left on disk (exit 2). After a Codex pass it saves the session files as `pass-NN.rollouts/` and reads them as rung-0 line 11 does: a pass that started a helper agent has its output moved aside to `pass-NN.discarded.md` and exits 3, to be re-run once as a new pass (a second spawn stops Blocked, #123). Everything the record's completion fields need lands in `pass-NN.launch.json`: times, tool calls, the stop, the wall file's path and hash, the output's hash, the raw usage and its meter source, the session stamps.
5. **The frozen diff.** After a pass that touched the target repo, `seat.py freeze-diff <context> --base <base> [--point HEAD]` saves `git diff <base>..<point>` (binary-safe, no personal git settings) as `<eng>/artifacts/pass-NN.diff.patch`, written once, and prints its hash and both commits for the pass record. The patch outlives the worktree.

`seat.py probe` is the model check at Route: one tiny call per pinned id (`claude-opus-5-5` on `claude -p`, and `gpt-6.1-sol` on `codex exec`, effort `high`, which is both the Builder's model and, since 2026-10-12, the gate default), printed as the Route entry's lines. The match is read from the log's model stamp, never from the answer: on 2026-10-12 GPT-5.6 Sol answered "gpt-6.1-sol" and GPT-6.1 Sol said it did not know, while both logs stamped the right model. Exit 1 on any mismatch, which goes to Sean before any seat runs.

`seat.py check` is the preflight: both machine-local lists present, the scanners at their full paths, the Codex seat home signed in and its guard trusted at its current hash. Run it before every engagement; a gap stops the engagement at Open.

## The machine-local lists

Two files outside every repo, in `~/.config/devcraft/` (override with `$DEVCRAFT_LOCAL` for tests), one entry per line, `#` for comments: **`employer-paths`**, folders denied at the OS level (never-do 2), and **`names`**, the employer, client and startup names the git hooks refuse (never-do 11). Sean writes both by hand on each Mac. Neither is ever tracked, quoted or shown to a seat: the folder is in every pass's read deny, and a hit is reported by file and line, never by the name. A missing or empty list refuses every call: the wall fails closed. That includes a `git commit` run inside a seat's sandbox, so seats never commit: the coordinator commits a seat's staged paths under the seat's context (`DEVCRAFT_CONTEXT` and `DEVCRAFT_SEAT` set), where the hook can read the list and still applies the seat's zone ([the bench](../bench/README.md), SWCB #133).

## Item by item

| # | Wall here | Holds by |
|---|---|---|
| 1 | Seats never push or post; pushes only to `seanwinslow28` remotes | guard (`git push`, `gh` writes), sandbox network, pre-push |
| 2 | Employer paths unreadable | Claude `denyRead` + `Read` deny, Codex profile `deny`, guard |
| 3 | Nothing reaches a default branch from a build worktree; the merge runs in Sean's own checkout after his dated yes; no credential in a seat's environment | pre-push, scrubbed launch env, credential read denies |
| 4 | Boundary rule by seat; snapshot regeneration refused to Builder and Release; a seat's commit, made by the coordinator under that seat's context, holds only that seat's paths | Codex profile `read` entries, Claude `Edit` denies, guard, pre-commit |
| 6 | Credential files unreadable unless the plan opened that file to that seat; no credential variable printed | sandbox denies, guard, Codex env policy, pre-commit secret scan (gitleaks) |
| 7 | Writes resolve inside the worktree; no stash, branch, worktree or git-config changes; force-push only the build's own branch and never after the release gate | sandbox write limits, guard path resolution, pre-push |
| 8 | No `launchctl` load, `crontab`, workflow enable, publish or deploy commands | guard, settings denies |
| 11 | Listed names refused in commits, messages and pushes | pre-commit, commit-msg, pre-push |
| 12 | Seats never install; the coordinator's installs must run with scripts off | guard (`coordinator` role for the coordinator's own session) |
| 14 | Controls read-only, opened only for a plan-named file, never for `AGENTS.md`, `CLAUDE.md` or a skill; project settings and hooks never load into a seat | Codex profile, Claude `Edit` denies and `--setting-sources ""`, Codex hook trust, guard |
| 15 | Network off but the plan's hosts | Claude sandbox allowlist, Codex profile network off |
| 16 | No `sudo`, global installs or system settings | guard, settings denies |
| 17 | Records, traces and logs never rewritten by a seat | sandbox and `Edit` denies, guard |

Items 5, 9, 10 and 13 have no wall here: 5 and 12's scan side are [the diff check's](../diffcheck/README.md), 9 is the launcher's caps (`seat.py launch`, above), 10 and 13 are contract only.

## What the guard cannot see

A script the seat writes and then runs (`python3 x.py`) does whatever the sandbox lets it; that is why the sandbox is the wall. On Claude, file tools and hooks run outside the sandbox, so `Read` and `Edit` denies cover the file tools. A new file a Verifier or Release creates outside its zone after the settings were written is the guard's alone. Codex's sub-agent tools cannot be switched off: a spawn is caught from the pass log (`collab_tool_call`), never prevented.

## Tests

```bash
cd ~/Code-Brain/studios && uv run --no-project --with pytest python -m pytest devcraft/hooks/tests -q
```

The seeded cases run every call through the guard in both vendors' payload shapes, under `/usr/bin/python3` and the current Python; the git hooks run through real commits; the Codex profiles run through `codex sandbox`, the real Seatbelt policy, with no model call; the launcher's caps, kill switch, helper catch, output filing and probe run against a fake `codex` and `claude` put first on `PATH`. `python3 devcraft/hooks/tests/live.py` then sends one real seat session per vendor into a fresh worktree and reads the guard log and the worktree, never the seat's own account, to confirm each vendor held, and launches one real Builder pass through `seat.py launch` capped at two tool calls, which must be killed at the second.
