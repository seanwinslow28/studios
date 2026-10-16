"""The eleventh rung-0 line: a pass's recorded runtime matches what its own logs say ran, and nothing ran beside it.

Ruled on #321 (2026-09-29): the Agent tool's `opus` / `sonnet` aliases moved from
Opus 5 / Sonnet 5 to the 5.5 generation after pc-eng-001 closed, and nothing in
the studio noticed. An alias is not a pin, so the record's `runtime:` is checked
against the model the transcript itself says answered. Widened on SWCB #123
(2026-10-12) to Codex passes, read from their saved session files, and to the
helper agents Codex's sub-agent tools can start whatever the config says.
"""
import json
from pathlib import Path

import pytest

from synth import build
from tracekit.checker import CHECK_NAMES, run_checks
from tracekit.engagement import load_engagement

LINE = CHECK_NAMES[10]


@pytest.fixture
def eng_dir(tmp_path) -> Path:
    return build(tmp_path / "pc-eng-000-callboard")


def stamp(eng_dir: Path, pid: str, *models: str) -> None:
    """Replace a pass's stub log with Claude Code transcript lines stamped with these models."""
    lines = [json.dumps({"type": "user", "message": {"role": "user", "content": "seat brief"}})]
    for m in models:
        lines.append(json.dumps({"type": "assistant", "message": {"model": m, "role": "assistant", "content": []}}))
    (eng_dir / "trace" / "logs" / f"{pid}.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")


def line(eng_dir: Path):
    checks = run_checks(load_engagement(eng_dir))
    return next(c for c in checks if c.name == LINE)


def test_the_line_is_the_eleventh_and_runs_last():
    assert len(CHECK_NAMES) == 11 and LINE == "Recorded runtime matches the raw log: its model stamps, and no helper agent"


def test_stub_logs_are_unverifiable_never_passed_or_failed(eng_dir):
    c = line(eng_dir)
    assert c.ok and c.n_ok == 0
    assert c.n_unverifiable == c.n_total == 24   # 13 Opus + 6 Sonnet + 5 Codex passes; the coordinator is out of scope
    assert any("carry no model stamp" in n for n in c.notes)
    assert any("no readable JSONL raw log" in n for n in c.notes)   # the Codex passes' plain-form logs
    assert any("out of scope" in n for n in c.notes)


def test_a_matching_stamp_verifies_the_pass(eng_dir):
    stamp(eng_dir, "pass-01", "claude-opus-5", "claude-opus-5")
    c = line(eng_dir)
    assert c.ok and c.n_ok == 1 and c.n_unverifiable == 23


def test_an_alias_that_moved_is_a_finding_naming_both_models(eng_dir):
    stamp(eng_dir, "pass-01", "claude-opus-5-5", "claude-opus-5-5")
    c = line(eng_dir)
    assert not c.ok
    assert c.findings == ["pass-01: runtime claude-opus-5 but its raw log is stamped claude-opus-5-5"]


def test_a_second_model_in_one_log_is_a_finding(eng_dir):
    stamp(eng_dir, "pass-01", "claude-opus-5", "claude-haiku-4-5")
    c = line(eng_dir)
    assert c.findings == ["pass-01: runtime claude-opus-5 but its raw log is stamped claude-haiku-4-5, claude-opus-5"]


def test_synthetic_stamps_are_not_models(eng_dir):
    # Claude Code writes "<synthetic>" on messages no model produced; they say nothing about the runtime.
    stamp(eng_dir, "pass-01", "claude-opus-5", "<synthetic>")
    assert line(eng_dir).n_ok == 1


def test_a_missing_log_is_unverifiable_and_named(eng_dir):
    (eng_dir / "trace" / "logs" / "pass-01.jsonl").unlink()
    c = line(eng_dir)
    assert c.ok
    assert any("no readable JSONL raw log" in n and "pass-01" in n for n in c.notes)


