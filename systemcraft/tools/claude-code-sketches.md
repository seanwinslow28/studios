# Claude Code for sketches

A sketch is a cheap working version of a design, built to prove the design before another studio builds it properly. Systemcraft builds its sketches out of Claude Code's own parts and runs them with nobody at the keyboard, on Sean's Claude plan. Read this before turning a design on paper into something that runs. Devcraft's guide to Claude Code covers building software with it; this one adds only what a sketch needs.

## What it's best at

- **A design's parts already exist as small text files,** listed below.
- **Every run reports on itself:** its turns, its tokens (a token is a piece of a word; models are billed by the token) and an estimate of its cost.
- **Every run can be capped,** on turns and on spend.

Where another tool beats it: a sketch that must be a standalone program needs the Claude Agent SDK and a pay-per-use key, which Sean has said "not now" to. Checks worth repeating belong in promptfoo.

## Setup

Nothing to install or buy. The command that proves it works, from an empty folder:

```bash
claude -p "Reply with one word: ready" --model haiku --tools "" --max-turns 1 \
  --setting-sources project --strict-mcp-config --output-format json < /dev/null
```

It prints one block of JSON (text laid out as named fields) holding `"result":"ready"` and `"total_cost_usd"`, about $0.0007 when tested.

## Which part plays which role

| In the design | The part | Where it lives |
|---|---|---|
| Instructions and reference, loaded only when the task calls for them | A skill | `.claude/skills/<name>/SKILL.md` |
| A worker with its own separate memory and its own tool list | A helper (Claude Code calls it a subagent) | `.claude/agents/<name>.md` |
| A rule that must hold every time | A hook: ordinary code that Claude Code runs at a fixed moment, such as just before a file is written | `.claude/settings.json`, plus a script |
| What the run may and may not do | The tool list and permission rules | Flags on the command, and `deny` rules in `.claude/settings.json` |
| Memory between runs | Plain files | The sketch's own folder |

- **A helper's file names its `tools` and `model` at the top.** Adding `--agent checker` to a run makes the whole run that helper, with only its tools.
- **A hook enforces; an instruction only asks.** A hook that exits with code 2 blocks the step, and its error text goes to the model.
- **A `deny` rule in the folder's settings always holds.** An `allow` rule there is ignored, with a warning, until the folder has been trusted in a normal session. Allow things on the command instead.

Devcraft's `claude-code.md` covers each part in more depth.

## Running with nobody at the keyboard

`claude -p "prompt"` runs once and exits. The flags a sketch needs:

- `--output-format json` gives one result at the end. `stream-json` with `--verbose` prints every step.
- `--json-schema '<shape>'` makes the answer fit a shape you define. It arrives in the field `structured_output`.
- `--max-turns 6` stops a run that wanders: `"subtype":"error_max_turns"`, exit code 1.
- `--max-budget-usd 0.10` stops it on cost: `"subtype":"error_max_budget_usd"`, exit code 1. A run can pass the cap a little: a test capped at $0.0001 spent $0.0003.
- `--model haiku` picks the model; the others are `sonnet`, `opus` and `fable`. Start on `haiku`.
- `--tools "Read,Write"` is the run's whole list of built-in tools; `""` means none.
- `--allowedTools "Edit(draft.md)"` says what may happen without asking: here, writing that one file.
- `--permission-mode dontAsk` refuses anything not allowed.
- `--setting-sources project --strict-mcp-config` loads the sketch folder's own parts and none of the Mac's other add-ons.
- `--resume <id>` carries on an earlier run, using the `session_id` from its result.

**A step that would ask permission is refused, and the run carries on.** It still ends with exit code 0 and `"subtype":"success"`. The refused steps are listed in `permission_denials`, so the script must check that list is empty.

**What a run reports:** `total_cost_usd`, `num_turns`, `duration_ms`, `usage` (tokens in and out) and `modelUsage` (the same for each model, helpers included). The dollar figure is Claude Code's own estimate at list prices. On the plan nothing is billed for a run; it draws on the plan's usage limits. A resumed run reports the whole conversation's total.

## A worked example

The smallest sketch of the long-job harness on the shelf: a maker, a separate checker, written pass marks. A made-up bakery needs a notice for its door. `brief.md` says closed Monday, oven repair, open Tuesday at 7am. `pass-marks.md` says: names the day; says when it reopens; 30 words or fewer; no exclamation marks.

```bash
#!/bin/bash
common=(--model haiku --setting-sources project --strict-mcp-config
        --permission-mode dontAsk --max-turns 6 --max-budget-usd 0.10
        --output-format json)
shape='{"type":"object","properties":{"pass":{"type":"boolean"},
  "failed":{"type":"array","items":{"type":"string"}}},"required":["pass","failed"]}'

claude -p "Read brief.md and write the notice to draft.md." "${common[@]}" \
  --tools "Read,Write" --allowedTools "Edit(draft.md)" < /dev/null > maker.json

claude -p "Read pass-marks.md and draft.md. Mark the draft against every pass mark." \
  "${common[@]}" --tools "Read" --json-schema "$shape" < /dev/null > checker.json

jq '{subtype, num_turns, total_cost_usd, denied: (.permission_denials | length)}' \
  maker.json checker.json
jq '.structured_output' checker.json
```

