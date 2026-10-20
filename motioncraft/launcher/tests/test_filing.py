"""Motioncraft's filing step: the images a pass opened stripped from its logs, the employer folders replaced.

The unit tests build logs in the two vendors' real shapes (a Claude Code tool result
carrying the picture it read, twice on the line; a Codex rollout carrying a data URL
after its image view) and file them. Two launches through the fake vendors show the
launcher filing a pass's logs before it writes the record.
"""
from __future__ import annotations

import base64
import hashlib
import json
import struct
import sys
import zlib
from pathlib import Path

import pytest

from test_seat import LAUNCHER, behave, codex_home, codex_pass, context, fake, launch, record, seat, world  # noqa: F401

sys.path.insert(0, str(LAUNCHER))
import filing  # noqa: E402


def png(w: int = 4, h: int = 3) -> bytes:
    """A real, small PNG: what a pass would have opened."""
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    rows = b"".join(b"\x00" + b"\x80\x40\x20" * w for _ in range(h))
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(rows)) + chunk(b"IEND", b""))


def b64(b: bytes) -> str:
    return base64.b64encode(b).decode()


def claude_read(tid: str, path: str, data: bytes):
    """The two lines Claude Code writes when a pass Reads an image: the tool use, then its result."""
    return [
        {"type": "assistant", "message": {"model": "claude-opus-5-5", "content": [
            {"type": "tool_use", "id": tid, "name": "Read", "input": {"file_path": path}}]}},
        {"type": "user", "message": {"role": "user", "content": [{"type": "tool_result", "tool_use_id": tid, "content": [
            {"type": "image", "source": {"type": "base64", "data": b64(data), "media_type": "image/png"}}]}]},
         "tool_use_result": {"type": "image", "file": {"base64": b64(data), "type": "image/png", "originalSize": len(data)}}},
    ]


def codex_view(path: str, data: bytes):
    """A Codex rollout's image view, then the tool output carrying the image as a data URL."""
    return [
        {"type": "event_msg", "payload": {"type": "item_completed", "item": {"type": "ImageView", "path": "file://" + path}}},
        {"type": "response_item", "payload": {"type": "custom_tool_call_output", "output": [
            {"type": "input_text", "text": "viewed"},
            {"type": "input_image", "image_url": "data:image/png;base64," + b64(data), "detail": "high"}]}},
    ]


@pytest.fixture()
def place(tmp_path):
    media = tmp_path / "media"
    (media / "Film" / "proj").mkdir(parents=True)
    emp = tmp_path / "work" / "day-job"
    emp.mkdir(parents=True)
    logs = tmp_path / "eng" / "trace" / "logs"
    logs.mkdir(parents=True)
    return {"media": media, "emp": str(emp), "logs": logs, "root": tmp_path}


def jsonl(path: Path, lines) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(l) + "\n" for l in lines))


def test_a_claude_log_keeps_each_picture_as_one_line_naming_it(place):
    kept = place["media"] / "Film" / "proj" / "frame.png"
    kept.write_bytes(png())
    stray = place["root"] / "scratch" / "probe.png"
    stray.parent.mkdir()
    stray.write_bytes(png(2, 2))
    log = place["logs"] / "pass-03.jsonl"
    jsonl(log, claude_read("t1", str(kept), png()) + claude_read("t2", str(stray), png(2, 2))
          + [{"type": "assistant", "message": {"content": [{"type": "text", "text": f"I read {place['emp']}/notes"}]}}])
    res = filing.file_logs(place["logs"], ["pass-03"], str(place["media"]), [place["emp"]])
    assert res["media_stripped"] == 4 and res["survivors"] == {} and res["rewritten"] == ["pass-03.jsonl"]
    text = log.read_text()
    assert b64(png()) not in text and "base64," not in text
    lines = [json.loads(l) for l in text.splitlines()]
    note = lines[1]["message"]["content"][0]["content"][0]["source"]["data"]
    assert note.startswith("motioncraft-stripped · image/png · sha256 " + hashlib.sha256(png()).hexdigest())
    assert f"path {kept}" in note and f"file sha256 {hashlib.sha256(png()).hexdigest()}" in note and "in the media folder" in note
    assert lines[1]["tool_use_result"]["file"]["base64"] == note, "the line's second copy gets the same note"
    assert "not kept (outside the media folder)" in lines[3]["message"]["content"][0]["content"][0]["source"]["data"]
    assert "<employer folder>/notes" in text and place["emp"] not in text
    assert lines[0]["message"]["model"] == "claude-opus-5-5", "the stamps the trace checker reads are untouched"


def test_a_codex_rollout_matches_each_image_to_the_view_before_it(place):
    a, b = place["media"] / "Film" / "proj" / "a.png", place["media"] / "Film" / "proj" / "b.png"
    a.write_bytes(png(3, 3))
    b.write_bytes(png(5, 5))
    roll = place["logs"] / "pass-04.rollouts" / "rollout-x.jsonl"
    jsonl(roll, [{"type": "turn_context", "payload": {"model": "gpt-6.1-sol", "effort": "high"}}]
          + codex_view(str(a), png(3, 3)) + codex_view(str(b), png(5, 5)) + [
              {"type": "response_item", "payload": {"type": "message", "content": [
                  {"type": "input_image", "image_url": "data:image/png;base64," + b64(png(6, 6))}]}}])
    res = filing.file_logs(place["logs"], ["pass-04"], str(place["media"]), [place["emp"]])
    assert res["media_stripped"] == 3 and res["survivors"] == {}
    notes = [json.loads(l) for l in roll.read_text().splitlines()]
    first, second = notes[2]["payload"]["output"][1]["image_url"], notes[4]["payload"]["output"][1]["image_url"]
    assert f"path {a}" in first and f"path {b}" in second, "each image takes the path of the view before it"
    assert "no path shown" in notes[5]["payload"]["content"][0]["image_url"], "an image with no view keeps its sha256 alone"
    assert notes[0]["payload"]["model"] == "gpt-6.1-sol"


