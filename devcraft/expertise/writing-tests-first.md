# Writing tests first.

Read this before writing code that matters, or when a test fails for no clear reason. Writing the test first means stating what the code must do, in a form a machine can check, before the code exists.

## What a good test protects against.

A test earns its place on four counts at once, as Unit Testing: Principles, Practices and Patterns frames them:

- **Catching regressions.** It runs real code, enough of it and the parts that matter, so a break turns it red.
- **Surviving refactoring.** It stays green when the code is rewritten to do the same thing another way. A test that goes red with no real bug is a false alarm, and false alarms teach people to ignore red.
- **Fast feedback.** Seconds, so it runs after every change.
- **Easy to maintain.** Short, readable, little to set up.

The four don't average out: a test that fails badly on any one of them is worth nothing, however good it is on the rest. Never give up on surviving refactoring; trade speed against breadth instead.

Coverage, the share of lines the tests run, is a warning light, not a goal. Low means untested code. High proves only that lines ran, not that anything was checked.

## Test behaviour, not implementation.

Test what the code promises: a value returned, a file written, an exit code, a message sent. Don't test how it gets there.

- **Name tests after behaviour:** "upgrade keeps the old Python while a project uses it", not "test_upgrade". The names together should read as a list of promises.
- **One behaviour per test.** If the name needs "and", split it.
- **Expected values as plain literals,** worked out by hand. A test that computes the answer the same way the code does checks nothing.
- **No branches or loops in a test.** Nothing checks a test, so it has to be obviously correct at a glance.
- **Cause next to effect.** The setup a result depends on sits beside the check on it, even if that repeats.
- **Check the result, not the calls.** A test that asserts "A was called, then B" breaks on every rewrite and catches no bugs. Testing on the Toilet calls these change-detector tests.

Software Engineering at Google offers a test of tests. A pure tidy-up changes no test, a feature adds tests, a bug fix adds the missing case, and only a deliberate change in behaviour edits old checks. A tidy-up that forces edits to old tests means the tests are watching the wrong thing.

## Seams and test doubles.

A seam is a place where a test can swap in a stand-in for something the code depends on. The stand-in is a test double, and three kinds matter. A fake is a small working version, like a temporary folder. A stub hands back canned answers. A mock records how it was called, so the test can check.

Prefer the real thing, then a fake, and use mocks sparingly.

- **Use the real thing** when it's fast and predictable. A real temporary folder, such as pytest's `tmp_path`, beats a mocked file system nearly every time, and catches real path and permission bugs.
- **Fake what's slow, costly or unpredictable:** the network, a paid service, the clock.
- **Mock only at the outer edge,** where the code does something others can see, like sending a message or running a command that changes the system. Check exactly what was sent, and that nothing else was. Never mock the logic under test, and never check calls that only read.
- **Don't mock what you don't own.** Wrap an outside library or command in a thin piece of your own and fake that. A mock of someone else's tool freezes your guess about it, and stays green when the real tool changes.

Plan seams before writing code; adding them later often means a rewrite. Two shapes help most. First, keep decisions apart from actions. A pure core takes facts in and returns what should happen ("move this pointer, leave that folder") without touching files. A thin shell gathers the facts and carries out the decision. The core gets fast, thorough tests with no doubles; the shell gets a few real ones. Second, pass in the time, so a test can set "now" to midnight or a month's end.

## Red, green, refactor.

Write one small failing test. Write just enough code to pass it. Tidy up, with the test as a safety net. Repeat.

The red step matters most. Watch the test fail, and fail for the right reason: a check showing the wrong value, not an import error or a typo. A test never seen failing may never fail. For a bug fix, the first test reproduces the bug, and goes red on today's code before any fix is written.

A failure should explain itself without a rerun: expected, actual, and the inputs. Pick values that can't pass by accident: not zero or empty, and a different value per input, so swapped arguments show.

## Scheduled jobs and shell scripts.

