"""The generated walls: Claude seat settings, the Codex seat home and pass layers.

The Codex layers are run through `codex sandbox`, the same Seatbelt policy a
seat pass gets, with no model call, so this is the OS-level half of the wall
tested for real. The Claude sandbox has no standalone runner; its half is the
live check (`live.py`). Skips the Codex half where `codex` is not installed.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

HOOKS = Path(__file__).resolve().parents[1]
SEAT = HOOKS / "seat.py"
CODEX = shutil.which("codex")


@pytest.fixture(scope="module")
def world(tmp_path_factory):
    # Under the home folder, not /tmp: Codex's :workspace profile always lets
    # a pass write the system temp folder, which would hide an outside write.
    base = Path(os.path.expanduser("~/.cache/devcraft-hooks-test"))
    base.mkdir(parents=True, exist_ok=True)
    root = Path(os.path.realpath(tmp_path_factory.mktemp("w").name and base / os.urandom(4).hex()))
    root.mkdir()
    local, emp = root / "local", root / "emp"
    local.mkdir()
    (emp / "src").mkdir(parents=True)
    (emp / "src" / "x.py").write_text("x")
    (local / "employer-paths").write_text(f"{emp}\n")
    (local / "names").write_text("Examplecorp\n")
    env = dict(os.environ, DEVCRAFT_LOCAL=str(local), DEVCRAFT_PASSES=str(root / "passes"), GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
               GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
    env.pop("DEVCRAFT_CONTEXT", None)
    main = root / "main"
    for d in ("src", "tests", "deploy", ".devcraft", ".github/workflows"):
        (main / d).mkdir(parents=True)
    (main / ".devcraft" / "test-paths").write_text("tests/\n")
    for f, t in (("src/app.py", "a"), ("tests/test_a.py", "t"), ("deploy/job.plist", "j"), (".github/workflows/ci.yml", "c"),
                 ("AGENTS.md", "rules"), (".env", "SECRET=1"), (".env.example", "SECRET=")):
        (main / f).write_text(t)
    run = lambda *a, cwd=main: subprocess.run(list(a), cwd=cwd, env=env, check=True, capture_output=True)  # noqa: E731
    run("git", "init", "-q", "-b", "main")
    run("git", "add", "-A")
    run("git", "commit", "-qm", "init")
    wt = root / "wt"
    run("git", "worktree", "add", "-q", "-b", "devcraft/dc-eng-900", str(wt))
    eng = root / "dc-eng-900-test"
    for d in ("artifacts", "audits", "trace/logs", "held-out"):
        (eng / d).mkdir(parents=True)
    (eng / "held-out" / "h.py").write_text("hidden")
    home = root / "home"
    yield {"root": root, "wt": wt, "eng": eng, "emp": emp, "home": home, "env": env}
    shutil.rmtree(root)


def seat(w, *args):
    return subprocess.run(["python3", str(SEAT), *args], env=w["env"], capture_output=True, text=True, check=True).stdout.strip()


def context(w, s, n, *extra):
    return seat(w, "context", "--seat", s, "--worktree", str(w["wt"]), "--engagement", str(w["eng"]),
                "--pass", n, "--branch", "devcraft/dc-eng-900", *extra)



def test_no_exception_for_agents_md(world):
    r = subprocess.run(["python3", str(SEAT), "context", "--seat", "builder", "--worktree", str(world["wt"]),
                        "--engagement", str(world["eng"]), "--pass", "90", "--grant-control", "AGENTS.md"],
                       env=world["env"], capture_output=True, text=True)
    assert r.returncode != 0 and "no exception" in r.stderr


def test_repo_without_test_path_floor_stops(world, tmp_path):
    bare = tmp_path / "bare"
    bare.mkdir()
    r = subprocess.run(["python3", str(SEAT), "context", "--seat", "builder", "--worktree", str(bare),
                        "--engagement", str(world["eng"]), "--pass", "91"], env=world["env"], capture_output=True, text=True)
    assert r.returncode != 0 and "test-paths" in r.stderr


def test_planner_runs_without_a_floor(world, tmp_path):
    # Open's first stop: the Planner drafts the floor on a repo that has none (master skill, Open 1)
    bare = tmp_path / "bare"
    bare.mkdir()
    ctx = seat(world, "context", "--seat", "build-planner", "--worktree", str(bare), "--engagement", str(world["eng"]), "--pass", "93")
    s = json.loads(Path(seat(world, "claude-settings", ctx)).read_text())
    assert f"Edit(/{bare}/**)" in s["permissions"]["deny"]


def test_context_is_written_once(world):
    context(world, "verifier", "92")
    r = subprocess.run(["python3", str(SEAT), "context", "--seat", "verifier", "--worktree", str(world["wt"]),
                        "--engagement", str(world["eng"]), "--pass", "92"], env=world["env"], capture_output=True, text=True)
    assert r.returncode != 0 and "written once" in r.stderr


def test_claude_settings(world):
    ctx = context(world, "verifier", "10")
    s = json.loads(Path(seat(world, "claude-settings", ctx)).read_text())
    deny = s["permissions"]["deny"]
    wt = str(world["wt"])
    assert f"Read(/{world['emp']})" in deny
    # "tests/" can match at any depth, so src/ is denied file by file
    assert f"Edit(/{wt}/src/app.py)" in deny
    assert not any(r.startswith(f"Edit(/{wt}/tests") for r in deny), "the Verifier writes tests"
    assert f"Read(/{wt}/.env)" in deny and f"Read(/{wt}/.env.example)" not in deny
    sb = s["sandbox"]
    assert sb["enabled"] and sb["failIfUnavailable"] and sb["allowUnsandboxedCommands"] is False
    assert sb["network"]["allowedDomains"] == []
    assert str(world["eng"] / "held-out") not in sb["filesystem"]["denyRead"], "the Verifier writes held-out"
    hooks = s["hooks"]
    assert hooks["PreToolUse"][0]["hooks"][0]["command"].endswith("guard.py") and "SessionStart" in hooks
    assert s["env"]["DEVCRAFT_CONTEXT"] == ctx


def test_planner_cannot_write_the_worktree(world):
    s = json.loads(Path(seat(world, "claude-settings", context(world, "build-planner", "11"))).read_text())
    assert f"Edit(/{world['wt']}/**)" in s["permissions"]["deny"]
    assert str(world["eng"] / "held-out") in s["sandbox"]["filesystem"]["denyRead"]


@pytest.fixture(scope="module")
def codex_home(world):
    seat(world, "codex-home", "--home", str(world["home"]))
    return world["home"]


def test_codex_home_trusts_only_the_guard(world, codex_home):
    hooks = json.loads((codex_home / "hooks.json").read_text())["hooks"]
    assert list(hooks) == ["PreToolUse"]
    cfg = (codex_home / "config.toml").read_text()
    assert "trusted_hash" in cfg and 'default_permissions = "devcraft-floor"' in cfg and "shell_snapshot = false" in cfg


def test_preflight_catches_an_untrusted_hook(world, codex_home):
    hj = codex_home / "hooks.json"
    saved = hj.read_text()
    hj.write_text(saved.replace("guard.py", "guard.py --changed"))
    try:
        r = subprocess.run(["python3", str(SEAT), "check", "--home", str(codex_home)], env=world["env"], capture_output=True, text=True)
        assert r.returncode == 1 and "not trusted" in r.stdout
    finally:
        hj.write_text(saved)


BUILDER_MATRIX = [
    ("echo a > src/new.py && echo WROTE", True),
    ("echo a > tests/x.py && echo WROTE", False),
    ("echo a > deploy/x && echo WROTE", False),
    ("echo a > .github/workflows/x.yml && echo WROTE", False),
    ("echo a >> AGENTS.md && echo WROTE", False),
    ("mkdir -p .claude && echo a > .claude/s.json && echo WROTE", False),
    ("echo a > .git/hooks/pre-commit && echo WROTE", False),
    ("cat .env && echo WROTE", False),
    ("cat .env.example && echo WROTE", True),
    ("cat {EMP}/src/x.py && echo WROTE", False),
    ("cat {ENG}/held-out/h.py && echo WROTE", False),
    ("ls ~/.ssh && echo WROTE", False),
    ("echo a > {ENG}/artifacts/x && echo WROTE", False),
    ("echo a > {ROOT}/outside && echo WROTE", False),
    ("curl -sS -m 5 -o /dev/null https://example.com && echo WROTE", False),
]


def sandboxed(world, home, profile, perm, cmd):
    env = dict(world["env"], CODEX_HOME=str(home))
    r = subprocess.run(["codex", "sandbox", "-p", profile, "-P", perm, "-C", str(world["wt"]), "--", "bash", "-c", cmd],
                       env=env, capture_output=True, text=True, timeout=60)
    return "WROTE" in r.stdout


@pytest.mark.skipif(not CODEX, reason="codex not installed")
@pytest.mark.parametrize("cmd,allowed", BUILDER_MATRIX, ids=[c for c, _ in BUILDER_MATRIX])
def test_builder_layer_in_the_real_sandbox(world, codex_home, cmd, allowed):
    profile_file = codex_home / f"{world['eng'].name}-pass-20.config.toml"
    if not profile_file.exists():
        seat(world, "codex-pass", context(world, "builder", "20", "--ops-path", "deploy/"), "--home", str(codex_home))
    cmd = cmd.replace("{EMP}", str(world["emp"])).replace("{ENG}", str(world["eng"])).replace("{ROOT}", str(world["root"]))
    assert sandboxed(world, codex_home, profile_file.stem.replace(".config", ""), "pass-20", cmd) is allowed


@pytest.mark.skipif(not CODEX, reason="codex not installed")
def test_gate_layer_is_read_only(world, codex_home):
    seat(world, "codex-pass", context(world, "release-gate", "21"), "--home", str(codex_home))
    profile = f"{world['eng'].name}-pass-21"
    assert sandboxed(world, codex_home, profile, "pass-21", "cat src/app.py && echo WROTE")
    assert not sandboxed(world, codex_home, profile, "pass-21", "echo a > src/app.py && echo WROTE")
    assert not sandboxed(world, codex_home, profile, "pass-21", "cat {}/src/x.py && echo WROTE".format(world["emp"]))


# --- launcher: caps, wall files off the ledger, -o to the artifact, frozen diff, probe -------

import sys  # noqa: E402

sys.path.insert(0, str(HOOKS))
import seat as seatmod  # noqa: E402

# One fake for both vendors, run as `codex` or `claude` from a folder put first on
# PATH. The launcher passes PATH through its scrubbed environment and nothing
# else, so the fake reads what to do from behavior.json beside itself.
FAKE = r'''#!/usr/bin/env python3
import json, os, sys, time
from pathlib import Path
b = json.loads((Path(__file__).resolve().parent / "behavior.json").read_text())
argv = sys.argv[1:]
def out(e):
    print(json.dumps(e), flush=True)
if Path(sys.argv[0]).name == "claude":
    model = argv[argv.index("--model") + 1]
    for i in range(b.get("calls", 0)):
        out({"type": "assistant", "message": {"model": b.get("stamp", model), "content": [{"type": "tool_use", "id": f"t{i}", "name": "Bash"}]}})
        time.sleep(b.get("pause", 0))
    time.sleep(b.get("sleep", 0))
    out({"type": "assistant", "message": {"model": b.get("stamp", model), "content": [{"type": "text", "text": "done"}]}})
    out({"type": "result", "subtype": b.get("subtype", "success"), "result": b.get("answer", "FINDINGS"), "usage": {"input_tokens": 10, "output_tokens": 2}})
    sys.exit(0)
model = argv[argv.index("--model") + 1]
effort = [a for a in argv if a.startswith("model_reasoning_effort=")][0].split("=")[1].strip('"')
thread = "th-" + os.urandom(3).hex()
home = Path(os.environ["CODEX_HOME"]) / "sessions" / "2026" / "10" / "12"
home.mkdir(parents=True, exist_ok=True)
(home / f"rollout-{thread}.jsonl").write_text(
    json.dumps({"type": "session_meta", "payload": {"id": thread, "session_id": thread}}) + "\n"
    + json.dumps({"type": "turn_context", "payload": {"model": b.get("stamp", model), "effort": effort}}) + "\n")
if b.get("helper"):
    (home / f"rollout-h-{thread}.jsonl").write_text(json.dumps({"type": "session_meta", "payload": {
        "id": "h-" + thread, "session_id": thread, "thread_source": "subagent", "parent_thread_id": thread}}) + "\n")
out({"type": "thread.started", "thread_id": thread})
for i in range(b.get("calls", 0)):
    out({"type": "item.started", "item": {"id": f"item_{i}", "type": "command_execution", "command": "echo"}})
    out({"type": "item.completed", "item": {"id": f"item_{i}", "type": "command_execution", "command": "echo"}})
    time.sleep(b.get("pause", 0))
time.sleep(b.get("sleep", 0))
out({"type": "item.completed", "item": {"id": "msg", "type": "agent_message", "text": b.get("answer", "CHANGE NOTE")}})
out({"type": "turn.completed", "usage": {"input_tokens": 100, "cached_input_tokens": 40, "output_tokens": 7}})
if "-o" in argv:
    Path(argv[argv.index("-o") + 1]).write_text(b.get("answer", "CHANGE NOTE") + "\n")
Path(__file__).resolve().parent.joinpath("finished").write_text("1")
'''


@pytest.fixture(scope="module")
def fake(world):
    bin_dir = world["root"] / "fakebin"
    bin_dir.mkdir()
    for name in ("codex", "claude"):
        (bin_dir / name).write_text(FAKE)
        (bin_dir / name).chmod(0o755)
    world["env"]["PATH"] = f"{bin_dir}:{world['env']['PATH']}"
    yield bin_dir
    world["env"]["PATH"] = world["env"]["PATH"].split(":", 1)[1]


def behave(fake, **b):
    (fake / "behavior.json").write_text(json.dumps(b))
    (fake / "finished").unlink(missing_ok=True)


def launch(w, ctx, *extra):
    prompt = w["root"] / "prompt.md"
    prompt.write_text("do the work")
    return subprocess.run(["python3", str(SEAT), "launch", ctx, "--prompt-file", str(prompt), "--home", str(w["home"]), *extra],
                          env=w["env"], capture_output=True, text=True, timeout=120)


def record(w, n):
    return json.loads((w["eng"] / "trace" / "logs" / f"pass-{n}.launch.json").read_text())


def test_caps_default_by_seat_and_override(world):
    b = json.loads(Path(context(world, "builder", "30")).read_text())["caps"]
    assert b == {"minutes": 60, "tool_calls": 200}
    v = json.loads(Path(context(world, "verifier", "31", "--cap-minutes", "45")).read_text())["caps"]
    assert v == {"minutes": 45, "budget_usd": 15}
    g = json.loads(Path(context(world, "release-gate", "32")).read_text())["caps"]
    assert g == {"minutes": 20, "tool_calls": 80}
    r = subprocess.run(["python3", str(SEAT), "context", "--seat", "builder", "--worktree", str(world["wt"]), "--engagement",
                        str(world["eng"]), "--pass", "33", "--cap-budget-usd", "5"], env=world["env"], capture_output=True, text=True)
    assert r.returncode != 0 and "no budget flag" in r.stderr


def test_wall_files_live_outside_the_engagement(world, codex_home):
    passes = world["root"] / "passes" / world["eng"].name
    s = Path(seat(world, "claude-settings", context(world, "build-planner", "34")))
    assert s == passes / "pass-34.settings.json" and (s.stat().st_mode & 0o777) == 0o600
    again = subprocess.run(["python3", str(SEAT), "claude-settings", str(world["eng"] / "trace" / "logs" / "pass-34.context.json")],
                           env=world["env"], capture_output=True, text=True)
    assert again.returncode != 0 and "written once" in again.stderr
    profile = seat(world, "codex-pass", context(world, "builder", "35"), "--home", str(codex_home))
    link = codex_home / f"{profile}.config.toml"
    assert link.is_symlink() and link.resolve() == (passes / "pass-35.codex-layer.toml").resolve()
    logs = world["eng"] / "trace" / "logs"
    assert not list(logs.glob("*.settings.json")) and not list(logs.glob("*.codex-layer.toml"))
    assert (logs / "pass-34.context.json").exists(), "the context stays in trace/logs"
    deny = json.loads(s.read_text())["permissions"]["deny"]
    assert f"Edit(/{world['root'] / 'passes'}/**)" in deny, "a seat cannot touch its own wall"


def test_security_pass_runs_on_claude_read_only(world):
    s = json.loads(Path(seat(world, "claude-settings", context(world, "security-pass", "36"))).read_text())
    assert f"Edit(/{world['wt']}/**)" in s["permissions"]["deny"]
    assert str(world["eng"] / "held-out") in s["sandbox"]["filesystem"]["denyRead"]


def test_output_rules(world, codex_home):
    ctx = context(world, "release-gate", "37")
    seat(world, "codex-pass", ctx, "--home", str(codex_home))
    r = launch(world, ctx)
    assert r.returncode != 0 and "--output" in r.stderr, "a Codex pass names its artifact"
    r = launch(world, ctx, "--output", "trace/logs/x.md")
    assert r.returncode != 0 and "artifacts/ or audits/" in r.stderr
    r = launch(world, ctx, "--output", "artifacts/release-gate-findings.md")
    argv = json.loads(r.stderr)["argv"]
    assert r.returncode == 0 and argv[argv.index("-o") + 1] == str(world["eng"] / "artifacts" / "release-gate-findings.md")
    assert argv[argv.index("--model") + 1] == "gpt-6.1-sol"
    v = context(world, "verifier", "38")
    seat(world, "claude-settings", v)
    r = launch(world, v, "--output", "artifacts/x.md")
    assert r.returncode != 0 and "writes its own artifact" in r.stderr
    argv = json.loads(launch(world, v).stderr)["argv"]
    assert argv[argv.index("--output-format") + 1] == "stream-json" and "--verbose" in argv
    assert argv[argv.index("--max-budget-usd") + 1] == "15"
    assert argv[argv.index("--settings") + 1] == str(world["root"] / "passes" / world["eng"].name / "pass-38.settings.json")


def codex_pass(w, home, n, *caps):
    ctx = context(w, "builder", n, *caps)
    seat(w, "codex-pass", ctx, "--home", str(home))
    return ctx


def test_launch_kills_at_the_tool_call_cap(world, codex_home, fake):
    behave(fake, calls=10, pause=0.3)
    r = launch(world, codex_pass(world, codex_home, "40", "--cap-tool-calls", "3"), "--output", "artifacts/pass-40.md", "--run")
    rec = record(world, "40")
    assert r.returncode == 2 and rec["stopped"] == "tool-calls" and rec["outcome"].startswith("Blocked: budget")
    assert rec["tool_calls"] == 3 and not (fake / "finished").exists(), "killed, not finished"
    assert (world["eng"] / rec["raw_log"]).read_text().count('"item.started"') == 3


def test_launch_kills_at_the_wall_clock(world, codex_home, fake):
    behave(fake, calls=1, sleep=60)
    r = launch(world, codex_pass(world, codex_home, "41", "--cap-minutes", "0.03"), "--output", "artifacts/pass-41.md", "--run")
    rec = record(world, "41")
    assert r.returncode == 2 and rec["stopped"] == "wall-clock" and rec["wall_clock_s"] < 20
    assert rec["tool_calls"] == 1 and not (fake / "finished").exists()


def test_launch_files_a_clean_codex_pass(world, codex_home, fake):
    behave(fake, calls=2, answer="CHANGE NOTE v1")
    r = launch(world, codex_pass(world, codex_home, "42"), "--output", "artifacts/change-note.md", "--run")
    rec = record(world, "42")
    out = world["eng"] / "artifacts" / "change-note.md"
    assert r.returncode == 0 and rec["stopped"] is None and rec["exit_code"] == 0
    assert out.read_text() == "CHANGE NOTE v1\n"
    assert rec["outputs"] == [{"path": "artifacts/change-note.md", "sha256": seatmod.sha256(out)}]
    assert rec["usage"]["input_tokens"] == 100 and rec["meter_source"] == "codex turn.completed.usage"
    assert rec["rollouts"] == {"path": "trace/logs/pass-42.rollouts", "files": 1}
    assert rec["runtime_stamps"] == ["gpt-6.1-sol high"]
    wall = rec["wall_files"][0]
    assert wall["sha256"] == seatmod.sha256(Path(wall["path"])) and not wall["path"].startswith(str(world["eng"]))
    again = launch(world, str(world["eng"] / "trace" / "logs" / "pass-42.context.json"), "--output", "artifacts/other.md", "--run")
    assert again.returncode != 0 and "launched once" in again.stderr


def test_launch_catches_a_helper_agent(world, codex_home, fake):
    behave(fake, calls=1, helper=True)
    r = launch(world, codex_pass(world, codex_home, "43"), "--output", "artifacts/change-note-43.md", "--run")
    rec = record(world, "43")
    assert r.returncode == 3 and any("helper session" in h for h in rec["helper_agent"])
    assert not (world["eng"] / "artifacts" / "change-note-43.md").exists(), "the artifact path is freed for the re-run"
    assert (world["eng"] / rec["discarded_output"]).exists() and "outputs" not in rec


def test_launch_files_a_read_only_claude_pass(world, fake):
    behave(fake, calls=2, answer="SECURITY PASS FINDINGS")
    ctx = context(world, "security-pass", "44")
    seat(world, "claude-settings", ctx)
    r = launch(world, ctx, "--output", "artifacts/security-findings.md", "--run")
    rec = record(world, "44")
    assert r.returncode == 0 and rec["tool_calls"] == 2 and rec["meter_source"] == "claude -p result.usage"
    assert (world["eng"] / "artifacts" / "security-findings.md").read_text() == "SECURITY PASS FINDINGS\n"
    assert '"model": "claude-opus-5-5"' in (world["eng"] / rec["raw_log"]).read_text(), "line 11's stamp is in the raw log"


def test_claude_stopping_at_its_budget_is_blocked_budget(world, fake):
    behave(fake, calls=1, subtype="error_max_budget_usd")
    ctx = context(world, "verifier", "45")
    seat(world, "claude-settings", ctx)
    r = launch(world, ctx, "--run")
    assert r.returncode == 2 and record(world, "45")["stopped"] == "budget-usd"


def test_freeze_diff(world):
    wt, env = world["wt"], world["env"]
    (wt / "src" / "app.py").write_text("b\n")
    subprocess.run(["git", "-C", str(wt), "commit", "-qam", "slice 1"], env=env, check=True)
    ctx = context(world, "builder", "46")
    out = json.loads(seat(world, "freeze-diff", ctx, "--base", "main"))
    patch = world["eng"] / out["path"]
    assert out["path"] == "artifacts/pass-46.diff.patch" and out["sha256"] == seatmod.sha256(patch)
    assert "+b" in patch.read_text() and len(out["base"]) == 40 and out["base"] != out["point"]
    check = subprocess.run(["git", "-C", str(world["root"] / "main"), "apply", "--check", str(patch)], capture_output=True)
    assert check.returncode == 0, "the patch applies to the base"
    r = subprocess.run(["python3", str(SEAT), "freeze-diff", ctx, "--base", "main"], env=env, capture_output=True, text=True)
    assert r.returncode != 0 and "written once" in r.stderr


def test_probe_reads_the_stamp_not_the_answer(world, codex_home, fake):
    behave(fake, answer="I am some model")
    r = subprocess.run(["python3", str(SEAT), "probe", "--home", str(codex_home)], env=world["env"], capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stdout + r.stderr
    for line in ("`claude-opus-5-5` on `claude -p`", "`gpt-6.1-sol` (high) on `codex exec`"):
        assert line in r.stdout
    assert "gpt-5.6-sol" not in r.stdout, "the gate default is gpt-6.1-sol since 2026-10-12, so the probe has two ids"
    assert r.stdout.count("Match.") == 2
    behave(fake, stamp="gpt-5.4")
    r = subprocess.run(["python3", str(SEAT), "probe", "--home", str(codex_home)], env=world["env"], capture_output=True, text=True, timeout=60)
    assert r.returncode == 1 and "MISMATCH" in r.stdout


def test_seat_files_name_the_launcher_pins():
    bench = HOOKS.parents[0] / "bench"
    lines = {f.stem: next(line for line in f.read_text().splitlines() if line.startswith("model:"))
             for f in bench.glob("*.md") if f.stem in seatmod.policy.SEATS}
    for s, line in lines.items():
        want = seatmod.CLAUDE_MODEL if s in seatmod.CLAUDE_LAUNCH else f"codex {seatmod.codex_model(s)} {seatmod.CODEX_EFFORT}"
        assert line.split("#")[0].split(":", 1)[1].strip() == want, s
