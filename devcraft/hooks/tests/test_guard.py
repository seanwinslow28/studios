"""Every seeded case through the guard, in both vendors' payload shapes.

Each case runs the guard as the harness does: a fresh `/usr/bin/python3`
process (the interpreter the hooks name), the tool call on stdin, the seat
context named by `$DEVCRAFT_CONTEXT`. A temporary home stands in for `~`, so
credential and employer paths are fixtures, never the real ones.

Run: `uv run --no-project --with pytest python -m pytest devcraft/hooks/tests -q`
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cases  # noqa: E402

HOOKS = Path(__file__).resolve().parents[1]
GUARD = HOOKS / "guard.py"
PYTHONS = [p for p in ("/usr/bin/python3", sys.executable) if os.path.exists(p)]


@pytest.fixture(scope="module")
def world(tmp_path_factory):
    root = Path(os.path.realpath(tmp_path_factory.mktemp("world")))
    home = root / "home"
    (home / ".ssh").mkdir(parents=True)
    (home / ".ssh" / "id_ed25519").write_text("fake")
    (home / ".config" / "gh").mkdir(parents=True)
    (home / ".aws").mkdir()
    emp = home / "Work" / "employer"
    (emp / "src").mkdir(parents=True)
    local = home / ".config" / "devcraft"
    local.mkdir(parents=True)
    (local / "employer-paths").write_text(f"# test list\n{emp}\n")
    (local / "names").write_text("Examplecorp\n")
    wt = root / "wt"
    for d in ("src", "tests", "deploy", ".devcraft", ".github/workflows", ".claude"):
        (wt / d).mkdir(parents=True)
    (wt / ".devcraft" / "test-paths").write_text("tests/\n__snapshots__/\n")
    (wt / "tests" / "test_a.py").write_text("")
    (wt / "src" / "app.py").write_text("")
    (wt / "link-out").symlink_to(root / "elsewhere", target_is_directory=True)
    (root / "elsewhere").mkdir()
    eng = root / "eng"
    for d in ("artifacts", "audits", "trace/logs", "held-out"):
        (eng / d).mkdir(parents=True)
    (eng / "audits" / "plan-audit.md").write_text("x")
    scratch = root / "scratch" / "eng" / "pass-01"  # as policy.scratch_dir lays it out
    scratch.mkdir(parents=True)
    (root / "scratch" / "eng" / "pass-00").mkdir()  # an earlier pass's, perhaps the Verifier's
    (root / "scratch" / "eng" / "pass-00" / "held-copy.py").write_text("hidden")
    contexts = {}
    for seat in ("build-planner", "builder", "verifier", "release-reliability", "security-pass", "release-gate"):
        ctx = {"seat": seat, "worktree": str(wt), "engagement": str(eng), "branch": "devcraft/dc-eng-001",
               "ops_paths": ["deploy/"], "log": str(eng / "trace" / "logs" / "guard.jsonl"),
               "scratch": str(scratch), "read_only": seat in ("security-pass", "release-gate")}
        if seat == "builder":
            ctx["grants"] = {"read": [str(wt / ".env.test")], "control": [".github/workflows/ci.yml"]}
        p = eng / "trace" / "logs" / f"{seat}.context.json"
        p.write_text(json.dumps(ctx))
        contexts[seat] = p
    return {"root": root, "home": home, "wt": wt, "eng": eng, "emp": emp, "scratch": scratch, "contexts": contexts}


def fill(text: str, w) -> str:
    return (text.replace("{WT}", str(w["wt"])).replace("{ENG}", str(w["eng"])).replace("{EMP}", str(w["emp"]))
            .replace("{SCR}", str(w["scratch"])))


def run(w, seat, event, python=PYTHONS[0], context=True):
    env = {"PATH": "/usr/bin:/bin", "HOME": str(w["home"]), "DEVCRAFT_SEAT": seat}
    if context:
        env["DEVCRAFT_CONTEXT"] = str(w["contexts"][seat])
    r = subprocess.run([python, str(GUARD)], input=json.dumps(event), capture_output=True, text=True, env=env, cwd=str(w["wt"]))
    return r.returncode, r.stderr


def bash_events(cmd, wt):
    claude = {"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": cmd}, "cwd": str(wt)}
    codex = dict(claude, turn_id="t1", model="gpt-5.6-sol", permission_mode="bypassPermissions")
    return [("claude", claude), ("codex", codex)]


def tool_event(tool, path, wt):
    if tool == "apply_patch":
        patch = f"*** Begin Patch\n*** Update File: {path}\n@@\n-a\n+b\n*** End Patch"
        return {"hook_event_name": "PreToolUse", "tool_name": "apply_patch", "tool_input": {"command": patch}, "cwd": str(wt), "turn_id": "t1"}
    key = "url" if tool == "WebFetch" else "file_path"
    return {"hook_event_name": "PreToolUse", "tool_name": tool, "tool_input": {key: path}, "cwd": str(wt)}


@pytest.mark.parametrize("seat,cmd,why", cases.DENY_BASH, ids=[c[2] for c in cases.DENY_BASH])
def test_bash_denied(world, seat, cmd, why):
    for vendor, ev in bash_events(fill(cmd, world), world["wt"]):
        code, err = run(world, seat, ev)
        assert code == 2, f"{vendor}: not refused: {cmd!r} ({why})"
        assert "Devcraft guard:" in err


@pytest.mark.parametrize("seat,cmd,why", cases.ALLOW_BASH, ids=[c[2] for c in cases.ALLOW_BASH])
def test_bash_allowed(world, seat, cmd, why):
    for vendor, ev in bash_events(fill(cmd, world), world["wt"]):
        code, err = run(world, seat, ev)
        assert code == 0, f"{vendor}: refused {cmd!r} ({why}): {err}"


@pytest.mark.parametrize("seat,call,why", cases.DENY_TOOL, ids=[c[2] for c in cases.DENY_TOOL])
def test_tool_denied(world, seat, call, why):
    code, err = run(world, seat, tool_event(call[0], fill(call[1], world), world["wt"]))
    assert code == 2, f"not refused: {call} ({why})"


@pytest.mark.parametrize("seat,call,why", cases.ALLOW_TOOL, ids=[c[2] for c in cases.ALLOW_TOOL])
def test_tool_allowed(world, seat, call, why):
    code, err = run(world, seat, tool_event(call[0], fill(call[1], world), world["wt"]))
    assert code == 0, f"refused {call} ({why}): {err}"


@pytest.mark.parametrize("seat,cmd,why", cases.GRANTED, ids=[c[2] for c in cases.GRANTED])
def test_grants_open_only_the_named_file(world, seat, cmd, why):
    ev = bash_events(fill(cmd, world), world["wt"])[1][1]
    assert run(world, seat, ev)[0] == 0, why
    # the same call by another seat stays shut
    other = "release-reliability"
    assert run(world, other, ev)[0] == 2


def test_no_context_fails_closed(world):
    code, err = run(world, "builder", bash_events("ls", world["wt"])[0][1], context=False)
    assert code == 2 and "cannot run" in err


def test_missing_employer_list_fails_closed(world):
    lst = world["home"] / ".config" / "devcraft" / "employer-paths"
    saved = lst.read_text()
    lst.unlink()
    try:
        code, err = run(world, "builder", bash_events("cat src/app.py", world["wt"])[0][1])
        assert code == 2 and "employer-path list is missing" in err
    finally:
        lst.write_text(saved)


def test_every_decision_is_logged(world):
    log = world["eng"] / "trace" / "logs" / "guard.jsonl"
    before = log.read_text().count("\n") if log.exists() else 0
    run(world, "builder", bash_events("ls", world["wt"])[0][1])
    lines = log.read_text().splitlines()
    assert len(lines) == before + 1 and json.loads(lines[-1])["decision"] == "allow"


@pytest.mark.parametrize("python", PYTHONS)
def test_runs_on_each_interpreter(world, python):
    assert run(world, "builder", bash_events("sudo ls", world["wt"])[0][1], python=python)[0] == 2


def test_no_floor_stops_every_seat_but_the_planner(world):
    # The one-off that drafts a repo's floor runs the Build Planner on a repo
    # without one; it writes only in the engagement folder, so the floor never
    # bears on its wall. Every other seat still fails closed.
    floor = world["wt"] / ".devcraft" / "test-paths"
    saved = floor.read_text()
    floor.unlink()
    try:
        start = {"hook_event_name": "SessionStart", "cwd": str(world["wt"])}
        log = world["eng"] / "trace" / "logs" / "guard.jsonl"
        run(world, "build-planner", start)
        assert json.loads(log.read_text().splitlines()[-1])["decision"] == "session-start"
        run(world, "builder", start)
        assert "cannot run" in json.loads(log.read_text().splitlines()[-1])["decision"]
        artifact = str(world["eng"] / "artifacts" / "test-paths.md")
        assert run(world, "build-planner", tool_event("Write", artifact, world["wt"]))[0] == 0
        assert run(world, "build-planner", tool_event("Write", str(world["wt"] / "src" / "app.py"), world["wt"]))[0] == 2
        assert run(world, "build-planner", tool_event("Write", str(floor), world["wt"]))[0] == 2
        assert run(world, "builder", tool_event("Write", str(world["wt"] / "src" / "app.py"), world["wt"]))[0] == 2
    finally:
        floor.write_text(saved)
