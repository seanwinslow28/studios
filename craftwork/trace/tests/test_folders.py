"""Named folders set per machine: `media:<path>` in a record, `folders.local` on each machine (SWCB #210, ruled on #186 §§ 7–8)."""
import hashlib
import subprocess
import sys
from pathlib import Path

import pytest

from synth import build
from tracekit.cases import Case, CasesDoc, Source, resolve_sources
from tracekit.checker import run_checks
from tracekit.engagement import load_engagement
from tracekit.folders import NOT_SET_UP, load_folders, read_folders, split_named
from tracekit.viewer import render_html

TRACE = Path(__file__).resolve().parents[1]
HASHES = "Input hashes match disk or a recorded prior revision"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# --------------------------------------------------------------------------- #
# the name and the settings file
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("raw, expected", [
    ("media:Question/idea-seed/appearance-v01", ("media", "Question/idea-seed/appearance-v01")),
    ("target:swcb/tools/x.py", ("target", "swcb/tools/x.py")),
    ("target-swcb:README.md", ("target-swcb", "README.md")),
    ("  media:a.png  ", ("media", "a.png")),
])
def test_a_named_path_splits_into_name_and_path(raw, expected):
    assert split_named(raw) == expected


@pytest.mark.parametrize("raw", [
    "craftwork/law.md",                  # an ordinary repo path
    "artifacts/a:b.md",                  # a colon later in a relative path is not a name
    "https://example.com/page",          # a web address is not a name
    "/Users/someone/Movies/a.png",       # a full path is not a name
    "media:/Users/someone/a.png",        # a named path never carries a full path
    "media:../outside.png",              # ... nor climbs out of its folder
    "media:",                            # ... nor is empty
    "Media:a.png",                       # names are lower case
    "—",
])
def test_anything_else_is_not_a_named_path(raw):
    assert split_named(raw) is None


def test_the_settings_file_maps_names_to_folders(tmp_path):
    f = tmp_path / "folders.local"
    f.write_text(
        "# this machine only, never committed\n"
        "\n"
        "media = ~/Movies/Animation-Studio\n"
        "target-swcb=/Users/someone/Code-Brain/SWCB   # trailing comment\n"
    )
    folders, problems = read_folders(f)
    assert folders == {
        "media": Path.home() / "Movies" / "Animation-Studio",
        "target-swcb": Path("/Users/someone/Code-Brain/SWCB"),
    }
    assert problems == []


def test_a_bad_settings_line_is_reported_and_its_name_stays_unset(tmp_path):
    f = tmp_path / "folders.local"
    f.write_text("media ~/Movies\nrelative = some/folder\nMedia = /x\nok = /y\n")
    folders, problems = read_folders(f)
    assert folders == {"ok": Path("/y")}
    assert len(problems) == 3
    assert all("folders.local line" in p for p in problems)


def test_the_settings_file_is_found_at_the_repo_root(tmp_path, monkeypatch):
    monkeypatch.delenv("TRACEKIT_FOLDERS", raising=False)
    (tmp_path / "folders.local").write_text("media = /m\n")
    assert load_folders(tmp_path).folders == {"media": Path("/m")}
    assert load_folders(None).folders == {}
    assert load_folders(tmp_path / "nowhere").folders == {}


def test_an_environment_variable_names_another_settings_file(tmp_path, monkeypatch):
    (tmp_path / "folders.local").write_text("media = /from-repo\n")
    other = tmp_path / "elsewhere.local"
    other.write_text("media = /from-env\n")
    monkeypatch.setenv("TRACEKIT_FOLDERS", str(other))
    assert load_folders(tmp_path).folders == {"media": Path("/from-env")}


def test_the_example_file_is_tracked_and_holds_no_real_path():
    example = TRACE.parents[1] / "folders.example"
    assert example.is_file()
    folders, problems = read_folders(example)
    assert problems == []
    assert "media" in folders
    assert "seanwinslow" not in example.read_text()


