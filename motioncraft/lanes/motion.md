---
lane: motion
seat: animator
updated: 2026-10-19
---
# Lane manifest — Animator

Mandatory first read for the [Animator](../bench/animator.md). Entries are title + pointer + one-line when-to-read — shelf labels, never the books: the content lives in the private corpus (`../corpus/`, gitignored), so pointers resolve only on a machine that has it (`manifest-only` grounding otherwise, per the seat preamble). Follow only the pointers relevant to the moves in hand. Seats stop at `## Reading path`; that section is the owner's.

This shelf is about moving the approved design with weight: timing and spacing as two separate controls, slow in and slow out named by pose and direction, arcs, weight from timing, spacing and squash at the contact with anticipation before and settling after, overlap, and holds with a stated cadence. The look is Art's, every duration is the Director's, the finish is Finishing's; this seat is the first Codex seat on visual work in any studio, and its first passes say so. The order below is vocabulary, principles, technique, then the application chapters last, as the book-to-seat brief fixed it.

## Before the first engagement

The five things this seat holds before mc-eng-001 opens (the book-to-seat brief's bold items, in the naming rulings' words), and where each is carried:

- **Timing (how many frames) versus spacing (how far between them)** — rows *Timing* and *Spacing* below; principle 1; the timing chart in [`contact-weight-and-settling.md`](../corpus/guides/contact-weight-and-settling.md).
- **Arcs** — row *Arc*; principle 3; the same guide.
- **Weight, through spacing into the contact and squash on it** — rows *Weight*, *Slow in and slow out*, *Squash and stretch*; principles 2 and 4, with the brief's corrected sign: a falling object speeds up into the floor, so the chart widens into the contact; the same guide.
- **Overlap** — row *Follow-through and overlap*; principle 5; no guide yet, so the row carries it.
- **Hold cadence and line-boil cadence** — rows *Hold*, *Moving hold*, *On ones, on twos*, *Line boil*; principle 6; [`grease-pencil-4-3-and-later.md`](../corpus/guides/grease-pencil-4-3-and-later.md) for holds, [`boil-and-painted-texture-continuity.md`](../corpus/guides/boil-and-painted-texture-continuity.md) for the boil.

## Vocabulary

This seat's words are rows of [the glossary](glossary.md), which every pass carries after this manifest, with each row's definition, field terms and sources, which seats share it, and the four naming rulings. This seat's rows, in learning order: *Volume*, *Smear*, *Multiple*, *Pigment variation*, *Timing*, *Spacing*, *Slow in and slow out*, *Weight*, *Anticipation*, *Squash and stretch*, *Follow-through and overlap*, *Arc*, *Deformation*, *In-between*, *Hold*, *Moving hold*, *On ones, on twos*, *Line boil* and *Texture continuity*.

## Principles, in learning order

Learned after the rows above and before the guides. "Named, not read" means the canon title was not read and no copy is ingested.

1. **Timing and spacing are two controls.** Canon: Williams, *The Animator's Survival Kit* (ingested, ch. 3–5 in [`books/the-animators-survival-kit/`](../corpus/books/the-animators-survival-kit/)): plan both on a chart before the in-betweens. Carried by the timing chart in [`contact-weight-and-settling.md`](../corpus/guides/contact-weight-and-settling.md) and the ingest, until "Timing and spacing on a chart" is written.
2. **Slow in and slow out, named by pose and direction** ("slow into the rest"), never bare "ease in". Carried by the same guide.
3. **Arcs.** An arc traced over adjacent frames runs smooth; a kink is a finding before anyone else finds it. Carried by the same guide.
4. **Weight comes from timing, spacing and squash at contact, with anticipation before and settling after.** Canon: Thomas and Johnston, *The Illusion of Life* (named, not read): the source of the twelve principles, drawn from Disney's studio practice. Carried by the same guide, with the corrected sign: the chart widens into the contact and bunches at each rebound's peak and into the rest.
5. **Follow-through and overlap.** No guide yet; the row, Lasseter 1987, p. 39, and the Williams ingest (ch. 8) carry it until "Anticipation, follow-through, overlap" is written.
6. **Holds and cadence: what stays still, what keeps living, ones or twos.** Carried by [`grease-pencil-4-3-and-later.md`](../corpus/guides/grease-pencil-4-3-and-later.md) for drawing keys and holds, until "Holds and cadence" is written.

