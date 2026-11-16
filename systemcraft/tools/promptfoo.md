# promptfoo

promptfoo is a free tool for checks worth repeating. The test cases sit in a short text file, one run puts every case through the design, and the results show side by side: one row a case, one column a version of the prompt. It comes second. First the lead reads real outputs by hand and writes down what good means. And it always runs with its reporting to its maker switched off. Facts below were checked on November 16, 2026, in promptfoo's own documents, the installed copy and test runs on this Mac.

## Always run it with reporting off

promptfoo reports how it is used back to its maker unless told not to, and OpenAI agreed to buy that maker in March 2026. Set these four switches at the top of every terminal session or script, and keep the first on every command as well:

```bash
export PROMPTFOO_DISABLE_TELEMETRY=1          # no usage reports
export PROMPTFOO_DISABLE_UPDATE=1             # no check for a newer version
export PROMPTFOO_DISABLE_REMOTE_GENERATION=1  # nothing written on promptfoo's servers
export PROMPTFOO_DISABLE_SHARING=1            # no uploading of results
```

Two things still get out, both seen in tests:

- **One small notice a run.** With reporting off, each run still tells the maker that reporting is off. The notice carries a random number for this install, the version and the kind of Mac. No prompts, cases or answers.
- **The viewer page.** `promptfoo view` shows results in the browser, and that page tries to report to the maker's analytics whatever the switches say. Use the report file instead (below), which calls nothing.

Never sign in (`promptfoo auth login`) and never run `promptfoo share`. Once signed in, promptfoo uploads results by default.

## By hand first

No tool comes before reading. Put the first twenty or so real outputs in a sheet, one a row. Beside each, write one line on what is wrong with it. Group the lines, count the groups, and write down what good means for this design. The public shelf has the case: a letting assistant's team read its conversations, counted the failures, and found requests about dates were right only 33% of the time. One fix took that to 95% (`../research/husain-field-guide-nurtureboss.md`). The craft itself is in `../expertise/how-a-design-is-judged.md`.

Only a check that will be run again earns a place in promptfoo: a failure that was fixed and must not come back, or two versions of a prompt that need comparing.

## What it's best at

- **The same cases every time.** Change the prompt, run again, see which cases flipped.
- **Two versions side by side.** One column each, the same rows.
- **Cheap checks with no model involved.** Does the answer contain the date, is it under 200 characters.

Where something else beats it: finding out what is wrong in the first place is reading by hand. Checking a whole agent inside a sealed box is Inspect, a runner-up on the tool list.

## Setup

- **Installed:** promptfoo 0.125.1, through Homebrew. Free.
- **The command that proves it works,** with no model call. A provider is whatever answers a case, a model or a command, and the `echo` provider just hands the prompt back:

```bash
printf 'prompts: ["Say hello to {{name}}"]\nproviders: [echo]\ntests:\n  - vars: {name: Ada}\n    assert:\n      - {type: contains, value: Ada}\n' > promptfooconfig.yaml && PROMPTFOO_DISABLE_TELEMETRY=1 promptfoo eval
```

It prints a small table and `1 passed (100%)`.

- **What stays on the Mac:** all the results, in a database in `~/.promptfoo/`, with a `cache` folder of saved answers and a `logs` folder beside it. All three hold prompts and answers.

## Running checks on the Claude plan

This Mac has no API key (a pay-per-use password), and promptfoo's built-in link to Claude stops without one. What works is a provider that runs a command: each case goes through `claude -p`, Claude Code with nobody at the keyboard, on the plan. The command is a two-line script, `ask-claude.sh`:

```bash
#!/bin/bash
exec claude -p "$1" --model haiku --safe-mode --tools "" --no-session-persistence
```

`--model haiku` picks the cheap model. `--safe-mode` leaves out Sean's own skills, plugins and hooks, so the check meets a plain Claude. `--tools ""` means a case can make Claude answer and nothing else. Then the config file, `promptfooconfig.yaml`, and the run:

```yaml
description: Dates in a renter's message
prompts:
  - file://prompt-v1.txt
providers:
  - id: 'exec: ./ask-claude.sh'
    label: haiku
tests: file://cases.csv
```

```bash
PROMPTFOO_DISABLE_TELEMETRY=1 promptfoo eval -o report.html
```

Three made-up cases took 12 seconds on one run and 5 on another, four calls at a time, and all passed. Claude Code priced each call at under a tenth of a cent at pay-per-use rates; on the plan a call counts toward the usage limit instead.

Two other ways. A small Python file as the provider also worked, and it can pass Claude Code's cost figure back, which the command can't. promptfoo's built-in Claude Agent SDK provider needs a package that isn't installed, so it is a question for Sean.

## Getting the best out of it

**The config file has four parts.** `prompts` is the wording under test, with `{{message}}` marking a variable. `providers` is what answers. `tests` is the cases, each giving the variables their values. Assertions are the checks made on each answer.

**Keep the cases in a text file beside the design.** One row a case, one column a variable, and a column named `__expected` for the check:

