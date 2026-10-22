# Test record template — the test suite and its run record

Owned by the **Verifier** ([seat file](../bench/verifier.md)). Stage 2 of a full build. The suite itself lives in the target repo's test paths; this record is what the suite promises and what happened when it ran. Two passes write it: the **draft**, after the plan gate and before any code, writes the map, the security tests and the **red record**; the **`run`** pass, against the merge candidate, bumps `revision:` and fills the **final record**. A test that guessed wrong is fixed by the Verifier's own `repair` pass and listed under Repairs. Audited by **Release & Reliability**. Header fields per [artifact-header.md](artifact-header.md); written to `artifacts/test-record.md`, long output to `evidence/`.

The Builder receives this record with the red record filled. So the **held-out slice** (tests the Builder never sees, which catch code written to pass only the visible tests) appears here only as a count and a hash. The tests and their own red record live in the engagement folder's `held-out/`, which the coordinator never hands to a Builder pass: no Builder pass record lists it as an input. The slice is spent at the final run, when the Verifier stages it and the coordinator commits it to the build branch under the Verifier's context; a Builder repair after that runs against a suite that includes it, and the run record says so.

**The test-files hash** is one recipe, so the Builder and Release reproduce it exactly:

```bash
git ls-tree -r <commit> -- <test paths> | shasum -a 256
```

The held-out folder's hash: `find held-out -type f -print0 | sort -z | xargs -0 shasum -a 256 | shasum -a 256`, run from the engagement folder.

```markdown
---
id: dc-eng-001.tests
engagement: dc-eng-001-<slug>
date: 2026-10-15
seat: verifier
stage: 2
model: claude-opus-5-5
grounding: pending
thin_lane: []
adjacent_lanes: []
target: seanwinslow28/<repo>
branch: <the build's branch>
base: <commit>
at: <commit>                       # the red commit on the draft; the merge candidate after the run pass
exit: none
revision: 1                        # 1 at the draft; the run pass makes it 2 (repairs bump it too)
stale_from: null
status: draft
auditor: release-reliability
audit: pending
red_commit: <commit>               # the suite committed by the coordinator under this pass's context, no build code yet
candidate: pending                 # the merge candidate the final run ran against; filled by the run pass
tests_hash_red: <sha256>           # the recipe above, at red_commit
tests_hash_final: pending          # the recipe above, at candidate
held_out: 3 tests · <sha256>       # count and folder hash only; never names or contents
---

## Criterion → test map

Every criterion maps to at least one test, and every test to a criterion.

| Criterion | Test | File and name | Level | Seam |
|---|---|---|---|---|
| AC<n> | T<n> | `tests/test_<x>.py::test_<name>` | unit | `<module>.<function>` |

**Orphans:** criteria with no test, tests with no criterion: `none`, or each listed with its why.

## Security tests

Real attacks on the surface the plan rated, drawn from its Security & privacy surface section and the relevant chapters of OWASP ASVS 5.0.

| Id | Surface line it attacks | ASVS chapter | The attack | Passes when |
|---|---|---|---|---|
| ST<n> | untrusted input at `<path>` | V1 Encoding and Sanitization | | |

On a low surface with no attack worth writing: `none`, with the one-line why.

## Held-out slice

`<n>` tests, covering `<n>` criteria, in `held-out/` (hash in the header). Shown failing for the right reason in `held-out/red.md`. Never handed to the Builder.

## Red record

Run at `red_commit`, with no build code. Every test fails, and for the right reason: the behavior is missing, not an import error, a typo or a missing fixture.

**Command:** `<exact command>`
**Output:** `evidence/red-run.txt` (sha256 `<hash>`); the failing lines that show the reason are quoted below.

| Test | Failed? | The reason, from the output | Right reason? |
|---|---|---|---|
| T<n> | yes | `AssertionError: expected 1 line, got 0` | yes |

## Repairs

A test that guessed wrong, fixed by this seat's `repair` pass, never by the Builder and never silently.

| Test | What changed | Why | Repair pass |
|---|---|---|---|

`none`, until one happens.

## Final record

Filled by the `run` pass against the merge candidate. Real output only: a result that was not run is not a result.

**Commit:** `<candidate>`
**Environment:** OS and version, language and tool versions, the env vars the suite reads (by name), the fixtures the build created.
**Commands:** each one exactly, in order.
**Output:** `evidence/final-run.txt` (sha256 `<hash>`), with the summary line quoted here.

| Test | Result | Re-runs (flakes) | Note |
|---|---|---|---|
| T<n> | pass | 0 | |
| held-out, 3 | 3 pass | 0 | |

**Skipped tests:** must be `none`. Any other answer lists each skipped, disabled or quarantined test with the exception id (`EX<n>`) the plan named before the plan gate, or Sean's dated yes and its restore ticket.
**Test-files hash at the candidate:** `<sha256>`. It matches `tests_hash_red`, or the difference is exactly the commits under Repairs and the held-out slice's commit, each listed.
**Checks loosened:** coverage thresholds, lint or type suppressions, timeouts, CI edits: `none`, or each with its exception id.

## Moves

<!-- MACHINE-READ by the rung-0 checker (craftwork/trace/check.py): move lines only, one per line,
     per artifact-header.md § The closing sections. A note goes in the pass record's ## Notes. -->

- split — AC<n> → T<n>, ST<n> from dc-eng-001.plan
- kept — AC<n> from dc-eng-001.plan

meter: <runtime> · <tokens> · <wall-clock>
```

On the `run` pass the moves name the record's own tests (`- kept — T<n>–T<m> from dc-eng-001.tests`).

**What attacks this record:** Release's audit, on its stake in [the seat file](../bench/release-reliability.md#audit-duty), and the release gate, on [gate-schedule.md § Test record](gate-schedule.md#test-record).
