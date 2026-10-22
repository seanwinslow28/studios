"""The `grounding:` line written from the pass's reads, never declared by the seat (SWCB #260).

mc-eng-001's pass-10 and pass-33 repaired a packet, opened no library file, and kept
the draft's `grounding: full` by copying its header. The script writes the line from
the record instead, along the same revision chain rung-0 line 5 reads. Every record
and transcript here is the synthetic Callboard engagement's, or invented below.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from synth import build
from tracekit.checker import CHECK_NAMES, run_checks
from tracekit.engagement import load_engagement
from tracekit.grounding import GroundingError, stamp

TRACE = Path(__file__).resolve().parents[1]
CORPUS = CHECK_NAMES[4]
MOM_TEST = "corpus/discovery/the-mom-test.md"


@pytest.fixture
def eng_dir(tmp_path) -> Path:
    return build(tmp_path / "pc-eng-000-callboard")


@pytest.fixture
def library(tmp_path) -> Path:
    lib = tmp_path / "productcraft" / "corpus"
    (lib / "discovery").mkdir(parents=True)
    (lib / "discovery" / "the-mom-test.md").write_text("# invented\n", encoding="utf-8")
    return lib


def record(eng_dir: Path, pid: str) -> Path:
    return next((eng_dir / "trace").glob(f"{pid}-*.md"))


def claude_log(*paths: str) -> str:
    """A Claude stream-json log whose only calls are successful Reads of these files."""
    lines = [json.dumps({"type": "system", "subtype": "init", "model": "claude-opus-5"})]
    for i, p in enumerate(paths):
        uid = f"toolu_{i}"
        lines.append(json.dumps({"type": "assistant", "message": {"model": "claude-opus-5", "content": [
            {"type": "tool_use", "id": uid, "name": "Read", "input": {"file_path": p}}]}}))
        lines.append(json.dumps({"type": "user", "message": {"content": [
            {"type": "tool_result", "tool_use_id": uid, "content": "1\t# invented", "is_error": False}]}}))
    return "\n".join(lines) + "\n"


def before_hashing(eng_dir: Path, pid: str, *, reads: list[str], listed: list[str], grounding: str) -> Path:
    """The pass as the coordinator holds it on return: its log, its pasted list, its outputs not yet hashed,
    and the seat's artifact carrying `grounding: <grounding>`."""
    rec = record(eng_dir, pid)
    (eng_dir / "trace" / "logs" / f"{pid}.jsonl").write_text(claude_log(*reads), encoding="utf-8")
    t = rec.read_text()
    t = re.sub(r"(## Corpus read\n\n)(.*?)(\n\n## )", lambda m: m.group(1) + (
        "\n".join(f"- {x}" for x in listed) or "none") + m.group(3), t, count=1, flags=re.S)
    head, body = t.split("\n---\n", 1)
    out = head.index("outputs:")
    end = head.index("raw_log:")
    head = head[:out] + re.sub(r"\n\s+sha256: [0-9a-f]{64}", "", head[out:end]) + head[end:]
    rec.write_text(head + "\n---\n" + body)
    art = eng_dir / "artifacts" / "discovery-packet.md"
    art.write_text(re.sub(r"^grounding: \S+", f"grounding: {grounding}", art.read_text(), count=1, flags=re.M))
    return art


def no_library_reads(rec: Path) -> None:
    """Take every library file out of a record's `## Corpus read`."""
    rec.write_text(re.sub(r"^- corpus/.*\n", "", rec.read_text(), flags=re.M))


def hash_output(rec: Path, rel: str, h: str) -> None:
    """Record an output's hash, as the coordinator does once the line is written."""
    t = rec.read_text()
    i = t.index("outputs:")
    rec.write_text(t[:i] + t[i:].replace(f"  - path: {rel}\n", f"  - path: {rel}\n    sha256: {h}\n", 1))


def grounding_of(p: Path) -> str:
    return re.search(r"^grounding: (\S+)", p.read_text(), re.M).group(1)


def test_a_pass_that_read_the_library_gets_full(eng_dir, library):
    art = before_hashing(eng_dir, "pass-07", reads=[str(library / "discovery/the-mom-test.md")],
                         listed=[MOM_TEST], grounding="pending")
    [s] = stamp(load_engagement(eng_dir), "pass-07", library=library)
    assert (s.value, s.written, s.basis) == ("full", True, "this pass's reads")
    assert grounding_of(art) == "full"


def test_a_repair_that_opened_nothing_keeps_full_on_its_drafts_reads(eng_dir, library):
    """pass-10 and pass-33's shape: the line is right, and now the script, not the seat, wrote it."""
    art = before_hashing(eng_dir, "pass-07", reads=[], listed=[], grounding="pending")
    [s] = stamp(load_engagement(eng_dir), "pass-07", library=library)
    assert s.value == "full" and "pass-05" in s.basis and "earlier revision" in s.basis
    assert grounding_of(art) == "full"


def test_nothing_read_on_the_chain_is_none_with_the_library_here(eng_dir, library):
    no_library_reads(record(eng_dir, "pass-05"))
    art = before_hashing(eng_dir, "pass-07", reads=[], listed=[], grounding="full")
    [s] = stamp(load_engagement(eng_dir), "pass-07", library=library)
    assert (s.was, s.value) == ("full", "none")
    assert grounding_of(art) == "none"


def test_nothing_read_without_the_library_is_manifest_only(eng_dir, tmp_path):
    no_library_reads(record(eng_dir, "pass-05"))
    before_hashing(eng_dir, "pass-07", reads=[], listed=[], grounding="pending")
    [s] = stamp(load_engagement(eng_dir), "pass-07", library=tmp_path / "no-such-library")
    assert s.value == "manifest-only"


