# trace — Motioncraft's side of the shared trace kit

The kit itself lives in [craftwork/trace/](../../craftwork/trace/README.md): the record and labels templates, the rung-0 checker, the viewer, the registry numbers and the handoff freezer. This folder holds only what is Motioncraft's, written at scaffold on 2026-10-17.

| File | What it holds |
|---|---|
| [studio.py](studio.py) | The profile the kit reads: the four seats as stages in a full train's running order (1 Story, 2 Appearance, 3 Motion, 4 Finish), the record kinds (`intake` for an arriving brief), the closed audit cycle, the story, appearance and motion gates and the self-check gate (SWCB #261), the other studios' folders among the paths an input may cite, and rung-0 line 8, which reads the brief's `type:` and `parts:`: a full train runs its own shape (no motion before the appearance gate, all three gates on the record by Close), a train in parts counts stages 2 and 3 per part, a small piece runs only stages 3 and 4 and the motion gate, and a one-off is not asserted. Three drafts are not the stage's one draft and are named in notes (SWCB #246): Finishing's assembled frame when the appearance gate's `proof:` names it, a draft whose artifact `answers:` a ticket (the camera prototypes), and a draft resuming one stopped on `exit: "Blocked: Sean's call"` by its `triggered_by`. The types are [the master skill's](../../.claude/skills/motioncraft/SKILL.md) |
| [taxonomy.md](taxonomy.md) | Motioncraft's own seat failure modes. It is empty until its own labels earn one; the shared process-waste family is the kit's |

**Traced from mc-eng-001 on.** The kit finds this profile by walking up from the engagement folder, so the Close lines need no flag:

```bash
python3 craftwork/trace/check.py motioncraft/ledger/engagements/<eng-id>
```

```bash
python3 craftwork/trace/render.py motioncraft/ledger/engagements/<eng-id>
```
