# Handoff return template — to Scriptcraft

The return half of [the handoff contract](../../craftwork/handoff-contract.md) for a locked script or beat sheet Scriptcraft hands Motioncraft to make into a film. It carries Motioncraft's own strip list (below) and Motioncraft's side of what the pair's binding names. Written on the Motioncraft build map's **The two bindings and the interim words rule** ticket, 2026-10-18.

**Scriptcraft does not exist yet** ([Explore Scriptcraft](https://github.com/seanwinslow28/SWCB/issues/178)). A binding sits in the sending team's `templates/` (contract § 9), so the binding for this pair is Scriptcraft's to write, as `scriptcraft/templates/handoff-binding-motioncraft.md`, when Scriptcraft is built. Until that file exists, no crossing can be taken: anything arriving from Scriptcraft is `rejected`, naming the missing binding. Until then every on-screen or spoken word is Sean's ([`motioncraft/CLAUDE.md`](../CLAUDE.md), rule 8).

**The other way in** is Sean's own idea or brief, which the Director breaks down the same way at the master skill's Open. It is not a crossing, and no return is written for it.

## Motioncraft's side of the binding

What Scriptcraft's binding must name (contract § 9), and the part of each that is Motioncraft's to fix. Scriptcraft writes the rest.

| § 9 item | Motioncraft's side |
|---|---|
| 1. The artifacts that cross | A locked script or beat sheet, plus the voice-over text, each scene carrying an id that stays fixed for the crossing: the **script id** the return answers by. What else crosses, and its ids, is Scriptcraft's |
| 2. The trigger, and how the receiver takes it | Fires after Scriptcraft's final gate passes. Motioncraft types the engagement at its own Open (`full-train`, or a small piece) under the handoff modifier its master skill carries. Scriptcraft never picks Motioncraft's type |
| 3. The seats | The **Visual Story Director** runs the intake check and issues the state on arrival, then breaks the script down (treatment, beats, shot list, plan) before anything is drawn, and writes the return. Who reads the return is Scriptcraft's |
| 4. The return's gate | Motioncraft's **story gate**, once Sean has approved the animatic it read. No later Motioncraft gate waits on Scriptcraft, so no candidate note is sent: a rewrite is a new crossing |
| 5. What counts at D+14 | For Motioncraft's engagement: the film published, or dependent work begun from it, the same measure as every Motioncraft film. Scriptcraft names what counts for its own work |
| 6. The strip list | Scriptcraft's, for its own artifacts. Motioncraft's is below, for this return |

**On arrival.** Each script id becomes one `ASK<n>` line in the story packet's intake, with the script id beside it, so every scene maps to beats, a routed question or an out-of-scope line, and none is dropped silently. The words arrive locked. No seat rewrites, trims or re-times a word to fit a shot: a change the film needs goes back on that scene's return line. "Scene" is Scriptcraft's word for its unit and is kept only in the script id. Motioncraft's own pieces of the film stay shots and sequences ([artifact-header.md](artifact-header.md), the four naming rulings).

## The return note

Private, at `ledger/engagements/<project>-<YYYY-MM-DD>/handoff/outbound/return.md`. Written by the Director in a pass of its own after Sean's decision on the animatic, because the durations come from the version he approved. **The note crosses alone, with no frozen copies:** boards and the animatic are media and stay in the media folder, and Scriptcraft works on words, so the lines and their durations are all it needs. The note carries states, durations and ids, never the reasoning behind them.

```markdown
---
id: mc-eng-001.return
engagement: <project>-<YYYY-MM-DD>
date: 2026-11-04
seat: visual-story-director
originates_from: <scriptcraft brief id>   # the brief this answers
answers_brief: <scriptcraft brief id>
animatic: animatic-vNN-<YYYY-MM-DD>       # the version Sean approved; every duration below is read from it
approval: <approvals entry id>            # his decision on that version, in the approvals ledger
frame_rate: 24
story_gate: STORY PASS <date>             # verbatim from the gate's ledger entry
state: returned                           # returned | returned-partial (a scene deferred, with its ticket)
---

## Script lines

One row per script id the brief carried, in script order. The duration is that scene's shots added up in the approved animatic, in seconds and frames at the frame rate above (ruled by Sean, 2026-10-18: one duration per script id).

| Script id | State | Duration | Shots | What must change |
|---|---|---|---|---|
| <script id> | boarded | 3.5 s · 84 f | SH<n>–SH<m> | — |
| <script id> | cut | — | — | — (the story decision that cut it, by id) |
| <script id> | needs rewrite | 2.0 s · 48 f | SH<n> | the line and what the film needs of it, as a fact: "voice-over runs 62 f; its shot holds 48 f", "on-screen word unreadable at its size in SH<n>" |

## Overturned assumptions

Every Motioncraft decision that supersedes something the script assumed, such as a scene Sean cut at the story gate. Motioncraft has already written `supersedes_external` on its entry. "None" is a legal row.

| Motioncraft entry | Supersedes (Scriptcraft entry) | What changed, one line |
|---|---|---|

## Holds

Every `needs rewrite` line is a hold: nothing under it is designed or moved until the rewrite re-crosses. "None" is a legal row.

## Deferred

Only on `returned-partial`: each deferred scene, why, and its rule-8 ticket.
```

**A rewrite is a new crossing** (contract § 1: a material change is a new crossing). The rewritten scenes arrive under Scriptcraft's binding again, and the shots they change take a new animatic version, its audit and the story gate as a fresh series, per [the gate schedule](gate-schedule.md#seans-decision-after-a-gate). Every other line goes on.

## Filing

1. The coordinator copies `return.md` into Scriptcraft's engagement `handoff/inbound/` and appends `returned · <date> · visual-story-director · <one line>` (or `returned-partial`) to `crossing.md` on both sides, then pushes `motioncraft/ledger/` to its private remote.
2. No copies cross, so `freeze.py` does not run. The strip list below stands so the pair's mirror is complete and a copy can cross the day Scriptcraft's binding asks for one.

## What is stripped from the copies

Motioncraft's process parts, the same list as [Motioncraft's binding for Devcraft](handoff-binding-devcraft.md#what-is-stripped-from-the-copies), where it is explained. A change to one is made to both.

```strip
heading: ## Moves
heading: ## Loopbacks
heading: ## Audit dispositions
key: audit
key: stale_from
key: thin_lane
paragraph: **Repair note
paragraph: meter:
```
