# Appearance packet template

Owned by the **Art and Pose Designer** ([seat file](../bench/art-pose-designer.md)). Stage 2 of a full train: what the film looks like, in a form that can actually move. The style frame as separated painted layers, the pose and smear plan, colour design and model notes, the silhouette sheet, the greyscale value study, each new pose beside the approved frame, and the master layers' checksums. The anchor of the **appearance gate**, with Finishing's assembled frame attached as proof the layers animate; nothing moves before that gate on a full train. Audited by the **Visual Story Director** before the gate. Header fields per [artifact-header.md](artifact-header.md); written to `artifacts/appearance-packet.md`. Every layer, sheet and study lives in the version folder under the media folder's `appearance/`, cited here by path and sha256.

```markdown
---
id: mc-eng-001.appearance
engagement: <project>-<YYYY-MM-DD>
date: 2026-10-22
seat: art-pose-designer
stage: 2
model: claude-opus-5-5
grounding: full
thin_lane: []
adjacent_lanes: []
version: appearance-vNN-<YYYY-MM-DD>
version_path: "media:<film>/<project>-<YYYY-MM-DD>/appearance/appearance-vNN-<YYYY-MM-DD>"
version_sha256: <sha256>
prior_version: none
prior_note: none                   # the approvals entry id for the approved frame this packet builds beside, or none
exit: none
revision: 1
stale_from: null
status: draft
auditor: visual-story-director
audit: pending
story: mc-eng-001.story            # the story packet revision designed against
viewing_size: 1920x1080            # the size every still in this packet is judged at
edit_mode: unconfirmed             # confirmed | unconfirmed: the Codex image path's edit mode with a reference image
---

## Intake

What arrived, by id: the story packet's beats, panels and shots this packet designs for, and every approved frame in force.

**Approved frames in force:** one row per approval this packet must keep.

| Approvals entry | What Sean approved | Frozen copy | sha256 at approval |
|---|---|---|---|
| `mc-eng-001.a<n>` | | `media:…/approved/<version-id>/` | |

## Style frame as separated painted layers

Line, pigment and paper, each its own file, each with a rule for how it may change between drawings. The change rule names the effect: line boil, paper boil, pigment variation, or none. A layer that cannot change without the others is not separated.

| Layer | Kind | File | sha256 | Change rule between drawings |
|---|---|---|---|---|
| L<n> | line | `media:…/appearance/appearance-vNN-<date>/layers/<file>` | | line boil: redrawn every two frames, the shape held |
| L<n> | pigment | | | pigment variation within the shape; never slides over it |
| L<n> | paper | | | paper boil off; fixed to the subject, never to the screen |

**Why this over that:** <chosen layer split> over <strongest alternative>, because <reason>.
**Canon:** <title and idea, in your own words, "named, not read"> · or `none`.

## Pose and smear plan

**Key poses.** Every key reads as a solid black shape, with its line of action drawn over it. Two keys that share a silhouette are one key. Squash and stretch keys keep about the resting size.

| Key | Pose, named | Panel and shot it serves | Line of action | Area against the resting key | File | sha256 |
|---|---|---|---|---|---|---|
| K<n> | | P<n>, SH<n> | | within <n>% | | |

**Smears.** Each smear is a designed pose, listed by its frames, the keys it joins and its arc, never a blur left to a filter.

| Smear | Frames (from the animatic) | Joins | Arc | Kind (stretched, multiple, blur-shaped drawing) | File | sha256 |
|---|---|---|---|---|---|---|
| SM<n> | <a>–<b> | K<n> → K<m> | | | | |

## Colour design

The palette and its order, and how value and temperature carry the beat order. Colour design is this seat's; the grade is Finishing's, and keeps it.

| Beat | Palette (named) | Value: where the light is | Temperature | Why |
|---|---|---|---|---|
| B<n> | | | warm against cool | |

## Type

For a film that sets text: how its words look on screen. `none` when the film sets no text. The words themselves are Sean's or Scriptcraft's (the interim words rule); until they arrive, cards carry marked placeholders. Every face comes from the font shelf ([source-contract.md § 10](source-contract.md#10-the-font-shelf)); every size is judged at `viewing_size`, never zoomed. Terms are the glossary's type rows.

**Faces, cast by role.** One row per role the film uses.

| Role | Face, size cut and style | Designer and foundry | Shelf path | Why this over that | Canon |
|---|---|---|---|---|---|
| title | | | `media:fonts/<family>-<version>/<file>` | <this face> over <the strongest alternative>, because <reason> | |
| cards | | | | | |
| credits | | | | | |

**Sizes, on a gentle scale.** Few sizes, each a step the eye reads as different, every one read at delivery size.

| Role | Size (px at 1920×1080) | Leading | Step from the next size | Read at delivery size? | Why | Canon |
|---|---|---|---|---|---|---|
| title | | | | yes | | |

**Spacing.** Tracking per role, tightening as size grows; the kerning of each display pair, as the font's own pair value and any change made by eye.

| Role or pair | Tracking | Pair kerning (font's value → set value) | Why | Canon |
|---|---|---|---|---|
| title | | | | |
| `Wo` in <word> | | <n> → <n> | | |

**Placement.** One hang line held from card to card, inside title safe (5% in from each edge at 1920×1080: x 96–1824, y 54–1026). Credits grouped by proximity.

| Card | Hang line (x px) | Baseline (y px) | Inside title safe? | Grouping | Why | Canon |
|---|---|---|---|---|---|---|
| C<n> | | | yes | | | |

**Legibility against the picture.** Each card read over the frames it sits on.

| Card | Frames it sits on | Value contrast with the picture behind | Colour (kept a little under full white, less saturated than the picture) | Reads at delivery size? | Why | Canon |
|---|---|---|---|---|---|---|
| C<n> | <a>–<b> | | | yes | | |

## Model notes

What must stay the same about each subject through every pose and transformation: its identity, written so the Animator and the motion gate can check it frame by frame.

| Note | Subject | What never changes | How to check it in a frame |
|---|---|---|---|
| MN<n> | | | |

## Silhouette sheet

Every key filled black and numbered, its line of action drawn over it. `media:…/appearance/appearance-vNN-<date>/silhouettes.<ext>` · sha256 `<sha256>`

## Greyscale value study

The boarded frames in greys only, finding the focal point each panel asks for. `media:…/value-study.<ext>` · sha256 `<sha256>`

| Panel | Focal point the board asks for | Where the value study puts the eye | Agrees? |
|---|---|---|---|
| P<n> | | | yes |

## Each new pose beside the approved frame

One still per new key and smear, set beside the approved frame at viewing size, so identity is judged side by side and never from memory.

| Pose | Comparison still | sha256 | Model notes it shows held |
|---|---|---|---|
| K<n> | `media:…/beside-approved/<file>` | | MN<n> |

## Master layers' checksums

Proof the approved masters are unchanged. The command and its output are pasted below the table, never typed.

| Approved master | Path | sha256 at approval | sha256 now | Unchanged? |
|---|---|---|---|---|
| | `media:…/approved/<version-id>/<file>` | | | yes |

~~~
shasum -a 256 <each master, path written in full>
<output, pasted>
~~~

A master that changed is a material design change: the packet stops and the appearance gate reopens (never-do 3).

## Generated style targets

Every target from the Codex image path, generated or edited from a reference, by file, sha256 and the layer it informed, labelled generated, downloaded to the version folder on creation (never-do 13). If `edit_mode: unconfirmed`, say here which targets would have used it. `none` when none was made.

## Decisions

Choices made in design, one row each, filed by the coordinator as ledger entries in this seat's name.

| Choice | Over | Because | Canon |
|---|---|---|---|

## Questions for Sean

Taste calls on the look are Sean's at the appearance gate; this seat writes them as questions and rules none.

| Id | Question | Where it bites | The seat's recommendation |
|---|---|---|---|
| Q<n> | | K<n> | |

## Moves

<!-- MACHINE-READ by the rung-0 checker (craftwork/trace/check.py): move lines only, one per line,
     per artifact-header.md § The closing sections. A note goes in the pass record's ## Notes. -->

- kept — P<n>–P<m> from mc-eng-001.story
- split — B<n> → K<n>, K<m> from mc-eng-001.story
- added — SM<n> from mc-eng-001.appearance

meter: <runtime> · <tokens> · <wall-clock>
```

**What attacks this packet:** the Director's audit, on its stake in [the seat file](../bench/visual-story-director.md#audit-duty) (*does this look stage the boards?*), and the appearance gate, on the gate schedule's list for the appearance packet. Finishing's assembled frame is the gate's proof that the layers animate, attached by the coordinator; it is never part of this packet, and this seat never composites it.
