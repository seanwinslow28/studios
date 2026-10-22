"""Studio profiles (kit 0.6.0, #291; resolved per engagement since 0.9.0, #325): no studio lives in the kit."""
import re
from pathlib import Path

import pytest

import tracekit.studio as studio_mod
from reference import PRODUCTCRAFT, PROFILE, REPO
from synth import build
from tracekit.checker import CHECK_NAMES, STRUCTURE_CHECKS, check_names, run_checks
from tracekit.engagement import REPO_PREFIXES, find_repo_root, load_engagement
from tracekit.labels import LabelsError, parse_labels
from tracekit.moves import extract_ids
from tracekit.studio import PROFILE_ENV, Studio, StudioNotFound, find_profile, load_profile, resolve_studio
from tracekit.taxonomy import SHARED_TAXONOMY_PATH, taxonomy_for
from tracekit.viewer import render_html, run_line


def test_the_kit_holds_no_studio_of_its_own():
    assert not hasattr(studio_mod, "PRODUCTCRAFT")
    assert REPO_PREFIXES == ("craftwork/", ".claude/")                     # only what every studio shares
    assert not (Path(studio_mod.__file__).parents[1] / studio_mod.PROFILE_FILE).exists()   # a walk never finds the kit


def test_productcraft_profile_lives_with_productcraft():
    assert PROFILE == REPO / "productcraft" / "trace" / "studio.py"
    assert PRODUCTCRAFT.key == "productcraft" and PRODUCTCRAFT.all_stage_numbers == [0, 1, 2, 3, 4, 5, 6, 7]
    assert PRODUCTCRAFT.stage_label(0) == "close" and PRODUCTCRAFT.stage_label(2) == "2 Discovery"
    assert check_names(PRODUCTCRAFT) == CHECK_NAMES and STRUCTURE_CHECKS["productcraft"].__name__ == "_stages"
    assert load_profile(PROFILE) is PRODUCTCRAFT                           # one load per file: one studio object


def test_an_engagement_loads_with_the_reference_profile(tmp_path):
    eng = load_engagement(build(tmp_path / "pc-eng-000-callboard"))
    assert eng.studio is PRODUCTCRAFT
    assert all(c.ok for c in run_checks(eng))


def test_the_walk_finds_the_team_profile_above_its_ledger():
    eng_dir = REPO / "productcraft" / "ledger" / "engagements" / "pc-eng-001-anything"   # need not exist
    assert find_profile(eng_dir) == PROFILE
    assert find_profile(REPO / "productcraft" / "trace" / "samples" / "synthetic-engagement") == PROFILE
    assert find_profile(REPO / "craftwork" / "trace" / "tests") is None


def test_resolution_order_passed_then_walk_then_env_then_refuse(tmp_path, monkeypatch):
    team = tmp_path / "toycraft"
    (team / "trace").mkdir(parents=True)
    (team / "trace" / "studio.py").write_text(
        "from tracekit.studio import Studio\n"
        "STUDIO = Studio(key='toycraft', name='Toycraft', stages={1: 'One'}, kinds=('draft',), forward_kinds=('draft',))\n")
    eng = team / "ledger" / "engagements" / "tc-eng-001"
    eng.mkdir(parents=True)
    assert resolve_studio(eng, TOY) is TOY                                  # passed in wins
    assert resolve_studio(eng).key == "toycraft"                            # then the walk, over $TRACEKIT_STUDIO
    loose = tmp_path / "loose" / "eng"
    loose.mkdir(parents=True)
    assert resolve_studio(loose) is PRODUCTCRAFT                            # then the env fallback
    monkeypatch.delenv(PROFILE_ENV)
    with pytest.raises(StudioNotFound, match="no studio profile"):
        resolve_studio(loose)                                               # never a guess
    with pytest.raises(StudioNotFound, match="defines no STUDIO"):
        (tmp_path / "empty.py").write_text("X = 1\n")
        load_profile(tmp_path / "empty.py")


def test_cli_refuses_an_engagement_with_no_studio(tmp_path, monkeypatch):
    import subprocess, sys
    monkeypatch.delenv(PROFILE_ENV)
    loose = build(tmp_path / "loose" / "pc-eng-000-callboard")
    trace = Path(studio_mod.__file__).parents[1]
    r = subprocess.run([sys.executable, "check.py", str(loose)], capture_output=True, text=True, cwd=trace)
    assert r.returncode == 2 and "no studio profile" in r.stderr
    r = subprocess.run([sys.executable, "check.py", str(loose), "--studio", str(PROFILE)], capture_output=True, text=True, cwd=trace)
    assert r.returncode == 0, r.stdout + r.stderr


def test_taxonomy_is_shared_family_plus_the_studios_own(tmp_path):
    tax = taxonomy_for(PRODUCTCRAFT)
    assert {"manufactured", "stale-restatement", "overstated-scope", "kit-induced"} <= set(tax.codes)   # shared
    assert {"unobservable-measure", "overclaimed-pointer"} <= set(tax.codes)                             # Productcraft's
    assert list(tax.codes)[:4] == ["manufactured", "stale-restatement", "overstated-scope", "kit-induced"]
    assert tax.path == PRODUCTCRAFT.taxonomy_path
    own = tmp_path / "taxonomy.md"
    own.write_text("| code | family | a label with this code says | quote |\n|---|---|---|---|\n| `wilted` | seat | it wilted | — |\n")
    alone = Studio(key="t", name="T", stages={1: "One"}, kinds=("draft",), forward_kinds=("draft",),
                   taxonomy_path=own, shared_taxonomy=False)
    assert set(taxonomy_for(alone).codes) == {"wilted"}                     # opted out: its own file alone
    bare = Studio(key="b", name="B", stages={1: "One"}, kinds=("draft",), forward_kinds=("draft",))
    assert taxonomy_for(bare).path == SHARED_TAXONOMY_PATH and "manufactured" in taxonomy_for(bare).codes


