"""SWCB #212: a new Devcraft record using the adopted target:<repo>/<path> form.

Everything is invented: no seat ran, no owner labeled it, and no private
ledger is read or changed. The target sits outside both studios and the
engagement, just as a real target repository does.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from reference import REPO
from tracekit.engagement import sha256_path


@pytest.fixture
def devcraft_target(tmp_path, monkeypatch):
    repo = tmp_path / "studios"
    eng = repo / "devcraft" / "ledger" / "engagements" / "dc-eng-000-target-example"
    (eng / "trace").mkdir(parents=True)
    (eng / "audits").mkdir()
    (repo / "craftwork").mkdir()
    (repo / "CLAUDE.md").write_text("# Invented studios root.\n")
    target = tmp_path / "targets" / "demo-app" / "src" / "message.py"
    target.parent.mkdir(parents=True)
    target.write_text('MESSAGE = "An invented target."\n')
    settings = repo / "folders.local"
    settings.write_text(f"target = {tmp_path / 'targets'}\n")
    monkeypatch.setenv("TRACEKIT_FOLDERS", str(settings))
    (eng / "brief.md").write_text(
        "---\nid: dc-eng-000\nname: Named target example\ntype: one-off\nsynthetic: true\n---\n"
        "\nInvented one-off source audit; no real seat ran.\n")
    audit = eng / "audits" / "source-check.md"
    audit.write_text("# Invented source audit.\n\nThe example names the target file and its exact hash.\n")
    (eng / "trace" / "pass-01-build-planner-audit.md").write_text(f"""---
pass: pass-01
seat: build-planner
kind: audit
stage: 1
runtime: claude-sonnet-5-5
launch: synthetic fixture, no invocation
effort: high
launched: 2026-10-20T10:00:00-04:00
completed: 2026-10-20T10:00:01-04:00
wall_clock_s: 1
meter: null
meter_source: UNMEASURED
inputs:
  - path: target:demo-app/src/message.py
    sha256: {sha256_path(target)}
withheld:
  - the drafting conversation
outputs:
  - path: audits/source-check.md
    sha256: {sha256_path(audit)}
raw_log: trace/logs/pass-01.jsonl
checks: []
triggered_by: null
shadow_of: null
---

## Corpus read

none

## Notes

Synthetic example only: no seat ran and no owner judgment was made.
""")
    logs = eng / "trace" / "logs"
    logs.mkdir()
    (logs / "pass-01.jsonl").write_text('{"synthetic": true, "note": "No real invocation or model stamp."}\n')
    (eng / "trace" / "labels.md").write_text(
        "---\nlabeler: synthetic fixture, not Sean\n---\n\n"
        "| pass | verdict | first_failing_stage | critique | failure_code |\n"
        "|---|---|---|---|---|\n"
        "| pass-01 | pass | | Invented label for the adoption check. | |\n")
    return eng, settings, target


def check(eng):
    result = subprocess.run(
        [sys.executable, str(REPO / "craftwork/trace/check.py"), str(eng),
         "--studio", str(REPO / "devcraft/trace/studio.py"), "--json"],
        capture_output=True, text=True,
    )
    checks = json.loads(result.stdout)
    return result.returncode, checks


def test_new_devcraft_target_record_checks_clean_on_each_machine(devcraft_target, tmp_path):
    eng, settings, target = devcraft_target
    code, checks = check(eng)
    assert code == 0, checks
    assert len(checks) == 11 and all(c["ok"] for c in checks)
    assert checks[3]["n_ok"] == checks[3]["n_total"] == 2
    # The synthetic log explicitly carries no real model stamp: no runtime claim.
    assert checks[10]["n_unverifiable"] == 1

    record = next((eng / "trace").glob("pass-*.md"))
    original = record.read_bytes()
    other_machine = tmp_path / "other-machine" / "projects"
    shutil.move(str(target.parents[1]), str(other_machine / "demo-app"))
    settings.write_text(f"target = {other_machine}\n")
    code, checks = check(eng)
    assert code == 0, checks
    assert record.read_bytes() == original


@pytest.mark.parametrize("state, finding", [
    ("unset", "not set up on this machine"),
    ("changed", "hash no longer matches disk"),
    ("missing", "missing on disk"),
])
def test_devcraft_target_record_never_passes_without_its_recorded_bytes(devcraft_target, state, finding):
    eng, settings, target = devcraft_target
    if state == "unset":
        settings.write_text("# No target folder on this machine.\n")
    elif state == "changed":
        target.write_text('MESSAGE = "Changed after the audit."\n')
    else:
        target.unlink()
    code, checks = check(eng)
    assert code == 1
    assert not checks[3]["ok"]
    assert any("target:demo-app/src/message.py" in f and finding in f for f in checks[3]["findings"])
