"""Tests for the checks git runs before each commit. Run: uvx --from pytest pytest craftwork/checks

Each test builds a throwaway git repo and a made-up name list, so no real
private name and no real secret ever appears in this file.
"""
from __future__ import annotations

import os
import random
import shutil
import string
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
NAMES = ROOT / "craftwork" / "checks" / "private-names.sh"
SECRETS = ROOT / "craftwork" / "checks" / "secrets.sh"
FAKE_NAME = "Quorbltex"          # made up; stands in for a private name
FAKE_TWO_WORDS = "Vantro Plex"   # a name with a space in it

needs_scanner = pytest.mark.skipif(
    not (shutil.which("betterleaks") or shutil.which("gitleaks")),
    reason="neither Betterleaks nor Gitleaks is installed",
)
needs_prek = pytest.mark.skipif(not shutil.which("prek"), reason="prek isn't installed")


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=check)


@pytest.fixture
def repo(tmp_path: Path, monkeypatch) -> Path:
    r = tmp_path / "repo"
    r.mkdir()
    git(r, "init", "-q")
    git(r, "config", "user.email", "test@example.com")
    git(r, "config", "user.name", "Test")
    names = tmp_path / "names"
    names.write_text(f"# private list\n\n{FAKE_NAME}\n{FAKE_TWO_WORDS}\n")
    monkeypatch.setenv("STUDIOS_PRIVATE_NAMES", str(names))
    return r


def stage(repo: Path, path: str, text: str) -> None:
    f = repo / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(text)
    git(repo, "add", path)


def run(script: Path, repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["sh", str(script), *args], cwd=repo, capture_output=True, text=True)


def fake_token() -> str:
    # Built at run time so this file holds no secret-shaped text.
    body = "".join(random.choices(string.ascii_letters + string.digits, k=36))
    return "gh" + "p_" + body


# ---- private names ----------------------------------------------------------

def test_clean_staged_text_passes(repo):
    stage(repo, "notes.md", "A plain page about scripts.\n")
    assert run(NAMES, repo, "staged").returncode == 0


def test_a_name_in_staged_text_is_stopped_and_never_printed(repo):
    stage(repo, "docs/page.md", "line one\nmade at quorbltex last year\n")
    r = run(NAMES, repo, "staged")
    assert r.returncode == 1
    assert "docs/page.md:2" in r.stderr
    assert FAKE_NAME.lower() not in (r.stdout + r.stderr).lower()


def test_a_two_word_name_is_found(repo):
    stage(repo, "a.md", "see VANTRO PLEX for that\n")
    assert run(NAMES, repo, "staged").returncode == 1


def test_only_whole_words_count(repo):
    stage(repo, "a.md", "xquorbltexy is a different word\n")
    assert run(NAMES, repo, "staged").returncode == 0


def test_a_name_in_a_file_path_is_stopped_and_never_printed(repo):
    stage(repo, f"{FAKE_NAME}/plan.md", "nothing private in here\n")
    r = run(NAMES, repo, "staged")
    assert r.returncode == 1
    assert FAKE_NAME.lower() not in (r.stdout + r.stderr).lower()


def test_a_path_with_spaces_is_checked(repo):
    stage(repo, "my notes/a page.md", f"hello {FAKE_NAME}\n")
    r = run(NAMES, repo, "staged")
    assert r.returncode == 1
    assert "my notes/a page.md:1" in r.stderr


def test_a_name_in_the_commit_message_is_stopped(repo, tmp_path):
    msg = tmp_path / "MSG"
    msg.write_text(f"Fix the build\n\nAs asked at {FAKE_NAME}.\n")
    r = run(NAMES, repo, "message", str(msg))
    assert r.returncode == 1
    assert "line(s): 3" in r.stderr
    assert FAKE_NAME.lower() not in r.stderr.lower()


def test_a_name_on_a_hash_line_is_stopped(repo, tmp_path):
    # git commit -m keeps lines that start with #, so they count.
    msg = tmp_path / "MSG"
    msg.write_text(f"Fix the build\n# {FAKE_NAME} kept by git commit -m\n")
    assert run(NAMES, repo, "message", str(msg)).returncode == 1


def test_the_diff_below_the_scissors_line_is_ignored(repo, tmp_path):
    msg = tmp_path / "MSG"
    cut = "# " + "-" * 24 + " >8 " + "-" * 24
    msg.write_text(f"Fix the build\n{cut}\n-old line with {FAKE_NAME}\n")
    assert run(NAMES, repo, "message", str(msg)).returncode == 0


def test_a_path_that_looks_like_pathspec_magic_is_still_checked(repo):
    stage(repo, ":(exclude)a.md", f"hello {FAKE_NAME}\n")
    assert run(NAMES, repo, "staged").returncode == 1


def test_a_missing_list_fails_rather_than_passing(repo, monkeypatch, tmp_path):
    monkeypatch.setenv("STUDIOS_PRIVATE_NAMES", str(tmp_path / "nowhere"))
    stage(repo, "a.md", "fine\n")
    r = run(NAMES, repo, "staged")
    assert r.returncode == 1
    assert "couldn't run" in r.stderr


