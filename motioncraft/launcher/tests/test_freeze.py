"""Freezing version folders: the state read by mode bits, the lock, and the sweep over a media project.

SWCB #258: on the first film only the approved copies were ever locked; nine superseded versions
and 40 folders inside four approved copies stayed writable, and the Close checklist, reading only
`approved/`, never saw it. The Codex reviewer added that `os.access` reads zero writable paths from
inside a read-only sandbox, so everything here reads `st_mode`, never asks whether it may write.
"""
from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

import pytest

LAUNCHER = Path(__file__).resolve().parents[1]
FREEZE = LAUNCHER / "freeze.py"
sys.path.insert(0, str(LAUNCHER))
import freeze  # noqa: E402


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def version(where: Path, name: str, files: dict, *, listed: dict = None, extra_lines: str = "") -> Path:
    """A version folder holding `files` (relative path -> text), its checksums covering `listed` (default: all)."""
    v = where / name
    for rel, text in files.items():
        (v / rel).parent.mkdir(parents=True, exist_ok=True)
        (v / rel).write_text(text)
    lines = "".join(f"{sha(text)}  {rel}\n" for rel, text in sorted((listed if listed is not None else files).items()))
    (v / "checksums.sha256").write_text(lines + extra_lines)
    return v


def whole(where: Path, name: str, **more) -> Path:
    return version(where, name, {"pointer.txt": "mc-eng-900", "manifest.md": "---\nversion: x\n---\n", **more})


def mode(p: Path) -> int:
    return stat.S_IMODE(os.lstat(p).st_mode)


@pytest.fixture()
def stage(tmp_path):
    return tmp_path / "motion"


# --- the state of one version, by mode bits -----------------------------------------------

def test_a_whole_version_reads_complete_and_writable(stage):
    v = whole(stage, "motion-v01-2026-10-21", **{"renders/f0001.png": "px", "sources/scene.blend": "blend"})
    st = freeze.state(v)
    assert st["missing"] == [] and st["links"] == []
    assert st["checksums"] == {"listed": 4, "failed": [], "missing": [], "unlisted": []}
    # the folder itself, renders/ and sources/ are writable dirs; every file is writable
    assert st["writable_dirs"] == 3 and st["writable_files"] == 5
    assert freeze.gaps(st) == []


def test_the_three_files_are_read_in_any_case(stage):
    v = version(stage, "animatic-v01-2026-10-20", {"POINTER.txt": "mc-eng-001", "Manifest.md": "m"})
    assert freeze.state(v)["missing"] == []


def test_a_missing_file_is_named(stage):
    v = version(stage, "motion-v02-2026-10-21", {"pointer.txt": "p"})
    assert freeze.state(v)["missing"] == ["manifest.md"]
    assert freeze.gaps(freeze.state(v)) == ["lacks manifest.md"]


def test_no_checksums_file_at_all(stage):
    v = stage / "motion-v03-2026-10-21"
    v.mkdir(parents=True)
    (v / "pointer.txt").write_text("p")
    (v / "manifest.md").write_text("m")
    st = freeze.state(v)
    assert st["missing"] == ["checksums.sha256"] and st["checksums"] is None
    assert freeze.gaps(st) == ["lacks checksums.sha256"]


def test_a_listed_file_that_differs_or_is_gone_fails_the_checksums(stage):
    v = whole(stage, "motion-v04-2026-10-21", **{"renders/a.mp4": "film", "renders/b.mp4": "film2"})
    (v / "renders" / "a.mp4").write_text("re-rendered")
    (v / "renders" / "b.mp4").unlink()
    st = freeze.state(v)
    assert st["checksums"]["failed"] == ["renders/a.mp4"] and st["checksums"]["missing"] == ["renders/b.mp4"]
    assert freeze.gaps(st) == ["checksums.sha256 does not verify (renders/a.mp4 differs; renders/b.mp4 missing)"]


def test_a_file_the_checksums_do_not_list_is_named(stage):
    v = whole(stage, "motion-v05-2026-10-21", **{"renders/a.mp4": "film"})
    (v / ".DS_Store").write_bytes(b"\0" * 8)
    (v / "renders" / "stray.txt").write_text("s")
    st = freeze.state(v)
    assert st["checksums"]["unlisted"] == [".DS_Store", "renders/stray.txt"]
    assert freeze.gaps(st) == ["holds files not in checksums.sha256 (.DS_Store, renders/stray.txt)"]


