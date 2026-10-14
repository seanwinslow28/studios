---
name: devcraft
description: Run the Devcraft studio — the four-seat software engineering bench at devcraft/ (Build Planner, Builder, Verifier, Release & Reliability) that plans, tests, builds and releases code in Sean's own repos. User-invoked only — run as /devcraft when Sean names a build, a small change, an ops change or a one-off engineering question for the studio, or hands it a Productcraft breakdown or a Systemcraft design to build. It never fires on its own. NOT for what to build or the architecture (Productcraft and Systemcraft own those), employer code, or quick coding help in a live session — do those directly.
disable-model-invocation: true
---

# Devcraft — master skill

The studio's orchestrator. **The skill knows the process, the seats know the craft, the law is the law**: craft lives in [devcraft/bench/](../../../devcraft/bench/README.md) (contracts, write zones, audit duties, launch forms, toolbelts), the studio's law in [devcraft/CLAUDE.md](../../../devcraft/CLAUDE.md) (public/private split, how never what, the boundary rule, Claude plans and Codex codes, the never-do list), and what every -craft team shares in [craftwork/law.md](../../../craftwork/law.md). This file owns only what happens when: the engagement types, the phases, the pass budget and the Close checklist. It never restates the other two. Excluded from export groups: it is useless without this repo's bench, wall and trace kit. User-invoked only (`disable-model-invocation`); Codex reads it through `.agents/skills/devcraft`.

Written on the Devcraft build map's **Write the master skill** ticket (2026-10-11), from the rulings of its **Master skill design** ticket.

## Engagement types and routing

Type by the change the engagement may make. Every brief carries one `type:` value.

| `type:` | Selection test | Roster, in running order | Gates |
|---|---|---|---|
| `full-build` | Anything that is not one of the three below: more than one slice, a public interface or data schema, or any exception (a dependency, a credential file, a control file, a network host) | The bench README's [full running order](../../../devcraft/bench/README.md): Planner drafts → Verifier audits the plan → plan gate → Verifier's suite, red → Builder, slice by slice → Planner audits the change while Release drafts → Builder audits the release plan → Verifier's final run → Release audits the test record → release gate | Plan gate, the security pass when the plan rates its surface high, release gate |
| `small-ask` | Fits one slice, changes no public interface or data schema, and needs **no exception**. Exceptions count only when a plan gate froze them, so an ask that needs one is a full build | Open numbers Sean's ask as `ASK<n>` lines, which stand in for criteria. Verifier writes the tests and records them red → Builder codes → **Build Planner audits the change and the tests together**, in one pass (the only seat that wrote nothing) → Verifier's final run. No build plan, no plan gate | Release gate only when the ask touches live data, a migration or anything unattended: then Release drafts, the Builder audits, the release gate runs. Otherwise `NOT FIRED — TRIGGER NOT MET`, with the reason |
| `ops-only` | A job definition, a schedule or a config file, and no source change | Release drafts → Builder audits → release gate, per [Release & Reliability](../../../devcraft/bench/release-reliability.md). The drill record stands in for tests. A source change found on the way re-opens it as a full build | Release gate, always |
| `one-off` | One engineering question one seat can answer with no code changed | One seat, one ledger entry. If the answer means code should change, it stops and retypes | None |

No audit type and no role-support type: a row is added when a real case earns it.

**Two modifiers sit on top of a type, never as types.**

- **Handoff.** Work arriving from Productcraft or Systemcraft runs under [the handoff contract](../../../craftwork/handoff-contract.md) and the sender's binding for the pair. The receiving seat's intake check is a `kind: intake` pass, its first act `python3 craftwork/trace/freeze.py verify` on every inbound copy; it issues `accepted`, `input-required` or `rejected` into `crossing.md` and the Open entry. `originates_from:` is set on the brief and every ledger entry. Forwarded copies cross byte for byte (contract § 10). Devcraft builds how, never re-litigating what the sender decided. The return goes back on the pair's mirror: [to Productcraft](../../../devcraft/templates/handoff-return-productcraft.md) at Close, one line per story; [to Systemcraft](../../../devcraft/templates/handoff-return-systemcraft.md) at release-gate PASS, as the candidate note. Devcraft sends one crossing of its own: an AI-shaped architecture call with no covering design goes to Systemcraft as a one-off ask under [its binding](../../../devcraft/templates/handoff-binding-systemcraft.md), and the build waits for the answer.
- **Self-targeted.** The trigger: the diff touches `devcraft/`, `craftwork/`, this skill, or any control a seat runs under (`seat.py`, the guard, the diff check, the trace checker). Decided at Open from the plan's file list and re-confirmed by the diff check at the release gate. Open adds the five duties of [craftwork § Self-targeted modifier](../../../craftwork/law.md#self-targeted-modifier). Devcraft's reading of "may only draft": the build up to the release gate is the draft; implementing and ratifying it are Sean's merge from his own checkout. The gates already run on the vendor that did not write the anchor, which meets the different-lineage duty; any fallback is named. **Hard limit:** a self-targeted build never widens a seat's own reach (write zone, network, never-do exceptions) in the same build that uses it.

