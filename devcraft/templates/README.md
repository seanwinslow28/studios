# Templates

Public machinery; filled artifacts are private, in the engagement folder of the private ledger (`ledger/engagements/<eng-id>/artifacts/`, `audits/`, `evidence/`). Every seat artifact opens with the shared header and closes with `## Moves` and a `meter:` line, defined once in [artifact-header.md](artifact-header.md). Every attack a gate runs has a named home in [gate-schedule.md](gate-schedule.md). Written on the Devcraft build map's **Artifact templates and the gate schedule** ticket (2026-10-11), on Productcraft's and Systemcraft's shapes.

**Law and standing behavior**

- [artifact-header.md](artifact-header.md): the shared frontmatter (build target, typed `exit:`, the fixed `auditor`), who writes which field, the status lifecycle, the exits, the artifact ids and item ids, and the closing sections.
- [seat-preamble.md](seat-preamble.md): the standing behavior every seat invocation carries, prepended verbatim to every dispatch on either vendor.
- [gate-schedule.md](gate-schedule.md): when the plan gate, the security pass and the release gate fire, their vendors and the switch rule, the automatic checks, the fixed security attack list, and the attack checklists per artifact.

**The four seat artifacts, in running order**

| Stage | Seat | Template | Audited by | Anchors |
|---|---|---|---|---|
| 1 Plan | Build Planner | [build-plan.md](build-plan.md) | Verifier | the plan gate |
| 2 Tests | Verifier | [test-record.md](test-record.md): the suite's map, the red record, the held-out slice, the final record | Release & Reliability | — |
| 3 Code | Builder | [change-note.md](change-note.md): the pass's final message | Build Planner | the security pass, on a high surface |
| 4 Release | Release & Reliability | [release-plan.md](release-plan.md): plan, runbook, drill record, gate packet | Builder | the release gate |

**The checks**

- [check-record.md](check-record.md): the record of each of the four audits, with each seat's stake and the verify stance.
- [gate-findings.md](gate-findings.md): the findings file of each gate, with Devcraft's typed verdicts (`PLAN | RELEASE | SECURITY`), the plan gate's frozen exceptions and the release gate's automatic checks.

**Handoffs**, under [the handoff contract](../../craftwork/handoff-contract.md), written on the map's **The two bindings and Devcraft's return templates** ticket (2026-10-11). A binding sits in the sending team's `templates/`, and its mirror in the receiving team's.

- [handoff-return-productcraft.md](handoff-return-productcraft.md): the return to Productcraft's execution breakdown, one line per story, plus the Gate 3 packet Productcraft relays when a Systemcraft design sits underneath. Its binding is [Productcraft's](../../productcraft/templates/handoff-binding-devcraft.md).
- [handoff-return-systemcraft.md](handoff-return-systemcraft.md): the return to a Systemcraft design, which is the candidate note that fires Gate 3. Its binding is [Systemcraft's](../../systemcraft/templates/handoff-binding-devcraft.md).
- [handoff-binding-systemcraft.md](handoff-binding-systemcraft.md): Devcraft's one crossing out, an AI-shaped architecture call sent to Systemcraft as a one-off ask, and the home of Devcraft's strip list. Its mirror is Systemcraft's [handoff-return-one-off.md](../../systemcraft/templates/handoff-return-one-off.md).

**Shared law, inherited by link from [craftwork/](../../craftwork/README.md):** the [ledger-entry schema](../../craftwork/templates/ledger-entry.md), the [runtime registry](../../craftwork/templates/runtime-registry.md), the [red-team protocol](../../craftwork/templates/red-team-protocol.md), the [close digest](../../craftwork/templates/close-digest.md) and the [status vocabulary](../../craftwork/templates/status-vocabulary.md).
