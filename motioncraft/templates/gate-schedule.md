# Gate schedule and attack checklists

Motioncraft's own half of the red-team gate: when its three craft gates fire, what each one reads and may demand, which vendor runs it, what Sean decides after it, and what it attacks per artifact. The protocol itself (posture, statelessness, typed verdicts, holds, the rule that a gate never silently skips) is shared law at [craftwork/templates/red-team-protocol.md](../../craftwork/templates/red-team-protocol.md); this file is kept as Systemcraft and Devcraft keep theirs ([systemcraft](../../systemcraft/templates/gate-schedule.md), [devcraft](../../devcraft/templates/gate-schedule.md)). Written on the Motioncraft build map's **Gate schedule: the story, appearance and motion gates** ticket (2026-10-17), from the review order Sean approved on SWCB #164, the quality bar (#159), the opening treatment (#177), the camera question (#174), the assessment brief's exercises, critique rules and seed-shape exercise (sections 1 to 4, ratified 2026-10-17), and the bench and templates on `main`.

Gates are protocols, not seats. The trace kit files them as the gate seats `story-gate`, `appearance-gate` and `motion-gate` ([trace/studio.py](../trace/studio.py)) so their records have lanes. Each writes [gate-findings.md](gate-findings.md); the motion gate's second record is the held checks in [directed-revision.md](directed-revision.md).

**A gate never approves artistry** (rule 3 of [`motioncraft/CLAUDE.md`](../CLAUDE.md)). It rules on what a measurement proves or a frame shows, in the glossary's words, and writes every taste call as a question. Sean's decision on the version follows every gate, in his own words, in the approvals ledger.

## When gates fire

