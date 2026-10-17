# Templates

Public machinery; filled artifacts are private, in the engagement folder of the private ledger (`ledger/engagements/<project>-<YYYY-MM-DD>/artifacts/`, `audits/`, `evidence/`), and the media they cite stays in the engagement's media folder, by path and sha256. Every seat artifact opens with the shared header and closes with `## Moves` and a `meter:` line, defined once in [artifact-header.md](artifact-header.md). Every motion claim ships its evidence pack, whose fields are in [scene-record.md](scene-record.md). Written on the Motioncraft build map's **Artifact templates with the evidence-pack fields** ticket (2026-10-17), on Devcraft's shapes.

**Law and standing behavior**

- [artifact-header.md](artifact-header.md): the shared frontmatter (version folder, prior note, typed `exit:`, the fixed `auditor`), who writes which field, the status lifecycle, the exits, the artifact ids and item ids, the closing sections, and the four naming rulings.
- [seat-preamble.md](seat-preamble.md): the standing behavior every seat invocation carries, prepended verbatim to every dispatch on either vendor.

**The four seat artifacts, in running order**

| Stage | Seat | Template | Audited by | Anchors |
|---|---|---|---|---|
| 1 Story | Visual Story Director | [story-packet.md](story-packet.md): treatment, beat sheet, boards, timed animatic with scratch sound, shot list, muted copy | Finishing and Sound | the story gate |
| 2 Appearance | Art and Pose Designer | [appearance-packet.md](appearance-packet.md): style frame as separated painted layers, pose and smear plan, colour design, model notes, silhouette sheet, value study, master checksums | Visual Story Director | the appearance gate, with Finishing's assembled frame as proof |
| 3 Motion | Animator | [scene-record.md](scene-record.md): the moving test and its evidence pack; the pass's final message | Art and Pose Designer | the motion gate |
| 4 Finish | Finishing and Sound Designer | [delivery-package.md](delivery-package.md): conformed cut, composite, grade, sound plan, mix, delivery package, and the check record on the six technical checks plus loudness | Animator | — (the six checks, then Sean's yes) |

**The checks**

- [check-record.md](check-record.md): the record of each of the four audits, with each seat's stake, the three finding kinds and the verify stance.
- [gate-findings.md](gate-findings.md): the findings file of each gate, with Motioncraft's typed verdicts (`STORY | APPEARANCE | MOTION`), the evidence-present check and the questions for Sean.
- [directed-revision.md](directed-revision.md): the form for Sean's one change, and the motion gate's record of the three held checks.
- [labels-row.md](labels-row.md): what each column of a pass's row in `trace/labels.md` means here, and why it is never Sean's verdict on the film.

**The gates**

- [gate-schedule.md](gate-schedule.md): when the story, appearance and motion gates fire (once per half on a train in halves), what each reads and may demand, its vendor, Sean's decision after it, FAIL and re-runs, and the attack list for every artifact.

**Still to land here**, on its own map ticket: the two bindings with the interim words rule (**The two bindings and the interim words rule**).

**Shared law, inherited by link from [craftwork/](../../craftwork/README.md):** the [ledger-entry schema](../../craftwork/templates/ledger-entry.md), the [runtime registry](../../craftwork/templates/runtime-registry.md), the [red-team protocol](../../craftwork/templates/red-team-protocol.md), the [close digest](../../craftwork/templates/close-digest.md), the [status vocabulary](../../craftwork/templates/status-vocabulary.md) and the trace kit's [labels template](../../craftwork/trace/labels-template.md).
