# Gate findings template — build gates and the self-check gate

The findings file a gate writes: stateless, receiving only the artifacts, the shared [red-team protocol](../../craftwork/templates/red-team-protocol.md) and [the gate schedule](gate-schedule.md), never the drafting conversation, on the vendor that did not last write its anchor. The gate schedule defines Devcraft's build gates and its self-check gate, and when each fires. Every gate also writes its ledger entry, naming its vendor and why; this file is the authoritative record of the verdict and the entry is derived from it. On Productcraft's shape ([productcraft/templates/gate-findings.md](../../productcraft/templates/gate-findings.md)).

A gate runs read-only on either vendor; its findings file is its final message, filed byte for byte by the launcher. Header fields per [artifact-header.md](artifact-header.md); written to `audits/<gate>.md`, a re-run to `audits/<gate>-r2.md`. For the self-check gate these are `audits/self-check.md` and `audits/self-check-r2.md`; its anchor is the check report, with the raw record as evidence, and its verdict type is AUDIT.

Posture is inherited: *find the strongest case that this fails; being unable to find a material flaw is a finding, so state what you attacked and why it held*; propose the steel-man alternative.

```markdown
---
id: dc-eng-001.plan-gate           # plan-gate | release-gate | security-pass | self-check, -r2 on a re-run
engagement: dc-eng-001-<slug>
date: 2026-10-14
seat: plan-gate                    # plan-gate | release-gate | security-pass | self-check
kind: gate
stage: 1                           # the anchor's stage: plan gate 1, security pass 3, release gate 4; self-check follows its check report
gate: PLAN                         # PLAN | RELEASE | SECURITY | AUDIT
anchor: dc-eng-001.plan            # the anchor artifact and its revision
anchor_revision: 1
anchor_sha256: <sha256>            # the anchor as this gate read it; the plan gate's freezes the exceptions
anchor_last_written_on: claude     # claude | codex, read from the anchor's model: line; decides the vendor
vendor: codex gpt-6.1-sol high     # the runtime that ran the gate
vendor_switch: none                # none | "<why the gate left its default vendor>"
fallback: none                     # none | same-vendor → re-run ticket <link>
inputs: [dc-eng-001.plan, dc-eng-001.audit-plan, brief.md]
verdict: PLAN PASS — QUALITY VERDICT ONLY
unforeseen_security_critical: no   # release gate and security pass: yes when a CRITICAL security finding is one the plan's surface section did not foresee
ledger_entry: dc-eng-001.d04
---

## Verdict line

Typed, so a plan verdict can never be quoted as a release verdict: `PLAN | RELEASE | SECURITY | AUDIT` × `PASS | PASS WITH ACCEPTANCES | FAIL`, then ` — QUALITY VERDICT ONLY`, then scope and authority, then **Means** and **Does not mean / Next**, per the shared [status vocabulary](../../craftwork/templates/status-vocabulary.md). `NOT FIRED — TRIGGER NOT MET` is a state, not a verdict (a security pass on a surface not rated high; a release gate on a small direct ask that touches no live data, no migration and nothing unattended). A RELEASE PASS is never a go-live: Sean's dated yes is separate. AUDIT rules only on the check's claims and limits; it grants no build, merge or go-live authority. FAIL → the owning seat of each blocking finding redrafts one tier up, and the gate re-runs as `-r2`.

## Claim reproduction (self-check gate)

One row for every claim in the check report. Reproduce it from the raw record, name the exact input and command or record location, and save the output. A claim that cannot be reproduced names a finding or a recorded limit. Build-only sections below (frozen exceptions, automatic checks, security attacks and implementation holds) are marked not applicable when this check has no build.

| Claim | Raw record and input | Command or record location | Saved output | Held, finding or limit |
|---|---|---|---|---|

## Findings

| Id | Severity | Artifact and section | Finding | Attack it came from | Owner | Disposition |
|---|---|---|---|---|---|---|
| F<n> | CRITICAL \| MATERIAL \| NOTE | dc-eng-001.plan § Exceptions | | gate-schedule.md § Build plan, "Late exceptions" | build-planner | redraft \| accepted by Sean <date>: <why> \| noted |

CRITICAL blocks the gate. MATERIAL is fixed, or Sean accepts it with a recorded why. Every finding names the attack line it came from; an attack with no home in the gate schedule is a finding against this folder. A finding that appears in more than one check gets one row, one owner and one disposition, with every appearance named in it.

## Exceptions on the record (plan gate only)

The plan's Exceptions section exactly as this gate read it, at `anchor_sha256`: the only exceptions the diff check honors for this build. A plan amendment adds to this list only through a re-run of the plan gate.

| Id | Kind | Exactly what | For which seat |
|---|---|---|---|

## Automatic checks (release gate; the security pass reads them too)

Run by the coordinator just before the gate, their outputs saved to `evidence/` and handed in. Each renders the literal result, what it exercises and what it does not. A check that could not run is a finding, never a silent skip.

| Check | Command | Output | Exercises | Does not exercise |
|---|---|---|---|---|
| Diff check | | `evidence/diff-check-<candidate>.txt` | | |
| Secret scan | | `evidence/secrets-<candidate>.txt` | | |
| Dependency check | | `evidence/deps-<candidate>.txt` | | |

## Fixed security attack list (release gate, every time; the security pass, weighted to the triggers that fired)

One row per line of [gate-schedule.md § The fixed security attack list](gate-schedule.md#the-fixed-security-attack-list): attacked how, and held or the finding's id.

| Line | Attacked how | Held, or finding |
|---|---|---|
| SA1 | | held |

## Check series

One row per check series that ran on an artifact this gate is answerable for, from the check records' series lines. A series that did not shrink is a question to Sean, raised here.

| Artifact | Check | Rounds | Findings by round | Repair size by round | Ended on | Gate residuals carried |
|---|---|---|---|---|---|---|

Every gate residual appears in Findings above as a candidate acceptance, with its origin check named. A residual a later round already repaired closes here as stale.

## Implementation holds

Evidence only a later point can produce, recorded as an obligation, never a severity: owner, trigger, required record, the test or command, what happens if it is unmet. The plan gate's holds are what the release gate must see; the release gate's are what Gate 3 or go-live must see.

| Hold | Owner | Trigger | Required record | Test or command | If unmet |
|---|---|---|---|---|---|

## Steel-man alternative

The strongest competing approach the build did not take, in one paragraph, and why the build's choice survives it, or does not.

## What was attacked and held

Per artifact: the attacks run, and why each held. Empty is a defect.

## Six months on

"Name the most likely way this is quietly failing six months after it goes live, or at 3 a.m. on an unattended run." One paragraph, and the signal in the release plan that would show it, or the fact that none does.

meter: <runtime> · <tokens> · <wall-clock>
```