| Engagement | Gates |
|---|---|
| **Full train** (`type: full-train`) | **Story gate** after Finishing's audit of the story packet, before Art designs anything · **Appearance gate** after the Director's audit of the appearance packet, with Finishing's assembled frame attached, before anything moves · **Motion gate** after Art's audit of the scene record, then its one directed revision and the held checks · then the **integrated film**, which is not a gate (below) |
| **Small piece** | **Motion gate** only. The story and appearance gates are `NOT FIRED — TRIGGER NOT MET`, recorded with the reason. What qualifies as a small piece is the master skill's |
| **One-off** (a single seat pass) | No gate |
| **Self-targeted check** (the shared law's modifier) | Its own fresh gate under [the modifier](../../craftwork/law.md#self-targeted-modifier), on its own map ticket (**Self-targeted check on mc-eng-001, red-teamed on Codex**). It is none of the three below and never stands in for one |

**Parts: split by approval state.** A film splits only where some of it is already approved and some is new (an approved background behind a changed character, say), never into halves of its running time ([Master skill design](https://github.com/seanwinslow28/SWCB/issues/192), item 2). Every appearance packet lists its **approved elements**, frozen and unchanged by checksum, and its **new elements**; the appearance gate judges only the new ones, against the approved. A film takes one artifact per part (its own version folders, gate record and Sean's yes) only when its parts reach Sean's yes at different times; the animatic and the finished cut always stay whole, so the story gate fires once. Each part's gate is then its own series: a pass takes the part as a suffix on its id and file (`<eng>.appearance-gate-<part>`, `audits/appearance-gate-<part>.md`, then `-r2` after it), and so do the revision form and the held checks (`<eng>.revision-<part>`, `audits/revision-check-<part>.md`). The record's `seat:` stays the gate seat. Every part passes the appearance gate, with Sean's yes on each, before any motion draft.

**mc-eng-001 runs unsplit.** Sean restarted the seed from scratch (Master skill design, item 3): the October seed approval (approvals ledger, mc-ap-004) is a non-binding taste reference, and nothing in the film is approved, so there is one animatic, one appearance packet, one appearance gate and one motion stage holding both E4's seed-shape exercise and the world's moving test with E5's leaf unfold. The coordinator claims the camera ticket (**Camera through one painted world**, #174) when the train reaches the appearance gate, never before.

Outcomes are typed **STORY** / **APPEARANCE** / **MOTION**, each `PASS | PASS WITH ACCEPTANCES | FAIL` and always `— QUALITY VERDICT ONLY`, per [gate-findings.md](gate-findings.md). No verdict here approves a version: that is Sean's, recorded in the approvals ledger.

## The three craft gates

| | Story gate | Appearance gate | Motion gate |
|---|---|---|---|
| **Anchor** | the story packet's timed animatic (stage 1) | the appearance packet (stage 2), with Finishing's assembled frame as `proof:` | the scene record's moving test (stage 3), and on its second record the directed revision |
| **The audit before it** | Finishing's, *can this animatic be finished into the film it promises?* | the Director's, *does this look stage the boards?* | Art's, *is this still the subject Sean approved, in every frame?* |
| **Default vendor** | Codex GPT-6.1 Sol High, because Claude wrote the anchor | Codex GPT-6.1 Sol High, because Claude wrote the anchor | a fresh-context Opus 5.5, because Codex wrote the anchor |
| **Launch** | the Codex form (registry row 3; [bench § Launch forms](../bench/README.md#launch-forms)), `--model gpt-6.1-sol`, effort `high` spelled out, read-only sandbox; its findings are its final message, saved by `-o` and filed byte for byte | the Codex form, as the story gate | the Claude form (registry row 2), `--model claude-opus-5-5`, read-only tools; the launcher files its final message as its findings |
| **Reads** | the story packet; Finishing's audit and any verification of it; the brief and the approvals entries it names; the packet's media by path, its checksums re-taken; [the glossary](../lanes/glossary.md), whole | the appearance packet; the Director's audit; the story packet; the approvals entries in force; the assembled frame; the packet's media by path; [the glossary](../lanes/glossary.md), whole | the scene record (and `scene-record-r2.md` on the revision); Art's audit; the appearance packet and its gate's findings; Sean's decision on that gate; the story packet; the brief; the evidence pack by path; [the glossary](../lanes/glossary.md), whole |
| **May demand** | only what an animatic shows: boards, timing in frames, the probe, the muted copy, the shot list. Motion, look and finished sound are holds for later, never findings | only what still frames show: the layers, the poses, the sheets and studies, the checksums, the assembled frame. Moving without sliding paint is a hold for the motion gate | everything a moving test shows: the evidence pack, the probe, the save-reopen-render comparison, frames the gate extracts itself. Felt weight and snap at speed are Sean's. What only the cut can show is a hold for the Animator's audit and the six technical checks |
| **Attacks** | § Story packet, § Check records, § Whole train | § Appearance packet, § Check records, § Whole train | § Scene record, § Check records, § Whole train; on its second record, § Directed revision |
| **Record** | `audits/story-gate.md` | `audits/appearance-gate.md`, or one per part | `audits/motion-gate.md` and `audits/revision-check.md`, or one of each per part |

Every gate reads artifacts only, never the drafting conversation, and carries the [protocol](../../craftwork/templates/red-team-protocol.md), this file, [gate-findings.md](gate-findings.md) and [the glossary](../lanes/glossary.md), never the seat preamble or a lane manifest. The glossary is where a gate gets its words: every craft fail's **Glossary term** is a row's Term exactly, whatever artifact or lane the fault sits in, and the four naming rulings beside the rows are the ones its § Check records attack, "Bare words", enforces. The exact flags, the per-pass caps and how a read-only pass gets a scratch folder for the frames it extracts are the master skill design's and the launch-form ticket's (**Plugin allowlist and launch form for seat runs**). Until those close, no gate runs.

**Evidence before findings.** Every gate opens on the findings file's **Evidence present** table: each field the anchor's template requires, and the assembled frame at the appearance gate, present and matching its sha256. A missing or mismatched field is a technical fail, CRITICAL, and the gate judges nothing that depends on it.

## Sean's decision after a gate

A PASS goes to Sean as a version: its id, its status and his prior note on it (never-do 14), the verdict line, the questions for Sean with the frames to watch, and one recommendation, inside his checkpoint (#158: up to three short clips or stills, one recommendation, one decision, five to ten minutes). He decides in his own words, one of four:

- **Approved.** The train advances to the next stage, or the next part.
- **Artistic retake** or **technical retake.** The owning seat makes a new version on his note. A gate verdict covers only the version it read, so the new version takes its stage's audit and the gate again before he sees it. A retake is his direction, not a gate round: it opens a fresh series. How many a stage may take is the master skill's pass caps, inside #158's limits.
- **Rejected.** The train stops at that gate and returns to Sean with the evidence and one recommended next step (#164).

At the motion gate his decision on the passed version comes with the one directed revision he names, written on [the form](directed-revision.md); the held checks then run, and he decides again on the revised version.

A FAIL never reaches Sean as a version to decide on. It goes back to the owning seats (below), unless it is the gate's last round.

## The integrated film

The integrated film closes on the Animator's audit of the delivery package (*did the motion survive finishing?*), then the six technical checks of the quality bar (`TC1`–`TC6` in [delivery-package.md](delivery-package.md#technical-check-record), with the loudness record), then Sean's artistic yes. It is not a red-team gate and takes no verdict type. A check that could not run is a fail, and a known technical defect is never accepted in the final film. The motion gate's holds are what these checks must see.

## Vendors, and when a gate switches

A gate runs on the vendor that did not last write its anchor, read from the anchor's `model:` line and written into the findings as `anchor_last_written_on:`. At the appearance gate the packet decides, not the assembled frame.

A FAIL's redraft runs one tier up ([craftwork § Model delegation](../../craftwork/law.md#model-delegation)). A Claude seat's next tier is Codex GPT-6.1 Sol High, so a Director or Art redraft moves the story or appearance anchor onto Codex, and the re-run moves to a fresh-context Opus 5.5. The Animator's ladder stays on Codex (`high`, then `xhigh`, then stop and ask Sean, never `ultra`), so the motion gate stays on Claude. The findings say why in `vendor_switch:`, and the coordinator says so at the gate.

If the planned vendor is unavailable, the protocol's fallback holds: the gate runs fresh on the other vendor, labelled `fallback: same-vendor`, and a re-run ticket is filed.

## FAIL and re-runs

FAIL → the owning seat of each CRITICAL or MATERIAL finding redrafts one tier up, and the gate re-runs as `-r2`. That re-run is the gate's last round ([craftwork § Checks converge](../../craftwork/law.md#checks-converge-and-the-ladder-has-brakes), clause 9): a second FAIL stops the engagement and hands it to Sean with every open finding as a candidate acceptance. Every check series still open is reported at each gate as round / findings / repair size, and a gate's own non-shrinking line binds the coordinator (clause 10). On a film in parts the cap is per part.

The held checks are the motion gate's second record and take the same shape: a failed check sends the Animator back to the source once, the checks re-run as `revision-check-r2`, and a second FAIL stops and goes to Sean. A repair here answers the failed check alone and never mixes with a further change of Sean's.

A redraft that changes an approved master, or an approved pose, is a material design change: the appearance gate reopens for it, and nothing moves on the old approval (never-do 3).

## Attack checklists per artifact

Every finding names the line it came from, as `gate schedule § <list>, "<line>"`. An attack a gate needs that has no line here is a finding against this folder.

### Story packet

- **The sum does not hold.** The panel list's frames do not sum to `total_frames:`, or the probe is not pasted, or its frames, rate and duration differ from the panel list.
- **A beat where nothing changes.** A beat or panel that names no change and is not timed as a hold in frames.
- **Two places to look.** A panel with more than one focal point, or a cut with no known place for the eye.
- **Screen direction crossed.** Direction reverses across a cut with no stated motive.
- **Holds by feel.** A hold or a pause written as "a beat" or "a moment", not in frames.
- **Camera words wrong.** A camera move named zoom that is travel, or a move left unnamed.
- **It does not read muted.** The muted copy missing, the muted-reading sentence missing, or the sentence admits a stretch that reads only with sound and nothing marks it.
- **No room for sound.** A moment that needs a sound to land with no mark, or a score, voice or dialogue written in rather than marked to route out.
- **Not buildable.** A shot whose staging, size or camera the shot list leaves open, or a panel no shot owns.
- **The world as two places.** The world staged as anything but one camera in one space: two framings joined by a crossfade, or the pull-back revealing a place the planting close-up was not in (#174).
- **The opening redesigned.** The opening departs from the approved treatment (#177): the seed not complete and suspended at the start, the question stroke not carried by smear poses, the seed not readable through the fall, or any literal disassembly and reassembly.
- **Timing squeezed.** A duration shortened to fit a review window or a test, or a total length nobody agreed (never-do 9).
- **Words shipped as final.** On-screen or spoken words not marked as placeholders and not Sean's (never-do 10).
- **A rough passed as a board.** A generated rough standing in for a drawn board, not labelled, or not downloaded to the version folder (never-dos 8 and 13).
- **Intake that leaked.** A brief line mapped to nothing.

### Appearance packet

- **A shape that does not read.** A key that does not read as a solid black shape, or two keys that share one silhouette.
- **No line of action.** A key with no line of action drawn over it.
- **Volume lost.** A squash or stretch key outside about the resting size, against the area its row claims.
- **Smears left to chance.** A smear the plan leaves without its frames, the keys it joins or its arc, or a smear that is a filter, a blur or a generated image rather than a designed drawing (never-do 8).
- **Layers that are not separate.** Line, pigment and paper not each their own file, or a layer with no change rule, or a rule named in bare words rather than line boil, paper boil or pigment variation.
- **The eye in the wrong place.** The value study puts the eye somewhere other than the board's focal point, and the table says it agrees.
- **A master touched.** An approved master whose sha256 differs, or a checksum typed rather than pasted from the command.
- **The proof does not match.** The assembled frame built from layers whose checksums differ from the packet's, or a frame that does not look like the packet's style frame, or no frame.
- **Identity judged from memory.** A new key or smear with no still beside the approved frame, or a model note that cannot be checked in a single frame.
- **An approval carried across a change.** A design change to an approved frame, pose or palette that the packet does not name as one and route to Sean (never-do 3).
- **Colour that does not carry the beats.** A beat with no palette, value or temperature line, or a colour choice the grade would have to invent.
- **Type not set for the screen.** A film that sets text with no Type section; a face not on the font shelf; a size, spacing or placement row with no why or no canon; a card outside title safe or off the hang line; a size not read at delivery size; real words where the film has none yet from Sean or Scriptcraft.
- **A target passed as a design.** A generated style target not labelled, not downloaded, or standing in for a painted layer; edit mode relied on while unconfirmed and not said.
- **The rejected look back.** A composed frame that reuses the earlier look Sean did not accept, or a frame whose layers could not move under the camera construction the shot list names.

### Scene record

Every moving test:

- **Version unnamed.** The version id, its status or Sean's prior note missing (never-do 14).
- **Evidence missing.** Full-speed playback, the frame-numbered copy, a timing chart for a move, two adjacent frames either side of a contact or transformation, the layer stack, the technical record, or an optional field the brief asked for, missing or not matching its sha256.
- **Re-timed to fit.** Frames, rate or duration differ from the animatic (never-do 9).
- **A render that will not reopen.** The save, reopen and render comparison missing, or any frame differs.
- **Paint changed underneath.** A layer's sha256 in the stack differs from the appearance packet's.
- **Spacing in the wrong words.** A move described in bare "ease in" or "ease out", or spacing the chart does not show.
- **A drawing passed as a smear.** A smear frame that is a filter, a motion blur or a generated frame (never-do 8).
- **A quiet redraw.** A move the approved poses cannot reach drawn anyway, rather than declared as a deviation and sent back to Art.
- **Texture sliding.** Paint fixed on screen while the subject moves under it, in the adjacent crops; CRITICAL, as Sean ruled on #161.
- **The video-game look.** Rigid card rotation, even spacing, cards repeated where change is planned; CRITICAL on its observable sign, the final call Sean's (#162).
- **The first-Codex line missing.** No line saying the pass ran as the first Codex seat on visual work.

The seed's movement (E4's seed-shape exercise), in the review order of the assessment brief, section 4: the technical record first, a one-sentence muted reading of the frame-numbered copy, the charts against the animatic, the adjacent frames at the contact and each smear, the silhouette sheet against the appearance packet's plan.

- **Sean's six named fail conditions, each CRITICAL:** the video-game look and texture sliding, above; assembly from chunks (any frame built from separate pieces); repeated silhouettes (one drawing reused where the plan calls for change, or a seed with a tail); floaty weight (a gap at contact, even spacing into the floor, no squash, or a one-frame jump); lost identity in the smear (a smear frame that loses an identity mark the approved appearance packet names).
- **The eight criteria, each with frames:** appearance kept; the stroke on designed smears only, on the arc, about the resting size; the readable seed back before the fall, with no broad smear carried into it; the tumble readable on every frame, on one rotation rule, spacing widening toward the contact; the contact on its frame with squash there and no unplanned jump; exactly two rebounds, each lower, drawings bunching at each peak; drawings bunching into a rest that holds visibly; paint moving with the seed through rotation and squash, with no undesigned flicker.

The world's moving test:

- **Two shots joined.** The pull-back reads as two places put together, or a crossfade joins unrelated framings; CRITICAL, as Sean found it on #174.
- **The landmark moved.** The planting point does not stay fixed in the world through the camera move.
- **Depth broken.** Ground contact lost or depth order wrong as the camera travels.
- **Growth mistaken for scenery.** New growth and scenery entering the frame cannot be told apart.
- **A move with no motive.** The camera travels before the growth's direction reads.
- **Edge in frame.** A painted layer's edge, or bare canvas, inside the frame anywhere along the camera move: crops along the frame's edges at every frame where the camera nears a layer's end, and the whole frame across the move.
- **The arrival cut short.** The three-second living arrival is shorter than three seconds, or does not hold.
- **The leaf stretched.** The leaf unfold shows fewer than three distinct drawn poses (folded, half, open), or one pose stretched, or no follow-through from the branch.
- **Outside the construction.** The test goes beyond the limits Sean's choice on the camera ticket recorded.

### Directed revision

- **More than one change.** The form's sentence names two changes, or the record shows a second change made.
- **The named frames did not change as named.** Check 1: the before and after frames and charts do not show the change in its direction.
- **Something else moved.** Check 2: the comparison's command or output missing, a frame before the range that differs, or a frame after it that is not the same drawing at the declared shift.
- **A passed criterion lost.** Check 3: a criterion the passed version met that no longer holds, or a master whose sha256 changed.
- **Changed in the render.** The change made in a render, not the editable source.
- **A repair mixed in.** A fix to a reviewer's finding carried inside the directed revision's pass.
- **A new pose smuggled in.** A change that needed a new pose, made here instead of going back to Art.

### Check records

- **A check that saw the conversation.** Inputs listing anything but artifacts.
- **A silent pass.** What was attacked and held left empty on a clean verdict.
- **Severity laundering.** A material defect filed as a note to avoid the loopback.
- **Taste ruled as a finding.** Beauty, life or feeling ruled by a seat, rather than written as a question for Sean (rule 6).
- **A finding with no frames.** A craft fail with no frame numbers, or no glossary term, or a term that is not a row of [the glossary](../lanes/glossary.md).
- **Bare words.** "Ease in", "boil", "jitter", "scene" for a piece of the film, or "zoom" for travel, in a finding.
- **The limit unstated.** No line saying the review read decoded frames, not a real-time viewing.
- **The stake not answered.** Rows that never address the auditor's stake.
- **A verification pass that re-audited.** Findings from frames the repair never touched filed as material, or a passed finding reopened.
- **A second loopback on one check.** The repair cap spent and a third round requested.

### Whole train

- **Cross-artifact contradictions.** A beat with no panel, a panel with no shot, a key the motion never uses, a move from a pose the packet does not have.
- **The cascade that did not fire.** An artifact below a loopback still at its old revision, or an assembled frame older than the layers it proves.
- **Checks that never ran.** A stage with no audit record, or a motion draft before its appearance gate (never-do 3).
- **The steel-man.** A competing staging, design or timing that serves the brief better, and no artifact rules it out.
- **Data outside the fence.** Production media cited by anything but a `media:` path and sha256, or a cloud upload or generation outside its intended-use approval (never-do 6).
- **Process waste.** A series run past its stopping rule, a finding recounted per appearance, a defect this folder or the kit caused. Coded from the shared process-waste family ([craftwork/trace/taxonomy.md](../../craftwork/trace/taxonomy.md)), not graded as a seat's failure.