Two runs, and `draft.md` between them. The maker never sees the pass marks. The checker never sees the brief or the maker's thinking, and can only read. Run five times, the checker failed all five drafts: an exclamation mark every time, too long most times. Each pair of runs cost about $0.003.

They also showed a flaw. On one draft the checker passed the length while a plain word count said 31; they disagreed over a heading mark. A pass mark that can be counted belongs in the script, not with the model.

## Getting the best out of it

- **Fixed steps in the script, the model only where judgement is needed.** This is Stripe's design from the shelf. The order of the stages, counting and adding up cost are shell. Writing and judging are the model's.
- **One bounded task for each helper,** with a short tool list. The checker above cannot write, so it cannot fix the draft itself.
- **A checker that sees something different from the maker.** The shelf's harness found that a model marking its own work is too kind to it.
- **Pass marks written down before the first run.**
- **A cap on turns and on spend for every run,** and a fixed number of rounds in the script.
- **Record what each stage cost.** The shelf's harness could say planning cost $0.46 and each check $3 to $4.
- **Keep the Mac's add-ons out.** The same one-word run loaded about 52,000 tokens and cost $0.0104 with Sean's usual add-ons, and about 4,000 tokens and $0.0007 without.
- **Run it several times.** One good run proves little.
- **Read the saved record of the run afterwards.** See `transcripts-and-phoenix.md`.

## Where it goes wrong

- **The sketch grows into the product.** Once it has answered its question, stop. Retries, tidy errors and a schedule belong to the building studio.
- **A hook that fails silently.** A hook meant to block that exits with code 1, not 2, lets the step through, and the result says nothing. Test every hook with a step it should block.
- **A run that waits, or quietly skips.** If the Agent SDK or `--permission-prompt-tool` is set up to answer permission questions and nobody does, the run waits; `--permission-prompts none` refuses instead. Otherwise the step is refused and the run still reports success.
- **A test written after seeing the output.** It passes because it was shaped to. Write the pass marks first.
- **The folder's own hooks, in someone else's folder.** A run with nobody at the keyboard never asks whether the folder is trusted; its hooks just run.

## Safety

- **What a run spends.** No money on the plan, but each run uses up the same limits as Sean's own sessions. Cap each run and the number of runs.
- **What it sends.** The prompt, every file the run reads and every tool result go to Anthropic. A record is saved on the Mac. Sketches use made-up material, never day-job material.
- **Never point a run at a folder someone else wrote** before reading its `.claude` folder and its `.mcp.json` file. Its hooks and connected tools would start without a question.
- **Never use a flag that skips permission checks.**
- **Ask Sean first** before a sketch reads real material, reaches the network, sends anything, runs in a folder he didn't write, or runs a batch big enough to dent the plan's limits.

## More details

**Checked November 16, 2026** on this Mac: Claude Code 2.1.325 at `~/.local/bin/claude`, signed in with Sean's plan, no API key set. jq 1.7.1.

**Run and seen** (29 small runs on `haiku`, about $0.05 in all by their own estimates, in a scratch folder):

- The setup command, with and without the two add-on flags. `--safe-mode` cost less still ($0.0002) but switches off the folder's own parts.
- A turn limit and a spending cap being hit; a write refused, with no mode set and with `dontAsk`.
- Both code blocks above, exactly as printed; the worked example seven times in all.
- In a never-trusted folder: a hook running and blocking with exit code 2; the folder's `allow` rules ignored with the warning "this workspace has not been trusted"; its `deny` rule holding.
- A hook exiting with code 1: the write went ahead. Only `--output-format stream-json --verbose --include-hook-events` showed it, as `"outcome":"error"`.
- A folder's skill and helper loading and being used; `--agent checker` leaving only the Read tool. One run calling the helper cost $0.005, against $0.003 for two runs.
- `--resume` keeping the session and reporting the running total.

**Worth knowing:**

- `--max-turns` works and is in the documents, but `claude --help` doesn't list it.
- Without `< /dev/null`, a run started from a script waits three seconds for input and prints a warning.
- zsh doesn't split a variable holding several flags; use a bash array as above.
- `--bare` needs a pay-per-use key, so sketches don't use it.

**From the documents, not tested:** `--continue` carries on the latest run in a folder. `"onFailure": "block"` makes a failing hook block (2.1.295 or later). `--setting-sources user` or `--settings '{"disableAllHooks": true}'` keeps a folder's hooks out. `.mcp.json` servers connect without asking under `-p`. The wait at a permission question.

**Could not confirm:** each model's price (read the price page for each job); whether paid top-ups past the plan's limit are on for Sean's account, which would make a runaway batch cost money.

**Sources,** all read November 16, 2026: `claude --help`; [script runs](https://code.claude.com/docs/en/headless); [flags](https://code.claude.com/docs/en/cli-reference); [permissions](https://code.claude.com/docs/en/permissions); [modes](https://code.claude.com/docs/en/permission-modes); [hooks](https://code.claude.com/docs/en/hooks); [subagents](https://code.claude.com/docs/en/sub-agents); [skills](https://code.claude.com/docs/en/skills); [cost tracking](https://code.claude.com/docs/en/agent-sdk/cost-tracking); [costs](https://code.claude.com/docs/en/costs).