## Technique

The starred guides by file. This seat owns one principle guide and one tool guide (under Application), times the smears of a second, moves the layers of a third, and reads a fourth for its audit.

- **Contact, weight and settling** — [`contact-weight-and-settling.md`](../corpus/guides/contact-weight-and-settling.md) — owned: before every contact, landing and settle; the timing chart for each move, squash on the contact frame with volume kept, and the evidence pack's adjacent frames.
- **Smears as designed poses** — [`smears-as-designed-poses.md`](../corpus/guides/smears-as-designed-poses.md) — this seat times what Art designed: each smear on the frames, between the keys and along the arc the plan lists, each strong smear one frame on ones, then one or two folding drawings into the next key (the canon's count, by Sean's ruling of 2026-10-19).
- **Line boil and painted-texture continuity** — [`boil-and-painted-texture-continuity.md`](../corpus/guides/boil-and-painted-texture-continuity.md) — this seat moves what Art designed: paint travels with the subject, line boil at Art's cadence, pigment variation held steady, nothing sliding.

Not yet written, so a topic for `thin_lane:` until it exists: **Timing and spacing on a chart**, **Anticipation, follow-through, overlap**, **Squash, stretch, constant volume** (with Art) and **Holds and cadence** (all ready now; Williams is ingested, so their depth can be drawn from it); **Straight ahead and pose to pose** and **Secondary action, exaggeration, appeal** (after the first film); **Multiples** (waits on a team test; Goldberg, ch. 12, now gives its timing); **Staggers** (ready now: Williams, ch. 12; Goldberg, ch. 12); **Kinetic type** (parked for a type engagement).

## Application

Last on the path, in the order the book-to-seat brief set. Grease Pencil was rewritten in Blender 4.3, so tutorials older than that, Blender Studio's free course included, are out of date. Blender 5.2.2 LTS is the scene tool on both machines, run by script through the application doorway. Fusion is closed for every seat (Sean, 2026-10-19): the scene crosses to Finishing as its CPU renders plus the `.blend`, never an exported composition, and since Resolve's API cannot keyframe, anything that moves, layered elements and the camera included, is animated in Blender.

- **Grease Pencil 4.3 and later** — [`grease-pencil-4-3-and-later.md`](../corpus/guides/grease-pencil-4-3-and-later.md) — owned: the introduction, draw mode, layers and onion skinning, animation and interpolation, the dope sheet, then the Noise and Time Offset modifiers, in that order; the Python reference last, read on the page (its licence is unconfirmed, so it is read-only).
- **Grease Pencil by script in Blender 5.2** — [`grease-pencil-by-script-5-2.md`](../corpus/guides/grease-pencil-by-script-5-2.md) — owned: before every Grease Pencil script; the pre-4.3 names beside their 5.2 replacements, drawings, strokes and points, thickness and opacity, materials, layers and groups, one drawing per key, Noise and Time Offset for line boil. A Grease Pencil scene is saved by the seat's script and rendered by the doorway's render request (`ask blender --render`), never by the seat's own script.
- **The scene by script for a painted 2D film** — [`the-scene-by-script.md`](../corpus/guides/the-scene-by-script.md) — owned: before every scene; keys and easing from the timing chart, on twos, squash and stretch with volume kept, layered image planes under a moving camera, layering and blending in Blender since Resolve cannot keyframe, and frame-repeatable CPU renders at 24 fps with the TC5 comparison. In place of the dropped "Compositing in Fusion".
- Blender's built-in Python, `DaVinciResolveScript`, `ffmpeg` and `ffprobe` are toolbelt ([seat file](../bench/animator.md#toolbelt)), not corpus.

## Audit duty: the delivery package and check record

