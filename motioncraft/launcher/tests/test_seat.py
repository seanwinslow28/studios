"""Motioncraft's launcher: the context and its fence, both walls, the caps, the helper catch and the probe.

Copied in shape from Devcraft's launcher tests (devcraft/hooks/tests/test_seat.py).
The Codex layers run through `codex sandbox`, the same Seatbelt policy a seat pass
gets, with no model call, so the fence's Codex half is tested for real; that half
skips where `codex` is not installed. The launch, the caps and the probe run
against one fake `claude` and `codex` put first on PATH.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

LAUNCHER = Path(__file__).resolve().parents[1]
SEAT = LAUNCHER / "seat.py"
CODEX = shutil.which("codex")
sys.path.insert(0, str(LAUNCHER))
import seat as seatmod  # noqa: E402

PROJECT = "Film/proj-2026-10-19"
# The application doorway's tests run the real Blender where it is installed (launcher/tests/test_apps.py).
BLENDER = "/Applications/Blender.app/Contents/MacOS/Blender"


@pytest.fixture(scope="module")
def world():
    # Under the home folder, not /tmp: Codex's sandbox always lets a pass write the
    # system temp folder, which would hide a write outside the fence.
    base = Path(os.path.expanduser("~/.cache/motioncraft-launcher-test"))
    base.mkdir(parents=True, exist_ok=True)
    root = Path(os.path.realpath(base / os.urandom(4).hex()))
    root.mkdir()
    emp = root / "emp"
    (emp / "src").mkdir(parents=True)
    (emp / "src" / "x.txt").write_text("day job")
    (root / "local").mkdir()
    (root / "local" / "employer-paths").write_text(f"# the machine's list\n{emp}\n")
    media = root / "media"
    project = media / PROJECT
    for d in ("inputs", "story/animatic-v01-2026-10-19", "appearance", "motion/motion-v01-2026-10-19", "finish", "approved"):
        (project / d).mkdir(parents=True)
    (project / "motion" / "motion-v01-2026-10-19" / "scene.blend").write_text("v01")
    (root / "folders.local").write_text(f"media = {media}\n")
    eng = root / "ledger" / "engagements" / "proj-2026-10-19"
    for d in ("artifacts", "audits", "trace/logs"):
        (eng / d).mkdir(parents=True)
    (eng / "brief.md").write_text(f"---\nid: mc-eng-900\ntype: full-train\nmachine: laptop\nmedia: media:{PROJECT}\n---\n\nbrief\n")
    (eng / "d01-open.md").write_text("open")
    (eng / "artifacts" / "story-packet.md").write_text("---\nid: x\nmodel: claude-opus-5-5             # the runtime\n---\n\npacket\n")
    (eng / "artifacts" / "scene-record.md").write_text("---\nmodel: codex gpt-6.1-sol high\n---\n\nscene\n")
    # Fake skill sources and the allowlist naming them; the real file's shape, the test's own folders.
    for src, name in (("agents", "shot-composition"), ("agents", "animation-principles"), ("desk/a1/b2", "2d-animation-principles")):
        (root / "skills" / src / name).mkdir(parents=True)
        (root / "skills" / src / name / "SKILL.md").write_text(f"---\nname: {name}\n---\n\nchecklist\n")
    (root / "skills" / "desk/a1/b2/2d-animation-principles/references").mkdir()
    (root / "skills" / "desk/a1/b2/2d-animation-principles/references/smears.md").write_text("smears")
    (root / "Blender.app").mkdir()
    (root / "toolbelts.toml").write_text(f"""
