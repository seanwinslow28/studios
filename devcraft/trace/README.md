# trace — Devcraft's side of the shared trace kit

The kit itself lives in [craftwork/trace/](../../craftwork/trace/README.md): the record and labels templates, the rung-0 checker, the viewer, the registry numbers and the handoff freezer. This folder holds only what is Devcraft's, written at scaffold on 2026-10-08.

| File | What it holds |
|---|---|
| [studio.py](studio.py) | The profile the kit reads: the four seats as stages in a full build's running order (1 Plan, 2 Tests, 3 Code, 4 Release), the record kinds (`intake` for an arriving brief, `run` for the Verifier's final run), the closed audit cycle, the plan gate, the release gate and the security pass, and rung-0 line 8, which checks that a full build ran its own shape: tests and the plan gate before any code, and both gates on the record by Close |
| [taxonomy.md](taxonomy.md) | Devcraft's own seat failure modes. It is empty until its own labels earn one; the shared process-waste family is the kit's |

**Traced from dc-eng-001 on.** The kit finds this profile by walking up from the engagement folder, so the Close lines need no flag:

```bash
python3 craftwork/trace/check.py devcraft/ledger/engagements/<eng-id>
```

```bash
python3 craftwork/trace/render.py devcraft/ledger/engagements/<eng-id>
```
