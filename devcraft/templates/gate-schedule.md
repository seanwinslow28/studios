# Gate schedule and attack checklists

Devcraft's own half of the red-team gate: when its gates fire, what each one reads and may demand, which vendor runs it, and what it attacks per artifact. The protocol itself (posture, statelessness, typed verdicts, IMPLEMENTATION HOLD, the rule that a gate never silently skips) is shared law at [craftwork/templates/red-team-protocol.md](../../craftwork/templates/red-team-protocol.md); this file is kept as Systemcraft keeps [its own](../../systemcraft/templates/gate-schedule.md). Written on the Devcraft build map's **Artifact templates and the gate schedule** ticket (2026-10-11), from rules 6 and 7 of [`devcraft/CLAUDE.md`](../CLAUDE.md), the bench and plugin-routing briefs (ratified 2026-10-08) and the seat-contract rulings (2026-10-11).

Gates are protocols, not seats. The trace kit files them as the gate seats `plan-gate`, `release-gate` and `security-pass` so their records have lanes. Each writes [gate-findings.md](gate-findings.md).

## When gates fire

| Engagement | Gates |
|---|---|
| **Full build** (`type: full-build`) | **Plan gate** after the Verifier's audit of the build plan, before any test or code · **Security pass**, only when the plan rates its surface high, after the Planner's audit of the change · **Release gate** after Release's audit of the test record, before Sean's yes |
| **Small direct ask** | **Release gate** only, and only when the change touches live data, a migration, or anything that runs unattended. Otherwise its state is `NOT FIRED — TRIGGER NOT MET`, recorded with the reason |
| **Ops-only direct ask** (a job, a schedule or a config file; no source) | **Release gate**, always. The drill record stands in for tests; a missing drill record is a release-gate FAIL |
| **One-off question** | No gate |

When Systemcraft's Gate 3 waits on a build, the release gate runs first and feeds it, never replacing it. Its verdict is typed RELEASE, never LAUNCH.

