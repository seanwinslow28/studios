"""Motioncraft's studio profile — the one file the shared trace kit reads to know this studio.

Written at scaffold on the Motioncraft build map (2026-10-17), from the bench
the research briefs ruled: four seats, one closed audit cycle, three craft gates
on a full train. Motioncraft traces from its first engagement, mc-eng-001, on.
Engagement ids are `mc-eng-NNN`, ledger entries `mc-eng-NNN.dNN`.

The shape: the four seats in their running order on a full train. Stage 1 Story
(the Visual Story Director's boards, animatic and shot list), stage 2 Appearance
(the Art and Pose Designer's appearance packet), stage 3 Motion (the Animator's
moving scene and its evidence pack), stage 4 Finish (Finishing and Sound's
conform, composite, grade, mix, delivery package and check record). The audit
cycle is Director → Art → Animator → Finishing → Director, the arrow reading
"audits", so each stage's fixed auditor is the seat before it in that cycle:
Finishing audits the Director's story, the Director audits Art's appearance
packet, Art audits the Animator's motion, the Animator audits Finishing's cut.
No seat co-signs.

The kinds a Motioncraft engagement produces: the shared draft, audit, gate,
repair and trial; `intake`, the handoff modifier's check on a brief arriving
from Scriptcraft; and the coordinator's open and close. Draft, repair and trial
hand an artifact forward and own `## Moves`. Gate passes carry the stage of
their anchor: the story gate sits at stage 1 (the animatic), the appearance gate
at stage 2 (the appearance packet, the assembled frame attached as proof), the
motion gate at stage 3 (the moving test and its one directed revision).

Rung-0 line 8 reads the engagement's `type:`, the master skill's three types
(ruled on the build map's Master skill design ticket, 2026-10-18; written on
Write the master skill). A full train: per stage reached, one draft by the
stage's seat and at least one audit by its fixed auditor; no motion draft before
the appearance gate; and, once the engagement has closed, all three gates on the
record. A train split into parts (the brief's `parts:` list, split by approval
state, never by halves of the film) counts one draft per part at stages 2 and 3,
each record naming its `part:`, its fixed auditor on each, every part's
appearance gate before any motion draft, and by Close an appearance gate and a
motion gate per part. A small piece: no stage 1 or 2 pass and no story or
appearance gate (both are recorded NOT FIRED in the brief, never run); the
Animator's draft, Art's audit, the motion gate before Finishing drafts, then
Finishing's draft and the Animator's audit; a stage not yet reached is a note
until Close, then a finding. A one-off is one seat pass with no order to check,
and line 8 says so. Its taxonomy file (`taxonomy.md`, beside this one) is empty until
Motioncraft's own labels earn a seat mode; the shared process-waste family is
the kit's.

The kit finds this file by walking up from an engagement folder, so
`python3 craftwork/trace/check.py motioncraft/ledger/engagements/<eng-id>` needs
no flag. Loading it registers the structure check.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Optional

HERE = Path(__file__).resolve().parent
KIT_DIR = HERE.parents[1] / "craftwork" / "trace"
try:
    import tracekit  # noqa: F401
except ModuleNotFoundError:
    sys.path.insert(0, str(KIT_DIR))

from tracekit.checker import STRUCTURE_CHECKS, Check  # noqa: E402
from tracekit.engagement import Engagement  # noqa: E402
from tracekit.studio import Studio  # noqa: E402

__all__ = ["STUDIO", "MOTIONCRAFT", "MOTIONCRAFT_CHECK_IMPLICATIONS", "STAGE_SEATS", "FIXED_AUDITORS", "GATE_STAGES"]

MOTIONCRAFT_CHECK_IMPLICATIONS = (
    "A record that will not parse cannot be checked at all, so treat that pass's line on this page as unread.",
    "A pass with no record is work this page cannot show you.",
    "A pass with no row is unfinished review, not a pass.",
    "A hash that no longer matches means the file on disk is not the one the seat read, so a quotation into it may point at different words.",
    "A cited corpus file the transcript never opened means the citation was not read when it was made.",
    "A move that names nothing upstream means the artifact's history does not add up; an unverifiable move is one an overwritten revision took with it.",
    "An unmeasured pass costs the reading nothing; it only means the token figures here are a subtotal.",
    "A stage or part missing its draft or its audit, motion drafted before the appearance gate, a closed train missing a gate, or a small piece that ran a stage it has none of, is a film that did not run its own shape.",
    "A blind pair whose runtime is already visible cannot produce an unbiased verdict.",
    "A failure code outside the taxonomy is free text, and free text does not count toward a mode.",
    "A pass whose logs name a different model ran on something the registry never ruled, so its row counts toward the wrong runtime; a pass that started a helper agent did work no record shows and no meter counted.",
)

# the running order on a full train: stage → drafting seat
STAGE_SEATS = {1: "visual-story-director", 2: "art-pose-designer", 3: "animator", 4: "finishing-sound-designer"}
# the closed audit cycle, Director → Art → Animator → Finishing → Director: stage → the seat that audits it
FIXED_AUDITORS = {1: "finishing-sound-designer", 2: "visual-story-director", 3: "art-pose-designer", 4: "animator"}
# the gates on a full train: gate seat → the stage of its anchor
GATE_STAGES = {"story-gate": 1, "appearance-gate": 2, "motion-gate": 3}
MOTION_STAGE = 3

FULL_TRAIN_TYPES = ("full-train", "full train")
SMALL_PIECE_TYPES = ("small-piece", "small piece")
ONE_OFF_TYPES = ("one-off", "one off")
# the stages a train in parts drafts once per part: Appearance and Motion; the animatic and the cut stay whole
PART_STAGES = (2, 3)

STUDIO = Studio(
    key="motioncraft",
    name="Motioncraft",
    stages={1: "Story", 2: "Appearance", 3: "Motion", 4: "Finish"},
    kinds=("draft", "audit", "gate", "repair", "trial", "intake", "open", "close"),
    forward_kinds=("draft", "repair", "trial"),
    coordinator_kinds=("open", "close"),
    coordinator_stage=0,
    coordinator_label="open · close",
    gate_seats=("story-gate", "appearance-gate", "motion-gate"),
    seat_names={
        "visual-story-director": "Director", "art-pose-designer": "Art", "animator": "Animator",
        "finishing-sound-designer": "Finishing", "coordinator": "Coordinator",
        "story-gate": "Story gate", "appearance-gate": "Appearance gate", "motion-gate": "Motion gate",
    },
    repo_prefixes=("motioncraft/", "craftwork/", ".claude/"),
    corpus_path_re=re.compile(r"(?<![\w/])((?:motioncraft/)?corpus/[\w\-./]+?\.md)"),
    id_re=None,                        # shot ids, beat ids and finding ids read in the kit's default shape
    taxonomy_path=HERE / "taxonomy.md",
    shared_taxonomy=True,
    withheld_required="the drafting conversation",
    brief_file="brief.md",
    checks_dir="audits",               # audits, gate findings and the check record sit in audits/
    structure_check_name="The film ran its type's shape: each stage its draft and its audit, motion after the appearance gate, every gate its type owes by Close",
    check_implications=MOTIONCRAFT_CHECK_IMPLICATIONS,
    review_prompts=(
        ("draft", "Does its work answer the assigned question within the evidence and constraints?"),
        ("audit", "Is the claimed defect supported, consequential, and explained well enough to act on?"),
        ("repair", "Does the new version resolve the identified issue without creating a material contradiction?"),
        ("gate", "Are verification, residuals, and decision authority clear?"),
        ("intake", "Can the seat do its job from this packet, and does the state it issued follow from the gaps it named?"),
    ),
    review_prompts_version="v1 · 2026-10-17",
    root_markers=("motioncraft", ".claude"),
)
MOTIONCRAFT = STUDIO


def _pass_no(pass_id: str) -> int:
    m = re.search(r"\d+", pass_id or "")
    return int(m.group(0)) if m else 0


def _part(r) -> str:
    """The part a record belongs to, from its optional `part:` field; empty on an unsplit train."""
    return str(r.raw.get("part") or "").strip()


def _parts(eng: Engagement) -> list[str]:
    """The brief's `parts:` list, by name; empty when the train runs unsplit."""
    raw = eng.brief.get("parts") or []
    if isinstance(raw, str):
        raw = [raw]
    return [str(p).strip() for p in raw if str(p).strip()]