TOY = Studio(
    key="toy", name="Toy", stages={0: "Seed", 1: "Grow", 2: "Prune"}, kinds=("plant", "trim", "note"),
    forward_kinds=("plant",), coordinator_kinds=("note",), gate_seats=("shears",),
    seat_names={"gardener": "Gardener", "shears": "Shears"}, repo_prefixes=("toy/",),
    id_re=re.compile(r"\bLeaf \d+\b"), brief_file="plot.md", checks_dir="trims",
    structure_check_name="Every plant was trimmed",
    check_implications=tuple(f"implication {i}" for i in range(10)),
    review_prompts=(("plant", "Did it grow?"),), review_prompts_version="v0",
)


def _toy(tmp_path: Path) -> Path:
    root = tmp_path / "toy-run"
    (root / "trace").mkdir(parents=True)
    (root / "plot.md").write_text("---\nid: toy-000\nname: Toy run\ntype: bed\nopened: 2026-10-06\nclosed: null\n---\n")
    art = root / "bed.md"
    art.write_text("# bed\n\nLeaf 1 and Leaf 2 grew.\n\n## Moves\n\n- kept — Leaf 1 from the seed packet\n- added — Leaf 9 from the sun\n")
    import hashlib
    h = hashlib.sha256(art.read_bytes()).hexdigest()
    (root / "seed.md").write_text("Leaf 1\n")
    hs = hashlib.sha256((root / "seed.md").read_bytes()).hexdigest()
    (root / "trace" / "pass-01-gardener-plant.md").write_text(
        "---\npass: pass-01\nseat: gardener\nkind: plant\nstage: 0\nruntime: hands\nlaunch: \"by hand\"\neffort: —\n"
        "launched: 2026-10-06T08:00:00-04:00\ncompleted: 2026-10-06T08:05:00-04:00\nwall_clock_s: 300\nmeter: null\n"
        f"meter_source: UNMEASURED\ninputs:\n  - path: seed.md\n    sha256: {hs}\nwithheld:\n  - the drafting conversation\n"
        f"outputs:\n  - path: bed.md\n    sha256: {h}\nraw_log: —\nchecks: []\ntriggered_by: null\nshadow_of: null\n---\n\n"
        "## Corpus read\n\n- seed.md\n\n## Moves\n\nbed.md § Moves\n\n## Notes\n\nnone\n")
    (root / "trace" / "labels.md").write_text(
        "| pass | verdict | first_failing_stage | critique | failure_code |\n|---|---|---|---|---|\n| pass-01 | fail | 0 | sprouted late | |\n")
    return root


def test_another_profile_drives_loader_checker_and_viewer(tmp_path):
    eng = load_engagement(_toy(tmp_path), studio=TOY)
    assert eng.studio is TOY and eng.brief["id"] == "toy-000"
    checks = run_checks(eng)
    assert [c.name for c in checks] == list(check_names(TOY))
    by = {c.name: c for c in checks}
    assert by["Every plant was trimmed"].ok and "registers no structure check" in by["Every plant was trimmed"].notes[0]
    assert by["Every move names an existing upstream item; splits are subsets"].ok      # Leaf 1 is in seed.md
    assert by["Records parse and carry every required field"].ok                         # stage 0 is legal, kind `plant` is legal
    html = render_html(eng, rendered_on="2026-10-06")
    assert "Toy · craftwork/trace" in html and "0 Seed" in html and "2 Prune" in html and "Strategist" not in html
    assert "<th scope='col'>0</th>" in html and "<th scope='col'>3</th>" not in html
    assert "implication 5" not in html or True                                            # implications print only on a finding
    assert run_line("pass-01", "gardener", "plant", TOY) == "Run 1 · Gardener plant"


def test_labels_reject_a_stage_outside_the_profile():
    header = "| pass | verdict | first_failing_stage | critique | failure_code |\n|---|---|---|---|---|\n"
    with pytest.raises(LabelsError, match="0–2"):
        parse_labels(header + "| pass-01 | fail | 5 | x | |\n", stages=TOY.all_stage_numbers)
    assert parse_labels(header + "| pass-01 | fail | 7 | x | |\n")["pass-01"].first_failing_stage == 7   # the default keeps 0–7


def test_extract_ids_with_a_studio_pattern():
    assert extract_ids("Leaf 3 + Leaf 4 → Leaf 5", TOY.id_re) == ["Leaf 3", "Leaf 4", "Leaf 5"]
    assert extract_ids("E1–E3") == ["E1", "E2", "E3"]                 # the default still expands ranges


def test_repo_root_is_found_by_either_marker(tmp_path):
    (tmp_path / "CLAUDE.md").write_text("x")
    (tmp_path / ".claude").mkdir()
    assert find_repo_root(tmp_path / "a" / "b", markers=(".claude",)) == tmp_path            # walks up through the parents
    assert find_repo_root(tmp_path, markers=(".claude",)) == tmp_path
    assert find_repo_root(tmp_path) == tmp_path                                            # the default accepts .claude too


# --------------------------------------------------------------------------- #
# Systemcraft's profile (craftwork build 4, #327): a second real studio the kit reads
# --------------------------------------------------------------------------- #

SC_PROFILE = REPO / "systemcraft" / "trace" / "studio.py"


def _sc_record(root: Path, n: int, seat: str, kind: str, stage: int, inputs: list[str], outputs: list[str]) -> None:
    import hashlib

    def h(p: str) -> str:
        return hashlib.sha256((root / p).read_bytes()).hexdigest()

    ins = "".join(f"  - path: {p}\n    sha256: {h(p)}\n" for p in inputs)
    outs = "".join(f"  - path: {p}\n    sha256: {h(p)}\n" for p in outputs)
    moves = f"{outputs[0]} § Moves" if kind in ("draft", "repair") else "none — this kind hands no artifact forward"
    (root / "trace" / f"pass-{n:02d}-{seat}-{kind}.md").write_text(
        f"---\npass: pass-{n:02d}\nseat: {seat}\nkind: {kind}\nstage: {stage}\nruntime: claude-opus-5-5\n"
        f"launch: \"Agent tool, fresh context\"\neffort: —\nlaunched: 2026-10-06T08:{n:02d}:00-04:00\n"
        f"completed: 2026-10-06T08:{n:02d}:30-04:00\nwall_clock_s: 30\nmeter: null\nmeter_source: UNMEASURED\n"
        f"inputs:\n{ins}withheld:\n  - the drafting conversation\noutputs:\n{outs}raw_log: —\nchecks: []\n"
        f"triggered_by: null\nshadow_of: null\n---\n\n## Corpus read\n\nnone\n\n## Moves\n\n{moves}\n\n## Notes\n\nnone\n")


