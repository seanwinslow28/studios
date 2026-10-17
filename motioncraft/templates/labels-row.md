# Labels row — Sean's verdict on each pass, apart from his verdict on the film

Every Motioncraft pass gets one row in the engagement's `trace/labels.md`, in the shared kit's columns ([craftwork/trace/labels-template.md](../../craftwork/trace/labels-template.md), which governs; this file only says what the columns mean here). Written on the Motioncraft build map's **Artifact templates with the evidence-pack fields** ticket (2026-10-17), from brief 5, section 6.

**Two verdicts, never one for the other.** A label judges the *pass*: did this seat, this audit or this gate do its job on its inputs, within the evidence? It never judges the artistry. Sean's verdict on a *version* (approved, artistic retake, technical retake, rejected) is a separate entry in the approvals ledger, in his words, with the version id and a frozen copy's checksum. A pass can be labelled `pass` on a version Sean sent back for an artistic retake, and a version Sean approved can sit on a pass labelled `fail` for a missing evidence field. Neither file is ever filled from the other.

```markdown
| pass | verdict | first_failing_stage | critique | failure_code |
|---|---|---|---|---|
| pass-<nn> | fail | 3 | The contact frames are shown, but the frame-numbered copy is missing, so the squash claim at the first contact cannot be checked; ship the copy with the pack. | |
```

## The columns, as Motioncraft reads them

- **`pass`**: the pass id, `pass-NN`, matching one record in `trace/`.
- **`verdict`**: `pass` or `fail`, nothing between; or `defer`, a recorded "come back to this" that is not a verdict. "Mostly fine" fails.
- **`first_failing_stage`**: set on every fail, never on a pass: the stage where the problem *entered* the train, which may be upstream of the pass read. **1** Story, **2** Appearance, **3** Motion, **4** Finish. A motion pass that fails because the animatic gave a contact no frames has first failing stage 1.
- **`critique`**: one to three sentences a new hire could act on, on one line, with a pipe escaped as `\|`. In the glossary's words and the four naming rulings, pinned to frames where it is about frames. A taste call never appears here as a reason for a fail.
- **`failure_code`**: blank, which is the normal state. Motioncraft's own seat failure modes are none yet ([../trace/taxonomy.md](../trace/taxonomy.md)); a code from the shared process-waste family is allowed. A shape that recurs before it earns a code is written into the taxonomy file as sighted, not coded: "floaty weight", by the earlier tests' history, is the likely first.

## When rows are written

Sean labels as he reads, during the train, and the Close sweep makes sure every pass has a row. Before the first engagement, the two warm-up exercises (the bouncing ball and the finishing test) label their passes the same way.

The kit's checker enforces the header, one row per pass, the verdict values, and a stage on every fail ([craftwork/trace/README.md § Rung 0](../../craftwork/trace/README.md#rung-0--what-the-checker-asserts-and-what-it-cannot-see), lines 3 and 10).