def test_shasum_binary_marker_and_blank_lines_are_read(stage):
    v = version(stage, "motion-v06-2026-10-21", {"pointer.txt": "p", "manifest.md": "m"}, listed={},
                extra_lines=f"\n{sha('p')} *pointer.txt\n{sha('m')}  manifest.md\n\n")
    assert freeze.state(v)["checksums"] == {"listed": 2, "failed": [], "missing": [], "unlisted": []}


def test_a_link_inside_a_version_is_named_and_is_a_gap(stage):
    v = whole(stage, "motion-v07-2026-10-21")
    (v / "assets").mkdir()
    os.symlink("/etc/hosts", v / "assets" / "hosts")
    st = freeze.state(v)
    assert st["links"] == ["assets/hosts"]
    assert "holds a link (assets/hosts)" in freeze.gaps(st)


# --- the lock -----------------------------------------------------------------------------

def test_lock_clears_every_write_bit_and_reads_none_left(stage):
    v = whole(stage, "motion-v08-2026-10-21", **{"renders/f0001.png": "px", "evidence/pack/frames.txt": "f"})
    res = freeze.lock(v)
    assert res == {"writable_dirs": 0, "writable_files": 0, "errors": []}
    for p in [v, *v.rglob("*")]:
        assert mode(p) & 0o222 == 0, p
    assert mode(v / "renders") == 0o555 and mode(v / "renders" / "f0001.png") == 0o444
    st = freeze.state(v)
    assert st["writable_dirs"] == 0 and st["writable_files"] == 0
    # locking a locked version changes nothing and still reads clean
    assert freeze.lock(v) == {"writable_dirs": 0, "writable_files": 0, "errors": []}


def test_lock_keeps_the_other_bits(stage):
    v = whole(stage, "motion-v09-2026-10-21", **{"sources/run.sh": "#!/bin/sh\n"})
    (v / "sources" / "run.sh").chmod(0o755)
    (v / "pointer.txt").chmod(0o600)
    freeze.lock(v)
    assert mode(v / "sources" / "run.sh") == 0o555 and mode(v / "pointer.txt") == 0o400


def test_lock_does_not_follow_a_link(stage):
    v = whole(stage, "motion-v10-2026-10-21")
    target = stage.parent / "outside.txt"
    target.write_text("outside")
    os.symlink(target, v / "out")
    freeze.lock(v)
    assert mode(target) & 0o222, "the link's target outside the version must keep its write bit"


# --- the sweep over a media project ---------------------------------------------------------

def project(root: Path) -> Path:
    p = root / "media" / "Film" / "proj-2026-10-21"
    for d in ("inputs/fonts", "story", "appearance", "motion", "finish", "approved"):
        (p / d).mkdir(parents=True)
    (p / "inputs" / "fonts" / "a.otf").write_text("font")
    (p / "story" / "notes.txt").write_text("not a version")
    whole(p / "story", "animatic-v01-2026-10-20", **{"renders/a.mp4": "film"})
    whole(p / "appearance", "appearance-v01-2026-10-20")
    v3 = whole(p / "motion", "motion-v03-2026-10-20", **{"renders/f.png": "px"})
    whole(p / "approved", "motion-v03-2026-10-20", **{"renders/f.png": "px"})
    freeze.lock(v3)
    return p


def test_versions_in_lists_every_version_folder_and_nothing_else(tmp_path):
    p = project(tmp_path)
    assert [str(v.relative_to(p)) for v in freeze.versions_in(p)] == [
        "story/animatic-v01-2026-10-20", "appearance/appearance-v01-2026-10-20",
        "motion/motion-v03-2026-10-20", "approved/motion-v03-2026-10-20"]


def run(*args, env=None):
    return subprocess.run([sys.executable, str(FREEZE), *args], capture_output=True, text=True, env=env)


def test_sweep_names_every_writable_version_and_exits_1(tmp_path):
    p = project(tmp_path)
    r = run("sweep", str(p))
    assert r.returncode == 1, r.stdout + r.stderr
    rows = {l.split()[0]: l for l in r.stdout.splitlines() if l.startswith(("story/", "appearance/", "motion/", "finish/", "approved/"))}
    assert set(rows) == {"story/animatic-v01-2026-10-20", "appearance/appearance-v01-2026-10-20",
                         "motion/motion-v03-2026-10-20", "approved/motion-v03-2026-10-20"}
    assert "locked" in rows["motion/motion-v03-2026-10-20"] and "writable" not in rows["motion/motion-v03-2026-10-20"]
    assert "2 dirs, 4 files writable" in rows["story/animatic-v01-2026-10-20"]
    assert "3 of 4 version folders writable" in r.stdout


