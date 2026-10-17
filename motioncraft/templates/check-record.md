# Check record template — the four audits

The artifact of an **audit** pass: what the auditing seat saw, what it attacked, what held, and what goes back. Motioncraft has no co-signs, so every check record is one of the four audits in the closed cycle, Director → Art → Animator → Finishing → Director, the arrow reading "audits". Written by the fixed auditor in a fresh-context invocation that receives artifacts only, never the drafting conversation. On Productcraft's shape ([productcraft/templates/check-record.md](../../productcraft/templates/check-record.md)) as Devcraft adapted it ([devcraft/templates/check-record.md](../../devcraft/templates/check-record.md)); the convergence rules are shared law, [craftwork § Checks converge](../../craftwork/law.md#checks-converge-and-the-ladder-has-brakes).

| Id | Auditor | Checks | Runs | Stake (from the seat file) |
|---|---|---|---|---|
| `<eng>.audit-story` | finishing-sound-designer | the story packet | after the Director's draft, before the story gate | *Can this animatic be finished into the film it promises?* |
| `<eng>.audit-appearance` | visual-story-director | the appearance packet | after Art's draft, before the appearance gate | *Does this look stage the boards?* |
| `<eng>.audit-motion` | art-pose-designer | the scene record and its evidence pack | after the Animator's draft, before the motion gate | *Is this still the subject Sean approved, in every frame?* |
| `<eng>.audit-finish` | animator | the delivery package and its check record | after Finishing's draft, before Sean's yes; a read-only Codex pass | *Did the motion survive finishing?* |

An audit never edits the checked artifact or its files: a material finding is a loopback to its drafting seat, and one repair round per artifact per check is the cap. The coordinator transcribes the verdict into the checked artifact's `audit:` field and into the pass record's `checks`. The Animator's audit is a Codex pass, so its record is the pass's final message, filed by the coordinator byte for byte. Header fields per [artifact-header.md](artifact-header.md); written to `audits/audit-<slug>.md` once. A Claude auditor drafts it in its scratch folder and copies it there as its last write (seat preamble).

**Three finding kinds, never a fourth.** A **technical fail** is decided by a measurement: a checksum, a probe, a frame count, a loudness figure, or evidence that is missing. A **craft fail** is a glossary term and a frame number, such as squash missing the contact frame. A **taste call** is neither: whether it is beautiful, alive, or the film Sean wants. It is written as a question for Sean and never ruled. A missing piece of the evidence pack is a technical fail and is checked first, since nothing else can be judged without it.

