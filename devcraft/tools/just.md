# just.

just is a command runner: a file called `justfile` at the top of a project holds named recipes, and `just check` runs one. It gives every job the same few one-word commands, for Sean, for Claude and for the hooks. Read this before adding a justfile to a project.

## What it's best at.

- **One name for a group of commands.** `just check` runs the tidy check, the type check and the tests, in order, stopping at the first failure.
- **A menu anyone can read.** `just --list` prints every recipe with its one-line description, so nobody has to dig through a README to find the test command.
- **One source of truth.** The pre-commit hook, Claude's `Stop` hook and Sean all run the same `just check`, so "it passed for me" means the same thing everywhere.

Where another tool beats it:

- **A project with two commands.** A justfile for `pytest` alone is ceremony. It earns its place once a job has more than a few commands, or a command with fussy flags people keep getting wrong.
- **Real logic.** Loops, branches and error handling belong in a Python or shell script that a recipe calls. A recipe should read like a list.
- **Building files only when their inputs change.** That's make's job. just always runs what you ask.

## Setup.

- **Install** with `brew install just` (1.59.0, October 15, 2026). Free. Not yet on Sean's Macs.
- **The command that proves it works,** in a folder with a justfile:

```bash
just --version && just --list
```

## Getting the best out of it.

**A good justfile for a small Python project.** uv runs the project, Ruff tidies and lints, Pyrefly checks types, pytest tests:

```just
set positional-arguments

# Run every check: lint, types, tests.
check: lint types test

# Ruff: style and common mistakes, without changing files.
lint:
    ruff check .
    ruff format --check .

# Pyrefly: catch type mistakes before the code runs.
types:
    pyrefly check

# Run the tests. Extra pytest options go after the name.
test *args:
    uv run pytest "$@"

# Tidy the code in place.
fmt:
    ruff format .
    ruff check --fix .
```

The comment above each recipe becomes its description in `just --list`. With no recipe named, just runs the first one, so `check` goes first and plain `just` does the safe thing. `check` does no work of its own; it lists the recipes it depends on, which run first. A line that fails stops the recipe, so `check` stops at the first broken step and the error stays on screen.

**Recipes with arguments.** `test *args` takes zero or more extra words, so `just test -x` and `just test tests/test_jobs.py` both work. `+args` would need at least one, and `name` alone is a required argument. A default is written `name="all"`. By default just pastes arguments in as text with `{{args}}`, and the shell then splits anything with a space in it, so `just test -k "uv and launchd"` turns into the wrong command. `set positional-arguments` hands the words to the shell as real arguments, and `"$@"` passes them through whole. For a single argument, putting quotes around it (`'{{name}}'`) also works, unless the value itself holds a quote.

**Each line is its own shell.** A `cd` on one line is forgotten by the next. Either put both on one line with `&&`, or write the recipe as a script.

**Pick the shell on purpose.** just uses `sh` by default, not Sean's zsh. For recipes that should stop on any error, including one in the middle of a pipe, add `set shell := ["bash", "-euo", "pipefail", "-c"]`.

**Hide helpers.** A recipe whose name starts with an underscore, or that has `[private]` above it, still runs but stays out of `just --list`. Keep the menu to what a person would type.

**Wire it into the hooks.** Inside a job's own project, its pre-commit hook and Claude Code's `Stop` hook should both call `just check`, not their own copy of the commands. (The studios repo's own commit check is separate: it guards secrets and private names for every studio.) When the check changes, it changes in one place.

## Where it goes wrong.

- **The recipe that became a program.** Twenty lines of shell with `if` and loops inside a recipe. Move it to `scripts/` and call it; scripts can be tested and checked with ShellCheck.
- **Split arguments.** A path or test name with a space breaks in a way that looks like a pytest bug. Use `set positional-arguments` and `"$@"`.
- **Mixed indentation.** Each recipe's lines must be indented the same way throughout. A tab and spaces mixed in one recipe is an error.
- **Drift.** A justfile nobody runs goes stale while the hook keeps its own list of commands. If the hook doesn't call `just check`, one of them is lying.
- **Too many recipes.** Thirty recipes is a menu nobody reads. Keep the few that are used; delete the rest.
- **Secrets through `.env`** (below).

## Safety.

just runs commands on Sean's Mac and uploads nothing. The caution is `set dotenv-load`. It's off by default. Switched on, just reads a `.env` file from the working folder or a folder above it and puts every value into the environment of every recipe and every command those recipes start. A password kept there for one recipe then reaches the tests, the linters and anything Claude runs through `just`, and one stray debug print can put it in a log. A `.env` is also easy to commit by mistake in a public repo. Leave `dotenv-load` off. When one recipe needs a secret, read it by name in that recipe only, for example from the macOS keychain with `security find-generic-password -s <name> -w`, and keep the value out of the justfile.

Sources: [just manual](https://just.systems/man/en/), especially [settings](https://just.systems/man/en/settings.html), [recipe parameters](https://just.systems/man/en/recipe-parameters.html), [avoiding argument splitting](https://just.systems/man/en/avoiding-argument-splitting.html) and [dotenv settings](https://just.systems/man/en/dotenv-settings.html); [releases](https://github.com/casey/just/releases). Checked November 10, 2026. just isn't installed yet, so the example justfile hasn't been run.
