"""Blind Close review: no draft leakage, no approval from incomplete or changed evidence."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

from synth import build
from tracekit.labels import Label, format_rows, parse_labels

TRACE = Path(__file__).resolve().parents[1]
HEADER = "| pass | verdict | first_failing_stage | critique | failure_code |\n|---|---|---|---|---|\n"


def run(eng, action):
    return subprocess.run([sys.executable, str(TRACE / "close_sample.py"), action, str(eng)],
                          capture_output=True, text=True)


@pytest.fixture
def eng(tmp_path):
    root = build(tmp_path / "pc-eng-000-callboard")
    path = root / "trace/labels.md"
    labels = parse_labels(path.read_text())
    path.write_text(HEADER + format_rows([
        Label(pid, row.verdict or "pass", row.first_failing_stage,
              "SECRET COORDINATOR CRITIQUE", row.failure_code)
        for pid, row in labels.items()
    ]))
    return root


def review(eng):
    return eng / "trace/close-sample"


def answer(eng, *, change=None, omit=False):
    folder = review(eng)
    plan = json.loads((folder / "sample.json").read_text())
    labels = parse_labels((folder / "draft-labels.md").read_text())
    rows = [labels[pid] for pid in plan["selected"]]
    if change:
        rows = change(rows)
    if omit:
        rows = rows[:-1]
    (folder / "blind-labels.md").write_text(
        f"<!-- close-sample: {plan['id']} -->\n" + HEADER + format_rows(rows))
    return rows


def test_draw_freezes_three_unique_rows_including_fail_and_pass_without_draft_in_html(eng):
    before = (eng / "trace/labels.md").read_bytes()
    result = run(eng, "draw")
    assert result.returncode == 0, result.stderr
    plan = json.loads((review(eng) / "sample.json").read_text())
    selected = plan["selected"]
    assert len(selected) == len(set(selected)) == 3
    labels = parse_labels(before.decode())
    assert {labels[pid].verdict for pid in selected} == {"pass", "fail"}
    page = (review(eng) / "blind.html").read_text()
    assert "SECRET COORDINATOR CRITIQUE" not in page
    assert "draft-labels.md" not in page
    assert "localStorage" not in page  # never restore ordinary viewer drafts
    assert "blind-labels.md" in page
    assert (eng / "trace/labels.md").read_bytes() == before


def test_draw_refuses_reroll_and_preserves_the_frozen_draw(eng):
    assert run(eng, "draw").returncode == 0
    before = {p.name: p.read_bytes() for p in review(eng).iterdir()}
    assert run(eng, "draw").returncode == 2
    assert before == {p.name: p.read_bytes() for p in review(eng).iterdir()}


def test_agreement_keeps_owner_approval_pending_and_does_not_replace_labels(eng):
    assert run(eng, "draw").returncode == 0
    answer(eng)
    before = (eng / "trace/labels.md").read_bytes()
    result = run(eng, "compare")
    assert result.returncode == 0, result.stderr
    report = (review(eng) / "comparison.md").read_text()
    assert "AGREEMENT" in report and "awaits Sean" in report
    assert "SECRET COORDINATOR CRITIQUE" in report
    assert (eng / "trace/labels.md").read_bytes() == before
    assert run(eng, "compare").returncode == 2  # append-only evidence


@pytest.mark.parametrize("field", ["verdict", "stage"])
def test_any_sampled_disagreement_holds_batch_approval(eng, field):
    assert run(eng, "draw").returncode == 0
    def change(rows):
        fail = next(i for i, row in enumerate(rows) if row.verdict == "fail")
        row = rows[fail]
        rows[fail] = (Label(row.pass_id, "pass", None, "I disagree.", "") if field == "verdict"
                      else Label(row.pass_id, "fail", 7 if row.first_failing_stage != 7 else 1,
                                 "I disagree.", ""))
        return rows
    answer(eng, change=change)
    result = run(eng, "compare")
    assert result.returncode == 1, result.stderr
    report = (review(eng) / "comparison.md").read_text()
    assert "WIDER REVIEW REQUIRED" in report
    assert "remaining rows" in report and "fresh" in report


@pytest.mark.parametrize("problem", ["missing", "deferred", "wrong-draw", "draft-changed", "record-changed", "artifact-changed"])
def test_comparison_cannot_clear_missing_answers_or_changed_evidence(eng, problem):
    assert run(eng, "draw").returncode == 0
    rows = answer(eng, omit=problem == "missing")
    if problem == "deferred":
        answer(eng, change=lambda rs: [Label(rs[0].pass_id, "defer", None, "", ""), *rs[1:]])
    elif problem == "wrong-draw":
        path = review(eng) / "blind-labels.md"
        path.write_text(path.read_text().replace("close-sample:", "other-sample:"))
    elif problem == "draft-changed":
        with (eng / "trace/labels.md").open("a") as out:
            out.write("\nChanged after the draw.\n")
    elif problem == "record-changed":
        path = next((eng / "trace").glob(rows[0].pass_id + "-*.md"))
        with path.open("a") as out:
            out.write("\nChanged after the draw.\n")
    elif problem == "artifact-changed":
        path = next((eng / "artifacts").glob("*.md"))
        with path.open("a") as out:
            out.write("\nChanged after the draw.\n")
    result = run(eng, "compare")
    assert result.returncode == 2, result.stdout
    assert not (review(eng) / "comparison.md").exists()


def test_draw_refuses_incomplete_drafts(eng):
    path = eng / "trace/labels.md"
    path.write_text(path.read_text().replace("| pass |", "| defer |", 2).replace("| defer | verdict", "| pass | verdict"))
    result = run(eng, "draw")
    assert result.returncode == 2
    assert not review(eng).exists()


def test_tiny_all_pass_batch_uses_all_rows_and_reports_no_drafted_fail(eng):
    for path in (eng / "trace").glob("pass-*.md"):
        if not path.name.startswith(("pass-01-", "pass-02-")):
            path.unlink()
    path = eng / "trace/labels.md"
    path.write_text(HEADER + "| pass-01 | pass | | | |\n| pass-02 | pass | | | |\n")
    assert run(eng, "draw").returncode == 0
    answer(eng)
    assert run(eng, "compare").returncode == 0
    assert "No drafted fail was available" in (review(eng) / "comparison.md").read_text()


def test_devcraft_can_label_a_failure_that_began_at_the_coordinators_stage(tmp_path):
    from test_studio import DC_CLOSE, DC_PROFILE, DC_SMALL, _dc_engagement
    root = _dc_engagement(tmp_path, "small-ask", DC_SMALL + DC_CLOSE)
    path = root / "trace/labels.md"
    path.write_text(path.read_text().replace("| pass-05 | pass | | fine | |",
                                            "| pass-05 | fail | 0 | Coordination failed. | |"))
    def dc_run(action):
        return subprocess.run([sys.executable, str(TRACE / "close_sample.py"), action, str(root),
                               "--studio", str(DC_PROFILE)], capture_output=True, text=True)
    assert dc_run("draw").returncode == 0
    answer(root)
    result = dc_run("compare")
    assert result.returncode == 0, result.stderr
    assert '<option value="0">' in (review(root) / "blind.html").read_text()


@pytest.mark.parametrize("rewrite", [False, True])
def test_live_coordinator_transcript_may_append_but_not_rewrite_its_frozen_prefix(eng, rewrite):
    path = next((eng / "trace").glob("pass-25-*.md"))
    path.write_text(path.read_text().replace("raw_log: —", "raw_log: trace/logs/live.jsonl"))
    transcript = eng / "trace/logs/live.jsonl"
    transcript.write_text("Original session text.\n")
    assert run(eng, "draw").returncode == 0
    answer(eng)
    transcript.write_text(("Rewritten session text.\n" if rewrite else "Original session text.\n") +
                          "Draw returned; Sean saved answers.\n")
    result = run(eng, "compare")
    assert result.returncode == (2 if rewrite else 0), result.stderr


def test_blind_page_does_not_link_to_label_views_backups_or_containing_directories(eng):
    from tracekit.close_sample import draw
    from tracekit.engagement import InputRef, load_engagement
    loaded = load_engagement(eng)
    (eng / "trace/eval.html").write_text("SECRET COORDINATOR CRITIQUE")
    (eng / "trace/labels-backup.md").write_text("SECRET COORDINATOR CRITIQUE")
    for record in loaded.records:
        record.inputs.extend(InputRef(path, "unused") for path in
                             ("trace/eval.html", "trace/labels-backup.md", "trace", "."))
    page = draw(loaded).read_text()
    assert "SECRET COORDINATOR CRITIQUE" not in page
    for href in ('href="../eval.html"', 'href="../labels-backup.md"', 'href=".."', 'href="../.."'):
        assert href not in page


def test_directory_evidence_does_not_include_the_samples_own_generated_files(eng):
    from tracekit.close_sample import compare, draw
    from tracekit.engagement import InputRef, load_engagement
    loaded = load_engagement(eng)
    loaded.records[0].inputs.append(InputRef(".", "unused"))
    draw(loaded)
    answer(eng)
    agrees, _ = compare(loaded)
    assert agrees


def test_blind_page_preserves_access_to_a_sampled_trials_actual_artifact(eng):
    from tracekit.close_sample import draw
    from tracekit.engagement import load_engagement
    loaded = load_engagement(eng)
    loaded.records = [loaded.by_id["pass-18"]]
    loaded.labels = {"pass-18": loaded.labels["pass-18"]}
    page = draw(loaded).read_text()
    assert 'href="../trials/outcome-roadmap-trial.md"' in page
