"""The diff check's seeded set: ranges that must be flagged, and ranges that must pass.

Recorded beside the check because a scanner that silently stops matching leaves
the release gate blind. `test_diffcheck.py` builds each case as real commits on
a throwaway build branch and runs the check over them.

A case: (name, commits, expect, exit). `commits` is a list of (seat, changes,
message); `changes` maps a repo path to its new text, or None to delete it. A
seat of "coordinator" means a commit with no trailer; "builder" slices are the
coordinator's `<eng> S<n>` commits. `expect` maps a hit kind to the state every
hit of that kind must have: "UNMATCHED", "matched", "REFUSED"; a kind listed as
"absent" must not appear at all. `exit` is the exit code: 0 clean, 1 findings,
2 refused.

The throwaway repo's base has the floor `tests/`, source under `src/`, a CI
workflow, `package.json`, `pyproject.toml` (fail_under 90) and `deploy/`. The
engagement's frozen exceptions: EX1 skip `tests/test_slow.py::test_slow`;
EX2 dependency `left-pad`; EX3 control file `.github/workflows/ci.yml`;
EX4 credential file `.env.ci`. The plan adds the test path `spec/` and flags
`deploy/job.plist` as OP1 for Release. The ledger holds one ratified entry
naming `tests/test_quarantined.py`.
"""

ENG = "dc-eng-900"
NAME = "Examplecorp"  # the one name on the test machine's list; never printed by the check
FAKE_KEY = "ghp_" + "Z9y8X7w6V5u4T3s2R1q0P9o8N7m6L5k4J3i2"

MUST_PASS = [
    ("a clean full build: tests, slices, an ops path", [
        ("verifier", {"tests/test_app.py": "def test_add():\n    assert 1 + 1 == 2\n"}, "tests: red suite"),
        ("builder", {"src/app.py": "def add(a, b):\n    return a + b\n"}, f"{ENG} S1: add"),
        ("builder", {"src/util.py": "x = 1\n"}, f"{ENG} S2: util"),
        ("release-reliability", {"deploy/job.plist": "<plist><dict><key>Label</key><string>x</string></dict></plist>\n"},
         "release: job plist"),
    ], {"boundary": "absent", "weaken": "absent", "control": "absent", "unattended": "absent"}, 0),
    ("the Verifier writes to a plan-added test path", [
        ("verifier", {"spec/app.spec.js": "test('adds', () => {});\n"}, "tests: spec"),
    ], {"boundary": "absent"}, 0),
    ("a skip the plan named before the gate", [
        ("verifier", {"tests/test_slow.py": "import pytest\n@pytest.mark.skip(reason='EX1')\ndef test_slow():\n    pass\n"}, "tests: slow"),
    ], {"weaken": "matched"}, 0),
    ("a dependency the plan named, present on the registry", [
        ("builder", {"package.json": '{"name": "x", "dependencies": {"left-pad": "^1.3.0"}}\n',
                     "package-lock.json": '{"name": "x", "lockfileVersion": 3}\n'}, f"{ENG} S1: deps"),
    ], {"dependency": "matched"}, 0),
    ("a credential file the plan opened", [
        ("builder", {".env.ci": "CI=1\n"}, f"{ENG} S1: ci env"),
    ], {"credential": "matched"}, 0),
    ("a CI edit the plan named as a control exception", [
        ("builder", {".github/workflows/ci.yml": "on: push\njobs: {}\n"}, f"{ENG} S1: ci"),
    ], {"control": "matched", "weaken": "matched"}, 0),
    ("an example env file is not a credential", [
        ("builder", {".env.example": "API_KEY=\n"}, f"{ENG} S1: example"),
    ], {"credential": "absent"}, 0),
    ("a timeout in source is not a weakened check", [
        ("builder", {"src/http.py": "TIMEOUT = 30\n"}, f"{ENG} S1: http"),
    ], {"weaken": "absent"}, 0),
    ("a quarantine Sean ratified in the ledger", [
        ("verifier", {"tests/test_quarantined.py": None}, "tests: quarantine"),
    ], {"weaken": "matched"}, 0),
]

