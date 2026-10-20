---
name: motioncraft
description: Run the Motioncraft studio — the four-seat animation and motion-design bench at motioncraft/ (Visual Story Director, Art and Pose Designer, Animator, Finishing and Sound Designer) that takes a film from brief to delivered cut. User-invoked only — run as /motioncraft when Sean names a film, a short moving piece, or a one-off style frame or rough board for the studio. It never fires on its own. NOT for what the film is (its story, words and purpose are Sean's), standalone static design, pipeline software (Devcraft), day-job video, or quick animation help in a live session — do those directly.
disable-model-invocation: true
---

# Motioncraft — master skill

The studio's orchestrator. **The skill knows the process, the seats know the craft, the law is the law**: craft lives in [motioncraft/bench/](../../../motioncraft/bench/README.md) (contracts, the audit cycle, launch forms, baselines, exits), the studio's law in [motioncraft/CLAUDE.md](../../../motioncraft/CLAUDE.md) (public machinery and private brain, Sean alone approves artistry, how a film is made never what, one operator per application, the three finding kinds, the fourteen never-dos, the interim words rule), and what every -craft team shares in [craftwork/law.md](../../../craftwork/law.md). The artifacts' shapes are [the templates](../../../motioncraft/templates/README.md); what each gate reads and attacks is [the gate schedule](../../../motioncraft/templates/gate-schedule.md); where files and media live is [the ledger README](../../../motioncraft/ledger/README.md). This file owns only what happens when: the engagement types, the phases, parts, the pass budget, the sound trigger and the Open and Close checklists. It never restates the others. Excluded from export groups: it is useless without this repo's bench, templates and trace kit. User-invoked only (`disable-model-invocation`); Codex reads it through `.agents/skills/motioncraft`.

Written on the Motioncraft build map's **Write the master skill** ticket (2026-10-18), from the rulings of its **Master skill design** ticket. Not voice-bearing: every engagement runs in plain mode.

## Engagement types and routing

Type by what the job must deliver. Every brief carries one `type:` value.

| `type:` | Selection test | Roster, in running order | Gates |
|---|---|---|---|
| `full-train` | Anything that is not one of the two below | The bench README's [running order](../../../motioncraft/bench/README.md): Director drafts → Finishing audits → story gate → Art drafts → Director audits → appearance gate → Animator drafts → Art audits → motion gate, its one directed revision and the held checks → Finishing drafts → Animator audits → the six technical checks → Sean's artistic yes | Story, appearance and motion gates |
| `small-piece` | **All four hold:** (1) the look is already approved and used unchanged, by checksum; any material design change makes it a full train (never-do 3); (2) the staging is given: one shot, fixed by Sean's brief or an approved board, so there is no story or cut decision; (3) short: one shot, about five seconds or less; (4) no new words | Animator drafts → Art audits → motion gate, its one directed revision and the held checks → Finishing drafts the package and runs the six technical checks → Animator audits → Sean's artistic yes | Motion gate only. The story and appearance gates are recorded in the brief as `NOT FIRED — TRIGGER NOT MET`, with the reason, and never run |
| `one-off` | One seat can answer it with no film delivered: a style frame, a rough board for Sean to react to | One seat, one ledger entry | None |

A test failed at Open makes the job a full train. One that fails mid-run stops the work, and Sean retypes it. A one-off whose answer needs a moving film stops and is retyped. **A seat never widens the job.** Whether a kinetic-type piece is a small piece or a type of its own waits for a second engagement that needs it.

**Two modifiers sit on top of a type, never as types.**

- **Handoff.** A brief arriving from Scriptcraft runs under [the handoff contract](../../../craftwork/handoff-contract.md) and Scriptcraft's binding, once it exists. The Director's intake check is a `kind: intake` pass, its first act `python3 craftwork/trace/freeze.py verify` on every inbound copy; each script id becomes one `ASK<n>` line, and the intake issues `accepted`, `input-required` or `rejected` into `crossing.md` and the Open entry. `originates_from:` is set on the brief and every ledger entry. The return fires **at the story gate**, after Sean's decision there, on [the Scriptcraft return](../../../motioncraft/templates/handoff-return-scriptcraft.md): one line per script id, with **one duration each** from the approved animatic. Motioncraft sends one crossing of its own, the tool brief to Devcraft, at Close (below).
- **Self-targeted.** When the job works on Motioncraft's own machinery (this skill, `motioncraft/`, `craftwork/`, the launcher or the trace kit), Open adds the five duties of [craftwork § Self-targeted modifier](../../../craftwork/law.md#self-targeted-modifier).

## Parts: split by approval state, never by halves of the film

What splits a train is what is already approved against what is new (an approved background behind a changed character, say), never the film's first and second halves.

- **Every appearance packet lists its approved elements**, frozen and unchanged by checksum, **and its new ones.** The appearance gate judges only the new elements, against the approved ones.
- A film takes **one artifact per part** (its own version folders, gate records and Sean's yes) only when its parts reach Sean's yes at different times. The animatic and the finished cut always stay whole.
- A train in parts names them in the brief's `parts:` list. Every pass record at stages 2 and 3 carries `part: <name>`; gate records keep the gate schedule's suffix form (`<eng>.appearance-gate-<part>`, `audits/appearance-gate-<part>.md`, then `-r2`), and so do the revision form and the held checks. The record's `seat:` stays the gate seat.
- Rung-0 line 8 then counts one draft per part at stages 2 and 3, its fixed auditor on each, every part's appearance gate before any motion draft, and by Close an appearance gate and a motion gate per part.

With nothing approved, a train runs unsplit. **mc-eng-001 runs unsplit**: Sean restarted the seed design from scratch (2026-10-18), and the October seed approval stays in the approvals ledger as a non-binding taste reference only.

## Standing success measure

An engagement succeeds only on outside use at Close + 14 days, and Close is declared `ADMINISTRATIVE CLOSE — OUTCOME PENDING D+14`, never success. The authority is [craftwork § Standing success measure](../../../craftwork/law.md#standing-success-measure); Motioncraft's P0-equivalent rule is below, at Open. **The D+14 record never holds up the next job**: the next job may open the day after Close.

## The phases

### 1 — Open

The coordinator's own session, one `kind: open` pass record at stage 0, whose outputs are the brief and anything the chain anchors on. Its `raw_log` is the session's own transcript, the path `python3 craftwork/trace/sessionlog.py` prints from inside it; its meter is `UNMEASURED`. The same holds for the Close record. In order:

1. **Type and privacy class.** Type it (the table above) and name any modifier. The class comes from the source: an SWCB work ticket's `privacy:` field; for a direct ask, Sean says, and if it is unclear the coordinator asks in one line. A `local` stop **writes nothing to the ledger**, which is pushed to GitHub, tells Sean in chat, and stops.
2. **The machine.** One machine per job at a time, the laptop or the Mac Mini, named here so one operator per application holds across machines. **Preflight on that machine:** the applications the roster operates are present (Blender for the Director and the Animator, Krita for Art (run through the application doorway with no screen), Resolve for Finishing, `codex` for the image path, `ffmpeg` and `ffprobe`; Krita is installed on both machines), the studios repo and the private ledger are present, sign-ins and API keys work, and the media folder is mapped by the machine's `media:` setting. Any gap stops the job before it begins.
3. **The brief:** the film, the **sound scope** ("texture and accents only", or the score, voice or dialogue and its source), the words, every one a marked placeholder (`WP<n>`) unless Sean's or arriving locked (rule 8). On a handoff, the Scriptcraft intake.
4. **Mode:** always plain.
5. **The P0-equivalent rule, pre-registered.** For a film, a P0 is **a process or safety failure, never craft or taste**; craft and taste go through the gates and Sean's yes. Four classes: **private material out** (production material, book text or the employer's name in the public repo or an issue; a cloud upload without its approval); **money or work lost** (spend over a cap; an approved version overwritten or missing); **evidence false** (the frames a gate reviewed are not the delivered frames; a check record says pass on something never measured); **a rule gate skipped** (motion before the appearance gate; a version shown to Sean without its id, its status and his prior note, never-do 14).
6. **Budgets** (the table below): the pass cap, two hours of agent work and rendering per stage, the **API spend cap** for generated sound ($10 on mc-eng-001, for Lyria, which bills per call) and its **credits cap** for ElevenLabs sound effects (15,000 credits, 5% of a month's prepaid plan, which can buy no more; Sean's ruling on the sound doorway ticket, 2026-10-19), and the **attention budget**, the number of stops Sean will be asked for: 10 on a full train, 5 on a small piece, 1 on a one-off. Going over it is itself one question to Sean. Any default may change with a stated reason in the brief.
7. **One operator named per file, and per application:** the rule protects files (rule 5): every source file has one seat that may write it, and two seats share a program only in their own files. Name each: the Director, its Blender sequencer file (the animatic and its scratch timing track) and the boards; Art, its Krita files (provisional on E7) and the style targets; the Animator, the Blender scene, Blender only (Fusion is closed for every seat; [the reopen rule](#fusion-stays-closed-the-reopen-rule)); Finishing, the Resolve delivery project, the mix's ffmpeg filter file and the sound doorway (ElevenLabs and the Gemini API for audio, Finishing alone); the Director and Art, the Codex image path through `codex exec`, each into its own version folders. Ruled on the build map's **Tool ownership** ticket (2026-10-20).
8. **Tool approvals and settings confirmed**, each with its tool-specific intended-use approval (never-do 6): ChatGPT's "Improve the model for everyone" off and Codex's "Include environments" checked before any image is generated; each audio service's data-use setting before any sound is. Recorded in `ledger/setup/`.
9. **Read the approvals ledger** (`ledger/approvals/`) as the taste reference, and pull precedent from `ledger/index.md` (two hops: index line → entry).
10. **Open the ledger entry and the folders**, per [the ledger README](../../../motioncraft/ledger/README.md) and the source and version contract: the id `mc-eng-NNN`, the next free number among the briefs' `id:` lines; the ledger's engagement folder and the media folder both named `<project>-<YYYY-MM-DD>`, the ledger's with `artifacts/`, `audits/`, `evidence/` and `trace/logs/`.
11. **Write `brief.md`**, the header first, then the brief:

```markdown
---
id: mc-eng-NNN
name: <a short name>
type: full-train                  # full-train | small-piece | one-off
modifiers: []                     # handoff, self-targeted
parts: []                         # names, only when parts reach Sean's yes at different times
opened: YYYY-MM-DD
closed: null
pass_budget: 21                   # the cap, the coordinator's own session inside it
attention_budget: 10              # Sean's stops
spend_cap_usd: 10                 # generated sound, inside #158's testing total
sound_credits_cap: 15000          # ElevenLabs credits for sound effects; the sound doorway reads both caps
machine: laptop                   # laptop | mini; one machine per job at a time
media: media:<film>/<project>-<YYYY-MM-DD>
sound_scope: texture and accents only
originates_from: null             # the Scriptcraft brief's id, on a handoff
---
```

Then, in a breath each: the film; the sound scope; the words and their placeholders; the P0 rule; the roster and the named operators; the budgets and any change from the defaults with its why; on a small piece, the four tests met and the story and appearance gates `NOT FIRED — TRIGGER NOT MET`; on a train in parts, each part with its approved and new elements; the five self-targeted duties when that modifier is on. The kit reads the header ([craftwork/trace/README.md](../../../craftwork/trace/README.md)); line 8 reads `type:` and `parts:`.

### 2 — Route

Written into the Route entry, before any seat runs.

- **The roster and each seat's runtime from its seat file's `model:` line**, never the session's model, each a ruled row of [the runtime registry](../../../craftwork/templates/runtime-registry.md). Every Codex pass pins `--model gpt-6.1-sol` with its effort spelled out, never the config default and never `ultra`. Fable drives only the coordinator's own session.
- **The alias probe:** one tiny call per pinned id through the launcher, the match read from the log's model stamp, never the answer. Outside the budget; answers into the Route entry; a mismatch goes to Sean before any seat runs. This is Motioncraft's form of [craftwork § The alias probe at Route](../../../craftwork/law.md#the-alias-probe-at-route).
- **Deviations**, each with its one-line why against a named trigger of [craftwork § Model delegation](../../../craftwork/law.md#model-delegation). A mechanical conform or check run may downshift to `claude-sonnet-5-5`; judgement never does.

### 3 — Run

Seats run in the type's order. Every invocation is fresh-context and carries what [the bench says it carries](../../../motioncraft/bench/README.md), never this conversation. No seat launches another. Each pass runs through the Motioncraft launcher under the caps below, in its vendor's [launch form](../../../motioncraft/bench/README.md#launch-forms), inside the launcher's write fence (its own version folders and the engagement folder; gates read-only); until the launch forms are written, no seat pass runs.

**Each pass, in order:**

1. Write the pass record's launch fields ([record-template.md](../../../craftwork/trace/record-template.md); one file per invocation at `trace/pass-NN-<seat>-<kind>.md`, the hash of every input, `part:` on a train in parts). Media inputs are cited as `media:` paths with their sha256.
2. Launch. The prompt states the caps and the seat stops at 90% (`Blocked: budget`); the launcher kills at 100%. Codex writes its final message straight to the artifact's path with `-o`; its raw log goes to `trace/logs/`.
3. On return, the completion fields: outputs and their hashes, the meter or `UNMEASURED`, `## Corpus read` pasted from `python3 craftwork/trace/reads.py <eng>/trace/logs/pass-NN.jsonl`, never typed, `runtime:` from the transcript's model stamp. Run `check.py` once the record is written: a pass that started a helper agent fails line 11, its output is discarded and the pass re-run once; a second spawn stops the engagement Blocked.
4. **Every version a seat saves** is a new version folder, `<artifact>-vNN-<YYYY-MM-DD>`, with its pointer file and checksums, never overwritten (rule 5). Every generated image or sound is downloaded into its version folder on creation with its prompt beside it (never-do 13) and labelled generated (never-do 8).

**The Animator on Codex.** Every Animator pass record on mc-eng-001 carries one line in `## Notes`: "first Codex seat on visual work in any studio; read as a first measurement, not a settled baseline." The labels and the Close's registry line say the same. **One bad pass never moves it off Codex.** Only (a) the ladder running out on a craft fail (the same finding, on the same frames, surviving the redraft at `high` then `xhigh`) or (b) the same tool failure three times triggers **one trial**: the same shot on Opus 5.5, shown to Sean beside the Codex version, blind to vendor (a `trial` record pair, its artifact in `trace/trials/`). Sean picks, recorded in the ledger. A permanent change to the seat's `model:` line is his decision at Close, from that evidence.

**The directed revision.** After Sean names his one change at the motion gate, the coordinator writes [the form](../../../motioncraft/templates/directed-revision.md) from his words, verbatim, before the Animator's revision runs, and never edits it. The form enters the hash chain as an input of the Animator's `repair` pass (with `triggered_by` naming the motion gate's pass) and of the held-checks gate pass, so both records hold its sha256.

**Checks converge** under [craftwork § Checks converge](../../../craftwork/law.md#checks-converge-and-the-ladder-has-brakes): one repair round per artifact per check; round two is a verification pass on the vendor that did not write the repair.

**Ledger writes happen here.** The deciding seat writes an entry at the moment of a material decision, to [the shared schema](../../../craftwork/templates/ledger-entry.md) with its `## From the canon`; ids from `python3 craftwork/trace/nextid.py motioncraft/ledger/engagements/<eng>`. Every session that touched the ledger pushes it before it ends.

**Exits.** A seat that stops returns one typed `exit:` ([artifact-header.md](../../../motioncraft/templates/artifact-header.md#exits)) and the coordinator routes it from that table. A budget stop is `BUDGET STOP — WORK PAUSED` and one variance question to Sean.

#### Fusion stays closed: the reopen rule

Fusion is closed for every seat (Sean, 2026-10-19, on the build map's **Fusion through the doorway** ticket): anything that reaches Fusion can make Resolve run code outside every fence, so the doorway's broker refuses every Fusion call ([the launcher README](../../../motioncraft/launcher/README.md#the-application-doorway)). Anything that moves is animated in Blender; Resolve's API sets fixed values only (opacity, blend modes, position, zoom, crop, rotation, the grade) and cannot keyframe them, so Resolve stacks, cuts, grades and delivers.

1. **The seat stops.** When a pass needs something Blender plus Resolve's edit and colour pages cannot do and Fusion could, it stops on `exit: "Blocked: needs Fusion"` with the need in one sentence, what it tried in Blender by version folder and script, and the frames showing the shortfall. It never works around the doorway, and never swaps the shot's design to dodge the need (that is Art's, or Sean's).
2. **The coordinator checks the evidence.** A pass's own "Blender can't" is not evidence: the frames must show the shortfall, and the attempt must be one the Blender tool guides would recognise as a real try. If the evidence does not hold, the work goes back to the seat as a loopback naming what to try.
3. **If it holds,** the coordinator files **"Fusion for <the need>"** on the Motioncraft build map and tells Sean in one line. That ticket opens only the slice the need calls for: a named list of Fusion methods the broker allows, with expressions, scripts, settings files and Fuses refused and a test that each refused route stays refused (option B's shape on the **Fusion through the doorway** ticket). Nothing opens before it closes.
4. **Meanwhile** the shot waits, or takes a fallback Sean picks. The wait is one of his attention-budget stops.

#### The sound trigger

Three fixed points catch a film that needs more sound than its brief's scope:

1. **Open:** the brief states the sound scope. mc-eng-001 is texture and accents.
2. **Stage 1:** the Director marks any beat that needs music or a voice in the animatic's scratch sound, and Finishing re-checks at its audit of the story packet.
3. **Stage 4:** Finishing's sound plan is the last catch.

Whoever spots it stops (`Blocked: Sean's call`). Sean picks one: cut back to texture and accents, he supplies it, or it is generated or routed outside. **No seat composes music or writes a line.** **Dialogue is Sean's:** he records it and runs the voice changer himself; it arrives as source on Finishing's `Blocked: needs source` exit, its words under rule 8.

**Generated sound.** Finishing is the sole operator of ElevenLabs (sound effects, on a paid plan) and the Gemini API's Lyria (music, on a billed project); no other seat generates sound, and the Director's animatic keeps rough scratch sound. Finishing's sound plan lists each cue with its prompt and tool, and **Sean approves the list in one decision** before anything is generated. Up to three takes per cue; Finishing picks and places them in the edit timeline, and Sean hears them in the cut. Reaching either cap is a checkpoint. Finishing reaches both services only through the sound doorway ([the launcher README](../../../motioncraft/launcher/README.md#the-sound-doorway)), which sends a cue only from the approved list's locked copy, counts the takes and meters both caps. Keys are Sean's to place, outside every repo.

### 4 — Gate

When each gate fires, what it reads and may demand, its vendor, what it attacks, and Sean's four decisions after it are [the gate schedule](../../../motioncraft/templates/gate-schedule.md); the posture and typed verdicts are [the shared protocol](../../../craftwork/templates/red-team-protocol.md). A gate never silently skips; every gate writes its ledger entry. The firing order, by type:

- **Full train:** story gate → (on a handoff, the Scriptcraft return) → appearance gate, once per part on a train in parts, every part passed and approved before any motion → motion gate, once per part, then its one directed revision and the held checks → the integrated film: the Animator's audit, the six technical checks, Sean's artistic yes. The integrated film is not a gate.
- **Small piece:** motion gate → its one directed revision and the held checks → the integrated film.
- **One-off:** none.

**Sean's decision follows every gate** and is copied into the approvals ledger with his words and date. A version goes to him with its id, its status and his prior note on it (never-do 14), inside his checkpoint (#158: up to three short clips or stills, one recommendation, one decision). The coordinator claims the camera ticket for a world shot when the train reaches that shot's appearance gate, never before.

**Retakes.** An artistic or technical retake after a PASS opens a fresh series and adds three passes on top of the cap (the new draft, its audit, the gate again), because Sean asked for the work. A **third retake on the same stage** counts as #158's three repeats of the same failure: the job stops for a checkpoint with the evidence and one recommended next step.

### 5 — Close

The coordinator's own session, one `kind: close` pass record. In order:

- [ ] **Ledger complete**: every entry written, the Close entry among them; one line per entry appended to `motioncraft/ledger/index.md`.
- [ ] **Every version Sean saw** is in the approvals ledger with his words and date; every approved version frozen as a read-only copy in the media folder's `approved/<version-id>/`, its path and sha256 in the approvals entry.
- [ ] **Trace 1, check**: `python3 craftwork/trace/check.py motioncraft/ledger/engagements/<eng>`. Every rung-0 line PASS, or each FAIL fixed in the record it names, never by editing an artifact after its pass.
- [ ] **Trace 2, render**: `python3 craftwork/trace/render.py motioncraft/ledger/engagements/<eng>`, local only, never hosted. Do not open it for Sean or show him its labels until he completes or declines the optional blind sample in the next step.
- [ ] **Trace 3, labels**: every pass has a row with a verdict in `trace/labels.md`, coordinator-drafted and Sean-approved, and its provenance block says so. Before showing the draft, offer Sean the optional [blind Close sample](../../../craftwork/trace/README.md#optional-blind-close-sample), run exactly as that section says (`close_sample.py draw`, then `compare` only after his answers are saved); record whether it was used or declined. Labels follow [labels-row.md](../../../motioncraft/templates/labels-row.md): a pass's row is never Sean's verdict on the film.
- [ ] **Trace 4, registry numbers** across **every** studio's traced engagements, since the numbers are shared: `python3 craftwork/trace/registry.py $(find productcraft/ledger/engagements systemcraft/ledger/engagements devcraft/ledger/engagements motioncraft/ledger/engagements -mindepth 2 -maxdepth 2 -name trace -type d -exec dirname {} \; | sort)`, and replace § Numbers of the runtime registry with its output.
- [ ] **SWCB `raw/`** gets a **text record of the finished film only**, once Sean marks it good: the film's name, the approved version id and date, the frozen copy's path and sha256, and a link to its approvals entry. No media.
- [ ] **Devcraft**: each `devcraft:` adjacent-lane line becomes a tool request sent on [the binding](../../../motioncraft/templates/handoff-binding-devcraft.md), or a written no-handoff verdict. The film never waits on Devcraft.
- [ ] **Live deferred work**: one issue each on `seanwinslow28/SWCB`, labelled `needs-triage`.
- [ ] **Private layer**: `git status` shows nothing under `motioncraft/{corpus,ledger,books}/`; then commit and push the ledger's own repo (`git -C motioncraft/ledger add <paths> && git -C motioncraft/ledger commit -m "<eng>: <close gist>" && git -C motioncraft/ledger push`), and confirm the Drive backup of the studio media folder has synced.
- [ ] **Freeze** the P0-equivalent count (Sean ratifies), one rule-8 ticket per P0 finding with his dated disposition, set the D+14 outcome-record date, and declare `ADMINISTRATIVE CLOSE — OUTCOME PENDING D+14`.
- [ ] **The explain-why digest** per [the close digest](../../../craftwork/templates/close-digest.md): recommendation first, one question, statuses per [the status vocabulary](../../../craftwork/templates/status-vocabulary.md).

The Scriptcraft return is not a Close step: it fired at the story gate.

## Pass budget and launcher caps

Day-one defaults. Any Open may change them, with a stated reason in the brief.

| Type | Base passes | Rounds | Cap |
|---|---|---|---|
| `full-train` | 15: Open and Close, each stage's draft and audit, the three gates, the directed revision and its held checks | +6: one `-r2` round per gate, with its redraft | **21** |
| `small-piece` | 9 | +2 | **11** |
| `one-off` | 1 | none | **1** |

A train in parts adds each extra part's draft, audit and gates at stages 2 and 3, said in the brief. Sean's retakes add three passes each on top of the cap (above). The coordinator's own session counts inside the cap. Exhaustion is a stop: actual against cap, and one variance question to Sean, never a silent overrun.

**Per stage:** #158's two hours of agent work and rendering, per stage (story, appearance, motion, finish). Reaching it is a checkpoint: up to three clips or stills, one recommendation, one decision. A limit reached is never a lower bar (never-do 5).

**Per pass:** Claude seats and the motion gate 30 minutes and `--max-budget-usd 15`; the Animator on Codex 60 minutes and 200 tool calls; the Codex gates 20 minutes and 80 tool calls. A killed pass is filed `Blocked: budget` with what it left on disk. Every pass records a meter line, or `UNMEASURED`, never an estimate.

**Availability.** An unavailable runtime follows [craftwork § Availability ladder](../../../craftwork/law.md#availability-ladder): a dated, Sean-approved substitution from a registry row, or a dated deferral. Never a merged lane or a silent switch.

## Where jobs run

Both machines, the laptop and the Mac Mini, so no train is tied to one. **One machine per job at a time**, named at Open and preflighted there. **Moving a job mid-run is a clean handover**: finish the current pass, push the ledger, sync the media, record the move in the ledger, reopen on the other machine. Every job runs in sessions Sean starts, on either machine, Remote Control included; unattended operation waits for its own ruling.

## Degradation

On a machine without the private layer (a fresh clone, an employer machine), the seats already carry the ladder (`manifest-only`, then `none`). The skill's own duty is to say so once at Open and proceed, never fabricating ledger precedent or corpus grounding it cannot read. With no media folder mapped, no film job opens; a one-off may still run on what it can read.
