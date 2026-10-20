# trace — Productcraft's side of the trace kit

The trace kit is shared. Its code, templates, viewer and tests live in [craftwork/trace/](../../craftwork/trace/README.md), the home every -craft team inherits from. They moved there from this folder on [#325](https://github.com/seanwinslow28/code-brain/issues/325) (kit 0.9.0, 2026-10-01). This folder keeps only what is Productcraft's own:

| File | What it is |
|---|---|
| [studio.py](studio.py) | Productcraft's **profile**: the seven-stage train, the record kinds, the gate seat, the repo path prefixes, the corpus citation shape, the review prompts, and rung-0 line 8 (*each drafting stage has one draft, an audit, and its required co-signs*), registered when the kit loads the file |
| [taxonomy.md](taxonomy.md) | Productcraft's **seat failure modes**, ratified by Sean on [#299](https://github.com/seanwinslow28/code-brain/issues/299) from pc-eng-001's labels. The shared process-waste family is the kit's [taxonomy.md](../../craftwork/trace/taxonomy.md), and the checker reads both |
| [samples/](samples/README.md) | The invented Callboard engagement the kit's tests simulate, committed with its render, and the #292 prototype render Sean ratified |

The kit finds `studio.py` by walking up from the engagement folder, so the Close lines need no flag:

```bash
python3 craftwork/trace/check.py productcraft/ledger/engagements/<eng-id>
```

```bash
python3 craftwork/trace/render.py productcraft/ledger/engagements/<eng-id>
```

Everything else about the kit — the record layout inside an engagement, the rung-0 lines, the viewer, the registry numbers, the next-id helper — is in [craftwork/trace/README.md](../../craftwork/trace/README.md).

## Folder audit, 2026-10-20.

[SWCB #212](https://github.com/seanwinslow28/SWCB/issues/212) found **no named folder needed under the current contract**. Evidence snapshots, artifacts, audits and frozen handoffs belong inside the engagement; machinery and corpus already resolve inside studios. Web sources are captured as evidence rather than treated as local folder paths.

Keep those path forms; no records switch and closed records are not migrated. Coordinator transcript pointers follow the shared session-log convention separately. [folders.example](../../folders.example) lists the names used by other teams; Productcraft adds none. If a later engagement needs an external folder, name and configure it before writing that engagement's first such record. Handoffs keep their frozen copies rather than pointing into another team's ledger.
