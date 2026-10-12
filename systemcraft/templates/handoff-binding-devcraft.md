# Handoff binding: Systemcraft → Devcraft

Systemcraft's side of one pair under [the handoff contract](../../craftwork/handoff-contract.md), the shared law every crossing between -craft teams follows. A Systemcraft design with no product parent goes straight to Devcraft to be built in one of Sean's own repos; Devcraft's release-gate evidence comes back and fires Gate 3. The contract holds the law (the brief, frozen copies, the five states, `crossing.md`, the mirror return, ids as the only thing that crosses). This file names only what is particular to the pair (contract § 9). The two packets are the brief below and Devcraft's [handoff-return-systemcraft.md](../../devcraft/templates/handoff-return-systemcraft.md) (the mirror, with Devcraft's own strip list). Written on the Devcraft build map's [bindings ticket](https://github.com/seanwinslow28/SWCB/issues/117), 2026-10-11.

**A design with a product parent never uses this binding.** It returns to Productcraft after Gate 2, and its build reaches Devcraft through Productcraft's execution breakdown, which forwards these same copies ([Productcraft's binding for Devcraft](../../productcraft/templates/handoff-binding-devcraft.md)).

## What crosses

Frozen copies of the five design artifacts, stripped of the process parts named below:

| # | Artifact | Source id | Owner |
|---|---|---|---|
| 1 | PRD | `eng-NNN.prd` | Design Strategist |
| 2 | ADR | `eng-NNN.adr` | Architecture Advisor |
| 3 | Failure-UX spec + model card | `eng-NNN.trust` | Interaction & Trust Designer |
| 4 | Eval plan | `eng-NNN.eval` | Evals & Evidence Architect |
| 5 | Ops/economics model + incident runbook | `eng-NNN.ops` | Ops & Economics Modeler |

**The holds travel in the brief.** Gate 2's open implementation holds, each copied unchanged from its ledger entry by hold id: owner · trigger · required record · fail-closed consequence. They are what the build must close before Gate 3 can pass.

Devcraft builds how, never what. A design decision it cannot build is a `Blocked: architecture call` on its side, and a covering design wins; it never overturns one.

**Also stays behind** (beyond the contract's list): gate findings, criteria deltas, revision snapshots and appendix files the five artifacts do not carry inside themselves.

## The brief

Private, at `ledger/engagements/<eng-id>/handoff/outbound/brief.md`. A typed packet of references; the five copies travel beside it.

```markdown
---
id: eng-007.handoff
engagement: eng-007-<slug>
date: 2026-11-02
seat: design-strategist
ledger_entry: eng-007.d40             # the entry that decided to hand off (hands_off_to set there)
trigger: design-complete-no-product-parent
receive_as: build                     # Devcraft types the engagement at its own Open
target: seanwinslow28/<repo>          # where the build lands; one of Sean's own repos
gate2: PASS WITH ACCEPTANCES 2026-11-01   # verbatim from its ledger entry
return_by: 2026-11-30                 # a miss is a variance question before the date
gate: pending                         # the outbound gate: pending | PASS <date> | PASS WITH ACCEPTANCES <date>
state: null                           # written by Devcraft's Build Planner: accepted | input-required | rejected
---

## The ask

What to build, one row per part, each pointing at the section of a copy that specifies it. Never restated.

| Id | Build | Specified in |
|---|---|---|
| Q1 | | eng-007.adr § |

## Holds to close

| Hold | Owner | Trigger | Required record | If unmet |
|---|---|---|---|---|

## Referenced artifacts

| Source id | Artifact | What Devcraft should take from it |
|---|---|---|
| eng-007.prd | PRD | |
| eng-007.adr | ADR | |
| eng-007.trust | Failure-UX spec + model card | |
| eng-007.eval | Eval plan | |
| eng-007.ops | Ops/economics model + incident runbook | |

## Stays behind

One line per pointer Devcraft may need to know exists, with the claim it supports.
```

## When it fires, and who sends and receives

| Engagement | Trigger | Files and drafts the brief | Devcraft receives it as |
|---|---|---|---|
| Design a new project | Gate 2 passes, the design has no product parent, and its build lands in one of Sean's own repos | Design Strategist, at Close | `receive_as: build`, typed at Devcraft's Open (normally `full-build`) |
| Audit, one-off | Never. An audit finding that needs code is a new design or Sean's direct ask to Devcraft | — | — |

**A no-handoff verdict** reads "no handoff: <why>", for example a design that will not be built yet, with `hands_off_to: none`.

- **The outbound gate** runs on the vendor that did not last write the brief ([craftwork § Model delegation](../../craftwork/law.md#model-delegation)).
- **The intake check on arrival** is Devcraft's Build Planner's, a `kind: intake` pass at Devcraft's Open.
- **The return is read by** the Design Strategist, whose intake check on it opens Gate 3.

## The return's gate

Devcraft's **release gate**. A build Gate 3 waits on always takes Release & Reliability and the release gate, whatever its type, because Gate 3 demands a drill record. At release-gate PASS, Devcraft's coordinator sends the return at once, before the merge: the return note is the candidate note (build identity and the release-gate verdict), with frozen copies of the change note, the test record and the release plan, whose Gate 3 evidence maps each hold to its record.

**Gate 3** stays Systemcraft's and fires on that packet. Its verdict goes back as `gate3-note.md` in Devcraft's `handoff/inbound/`, one line: `<verdict, verbatim> · <date> · <Systemcraft entry id> · holds still open: <hold ids> | none`. The merge does not wait for it; Devcraft's go-live does, along with Sean's go-live yes. A Gate 3 FAIL is a new crossing naming the failed holds, which Devcraft takes as a new build. The merged code does not go live.

## What counts at D+14

For Devcraft's engagement: the build merged into the target's default branch and not reverted by D+14 is **shipped**, and counts. Gate 3 firing on the return counts too: that is dependent work begun.

## What is stripped from the copies

The same five artifacts cross to Productcraft, so the list is [the Productcraft return's](handoff-return.md#what-is-stripped-from-the-copies), line for line. A change to one is made to both. Tested against eng-004's PRD and ADR on 2026-10-11: every named part stripped, and nothing else.

```strip
heading: ## Routed to other seats
heading: ## Audit state
heading: ## Version history
heading: ## Sean rulings
heading: ## One decision for Sean
heading: ## Acceptances Sean must sign
heading: ## Grounding
heading: ## Moves
heading-ending: ## disposition
heading-ending: ## dispositions
heading-ending: ## dispositioned
heading-tag: [Δ
key: audit
key: cosign
key: evals_cosign
key: cosign_touch
key: criteria_contributors
paragraph: *Toolbelt note
paragraph: END-OF-PASS
paragraph: meter:
```

A note that leaks anyway is the outbound gate's *reasoning that crossed* finding, and the fix is a new line here and in the Productcraft return.
