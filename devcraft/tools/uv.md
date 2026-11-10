# uv.

uv installs Python itself, builds each project's venv (its private Python folder), locks package versions and runs scripts. Read this before creating a venv, pinning a Python, or pointing a scheduled job at one.

## What it's best at.

- **Python that Homebrew can't touch.** uv installs Python into its own folder and upgrades it only when asked. This is the heart of the first job.
- **Exact, repeatable environments.** A lockfile records every package version, and `uv sync --locked` rebuilds the same venv anywhere.
- **Single-file scripts with their own needs.** A comment block at the top of a script lists its packages, and `uv run` builds a matching environment on demand.
- **Speed.** Rebuilding a venv takes seconds, so throwing one away and rebuilding it is a normal move, not a risky one.

Where another tool beats it: the python.org installer also sits out of Homebrew's reach, but every upgrade is a manual download. pipx installs Python apps too, but it repairs broken environments after the fact; uv's design tries to stop them breaking.

## Setup.

- **What's installed.** uv 0.10.2 at `~/.local/bin/uv`. The latest is 0.13.7 (November 3, 2026). Free. Update with `uv self update`; the update is Sean's call, since every job uses uv.
- **Pythons on this Mac:** uv's own 3.11.14 and 3.12.11, Homebrew's 3.13.12 and 3.14.8, and Apple's 3.9.6 at `/usr/bin/python3`.
- **The command that proves it works,** and shows which Python each request would use:

```bash
uv --version && uv python list --only-installed
```

**Changes since 0.10.2 that matter here:**

- 0.11.8: a `.python-version` file naming an exact patch (`3.14.8`) turns off automatic patch upgrades for that project. Pin `3.14`, not `3.14.8`.
- 0.11.24: project venvs are reused after a patch upgrade instead of being rebuilt.
- 0.12.0: `uv python install 3.14 --reinstall` now reinstalls the patch you have. Use `--upgrade` to move to a newer one.
- 0.13.0: uv's default Python became 3.15. A project that needs 3.14 must pin it.

## Keep Homebrew's Python out.

By default uv prefers its own Python, but it will still use one it finds on the system, Homebrew's included, before downloading. So a venv can quietly land on Homebrew's Python. One setting closes that door. In `~/.config/uv/uv.toml`:

```toml
python-preference = "only-managed"
```

Put the same line under `[tool.uv]` in each project's `pyproject.toml`. A scheduled job may not find the user settings file, and a project file travels with the code. For a single command, `--managed-python` does the same.

A second setting decides whether uv may download Python by itself mid-command. `python-downloads = "manual"` allows downloads only through `uv python install`, so an overnight job never fetches a Python from the internet. The trade-off: a fresh checkout fails until someone runs the install. That's a choice for Sean.

## How a venv finds its Python.

A venv holds no Python of its own. It holds a link. `.venv/bin/python` is a symlink (a file that points at another file) to the real interpreter, and `.venv/pyvenv.cfg` records that interpreter's folder on a `home =` line. Read both to see where a venv really points:

```bash
cat .venv/pyvenv.cfg
ls -l .venv/bin/python
ls ~/.local/share/uv/python
```

When the interpreter at the end of that link disappears, the venv is dead. Nothing warns you. The next run fails to start, or dies with a "library not loaded" error. A venv can't be repaired by pointing it somewhere new; it's rebuilt, which with uv is quick:

```bash
uv venv --clear        # plain venv
uv sync --locked       # project: rebuilds .venv from the lockfile
```

**What this Mac shows (checked November 10, 2026, read-only).** All six uv-built venvs and tools found here point at an exact patch folder, such as `cpython-3.12.11-macos-aarch64-none`. There is no minor-version folder (`cpython-3.12-…`) at all, so none of them would follow a patch upgrade. Remove 3.12.11 and five of them break, including one behind a nightly job. Why the folder is missing wasn't confirmed: 3.11.14 predates the design becoming standard, but 3.12.11 was installed in April 2026 by a uv that should have made one. The likely fix is to install through an updated uv, check that the minor folder appears, then rebuild each venv so it points through it.

Venvs made by Homebrew's own Python point at `/opt/homebrew/opt/python@3.14`, a link Homebrew moves on each patch upgrade. Those survived 3.14.5 to 3.14.8 here. They break when Homebrew drops 3.14 altogether.

## Patch upgrades.

```bash
uv python upgrade 3.14     # newest 3.14.x
uv python upgrade          # every installed minor version
```

The design, standard since 0.10.0: uv keeps a folder named for the minor version (`cpython-3.14-macos-aarch64-none`) that links to the newest patch. Venvs built through it follow each upgrade with no rebuild. The old patch stays installed, because something might still use it. Upgrades never cross a minor version; 3.14 to 3.15 is always a deliberate rebuild.

