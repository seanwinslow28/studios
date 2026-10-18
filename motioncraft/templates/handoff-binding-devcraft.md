# Handoff binding: Motioncraft → Devcraft, the tool brief

Motioncraft's side of one pair under [the handoff contract](../../craftwork/handoff-contract.md), the shared law every crossing between -craft teams follows. A seat does a pipeline job by hand that software should do, such as turning the animatic's cut list into a Resolve timeline, batch-renaming a painted layer sequence or checking a render's frame count. Devcraft builds the tool in one of Sean's own repos and says, request by request, what shipped. Pipeline software is Devcraft's ([`motioncraft/CLAUDE.md`](../CLAUDE.md), rule 4). The contract holds the law. This file names only what is particular to the pair (contract § 9). The two packets are the brief below and Devcraft's [handoff-return-motioncraft.md](../../devcraft/templates/handoff-return-motioncraft.md) (the mirror, with Devcraft's own strip list). Written on the Motioncraft build map's **The two bindings and the interim words rule** ticket, 2026-10-18.

**The film never waits on Devcraft** (ruled by Sean, 2026-10-18, on that ticket). The seat does the job by hand, records what it did, and the request crosses at Close, so the tool serves later films. A pass that truly cannot go on by hand returns with `exit: "Blocked: Sean's call"`, and whether to wait is then his decision.

## What crosses

| # | What | Source id | Owner |
|---|---|---|---|
| 1 | The seat artifact in which the job was done by hand, at its current revision: the story packet, appearance packet, scene record or delivery package | `mc-eng-NNN.<story \| appearance \| motion \| finish>` | the seat that wrote it, which is the brief's operator |

One copy only, from the operating seat. It is the record of how the job was done by hand, which is the tool's working spec. Nothing is forwarded: copies Motioncraft received from Scriptcraft stay home.

**Samples cross as files made for the brief, never production material.** Each sample is a synthetic stand-in at the real format (frame size, rate, layer naming, file type), made by the operating seat in the engagement's media folder under `handoff/samples/`, and named in the brief by `media:` path and sha256. A sample may become a test fixture in a repo, and Devcraft's Builder runs on Codex, so a production frame, render, board or approved layer never stands in as one (never-do 6 and the privacy law, [`motioncraft/CLAUDE.md`](../CLAUDE.md), rule 1). A request that cannot be judged without production media goes to Sean as a question, never across.

**Also stays behind** (beyond the contract's list): check records, gate findings and the approvals ledger; every media file except the samples; and the other three seat artifacts.

**A tool that would make a frame, an in-between or a look is not pipeline software and never crosses** (never-do 8). Devcraft builds how a job runs, never what the film looks like.

**`local`-class work never crosses.** A tool need met in a `local` engagement goes to Sean instead, because Devcraft's Builder runs on Codex.

## The brief

Private, at `ledger/engagements/<project>-<YYYY-MM-DD>/handoff/outbound/brief.md`. The artifact copy travels beside it in `artifacts/`; the samples stay in the media folder.

```markdown
---
id: mc-eng-001.handoff
engagement: <project>-<YYYY-MM-DD>
date: 2026-11-02
seat: finishing-sound-designer        # the operating seat, which drafts the brief
operator: finishing-sound-designer    # the one seat that will run the tool, one operator per application (rule 5)
application: "DaVinci Resolve <version>"   # the application and version the tool must work with, or "none" for a standalone tool
ledger_entry: mc-eng-001.d<NN>        # the entry that decided to hand off (hands_off_to set there)
trigger: tool-need
receive_as: build                     # Devcraft types it at its own Open; Motioncraft never picks Devcraft's type
target: seanwinslow28/<repo>          # the repo of Sean's own the tool lands in, named by Sean at Close
gate: pending                         # the outbound gate: pending | PASS <date> | PASS WITH ACCEPTANCES <date>
state: null                           # written by Devcraft's Build Planner: accepted | input-required | rejected
---

## The ask

One row per tool, by its request id; the return answers by these ids. What the tool takes in and gives back is stated here; how the job was done by hand is in the copy, cited by item id, never restated.

| Id | The job | Done by hand in | Takes in | Gives back | Done when |
|---|---|---|---|---|---|
| RQ<n> | | `mc-eng-001.finish`, CUT<n>–CUT<m> | | | a check a fresh reader can run on the samples |

## Referenced artifacts

| Source id | Artifact | What Devcraft should take from it |
|---|---|---|
| mc-eng-001.finish | Delivery package | the steps done by hand, the formats and the frame counts the tool must match |

## Samples

| Id | Path | sha256 | Stands in for |
|---|---|---|---|
| RQ<n>-S<n> | `media:<film>/<project>-<YYYY-MM-DD>/handoff/samples/<file>` | | <what real material it mimics, by format only> |

## Constraints

What the tool must fit, each line pointing at where it is stated: the machine it runs on and the application's version; that it never writes inside the media folder's `approved/` or overwrites a saved version (rule 5); that it runs without a network call unless Sean approved one; and the privacy class.
```

## When it fires, and who sends and receives

| Engagement | Trigger | Files and drafts the brief | Devcraft receives it as |
|---|---|---|---|
| Full train, small piece | A seat did a pipeline job by hand that no installed tool or plugin does, and wrote it on its artifact as `adjacent_lanes: ["devcraft: <the job, one line>"]` | The operating seat, at the engagement's Close, in a pass of its own | `receive_as: build`, typed at Devcraft's Open (`full-build`, or `small-ask` when it passes Devcraft's selection test) |

**A no-handoff verdict** is written at Close on every `devcraft:` line that does not become a request: "no handoff: <why>", for example a job done once that no later film repeats, with `hands_off_to: none`. Sean sees both lists in the Close.

- **The outbound gate** runs on the vendor that did not write the brief: on Codex when Director, Art or Finishing drafted it on Claude, and on a fresh Opus 5.5 when the Animator drafted it on Codex. Its passes count inside the engagement's #158 limits, and a limit reached is a review and a decision for Sean.
- **The intake check on arrival** is Devcraft's Build Planner's, a `kind: intake` pass at Devcraft's Open.
- **The return is read by** the operator seat, in an intake pass at the Open of the next engagement after the return lands. It writes `informed_by`. A shipped tool joins that seat's toolbelt only under the plugin allowlist's rule (the map's **Plugin allowlist and launch form for seat runs** ticket), with Sean's yes; until then no seat runs it.

## The return's gate

Devcraft's **release gate**, where its type fires one. The return fires at Devcraft's Close, after the merge, with one line per request: `shipped` (merged, with the commit), `cut` (with the plan's out-of-scope or routed-upstream id) or `blocked` (with its ticket). A blocked request makes the state `returned-partial`. No Motioncraft gate waits on the tool, so no candidate note is sent.

## What counts at D+14

For Devcraft's engagement: a tool merged into the target's default branch and not reverted by D+14 is **shipped**, and counts. A Motioncraft seat running it in a recorded pass counts too: that is dependent work begun.

## What is stripped from the copies

The process parts of Motioncraft's seat artifacts, from [artifact-header.md](artifact-header.md): the closing `## Moves` and `meter:` line, the process notes (`**Repair note …**` paragraphs, `## Loopbacks`, `## Audit dispositions`), the coordinator's `audit:` and `stale_from:` history, and the `thin_lane` key. The `## Exit` section and the `adjacent_lanes:` line stay, because they carry the need. The same list strips Motioncraft's copies in [the Scriptcraft return](handoff-return-scriptcraft.md), and a change to one is made to both. Tested on 2026-10-18 against a filled scene record and delivery package from the templates, with every process-note form added: every named part stripped, and nothing else.

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

A note that leaks anyway is the outbound gate's *reasoning that crossed* finding, and the fix is a new line here and in the Scriptcraft return.