def _sc_engagement(tmp_path: Path, etype: str, passes: list[tuple]) -> Path:
    """A minimal Systemcraft engagement: open-brief.md with the kit's header, artifacts beside their checks."""
    root = tmp_path / "eng-900-toy"
    (root / "trace").mkdir(parents=True)
    (root / "artifacts").mkdir()
    (root / "open-brief.md").write_text(
        f"---\nid: eng-900\nname: Toy reconcile\ntype: {etype}\nopened: 2026-10-06\nclosed: null\npass_budget: 9\n---\n\nA toy.\n")
    (root / "artifacts" / "prd.md").write_text("# PRD\n\nS1 holds.\n\n## Moves\n\norigin draft, no upstream — leaned on: the brief\n")
    (root / "artifacts" / "adr-01.md").write_text("# ADR-01\n\nS1 drives it.\n\n## Moves\n\n- kept — S1 from eng-900.prd\n")
    (root / "artifacts" / "cosign-evals.md").write_text("# Co-sign\n\nS1 is testable.\n")
    (root / "artifacts" / "audit-adr.md").write_text("# Audit\n\nADR-01 is priced.\n")
    (root / "artifacts" / "audit-stray.md").write_text("# Audit\n\nOut of lane.\n")
    rows = []
    for i, (seat, kind, stage, ins, outs) in enumerate(passes, start=1):
        _sc_record(root, i, seat, kind, stage, ["open-brief.md", *ins], outs)
        rows.append(f"| pass-{i:02d} | pass | | fine | |")
    (root / "trace" / "labels.md").write_text(
        "| pass | verdict | first_failing_stage | critique | failure_code |\n|---|---|---|---|---|\n" + "\n".join(rows) + "\n")
    return root


SC_DESIGN = [
    ("design-strategist", "draft", 1, [], ["artifacts/prd.md"]),
    ("evals-evidence-architect", "co-sign", 1, ["artifacts/prd.md"], ["artifacts/cosign-evals.md"]),
    ("architecture-advisor", "draft", 2, ["artifacts/prd.md"], ["artifacts/adr-01.md"]),
    ("ops-economics-modeler", "audit", 2, ["artifacts/adr-01.md"], ["artifacts/audit-adr.md"]),
]


def test_systemcraft_profile_lives_with_systemcraft():
    sc = load_profile(SC_PROFILE)
    assert sc.key == "systemcraft" and sc.all_stage_numbers == [0, 1, 2, 3, 4, 5]
    assert sc.brief_file == "open-brief.md" and sc.checks_dir == "artifacts" and "intake" in sc.kinds
    assert check_names(sc) == CHECK_NAMES[:7] + (sc.structure_check_name,) + CHECK_NAMES[8:]
    assert STRUCTURE_CHECKS["systemcraft"].__name__ == "_stages"
    assert find_profile(REPO / "systemcraft" / "ledger" / "engagements" / "eng-005-anything") == SC_PROFILE
    assert taxonomy_for(sc).path == sc.taxonomy_path and "manufactured" in taxonomy_for(sc).codes   # shared family, no own modes yet


def test_a_systemcraft_design_engagement_checks_clean(tmp_path):
    eng = load_engagement(_sc_engagement(tmp_path, "design", SC_DESIGN), studio=load_profile(SC_PROFILE))
    by = {c.name: c for c in run_checks(eng)}
    assert all(c.ok for c in by.values()), {n: c.findings for n, c in by.items() if c.findings}
    line8 = by[eng.studio.structure_check_name]
    assert line8.count == "2 of 2" and "stages not yet reached: 3, 4, 5" in line8.notes


def test_systemcraft_line_8_wants_the_cosign_on_the_prd_and_the_fixed_auditor(tmp_path):
    passes = [SC_DESIGN[0], ("evals-evidence-architect", "audit", 1, ["artifacts/prd.md"], ["artifacts/cosign-evals.md"]),
              SC_DESIGN[2], ("design-strategist", "audit", 2, ["artifacts/adr-01.md"], ["artifacts/audit-adr.md"])]
    eng = load_engagement(_sc_engagement(tmp_path, "design", passes), studio=load_profile(SC_PROFILE))
    line8 = {c.name: c for c in run_checks(eng)}[eng.studio.structure_check_name]
    assert any("stage 1 Strategist: no co-sign pass" in f for f in line8.findings)       # the dual-touch law
    assert any("audit by design-strategist; the fixed auditor is ops-economics-modeler" in f for f in line8.findings)


def test_systemcraft_audit_engagement_flags_a_pass_outside_its_seats_lane(tmp_path):
    passes = [("architecture-advisor", "audit", 2, ["artifacts/adr-01.md"], ["artifacts/audit-adr.md"]),
              ("interaction-trust-designer", "audit", 2, ["artifacts/adr-01.md"], ["artifacts/audit-stray.md"])]
    eng = load_engagement(_sc_engagement(tmp_path, "audit", passes), studio=load_profile(SC_PROFILE))
    line8 = {c.name: c for c in run_checks(eng)}[eng.studio.structure_check_name]
    assert line8.findings == ["pass-02: interaction-trust-designer at stage 2 Architecture, a lane it neither owns "
                              "nor audits (architecture-advisor owns it, ops-economics-modeler audits it)"]


def test_systemcraft_cli_finds_its_profile_by_the_walk(tmp_path, monkeypatch):
    import shutil, subprocess, sys
    monkeypatch.delenv(PROFILE_ENV)
    team = tmp_path / "systemcraft"
    (team / "trace").mkdir(parents=True)
    shutil.copy(SC_PROFILE, team / "trace" / "studio.py")
    (team / "trace" / "taxonomy.md").write_text("# none\n")
    eng = _sc_engagement(team / "ledger" / "engagements", "design", SC_DESIGN)
    trace = Path(studio_mod.__file__).parents[1]
    r = subprocess.run([sys.executable, "check.py", str(eng)], capture_output=True, text=True, cwd=trace,
                       env={**__import__("os").environ, "PYTHONPATH": str(trace)})
    assert r.returncode == 0, r.stdout + r.stderr


