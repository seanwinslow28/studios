# uv's managed Python and its "upgrade without breaking" design (2024 to 2026)

## What it is

Closest to Devcraft's first job. When Homebrew, the main Mac installer, upgrades its Python, it deletes the old copy. Any project box built on it (a "virtual environment": a private set of Python add-ons for one project) is left pointing at nothing, and a scheduled job running from it quietly stops.

uv is a fast Python installer from Astral, a software company, first released in February 2024. It can install Python itself into its own folder, where Homebrew never touches it. In June 2025 Astral added a further piece: when uv installs a newer bug-fix release of the same Python (say 3.12.10 to 3.12.11), project boxes move to it automatically and the old copy is kept. Standard since February 2026.

Docs: https://docs.astral.sh/uv/concepts/python-versions/ (see "Upgrading Python versions" and "Minor version directories").

**Best part to look at: the "Compatibility" list in the description of the change that added it** (linked under More details). In a short list it says exactly which project boxes get the automatic move and which don't, including that boxes made before the change keep working but won't move until rebuilt.

## How it turned out

- **Huge adoption.** uv has about 91,800 stars on GitHub (a star is a public bookmark), and Homebrew counted about 2 million uv installs in the past year, the 15th most installed item it tracks.
- **The demand was real.** The change closed five separate requests from users, the oldest from September 2024, all asking for some version of "upgrade Python without breaking my projects".
- **Reviewed in the open.** The combined change had 69 review comments. Its author notes that each smaller piece inside it had already been reviewed on its own.
- **Careful rollout.** It shipped behind a trial switch in uv 0.7.14 (June 2025) and only became the default after about eight months, in 0.10.
- **Thin spot:** I found no independent write-up measuring how often it saves a broken setup. The evidence is adoption, the closed requests and the documentation, not a study.

## What makes it good, measured

I read the documentation, the release notes and the change itself on GitHub. I didn't run uv.

- **The trick is one extra pointer.** uv keeps a folder named for the minor version (3.12) that points at the newest installed bug-fix copy (3.12.11). Project boxes point at the 3.12 folder, not at a specific copy, so an upgrade only has to move one pointer.
- **Nothing is deleted under you.** After an upgrade, uv prefers the new copy but keeps the old one, because a box might still use it. That's the opposite of Homebrew, whose manual says it runs a cleanup after every upgrade unless you set a switch to stop it.
- **It refuses to jump too far.** Automatic moves stay within one minor version (3.12.x). Going to 3.13 can change which add-ons work, so that stays a deliberate step.
- **You can opt out on purpose.** Ask for an exact version (3.10.8) and that box stays put.
- **Its limits are written down.** The docs name two cases where the automatic move won't happen: a box made with an exact version, and a box made by another tool that follows the pointer to the real folder. It also covers only uv-installed Python, not Homebrew's.
- **Size of the change:** about 3,000 lines added and 300 removed across 73 files, merged after 10 days.
- **The other approach, for contrast:** pipx, an older tool for installing Python apps, fixes breakage after the fact. Its manual lists commands to check environments, repair broken ones, or rebuild them all. uv's design tries to stop the breakage happening at all.

### Why it's here

It's a working answer to the exact failure Devcraft is being asked to fix, and a model of how to make such a change: a small, clear mechanism, nothing deleted that might still be in use, a deliberate escape hatch, and honest notes on where it doesn't apply.

## What Sean said about it

Sean's pick as the shelf piece closest to what Devcraft should make, November 10, 2026. He agreed with the reason the lead gave: it fixes the very problem of the first job the way Devcraft should work, with one small mechanism, nothing deleted that might still be in use, and honest notes on where it doesn't help.

It's the focus for now: a small fix that prevents the breakage, keeps what's in use, and says plainly where it stops.

On the first job's step 2 page (November 10), he said yes to the four things measured from it and its neighbours, in order: nothing still in use gets deleted; one fixed name, moved by one quick swap; tested against the real failure, with a way back that's been tried; says plainly where it stops.

## More details

- uv documentation, Python versions: https://docs.astral.sh/uv/concepts/python-versions/ and storage location (`~/.local/share/uv/python` by default): https://docs.astral.sh/uv/reference/storage/
- The change: "Support transparent Python patch version upgrades", pull request 13954, by John Mumm, opened June 10 and merged June 20, 2025: https://github.com/astral-sh/uv/pull/13954
- Release notes: 0.7.14 (trial) https://github.com/astral-sh/uv/blob/main/changelogs/0.7.x.md and 0.10.0 (standard) https://github.com/astral-sh/uv/blob/main/changelogs/0.10.x.md
- Requests it closed: issues 7287, 7325, 7892, 9031 and 12977 on https://github.com/astral-sh/uv/issues
- The Python builds uv installs come from python-build-standalone, started by Gregory Szorc in 2018 and handed to Astral in December 2024: https://gregoryszorc.com/blog/2024/12/03/transferring-python-build-standalone-stewardship-to-astral
- Homebrew's cleanup behaviour: `man brew`, under `upgrade` (cleanup runs unless `HOMEBREW_NO_INSTALL_CLEANUP` is set). Homebrew's own guide says to use a separate Python version manager when you need a lifecycle independent of Homebrew upgrades: https://docs.brew.sh/Language-Runtimes-and-Packages
- pipx commands (`health`, `repair`, `reinstall-all`) from its manual page in https://github.com/pypa/pipx
- Star and install counts read November 10, 2026, from GitHub's API and Homebrew's public analytics.
