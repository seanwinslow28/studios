---
lane: finishing
seat: finishing-sound-designer
updated: 2026-10-19
---
# Lane manifest — Finishing and Sound Designer

Mandatory first read for the [Finishing and Sound Designer](../bench/finishing-sound-designer.md). Entries are title + pointer + one-line when-to-read — shelf labels, never the books: the content lives in the private corpus (`../corpus/`, gitignored), so pointers resolve only on a machine that has it (`manifest-only` grounding otherwise, per the seat preamble). Follow only the pointers relevant to the finish in hand. Seats stop at `## Reading path`; that section is the owner's.

This shelf is about one delivered film, proven: a cut made for emotion first (the Director decides, this seat executes), a film designed for sound from the start, few sound layers, loudness measured against a written target, correction then a grade in linear light, and texture continuity checked in the composite. This seat is the accountable integrator; the delivered result is its artifact. The order below is vocabulary, principles, technique, then the application chapters last, as the book-to-seat brief fixed it.

## Before the first engagement

The five things this seat holds before mc-eng-001 opens (the book-to-seat brief's bold items), and where each is carried:

- **Cut for emotion before continuity** — rows *Cut*, *Match cut*, *J-cut and L-cut* below; principle 1; *In the Blink of an Eye*, ch. 6; the conform and cut sections of [`resolve-finishing-and-delivery.md`](../corpus/guides/resolve-finishing-and-delivery.md).
- **How many sound layers a listener can follow** — row *Sound layers*; principle 3; no guide yet, so the row and the *Suddenly Something Clicked* ingest's ch. 21 carry it.
- **The loudness target and true peak** — rows *Loudness* and *True peak*; principle 4; the Resolve guide's loudness section.
- **Linear versus display colour** — rows *Linear and output colour* and *Grade*; principle 5; the Resolve guide's grade section, stated there from the curriculum brief.
- **Texture continuity checked in the composite** — rows *Texture continuity*, *Texture sliding*, *Image jitter*, *Line boil*; principle 6; [`boil-and-painted-texture-continuity.md`](../corpus/guides/boil-and-painted-texture-continuity.md).

## Vocabulary

This seat's words are rows of [the glossary](glossary.md), which every pass carries after this manifest, with each row's definition, field terms and sources, which seats share it, and the four naming rulings. This seat's rows, in learning order: *Cut*, *Match cut*, *Line boil*, *Image jitter*, *Texture sliding*, *Texture continuity*, *J-cut and L-cut*, *Compositing*, *Grade*, *Linear and output colour*, *Loudness*, *True peak* and *Sound layers*.

## Principles, in learning order

Learned after the rows above and before the guides. "Named, not read" means the canon title was not read and no copy is ingested.

1. **Cut for emotion first, then story, then rhythm.** Canon: Murch, *In the Blink of an Eye*, ch. 6 (ingested): the Rule of Six ranks a cut's reasons (emotion, story, rhythm, eye-trace, the screen's two-dimensional plane, three-dimensional space, weighted 51, 23, 10, 7, 5 and 4 percent) and gives them up from the bottom, emotion last, which is why the Director decides each cut and this seat only executes it. Where a cut falls is the same book's ch. 14–15: where the thought in the shot completes, at one of the shot's few branch points, marked in real time at full speed. How a cut is executed (the node, dynamic trimming, blink and fricative cuts) is in the ingested *Suddenly Something Clicked*, ch. 4 and 15. Carried by the conform and cut sections of [`resolve-finishing-and-delivery.md`](../corpus/guides/resolve-finishing-and-delivery.md), until "Cutting for emotion, with J and L cuts" is written.
2. **Design the film for sound from the start**, after Thom's 1999 essay. No guide yet; the row *Sound layers*, the story packet's "Room for sound" section and the *Suddenly Something Clicked* ingest's ch. 18 and 20 (reassociation, image–sound distance, withheld score) carry it until "Sound layers, designing for sound" is written.
3. **Keep layers few:** about two and a half of one kind, up to five spread from speech to music, after Murch on Transom. Canon: *Suddenly Something Clicked*, ch. 21 (ingested), which states the rule as at most two and a half per five-second moment, spread across the spectrum, and gives no five-layer figure; the "up to five" is Transom's. Same future guide; the row and the ingest carry it.
4. **Measure loudness against a written target:** −23 LUFS integrated, true peak at most −1 dBTP, short-term at most −18 LUFS for short-form, per EBU R 128 and R 128 s1, set by hand. Carried by the Resolve guide's loudness section.
5. **Correct, then grade, in linear light through the output transform.** Carried by the Resolve guide's grade section, stated there from the curriculum brief, until "Correct, then grade" is written.
6. **Check texture continuity in the composite:** no sliding, no undesigned flicker. Carried by [`boil-and-painted-texture-continuity.md`](../corpus/guides/boil-and-painted-texture-continuity.md).

## Technique

The starred guides by file. This seat owns one tool guide (under Application), checks the composite against a second, and reads a third for its audit.