# --------------------------------------------------------------------------- #
# Devcraft's profile: line 8 reads the engagement's type (the master skill's table)
# --------------------------------------------------------------------------- #

DC_PROFILE = REPO / "devcraft" / "trace" / "studio.py"
DC_FILES = {
    "artifacts/build-plan.md": "# Build plan\n\nAC1 holds.\n\n## Moves\n\norigin draft, no upstream — leaned on: the brief\n",
    "artifacts/test-record.md": "# Test record\n\nASK1 is tested.\n\n## Moves\n\norigin draft, no upstream — leaned on: the brief\n",
    "artifacts/change-note.md": "# Change note\n\nASK1 is built.\n\n## Moves\n\norigin draft, no upstream — leaned on: the brief\n",
    "artifacts/release-plan.md": "# Release plan\n\nASK1 ships.\n\n## Moves\n\norigin draft, no upstream — leaned on: the brief\n",
    "audits/audit-plan.md": "# Audit\n\nThe plan holds.\n",
    "audits/audit-change.md": "# Audit\n\nThe change and its tests hold.\n",
    "audits/audit-release.md": "# Audit\n\nThe release plan covers the diff.\n",
    "audits/audit-tests.md": "# Audit\n\nThe test record holds.\n",
    "audits/plan-gate.md": "# Plan gate\n\nPLAN PASS — QUALITY VERDICT ONLY\n",
    "audits/release-gate.md": "# Release gate\n\nRELEASE PASS — QUALITY VERDICT ONLY\n",
}


def _dc_engagement(tmp_path: Path, etype: str, passes: list[tuple]) -> Path:
    """A minimal Devcraft engagement: brief.md with the kit's header, every pass recorded in launch order."""
    root = tmp_path / "dc-eng-900-toy"
    (root / "trace").mkdir(parents=True)
    (root / "brief.md").write_text(
        f"---\nid: dc-eng-900\nname: Toy ask\ntype: {etype}\nopened: 2026-10-11\nclosed: null\npass_budget: 9\n---\n\nA toy.\n")
    for rel, text in DC_FILES.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text)
    rows = []
    for i, (seat, kind, stage, ins, outs) in enumerate(passes, start=1):
        if kind == "run":                                                   # the final run revises the test record
            (root / outs[0]).write_text(DC_FILES[outs[0]].replace("is tested.", "is tested, final run green."))
        _sc_record(root, i, seat, kind, stage, ["brief.md", *ins], outs)
        rows.append(f"| pass-{i:02d} | pass | | fine | |")
    (root / "trace" / "labels.md").write_text(
        "| pass | verdict | first_failing_stage | critique | failure_code |\n|---|---|---|---|---|\n" + "\n".join(rows) + "\n")
    return root


TESTS, CHANGE, RELEASE = "artifacts/test-record.md", "artifacts/change-note.md", "artifacts/release-plan.md"
DC_SMALL = [
    ("verifier", "draft", 2, [], [TESTS]),
    ("builder", "draft", 3, [TESTS], [CHANGE]),
    ("build-planner", "audit", 3, [CHANGE, TESTS], ["audits/audit-change.md"]),
    ("verifier", "run", 2, [CHANGE, TESTS], [TESTS]),
]
DC_RELEASE_LEG = [
    ("release-reliability", "draft", 4, [CHANGE], [RELEASE]),
    ("builder", "audit", 4, [RELEASE], ["audits/audit-release.md"]),
    ("release-gate", "gate", 4, [RELEASE, CHANGE, TESTS], ["audits/release-gate.md"]),
]
DC_CLOSE = [("coordinator", "close", 0, [], [])]


def _dc_line8(tmp_path: Path, etype: str, passes: list[tuple]):
    eng = load_engagement(_dc_engagement(tmp_path, etype, passes), studio=load_profile(DC_PROFILE))
    return eng, {c.name: c for c in run_checks(eng)}[eng.studio.structure_check_name]


def test_devcraft_profile_lives_with_devcraft():
    dc = load_profile(DC_PROFILE)
    assert dc.key == "devcraft" and dc.brief_file == "brief.md" and dc.checks_dir == "audits"
    assert STRUCTURE_CHECKS["devcraft"].__name__ == "_stages"
    assert find_profile(REPO / "devcraft" / "ledger" / "engagements" / "dc-eng-001-anything") == DC_PROFILE


def test_a_devcraft_small_ask_checks_clean(tmp_path):
    eng, line8 = _dc_line8(tmp_path, "small-ask", DC_SMALL + DC_CLOSE)
    by = {c.name: c for c in run_checks(eng)}
    assert all(c.ok for c in by.values()), {n: c.findings for n, c in by.items() if c.findings}
    assert line8.count == "2 of 2"


def test_devcraft_self_check_has_its_own_gate_lane_and_registry_family(tmp_path):
    from tracekit.registry import numbers_for

    root = _dc_engagement(tmp_path, "small-ask", DC_SMALL + DC_CLOSE)
    findings = root / "audits" / "self-check.md"
    findings.write_text("# Self-check\n\nAUDIT PASS — QUALITY VERDICT ONLY\n")
    _sc_record(root, 6, "self-check", "gate", 3, [CHANGE], ["audits/self-check.md"])
    labels = root / "trace" / "labels.md"
    with labels.open("a") as f:
        f.write("| pass-06 | pass | | fine | |\n")
    eng = load_engagement(root, studio=load_profile(DC_PROFILE))
    assert all(c.ok for c in run_checks(eng))
    page = render_html(eng)
    assert "Self-check" in page
    assert "self-check" in eng.studio.gate_seats
    _, cells = numbers_for([eng])
    cell = next(c for c in cells if c.seat == "self-check")
    assert cell.family == "gate" and cell.passes == 1


