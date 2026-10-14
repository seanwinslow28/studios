"""The diff check's seeded set, run as real commits in a throwaway repo.

Each case in `seeded.py` is built as commits on a fresh build branch off one
base, with an engagement folder that holds a frozen plan gate, the plan it
read, and one ratified ledger entry. Registry lookups read a fixture file, so
the set runs offline and the same every time; the secret scan runs the real
gitleaks at its full path.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
CHECK = HERE.parent / "diffcheck.py"
HOOKS = HERE.parents[1] / "hooks"
sys.path.insert(0, str(HERE))
import seeded as cases  # noqa: E402

BASE_FILES = {
    ".devcraft/test-paths": "tests/\n",
    "AGENTS.md": "# agents\n",
    "src/app.py": "x = 1\n",
    "tests/test_app.py": "def test_add():\n    assert 2 == 2\n",
    "tests/test_two.py": "def test_keep():\n    pass\n\n\ndef test_drop():\n    pass\n",
    "tests/test_quarantined.py": "def test_q():\n    pass\n",
    ".github/workflows/ci.yml": "on: push\njobs:\n  t:\n    runs-on: ubuntu-latest\n",
    "package.json": '{"name": "x", "dependencies": {}}\n',
    "pyproject.toml": "[project]\nname = 'x'\ndependencies = []\n\n[tool.coverage.report]\nfail_under = 90\n",
    "deploy/README.md": "ops\n",
}

PLAN = """---
id: dc-eng-900.plan
engagement: dc-eng-900-toy
seat: build-planner
---

## Interfaces and data changes

| Change | Fixed by | Note |
|---|---|---|

**Ops paths flagged for Release.**

| Id | Path | What it is | Why it changes |
|---|---|---|---|
| OP1 | `deploy/job.plist` | launchd job | new job |

## Test seams

**Test paths added:** `spec/` because the JavaScript suite lives there.

## Exceptions

| Id | Kind | Exactly what | Why | For which seat |
|---|---|---|---|---|
| EX1 | skip | `tests/test_slow.py::test_slow` | needs the network | verifier |
| EX2 | dependency | `left-pad==1.3.0`, on npm since 2014, maintainers x | padding | builder |
| EX3 | control file | `.github/workflows/ci.yml` | add the suite | builder |
| EX4 | credential file | `.env.ci` | CI reads it | builder |
"""

GATE = """---
id: dc-eng-900.plan-gate
seat: plan-gate
gate: PLAN
anchor: dc-eng-900.plan
anchor_sha256: {sha}
verdict: PLAN PASS — QUALITY VERDICT ONLY
---

## Exceptions on the record (plan gate only)

| Id | Kind | Exactly what | For which seat |
|---|---|---|---|
| EX1 | skip | `tests/test_slow.py::test_slow` | verifier |
| EX2 | dependency | `left-pad==1.3.0`, on npm since 2014, maintainers x | builder |
| EX3 | control file | `.github/workflows/ci.yml` | builder |
| EX4 | credential file | `.env.ci` | builder |
"""

YES = """---
id: dc-eng-900.d02
engagement: dc-eng-900-toy
date: 2026-10-12
seat: coordinator
status: decided
ratified: 2026-10-12
---

## Decision