# --------------------------------------------------------------------------- #
# Codex passes (#123): session files beside the JSONL, shaped like the 2026-10-10 probes
# --------------------------------------------------------------------------- #

ROOT = "01a1253e-0000-7000-8000-000000000001"
HELPER = "01a1253e-0000-7000-8000-000000000002"


def _meta(id_, root, helper=False):
    p = {"id": id_, "session_id": root, "source": "exec", "thread_source": "user", "cli_version": "0.162.1"}
    if helper:
        p.update(parent_thread_id=root, thread_source="subagent",
                 source={"subagent": {"thread_spawn": {"parent_thread_id": root, "depth": 1}}})
    return {"type": "session_meta", "payload": p}


def _turn(model="gpt-5.6-sol", effort="high"):
    return {"type": "turn_context", "payload": {"model": model, "effort": effort}}


def _tokens(n):
    return {"type": "event_msg", "payload": {"type": "token_count", "info": {"total_token_usage": {"input_tokens": n, "output_tokens": 5}}}}


def codex_pass(eng_dir: Path, *, jsonl=None, sessions=None) -> str:
    """Point the first Codex pass at a JSONL raw log, and save its session files; returns its id."""
    pid = next(r.pass_id for r in load_engagement(eng_dir).records if r.runtime.startswith("codex "))
    rec = next((eng_dir / "trace").glob(f"{pid}-*.md"))
    rec.write_text(rec.read_text().replace(f"trace/logs/{pid}.txt", f"trace/logs/{pid}.jsonl"))
    logs = eng_dir / "trace" / "logs"
    if jsonl is None:
        jsonl = [{"type": "thread.started", "thread_id": ROOT}, {"type": "turn.completed", "usage": {"input_tokens": 9, "output_tokens": 1}}]
    (logs / f"{pid}.jsonl").write_text("".join(json.dumps(e) + "\n" for e in jsonl))
    if sessions is not None:
        d = logs / f"{pid}.rollouts"
        d.mkdir()
        for name, events in sessions.items():
            (d / name).write_text("".join(json.dumps(e) + "\n" for e in events))
    return pid


def test_a_codex_pass_with_matching_session_stamps_verifies(eng_dir):
    pid = codex_pass(eng_dir, sessions={"rollout-a.jsonl": [_meta(ROOT, ROOT), _turn(), _tokens(9)]})
    c = line(eng_dir)
    assert c.ok and c.n_ok == 1 and pid not in " ".join(c.notes)


def test_a_codex_pass_without_session_files_is_unverifiable_and_named(eng_dir):
    pid = codex_pass(eng_dir)
    c = line(eng_dir)
    assert c.ok and c.n_ok == 0
    assert any("no saved session files" in n and pid in n for n in c.notes)


def test_a_codex_model_or_effort_that_differs_is_a_finding(eng_dir):
    pid = codex_pass(eng_dir, sessions={"rollout-a.jsonl": [_meta(ROOT, ROOT), _turn(effort="low")]})
    c = line(eng_dir)
    assert c.findings == [f"{pid}: runtime codex gpt-5.6-sol high but its session files are stamped codex gpt-5.6-sol low"]


def test_a_spawn_in_the_session_files_fails_the_pass(eng_dir):
    # what the probes showed: the parent's spawn_agent call, its sub_agent_activity event, and the helper's own file
    parent = [_meta(ROOT, ROOT), _turn(),
              {"type": "response_item", "payload": {"type": "function_call", "name": "spawn_agent", "arguments": "{}"}},
              {"type": "event_msg", "payload": {"type": "sub_agent_activity", "agent_thread_id": HELPER, "kind": "started"}}]
    pid = codex_pass(eng_dir, sessions={"rollout-a.jsonl": parent, "rollout-b.jsonl": [_meta(HELPER, ROOT, helper=True), _turn(), _tokens(10326)]})
    c = line(eng_dir)
    assert len(c.findings) == 1 and c.findings[0].startswith(f"{pid}: started a helper agent (1 spawn call(s); 1 helper session(s): rollout-b.jsonl)")