[sources]
agents = "{root}/skills/agents"
desk = "{root}/skills/desk/*/*"
[seats.visual-story-director]
skills = ["agents:shot-composition"]
image = true
apps = ["blender"]
[seats.art-pose-designer]
skills = ["desk:2d-animation-principles", "agents:shot-composition"]
image = true
[seats.animator]
skills = ["desk:2d-animation-principles", "agents:animation-principles"]
apps = ["blender"]
[seats.finishing-sound-designer]
apps = ["resolve"]
sound = true
[apps]
blender = "{BLENDER}"
python = "{sys.executable}"
[env]
path = ["{root}/Blender.app"]
RESOLVE_SCRIPT_API = "{root}/Blender.app"
[never]
names = ["higgsfield", "adobe"]
""")
    env = dict(os.environ, TRACEKIT_FOLDERS=str(root / "folders.local"),
               MOTIONCRAFT_EMPLOYER_PATHS=str(root / "local" / "employer-paths"),
               MOTIONCRAFT_PASSES=str(root / "passes"), MOTIONCRAFT_SCRATCH_ROOT=str(root / "scratch"),
               MOTIONCRAFT_TOOLBELTS=str(root / "toolbelts.toml"), MOTIONCRAFT_TOOLBELT_ROOT=str(root / "toolbelt"))
    env.pop("MOTIONCRAFT_CONTEXT", None)
    w = {"root": root, "eng": eng, "project": project, "emp": emp, "home": root / "home", "env": env}
    seat(w, "toolbelt")
    yield w
    shutil.rmtree(root)


def seat(w, *args):
    r = subprocess.run([sys.executable, str(SEAT), *args], env=w["env"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return r.stdout.strip()


def fails(w, *args):
    r = subprocess.run([sys.executable, str(SEAT), *args], env=w["env"], capture_output=True, text=True)
    assert r.returncode != 0, r.stdout
    return r.stderr


def context(w, s, n, *extra):
    return seat(w, "context", "--seat", s, "--engagement", str(w["eng"]), "--pass", n, *extra)


def context_fails(w, s, n, *extra):
    return fails(w, "context", "--seat", s, "--engagement", str(w["eng"]), "--pass", n, *extra)


def ctx_data(path):
    return json.loads(Path(path).read_text())


CLAUDE_ANCHOR = ("--anchor", "artifacts/story-packet.md")
CODEX_ANCHOR = ("--anchor", "artifacts/scene-record.md")


# --- the context ------------------------------------------------------------------------

def test_caps_default_by_seat_and_override(world):
    assert ctx_data(context(world, "animator", "01"))["caps"] == {"minutes": 60, "tool_calls": 200}
    assert ctx_data(context(world, "visual-story-director", "02"))["caps"] == {"minutes": 30, "budget_usd": 15}
    assert ctx_data(context(world, "story-gate", "03", *CLAUDE_ANCHOR))["caps"] == {"minutes": 20, "tool_calls": 80}
    assert ctx_data(context(world, "motion-gate", "04", *CODEX_ANCHOR))["caps"] == {"minutes": 30, "budget_usd": 15}
    assert ctx_data(context(world, "animator", "05", "--cap-minutes", "90"))["caps"]["minutes"] == 90
    assert "no budget flag" in context_fails(world, "animator", "06", "--cap-budget-usd", "5")


def test_context_is_written_once(world):
    context(world, "art-pose-designer", "07")
    assert "written once" in context_fails(world, "art-pose-designer", "07")


def test_the_media_project_comes_from_the_brief(world):
    data = ctx_data(context(world, "animator", "08"))
    assert data["media"] == f"media:{PROJECT}" and data["media_project"] == str(world["project"])
    assert data["machine"] == seatmod.machine()


def test_no_film_job_opens_without_its_media_folder(world):
    env = dict(world["env"], TRACEKIT_FOLDERS=str(world["root"] / "nowhere.local"))
    r = subprocess.run([sys.executable, str(SEAT), "context", "--seat", "animator", "--engagement", str(world["eng"]),
                        "--pass", "09"], env=env, capture_output=True, text=True)
    assert r.returncode != 0 and "not set up on this machine" in r.stderr


def test_unknown_seat_stops(world):
    assert "unknown seat" in context_fails(world, "builder", "10")


def test_a_drafting_seat_writes_new_versions_in_its_own_stage(world):
    fence = ctx_data(context(world, "animator", "11"))["fence"]
    motion = world["project"] / "motion"
    assert str(motion) in fence["write"] and str(motion / "motion-v01-2026-10-19") in fence["frozen"]
    assert not any("story" in w for w in fence["write"]), "never another seat's stage"
    assert str(world["eng"] / "artifacts") not in fence["write"], "a pass on Codex files its record by -o"
    fence = ctx_data(context(world, "visual-story-director", "12"))["fence"]
    assert str(world["project"] / "story") in fence["write"] and str(world["eng"] / "artifacts") in fence["write"]
    assert str(world["eng"] / "artifacts" / "story-packet.md") in fence["frozen"], "a record is written once"


def test_gates_and_audits_write_only_their_scratch_folder(world):
    for data in (ctx_data(context(world, "story-gate", "13", *CLAUDE_ANCHOR)),
                 ctx_data(context(world, "motion-gate", "14", *CODEX_ANCHOR)),
                 ctx_data(context(world, "art-pose-designer", "15", "--read-only"))):
        assert data["read_only"] and data["fence"] == {"write": [data["scratch"]], "frozen": []}


def test_codex_runs_with_the_network_off(world):
    assert "network off" in context_fails(world, "animator", "16", "--host", "example.com")
    assert ctx_data(context(world, "finishing-sound-designer", "17", "--host", "127.0.0.1"))["hosts"] == ["127.0.0.1"]


def test_a_scratch_folder_starts_empty_and_private(world):
    data = ctx_data(context(world, "animator", "18"))
    scr = Path(data["scratch"])
    assert scr.is_dir() and not any(scr.iterdir()) and oct(scr.stat().st_mode & 0o777) == "0o700"
    (world["root"] / "scratch" / world["eng"].name / "pass-19").mkdir(parents=True)
    (world["root"] / "scratch" / world["eng"].name / "pass-19" / "left.txt").write_text("x")
    assert "not empty" in context_fails(world, "animator", "19")


# --- vendors: read from a record, never chosen -----------------------------------------------

def test_a_gate_runs_on_the_vendor_that_did_not_write_its_anchor(world):
    data = ctx_data(context(world, "appearance-gate", "20", *CLAUDE_ANCHOR))
    assert data["vendor"] == "codex" and data["vendor_basis"]["last_writer"] == "claude"
    data = ctx_data(context(world, "motion-gate", "21", *CODEX_ANCHOR))
    assert data["vendor"] == "claude"
    # an appearance anchor redrafted on Codex moves its gate onto Claude, with Claude's caps
    data = ctx_data(context(world, "appearance-gate", "22", *CODEX_ANCHOR))
    assert data["vendor"] == "claude" and data["caps"] == {"minutes": 30, "budget_usd": 15}
    assert "--anchor" in context_fails(world, "story-gate", "23")


def test_fallback_keeps_the_writer_vendor_with_its_ticket(world):
    link = "https://github.com/seanwinslow28/SWCB/issues/999"
    data = ctx_data(context(world, "story-gate", "24", *CLAUDE_ANCHOR, "--fallback", link))
    assert data["vendor"] == "claude" and data["vendor_basis"]["fallback"] == link
    assert "issue link" in context_fails(world, "story-gate", "25", *CLAUDE_ANCHOR, "--fallback", "later")


def test_a_verification_pass_runs_read_only_on_the_other_vendor(world):
    data = ctx_data(context(world, "art-pose-designer", "26", "--verify", "artifacts/scene-record.md"))
    assert data["vendor"] == "claude" and data["read_only"]


def failed_gate(w, name, verdict="APPEARANCE FAIL"):
    (w["eng"] / "audits" / name).write_text(f"---\nseat: appearance-gate\nverdict: {verdict}\n---\n\n## Findings\n")


def test_the_animator_climbs_to_xhigh_only_on_a_record(world):
    failed_gate(world, "motion-gate.md", "MOTION FAIL")
    data = ctx_data(context(world, "animator", "27", "--effort", "xhigh", "--escalation", "audits/motion-gate.md"))
    assert data["effort"] == "xhigh" and data["escalation"]["path"] == "audits/motion-gate.md"
    assert ctx_data(context(world, "animator", "28"))["effort"] == "high"
    assert "go together" in context_fails(world, "animator", "29", "--effort", "xhigh")
    assert "only step above" in context_fails(world, "animator", "30", "--effort", "ultra", "--escalation", "audits/motion-gate.md")
    failed_gate(world, "motion-gate-r2.md", "MOTION PASS")
    assert "not a gate FAIL" in context_fails(world, "animator", "31", "--effort", "xhigh", "--escalation", "audits/motion-gate-r2.md")


def test_a_claude_seat_redraft_climbs_onto_codex_and_writes_its_stage(world):
    failed_gate(world, "appearance-gate.md")
    data = ctx_data(context(world, "art-pose-designer", "32", "--escalation", "audits/appearance-gate.md"))
    assert data["vendor"] == "codex" and data["effort"] == "high" and data["caps"] == {"minutes": 60, "tool_calls": 200}
    assert str(world["project"] / "appearance") in data["fence"]["write"]
    assert "ledger entry" in context_fails(world, "art-pose-designer", "33", "--effort", "xhigh",
                                           "--escalation", "audits/appearance-gate.md")
    (world["eng"] / "d02-xhigh.md").write_text("Sean calls the xhigh step for Art's redraft.")
    assert ctx_data(context(world, "art-pose-designer", "34", "--effort", "xhigh", "--escalation", "d02-xhigh.md"))["effort"] == "xhigh"
    failed_gate(world, "story-gate.md", "STORY FAIL")
    assert "is a gate" in context_fails(world, "story-gate", "35", *CLAUDE_ANCHOR, "--escalation", "audits/story-gate.md")


@pytest.mark.parametrize("line,writer", [
    ("model: claude-opus-5-5", "claude"), ("model: codex gpt-6.1-sol high", "codex"),
    ("model: claude-opus-5-5 → codex gpt-6.1-sol high: appearance gate FAIL", "codex"),
    ('model: "gpt-6.1-sol (high)"', "codex"), ("model: tbd", None),
])
def test_last_writer_reads_the_model_line(line, writer):
    assert seatmod.last_writer(f"---\n{line}\n---\n") == writer


# --- the Claude wall --------------------------------------------------------------------

def test_claude_settings_fence_a_drafting_seat(world):
    ctx = context(world, "visual-story-director", "40")
    s = json.loads(Path(seat(world, "claude-settings", ctx)).read_text())
    deny, sb = s["permissions"]["deny"], s["sandbox"]
    eng, project = world["eng"], world["project"]
    assert f"Edit(/{project}/story/animatic-v01-2026-10-19/**)" in deny, "a saved version is never overwritten"
    assert f"Edit(/{project}/story/**)" not in deny and f"Edit(/{eng}/artifacts/**)" not in deny
    for other in ("appearance", "motion", "finish", "approved", "inputs"):
        assert f"Edit(/{project}/{other}/**)" in deny
    for record in ("brief.md", "d01-open.md"):
        assert f"Edit(/{eng}/{record})" in deny
    assert f"Edit(/{eng}/trace/**)" in deny and f"Edit(/{eng}/audits/**)" in deny
    assert f"Edit(/{eng}/artifacts/story-packet.md)" in deny
    assert f"Read(/{world['emp']}/**)" in deny and f"Read(/{os.path.expanduser('~/.codex')}/**)" in deny
    assert {"WebFetch", "WebSearch", "Task", "Agent"} <= set(deny)
    assert sb["enabled"] and sb["failIfUnavailable"] and sb["excludedCommands"] == []
    assert sb["network"]["allowedDomains"] == [] and sb["filesystem"]["allowWrite"] == ctx_data(ctx)["fence"]["write"]
    assert s["disableAllHooks"] and s["env"]["MOTIONCRAFT_CONTEXT"] == ctx
    # reads outside the working folders need a rule in a headless run
    allow = s["permissions"]["allow"]
    for p in (eng, project, LAUNCHER.parent, LAUNCHER.parents[1] / "craftwork", world["root"] / "toolbelt" / "visual-story-director"):
        assert f"Read(/{p}/**)" in allow
    # the Director's one way out of the sandbox is the image doorway, for this pass's own context
    assert sb["allowUnsandboxedCommands"] is True
    assert [r for r in allow if r.startswith("Bash(")] == [f"Bash({LAUNCHER / 'image.py'} --context {ctx}:*)"]
    for cmd in ("codex", "higgsfield", "gh", "git push"):
        assert f"Bash({cmd}:*)" in deny
    for root in ("~/.agents/skills", "~/.claude/skills", "~/.claude/plugins"):
        assert f"Read(/{os.path.expanduser(root)}/**)" in deny and os.path.expanduser(root) in sb["filesystem"]["denyRead"]


@pytest.mark.parametrize("seat_name,extra", [("finishing-sound-designer", ("--read-only",)), ("art-pose-designer", ("--read-only",)),
                                             ("motion-gate", CODEX_ANCHOR)])
def test_no_other_claude_pass_has_a_way_out_of_the_sandbox(world, seat_name, extra):
    ctx = context(world, seat_name, f"9{len(extra)}{seat_name[:3]}", *extra)
    s = json.loads(Path(seat(world, "claude-settings", ctx)).read_text())
    assert s["sandbox"]["allowUnsandboxedCommands"] is False
    # ffmpeg and ffprobe are let past the name=value hold, and stay sandboxed: nothing here lets a command out
    assert [r for r in s["permissions"]["allow"] if r.startswith("Bash(")] == ["Bash(ffmpeg:*)", "Bash(ffprobe:*)"]
    assert ctx_data(ctx)["toolbelt"]["image"] is False and ctx_data(ctx)["toolbelt"]["sound"] is False


def test_finishing_has_one_way_out_the_sound_doorway_and_no_ffmpeg_rule(world):
    ctx = context(world, "finishing-sound-designer", "fs1")
    s = json.loads(Path(seat(world, "claude-settings", ctx)).read_text())
    assert s["sandbox"]["allowUnsandboxedCommands"] is True and ctx_data(ctx)["toolbelt"]["sound"] is True
    # its one way out, for its own context; ffmpeg and ffprobe lose their allow rule, which would let them out too
    assert [r for r in s["permissions"]["allow"] if r.startswith("Bash(")] == [f"Bash({LAUNCHER / 'sound.py'} --context {ctx}:*)"]
    keys = os.path.expanduser("~/.config/audio-keys")
    assert f"Read(/{keys}/**)" in s["permissions"]["deny"] and keys in s["sandbox"]["filesystem"]["denyRead"]


def test_only_finishing_may_have_the_sound_path(world):
    toml = world["root"] / "toolbelts-sound.toml"
    toml.write_text((world["root"] / "toolbelts.toml").read_text().replace(
        '[seats.animator]\n', '[seats.animator]\nsound = true\n'))
    env = dict(world["env"], MOTIONCRAFT_TOOLBELTS=str(toml))
    r = subprocess.run([sys.executable, str(SEAT), "context", "--seat", "animator", "--engagement", str(world["eng"]),
                        "--pass", "fs2"], env=env, capture_output=True, text=True)
    assert r.returncode != 0 and "Finishing alone generates sound" in r.stderr


def test_a_read_only_claude_pass_writes_nothing_but_scratch(world):
    ctx = context(world, "motion-gate", "41", *CODEX_ANCHOR)
    s = json.loads(Path(seat(world, "claude-settings", ctx)).read_text())
    deny = s["permissions"]["deny"]
    assert f"Edit(/{world['eng']}/**)" in deny and f"Edit(/{world['project']}/**)" in deny
    assert s["sandbox"]["filesystem"]["allowWrite"] == [ctx_data(ctx)["scratch"]]


def test_wall_files_live_outside_the_engagement(world):
    ctx = context(world, "finishing-sound-designer", "42")
    out = Path(seat(world, "claude-settings", ctx))
    assert out == world["root"] / "passes" / world["eng"].name / "pass-42.settings.json"
    assert oct(out.stat().st_mode & 0o777) == "0o600"
    assert "written once" in fails(world, "claude-settings", ctx)
    assert "runs on Codex" in fails(world, "claude-settings", context(world, "animator", "43"))


# --- the Codex wall ---------------------------------------------------------------------

@pytest.fixture(scope="module")
def codex_home(world):
    seat(world, "codex-home", "--home", str(world["home"]))
    return world["home"]


def test_codex_home_turns_off_what_a_seat_must_not_have(world, codex_home):
    cfg = (codex_home / "config.toml").read_text()
    for f in ("plugins", "apps", "memories", "multi_agent", "image_generation"):
        assert f"{f} = false" in cfg
    assert 'default_permissions = "motioncraft-floor"' in cfg
    assert f'"{os.path.expanduser("~/.codex")}" = "deny"' in cfg and f'"{world["emp"]}" = "deny"' in cfg


def test_the_seat_home_never_sits_inside_sean_codex_home(world):
    assert "Sean's own Codex home" in fails(world, "codex-home", "--home", os.path.expanduser("~/.codex/motioncraft"))


def sandboxed(world, home, profile, cmd):
    env = dict(world["env"], CODEX_HOME=str(home))
    # the real codex by its path: the launcher tests put a fake one first on PATH
    perm = "pass-" + profile.rsplit("-pass-", 1)[1]
    r = subprocess.run([CODEX, "sandbox", "-p", profile, "-P", perm, "-C", str(world["project"]), "--", "bash", "-c", cmd],
                       env=env, capture_output=True, text=True, timeout=60)
    return "WROTE" in r.stdout


def codex_pass(w, home, n, *extra, seat_name="animator"):
    ctx = context(w, seat_name, n, *extra)
    seat(w, "codex-pass", ctx, "--home", str(home))
    return ctx


ANIMATOR_MATRIX = [
    ("mkdir {P}/motion/motion-v02-2026-10-19 && echo a > {P}/motion/motion-v02-2026-10-19/scene.blend && echo WROTE", True),
    ("echo b > {P}/motion/motion-v01-2026-10-19/scene.blend && echo WROTE", False),
    ("echo b > {P}/motion/motion-v01-2026-10-19/new.txt && echo WROTE", False),
    ("echo c > {P}/story/animatic-v01-2026-10-19/x && echo WROTE", False),
    ("echo c > {P}/approved/x && echo WROTE", False),
    ("echo d > {ENG}/artifacts/scene-record-r2.md && echo WROTE", False),
    ("cat {ENG}/brief.md && echo WROTE", True),
    ("cat {EMP}/src/x.txt && echo WROTE", False),
    ("echo e > {SCR}/probe.py && echo WROTE", True),
]


@pytest.mark.skipif(not CODEX, reason="codex not installed")
@pytest.mark.parametrize("cmd,allowed", ANIMATOR_MATRIX, ids=[c for c, _ in ANIMATOR_MATRIX])
def test_animator_fence_in_the_real_sandbox(world, codex_home, cmd, allowed):
    profile = f"{world['eng'].name}-pass-50"
    if not (codex_home / f"{profile}.config.toml").exists():
        codex_pass(world, codex_home, "50")
    scr = world["root"] / "scratch" / world["eng"].name / "pass-50"
    cmd = cmd.replace("{P}", str(world["project"])).replace("{ENG}", str(world["eng"]))
    cmd = cmd.replace("{EMP}", str(world["emp"])).replace("{SCR}", str(scr))
    assert sandboxed(world, codex_home, profile, cmd) is allowed


@pytest.mark.skipif(not CODEX, reason="codex not installed")
def test_a_codex_gate_is_read_only(world, codex_home):
    codex_pass(world, codex_home, "51", *CLAUDE_ANCHOR, seat_name="story-gate")
    profile = f"{world['eng'].name}-pass-51"
    scr = world["root"] / "scratch" / world["eng"].name / "pass-51"
    assert sandboxed(world, codex_home, profile, f"ls {world['project']}/story && echo WROTE")
    for target in (f"{world['project']}/story/new.txt", f"{world['project']}/motion/x", f"{world['eng']}/audits/story-gate.md"):
        assert not sandboxed(world, codex_home, profile, f"echo a > {target} && echo WROTE"), target
    assert sandboxed(world, codex_home, profile, f"echo a > {scr}/frame.png && echo WROTE")


def test_codex_pass_links_its_layer_into_the_seat_home(world, codex_home):
    ctx = codex_pass(world, codex_home, "52")
    link = codex_home / f"{world['eng'].name}-pass-52.config.toml"
    assert link.is_symlink() and link.resolve() == (world["root"] / "passes" / world["eng"].name / "pass-52.codex-layer.toml")
    assert "written once" in fails(world, "codex-pass", ctx, "--home", str(codex_home))
    assert "runs on Claude" in fails(world, "codex-pass", context(world, "motion-gate", "53", *CODEX_ANCHOR),
                                     "--home", str(codex_home))


# --- the launch: caps, logs, the helper catch -------------------------------------------------

# One fake for both vendors, run as `codex` or `claude` from a folder put first on
# PATH. The launcher passes PATH through its scrubbed environment and nothing
# else, so the fake reads what to do from behavior.json beside itself.
FAKE = r'''#!/usr/bin/env python3
import json, os, sys, time
from pathlib import Path
b = json.loads((Path(__file__).resolve().parent / "behavior.json").read_text())
argv = sys.argv[1:]
def out(e):
    print(json.dumps(e), flush=True)
Path(__file__).resolve().parent.joinpath("seen-env.json").write_text(json.dumps(dict(os.environ)))
if Path(sys.argv[0]).name == "claude":
    model = argv[argv.index("--model") + 1]
    for i in range(b.get("calls", 0)):
        name = b.get("tool", "Bash")
        out({"type": "assistant", "message": {"model": b.get("stamp", model), "content": [{"type": "tool_use", "id": f"t{i}", "name": name}]}})
        time.sleep(b.get("pause", 0))
    time.sleep(b.get("sleep", 0))
    if b.get("progress"):  # a long Bash call's progress, as Claude Code logs it
        out({"type": "system", "subtype": "task_started", "task_id": "b1", "description": "a long command"})
        out({"type": "tool_progress", "tool_use_id": "t0", "parent_tool_use_id": "t0", "elapsed_time_seconds": 31})
        out({"type": "system", "subtype": "task_notification", "task_id": "b1", "status": "completed"})
    if b.get("child"):  # a helper's own message under its parent's tool use
        out({"type": "assistant", "parent_tool_use_id": "t0", "message": {"model": model, "content": [{"type": "text", "text": "x"}]}})
    out({"type": "assistant", "message": {"model": b.get("stamp", model), "content": [{"type": "text", "text": "done"}]}})
    for r in [argv[j + 1] for j, x in enumerate(argv) if x == "--add-dir"] + [os.getcwd()]:
        if b.get("claude_dirs_under") and r.startswith(b["claude_dirs_under"]):
            (Path(r) / ".claude").mkdir(exist_ok=True)
    for p in b.get("make_dirs", []):  # what the pass leaves on disk, as Claude Code does after a cd
        Path(p).mkdir(parents=True, exist_ok=True)
    for p, text in b.get("make_files", {}).items():
        Path(p).parent.mkdir(parents=True, exist_ok=True)
        Path(p).write_text(text)
    out({"type": "result", "subtype": b.get("subtype", "success"), "result": b.get("answer", "FINDINGS"), "usage": {"input_tokens": 10, "output_tokens": 2}})
    sys.exit(0)
model = argv[argv.index("--model") + 1]
effort = [a for a in argv if a.startswith("model_reasoning_effort=")][0].split("=")[1].strip('"')
thread = "th-" + os.urandom(3).hex()
home = Path(os.environ["CODEX_HOME"]) / "sessions" / "2026" / "10" / "19"
home.mkdir(parents=True, exist_ok=True)
(home / f"rollout-{thread}.jsonl").write_text(
    json.dumps({"type": "session_meta", "payload": {"id": thread, "session_id": thread}}) + "\n"
    + json.dumps({"type": "turn_context", "payload": {"model": b.get("stamp", model), "effort": effort}}) + "\n")
if b.get("helper"):
    (home / f"rollout-h-{thread}.jsonl").write_text(json.dumps({"type": "session_meta", "payload": {
        "id": "h-" + thread, "session_id": thread, "thread_source": "subagent", "parent_thread_id": thread}}) + "\n")
out({"type": "thread.started", "thread_id": thread})
if "features.image_generation=true" in argv:  # the image doorway's call
    here = Path(__file__).resolve().parent
    here.joinpath("seen-stdin.txt").write_text(sys.stdin.read() if argv[-1] == "-" else "")
    here.joinpath("seen-argv.json").write_text(json.dumps(argv))
    if b.get("image", True):
        g = Path(os.environ["CODEX_HOME"]) / "generated_images" / thread
        g.mkdir(parents=True, exist_ok=True)
        (g / "exec-1.png").write_bytes(b"\x89PNG fake")
for i in range(b.get("calls", 0)):
    out({"type": "item.started", "item": {"id": f"item_{i}", "type": "command_execution", "command": "echo"}})
    out({"type": "item.completed", "item": {"id": f"item_{i}", "type": "command_execution", "command": "echo"}})
    time.sleep(b.get("pause", 0))
time.sleep(b.get("sleep", 0))
out({"type": "item.completed", "item": {"id": "msg", "type": "agent_message", "text": b.get("answer", "SCENE RECORD")}})
out({"type": "turn.completed", "usage": {"input_tokens": 100, "cached_input_tokens": 40, "output_tokens": 7}})
for i, cmd in enumerate(b.get("run", [])):  # a command the seat runs from its shell, as the doorway's ask
    import subprocess
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    Path(__file__).resolve().parent.joinpath(f"seen-run-{i}.txt").write_text(f"{r.returncode}\n{r.stdout}\n{r.stderr}")
if "-o" in argv:
    Path(argv[argv.index("-o") + 1]).write_text(b.get("answer", "SCENE RECORD") + "\n")
Path(__file__).resolve().parent.joinpath("finished").write_text("1")
sys.exit(b.get("exit", 0))
'''


@pytest.fixture(scope="module")
def fake(world):
    bin_dir = world["root"] / "fakebin"
    bin_dir.mkdir()
    for name in ("codex", "claude"):
        (bin_dir / name).write_text(FAKE)
        (bin_dir / name).chmod(0o755)
    world["env"]["PATH"] = f"{bin_dir}:{world['env']['PATH']}"
    yield bin_dir
    world["env"]["PATH"] = world["env"]["PATH"].split(":", 1)[1]


def behave(fake, **b):
    (fake / "behavior.json").write_text(json.dumps(b))
    (fake / "finished").unlink(missing_ok=True)


def launch(w, ctx, *extra):
    prompt = w["root"] / "prompt.md"
    prompt.write_text("do the work")
    return subprocess.run([sys.executable, str(SEAT), "launch", ctx, "--prompt-file", str(prompt), "--home", str(w["home"]), *extra],
                          env=w["env"], capture_output=True, text=True, timeout=120)


def record(w, n):
    return json.loads((w["eng"] / "trace" / "logs" / f"pass-{n}.launch.json").read_text())


def test_the_codex_launch_form(world, codex_home):
    ctx = codex_pass(world, codex_home, "60")
    r = launch(world, ctx, "--output", "artifacts/scene-record-60.md")
    argv = json.loads(r.stderr)["argv"]
    assert argv[:6] == ["codex", "exec", "--json", "--model", "gpt-6.1-sol", "-c"]
    assert 'model_reasoning_effort="high"' in argv and "--strict-config" in argv and 'web_search="disabled"' in argv
    assert argv[argv.index("-p") + 1] == f"{world['eng'].name}-pass-60"
    assert argv[argv.index("-C") + 1] == str(world["project"])


def test_the_claude_launch_form(world):
    ctx = context(world, "art-pose-designer", "61")
    seat(world, "claude-settings", ctx)
    argv = json.loads(launch(world, ctx).stderr)["argv"]
    assert argv[argv.index("--model") + 1] == "claude-opus-5-5" and argv[argv.index("--setting-sources") + 1] == ""
    assert "--strict-mcp-config" in argv and argv[argv.index("--max-budget-usd") + 1] == "15"
    assert argv[argv.index("--tools") + 1] == "Read,Write,Edit,Bash,Glob,Grep,Skill"
    # its file tools write only inside its working folders, so it is given only the ones the fence lets it write
    dirs = [argv[i + 1] for i, x in enumerate(argv) if x == "--add-dir"]
    assert dirs == [str(world["project"] / "appearance"), str(world["eng"] / "artifacts")]


def test_a_read_only_claude_pass_has_no_working_folder_but_scratch(world):
    ctx = context(world, "visual-story-director", "73", "--read-only")
    seat(world, "claude-settings", ctx)
    argv = json.loads(launch(world, ctx, "--output", "audits/audit-73.md").stderr)["argv"]
    assert "--add-dir" not in argv and argv[argv.index("--tools") + 1] == "Read,Write,Bash,Glob,Grep,Skill"


def test_output_rules(world, codex_home):
    ctx = codex_pass(world, codex_home, "62")
    assert "name its record" in launch(world, ctx).stderr
    assert "artifacts/ or audits/" in launch(world, ctx, "--output", "brief-2.md").stderr
    assert "written once" in launch(world, ctx, "--output", "artifacts/story-packet.md").stderr
    ctx = context(world, "art-pose-designer", "63")
    seat(world, "claude-settings", ctx)
    assert "writes its own artifact" in launch(world, ctx, "--output", "artifacts/x.md").stderr


def test_launch_kills_at_the_tool_call_cap(world, codex_home, fake):
    behave(fake, calls=10, pause=0.3)
    r = launch(world, codex_pass(world, codex_home, "64", "--cap-tool-calls", "3"), "--output", "artifacts/pass-64.md", "--run")
    rec = record(world, "64")
    assert r.returncode == 2 and rec["stopped"] == "tool-calls" and rec["outcome"].startswith("Blocked: budget")
    assert rec["tool_calls"] == 3 and not (fake / "finished").exists(), "killed, not finished"


def test_launch_kills_at_the_wall_clock(world, codex_home, fake):
    behave(fake, calls=1, sleep=60)
    r = launch(world, codex_pass(world, codex_home, "65", "--cap-minutes", "0.03"), "--output", "artifacts/pass-65.md", "--run")
    rec = record(world, "65")
    assert r.returncode == 2 and rec["stopped"] == "wall-clock" and rec["wall_clock_s"] < 20
    assert not (fake / "finished").exists()


def test_launch_files_a_clean_codex_pass(world, codex_home, fake):
    behave(fake, calls=2, answer="SCENE RECORD v1")
    r = launch(world, codex_pass(world, codex_home, "66"), "--output", "artifacts/scene-record-66.md", "--run")
    rec = record(world, "66")
    out = world["eng"] / "artifacts" / "scene-record-66.md"
    assert r.returncode == 0 and rec["stopped"] is None and rec["exit_code"] == 0
    assert out.read_text() == "SCENE RECORD v1\n"
    assert rec["outputs"] == [{"path": "artifacts/scene-record-66.md", "sha256": seatmod.sha256(out)}]
    assert rec["usage"]["input_tokens"] == 100 and rec["meter_source"] == "codex turn.completed.usage"
    assert rec["rollouts"] == {"path": "trace/logs/pass-66.rollouts", "files": 1}
    assert rec["runtime_stamps"] == ["gpt-6.1-sol high"] and rec["machine"] == seatmod.machine()
    assert rec["media"] == f"media:{PROJECT}" and rec["fence"] == ctx_data(world["eng"] / "trace" / "logs" / "pass-66.context.json")["fence"]
    wall = rec["wall_files"][0]
    assert wall["sha256"] == seatmod.sha256(Path(wall["path"])) and not wall["path"].startswith(str(world["eng"]))
    seen = json.loads((fake / "seen-env.json").read_text())
    assert seen["TMPDIR"] == rec["scratch"] and seen["CODEX_HOME"] == str(world["home"])
    assert not any(k.endswith(("TOKEN", "_KEY")) for k in seen), "a scrubbed environment"
    again = launch(world, str(world["eng"] / "trace" / "logs" / "pass-66.context.json"), "--output", "artifacts/other.md", "--run")
    assert again.returncode != 0 and "launched once" in again.stderr


def test_launch_catches_a_codex_helper_agent(world, codex_home, fake):
    behave(fake, calls=1, helper=True)
    r = launch(world, codex_pass(world, codex_home, "67"), "--output", "artifacts/scene-record-67.md", "--run")
    rec = record(world, "67")
    assert r.returncode == 3 and any("helper session" in h for h in rec["helper_agent"])
    assert not (world["eng"] / "artifacts" / "scene-record-67.md").exists(), "the record path is freed for the re-run"
    assert (world["eng"] / rec["discarded_output"]).exists() and "outputs" not in rec


def test_a_long_commands_progress_is_no_helper_but_a_helpers_message_is(world, fake):
    behave(fake, calls=1, progress=True)
    ctx = context(world, "finishing-sound-designer", "hp1")
    seat(world, "claude-settings", ctx)
    r = launch(world, ctx, "--run")
    assert r.returncode == 0, r.stderr
    assert "helper_agent" not in record(world, "hp1")
    behave(fake, calls=1, child=True)
    ctx = context(world, "finishing-sound-designer", "hp2")
    seat(world, "claude-settings", ctx)
    r = launch(world, ctx, "--run")
    assert r.returncode == 3 and record(world, "hp2")["helper_agent"] == ["a helper agent's message (parent tool use t0)"]


def test_launch_catches_a_claude_helper_agent(world, fake):
    behave(fake, calls=1, tool="Task", answer="GATE FINDINGS")
    ctx = context(world, "motion-gate", "68", *CODEX_ANCHOR)
    seat(world, "claude-settings", ctx)
    r = launch(world, ctx, "--output", "audits/motion-gate-68.md", "--run")
    rec = record(world, "68")
    assert r.returncode == 3 and rec["helper_agent"] == ["a Task tool call (t0)"]
    assert not (world["eng"] / "audits" / "motion-gate-68.md").exists()


def test_launch_files_a_read_only_claude_pass(world, fake):
    behave(fake, calls=2, answer="MOTION GATE FINDINGS", claude_dirs_under=str(world["root"]))
    ctx = context(world, "motion-gate", "69", *CODEX_ANCHOR)
    seat(world, "claude-settings", ctx)
    r = launch(world, ctx, "--output", "audits/motion-gate-69.md", "--run")
    rec = record(world, "69")
    assert r.returncode == 0 and rec["tool_calls"] == 2 and rec["meter_source"] == "claude -p result.usage"
    assert (world["eng"] / "audits" / "motion-gate-69.md").read_text() == "MOTION GATE FINDINGS\n"
    assert rec["runtime_stamps"] == ["claude-opus-5-5"]
    left = Path(rec["scratch"]) / ".claude"  # Claude Code leaves one in its working folder, the scratch folder
    assert rec["claude_dirs"]["removed"] == [str(left)] and not left.exists()


def test_a_claude_dir_left_in_a_version_folder_the_pass_made_is_swept(world, fake):
    """A pass that cd's into a version folder it made leaves `.claude/.cc-writes/` there (mc-setup-011)."""
    ctx = context(world, "finishing-sound-designer", "sw1")
    seat(world, "claude-settings", ctx)
    stage = Path(ctx_data(ctx)["fence"]["write"][1])
    older = stage / "older-v01" / ".claude"  # there before the launch: not this pass's, so not touched
    older.mkdir(parents=True)
    made, kept = stage / "takes-v01" / ".claude", stage / "takes-v02" / ".claude"
    behave(fake, calls=1, make_dirs=[str(made / ".cc-writes")],
           make_files={str(stage / "takes-v01" / "fx1-take1.mp3"): "take", str(kept / "notes.md"): "a seat's file"})
    r = launch(world, ctx, "--run")
    rec = record(world, "sw1")
    assert r.returncode == 0, r.stderr
    assert rec["claude_dirs"] == {"removed": [str(made)], "left": [str(kept)]}
    assert not made.exists() and (stage / "takes-v01" / "fx1-take1.mp3").exists()
    assert (kept / "notes.md").exists() and older.is_dir()


