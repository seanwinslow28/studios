# Handoff binding: Productcraft → Devcraft

Productcraft's side of one pair under [the handoff contract](../../craftwork/handoff-contract.md), the shared law every crossing between -craft teams follows. Productcraft's execution breakdown turns a design into stories; Devcraft builds them in Sean's own repos and says, story by story, what shipped. The contract holds the law (the brief, frozen copies, the five states, `crossing.md`, the mirror return, ids as the only thing that crosses). This file names only what is particular to the pair (contract § 9). The two packets are the brief, on [handoff-brief.md](handoff-brief.md)'s shape with the differences below, and Devcraft's [handoff-return-productcraft.md](../../devcraft/templates/handoff-return-productcraft.md) (the mirror, with Devcraft's own strip list). Written on the Devcraft build map's [bindings ticket](https://github.com/seanwinslow28/SWCB/issues/117), 2026-10-11.

## What crosses

| # | What | Source id | Owner | How |
|---|---|---|---|---|
| 1 | Execution breakdown | `pc-eng-NNN.breakdown` | Delivery & Execution Lead | frozen with this file's strip list |
| 2 | Every copy in the Systemcraft return Productcraft holds for the design under the breakdown | `eng-NNN.<slug>`, as they arrived on `eng-NNN.return` | Systemcraft | forwarded byte for byte, never re-frozen ([contract § 10](../../craftwork/handoff-contract.md#10-forwarded-copies)); only when a Systemcraft design sits under the breakdown |

Devcraft builds how, never what. It works from the breakdown's **implementation set** and the design copies, and never re-opens a story's scope or a design decision.

**The holds travel in the brief.** When a Systemcraft design sits under the breakdown, the brief's `## Holds to close` section copies each line of the Systemcraft return note's `## Implementation holds` unchanged, by its hold id. They are typed records, not reasoning, and the return note itself stays behind.

**Also stays behind** (beyond the contract's list): the design train's six artifacts and its Leadership packet, which framed what to build and are not Devcraft's to read; the Systemcraft return note itself; and the breakdown's design-set stories, which wait for a Designcraft team and are never part of the ask.

## The brief

On [handoff-brief.md](handoff-brief.md)'s shape, with four differences:

- `trigger: breakdown-filed` and `receive_as: build`. Devcraft's coordinator types each engagement at its own Open (`full-build`, or `small-ask` when a story passes its selection test). Several stories that no single plan carries become a series of builds, one engagement each, sharing a `series:` line, split at Open with Sean's yes. Productcraft never picks Devcraft's type.
- `## The ask` holds one row per implementation-set story, by its breakdown id, with its tracker issue. Its acceptance is in the breakdown copy, never restated.
- `## Referenced artifacts` lists the breakdown and, under a `Forwarded` line naming `eng-NNN.return` and its date, each forwarded copy.
- `## Holds to close` (above) replaces `## Constraints`. What the build may not change is fixed by the copies themselves.

## When it fires, and who sends and receives

| Engagement | Trigger | Files and drafts the brief | Devcraft receives it as |
|---|---|---|---|
| Execution breakdown | Its implementation-set stories are filed, and the target is one of Sean's own repos | Delivery, at the breakdown's close | `receive_as: build`, typed at Devcraft's Open |
| Full train, audit, one-off, role support | Never. Only a breakdown hands work to Devcraft | — | — |

**A no-handoff verdict** reads "no handoff: <why the stories are not Devcraft's to build>", for example a repo that is not Sean's, with `hands_off_to: none`.

- **The outbound gate** runs on Codex: Delivery drafts on Sonnet, so the vendor rule puts the gate there. It is the one gate an execution breakdown runs, and it gates the brief only.
- **The intake check on arrival** is Devcraft's Build Planner's, a `kind: intake` pass at Devcraft's Open.
- **The return is read by** Productcraft's Delivery & Execution Lead, in a Delivery one-off that takes it up. Productcraft's Open proposes it when it finds the return waiting in `handoff/inbound/`.

## The return's gate

Devcraft's **release gate**. The return fires at Devcraft's Close, after the merge, with one line per story: `shipped` (merged, with the commit), `cut` (with the plan's out-of-scope or routed-upstream id) or `blocked` (with its ticket). A blocked story makes the state `returned-partial`.

**When a Systemcraft design sits under the breakdown, Systemcraft's Gate 3 waits on this build, and Productcraft relays** (ruled by Sean, 2026-10-11, on the [bindings ticket](https://github.com/seanwinslow28/SWCB/issues/117)). Such a build always takes Release & Reliability and the release gate, whatever its type, because Gate 3 demands a drill record. Devcraft's return then also carries the **Gate 3 packet**: frozen copies of the change note, the test record and the release plan with its Gate 3 evidence, and the release-gate verdict and holds in the note. Delivery's take-up forwards that packet byte for byte to Systemcraft with its `candidate-note.md`, under [the Systemcraft binding](handoff-binding-systemcraft.md#the-returns-gate). Systemcraft answers Delivery with `gate3-note.md`, and Delivery forwards it unchanged into Devcraft's `handoff/inbound/`. Devcraft's go-live waits on that note and Sean's go-live yes. Every message stays between two teams that have a binding.

## What counts at D+14

For Devcraft's engagement: a story merged into the target's default branch and not reverted by D+14 is **shipped**, and counts. Delivery taking up the return counts too: that is dependent work begun.

## What is stripped from the copies

The process parts of the execution breakdown: [the Systemcraft binding's list](handoff-binding-systemcraft.md#what-is-stripped-from-the-copies), because Delivery writes its process notes in the same forms as every Productcraft seat ([artifact-header.md](artifact-header.md), Process notes), plus two lines for what only a breakdown carries: the `## Intake check` it ran on Systemcraft's return, and its `crossing_state` key. Story, epic, sprint, filed-issue and implementation-candidate content stays, and so do the `informed_by` and `return_note` ids. The forwarded Systemcraft copies are never stripped again: Systemcraft's strip stands (contract § 10).

```strip
heading: ## Intake check
heading: ## Moves
heading: ## Red-team checklist
heading: ## Loopbacks
heading: ## Audit dispositions
heading: ## Audit NOTE dispositions
heading: ## Repair dispositions
heading: ## Repair notes
heading: ## P0-equivalent check
key: audit
key: cosign
key: gate_1
key: thin_lane
key: crossing_state
paragraph: **Repair note
paragraph: **Revision
paragraph: Corpus opened
paragraph: What was on disk
paragraph: Hands forward,
paragraph: meter:
```

A note that leaks anyway is the outbound gate's *reasoning that crossed* finding, and the fix is a new line here.