A scheduled job speaks only through its exit code and what it writes. Test those.

- **Split the job from its schedule.** The job is a program you can run by hand against a test folder and a test clock. The launchd file is settings. launchd is the macOS scheduler; its job files are property lists, or plists. Check one with `plutil -lint` for syntax, and with a test that reads it and confirms the program it names exists, outside any folder Homebrew can delete.
- **Run it twice.** Run the job, run it again, and check that the second run changes nothing and exits 0.
- **Test the bad nights:** a missing file, a folder it can't write to, a run cut off halfway, Python missing from where it should be. Each should fail loudly, with a nonzero exit code and a clear message, and leave nothing half-written.
- **Test in launchd's bare surroundings.** A launchd job gets a short search path and none of your terminal's setup, so a job that passes in the terminal can fail at 3 a.m. Running the test with an emptied environment (`env -i`) catches it.

For shell scripts, Bats is the test runner: each test runs the script through `run`, then checks `$status` and `$output`. ShellCheck catches whole kinds of shell bug, like unquoted variables, before any test runs.

## Property-based tests.

An example test checks one input you thought of. A property-based test states a rule that must hold for every input, then tries hundreds of generated ones, including odd ones nobody writes by hand: empty text, very long paths, unusual characters. Hypothesis does this for Python. When it finds a failure, it shrinks it to the smallest input that still fails, so the report is readable.

Good rules for small software: reading back what you wrote gives the same thing; running twice matches running once; comparing two version numbers agrees with semantic versioning's ordering. Use them where inputs vary widely, such as parsing, paths and versions, beside a few plain examples.

## Flaky tests.

A flaky test passes and fails on the same code. It's worse than no test, because it teaches everyone to ignore red. Treat it as a bug and find the cause. Never rerun until green.

The usual causes:

- **The clock.** "Now" is a hidden random input. Pass it in.
- **Shared state.** Two tests using the same file, or a test assuming a folder starts empty. Give each test its own temporary folder.
- **Sleeping to wait.** A sleep is a guess about timing. Wait for the real event, checking often, with a generous time limit.
- **Order.** A test that passes only after another one. Each test sets up everything it needs.

## Testing on a throwaway machine.

Some changes touch the system itself: installing Python, loading a launchd job, changing Homebrew. Testing those on the real Mac risks the very thing being protected. Use a throwaway copy of macOS instead. Tart runs one in a window: copy a clean image, install the change, run it, run the undo, check both, then delete the copy. A second user account isn't enough, because it shares Homebrew with the main one.

Running the undo there, and checking the machine ends where it started, is the only proof the way back works.

## Where it goes wrong.

- **Tests written after the code, to match it.** Fix: write each test from the promise, first.
- **Mocking everything.** Fix: real first, fake second, mock only the outer edge.
- **A test that goes red on every rewrite.** Fix: check the outcome, not the steps.
- **A test never seen red.** Fix: break the code on purpose and watch it fail.
- **Rerunning a flaky test until it passes.** Fix: find the cause.
- **Testing only the good night.** Fix: missing files, second runs, bare surroundings.
- **Testing system changes on the real Mac.** Fix: a throwaway copy, undo included.

## Examples.

- **entr** (`devcraft/research/entr-run-on-change.md`): 54 test cases with plain names that read as the tool's promises, and a manual that names every exit code.
- **Simon Willison's sqlite-utils change** (`devcraft/research/simon-willison-perfect-commit.md`): 10 lines of code, 57 lines of tests, one change.
- **Cloudflare's 2019 outage** (`devcraft/research/cloudflare-2019-outage-rollback.md`): the tests passed six minutes after the change was merged, but none measured processor use. Tests only catch what they check.

## Tools.

pytest and Hypothesis for Python, Bats and ShellCheck for shell, `plutil` for launchd files, and Tart for the throwaway Mac. Versions are in `devcraft/tools/choices.md`.
