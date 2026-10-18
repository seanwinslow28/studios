# Scene record template — the moving test and its evidence pack

Owned by the **Animator** ([seat file](../bench/animator.md)). Stage 3 of a full train, and the whole of a small piece: the moving test as an editable source plus its render, and the **evidence pack** that every motion claim ships with (never-do 2; brief 5, section 2). The anchor of the **motion gate**, with its one directed revision ([directed-revision.md](directed-revision.md)). Audited by **Art and Pose** before the gate. Header fields per [artifact-header.md](artifact-header.md). "Scene" here is the application's word for the editable file (Blender's scene, a Fusion composition), the one use the naming rulings allow; a piece of the film is a shot.

**This record is the pass's final message.** The Animator runs on Codex, so the launch form's `-o` saves the final message and the coordinator files it as `artifacts/scene-record.md`, byte for byte; a repair or a directed revision is filed as `artifacts/scene-record-r2.md`. Write it as one message: the frontmatter first, then the sections, no preamble and no sign-off. The moving test, its render and every evidence file live in the version folder under the media folder's `motion/`, cited here by path and sha256. Commands are pasted with their exact output; a field with no pasted output is a claim, and a claim is not evidence.

```markdown
---
id: mc-eng-001.motion
engagement: <project>-<YYYY-MM-DD>
date: 2026-10-24
seat: animator
stage: 3
model: codex gpt-6.1-sol high
grounding: full
thin_lane: []
adjacent_lanes: []
version: motion-vNN-<YYYY-MM-DD>
version_path: "media:<film>/<project>-<YYYY-MM-DD>/motion/motion-vNN-<YYYY-MM-DD>"
version_sha256: <sha256>
prior_version: none
prior_note: none                   # Sean's note on the prior version: its approvals entry id, quoted in § Version below
exit: none                         # or "Blocked: appearance not approved", "Blocked: budget", …
revision: 1
stale_from: null
status: draft
auditor: art-pose-designer
audit: pending
story: mc-eng-001.story            # the animatic the timing comes from
appearance: mc-eng-001.appearance  # the appearance packet moved; none on a small piece with no packet
appearance_gate: mc-eng-001.appearance-gate   # the gate pass this motion follows on a full train; none on a small piece
directed_revision: none            # on a revision: the form's id, mc-eng-001.revision
frame_rate: 24                     # the working frame rate
frames: <n>                        # the moving test's length in frames, as the animatic gives it
viewing_size: 1920x1080
---

## Version

The three things never-do 14 requires, before anything else.

| Version id | Status | Sean's prior note |
|---|---|---|
| motion-vNN-<date> | draft, unreviewed | his words, verbatim, from approvals entry `mc-eng-001.a<n>`, or `none` |

**First Codex seat on visual work.** One line, on every pass until the master skill design rules otherwise: this pass ran on Codex as the first Codex seat on visual work in any studio, so its numbers are a first measurement.

## Source and render

| What | Application | Path | sha256 |
|---|---|---|---|
| Editable source | Blender \| Fusion (its own isolated project) | `media:…/motion/motion-vNN-<date>/source/<file>` | |
| Render | | `media:…/render/<file>` | |
| Exported composition, for Finishing (Fusion only) | | | |

A flattened render is not a source. A revision is made in the source.

## Playback

- **Full speed at the working frame rate:** `media:…/evidence/playback.<ext>` · sha256 `<sha256>`
- **Frame-numbered copy**, the frame number burned into every frame: `media:…/evidence/playback-numbered.<ext>` · sha256 `<sha256>`

The command that burned the numbers, pasted.

## Timing charts, move by move

One row per move, from key to key, in the appearance packet's poses. Name the pose and the direction ("slow into the rest", "fast out of the anticipation"), never bare "ease in". The chart is the spacing drawn frame by frame: positions per frame, or a chart image beside the row.

| Move | From → to | Frames | Spacing, in the pose-and-direction words | Chart |
|---|---|---|---|---|
| MV<n> | K<n> → K<m> | <a>–<b> | fast out of K<n>, slow into the peak | `media:…/evidence/charts/MV<n>.<ext>` |

## Contacts and transformations

Every contact and every transformation, with two adjacent frames either side of it, at viewing size. A contact or transformation with no row here is missing evidence, which is a technical fail before anything else is judged.

| Id | Frame | What happens | Frames shown | Files | Squash or shape change there |
|---|---|---|---|---|---|
| CT<n> | <f> | lands on the floor | <f−2>, <f−1>, <f>, <f+1>, <f+2> | `media:…/evidence/adjacent/CT<n>/` · sha256 `<sha256>` | squash on <f>, area within <n>% of rest |
| TF<n> | <f> | | <f−2>…<f+2> | | |

## Layer stack

Each painted layer the moving test uses, by file and checksum, against the appearance packet.

| Layer | File | sha256 now | sha256 in the appearance packet | Same? |
|---|---|---|---|---|
| L<n> | | | | yes |

## Technical record

**Probe**, pasted: frames, rate and duration from `ffprobe`, and the decode-error pass.

~~~
ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames,r_frame_rate,duration -of default=nw=1 <render, full path>
<output, pasted>
ffmpeg -v error -i <render, full path> -f null -
<output, pasted; empty means no decode errors>
~~~

| Measure | Expected (from the animatic) | Measured | Holds? |
|---|---|---|---|
| Frames | | | |
| Frame rate | | | |
| Duration | | | |
| Decode errors | none | | |

**Save, reopen and render comparison:** the source saved, reopened in a fresh session, and rendered again; the two renders compared frame by frame. The commands and their output, pasted, with the count of frames that differ. Any frame that differs is a technical fail.

## Optional evidence

Required when the brief names it (the seed-shape exercise asks for all five; the bouncing-ball exercise asks for the arc trace). Otherwise `not asked`, row by row, never left blank.

| Field | Path | sha256 | Asked by |
|---|---|---|---|
| Quarter-speed copy | | | |
| Arc trace over a stack of the frames | | | |
| Numbered silhouette sheet, every distinct drawing filled black, with how often each is exposed | | | |
| Crops at twice viewing size across each turn or tumble, for sliding paint | | | |
| Every readable frame of the subject beside the approved frame | | | |

## Directed revision (on a revision only)

Omit on a first draft. On the pass that answers a directed revision: the form's id and Sean's sentence, verbatim; the frames changed; the declared shift after the range, in frames; and the before-and-after frames and charts the held checks will read.

| Revision | Sean's sentence | Frames changed | Declared shift after the range | Before and after |
|---|---|---|---|---|
| DR<n> | | <a>–<b> | +<n> frames | `media:…/evidence/revision/` |

## Deviations

From the animatic or the appearance packet, each declared with its reason, or `none`. A move the approved poses cannot reach is a loopback to Art with frames, never a quiet redraw.

| Id | Upstream line | What was done instead | Why |
|---|---|---|---|
| DV<n> | | | |

## Decisions

Choices made in timing and spacing, one row each, filed by the coordinator as ledger entries in this seat's name.

| Choice | Over | Because | Canon |
|---|---|---|---|

## Questions for Sean

Felt weight and snap at speed are Sean's call at the motion gate, written here as questions and never ruled.

| Id | Question | Frames | The seat's recommendation |
|---|---|---|---|
| Q<n> | | <a>–<b> | |

## Moves

<!-- MACHINE-READ by the rung-0 checker (craftwork/trace/check.py): move lines only, one per line,
     per artifact-header.md § The closing sections. A note goes in the pass record's ## Notes. -->

- kept — K<n>–K<m> from mc-eng-001.appearance
- split — SH<n> → MV<n>, MV<m> from mc-eng-001.story
- added — CT<n>–CT<m> from mc-eng-001.motion

meter: <runtime> · <tokens> · <wall-clock>
```

**What attacks this record:** Art's audit, on its stake in [the seat file](../bench/art-pose-designer.md#audit-duty) (*is this still the subject Sean approved, in every frame?*), and the motion gate, on the gate schedule's list for the scene record. A missing evidence field is the first thing either one finds.
