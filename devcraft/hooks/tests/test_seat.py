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
    # The Codex plugin cache the toolbelt's copies come from, an old and a newer version (SWCB #149)
    for version, text in (("old", "stale"), ("new", "current")):
        for skill in ("executing-plans", "verification-before-completion"):
            d = root / "plugins" / "superpowers" / version / "skills" / skill
            d.mkdir(parents=True)
            (d / "SKILL.md").write_text(text)
    os.utime(root / "plugins" / "superpowers" / "old", (1, 1))
    env = dict(os.environ, DEVCRAFT_LOCAL=str(local), DEVCRAFT_PASSES=str(root / "passes"),
               DEVCRAFT_SCRATCH_ROOT=str(root / "scratch"), DEVCRAFT_PLUGIN_CACHE=str(root / "plugins"),
               GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
               GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
    env.pop("DEVCRAFT_CONTEXT", None)
    main = root / "main"
    for d in ("src/pkg/tests", "tests", "deploy", ".devcraft", ".github/workflows"):
        (main / d).mkdir(parents=True)
    (main / ".devcraft" / "test-paths").write_text("tests/\ntest_*.py\nfixtures/\n")
    for f, t in (("src/app.py", "a"), ("src/test_c.py", "t"), ("src/pkg/tests/test_b.py", "t"),
                 ("tests/test_a.py", "t"), ("deploy/job.plist", "j"), (".github/workflows/ci.yml", "c"),
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
    # Anchors and repaired artifacts, by who last wrote them (their header's model: line)
    (eng / "artifacts" / "by-claude.md").write_text("---\nid: x\nmodel: claude-opus-5-5             # the runtime\n---\n\nplan\n")
    (eng / "artifacts" / "by-codex.md").write_text("---\nmodel: codex gpt-6.1-sol high\n---\n\nnote\n")
    home = root / "home"
    yield {"root": root, "wt": wt, "eng": eng, "emp": emp, "home": home, "env": env}
    shutil.rmtree(root)


def seat(w, *args):
    return subprocess.run(["python3", str(SEAT), *args], env=w["env"], capture_output=True, text=True, check=True).stdout.strip()


CLAUDE_ANCHOR = ("--anchor", "artifacts/by-claude.md")
CODEX_ANCHOR = ("--anchor", "artifacts/by-codex.md")


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
    codex = os.path.expanduser("~/.codex")  # Sean's own Codex home (SWCB #149)
    assert codex in sb["filesystem"]["denyRead"] and f"Read(/{codex}/**)" in deny
    hooks = s["hooks"]
    assert hooks["PreToolUse"][0]["hooks"][0]["command"].endswith("guard.py") and "SessionStart" in hooks
    assert s["env"]["DEVCRAFT_CONTEXT"] == ctx


def test_release_cannot_write_a_nested_test(world):
    # src/ is Release's ops path here, but the tests inside it stay out of reach
    s = json.loads(Path(seat(world, "claude-settings", context(world, "release-reliability", "12", "--ops-path", "src/"))).read_text())
    deny, wt = s["permissions"]["deny"], str(world["wt"])
    assert f"Edit(/{wt}/src/pkg/tests/**)" in deny and f"Edit(/{wt}/src/test_c.py)" in deny
    assert f"Edit(/{wt}/src/app.py)" not in deny


def test_covered_lists_every_match_at_any_depth(world):
    ctx = seatmod.load(context(world, "builder", "13"))
    got = seatmod.covered(ctx, ctx.test_paths())
    # a matched folder is listed whole; an absent glob-free pattern is listed at the top
    assert got == ["fixtures", "src/pkg/tests", "src/test_c.py", "tests"]


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
    assert f'"{os.path.expanduser("~/.codex")}" = "deny"' in cfg, "the floor denies Sean's own Codex home (SWCB #149)"


def test_codex_home_copies_the_toolbelt_from_the_newest_version(world, codex_home):
    for skill in ("executing-plans", "verification-before-completion"):
        assert (codex_home / "toolbelt" / "superpowers" / skill / "SKILL.md").read_text() == "current"


def test_the_seat_home_never_sits_inside_sean_codex_home(world):
    r = subprocess.run(["python3", str(SEAT), "codex-home", "--home", "~/.codex/devcraft-seat-test"],
                       env=world["env"], capture_output=True, text=True)
    assert r.returncode != 0 and "SWCB #149" in r.stderr
    assert not os.path.exists(os.path.expanduser("~/.codex/devcraft-seat-test"))


def test_preflight_catches_a_missing_toolbelt_copy(world, codex_home):
    saved = codex_home / "toolbelt" / "superpowers" / "executing-plans"
    saved.rename(saved.with_name("moved"))
    try:
        r = subprocess.run(["python3", str(SEAT), "check", "--home", str(codex_home)], env=world["env"], capture_output=True, text=True)
        assert r.returncode == 1 and "superpowers:executing-plans has no copy" in r.stdout
    finally:
        saved.with_name("moved").rename(saved)


@pytest.mark.skipif(not CODEX, reason="codex not installed")
def test_codex_finds_no_skills_in_sean_codex_home(world, codex_home):
    # Codex finds skills by $CODEX_HOME and ~/.agents/skills, never by Sean's own ~/.codex (SWCB #149)
    roots = seatmod.skill_roots(codex_home)
    assert roots, "the skill-roots table could not be read"
    assert not [r for r in roots if r.startswith(os.path.expanduser("~/.codex/"))]
    assert any(r.startswith(str(codex_home)) for r in roots)


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
    # "tests/" and "test_*.py" match at any depth, not just the top (SWCB #134)
    ("echo a > src/pkg/tests/test_b.py && echo WROTE", False),
    ("echo a > src/pkg/tests/new.py && echo WROTE", False),
    ("echo a > src/test_c.py && echo WROTE", False),
    ("echo a > src/pkg/helper.py && echo WROTE", True),
    # a glob-free pattern is held even before it exists
    ("mkdir -p fixtures && echo a > fixtures/x.json && echo WROTE", False),
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
    ("ls ~/.codex/skills && echo WROTE", False),  # Sean's own Codex home (SWCB #149)
    ("ls ~/.codex/packages && echo WROTE", True),  # but Codex's own install, which the sandbox re-runs
    ("echo a > {ENG}/artifacts/x && echo WROTE", False),
    ("echo a > {ROOT}/outside && echo WROTE", False),
    ("curl -sS -m 5 -o /dev/null https://example.com && echo WROTE", False),
    ("echo a > {SCR}/probe.py && echo WROTE", True),
    ("echo a > {ROOT}/scratch/{ENGNAME}/pass-99/x && echo WROTE", False),
]


def scratch_of(world, n):
    return world["root"] / "scratch" / world["eng"].name / f"pass-{n}"


def sandboxed(world, home, profile, perm, cmd):
    env = dict(world["env"], CODEX_HOME=str(home))
    # the real codex by its path: the launcher tests put a fake one first on PATH
    r = subprocess.run([CODEX, "sandbox", "-p", profile, "-P", perm, "-C", str(world["wt"]), "--", "bash", "-c", cmd],
                       env=env, capture_output=True, text=True, timeout=60)
    return "WROTE" in r.stdout


@pytest.mark.skipif(not CODEX, reason="codex not installed")
@pytest.mark.parametrize("cmd,allowed", BUILDER_MATRIX, ids=[c for c, _ in BUILDER_MATRIX])
def test_builder_layer_in_the_real_sandbox(world, codex_home, cmd, allowed):
    profile_file = codex_home / f"{world['eng'].name}-pass-20.config.toml"
    if not profile_file.exists():
        seat(world, "codex-pass", context(world, "builder", "20", "--ops-path", "deploy/"), "--home", str(codex_home))
    cmd = cmd.replace("{EMP}", str(world["emp"])).replace("{ENG}", str(world["eng"])).replace("{ROOT}", str(world["root"]))
    cmd = cmd.replace("{SCR}", str(scratch_of(world, "20"))).replace("{ENGNAME}", world["eng"].name)
    assert sandboxed(world, codex_home, profile_file.stem.replace(".config", ""), "pass-20", cmd) is allowed


@pytest.mark.skipif(not CODEX, reason="codex not installed")
def test_gate_layer_is_read_only(world, codex_home):
    seat(world, "codex-pass", context(world, "release-gate", "21", *CLAUDE_ANCHOR, "--candidate", "HEAD"), "--home", str(codex_home))
    profile = f"{world['eng'].name}-pass-21"
    assert sandboxed(world, codex_home, profile, "pass-21", "cat src/app.py && echo WROTE")
    assert not sandboxed(world, codex_home, profile, "pass-21", "echo a > src/app.py && echo WROTE")
    assert not sandboxed(world, codex_home, profile, "pass-21", "cat {}/src/x.py && echo WROTE".format(world["emp"]))
    # its one write is its own scratch folder (SWCB #148): a probe, a copy of the tree, a test home
    scr = scratch_of(world, "21")
    assert sandboxed(world, codex_home, profile, "pass-21", f"echo a > {scr}/probe.py && echo WROTE")
    assert sandboxed(world, codex_home, profile, "pass-21",
                     f"git archive -o {scr}/src.tar HEAD src && mkdir {scr}/copy && tar -x -f {scr}/src.tar -C {scr}/copy && echo WROTE")
    assert sandboxed(world, codex_home, profile, "pass-21", f"TMPDIR={scr} mktemp -d && echo WROTE")
    assert not sandboxed(world, codex_home, profile, "pass-21", f"echo a > {world['eng']}/artifacts/x && echo WROTE")


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
    g = json.loads(Path(context(world, "release-gate", "32", *CLAUDE_ANCHOR, "--candidate", "HEAD")).read_text())["caps"]
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
    s = json.loads(Path(seat(world, "claude-settings", context(world, "security-pass", "36", *CODEX_ANCHOR))).read_text())
    assert f"Edit(/{world['wt']}/**)" in s["permissions"]["deny"]
    assert str(world["eng"] / "held-out") in s["sandbox"]["filesystem"]["denyRead"]


# --- the scratch folder (SWCB #148) -------------------------------------------------

def test_every_pass_gets_an_empty_private_scratch_folder(world):
    data = json.loads(Path(context(world, "security-pass", "160", *CODEX_ANCHOR)).read_text())
    scr = scratch_of(world, "160")
    assert data["scratch"] == str(scr) and scr.is_dir() and not any(scr.iterdir())
    assert scr.stat().st_mode & 0o777 == 0o700


def test_a_scratch_folder_starts_empty_and_outside_every_repo(world):
    scr = scratch_of(world, "161")
    scr.mkdir(parents=True)
    (scr / "left-over").write_text("x")
    args = ["python3", str(SEAT), "context", "--seat", "verifier", "--worktree", str(world["wt"]),
            "--engagement", str(world["eng"]), "--pass", "161"]
    r = subprocess.run(args, env=world["env"], capture_output=True, text=True)
    assert r.returncode != 0 and "not empty" in r.stderr
    assert not (world["eng"] / "trace" / "logs" / "pass-161.context.json").exists()
    env = dict(world["env"], DEVCRAFT_SCRATCH_ROOT=str(world["root"] / "main" / "scratch"))  # another repo
    r = subprocess.run(args[:-1] + ["162"], env=env, capture_output=True, text=True)
    assert r.returncode != 0 and "inside the repo" in r.stderr
    env = dict(world["env"], DEVCRAFT_SCRATCH_ROOT=str(world["wt"] / "scratch"))
    r = subprocess.run(args[:-1] + ["162"], env=env, capture_output=True, text=True)
    assert r.returncode != 0 and "overlaps the worktree" in r.stderr


def test_a_read_only_claude_pass_writes_only_its_scratch_folder(world):
    ctx = context(world, "security-pass", "163", *CODEX_ANCHOR)
    s = json.loads(Path(seat(world, "claude-settings", ctx)).read_text())
    scr = str(scratch_of(world, "163"))
    assert s["sandbox"]["filesystem"]["allowWrite"] == [scr]
    deny = s["permissions"]["deny"]
    assert f"Edit(/{world['eng']}/**)" in deny and f"Edit(/{world['wt']}/**)" in deny
    assert not any(scr in r for r in deny)
    shown = json.loads(launch(world, ctx, "--output", "audits/security-pass-163.md").stderr)
    argv, env = shown["argv"], shown["env"]
    assert argv[argv.index("--tools") + 1] == "Read,Write,Bash,Glob,Grep,Skill", "Write, never Edit"
    assert ["--add-dir", scr] == argv[argv.index(scr) - 1:argv.index(scr) + 1]
    assert "TMPDIR" in env and "DEVCRAFT_SCRATCH" in env


def test_the_launch_points_tmpdir_at_the_scratch_folder(world):
    ctx = seatmod.load(context(world, "verifier", "164"))
    env = seatmod.scrubbed_env(ctx, world["home"])
    assert env["TMPDIR"] == env["DEVCRAFT_SCRATCH"] == str(scratch_of(world, "164"))


def test_an_old_context_runs_without_a_scratch_folder(world):
    p = Path(context(world, "security-pass", "165", *CODEX_ANCHOR))
    data = json.loads(p.read_text())
    del data["scratch"]
    p.write_text(json.dumps(data))
    s = json.loads(Path(seat(world, "claude-settings", str(p))).read_text())
    assert s["sandbox"]["filesystem"]["allowWrite"] == []
    argv = json.loads(launch(world, str(p), "--output", "audits/security-pass-165.md").stderr)["argv"]
    assert argv[argv.index("--tools") + 1] == "Read,Bash,Glob,Grep,Skill"


@pytest.mark.skipif(not CODEX, reason="codex not installed")
def test_no_pass_reads_another_pass_scratch_folder(world, codex_home):
    # A Verifier sees held-out/ and could copy it into its scratch; the Builder after it never reads that
    context(world, "verifier", "166")
    (scratch_of(world, "166") / "held-copy.py").write_text("hidden")
    ctx = context(world, "builder", "167")
    seat(world, "codex-pass", ctx, "--home", str(codex_home))
    profile = f"{world['eng'].name}-pass-167"
    assert not sandboxed(world, codex_home, profile, "pass-167", f"cat {scratch_of(world, '166')}/held-copy.py && echo WROTE")
    assert sandboxed(world, codex_home, profile, "pass-167", f"echo a > {scratch_of(world, '167')}/x && cat {scratch_of(world, '167')}/x && echo WROTE")
    s = json.loads(Path(seat(world, "claude-settings", context(world, "release-reliability", "168"))).read_text())
    assert str(scratch_of(world, "166")) in s["sandbox"]["filesystem"]["denyRead"]
    assert f"Read(/{scratch_of(world, '166')}/**)" in s["permissions"]["deny"]
    assert str(scratch_of(world, "168")) not in s["sandbox"]["filesystem"]["denyRead"]


def test_output_rules(world, codex_home):
    ctx = context(world, "plan-gate", "37", *CLAUDE_ANCHOR)
    seat(world, "codex-pass", ctx, "--home", str(codex_home))
    r = launch(world, ctx)
    assert r.returncode != 0 and "--output" in r.stderr, "a Codex pass names its artifact"
    r = launch(world, ctx, "--output", "trace/logs/x.md")
    assert r.returncode != 0 and "artifacts/ or audits/" in r.stderr
    r = launch(world, ctx, "--output", "artifacts/plan-gate-findings.md")
    argv = json.loads(r.stderr)["argv"]
    assert r.returncode == 0 and argv[argv.index("-o") + 1] == str(world["eng"] / "artifacts" / "plan-gate-findings.md")
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
    ctx = context(world, "security-pass", "44", *CODEX_ANCHOR)
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


# --- an escalated Builder repair: one effort step up, only on the record (SWCB #135) ---------

def failed_gate(w, name, verdict="RELEASE FAIL — QUALITY VERDICT ONLY"):
    (w["eng"] / "audits" / name).write_text(f"---\nseat: release-gate\nverdict: {verdict}\n---\n\n## Findings\n")
    return f"audits/{name}"


def context_fails(w, s, n, *extra):
    r = subprocess.run(["python3", str(SEAT), "context", "--seat", s, "--worktree", str(w["wt"]), "--engagement", str(w["eng"]),
                        "--pass", n, *extra], env=w["env"], capture_output=True, text=True)
    assert r.returncode != 0
    return r.stderr


def test_builder_escalates_to_xhigh_on_a_gate_fail(world, codex_home, fake):
    rec_path = failed_gate(world, "release-gate.md")
    ctx = context(world, "builder", "50", "--effort", "xhigh", "--escalation", rec_path)
    data = json.loads(Path(ctx).read_text())
    assert data["effort"] == "xhigh"
    assert data["escalation"] == {"path": rec_path, "sha256": seatmod.sha256(world["eng"] / rec_path)}
    seat(world, "codex-pass", ctx, "--home", str(codex_home))
    behave(fake, calls=1)
    r = launch(world, ctx, "--output", "artifacts/change-note-50.md", "--run")
    rec = record(world, "50")
    assert r.returncode == 0 and 'model_reasoning_effort="xhigh"' in rec["argv"]
    assert rec["effort"] == "xhigh" and rec["escalation"] == data["escalation"]
    assert rec["runtime_stamps"] == ["gpt-6.1-sol xhigh"]


def test_a_plain_pass_stays_at_high(world):
    data = json.loads(Path(context(world, "builder", "51")).read_text())
    assert data["effort"] == "high" and data["escalation"] is None


def test_an_effort_override_needs_a_record(world):
    assert "--escalation" in context_fails(world, "builder", "52", "--effort", "xhigh")
    assert "--effort" in context_fails(world, "builder", "52", "--escalation", failed_gate(world, "release-gate-r9.md"))


def test_never_ultra_and_never_a_skipped_step(world):
    rec_path = failed_gate(world, "release-gate-r8.md")
    for effort in ("ultra", "max", "high", "low"):
        assert "xhigh" in context_fails(world, "builder", "53", "--effort", effort, "--escalation", rec_path), effort


def test_the_record_must_be_a_failed_gate_or_a_ledger_entry_naming_it(world):
    passed = failed_gate(world, "plan-gate-r9.md", verdict="PLAN PASS — QUALITY VERDICT ONLY")
    assert "FAIL" in context_fails(world, "builder", "54", "--effort", "xhigh", "--escalation", passed)
    loop = failed_gate(world, "audit-change.md", verdict="AUDIT LOOPBACK — 2 material")
    assert "gate findings" in context_fails(world, "builder", "54", "--effort", "xhigh", "--escalation", loop)
    assert "no record" in context_fails(world, "builder", "54", "--effort", "xhigh", "--escalation", "audits/release-gate-r7.md")
    outside = world["root"] / "release-gate.md"
    outside.write_text("---\nverdict: RELEASE FAIL\n---\n")
    assert "engagement" in context_fails(world, "builder", "54", "--effort", "xhigh", "--escalation", str(outside))
    silent = world["eng"] / "d90-one-more-round.md"
    silent.write_text("Sean: one more Builder round.\n")
    assert "does not name" in context_fails(world, "builder", "54", "--effort", "xhigh", "--escalation", silent.name)
    named = world["eng"] / "d91-builder-at-xhigh.md"
    named.write_text("Sean: one more Builder round, one tier up at xhigh.\n")
    data = json.loads(Path(context(world, "builder", "54", "--effort", "xhigh", "--escalation", named.name)).read_text())
    assert data["escalation"]["path"] == named.name


def test_a_gate_never_climbs_and_a_claude_seat_climbs_one_step_at_a_time(world):
    rec_path = failed_gate(world, "plan-gate-r8.md", verdict="PLAN FAIL — QUALITY VERDICT ONLY")
    assert "gate" in context_fails(world, "plan-gate", "55", "--effort", "xhigh", "--escalation", rec_path, *CLAUDE_ANCHOR)
    # Opus 5.5 → Codex high on a gate FAIL; the step on to xhigh takes a ledger entry naming it (SWCB #126)
    assert "ledger entry that names it" in context_fails(world, "build-planner", "55", "--effort", "xhigh", "--escalation", rec_path)


def test_a_record_changed_after_the_context_stops_the_launch(world, codex_home):
    rec_path = failed_gate(world, "security-pass-r9.md", verdict="SECURITY FAIL — QUALITY VERDICT ONLY")
    ctx = context(world, "builder", "56", "--effort", "xhigh", "--escalation", rec_path)
    seat(world, "codex-pass", ctx, "--home", str(codex_home))
    (world["eng"] / rec_path).write_text("---\nverdict: SECURITY FAIL, rewritten\n---\n")
    r = launch(world, ctx, "--output", "artifacts/change-note-56.md")
    assert r.returncode != 0 and "changed since the context" in r.stderr


# --- a pass on the other vendor, read from the record that calls for it (SWCB #126) ----------

def ctx_data(path):
    return json.loads(Path(path).read_text())


@pytest.mark.parametrize("line,writer", [
    ("claude-opus-5-5", "claude"),
    ("claude-opus-5-5             # the runtime that actually ran", "claude"),
    ("codex gpt-6.1-sol high", "codex"),
    ('"codex gpt-6.1-sol high (substitute for xhigh on the security pass FAIL; Sean, d18)"', "codex"),
    ('"claude-opus-5-5 (substitute for the tier-up escalation on plan-gate-r5 FAIL; d07)"', "claude"),
    ('"claude-opus-5-5 → codex gpt-6.1-sol high: plan gate FAIL"', "codex"),
    ('"codex gpt-6.1-sol high -> claude-opus-5-5: fallback"', "claude"),
    ("gpt-6.1-sol", "codex"),
    ("opus", None),
    ("", None),
])
def test_last_writer_reads_the_model_line(line, writer):
    assert seatmod.last_writer(f"---\nid: x\nmodel: {line}\n---\n\nbody\n") == writer


def test_last_writer_needs_a_header():
    assert seatmod.last_writer("model: claude-opus-5-5\n") is None
    assert seatmod.last_writer("---\nid: x\n---\nmodel: claude-opus-5-5\n") is None


def test_the_verifiers_verification_pass_runs_on_codex(world, codex_home, fake):
    # a Planner repair written on Claude is verified on Codex; the brake covers only test-writing passes
    ctx = context(world, "verifier", "60", "--verify", "artifacts/by-claude.md")
    data = ctx_data(ctx)
    assert data["vendor"] == "codex" and data["read_only"] and data["effort"] == "high"
    assert data["vendor_basis"] == {"by": "verify", "path": "artifacts/by-claude.md", "last_writer": "claude",
                                    "sha256": seatmod.sha256(world["eng"] / "artifacts" / "by-claude.md")}
    assert data["caps"] == {"minutes": 20, "tool_calls": 80}, "a read-only Codex pass takes the gates' caps"
    r = subprocess.run(["python3", str(SEAT), "claude-settings", ctx], env=world["env"], capture_output=True, text=True)
    assert r.returncode != 0 and "codex-pass" in r.stderr
    profile = seat(world, "codex-pass", ctx, "--home", str(codex_home))
    layer = (codex_home / f"{profile}.config.toml").read_text()
    assert 'extends = ":read-only"' in layer
    assert f'"{world["eng"] / "held-out"}" = "deny"' not in layer, "held-out is the Verifier's own slice"
    assert "--output" in launch(world, ctx).stderr, "its check record is the final message, filed by -o"
    behave(fake, calls=1, answer="VERIFY RECORD")
    r = launch(world, ctx, "--output", "audits/audit-plan-verify.md", "--run")
    rec = record(world, "60")
    assert r.returncode == 0, r.stderr
    assert rec["vendor"] == "codex" and rec["model"] == "gpt-6.1-sol" and rec["vendor_basis"]["by"] == "verify"
    assert rec["argv"][:2] == ["codex", "exec"] and rec["runtime_stamps"] == ["gpt-6.1-sol high"]
    assert (world["eng"] / "audits" / "audit-plan-verify.md").read_text() == "VERIFY RECORD\n"


def test_releases_verification_pass_never_reads_held_out(world, codex_home):
    ctx = context(world, "release-reliability", "61", "--verify", "artifacts/by-claude.md")
    assert ctx_data(ctx)["vendor"] == "codex"
    profile = seat(world, "codex-pass", ctx, "--home", str(codex_home))
    layer = (codex_home / f"{profile}.config.toml").read_text()
    assert f'"{world["eng"] / "held-out"}" = "deny"' in layer and 'extends = ":read-only"' in layer


def test_a_verification_of_a_codex_repair_runs_on_claude(world):
    # the Builder verifying a Release repair that was written on Codex
    ctx = context(world, "builder", "62", "--verify", "artifacts/by-codex.md")
    data = ctx_data(ctx)
    assert data["vendor"] == "claude" and data["read_only"] and data["effort"] == ""
    assert data["caps"] == {"minutes": 30, "budget_usd": 15}, "a Claude pass takes the Claude seats' caps"
    s = json.loads(Path(seat(world, "claude-settings", ctx)).read_text())
    assert f"Edit(/{world['wt']}/**)" in s["permissions"]["deny"]
    assert str(world["eng"] / "held-out") in s["sandbox"]["filesystem"]["denyRead"]
    argv = json.loads(launch(world, ctx, "--output", "audits/audit-release-verify.md").stderr)["argv"]
    assert argv[0] == "claude" and argv[argv.index("--tools") + 1] == "Read,Write,Bash,Glob,Grep,Skill", "Write for scratch only"
    assert argv[argv.index("--model") + 1] == "claude-opus-5-5" and argv[argv.index("--max-budget-usd") + 1] == "15"


def test_a_verification_on_its_own_vendor_stays_put(world):
    data = ctx_data(context(world, "build-planner", "63", "--verify", "artifacts/by-codex.md"))
    assert data["vendor"] == "claude" and data["read_only"] and data["caps"] == {"minutes": 30, "budget_usd": 15}


def test_every_gate_names_its_anchor(world):
    for g in ("plan-gate", "release-gate", "security-pass"):
        assert "--anchor" in context_fails(world, g, "64")
    assert "--anchor" in context_fails(world, "plan-gate", "64", "--verify", "artifacts/by-claude.md")
    assert "--anchor is a gate's" in context_fails(world, "verifier", "64", *CLAUDE_ANCHOR)


def test_a_gate_runs_on_the_vendor_that_did_not_last_write_its_anchor(world):
    g = ctx_data(context(world, "release-gate", "65", *CLAUDE_ANCHOR, "--candidate", "HEAD"))
    assert g["vendor"] == "codex" and g["vendor_basis"]["last_writer"] == "claude" and g["caps"] == {"minutes": 20, "tool_calls": 80}
    s = ctx_data(context(world, "security-pass", "66", *CODEX_ANCHOR))
    assert s["vendor"] == "claude" and s["caps"] == {"minutes": 30, "budget_usd": 15}
    moved = ctx_data(context(world, "security-pass", "67", *CLAUDE_ANCHOR))
    assert moved["vendor"] == "codex" and moved["effort"] == "high" and moved["caps"] == {"minutes": 20, "tool_calls": 80}


def test_a_moved_plan_gate_runs_on_opus_read_only(world, fake):
    # the Planner redrafted on Codex after a FAIL, so the plan gate moves to Claude
    (world["eng"] / "artifacts" / "plan-r2.md").write_text(
        '---\nmodel: "claude-opus-5-5 → codex gpt-6.1-sol high: plan gate FAIL"\n---\n\nplan\n')
    ctx = context(world, "plan-gate", "68", "--anchor", "artifacts/plan-r2.md")
    data = ctx_data(ctx)
    assert data["vendor"] == "claude" and data["read_only"] and data["caps"] == {"minutes": 30, "budget_usd": 15}
    s = json.loads(Path(seat(world, "claude-settings", ctx)).read_text())
    assert f"Edit(/{world['wt']}/**)" in s["permissions"]["deny"]
    behave(fake, calls=1, answer="PLAN GATE FINDINGS")
    r = launch(world, ctx, "--output", "audits/plan-gate-r2.md", "--run")
    rec = record(world, "68")
    assert r.returncode == 0, r.stderr
    assert rec["vendor"] == "claude" and rec["model"] == "claude-opus-5-5" and rec["argv"][0] == "claude"
    assert rec["vendor_basis"]["last_writer"] == "codex" and rec["effort"] == ""
    assert (world["eng"] / "audits" / "plan-gate-r2.md").read_text() == "PLAN GATE FINDINGS\n"


def test_a_fallback_keeps_the_writers_vendor_and_names_its_ticket(world):
    link = "https://github.com/seanwinslow28/SWCB/issues/999"
    data = ctx_data(context(world, "plan-gate", "69", *CLAUDE_ANCHOR, "--fallback", link))
    assert data["vendor"] == "claude" and data["vendor_basis"]["fallback"] == link
    v = ctx_data(context(world, "verifier", "70", "--verify", "artifacts/by-claude.md", "--fallback", link))
    assert v["vendor"] == "claude" and v["read_only"]
    assert "issue link" in context_fails(world, "plan-gate", "71", *CLAUDE_ANCHOR, "--fallback", "Codex is down")
    assert "--fallback is for" in context_fails(world, "build-planner", "71", "--fallback", link)


def test_the_record_must_be_an_artifact_whose_writer_can_be_read(world):
    assert "artifacts/ or inherited/" in context_fails(world, "plan-gate", "72", "--anchor", failed_gate(world, "plan-gate-r6.md"))
    assert "no record" in context_fails(world, "verifier", "72", "--verify", "artifacts/missing.md")
    (world["eng"] / "artifacts" / "unsigned.md").write_text("---\nid: x\nmodel: some model\n---\n")
    assert "cannot tell who last wrote" in context_fails(world, "plan-gate", "72", "--anchor", "artifacts/unsigned.md")
    inherited = world["eng"] / "inherited"
    inherited.mkdir(exist_ok=True)
    (inherited / "plan.md").write_text("---\nmodel: claude-opus-5-5\n---\n")
    assert ctx_data(context(world, "plan-gate", "73", "--anchor", "inherited/plan.md"))["vendor"] == "codex"


def test_a_changed_anchor_stops_the_launch(world, codex_home):
    anchor = world["eng"] / "artifacts" / "release-plan-74.md"
    anchor.write_text("---\nmodel: claude-opus-5-5\n---\n\nplan\n")
    ctx = context(world, "release-gate", "74", "--anchor", "artifacts/release-plan-74.md", "--candidate", "HEAD")
    seat(world, "codex-pass", ctx, "--home", str(codex_home))
    anchor.write_text("---\nmodel: claude-opus-5-5\n---\n\nplan, edited\n")
    r = launch(world, ctx, "--output", "audits/release-gate-74.md")
    assert r.returncode != 0 and "changed since the context" in r.stderr


def test_a_planner_redraft_one_tier_up_runs_on_codex(world, codex_home, fake):
    fail = failed_gate(world, "plan-gate-r5.md", verdict="PLAN FAIL — QUALITY VERDICT ONLY")
    ctx = context(world, "build-planner", "75", "--escalation", fail)
    data = ctx_data(ctx)
    assert data["vendor"] == "codex" and data["effort"] == "high" and not data["read_only"]
    assert data["vendor_basis"]["by"] == "escalation" and data["escalation"]["path"] == fail
    assert data["caps"] == {"minutes": 60, "tool_calls": 200}, "a redraft on Codex takes the Builder's caps"
    profile = seat(world, "codex-pass", ctx, "--home", str(codex_home))
    assert 'extends = ":read-only"' in (codex_home / f"{profile}.config.toml").read_text(), "the Planner never writes the worktree"
    behave(fake, calls=1, answer="PLAN r2")
    r = launch(world, ctx, "--output", "artifacts/build-plan-r2.md", "--run")
    rec = record(world, "75")
    assert r.returncode == 0, r.stderr
    assert rec["model"] == "gpt-6.1-sol" and 'model_reasoning_effort="high"' in rec["argv"]
    assert (world["eng"] / "artifacts" / "build-plan-r2.md").read_text() == "PLAN r2\n"


def test_a_claude_seats_second_step_takes_a_ledger_entry_naming_xhigh(world):
    vague = world["eng"] / "d92-planner-up-again.md"
    vague.write_text("Sean: the Planner goes up one more tier.\n")
    assert "does not name the xhigh step" in context_fails(world, "build-planner", "76", "--effort", "xhigh", "--escalation", vague.name)
    assert "does not name the Codex step" in context_fails(world, "build-planner", "76", "--escalation", vague.name)
    named = world["eng"] / "d93-planner-xhigh.md"
    named.write_text("Sean: the Planner's next redraft runs on Codex at xhigh.\n")
    data = ctx_data(context(world, "build-planner", "76", "--effort", "xhigh", "--escalation", named.name))
    assert data["vendor"] == "codex" and data["effort"] == "xhigh"


def test_the_verifier_never_escalates_onto_codex(world):
    fail = failed_gate(world, "release-gate-r6.md")
    assert "never escalates onto Codex" in context_fails(world, "verifier", "77", "--escalation", fail)
    assert "do not go together" in context_fails(world, "release-reliability", "77", "--escalation", fail,
                                                  "--verify", "artifacts/by-claude.md")
    assert "no budget flag" in context_fails(world, "build-planner", "77", "--escalation", fail, "--cap-budget-usd", "5")


def test_the_guard_reads_the_vendor_the_pass_runs_on(world):
    fail = failed_gate(world, "release-gate-r5.md")
    rel = seatmod.load(context(world, "release-reliability", "78", "--escalation", fail, "--ops-path", "deploy/"))
    art = str(world["eng"] / "artifacts" / "release-plan.md")
    assert "filed by -o" in rel.write_verdict(art, creating=True), "a Codex pass never writes the engagement folder"
    assert rel.write_verdict(str(world["wt"] / "deploy" / "x")) is None
    assert "not one of Release's" in rel.write_verdict(str(world["wt"] / "src" / "app.py"))
    own = seatmod.load(context(world, "release-reliability", "79", "--ops-path", "deploy/"))
    assert own.vendor == "claude" and own.write_verdict(art, creating=True) is None
    old = dict(ctx_data(context(world, "builder", "80")))
    old.pop("vendor")
    assert seatmod.policy.Context(old).vendor == "codex", "a context from before #126 runs on its seat's vendor"


RELEASE_MATRIX = [
    ("echo a > deploy/x && echo WROTE", True),
    ("echo a > src/app.py && echo WROTE", False),
    ("echo a > src/new.py && echo WROTE", False),
    ("echo a > tests/x.py && echo WROTE", False),
    ("echo a > .github/workflows/x.yml && echo WROTE", False),
    ("echo a > {ENG}/artifacts/x && echo WROTE", False),
    ("cat {ENG}/held-out/h.py && echo WROTE", False),
    ("cat src/app.py && echo WROTE", True),
]


@pytest.mark.skipif(not CODEX, reason="codex not installed")
@pytest.mark.parametrize("cmd,allowed", RELEASE_MATRIX, ids=[c for c, _ in RELEASE_MATRIX])
def test_releases_redraft_on_codex_writes_only_its_ops_paths(world, codex_home, cmd, allowed):
    profile_file = codex_home / f"{world['eng'].name}-pass-81.config.toml"
    if not profile_file.exists():
        fail = failed_gate(world, "release-gate-r4.md")
        seat(world, "codex-pass", context(world, "release-reliability", "81", "--escalation", fail, "--ops-path", "deploy/"),
             "--home", str(codex_home))
    cmd = cmd.replace("{ENG}", str(world["eng"]))
    assert sandboxed(world, codex_home, profile_file.stem.replace(".config", ""), "pass-81", cmd) is allowed


@pytest.mark.skipif(not CODEX, reason="codex not installed")
def test_the_verifiers_codex_layer_in_the_real_sandbox(world, codex_home):
    ctx = context(world, "verifier", "82", "--verify", "artifacts/by-claude.md")
    seat(world, "codex-pass", ctx, "--home", str(codex_home))
    profile = f"{world['eng'].name}-pass-82"
    assert not sandboxed(world, codex_home, profile, "pass-82", "echo a > tests/test_a.py && echo WROTE"), "it changes no test"
    assert not sandboxed(world, codex_home, profile, "pass-82", "echo a > {}/audits/x.md && echo WROTE".format(world["eng"]))
    assert sandboxed(world, codex_home, profile, "pass-82", "cat {}/held-out/h.py && echo WROTE".format(world["eng"]))
    assert not sandboxed(world, codex_home, profile, "pass-82", "cat {}/src/x.py && echo WROTE".format(world["emp"]))


# --- the release gate launches only on its evidence at the candidate (SWCB #150) -------------

FAKE_TOOL = '''#!/usr/bin/env python3
import sys
if sys.argv[1:] == ["--version"]:
    print("faketool version 9.9.9")
    sys.exit(0)
print("scanned: " + " ".join(sys.argv[1:]))
sys.exit(int(sys.argv[1]) if sys.argv[1:] and sys.argv[1].isdigit() else 0)
'''


@pytest.fixture(scope="module")
def tool(world):
    t = world["root"] / "tools" / "faketool"
    t.parent.mkdir()
    t.write_text(FAKE_TOOL)
    t.chmod(0o755)
    return t


def head(w):
    return subprocess.run(["git", "-C", str(w["wt"]), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()


def gate_engagement(w, name, plan="---\nmodel: claude-opus-5-5\n---\n\nA release plan.\n"):
    """A fresh engagement folder per test, so no test's evidence counts for another's gate."""
    eng = w["root"] / name
    for d in ("artifacts", "audits", "trace/logs", "evidence"):
        (eng / d).mkdir(parents=True)
    (eng / "artifacts" / "release-plan.md").write_text(plan)
    return eng


def gate_context(w, eng, n, *extra):
    return seat(w, "context", "--seat", "release-gate", "--worktree", str(w["wt"]), "--engagement", str(eng), "--pass", n,
                "--branch", "devcraft/dc-eng-900", "--anchor", "artifacts/release-plan.md", *extra)


def record_check(w, ctx, check, *argv):
    return subprocess.run(["python3", str(SEAT), "record", ctx, "--check", check, "--", *argv],
                          env=w["env"], capture_output=True, text=True)


def diffcheck_report(cand, exit_code=0, mode="online (registry lookups over the network)", at=None):
    """The diff check's report as diffcheck.py writes it since SWCB #146, cut to the lines the launcher reads."""
    verdict = "DIFF CHECK CLEAN — 0 hit(s), every one on the record" if exit_code == 0 else \
        "DIFF CHECK FINDINGS — 2 unmatched hit(s), 0 check(s) that could not run"
    return "\n".join([
        "# Diff check — dc-eng-9xx", "", "run: 2026-10-15T12:00:00Z", f"candidate: {at or cand}", "commits: 1", "",
        "## Invocation", "", "command: /usr/bin/python3 /x/devcraft/diffcheck/diffcheck.py --worktree /wt --engagement /eng",
        "cwd: /x", "interpreter: /usr/bin/python3 (Python 3.9.6)", "checker: /x/diffcheck.py (sha256 ab)",
        f"worktree HEAD: {at or cand} (the candidate)", "worktree status: clean", f"mode: {mode}",
        f"process exit: {exit_code}", "", "## Hits", "", "none", "", "## Verdict", "", verdict, "",
        "Exit 0 clean, 1 findings for the release gate, 2 refused (the push fails).", f"exit: {exit_code}", ""])


def test_a_release_gate_names_its_candidate(world):
    eng = gate_engagement(world, "dc-eng-910-cand")
    r = subprocess.run(["python3", str(SEAT), "context", "--seat", "release-gate", "--worktree", str(world["wt"]),
                        "--engagement", str(eng), "--pass", "01", "--anchor", "artifacts/release-plan.md"],
                       env=world["env"], capture_output=True, text=True)
    assert r.returncode != 0 and "--candidate" in r.stderr
    assert "not a commit" in subprocess.run(
        ["python3", str(SEAT), "context", "--seat", "release-gate", "--worktree", str(world["wt"]), "--engagement", str(eng),
         "--pass", "01", "--anchor", "artifacts/release-plan.md", "--candidate", "no-such-rev"],
        env=world["env"], capture_output=True, text=True).stderr
    assert "release gate's" in context_fails(world, "builder", "93", "--candidate", "HEAD")
    data = ctx_data(gate_context(world, eng, "01", "--candidate", "HEAD"))
    assert data["candidate"] == head(world)


def test_record_files_a_check_with_its_full_invocation(world, tool):
    eng = gate_engagement(world, "dc-eng-911-rec")
    ctx = gate_context(world, eng, "01", "--candidate", "HEAD")
    cand = head(world)
    r = record_check(world, ctx, "secrets", str(tool), "1", "--log-opts", f"base..{cand}")
    assert r.returncode == 0, r.stderr
    out = json.loads(r.stdout)
    f = eng / "evidence" / f"secrets-{cand[:7]}.txt"
    assert out["path"] == f"evidence/secrets-{cand[:7]}.txt" and out["sha256"] == seatmod.sha256(f) and out["exit"] == 1
    text = f.read_text()
    for line in ("check: secrets", f"candidate: {cand}", f"cwd: {world['wt']}",
                 f"command: {tool} 1 --log-opts base..{cand}", f"tool: {tool} (faketool version 9.9.9)",
                 "interpreter: /usr/bin/env python3", f"worktree HEAD: {cand} (the candidate)", "exit: 1",
                 f"scanned: 1 --log-opts base..{cand}"):
        assert line in text.splitlines(), line
    again = json.loads(record_check(world, ctx, "secrets", str(tool)).stdout)
    assert again["path"] == f"evidence/secrets-{cand[:7]}-2.txt", "evidence is append-only"


def test_record_refuses_what_it_cannot_record_at_the_candidate(world, tool):
    eng = gate_engagement(world, "dc-eng-912-rec")
    ctx = gate_context(world, eng, "01", "--candidate", "HEAD")
    assert "full path" in record_check(world, ctx, "secrets", "faketool").stderr
    assert "invalid choice" in record_check(world, ctx, "lint", str(tool)).stderr
    builder = context(world, "builder", "94")
    assert "the gate's context" in record_check(world, builder, "secrets", str(tool)).stderr
    # a candidate the worktree is not at: a commit beside HEAD, made without checking it out
    other = subprocess.run(["git", "-C", str(world["wt"]), "commit-tree", "HEAD^{tree}", "-p", "HEAD", "-m", "side"],
                           env=world["env"], capture_output=True, text=True, check=True).stdout.strip()
    off = gate_context(world, eng, "02", "--candidate", other)
    r = record_check(world, off, "deps", str(tool))
    assert r.returncode != 0 and "not the candidate" in r.stderr
    assert not list((eng / "evidence").iterdir())


def test_the_release_gate_does_not_launch_without_its_evidence(world, codex_home, tool, fake):
    eng = gate_engagement(world, "dc-eng-913-gate")
    ctx = gate_context(world, eng, "01", "--candidate", "HEAD")
    seat(world, "codex-pass", ctx, "--home", str(codex_home))
    cand, short = head(world), head(world)[:7]
    r = launch(world, ctx, "--output", "audits/release-gate.md")
    assert r.returncode == seatmod.EVIDENCE_EXIT == 4
    for gap in (f"drill-{short}.txt", f"secrets-{short}.txt", f"deps-{short}.txt", f"diff-check-{short}.txt"):
        assert gap in r.stderr, gap
    # a hand-written record with no invocation does not count
    (eng / "evidence" / f"secrets-{short}.txt").write_text(f"$ /opt/homebrew/bin/gitleaks git\nno leaks found\nexit=0\n")
    assert "no full invocation" in launch(world, ctx, "--output", "audits/release-gate.md").stderr
    (eng / "evidence" / f"drill-{short}.txt").write_text(f"coordinator drill at {cand}\nall steps held\n")
    record_check(world, ctx, "secrets", str(tool), "1")  # leaks found are the gate's finding, not a refusal
    record_check(world, ctx, "deps", str(tool))
    (eng / "evidence" / f"diff-check-{short}.txt").write_text(diffcheck_report(cand, exit_code=1))
    r = launch(world, ctx, "--output", "audits/release-gate.md")
    assert r.returncode == 4 and "unmatched" in r.stderr and "secrets" not in r.stderr and "drill" not in r.stderr
    (eng / "evidence" / f"diff-check-{short}-2.txt").write_text(diffcheck_report(cand))
    behave(fake, calls=1, answer="RELEASE GATE FINDINGS")
    r = launch(world, ctx, "--output", "audits/release-gate.md", "--run")
    assert r.returncode == 0, r.stderr
    rec = json.loads((eng / "trace" / "logs" / "pass-01.launch.json").read_text())
    assert [e["path"] for e in rec["evidence"]] == [f"evidence/drill-{short}.txt", f"evidence/secrets-{short}-2.txt",
                                                    f"evidence/deps-{short}.txt", f"evidence/diff-check-{short}-2.txt"]
    assert all(e["sha256"] == seatmod.sha256(eng / e["path"]) for e in rec["evidence"])


def test_a_diff_check_report_counts_only_clean_at_the_candidate(world, codex_home, tool):
    eng = gate_engagement(world, "dc-eng-914-dc")
    ctx = gate_context(world, eng, "01", "--candidate", "HEAD")
    seat(world, "codex-pass", ctx, "--home", str(codex_home))
    cand, short = head(world), head(world)[:7]
    (eng / "evidence" / f"drill-{short}.txt").write_text(f"drill at {cand}\n")
    record_check(world, ctx, "secrets", str(tool))
    record_check(world, ctx, "deps", str(tool))
    report = eng / "evidence" / f"diff-check-{short}.txt"
    for text, why in ((diffcheck_report(cand, mode="fixture (registry lookups answered from x; no network)"), "fixture"),
                      (diffcheck_report(cand, at="f" * 40), "not the candidate"),
                      ("# Diff check\n\ncandidate: " + cand + "\n\n## Verdict\n\nexit: 0\n", "no full invocation")):
        report.write_text(text)
        r = launch(world, ctx, "--output", "audits/release-gate.md")
        assert r.returncode == 4 and why in r.stderr, (why, r.stderr)
    report.write_text(diffcheck_report(cand))
    assert launch(world, ctx, "--output", "audits/release-gate.md").returncode == 0
    # the newest report at the candidate is the one that counts
    (eng / "evidence" / f"diff-check-{short}-2.txt").write_text(diffcheck_report(cand, exit_code=1))
    assert launch(world, ctx, "--output", "audits/release-gate.md").returncode == 4


def test_the_drill_is_the_one_the_release_plan_names(world, codex_home, tool):
    cand = head(world)
    plan = "---\nmodel: claude-opus-5-5\n---\n\n**Commands and output:** `evidence/drill-r2.txt` (sha256 `{}`), quoted here.\n"
    eng = gate_engagement(world, "dc-eng-915-drill", plan=plan.format("0" * 64))
    ctx = gate_context(world, eng, "01", "--candidate", "HEAD")
    seat(world, "codex-pass", ctx, "--home", str(codex_home))
    record_check(world, ctx, "secrets", str(tool))
    record_check(world, ctx, "deps", str(tool))
    (eng / "evidence" / f"diff-check-{cand[:7]}.txt").write_text(diffcheck_report(cand))
    (eng / "evidence" / f"drill-{cand[:7]}.txt").write_text(f"drill at {cand}\n")
    r = launch(world, ctx, "--output", "audits/release-gate.md")
    assert r.returncode == 4 and "evidence/drill-r2.txt" in r.stderr, "the plan's name wins over the default"
    drill = eng / "evidence" / "drill-r2.txt"
    drill.write_text("drill at some other commit\n")
    assert "does not name the candidate" in launch(world, ctx, "--output", "audits/release-gate.md").stderr
    drill.write_text(f"drill at {cand}\n")
    assert "hashed" in launch(world, ctx, "--output", "audits/release-gate.md").stderr
    eng2 = gate_engagement(world, "dc-eng-916-drill", plan=plan.format(seatmod.sha256(drill)))
    for p in (eng / "evidence").iterdir():
        shutil.copy(p, eng2 / "evidence" / p.name)
    ctx2 = gate_context(world, eng2, "01", "--candidate", "HEAD")
    seat(world, "codex-pass", ctx2, "--home", str(codex_home))
    r = launch(world, ctx2, "--output", "audits/release-gate.md")
    assert r.returncode == 0, r.stderr


def test_a_release_gate_context_with_no_candidate_does_not_launch(world, codex_home):
    eng = gate_engagement(world, "dc-eng-917-old")
    ctx = Path(gate_context(world, eng, "01", "--candidate", "HEAD"))
    data = json.loads(ctx.read_text())
    del data["candidate"]  # a context written before SWCB #150
    ctx.write_text(json.dumps(data))
    seat(world, "codex-pass", str(ctx), "--home", str(codex_home))
    r = launch(world, str(ctx), "--output", "audits/release-gate.md")
    assert r.returncode == 4 and "names no candidate" in r.stderr
