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
import re
import uuid
from pathlib import Path, PurePosixPath

from .engagement import Engagement, Record, sha256_path
from .folders import split_named
from .labels import COLUMNS, Label, decided, format_rows, parse_labels
from .viewer import CSS, _fonts_css, _join, esc, run_line

HEADER = "| " + " | ".join(COLUMNS) + " |\n|---|---|---|---|---|\n"

# A run's job in plain words, by kind (SWCB #253). A profile's `kind_jobs` overrides or adds.
KIND_JOBS = {
    "draft": "making the first version of its stage's work",
    "repair": "reworking its own earlier version",
    "audit": "checking another seat's work for defects",
    "co-sign": "checking one named section of another seat's work",
    "gate": "reviewing the stage's finished work independently, before it goes to Sean",
    "trial": "doing the same job on a different model, from identical inputs, so the two can be compared",
    "intake": "checking whether a handed-over brief is complete enough to work from",
    "open": "setting up the engagement: the brief and the evidence it starts from",
    "readout": "writing the plain readout of the finished work for Sean",
    "close": "closing the engagement: the record checks, the open items and the drafted labels",
}
# Label views, guided cases and process notes can disclose the draft; the page neither links nor quotes them.
HIDDEN_NAMES = ("eval.html", "cases.md", "notes.md")
GIST_CHARS = 600


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


def _hidden(eng: Engagement, rel: str) -> bool:
    """A path the blind page neither links nor quotes.

    Trials keep real artifacts in trace/trials/. The remaining trace files and
    directory listings can disclose labels.
    """
    path = eng.resolve(rel)
    name = path.name if path else PurePosixPath(rel).name
    if name.startswith("labels") or name in HIDDEN_NAMES or (path and path.is_dir()):
        return True
    if path is None:
        return rel.startswith("trace/") and not rel.startswith("trace/trials/")
    trace = eng.trace_dir.resolve()
    return path.resolve().is_relative_to(trace) and not path.resolve().is_relative_to(trace / "trials")


def _plain_name(rel: str) -> str:
    """`artifacts/story-packet-r2.md` → `story packet, revision 2`; a file name a reader can say."""
    named = split_named(rel)
    if named is not None:
        parts = PurePosixPath(named[1]).parts
        return parts[-1] + (f", in the {named[0]} folder's {parts[-2]}" if len(parts) > 1 else f", in the {named[0]} folder")
    path = PurePosixPath(rel)
    stem = path.stem
    m = re.match(r"^d(\d+)-(.+)$", stem)
    if m:
        return f"decision entry d{m.group(1)}: {m.group(2).replace('-', ' ')}"
    m = re.match(r"^(?:\d+-)?(\d{4}-\d{2}-\d{2})-(.+)$", stem)   # 004-2026-01-31-house-style
    if m:
        return f"{m.group(2).replace('-', ' ')} ({m.group(1)})"
    m = re.match(r"^(.+)-r(\d+)$", stem)
    if m:
        return f"{m.group(1).replace('-', ' ')}, revision {m.group(2)}"
    if stem.lower() in ("index", "readme") and path.parent.name:
        return f"{path.parent.name} {stem.lower()}"
    return stem.replace("-", " ").replace("_", " ")


def _gist(text: str) -> tuple[str, str]:
    """(verdict, opening): a file's own `verdict:` line, and its `Means:` paragraph or first prose paragraph."""
    header, body = "", text
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            header, body = text[4:end], text[end + 4:]
    m = re.search(r"^verdict:\s*(.+?)\s*$", header, re.M)
    verdict = m.group(1).strip("\"'") if m else ""

    def plain(p: str) -> str:
        return " ".join(p.replace("**", "").replace("`", "").split())

    def items(block: str) -> list[str]:
        """A list's items, or a table's rows as `first cell: second cell`."""
        lines = [l.strip() for l in block.split("\n") if l.strip()]
        if lines[0].startswith("|"):
            rows = [[c.strip() for c in l.strip("|").split("|")] for l in lines[2:] if l.startswith("|")]
            return [plain(": ".join(r[:2])) for r in rows if r and r[0]]
        return [plain(l[2:]) for l in lines if l.startswith(("- ", "* "))]

    def sentences(parts: list[str]) -> str:
        return " ".join(p if p.endswith((".", "!", "?")) else p + "." for p in parts)

    blocks = [b.strip() for b in re.split(r"\n\s*\n", body) if b.strip()]
    opening = ""
    for i, block in enumerate(blocks):
        if plain(block).startswith("Means:"):
            opening, rest = plain(block.split("\n- ")[0]), blocks[i + 1:]
            break
    else:
        for i, block in enumerate(blocks):
            if block.startswith(("#", ">", "```", "<!--")) or plain(block) == verdict:
                continue
            if block.startswith(("|", "- ", "* ")):
                opening, rest = sentences(items(block)), []
            elif len(plain(block)) >= 40:
                opening, rest = plain(block.split("\n- ")[0]), blocks[i + 1:]
            if opening:
                break
    if not opening:
        return verdict, ""
    if opening.endswith(":"):   # the paragraph introduces a list: carry its items
        inline = block.split("\n- ", 1)
        tail = (items("- " + inline[1]) if len(inline) > 1 else
                items(rest[0]) if rest and rest[0].startswith(("- ", "* ", "|")) else [])
        if tail:
            opening += " " + sentences(tail)
    opening = opening.removeprefix("Means:").strip()
    if len(opening) > GIST_CHARS:
        cut = opening.rfind(". ", 0, GIST_CHARS)
        opening = opening[:cut + 1] if cut > GIST_CHARS // 3 else opening[:GIST_CHARS].rstrip() + "…"
    return verdict, opening


