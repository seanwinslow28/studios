"""The git hooks' seeded cases, in a throwaway repo with a build worktree.

The hooks are installed exactly as `seat.py worktree` installs them (a
per-worktree `core.hooksPath`), and run through real `git commit`; pre-push is
fed its stdin directly, since a push needs a remote on GitHub.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

HOOKS = Path(__file__).resolve().parents[1]
SEAT = HOOKS / "seat.py"
GITCHECK = HOOKS / "gitcheck.py"
NAME = "Examplecorp"
FAKE_KEY = "ghp_" + "Z9y8X7w6V5u4T3s2R1q0P9o8N7m6L5k4J3i2"


def sh(*args, cwd, env=None, check=True):
    r = subprocess.run(list(args), cwd=cwd, env=env, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise AssertionError(r.stderr)
    return r


@pytest.fixture()
def repo(tmp_path):
    root = Path(os.path.realpath(tmp_path))
    local = root / "local"
    local.mkdir()
    (local / "employer-paths").write_text(str(root / "emp") + "\n")
    (local / "names").write_text(NAME + "\n")
    env = dict(os.environ, DEVCRAFT_LOCAL=str(local), DEVCRAFT_SCRATCH_ROOT=str(root / "scratch"),
               GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
    env.pop("DEVCRAFT_CONTEXT", None)
    main = root / "main"
    main.mkdir()
    sh("git", "init", "-q", "-b", "main", cwd=main)
    (main / ".devcraft").mkdir()
    (main / ".devcraft" / "test-paths").write_text("tests/\n")
    (main / "src").mkdir()
    (main / "tests").mkdir()
    (main / "src" / "app.py").write_text("a\n")
    sh("git", "add", "-A", cwd=main)
    sh("git", "commit", "-qm", "init", cwd=main, env=env)
    wt = root / "wt"
    sh("git", "worktree", "add", "-q", "-b", "devcraft/dc-eng-900", str(wt), cwd=main)
    eng = root / "eng"
    (eng / "trace" / "logs").mkdir(parents=True)
    base = sh("git", "rev-parse", "HEAD", cwd=main).stdout.strip()
    (eng / "brief.md").write_text(f"---\nid: dc-eng-900\nbase: {base}\nbranch: devcraft/dc-eng-900\n---\n")
    sh("python3", str(SEAT), "worktree", str(wt), "--engagement", str(eng), cwd=root, env=env)
    return {"root": root, "main": main, "wt": wt, "eng": eng, "env": env}


def commit(r, path, text, env=None, msg="change"):
    p = r["wt"] / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    sh("git", "add", path, cwd=r["wt"], env=env or r["env"])
    return sh("git", "commit", "-qm", msg, cwd=r["wt"], env=env or r["env"], check=False)


def test_hooks_are_this_worktrees_only(repo):
    got = sh("git", "config", "--get", "core.hooksPath", cwd=repo["wt"]).stdout.strip()
    assert got == str(HOOKS / "git")
    assert sh("git", "config", "--get", "core.hooksPath", cwd=repo["main"], check=False).stdout.strip() == ""


def test_clean_commit_passes(repo):
    assert commit(repo, "src/b.py", "ok\n").returncode == 0


def test_secret_is_refused(repo):
    r = commit(repo, "src/c.py", f'TOKEN = "{FAKE_KEY}"\n')
    assert r.returncode != 0 and "secret" in r.stderr


def test_name_in_change_is_refused_without_printing_it(repo):
    r = commit(repo, "src/d.py", f"# built for {NAME}\n")
    assert r.returncode != 0 and "never-do 11" in r.stderr and NAME not in r.stderr


def test_name_in_message_is_refused(repo):
    r = commit(repo, "src/e.py", "ok\n", msg=f"fix for {NAME.lower()}")
    assert r.returncode != 0 and "commit message" in r.stderr


def test_missing_name_list_fails_closed(repo):
    (Path(repo["env"]["DEVCRAFT_LOCAL"]) / "names").unlink()
    r = commit(repo, "src/f.py", "ok\n")
    assert r.returncode != 0 and "name list is missing" in r.stderr


def test_seat_commits_only_its_own_paths(repo):
    ctx = repo["eng"] / "trace" / "logs" / "pass-01.context.json"
    sh("python3", str(SEAT), "context", "--seat", "verifier", "--worktree", str(repo["wt"]),
       "--engagement", str(repo["eng"]), "--pass", "01", cwd=repo["root"], env=repo["env"])
    env = dict(repo["env"], DEVCRAFT_CONTEXT=str(ctx))
    assert commit(repo, "tests/test_x.py", "def test(): pass\n", env=env).returncode == 0
    r = commit(repo, "src/g.py", "x\n", env=env)
    assert r.returncode != 0 and "never edits source" in r.stderr


def pre_push(r, url, lines, env=None):
    return subprocess.run(["python3", str(GITCHECK), "pre-push", "origin", url], input="\n".join(lines) + "\n",
                          cwd=r["wt"], env=env or r["env"], capture_output=True, text=True)


def heads(r):
    return sh("git", "rev-parse", "HEAD", cwd=r["wt"]).stdout.strip()


ZERO = "0" * 40
OURS = "https://github.com/seanwinslow28/example.git"


def test_push_build_branch_passes(repo):
    h = heads(repo)
    assert pre_push(repo, OURS, [f"refs/heads/devcraft/dc-eng-900 {h} refs/heads/devcraft/dc-eng-900 {ZERO}"]).returncode == 0


def test_push_to_someone_elses_repo_is_refused(repo):
    h = heads(repo)
    r = pre_push(repo, "git@github.com:someone/else.git", [f"refs/heads/x {h} refs/heads/x {ZERO}"])
    assert r.returncode != 0 and "never-do 1" in r.stderr


def test_push_to_default_branch_is_refused(repo):
    h = heads(repo)
    r = pre_push(repo, OURS, [f"refs/heads/devcraft/dc-eng-900 {h} refs/heads/main {ZERO}"])
    assert r.returncode != 0 and "never-do 3" in r.stderr


def test_branch_delete_is_refused(repo):
    r = pre_push(repo, OURS, [f"(delete) {ZERO} refs/heads/old {heads(repo)}"])
    assert r.returncode != 0 and "never-do 7" in r.stderr


def test_force_push(repo):
    first = heads(repo)
    commit(repo, "src/h.py", "1\n")
    sh("git", "reset", "-q", "--hard", first, cwd=repo["wt"])
    commit(repo, "src/i.py", "2\n")
    rewritten = heads(repo)
    sh("git", "update-ref", "refs/tmp/old", first, cwd=repo["wt"])
    # the remote holds a commit the new head does not contain: a force-push
    old = sh("git", "rev-parse", "HEAD@{2}", cwd=repo["wt"]).stdout.strip()
    own = f"refs/heads/devcraft/dc-eng-900 {rewritten} refs/heads/devcraft/dc-eng-900 {old}"
    other = f"refs/heads/devcraft/dc-eng-900 {rewritten} refs/heads/devcraft/dc-eng-901 {old}"
    assert pre_push(repo, OURS, [own]).returncode == 0
    r = pre_push(repo, OURS, [other])
    assert r.returncode != 0 and "not this build's branch" in r.stderr
    (repo["eng"] / "audits").mkdir()
    (repo["eng"] / "audits" / "release-gate-findings.md").write_text("x")
    r = pre_push(repo, OURS, [own])
    assert r.returncode != 0 and "release gate has run" in r.stderr


def test_seat_never_pushes(repo):
    ctx = repo["eng"] / "trace" / "logs" / "pass-02.context.json"
    sh("python3", str(SEAT), "context", "--seat", "verifier", "--worktree", str(repo["wt"]),
       "--engagement", str(repo["eng"]), "--pass", "02", cwd=repo["root"], env=repo["env"])
    env = dict(repo["env"], DEVCRAFT_CONTEXT=str(ctx))
    h = heads(repo)
    r = pre_push(repo, OURS, [f"refs/heads/devcraft/dc-eng-900 {h} refs/heads/devcraft/dc-eng-900 {ZERO}"], env=env)
    assert r.returncode != 0 and "never pushes" in r.stderr


def test_name_in_pushed_commits_is_refused(repo):
    base = heads(repo)
    env = dict(repo["env"])
    # land a commit with the name past the commit hooks, as an outside clone might
    p = repo["wt"] / "src" / "j.py"
    p.write_text(f"# {NAME}\n")
    sh("git", "add", "src/j.py", cwd=repo["wt"], env=env)
    sh("git", "-c", "core.hooksPath=/dev/null", "commit", "-qm", "j", cwd=repo["wt"], env=env)
    h = heads(repo)
    r = pre_push(repo, OURS, [f"refs/heads/devcraft/dc-eng-900 {h} refs/heads/devcraft/dc-eng-900 {base}"])
    assert r.returncode != 0 and "never-do 11" in r.stderr and NAME not in r.stderr


def test_commit_msg_stamps_the_seat_trailer(repo):
    """The diff check attributes commits by this trailer; a seat cannot claim another seat's."""
    ctx = repo["eng"] / "trace" / "logs" / "pass-02.context.json"
    sh("python3", str(SEAT), "context", "--seat", "verifier", "--worktree", str(repo["wt"]),
       "--engagement", str(repo["eng"]), "--pass", "02", cwd=repo["root"], env=repo["env"])
    env = dict(repo["env"], DEVCRAFT_CONTEXT=str(ctx))
    assert commit(repo, "tests/test_t.py", "def test(): pass\n", env=env, msg="tests: t").returncode == 0
    body = sh("git", "log", "-1", "--format=%B", cwd=repo["wt"]).stdout
    assert body.rstrip().endswith("Devcraft-Seat: verifier")
    r = commit(repo, "tests/test_u.py", "def test(): pass\n", env=env, msg="tests: u\n\nDevcraft-Seat: builder")
    assert r.returncode != 0 and "names a seat other than" in r.stderr
    r = commit(repo, "src/h.py", "x\n", msg="coordinator edit")  # no context: no trailer added, none required
    assert r.returncode == 0 and "Devcraft-Seat" not in sh("git", "log", "-1", "--format=%B", cwd=repo["wt"]).stdout


def test_pre_push_runs_the_diff_check(repo):
    """The pre-push hook refuses a push whose range edits an unnamed control, and lets findings through."""
    assert commit(repo, ".claude/settings.json", "{}\n").returncode == 0
    r = pre_push(repo, OURS, [f"refs/heads/devcraft/dc-eng-900 {heads(repo)} refs/heads/devcraft/dc-eng-900 {ZERO}"])
    assert r.returncode != 0 and "diff check refused" in r.stderr and "REFUSED" in r.stderr
    sh("git", "reset", "-q", "--hard", "HEAD~1", cwd=repo["wt"])
    assert commit(repo, "src/plain.py", "x = 1\n", msg="hand edit").returncode == 0  # no seat: a finding, not a refusal
    r = pre_push(repo, OURS, [f"refs/heads/devcraft/dc-eng-900 {heads(repo)} refs/heads/devcraft/dc-eng-900 {ZERO}"])
    assert r.returncode == 0 and "FINDINGS" in r.stderr
    assert list((repo["eng"] / "evidence").glob("diff-check-*.txt"))
