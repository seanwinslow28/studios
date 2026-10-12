# Build plan template

Owned by the **Build Planner** ([seat file](../bench/build-planner.md)). Stage 1 of a full build, the anchor of the **plan gate**, and the only place an exception can be written: a skipped test, a credential file a seat may open, a dependency, a control file, the network allowlist and added test paths count only if this plan names them before the plan gate (rule 9 of [`devcraft/CLAUDE.md`](../CLAUDE.md)). The diff check matches its hits against the exceptions as they stood when the plan gate ran. Audited by the **Verifier** before the plan gate. Header fields per [artifact-header.md](artifact-header.md); written to `artifacts/build-plan.md`.

The plan says *how*. What gets built, and the architecture, arrive with the intake or go upstream.

```markdown
---
id: dc-eng-001.plan
engagement: dc-eng-001-<slug>
date: 2026-10-14
seat: build-planner
stage: 1
model: claude-opus-5-5
grounding: full
thin_lane: []
adjacent_lanes: []
target: seanwinslow28/<repo>
branch: <the build's branch>
base: <commit>
at: none
exit: none
revision: 1
stale_from: null
status: draft
auditor: verifier
audit: pending
intake: brief.md                   # the brief, plus the breakdown or design ids it carries
crossing_state: n/a                # accepted | input-required | rejected after an intake check; n/a for Sean's direct ask
surface: low                       # low | medium | high; high on any one of the seven triggers
security_pass: not scheduled       # scheduled on high, never otherwise
---

## Intake

What arrived and its crossing state. Every story id, design-hold id or direct-ask line (`ASK<n>`) maps to a criterion, an out-of-scope line or a routed-upstream line. Nothing is dropped silently. Cite by id; never restate.

| Intake item | Becomes | Note |
|---|---|---|
| ASK<n> | AC<n>, AC<m> | |
| ASK<n> | OUT<n> | Sean's spec fixed this; outside the build |

## Goal and acceptance criteria

The goal in one sentence. Then the criteria, numbered, each observable: a person or a test can watch it happen and say yes or no. "Works" and "is robust" are not criteria.

| Id | Criterion | Seam and level | Intake |
|---|---|---|---|
| AC<n> | `<command>` writes one line per <thing> to `<path>`, read back by the test | `<module>.<function>` · unit | ASK<n> |
| AC<n> | | · integration | ASK<n> |

## Scope

**In:** the files and modules this build may change, one per line. A file not named here is outside the build.

**Out:**

| Id | Out of scope | Why |
|---|---|---|
| OUT<n> | | |

## Approach and slices

The approach in a paragraph, with its why-A-over-B and its canon line. Then the slices, in the order they are built. Each merges on its own and leaves the suite no redder than it found it.

| Slice | What it changes | Criteria it turns green | Merges alone because | Undone by |
|---|---|---|---|---|
| S<n> | | AC<n> | | reverting its commit group |

**Why this over that:** <chosen> over <strongest alternative>, because <reason>.
**Canon:** <title and idea, in your own words> · or `none`.

## Interfaces and data changes

Public interfaces touched, data schemas, stored formats, jobs and schedules. Each was fixed upstream (cite it) or is routed (see Routed upstream); none is decided here.

| Change | Fixed by | Note |
|---|---|---|

**Ops paths flagged for Release.** This list is Release's write zone for the build, and the Builder is denied every path on it.

| Id | Path | What it is (job, schedule, CI workflow, rollback script, config) | Why it changes |
|---|---|---|---|
| OP<n> | | | |

## Test seams

Where the Verifier hooks in. Test paths: the repo's `.devcraft/test-paths` floor (its hash: `<sha256>`) plus the additions below. A plan may add paths, never remove one.

| Criterion | Seam | Level (unit, integration, end-to-end) | Fixtures the build creates | Edges a test may fake (network, clock, outside service) |
|---|---|---|---|---|
| AC<n> | | unit | | |

**Test paths added:** `<path>` because <reason>, or `none`.

## Security & privacy surface

What is valuable here, where untrusted input enters (prompt injection included), which secrets are touched (by name only), which dependencies are new, and which hosts the build talks to.

| Trigger (any one makes the surface **high**) | Hit? | Evidence |
|---|---|---|
| Login or access control | no | |
| Crypto | no | |
| A network-facing service | no | |
| Personal or private data, Sean's own included | no | |
| Money, including anything that can run up a bill | no | |
| An AI model that reads outside text and can act on it | no | |
| Data sent to an outside service | no | |

An API key alone is not a trigger, and no hit is argued down. **Rating: low | medium | high**: high on any hit; otherwise low or medium with a one-line why (only high changes the schedule). On high, the security pass is scheduled and the header says so.

**Untrusted input enters at:** <path or interface, and what reads it>.
**Secrets, by name:** `<ENV_NAME>` read at runtime by `<module>`; tests use a fake.

## Exceptions

Written here, before the plan gate, or nowhere. A plan edited mid-build never adds one. One row each; the diff check matches its hits to these ids.

| Id | Kind (skip, credential file, dependency, control file, host) | Exactly what | Why | For which seat |
|---|---|---|---|---|
| EX<n> | dependency | `<package>==<version>`, on its registry since <date>, maintainers <names>, installed with scripts off | | builder |

**Network allowlist for the build:** `<host>`, or `none`.

## Reversibility and risks

Per slice, what undoes it. Then each step that cannot be undone, named as one, with what Sean would be accepting. Then the risks, most likely first.

## Routed upstream

Product and architecture calls this build met, sent on, never decided here. Where the call goes depends on its kind: a covering Systemcraft design wins; an AI-shaped call goes to a Systemcraft one-off; any other gets a decision memo below, and the plan waits for Sean's pick.

| Id | The call | Kind | Sent to | Status |
|---|---|---|---|---|
| RU<n> | | other | Sean, by decision memo | picked <date> → <ledger entry id> |

**Decision memo, RU<n>.** Two or three options, each with its why-A-over-B, an order-of-magnitude cost and the canon it leaned on. Sean's pick, dated, and the ledger entry naming him as decider. The plan is finished around the pick.

## Budget

| Budget | Engagement | Per pass | Stop at 90% |
|---|---|---|---|
| Passes | | — | |
| Tokens | | | |
| Wall-clock | | | |
| Cash | | | |

## Moves

<!-- MACHINE-READ by the rung-0 checker (craftwork/trace/check.py): move lines only, one per line,
     per artifact-header.md § The closing sections. A note goes in the pass record's ## Notes. -->

- split — ASK<n> → AC<n>, AC<m> from brief.md
- dropped — ASK<n> from brief.md; out of scope as OUT<n>

meter: <runtime> · <tokens> · <wall-clock>
```

**What attacks this plan:** the Verifier's audit, on its stake in [the seat file](../bench/verifier.md#audit-duty), and the plan gate, on [gate-schedule.md § Build plan](gate-schedule.md#build-plan).
