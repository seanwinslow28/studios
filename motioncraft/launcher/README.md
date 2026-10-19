# The launcher

Motioncraft's launcher runs one seat pass on either vendor, under its caps and inside its write fence, and leaves the logs the pass record is built from. Built on the Motioncraft build map's **Build the slim Motioncraft launcher** ticket (2026-10-19), as ruled on Master skill design (SWCB #192, item 10): a slim copy of Devcraft's [`seat.py`](../../devcraft/hooks/seat.py) with only what Motioncraft needs, Devcraft untouched. The master skill's Run phase launches every pass through it; the per-seat launch forms and plugin allowlists are the **Plugin allowlist and launch form for seat runs** ticket's, written against it.

Kept from Devcraft: the per-pass caps and the kill at 100%, the model probe, the isolated launch on both vendors, the vendor read from a record (a gate's anchor, a verification pass's repair, a redraft's escalation), helper-agent detection, the scratch folder, and the logs. Added: the write fence and the machine check. Left with Devcraft: the guard hook, the git hooks, worktrees, the frozen diff and the release gate's evidence, all built around code.

| Command | What it does |
|---|---|
| `seat.py context --seat S --engagement E --pass NN [...]` | Writes `<E>/trace/logs/pass-NN.context.json`, once: the seat, the vendor and the record that says so, the caps, the effort, the machine, the media project read from the brief's `media:` line, the scratch folder, and the fence |
| `seat.py claude-settings <context>` | A pass on Claude: its settings file, sandbox on and failing closed |
| `seat.py codex-home` | The Codex seat home, `~/.codex-motioncraft`: plugins, apps, memories, multi-agent and image generation off, a read-only floor |
| `seat.py codex-pass <context>` | A pass on Codex: its permission layer, linked into the seat home as `<eng>-pass-NN.config.toml` |
| `seat.py launch <context> --prompt-file F [--output A] --run` | Runs the pass and writes `pass-NN.jsonl`, `pass-NN.stderr.log`, `pass-NN.launch.json` and, on Codex, `pass-NN.rollouts/` into `trace/logs/` |
| `seat.py probe [--logs DIR]` | The alias probe at Route: one tiny call per pinned id, printed as the Route entry's lines |
| `seat.py check` | This machine's preflight for the launcher: both CLIs, the `media` folder mapped, the employer-path list, the seat home set up and signed in |

The coordinator runs these; no seat does. Without `--run`, `launch` prints the command line, the environment's names, the caps and the fence, and starts nothing.

## The context

Everything a pass runs under is fixed in its context, written once before the pass, and the launch reads only that.

- **Seats.** The four seats (`visual-story-director`, `art-pose-designer`, `animator`, `finishing-sound-designer`) and the three gates (`story-gate`, `appearance-gate`, `motion-gate`, the held checks among the motion gate's passes).
- **Vendor, read from a record, never chosen.** A gate names its anchor with `--anchor artifacts/<file>` and runs on the vendor that did not last write it, read from the anchor's `model:` line. A verification pass names the repair with `--verify` and runs read-only on the other vendor. A redraft one tier up names its record with `--escalation` (a gate FAIL in `audits/`, or a `dNN-` ledger entry that names the step): a Claude seat's redraft runs on Codex at `high`; the Animator's takes `--effort xhigh`, the one step its ladder has before Sean. `--fallback <issue>` keeps a gate on the writer's vendor when the planned one is unavailable. The record's hash goes in the context, and a record changed since stops the launch.
- **Caps** ([master skill § Pass budget and launcher caps](../../.claude/skills/motioncraft/SKILL.md#pass-budget-and-launcher-caps)): Claude seats and the motion gate 30 minutes and `--max-budget-usd 15`; the Animator 60 minutes and 200 tool calls; the Codex gates 20 minutes and 80 tool calls. A pass moved to the other vendor takes that vendor's caps for its kind: on Claude 30 minutes and $15, a read-only pass on Codex 20 and 80, a redraft on Codex 60 and 200. `--cap-*` changes them, with the why in the brief.
- **The machine.** The context records the machine it was written on, and `launch` refuses on any other: one machine per job, and a job moved to the other machine writes its next context there.
- **Network.** Off on Codex. On Claude, only the hosts `--host` names.

## The write fence

Read from the brief's `media:` line and the machine's `folders.local` ([the trace kit's named folders](../../craftwork/trace/README.md)), so it works the same on the laptop and the Mini. A brief without one, or a `media` name this machine has not set up, stops at `context`: no film job opens without its media folder.

| Pass | May write | Frozen inside it |
|---|---|---|
| A drafting seat, or its redraft | its own stage folder in the media project (`story/`, `appearance/`, `motion/`, `finish/`), for new version folders; on Claude, the engagement's `artifacts/`, for new files | every version folder and every artifact already there when the context was written |
| A gate, an audit (`--read-only`), a verification pass | nothing | |
| Every pass | its scratch folder, `~/.cache/motioncraft/scratch/<eng>/pass-NN/`, outside every repo, new and empty, and its `TMPDIR` | |

A pass on Codex never writes the engagement folder: its one output, the scene record or the gate's findings, is its final message, which `-o` files. A read-only pass on Claude gets `Write` for its scratch folder only, and the launcher files its final message with `--output`. Nothing outside these folders is writable, so a seat never touches another seat's stage, `inputs/`, `approved/`, the brief, the ledger entries, the trace, or the studio's own files.

Every pass is denied reading credentials, Sean's own `~/.codex/` (Codex's install inside it stays readable on Codex, which re-runs it), the engagement's other scratch folders, and the folders on the machine's employer-path list (`~/.config/devcraft/employer-paths`, one list per machine, written by hand and never tracked). The wall files hold those paths, so they live in `~/.config/motioncraft/passes/<eng>/`, outside every repo, written once.

**What it holds by.** On Codex, the permission layer, enforced by Codex's own sandbox: the tests run each Codex layer through `codex sandbox`, the real policy, with no model call. On Claude, the settings file and the working folders. Commands run in the sandbox, whose write list is the fence. The file tools run outside the sandbox and write only inside a pass's working folders, so a pass is given only the folders the fence lets it write (`--add-dir`; none for a read-only pass, whose working folder is its scratch), `Edit` denies freeze what is already in them, and `Read` rules let it read the engagement, the media project, `motioncraft/`, `craftwork/` and the studios `AGENTS.md` from outside them. A live Director pass on 2026-10-19 confirmed both halves: it wrote a new version folder and a new artifact; its shell and its Write tool were refused on a saved version, another stage, the brief, a new file or folder at the engagement's top level and the media project's, and the employer folder. A file created after the context was written is outside the frozen list.

## The launch

- **Isolated.** A scrubbed environment (no tokens, stdin closed). Claude: `--setting-sources ""`, `--strict-mcp-config`, the scratch folder as its working folder, a limited `--tools` list with no tool that starts a helper, the studios `AGENTS.md` by flag, the seat's own plugin from `motioncraft/bench/plugins/<seat>/` once the allowlist ticket writes it, and no hooks. Codex: from the seat home with `-p <eng>-pass-NN`, `--model gpt-6.1-sol` and the effort spelled out, never the config default and never `ultra`, web search off, the media project as its working folder, marked untrusted.
- **Caps.** The launcher watches the live log and kills the pass's whole process group at 100% of a cap (wall clock, or tool calls counted from the log); Claude stops itself at its budget. Either stop is filed `Blocked: budget` with what the pass left on disk, exit 2. The prompt states the caps, so the seat stops itself at 90%.
- **Helper agents.** On Codex the session files are saved to `pass-NN.rollouts/` and read as rung-0 line 11 reads them; on Claude the log is read for a `Task` or `Agent` call or a helper's message. Either way the output is moved aside to `pass-NN.discarded.md` and the launcher exits 3: re-run once as a new pass, and a second spawn stops Blocked.
- **The record.** `pass-NN.launch.json` holds what the pass record's completion fields need: times, tool calls, the stop, the machine, the media project, the fence, the wall file's path and hash, the outputs and their hashes, the raw usage and its meter source, and the runtime stamps from the log.

## The probe

`seat.py probe` asks `claude-opus-5-5` on `claude -p` and `gpt-6.1-sol` (high) on `codex exec`, from the seat home, for their own ids, and reads the match from the log's model stamp, never the answer. Exit 1 on any mismatch, which goes to Sean before any seat runs. `--logs <eng>/trace/logs/route` keeps both raw logs.

## Tests

```bash
cd ~/Code-Brain/studios && uv run --no-project --with pytest python -m pytest motioncraft/launcher/tests -q
```

The fence's Codex half runs through `codex sandbox`, the real Seatbelt policy (skipped where Codex is not installed); the context, both walls, the launch forms, the caps, the kill, the helper catch on both vendors, the machine check and the probe run against a fake `claude` and `codex` put first on `PATH`.