Outcomes are typed **PLAN** / **RELEASE** / **SECURITY**, each `PASS | PASS WITH ACCEPTANCES | FAIL` and always `— QUALITY VERDICT ONLY`. No verdict here is a merge or a go-live: those take Sean's dated yes, recorded in the ledger. A finding that lies outside the brief's pre-registered threat model is a NOTE with a recorded limit, never MATERIAL ([SWCB #139](https://github.com/seanwinslow28/SWCB/issues/139), ruled 2026-10-13); the model and the P0 rule written from it are frozen by the plan gate beside the exceptions.

## The three gates

| | Plan gate | Security pass | Release gate |
|---|---|---|---|
| **Anchor** | the build plan (stage 1) | the code change (stage 3) | the release plan (stage 4) |
| **Default vendor** | Codex, because Claude wrote the plan | a fresh-context Opus 5.5, because Codex wrote the code | Codex, because Claude wrote the release plan |
| **Launch** | the Codex form (registry row 3) with a `:read-only` pass profile (`devcraft/hooks/seat.py codex-pass`; never `--sandbox`, which replaces it), model pinned | the Claude form (registry row 2), read-only tools, its findings file the one write | the Codex form, `--sandbox read-only`, model pinned |
| **Reads** | the plan, the Verifier's audit of it, the intake, the repo at `base` | the plan's security section, the diff, the change note, the test record's security tests, the automatic checks | the gate packet in the release plan: all four artifacts, the diff, every check record, the plan gate's findings, the security pass's when it fired, the automatic checks |
| **May demand** | paper only: no code exists yet, so runtime evidence is an IMPLEMENTATION HOLD for the release gate, never a finding | the fixed security attack list, weighted to the triggers that fired | everything a built change can show: real output at the named commit, the drill record, the automatic checks, the closure of every hold the plan gate set |
| **Attacks** | § Build plan, below | § The fixed security attack list | § Change note, § Test record, § Release plan, § Whole build, and the fixed security attack list, together |

**The plan gate freezes the exceptions.** Its findings copy the plan's Exceptions section as it stood at the hash the gate read. That list is the only one the diff check honors: a skip, a credential file, a dependency, a control file or a host the build needs and the list lacks is a release-gate finding, or a push that fails outright for a default branch or an unnamed control edit (rule 9). A call found after the plan gate comes back as a plan amendment, and the plan gate re-runs on the amendment alone.

**The automatic checks** run just before the release gate, by the coordinator, with each tool called by its full path. The two dependency scanners need the network, so they run outside any seat's sandbox. Each output is saved to `evidence/` and handed to the gate; a check that could not run is a finding, never a silent skip.

**The release gate does not launch without its evidence** ([SWCB #139](https://github.com/seanwinslow28/SWCB/issues/139), ruled 2026-10-13): a drill file at the exact candidate hash, each automatic check's output with its full invocation at that hash, and every diff-check hit matched to a frozen exception or a dated yes from Sean. The launcher refuses the launch when any is missing (its machine check is [SWCB #150](https://github.com/seanwinslow28/SWCB/issues/150)); until it does, the coordinator ticks the three by hand in the gate's pass record before `seat.py launch`. A gate round spent on the coordinator's own missing evidence is process waste: dc-eng-002's release gate carried two such findings and dc-eng-003's failed its first round on one.

| Check | Command (from the worktree) | What it covers |
|---|---|---|
| Diff check | `python3 devcraft/diffcheck/diffcheck.py --worktree <wt> --engagement <eng>` ([its README](../diffcheck/README.md)); base and branch from the brief, the candidate at `HEAD` | never-do hits matched to the frozen exceptions, each commit's seat against its paths |
| Secret scan | `/opt/homebrew/bin/gitleaks git --log-opts="<base>..<candidate>" --redact --no-banner` | credentials committed anywhere on the build's range |
| Dependency check | `/opt/homebrew/bin/osv-scanner scan source -r .`, and `/opt/homebrew/bin/pip-audit` on a Python project | known vulnerabilities in what the build depends on |

## Vendors, and when a gate switches

A gate runs on the vendor that did not last write its anchor. Before each gate, the launcher reads the anchor's `model:` line: every gate names its anchor (`seat.py context --anchor <anchor>`) and runs on the vendor that did not last write it, so a gate cannot launch on its writer's vendor by mistake (SWCB #126). When a FAIL's redraft moved the anchor's last writer to the other vendor (Release escalated to Codex, or the Planner did), the gate moves with it, to a fresh-context Opus 5.5 or to Codex, and the findings file says why in `vendor_switch:`. The coordinator says so at the gate. The security pass's anchor is always Codex-written, so it always runs on Claude.

If the planned vendor is unavailable, the protocol's fallback holds: the gate runs fresh on the other vendor, labelled `fallback: same-vendor`, and a re-run ticket is filed; the context names it (`--fallback <the ticket>`) and the launch record carries it.

## FAIL, re-runs and the security seat question

FAIL → the owning seat of each CRITICAL or MATERIAL finding redrafts one tier up ([craftwork § Model delegation](../../craftwork/law.md#model-delegation)), except the Verifier, whose ladder is Opus 5.5 → stop and ask Sean, and the gate re-runs as `-r2`. That re-run is the gate's last round ([craftwork § Checks converge](../../craftwork/law.md#checks-converge-and-the-ladder-has-brakes), clause 9): a second FAIL stops the engagement and hands it to Sean with the open findings as candidate acceptances. Every check series still open is reported at each gate as round / findings / repair size, and a gate's own non-shrinking line is binding on the coordinator (clause 10).

A **CRITICAL security finding at the release gate that the plan's surface section did not foresee** is the P0 of the security ruling: the findings file sets `unforeseen_security_critical: yes`, and the coordinator files a fresh ticket to reopen whether security needs a seat. Nothing else reopens that question.

## The fixed security attack list

The release gate runs every line on every build, whatever the plan rated. The security pass runs it on a high surface, starting from the triggers that fired. Each line names where its finding lands.

- **SA1 · A secret in the change.** A credential value in code, fixtures, logs or test output; a secret read other than by name at runtime; the secret scan's result. *Lands:* change note; release plan § Secure deployment.
- **SA2 · A credential store touched.** A read of `.env*` (not the example files), `~/.ssh`, `~/.aws`, the `gh` or agent auth files, or a keychain that no exception names; a change to git identity, credential helpers or signing keys. *Lands:* change note; the pass records.
- **SA3 · Untrusted text reaching an interpreter.** Text from issues, web pages, files or tool output reaching a shell, SQL, a path, a template or an `eval` without a boundary; path traversal; a symlink that resolves outside the worktree. *Lands:* change note; test record § Security tests.
- **SA4 · Prompt injection.** An AI model in the build reads outside text and can act: what can that text make it do, is the action gated, and is the injection test a real attack. *Lands:* build plan § Security & privacy surface; test record § Security tests.
- **SA5 · Data leaving.** Every host the change contacts against the plan's allowlist; what data leaves; private or `local`-class data reaching an outside service. *Lands:* release plan § Secure deployment; build plan § Exceptions.
- **SA6 · Dependencies.** Every manifest and lockfile change against the frozen exceptions; each package shown to exist, with its age and maintainers; install scripts off; invented or look-alike names; the dependency check's result. *Lands:* change note § Dependencies added.
- **SA7 · Controls edited.** Hooks, permission or sandbox settings, `.claude/`, `.codex/`, `.agents/`, `.devcraft/`, `.github/workflows/`, git hooks or config, the diff check, the trace kit's checker, read from the diff check's output. *Lands:* change note; build plan § Exceptions.
- **SA8 · Checks weakened.** Skip markers, expected failures, coverage thresholds, lint or type suppressions, timeouts, CI edits. *Lands:* test record § Final record.
- **SA9 · Access control and crypto, where present.** Who can do what, enforced where; home-made crypto; how keys are held. The relevant ASVS chapters. *Lands:* change note; test record § Security tests.
- **SA10 · Private data at rest and in logs.** Personal data written to logs, file modes, retention, a log line an attacker can forge. *Lands:* release plan § Secure deployment and § Monitoring.
- **SA11 · Unattended reach and money.** What runs without Sean, as whom, with what blast radius; anything that can run up a bill with no cap. *Lands:* release plan § Failure modes and § Rollout.
- **SA12 · Public leak.** Book-derived text, ledger detail, or an employer, client or startup name in a tracked file, a commit message, a branch name or an issue (never-do 11). *Lands:* the diff; the change note.

## Attack checklists per artifact

### Build plan

- **A criterion that cannot fail.** "Works", "is robust", or anything no test could observe.
- **Intake that leaked.** A story id, hold id or ask line mapped to nothing.
- **What dressed as how.** A plan choice that fixes a public interface, a schema or product behavior nobody upstream fixed and nobody routed.
- **An under-rated surface.** Any of the seven triggers hit and the rating below high, or a trigger argued down.
- **A slice that cannot merge alone.** A slice that leaves the suite red, or leans on a later slice.
- **An unflagged ops path.** A job, schedule, CI workflow, config or rollback script the build will touch and Interfaces and data changes does not list.
- **Late exceptions.** A skip, credential file, dependency, control file or host the build will need that Exceptions lacks; it cannot be added after this gate.
- **Test paths narrowed.** A path removed from the floor, or a test path the plan treats as source.
- **Unpriced irreversibility.** A step with no way back that is not named as one.
- **A build too big to test up front.** Later slices that hang on what earlier ones reveal; it should be split into consecutive builds.
- **A phantom dependency.** A named package not shown to exist on its registry, with its age and maintainers.

### Test record

- **Tests of the code, not the plan.** Assertions that know the inside of the code, private names, a mock of the very thing judged.
- **Red for the wrong reason.** An import error, a typo or a missing fixture recorded as a red test.
- **Orphans.** A criterion with no test, or a test with no criterion.
- **Security tests that attack nothing.** A happy path labelled security; no injection test where an AI reads outside text; no outbound-host test where data leaves.
- **Claims, not output.** A result with no command, no output, or a different commit.
- **Silent skips.** A skipped, expected-failure or quarantined test not listed with its exception.
- **Hash drift.** The visible test-files hash differs between red and final by anything but listed repairs and the held-out commit.
- **Flake laundering.** A test re-run until green with the re-runs unrecorded.
- **Production blindness.** No test or stated reason for the migration both ways, a restart, a missing secret or an unattended re-run.
- **A held-out leak.** `held-out/` listed in any Builder pass's inputs, or held-out results missing from the final record.

### Change note

- **An unplanned change.** Files or behavior no slice names.
- **A deviation with no reason.**
- **Special-casing.** Code that branches on values that appear only in the visible tests; a visible pass with a held-out fail is the evidence.
- **The judge touched.** A test path, snapshot or golden file in the diff, or a test-files hash that does not match.
- **A dependency walked in.** A manifest or lockfile change no exception names.
- **Local run as certification.** "Done" or "passes" without the command, its output and where it ran.
- **Migration drift.** Migration code that does not match the plan's data changes or Release's steps.
- **Docs left behind.** Behavior changed and the docs beside it not.
- **Architecture by stealth.** A public interface or schema changed inside a slice.

### Release plan

- **Kill-switch theater.** A rollback or kill never drilled, drilled on live data, or drilled somewhere the plan does not name.
- **Surface gaps.** A schema, job, schedule, CI or config change in the diff with no release-surface line.
- **Contract before expand.** The old shape removed before the new one is live; a step with no way back not named as one.
- **The unattended re-run.** A job that runs twice, after a restart, or with a secret missing, and nobody says what it does.
- **A 3 a.m. runbook that needs its author.** A step with no exact command or no expected output.
- **A silent failure.** A failure mode with no signal, or a signal nobody sees.
- **Over-privilege.** Job permissions beyond what works; a secret by value; a host beyond the allowlist.
- **Canary skipped.** Straight to live, or a stage with no abort condition.
- **A yes assumed.** Sean's line filled with no ledger entry behind it, or go-live written as a seat's action.
- **Outside the fence.** A file Release wrote that the plan never flagged (on an ops-only ask: that the brief's list does not hold).
- **Gate 3 claimed, not shown.** Gate 3 evidence that points at nothing.

### Check records

- **A check that saw the conversation.** Inputs listing anything but artifacts.
- **A silent pass.** What was attacked and held left empty on a clean verdict.
- **Severity laundering.** A material defect filed as a note to avoid the loopback.
- **The stake not answered.** Rows that never address the seat's stake sentence.
- **A re-run that was not re-run.** Release's audit of the test record comparing recorded output with nothing.
- **A verification pass that re-audited.** Findings from text the repair never touched filed as material, or a passed finding reopened.
- **A second loopback on one check.** The repair cap spent and a third round requested.

### Whole build (release gate)

- **Cross-artifact contradictions.** A criterion with no test, a test with no criterion, a slice with no commit group, an ops path with no release-surface line, a change with no slice.
- **Exceptions not on the record.** A diff-check hit that matches nothing in the plan gate's frozen list and no dated yes from Sean.
- **The cascade that did not fire.** An artifact below a loopback still at its old revision.
- **Checks that never ran.** A stage with no audit record; a high surface with no security pass; a plan-gate hold the packet does not close.
- **The steel-man.** A competing approach that reaches the same criteria more simply, and no artifact rules it out.
- **The quiet failure.** The six-months-on, or 3 a.m., scenario with no signal in the release plan.
- **Process waste.** A series run past its stopping rule; a finding recounted per appearance; a defect this folder or the kit caused. Coded from the shared process-waste family ([craftwork/trace/taxonomy.md](../../craftwork/trace/taxonomy.md)), not graded as a seat's failure.