def _stages(eng: Engagement) -> Check:
    """Motioncraft's structure line: the shape the engagement's type owes.

    A small piece and a one-off have their own branches, below. On a full train (or a brief that
    names no type): per stage reached, exactly one draft by the stage's seat and at least one audit
    by its fixed auditor; an appearance-gate pass launches before the motion draft; once the
    engagement has a close pass, the story, appearance and motion gates are all on the record. A
    train in parts counts stages 2 and 3 per part instead. Launch order is the pass number.
    """
    c = Check(eng.studio.structure_check_name)
    etype = str(eng.brief.get("type") or "").lower().strip()
    if etype in SMALL_PIECE_TYPES:
        return _small_piece(eng, c)
    if etype in ONE_OFF_TYPES:
        c.notes.append(f"engagement type is {etype}: one seat pass, no order to check, the stage structure is not asserted")
        return c
    if etype and etype not in FULL_TRAIN_TYPES:
        c.notes.append(f"engagement type is {etype}: not one of the master skill's types, the stage structure is not asserted")
        return c
    if not etype:
        c.notes.append(f"{eng.studio.brief_file} names no type; asserting the full-train structure")
    parts = _parts(eng)
    names = eng.studio.stage_name
    stages = sorted({r.stage for r in eng.records if 1 <= r.stage <= 4})
    first_draft: dict[int, int] = {}
    for s in stages:
        rs = [r for r in eng.records if r.stage == s]
        if parts and s in PART_STAGES:
            for p in parts:
                c.n_total += 1
                n = _drafted_and_audited(c, eng, s, [r for r in rs if _part(r) == p], f" part {p}")
                c.n_ok += n is not None
                if n is not None:
                    first_draft[s] = min(first_draft.get(s, n), n)
            for r in rs:
                if _part(r) not in parts and r.kind in ("draft", "audit", "repair"):
                    c.findings.append(f"{r.pass_id}: {eng.studio.seat_name(r.seat)} {r.kind} at stage {s} names "
                                      f"part {_part(r) or '(none)'}; the brief's parts are {', '.join(parts)}")
            continue
        c.n_total += 1
        n = _drafted_and_audited(c, eng, s, rs, "")
        c.n_ok += n is not None
        if n is not None:
            first_draft[s] = n
    motion = min((_pass_no(r.pass_id) for r in eng.records if r.stage == MOTION_STAGE and r.kind == "draft"), default=None)
    if motion is not None:
        gates = [r for r in eng.records if r.seat == "appearance-gate" and r.kind == "gate"]
        for p in parts or [None]:
            mine = [_pass_no(r.pass_id) for r in gates if p is None or _part(r) == p]
            if not mine or min(mine) > motion:
                where = f" part {p}'s" if p else " the"
                c.findings.append(f"stage {MOTION_STAGE} {names(MOTION_STAGE)}: drafted before{where} appearance gate ran")
    if any(r.kind == "close" for r in eng.records):
        for seat, stage in GATE_STAGES.items():
            gates = [r for r in eng.records if r.seat == seat and r.kind == "gate"]
            per_part = parts if parts and stage in PART_STAGES else [None]
            for p in per_part:
                if not any(p is None or _part(r) == p for r in gates):
                    of = f" for part {p}" if p else ""
                    c.findings.append(f"closed with no {eng.studio.seat_name(seat).lower()} pass{of} (anchor: stage {stage} {names(stage)})")
    missing = [s for s in range(1, 5) if s not in stages]
    if missing:
        c.notes.append(f"stages not yet reached: {', '.join(str(s) for s in missing)}")
    return c


