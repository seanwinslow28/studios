# Gate findings template — the story, appearance and motion gates

The findings file a gate writes: stateless, receiving only the artifacts, the shared [red-team protocol](../../craftwork/templates/red-team-protocol.md) and the gate schedule, never the drafting conversation, on the vendor that did not last write its anchor. Three craft gates on a full train, each a red-team attack and then one decision from Sean: the **story gate** on the animatic, the **appearance gate** on the appearance packet with Finishing's assembled frame attached as proof, and the **motion gate** on the moving test and its one directed revision. A small piece takes only the motion gate. When each fires, and the attack list for each artifact, are the [gate schedule](gate-schedule.md)'s. Every gate also writes its ledger entry, naming its vendor and why; this file is the authoritative record of the verdict, and the entry is derived from it. On Productcraft's shape ([productcraft/templates/gate-findings.md](../../productcraft/templates/gate-findings.md)) as Devcraft adapted it ([devcraft/templates/gate-findings.md](../../devcraft/templates/gate-findings.md)).

| Gate | Anchor | Anchor last written on | Runs on |
|---|---|---|---|
| story gate | `<eng>.story`, the animatic | Claude | Codex GPT-6.1 Sol High, read-only |
| appearance gate | `<eng>.appearance`, with the assembled frame | Claude | Codex GPT-6.1 Sol High, read-only |
| motion gate | `<eng>.motion`, and on its second pass the revision | Codex | a fresh-context Opus 5.5, read-only |

A FAIL that moves an anchor's last writer to the other vendor moves the gate too. A gate runs read-only on either vendor; its findings file is its final message, filed byte for byte by the launcher. Header fields per [artifact-header.md](artifact-header.md); written to `audits/<gate>.md`, a re-run to `audits/<gate>-r2.md`. The directed revision's held checks are the motion gate's second record, [directed-revision.md](directed-revision.md).

Posture is inherited: *find the strongest case that this fails; being unable to find a material flaw is a finding, so state what you attacked and why it held*; propose the steel-man alternative.

**A gate never approves artistry.** Its verdict is a quality verdict on what can be measured or named in frames. Sean's decision on the version (approved, artistic retake, technical retake, rejected) follows the gate, in his own words, and lives in the approvals ledger, never in this file.

```markdown
---
id: mc-eng-001.motion-gate         # story-gate | appearance-gate | motion-gate; -<part> per part on a film in parts; -r2 on a re-run
engagement: <project>-<YYYY-MM-DD>
date: 2026-10-26
seat: motion-gate                  # story-gate | appearance-gate | motion-gate
kind: gate
stage: 3                           # the anchor's stage: story gate 1, appearance gate 2, motion gate 3
gate: MOTION                       # STORY | APPEARANCE | MOTION
anchor: mc-eng-001.motion          # the anchor artifact and its revision or filed file
anchor_revision: 1
anchor_sha256: <sha256>            # the anchor as this gate read it
anchor_version: motion-vNN-<YYYY-MM-DD>   # the version folder judged; Sean's decision names the same id
anchor_last_written_on: codex      # claude | codex, read from the anchor's model: line; decides the vendor
proof: none                        # appearance gate: the assembled frame, "media:<path> · <sha256>"; none otherwise
vendor: claude-opus-5-5            # the runtime that ran the gate
vendor_switch: none                # none | "<why the gate left its default vendor>"
fallback: none                     # none | same-vendor → re-run ticket <link>
inputs: [mc-eng-001.motion, mc-eng-001.audit-motion, mc-eng-001.appearance, brief.md]
verdict: MOTION PASS — QUALITY VERDICT ONLY
ledger_entry: mc-eng-001.d<n>
---

## Verdict line

Typed, so a story verdict can never be quoted as a motion verdict: `STORY | APPEARANCE | MOTION` × `PASS | PASS WITH ACCEPTANCES | FAIL`, then ` — QUALITY VERDICT ONLY`, then scope and authority, then **Means** and **Does not mean / Next**, per the shared [status vocabulary](../../craftwork/templates/status-vocabulary.md). `NOT FIRED — TRIGGER NOT MET` is a state, not a verdict (a story or appearance gate on a small piece). A PASS is never an approval: the version goes to Sean with its id, its status and his prior note, and his decision is recorded in the approvals ledger. FAIL → the owning seat of each blocking finding redrafts one tier up, and the gate re-runs as `-r2`.

## The limit of this review

This is a review of decoded frames, not a real-time viewing. Felt weight, snap and timing at speed go to Sean's playback and are not passed here.

## Evidence present

Before any finding: each evidence field the anchor's template requires, and the proof attached at the appearance gate, present or missing, with its sha256 re-taken. A missing field is a technical fail, CRITICAL.

| Field | Path | sha256 in the anchor | sha256 now | Present and matching? |
|---|---|---|---|---|

## Findings

| Id | Kind | Severity | Artifact, section and frames | Finding | Glossary term | Attack it came from | Owner | Disposition |
|---|---|---|---|---|---|---|---|---|
| F<n> | technical fail \| craft fail | CRITICAL \| MATERIAL \| NOTE | mc-eng-001.motion § Contacts, frames <a>–<b> | | | gate schedule § Scene record, "<attack>" | animator | redraft \| accepted by Sean <date>: <why> \| noted |

A technical fail is decided by a measurement and is CRITICAL. A craft fail names a glossary term and frames, and is MATERIAL, or CRITICAL when it is one of Sean's named fail conditions. CRITICAL blocks the gate. MATERIAL is fixed, or Sean accepts it with a recorded why. Every finding names the attack line it came from; an attack with no home in the gate schedule is a finding against this folder. A finding that appears in more than one check gets one row, one owner and one disposition, with every appearance named in it.

## Questions for Sean

The taste calls this gate met, each written as a question, with the frames to watch. Never ruled here, and never a finding. Sean answers them with his decision on the version.

| Id | Question | Frames to watch at full speed |
|---|---|---|
| Q<n> | | <a>–<b> |

## Check series

One row per check series that ran on an artifact this gate is answerable for, from the check records' series lines. A series that did not shrink is a question to Sean, raised here.

| Artifact | Check | Rounds | Findings by round | Repair size by round | Ended on | Gate residuals carried |
|---|---|---|---|---|---|---|

Every gate residual appears in Findings above as a candidate acceptance, with its origin check named. A residual a later round already repaired closes here as stale.

## Holds for later

Evidence only a later point can produce, recorded as an obligation, never a severity: owner, trigger, required record, how it is measured, what happens if it is unmet. The story gate's holds are what the appearance gate or the motion gate must see; the motion gate's are what the six technical checks must see.

| Hold | Owner | Trigger | Required record | How measured | If unmet |
|---|---|---|---|---|---|

## Steel-man alternative

The strongest competing staging, design or timing the work did not take, in one paragraph, and why the work's choice survives it, or does not.

## What was attacked and held

Per artifact: the attacks run, and why each held. Empty is a defect.

meter: <runtime> · <tokens> · <wall-clock>
```