def test_codex_reviews_built_in_reviewer_is_a_helper_too(eng_dir):
    # `codex review` is not a launch form (#123): its reviewer is a helper and fails like any other
    reviewer = _meta(HELPER, ROOT)
    reviewer["payload"].update(parent_thread_id=ROOT, thread_source="subagent", source={"subagent": "review"})
    pid = codex_pass(eng_dir, sessions={"rollout-a.jsonl": [_meta(ROOT, ROOT), _turn()], "rollout-b.jsonl": [reviewer, _turn()]})
    assert any(f.startswith(f"{pid}: started a helper agent") for f in line(eng_dir).findings)


def test_a_helper_seen_only_in_the_jsonl_is_still_a_finding(eng_dir):
    # the --json stream shows the parent waiting on a helper, never the spawn; with no session files that is all there is
    wait = {"type": "item.completed", "item": {"id": "item_1", "type": "collab_tool_call", "tool": "wait"}}
    pid = codex_pass(eng_dir, jsonl=[{"type": "thread.started", "thread_id": ROOT}, wait])
    c = line(eng_dir)
    assert c.findings == [f"{pid}: its raw log shows a helper agent at work (wait); a seat pass never hands work to a sub-agent"]


def test_session_files_from_another_thread_are_a_finding(eng_dir):
    pid = codex_pass(eng_dir, sessions={"rollout-a.jsonl": [_meta(HELPER, HELPER), _turn()]})
    assert line(eng_dir).findings == [f"{pid}: its session files are thread {HELPER}, but its raw log is thread {ROOT}"]


def test_a_provider_route_stays_out_of_scope():
    from tracekit.codexlog import parse_runtime
    assert parse_runtime("codex gpt-6.1-sol high") == ("gpt-6.1-sol", "high")
    assert parse_runtime("codex/openrouter glm-5.3") is None


# --------------------------------------------------------------------------- #
# the probe logs themselves, when Devcraft's private ledger is on this disk
# --------------------------------------------------------------------------- #

PROBES = Path(__file__).resolve().parents[3] / "devcraft" / "ledger" / "setup" / "2026-10-10-seat-isolation" / "codex"


def _probe_pass(eng_dir: Path, log: Path, threads: list[str], rollouts: Path):
    """The first Codex pass, re-pointed at one probe's JSONL and session files (the probes ran at effort low)."""
    pid = codex_pass(eng_dir, jsonl=[json.loads(l) for l in log.read_text().splitlines() if l.strip()])
    rec = next((eng_dir / "trace").glob(f"{pid}-*.md"))
    rec.write_text(rec.read_text().replace("runtime: codex gpt-5.6-sol high", "runtime: codex gpt-5.6-sol low"))
    d = eng_dir / "trace" / "logs" / f"{pid}.rollouts"
    d.mkdir()
    for f in rollouts.rglob("*.jsonl"):
        if any(t in f.name for t in threads):
            (d / f.name).write_bytes(f.read_bytes())
    return line(eng_dir), pid


@pytest.mark.skipif(not PROBES.is_dir(), reason="Devcraft's private ledger is not on this disk")
@pytest.mark.parametrize("log,threads,fails", [
    ("F-spawn-test.jsonl", ["01a1253e-6bf9", "01a1253e-775e"], True),          # MacBook Pro, 0.146.0
    ("E-seat-config.jsonl", ["01a1253d-efd0"], False),
    ("mini-0.160.1/F.jsonl", ["01a1253f-a685", "01a1253f-b6e9"], True),        # Mac Mini, 0.160.1
    ("mini-0.160.1/E.jsonl", ["01a1253f-8826"], False),
])
def test_the_seat_isolation_probes(eng_dir, log, threads, fails):
    path = PROBES / log
    c, pid = _probe_pass(eng_dir, path, threads, path.parent / "rollouts")
    mine = [f for f in c.findings if f.startswith(pid + ":")]
    if fails:
        assert any("started a helper agent" in f for f in mine), c.findings
    else:
        assert not mine and c.n_ok == 1, c.findings