```
message,__expected
Can I tour two weeks from today?,equals:2026-11-30
Is this Friday free for a viewing?,contains:2026-11-20
```

**Pick the cheapest assertion that catches the failure.**

- *Exact and contains checks* (`equals`, `contains`, `icontains`, `regex`, `is-json`) are free and instant. Use them when the right answer has a fixed part.
- *A small script* (`javascript` or `python`) is one line such as `output.length < 200`. Use it when the rule can be worked out.
- *A model grading the answer* (`llm-rubric`) is for what only reading can judge, such as tone. It costs one more model call an answer, and the grader makes mistakes of its own. On the shelf, Shopify's grader agreed with its experts barely better than chance until the team tuned it. So label twenty or thirty answers pass or fail yourself, run the grader over the same answers, and read every disagreement before trusting it. The `echo` provider feeds it answers you already know. Name the grader in the config; left alone, promptfoo reaches for OpenAI and stops for want of a key:

```yaml
defaultTest:
  options:
    provider: 'exec: ./ask-claude.sh'
```

**Compare two versions.** List `prompt-v1.txt` and `prompt-v2.txt` under `prompts`. Each gets a column.

**See how much answers vary.** `--repeat 3 --no-cache` runs each case three times. One pass out of one says little.

**Know the cache.** promptfoo keeps each answer for 14 days and reuses it while the script and the prompt are unchanged, so a second run is instant and free. Add `--no-cache` when something it can't see has changed: the model behind `haiku`, or Claude Code itself.

**Read the report file.** `-o report.html` writes one page with every case, pass or fail, and a search box. It opens with no network. `-o results.csv` goes into a sheet. `-n 5` runs only the first five cases, and `-j 1` runs one call at a time.

## Where it goes wrong

- **A green table that proves nothing.** Checks written before reading the outputs measure what is easy. Klarna's launch numbers were nearly all speed, volume and cost, and quality was what slipped (`../research/klarna-assistant-walk-back.md`).
- **A grader nobody checked.** It passes and fails with confidence either way.
- **A stale cache.** A run that finishes at once and reports cache hits called no model.
- **Cost shows as zero.** Through a command, promptfoo can't see what a call used.
- **A stuck call stalls the run.** The command provider sets no time limit of its own.
- **The cheap model passes and the real one differs.** Run the last check on the model the design names.

## Safety

- **What it spends.** Model calls: cases times prompt versions times repeats, plus one more for every graded answer. Twenty cases, two versions, three repeats and a grader is 240 calls. Count before running, and ask Sean before a big run.
- **What leaves the Mac.** Every prompt and case goes to Anthropic, as in any Claude session, and the maker gets its one notice a run. Nothing private and nothing from the day job goes into a case.
- **Ask Sean first** before opening the viewer, installing anything or using a key.
- **Attack testing is not for use without asking.** `promptfoo redteam` writes several hundred takeover attempts and fires them at a design. By default promptfoo's servers write the attacks, and are sent what the design is for and how it is set up. With no OpenAI key those servers grade as well, so they also get each attack and the design's answer to it. It asks for an email address too.

## More details

- **Versions, November 16, 2026:** promptfoo 0.125.1 at `/opt/homebrew/bin/promptfoo`; Claude Code 2.1.325, where `haiku` answered as `claude-haiku-5-5`.
- **Run on this Mac, in a scratch folder:** the proof command; the three date cases through `claude -p` twice (4 to 12 seconds a call); one graded check with Claude as the grader, which passed a right answer and failed a known wrong one; a Python provider that returned a cost of $0.0002; two prompt versions, a case file, `--repeat` and the cache, with a script that calls no model; `report.html` opened in Chrome with the network blocked. Eleven small model calls in all.
- **What gets out, measured:** a local blocker logged every address promptfoo tried and let nothing through. First switch only: `api.promptfoo.dev` (the update check) and `r.promptfoo.app`. All four switches, and `PROMPTFOO_SELF_HOSTED=1` as well: `r.promptfoo.app`, once a run. The viewer page in Chrome: `a.promptfoo.app`. Pointing promptfoo at a dead proxy (`HTTPS_PROXY=http://127.0.0.1:9`) stopped the notice; the provider must then drop that setting before calling Claude, which the Python provider did.
- **Read in the installed code, not run:** signing in turns on uploading; the sharing switch blocks `share`; the command provider has no time limit.
- **Could not confirm:** what the viewer page sends; whether OpenAI's purchase has closed; the Agent SDK provider with a plan login, which its documents describe; how the plan counts a call.
- **Sources, read November 16, 2026:** `promptfoo --help`, `claude --help`, and these pages under https://www.promptfoo.dev/docs/: `configuration/telemetry/`, `faq/`, `usage/command-line/`, `providers/custom-script/`, `providers/python/`, `providers/echo/`, `providers/claude-agent-sdk/`, `configuration/expected-outputs/` and its `model-graded/` page, `configuration/caching/`, `configuration/outputs/`, and the quickstart, configuration and data-handling pages of the attack-testing section. The purchase: https://www.promptfoo.dev/blog/promptfoo-joining-openai/ (March 9, 2026).
