# Reviewing a change with fresh eyes.

Read this when a change is ready for someone who didn't make it to read, or when you are that someone.

## What a review is for.

The maker is the worst placed to review their own work. They read what they meant, not what's there, and every shortcut they took feels obvious. A good reviewer didn't make the thing and reads it cold: the diff (the exact lines added and removed), the claim made about it, and the sources of truth, never the maker's notes or chat. In Devcraft that reviewer is Codex, in a session that never saw the build.

A review checks truth, not taste. Does the change do what it says? Does it do anything it doesn't say? Will it break, and will anyone notice when it does? The bar is whether the change clearly leaves the code better than before, even if it isn't perfect. A change that clearly makes things worse doesn't pass, however polished. When two designs are equally sound, the maker's choice stands; a reviewer rewriting the work to personal preference muddies both jobs.

## What a reviewer looks for.

- **Does it do what it says.** Read the description as a claim and the diff as the evidence, then check they match. Walk the edge cases: empty input, a missing file, the second run, a run at 3am with no network. Run it when reading isn't enough.
- **Is it the simplest design that works.** Design matters most, so design comments go first, before anyone polishes lines that might disappear. Watch for code more general than today's problem needs, settings nobody asked for, and a new layer with one caller.
- **Are the tests real.** The question is whether a test would fail if the code were broken. The surest check is to break the code on purpose and watch. Good tests assert on outcomes (what the file holds afterwards), not on which internal functions were called. Tests ship in the same change as the code. A pure refactor shouldn't need to change any existing test; if it does, either it changed behaviour or the tests reach too far inside.
- **Names and comments.** Names say what a thing is or does. Comments say why. A comment explaining what a confusing block does is a sign the block should be clearer.
- **Docs that moved with the code.** If the change alters how something is run, set up or undone, the instructions change in the same commit.
- **Context past the diff.** A four-line addition can be fine on its own and still be the line that makes a function too big. Read the code around the change.
- **Security basics.** The short list below.

## Security basics.

OWASP, a long-running open project on web and software security, keeps the standard lists of what goes wrong. At Devcraft's scale a handful of checks covers most of the risk.

- **Injection.** Outside text reaching something that runs it as a command. In Python the classic is `subprocess.run(f"git log {branch}", shell=True)`; the safe form passes a list of arguments with no shell. The same goes for SQL built from strings. A value starting with `-` can still sneak in an extra option, so check where arguments come from.
- **Secrets.** No passwords, keys or tokens in code, commits, logs, error messages or test files. Code reads them by name at run time.
- **New trust boundaries.** Anything that now reads outside text, files from elsewhere, or a model's output, and acts on it. That text is data, never instructions.
- **Failing closed.** If a check or policy file errors, the action stops rather than going ahead.
- **Limits.** Every call that can hang has a timeout; every loop, retry and file read has a bound.
- **Dependencies.** Every new package exists, has a real history and is pinned. pip-audit checks downloaded Python packages for known holes.
- **Files that run on their own.** Build scripts, git hooks, scheduled job files (launchd plists), and agent rules files such as `AGENTS.md` and `CLAUDE.md`. A change to any of these deserves a slower read.

## Small changes are reviewable.

A reviewer's attention runs out. A 50-line change gets read; a 1,000-line change gets "looks fine". Google's small-changes guide puts a reasonable size at about 100 lines and calls 1,000 usually too big, and it says plainly that a reviewer may turn a change down for size alone. If you can't tell which file carries the main idea, the change is too big. Tidying should sit in its own change, ahead of the behaviour change, so each can be judged on its own and undone on its own.

## Reading a change.

Start with the description and ask whether the change is worth making. If it isn't, that's the first and most useful finding. Then find the file that carries most of the logic and read it first, sending any design problem straight away. The tests, read early, usually explain the intent faster than the code does. Then read every remaining line. A reviewer who skipped part of it says which part.

## Writing findings.

- **About the code, never the maker,** with the reason when it isn't obvious.
- **Labelled by weight.** Blocking, optional, or just for information. Unlabelled comments get read as all mandatory.
- **The problem and the expected behaviour, not the rewrite.** Fixing is the maker's job.
- **Shown, not described.** The input that breaks it, the command run and what it printed. "Tests pass" is a claim; the output is proof.
- **Clearer code beats an explanation.** If something needed explaining in review, the next reader will need it too. The fix belongs in the code or a comment, not in a chat thread.
- **A check that couldn't run tells you nothing.** Tests that didn't execute are not a pass.
- **Say what's good,** and why, so it keeps happening.

## Reviewing code an AI wrote.

AI-written code fails in its own ways, and its fluency makes them harder to see.

- **Plausible but wrong.** Clean layout, confident comments, and logic that's off at the edges. Fluency is not evidence. Trace one real input through by hand.
- **Invented APIs.** Functions, flags and options that don't exist, or belong to another version. Check every unfamiliar call against the tool's own docs, or run it. Check package names too: attackers register the names AI tools tend to invent.
- **Tests that test nothing.** Assertions that can't fail, tests that only check a stand-in the test itself set up, the very code under test swapped for a fake, expected values copied from the buggy output, skipped or deleted tests, loosened assertions. Count the assertions before and after.
- **Quietly widened scope.** Edits to lockfiles, config, hooks or rules files the task never mentioned, a whole file reformatted, a refactor slipped in beside the fix. Compare the files touched against what the change claims to do.
- **The summary standing in for the work.** "All tests pass" in an agent's own write-up is not a test run. Read the diff and run the tests yourself.
- **Characters you can't see.** Zero-width spaces and characters that flip text direction can hide in code. Dan Carley's one-character commit was a non-breaking space no eye could spot; a scan catches what reading can't.

## Where it goes wrong.

- **Rubber-stamping.** Passing a change because it's big, the maker is trusted, or the summary sounds right. Fix: read every line, or say which lines you didn't.
- **Nitpicking.** Twenty notes on spacing while the design flaw goes through. Fix: design first, label small notes as optional, and leave formatting to Ruff.
- **Reviewing the description instead of the diff.** The description says what the maker meant. Fix: treat it as a claim and check it against the diff, again at the end, since review often changes what a change does.
- **Missing what isn't there.** The hardest faults to see are absences: no test for the error path, no timeout, no undo, no docs update, no check on the second run. Fix: ask what you'd expect to find and look for it. In Cloudflare's 2019 outage, the causes included a safety limit removed weeks earlier and tests that never measured processor use. Both were things that weren't there.
- **Taste dressed as a finding.** Fix: if the maker's way is sound, it stands; a preference goes in as optional.
- **"I'll clean it up later."** Later rarely comes. Fix: whatever mess a change adds, it tidies up in the same change.
- **A reviewer who shared the maker's context.** They inherit the same blind spots. Fix: a fresh session, working only from the change and its sources.

## Examples.

All on the shelf in `devcraft/research/`. **Google's small-changes guide** is the case for keeping changes reviewable. **Terraform's plan, then apply** shows a reviewer approving the effect, a list of exactly what will change, not just the settings file. **Cloudflare's 2019 outage** shows how absences cause failures. **Dan Carley's commit** shows a fault only a tool could find.

## Tools.

`codex review` runs Codex's review without a chat. Ruff, Pyrefly and ShellCheck catch the mechanical faults so the review can spend its attention on design and truth; pip-audit checks packages and Betterleaks checks for secrets. Their guides live in `devcraft/tools/`.