This seat audits Finishing's package against the scene record's evidence pack, before the technical checks and Sean's yes, as a read-only pass (stake: *did the motion survive finishing?*). Every contact frame and every hold at its frame after compositing, grading and the edit; no cut trimming an anticipation, a contact or a settle; frame rate and duration matching the scene; nothing compressed or re-timed to fit. Read the checks section of [`resolve-finishing-and-delivery.md`](../corpus/guides/resolve-finishing-and-delivery.md) first, and look for what the curriculum brief says a reviewer should see in a cut, mix and check record:

- the loudness record shows −23 LUFS integrated and true peak at or below −1 dBTP, set by hand, since the normaliser's defaults are −24 and −2;
- no loudness-range figure, which the standard advises against under one minute;
- the sound plan lists layers per moment, at most about two and a half of one kind;
- the cut list gives each cut's reason, emotion first;
- the composite shows no texture sliding through the pull-back, and line boil at Art's cadence.

A craft fail is pinned to frame numbers in both versions in these rows of [the glossary](glossary.md): *Cut*, *Match cut*, *Image jitter*, *Texture sliding*, *J-cut and L-cut*, *Compositing*, *Grade*, *Linear and output colour*, *Loudness*, *True peak* and *Sound layers*, beside *Line boil* and *Texture continuity*, which this seat shares.

## Free layer

The free sources this seat's rows, principles and guides draw on, with the licence as the book-to-seat brief saw it on 2026-10-17 and what has become of each. `read-only` is a page a person reads; `open` is a licence that would allow an ingest, none made yet. "Carried by" names the guide that cites the source; "none yet" means a page with no guide behind it, so a decision leaning on it names the page.

| Source | Teaches | Licence, where seen | Status | Carried by |
|---|---|---|---|---|
| Lasseter 1987 | eleven of the twelve principles; timing as the source of weight; the timing chart; arcs | course copy, licence not checked | read-only | the contact guide, the smear guide |
| Pixar in a Box: the animation unit's bouncing-ball lessons | keys at the peak and the contact, the timing chart, squash on contact | CC BY-NC-SA shown on the lessons | read-only | the contact guide |
| Animation Mentor's bouncing-ball tutorials | rebounds that lose height in a steady pattern; spacing into the ground wider than out | all rights reserved | read-only | the contact guide |
| Becker's twelve-principles series | the vocabulary, with the picture | video, tier C | read-only | none yet |
| Toon Boom Learn and the Harmony documents | timing, spacing, straight ahead and pose to pose, hold exposure, deformation | all rights reserved | read-only | none yet |
| Blender manual: Grease Pencil animation, onion skinning, layers, materials, the dope sheet, the Noise and Time Offset modifiers; keyframes, F-curves and their modifiers, constraints, Mesh Plane, cameras, render output, colour management, the compositor; the release notes 4.3 to 5.2 | the application | CC BY-SA 4.0, the release notes' licence seen 2026-10-19 | open, not ingested; the notes read-only | the Grease Pencil guide, the Grease Pencil by script guide, the scene by script guide |
| Blender Python reference | scripting the scene | copyright Blender Authors, no licence shown (seen 2026-10-19) | read-only | the Grease Pencil by script guide, the scene by script guide |
| Blender Studio's animation page and free Grease Pencil course | a working studio's animation stage | CC BY 4.0 (studio terms); pre-4.3, so out of date for the tool | open, not ingested | none yet |
| Krita manual: the animation page, the walk cycle | in-betweens | GFDL 1.3 or later | open, not ingested | none yet |
| Meier 1996; the Paperman talk; Bénard 2010; the Jam Filled interview | line boil and painted texture in motion | all rights reserved; Toon Boom copyright | read-only | the texture guide (all four); the Grease Pencil guide (the interview) |
| Avender on Cartoon Research; AnimSchool's smear basics | smear terms, when to use one, multiples | no reuse licence; no licence shown | read-only | the smear guide |
| The earlier practical tests' checkpoints on the brain's private tracker | the contact that hovered, the landing that snapped: history, not an example | private | private tracker | the contact guide, the smear guide |

## Canon

