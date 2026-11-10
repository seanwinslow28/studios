# pytest and Hypothesis.

pytest runs Python tests: small functions that call your code and check what comes back. Hypothesis adds property tests, which describe a rule your code must always keep and then try hundreds of generated inputs to break it. Read this before writing or changing tests on a job.

## What they're best at.

- **pytest: short, readable tests.** A test is a plain function with a plain `assert`; when it fails, pytest shows both sides and where they differ. Fixtures (reusable setup that pytest hands to any test that asks for it by name) keep setup out of the way.
- **Hypothesis: the inputs you didn't think of.** Empty strings, odd Unicode, huge numbers, duplicates, lists of one. Example tests check the cases you imagined; property tests check the rule, and find the case you didn't.

Where something else beats them:

- **Shell scripts** are tested with Bats (see the shell scripts guide).
- **Changes to the whole machine,** like a Homebrew upgrade, need a throwaway Mac (see the Tart guide). A unit test can't show that a real upgrade breaks a real venv.
- Python's built-in `unittest` works, but the same test takes more lines.

## Setup.

Both are free and live in each project, not on the whole Mac. uv adds them as development-only dependencies and records the exact versions in `uv.lock`, so the tests run the same next month:

```bash
uv add --dev pytest hypothesis
uv run pytest
```

Always run through `uv run`. It uses the project's own Python and venv (its private Python folder), never whatever `pytest` happens to be first on the path. Current versions on November 10, 2026: pytest 9.2.0 (October 27) and Hypothesis 6.170.15.

Since pytest 9.0, settings go in a plain `[tool.pytest]` table with real TOML values:

```toml
[tool.pytest]
minversion = "9.2"
testpaths = ["tests"]
addopts = ["-ra"]
strict = true
markers = ["slow: takes more than a second; skip with -m 'not slow'"]
```

`strict = true` turns on four checks at once. The one that matters most: a misspelled marker such as `@pytest.mark.slwo` becomes an error instead of a test that silently never gets skipped. `-ra` prints a one-line reason for every skipped or expected-to-fail test at the end of the run. Don't mix this table with the older `[tool.pytest.ini_options]`; pytest refuses both at once.

## Getting the best out of pytest.

**`tmp_path` for anything that touches files.** Each test gets its own fresh, empty folder. Never test against real paths in the home folder.

```python
def test_rotate_keeps_newest_three(tmp_path):
    for day in range(5):
        (tmp_path / f"job-{day}.log").write_text("x")
    rotate_logs(tmp_path, keep=3)
    assert sorted(p.name for p in tmp_path.iterdir()) == ["job-2.log", "job-3.log", "job-4.log"]
```