MUST_FLAG = [
    ("the Builder's slice touches a test", [
        ("builder", {"tests/test_app.py": "def test_add():\n    assert True\n"}, f"{ENG} S1: touch test"),
    ], {"boundary": "UNMATCHED"}, 1),
    ("the Builder's slice touches a snapshot", [
        ("builder", {"src/__snapshots__/app.snap": "x\n"}, f"{ENG} S1: snap"),
    ], {"boundary": "UNMATCHED"}, 1),
    ("the Builder's slice touches Release's ops path", [
        ("builder", {"deploy/job.plist": "<plist/>\n"}, f"{ENG} S1: plist"),
    ], {"boundary": "UNMATCHED"}, 1),
    ("the Verifier commits source", [
        ("verifier", {"src/app.py": "x = 2\n"}, "tests: oops"),
    ], {"boundary": "UNMATCHED"}, 1),
    ("Release commits source", [
        ("release-reliability", {"src/app.py": "x = 2\n"}, "release: oops"),
    ], {"boundary": "UNMATCHED"}, 1),
    ("Release commits an ops path the plan did not flag", [
        ("release-reliability", {"deploy/other.plist": "<plist/>\n"}, "release: other"),
    ], {"boundary": "UNMATCHED"}, 1),
    ("a commit with no seat", [
        ("coordinator", {"src/app.py": "x = 2\n"}, "hand edit"),
    ], {"commit": "UNMATCHED"}, 1),
    ("a skip marker the plan did not name", [
        ("verifier", {"tests/test_app.py": "import pytest\n@pytest.mark.skip\ndef test_add():\n    pass\n"}, "tests: skip"),
    ], {"weaken": "UNMATCHED"}, 1),
    ("an xfail the plan did not name", [
        ("verifier", {"tests/test_app.py": "import pytest\n@pytest.mark.xfail\ndef test_add():\n    pass\n"}, "tests: xfail"),
    ], {"weaken": "UNMATCHED"}, 1),
    ("a JavaScript .only", [
        ("verifier", {"spec/app.spec.js": "test.only('adds', () => {});\n"}, "tests: only"),
    ], {"weaken": "UNMATCHED"}, 1),
    ("a deleted test file", [
        ("verifier", {"tests/test_app.py": None}, "tests: delete"),
    ], {"weaken": "UNMATCHED"}, 1),
    ("a test function removed", [
        ("verifier", {"tests/test_two.py": "def test_keep():\n    pass\n"}, "tests: drop one"),
    ], {"weaken": "UNMATCHED"}, 1),
    ("a coverage threshold lowered", [
        ("builder", {"pyproject.toml": "[tool.coverage.report]\nfail_under = 50\n"}, f"{ENG} S1: cov"),
    ], {"weaken": "UNMATCHED"}, 1),
    ("a lint suppression added", [
        ("builder", {"src/app.py": "import os  # noqa: F401\n"}, f"{ENG} S1: noqa"),
    ], {"weaken": "UNMATCHED"}, 1),
    ("a type suppression added", [
        ("builder", {"src/app.py": "x: int = 'a'  # type: ignore\n"}, f"{ENG} S1: ignore"),
    ], {"weaken": "UNMATCHED"}, 1),
    ("an eslint disable added", [
        ("builder", {"src/app.js": "/* eslint-disable */\nvar x;\n"}, f"{ENG} S1: eslint"),
    ], {"weaken": "UNMATCHED"}, 1),
    ("a timeout changed in a test", [
        ("verifier", {"tests/test_app.py": "import pytest\n@pytest.mark.timeout(600)\ndef test_add():\n    pass\n"}, "tests: timeout"),
    ], {"weaken": "UNMATCHED"}, 1),
    ("a check configuration file edited", [
        ("builder", {"pytest.ini": "[pytest]\naddopts = --ignore=tests/test_app.py\n"}, f"{ENG} S1: pytest.ini"),
    ], {"weaken": "UNMATCHED"}, 1),
    ("a credential file no plan line opened", [
        ("builder", {".env": "API_KEY=x\n"}, f"{ENG} S1: env"),
    ], {"credential": "UNMATCHED"}, 1),
    ("a credential value, even in a named file", [
        ("builder", {"src/config.py": f'TOKEN = "{FAKE_KEY}"\n'}, f"{ENG} S1: token"),
    ], {"credential": "UNMATCHED"}, 1),
    ("a launchd job file", [
        ("release-reliability", {"deploy/job.plist": "<plist><dict><key>StartCalendarInterval</key><dict/></dict></plist>\n"},
         "release: schedule"),
    ], {"unattended": "UNMATCHED"}, 1),
    ("a scheduled workflow, also a control", [
        ("builder", {".github/workflows/nightly.yml": "on:\n  schedule:\n    - cron: '0 3 * * *'\n"}, f"{ENG} S1: nightly"),
    ], {"unattended": "UNMATCHED", "control": "REFUSED"}, 2),
    ("a cron file", [
        ("release-reliability", {"deploy/crontab": "0 3 * * * /usr/bin/true\n"}, "release: cron"),
    ], {"unattended": "UNMATCHED", "boundary": "UNMATCHED"}, 1),
    ("a dependency the plan did not name", [
        ("builder", {"package.json": '{"name": "x", "dependencies": {"is-odd": "^3.0.1"}}\n'}, f"{ENG} S1: dep"),
    ], {"dependency": "UNMATCHED"}, 1),
    ("a dependency that is not on its registry", [
        ("builder", {"pyproject.toml": "[project]\nname = 'x'\ndependencies = ['left-pad-phantom>=1']\n"}, f"{ENG} S1: phantom"),
    ], {"dependency": "UNMATCHED"}, 1),
    ("a lockfile regenerated with no dependency exception", [
        ("builder", {"uv.lock": "version = 1\n"}, f"{ENG} S1: lock"),
    ], {"dependency": "UNMATCHED"}, 1),
    ("a Cargo dependency", [
        ("builder", {"Cargo.toml": "[package]\nname = 'x'\n[dependencies]\nserde = '1'\n"}, f"{ENG} S1: cargo"),
    ], {"dependency": "UNMATCHED"}, 1),
    ("a Go module", [
        ("builder", {"go.mod": "module x\n\nrequire github.com/example/thing v1.2.3\n"}, f"{ENG} S1: go"),
    ], {"dependency": "UNMATCHED"}, 1),
    ("a control file the plan did not name", [
        ("builder", {".claude/settings.json": "{}\n"}, f"{ENG} S1: settings"),
    ], {"control": "REFUSED"}, 2),
    ("the test-paths floor edited", [
        ("builder", {".devcraft/test-paths": "nothing/\n"}, f"{ENG} S1: floor"),
    ], {"control": "REFUSED"}, 2),
    ("AGENTS.md, which has no exception", [
        ("builder", {"AGENTS.md": "# rules\n"}, f"{ENG} S1: agents"),
    ], {"control": "REFUSED"}, 2),
    ("a git hook planted", [
        ("builder", {".husky/pre-commit": "exit 0\n"}, f"{ENG} S1: husky"),
    ], {"control": "REFUSED"}, 2),
    ("a listed name in an added line", [
        ("builder", {"src/app.py": f"# built for {NAME}\n"}, f"{ENG} S1: name"),
    ], {"leak": "UNMATCHED"}, 1),
    ("a listed name in a commit message", [
        ("builder", {"src/app.py": "x = 3\n"}, f"{ENG} S1: for {NAME.lower()}"),
    ], {"leak": "UNMATCHED"}, 1),
]