def _drafted_and_audited(c: Check, eng: Engagement, stage: int, rs: list, label: str) -> Optional[int]:
    """Exactly one draft at `stage` by its seat and at least one audit by its fixed auditor, among `rs`.

    Returns the draft's pass number when both hold, else None; each gap is a finding.
    """
    names = eng.studio.stage_name
    ok = True
    drafts = [r for r in rs if r.kind == "draft"]
    n = None
    if len(drafts) != 1:
        c.findings.append(f"stage {stage} {names(stage)}{label}: {len(drafts)} drafts, expected exactly one (repairs are `kind: repair`)")
        ok = False
    elif drafts[0].seat != STAGE_SEATS[stage]:
        c.findings.append(f"stage {stage}{label}: draft by {drafts[0].seat}; the drafting seat is {STAGE_SEATS[stage]}")
        ok = False
    else:
        n = _pass_no(drafts[0].pass_id)
    audits = [r for r in rs if r.kind == "audit"]
    if not audits:
        c.findings.append(f"stage {stage} {names(stage)}{label}: no audit pass (the fixed auditor is {FIXED_AUDITORS[stage]})")
        ok = False
    for a in audits:
        if a.seat != FIXED_AUDITORS[stage]:
            c.findings.append(f"stage {stage}{label}: audit by {a.seat}; the fixed auditor is {FIXED_AUDITORS[stage]}")
            ok = False
    return n if ok else None


