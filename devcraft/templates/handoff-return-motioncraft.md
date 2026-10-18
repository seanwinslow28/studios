# Handoff return template — to Motioncraft

The return half of [the handoff contract](../../craftwork/handoff-contract.md) for a tool brief Motioncraft handed Devcraft. It mirrors [Motioncraft's binding for Devcraft](../../motioncraft/templates/handoff-binding-devcraft.md) and carries Devcraft's own strip list (below). Written by the **coordinator** in its Close pass, after the merge, because it holds only records: request states, commits, the release-gate verdict and holds. The **Build Planner** took the brief in, and Motioncraft's operator seat, the one the brief names, issues the state on arrival. Written on the Motioncraft build map's **The two bindings and the interim words rule** ticket, 2026-10-18.

Filled returns are **private** (`ledger/engagements/<eng-id>/handoff/outbound/return.md`); this template is public machinery. The note carries states and ids, never the reasoning behind them. **The note crosses alone, with no frozen copies:** the tool itself is in the target repo at the merge commit, and that is where Motioncraft reads it.

```markdown
---
id: dc-eng-001.return
engagement: dc-eng-001-<slug>
date: 2026-11-10
seat: coordinator
originates_from: mc-eng-001.handoff   # the brief this answers
answers_brief: mc-eng-001.handoff
target: seanwinslow28/<repo>
merge: <commit>                       # the merge commit on the target's default branch, from Sean's checkout
release_gate: NOT FIRED — TRIGGER NOT MET   # verbatim from its ledger entry, or the verdict when the type fired it
state: returned                       # returned | returned-partial (any request blocked)
---

## Requests

One row per request the brief asked for, by its id.

| Request | State | Record |
|---|---|---|
| RQ<n> | shipped | merged in `<commit>`; tests T<n>–T<m>; at `<path in the target>`, run as its README says |
| RQ<n> | cut | OUT<n> or RU<n> in dc-eng-001.plan |
| RQ<n> | blocked | <ticket link> |

## Overturned assumptions

Every Devcraft decision that supersedes something the brief assumed, such as a format the samples showed but the application does not export. Devcraft has already written `supersedes_external` on its entry. "None" is a legal row.

| Devcraft entry | Supersedes (Motioncraft entry) | What changed, one line |
|---|---|---|

## Holds

What the operator seat must see before a seat runs the tool on a film: owner · trigger · required record · if unmet, one line each. "None" is a legal row.

## Deferred

Only on `returned-partial`: each blocked request, why, and its rule-8 ticket.
```

## Filing

1. Copy `return.md` into Motioncraft's engagement `handoff/inbound/` (in `motioncraft/ledger/`, and push that ledger to its private remote). Append `returned · <date> · coordinator · <one line>` (or `returned-partial`) to `crossing.md` on both sides.
2. No copies cross, so `freeze.py` does not run. The strip list below stands so the pair's mirror is complete, and it is the same list as Devcraft's other mirrors.

## What is stripped from the copies

Devcraft's process parts, the same list as [Devcraft's binding for Systemcraft](handoff-binding-systemcraft.md#what-is-stripped-from-the-copies), where it is explained. A change to one is made to all four.

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
