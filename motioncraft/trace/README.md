# trace — Motioncraft's side of the shared trace kit

The kit itself lives in [craftwork/trace/](../../craftwork/trace/README.md): the record and labels templates, the rung-0 checker, the viewer, the registry numbers and the handoff freezer. This folder holds only what is Motioncraft's, written at scaffold on 2026-10-17.

| File | What it holds |
|---|---|
| [studio.py](studio.py) | The profile the kit reads: the four seats as stages in a full train's running order (1 Story, 2 Appearance, 3 Motion, 4 Finish), the record kinds (`intake` for an arriving brief), the closed audit cycle, the story, appearance and motion gates, and rung-0 line 8, which checks that a full train ran its own shape: no motion before the appearance gate, and all three gates on the record by Close. A small piece's shape is unchecked until the master skill design rules it |
| [taxonomy.md](taxonomy.md) | Motioncraft's own seat failure modes. It is empty until its own labels earn one; the shared process-waste family is the kit's |

**Traced from mc-eng-001 on.** The kit finds this profile by walking up from the engagement folder, so the Close lines need no flag:

```bash
python3 craftwork/trace/check.py motioncraft/ledger/engagements/<eng-id>
```

```bash
python3 craftwork/trace/render.py motioncraft/ledger/engagements/<eng-id>
```
