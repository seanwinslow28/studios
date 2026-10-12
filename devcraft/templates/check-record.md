# Check record template — the four audits

The artifact of an **audit** pass: what the auditing seat saw, what it attacked, what held, and what goes back. Devcraft has no co-signs, so every check record is one of the four audits in the closed cycle, Planner → Builder → Release → Verifier → Planner, the arrow reading "audits". Written by the fixed auditor in a fresh-context invocation that receives artifacts only, never the drafting conversation. On Productcraft's shape ([productcraft/templates/check-record.md](../../productcraft/templates/check-record.md)); the convergence rules are shared law, [craftwork § Checks converge](../../craftwork/law.md#checks-converge-and-the-ladder-has-brakes).

| Id | Auditor | Checks | Runs | Stake (from the seat file) |
|---|---|---|---|---|
| `<eng>.audit-plan` | verifier | the build plan | after the plan's draft, before the plan gate | *Can every promise in this plan be tested, and does it stay on how, never what?* |
| `<eng>.audit-change` | build-planner | the change note and the branch | once the change is final, while Release drafts | *Does the code do what the plan said, and nothing more?* |
| `<eng>.audit-release` | builder | the release plan and runbook | after Release's draft; a read-only Codex pass | *Does the release plan cover what this change really touches?* |
| `<eng>.audit-tests` | release-reliability | the test record, after the final run | the last audit before the release gate | *Would these tests catch what breaks in production or overnight?* |

An audit never edits the checked artifact: a material finding is a loopback to its drafting seat, and one repair round per artifact per check is the cap. The coordinator transcribes the verdict into the checked artifact's `audit:` field and into the pass record's `checks`. The Builder's audit is a Codex pass, so its record is the pass's final message, filed by the coordinator byte for byte. Header fields per [artifact-header.md](artifact-header.md); written to `audits/audit-<slug>.md`.

```markdown
---
id: dc-eng-001.audit-plan
engagement: dc-eng-001-<slug>
date: 2026-10-14
seat: verifier                     # the auditing seat
kind: audit
stance: first-sight                # first-sight | verify; a verify pass is round two
stage: 1                           # the checked artifact's stage
model: claude-opus-5-5
grounding: full
checked: dc-eng-001.plan           # the artifact id checked, and its revision
checked_revision: 1
stake: "Can every promise in this plan be tested, and does it stay on how, never what?"
verdict: AUDIT LOOPBACK — 1 material
---

## Verdict line

One of: `AUDIT CLEAN — stake held` · `AUDIT LOOPBACK — <n> material` · `AUDIT NOTES ONLY`. Then **Means**, then **Does not mean / Next**, per the shared [status vocabulary](../../craftwork/templates/status-vocabulary.md). An audit verdict is never a gate verdict.

## The stake, worked

The table for this audit's stake. Each row is evidence the auditor opened or ran, never a reading of the author's summary.

- **audit-plan:** one row per intake item (mapped to what?), per criterion (observable? its seam and level?), and per security trigger (does the build hit it, whatever the plan says?). A trigger the build hits and the plan rated below high is material, whatever reason the plan gives. A test path removed from the floor is material.
- **audit-change:** one row per slice, read on the review dimensions (design, functionality, complexity, tests, naming, comments, docs, every line) against the plan. An unplanned change, a deviation without a reason, or a slice that cannot merge alone is material. A change that quietly made an architecture call goes back as `"Blocked: architecture call"`.
- **audit-release:** one row per path the diff touches that is a schema, job, schedule or config, matched to a release-surface line (`RS<n>`) or marked MISSING; the migration plan against the migration code; the rollback against this code; where the drill ran. An ops path the diff touches and the plan never flagged is material.
- **audit-tests:** one row per command in the final record, re-run, its output compared with the record; then the suite against the plan's criteria and the release plan's failure modes (the migration both ways, a restart, a missing secret, an unattended re-run). A result that does not reproduce is material.

| Row | What was checked | Evidence opened or command run | Holds? |
|---|---|---|---|
| AC<n> | observable; seam named | build plan § Goal and acceptance criteria | yes |

## Findings

One row per finding, severity **MATERIAL** (loops back) or **NOTE**.

| Id | Finding | Artifact and section | Severity | Evidence | What would pass |
|---|---|---|---|---|---|
| M<n> | | dc-eng-001.plan § Security & privacy surface | MATERIAL | | |

## What was attacked and held

Being unable to find a defect is a finding: name what was attacked, how, and why it held. Empty is a defect.

## Loopback

The one message to the drafting seat: which rows, what evidence, what would pass. `none` on a clean audit.

## Verification (`stance: verify` only; omit the section entirely on a first-sight check)

Round two is a verification pass, not a fresh audit. It runs on the vendor that did not write the repair. Exactly three duties:

1. **Rule each repair** `holds` or `residual`, one row per first-sight finding, in its original numbering.
2. **Attack the text the repair changed**, and that text only. A defect found outside it is a **gate residual**, carried to the next gate as a candidate acceptance, never a loopback.
3. **Stop.**

| Id | First-sight finding | Repair | holds \| residual | If residual: what still fails, what would pass |
|---|---|---|---|---|
| M<n> | | | holds | |

| Outside the changed text | Section | Severity | Carried to | Why it is not a loopback |
|---|---|---|---|---|

**The series line**, for the gate's check series table: `round <n> / <findings> findings / <sections or lines> changed`. A series that does not shrink is a question to Sean, never another round.

meter: <runtime> · <tokens> · <wall-clock>
```

**What attacks a check record:** the gates read every check record in scope; the attacks are in [gate-schedule.md § Check records](gate-schedule.md#check-records).