def test_sweep_as_json(tmp_path):
    p = project(tmp_path)
    r = run("sweep", str(p), "--json")
    rows = json.loads(r.stdout)
    assert [row["version"] for row in rows][2] == "motion/motion-v03-2026-10-20"
    assert rows[2]["writable_dirs"] == 0 and rows[2]["locked"] is True and rows[0]["locked"] is False
    assert rows[0]["checksums"]["listed"] == 3


def test_sweep_exits_0_once_every_version_is_locked_and_verifies(tmp_path):
    p = project(tmp_path)
    for v in freeze.versions_in(p):
        freeze.lock(v)
    r = run("sweep", str(p))
    assert r.returncode == 0, r.stdout
    assert "0 of 4 version folders writable" in r.stdout


def test_sweep_fails_on_checksums_that_do_not_verify_even_when_locked(tmp_path):
    p = project(tmp_path)
    v = p / "appearance" / "appearance-v01-2026-10-20"
    (v / "pointer.txt").write_text("changed after the checksums")
    for x in freeze.versions_in(p):
        freeze.lock(x)
    r = run("sweep", str(p))
    assert r.returncode == 1 and "pointer.txt differs" in r.stdout


def test_sweep_reads_a_media_path_from_the_named_folders(tmp_path):
    p = project(tmp_path)
    (tmp_path / "folders.local").write_text(f"media = {tmp_path / 'media'}\n")
    env = dict(os.environ, TRACEKIT_FOLDERS=str(tmp_path / "folders.local"))
    r = run("sweep", "media:Film/proj-2026-10-21", env=env)
    assert r.returncode == 1 and "story/animatic-v01-2026-10-20" in r.stdout
    r = run("sweep", "media:Film/nowhere", env=env)
    assert r.returncode == 2 and "not a folder" in r.stderr


# --- the lock by hand: approved copies and the versions made before the launcher locked -----

def test_lock_command_locks_every_writable_version_whose_checksums_verify(tmp_path):
    p = project(tmp_path)
    # a version from before the manifest rule: no manifest, checksums clean. It is locked all the same.
    version(p / "finish", "finish-v01-2026-10-20", {"POINTER.txt": "mc-e6", "renders/out.mov": "mov"})
    r = run("lock", str(p))
    assert r.returncode == 0, r.stdout + r.stderr
    for v in freeze.versions_in(p):
        st = freeze.state(v)
        assert st["writable_dirs"] == 0 and st["writable_files"] == 0, v
    assert "finish/finish-v01-2026-10-20" in r.stdout and "lacks manifest.md" in r.stdout
    assert "motion/motion-v03-2026-10-20" in r.stdout and "already locked" in r.stdout


def test_lock_command_refuses_a_version_whose_checksums_fail_and_leaves_it_writable(tmp_path):
    p = project(tmp_path)
    bad = p / "story" / "animatic-v01-2026-10-20"
    (bad / "renders" / "a.mp4").write_text("re-rendered")
    r = run("lock", str(p))
    assert r.returncode == 1
    assert "refused" in r.stdout and "story/animatic-v01-2026-10-20" in r.stdout and "renders/a.mp4 differs" in r.stdout
    assert mode(bad / "renders" / "a.mp4") & 0o222, "a version refused is left as it was"
    assert freeze.state(p / "appearance" / "appearance-v01-2026-10-20")["writable_files"] == 0, "the others are locked"


def test_lock_command_takes_named_versions_only(tmp_path):
    p = project(tmp_path)
    r = run("lock", str(p), "--version", "approved/motion-v03-2026-10-20")
    assert r.returncode == 0, r.stdout + r.stderr
    assert freeze.state(p / "approved" / "motion-v03-2026-10-20")["writable_dirs"] == 0
    assert freeze.state(p / "story" / "animatic-v01-2026-10-20")["writable_dirs"] == 2
    r = run("lock", str(p), "--version", "approved/nothing-v01-2026-10-20")
    assert r.returncode == 2 and "no version folder" in r.stderr
