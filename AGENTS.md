# studios

Sean Winslow's -craft teams: craftwork's shared law and every team's public machinery, in one repo. A project repo of the SWCB brain.

## The rules live in the brain

Read the brain's rulebook first: [`SWCB/AGENTS.md`](https://github.com/seanwinslow28/SWCB/blob/main/AGENTS.md), locally `~/Code-Brain/SWCB/AGENTS.md`. Nothing from it is copied here.

## Folder map

| Folder | Holds | Owner |
|---|---|---|
| `craftwork/` | The law every team inherits, the shared templates, the handoff law and the trace kit | Sean |
| `productcraft/`, `systemcraft/` | Each team's machinery: its own law (`CLAUDE.md`), bench, lanes, templates and trace profile | Sean |
| `<team>/corpus/` | The team's canon: distillates and book ingests. **Private, gitignored** | Sean |
| `<team>/ledger/` | A clone of the team's private `<team>-ledger` repo. **Private, gitignored**; commit and push it in its own repo | Sean |
| `<team>/books/` | Guard only: ebooks live in `~/Books/<team>/`. **Gitignored** | Sean |
| `.claude/skills/` | The doors: `craftwork`, `productcraft`, `systemcraft`. `.agents/skills/` links to them for Codex | Sean |
| `bin/` | Repo checks | Sean |

A live session Sean drives counts as Sean. No overnight agent works this repo.

## Rules for this repo

- **This repo is public; the private layer never enters it.** A team's corpus, ledger and books stay on disk, and book-derived text never lands in a tracked file or an issue.
- **Run `bin/canary-check.sh` before every push.** It proves git would stage nothing private. A new team gets the same three private folders, and the check covers it without edits.
- **Each team's law is its own `CLAUDE.md`**, on top of [`craftwork/law.md`](craftwork/law.md). Work inside a team follows both.
