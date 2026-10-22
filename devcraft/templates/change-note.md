# Change note template — the code change and its note

Owned by the **Builder** ([seat file](../bench/builder.md)). Stage 3 of a full build. The code lives on the build branch; this note says what changed, slice by slice, and why. Audited by the **Build Planner**; the anchor of the **security pass** when the plan rated its surface high. Header fields per [artifact-header.md](artifact-header.md).

**This note is the pass's final message.** The Builder runs on Codex in a `workspace-write` sandbox and writes nothing outside the worktree, so the launch form's `-o` saves the final message and the coordinator files it as `artifacts/change-note.md`, byte for byte. Write it as one message: the frontmatter first, then the sections, no preamble and no sign-off.

**No commit hashes here.** A `workspace-write` pass cannot commit. The note gives each slice's paths and its commit message, and the coordinator commits each slice as one commit group with exactly that message, so `git log --grep "<eng> S<n>"` recovers every hash. The local run is therefore at the base commit plus the uncommitted change, and says so.

```markdown
---
id: dc-eng-001.change
engagement: dc-eng-001-<slug>
date: 2026-10-16
seat: builder
stage: 3
model: codex gpt-6.1-sol high
grounding: pending
thin_lane: []
adjacent_lanes: []
target: seanwinslow28/<repo>
branch: <the build's branch>
base: <commit>
at: <HEAD when the pass ran> + uncommitted
exit: none                         # or "Blocked: spec and tests conflict", "Blocked: budget", …
revision: 1
stale_from: null
status: draft
auditor: build-planner
audit: pending
plan: dc-eng-001.plan              # the plan revision built against
tests: dc-eng-001.tests            # the red record the suite was taken from
---

## Plan step → commit map

| Slice | Plan step | Paths changed | Commit message for the coordinator |
|---|---|---|---|
| S<n> | | `src/<x>.py` | `dc-eng-001 S<n>: <what>` |

## Deviations

Each declared with its reason, or `none`. An undeclared deviation is a defect the Planner's audit will find.

| Id | Plan line | What was done instead | Why |
|---|---|---|---|
| DV<n> | | | |

## Decisions

Choices made inside the plan's bounds, one row each, filed by the coordinator as ledger entries in this seat's name.

| Choice | Over | Because | Canon |
|---|---|---|---|

## Docs updated

`<path>`: what changed, or `none`. Prose that will be read as Sean is drafted plain and flagged here for the voice skills.

## Dependencies added

Each with the plan's exception id that named it. The coordinator installs it, with install scripts off; this seat never does.

| Package and version | Exception | Why |
|---|---|---|

`none`.

## Migration code

Migration code is source: written here, to the plan's data changes and, on a repair after Release has drafted, to Release's migration steps by id. The Verifier tests it.

| Path | Plan line or migration step (`MG<n>`) | Phase (expand, migrate, contract) |
|---|---|---|

`none`.

## Test files untouched

The visible suite's hash, by the recipe in [test-record.md](test-record.md), at `HEAD`, and the worktree's status over the test paths. The hash matches `tests_hash_red`; the status is empty.

**Command:** `git ls-tree -r HEAD -- <test paths> | shasum -a 256` → `<sha256>`
**Command:** `git status --porcelain -- <test paths>` → (empty)

No snapshot or golden file was regenerated.

## Local run of the Verifier's suite

Evidence, never certification: the change counts on the Verifier's final run and the gates.

**Ran at:** `<HEAD>` plus the uncommitted change above.
**Command:** `<exact command>`
**Output:**

    <pasted in full; past about 200 lines, the summary line and the tail, and the coordinator saves the whole from the raw log>

## Exit

On `exit: "Blocked: spec and tests conflict"`: the test (`T<n>`), the criterion (`AC<n>`), and the evidence that one cannot pass without breaking the other. The test is not edited, skipped or routed around. Omit this section when `exit: none`.

## Moves

<!-- MACHINE-READ by the rung-0 checker (craftwork/trace/check.py): move lines only, one per line,
     per artifact-header.md § The closing sections. A note goes in the pass record's ## Notes. -->

- kept — S<n> from dc-eng-001.plan
- kept — S<m> from dc-eng-001.plan

meter: <runtime> · <tokens> · <wall-clock>
```

**What attacks this change:** the Planner's audit, on its stake in [the seat file](../bench/build-planner.md#audit-duty); the security pass on a high surface; and the release gate, on [gate-schedule.md § Change note](gate-schedule.md#change-note) and the fixed security attack list.
