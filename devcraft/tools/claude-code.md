# Claude Code.

Claude Code is Devcraft's lead and builder: it reads the code, plans the change, writes it, runs it and shows the proof. Read this before starting any build.

## What it's best at.

- **Working inside a real project.** It reads files, runs commands, edits, reruns the tests and reads the output, in one loop, on Sean's Mac.
- **Plans before changes.** In plan mode it explores and writes a plan without touching a file, so Sean can see the whole change before any of it happens.
- **Breadth.** It can send several helpers (subagents: separate Claude workers with their own fresh context) at once, each with one clear piece, and gather what they find.
- **Rules it can't forget.** Hooks and permission rules are run by the program itself, not by the model, so they hold every time.

Where another tool beats it:

- **The cold fresh check.** Claude reviewing Claude shares the same blind spots. Codex, a different maker's model that never saw the build, does the fresh check (see `codex.md`).
- **Fixed, repeatable commands.** A sequence that never changes belongs in a justfile (see `just.md`), not in a prompt.
- **Known holes in downloaded packages.** pip-audit answers that from a database, not from judgment (see `pip-audit.md`).

## Setup.

- **What's installed.** Claude Code 2.1.322, the latest on November 10, 2026, as the native build at `~/.local/bin/claude`. Paid for through Sean's existing plan; no extra cost.
- **The command that proves it works:**

```bash
claude --version && claude doctor
```

- **Updates** come with `claude update`. Do them between jobs, not halfway through one.
- **Where the settings live.** `.claude/settings.json` in a project holds its hooks and permission rules and is shared with the repo. `CLAUDE.md` holds what Claude should know there. Personal preferences go in `CLAUDE.local.md`, kept out of git.

## Getting the best out of it.

**Plan first, then build.** Plan mode reads and explores but blocks every edit until the plan is approved. Press Shift+Tab to cycle into it, or start with `claude --permission-mode plan`. This is Terraform's habit from the shelf: show every change before making it. For the first job, a good plan names each scheduled job it will move, the exact Python each will run on afterwards, and how to put each one back. A plan that says "update the jobs" has not done the looking yet.

**Give it a check it can run.** Claude stops when the work looks done. With a command that comes back pass or fail (`just check`, a test file, a script that compares output to a saved copy) it can close the loop itself: change, run, read the failure, fix, run again. The most useful line in a project's `CLAUDE.md` is the command that runs that check. Done means Sean can see it run, so the proof is the command and its real output, never a sentence saying it passed.

**Keep `CLAUDE.md` short.** It loads into every session, and every line costs a little attention on every task. Write only what Claude can't learn from the code: the check command, a trap the code hides, a name that means something odd here. Claude Code's own guide suggests staying under 200 lines. If a line keeps being ignored, capitals won't fix it. Either the file is too long and the line is lost, or the rule has no exceptions and belongs in a hook.

**Hooks for what must happen every time.** A hook is a script Claude Code runs at a fixed moment: before a tool runs (`PreToolUse`), after it (`PostToolUse`), or when Claude tries to finish (`Stop`). A `Stop` hook that runs the check and exits with code 2 on failure sends Claude back to work with the error, and the turn can't end until it passes. After eight blocked stops in a row, Claude Code lets the turn end anyway. Keep hooks for zero-exception rules; preferences stay in `CLAUDE.md`.

**Skills for procedures.** A skill is a folder (`.claude/skills/<name>/SKILL.md`) holding instructions for one kind of task. Claude sees only its name and description until the task calls for it, so a long procedure costs nothing on unrelated work.

**Send several helpers at once, for the right reasons.** Helpers earn their cost on independent pieces that can run side by side, on noisy searches whose output you only need the answer from, and on a review by someone who hasn't seen the reasoning. Handing the same task to a helper doesn't make the answer better, and a fresh helper first has to gather what the main session already knew, so it can be slower. A helper defined in `.claude/agents/` with only `tools: Read, Grep, Glob` is a reviewer that cannot edit, enforced by the program rather than asked for in a prompt.