def test_claude_stopping_at_its_budget_is_blocked_budget(world, fake):
    behave(fake, calls=1, subtype="error_max_budget_usd")
    ctx = context(world, "visual-story-director", "70")
    seat(world, "claude-settings", ctx)
    r = launch(world, ctx, "--run")
    assert r.returncode == 2 and record(world, "70")["stopped"] == "budget-usd"


def test_a_pass_launches_on_the_machine_its_context_was_written_on(world, fake):
    ctx = context(world, "visual-story-director", "71")
    seat(world, "claude-settings", ctx)
    data = ctx_data(ctx)
    data["machine"] = "elsewhere"
    Path(ctx).write_text(json.dumps(data))
    r = launch(world, ctx, "--run")
    assert r.returncode != 0 and "one machine per job" in r.stderr


def test_a_record_changed_after_the_context_stops_the_launch(world, codex_home):
    (world["eng"] / "artifacts" / "anchor-72.md").write_text("---\nmodel: claude-opus-5-5\n---\n\nv1\n")
    ctx = codex_pass(world, codex_home, "72", "--anchor", "artifacts/anchor-72.md", seat_name="story-gate")
    (world["eng"] / "artifacts" / "anchor-72.md").write_text("---\nmodel: claude-opus-5-5\n---\n\nv2\n")
    r = launch(world, ctx, "--output", "audits/story-gate-72.md")
    assert r.returncode != 0 and "changed since the context named it" in r.stderr