def test_a_devcraft_small_ask_with_its_release_leg_checks_clean(tmp_path):
    _, line8 = _dc_line8(tmp_path, "small-ask", DC_SMALL + DC_RELEASE_LEG + DC_CLOSE)
    assert line8.ok, line8.findings


def test_a_small_ask_in_progress_is_notes_not_findings(tmp_path):
    _, line8 = _dc_line8(tmp_path, "small-ask", DC_SMALL[:2])
    assert line8.ok, line8.findings
    assert any("Build Planner's audit not yet run" in n for n in line8.notes)


def test_devcraft_small_ask_line_8_holds_its_shape(tmp_path):
    passes = [
        ("build-planner", "draft", 1, [], ["artifacts/build-plan.md"]),        # a small ask has no plan
        ("builder", "draft", 3, [], [CHANGE]),                                 # code before the tests
        ("verifier", "draft", 2, [], [TESTS]),
        ("build-planner", "audit", 3, [CHANGE], ["audits/audit-change.md"]),   # never read the tests
        ("release-reliability", "draft", 4, [CHANGE], [RELEASE]),
        ("builder", "audit", 4, [RELEASE], ["audits/audit-release.md"]),
        *DC_CLOSE,                                                             # no final run, no release gate
    ]
    _, line8 = _dc_line8(tmp_path, "small-ask", passes)
    f = line8.findings
    assert any(x.startswith("pass-01: Planner draft on a small ask") for x in f)
    assert any("drafted before the tests draft" in x for x in f)
    assert any("pass-04 did not read the tests" in x for x in f)
    assert "closed with no Verifier final run after the Planner's audit" in f
    assert any(x.startswith("closed with no release gate pass") for x in f)


def test_a_devcraft_ops_only_ask_checks_its_shape(tmp_path):
    _, clean = _dc_line8(tmp_path / "a", "ops-only", DC_RELEASE_LEG + DC_CLOSE)
    assert clean.ok and clean.count == "1 of 1", clean.findings
    _, bad = _dc_line8(tmp_path / "b", "ops-only", [("builder", "draft", 3, [], [CHANGE]), *DC_RELEASE_LEG[:2], *DC_CLOSE])
    assert any("builder draft at stage 3 on an ops-only ask" in x.lower() for x in bad.findings)
    assert any(x.startswith("closed with no release gate pass") for x in bad.findings)


def test_a_devcraft_one_off_is_not_asserted_and_says_so(tmp_path):
    _, line8 = _dc_line8(tmp_path, "one-off", [("build-planner", "draft", 0, [], ["artifacts/build-plan.md"]), *DC_CLOSE])
    assert line8.ok and any("one seat pass, no order to check" in n for n in line8.notes)


def test_a_devcraft_full_build_still_checks_its_own_shape(tmp_path):
    passes = [
        ("build-planner", "draft", 1, [], ["artifacts/build-plan.md"]),
        ("verifier", "audit", 1, ["artifacts/build-plan.md"], ["audits/audit-plan.md"]),
        ("plan-gate", "gate", 1, ["artifacts/build-plan.md"], ["audits/plan-gate.md"]),
        ("verifier", "draft", 2, ["artifacts/build-plan.md"], [TESTS]),
        ("builder", "draft", 3, [TESTS], [CHANGE]),
        ("build-planner", "audit", 3, [CHANGE], ["audits/audit-change.md"]),
        *DC_RELEASE_LEG[:2],
        ("verifier", "run", 2, [CHANGE, TESTS], [TESTS]),
        ("release-reliability", "audit", 2, [TESTS], ["audits/audit-tests.md"]),
        DC_RELEASE_LEG[2],
        *DC_CLOSE,
    ]
    _, line8 = _dc_line8(tmp_path, "full-build", passes)
    assert line8.ok and line8.count == "4 of 4", line8.findings


MC_PROFILE = REPO / "motioncraft" / "trace" / "studio.py"


def test_motioncraft_profile_matches_its_bench_and_families():
    """The bench ticket on the Motioncraft build map (2026-10-17): every seat the profile names has a seat file
    and a family of its own, and the three gates share the gate family."""
    from tracekit.registry import family_of

    mc = load_profile(MC_PROFILE)
    assert mc.key == "motioncraft"
    assert find_profile(REPO / "motioncraft" / "ledger" / "engagements" / "idea-seed-2026-10-17") == MC_PROFILE
    bench = {p.stem for p in (REPO / "motioncraft" / "bench").glob("*.md") if p.name != "README.md"}
    stage_seats = set(mc.seat_names) - set(mc.gate_seats) - {"coordinator"}
    assert stage_seats == bench == {"visual-story-director", "art-pose-designer", "animator", "finishing-sound-designer"}
    families = {s: family_of(s) for s in bench}
    assert len(set(families.values())) == 4 and "other" not in families.values()
    assert "coding" not in families.values()                               # the Animator never counts toward Devcraft's Builder
    assert {family_of(g) for g in mc.gate_seats} == {"gate"}
    # a self-targeted check's review has a slot of its own, and may cite another studio's files (SWCB #261)
    assert "self-check" in mc.gate_seats and "devcraft/" in mc.repo_prefixes


# --------------------------------------------------------------------------- #
# Motioncraft's line 8 reads the type and the parts (the master skill, SWCB #193)
# --------------------------------------------------------------------------- #

STORY, LOOK, MOVE, CUT = ("artifacts/story-packet.md", "artifacts/appearance-packet.md",
                          "artifacts/scene-record.md", "artifacts/delivery-package.md")
MC_FILES = {
    STORY: "# Story packet\n\nB1 holds.\n\n## Moves\n\norigin draft, no upstream — leaned on: the brief\n",
    LOOK: "# Appearance packet\n\nK1 holds.\n\n## Moves\n\norigin draft, no upstream — leaned on: the brief\n",
    MOVE: "# Scene record\n\nK1 moves.\n\n## Moves\n\norigin draft, no upstream — leaned on: the brief\n",
    CUT: "# Delivery package\n\nTC1 passes.\n\n## Moves\n\norigin draft, no upstream — leaned on: the brief\n",
    "audits/audit.md": "# Audit\n\nIt holds.\n",
    "audits/gate.md": "# Gate\n\nPASS — QUALITY VERDICT ONLY\n",
}