**Worktrees for parallel work.** A worktree is a second checkout of the same repo in its own folder, so two pieces of work can't trample each other's edits. `claude -w fix-launchd` starts a session in a new one. A worktree is a fresh copy: ignored files such as `.env` aren't there and nothing is installed yet. List small ignored files Claude should copy in a `.worktreeinclude` at the repo root. A worktree made by `claude -p --worktree` isn't cleaned up for you; remove it with `git worktree remove <path>`.

**Manage the conversation.** `/clear` between unrelated tasks costs nothing and keeps the next answer focused. `/compact keep the test commands and the plan` shortens a long session around what matters. `/rewind`, or Esc twice on an empty prompt, rolls the code, the conversation or both back to an earlier prompt, which makes a bold first attempt cheap. After two failed corrections, `/clear` and write one better prompt that folds in what you learned; a third correction adds to a conversation already full of wrong attempts.

**Scripted runs with `claude -p`.** `claude -p "prompt"` runs once and exits, for shell loops and scheduled jobs. A safe scripted run names its tools and caps itself:

```bash
claude -p "Run just check and fix any failure in src/. Reply OK or FAIL." \
  --allowedTools "Read,Edit,Bash(just check)" \
  --permission-mode dontAsk --max-turns 20 --output-format json
```

`--allowedTools` pre-approves what it may use, `dontAsk` refuses everything else instead of waiting for a person, `--max-turns` stops a run that wanders, and `--max-budget-usd` caps spend in this mode. `--output-format json` gives one result to parse. `--bare` skips `CLAUDE.md`, hooks and plugins so a run behaves the same anywhere, but it signs in only with an API key, never Sean's normal login, and hooks don't run under it.

## Where it goes wrong.

- **Says done without proof.** "All tests pass" with no command shown. Ask for the command and its output, or let a `Stop` hook decide. A described result is not a result.
- **Widens the scope.** Asked to fix one job, it tidies five files and renames a function. Small changes are easier to review and to undo, as Google's small-changes guide on the shelf argues. Name the boundary in the prompt and read the diff for anything outside it.
- **Invents an API.** A flag, a setting or a function that sounds right and doesn't exist. Check against the tool's own `--help` or docs before relying on it. One real case: Codex's review command looks as if it takes a branch and custom instructions together, and it refuses.
- **Long sessions drift.** After hours and several compactions, early instructions fade and old wrong attempts pull the work sideways. A boundary stated only in chat can be lost when the conversation is compacted; anything that must hold goes in a deny rule or a hook.
- **Checkpoints miss shell edits.** `/rewind` restores files Claude changed with its own edit tools, not files a shell command changed. Commit before anything risky; git is the real undo.
- **Over-trusting a helper.** Its summary sounds sure whether it's right or not. Check anything load-bearing yourself.

## Safety.

Claude Code runs commands on Sean's Mac with his permissions, so the permission mode decides what it can do unasked:

- **manual** (`default` in settings): asks before every edit and every command that isn't read-only.
- **acceptEdits**: makes file edits and simple file commands without asking.
- **plan**: reads only, until the plan is approved.
- **auto**: runs everything, with a separate model checking risky actions first. New terminal sessions start here. It blocks things like piping a download into a shell, force pushes and sending private data out, but its makers say plainly it doesn't guarantee safety.
- **dontAsk**: refuses anything that would have asked. Good for scripted runs.
- **bypassPermissions**: runs everything unchecked. Only inside a throwaway machine, such as a Tart test Mac.

Writes to `.git`, `.claude`, `.zshrc` and similar files are never approved automatically outside `bypassPermissions`. Deny rules (`"deny": ["Read(./.env)"]` in settings) hold in every mode, so a never-rule goes there, not in `CLAUDE.md`. `/sandbox` adds an operating-system fence around its shell commands on macOS. `claude -p` skips the "do you trust this folder?" question, so run it only in folders you trust. Everything Claude reads goes to Anthropic to be processed, so it reads secrets and private material only when the job needs them, and never writes them into a public repo. Ask Sean before anything that spends money, publishes, uploads his work, or deletes outside the job's folder.

Sources: [Claude Code docs](https://code.claude.com/docs/en/best-practices), [permission modes](https://code.claude.com/docs/en/permission-modes), [releases](https://github.com/anthropics/claude-code/releases); flags checked against `claude --help` on 2.1.322, November 10, 2026.
