# Transcripts and Phoenix

Claude Code saves a full record of every session on the Mac: each message, each tool call and what came back. That record is a transcript, and reading one from top to bottom is how Systemcraft sees what a run did. Phoenix is a free viewer for the day reading stops being enough. It has not been needed yet, so it has never been run on this Mac. Facts were checked on November 16, 2026 against Claude Code's documents, a test run on this Mac and Phoenix's documents.

## What they're best at

- **A transcript: the truth about one run.** What the model was shown, what it did and what came back, in order. Free, already on the Mac, nothing to switch on.
- **Phoenix: many runs, or one very long one.** It lists runs side by side and draws each as a tree that folds.

Where something else beats them: ccusage for what past runs cost, promptfoo for checks worth repeating.

## Where transcripts live

- **One folder per project,** inside `~/.claude/projects/`. The name is the working folder's path with every character that isn't a letter or digit turned into a dash: `/Users/sam/Code/letting-bot` becomes `-Users-sam-Code-letting-bot`.
- **One file per session:** `<session-id>.jsonl`. A run started with `claude -p --output-format json` prints its `session_id`, and `ls ~/.claude/projects/*/<session-id>.jsonl` finds the file.
- **A helper's record sits beside it.** A helper (Claude Code's word is subagent) gets its own file, `<session-id>/subagents/agent-<id>.jsonl`, plus a small `.meta.json` naming its kind and its job. The main file holds only the brief it was sent and the report it sent back.
- **Large tool results are stored aside,** in `<session-id>/tool-results/`.
- **How long they are kept:** the setting `cleanupPeriodDays` in `~/.claude/settings.json`. The default is 30 days and the least is 1, so check what this Mac is set to before counting on an old run still being there. Sessions from the desktop app are kept at any age unless `desktopSessionCleanupPeriodDays` is set.

The command that proves it works, with a made-up project:

```bash
T=$(ls -t ~/.claude/projects/-Users-sam-Code-letting-bot/*.jsonl | head -1)
jq -r .type "$T" | sort | uniq -c
```

It counts the newest transcript's lines by kind. Run it first, every time. If `user` and `assistant` are missing, the format has changed and the commands below will print nothing.

## The shape of a record

A transcript is a text file with one JSON object (a record with named fields) on each line. The format is Claude Code's own, and its documents say it changes between versions, so any command here can break on a new release. On version 2.1.325 the lines that matter are:

- **`user`:** `message.content` is plain text (a prompt) or a list of `tool_result` items (what a tool sent back). A failed tool has `is_error: true`. A line with `isMeta: true` came from the harness, the set-up around the model, not from a person.
- **`assistant`:** `message.content` is a list. `text` is the model's words. `tool_use` is a tool call, with its `name`, `input` and `id`. `message.model` names the model, and `message.usage` holds the token counts (a token is a piece of a word, and models bill by the token).
- **`attachment`:** text the harness added for the model, such as the date.
- **`api-request-shape`:** the system prompt and tool definitions the model was sent.
- **`cost-state`:** the session's cost and tokens for each model, helpers included.

The rest is bookkeeping. In the test run the model's private thinking was stored blank: the record shows that it thought, not what.

## Reading one whole

Each command below was run on the test transcript. They work on a helper's file too.

```bash
# Just the conversation
jq -r 'select(.type=="user" or .type=="assistant") | .message as $m
  | ($m.content | if type=="string" then [{type:"text",text:.}] else . end)[]
  | select(.type=="text") | "\($m.role|ascii_upcase): \(.text)\n"' "$T"

# Every tool call, in order
jq -r 'select(.type=="assistant") | .timestamp[11:19] as $t | .message.content[]
  | select(.type=="tool_use") | "\($t)  \(.name)  \(.input|tostring|.[0:100])"' "$T"

# The first error, and its line number in the file
jq -c 'select(.type=="user") | .message.content | arrays | .[]
  | select(.type=="tool_result" and .is_error==true)
  | {line: input_line_number, said: (.content|tostring|.[0:200])}' "$T" | head -1

# Tokens for each reply: new, stored for reuse, reused, written
jq -r 'select(.type=="assistant") | .message | [.id, .model, .usage.input_tokens,
  .usage.cache_creation_input_tokens, .usage.cache_read_input_tokens,
  .usage.output_tokens] | @tsv' "$T" | awk '!seen[$1]++'

# The helpers that were started
jq -r '[input_filename, .agentType, .description] | @tsv' "${T%.jsonl}"/subagents/*.meta.json
```

Then read, the way the shelf's field guide does. Look for:

- **The first place it went wrong, not the last.** Later failures are often its children.
- **What the model was shown just before.** If the first error is on line 26, `sed -n '22,26p' "$T" | jq -c .message.content` prints the lines above it. A wrong step often follows a missing or misleading tool result.
- **Tool results it ignored.** An error comes back and the next message carries on as if it hadn't.
- **The same step repeated.** The same call with the same input, three times or more, means it is stuck.
- **Where it claimed done, and what proof it had.** Find the tool result that backs the claim. No result, no proof.

Write one plain note for each failure, group the notes, count each group and fix the biggest.

