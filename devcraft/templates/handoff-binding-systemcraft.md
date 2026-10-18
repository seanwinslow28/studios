# Handoff binding: Devcraft → Systemcraft, the one-off ask

Devcraft's side of one pair under [the handoff contract](../../craftwork/handoff-contract.md), the shared law every crossing between -craft teams follows. A build meets an AI-shaped architecture call that no Systemcraft design covers, such as a model choice, prompting versus fine-tuning, retrieval or eval design. Systemcraft answers it as a one-question job, and the build resumes around the answer. The route is the [architecture-call ruling](https://github.com/seanwinslow28/SWCB/issues/107), and this binding is how the call crosses (ruled by Sean, 2026-10-11, on the [bindings ticket](https://github.com/seanwinslow28/SWCB/issues/117)). The contract holds the law. This file names only what is particular to the pair (contract § 9). The two packets are the brief below and Systemcraft's [handoff-return-one-off.md](../../systemcraft/templates/handoff-return-one-off.md) (the mirror).

This is the only crossing Devcraft sends. The other direction, a finished design for Devcraft to build, is [Systemcraft's binding for Devcraft](../../systemcraft/templates/handoff-binding-devcraft.md).

## What crosses

| # | What | Source id | Owner |
|---|---|---|---|
| 1 | The paused build plan, at its current revision, with `exit: "Blocked: architecture call"` and the call in its `## Exit` and `## Routed upstream` row | `dc-eng-NNN.plan` | Build Planner |

On a call found after the plan gate, the copy is the plan amendment that carries the call. Nothing is forwarded: copies Devcraft received from a third team stay home. If the Architecture Advisor cannot answer without them, it says so (`input-required`), and the call goes to Sean, because it needs a design, not a one-off.

**Also stays behind** (beyond the contract's list): the test record, the change note and every code diff. The call is about how to build, so the plan carries it.

**`local`-class work never crosses.** A build in the `local` privacy class routes its AI-shaped call to Sean instead, because Systemcraft's ledger leaves the Mac Mini.

## The brief

Private, at `ledger/engagements/<eng-id>/handoff/outbound/brief.md`. The plan copy travels beside it.

```markdown
---
id: dc-eng-001.handoff
engagement: dc-eng-001-<slug>
date: 2026-10-14
seat: build-planner
ledger_entry: dc-eng-001.d05          # the entry that decided to hand off (hands_off_to set there)
trigger: ai-shaped-call
routed: RU<n>                         # the plan's routed-upstream row this asks about
receive_as: one-off                   # Systemcraft's bounded one-off question
return_by: 2026-10-17                 # a miss is a variance question before the date; the build waits
gate: pending                         # the outbound gate: pending | PASS <date> | PASS WITH ACCEPTANCES <date>
state: null                           # written by Systemcraft's Architecture Advisor: accepted | input-required | rejected
---

## The ask

The call, as one question or a few on the same call, each with an id the return answers by.

| Id | Question | Why it is Systemcraft's |
|---|---|---|
| Q1 | | AI-shaped: <model choice, prompting or fine-tuning, retrieval, eval design> |

## Referenced artifacts

| Source id | Artifact | What Systemcraft should take from it |
|---|---|---|
| dc-eng-001.plan | Build plan, paused at the call | the call in `## Exit` and its RU row; the scope, interfaces and security surface the answer must fit |

## Constraints

What the answer must fit, each line pointing at the plan section that states it: what is fixed upstream, the run-cost envelope, the privacy limits, and the build's deadline.
```

## When it fires, and who sends and receives

| Engagement | Trigger | Files and drafts the brief | Systemcraft receives it as |
|---|---|---|---|
| Full build | A routed-upstream row of kind AI-shaped, with no Systemcraft design covering it | Build Planner, in the pass that met the call | *Bounded one-off question* (`receive_as: one-off`), one seat: the Architecture Advisor |
| Small ask, ops-only, one-off | Never directly. They have no plan to carry the call, so the type that meets one stops and re-opens as a full build, and the call crosses from that build's plan | — | — |

**A no-handoff verdict** is written on every routed-upstream row the trigger was checked for and did not fire: "no handoff: <a covering design wins, eng-NNN | the call is not AI-shaped, decision memo>", with `hands_off_to: none`.

- **The outbound gate** runs on Codex: the Planner drafts on Claude. Its passes count inside the build's cap, and a cap they would break is the variance question to Sean.
- **The intake check on arrival** is the Architecture Advisor's, at Systemcraft's Open.
- **The return is read by** the Build Planner, in the resume pass that finishes the plan around the answer. Its intake check writes `informed_by` and sets the RU row's status to `answered <date> → eng-NNN.dNN`.

**The answer binds like a covering design.** The plan gate attacks the plan built around it, never the answer. A finding against the answer itself goes to Sean once, as a hold. If the one-off finds the call needs a design (dependent decisions, a hard-to-reverse commitment), it stops under Systemcraft's own rule and its return says so. The build then waits on Sean, who may open a Systemcraft design, and that design crosses back under Systemcraft's binding as the covering design.

## The return's gate

None. A one-off has no gate, so its return fires at Systemcraft's Close and carries the note alone, with no copies, because a one-off writes one decision entry and no artifact ([contract § 5](../../craftwork/handoff-contract.md#5-what-comes-back-the-mirror)). No later Systemcraft gate waits on this build, and no candidate note is sent.

## What counts at D+14

For Systemcraft's one-off: the plan finished around the answer and passing the plan gate is dependent work begun, and counts.

## What is stripped from the copies

The process parts of Devcraft's seat artifacts, from [artifact-header.md](artifact-header.md): the closing `## Moves` and `meter:` line, the process notes (`**Repair note …**` paragraphs, `## Loopbacks`, `## Audit dispositions`), the coordinator's `audit:` and `stale_from:` history, the `thin_lane` key, the plan's `## Budget` and the release plan's `## Sean's yes`. The `## Exit` section stays, because it carries the call. The same list strips Devcraft's copies in its three return templates ([to Productcraft](handoff-return-productcraft.md), [to Systemcraft](handoff-return-systemcraft.md), [to Motioncraft](handoff-return-motioncraft.md)), and a change to one is made to all four. Tested on 2026-10-11 against a filled build plan and release plan from the templates, with every process-note form added: every named part stripped, and nothing else.

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

A note that leaks anyway is the outbound gate's *reasoning that crossed* finding, and the fix is a new line here and in the three return templates.