def test_an_empty_list_fails_rather_than_passing(repo, monkeypatch, tmp_path):
    empty = tmp_path / "empty"
    empty.write_text("# only a comment\n\n")
    monkeypatch.setenv("STUDIOS_PRIVATE_NAMES", str(empty))
    stage(repo, "a.md", "fine\n")
    assert run(NAMES, repo, "staged").returncode == 1


# ---- secrets ----------------------------------------------------------------

@needs_scanner
def test_clean_staged_change_passes_the_secrets_check(repo):
    stage(repo, "a.py", "print('hello')\n")
    assert run(SECRETS, repo).returncode == 0


@needs_scanner
def test_a_staged_token_is_stopped_and_redacted(repo):
    token = fake_token()
    stage(repo, "config.py", f'TOKEN = "{token}"\n')
    r = run(SECRETS, repo)
    assert r.returncode == 1
    assert "config.py" in r.stdout + r.stderr
    assert token not in r.stdout + r.stderr


@needs_scanner
def test_text_beside_a_staged_token_is_never_printed(repo):
    stage(repo, "config.py", f'TOKEN = "{fake_token()}"  # for {FAKE_NAME}\n')
    r = run(SECRETS, repo)
    assert r.returncode == 1
    assert FAKE_NAME.lower() not in (r.stdout + r.stderr).lower()


def test_no_scanner_fails_rather_than_passing(repo, tmp_path):
    bare = tmp_path / "bin"
    bare.mkdir()
    for tool in ("sh", "git"):
        (bare / tool).symlink_to(shutil.which(tool))
    env = {**os.environ, "PATH": str(bare)}
    r = subprocess.run(["sh", str(SECRETS)], cwd=repo, capture_output=True, text=True, env=env)
    assert r.returncode == 1
    assert "couldn't run" in r.stderr


# ---- the whole thing, through git ---------------------------------------------

@needs_prek
@needs_scanner
def test_git_commit_runs_the_checks(repo):
    for part in (".pre-commit-config.yaml", ".githooks", "craftwork/checks/secrets.sh",
                 "craftwork/checks/private-names.sh"):
        src, dst = ROOT / part, repo / part
        dst.parent.mkdir(parents=True, exist_ok=True)
        (shutil.copytree if src.is_dir() else shutil.copy2)(src, dst)
    git(repo, "config", "core.hooksPath", ".githooks")
    git(repo, "add", ".")
    assert git(repo, "commit", "-q", "-m", "Add the checks", check=False).returncode == 0

    stage(repo, "page.md", f"made with {FAKE_NAME}\n")
    blocked = git(repo, "commit", "-q", "-m", "Add a page", check=False)
    assert blocked.returncode != 0
    assert FAKE_NAME.lower() not in (blocked.stdout + blocked.stderr).lower()

    stage(repo, "page.md", "made with care\n")
    assert git(repo, "commit", "-q", "-m", f"Thanks {FAKE_NAME}", check=False).returncode != 0
    assert git(repo, "commit", "-q", "-m", "Add a page", check=False).returncode == 0


# ---- names joined to other words --------------------------------------------

@pytest.mark.parametrize("text", [
    "see quorbltex_notes.md",
    "QUORBLTEX-api key",
    "the vantro_plex job",
    "(quorbltex)",
])
def test_names_joined_by_underscores_or_dashes_are_caught(repo, text):
    stage(repo, "a.md", text + "\n")
    assert run(NAMES, repo, "staged").returncode == 1


def test_a_name_with_regex_characters_is_matched_literally(repo, monkeypatch, tmp_path):
    names = tmp_path / "special"
    names.write_text("Zy.x+\n")
    monkeypatch.setenv("STUDIOS_PRIVATE_NAMES", str(names))
    stage(repo, "a.md", "zyAxx is fine\n")
    assert run(NAMES, repo, "staged").returncode == 0
    stage(repo, "a.md", "made at ZY.X+ today\n")
    assert run(NAMES, repo, "staged").returncode == 1


@needs_prek
@needs_scanner
def test_a_token_in_a_file_whose_path_holds_a_name_never_prints_the_name(repo):
    for part in (".pre-commit-config.yaml", ".githooks", "craftwork/checks/secrets.sh",
                 "craftwork/checks/private-names.sh"):
        src, dst = ROOT / part, repo / part
        dst.parent.mkdir(parents=True, exist_ok=True)
        (shutil.copytree if src.is_dir() else shutil.copy2)(src, dst)
    git(repo, "config", "core.hooksPath", ".githooks")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "Add the checks")
    stage(repo, f"{FAKE_NAME}_work/config.py", f'TOKEN = "{fake_token()}"\n')
    r = git(repo, "commit", "-q", "-m", "Add config", check=False)
    assert r.returncode != 0
    assert FAKE_NAME.lower() not in (r.stdout + r.stderr).lower()


def test_a_two_word_name_run_together_is_not_caught(repo):
    stage(repo, "a.md", "vantroplex could be an ordinary word\n")
    assert run(NAMES, repo, "staged").returncode == 0
