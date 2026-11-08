# studios

Sean Winslow's studios: each one makes one kind of work, with one lead who owns a job from the front door to the finish. Every studio is built from the shared kit in `craftwork/`. This is a project repo of Sean's private second brain, the SWCB repo.

## The rules live in the brain

Read the brain's rulebook first: [`SWCB/AGENTS.md`](https://github.com/seanwinslow28/SWCB/blob/main/AGENTS.md), locally `~/Code-Brain/SWCB/AGENTS.md`. Nothing from it is copied here.

## Folder map

| Folder | Holds |
|---|---|
| `craftwork/` | The shared kit: the template a studio copies, the shared guides, the builder and the checks. See [`craftwork/README.md`](craftwork/README.md). |
| `<studio>/` | One studio, built from the kit. The folder is also the studio's skill: its `SKILL.md` is the lead's page, beside the taste page and the folders that load only when needed. |
| `<studio>/library/` | The studio's book notes. **Private: git ignores it, and it never leaves this disk.** |
| `.claude/skills/`, `.agents/skills/` | Links to each studio folder, so Claude and Codex find it by name. The builder makes them. |
| `bin/` | The public-safety check. |

Sean owns all of it. A live session Sean drives counts as Sean. No overnight agent works this repo.

## Rules for this repo

- **This repo is public.** Book notes stay in each studio's private `library/`, and text drawn from a book never lands in a tracked file or an issue. Never name Sean's employer or its products here.
- **Run the checks before every push:** `bin/canary-check.sh` proves git would stage nothing private, and the kit's checks are listed in [`craftwork/README.md`](craftwork/README.md).
- **Follow-up work goes on the brain's private tracker,** one issue per item on `seanwinslow28/SWCB`, labelled `needs-triage`. Never an issue on this public repo, and never with text drawn from a book.