# --- the probe and the preflight ------------------------------------------------------------

def test_probe_reads_the_stamp_not_the_answer(world, codex_home, fake):
    behave(fake, answer="I am some model")
    logs = world["root"] / "probe-logs"
    r = subprocess.run([sys.executable, str(SEAT), "probe", "--home", str(codex_home), "--logs", str(logs)],
                       env=world["env"], capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stdout + r.stderr
    for line in ("`claude-opus-5-5` on `claude -p`", "`gpt-6.1-sol` (high) on `codex exec`"):
        assert line in r.stdout
    assert r.stdout.count("Match.") == 2 and (logs / "probe-codex.jsonl").exists()
    behave(fake, stamp="gpt-5.4")
    r = subprocess.run([sys.executable, str(SEAT), "probe", "--home", str(codex_home)], env=world["env"],
                       capture_output=True, text=True, timeout=60)
    assert r.returncode == 1 and "MISMATCH" in r.stdout


def test_preflight_names_each_gap(world, codex_home):
    r = subprocess.run([sys.executable, str(SEAT), "check", "--home", str(codex_home)], env=world["env"],
                       capture_output=True, text=True)
    assert r.returncode == 1 and "has no sign-in" in r.stdout and r.stdout.count("GAP:") == 1
    (codex_home / "auth.json").write_text("{}")
    env = dict(world["env"], TRACEKIT_FOLDERS=str(world["root"] / "nowhere.local"))
    r = subprocess.run([sys.executable, str(SEAT), "check", "--home", str(codex_home)], env=env, capture_output=True, text=True)
    assert r.returncode == 1 and "`media` is not set up" in r.stdout
    r = subprocess.run([sys.executable, str(SEAT), "check", "--home", str(codex_home)], env=world["env"], capture_output=True, text=True)
    assert r.returncode == 0 and "clean" in r.stdout
    (codex_home / "auth.json").unlink()


# --- the toolbelts (bench/toolbelts.toml) ---------------------------------------------------

def test_a_toolbelt_is_a_plugin_of_copies_of_exactly_the_allowlist(world):
    belt = world["root"] / "toolbelt" / "art-pose-designer"
    assert json.loads((belt / ".claude-plugin" / "plugin.json").read_text())["name"] == "motioncraft-art-pose-designer"
    assert sorted(p.name for p in (belt / "skills").iterdir()) == ["2d-animation-principles", "shot-composition"]
    assert not (belt / "skills" / "shot-composition").is_symlink(), "a copy, fixed and hashed, never a link"
    assert (belt / "skills" / "2d-animation-principles" / "references" / "smears.md").is_file()
    rows = json.loads((belt / "manifest.json").read_text())["skills"]
    assert {r["skill"]: r["sha256"] for r in rows}["shot-composition"] == seatmod.tree_sha(
        world["root"] / "skills" / "agents" / "shot-composition")
    for none in ("finishing-sound-designer", "story-gate", "motion-gate"):
        assert not (world["root"] / "toolbelt" / none).exists(), f"{none} names no skill, so it loads none"


def test_the_context_fixes_the_toolbelt(world):
    data = ctx_data(context(world, "animator", "t1"))
    belt = world["root"] / "toolbelt" / "animator"
    assert data["toolbelt"]["skills"] == [
        {"skill": "2d-animation-principles", "path": str(belt / "skills" / "2d-animation-principles" / "SKILL.md")},
        {"skill": "animation-principles", "path": str(belt / "skills" / "animation-principles" / "SKILL.md")}]
    assert data["toolbelt"]["manifest_sha256"] == seatmod.sha256(belt / "manifest.json") and data["toolbelt"]["image"] is False
    assert ctx_data(context(world, "visual-story-director", "t2"))["toolbelt"]["image"] is True
    assert ctx_data(context(world, "visual-story-director", "t3", "--read-only"))["toolbelt"]["image"] is False
    assert ctx_data(context(world, "story-gate", "t4", *CLAUDE_ANCHOR))["toolbelt"] == {
        "dir": "", "skills": [], "manifest_sha256": "", "image": False, "sound": False, "apps": []}
    assert data["toolbelt"]["apps"] == ["blender"], "the Animator's app, through the doorway"
    assert ctx_data(context(world, "visual-story-director", "t2b"))["toolbelt"]["apps"] == ["blender"], "the animatic's sequencer"
    assert ctx_data(context(world, "art-pose-designer", "t2c"))["toolbelt"]["apps"] == []
    assert ctx_data(context(world, "animator", "t5b", "--read-only"))["toolbelt"]["apps"] == [], "an audit runs no app"


def test_a_changed_source_stops_the_context_until_the_copy_is_rebuilt(world):
    src = world["root"] / "skills" / "agents" / "animation-principles" / "SKILL.md"
    old = src.read_text()
    src.write_text(old + "an edit upstream\n")
    try:
        assert "changed at" in context_fails(world, "animator", "t5")
        r = subprocess.run([sys.executable, str(SEAT), "check", "--home", str(world["home"])], env=world["env"],
                           capture_output=True, text=True)
        assert r.returncode == 1 and "changed at" in r.stdout
        seat(world, "toolbelt")
        context(world, "animator", "t5")
    finally:
        src.write_text(old)
        seat(world, "toolbelt")


def test_a_missing_skill_is_a_gap(world):
    toml = world["root"] / "toolbelts-2.toml"
    toml.write_text((world["root"] / "toolbelts.toml").read_text().replace("agents:animation-principles", "agents:nowhere"))
    env = dict(world["env"], MOTIONCRAFT_TOOLBELT_ROOT=str(world["root"] / "toolbelt-2"), MOTIONCRAFT_TOOLBELTS=str(toml))
    r = subprocess.run([sys.executable, str(SEAT), "toolbelt"], env=env, capture_output=True, text=True)
    assert r.returncode == 1 and "GAP: animator: agents:nowhere is not on this machine" in r.stdout


def test_the_claude_launch_form_carries_the_seat_plugin_only(world):
    ctx = context(world, "art-pose-designer", "t6")
    seat(world, "claude-settings", ctx)
    argv = json.loads(launch(world, ctx).stderr)["argv"]
    assert argv[argv.index("--plugin-dir") + 1] == str(world["root"] / "toolbelt" / "art-pose-designer")
    assert argv.count("--plugin-dir") == 1
    ctx = context(world, "motion-gate", "t7", *CODEX_ANCHOR)
    seat(world, "claude-settings", ctx)
    assert "--plugin-dir" not in json.loads(launch(world, ctx, "--output", "audits/motion-gate-t7.md").stderr)["argv"]


def test_a_claude_prompt_names_the_image_door_only_for_the_director_and_art(world):
    director = seatmod.load(context(world, "visual-story-director", "t8"))
    prompt = seatmod.launch_argv(director, "do the work")[-1]
    assert prompt.startswith("do the work") and f"{LAUNCHER / 'image.py'} --context {director['source']}" in prompt
    finishing = seatmod.load(context(world, "finishing-sound-designer", "t9"))
    prompt = seatmod.launch_argv(finishing, "do the work")[-1]
    assert prompt.startswith("do the work") and "image.py" not in prompt and "apps.py ask resolve" in prompt
    assert f"{LAUNCHER / 'sound.py'} --context {finishing['source']}" in prompt and "-/af <file>" in prompt
    assert "sound.py" not in seatmod.launch_argv(director, "do the work")[-1]
    gate = seatmod.load(context(world, "motion-gate", "t10", "--anchor", "artifacts/scene-record.md"))
    assert seatmod.launch_argv(gate, "do the work")[-1] == "do the work", "a gate gets neither door"


def test_a_codex_prompt_carries_agents_md_and_the_skills_by_path(world, codex_home):
    ctx = seatmod.load(codex_pass(world, codex_home, "u1"))
    prompt = seatmod.launch_argv(ctx, "do the work", "p", "o")[-1]
    assert prompt.endswith("do the work") and "The studios AGENTS.md, which binds this pass" in prompt
    for s in ctx["toolbelt"]["skills"]:
        assert s["path"] in prompt
    gate = seatmod.load(codex_pass(world, codex_home, "u2", *CLAUDE_ANCHOR, seat_name="story-gate"))
    assert "toolbelt" not in seatmod.launch_argv(gate, "do the work", "p", "o")[-1]


def test_a_launch_stops_when_the_toolbelt_changed_since_the_context(world, codex_home):
    ctx = codex_pass(world, codex_home, "u3")
    man = world["root"] / "toolbelt" / "animator" / "manifest.json"
    old = man.read_text()
    man.write_text(old.replace('"seat"', '"seat_"'))
    try:
        assert "toolbelt copy changed" in launch(world, ctx, "--output", "artifacts/scene-record-u3.md").stderr
    finally:
        man.write_text(old)


def test_every_pass_carries_the_applications_paths(world, codex_home, fake):
    behave(fake, answer="SCENE RECORD")
    launch(world, codex_pass(world, codex_home, "u4"), "--output", "artifacts/scene-record-u4.md", "--run")
    seen = json.loads((fake / "seen-env.json").read_text())
    assert seen["PATH"].split(":")[-1] == str(world["root"] / "Blender.app")
    assert seen["RESOLVE_SCRIPT_API"] == str(world["root"] / "Blender.app")


@pytest.mark.skipif(not CODEX, reason="codex not installed")
def test_a_codex_pass_reads_its_toolbelt_and_no_other_skill_folder(world, codex_home):
    codex_pass(world, codex_home, "u5")
    profile = f"{world['eng'].name}-pass-u5"
    mine = world["root"] / "toolbelt" / "animator" / "skills" / "animation-principles" / "SKILL.md"
    assert sandboxed(world, codex_home, profile, f"head -1 {mine} && echo WROTE")
    outside = Path(os.path.expanduser("~/.agents/skills"))
    probe = next((p / "SKILL.md" for p in sorted(outside.iterdir()) if (p / "SKILL.md").is_file()), None) \
        if outside.is_dir() else None
    if probe:
        assert not sandboxed(world, codex_home, profile, f"head -1 '{probe}' && echo WROTE")


@pytest.mark.skipif(not CODEX or not os.path.isfile(os.path.expanduser("~/.config/audio-keys/keys.env")),
                    reason="codex or the audio keys file not on this machine")
def test_no_codex_pass_reads_the_audio_keys(world, codex_home):
    codex_pass(world, codex_home, "u6")  # every Codex pass has the same credential wall; the Animator's is one
    keys = os.path.expanduser("~/.config/audio-keys/keys.env")
    # the file is read into /dev/null: nothing of it is printed, whatever the sandbox does
    assert not sandboxed(world, codex_home, f"{world['eng'].name}-pass-u6", f"cat '{keys}' > /dev/null && echo WROTE")


# --- the image doorway (launcher/image.py) ----------------------------------------------------

IMAGE = LAUNCHER / "image.py"


@pytest.fixture()
def door(world, fake):
    """A Director pass's context, a new version folder in its stage, a prompt in its scratch, and a signed-in home."""
    world["home"].mkdir(parents=True, exist_ok=True)
    (world["home"] / "auth.json").write_text("{}")
    n = f"i{os.urandom(2).hex()}"
    ctx = context(world, "visual-story-director", n)
    vdir = world["project"] / "story" / f"boards{n}-v01-2026-10-19"
    vdir.mkdir()
    prompt = Path(ctx_data(ctx)["scratch"]) / "prompt.txt"
    prompt.write_text("a red cube on grey")
    (fake / "seen-argv.json").unlink(missing_ok=True)
    yield {"ctx": ctx, "vdir": vdir, "prompt": prompt, "n": n}
    (world["home"] / "auth.json").unlink()


def run_door(w, *args):
    env = dict(w["env"], MOTIONCRAFT_CODEX_HOME=str(w["home"]))
    return subprocess.run([sys.executable, str(IMAGE), *args], env=env, capture_output=True, text=True, timeout=60)


def test_the_door_files_one_image_and_its_prompt_beside_it(world, fake, door):
    behave(fake, exit=1)  # a run can exit 1 after the image is made (mc-setup-003)
    out = door["vdir"] / "board-01.png"
    r = run_door(world, "--context", door["ctx"], "--out", str(out), "--prompt-file", str(door["prompt"]))
    assert r.returncode == 0, r.stderr
    assert out.read_bytes() == b"\x89PNG fake" and "exited 1 after the image was made" in r.stdout
    side = json.loads((door["vdir"] / "board-01.image.json").read_text())
    assert side["label"].startswith("generated") and side["prompt"] == "a red cube on grey"
    assert side["sha256"] == seatmod.sha256(out) and side["exit_code"] == 1
    argv = json.loads((fake / "seen-argv.json").read_text())
    assert argv[argv.index("--model") + 1] == "gpt-6.1-sol" and 'model_reasoning_effort="high"' in argv and argv[-1] == "-"
    assert "a red cube on grey" in (fake / "seen-stdin.txt").read_text()
    log = world["eng"] / "trace" / "logs" / f"pass-{door['n']}.images.jsonl"
    assert json.loads(log.read_text().splitlines()[-1])["out"] == str(out)
    again = run_door(world, "--context", door["ctx"], "--out", str(out), "--prompt-file", str(door["prompt"]))
    assert again.returncode == 1 and "written once" in again.stderr


def test_the_door_sends_references_from_the_media_project_only(world, fake, door):
    behave(fake)
    ref = world["project"] / "inputs" / "ref.png"
    ref.write_bytes(b"png")
    r = run_door(world, "--context", door["ctx"], "--out", str(door["vdir"] / "b.png"), "--prompt-file",
                 str(door["prompt"]), "--ref", str(ref))
    assert r.returncode == 0, r.stderr
    argv = json.loads((fake / "seen-argv.json").read_text())
    assert argv[argv.index("-i") + 1] == str(ref) and argv[-1] == "-"
    (world["emp"] / "a.png").write_bytes(b"png")
    for bad in (world["emp"] / "a.png", world["eng"] / "brief.md"):
        r = run_door(world, "--context", door["ctx"], "--out", str(door["vdir"] / "c.png"), "--prompt-file",
                     str(door["prompt"]), "--ref", str(bad))
        assert r.returncode == 1 and "nothing else goes to the image path" in r.stderr


def test_the_door_refuses_outside_the_pass_fence(world, fake, door):
    behave(fake)
    story = world["project"] / "story"
    cases = [
        (story / "animatic-v01-2026-10-19" / "x.png", "saved before this pass"),
        (story / "x.png", "version folder directly in this seat's stage"),
        (world["project"] / "appearance" / "t-v01-2026-10-19" / "x.png", "version folder directly"),
        (world["eng"] / "artifacts" / "x.png", "version folder directly"),
        (door["vdir"] / "x.jpg", "names a .png"),
        (story / "new-v09-2026-10-19" / "x.png", "make the version folder"),
    ]
    for out, why in cases:
        r = run_door(world, "--context", door["ctx"], "--out", str(out), "--prompt-file", str(door["prompt"]))
        assert r.returncode == 1 and why in r.stderr, (out, r.stderr)
    r = run_door(world, "--context", door["ctx"], "--out", str(door["vdir"] / "y.png"), "--prompt-file",
                 str(world["eng"] / "brief.md"))
    assert r.returncode == 1 and "a file the pass wrote" in r.stderr
    assert not (fake / "seen-argv.json").exists(), "no refused call reaches Codex"


@pytest.mark.parametrize("seat_name,extra", [("finishing-sound-designer", ()), ("visual-story-director", ("--read-only",)),
                                             ("animator", ())])
def test_only_a_drafting_director_or_art_pass_may_use_the_door(world, fake, door, seat_name, extra):
    ctx = context(world, seat_name, f"j{os.urandom(2).hex()}", *extra)
    r = run_door(world, "--context", ctx, "--out", str(door["vdir"] / "z.png"), "--prompt-file", str(door["prompt"]))
    assert r.returncode == 1 and "may not call the image path" in r.stderr


def test_the_door_reads_only_a_context_in_trace_logs(world, fake, door):
    forged = Path(ctx_data(door["ctx"])["scratch"]) / "pass-99.context.json"
    forged.write_text(Path(door["ctx"]).read_text())
    r = run_door(world, "--context", str(forged), "--out", str(door["vdir"] / "z.png"), "--prompt-file", str(door["prompt"]))
    assert r.returncode == 1 and "only the coordinator writes" in r.stderr


def test_the_image_call_has_no_shell_and_files_nothing_if_it_acted(world, fake, door):
    behave(fake, calls=1)  # the run's log shows a command
    out = door["vdir"] / "acted.png"
    r = run_door(world, "--context", door["ctx"], "--out", str(out), "--prompt-file", str(door["prompt"]))
    assert r.returncode == 1 and "more than the image tool" in r.stderr and not out.exists()
    argv = json.loads((fake / "seen-argv.json").read_text())
    for f in ("shell_tool", "unified_exec"):
        assert f"features.{f}=false" in argv


def test_the_door_never_writes_through_a_planted_link(world, fake, door):
    behave(fake)
    target = world["root"] / "outside-target.json"
    (door["vdir"] / "linked.image.json").symlink_to(target)  # dangling, so it does not read as an existing file
    r = run_door(world, "--context", door["ctx"], "--out", str(door["vdir"] / "linked.png"), "--prompt-file", str(door["prompt"]))
    assert r.returncode == 1 and not target.exists() and not (door["vdir"] / "linked.png").exists()


def test_no_image_made_is_logged_and_refused(world, fake, door):
    behave(fake, image=False)
    r = run_door(world, "--context", door["ctx"], "--out", str(door["vdir"] / "none.png"), "--prompt-file", str(door["prompt"]))
    assert r.returncode == 1 and "no image was made" in r.stderr and not (door["vdir"] / "none.png").exists()


# --- the seat probe's judgement ---------------------------------------------------------------

def good_init(seat_name="art-pose-designer"):
    return {"tools": ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "Skill"], "mcp_servers": [], "model": "claude-opus-5-5",
            "plugins": [{"name": f"motioncraft-{seat_name}", "path": "/x"}, {"name": "cc-plugin-telemetry", "path": "builtin"}],
            "skills": ["debug", f"motioncraft-{seat_name}:2d-animation-principles", f"motioncraft-{seat_name}:shot-composition"]}


