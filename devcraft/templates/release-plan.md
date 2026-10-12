# Release plan template — the release plan, its runbook and the drill record

Owned by **Release & Reliability** ([seat file](../bench/release-reliability.md)). Stage 4 of a full build, the anchor of the **release gate**, and the one artifact no test checks. It is drafted once the diff is stable, while the Planner audits the change. Audited by the **Builder**, against the actual diff. Header fields per [artifact-header.md](artifact-header.md); written to `artifacts/release-plan.md`, drill output to `evidence/`.

**On an ops-only direct ask** (a job definition, a schedule or a config file, no source change), there is no build plan: the release surface comes from the file list the coordinator copied into the brief at Open, that list is this seat's whole write zone, and the **drill record stands in for tests**. A missing drill record is a release-gate FAIL. Sections that do not apply say `n/a — ops-only`. A source change found on the way stops the seat with `exit: "Blocked: needs source"`.

**No seat flips the switch.** This plan writes the go-live step. The coordinator runs it, in a session Sean is driving, after the release gate and his dated yes.

```markdown
---
id: dc-eng-001.release
engagement: dc-eng-001-<slug>
date: 2026-10-17
seat: release-reliability
stage: 4
model: claude-opus-5-5
grounding: full
thin_lane: []
adjacent_lanes: []
target: seanwinslow28/<repo>
branch: <the build's branch>
base: <commit>
at: <commit>                       # the stable diff this plan was drafted on
exit: none                         # or "Blocked: needs source", "Blocked: budget", …
revision: 1
stale_from: null
status: draft
auditor: builder
audit: pending
ask: full-build                    # full-build | ops-only
drill: run 2026-10-17              # run <date> | missing; no drill record, no release
gate3: n/a                         # n/a | waiting: <Systemcraft engagement id>
---

## Release surface

What changes in the running world when this merges: databases and stored files, launchd jobs and schedules, CI, config, secret *names*. Every ops path the plan flagged appears here, and nothing this seat may not write.

| Id | What changes | Path | From |
|---|---|---|---|
| RS<n> | | | OP<n> |

## Preconditions and backup

What must be true before the first step, each with the command that shows it. Then the backup: the command, where the copy lands, and the proof it restores.

## Migration plan

Expand, then contract: the new shape is added before the old one is removed, so every step has a way back. Each step says whether the code on either side of it still works.

| Step | Phase | What | Backward compatible? | Way back |
|---|---|---|---|---|
| MG<n> | expand | | yes | |

A step with no way back is named as one, with what Sean is accepting. `none` when nothing stored changes.

## Rollout

A solo-scale canary: a small, watched first exposure before the whole thing.

| Stage | What runs | For how long | Promote when | Abort when |
|---|---|---|---|---|
| Dry run | | | | |
| Log-only shadow | | | | |
| Live | | | | |

## Failure modes

Every way this breaks in the running world, each with the signal that would show it. Always covered: the migration both ways, a restart mid-run, a missing secret, and an unattended re-run (the job that runs twice).

| Id | Failure mode | Signal | Runbook line |
|---|---|---|---|
| FM<n> | migration rolled back after new rows exist | | R<n> |

## Rollback and kill drill

**Rollback:** the exact commands that undo this change.
**Kill:** the exact command that stops it running, and what it leaves behind.

**Drill record.** Run in the build's worktree or on a copy the build made and this plan names, never on live data. Paste what actually ran.

**Where:** `<worktree path or named copy>`
**When:** `<instant>`
**Commands and output:** `evidence/drill.txt` (sha256 `<hash>`), with the lines that show the change applied, undone and stopped quoted here.
**Result:** what the drill proved, and what it did not exercise.

## Monitoring

Per failure mode, the heartbeat, log line or alert that says it broke, and where Sean sees it.

## Runbook

Readable at 3 a.m. by someone who did not build this: exact commands, the expected output, the next step if it differs.

| Line | Symptom | Check (command → expected output) | Action | If that fails |
|---|---|---|---|---|
| R<n> | | | | |

## Secure deployment

- **Permissions:** what the job runs as, its file modes, the least that works.
- **Secrets:** by name, how each is loaded at runtime, and what happens when one is missing.
- **Hosts:** every host the change talks to, against the plan's allowlist.
- **Dependency check:** the scanner, its command and its result (`evidence/deps.txt`), or `no dependency changed`.
- **Secret scan:** the command over the build's commit range and its result (`evidence/secrets.txt`).

## Go-live step

The exact commands the coordinator runs, in a session Sean is driving, after the release gate and his dated yes. Never run by this seat.

## Gate packet

What the release gate receives, every file whole: the build plan, the test record with its final record, the change note, this plan with its drill record, the diff (`git diff <base>..<candidate>`), the diff check's output, the secret scan and the dependency check, every check record, the plan gate's findings, and the security pass's findings when it fired.

**Gate 3 evidence**, only when Systemcraft waits on this build (the release gate runs first and feeds Gate 3, never replacing it):

| Gate 3 demands | Evidence here | Hold it closes |
|---|---|---|
| Build identity | | |
| Actual path and schema | | |
| Migrations | MG<n>–MG<m> | |
| End-to-end positive and negative tests | the test record's final record | |
| Rollback and kill drills | the drill record | |
| Instrument records and measurements | | |

## Sean's yes

`Sean's yes: <blank until given>`. The authority is the dated ledger entry recording his yes to merge or go live (never-do 3); the coordinator copies its date, what he approved and its entry id here, inside a recorded pass, never by hand.

## Exit

On `exit: "Blocked: needs source"`: the source change the release needs, and why no ops change can stand in. Omit this section when `exit: none`.

## Moves

<!-- MACHINE-READ by the rung-0 checker (craftwork/trace/check.py): move lines only, one per line,
     per artifact-header.md § The closing sections. A note goes in the pass record's ## Notes. -->

- split — OP<n> → RS<n>, RS<m> from dc-eng-001.plan
- added — FM<n>–FM<m> from dc-eng-001.change

meter: <runtime> · <tokens> · <wall-clock>
```

**What attacks this plan:** the Builder's audit, on its stake in [the seat file](../bench/builder.md#audit-duty), and the release gate, on [gate-schedule.md § Release plan](gate-schedule.md#release-plan) and the whole-build attacks.
