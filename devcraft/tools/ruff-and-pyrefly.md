# Ruff and Pyrefly.

Ruff tidies and checks Python: its linter flags likely mistakes and bad habits, and its formatter rewrites the layout so every file looks the same. Pyrefly is a type checker: it reads the type hints (notes in the code like `path: str` that say what kind of value goes where) and finds code that would fail when it runs. Neither runs your code. Read this before setting up a Python project or tidying a script.

## What they're best at.

- **Ruff: one fast tool for three jobs.** Lint, sort imports and format, in well under a second for a small project, with safe automatic fixes for most of what it finds.
- **Pyrefly: the 2 a.m. failures, caught at noon.** A value that might be `None` used as if it were text, a function called with the wrong kind of argument, a misspelled attribute, a name only set on one branch of an `if`. A scheduled job hits these at night with no one watching; Pyrefly finds them while you write.

Where something else beats them:

- **Proving behaviour** belongs to tests (see the pytest guide). A clean lint says the code is tidy, not that it's right.
- **Shell scripts** belong to ShellCheck.
- **ty**, from the makers of uv and Ruff, is the runner-up type checker. See the last section.

## Setup.

Both are free and install as standalone tools that uv keeps in its own folder, away from Homebrew:

```bash
uv tool install ruff==0.17.4
uv tool install pyrefly==1.4.1
ruff --version && pyrefly --version
```

Versions current on November 10, 2026: Ruff 0.17.4 (November 5) and Pyrefly 1.4.1 (November 4, a stable release line since 1.0).

**Pin the version and upgrade on purpose.** Ruff 0.16, in July 2026, grew its default rule set from 59 rules to 413. Simon Willison wrote up his own projects failing their checks overnight, with no code change, because they installed whatever was newest. The same lesson as uv's Python design on the shelf: nothing should change under a working setup without a deliberate step. Upgrade between jobs with `uv tool upgrade ruff`, run the checks, and fix or note what's new. Ruff can also refuse to run at the wrong version: `required-version = ">=0.17.4"` in its settings.

## A starting setup for small scripts.

```toml
[project]
requires-python = ">=3.14"

[tool.ruff]
required-version = ">=0.17.4"
line-length = 88

[tool.ruff.lint]
extend-select = ["I", "B"]

[tool.pyrefly]
project-includes = ["src", "tests"]
python-interpreter-path = ".venv/bin/python"
preset = "default"
```

Why these and not more:

- **Ruff's own defaults earn their keep now.** Since 0.16 they cover syntax errors, names used before they exist, unused imports and variables, and slices of the best plugin groups (bugbear, pyupgrade, simplify, Pylint's error checks). They were chosen to catch real faults, not taste. Keep them; add to them with `extend-select`, because `select` throws the defaults away.
- **`I`, import sorting,** so imports always come in one order and diffs stay small.
- **`B`, bugbear,** the whole group. Its rules catch genuine bugs: a list used as a default argument (shared between every call), a bare `except:` that swallows Ctrl-C, a function made in a loop that captures the loop variable late.
- **Leave out** `D` (docstring style, mostly noise in a script), `ANN` (demands type hints everywhere; let Pyrefly judge the hints you write) and `ALL`. Try `S`, the security group, once on a script that handles input from outside, but expect it to flag every `subprocess` call, wanted or not.
- **Ruff reads the Python version** from `requires-python`, so it suggests only syntax your Python has.

## What each catches.

```python
import os, sys                      # Ruff: sys unused (F401); imports unsorted (I001)

def add_job(name, jobs=[]):          # Ruff: mutable default argument (B006)
    jobs.append(name)
    return jobs

def home_dir() -> str:
    return os.environ.get("HOME")   # Pyrefly: bad-return. get() may give None
```