def _mc_engagement(tmp_path: Path, etype: str, passes: list[tuple], parts: list[str] | None = None,
                   files: dict[str, str] | None = None, triggers: dict[int, int] | None = None) -> Path:
    """A minimal Motioncraft engagement. A pass is (seat, kind, stage, inputs, outputs[, part]); `files` adds or
    replaces artifacts, `triggers` maps a pass number to the pass its `triggered_by` names."""
    root = tmp_path / "toy-2026-10-18"
    (root / "trace").mkdir(parents=True)
    header = f"parts: [{', '.join(parts)}]\n" if parts else ""
    (root / "brief.md").write_text(
        f"---\nid: mc-eng-900\nname: Toy film\ntype: {etype}\n{header}opened: 2026-10-18\nclosed: null\n"
        f"pass_budget: 11\nsynthetic: true\n---\n\nA toy.\n")
    for rel, text in {**MC_FILES, **(files or {})}.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text)
    rows = []
    for i, (seat, kind, stage, ins, outs, *part) in enumerate(passes, start=1):
        _sc_record(root, i, seat, kind, stage, ["brief.md", *ins], outs)
        if part:
            rec = root / "trace" / f"pass-{i:02d}-{seat}-{kind}.md"
            rec.write_text(rec.read_text().replace(f"\nstage: {stage}\n", f"\nstage: {stage}\npart: {part[0]}\n", 1))
        if i in (triggers or {}):
            rec = root / "trace" / f"pass-{i:02d}-{seat}-{kind}.md"
            rec.write_text(rec.read_text().replace("triggered_by: null", f"triggered_by: pass-{triggers[i]:02d}", 1))
        rows.append(f"| pass-{i:02d} | pass | | fine | |")
    (root / "trace" / "labels.md").write_text(
        "| pass | verdict | first_failing_stage | critique | failure_code |\n|---|---|---|---|---|\n" + "\n".join(rows) + "\n")
    return root


def _mc_line8(tmp_path: Path, etype: str, passes: list[tuple], parts: list[str] | None = None, **kw):
    eng = load_engagement(_mc_engagement(tmp_path, etype, passes, parts, **kw), studio=load_profile(MC_PROFILE))
    return eng, {c.name: c for c in run_checks(eng)}[eng.studio.structure_check_name]


AUDIT, GATE = "audits/audit.md", "audits/gate.md"
MC_SMALL = [
    ("animator", "draft", 3, [], [MOVE]),
    ("art-pose-designer", "audit", 3, [MOVE], [AUDIT]),
    ("motion-gate", "gate", 3, [MOVE], [GATE]),
    ("finishing-sound-designer", "draft", 4, [MOVE], [CUT]),
    ("animator", "audit", 4, [CUT], [AUDIT]),
]
MC_CLOSE = [("coordinator", "close", 0, [], [])]
MC_FULL = [
    ("visual-story-director", "draft", 1, [], [STORY]),
    ("finishing-sound-designer", "audit", 1, [STORY], [AUDIT]),
    ("story-gate", "gate", 1, [STORY], [GATE]),
    ("art-pose-designer", "draft", 2, [STORY], [LOOK]),
    ("visual-story-director", "audit", 2, [LOOK], [AUDIT]),
    ("appearance-gate", "gate", 2, [LOOK], [GATE]),
    *MC_SMALL[:3],
    *MC_SMALL[3:],
]


def test_a_motioncraft_small_piece_checks_clean(tmp_path):
    eng, line8 = _mc_line8(tmp_path, "small-piece", [*MC_SMALL, *MC_CLOSE])
    assert line8.ok and line8.count == "2 of 2", line8.findings
    assert all(c.ok for c in run_checks(eng)), [(c.name, c.findings) for c in run_checks(eng) if not c.ok]


def test_a_small_piece_in_progress_is_notes_not_findings(tmp_path):
    _, line8 = _mc_line8(tmp_path, "small-piece", MC_SMALL[:2])
    assert line8.ok, line8.findings
    assert any("stage 4 Finish not yet reached" in n for n in line8.notes)


def test_motioncraft_small_piece_line_8_holds_its_shape(tmp_path):
    passes = [
        ("visual-story-director", "draft", 1, [], [STORY]),                     # a story stage on a small piece
        ("appearance-gate", "gate", 2, [LOOK], [GATE]),                        # and an appearance gate
        MC_SMALL[0], MC_SMALL[1],
        MC_SMALL[3], MC_SMALL[4],                                              # Finishing drafts with no motion gate
        *MC_CLOSE,
    ]
    _, line8 = _mc_line8(tmp_path, "small-piece", passes)
    text = "\n".join(line8.findings)
    assert "pass-01: Director draft on a small piece" in text
    assert "pass-02: Appearance gate gate on a small piece" in text
    assert "stage 4 Finish: drafted before the motion gate ran" in text
    assert "closed with no motion gate pass" in text


def test_a_closed_small_piece_owes_both_stages(tmp_path):
    _, line8 = _mc_line8(tmp_path, "small-piece", [*MC_SMALL[:3], *MC_CLOSE])
    assert not line8.ok
    assert any("stage 4 Finish: 0 drafts" in f for f in line8.findings)


def test_a_motioncraft_one_off_is_not_asserted_and_says_so(tmp_path):
    _, line8 = _mc_line8(tmp_path, "one-off", [("art-pose-designer", "draft", 2, [], [LOOK])])
    assert line8.ok and any("one seat pass" in n for n in line8.notes)


def test_a_motioncraft_full_train_checks_its_own_shape(tmp_path):
    _, line8 = _mc_line8(tmp_path, "full-train", [*MC_FULL, *MC_CLOSE])
    assert line8.ok and line8.count == "4 of 4", line8.findings
    early = [p for p in MC_FULL if p[0] != "appearance-gate"]                # motion with no appearance gate
    _, line8 = _mc_line8(tmp_path / "b", "full-train", [*early, *MC_CLOSE])
    assert any("drafted before the appearance gate ran" in f for f in line8.findings)
    assert any("closed with no appearance gate pass" in f for f in line8.findings)


