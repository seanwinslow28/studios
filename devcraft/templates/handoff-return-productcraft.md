# Handoff return template — to Productcraft

The return half of [the handoff contract](../../craftwork/handoff-contract.md) for work Productcraft's execution breakdown handed Devcraft. It mirrors [Productcraft's binding for Devcraft](../../productcraft/templates/handoff-binding-devcraft.md) and carries Devcraft's own strip list (below). Written by the **coordinator** in its Close pass, after the merge, because it holds only records: story states, commits, the release-gate verdict and holds. The **Build Planner** took the brief in, and Productcraft's Delivery & Execution Lead issues the state on arrival. Written on the Devcraft build map's [bindings ticket](https://github.com/seanwinslow28/SWCB/issues/117), 2026-10-11.

Filled returns are **private** (`ledger/engagements/<eng-id>/handoff/outbound/return.md`); this template is public machinery. The note carries states and ids, never the reasoning behind them.

**The Gate 3 packet.** When the brief forwarded Systemcraft copies, Systemcraft's Gate 3 waits on this build, and Productcraft relays. The return then carries frozen copies of the change note, the test record and the release plan, and fills `## Gate 3 packet`. Delivery forwards the copies to Systemcraft byte for byte with its candidate note, and forwards Systemcraft's `gate3-note.md` back to Devcraft's `handoff/inbound/`. Go-live waits on that note.

```markdown
---
id: dc-eng-001.return
engagement: dc-eng-001-<slug>
date: 2026-10-20
seat: coordinator
originates_from: pc-eng-003.handoff   # the brief this answers
answers_brief: pc-eng-003.handoff
target: seanwinslow28/<repo>
merge: <commit>                       # the merge commit on the target's default branch, from Sean's checkout
release_gate: RELEASE PASS — QUALITY VERDICT ONLY 2026-10-18   # verbatim from its ledger entry, or NOT FIRED — TRIGGER NOT MET
gate3: n/a                            # n/a | waiting: eng-NNN — Systemcraft's Gate 3 waits on this build
state: returned                       # returned | returned-partial (any story blocked)
---

## Stories

One row per story the brief asked for, by its breakdown id.

| Story | State | Record |
|---|---|---|
| <story id> | shipped | merged in `<commit>`; tests T<n>–T<m> |
| <story id> | cut | OUT<n> or RU<n> in dc-eng-001.plan |
| <story id> | blocked | <ticket link> |

## Overturned assumptions

Every Devcraft decision that supersedes a Productcraft assumption, such as a story cut by a routed-upstream call Sean picked. Devcraft has already written `supersedes_external` on its entry; Delivery flips its own entry on reading this. "None" is a legal row.

| Devcraft entry | Supersedes (Productcraft entry) | What changed, one line |
|---|---|---|

## Implementation holds

The release gate's holds that go-live, or Gate 3, must see: owner · trigger · required record · if unmet, one line each. "None" is a legal row.

## Gate 3 packet

Only when `gate3:` is `waiting`. The three frozen copies in `artifacts/`, by id; the manifest holds the hashes.

| Id | Artifact | What Gate 3 takes from it |
|---|---|---|
| dc-eng-001.change | Change note | build identity, actual path and schema |
| dc-eng-001.tests | Test record | end-to-end positive and negative tests, the final record |
| dc-eng-001.release | Release plan | migrations, rollback and kill drills, instrument records, the Gate 3 evidence by hold |

## Deferred

Only on `returned-partial`: each blocked story, why, and its rule-8 ticket.
```

## Filing

1. On a Gate 3 build, freeze the three copies with the shared kit, using this file as the binding: `python3 craftwork/trace/freeze.py copy --binding devcraft/templates/handoff-return-productcraft.md --out <eng>/handoff/outbound/artifacts <eng>/artifacts/change-note.md=dc-eng-NNN.change <eng>/artifacts/test-record.md=dc-eng-NNN.tests <eng>/artifacts/release-plan.md=dc-eng-NNN.release`. It prints the table that is `manifest.md`. Run `freeze.py show` first to see what each copy loses. Otherwise no copies cross.
2. Copy `return.md`, and on a Gate 3 build `manifest.md` and `artifacts/`, into Productcraft's engagement `handoff/inbound/`. Append `returned · <date> · coordinator · <one line>` (or `returned-partial`) to `crossing.md` on both sides.
3. On a Gate 3 build, record Gate 3 as pending and open the dated go-live reminder ticket on SWCB, per the master skill's Close checklist.

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
