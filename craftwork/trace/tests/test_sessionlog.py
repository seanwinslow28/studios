"""The coordinator's session pointer (SWCB #169): where Claude Code keeps the running session's transcript."""
import os
import subprocess
import sys
import time
from pathlib import Path

from tracekit.sessionlog import session_log

TRACE = Path(__file__).resolve().parents[1]
SID = "267eadef-0000-4000-8000-000000000001"


def transcript(home: Path, project: str, sid: str = SID) -> Path:
    p = home / ".claude" / "projects" / project / f"{sid}.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text('{"type": "user"}\n', encoding="utf-8")
    return p


def test_the_running_session_is_found_by_its_id(tmp_path, monkeypatch):
    want = transcript(tmp_path, "-Users-sean-Code-Brain-studios")
    transcript(tmp_path, "-Users-sean-Code-Brain-studios", "another-session")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SID)
    assert session_log(home=tmp_path) == want
    assert session_log("another-session", home=tmp_path).name == "another-session.jsonl"


def test_the_newest_copy_wins_when_two_projects_hold_the_id(tmp_path):
    old = transcript(tmp_path, "-old")
    os.utime(old, (time.time() - 60, time.time() - 60))
    new = transcript(tmp_path, "-new")
    assert session_log(SID, home=tmp_path) == new


def test_no_id_or_no_file_is_none(tmp_path, monkeypatch):
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID", raising=False)
    assert session_log(home=tmp_path) is None
    assert session_log(SID, home=tmp_path) is None
    assert session_log("../escape", home=tmp_path) is None


def test_the_command_prints_the_path_or_exits_two(tmp_path):
    want = transcript(tmp_path, "-p")
    env = {**os.environ, "HOME": str(tmp_path), "CLAUDE_CODE_SESSION_ID": SID}
    r = subprocess.run([sys.executable, "sessionlog.py"], capture_output=True, text=True, cwd=TRACE, env=env)
    assert r.returncode == 0 and r.stdout.strip() == str(want)
    r = subprocess.run([sys.executable, "sessionlog.py", "nope"], capture_output=True, text=True, cwd=TRACE, env=env)
    assert r.returncode == 2 and "no session transcript found" in r.stderr
