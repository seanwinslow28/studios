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

Rung-0 line 8 checks that a full train ran its own shape: per stage reached, one
draft by the stage's seat and at least one audit by its fixed auditor; no motion
draft before the appearance gate; and, once the engagement has closed, all three
gates on the record. A small piece takes only the motion gate; its shape is
checked once the master skill design rules it, and until then line 8 says it is
unchecked. Its taxonomy file (`taxonomy.md`, beside this one) is empty until
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
    "A stage missing its draft or its audit, motion drafted before the appearance gate, or a closed train missing a gate, is a film that did not run its own shape.",
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
    structure_check_name="Each stage has its draft and its audit, motion comes after the appearance gate, and a closed train ran all three gates",
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


def _stages(eng: Engagement) -> Check:
    """Motioncraft's structure line: the full train's shape.

    Per stage reached, exactly one draft by the stage's seat and at least one audit by its fixed
    auditor. An appearance-gate pass launches before the motion draft. Once the engagement has a
    close pass, the story, appearance and motion gates are all on the record. A small piece, or any
    other type, is not yet asserted, and says so. Launch order is the pass number.
    """
    c = Check(eng.studio.structure_check_name)
    names = eng.studio.stage_name
    etype = str(eng.brief.get("type") or "").lower().strip()
    if etype and etype not in FULL_TRAIN_TYPES:
        c.notes.append(f"engagement type is {etype}: unchecked until the master skill design rules its shape")
        return c
    if not etype:
        c.notes.append(f"{eng.studio.brief_file} names no type; asserting the full-train structure")
    stages = sorted({r.stage for r in eng.records if 1 <= r.stage <= 4})
    c.n_total = len(stages)
    first_draft: dict[int, int] = {}
    for s in stages:
        ok = True
        rs = [r for r in eng.records if r.stage == s]
        drafts = [r for r in rs if r.kind == "draft"]
        if len(drafts) != 1:
            c.findings.append(f"stage {s} {names(s)}: {len(drafts)} drafts, expected exactly one (repairs are `kind: repair`)")
            ok = False
        elif drafts[0].seat != STAGE_SEATS[s]:
            c.findings.append(f"stage {s}: draft by {drafts[0].seat}; the drafting seat is {STAGE_SEATS[s]}")
            ok = False
        if drafts:
            first_draft[s] = min(_pass_no(r.pass_id) for r in drafts)
        audits = [r for r in rs if r.kind == "audit"]
        if not audits:
            c.findings.append(f"stage {s} {names(s)}: no audit pass (the fixed auditor is {FIXED_AUDITORS[s]})")
            ok = False
        for a in audits:
            if a.seat != FIXED_AUDITORS[s]:
                c.findings.append(f"stage {s}: audit by {a.seat}; the fixed auditor is {FIXED_AUDITORS[s]}")
                ok = False
        c.n_ok += 1 if ok else 0
    motion = first_draft.get(MOTION_STAGE)
    if motion is not None:
        appearance_gates = [_pass_no(r.pass_id) for r in eng.records if r.seat == "appearance-gate" and r.kind == "gate"]
        if not appearance_gates or min(appearance_gates) > motion:
            c.findings.append(f"stage {MOTION_STAGE} {names(MOTION_STAGE)}: drafted before the appearance gate ran")
    if any(r.kind == "close" for r in eng.records):
        for seat, stage in GATE_STAGES.items():
            if not any(r.seat == seat and r.kind == "gate" for r in eng.records):
                c.findings.append(f"closed with no {eng.studio.seat_name(seat).lower()} pass (anchor: stage {stage} {names(stage)})")
    missing = [s for s in range(1, 5) if s not in stages]
    if missing:
        c.notes.append(f"stages not yet reached: {', '.join(str(s) for s in missing)}")
    return c


STRUCTURE_CHECKS[STUDIO.key] = _stages
