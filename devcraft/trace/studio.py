"""Devcraft's studio profile — the one file the shared trace kit reads to know this studio.

Written at scaffold on the Devcraft build map (2026-10-08), from the bench ruled
that day: four seats, one closed audit cycle, two gates on a full build. Devcraft
traces from its first engagement, dc-eng-001, on. Engagement ids are
`dc-eng-NNN`, ledger entries `dc-eng-NNN.dNN`.

The shape: the four seats in their running order on a full build, not in seat
order. Stage 1 Plan (the Build Planner's build plan), stage 2 Tests (the
Verifier's suite, written and shown failing before any code), stage 3 Code (the
Builder's change), stage 4 Release (Release & Reliability's release plan and
runbook). The audit cycle is Planner → Builder → Release → Verifier → Planner,
the arrow reading "audits", so each stage's fixed auditor is the seat before it
in that cycle. No seat co-signs.

The kinds a Devcraft engagement produces: the shared draft, audit, gate, repair
and trial; `intake`, the handoff modifier's check on a brief arriving from
Productcraft or Systemcraft; `run`, the Verifier's final run of its suite
against the merge candidate, which revises the test record that Release audits
and so hands an artifact forward; and the coordinator's open and close. Gate
passes carry the stage of their anchor: the plan gate sits at stage 1 (the build
plan), the release gate at stage 4 (the release plan), and the extra security
pass, which fires only on a plan that rates its surface high, at stage 3 (the
code change). The security pass is a protocol, never a seat; it is drawn as a
gate so its record has a lane.

Rung-0 line 8 checks that an engagement ran its type's shape (the master skill's
table, `.claude/skills/devcraft/SKILL.md`). A full build: per stage reached, one
draft by the stage's seat and at least one audit by its fixed auditor; the tests
drafted before the code; the plan gate run before the code; and, once the
engagement has closed, both gates on the record. A small ask: no plan and no plan
gate; one tests draft by the Verifier before one code draft by the Builder; the
Build Planner's one audit after the code, reading the tests too; and, by Close,
the Verifier's final run after that audit, plus Release's draft, the Builder's
audit of it and the release gate when the release gate fired. An ops-only ask:
Release's draft alone, the Builder's audit of it, and by Close the release gate.
A one-off is a single seat pass with no order to check, and says so. Its taxonomy file
(`taxonomy.md`, beside this one) is empty until Devcraft's own labels earn a
seat mode; the shared process-waste family is the kit's.

The kit finds this file by walking up from an engagement folder, so
`python3 craftwork/trace/check.py devcraft/ledger/engagements/<eng-id>` needs no
flag. Loading it registers the structure check.
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

__all__ = ["STUDIO", "DEVCRAFT", "DEVCRAFT_CHECK_IMPLICATIONS", "STAGE_SEATS", "FIXED_AUDITORS", "GATE_STAGES"]

DEVCRAFT_CHECK_IMPLICATIONS = (
    "A record that will not parse cannot be checked at all, so treat that pass's line on this page as unread.",
    "A pass with no record is work this page cannot show you.",
    "A pass with no row is unfinished review, not a pass.",
    "A hash that no longer matches means the file on disk is not the one the seat read, so a quotation into it may point at different words.",
    "A cited corpus file the transcript never opened means the citation was not read when it was made.",
    "A move that names nothing upstream means the artifact's history does not add up; an unverifiable move is one an overwritten revision took with it.",
    "An unmeasured pass costs the reading nothing; it only means the token figures here are a subtotal.",
    "A stage missing its draft or its audit, code drafted before its tests or its plan gate, or a closed build missing a gate, is a build that did not run its own shape.",
    "A blind pair whose runtime is already visible cannot produce an unbiased verdict.",
    "A failure code outside the taxonomy is free text, and free text does not count toward a mode.",
    "A pass whose transcript names a different model ran on something the registry never ruled, so its row counts toward the wrong runtime.",
)

# the running order on a full build: stage → drafting seat
STAGE_SEATS = {1: "build-planner", 2: "verifier", 3: "builder", 4: "release-reliability"}
# the closed audit cycle, Planner → Builder → Release → Verifier → Planner: stage → the seat that audits it
FIXED_AUDITORS = {1: "verifier", 2: "release-reliability", 3: "build-planner", 4: "builder"}
# the gates on a full build: gate seat → the stage of its anchor
GATE_STAGES = {"plan-gate": 1, "release-gate": 4}
CODE_STAGE = 3
TESTS_STAGE = 2

FULL_BUILD_TYPES = ("full-build", "full build")
SMALL_ASK_TYPES = ("small-ask", "small ask")
OPS_ONLY_TYPES = ("ops-only", "ops only")

STUDIO = Studio(
    key="devcraft",
    name="Devcraft",
    stages={1: "Plan", 2: "Tests", 3: "Code", 4: "Release"},
    kinds=("draft", "audit", "gate", "repair", "trial", "run", "intake", "open", "close"),
    forward_kinds=("draft", "repair", "trial", "run"),
    coordinator_kinds=("open", "close"),
    coordinator_stage=0,
    coordinator_label="open · close",
    gate_seats=("plan-gate", "release-gate", "security-pass"),
    seat_names={
        "build-planner": "Planner", "verifier": "Verifier", "builder": "Builder",
        "release-reliability": "Release", "coordinator": "Coordinator",
        "plan-gate": "Plan gate", "release-gate": "Release gate", "security-pass": "Security pass",
    },
    repo_prefixes=("devcraft/", "productcraft/", "systemcraft/", "craftwork/", ".claude/"),
    corpus_path_re=re.compile(r"(?<![\w/])((?:devcraft/)?corpus/[\w\-./]+?\.md)"),
    id_re=None,                        # plan criteria, story ids and hold ids read in the kit's default shape
    taxonomy_path=HERE / "taxonomy.md",
    shared_taxonomy=True,
    withheld_required="the drafting conversation",
    brief_file="brief.md",
    checks_dir="audits",               # audits, gate findings and the security pass sit in audits/
    structure_check_name="The engagement ran its type's shape: each stage its draft and its audit, tests before the code, and the gates its type owes",
    check_implications=DEVCRAFT_CHECK_IMPLICATIONS,
    review_prompts=(
        ("draft", "Does its work answer the assigned question within the evidence and constraints?"),
        ("audit", "Is the claimed defect supported, consequential, and explained well enough to act on?"),
        ("repair", "Does the new version resolve the identified issue without creating a material contradiction?"),
        ("run", "Is every result real output against the named commit, with no test skipped and the test files unchanged?"),
        ("gate", "Are verification, residuals, and decision authority clear?"),
        ("intake", "Can the seat do its job from this packet, and does the state it issued follow from the gaps it named?"),
    ),
    review_prompts_version="v1 · 2026-10-08",
    root_markers=("devcraft", ".claude"),
)
DEVCRAFT = STUDIO


def _pass_no(pass_id: str) -> int:
    m = re.search(r"\d+", pass_id or "")
    return int(m.group(0)) if m else 0


def _stages(eng: Engagement) -> Check:
    """Devcraft's structure line: the full build's shape.

    Per stage reached, exactly one draft by the stage's seat and at least one audit by its fixed
    auditor. The tests' draft launches before the code's draft (the Verifier writes them first),
    and a plan-gate pass launches before the code's draft. Once the engagement has a close pass,
    both the plan gate and the release gate are on the record. A small ask and an ops-only ask
    have their own shapes, below; a one-off is not asserted, said so. Launch order is the pass
    number.
    """
    c = Check(eng.studio.structure_check_name)
    names = eng.studio.stage_name
    etype = str(eng.brief.get("type") or "").lower().strip()
    if etype in SMALL_ASK_TYPES:
        return _small_ask(eng, c)
    if etype in OPS_ONLY_TYPES:
        return _ops_only(eng, c)
    if etype and etype not in FULL_BUILD_TYPES:
        c.notes.append(f"engagement type is {etype}: one seat pass, no order to check, the stage structure is not asserted")
        return c
    if not etype:
        c.notes.append(f"{eng.studio.brief_file} names no type; asserting the full-build structure")
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
    code = first_draft.get(CODE_STAGE)
    if code is not None:
        tests = first_draft.get(TESTS_STAGE)
        if tests is None or tests > code:
            c.findings.append(f"stage {CODE_STAGE} {names(CODE_STAGE)}: drafted before any tests draft; the Verifier writes the tests first")
        plan_gates = [_pass_no(r.pass_id) for r in eng.records if r.seat == "plan-gate" and r.kind == "gate"]
        if not plan_gates or min(plan_gates) > code:
            c.findings.append(f"stage {CODE_STAGE} {names(CODE_STAGE)}: drafted before the plan gate ran")
    if any(r.kind == "close" for r in eng.records):
        for seat, stage in GATE_STAGES.items():
            if not any(r.seat == seat and r.kind == "gate" for r in eng.records):
                c.findings.append(f"closed with no {eng.studio.seat_name(seat).lower()} pass (anchor: stage {stage} {names(stage)})")
    missing = [s for s in range(1, 5) if s not in stages]
    if missing:
        c.notes.append(f"stages not yet reached: {', '.join(str(s) for s in missing)}")
    return c




def _one_draft(c: Check, eng: Engagement, stage: int) -> Optional[int]:
    """Exactly one draft at `stage`, by its seat; returns its pass number, or None."""
    names = eng.studio.stage_name
    drafts = [r for r in eng.records if r.stage == stage and r.kind == "draft"]
    if len(drafts) != 1:
        c.findings.append(f"stage {stage} {names(stage)}: {len(drafts)} drafts, expected exactly one (repairs are `kind: repair`)")
        return None
    if drafts[0].seat != STAGE_SEATS[stage]:
        c.findings.append(f"stage {stage}: draft by {drafts[0].seat}; the drafting seat is {STAGE_SEATS[stage]}")
        return None
    return _pass_no(drafts[0].pass_id)


def _release_leg(c: Check, eng: Engagement, closed: bool, owed: bool) -> bool:
    """Release's draft, the Builder's audit of it after the draft, and, once closed, the release gate.

    `owed` says the type always runs this leg (ops-only); otherwise it is checked only once reached.
    Returns whether the leg is whole so far.
    """
    names = eng.studio.stage_name
    s = 4
    reached = any(r.stage == s for r in eng.records)
    gates = [_pass_no(r.pass_id) for r in eng.records if r.seat == "release-gate" and r.kind == "gate"]
    if not reached and not gates:
        if owed and closed:
            c.findings.append(f"closed with no stage {s} {names(s)} draft; this type always runs Release")
            return False
        return True
    ok = True
    draft = _one_draft(c, eng, s)
    ok = ok and draft is not None
    audits = [r for r in eng.records if r.stage == s and r.kind == "audit"]
    if not audits:
        if closed:
            c.findings.append(f"stage {s} {names(s)}: no audit pass (the fixed auditor is {FIXED_AUDITORS[s]})")
        else:
            c.notes.append(f"stage {s} {names(s)}: the {eng.studio.seat_name(FIXED_AUDITORS[s])}'s audit not yet run")
        ok = False
    for a in audits:
        if a.seat != FIXED_AUDITORS[s]:
            c.findings.append(f"stage {s}: audit by {a.seat}; the fixed auditor is {FIXED_AUDITORS[s]}")
            ok = False
        elif draft is not None and _pass_no(a.pass_id) < draft:
            c.findings.append(f"stage {s}: {a.pass_id} audits before the draft it audits")
            ok = False
    if closed and not gates:
        c.findings.append(f"closed with no release gate pass (anchor: stage {s} {names(s)})")
        ok = False
    return ok


def _small_ask(eng: Engagement, c: Check) -> Check:
    """A small ask's shape: Verifier's tests → Builder's code → the Planner's one audit of both → the final run.

    No build plan and no plan gate. The Planner's audit is the stage-3 audit, launched after the
    code's draft, with the tests draft's output among its inputs (it audits the change and the tests
    together). By Close, a Verifier `run` after that audit. The release leg is checked when it
    fired: Release's draft, the Builder's audit, and the release gate. A stage not yet reached is a
    note until Close, then a finding.
    """
    names = eng.studio.stage_name
    closed = any(r.kind == "close" for r in eng.records)
    for r in eng.records:
        if r.stage == 1 or r.seat == "plan-gate":
            c.findings.append(f"{r.pass_id}: {eng.studio.seat_name(r.seat)} {r.kind} on a small ask, which has no build plan "
                              "and no plan gate; one that needs a plan is a full build")

    def reached(stage: int) -> bool:
        return any(r.stage == stage for r in eng.records)

    tests = code = None
    for stage in (TESTS_STAGE, CODE_STAGE):
        if reached(stage) or closed:
            c.n_total += 1
            n = _one_draft(c, eng, stage)
            if stage == TESTS_STAGE:
                tests = n
            else:
                code = n
        else:
            c.notes.append(f"stage {stage} {names(stage)} not yet reached")
    c.n_ok += tests is not None

    code_ok = code is not None
    if code is not None and (tests is None or tests > code):
        c.findings.append(f"stage {CODE_STAGE} {names(CODE_STAGE)}: drafted before the tests draft; the Verifier writes the tests first")
        code_ok = False
    audit_at = None
    if code is not None:
        test_outputs = {o.path for r in eng.records if r.stage == TESTS_STAGE and r.kind == "draft" for o in r.outputs if o.path}
        audits = [r for r in eng.records if r.stage == CODE_STAGE and r.kind == "audit"]
        for a in audits:
            if a.seat != FIXED_AUDITORS[CODE_STAGE]:
                c.findings.append(f"stage {CODE_STAGE}: audit by {a.seat}; on a small ask the Build Planner audits the change and the tests")
            elif _pass_no(a.pass_id) < code:
                c.findings.append(f"stage {CODE_STAGE}: {a.pass_id} audits before the code it audits")
            elif test_outputs and not test_outputs & {i.path for i in a.inputs}:
                c.findings.append(f"stage {CODE_STAGE}: {a.pass_id} did not read the tests; on a small ask the Planner audits "
                                  "the change and the tests together")
            elif audit_at is None:
                audit_at = _pass_no(a.pass_id)
        if not audits:
            if closed:
                c.findings.append(f"stage {CODE_STAGE} {names(CODE_STAGE)}: no audit pass by the Build Planner")
            else:
                c.notes.append(f"stage {CODE_STAGE} {names(CODE_STAGE)}: the Build Planner's audit not yet run")
    c.n_ok += code_ok and audit_at is not None
    if closed:
        runs = [_pass_no(r.pass_id) for r in eng.records if r.kind == "run" and r.seat == STAGE_SEATS[TESTS_STAGE]]
        if not runs or (audit_at is not None and max(runs) < audit_at):
            c.findings.append("closed with no Verifier final run after the Planner's audit")
    if reached(4) or any(r.seat == "release-gate" for r in eng.records):
        c.n_total += 1
        c.n_ok += _release_leg(c, eng, closed, owed=False)
    return c


def _ops_only(eng: Engagement, c: Check) -> Check:
    """An ops-only ask's shape: Release drafts → the Builder audits → the release gate. Nothing else drafts."""
    closed = any(r.kind == "close" for r in eng.records)
    for r in eng.records:
        if 1 <= r.stage <= 3 and r.kind in ("draft", "repair", "run"):
            c.findings.append(f"{r.pass_id}: {eng.studio.seat_name(r.seat)} {r.kind} at stage {r.stage} on an ops-only ask, "
                              "which changes no source; it re-opens as a full build")
        if r.seat == "plan-gate":
            c.findings.append(f"{r.pass_id}: a plan gate on an ops-only ask, which has no build plan")
    c.n_total = 1
    c.n_ok += _release_leg(c, eng, closed, owed=True)
    return c


STRUCTURE_CHECKS[STUDIO.key] = _stages
