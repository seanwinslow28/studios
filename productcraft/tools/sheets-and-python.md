# Sheets and Python.

Google Sheets for numbers Sean wants to see and touch; Python, run through uv, for anything a sheet does badly: joining exports, cleaning messy data, doing the statistics properly. Two installed skills help: an A/B test reader and a data check. Read this before putting a number in front of Sean that came from a survey, a waitlist, a test or a model.

## What it's best at.

- **Sheets: the model Sean can poke.** A market size, a pricing guess, a break-even line. Every assumption sits in a cell he can change, and the answer moves. Shareable, free, and already on his Mac.
- **Python: the work a sheet hides.** Merging two exports, removing duplicate signups, counting conversions by day, running a significance test. A short script leaves a record of exactly what was done, which a chain of hand edits in a sheet never does.
- **The skills: a second pair of eyes.** `pm-data-analytics:ab-test-analysis` lays out lift, a confidence range, guard numbers and a ship-or-stop call. `data:validate-data` checks an analysis before anyone sees it: the right denominator, no double counting, parts that add up to the whole, conclusions the data actually supports.

Where another tool beats them: once a product is live and the question is about behaviour inside it, PostHog holds the data (see `posthog.md`). For survey answers, Tally's own results view is quicker for a first look.

## Setup.

- **Sheets:** Sean's Google account; the Google Drive connector can read and create files.
- **uv 0.10.3** is installed (checked November 12, 2026). The newest is 0.13.7, released November 3; updating is Sean's call because other jobs depend on it. Devcraft's `uv.md` covers uv in depth.
- **No data libraries are installed, on purpose.** Each run fetches what it needs into uv's cache and leaves the Mac clean. The command that proves it works:

```bash
uv run --no-project --with pandas python -c "import pandas; print(pandas.__version__)"
```

The first run downloads pandas, so it needs the internet; later runs reuse the cache. Add `--with scipy` for statistical tests and `--with matplotlib` for a quick chart. `--no-project` stops uv looking for a project folder it doesn't need.

## Getting the best out of it.

**Keep the raw data untouched.** The export from Tally, Stripe or PostHog goes in a folder or tab marked raw and is never edited. Every cleaning step happens in a copy or in a script that reads the raw file and writes a new one. When a number looks odd later, you can always go back to what actually came in. A cleaned sheet with no raw original is a number nobody can check.

**One sheet of assumptions.** Every guess the model rests on (price, conversion rate, how many people in the group, how many stay each month) lives on one tab, each with a source or the word "guess" beside it. Formulas elsewhere point at those cells and never hold a typed-in number of their own. Sean can then see in one place what the whole answer depends on, and change one guess to watch the result move. A model that hides a 4% conversion rate inside a formula three tabs deep is how a guess quietly becomes a fact.

**Show ranges, not points.** "Somewhere between $3,000 and $14,000 a year, most likely near $6,000" is honest. "$6,247" claims a precision nobody has. Give the low, likely and high cases side by side, so the reader sees how wide the doubt is.

**Be honest about small samples.** Side-product tests are small, and small samples lie with a straight face:

- **3 of 10 people said they'd pay.** The true share could plausibly be anywhere from about 11% to 60%. With 30 of 100, the range narrows to about 22% to 40%. Say the range, not "30%".
- **Version B converted 9 of 40; version A, 4 of 40.** It looks like more than double. A standard test gives a p-value (the chance of a gap this big if there were no real difference) of about 0.13. The plausible size of the real difference runs from B being 3 points worse to 28 points better. That's "promising, keep going", not "B wins".
- **How big a test needs to be:** to reliably catch a lift from 10% to 15% conversion takes about 690 people per version (the usual 5% false-alarm rate and an 80% chance of catching a real effect). Most side-product tests can't reach that. Then the honest move is a bigger change, a stronger signal like money, or a call made on direction with the doubt stated.

