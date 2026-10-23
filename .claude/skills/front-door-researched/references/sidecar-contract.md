# The room's sidecar: `Planning/<slug>/session.md`

The running memory of a front-door session and the only place Sean's reasons live. **The discipline is `creative-partner`'s sidecar contract, adopted whole and not copied here**: two blocks with hard ownership (LOCKED DECISIONS, orchestrator-owned and append-only; PROPOSALS LOG, stage-appended, four content kinds only), every lock a named specific carrying Sean's reason verbatim or no reason at all, `SUPERSEDES` entries instead of edits, option records with fixed fields, round headers on repeated axes, the five-lock honesty checkpoint with its trace comment, write failures that fail stop, and resume only when Sean names the file. Read that contract before the first session; this file lists only where the room departs from it. Written on SWCB #267 (2026-10-23), lock 2 and the open item on linking rather than copying.

## Where it departs

**Location.** Not the creative harness home. The sidecar sits **beside the bundle it produced**, at `<media root>/<piece>/Planning/<slug>/session.md`, because the bundle is what the studio's Open reads and the reasons behind its lines belong beside them. The preflight keeps its force: resolve the media root (`folders.local`, `media =`) and the target to canonical absolute paths; refuse to start unless the target is under the media root **and** outside every git working tree (`git -C <dir> rev-parse` on the folder must fail). The media project is never a repo; if that ever changes, the room stops and says so.

**One sidecar per piece, not per session.** A second evening on the same piece resumes the same file (a new `date:` entry in the header, locks continuing from the last id). A new slug is a new piece.

**Header stamps.** Every file that shapes the room, so two behaviourally different sessions never carry the same stamps:

```
skill: front-door-researched @ sha256:<SKILL.md>
sidecar_contract: sha256:<this file>
bundle_shapes: sha256:<bundle-shapes.md>
stress_test_rubric: sha256:<stress-test-rubric.md>
lens: <studio> @ sha256:<lens.md>
lens_files: <one `name @ sha256:` per template file in the lens folder, in folder order>
model: <the launched model id>
studio: <studio>
piece: <the piece's working name>
date: <YYYY-MM-DD>            # one line per evening, appended
ceiling: <the lens's spend ceiling, with its unit>   # Motioncraft: Higgsfield credits
stages: []                    # appended as stages run, in order
```

Hashes are 64 lowercase hex characters from `shasum -a 256`. `stages:` and `date:` are the header's only mutable lines; `stages:` records what actually ran (`micro-expand`, `expand:<axis>`, `grill`, `board`, `look:<axis>`, `motion:<axis>`, `stress-test`, `synthesis`, `structure-check`), a skipped stage simply absent.

**The opening locks.** `[L1] ASK (verbatim)` is Sean's idea, unedited, and takes no reason ask. The lens may require locks before any question (Motioncraft: `[L2] CEILING`, the Higgsfield credits the session may spend, set from his balance); they are Sean's numbers and take a reason only if he gives one.

## Proposals blocks the room adds

The four content kinds hold (`observations`, `options`, `recommendation`, `open_questions`). The block headers:

- `### micro-expand`, then `### expand:<axis> — round: n` on a deepened axis.
- `### grill:<point>` for each North Star point of the lens, numbered as the lens numbers them (`grill:3-where-it-lives`).
- `### board` for the reference board's rows as proposed, before Sean rules on each.
- `### look:<axis> — round: n — host: <chatgpt-desktop | codex-image-path>`: the three options as option records, each with `file:` (the captured frame's path under `look/`, filled at capture-back) and `prompt:` (the file beside it); `held:` what the round held and `varies:` the one thing it varied; `recommendation` the room's lean; `open_questions` what the eye could not settle.
- `### motion:<axis> — round: n — host: higgsfield — cost: <credits>` with the same option records (`file:` under `motion/`) and a `meter:` line (`spent / ceiling`).
- `### stress-test — pass: <in-room | fresh-context> — vendor: <...>`: observations hold the load-bearing assumptions and the bias note; options hold the triaged risks, each a `Fails if ___` with its cheapest test; recommendation holds the verdict and residuals.
- `### synthesis` only for a hole found while writing (an `open_question` naming the point to reopen).

## Locks the room writes

Besides the ordinary `[Ln] <axis>: <named specific>` with its `why (verbatim)` sub-line:

- A look-round lock names the option id and the file: `[Ln] look:<axis>: <option id>, <file>` so the chosen frame is found again without reading the block. A mix names where each element came from: `[Ln] look:<axis>: mix (palette from look:palette.b, line from look:line.a), <file>`.
- `[Ln] stress verdict: proceed (residuals: <named>)` or `revise`, after Sean's decision.
- `[Ln] bundle: <path>, bundle.sha256 <hash>` is the last lock of the room, written after the structure check passes.

## What the sidecar is for, and is not

It is the audit trail of the brief: the studio's Open cites the bundle by path and hash, and anyone asking "why does the brief say this" reads the lock. It is **never quoted into a tracked file, an issue or a ledger entry**; the brief carries the decision, the sidecar carries the reason. Thumbnails and frames never go inside it; they sit in `look/` and `motion/` and the sidecar names them by path.
