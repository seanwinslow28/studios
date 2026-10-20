# Delivery package template — the finished film and its check record

Owned by the **Finishing and Sound Designer** ([seat file](../bench/finishing-sound-designer.md)), the accountable integrator. Stage 4 of a full train: the conformed cut with each cut's reason, the composite, the grade (corrected, then graded to one written look), the sound plan, the mix, the delivery package, and the **technical check record** on the quality bar's six checks (SWCB #159) plus the loudness record. Audited by the **Animator** before the technical checks are read and Sean gives or withholds his artistic yes. Header fields per [artifact-header.md](artifact-header.md); written to `artifacts/delivery-package.md`. The Resolve project, every render and every still live in the version folder under the media folder's `finish/`, cited here by path and sha256.

This seat executes the Director's cut, frame for frame. The six checks pass or fail; whether the film is good is Sean's yes, never this record's.

```markdown
---
id: mc-eng-001.finish
engagement: <project>-<YYYY-MM-DD>
date: 2026-10-28
seat: finishing-sound-designer
stage: 4
model: claude-opus-5-5             # a mechanical conform or check run may name claude-sonnet-5-5 here, with why
grounding: full
thin_lane: []
adjacent_lanes: []
version: finish-vNN-<YYYY-MM-DD>
version_path: "media:<film>/<project>-<YYYY-MM-DD>/finish/finish-vNN-<YYYY-MM-DD>"
version_sha256: <sha256>
prior_version: none
prior_note: none
exit: none                         # or "Blocked: needs source", "Blocked: budget", …
revision: 1
stale_from: null
status: draft
auditor: animator
audit: pending
story: mc-eng-001.story            # the animatic every cut comes from
motion: mc-eng-001.motion          # the scene record conformed, by its latest filed revision
frame_rate: 24
frames: <n>
delivery: "master: mov, prores 422 hq, 1920x1080, 24 fps, pcm 48 kHz 24-bit stereo; web: mp4, h.264 high, 1920x1080, 24 fps, aac 48 kHz stereo 320 kb/s"   # source-contract.md § 8; an exercise names its source's settings
---

## Conformed cut

Every cut from the animatic, each with its reason from the Director's panel list. This seat never trims, extends or re-times on its own judgement.

| Cut | Out of | Into | Frame in the cut | Frame in the animatic | Reason, from the animatic |
|---|---|---|---|---|---|
| CUT<n> | SH<n> | SH<m> | | | |

Every duration matches the animatic, or the row is a loopback to the Director with frames, listed under Deviations.

## Composite

Each layer composited, from which version, and how. A layer that does not composite goes back to its owner with the frame (`exit: "Blocked: needs source"`).

| Element | From | File | sha256 | How composited |
|---|---|---|---|---|
| L<n> | mc-eng-001.motion | | | |

## Grade

**The written look**, one sentence, written before grading started: <the look>.

Correction first, then the grade to that look. Colour design is Art's; the grade keeps it.

| Step | What was done | Before still | After still |
|---|---|---|---|
| Correction | | `media:…/finish/finish-vNN-<date>/stills/<file>` | |
| Grade | | | |

## Sound plan

Every sound has a moment and a reason; silence is a choice and is planned too. Texture and accents only: a score, a voice or dialogue routes out under the master skill's sound reopen rule.

| Moment | Frames | Layers | Reason | Answers |
|---|---|---|---|---|
| SP<n> | <a>–<b> | | | SN<n> from mc-eng-001.story, or none |

**Cues to generate**, when a layer is a generated sound: one row per cue, its prompt word for word, and the same cues as `cues.json` in a `sound-plan-vNN-<date>` version folder in `finish/`, in [the sound doorway's form](../launcher/README.md#the-sound-doorway). Sean approves the list in one decision; the doorway sends only cues from its approved copy, as worded there.

| Cue | Moment | Tool | Prompt | Takes kept |
|---|---|---|---|---|
| FX<n> or MU<n> | SP<n> | effect (ElevenLabs) or music (Lyria, its model) | | `media:…/finish/<version>/<file>`, sha256 |

## Mix

The mix is Resolve clip levels plus an ffmpeg filter file (limiter, fades, loudness to −23 LUFS), saved with the version so it repeats exactly; no seat mixes by hand.

| What | Path | sha256 |
|---|---|---|
| The mixed sound | `media:…/finish/finish-vNN-<date>/<file>` | |
| The filter file | `media:…/finish/finish-vNN-<date>/sources/<file>` | |
| The command that ran it | pasted below | |

Clip levels set in Resolve, by clip, and the filter command, pasted:

## Delivery package

| What | Path | sha256 |
|---|---|---|
| Delivery file | `media:…/finish/finish-vNN-<date>/delivery/<file>` | |
| Resolve project export | | |
| Scratch or placeholder material left out | `none`, or what and where | |

## Technical check record

The six technical checks of the quality bar, by row, each with the command or method and its output pasted or saved to `evidence/`. A check that could not run is a fail, never a skip. A known technical defect is never accepted in the final film.

| Check | What it asks | Command or method | Output | Passes? |
|---|---|---|---|---|
| TC1 | Complete playback: the whole export plays, with its intended opening and ending | `ffmpeg -v error -i <file> -f null -`, then a full-speed play | `evidence/tc1-<version>.txt` | |
| TC2 | Picture integrity: no unintended black frames, freezes, flicker, missing elements, broken edges or export artifacts | `blackdetect` and `freezedetect` over the file; frame review at the flagged frames | `evidence/tc2-<version>.txt` | |
| TC3 | Text and framing: any text readable at viewing size; nothing cropped or hidden | frames at viewing size, by shot | | |
| TC4 | Audio integrity: no clipping, clicks, cutoffs, unintended gaps or sync errors; accents land on their frames | `ebur128` true peak; each `SP<n>` checked at its frame | | |
| TC5 | Source integrity: the project opens with every asset and font; the export matches the approved version; every version in the chain has its manifest | the save, reopen and render comparison below, by [source-contract.md § 7](source-contract.md#7-tc5-save-reopen-and-render-again) | | |
| TC6 | Delivery compliance: resolution, frame rate, format and audio meet the delivery targets ([source-contract.md § 8](source-contract.md#8-delivery-targets)), on each delivered file | `ffprobe` against `delivery:` in the header | | |

**Loudness record**, set by hand, never `loudnorm`'s defaults (−24, −2, which fail):

| Measure | Target | Measured | Holds? |
|---|---|---|---|
| Integrated | −23 LUFS | | |
| Short-term, highest | at most −18 LUFS | | |
| True peak | at most −1 dBTP | | |

No loudness-range figure on a film under a minute.

~~~
ffmpeg -nostats -i <delivery file, full path> -af ebur128=peak=true -f null -
<summary block, pasted>
~~~

**Frames, rate and duration** from `ffprobe`, pasted, against the scene record and the animatic. A mismatch is a technical fail before any look is judged.

**Save, reopen and render comparison:** the project saved, reopened in a fresh session, rendered again; the two renders compared frame by frame by [the source contract's commands](source-contract.md#7-tc5-save-reopen-and-render-again), output pasted, with the count of frames that differ and the largest difference. Any frame that differs is a technical fail until its cause is found.

## Renders and caches deleted

Only render caches this seat made inside its own finish folders, only to stay under the storage limits. Never a version folder, an input, an approved copy or another seat's file.

| What | Path | Size | Why |
|---|---|---|---|

`none` when nothing was deleted.

## Deviations

| Id | Upstream line | What was done instead | Why |
|---|---|---|---|
| DV<n> | | | |

## Decisions

| Choice | Over | Because | Canon |
|---|---|---|---|

## Questions for Sean

Whether the film is good is Sean's yes. Taste calls on the grade or the sound are written here as questions and never ruled.

| Id | Question | Frames | The seat's recommendation |
|---|---|---|---|
| Q<n> | | | |

## Moves

<!-- MACHINE-READ by the rung-0 checker (craftwork/trace/check.py): move lines only, one per line,
     per artifact-header.md § The closing sections. A note goes in the pass record's ## Notes. -->

- kept — SH<n>–SH<m> from mc-eng-001.story
- kept — MV<n>–MV<m> from mc-eng-001.motion
- split — SN<n> → SP<n>, SP<m> from mc-eng-001.story

meter: <runtime> · <tokens> · <wall-clock>
```

**What attacks this package:** the Animator's audit, on its stake in [the seat file](../bench/animator.md#audit-duty) (*did the motion survive finishing?*). No gate anchors here: the six technical checks above and Sean's artistic yes close the film.