def _quote(eng: Engagement, rel: str, sha: str | None, writer: Record | None, verdicts_only: bool = False) -> str:
    """The file's verdict and opening, only when the disk still holds the revision the record names.

    Never quotes a hidden file, the brief, or anything the coordinator wrote: its
    Open and Close files can carry label totals and the drafter's reading. An
    input is quoted only when it is a finding (it carries a verdict), since that
    is what the run was answering; other earlier work is named, not quoted.
    """
    if (_hidden(eng, rel) or rel == eng.studio.brief_file or not rel.endswith(".md") or
            (writer is not None and writer.kind in eng.studio.coordinator_kinds)):
        return ""
    if sha and eng.hash_of(rel) not in (None, sha):
        return " The file has since been replaced by a later revision, so it is not quoted here."
    text = eng.read_text(rel)
    if text is None:
        return ""
    verdict, opening = _gist(text)
    if verdicts_only and not verdict:
        return ""
    out = f" Its verdict: <strong>{esc(verdict)}</strong>." if verdict else ""
    return out + (f' <q>{esc(opening)}</q>' if opening else "")


def plain_account(eng: Engagement, record: Record) -> str:
    """A short account of one pass from the records alone (SWCB #253): the step's job,
    what came in, what came out, what later checks found. No label, critique or
    record note: those are the drafter's words, and the reader is judging the drafter."""
    S = eng.studio
    by_id = eng.by_id
    order = [r.pass_id for r in eng.records]

    def run(pid: str) -> str:
        r = by_id.get(pid)
        return esc(run_line(pid, r.seat, r.kind, S)) if r else esc(pid)

    def runs(pids: list[str]) -> str:
        shown = [run(p) for p in pids[:4]]
        return _join(shown + ([f"{len(pids) - 4} more"] if len(pids) > 4 else []))

    writers: dict[tuple[str, str], Record] = {}
    for r in eng.records:
        for o in r.outputs:
            if o.path and o.sha256:
                writers.setdefault((o.path, o.sha256), r)
    here = order.index(record.pass_id)

    def writer_of(rel: str, sha: str | None) -> Record | None:
        w = writers.get((rel, sha or ""))
        return w if w is not None and order.index(w.pass_id) < here else None

    # ---- the step's job ------------------------------------------------------
    jobs = {**KIND_JOBS, **dict(S.kind_jobs)}
    who = S.seat_name(record.seat)
    where = f", at stage {record.stage} ({esc(S.stage_name(record.stage))})," if record.stage in S.stages else ","
    job = f"{esc(who)}{where} {esc(jobs.get(record.kind, f'a {record.kind} run'))}"
    if record.triggered_by:
        job += (f", after findings from {run(record.triggered_by)}" if record.kind == "repair"
                else f". It was launched in answer to {run(record.triggered_by)}")
    if record.shadow_of:
        job += f". It shadows {run(record.shadow_of)}"
    job += "."

    # ---- what came in --------------------------------------------------------
    came_in, others, unseen = [], [], 0
    standing: dict[str, list[str]] = {}
    instructions = False
    for ref in record.inputs:
        if not ref.path:
            continue
        w = writer_of(ref.path, ref.sha256)
        if ref.path == S.brief_file:
            came_in.insert(0, "<li>The engagement's brief.</li>")
        elif _hidden(eng, ref.path):
            if re.search(r"\.(task|prompt)\.", ref.path):
                instructions = True
            else:
                unseen += 1
        elif w is not None:
            came_in.append(f"<li><strong>{esc(_plain_name(ref.path))}</strong>, made by {run(w.pass_id)}."
                           f"{_quote(eng, ref.path, ref.sha256, w, verdicts_only=True)}</li>")
        elif any(ref.path.startswith(p) for p in S.repo_prefixes):
            folder = PurePosixPath(ref.path).parent.name
            standing.setdefault(folder, []).append(_plain_name(ref.path))
        else:
            others.append(_plain_name(ref.path))
    if others:
        came_in.append(f"<li>Other files: {esc('; '.join(others))}.</li>")
    if standing:
        n = sum(map(len, standing.values()))
        came_in.append(f"<li>{n} standing studio file{'s' if n > 1 else ''}, kept outside this engagement: "
                       + esc("; ".join(f"{k}: {', '.join(v)}" for k, v in standing.items())) + ".</li>")
    if instructions:
        came_in.append("<li>The task the coordinator wrote for this run.</li>")
    if unseen:
        came_in.append(f"<li>{unseen} trace file{'s' if unseen > 1 else ''} this page does not show.</li>")

    # ---- what came out -------------------------------------------------------
    came_out, withheld = [], 0
    for o in record.outputs:
        if not o.path:
            continue
        if _hidden(eng, o.path):
            withheld += 1
            continue
        state = eng.output_state(o)
        line = ("<li>The engagement's brief, updated." if o.path == S.brief_file else
                f"<li><strong>{esc(_plain_name(o.path))}</strong>.")
        if state in ("missing", "not-set-up"):
            line += " It is not on this machine."
        else:
            line += _quote(eng, o.path, o.sha256, record)
        readers = [r.pass_id for r in eng.records[here + 1:]
                   if any(i.path == o.path and i.sha256 == o.sha256 for i in r.inputs)]
        if readers:
            line += f" Read next by {runs(readers)}."
        came_out.append(line + "</li>")
    if withheld:
        came_out.append(f"<li>{withheld} trace file{'s' if withheld > 1 else ''} this page does not show.</li>")

    # ---- what later checks found ---------------------------------------------
    later = []
    for c in record.checks:
        checker = by_id.get(c.pass_id)
        line = f"<li>{run(c.pass_id)}: <strong>{esc(c.verdict)}</strong>."
        own = [o for o in (checker.outputs if checker and checker.kind not in S.coordinator_kinds else [])
               if o.path and o.path.startswith(S.checks_dir + "/") and not _hidden(eng, o.path)
               and eng.hash_of(o.path) == o.sha256]
        if own:
            _, opening = _gist(eng.read_text(own[0].path) or "")
            line += f" <q>{esc(opening)}</q>" if opening else ""
        later.append(line + "</li>")
    checked_by = {c.pass_id for c in record.checks}
    answered = [r.pass_id for r in eng.records if r.triggered_by == record.pass_id and r.pass_id not in checked_by]
    if answered:
        later.append(f"<li>Launched in answer to this run: {runs(answered)}.</li>")
    if not later:
        later.append("<li>No later run checked this work, and none was launched in answer to it.</li>")

    none = "<li>None recorded.</li>"
    return (f'<p class="job"><strong>The step\'s job.</strong> {job}</p>'
            f"<h3>What came in.</h3><ul>{''.join(came_in) or none}</ul>"
            f"<h3>What came out.</h3><ul>{''.join(came_out) or none}</ul>"
            f"<h3>What later checks found.</h3><ul>{''.join(later)}</ul>")


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
                if not ref.path or _hidden(eng, ref.path):
                    continue
                path = eng.resolve(ref.path)
                href = os.path.relpath(path, eng.trace_dir / "close-sample") if path else ""
                label = (f'<a href="{esc(href)}" target="_blank" rel="noopener">{esc(ref.path)}</a>'
                         if href else esc(ref.path))
                links.append(f"<li>{label}</li>")
            refs.append(f"<h4>{name}.</h4><ul>{''.join(links) or '<li>No reviewable files linked.</li>'}</ul>")
        rows.append(f'''<section data-pass="{esc(pid)}">
<h2>{esc(run_line(pid, record.seat, record.kind, eng.studio))}.</h2>
{plain_account(eng, record)}
<p class="ask"><strong>Your question.</strong> {esc(prompts.get(record.kind, 'Read the work and its evidence. Does this pass meet its duty?'))}</p>
<details><summary>More details: open the files yourself.</summary>
<p>A file that a later run overwrote opens at its current revision. If you cannot judge
the recorded run from what is here, defer it.</p>
{''.join(refs)}</details>
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
li {{ overflow-wrap: anywhere; margin-bottom: .5rem; }} button {{ margin-top: 1rem; }}
q {{ font-style: italic; }} .ask {{ margin-top: 1.5rem; }}
</style></head><body><h1>Blind Close review.</h1>
<p class="lead">{len(plan['selected'])} runs from {esc(eng.id)} to judge on your own: read each short account,
then answer pass or fail.</p>
<p>Each account is built from the run records alone: the step's job, what came in, what came out,
and what the later checks found. Quotes are the seats' own words from their files. Nothing here
comes from the coordinator's draft: no drafted labels, critiques, notes or counts.</p>
<details><summary>More details: the blind rule.</summary>
<p>Label these before opening the ordinary viewer or the coordinator's draft. If you already saw
the draft, tell the coordinator; do not describe these answers as blind. Your answers stay in
this page until downloaded; reloading clears them.</p></details>
{''.join(rows)}<button class="btn" id="download">Download my labels</button>
<p id="status" role="status">Save all answers before comparing. Nothing here approves the batch.</p>
<script>const HEADER = {json.dumps(marker)};{script}</script></body></html>'''
