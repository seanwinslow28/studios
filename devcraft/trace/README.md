# trace — Devcraft's side of the shared trace kit

The kit itself lives in [craftwork/trace/](../../craftwork/trace/README.md): the record and labels templates, the rung-0 checker, the viewer, the registry numbers and the handoff freezer. This folder holds only what is Devcraft's, written at scaffold on 2026-10-08.

| File | What it holds |
|---|---|
| [studio.py](studio.py) | The profile the kit reads: the four seats as stages in a full build's running order (1 Plan, 2 Tests, 3 Code, 4 Release), the record kinds (`intake` for an arriving brief, `run` for the Verifier's final run), the closed audit cycle, the plan gate, the release gate, the security pass and the self-check gate, and rung-0 line 8, which checks that an engagement ran its type's shape from the master skill's table: on a full build, tests and the plan gate before any code and both gates on the record by Close; on a small ask, tests before code, the Build Planner's one audit reading both, the final run, and the release leg when it fired; on an ops-only ask, Release's draft, the Builder's audit and the release gate. A one-off is one pass and is not asserted |
| [taxonomy.md](taxonomy.md) | Devcraft's own seat failure modes. It is empty until its own labels earn one; the shared process-waste family is the kit's |

**Traced from dc-eng-001 on.** The kit finds this profile by walking up from the engagement folder, so the Close lines need no flag:

```bash
python3 craftwork/trace/check.py devcraft/ledger/engagements/<eng-id>
```

```bash
python3 craftwork/trace/render.py devcraft/ledger/engagements/<eng-id>
```

## Named target folders.

For records written after [SWCB #212](https://github.com/seanwinslow28/SWCB/issues/212), a file read or written in a target repository is `target:<repo>/<path>`, for example `target:demo-app/src/message.py`. The name is `target`; `<repo>` is the repository's folder name, not its GitHub owner. Each machine maps `target` to the **parent** of those repositories in the gitignored `folders.local` at the top of studios. [folders.example](../../folders.example) carries the machine setup example. A missing mapping reports **not set up on this machine**, never a pass; set up that machine before checking the record.

| Files the record names. | Path form. |
|---|---|
| Target repository source, tests or other files actually read or written. | `target:<repo>/<path>`, with the hash of the exact revision seen. |
| Briefs, artifacts, audits, evidence, frozen diffs and copied handoff files inside the engagement. | Relative to the engagement, as before. |
| Studio contracts, lane manifests, templates and corpus inside studios. | Existing studio-prefixed paths, as before. |

**Worktrees.** `target:<repo>` names the repository checkout that this machine's mapping reaches. Do not use it for bytes read from a different, temporary build worktree, and do not repoint the shared mapping from build to build. Keep using `seat.py freeze-diff` to preserve a pass's exact change under `artifacts/`, with its base and point commits; trace records cite that engagement-relative patch and hash. If a pass also needs to preserve an exact source or test file from its worktree, copy it into the engagement's evidence and hash the copy. A current checkout can change after a pass; naming a folder does not preserve a revision or excuse a hash mismatch.

**Adoption, 2026-10-20.** Closed records stay immutable and are not migrated. New records use the forms above; engagement-relative paths and studio prefixes remain valid. Coordinator transcript pointers (`raw_log`) keep their existing session-log convention: this change concerns input/output paths.

The invented Devcraft one-off in [the adoption check](../../craftwork/trace/tests/test_team_folders.py) creates a new `target:demo-app/src/message.py` record and runs all eleven checker lines with Devcraft's own profile. It also exercises another machine's folder mapping, an unset mapping and a changed target file. It contains no private engagement data and claims no real seat pass or owner verdict.
