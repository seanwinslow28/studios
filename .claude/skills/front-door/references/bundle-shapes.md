# The brief bundle: `Planning/<slug>/`

What a front-door room leaves behind, in the piece's folder in the media root, and what the studio's master skill does with it at Open. The lens's brief-draft template fixes the studio-specific sections; this file fixes what every bundle has. Written on SWCB #267 (2026-10-23), lock 2.

```
<media root>/<piece>/Planning/<slug>/
├── concept.md            # the human document: why the piece matters, in the room's own words
├── brief-draft.md        # the studio's brief shape, from its lens's template; the source Open copies from
├── board.md              # the reference board, to the lens's board template
├── session.md            # the sidecar (references/sidecar-contract.md); never quoted onward
├── look/                 # every captured still: round-NN-<axis>-<option>.png and .txt (its prompt), host named in the .txt
├── motion/               # every motion clip the same way, when a motion round ran; absent otherwise
└── bundle.sha256         # sha256 of every file above but itself, written last by `shasum -a 256`, verified before the bundle is shown
```

Nothing else lives here. A thumbnail of someone else's work stays out of the folder (the board links it); a frame of Sean's own earlier work may sit in `look/` as a reference, named as his in its `.txt`.

## `concept.md`

Prose Sean would sign, not a form. The movements it plays through, in the session's own language, dropped when one truly does not apply:

1. Title options, three or four, the lean first with why.
2. The idea in one sentence: subject, engine, payoff.
3. Register: the tonal contract, where the humour or gravity is allowed to come from and where it is forbidden, the references named with their *what*.
4. The subjects and the engine: who or what is in it and the mechanism that makes it move, one design-bearing specific each.
5. The hero moment and the signature move, and the craft rule that makes it land, in words a gate can hold.
6. The look, as the look stage settled it: the board's borrowed elements, the chosen hero frame by path, the negatives.
7. Objective, audience, where it lives.
8. The stress test: the triage, each surviving risk as "Fails if ___" with its cheapest test, the verdict and Sean's decision.
9. Open threads: the non-binding residuals and what a fuller session would still grill. An empty list reads as "we stopped thinking".

A studio's lens may add a movement; it never removes one.

## `brief-draft.md`

The lens's template, section for section, exact headers and order. Every bundle's brief-draft carries, whatever the studio:

- **A header** the studio's Open can read: `slug`, `piece`, `studio`, the recommended engagement `type` (Open decides), `concept`, `board` and `hero_frame` each as `<path> sha256:<hash>`, `sidecar` by path, `written` (date).
- **The ASK lines**, `ASK1`, `ASK2`, …, each one thing the studio is held to, each ending with the lock id it traces to (`[L14]`). The studio's intake maps these as it maps any brief's.
- **What good looks like**: the board rows that bind, by row id; the chosen hero frame by path and hash **as a taste reference, never a frozen look**; and the signature move's timing feel in Sean's words. This is the section the first train never had, and the reason the room exists.
- **What this is NOT**: the nearest plausible wrong versions, fenced. A NOT that only inverts a positive is padding and fails the structure check.
- **Non-negotiables**: one checkable directive per line, each something a reviewer could verdict a frame, a clip or a file against. "Hold the pre-strike frames past comfort, at least 36 frames" checks; "punchy timing" does not.
- **Stress residuals that bind** are already folded into the two sections above; the brief-draft does not keep a separate list. The non-binding ones stay in `concept.md`.

## `board.md`, `look/`, `motion/`

Owned by the lens: its board template and its look-stage forms say what a row and a round carry. The spine requires only that every row has a link and a borrowed-what, every file has its prompt beside it, and nothing generated is the only copy.

## What the studio's Open does with it

Fixed by the studio's master skill, one line there (SWCB #267, next ticket 2). The shape every studio follows: Open **takes `brief-draft.md` as the brief's source**, copies its ASK lines into the engagement's `brief.md` unchanged, and cites `concept.md`, `board.md` and the hero frame **by path and sha256**, so the brief, the sidecar and the bundle hash tie together and the ledger can prove which bundle a train opened from. Open may add (the id, the roster, the budgets, the P0 rule) and may refuse (a bundle whose hash does not verify, a type the piece does not fit); it never rewrites a line. A rewrite is a `SUPERSEDES` entry in the sidecar, in a new front-door sitting Sean asks for.