def test_the_real_settings_file_is_ignored_by_git():
    repo = TRACE.parents[1]
    r = subprocess.run(["git", "check-ignore", "-q", "folders.local"], cwd=repo)
    assert r.returncode == 0, "folders.local must be gitignored"


# --------------------------------------------------------------------------- #
# an engagement whose records name the media folder
# --------------------------------------------------------------------------- #


@pytest.fixture
def studio(tmp_path, monkeypatch) -> dict:
    """A repo root holding studio machinery and a settings file; the media folder lives outside it."""
    monkeypatch.delenv("TRACEKIT_FOLDERS", raising=False)
    repo = tmp_path / "studios"
    repo.mkdir()
    (repo / "CLAUDE.md").write_text("# fake repo root\n")
    for d in ("craftwork", "productcraft"):
        (repo / d).mkdir()
    media = tmp_path / "Movies" / "Animation-Studio"
    frame = media / "film" / "appearance" / "appearance-v01" / "frame-001.png"
    frame.parent.mkdir(parents=True)
    frame.write_bytes(b"\x89PNG painted frame")
    (repo / "folders.local").write_text(f"media = {media}\n")
    eng = build(repo / "pc-eng-000-callboard")
    return {"repo": repo, "media": media, "frame": frame, "eng": eng}


def record(eng_dir: Path, pass_id: str) -> Path:
    return next((eng_dir / "trace").glob(f"{pass_id}-*.md"))


def add_input(eng_dir: Path, pass_id: str, rel: str, digest: str) -> None:
    p = record(eng_dir, pass_id)
    p.write_text(p.read_text().replace("inputs:\n", f"inputs:\n  - path: {rel}\n    sha256: {digest}\n", 1))


def add_output(eng_dir: Path, pass_id: str, rel: str, digest: str) -> None:
    p = record(eng_dir, pass_id)
    p.write_text(p.read_text().replace("outputs:\n", f"outputs:\n  - path: {rel}\n    sha256: {digest}\n", 1))


def hashes(eng_dir: Path):
    return {c.name: c for c in run_checks(load_engagement(eng_dir))}[HASHES]


FRAME = "media:film/appearance/appearance-v01/frame-001.png"
VERSION = "media:film/appearance/appearance-v01"


def test_a_named_input_resolves_through_the_settings_file_and_checks(studio):
    add_input(studio["eng"], "pass-03", FRAME, sha(studio["frame"]))
    eng = load_engagement(studio["eng"])
    assert eng.resolve(FRAME) == studio["frame"]
    assert eng.hash_of(FRAME) == sha(studio["frame"])
    c = hashes(studio["eng"])
    assert c.ok, c.findings


def test_a_named_version_folder_hashes_as_a_whole(studio):
    from tracekit.engagement import sha256_path
    folder = studio["frame"].parent
    add_input(studio["eng"], "pass-03", VERSION, sha256_path(folder))
    c = hashes(studio["eng"])
    assert c.ok, c.findings


def test_moving_the_folder_changes_one_line_and_old_records_still_check(studio, tmp_path):
    add_input(studio["eng"], "pass-03", FRAME, sha(studio["frame"]))
    moved = tmp_path / "External" / "Animation-Studio"
    moved.parent.mkdir()
    studio["media"].rename(moved)
    assert not hashes(studio["eng"]).ok                      # the old line points at nothing now
    (studio["repo"] / "folders.local").write_text(f"media = {moved}\n")
    c = hashes(studio["eng"])
    assert c.ok, c.findings


def test_a_name_with_no_mapping_is_not_set_up_never_a_pass(studio):
    add_input(studio["eng"], "pass-03", FRAME, sha(studio["frame"]))
    (studio["repo"] / "folders.local").write_text("# another machine: no media folder here\n")
    eng = load_engagement(studio["eng"])
    assert eng.resolve(FRAME) is None
    assert eng.path_state(FRAME) == NOT_SET_UP
    c = hashes(studio["eng"])
    assert not c.ok
    [finding] = [f for f in c.findings if FRAME in f]
    assert "not set up on this machine" in finding
    assert "missing" not in finding


