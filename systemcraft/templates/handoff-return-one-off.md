# Handoff return template — a one-off answer

The return half of [the handoff contract](../../craftwork/handoff-contract.md) for a single question another team asked Systemcraft as a one-off. Today that team is Devcraft, which sends an AI-shaped architecture call its build met ([Devcraft's binding for Systemcraft](../../devcraft/templates/handoff-binding-systemcraft.md)). Owned by the **Architecture Advisor**, the one seat a one-off runs, and written at Close. A one-off has no gate and writes one decision entry and no artifact, so **the note crosses alone, with no frozen copies** ([contract § 5](../../craftwork/handoff-contract.md#5-what-comes-back-the-mirror)). Devcraft's Build Planner issues the state on arrival. Written on the Devcraft build map's [bindings ticket](https://github.com/seanwinslow28/SWCB/issues/117), 2026-10-11.

Filled returns are **private** (`ledger/engagements/<eng-id>/handoff/outbound/return.md`); this template is public machinery. The answer states what to do and what it binds, never the why: that stays in the decision entry, referenced by id.

```markdown
---
id: eng-008.return
engagement: eng-008-<slug>
date: 2026-10-16
seat: architecture-advisor
originates_from: dc-eng-001.handoff   # the brief this answers
answers_brief: dc-eng-001.handoff
gate: none — one-off
state: returned                       # returned | returned-partial
---

## Answers

One row per ask id. The answer is what to do and the limits it sets, in one to three sentences. The entry holds the why.

| Ask id | Answer | Systemcraft entry |
|---|---|---|
| Q1 | | eng-008.d01 |

An answer that needs a design says so in its row: "no one-off answer: needs a design engagement", with the reason (dependent decisions, a hard-to-reverse commitment). The asking team then routes the call to Sean.

## Overturned assumptions

Every Systemcraft decision that supersedes an assumption in the asking team's plan. Systemcraft has already written `supersedes_external` on its entry. "None" is a legal row.

| Systemcraft entry | Supersedes (asking team's entry) | What changed, one line |
|---|---|---|

## Holds

What the build must prove for the answer to stand: owner · trigger · required record · if unmet, one line each. "None" is a legal row.

## Deferred

Only on `returned-partial`: the question not answered, why, and its rule-8 ticket.
```

## Filing

1. Copy `return.md` into the asking team's engagement `handoff/inbound/`. Append `returned · <date> · architecture-advisor · <one line>` to `crossing.md` on both sides.
2. Close per the master skill. Nothing is frozen, and no later gate waits.

**No strip list.** No copy crosses, so there is nothing to strip. A question whose answer would need an artifact to cross is a design, not a one-off.