```markdown
---
id: mc-eng-001.audit-motion
engagement: <project>-<YYYY-MM-DD>
date: 2026-10-25
seat: art-pose-designer            # the auditing seat
kind: audit
stance: first-sight                # first-sight | verify; a verify pass is round two
stage: 3                           # the checked artifact's stage
model: claude-opus-5-5
grounding: full
checked: mc-eng-001.motion         # the artifact id checked, and its revision or filed file
checked_revision: 1
checked_version: motion-vNN-<YYYY-MM-DD>   # the version folder the evidence lives in
stake: "Is this still the subject Sean approved, in every frame?"
verdict: AUDIT LOOPBACK — 1 material
---

## Verdict line

One of: `AUDIT CLEAN — stake held` · `AUDIT LOOPBACK — <n> material` · `AUDIT NOTES ONLY`. Then **Means**, then **Does not mean / Next**, per the shared [status vocabulary](../../craftwork/templates/status-vocabulary.md). An audit verdict is never a gate verdict and never an approval.

## The limit of this review

This is a review of decoded frames, not a real-time viewing. Felt weight, snap and timing at speed go to Sean's playback and are not passed here.

## Evidence present

First, before anything is judged: each field the checked artifact's template requires, present or missing, with its sha256 re-taken. A missing field is a technical fail, CRITICAL, and stops the craft reading for that field.

| Field | Path | sha256 in the artifact | sha256 now | Present and matching? |
|---|---|---|---|---|
| Full-speed playback | | | | yes |

## The stake, worked

The table for this audit's stake. Each row is evidence the auditor opened or ran, never a reading of the author's summary.

- **audit-story:** one row per shot and per hold, read for pace (holds in frames that land, cuts that do not crowd a beat), room for sound (each `SN<n>` has the frames it needs), and buildability (every shot can be made, composited and delivered inside the limits, its camera named). An animatic that reads but cannot be built inside the limits is material.
- **audit-appearance:** one row per key and per panel: the key reads in the panel it serves, at its size and against its background; the silhouettes read in the boarded framing; the value study puts the eye where the board does; colour carries the beat order. A packet that stages a different film from the boards is material.
- **audit-motion:** one row per contact, transformation and smear, against the appearance packet alone: identity holds through every pose (each `MN<n>`), volume holds through squash and stretch, the designed silhouettes appear where the plan puts them with none repeated or assembled from pieces, each smear lands on its listed frames and arc, and paint moves with the subject.
- **audit-finish:** one row per contact frame and per hold in the scene record, found again in the delivered cut at its frame after compositing, grading and the edit; no cut trims an anticipation, a contact or a settle; frame rate and duration match. Each finding names the frame in both versions.

| Row | What was checked | Evidence opened or command run | Holds? |
|---|---|---|---|
| CT<n> | squash on the contact frame, area within the plan | `media:…/evidence/adjacent/CT<n>/`, frames <f−2>–<f+2> | yes |

## Findings

One row per finding. Every finding names its kind, and a craft fail names its glossary term and its frames. Severity follows the kind (brief 5, section 2): a **technical fail** is **CRITICAL**, since nothing else can be judged without it; a **craft fail** is **MATERIAL**, or **CRITICAL** when it is one of the fail conditions Sean has already named for the exercise or the shot; a **NOTE** is a craft observation that does not fail the stake. Both CRITICAL and MATERIAL loop back. A taste call has no severity and is not a row here.

| Id | Kind | Finding | Artifact, section and frames | Glossary term | Severity | Evidence | What would pass |
|---|---|---|---|---|---|---|---|
| M<n> | craft fail | | mc-eng-001.motion § Contacts, frames <a>–<b> | squash | MATERIAL | | |
| M<n> | technical fail | | mc-eng-001.motion § Technical record | — | CRITICAL | | |
| N<n> | craft fail | | | arc | NOTE | | |

## Questions for Sean

Taste calls, written as questions, unruled. `none` when there are none.

| Id | Question | Frames |
|---|---|---|
| Q<n> | | <a>–<b> |

## What was attacked and held

Being unable to find a defect is a finding: name what was attacked, how, and why it held. Empty is a defect.

## Loopback

The one message to the drafting seat: which rows, what frames, what evidence, what would pass. `none` on a clean audit.

## Verification (`stance: verify` only; omit the section entirely on a first-sight check)

Round two is a verification pass, not a fresh audit. It runs on the vendor that did not write the repair, read-only, so its record is the pass's final message. Exactly three duties:

1. **Rule each repair** `holds` or `residual`, one row per first-sight finding, in its original numbering.
2. **Attack the frames and text the repair changed**, and those only. A defect found outside them is a **gate residual**, carried to the next gate as a candidate acceptance, never a loopback.
3. **Stop.**

| Id | First-sight finding | Repair | holds \| residual | If residual: what still fails, what would pass |
|---|---|---|---|---|
| M<n> | | | holds | |

| Outside the changed frames | Section | Severity | Carried to | Why it is not a loopback |
|---|---|---|---|---|

**The series line**, for the gate's check series table: `round <n> / <findings> findings / <frames or sections> changed`. A series that does not shrink is a question to Sean, never another round.

meter: <runtime> · <tokens> · <wall-clock>
```

**What attacks a check record:** the gates read every check record in scope, on the gate schedule's list for check records.