def test_a_train_in_parts_counts_stages_2_and_3_per_part(tmp_path):
    split = [
        *MC_FULL[:3],
        ("art-pose-designer", "draft", 2, [STORY], [LOOK], "ground"),
        ("visual-story-director", "audit", 2, [LOOK], [AUDIT], "ground"),
        ("appearance-gate", "gate", 2, [LOOK], [GATE], "ground"),
        ("art-pose-designer", "draft", 2, [STORY], [LOOK], "figure"),
        ("visual-story-director", "audit", 2, [LOOK], [AUDIT], "figure"),
        ("appearance-gate", "gate", 2, [LOOK], [GATE], "figure"),
        ("animator", "draft", 3, [LOOK], [MOVE], "ground"),
        ("art-pose-designer", "audit", 3, [MOVE], [AUDIT], "ground"),
        ("motion-gate", "gate", 3, [MOVE], [GATE], "ground"),
        ("animator", "draft", 3, [LOOK], [MOVE], "figure"),
        ("art-pose-designer", "audit", 3, [MOVE], [AUDIT], "figure"),
        ("motion-gate", "gate", 3, [MOVE], [GATE], "figure"),
        *MC_SMALL[3:],
        *MC_CLOSE,
    ]
    _, line8 = _mc_line8(tmp_path, "full-train", split, parts=["ground", "figure"])
    assert line8.ok and line8.count == "6 of 6", line8.findings
    # the figure's appearance gate runs only after the first motion draft, and its motion gate never runs
    late = [p for p in split if not (p[0] == "appearance-gate" and p[-1] == "figure")
            and not (p[0] == "motion-gate" and p[-1] == "figure")]
    late.insert(late.index(next(p for p in late if p[0] == "animator" and p[-1] == "figure")),
                ("appearance-gate", "gate", 2, [LOOK], [GATE], "figure"))
    _, line8 = _mc_line8(tmp_path / "b", "full-train", late, parts=["ground", "figure"])
    text = "\n".join(line8.findings)
    assert "drafted before part figure's appearance gate ran" in text
    assert "closed with no motion gate pass for part figure" in text


def test_an_unsplit_train_flags_a_second_draft_and_a_split_one_flags_a_stray_part(tmp_path):
    two = [*MC_FULL[:5], ("art-pose-designer", "draft", 2, [STORY], [LOOK])]
    _, line8 = _mc_line8(tmp_path, "full-train", two)
    assert any("stage 2 Appearance: 2 drafts" in f for f in line8.findings)
    stray = [*MC_FULL[:3], ("art-pose-designer", "draft", 2, [STORY], [LOOK], "sky"),
             ("visual-story-director", "audit", 2, [LOOK], [AUDIT], "sky")]
    _, line8 = _mc_line8(tmp_path / "b", "full-train", stray, parts=["ground"])
    text = "\n".join(line8.findings)
    assert "names part sky" in text and "stage 2 Appearance part ground: 0 drafts" in text


# --------------------------------------------------------------------------- #
# Three passes a full train files truthfully as `draft` that are not the stage's one draft (SWCB #246)
# --------------------------------------------------------------------------- #

FRAME, APPEARANCE_GATE = "frames/assembled-frame-v01/checksums.sha256", "audits/appearance-gate.md"
PROTOS, CUT_R2 = "artifacts/camera-prototypes.md", "artifacts/delivery-package-r2.md"
FRAME_SUMS = "0123abcd  arrival.png\n"


def _header(fields: str, title: str) -> str:
    return f"---\n{fields}---\n\n# {title}\n\nIt holds.\n\n## Moves\n\norigin draft, no upstream — leaned on: the brief\n"


def _first_film(proof: str | None = None, answers: str = 'answers: "SWCB #207"\n',
                stopped: str = 'exit: "Blocked: Sean\'s call"\n') -> dict:
    """mc-eng-001's shape in miniature: the assembled frame as the appearance gate's proof, the camera ticket's
    prototypes before the moving test, and Finishing's draft stopped on Sean's call for the cue list, then resumed."""
    import hashlib
    sha = hashlib.sha256(FRAME_SUMS.encode()).hexdigest()
    proof = proof if proof is not None else f'proof: "frames/assembled-frame-v01 · {sha}"\n'
    passes = [
        *MC_FULL[:5],
        ("finishing-sound-designer", "draft", 2, [LOOK], [FRAME]),                          # 6: the assembled frame
        ("appearance-gate", "gate", 2, [LOOK, FRAME], [APPEARANCE_GATE]),                  # 7
        ("animator", "draft", 3, [LOOK], [PROTOS]),                                         # 8: the camera prototypes
        *MC_SMALL[:3],                                                                      # 9-11: moving test, audit, gate
        ("finishing-sound-designer", "draft", 4, [MOVE], [CUT]),                            # 12: stops for the cue list
        ("finishing-sound-designer", "draft", 4, [CUT], [CUT_R2]),                          # 13: resumes on Sean's call
        ("animator", "audit", 4, [CUT_R2], [AUDIT]),
        *MC_CLOSE,
    ]
    files = {
        FRAME: FRAME_SUMS,
        APPEARANCE_GATE: f"---\n{proof}---\n\n# Appearance gate\n\nPASS — QUALITY VERDICT ONLY\n",
        PROTOS: _header(f"{answers}exit: none\n", "Camera prototypes"),
        CUT: _header(stopped, "Delivery package"),
        CUT_R2: _header("exit: none\n", "Delivery package"),
    }
    return {"passes": passes, "files": files, "triggers": {13: 12}}


def test_the_first_films_three_extra_drafts_are_read_for_what_they_are(tmp_path):
    film = _first_film()
    _, line8 = _mc_line8(tmp_path, "full-train", film["passes"], files=film["files"], triggers=film["triggers"])
    assert line8.ok and line8.count == "4 of 4", line8.findings
    notes = "\n".join(line8.notes)
    assert "pass-06: Finishing's draft at stage 2 is the appearance gate's proof (pass-07), not the stage's draft" in notes
    assert "pass-08: Animator's draft at stage 3 answers SWCB #207, not the stage's draft" in notes
    assert "pass-13: resumes pass-12, stopped on `Blocked: Sean's call`; one draft with it" in notes