Jason Cohen's "ten people who'll pay" on the shelf is the right instinct for this scale: at ten people, count commitments and talk to each one, rather than compute percentages.

**Check a result before believing it.** The Bing headline test on the shelf is the model. When revenue jumped 12%, the first move was to hunt for a bug, not to celebrate. Before Sean sees a surprising number:

- **Recount it another way.** Total the signups by day and check it matches the overall count.
- **Check the split.** If a test meant to send half the visitors each way sent 60/40, something is broken (people who run tests call this a sample ratio mismatch).
- **Look for duplicates and test entries.** Sean's own test signup, a bot that filled the form twelve times, someone joining twice.
- **Ask what's missing.** People who left before the page loaded never appear in the data.
- **Run `data:validate-data`** on the finished analysis; it catches the common mistakes listed above and says what caveats to state.

**Decide the bar before the data arrives.** Write down "we'd call it a yes at 40 signups from 1,000 visitors" before the test starts. Choosing the bar after seeing the result turns any outcome into a win. The Superhuman example on the shelf set its 40% bar before measuring.

## Where it goes wrong.

- **The A/B skill's sample-size formula is short.** It leaves out the term for the chance of catching a real effect, so it suggests about half the people needed (about 340 instead of 690 in the example above). Use the full calculation, or ask for it with "80% power" stated.
- **Peeking.** Checking a test daily and stopping the moment it looks good finds false winners. Set the size or the end date first and read it once at the end.
- **Many cuts of the same data.** Slice results by enough groups and one will look special by chance. If you looked at ten groups to find one, say so.
- **Averages that mislead.** A few big buyers drag an average far from the typical customer. Report the median (the middle value) beside the average.
- **Typed-over formulas in a sheet.** One hard-typed number in a column of formulas breaks the model silently. Check by turning on formula view (View, Show, Formulas).
- **Spreadsheet size.** Sheets holds up to 20 million cells. A raw event export can get there; that's the point to move to Python.
- **A script with no record.** Save the script beside the result in the job folder, so the number can be rebuilt.

## Examples.

- **Weak:** "The waitlist converted at 4.2%, so the market is there." One number, no source, no range, no bar set beforehand.
- **Strong:** "42 of about 1,000 visitors joined (between roughly 3% and 6% is plausible). We set 3% as the bar before launch, so it passed, just. Six of the 42 were friends who saw Sean's post, so the stranger rate is nearer 3.6%. Raw export and the script that cleaned it are in the job folder."

## Safety.

uv downloads packages from the internet and uploads nothing. Sheets live in Sean's Google account, so anything put there is stored by Google: keep day-job data out of personal sheets and in Sean's private work repo, and keep personal details of signups (emails, names) out of any sheet that gets shared. Ask Sean before sharing a sheet with anyone. Nothing here costs money.

## More details

- uv version checked with `uv --version` on this Mac, November 12, 2026: 0.10.3. Newest release 0.13.7 (November 3, 2026), from PyPI.
- `uv run --with` and `--no-project`: https://docs.astral.sh/uv/guides/scripts/ and `uv run --help`.
- Sheets size limit: https://support.google.com/drive/answer/37603 (20 million cells or 100MB).
- Skills read: `pm-data-analytics/skills/ab-test-analysis/SKILL.md`, `data/skills/validate-data/SKILL.md`, `data/skills/statistical-analysis/SKILL.md`, under `~/.claude/plugins/synced/*/`.
- The worked numbers were computed here: Wilson intervals for 3 of 10 and 30 of 100; a two-proportion z-test for 4 of 40 against 9 of 40 (z about 1.52, p about 0.13, 95% range for the difference about minus 3 to plus 28 points); sample size for 10% to 15% at a 5% significance level and 80% power, about 686 per version, against about 336 from the skill's formula.
- Shelf examples: `productcraft/research/bing-headline-test.md`, `productcraft/research/cohen-ten-who-will-pay.md`, `productcraft/research/superhuman-fit-engine.md`.