Three cases don't follow:

- **An exact patch request,** such as `uv venv -p 3.14.8` or a `.python-version` that says `3.14.8`. That's the escape hatch, on purpose.
- **A venv made by another tool** that resolved the link to the real patch folder.
- **Anything not uv-installed,** including Homebrew's Python.

After a uv update, 0.13.5's notes say to run `uv python upgrade` to pick up refreshed builds.

## Projects and lockfiles.

```bash
uv python pin 3.14       # writes .python-version
uv lock                  # writes uv.lock
uv lock --check          # fails if uv.lock is out of date
uv sync --locked         # builds .venv exactly from uv.lock
uv run --locked job.py   # runs inside it
```

`--locked` fails if the lockfile is missing or out of date. `--frozen` uses the lockfile without checking it. For anything unattended, `--locked` is right: a mismatch stops the run instead of silently installing something new. `--offline` forbids network use entirely.

## Single-file scripts.

A script can carry its own needs in a comment block (the PEP 723 standard):

```python
# /// script
# requires-python = ">=3.14"
# dependencies = ["httpx"]
# ///
```

`uv init --script job.py --python 3.14` starts one; `uv add --script job.py httpx` adds a package; `uv lock --script job.py` writes `job.py.lock` beside it, which later runs reuse. The `dependencies` line must be there even when empty. A shebang of `#!/usr/bin/env -S uv run --script` makes the file runnable, but only where `uv` is on the PATH, which a scheduled job's isn't.

## Tools.

`uv tool install ruff` puts a tool in its own venv under `~/.local/share/uv/tools` and its command in `~/.local/bin`. Those venvs link to an interpreter like any other, so they break the same way. `uv tool list` shows them; `uv tool upgrade --all` updates them; `uv tool install --reinstall <name>` rebuilds one.

## Pointing a launchd job at a stable path.

launchd, macOS's scheduler, gives jobs a bare PATH with neither Homebrew nor `~/.local/bin` on it, so every path in a job file is written out in full. Two good shapes:

- **The venv's own interpreter:** `/Users/<you>/project/.venv/bin/python` followed by the script. No uv at run time. It follows patch upgrades only if the venv was built through the minor-version folder, so check with `ls -l` after building.
- **uv itself, by full path:** `/Users/<you>/.local/bin/uv run --locked --offline --project /Users/<you>/project /Users/<you>/project/job.py`. `--project` finds the venv but doesn't change folder, so the script needs its full path too. uv checks the venv matches the lockfile on every run. The cost is that the job now depends on uv's own version.

Never point a job at `/opt/homebrew/bin/python3`. That name moves to a new minor version without asking, and the job's packages don't move with it.

## Where it goes wrong.

- **Quietly on Homebrew's Python.** Without `only-managed`, uv may build on whatever it finds. Check `pyvenv.cfg`.
- **Pinned to a patch by accident.** A `.python-version` of `3.14.8` turns off upgrades. Pin the minor version.
- **Old installs without the minor folder.** Venvs built on them never move. List `~/.local/share/uv/python` and look for the link.
- **Removing a Python something still uses.** `uv python uninstall` on a patch a venv points at kills that venv. Check every venv and tool first.
- **A lockfile out of step.** Without `--locked`, a run can quietly install new versions. With it, the run stops and says why.
- **An unpinned script.** Without a `.lock` or `exclude-newer` (a date after which no package release counts), a script's packages drift between runs.

## Safety.

uv downloads Python builds and packages from the internet and installs them into your home folder; it uploads nothing and costs nothing. Ask Sean before `uv self update`, before uninstalling any Python, and before rebuilding a venv that a scheduled job uses. Rebuild beside the old one where you can, and keep the old one until the job has run cleanly on the new.

## More details

- Python versions, upgrades, minor-version folders and preferences: https://docs.astral.sh/uv/concepts/python-versions/
- Settings (`python-preference`, `python-downloads`, `offline`, `exclude-newer`): https://docs.astral.sh/uv/reference/settings/
- Settings file locations (`~/.config/uv/uv.toml`, `/etc/uv/uv.toml`): https://docs.astral.sh/uv/concepts/configuration-files/
- Scripts: https://docs.astral.sh/uv/guides/scripts/
- Release notes: https://github.com/astral-sh/uv/blob/main/changelogs/0.10.x.md, 0.11.x.md, 0.12.x.md, and https://github.com/astral-sh/uv/blob/main/CHANGELOG.md for 0.13.
- Flags were checked against `--help` on uv 0.10.2 and the release notes through 0.13.7, November 10, 2026.