def test_no_settings_file_at_all_is_not_set_up_too(studio):
    add_input(studio["eng"], "pass-03", FRAME, sha(studio["frame"]))
    (studio["repo"] / "folders.local").unlink()
    c = hashes(studio["eng"])
    assert not c.ok
    assert any("not set up on this machine" in f for f in c.findings)


def test_a_set_up_name_whose_file_is_gone_is_missing_not_unset(studio):
    add_input(studio["eng"], "pass-03", FRAME, sha(studio["frame"]))
    studio["frame"].unlink()
    eng = load_engagement(studio["eng"])
    assert eng.path_state(FRAME) == "missing"
    c = hashes(studio["eng"])
    assert any(FRAME in f and "missing on disk" in f for f in c.findings)
    assert not any("not set up" in f for f in c.findings)


def test_a_named_file_edited_after_the_pass_is_still_a_finding(studio):
    add_input(studio["eng"], "pass-03", FRAME, sha(studio["frame"]))
    studio["frame"].write_bytes(b"repainted outside any pass")
    eng = load_engagement(studio["eng"])
    assert eng.path_state(FRAME) == "present"                 # on disk; whether it matches is the checker's line
    c = hashes(studio["eng"])
    assert any(FRAME in f and "no longer matches disk" in f for f in c.findings)


def test_a_named_output_not_set_up_is_its_own_state(studio):
    add_output(studio["eng"], "pass-03", FRAME, sha(studio["frame"]))
    eng = load_engagement(studio["eng"])
    [o] = [o for o in eng.by_id["pass-03"].outputs if o.path == FRAME]
    assert eng.output_state(o) == "current"
    (studio["repo"] / "folders.local").write_text("")
    eng = load_engagement(studio["eng"])
    [o] = [o for o in eng.by_id["pass-03"].outputs if o.path == FRAME]
    assert eng.output_state(o) == NOT_SET_UP
    c = hashes(studio["eng"])
    assert any(f"output {FRAME}" in f and "not set up on this machine" in f for f in c.findings)


def test_any_name_works_not_only_media(studio, tmp_path):
    target = tmp_path / "Code-Brain" / "SWCB"
    target.mkdir(parents=True)
    (target / "README.md").write_text("the brain\n")
    (studio["repo"] / "folders.local").write_text(f"media = {studio['media']}\ntarget = {target.parent}\n")
    add_input(studio["eng"], "pass-03", "target:SWCB/README.md", sha(target / "README.md"))
    c = hashes(studio["eng"])
    assert c.ok, c.findings


def test_existing_records_check_exactly_as_before(studio):
    """No named path in any record: the settings file changes nothing."""
    with_file = [(c.name, c.ok, c.findings, c.notes) for c in run_checks(load_engagement(studio["eng"]))]
    (studio["repo"] / "folders.local").unlink()
    without = [(c.name, c.ok, c.findings, c.notes) for c in run_checks(load_engagement(studio["eng"]))]
    assert with_file == without
    assert all(ok for _, ok, _, _ in with_file)


def test_a_bad_settings_line_is_a_note_on_the_hash_line(studio):
    (studio["repo"] / "folders.local").write_text(f"media = {studio['media']}\nbroken line\n")
    c = hashes(studio["eng"])
    assert any("folders.local line 2" in n for n in c.notes)


# --------------------------------------------------------------------------- #
# the viewer and the guided-reading cases show it
# --------------------------------------------------------------------------- #


