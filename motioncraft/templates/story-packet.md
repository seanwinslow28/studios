# Story packet template

Owned by the **Visual Story Director** ([seat file](../bench/visual-story-director.md)). Stage 1 of a full train: the treatment, the beat sheet, the boards, the timed animatic with scratch sound, the shot list and the muted copy. The animatic is the anchor of the **story gate**, and the first version of the finished film: every duration and every cut in the engagement comes from it. Audited by **Finishing and Sound** before the story gate. Header fields per [artifact-header.md](artifact-header.md); written to `artifacts/story-packet.md`. Boards, the animatic and its copies live in the version folder under the media folder's `story/`, cited here by path and sha256.

The packet says *how the film is staged and timed*. What it is about arrives with the brief, and every word in it is Sean's or Scriptcraft's.

```markdown
---
id: mc-eng-001.story
engagement: <project>-<YYYY-MM-DD>
date: 2026-10-20
seat: visual-story-director
stage: 1
model: claude-opus-5-5
grounding: pending
thin_lane: []
adjacent_lanes: []
version: animatic-vNN-<YYYY-MM-DD>
version_path: "media:<film>/<project>-<YYYY-MM-DD>/story/animatic-vNN-<YYYY-MM-DD>"
version_sha256: <sha256>
prior_version: none
prior_note: none
exit: none
revision: 1
stale_from: null
status: draft
auditor: finishing-sound-designer
audit: pending
intake: brief.md                   # the brief, plus the approvals entries it names
frame_rate: 24                     # the working frame rate; every frame count here is at this rate
total_frames: <n>                  # the animatic's length in frames
---

## Intake

What arrived: Sean's idea, or a locked script or beat sheet from Scriptcraft under its binding. Every brief line (`ASK<n>`) maps to a beat, a routed question or an out-of-scope line. Nothing is dropped silently. Cite by id; never restate.

| Brief line | Becomes | Note |
|---|---|---|
| ASK<n> | B<n>, B<m> | |
| ASK<n> | Q<n> | a what-call for Sean, below |

## Treatment

The film in one paragraph: what the viewer sees happen, in order, and the one feeling it is staged for. Then its why-A-over-B and its canon line.

**Why this over that:** <chosen staging> over <strongest alternative>, because <reason>.
**Canon:** <title and idea, in your own words, "named, not read"> · or `none`.

## Beat sheet

Every beat names what changes. A beat where nothing changes is a hold, and its length is a choice made in the animatic.

| Beat | What happens | What changes | Needs a sound to land? | Words |
|---|---|---|---|---|
| B<n> | | | SN<n>, or no | none, or WP<n> |

## Boards

One focal point per panel, and a known place for the eye at every cut. Each panel names its beat and what changes. A rough from the Codex image path is labelled `generated rough` here and is reference for a drawn board, never the board.

| Panel | Beat | What changes | Focal point | Shot | File | sha256 | Drawn or generated rough |
|---|---|---|---|---|---|---|---|
| P<n> | B<n> | | one thing, named | SH<n> | `media:…/story/animatic-vNN-<date>/boards/<file>` | | drawn |

## Timed animatic

The boards played as a timed film over scratch sound, at the working frame rate. Holds are timed in frames, never "a beat" or "a moment". Camera moves are named push-in, pull-back, pan or track; zoom only for a lens change.

**Playback, full speed, with scratch sound:** `media:…/story/animatic-vNN-<date>/animatic.<ext>` · sha256 `<sha256>`
**Muted copy:** `media:…/story/animatic-vNN-<date>/animatic-muted.<ext>` · sha256 `<sha256>`
**Sequencer project:** Blender's sequencer, `media:…/story/animatic-vNN-<date>/sources/animatic.blend` · sha256 `<sha256>`, rendered through the doorway's render request (the call's id). It is this seat's own file, never Finishing's delivery project and never the Animator's scene.

**Panel list in frames:**

| Panel | In frame | Out frame | Frames | Hold? | Camera move | Cut out of it, and why there |
|---|---|---|---|---|---|---|
| P<n> | | | | no | none \| push-in \| pull-back \| pan \| track | |

The frame counts sum to `total_frames:` in the header. A mismatch is a technical fail in this packet before anything else is read.

**Scratch sound:** the scratch timing track, made in the sequencer file by Blender's own sound module: tones, clicks and silence marking beats, hits and where music swells, at which frames. Labelled scratch, so it never reaches the delivery file; no generated sound and no spend. Sound the seat cannot make there is for Finishing, after Sean approves the cue list.

| Mark | Frame | What it marks | Tone, click or silence |
|---|---|---|---|
| T<n> | | beat \| hit \| swell | |

**Sean's guide recording:** `none`, or his own hummed or spoken guide, by path and sha256, counted as his own recording and placed on its own strip.

**Muted reading:** one sentence on what the muted copy reads as, start to finish. The story reads with the sound off, or this sentence says where it does not.

**Probe, pasted:** the `ffprobe` command and its output for the playback file (frames, rate, duration), so the panel list's sum is a measurement, not a claim.

## Shot list

Staging and camera for every shot. Shot size is named by the subject in frame, since "medium" has no fixed size.

| Shot | Panels | Shot size (by the subject) | Staging: where the subject is, where it goes | Camera | Screen direction | Enters and exits |
|---|---|---|---|---|---|---|
| SH<n> | P<n>–P<m> | | | none \| push-in \| pull-back \| pan \| track | left to right | |

Screen direction agrees across cuts, or the crossing is motivated and the row says why.

## Room for sound

The moments that need a sound to land, for Finishing's sound plan. A score, a voice or dialogue is marked here as needed and routes out under the master skill's sound reopen rule; this seat never writes one.

| Mark | Beat and frames | What the sound must do | Texture or accent | Routes out? |
|---|---|---|---|---|
| SN<n> | B<n>, frames <a>–<b> | | accent | no |

## Words

Every on-screen or spoken word is Sean's, or Scriptcraft's once it exists. A placeholder is marked and never shipped (never-do 10). A word change this seat needs goes back on the brief's return line.

| Mark | Where | Placeholder text, marked as one | Whose word it waits for |
|---|---|---|---|
| WP<n> | P<n> | | Sean |

`none` when the film has no words.

## Generated roughs

Every rough from the Codex image path, by file, sha256 and the panel it informed, downloaded to the version folder on creation (never-do 13). `none` when none was made.

## Decisions

Choices made in staging and timing, one row each, filed by the coordinator as ledger entries in this seat's name.

| Choice | Over | Because | Canon |
|---|---|---|---|

## Questions for Sean

What-calls and taste calls this seat met and did not rule, one question each.

| Id | Question | Where it bites | The seat's recommendation |
|---|---|---|---|
| Q<n> | | P<n> | |

## Moves

<!-- MACHINE-READ by the rung-0 checker (craftwork/trace/check.py): move lines only, one per line,
     per artifact-header.md § The closing sections. A note goes in the pass record's ## Notes. -->

- split — ASK<n> → B<n>, B<m> from brief.md
- added — P<n>–P<m> from mc-eng-001.story
- added — SH<n>–SH<m> from mc-eng-001.story

meter: <runtime> · <tokens> · <wall-clock>
```

**What attacks this packet:** Finishing's audit, on its stake in [the seat file](../bench/finishing-sound-designer.md#audit-duty) (*can this animatic be finished into the film it promises?*), and the story gate, on the gate schedule's list for the story packet.