def judge(world, init, seat_name="art-pose-designer"):
    # in a subprocess, so the allowlist read is the test world's (seat.py reads its paths at import)
    code = ("import json, sys; sys.path.insert(0, %r); import seat; "
            "print(json.dumps(seat.judge_claude(json.loads(sys.argv[1]), json.loads(sys.argv[2]), sys.argv[3], "
            "{'skills': ['debug', 'code-review'], 'plugins': ['cc-plugin-telemetry']})))") % str(LAUNCHER)
    argv = ["claude", "--tools", "Read,Write,Edit,Bash,Glob,Grep,Skill"]
    r = subprocess.run([sys.executable, "-c", code, json.dumps(init), json.dumps(argv), seat_name], env=world["env"],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def test_the_probe_passes_a_seat_that_loads_only_its_toolbelt(world):
    assert judge(world, good_init()) == []


@pytest.mark.parametrize("change,finding", [
    (lambda i: i["mcp_servers"].append({"name": "higgsfield"}), "connectors loaded"),
    (lambda i: i["plugins"].append({"name": "adobe-for-creativity", "path": "/p"}), "plugins"),
    (lambda i: i["skills"].append("superpowers:brainstorming"), "another plugin's skill"),
    (lambda i: i["skills"].remove("motioncraft-art-pose-designer:shot-composition"), "its toolbelt skills"),
    (lambda i: i["tools"].append("Agent"), "tools"),
    (lambda i: i["skills"].append("grilling"), "outside Claude Code's built-ins"),
    (lambda i: i["plugins"].append({"name": "superpowers", "path": "builtin"}), "plugins"),
    (lambda i: i.update(model="claude-sonnet-5-5"), "model"),
], ids=["connector", "plugin", "other-skill", "missing-skill", "helper-tool", "personal-skill", "unknown-builtin", "model"])
def test_the_probe_names_what_should_not_be_there(world, change, finding):
    init = good_init()
    change(init)
    found = judge(world, init)
    assert any(finding in f for f in found), found


def test_the_codex_probe_reads_the_session_state(world):
    good = {"skills": {"includeInstructions": False}, "host_skills": {"includeInstructions": False},
            "plugins_instructions": False, "apps_instructions": False, "agents_md": {}}
    assert seatmod.judge_codex(good, "<permissions instructions>", "exec, wait\nnone\nBLOCKED") == []
    assert any("plugins_instructions" in f for f in seatmod.judge_codex(dict(good, plugins_instructions=True), "", "exec"))
    assert any("image_gen" in f for f in seatmod.judge_codex(good, "", "exec, image_gen\nnone\nBLOCKED"))
    assert any("Skill roots" in f for f in seatmod.judge_codex(good, "### Skill roots\n", "exec"))
    assert seatmod.judge_codex(good, "", "exec, list_mcp_resources\nnone\nBLOCKED", "[features]\n") == []
    assert any("connector is configured" in f for f in seatmod.judge_codex(good, "", "exec", '[mcp_servers.higgsfield]\n'))


def test_seat_files_name_the_launcher_pins():
    bench = LAUNCHER.parent / "bench"
    for s in seatmod.SEATS:
        line = next(l for l in (bench / f"{s}.md").read_text().splitlines() if l.startswith("model:"))
        want = f"codex {seatmod.CODEX_MODEL} {seatmod.CODEX_EFFORT}" if s in seatmod.CODEX_DEFAULT else seatmod.CLAUDE_MODEL
        assert line.split("#")[0].split(":", 1)[1].strip() == want, s