def test_the_viewer_marks_a_path_not_set_up(studio):
    add_input(studio["eng"], "pass-03", FRAME, sha(studio["frame"]))
    add_output(studio["eng"], "pass-03", VERSION + "-out", "0" * 64)
    html = render_html(load_engagement(studio["eng"]), rendered_on="2026-10-18")
    assert "not set up on this machine" not in html
    (studio["repo"] / "folders.local").write_text("")
    html = render_html(load_engagement(studio["eng"]), rendered_on="2026-10-18")
    assert f"<li>{FRAME} <span class='sub unset'>not set up on this machine" in html
    assert f"<li>{VERSION}-out <span class='sub unset'>not set up on this machine" in html


def test_a_case_source_not_set_up_is_qualified_in_its_own_words(studio):
    (studio["repo"] / "folders.local").write_text("")
    doc = CasesDoc(cases=[Case(key="c1", title="t", pass_id="pass-03",
                               sources=[Source(path=FRAME, sha256=sha(studio["frame"]), excerpt="x")])])
    resolve_sources(doc, load_engagement(studio["eng"]))
    s = doc.cases[0].sources[0]
    assert s.state == NOT_SET_UP
    assert s.qualified and not s.shows_excerpt
    assert "not set up on this machine" in s.qualification
    assert any("not set up on this machine" in e for e in doc.errors)


# --------------------------------------------------------------------------- #
# the freeze tool reads named paths too
# --------------------------------------------------------------------------- #

BINDING = "# A binding\n\n```strip\nheading: ## Moves\n```\n"
ARTIFACT = "---\nid: x\n---\n\n# Story packet\n\nkept\n\n## Moves\n\n- kept: A\n"


def freeze_cli(*args, env_file: Path) -> subprocess.CompletedProcess:
    import os
    env = {**os.environ, "TRACEKIT_FOLDERS": str(env_file)}
    return subprocess.run([sys.executable, str(TRACE / "freeze.py"), *args],
                          capture_output=True, text=True, env=env)


@pytest.fixture
def media_text(tmp_path) -> dict:
    media = tmp_path / "media"
    (media / "story").mkdir(parents=True)
    src = media / "story" / "story-packet.md"
    src.write_text(ARTIFACT)
    binding = tmp_path / "binding.md"
    binding.write_text(BINDING)
    settings = tmp_path / "folders.local"
    settings.write_text(f"media = {media}\n")
    return {"media": media, "src": src, "binding": binding, "settings": settings, "out": tmp_path / "out"}


def test_freeze_copies_and_verifies_a_named_source(media_text):
    m = media_text
    r = freeze_cli("copy", "--binding", str(m["binding"]), "--out", str(m["out"]),
                   "media:story/story-packet.md=mc-eng-001.story", "--at", "2026-10-18T10:00:00-04:00",
                   env_file=m["settings"])
    assert r.returncode == 0, r.stderr
    copy = m["out"] / "mc-eng-001.story--story-packet.md"
    assert copy.is_file()
    r = freeze_cli("verify", f"{copy}=media:story/story-packet.md", env_file=m["settings"])
    assert r.returncode == 0, r.stdout + r.stderr
    assert "unchanged since the freeze" in r.stdout


def test_freeze_reports_a_name_not_set_up_and_never_passes(media_text):
    m = media_text
    r = freeze_cli("copy", "--binding", str(m["binding"]), "--out", str(m["out"]),
                   "media:story/story-packet.md=mc-eng-001.story", env_file=m["settings"])
    copy = m["out"] / "mc-eng-001.story--story-packet.md"
    m["settings"].write_text("# no media folder on this machine\n")
    for args in (("verify", f"{copy}=media:story/story-packet.md"),
                 ("copy", "--binding", str(m["binding"]), "--out", str(m["out"]),
                  "media:story/story-packet.md=again"),
                 ("show", "--binding", str(m["binding"]), "media:story/story-packet.md")):
        r = freeze_cli(*args, env_file=m["settings"])
        assert r.returncode != 0, args
        assert "not set up on this machine" in r.stdout + r.stderr, args