def test_a_list_that_is_not_reads_pys_output_is_refused(eng_dir, library):
    """dc-eng-002's shape: the log shows a read the typed list leaves out. Nothing is written from it."""
    art = before_hashing(eng_dir, "pass-07", reads=[str(library / "discovery/the-mom-test.md")],
                         listed=[], grounding="pending")
    with pytest.raises(GroundingError, match="not what reads.py prints"):
        stamp(load_engagement(eng_dir), "pass-07", library=library)
    assert grounding_of(art) == "pending"


def test_a_read_reads_py_could_not_judge_may_be_listed_once_confirmed(eng_dir, library):
    """The record template lets the coordinator add a read it confirmed in the transcript, with a note."""
    before_hashing(eng_dir, "pass-07", reads=[], listed=[MOM_TEST], grounding="pending")
    log = eng_dir / "trace" / "logs" / "pass-07.jsonl"
    call = {"type": "assistant", "message": {"model": "claude-opus-5", "content": [{"type": "tool_use", "id": "toolu_9",
            "name": "Bash", "input": {"command": f"python3 - <<'PY'\nprint(open('{library}/discovery/the-mom-test.md').read())\nPY"}}]}}
    done = {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "toolu_9",
            "content": "# invented", "is_error": False}]}}
    log.write_text(log.read_text() + json.dumps(call) + "\n" + json.dumps(done) + "\n")
    [s] = stamp(load_engagement(eng_dir), "pass-07", library=library)
    assert s.value == "full" and s.basis == "this pass's reads"

def test_a_dated_correction_is_what_the_line_is_written_from(eng_dir, library):
    before_hashing(eng_dir, "pass-07", reads=[str(library / "discovery/the-mom-test.md")], listed=[],
                   grounding="pending")
    rec = record(eng_dir, "pass-07")
    rec.write_text(rec.read_text().replace(
        "## Corpus read\n\nnone\n",
        f"## Corpus read\n\nnone\n\n**Correction, 2026-10-22** The transcript shows one read.\n\n- {MOM_TEST}\n"))
    [s] = stamp(load_engagement(eng_dir), "pass-07", library=library)
    assert s.value == "full" and s.basis == "this pass's reads"


def test_an_output_already_hashed_is_refused_not_rewritten(eng_dir, library):
    before_hashing(eng_dir, "pass-07", reads=[], listed=[], grounding="none")
    rec = record(eng_dir, "pass-07")
    import hashlib
    art = eng_dir / "artifacts" / "discovery-packet.md"
    h = hashlib.sha256(art.read_bytes()).hexdigest()
    hash_output(rec, "artifacts/discovery-packet.md", h)
    [s] = stamp(load_engagement(eng_dir), "pass-07", library=library)
    assert s.value == "full" and not s.written and "before taking the outputs' hashes" in s.refused
    assert grounding_of(art) == "none"


def test_only_the_value_changes_and_a_comment_after_it_stays(eng_dir, library):
    art = before_hashing(eng_dir, "pass-07", reads=[], listed=[], grounding="pending")
    art.write_text(art.read_text().replace("grounding: pending", "grounding: pending   # coordinator: grounding.py"))
    before = art.read_text()
    stamp(load_engagement(eng_dir), "pass-07", library=library)
    assert art.read_text() == before.replace("grounding: pending   #", "grounding: full   #")


def test_the_line_it_writes_passes_rung_0_line_5(eng_dir, library):
    before_hashing(eng_dir, "pass-07", reads=[], listed=[], grounding="pending")
    stamp(load_engagement(eng_dir), "pass-07", library=library)
    rec = record(eng_dir, "pass-07")
    import hashlib
    h = hashlib.sha256((eng_dir / "artifacts" / "discovery-packet.md").read_bytes()).hexdigest()
    hash_output(rec, "artifacts/discovery-packet.md", h)
    c = {c.name: c for c in run_checks(load_engagement(eng_dir))}[CORPUS]
    assert not [f for f in c.findings if "pass-07" in f and "grounding" in f]


def test_check_mode_writes_nothing_and_exits_1_on_a_wrong_line(eng_dir, library):
    art = before_hashing(eng_dir, "pass-07", reads=[], listed=[], grounding="none")
    r = subprocess.run([sys.executable, str(TRACE / "grounding.py"), str(eng_dir), "pass-07", "--check",
                        "--library", str(library)], capture_output=True, text=True)
    assert r.returncode == 1, r.stderr
    assert "should read full" in r.stdout
    assert grounding_of(art) == "none"
    r = subprocess.run([sys.executable, str(TRACE / "grounding.py"), str(eng_dir), "pass-07",
                        "--library", str(library)], capture_output=True, text=True)
    assert r.returncode == 0 and "written" in r.stdout
    assert grounding_of(art) == "full"


def test_a_pass_with_no_record_is_exit_2(eng_dir):
    r = subprocess.run([sys.executable, str(TRACE / "grounding.py"), str(eng_dir), "pass-99"],
                       capture_output=True, text=True)
    assert r.returncode == 2 and "no record for pass-99" in r.stderr


# --------------------------------------------------------------------------- #
# rung-0 line 5 on a line left pending
# --------------------------------------------------------------------------- #


def test_a_pending_line_left_after_the_pass_is_a_finding(eng_dir):
    from test_checker import edit_artifact
    edit_artifact(eng_dir, "artifacts/discovery-packet.md", "grounding: full", "grounding: pending")
    c = {c.name: c for c in run_checks(load_engagement(eng_dir))}[CORPUS]
    assert not c.ok
    assert any("pass-07" in f and "pending" in f and "grounding.py" in f for f in c.findings)
