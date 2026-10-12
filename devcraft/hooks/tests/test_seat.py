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
    env = dict(os.environ, DEVCRAFT_LOCAL=str(local), GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
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
