# Devcraft's tool list

The tools Devcraft uses, one pick per kind of work, with Sean's yes or no. Scouted on November 10, 2026 for today's best, not for what the last setup used. Each tool gets a mastery guide in this folder before the lead uses it on a job.

Sean said yes to the whole list on November 10, 2026: the free tools, installed or updated as each job needs them, and no paid apps. Everything picked is free, apart from the two coding agents Sean already pays for. The only paid options are two apps for seeing scheduled jobs, listed as runners-up; the first job doesn't need either.

A few words used below: a **venv** is a project's private Python folder; **launchd** is the scheduler built into macOS that runs jobs overnight; a **hook** is a check git runs on its own before each commit.

## The list

| Kind of work | The pick | Sean's answer |
|---|---|---|
| The coding agent | Claude Code builds and leads; Codex CLI does the cold fresh check with its built-in review command. Already paid for. Both installed. | Yes. |
| Python versions and venvs | uv, with Python installed by uv itself, never Homebrew's. Homebrew can't upgrade what it didn't install, which is the heart of the first job. Free. Installed, but eight months out of date. | Yes. |
| Tidying and checking Python | Ruff for tidy, consistent code; Pyrefly to catch mistakes before the code runs (a "type checker"). Free. Not installed. | Yes. |
| Testing | pytest, with Hypothesis for tests that try hundreds of odd inputs. Free. Not installed (added per project). | Yes. |
| Shell script quality | ShellCheck to catch bugs, shfmt to tidy, Bats to test. Free. ShellCheck installed; the other two not. | Yes. |
| Scheduled jobs (launchd) | macOS's own tools, `launchctl` and `plutil`, which agents can drive and read. Free. Built in. | Yes. |
| A throwaway test Mac | Tart: a disposable copy of macOS running inside a window, wiped after each test. Free for personal use. Not installed. Needs about 25 GB of disk. | Yes. |
| Secret and private-name scanning | Betterleaks, run before every commit by prek. Free. Gitleaks installed; Betterleaks and prek not. | Yes. |
| Repeatable commands | just, so every job has one-word commands like `just check`. Free. Not installed. Only once a job has more than a few commands. | Yes. |
| Extra code review | Nothing new. The Codex fresh check is enough, and pip-audit, already installed, checks downloaded Python parts for known holes. | Yes. |

## Runners-up and not now

- **Coding agent:** Codex as the builder and Claude Code as the checker works too; swap if one is weaker on a job. Others (Cursor's agent, Gemini's) add a third bill for little gain.
- **Python:** the python.org installer also sits where Homebrew can't touch it, but each upgrade is a manual download. mise handles many languages; overkill for mostly Python. pyenv builds Python from source: slower, more to go wrong.
- **Type checker:** ty, from the makers of uv and Ruff, is still a test version (0.0.100). Switch once it reaches 1.0.
- **Testing:** Python's built-in unittest works, but pytest tests are shorter and clearer.
- **Scheduled jobs:** Sean said no to both paid apps. LaunchControl, about **$33 once**, shows every job and why it failed, with one-click fixes. Worth it if Sean wants to see the jobs himself; agents don't need it. Lingon Pro, **$23.99 once**, is simpler but has no fix-it help.
- **Test Mac:** UTM, free, works but is harder to script. A second user account shares Homebrew with the real one, so it isn't safe. A second Homebrew folder isn't supported by Homebrew.
- **Scanning:** Gitleaks, already installed, uses the same rules; fine as a fallback. The original pre-commit framework needs Python, the very thing that breaks; prek is one file with no Python. Plain git hooks work but are harder to share.
- **Commands:** make is built in but fussier to write.

## The old safety walls

Sean's answer, November 10, 2026, on the three walls the old setup had:

- **The check before each commit: rebuild it smaller.** Yes. One short check before every commit in the studios repo stops passwords, keys and Sean's employer's name. It uses Betterleaks (Gitleaks as the fallback) and the private name list in Sean's home folder, and never prints a name it finds. Built on the next Devcraft ticket.
- **The command guard: dropped.** It blocked tools rather than bad outcomes, and would block the first job itself. The lead's page already says to ask before anything big, costly or hard to undo.
- **The hand-written password and key patterns: dropped.** The scanner's own maintained patterns cover them.

