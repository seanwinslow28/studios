# Directed-revision template — Sean's one change, and the three held checks

A **directed revision** is Sean's one change to a passed moving test, proving the work revises at its source (SWCB #159: one timing or shape change, made in the editable source, then exported again). It is never a repair: a repair answers a reviewer, a directed revision answers Sean, and the two are never mixed into one pass. At most one repair and one directed revision per exercise or moving test (brief 5, section 3). It follows the motion gate's PASS, and it is the second half of that gate's anchor.

Two records, one per half:

| Half | Id | File | Writer | When |
|---|---|---|---|---|
| The form | `<eng>.revision` | `artifacts/directed-revision.md` | the coordinator, from Sean's words, verbatim | after Sean plays the passed version at full speed and names the change |
| The held checks | `<eng>.revision-check` | `audits/revision-check.md` | the motion gate's second pass, on the vendor that did not write the revision (a fresh-context Opus 5.5 when the Animator revised on Codex), read-only | after the Animator's revision is filed as `artifacts/scene-record-r2.md` |

The Animator's revision is a `repair` pass at stage 3, with `triggered_by` naming the motion gate's pass. It writes a new version folder and fills the scene record's **Directed revision** section ([scene-record.md](scene-record.md)). Which recorded pass files the form, so the hash chain holds it, is the master skill design's to rule; until then the coordinator files it once and never edits it.

## The form

```markdown
---
id: mc-eng-001.revision
engagement: <project>-<YYYY-MM-DD>
date: 2026-10-27
seat: coordinator
stage: 3
kind: directed-revision
revises: mc-eng-001.motion         # the passed version's artifact
revises_version: motion-vNN-<YYYY-MM-DD>
gate: mc-eng-001.motion-gate       # the gate pass it follows
approvals_entry: mc-eng-001.a<n>   # Sean's decision on the passed version, where his words are kept
---

## The change

One sentence, one change, named by pose, frame range and direction, with what stays.

| Revision | Sean's sentence, verbatim | Pose | Frame range | Direction | What stays |
|---|---|---|---|---|---|
| DR<n> | "At the first rebound, frames <a> to <b>, slow into the peak by two more frames; keep the contact and the rest unchanged." | the first rebound's peak | <a>–<b> | slow into the peak, +2 frames | the contact, the rest, every frame before <a> |

A sentence that names two changes is two revisions, and only one is allowed: the coordinator asks Sean which, and records his pick. A change that needs a new pose is not a directed revision: it goes back to Art, and to the appearance gate if it is a material design change.

**Declared shift:** the number of frames every drawing after the range moves by, from the sentence: `+<n>`, `−<n>` or `0`.
```

## The held checks

The revision held when all three pass. Each is decided by a measurement, so a failed check is a technical fail.

```markdown
---
id: mc-eng-001.revision-check
engagement: <project>-<YYYY-MM-DD>
date: 2026-10-28
seat: motion-gate
kind: gate
stage: 3
gate: MOTION
anchor: mc-eng-001.motion          # the revised record, by its filed file
anchor_file: artifacts/scene-record-r2.md
anchor_sha256: <sha256>
anchor_version: motion-vNN-<YYYY-MM-DD>   # the revision's version folder
prior_version: motion-vNN-<YYYY-MM-DD>    # the passed version it revises
revision: mc-eng-001.revision
anchor_last_written_on: codex
vendor: claude-opus-5-5
vendor_switch: none
inputs: [mc-eng-001.revision, mc-eng-001.motion, mc-eng-001.motion-gate, mc-eng-001.appearance]
verdict: MOTION PASS — QUALITY VERDICT ONLY
ledger_entry: mc-eng-001.d<n>
---

## Verdict line

`MOTION PASS — QUALITY VERDICT ONLY` when all three checks hold; `MOTION FAIL — QUALITY VERDICT ONLY` when any does not. Then **Means** and **Does not mean / Next**. A held revision is never an approval: the revised version goes to Sean with its id, its status and his prior note, and his decision is recorded in the approvals ledger.

## The limit of this review

This is a review of decoded frames, not a real-time viewing. Whether the change reads right at speed is Sean's.

## Check 1 — the named frames changed as named

The named frames show the named change, in the named direction, in before and after frames and timing charts.

| Revision | Range | Before frames and chart | After frames and chart | Change as named? |
|---|---|---|---|---|
| DR<n> | <a>–<b> | | | yes |

## Check 2 — nothing else moved

Frames before the range match the prior version pixel for pixel. Frames after it are the same drawings, shifted by the declared count. The command and its output, pasted: a per-frame comparison of the two renders, before the range at the same frame numbers, after it offset by the shift.

~~~
<comparison command, paths in full>
<output, pasted: frames compared, frames that differ>
~~~

| Span | Frames compared | Offset | Frames that differ | Holds? |
|---|---|---|---|---|
| Before the range | 1–<a−1> | 0 | 0 | yes |
| After the range | <b+1>–<end> | declared shift | 0 | yes |

## Check 3 — everything that passed still passes

Every criterion the passed version met still holds, and the master layers' checksums are unchanged. One row per criterion from the motion gate's record and the motion audit, re-read on the revised frames; then the masters.

| Criterion | Where it passed before | On the revision | Holds? |
|---|---|---|---|

| Master | sha256 at approval | sha256 now | Unchanged? |
|---|---|---|---|

## Findings

A failed check is a finding, technical fail, CRITICAL. A defect the revision did not touch is outside this record: it is a gate residual, named here and carried to Sean as a candidate acceptance, never a loopback.

| Id | Kind | Severity | Check | Frames | Finding |
|---|---|---|---|---|---|
| F<n> | technical fail | CRITICAL | 2 | | |

meter: <runtime> · <tokens> · <wall-clock>
```