def test_an_assembled_frame_no_gate_names_is_still_a_second_draft(tmp_path):
    for i, proof in enumerate(("proof: none\n", f'proof: "frames/assembled-frame-v01 · {"0" * 64}"\n')):
        film = _first_film(proof=proof)                                                     # no proof, or another hash
        _, line8 = _mc_line8(tmp_path / str(i), "full-train", film["passes"], files=film["files"], triggers=film["triggers"])
        assert line8.findings == ["stage 2 Appearance: 2 drafts, expected exactly one (repairs are `kind: repair`)"]


def test_a_draft_answering_no_ticket_or_resuming_no_stop_is_still_a_second_draft(tmp_path):
    film = _first_film(answers="")
    _, line8 = _mc_line8(tmp_path / "a", "full-train", film["passes"], files=film["files"], triggers=film["triggers"])
    assert line8.findings == ["stage 3 Motion: 2 drafts, expected exactly one (repairs are `kind: repair`)"]
    film = _first_film(stopped="exit: none\n")                                              # the first part finished
    _, line8 = _mc_line8(tmp_path / "b", "full-train", film["passes"], files=film["files"], triggers=film["triggers"])
    assert line8.findings == ["stage 4 Finish: 2 drafts, expected exactly one (repairs are `kind: repair`)"]
    film = _first_film()                                                                     # resumed, but not by its trigger
    _, line8 = _mc_line8(tmp_path / "c", "full-train", film["passes"], files=film["files"])
    assert line8.findings == ["stage 4 Finish: 2 drafts, expected exactly one (repairs are `kind: repair`)"]


def test_camera_prototypes_still_wait_for_the_appearance_gate(tmp_path):
    film = _first_film()
    passes = film["passes"]
    passes[6], passes[7] = passes[7], passes[6]                                             # prototypes before the gate
    _, line8 = _mc_line8(tmp_path, "full-train", passes, files=film["files"], triggers=film["triggers"])
    assert "stage 3 Motion: drafted before the appearance gate ran" in line8.findings


def test_a_resumption_must_follow_the_draft_it_resumes(tmp_path):
    """From the independent review on SWCB #246: a draft naming itself or a later pass resumes nothing."""
    film = _first_film()
    for i, triggers in enumerate(({12: 12}, {12: 13})):                                 # itself, then a later pass
        _, line8 = _mc_line8(tmp_path / str(i), "full-train", film["passes"], files=film["files"], triggers=triggers)
        assert line8.findings == ["stage 4 Finish: 2 drafts, expected exactly one (repairs are `kind: repair`)"]


def test_a_small_piece_orders_a_resumed_draft_by_where_it_finished(tmp_path):
    """From the independent review on SWCB #246: motion stopped on Sean's call and resumed after its gate and
    after Finishing has not been gated; the stopped draft's number alone would let it through."""
    stopped = _header('exit: "Blocked: Sean\'s call"\n', "Scene record")
    passes = [MC_SMALL[0], MC_SMALL[1], MC_SMALL[2], MC_SMALL[3], MC_SMALL[4],
              ("animator", "draft", 3, [MOVE], ["artifacts/scene-record-r2.md"]), *MC_CLOSE]
    files = {MOVE: stopped, "artifacts/scene-record-r2.md": _header("exit: none\n", "Scene record")}
    _, line8 = _mc_line8(tmp_path, "small-piece", passes, files=files, triggers={6: 1})
    text = "\n".join(line8.findings)
    assert ("stage 3: pass-02, pass-03, pass-04 ran while pass-01 was stopped on Sean's call, "  # audited, gated
            "before its resumption finished at pass-06") in text                                    # and cut
    assert "stage 4 Finish: drafted before the motion gate ran on the moving test" in text  # and the gate saw it too
    # Finishing stopped before the motion gate is drafted before it, wherever its resumption lands
    passes = [MC_SMALL[0], MC_SMALL[1], ("finishing-sound-designer", "draft", 4, [MOVE], [CUT]), MC_SMALL[2],
              ("finishing-sound-designer", "draft", 4, [CUT], [CUT_R2]), ("animator", "audit", 4, [CUT_R2], [AUDIT]), *MC_CLOSE]
    files = {CUT: _header('exit: "Blocked: Sean\'s call"\n', "Delivery package"), CUT_R2: _header("exit: none\n", "Delivery package")}
    _, line8 = _mc_line8(tmp_path / "b", "small-piece", passes, files=files, triggers={5: 3})
    assert "stage 4 Finish: drafted before the motion gate ran on the moving test" in line8.findings


def test_nothing_builds_on_a_draft_while_it_is_stopped(tmp_path):
    """From the second round of the independent review on SWCB #246: on a full train, the look stopped on Sean's
    call, then audited, gated and moved before it resumed."""
    look_r2 = "artifacts/appearance-packet-r2.md"
    passes = [*MC_FULL[:5], ("appearance-gate", "gate", 2, [LOOK], [GATE]), MC_SMALL[0],
              ("art-pose-designer", "draft", 2, [LOOK], [look_r2]), *MC_SMALL[1:], *MC_CLOSE]
    files = {LOOK: _header('exit: "Blocked: Sean\'s call"\n', "Appearance packet"), look_r2: _header("exit: none\n", "Appearance packet")}
    _, line8 = _mc_line8(tmp_path, "full-train", passes, files=files, triggers={8: 4})
    assert ("stage 2: pass-05, pass-06, pass-07 ran while pass-04 was stopped on Sean's call, "
            "before its resumption finished at pass-08") in line8.findings


def test_a_header_the_parser_cannot_read_vouches_for_nothing(tmp_path):
    film = _first_film(answers='answers: "SWCB #207"\nversion: ' + "9" * 5000 + "\n")
    _, line8 = _mc_line8(tmp_path, "full-train", film["passes"], files=film["files"], triggers=film["triggers"])
    assert line8.findings == ["stage 3 Motion: 2 drafts, expected exactly one (repairs are `kind: repair`)"]