Two titles on this lane are ingested: Williams, under `../corpus/books/the-animators-survival-kit/`, and Goldberg, under `../corpus/books/character-animation-crash-course/` (both 2026-10-19). Every other canon title stays "named, not read" until its own ingest lands there on its own ticket.

- **Williams, *The Animator's Survival Kit*, expanded ed.** — the seat's primary: plan timing and spacing on a chart before the in-betweens; fast action is planned drawing by drawing, not left to blur. Ingested: [`books/the-animators-survival-kit/`](../corpus/books/the-animators-survival-kit/). Cheatsheet first; ch. 3–5 (timing, spacing, keys and breakdowns, ones and twos) are the core, then ch. 6–7 (walks, runs), ch. 8–12 (overlap, weight, anticipation, takes and accents, staggers), ch. 17 for ones against twos and holds. The fast-action line, which the brief marked least certain, now reads: on fast action every drawing is drawn, with contact drawings, skipped frames and one stretched in-between on ones, and inked speed lines are dropped (ch. 5); only the very fastest runs fall back on blur drawings or two-frame dissolves (ch. 7). Its drawings are described, not stored; its moving examples were not captured.
- **Goldberg, *Character Animation Crash Course!* (2008)** — the fast-action fill beside Williams, and the smear guide's depth. Ingested: [`books/character-animation-crash-course/`](../corpus/books/character-animation-crash-course/). Cheatsheet first (its gap-or-smear table); ch. 12 (smears, multiples, impact distortion, vibrations, staggers, camera shake) is the reason it is here, then ch. 5–7 (screen-time thresholds, cushions, ones with twos, the gap for impact, the off-centre breakdown), ch. 8–9 (squash, overlap, the mini-smear, weight). Its fast-action line: a smear is one drawing reaching the outer edges of both keys, one frame on ones, then one or two folding drawings into the new pose; a multiple, a double-speed in-between and an impact distortion are one frame each; on twos any of them reads as a bad drawing; gimmicks only where no correct movement can do the job. Its drawings are described, not stored; its movie tests and flipbooks were not captured.
- **Thomas and Johnston, *The Illusion of Life*** — the source of the twelve principles, drawn from Disney's studio practice, where weight is felt through timing and the way a body gives and recovers on impact. Named, not read; print only.

## Reading path

Corpus states are as of the `updated:` date in the header. Format and audio facts are the book-to-seat brief's, checked 2026-10-17.

| # | Title | Read this when | Format | Audio | Corpus |
|---|---|---|---|---|---|
| 1 | Becker's twelve-principles series, 24 minutes | first on this path: the vocabulary, at a screen | video | needs the picture | read-only · listen |
| 2 | Lasseter 1987 | the vocabulary and principles, with the page numbers the rows cite | PDF, a course copy | — | read-only |
| 3 | Williams, *The Animator's Survival Kit* (expanded ed.) | the seat's canon, after Lasseter: the chart before the in-betweens | Apple Books interactive ebook, screen-captured and ingested on Sean's word; its moving examples not captured | none found | ingested |
| 4 | Thomas and Johnston, *The Illusion of Life* | the principles' source, when Williams is done; half of it is history | print only | — | named · not bought |
| 5 | Blender Studio's animation page; Krita's walk cycle | principles, by a working studio and a manual | web | — | open, not ingested |
| 6 | Goldberg, *Character Animation Crash Course!* (2008) | the fast-action fill the brief named beside Williams, for the smear guide's depth | Apple Books fixed-layout ebook, screen-captured and ingested on Sean's word; its movie tests not captured | — | ingested |
| 7 | Grease Pencil chapters, then the Python reference | the application chapters, last | web | — | open, not ingested; the reference read-only |
| 8 | Bénard's survey and the Paperman talk | technique, for line boil | PDF | — | read-only |
| 9 | CGInsider #2304 on the twelve principles, 32 minutes | the listening order's animation item, tier C | audio | by ear | listen |

### Next

- Whitaker, Halas and Sito, *Timing for Animation* (2021) — the fallback to Williams, timing alone. Locked ebook, read-only; waits for a yes outside the map.
