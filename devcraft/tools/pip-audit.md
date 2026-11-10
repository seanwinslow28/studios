# pip-audit.

pip-audit checks a project's downloaded Python packages against public lists of known security holes and says which versions have them and which version fixes each. Read this before adding a package, before finishing a job that changed the lock file, and when a scheduled job's packages haven't been looked at in a while.

## What it's best at.

- **Known holes at exact versions.** A "known vulnerability" is a flaw someone has reported publicly and given an ID, such as `PYSEC-2023-74` (the Python advisory list), `GHSA-...` (GitHub's) or `CVE-...` (the general one). pip-audit matches every pinned package against those lists.
- **A plain answer for a script.** It exits 0 when nothing is found and 1 when something is, so a check can fail on it.
- **The fix, not just the problem.** Each finding names the first version without the hole.

Where another tool beats it:

- **uv's own `uv audit`.** uv added an audit command in June 2026. It reads `uv.lock` directly, asks OSV (an open vulnerability database run by Google), and can skip a hole only while no fix exists (`--ignore-until-fixed`). It is still a preview feature in uv 0.13.7, so it may change without notice, and Sean's uv 0.10.2 doesn't have it yet. pip-audit is stable and installed today. Once uv is updated, the choice is Sean's (see the end).
- **Malware.** pip-audit finds honest packages with mistakes, not packages built to attack. uv has a separate, opt-in malware check (`UV_MALWARE_CHECK=1`, also preview).
- **Your own code.** It reads the package list, never the code.

## Setup.

- **What's installed.** pip-audit 2.10.1 from Homebrew, the latest release (June 10, 2026). Free.
- **A catch.** The Homebrew copy runs on Homebrew's Python, the very thing that breaks when Homebrew upgrades. If it stops starting after an upgrade, run it through uv instead: `uvx pip-audit`, or install it once with `uv tool install pip-audit`.
- **The command that proves it works:**

```bash
pip-audit --version
```

## Getting the best out of it.

**Audit a uv project from its lock file.** Export the locked versions and feed them straight in:

```bash
uv export --format requirements-txt --frozen --no-emit-project \
  | pip-audit -r /dev/stdin --require-hashes --disable-pip
```

`--frozen` uses `uv.lock` exactly as it is, without re-solving. `--no-emit-project` leaves out the project itself, which isn't on any list. uv writes a hash (a fingerprint of each package file) next to every pin by default, and `--require-hashes` makes pip-audit insist on them. `--disable-pip` is the important one: it stops pip-audit from solving and installing the packages itself. Without it, `pip-audit -r` behaves much like `pip install`, which can run a package's own setup code on Sean's Mac. Add `--no-dev` to `uv export` to check only what the job runs, not the test tools. This exact command was run on November 10, 2026 against a throwaway project pinned to an old `requests`: it found 24 known holes in three packages and exited 1.

**Read the table.** Four columns: package, version, ID, and fix versions. `--desc` adds a short description of each hole and `--aliases` shows its other IDs. In 2.10.1 the same ID can appear twice in a row, so count distinct IDs, not lines. `-f json` gives one record per package for a script.

**Choose the database on purpose.** The default service is PyPI's own vulnerability data. `-s osv` asks OSV instead, which sometimes knows more; in that mode `--require-hashes` checks only that hashes are present, not that they match, and pip-audit prints a warning saying so.

## What to do with a finding.

- **Read the advisory first.** Does the flaw sit in a part of the package this job uses? A hole in a web server feature doesn't touch a script that never serves anything. Say which, in a sentence.
- **Upgrade through uv.** `uv lock --upgrade-package <name>` moves that one package to the newest allowed version; then `uv sync`, `just check`, and the audit again. One package per change keeps it easy to undo.
- **Don't use `--fix` on a uv project.** It knows nothing about `uv.lock`: it changes the environment or the requirements file it was handed, so the lock falls out of step.
- **When it can't be fixed yet.** No fix version, or the fix breaks something: skip it with `--ignore-vuln <ID>`, write the reason beside it, and look again. A skip with no reason is a hole nobody remembers deciding to keep.

## Where it goes wrong.

- **A clean run read as "safe".** It means no *known* hole in these *Python packages* today. It says nothing about malware, about your own code, about C libraries a package bundles inside it, or about the Python program itself. A new advisory can appear tomorrow against the same lock file, so a scheduled job's packages need checking again from time to time.
- **Auditing the wrong thing.** Run with no input, pip-audit checks whatever Python environment it happens to be running in, which may be Homebrew's, not the job's. Always feed it the project's lock.
- **Unpinned input.** A requirements file with loose versions makes pip-audit solve them, and it may check versions the job never installs. The export from `uv.lock` pins everything.
- **Noise.** Some advisories are wrong or don't apply to how a package is used. The fix is a reasoned skip, not switching the check off.

## Safety.

- **What it sends.** pip-audit sends the name and version of every package to the vulnerability service: PyPI by default, or OSV with `-s osv`. `uv audit` sends the same to OSV. For public packages that reveals little, but the package list of a private project hints at what it does, and a private package's name goes out too. Ask Sean before auditing anything he has marked private.
- **What it runs.** With `--disable-pip` and a hashed export, nothing is installed or built. Never audit a requirements file you wouldn't install.
- **What it changes.** Nothing, unless `--fix` is given. Upgrades go through uv as a normal change, with the check run after.

**A decision for Sean, later.** Once uv is updated, `uv audit` reads `uv.lock` with no export step and handles "skip until a fix exists" on its own. The cost is that it's a preview feature that can still change, against pip-audit's stable tool that works today. Keeping pip-audit until `uv audit` leaves preview is the cautious choice.

Sources: [pip-audit README and security model](https://github.com/pypa/pip-audit), [uv CLI reference for `uv audit` and `uv export`](https://docs.astral.sh/uv/reference/cli/), [uv changelog](https://github.com/astral-sh/uv/blob/main/CHANGELOG.md), [Astral's announcement](https://astral.sh/blog/uv-audit). Flags checked against `pip-audit --help` on 2.10.1, November 10, 2026.
