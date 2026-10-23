# A motion round on Higgsfield

For the rare piece whose signature move cannot be judged still (SWCB #267, locks 3 and 4). Claude hosts it through the `higgsfield-generate` skill and the `higgsfield` CLI, under the ceiling locked at the start, and nothing else spends. A clip here is a taste reference for the Animator and the motion gate, never a moving test, never authored craft (never-do 8), and never the only copy (never-do 13).

## When a motion round is allowed

All three hold: the stills walkthrough has settled the axis the move depends on (the medium at least); the grill's point 6 is locked, so the move and its timing feel are in Sean's words; and the question is one stills cannot answer (how the smear reads, how the tumble is paced, how the pull-back lands). A round opened to "see it move" with no question is refused with one line.

## The form, one per round, appended to the sidecar as the block header and option records

```
### motion:<axis> — round: n — host: higgsfield — cost: <credits for the three clips>
- observations: the question this round answers, in a line; the still(s) it starts from, by path under look/
- options:
  - id: motion:<axis>.a
    text: <the one variable this clip changes, named>
    model: <seedance-2.5 | seedance-2.0-fast>
    prompt: <terse imperative, one named style token, the full beat (approach, act, land); no "hold / settle / then" words that dampen the move>
    file: motion/round-NN-<axis>-a.mp4     # the .txt beside it holds the prompt, the model, the credits, "generated"
    tradeoff: <its cost to the piece if chosen>
    frame: orchestrator
    machine_fate_hypothesis: null
  - id: motion:<axis>.b ...
  - id: motion:<axis>.c ...
- recommendation: <the lean and why>
- open_questions: <what the clips could not settle>
- meter: <spent> / <ceiling> credits
```

## Rules

- **Defaults.** Seedance 2.5 for the read that will be cited; Seedance 2.0 Fast for a cheap first look at the pacing. The still it starts from is a captured `look/` frame, by path; a round from a text prompt alone is a stills question in disguise.
- **Three clips, one variable.** Each clip changes one thing (the spacing of the move, the length of the hold before it, the amount of smear), never the composition.
- **The meter is said before and after.** Quote the three clips' cost before submitting; a round that would cross the ceiling does not run, and the room asks Sean to raise it or stops the motion rounds. Credits spent are written into `brief-draft.md`'s constraints as "spent already".
- **Capture on creation.** Every clip downloaded to `motion/` with its `.txt` the moment it is ready; the Higgsfield URL is never the copy.
- **Sean's lean lands verbatim**, as a `[Ln] motion:<axis>: <option>, <file>` lock with his reason, before the next round or axis.
- **What a clip may bind.** Nothing but the timing feel in words: the lock quotes Sean on what the chosen clip got right, and that sentence goes to *What good looks like*. The clip's frames, spacing and model are never a non-negotiable; the Animator times the move, and the motion gate judges it in the glossary's words.