- **Line boil and painted-texture continuity** — [`boil-and-painted-texture-continuity.md`](../corpus/guides/boil-and-painted-texture-continuity.md) — this seat checks what Art designed and the Animator moved: in the composite, through every push-in and pull-back, paint travels with its subject and line boil runs at Art's cadence; sliding and undesigned flicker are craft fails.
- **The animatic and staging** — [`animatic-and-staging.md`](../corpus/guides/animatic-and-staging.md) — read for the audit of the story packet: the sound layers begin with the animatic's scratch track, and the beats marked for sound need the frames to land.

Not yet written, so a topic for `thin_lane:` until it exists: **Cutting for emotion, with J and L cuts** (ready now; the Director reads; *In the Blink of an Eye*, ch. 6 and 14–15, holds the decision and the cut point, *Suddenly Something Clicked*, ch. 4 and 15, the cut's execution), **Sound layers, designing for sound** (ready now; the *Suddenly Something Clicked* ingest is in, so its depth can be drawn from ch. 18–21) and **Correct, then grade** (ready now); **Compositing in Fusion** is dropped, Fusion being closed; moving layers are the Animator's, in [`the-scene-by-script.md`](../corpus/guides/the-scene-by-script.md), and this seat stacks them in Resolve; read that guide's render and TC5 section for what crosses and how it is compared; **Foley, room tone, scratch tracks** (waits on a tier B source).

## Application

Last on the path, in the order the book-to-seat brief set: the beginner's guide, then the manual's Edit, Fusion, Color, Fairlight and Deliver parts. This seat operates the Resolve delivery project alone; the Animator's scene arrives as its CPU renders plus the `.blend`. Fusion is closed for every seat, so the manual's Fusion part is background only. Resolve's API sets fixed values (opacity, blend modes, position, zoom, crop, rotation, the grade) and cannot keyframe them: this seat stacks, cuts, grades and delivers.

- **Resolve finishing and delivery** — [`resolve-finishing-and-delivery.md`](../corpus/guides/resolve-finishing-and-delivery.md) — owned: before the conform, before the grade, before the mix and before every delivery; the six technical checks, the loudness record with the targets set by hand, the save-reopen-render comparison, and the scripting calls that are known to fail while the application is busy.
- **Blackmagic's beginner's guide, then the manual's five parts** — no guide beyond the one above; all rights reserved, read on the page — the application chapters, as the brief ordered them.
- **The Resolve scripting documents shipped with the installed application** — cited in the Resolve guide — render settings, project colour management, the audio-normalise call whose default is not the target.
- `ffmpeg` with `ebur128` and `loudnorm`, `ffprobe`, `color-motion` and `beat-sync-editing` are toolbelt ([seat file](../bench/finishing-sound-designer.md#toolbelt)), not corpus.

## Audit duty: the story packet

This seat audits the Director's packet before the story gate (stake: *can this animatic be finished into the film it promises?*): pace, room for sound, and buildability within the limits. Lean on the staging guide above, and look for what the curriculum brief says a reviewer should see in boards and an animatic:

- every panel names its beat and what changes;
- each panel marks one focal point;
- screen direction agrees across cuts, or the crossing is motivated;
- the animatic runs full length with scratch sound, and holds are timed in frames;
- camera moves are named push-in, pull-back, pan or track;
- the story reads with the sound off, and the muted copy is there to prove it.

A craft fail is pinned to a panel or a frame in these rows of [the glossary](glossary.md): *Visual storytelling*, *Beat*, *Shot and sequence*, *Staging*, *Shot size*, *Screen direction*, *Animatic*, *Layout* and *Camera move*, beside *Cut* and *Match cut*, which this seat shares.

## Free layer

The free sources this seat's rows, principles and guides draw on, with the licence as the book-to-seat brief saw it on 2026-10-17 and what has become of each. `read-only` is a page a person reads; `open` is a licence that would allow an ingest, none made yet. "Carried by" names the guide that cites the source; "none yet" means a page with no guide behind it, so a decision leaning on it names the page.

| Source | Teaches | Licence, where seen | Status | Carried by |
|---|---|---|---|---|
| EBU R 128 (v5.0) and R 128 s1; EBU Tech 3341 to 3343; ITU-R BS.1770-5 | the loudness target, the tolerance, true peak, short-form, no loudness range under a minute | free downloads, licence not checked; ITU all rights reserved | read-only | the Resolve guide |
| FFmpeg filters documentation: `loudnorm`, `ebur128` | measuring, and the defaults that do not match the target | project documentation, licence not checked | read-only | the Resolve guide |
| Blackmagic's Resolve colour page and Fairlight page; the Resolve 20 and 21 guides and the Fusion guide | edit, colour, Fairlight, Fusion, deliver | all rights reserved | read-only | the Resolve guide (the two pages); the guides none yet |
| The Resolve scripting documents shipped with the installed application | render and project calls, the audio-normalise default | shipped with the application; read only, local | local, read-only | the Resolve guide |
| ACES documentation, output transforms | linear and output colour | CC BY 4.0 | open, not ingested | the Resolve guide |
| Meier 1996; the Paperman talk; Bénard 2010; Disney's SIGGRAPH 2024 page | texture continuity and its failures in the composite | all rights reserved, or the authors' and the Eurographics Association's | read-only | the texture guide |
| Thom, "Designing a Movie for Sound" (filmsound.org) | designing for sound from the start | © Randy Thom 1999, on a tier C host | read-only | none yet |
| Murch on Transom; Murch on Web of Stories, segments 293 to 295 | sound layers; emotion first | no terms stated; automatic captions | read-only | none yet |
| Yale Film Analysis, editing and sound; Adobe's J-cut and L-cut page | cuts, split edits, sound bridges | no licence stated; Adobe's | read-only | none yet |

## Canon

Two titles on this lane are ingested, both 2026-10-19: Murch, *Suddenly Something Clicked*, under `../corpus/books/suddenly-something-clicked/`, and Murch, *In the Blink of an Eye*, under `../corpus/books/in-the-blink-of-an-eye/`. Every other canon title stays "named, not read" until its own ingest lands there on its own ticket.

- **Murch, *Suddenly Something Clicked* (2025)** — the seat's primary: picture rhythm, sound design and mixing in one volume. Ingested: [`books/suddenly-something-clicked/`](../corpus/books/suddenly-something-clicked/). Cheatsheet first; ch. 21 (encoded and embodied sound, the Rule of Two and a Half, premix order) and ch. 19 (dialogue as the reference level, headroom, room translation) are the core for the mix; ch. 18 and 20 for designing for sound; ch. 24 and 27 for dialogue replacement and reverb; ch. 4 and 15 for executing a cut. Its figures are described, not stored; its linked clips were not watched or heard. Its levels are theatre sound-pressure readings, not LUFS, so principle 4's target stands.
- **Murch, *In the Blink of an Eye* (2nd ed., 2001)** — the emotion-first cut. Ingested: [`books/in-the-blink-of-an-eye/`](../corpus/books/in-the-blink-of-an-eye/). Cheatsheet first; ch. 6 (the Rule of Six) is the core; ch. 14–15 for where a cut falls (the blink, branch points, out-points marked at speed, cutting rate); ch. 7 and 17 for judging pace against screen size and image detail (paper figures beside the monitor); ch. 13 for reading a screening (referred pain). It is about live-action editing, with coverage and dailies this film does not have, so its applications here are marked as the corpus's; its Afterword's 2001 machines are history. It also survives as audio, on the reading path.

## Reading path

Corpus states are as of the `updated:` date in the header. Format and audio facts are the book-to-seat brief's, checked 2026-10-17.

| # | Title | Read this when | Format | Audio | Corpus |
|---|---|---|---|---|---|
| 1 | ACES getting-started pages | first on this path: the colour vocabulary | web | — | open, not ingested |
| 2 | Blackmagic's beginner's guide to Resolve | the application's vocabulary | PDF | — | read-only |
| 3 | Murch, *Suddenly Something Clicked* (2025) | the seat's canon, after the vocabulary: rhythm, sound and the mix in one book | Apple Books ebook, screen-captured and ingested on Sean's word | none found | ingested |
| 4 | Thom, "Designing a Movie for Sound" (1999) | principles: sound planned from the start | web | — | read-only |
| 5 | Murch on Transom | principles: how many layers a listener can follow | web, with audio | by ear | read-only · listen |
| 6 | EBU R 128 and R 128 s1 | the target and true peak, before the first mix | PDF | — | read-only |
| 7 | Murch, *In the Blink of an Eye* (2001) | the emotion-first idea, as audio if preferred | Apple Books ebook, screen-captured and ingested on Sean's word | unabridged, read by Chris Brinkley, 3 hours 48 minutes (Apple); optional | ingested |
| 8 | The Resolve manual: Edit, Fusion, Color, Fairlight, Deliver | the application chapters, last | PDF | — | read-only |
| 9 | Van Hurkman, *Color Correction Handbook* (2nd ed.) | when the first grade shows a need the free colourist guide does not meet (Sean's ruling, 2026-10-17) | EPUB and PDF, unlocked (InformIT) | — | on hand, not ingested |
| 10 | Murch on Web of Stories 293 to 295, 13 minutes; Bancroft Brothers, editing with Tom Scott, 78 minutes; Twenty Thousand Hertz, "Inside Movie Soundtracks", 15 minutes, then Murch's Krotos interview, 28 minutes; Tonebenders 231 on sound for feature animation, 41 minutes; Twenty Thousand Hertz, "The Loudness War", 32 minutes | the listening order's finishing items, in sessions under an hour | audio | by ear | listen |

### Next

- None held in reserve. Van Hurkman, the brief's one optional extra for this seat, is on the path above.
