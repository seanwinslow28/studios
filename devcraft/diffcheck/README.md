# The diff check

The after-check layer of Devcraft's never-do list ([`devcraft/CLAUDE.md`](../CLAUDE.md), rule 9): a model-free comparison of a build branch with its base, run by the coordinator and never by a seat. The wall ([`hooks/`](../hooks/README.md)) stops a seat at the moment it acts; the seat contract states every rule; this check reads what actually landed on the branch and reports it to the release gate. Built on the Devcraft build map's **Build the diff check** ticket (2026-10-12), from the never-do ticket's diff-check column and the seat-contract ruling on Release's zone.

| File | What it is |
|---|---|
| [`diffcheck.py`](diffcheck.py) | The check. Reads the wall's rules from [`hooks/policy.py`](../hooks/policy.py), the engagement folder's record, and the git range; writes one report into the engagement's `evidence/` |
| [`tests/seeded.py`](tests/seeded.py) | The seeded set: ranges that must be flagged, ranges that must pass, recorded beside the check |
| [`tests/test_diffcheck.py`](tests/test_diffcheck.py) | Builds each case as real commits in a throwaway repo and runs the check, with registry lookups from a fixture and the real gitleaks |

## When it runs

Twice on a full build, the same command both times:

```bash
python3 devcraft/diffcheck/diffcheck.py --worktree <build worktree> --engagement <engagement folder>
```

1. **Before every push.** The build worktree's pre-push hook ([`hooks/gitcheck.py`](../hooks/gitcheck.py)) runs it on every ref being pushed, offline. Exit 2 refuses the push; findings are recorded and the push proceeds, so the release gate reads them.
2. **For the release gate's packet.** The coordinator runs it once more, with the network, just before the gate, beside the secret scan and the dependency check ([gate-schedule.md § The automatic checks](../templates/gate-schedule.md)). The report is handed to the gate and cited in the release plan's gate packet.

Base and branch come from the brief (`base:`, `branch:`); the candidate is the worktree's `HEAD`. Flags override each, and `--test-path` / `--ops-path` supply what no plan can on an ops-only ask (the brief's file list), recorded in the report as coming from flags.

## What it reads

- **The test paths**: the repo's `.devcraft/test-paths` floor **at the base commit** (so a build cannot widen its own floor), plus the plan's "Test paths added" line. No floor at the base: refused, since the engagement should have stopped at Open.
- **Release's zone**: the plan's "Ops paths flagged for Release" rows (`OP<n>`).
- **The frozen exceptions**: the latest `audits/plan-gate*.md`, its "Exceptions on the record" table, by `EX` id and kind (`skip`, `credential file`, `dependency`, `control file`, `host`). The build plan is the file the plan gate's pass named with `--anchor`, read from the launch record that filed the gate file (`trace/logs/pass-NN.launch.json`), so a redraft filed under a new name by `-o` is read where the gate read it (SWCB #145); a gate filed with no launch record falls back to `artifacts/build-plan.md`, and an anchor outside `artifacts/` or `inherited/` is not followed. The plan's own path lists are honored only while that file still hashes to the gate's `anchor_sha256`; a plan edited after the gate voids its additions until the plan gate re-runs, and the report says so.
- **Sean's dated yes**: a ledger entry of this engagement (`d<NN>-*.md`) with `ratified: <date>` set. It covers a hit it names.
- **Which seat made each commit**: the `Devcraft-Seat: <seat>` trailer the commit-msg hook stamps from the seat context (a seat cannot claim another seat's), or the coordinator's `<eng> S<n>` message on a Builder slice. A commit with neither is a finding.

## What it flags

| Kind | The hit | Covered by |
|---|---|---|
| `boundary` | A Verifier commit outside the test paths; a Builder commit inside them, on a snapshot or golden file, or on Release's flagged paths; a Release commit outside its flagged paths or on a test; any commit by a seat that never writes the worktree (never-do 4) | nothing: always a finding |
| `commit` | A commit with no seat | nothing |
| `weaken` | Skip, xfail, `.only` and ignore markers; a deleted test file or test function; a threshold line; a lint, type or coverage suppression; a timeout in a test, a check config or CI; a CI file or check-configuration edit (never-do 5) | a `skip` exception naming the path or the test; a `control file` exception for a CI file |
| `credential` | A `.env*` file (not the example names) in the change; a credential value found by gitleaks over the range (never-do 6) | a `credential file` exception naming the file; a value, never |
| `unattended` | A launchd, cron, timer or service file, a plist with a schedule key, or a schedule added to a workflow (never-do 8) | a ratified entry only |
| `dependency` | A manifest with a new package (each looked up on its registry: exists, first release, age, maintainers), a removal or version change, a lockfile change (never-do 12) | a `dependency` exception naming the package; a lockfile, by a named and verified package of its ecosystem in the same range. A package not on its registry is never covered |
| `control` | A control file edited (never-do 14), from the wall's list plus the studios list on this repo | a `control file` exception naming it; never for `AGENTS.md`, `CLAUDE.md` or a skill |
| `leak` | A listed name in an added line, a commit message or the branch name (never-do 11) | nothing |
| `branch` | The candidate is a default branch (never-do 3) | nothing |

An unmatched `control` or `branch` hit **refuses** (exit 2). Every other unmatched hit, and every check that could not run (gitleaks missing, a registry lookup that failed or was skipped), is a **finding** (exit 1) for the release gate's "Exceptions not on the record" line. Clean is exit 0.

## The report

`evidence/diff-check-<candidate>.txt`, never overwritten: a re-run at the same candidate writes `-2`, `-3`. It opens with its own invocation, so the report alone is the execution record the gate packet asks for (SWCB #146): the command as run, the cwd, the interpreter and its version, the checker's and `policy.py`'s full paths and sha256, the engagement folder, the worktree's `HEAD` (and whether it is the candidate) and its uncommitted paths, the mode (`online`, `offline` from `--offline`, or `fixture` when `DIFFCHECK_REGISTRY_FIXTURE` answers the lookups), how many registry lookups ran, the gitleaks it used, and the process exit. It then lists what the check read (the floor, the added paths, the ops paths, the gate file and anchor, whether the plan is still frozen, the exceptions honored, the ratified entries seen), every commit with its seat, every hit with its state (`matched EX<n>`, `matched <entry> (ratified <date>)`, `UNMATCHED`, `REFUSED`), the checks that could not run, and the verdict line. The command prints the verdict and the report's path with its sha256, for the pass record's outputs. A listed name is replaced in the report, never printed; gitleaks runs redacted.

## Tests

```bash
cd ~/Code-Brain/studios && uv run --no-project --with pytest python -m pytest devcraft/diffcheck/tests -q
```

Registry lookups in tests come from `DIFFCHECK_REGISTRY_FIXTURE`, a JSON file keyed `<ecosystem>:<package>`; the secret scan runs the real gitleaks at `/opt/homebrew/bin/gitleaks` (override with `DEVCRAFT_GITLEAKS`). The machine-local name list comes from `DEVCRAFT_LOCAL`, as for the hooks.
