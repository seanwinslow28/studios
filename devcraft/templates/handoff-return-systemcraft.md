# Handoff return template — to Systemcraft

The return half of [the handoff contract](../../craftwork/handoff-contract.md) for a design Systemcraft handed Devcraft to build. It mirrors [Systemcraft's binding for Devcraft](../../systemcraft/templates/handoff-binding-devcraft.md) and carries Devcraft's own strip list (below). **This note is the candidate note.** It names the build that Gate 3 tests, and it travels with that build's evidence. The **coordinator** writes and sends it at once when the release gate passes, before the merge, because it holds only records: build identity, the verdict and the holds' evidence. The **Build Planner** took the brief in, and Systemcraft's Design Strategist issues the state on arrival, then fires Gate 3. Written on the Devcraft build map's [bindings ticket](https://github.com/seanwinslow28/SWCB/issues/117), 2026-10-11.

Filled returns are **private** (`ledger/engagements/<eng-id>/handoff/outbound/return.md`); this template is public machinery. The note carries records and ids, never the reasoning behind them.

```markdown
---
id: dc-eng-002.return
engagement: dc-eng-002-<slug>
date: 2026-11-20
seat: coordinator
originates_from: eng-007.handoff      # the brief this answers
answers_brief: eng-007.handoff
target: seanwinslow28/<repo>
branch: <the build's branch>
base: <commit>
candidate: <commit>                   # the merge candidate the release gate and the final test run saw
merge: pending                        # pending | <commit>; the merge does not wait for Gate 3
release_gate: RELEASE PASS — QUALITY VERDICT ONLY 2026-11-19   # verbatim from its ledger entry
gate3: waiting                        # waiting until gate3-note.md arrives in handoff/inbound/
state: returned                       # returned | returned-partial
---

## Answers

One row per ask id in the brief.

| Ask id | Built | Record |
|---|---|---|
| Q1 | yes | slices S<n>–S<m>, commits by `git log --grep "dc-eng-002 S<n>"` |

## Holds

One row per Gate 2 hold the brief carried, by its Systemcraft id: where its evidence is, or why it is still open. The release plan's Gate 3 evidence holds the detail.

| Hold | Evidence | Closed? |
|---|---|---|

## Returned artifacts

The three frozen copies in `artifacts/`, by id. The manifest holds the hashes.

| Id | Artifact | What Gate 3 takes from it |
|---|---|---|
| dc-eng-002.change | Change note | build identity, actual path and schema |
| dc-eng-002.tests | Test record | end-to-end positive and negative tests, the final record |
| dc-eng-002.release | Release plan | migrations, rollback and kill drills, instrument records, the Gate 3 evidence by hold |

## Routed calls

Devcraft never overturns a design decision. A design decision the build could not follow went back as a routed-upstream call. Each one is named here by its RU id and how it was settled, or "none".

## New holds

The release gate's own holds that go-live must see: owner · trigger · required record · if unmet, one line each. "None" is a legal row.

## Deferred

Only on `returned-partial`: the part of the ask not built, why, and its rule-8 ticket.
```

## Filing

1. Freeze the three copies with the shared kit, using this file as the binding: `python3 craftwork/trace/freeze.py copy --binding devcraft/templates/handoff-return-systemcraft.md --out <eng>/handoff/outbound/artifacts <eng>/artifacts/change-note.md=dc-eng-NNN.change <eng>/artifacts/test-record.md=dc-eng-NNN.tests <eng>/artifacts/release-plan.md=dc-eng-NNN.release`. It prints the table that is `manifest.md`. Run `freeze.py show` first to see what each copy loses.
2. Copy `return.md`, `manifest.md` and `artifacts/` into Systemcraft's engagement `handoff/inbound/`. Append `returned · <date> · coordinator · <one line>` to `crossing.md` on both sides.
3. At Close, record Gate 3 as pending and open the dated go-live reminder ticket on SWCB. Go-live waits for `gate3-note.md` in this engagement's `handoff/inbound/` and Sean's go-live yes.

## What is stripped from the copies

Devcraft's process parts, the same list as [Devcraft's binding for Systemcraft](handoff-binding-systemcraft.md#what-is-stripped-from-the-copies), where it is explained. A change to one is made to all three.

```strip
heading: ## Moves
heading: ## Loopbacks
heading: ## Audit dispositions
heading: ## Budget
heading: ## Sean's yes
key: audit
key: stale_from
key: thin_lane
paragraph: **Repair note
paragraph: meter:
```
