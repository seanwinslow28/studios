# The wall

The machine layer of Devcraft's never-do list ([`devcraft/CLAUDE.md`](../CLAUDE.md), rule 9): the sandbox and permission settings every seat pass runs under, the guard hook on top of them, and the git hooks on every build worktree. Built on the Devcraft build map's **Build the never-do hooks and sandbox config** ticket (2026-10-11), from the never-do ticket's wall column and that day's probes of both vendors.

The order of trust is fixed. **The OS sandbox is the wall**; the permission deny rules sit beside it; **the guard only adds sight** the first two lack (which seat is running, a path after `~` and links are resolved, a wrapped `sh -c`, a plan-named exception). A hook fails open on a timeout or a mistyped path, so nothing here relies on the guard alone, and every seat contract still states every item. The after-check is the diff check, on its own ticket.

| File | What it is |
|---|---|
| [`policy.py`](policy.py) | The rules as data: seats and their write zones, controls, credentials, records, snapshot flags, the machine-local lists. One copy, read by everything below and by the diff check |
| [`guard.py`](guard.py) | The PreToolUse hook, one script for both vendors. Exit 2 with a reason refuses; every decision is appended to the pass's guard log |
| [`shellparse.py`](shellparse.py) | Splits a command line into the simple commands the guard judges: `sh -c`, `$(…)`, `env`, `cd`, redirects, heredocs |
| [`gitcheck.py`](gitcheck.py), [`git/`](git/) | pre-commit, commit-msg and pre-push for a build worktree |
| [`seat.py`](seat.py) | The coordinator's tool: writes a pass's seat context, its Claude settings or Codex pass profile, the Codex seat home, a worktree's git hooks; builds the launch line; runs the preflight |
| [`tests/`](tests/) | The seeded cases (must refuse, must pass) beside the hooks, the Codex sandbox matrix, and `live.py` |

## How a pass is walled

1. **Open** installs the worktree's git hooks: `seat.py worktree <worktree> --engagement <eng>`. It sets `core.hooksPath` for that worktree only (`extensions.worktreeConfig`), so Sean's own checkout never runs them.
2. **Before each pass** the coordinator writes the seat context, copying every plan-named exception from the plan gate's frozen "Exceptions on the record" table and nowhere else: `seat.py context --seat <seat> --worktree <wt> --engagement <eng> --pass NN --branch <branch> [--test-path P] [--ops-path P] [--grant-read F] [--grant-control F] [--host H]`. It lands in `<eng>/trace/logs/pass-NN.context.json`, written once.
3. **Claude seat:** `seat.py claude-settings <context>` writes the settings file: sandbox on and failing closed, no escape hatch, network limited to the plan's hosts, `denyRead` and `Read` denies for credentials, employer paths and (for all but the Verifier) `held-out/`, `Edit` denies for controls, records, the shared references and everything outside the seat's zone as the worktree stands, git writes only to the build branch's own refs, and the guard on `PreToolUse` and `SessionStart`. **Codex seat or gate:** `seat.py codex-pass <context>` writes the pass profile into the seat home: the Builder's extends `:workspace` with test paths, Release's ops paths and every control (present or not) read-only; a gate's extends `:read-only`; both deny credentials, employer paths and `held-out/`, keep the engagement folder read-only and the network off, and mark the worktree untrusted so a repo's own `.codex/` config never loads.
4. **Launch** with `seat.py launch <context> --prompt-file <f> [--budget USD] --run`: a scrubbed environment (no tokens), `--setting-sources ""` for Claude, `-p <profile>` and no `--sandbox` for Codex. The forms are in [the bench README](../bench/README.md#launch-forms).

`seat.py check` is the preflight: both machine-local lists present, the scanners at their full paths, the Codex seat home signed in and its guard trusted at its current hash. Run it before every engagement; a gap stops the engagement at Open.

## The machine-local lists

Two files outside every repo, in `~/.config/devcraft/` (override with `$DEVCRAFT_LOCAL` for tests), one entry per line, `#` for comments: **`employer-paths`**, folders denied at the OS level (never-do 2), and **`names`**, the employer, client and startup names the git hooks refuse (never-do 11). Sean writes both by hand on each Mac. Neither is ever tracked, quoted or shown to a seat: the folder is in every pass's read deny, and a hit is reported by file and line, never by the name. A missing or empty list refuses every call: the wall fails closed.

## Item by item

| # | Wall here | Holds by |
|---|---|---|
| 1 | Seats never push or post; pushes only to `seanwinslow28` remotes | guard (`git push`, `gh` writes), sandbox network, pre-push |
| 2 | Employer paths unreadable | Claude `denyRead` + `Read` deny, Codex profile `deny`, guard |
| 3 | Nothing reaches a default branch from a build worktree; the merge runs in Sean's own checkout after his dated yes; no credential in a seat's environment | pre-push, scrubbed launch env, credential read denies |
| 4 | Boundary rule by seat; snapshot regeneration refused to Builder and Release; a seat commits only its own paths | Codex profile `read` entries, Claude `Edit` denies, guard, pre-commit |
| 6 | Credential files unreadable unless the plan opened that file to that seat; no credential variable printed | sandbox denies, guard, Codex env policy, pre-commit secret scan (gitleaks) |
| 7 | Writes resolve inside the worktree; no stash, branch, worktree or git-config changes; force-push only the build's own branch and never after the release gate | sandbox write limits, guard path resolution, pre-push |
| 8 | No `launchctl` load, `crontab`, workflow enable, publish or deploy commands | guard, settings denies |
| 11 | Listed names refused in commits, messages and pushes | pre-commit, commit-msg, pre-push |
| 12 | Seats never install; the coordinator's installs must run with scripts off | guard (`coordinator` role for the coordinator's own session) |
| 14 | Controls read-only, opened only for a plan-named file, never for `AGENTS.md`, `CLAUDE.md` or a skill; project settings and hooks never load into a seat | Codex profile, Claude `Edit` denies and `--setting-sources ""`, Codex hook trust, guard |
| 15 | Network off but the plan's hosts | Claude sandbox allowlist, Codex profile network off |
| 16 | No `sudo`, global installs or system settings | guard, settings denies |
| 17 | Records, traces and logs never rewritten by a seat | sandbox and `Edit` denies, guard |

Items 5, 9, 10 and 13 have no wall here: 5 and 12's scan side are the diff check's, 9 is the launcher's caps, 10 and 13 are contract only.

## What the guard cannot see

A script the seat writes and then runs (`python3 x.py`) does whatever the sandbox lets it; that is why the sandbox is the wall. On Claude, file tools and hooks run outside the sandbox, so `Read` and `Edit` denies cover the file tools. A new file a Verifier or Release creates outside its zone after the settings were written is the guard's alone. Codex's sub-agent tools cannot be switched off: a spawn is caught from the pass log (`collab_tool_call`), never prevented.

## Tests

```bash
cd ~/Code-Brain/studios && uv run --no-project --with pytest python -m pytest devcraft/hooks/tests -q
```

The seeded cases run every call through the guard in both vendors' payload shapes, under `/usr/bin/python3` and the current Python; the git hooks run through real commits; the Codex profiles run through `codex sandbox`, the real Seatbelt policy, with no model call. `python3 devcraft/hooks/tests/live.py` then sends one real seat session per vendor into a fresh worktree and reads the guard log and the worktree, never the seat's own account, to confirm each vendor held.