def test_collect_copies_a_pass_and_its_helpers_from_the_seat_home(tmp_path):
    from tracekit.codexlog import collect
    day = tmp_path / "home" / "sessions" / "2026" / "10" / "12"
    day.mkdir(parents=True)
    other = "01a1253e-0000-7000-8000-000000000009"
    for name, meta in (("rollout-1-own.jsonl", _meta(ROOT, ROOT)), ("rollout-2-helper.jsonl", _meta(HELPER, ROOT, helper=True)),
                       ("rollout-3-other.jsonl", _meta(other, other))):
        (day / name).write_text(json.dumps(meta) + "\n" + json.dumps(_turn()) + "\n")
    got = collect(tmp_path / "home", ROOT, tmp_path / "pass-07.rollouts")
    assert sorted(f.name for f in got) == ["rollout-1-own.jsonl", "rollout-2-helper.jsonl"]
    assert (day / "rollout-1-own.jsonl").exists()   # copied, never moved


# --------------------------------------------------------------------------- #
# The coordinator's own session (SWCB #169): `raw_log` points at its transcript
# --------------------------------------------------------------------------- #


def point_coordinator(eng_dir: Path, log: Path) -> str:
    """Point the close record's `raw_log` at a session transcript outside the engagement; returns its id."""
    rec = next((eng_dir / "trace").glob("pass-*-coordinator-close.md"))
    rec.write_text(rec.read_text().replace("raw_log: —", f"raw_log: {log}"))
    return rec.name[:7]


def session(path: Path, *models: str, quoted: str = "") -> Path:
    """A Claude Code session file: Sean's turns, the coordinator's replies, and a tool result that quotes a log."""
    lines = [{"type": "user", "message": {"role": "user", "content": "open the engagement"}, "cwd": "/x"}]
    for m in models:
        lines.append({"type": "assistant", "message": {"model": m, "role": "assistant", "content": []}})
    if quoted:
        lines.append({"type": "user", "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "t", "content": quoted}]}})
    path.write_text("".join(json.dumps(x) + "\n" for x in lines), encoding="utf-8")
    return path


def test_a_coordinator_session_pointer_is_checked_like_any_log(eng_dir, tmp_path):
    pid = point_coordinator(eng_dir, session(tmp_path / "s1.jsonl", "claude-fable-5-1", "claude-fable-5-1"))
    c = line(eng_dir)
    assert c.ok and c.n_ok == 1 and c.n_total == 25
    assert not any("out of scope" in n for n in c.notes)
    assert pid not in " ".join(c.notes)


def test_a_model_switch_in_the_coordinator_session_is_a_finding(eng_dir, tmp_path):
    pid = point_coordinator(eng_dir, session(tmp_path / "s2.jsonl", "claude-fable-5-1", "claude-opus-5-5"))
    assert line(eng_dir).findings == [
        f"{pid}: runtime claude-fable-5-1 but its raw log is stamped claude-fable-5-1, claude-opus-5-5"]


def test_a_seat_log_quoted_inside_the_session_is_not_a_stamp(eng_dir, tmp_path):
    # the coordinator reads seat logs all train long; their stamps sit inside a JSON string, escaped
    quoted = json.dumps({"type": "assistant", "message": {"model": "claude-opus-5-5"}})
    point_coordinator(eng_dir, session(tmp_path / "s3.jsonl", "claude-fable-5-1", quoted=quoted))
    assert line(eng_dir).n_ok == 1


def test_a_pruned_coordinator_transcript_is_unverifiable_and_named(eng_dir, tmp_path):
    pid = point_coordinator(eng_dir, tmp_path / "gone.jsonl")
    c = line(eng_dir)
    assert c.ok and c.n_ok == 0
    assert any("no readable JSONL raw log" in n and pid in n for n in c.notes)
