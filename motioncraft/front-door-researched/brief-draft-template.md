# `brief-draft.md`: the brief in the master skill's own shape

The source the Motioncraft Open copies from (SWCB #267, lock 2; the Open line is next ticket 2). Exact headers, exact order, every section non-empty, written at synthesis from the sidecar alone. The master skill's `brief.md` header fields the room cannot know (the id, the pass budget, the roster) are left to Open; everything below is the room's.

```markdown
---
slug: <slug>
piece: <the piece's working name>
studio: motioncraft
type: <full-train | small-piece | one-off>   # the room's recommendation; Open decides
machine: <laptop | mini | either>
media: media:<piece>
sound_scope: <texture and accents only | ...>
concept: Planning/<slug>/concept.md sha256:<hash>
board: Planning/<slug>/board.md sha256:<hash>
hero_frame: Planning/<slug>/look/<file> sha256:<hash>
key_shots: [Planning/<slug>/look/<file> sha256:<hash>, ...]   # up to three waypoints, if rendered
sidecar: Planning/<slug>/session.md
written: <YYYY-MM-DD>
---

# <the piece's name>

<One breath: the film, the single objective, who feels it, where it lives. [L<n>]>

Takeout: <what a cold viewer thinks, feels or does when it ends, in one line>. [L<n>]

## Constraints

- **Length, ratio, frame rate, delivery:** <the numbers the channel fixed; the defaults when it fixed none>. [L<n>]
- **Approved elements, used unchanged:** <mc-ap-NNN, what it is>, or none.
- **Deadline:** <date | none>.
- **Spent already:** <Higgsfield credits the look stage used; nothing else>.
- **Attention:** <the stops Sean expects to give the train; the master skill's default when unsaid>.

## The asks

- ASK1: **<handle>:** <one thing the studio is held to, in a sentence a gate can read>. [L<n>]
- ASK2: ...

## What good looks like

- **Board rows that bind:** B<n> (<borrowed-what>), B<n> (...). Everything else on the board is context.
- **Hero frame:** `look/<file>` (sha256 above), **a taste reference, never a frozen look**: Art designs the style frame; this says which way it leans and why. <Sean's words on it, verbatim.>
  - **For:** <one sentence on what the frame is for>.
  - **Rules lifted from it:** <three to five checkable lines a reviewer could hold a frame to, e.g. "no smooth gradients; flat fills only">. The direction Art designs toward, never the look system.
- **Key shots:** <each by path: what must be true in that moment (who, what changes, what must read); restageable, its camera and composition open>.
- **The signature move's timing feel:** "<Sean's words, verbatim>" [<glossary term(s) in brackets, when the room is sure>].
- **Negatives in force:** N<n>, N<n>, by what he named wrong.
- **Where taste is judged:** <each review point where Sean judges taste and the thing he judges there, from the gate schedule (the look on the style frame at the appearance gate, the story on the animatic at the story gate, the move at the motion gate); the schedule's defaults when he names none>.

### What this is NOT

- <the nearest plausible wrong version, fenced: medium, register, joke, the rejected look by approvals id>
- ...

## Non-negotiables

- <one checkable directive per line: a frame count, a hold, a volume rule, a continuity rule, a muted-reading rule> [L<n>]
- ...

## Sound scope

<the scope in one line; a beat that needs more stops on Blocked: Sean's call. [L<n>]>

## Words

<"None", or each line Sean's or a `WP<n>` placeholder, each tagged `locked` or `draft`. [L<n>]>

## Stress test

<verdict: proceed (residuals: ...) | revise; Sean's decision in his words; the binding residuals already folded above, named here by the line they became. [L<n>]>

## Read-back

Before any thumbnail, the Director's intake restates in its own words the objective, the takeout and the non-negotiables, and lists what it cannot board from this brief. Sean accepts or corrects it; the answer lands in the engagement, never back in this file.

## Locks not in this brief

- [L<n>] <its handle>: <why it stays in `concept.md` or the sidecar: room procedure, a ceiling, register, a superseded call>.
- ...
```

## Rules

- **Every ASK line ends with its lock id.** A line with no lock does not ship; the structure check fails it.
- **Every lock reaches this file.** Each lock id in the sidecar is cited by a line above or listed under *Locks not in this brief* with its reason; a lock in neither fails the structure check. A superseded lock counts through the lock that supersedes it, and the bundle lock is written after the check.
- **How the film is built is a non-negotiable.** A lock that names the build tool, host or route (a code tool, Blender, a browser-built clip), even inside a style lock, becomes a non-negotiable line citing it, so Open cannot route the film another way by default (SWCB #276).
- **One thing per ASK line.** The story gate attacks "Intake that leaked": a line the Director's intake cannot map to one thing is a leak.
- **No boards in the brief.** No shot size, no duration per shot, no order of shots beyond the waypoints; the structure check fails a line that has one.
- **Checkable or absent.** A non-negotiable the gates could not verdict a frame against is moved to `concept.md` as register, or sharpened until it checks.
- **The hero frame is a reference.** The word "style frame" never appears in this file; the appearance gate's "A target passed as a design" is written for exactly that slip.
- **Sean's words stay his.** Where a line quotes him, it quotes; the room's gloss sits outside the quotation marks.
- **Nothing private, nothing that names an employer.** The file is copied into a ledger that goes to a private remote and cited in issues by path and hash; its text is still written as if a recruiter read it.
