# Craftwork

Craftwork is the shared kit and recipe every studio is built from. It's a starting point, never a set of rules a studio has to obey: each studio takes a copy of the template, makes it its own, and reads the shared guides when a step needs them.

Every studio works the same way. One lead owns each job from the front door to the finish. Helpers add breadth and a fresh check for facts, but never send work back. Only truth and safety rules live in the template; taste lives on each studio's own taste page, in Sean's words. Everything Sean reads is plain English.

## What's in the kit

| Part | What it is |
|---|---|
| `template/` | What each studio copies: the lead's instructions (`SKILL.md`), the taste page, the studio's front-door page, and the folders for expertise briefs, tool mastery guides and the shelf of good work. Book notes go in a private `library/` folder that git ignores. |
| `guides/job.md` | The six steps every job runs, helpers, the fresh check, and the two records a job keeps. |
| `guides/front-door.md` | The shared front-door method: one question at a time, the brainstorm, showing options, and what a clear ask holds. |
| `guides/review-pages.md` | The house review page every checkpoint uses, and the end-of-job scorecard. |
| `guides/build-a-studio.md` | The recipe for building or rebuilding a studio, and how it stays small. |
| `new_studio.py` | Builds an empty studio from the template and links it in as a skill. |
| `checks/` | The size check, the old-terms scan, the two checks git runs before every commit, and their tests. The public-safety check sits in `bin/`. |

Two shared tools live in the brain, so there's one copy of each: the plain-writing check (`~/Code-Brain/SWCB/tools/plain-check/`), which this repo's Claude settings run before anything is posted, and the house page template and its tools (`~/Code-Brain/SWCB/docs/prototypes/house-look/`).

## Build a studio

```
python3 craftwork/new_studio.py <name> "<what it makes>"
```

Then follow `guides/build-a-studio.md` with Sean.

## Run the checks

```
python3 craftwork/checks/size_budget.py
python3 craftwork/checks/old_terms.py
bin/canary-check.sh
uvx --from pytest pytest craftwork/checks
```

The size check holds each studio's always-loaded pages, the lead's instructions plus the taste page, to 2,000 words. The old-terms scan fails on any word from the studios' earlier setup, anywhere in the repo. The canary check proves git would never stage a studio's private book notes.

## The check before each commit

Every commit in this repo, by any studio or by hand, is checked first. Betterleaks stops passwords, keys and tokens (Gitleaks stands in when Betterleaks isn't installed), and `checks/private-names.sh` stops any name on Sean's private list, which is kept outside the repo at `~/.config/devcraft/names`. Neither prints what it found, only where. prek runs them, as set in `.pre-commit-config.yaml`. Set it up once per clone:

```
brew install betterleaks prek
git config core.hooksPath .githooks
```

If the list or both scanners are missing, the commit stops and says so: a check that can't run never passes. How to get the best out of both tools is in `devcraft/tools/betterleaks-and-prek.md`.