**Sean's own spec, PRD or ticket set.** One build is one engagement, with its own id, budget, gates, Close and D+14. Consecutive builds from one spec share a `series:` line in their briefs. At Open the coordinator proposes the split (one engagement if a single plan carries it with every slice merging alone), and Sean confirms before anything runs. **Fixed:** whatever the spec states as a requirement, behavior, public interface or data schema (never-do 10). **Open:** whatever it leaves unsaid is the Planner's call within its bounds. A line that could be read either way is flagged at Open and settled by Sean before the Planner starts, never guessed.

**Architecture-sized calls** are routed by their kind, as the [Build Planner's contract](../../../devcraft/bench/build-planner.md) says: a covering Systemcraft design wins, an AI-shaped call goes to a Systemcraft one-off, any other gets the Planner's decision memo and Sean's pick. Never decided here.

## Standing success measure

An engagement succeeds only on outside use at Close + 14 days, and Close is declared `ADMINISTRATIVE CLOSE — OUTCOME PENDING D+14`, never success. The authority, P0-equivalent definition included, is [craftwork § Standing success measure](../../../craftwork/law.md#standing-success-measure).

## The phases

### 1 — Open

The coordinator's own session, one `kind: open` pass record at stage 0, whose outputs are the brief and anything the chain anchors on.

1. **Two stops come first.** Either one ends Open before an id is assigned.
   - **No `.devcraft/test-paths` in the target repo.** `.devcraft/` is a control (never-do 14), so no build can write it. The engagement does not open. A **one-off** runs instead: the Planner drafts the list into that one-off's engagement folder, with a why per path; Sean approves it and commits it to the target repo by hand; then the real engagement opens.
   - **`local`-class work.** The class comes from the source: an SWCB work ticket's `privacy:` field; a never-pushed branch or repo on the Mini is always `local`; for a direct ask, Sean says, and if it is unclear the coordinator asks in one line. A `local` stop **writes nothing to the ledger**, which is pushed to GitHub (even a file name from `local` work stays on the Mini). It tells Sean in chat and stops.
2. **Type it** (the table above) and name any modifier. For Sean's own spec, propose the split and the fixed/open reading, and get his yes.
3. **Assign the id** `dc-eng-NNN-<slug>`, the next free number under `devcraft/ledger/engagements/`, and create the folder with `artifacts/`, `audits/`, `evidence/` and `trace/logs/` ([layout](../../../devcraft/ledger/README.md)).
4. **Pull precedent** from `devcraft/ledger/index.md` (two hops: index line → entry).
5. **Preflight and worktree.** Run `python3 devcraft/hooks/seat.py check`; any gap stops the engagement at Open. Create the build's branch in its own worktree off the target repo's current base, and install its git hooks with `seat.py worktree <worktree> --engagement <eng>`. A one-off changes no code and takes no worktree.
6. **Thin-lane check.** Each rostered seat's [lane manifest](../../../devcraft/lanes/README.md) against the engagement's topics; a lane with no pointer for its topic is declared in the brief, and the thin-lane trigger is decided here, never mid-pass.
7. **Set the budgets** (the table below): the pass budget, the per-pass caps, and Sean's attention budget, the number of yes/no stops he will be asked for. Any default may change with a stated reason.
8. **Pre-register the threat model, then the P0 rule from it** ([SWCB #139](https://github.com/seanwinslow28/SWCB/issues/139), ruled 2026-10-13). One paragraph: who or what the build protects against, the harm it bounds, and what is out of model. The P0-equivalent rule ([craftwork § Standing success measure](../../../craftwork/law.md#standing-success-measure)) is then written from that paragraph with a likelihood clause, "in ordinary use" or "including deliberate evasion". The plan gate freezes both beside the exceptions, and a gate finding outside the model is a NOTE with a recorded limit, never MATERIAL. dc-eng-002 wrote its P0 rule with no model and no likelihood clause, and its plan gate spent five rounds inside the class Sean excluded at d13.
9. **Write `brief.md`**, the header first, then the brief:

```markdown
---
id: dc-eng-NNN
name: <a short name>
type: full-build                  # full-build | small-ask | ops-only | one-off
modifiers: []                     # handoff, self-targeted
series: null                      # shared by consecutive builds from one spec
opened: YYYY-MM-DD
closed: null
pass_budget: 15                   # the cap, the coordinator's own session inside it
attention_budget: 4               # Sean's yes/no stops
target_repo: seanwinslow28/<repo>
base: <commit>
branch: <the build's branch>
originates_from: null             # the handoff brief's id, on a handoff
---
```

Then, in a breath each: the ask (on a small ask, its `ASK<n>` lines); for Sean's spec, what is fixed and what is open; the threat model and the P0 rule written from it; on an ops-only ask, the file list that is Release's whole write zone; the roster; the budget, its caps and any change from the defaults with its why; the thin lanes; the security-pass expectation if already known; the five self-targeted duties when that modifier is on; the Jev slot when one is declared. The kit reads the header ([craftwork/trace/README.md](../../../craftwork/trace/README.md)); the structure check reads `type:`.

### 2 — Route

Written into the Route entry, before any seat runs.

- **The roster and each seat's runtime from its own seat file's `model:` line**, never the session's model. Every runtime is a ruled row of [the runtime registry](../../../craftwork/templates/runtime-registry.md). Every Codex pass pins the ruled model from its seat file or gate default with `--model`, with its effort spelled out, never the config default and never `ultra`.
- **The model check.** Devcraft launches by full id, so the probe is one tiny call per pinned id (`claude-opus-5-5` on `claude -p`, the Builder's ruled model and the gate default on `codex exec`), each asked for its own model id (`seat.py probe`, which reads the match from the log's model stamp, never the answer). Outside the budget; answers into the Route entry; a mismatch goes to Sean before any seat runs. This is Devcraft's form of [craftwork § The alias probe at Route](../../../craftwork/law.md#the-alias-probe-at-route).
- **Deviations**, each with its one-line why against a named trigger of [craftwork § Model delegation](../../../craftwork/law.md#model-delegation). Devcraft's brake: **the Verifier never escalates onto Codex** on any pass that writes or changes a test; its ladder is Opus 5.5 → ask Sean.
- **A Jev slot**, if one runs, declared here as a **shadow**: outside the funded cap and log-only. Its output is never an input to a seat, a gate packet, a verdict or a stop, and its log is read only at Close, for labels, blind. Every call inherits the guard's skip list, its secret scrubbing and the `local` class; an engagement that cannot guarantee those runs without it. Seat passes load no user-level hooks, so a Jev guard on Sean's own sessions never sees a seat.

### 3 — Run

Seats run in the type's order. Every invocation is fresh-context and carries what [the bench says it carries](../../../devcraft/bench/README.md): its seat file, [the seat preamble](../../../devcraft/templates/seat-preamble.md) verbatim, its lane manifest, the declared target, the upstream artifacts in full, and the target's `AGENTS.md`. Never this conversation. No seat launches another.

**Each pass, in order:**

1. Write the pass record's launch fields ([record-template.md](../../../craftwork/trace/record-template.md); one file per invocation at `trace/pass-NN-<seat>-<kind>.md`, with the hash of every input).
2. `seat.py context` for the pass, copying every exception from the plan gate's frozen "Exceptions on the record" table and nowhere else. The context file holds no employer paths and stays in `trace/logs/`. It also fixes the vendor the pass runs on, from the record that calls for it, never by name: a gate names its anchor (`--anchor`), a verification pass the repaired artifact (`--verify`), a redraft one tier up its gate FAIL or ledger entry (`--escalation`); anything else runs on its seat's own vendor ([hooks README](../../../devcraft/hooks/README.md#how-a-pass-is-walled), step 2; SWCB #126).
3. The wall files, for the vendor the context names: `seat.py claude-settings` or `seat.py codex-pass`. They hold the machine's employer paths, so they are written to `~/.config/devcraft/passes/<engagement>/`, outside every repo; the pass record keeps their path and hash, never their content.
4. `seat.py launch --output <artifact> --run`, under the caps below, which `context` wrote into the pass's context. Codex writes its final message **straight to the artifact's path** with `-o` (the change note, the audit of the release plan, gate findings), never to a log the coordinator copies; its raw JSONL log is captured separately into `trace/logs/`. The launcher writes `trace/logs/pass-NN.launch.json`, the source of the completion fields below; exit 2 is a cap reached (`Blocked: budget`), exit 3 a helper agent.
5. On return, the completion fields: outputs and their hashes, the meter or `UNMEASURED`, `## Corpus read` from the transcript's file reads, `runtime:` from the transcript's model stamp. After a Codex pass the launcher has already saved its session files beside its JSONL as `trace/logs/pass-NN.rollouts/` ([trace README](../../../craftwork/trace/README.md) line 11) and read them for a helper; run `check.py` once the record is written, not at Close: a pass that started a helper agent fails line 11, and its output is discarded and the pass re-run once, never used; a second spawn stops the engagement Blocked (ruled by Sean on SWCB #123, 2026-10-12).
6. **The frozen diff.** After every pass that touches the target repo (the red suite, the build, the final run), save `git diff <base>..<that point>` as a patch in `artifacts/` (`seat.py freeze-diff <context> --base <base>`) and record its hash as that pass's output. The patch outlives the worktree.
7. **Commits.** The coordinator commits each slice as one commit group, named paths only, with the message the change note gives (`<eng> S<n>`, which is how [the diff check](../../../devcraft/diffcheck/README.md) knows a Builder slice). No seat commits: the coordinator also commits a Verifier or Release pass's staged paths under that pass's context, and the hook stamps the `Devcraft-Seat:` trailer ([the bench](../../../devcraft/bench/README.md), SWCB #133). The pre-push hook runs the diff check before every push: exit 2 refuses, findings are recorded in `evidence/` for the release gate.

**The coordinator's own installs** run under the guard's `coordinator` role, scripts off.

**Checks converge** under [craftwork § Checks converge](../../../craftwork/law.md#checks-converge-and-the-ladder-has-brakes): one repair round per artifact per check; round two is a verification pass on the vendor that did not write the repair; every open series reported at each gate as *round / findings / repair size*. A Verifier verification pass after a Planner repair changes no test, so it runs on Codex like any other (`seat.py context --verify <the repaired plan>`); the brake covers only passes that write or change a test.

**Ledger writes happen here.** The deciding seat writes an entry at the moment of a material decision, to [the shared schema](../../../craftwork/templates/ledger-entry.md) with its `## From the canon`; ids from `python3 craftwork/trace/nextid.py devcraft/ledger/engagements/<eng>`.

**Exits.** A seat that stops returns one typed `exit:` ([artifact-header.md](../../../devcraft/templates/artifact-header.md#exits)) and the coordinator routes it from that table. A budget stop is `BUDGET STOP — WORK PAUSED` and one variance question to Sean.

### 4 — Gate

When each gate fires, what it reads, its vendor and what it attacks are [Devcraft's gate schedule](../../../devcraft/templates/gate-schedule.md); the posture and typed verdicts are [the shared protocol](../../../craftwork/templates/red-team-protocol.md). A gate runs on the vendor that did not last write its anchor, and the coordinator says so when a FAIL moves it; the launcher reads the move from the anchor's `model:` line, so every gate's context names its anchor. The automatic checks run just before the release gate, saved to `evidence/`. A gate never silently skips; every gate writes its ledger entry.

**Merge and go-live.** No verdict is a merge. After the release gate, Sean gives a dated yes recorded in the ledger, and the merge runs from his own checkout in a session he is driving. On a build Systemcraft's Gate 3 waits on, Release & Reliability and the release gate always run, whatever the type. Release gate PASS → the Gate 3 packet goes out: straight to Systemcraft at once when the design crossed from Systemcraft (the return is the candidate note), or inside the return to Productcraft at Close when the design's copies were forwarded, and Delivery relays it with its candidate note (ruled by Sean 2026-10-11, SWCB #117); **the merge proceeds on Sean's dated yes** without waiting for Gate 3; **go-live waits** for Gate 3's verdict (`gate3-note.md` in the engagement's `handoff/inbound/`) and Sean's go-live yes, and then the coordinator runs the runbook's go-live step in a session Sean is driving.

### 5 — Close

The coordinator's own session, one `kind: close` pass record. In order:

- [ ] **Ledger complete**: every entry written, the Close entry among them; one line per entry appended to `devcraft/ledger/index.md`.
- [ ] **Sean's yes, copied**: the Close pass copies his dated yes (date, what he approved, the ledger entry id) into the release plan's "Sean's yes" line, as a recorded output. The ledger entry stays the authority.
- [ ] **Trace 1, check**: `python3 craftwork/trace/check.py devcraft/ledger/engagements/<eng>`. Every rung-0 line PASS, or each FAIL fixed in the record it names, never by editing an artifact after its pass.
- [ ] **Trace 2, render**: `python3 craftwork/trace/render.py devcraft/ledger/engagements/<eng>`, opened from disk, never hosted.
- [ ] **Trace 3, labels**: every pass has a row with a verdict in `trace/labels.md`, coordinator-drafted and Sean-approved, and its provenance block says so. A Jev shadow's log is labeled blind, if a slot ran.
- [ ] **Trace 4, registry numbers** across **every** studio's traced engagements, since the numbers are shared: `python3 craftwork/trace/registry.py $(find productcraft/ledger/engagements systemcraft/ledger/engagements devcraft/ledger/engagements -mindepth 2 -maxdepth 2 -name trace -type d -exec dirname {} \; | sort)`, and replace § Numbers of the runtime registry with its output.
- [ ] **Residuals re-read** against current state (craftwork § Checks converge, clause 7).
- [ ] **Handoff builds**: the return filed on the pair's mirror (the candidate note, on a build Gate 3 waits on), Gate 3 recorded pending, and a dated reminder ticket on SWCB for the go-live.
- [ ] **Live deferred work**: one issue each on `seanwinslow28/SWCB`, labelled `needs-triage`.
- [ ] **Worktree removed** after the merge; the frozen diffs keep the record, and the machine-local wall files stay as evidence.
- [ ] **Private layer**: `git status` shows nothing under `devcraft/{corpus,ledger,books}/`; then commit and push the ledger's own repo, `git -C devcraft/ledger add -A && git -C devcraft/ledger commit -m "<eng>: <close gist>" && git -C devcraft/ledger push`. Every session that touched the ledger pushes before it ends, not just Close.
- [ ] **Freeze** the P0-equivalent count (Sean ratifies), set the D+14 outcome-record date, and declare `ADMINISTRATIVE CLOSE — OUTCOME PENDING D+14`. Close does not wait on Gate 3.
- [ ] **The explain-why digest** per [the close digest](../../../craftwork/templates/close-digest.md): recommendation first, one question, statuses per [the status vocabulary](../../../craftwork/templates/status-vocabulary.md).

No corpus-inbox sweep: Devcraft has no inbox yet.

## Pass budget and launcher caps

Day-one defaults. Any Open may change them, with a stated reason in the brief.

| Type | Base passes | Rounds | Cap |
|---|---|---|---|
| `full-build` | 11 | +4 | 15, or 18 when the security pass fires |
| `small-ask` | 4 | +1 repair | 5, or 9 when the release gate fires |
| `ops-only` | 3 | +2 | 5 |
| `one-off` | 1 | none | 1 |

The coordinator's own session counts inside the cap. Exhaustion is a stop: actual against cap, and one variance question to Sean, never a silent overrun.

**Per pass:** the Builder 60 minutes and 200 tool calls; Codex gates 20 minutes and 80 tool calls; Claude seats and the security pass 30 minutes and `--max-budget-usd 15`. The prompt states the caps and the seat stops at 90% (`Blocked: budget`). The launcher kills at 100%, because Codex has no budget, turn or time flag and macOS has no `timeout`; a killed pass is filed `Blocked: budget` with what it left on disk. Every pass records a meter line, or `UNMEASURED`, never an estimate.

**Availability.** An unavailable runtime follows [craftwork § Availability ladder](../../../craftwork/law.md#availability-ladder): a dated, Sean-approved substitution from a registry row, or a dated deferral. Never a merged lane or a silent switch.

## Degradation

On a machine without the private layer (a fresh clone, an employer machine), the seats already carry the ladder (`manifest-only`, then `none`). The skill's own duty is to say so once at Open and proceed, never fabricating ledger precedent or corpus grounding it cannot read. Devcraft never runs on employer code at all (never-do 2).
