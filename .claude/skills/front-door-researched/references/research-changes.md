# What the research changed in this copy of the room

`front-door-researched` is a trial copy of `front-door` (SWCB #269), cut from the studios branch `claude/267-front-door` at d0815f9 and kept beside the original until the compare (SWCB #267, next ticket 6) picks one. This file is what the compare reads and what a merge needs: every change Sean accepted, the pass and finding behind it, and every finding he declined or that was not put as a change.

The five passes are the front-door research track (SWCB #268), in SWCB at `raw/research/2026-10-23-front-door-*.md`. Sean ratified all five on 2026-10-23 in a live session: passes 1, 2, 4 and 5 as written, pass 3 with one amendment recorded in its header (assets his employer owns and has cleared him to use are clean inputs, like his own work; other people's work is reference and aspiration only, never in a final piece). Each change below was put to him as "change X to Y, because pass N says Z" and accepted with a yes; none was rewritten. A finding is the reason for a change; no research text was pasted into the room.

Besides these, the copy renames everything that names the room (the skill name, the invocation `/front-door-researched <studio> <idea>`, the lens folder `motioncraft/front-door-researched/`, the Codex link `.agents/skills/front-door-researched`, the sidecar's `skill:` stamp, and the links between them), and its description says it is a trial copy. No index rows were added: `bin/canary-check.sh` does not need them.

## Accepted

| # | File | What changed | Pass and finding |
|---|---|---|---|
| 1 | `lens.md`, `brief-draft-template.md` | Point 1 becomes the single objective and its takeout (what a cold viewer thinks, feels or does when it ends); the brief-draft gains a `Takeout:` line under the opening breath | 1, finding 2: evaluation agreed in the brief before work starts |
| 2 | `brief-draft-template.md` | *What good looks like* gains "Where taste is judged": each review point and what Sean judges there, from the gate schedule | 1, finding 1: taste is judged at named gates on named artefacts |
| 3 | `lens.md`, `brief-draft-template.md` | The constraints move from point 8 to point 4, beside where it lives (points renumbered; point 6 references became 7); the brief-draft's Constraints section moves above The asks | 1, finding 3: objective, audience and budget are the backbone, set together |
| 4 | `lens.md` | Sound and words: every word, read aloud at an ordinary pace, fits inside the length | 1, finding 3: the words-fit-the-length check |
| 5 | `brief-draft-template.md` | A closing *Read-back* section: the Director's intake restates objective, takeout and non-negotiables and lists what it cannot board, before any thumbnail; Sean accepts or corrects. The Director acts on it only if the master skill reads it, which is outside this ticket | 1, finding 6, and 4, finding 7: a brief is done when the receiver plays it back |
| 6 | `SKILL.md` | Micro-expand: two premises Sean will not choose between become two pieces, two slugs, two bundles, never a blend | 1, finding 7: one brief, one strategy |
| 7 | `lens.md` | The first never becomes "never designs the look system", naming the system (colour script, colour keys, model sheets, palette and line as a system) as Art's | 4, finding 4 and "Testing the two nevers" |
| 8 | `lens.md`, `brief-draft-template.md` | Key frames capped at four (the hero and up to three waypoints), each restageable, not a shot: what must be true in that moment, camera and composition open | 4, findings 2 and 3 |
| 9 | `lens.md` | Point 7: the hero moment placed in the shape of the piece in words, never seconds, frame counts or a beat order beyond the waypoints | 4, finding 5 |
| 10 | `lens.md`, `brief-draft-template.md` | Every word line tagged `locked` or `draft` | 4, finding 6 |
| 11 | `brief-draft-template.md` | Rule: no boards in the brief (no shot size, no per-shot duration, no shot order beyond the waypoints) | 4, finding 1 |
| 12 | `stress-test-rubric.md` | Step 8: the reviewer names problems, never shots | 4, finding 8 |
| 13 | `lens.md`, `chatgpt-opening-prompt.md` | The three options differ in kind, never three steps on one dial; a dial round is said to be one | 2, finding 1: the compromise effect |
| 14 | `SKILL.md`, `chatgpt-opening-prompt.md`, `sidecar-contract.md` | Each round names what was held and the one thing that varies; the look block gains `held:` and `varies:` | 2, finding 2 |
| 15 | `sidecar-contract.md` | A mix lock names which element came from which option | 2, finding 3 |
| 16 | `chatgpt-opening-prompt.md` | Capture-back takes what is wrong with the other two, in Sean's words, and offers it to the negatives table on his yes | 2, findings 4 and 5 |
| 17 | `brief-draft-template.md` | Under the hero frame: what it is for, in one sentence, and three to five checkable rules lifted from it, as the direction Art designs toward, never the look system | 2, finding 6 |
| 18 | `lens.md`, `motion-round-form.md` | At least one motion round on the leading direction before the look locks, unless Sean waives it in the sidecar; further rounds as before | 2, finding 7 |
| 19 | `lens.md` | Waypoints chosen so each stresses something different (an action, a travel, a face) | 2, finding 7 |
| 20 | `board-template.md` | One input rule for every generator host: only Sean's own work, his earlier look frames, and assets his employer owns and has cleared him to use go in as images; the room never refuses or warns against cleared employer assets; everything else crosses as link and words; no photo of a real person; other people's work never appears in a final piece. Replaces the ChatGPT-only default | 3, finding 5, with Sean's ratified amendment |
| 21 | `board-template.md` | Borrowed names one free element, never a whole shot; not borrowed names the protected specifics left behind | 3, finding 1 |
| 22 | `board-template.md` | Negatives stay in words, never shown to a generator as images | 3, finding 3 |
| 23 | `board-template.md` | At least one board row from outside animation | 3, finding 2 |
| 24 | `chatgpt-opening-prompt.md` | Round rule 5 reversed: describe the style in words from the board; never name an artist, studio or work in a prompt, never look one up to copy it | 3, finding 6 |
| 25 | `chatgpt-opening-prompt.md` | The opening prompt's board lines carry the borrowed and not-borrowed words only, never the work's name or link (follows from 24) | 3, finding 6 |
| 26 | `lens.md` | "Family, not twin" before the hero frame locks: the frame beside each binding row's source, any match beyond the named element flagged for Sean. In the look stage, not the stress test, because the reviewer reads only the two text files | 3, finding 7 |
| 27 | `SKILL.md` | Step 0 refuses a `Planning/<slug>/` that already holds a `session.md` Sean has not named to resume, and asks for another slug, so the two rooms never overwrite each other | The ticket's open decision on colliding bundles |

## Declined

- Recommend sleeping on the bundle before Open (pass 1, finding 7): declined. The compare already runs on separate evenings, and it would add a step to every piece.

## Not put as a change

- Label the hero frame "reference only" (pass 1, finding 4): the room already calls it "a taste reference, never a frozen look".
- Keep both board tables (pass 1, finding 5), keep three options per round (pass 2, finding 1), keep the links-only storage rule (pass 3, finding 4), keep the two nevers' line (pass 4, finding 1): each confirms the room as written.
- What does not transfer (pass 1, finding 8; pass 2, finding 8; pass 3's closing note; pass 4's closing note): nothing to change.
- Pass 5, all findings: they govern the compare, not the room.
- The sidecar's header stamps name the room by file hash. Kept for the record; for pass 5's blind read, the compare strips them with any other mark that shows which room wrote a bundle.