**`monkeypatch` for the environment.** It changes something for one test and undoes it afterwards, even if the test fails. The case that matters for scheduled jobs is a missing variable, because launchd (macOS's scheduler) starts jobs with almost none:

```python
def test_fails_clearly_without_home(monkeypatch):
    monkeypatch.delenv("HOME", raising=False)
    with pytest.raises(SystemExit, match="HOME is not set"):
        main([])
```

`monkeypatch.setenv`, `delenv` and `setattr` cover most needs.

**The clock: pass it in.** Code that calls `datetime.now()` deep inside is hard to test at midnight, on the first of the month, or across a clock change. Better design: take `now` as an argument with a sensible default, and the test simply passes a fixed time. When you can't change the code, `monkeypatch.setattr` on the module's own reference (`monkeypatch.setattr(jobs, "now", lambda: FIXED)`) works, but treat the need as a hint that the code wants that argument.

**`parametrize` for a table of cases.** One test, many rows, each reported on its own:

```python
@pytest.mark.parametrize("raw, expected", [
    ("3.12.11", (3, 12, 11)),
    ("3.14.0", (3, 14, 0)),
], ids=["patch", "first-release"])
def test_parse_version(raw, expected):
    assert parse_version(raw) == expected
```

Since 9.2, `ids`, `indirect` and `scope` must be passed by name, as here.

**Fixtures: small, close, and cleaned up.** A fixture that `yield`s gives the test its value and runs the code after `yield` as cleanup. Keep fixtures in the test file until two files need one, then move it to `conftest.py`, pytest's shared-fixture file.

**Markers for slow tests.** Mark them `@pytest.mark.slow` and run the fast set while working: `uv run pytest -m "not slow"`. Run everything before calling it done.

**Flags worth knowing.** `-x` stops at the first failure, `--lf` reruns only the tests that failed last time, `-k parse` runs tests whose names match.

**Test the script through its front door.** Give the script a `main(argv)` function and call it from the test with the `capsys` fixture to read what it printed. One slow end-to-end test that actually runs the script with `subprocess` is worth keeping; fifty are not.

## Getting the best out of Hypothesis.

**Find a rule, not an answer.** Good properties for small tools:

- **Round trip:** `parse(format(x)) == x`.
- **Always true:** the output is sorted, never longer than the input, never outside a range.
- **Matches a slow, obvious version:** the fast function and a plainly correct but slow one always agree.
- **Never crashes** on any input of the right shape.

Here is the rule at the heart of uv's patch-upgrade design on the shelf, written as a property: moving to a newer copy of Python never leaves the minor version.

```python
from hypothesis import example, given, strategies as st

versions = st.tuples(st.just(3), st.integers(0, 20), st.integers(0, 50))

@given(current=versions, available=st.lists(versions))
@example(current=(3, 12, 10), available=[(3, 13, 0)])
def test_upgrade_stays_within_minor(current, available):
    chosen = pick_upgrade(current, available)
    assert chosen[:2] == current[:2]
    assert chosen >= current
```

Hypothesis will try an empty list, a list holding only older versions, a list of one big jump; an example-based test would likely check only the happy path. `@example` pins a case that must run every time, before the generated ones.

**Shrinking.** When Hypothesis finds a failure, it doesn't hand you the messy input it found. It keeps simplifying until it has the smallest input that still fails, and prints it as a "Falsifying example". That small case is usually the bug report, already written.

**The example database.** Failures are saved under `.hypothesis/` in the project and replayed first on the next run, so a bug can't slip away by luck. Add `.hypothesis/` to `.gitignore`. When the `CI` environment variable is set, Hypothesis switches itself to a `ci` profile: no saved database, no deadline, and a fixed random sequence so runs repeat exactly.

**Deadlines.** Each generated example must finish within 200 milliseconds by default, or the test fails with a deadline error. On a busy Mac Mini that can fire at random. The fix is to find what's slow; if the work is slow by nature, set `@settings(deadline=None)` on that one test with a comment saying why.

**Settings and profiles.** Each test runs 100 examples by default. Register a heavier profile for an overnight run in `conftest.py` with `settings.register_profile("thorough", max_examples=2000)` and choose it with `uv run pytest --hypothesis-profile=thorough`. To replay one exact run, use `--hypothesis-seed`. To see what was generated, `--hypothesis-show-statistics`.

**Build valid data; don't filter for it.** If most generated inputs are thrown away by `assume()` or `.filter()`, Hypothesis warns that it's struggling. Build the shape you need directly from smaller strategies instead.

## Where it goes wrong.

- **Fixture tangles.** Fixtures that use fixtures that use fixtures, a session-wide fixture that one test quietly changes, or `autouse` fixtures that run for every test without being named. A reader can no longer see what a test starts with. Keep setup visible, and prefer a small helper function called in the test.
- **Over-mocking.** Replacing your own functions with fakes and then checking that they "were called" tests the wiring, not the result, and breaks on every harmless rewrite. Fake only what's truly outside: the network, the clock, a `brew` or `launchctl` call. Check outcomes: the file written, the value returned, the exact command sent out. This is the central argument of *Unit Testing: Principles, Practices and Patterns*.
- **Slow, flaky tests.** Real network calls, `time.sleep`, the real clock, tests that pass only in a certain order. A flaky test teaches everyone to rerun until green, which hides real failures. Fix the cause or delete the test.
- **Expected values computed the code's way.** If the test works out the expected answer with the same formula as the code, it checks nothing. Write expected values as plain literals.
- **Properties that restate the code.** A property that re-implements the function in the test passes whenever both share the same bug. Look for a rule that's simpler than the code.
- **The wrong pytest.** A bare `pytest` may run a different Python than the project's. Use `uv run pytest`.

## Safety.

Both run entirely on the Mac and upload nothing. Tests must never touch real files, real scheduled jobs or real network services: `tmp_path`, `monkeypatch` and fakes keep every test inside its own sandbox.

## More details

- pytest docs: https://docs.pytest.org/en/stable/ (configuration, fixtures, monkeypatch, parametrize, markers). Changelog for 9.0 to 9.2: https://docs.pytest.org/en/stable/changelog.html
- Hypothesis docs: https://hypothesis.readthedocs.io/en/latest/ (API reference for settings and profiles; pytest options under integrations). Releases: https://github.com/HypothesisWorks/hypothesis/releases
- uv development dependencies: https://docs.astral.sh/uv/