Quarantine `tests/test_quarantined.py` until the fixture is rebuilt; restore ticket filed.
"""

REGISTRY = {"npm:left-pad": {"exists": "yes", "first_release": "2014-03-20", "age_days": "4000", "maintainers": "x"}}


def sh(*args, cwd, env=None, check=True, inp=None):
    r = subprocess.run(list(args), cwd=cwd, env=env, capture_output=True, text=True, input=inp)
    if check and r.returncode != 0:
        raise AssertionError(r.stdout + r.stderr)
    return r


@pytest.fixture()
def world(tmp_path):
    root = Path(os.path.realpath(tmp_path))
    local = root / "local"
    local.mkdir()
    (local / "employer-paths").write_text(str(root / "emp") + "\n")
    (local / "names").write_text(cases.NAME + "\n")
    fixture = root / "registry.json"
    fixture.write_text(json.dumps(REGISTRY))
    env = dict(os.environ, DEVCRAFT_LOCAL=str(local), DIFFCHECK_REGISTRY_FIXTURE=str(fixture),
               GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
    env.pop("DEVCRAFT_CONTEXT", None)
    main = root / "main"
    main.mkdir()
    sh("git", "init", "-q", "-b", "main", cwd=main)
    for rel, text in BASE_FILES.items():
        p = main / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    sh("git", "add", "-A", cwd=main)
    sh("git", "commit", "-qm", "init", cwd=main, env=env)
    base = sh("git", "rev-parse", "HEAD", cwd=main).stdout.strip()
    eng = root / "dc-eng-900-toy"
    for d in ("artifacts", "audits", "evidence", "trace/logs"):
        (eng / d).mkdir(parents=True)
    (eng / "brief.md").write_text(f"---\nid: dc-eng-900\nbase: {base}\nbranch: devcraft/dc-eng-900\n---\n")
    (eng / "artifacts" / "build-plan.md").write_text(PLAN)
    sha = hashlib.sha256(PLAN.encode()).hexdigest()
    (eng / "audits" / "plan-gate.md").write_text(GATE.format(sha=sha))
    (eng / "d02-quarantine.md").write_text(YES)
    return {"root": root, "main": main, "base": base, "eng": eng, "env": env}


def build(w, commits, branch="devcraft/dc-eng-900"):
    wt = w["root"] / "wt"
    sh("git", "worktree", "add", "-q", "-b", branch, str(wt), w["base"], cwd=w["main"])
    for seat, changes, msg in commits:
        for rel, text in changes.items():
            p = wt / rel
            if text is None:
                sh("git", "rm", "-q", rel, cwd=wt)
                continue
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text)
            sh("git", "add", rel, cwd=wt)
        full = msg if seat in ("coordinator", "builder") else f"{msg}\n\nDevcraft-Seat: {seat}"
        sh("git", "commit", "-qm", full, cwd=wt, env=w["env"])
    return wt


def run(w, wt, *extra, env=None):
    r = subprocess.run([sys.executable, str(CHECK), "--worktree", str(wt), "--engagement", str(w["eng"]), *extra],
                       capture_output=True, text=True, env=env or w["env"])
    reports = sorted((w["eng"] / "evidence").glob("diff-check-*.txt"))
    text = reports[-1].read_text() if reports else ""
    return r, text


def hits(text):
    out = []
    for line in text.splitlines():
        m = re.match(r"^- H\d+ · (\S+) · (.*) · (REFUSED|matched .*|UNMATCHED)$", line)
        if m:
            out.append((m.group(1), m.group(2), m.group(3)))
    return out


def check_case(w, case):
    name, commits, expect, exit_code = case
    wt = build(w, commits)
    r, text = run(w, wt)
    assert r.returncode == exit_code, f"{name}: exit {r.returncode}, wanted {exit_code}\n{r.stderr}\n{text}"
    found = hits(text)
    for kind, state in expect.items():
        of_kind = [h for h in found if h[0] == kind]
        if state == "absent":
            assert not of_kind, f"{name}: unexpected {kind} hits: {of_kind}"
            continue
        assert of_kind, f"{name}: no {kind} hit\n{text}"
        for h in of_kind:
            assert h[2].startswith(state), f"{name}: {kind} hit {h} is not {state}"
    assert cases.NAME not in text and cases.NAME.lower() not in text.lower(), f"{name}: the name was printed"
    assert cases.FAKE_KEY not in text, f"{name}: a credential value was printed"


@pytest.mark.parametrize("case", cases.MUST_PASS, ids=[c[0] for c in cases.MUST_PASS])
def test_must_pass(world, case):
    check_case(world, case)


@pytest.mark.parametrize("case", cases.MUST_FLAG, ids=[c[0] for c in cases.MUST_FLAG])
def test_must_flag(world, case):
    check_case(world, case)


def test_default_branch_is_refused(world):
    wt = build(world, [("builder", {"src/app.py": "x = 2\n"}, f"{cases.ENG} S1: x")], branch="main-copy")
    r, text = run(world, wt, "--branch", "main")
    assert r.returncode == 2 and "REFUSED" in text and "default branch" in text


def test_plan_edited_after_the_gate_voids_its_additions(world):
    plan = world["eng"] / "artifacts" / "build-plan.md"
    plan.write_text(plan.read_text() + "\n**Test paths added:** `src/` because I say so.\n")
    wt = build(world, [("verifier", {"spec/a.spec.js": "test('a', () => {});\n"}, "tests: spec")])
    r, text = run(world, wt)
    assert r.returncode == 1
    assert "edited after the plan gate" in text
    assert any(h[0] == "boundary" for h in hits(text)), text
    assert "build plan frozen at that anchor: no" in text


def gate_launch(world, pass_id, gate, anchor):
    """The launch record `seat.py launch` leaves for a plan gate that named `anchor` and filed `gate`."""
    (world["eng"] / "trace" / "logs" / f"pass-{pass_id}.launch.json").write_text(json.dumps({
        "pass": f"pass-{pass_id}", "seat": "plan-gate", "vendor": "claude",
        "vendor_basis": {"by": "anchor", "path": anchor, "sha256": "x", "last_writer": "codex"},
        "outputs": [{"path": gate, "sha256": "x"}]}))


def test_a_redrafted_plan_is_read_where_the_plan_gate_read_it(world):
    eng = world["eng"]
    redraft = PLAN.replace("`spec/` because", "`spec/`, `e2e/` because")
    (eng / "artifacts" / "build-plan-r3.md").write_text(redraft)
    (eng / "audits" / "plan-gate-r2.md").write_text(GATE.format(sha=hashlib.sha256(redraft.encode()).hexdigest()))
    gate_launch(world, "08", "audits/plan-gate-r2.md", "artifacts/build-plan-r3.md")
    wt = build(world, [("verifier", {"e2e/a.spec.js": "test('a', () => {});\n"}, "tests: e2e")])
    r, text = run(world, wt)
    assert r.returncode == 0, text
    assert "build plan: artifacts/build-plan-r3.md (the anchor pass-08 named)" in text
    assert "build plan frozen at that anchor: yes" in text
    assert "test paths added: spec/, e2e/" in text


def test_a_gate_anchor_outside_the_artifacts_is_not_followed(world):
    eng = world["eng"]
    (eng / "notes.md").write_text(PLAN.replace("`spec/` because", "`src/` because"))
    (eng / "audits" / "plan-gate-r2.md").write_text(
        GATE.format(sha=hashlib.sha256((eng / "notes.md").read_bytes()).hexdigest()))
    gate_launch(world, "08", "audits/plan-gate-r2.md", "notes.md")
    wt = build(world, [("verifier", {"src/app.py": "x = 2\n"}, "tests: src")])
    r, text = run(world, wt)
    assert r.returncode == 1
    assert "notes.md is not in artifacts/ or inherited/" in text
    assert "build plan frozen at that anchor: no" in text
    assert any(h[0] == "boundary" for h in hits(text)), text


def test_no_floor_is_refused(world):
    main = world["main"]
    sh("git", "rm", "-q", ".devcraft/test-paths", cwd=main)
    sh("git", "commit", "-qm", "drop floor", cwd=main, env=world["env"])
    world["base"] = sh("git", "rev-parse", "HEAD", cwd=main).stdout.strip()
    wt = build(world, [("builder", {"src/app.py": "x = 2\n"}, f"{cases.ENG} S1: x")])
    r, text = run(world, wt, "--base", world["base"])
    assert r.returncode == 2 and "no .devcraft/test-paths" in r.stderr


def test_missing_name_list_fails_closed(world):
    (Path(world["env"]["DEVCRAFT_LOCAL"]) / "names").unlink()
    wt = build(world, [("builder", {"src/app.py": "x = 2\n"}, f"{cases.ENG} S1: x")])
    r, text = run(world, wt)
    assert r.returncode == 2 and "name list is missing" in r.stderr


def test_reports_are_append_only(world):
    wt = build(world, [("builder", {"src/app.py": "x = 2\n"}, f"{cases.ENG} S1: x")])
    run(world, wt)
    run(world, wt)
    names = sorted(p.name for p in (world["eng"] / "evidence").glob("diff-check-*.txt"))
    assert len(names) == 2 and any(n.endswith("-2.txt") for n in names)


def test_report_cites_what_it_read(world):
    wt = build(world, [("builder", {"src/app.py": "x = 2\n"}, f"{cases.ENG} S1: x")])
    r, text = run(world, wt)
    assert r.returncode == 0
    assert "plan gate: audits/plan-gate.md" in text
    assert "exceptions honored: EX1 skip, EX2 dependency, EX3 control, EX4 credential" in text
    assert "ratified ledger entries seen: dc-eng-900.d02 (2026-10-12)" in text
    assert "ops paths flagged for Release: deploy/job.plist" in text
    assert "test paths added: spec/" in text
    assert text.rstrip().endswith("exit: 0")
    assert re.search(r"report: .*diff-check-[0-9a-f]{7}\.txt \(sha256 [0-9a-f]{64}\)", r.stdout)


def test_the_hooks_stamp_the_trailer_the_check_reads(world):
    """End to end with the real git hooks: the Verifier's commit is attributed without a hand-written trailer."""
    wt = world["root"] / "wt"
    sh("git", "worktree", "add", "-q", "-b", "devcraft/dc-eng-900", str(wt), world["base"], cwd=world["main"])
    sh(sys.executable, str(HOOKS / "seat.py"), "worktree", str(wt), "--engagement", str(world["eng"]), cwd=world["root"], env=world["env"])
    sh(sys.executable, str(HOOKS / "seat.py"), "context", "--seat", "verifier", "--worktree", str(wt),
       "--engagement", str(world["eng"]), "--pass", "01", cwd=world["root"], env=world["env"])
    env = dict(world["env"], DEVCRAFT_CONTEXT=str(world["eng"] / "trace" / "logs" / "pass-01.context.json"))
    (wt / "tests" / "test_new.py").write_text("def test_new():\n    pass\n")
    sh("git", "add", "tests/test_new.py", cwd=wt)
    sh("git", "commit", "-qm", "tests: new", cwd=wt, env=env)
    assert "Devcraft-Seat: verifier" in sh("git", "log", "-1", "--format=%B", cwd=wt).stdout
    r, text = run(world, wt)
    assert r.returncode == 0, text
    assert "· verifier ·" in text and "UNATTRIBUTED" not in text