The difference it makes: the test run was asked three things and printed one line, about what its helper had replied. It looked like a run that skipped most of the job. The transcript showed the other two answers in an earlier message, written while the helper was still working. Only the last message had been printed.

## When reading whole stops working

Three signs: one transcript is too long for a sitting, there are too many runs to compare, or helpers started helpers and the story is spread over many files. Try the short lists first. The tool calls and the first error stay short however long the file is.

## What Phoenix adds

**Everything in this part is from Phoenix's documents, not yet run on this Mac.**

Phoenix is a free program from Arize that stores recorded runs and shows them in the browser. The one command, with its two outside-reporting switches off:

```bash
PHOENIX_TELEMETRY_ENABLED=false PHOENIX_ALLOW_EXTERNAL_RESOURCES=false uvx arize-phoenix serve
```

`uvx` fetches Phoenix on first use and starts it. The proof it works: the viewer opens at `http://localhost:6006`, and the start-up text says where its database is.

- **It cannot open a saved transcript.** Nothing in its documents loads a transcript after the fact. It shows only runs recorded into it while it was running, so it has to be started and connected before the run.
- **Three ways in.** Claude Code can send to it directly, with its own run-recording export. That export is in beta and leaves out prompts and tool results unless told to include them, and Phoenix's documents don't cover it. The route they do cover is Arize's plugin for Claude Code, whose hooks rebuild each turn from the transcript; that is an install, so ask Sean. A program built with the Claude Agent SDK uses a kit made for it, and needs the pay-per-use key Sean has said "not now" to.
- **Where it keeps data:** a single database file in `~/.phoenix/`, kept until deleted. It listens only on the Mac itself.

## Where it goes wrong

- **Counting tokens twice.** One reply is saved as several lines, each repeating the same counts. The token command above keeps one line for each reply.
- **Reading only the main file.** A helper's steps are in its own file, and a background helper's report arrives later as a `user` line.
- **An empty answer taken as good news.** If the format changes, a command prints nothing, which looks like "no errors". A check that says "fine" isn't proof. And `is_error` marks only failures the tool reported, not a command that ran and gave the wrong thing.
- **A stub in place of a result.** A very large tool result shows as a short preview; the full text is in `tool-results/`.
- **No transcript at all.** A run started with `--no-session-persistence` saves none, and old ones are deleted at the age limit.

## Safety

- **A transcript holds everything the session saw:** file contents, command output, pasted text, the system prompt. It is plain text, not locked. Nothing from one is ever pasted into the public repo, an issue or a page. Examples are made up.
- **Reading one inside a Claude session sends that text to Anthropic again.** Narrow it with `jq` first.
- **The hosted recorders upload every recorded step, prompts included.** The plugin's installer offers hosted Arize as well as Phoenix. Choose Phoenix.
- **Phoenix, left alone, does reach the internet:** page-view tracking from its viewer, and downloads of fonts, model prices and a code-running part. Its documents say no run data leaves. The two switches in the command stop all of it.
- **Ask Sean first** before installing the plugin, or deleting transcripts with `claude purge`.

## More details

- **Test run, November 16, 2026:** Claude Code 2.1.325, jq 1.7.1, in an empty scratch folder holding one small text file. One `claude -p` run on the cheapest model (`--model haiku`, which gave `claude-haiku-5-5`), with `--max-turns 8 --safe-mode --tools "Read,Agent" --permission-prompts none --output-format json`. It read the file, tried a missing file, and started one helper. Cost $0.003. Result: a 59-line transcript of 13 kinds of line, plus `subagents/agent-<id>.jsonl`, `.meta.json` and `.prefix.json`. Every command above was run on it. No other transcript was opened; folder and file names were listed to learn the layout.
- **Claude Code's documents, read the same day:** where transcripts are stored and the warning that the format changes (https://code.claude.com/docs/en/sessions), what is kept and for how long (https://code.claude.com/docs/en/claude-directory), helpers' files (https://code.claude.com/docs/en/sub-agents), flags (https://code.claude.com/docs/en/cli-reference), the run-recording export (https://code.claude.com/docs/en/monitoring-usage).
- **Claude Code's export to Phoenix, from that last page:** set `CLAUDE_CODE_ENABLE_TELEMETRY=1`, `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1`, `OTEL_TRACES_EXPORTER=otlp`, `OTEL_EXPORTER_OTLP_PROTOCOL=grpc` and `OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317`. Content needs `OTEL_LOG_USER_PROMPTS=1`, `OTEL_LOG_TOOL_DETAILS=1` and `OTEL_LOG_TOOL_CONTENT=1`.
- **Phoenix, read the same day, not run:** https://arize.com/docs/phoenix (start-up, ports 6006 and 4317, settings, the Claude Code page), https://github.com/Arize-ai/phoenix and https://github.com/Arize-ai/coding-harness-tracing. Newest release 21.0.0, October 30, 2026, an 8 MB package that needs 53 others and Python 3.11 or newer. Elastic License 2.0.
- **Could not confirm:** how Phoenix displays Claude Code's own export. Where the database really lands: the code says `~/.phoenix/phoenix.db`, one settings page says a temporary folder. The size of the full download. How a transcript looks after a long session is shortened into a summary. The plugin's notes say background helpers are not yet fully rebuilt.
