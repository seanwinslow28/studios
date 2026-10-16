"""A frozen, optional blind sample of coordinator-drafted Close labels (#171).

The blind page receives selected record facts only, never the draft labels.
The frozen draft and draw manifest stay on disk for the later comparison.
This is a bias check, not a replacement for rung 0 or Sean's approval.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import random
import uuid
from pathlib import Path

from .engagement import Engagement, sha256_path
from .labels import COLUMNS, Label, decided, format_rows, parse_labels
from .viewer import CSS, _fonts_css, esc, run_line

HEADER = "| " + " | ".join(COLUMNS) + " |\n|---|---|---|---|---|\n"


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _batch(eng: Engagement) -> dict[str, Label]:
    if eng.errors or eng.labels_error or any(r.errors for r in eng.records):
        raise ValueError("repair the engagement's record or label parsing errors first")
    if not eng.records or len(eng.by_id) != len(eng.records):
        raise ValueError("the batch needs unique pass records")
    if set(eng.labels) != set(eng.by_id):
        raise ValueError("draft exactly one label for every recorded pass before drawing")
    for row in eng.labels.values():
        if not decided(row.verdict) or (row.verdict == "pass" and row.first_failing_stage is not None):
            raise ValueError(f"{row.pass_id}: finish the drafted verdict and failure stage before drawing")
    return eng.labels


def _evidence(eng: Engagement, frozen_logs: dict | None = None) -> dict:
    """Bind comparison to the batch and the disk evidence available at the draw.

    Missing/superseded outputs are still review limitations, never made current
    by this snapshot. The ordinary record checker remains independent.
    """
    paths = {eng.root / eng.studio.brief_file}
    live_logs = {}
    excluded = (eng.trace_dir / "close-sample").resolve()
    for record in eng.records:
        paths.add(record.file)
        for ref in (*record.inputs, *record.outputs):
            if ref.path:
                path = eng.resolve(ref.path)
                if path is not None:
                    paths.add(path)
        if record.raw_log and record.raw_log != "none":
            path = eng.resolve(record.raw_log)
            if path is not None:
                if record.kind in eng.studio.coordinator_kinds and path.is_file():
                    # Close is still running in this transcript. Protect its
                    # existing bytes, while allowing the session to append.
                    key = str(path.resolve())
                    length = (frozen_logs or {}).get(key, {}).get("length", path.stat().st_size)
                    with path.open("rb") as source:
                        prefix = source.read(length)
                    live_logs[key] = {"length": len(prefix), "sha256": _digest(prefix)}
                else:
                    paths.add(path)
    files = {}
    for path in sorted(paths):
        if path.is_dir():
            files["directory:" + str(path.resolve())] = "directory"
            candidates = (p for p in path.rglob("*") if p.is_file())
        else:
            candidates = [path]
        for source in candidates:
            resolved = source.resolve()
            if resolved.is_relative_to(excluded) or str(resolved) in live_logs:
                continue
            files[str(resolved)] = sha256_path(source)
    return {"files": files, "live_logs": live_logs}


def draw(eng: Engagement) -> Path:
    labels = _batch(eng)
    folder = eng.trace_dir / "close-sample"
    if folder.exists():
        raise ValueError("a sample already exists; keep the frozen draw, never reroll it")
    rng = random.SystemRandom()
    selected = []
    # A drafted fail and a drafted pass when available. Diversify the third
    # across stage, seat and invocation kind, randomizing ties and display order.
    for verdict in ("fail", "pass"):
        pool = [r for r in eng.records if labels[r.pass_id].verdict == verdict]
        if pool:
            selected.append(rng.choice(pool))
    while len(selected) < min(3, len(eng.records)):
        pool = [r for r in eng.records if r not in selected]
        def novelty(record):
            return sum(getattr(record, key) not in {getattr(r, key) for r in selected}
                       for key in ("stage", "seat", "kind"))
        best = max(map(novelty, pool))
        selected.append(rng.choice([r for r in pool if novelty(r) == best]))
    rng.shuffle(selected)
    draft = (eng.trace_dir / "labels.md").read_bytes()
    plan = {"id": str(uuid.uuid4()), "engagement": eng.id,
            "drawn_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "selected": [r.pass_id for r in selected], "batch_size": len(labels),
            "draft_sha256": _digest(draft), "evidence": _evidence(eng),
            "has_fail": any(row.verdict == "fail" for row in labels.values())}
    page = _blind_html(eng, plan)
    folder.mkdir()  # exclusive: a second draw must never replace the first
    (folder / "draft-labels.md").write_bytes(draft)
    (folder / "sample.json").write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    (folder / "blind.html").write_text(page, encoding="utf-8")
    return folder / "blind.html"


def compare(eng: Engagement) -> tuple[bool, Path]:
    folder = eng.trace_dir / "close-sample"
    target = folder / "comparison.md"
    if target.exists():
        raise ValueError("a comparison already exists; preserve it as review evidence")
    plan = json.loads((folder / "sample.json").read_text(encoding="utf-8"))
    if plan["engagement"] != eng.id:
        raise ValueError("this sample belongs to a different engagement")
    frozen = (folder / "draft-labels.md").read_bytes()
    if _digest(frozen) != plan["draft_sha256"]:
        raise ValueError("the frozen draft changed after the draw")
    if _digest((eng.trace_dir / "labels.md").read_bytes()) != plan["draft_sha256"]:
        raise ValueError("the batch labels changed after the draw; review the changed batch in full")
    _batch(eng)
    if _evidence(eng, plan["evidence"]["live_logs"]) != plan["evidence"]:
        raise ValueError("the records or source evidence changed after the draw; review the changed batch in full")
    text = (folder / "blind-labels.md").read_text(encoding="utf-8")
    if not text.startswith(f"<!-- close-sample: {plan['id']} -->\n"):
        raise ValueError("answers must come from this draw's blind page")
    human = parse_labels(text, stages=eng.studio.all_stage_numbers)
    if set(human) != set(plan["selected"]):
        raise ValueError("save exactly the sampled rows before comparing")
    for row in human.values():
        if not decided(row.verdict) or (row.verdict == "pass" and row.first_failing_stage is not None):
            raise ValueError(f"{row.pass_id}: a missing or deferred answer cannot clear the sample")
    draft = parse_labels(frozen.decode("utf-8"), stages=eng.studio.all_stage_numbers)
    disagreements = [pid for pid in plan["selected"]
                     if (human[pid].verdict, human[pid].first_failing_stage) !=
                        (draft[pid].verdict, draft[pid].first_failing_stage)]
    outcome = ("WIDER REVIEW REQUIRED — batch approval held. Sean reads the remaining rows himself "
               "or a fresh-context reader redrafts the whole batch for his review. Do not repair "
               "only the sampled rows and treat the batch as approved." if disagreements else
               "AGREEMENT — batch awaits Sean's approval. This small check does not establish "
               "that the unsampled rows are correct.")
    report = (f"# Close sample comparison — {eng.id}.\n\n{outcome}\n\n"
              f"Compared {len(human)} of {plan['batch_size']} rows. "
              "Agreement compares verdict and first failing stage; critique wording is not scored. "
              "Sean can require wider review over any substantive critique difference.\n\n")
    if not plan["has_fail"]:
        report += "No drafted fail was available; this sample did not check agreement on a fail.\n\n"
    report += ("Disagreements: " + (", ".join(disagreements) or "none") + ".\n\n"
               "## Sean's independent sample labels.\n\n" + HEADER +
               format_rows([human[pid] for pid in plan["selected"]]) +
               "\n\n## Frozen coordinator draft for those rows.\n\n" + HEADER +
               format_rows([draft[pid] for pid in plan["selected"]]) +
               "\n\n## Provenance.\n\n"
               f"Draw: {plan['id']}. Frozen at {plan['drawn_at']}.\n\n"
               "Only the sampled rows were independently read. Unsampled rows remain "
               "coordinator-drafted. Preserve that distinction in labels.md; never describe "
               "the whole batch as independently or blindly labeled. No labels or approval "
               "were changed by this comparison.\n")
    with target.open("x", encoding="utf-8") as out:
        out.write(report)
    return not disagreements, target


def _blind_html(eng: Engagement, plan: dict) -> str:
    """Receive only the draw ids, not coordinator label values or aggregates."""
    rows = []
    prompts = dict(eng.studio.review_prompts)
    options = "".join(f'<option value="{n}">{n} {esc(eng.studio.stage_name(n))}</option>'
                      for n in eng.studio.all_stage_numbers)
    for pid in plan["selected"]:
        record = eng.by_id[pid]
        refs = []
        for name, items in (("Inputs", record.inputs), ("Outputs", record.outputs)):
            links = []
            for ref in items:
                if not ref.path:
                    continue
                # Trials keep real artifacts in trace/trials/. The remaining
                # trace files and directory listings can disclose labels.
                path = eng.resolve(ref.path)
                in_trace = path and path.resolve().is_relative_to(eng.trace_dir.resolve())
                trial_artifact = path and path.resolve().is_relative_to((eng.trace_dir / "trials").resolve())
                if path and (path.is_dir() or (in_trace and not trial_artifact) or
                             path.name.startswith("labels") or
                             path.name in ("eval.html", "cases.md", "notes.md")):
                    continue
                href = os.path.relpath(path, eng.trace_dir / "close-sample") if path else ""
                label = (f'<a href="{esc(href)}" target="_blank" rel="noopener">{esc(ref.path)}</a>'
                         if href else esc(ref.path))
                links.append(f"<li>{label}<details><summary>Record fingerprint</summary>"
                             f"{esc(ref.sha256 or 'none recorded')}</details></li>")
            refs.append(f"<h3>{name}</h3><ul>{''.join(links) or '<li>No reviewable files linked.</li>'}</ul>")
        rows.append(f'''<section data-pass="{esc(pid)}">
<h2>{esc(run_line(pid, record.seat, record.kind, eng.studio))}</h2>
<p>{esc(prompts.get(record.kind, 'Read the work and its evidence. Does this pass meet its duty?'))}</p>
<p>Read the input and output files below. An overwritten output shows its current revision;
if you cannot judge the recorded pass from the available evidence, defer it.</p>
{''.join(refs)}
<fieldset><legend>Your independent label.</legend>
<label>Verdict <select data-verdict><option value="">Choose…</option><option value="pass">Pass</option>
<option value="fail">Fail</option><option value="defer">Defer — needs evidence</option></select></label>
<label>Where did the failure first enter? <select data-stage disabled><option value="">Choose…</option>{options}</select></label>
<label>Your reason <textarea data-critique rows="3"></textarea></label></fieldset></section>''')
    marker = f"<!-- close-sample: {plan['id']} -->\n" + HEADER
    script = r'''
const sections = [...document.querySelectorAll('[data-pass]')];
const status = document.querySelector('#status');
sections.forEach(section => {
  section.querySelector('[data-verdict]').addEventListener('change', () => {
    const fail = section.querySelector('[data-verdict]').value === 'fail';
    const stage = section.querySelector('[data-stage]');
    stage.disabled = !fail; if (!fail) stage.value = '';
  });
});
document.querySelector('#download').addEventListener('click', () => {
  const cell = text => text.replace(/\|/g, '\\|').replace(/[\r\n]+/g, ' ');
  const rows = [];
  for (const section of sections) {
    const verdict = section.querySelector('[data-verdict]').value;
    const stage = section.querySelector('[data-stage]').value;
    const critique = section.querySelector('[data-critique]').value.trim();
    if (!verdict || (verdict === 'fail' && (!stage || !critique))) {
      status.textContent = 'Give every run a verdict, and every fail a stage and reason.'; return;
    }
    rows.push('| ' + [section.dataset.pass, verdict, stage, critique, ''].map(cell).join(' | ') + ' |');
  }
  const url = URL.createObjectURL(new Blob([HEADER + rows.join('\n') + '\n'], {type: 'text/markdown'}));
  const link = document.createElement('a'); link.href = url; link.download = 'blind-labels.md'; link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  status.textContent = 'Answers downloaded. Place blind-labels.md beside this page, then run compare. A deferred row holds the comparison.';
});
'''
    # UUID and fixed header only: no engagement text is interpolated into JS.
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Blind Close review · {esc(eng.id)}</title><style>{_fonts_css()}{CSS}
body {{ padding: 2rem; max-width: 1000px; margin: auto; }}
section {{ border-top: 1px solid var(--ink-hairline); padding: 2rem 0; }}
fieldset {{ display: grid; gap: 1rem; margin-top: 1rem; }}
label {{ display: grid; gap: .5rem; }} textarea, select {{ font: inherit; padding: .5rem; }}
li {{ overflow-wrap: anywhere; }} button {{ margin-top: 1rem; }}
</style></head><body><h1>Blind Close review.</h1>
<p>{esc(eng.id)} · {len(plan['selected'])} runs to read independently.</p>
<p>Label these before opening the ordinary viewer or the coordinator's draft. If you already saw
the draft, tell the coordinator; do not describe these answers as blind. No drafted labels,
critiques, guided cases or label counts are included here. Your answers stay in this page
until downloaded; reloading clears them.</p>
{''.join(rows)}<button class="btn" id="download">Download my labels</button>
<p id="status" role="status">Save all answers before comparing. Nothing here approves the batch.</p>
<script>const HEADER = {json.dumps(marker)};{script}</script></body></html>'''