The third is the classic overnight crash. `os.environ.get` returns `str | None`, and under launchd (macOS's scheduler, which starts jobs with almost no environment) the variable you counted on may well be missing. Pyrefly says so before the job ever runs. The fix is a decision, not a silencing: `os.environ["HOME"]` to fail loudly, or a stated fallback.

## Getting the best out of them.

**The everyday loop.**

```bash
ruff check --fix      # lint, apply the safe fixes
ruff format           # then format
pyrefly check         # then type check
```

Fix before formatting, because a fix can leave lines the formatter wants to tidy. For a yes or no without touching files, use `ruff format --check` and plain `ruff check`; both exit with 1 when something is wrong. `ruff check --watch` reruns on every save.

**Safe and unsafe fixes.** Ruff applies only fixes meant to keep the code's behaviour. Others, which may change behaviour or drop comments, need `--unsafe-fixes`. Since 0.17 Ruff shows them by default but doesn't apply them. Apply them only on a clean git state, then read the diff line by line.

**Pyrefly and gradual typing.** You don't have to annotate everything. Pyrefly still checks the insides of functions without hints and infers what they return. Hints pay most at the edges: function arguments and return values, especially anything read from the environment, a file or a command's output. Annotate those and Pyrefly can follow the values through the rest. Presets set how strict it is:

- **No config at all gets `basic`:** syntax errors, missing imports, unknown names. A clean run then means little.
- **`default`** checks the hints you wrote properly. Right for Devcraft's scripts.
- **`strict`** also forbids silent `Any` (the "anything goes" type) and missing `@override` markers. Worth it for a shared library, overkill for a script.

`pyrefly init` writes a starting config, and migrates a mypy or Pyright one if it finds it.

**Point Pyrefly at the project's own Python.** It has to see the venv (the project's private Python folder) to know what the installed packages look like. Without `python-interpreter-path`, a flood of `missing-import` errors usually means it found the wrong interpreter, not that the code is broken.

**Silence narrowly, with a reason.** Name the one rule and say why, on the line:

```python
from .api import client  # noqa: F401  re-exported for callers

# ruff: ignore[B008]  # built once at import, on purpose
def run(clock=SystemClock()): ...

value = parse(raw)  # pyrefly: ignore[bad-argument-type]  # upstream hint is wrong
```

The `# ruff: ignore[...]` form, new in 0.16, can sit on its own line above a statement and covers the whole statement, which suits a long function signature. Use `per-file-ignores` in the config for a rule that's wrong for a whole kind of file. Then let the tools find stale silences: `ruff check --extend-select RUF100 --fix` removes `noqa` comments that no longer suppress anything, and `pyrefly suppress --remove-unused` does the same for Pyrefly.

**Old code with many errors: use a baseline, not a carpet of comments.** `pyrefly check --baseline=baseline.json --update-baseline` records today's errors in one file; afterwards only new ones are reported, and the file shrinks as you fix the old ones.

## Where it goes wrong.

- **Noise.** Turning on `ALL`, or every group that sounds useful, buries the real finding under fifty style complaints, and people learn to ignore the tool. Add one group at a time and keep it only if its first findings were worth fixing.
- **Blanket ignores.** A bare `# noqa`, a file-wide `# ruff: noqa`, a bare `# type: ignore`, or running `ruff check --add-noqa` or `pyrefly suppress` across a project to "get to green". Each hides future mistakes on that line too. Spot it by grepping for ignores without a rule code.
- **Fighting the formatter.** Some lint rules disagree with the formatter: tab and indent checks (`W191`, `E111`, `E114`, `E117`), quote style (`Q000` to `Q004`), and trailing commas (`COM812`, `COM819`). Enabled together, fix and format undo each other forever. Leave those rules off. A file full of `# fmt: off` is the same fight by hand: accept the formatter's layout.
- **Unpinned upgrades.** New defaults arrive with new findings. Pin, then upgrade deliberately.
- **Unsafe fixes taken on trust.** One of Ruff's own examples swaps an `IndexError` for a `StopIteration` on an empty list. Read the diff.
- **Hints that lie.** `cast()`, `Any` and wrong hints make Pyrefly confidently agree with broken code. A type checker only knows what the hints say.
- **"Pyrefly passed" with no config.** That's the `basic` preset. Check that a config exists before trusting a clean run.

## ty, the runner-up.

ty is Astral's type checker, very fast and built to sit next to Ruff and uv. On November 9, 2026 it was at 0.0.100, still a test version whose behaviour can change between releases. Pyrefly is stable today. When ty reaches 1.0, try it on one project: if it catches the same faults with less noise, switching is a one-line change in how the check is run, since both read the same type hints.

## Safety.

Both run entirely on the Mac: they upload nothing and cost nothing. `--fix`, `--unsafe-fixes` and `ruff format` rewrite files in place, so start from a clean git state and let the diff show what changed.

## More details

- Ruff docs: https://docs.astral.sh/ruff/ (configuration, linter, formatter, default rules, settings). Release notes: https://github.com/astral-sh/ruff/releases
- Ruff 0.16 default rule change and `# ruff: ignore`: https://astral.sh/blog/ruff-v0.16.0
- Pyrefly docs: https://pyrefly.org/en/docs/ (installation, configuration, error suppressions, error kinds). Presets and 1.0: https://github.com/facebook/pyrefly/releases/tag/1.0.0
- Pyrefly's install page lists `pip` and `uvx`; `uv tool install` is uv's standard way to keep any such tool installed.