def _small_piece(eng: Engagement, c: Check) -> Check:
    """A small piece's shape: Animator drafts → Art audits → motion gate → Finishing drafts → Animator audits.

    The look is approved and the staging given, so nothing runs at stages 1 or 2 and neither the
    story nor the appearance gate runs (the brief records both NOT FIRED). Each of stages 3 and 4 has
    one draft by its seat and an audit by its fixed auditor launched after it; a motion-gate pass
    launches after the motion draft and before Finishing's draft; by Close both stages and the motion
    gate are on the record. A stage not yet reached is a note until Close, then a finding.
    """
    names = eng.studio.stage_name
    closed = any(r.kind == "close" for r in eng.records)
    for r in eng.records:
        if r.stage in (1, 2) or r.seat in ("story-gate", "appearance-gate"):
            c.findings.append(f"{r.pass_id}: {eng.studio.seat_name(r.seat)} {r.kind} on a small piece, which takes no story "
                              "or appearance stage and no gate but the motion gate; one that needs them is a full train")
    drafted: dict[int, Optional[int]] = {}
    for s in (MOTION_STAGE, 4):
        rs = [r for r in eng.records if r.stage == s]
        if not rs and not closed:
            c.notes.append(f"stage {s} {names(s)} not yet reached")
            continue
        c.n_total += 1
        n = _drafted_and_audited(c, eng, s, rs, "")
        if n is not None:
            early = [a.pass_id for a in rs if a.kind == "audit" and _pass_no(a.pass_id) < n]
            if early:
                c.findings.append(f"stage {s}: {', '.join(early)} audits before the draft it audits")
                n = None
        drafted[s] = n
        c.n_ok += n is not None
    gates = sorted(_pass_no(r.pass_id) for r in eng.records if r.seat == "motion-gate" and r.kind == "gate")
    motion, finish = drafted.get(MOTION_STAGE), drafted.get(4)
    if motion is not None and gates and gates[0] < motion:
        c.findings.append(f"motion gate pass-{gates[0]:02d} runs before the motion draft it gates")
    if finish is not None and not any(motion is not None and motion < g < finish for g in gates):
        c.findings.append(f"stage 4 {names(4)}: drafted before the motion gate ran on the moving test")
    if closed and not gates:
        c.findings.append(f"closed with no motion gate pass (anchor: stage {MOTION_STAGE} {names(MOTION_STAGE)})")
    return c


STRUCTURE_CHECKS[STUDIO.key] = _stages