## Two things to know

- **The scanner's private-name list must live outside the repo.** The repo is public, so a rule file naming what to hide would itself leak it. The list stays in Sean's home folder and the hook points at it.
- **The laptop has about 58 GB free.** One test Mac takes about 25 GB. The Mac Mini may be a better home for it; that needs checking.

## More details

**What's on this Mac (checked November 10, 2026, read-only):** Claude Code 2.1.322 (latest), Codex CLI 0.163.0 (latest 0.167.0), uv 0.10.2 (latest 0.13.7), ShellCheck 0.11.0 (latest), Gitleaks 8.30.1, pip-audit, osv-scanner, Homebrew 7.0.10, Homebrew Python 3.13.12 and 3.14.8, uv's own Python 3.11 and 3.12. Not installed: Ruff, ty, Pyrefly, pytest, shfmt, Bats, Betterleaks, prek, pre-commit, just, mise, pyenv, Tart, UTM, LaunchControl, Lingon.

**Versions and sources:**

- Claude Code 2.1.322, Nov 10: [releases](https://github.com/anthropics/claude-code/releases)
- Codex CLI 0.167.0, Nov 6; `codex review` runs a review without a chat: [releases](https://github.com/openai/codex/releases)
- uv 0.13.7, Nov 3: [releases](https://github.com/astral-sh/uv/releases). uv will still use Homebrew's Python if it finds one first, unless told "only-managed": [docs](https://docs.astral.sh/uv/concepts/python-versions/)
- Ruff 0.17.4, Nov 5: [releases](https://github.com/astral-sh/ruff/releases)
- Pyrefly 1.4.1, Nov 4, stable: [releases](https://github.com/facebook/pyrefly/releases)
- ty 0.0.100, Nov 9: [releases](https://github.com/astral-sh/ty/releases)
- pytest 9.2.0, Oct 27: [releases](https://github.com/pytest-dev/pytest/releases); Hypothesis 6.170.15: [releases](https://github.com/HypothesisWorks/hypothesis/releases)
- shfmt 3.14.1: [releases](https://github.com/mvdan/sh/releases); Bats 1.14.0: [releases](https://github.com/bats-core/bats-core/releases)
- Tart 2.41.1, Oct 15, Functional Source License (free for internal use): [license](https://github.com/openai/tart/blob/main/LICENSE), [repo](https://github.com/openai/tart)
- Betterleaks 1.10.0, Nov 4, MIT, by Gitleaks's original author: [releases](https://github.com/betterleaks/betterleaks/releases), [launch story](https://www.bleepingcomputer.com/news/security/betterleaks-a-new-open-source-secrets-scanner-to-replace-gitleaks/amp/). Gitleaks's last release was March 2026: [releases](https://github.com/gitleaks/gitleaks/releases)
- prek 0.5.10, Nov 4: [releases](https://github.com/j178/prek/releases)
- just 1.59.0, Oct 15: [releases](https://github.com/casey/just/releases)
- LaunchControl 2.12, Sep 28, ~$33: [comparison](https://soma-zone.com/LaunchControl/comparison.html), [release notes](https://www.soma-zone.com/LaunchControl/ReleaseNotes.html)
- Lingon Pro 10, $23.99: [site](https://www.peterborgapps.com/lingon/)
- UTM 5.0.8, Oct 17: [releases](https://github.com/utmapp/UTM/releases)

**Changes this year worth knowing:** OpenAI announced in March that it is buying Astral, maker of uv, Ruff and ty; both say all three stay open source ([report](https://thenewstack.io/openai-astral-acquisition/)). OpenAI now also keeps Tart. Gitleaks's author left and started Betterleaks.

**Install commands (for when Sean says yes):**

```
uv self update
uv python install 3.14 && uv python pin 3.14
uv tool install ruff && uv tool install pyrefly
uv add --dev pytest hypothesis   # per project
brew install shfmt bats-core betterleaks prek just
brew install openai/tools/tart
```

Set `python-preference = "only-managed"` in uv's settings so it never falls back to Homebrew's Python.