def test_lock_files_are_redacted_whole_path_only_and_the_call_log_records_both_hashes(place):
    apps = place["logs"] / "pass-05.apps"
    apps.mkdir()
    lock = apps / "blender-1.sb"
    lock.write_text(f'(deny file-read* (subpath "{place["emp"]}") (subpath "{place["emp"]}-archive"))\n'
                    f'(allow file-read* (subpath "{place["emp"]}shop"))\n')
    before = hashlib.sha256(lock.read_bytes()).hexdigest()
    (place["logs"] / "pass-05.apps.jsonl").write_text(json.dumps(
        {"id": "blender-1", "lock": {"path": str(lock), "sha256": before}}) + "\n")
    res = filing.file_logs(place["logs"], ["pass-05"], str(place["media"]), [place["emp"]])
    assert res["survivors"] == {}
    text = lock.read_text()
    assert '(subpath "<employer folder>")' in text
    assert f'{place["emp"]}shop' in text and f'{place["emp"]}-archive' in text, \
        "a longer folder name is not the employer folder, so it is left as it is (list such a folder to replace it)"
    entry = json.loads((place["logs"] / "pass-05.apps.jsonl").read_text())
    assert entry["lock"]["sha256"] == before and entry["lock"]["filed_sha256"] == hashlib.sha256(lock.read_bytes()).hexdigest()


def test_filing_again_changes_nothing_and_check_changes_nothing(place):
    kept = place["media"] / "Film" / "proj" / "frame.png"
    kept.write_bytes(png())
    log = place["logs"] / "pass-06.jsonl"
    jsonl(log, claude_read("t1", str(kept), png()))
    snapshot = log.read_text()
    res = filing.file_logs(place["logs"], ["pass-06"], str(place["media"]), [place["emp"]], check_only=True)
    assert log.read_text() == snapshot and "pass-06.jsonl" in res["survivors"], "check reports and touches nothing"
    filing.file_logs(place["logs"], ["pass-06"], str(place["media"]), [place["emp"]])
    once = log.read_text()
    again = filing.file_logs(place["logs"], ["pass-06"], str(place["media"]), [place["emp"]])
    assert log.read_text() == once and again["media_stripped"] == 0 and again["rewritten"] == []


def test_what_cannot_be_filed_is_refused(place):
    (place["logs"] / "pass-07.apps").mkdir()
    (place["logs"] / "pass-07.apps" / "frame.bin").write_bytes(png())
    res = filing.file_logs(place["logs"], ["pass-07"], str(place["media"]), [place["emp"]])
    assert "pass-07.apps/frame.bin" in res["not_read"], "a file the step cannot read is never committed"


def test_a_data_url_outside_json_survives_and_is_named(place):
    (place["logs"] / "pass-08.stderr.log").write_text("debug: data:image/png;base64," + b64(png()) * 20 + "\n")
    res = filing.file_logs(place["logs"], ["pass-08"], str(place["media"]), [place["emp"]])
    assert "pass-08.stderr.log" in res["survivors"]


def test_a_claude_pass_is_filed_before_its_record(world, fake):
    kept = world["project"] / "appearance" / "seen.png"
    kept.write_bytes(png())
    ctx = context(world, "art-pose-designer", "f1")
    seat(world, "claude-settings", ctx)
    emp = str(world["emp"])
    behave(fake, extra_lines=claude_read("tx", str(kept), png())
           + [{"type": "assistant", "message": {"content": [{"type": "text", "text": f"saw {emp}/src"}]}}])
    r = launch(world, ctx, "--run")
    assert r.returncode == 0, r.stderr
    rec = record(world, "f1")
    assert rec["filing"]["media_stripped"] == 2 and rec["filing"]["survivors"] == {} and rec["filing"]["employer_paths_checked"]
    log = (world["eng"] / "trace" / "logs" / "pass-f1.jsonl").read_text()
    assert b64(png()) not in log and emp not in log and "motioncraft-stripped" in log


def test_a_codex_pass_has_its_rollout_filed(world, codex_home, fake):
    kept = world["project"] / "motion" / "seen.png"
    kept.write_bytes(png())
    ctx = codex_pass(world, codex_home, "f2")
    behave(fake, rollout_lines=codex_view(str(kept), png()))
    r = launch(world, ctx, "--output", "artifacts/scene-record-f2.md", "--run")
    assert r.returncode == 0, r.stderr
    rec = record(world, "f2")
    assert rec["filing"]["media_stripped"] == 1 and rec["filing"]["survivors"] == {}
    rolls = list((world["eng"] / "trace" / "logs" / "pass-f2.rollouts").glob("*.jsonl"))
    assert rolls and all("base64," not in p.read_text() for p in rolls)
