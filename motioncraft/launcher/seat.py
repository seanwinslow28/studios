#!/usr/bin/env python3
"""Motioncraft's launcher: one seat pass, on either vendor, under its caps and inside its write fence.

    seat.py context   --seat S --engagement E --pass NN [--read-only] [--host H]...
                      [--cap-minutes N] [--cap-tool-calls N] [--cap-budget-usd N]
                      [--effort xhigh] [--escalation R]
                      [--verify A | --anchor A [--fallback ISSUE]]   → <E>/trace/logs/pass-NN.context.json
    seat.py claude-settings <context.json>                       → <passes>/<eng>/pass-NN.settings.json
    seat.py codex-home [--home ~/.codex-motioncraft]              → the Codex seat home
    seat.py codex-pass <context.json> [--home ...]               → <passes>/<eng>/pass-NN.codex-layer.toml,
                                                                   linked as <home>/<eng>-pass-NN.config.toml
    seat.py launch <context.json> --prompt-file F [--output A] [--home ...] [--run]
                                                                 → <E>/trace/logs/pass-NN.{jsonl,stderr.log,launch.json}
    seat.py probe [--home ...]                                   → the Route entry's model check
    seat.py toolbelt                                             → each seat's allowlisted skills, copied to
                                                                   ~/.local/share/motioncraft/toolbelt/<seat>/
    seat.py seat-probe [--seat S]... [--home ...] [--logs DIR]   → one probe pass per seat: only its toolbelt loads
    seat.py check [--home ...]                                   → this machine's preflight; exit 1 on any gap

The coordinator runs these; no seat does. Written on the Motioncraft build map's
"Build the slim Motioncraft launcher" ticket (2026-10-19), as ruled on Master
skill design (SWCB #192, item 10): copied from Devcraft's `devcraft/hooks/seat.py`
with only what Motioncraft needs, Devcraft untouched. Kept: the per-pass caps and
the kill at 100%, the model probe, the isolated launch on both vendors, the vendor
read from a record (a gate's anchor, a verification pass's repair, a redraft's
escalation), helper-agent detection, the scratch folder, and the logs the trace
record is built from. Added: the write fence, which lets a drafting seat write
only new version folders in its own stage of the media project and new files in
the engagement's `artifacts/`, and keeps every gate and audit read-only; and the
machine check, since a pass launches on the machine its context was written on.
Left with Devcraft: the guard hook, the git hooks, worktrees, the frozen diff and
the release gate's evidence. The per-seat launch forms were finished on the map's
"Plugin allowlist and launch form for seat runs" ticket (2026-10-19): each seat's
skills come only from bench/toolbelts.toml, copied per machine and fixed in the
context by hash; every other skill folder is denied; a Codex pass gets the studios
AGENTS.md and its skills by path in its prompt; the Director's and Art's Claude
passes reach the Codex image path only through launcher/image.py; and seat-probe
shows each seat loads only its toolbelt. Finishing's Claude pass reaches ElevenLabs
and Lyria only through launcher/sound.py (the map's "Finishing's sound doorway"
ticket, 2026-10-19).
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import re
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import threading
import time
import tomllib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

HERE = Path(__file__).resolve().parent
MOTIONCRAFT = HERE.parent
STUDIOS = MOTIONCRAFT.parent
sys.path.insert(0, str(STUDIOS / "craftwork" / "trace"))
from tracekit import codexlog  # noqa: E402
from tracekit.folders import load_folders, split_named  # noqa: E402

HOME = Path(os.path.expanduser("~"))
DEFAULT_HOME = HOME / ".codex-motioncraft"
KEEP_ENV = ("HOME", "USER", "LOGNAME", "PATH", "LANG", "LC_ALL", "TMPDIR", "TERM", "SHELL")

# --- the bench, as data (motioncraft/bench/README.md) ----------------------------------

SEATS = ("visual-story-director", "art-pose-designer", "animator", "finishing-sound-designer")
GATES = ("story-gate", "appearance-gate", "motion-gate")
# The vendor a seat runs on unless a record moves it: the Animator writes on Codex, and the
# story and appearance gates run there because Claude writes their anchors.
CODEX_DEFAULT = ("animator", "story-gate", "appearance-gate")
# Each drafting seat's stage folder in the media project (source contract § 1).
STAGE_DIRS = {"visual-story-director": "story", "art-pose-designer": "appearance",
              "animator": "motion", "finishing-sound-designer": "finish"}

# The pinned ids (bench README, "Baselines"). The config default never picks a pass's model.
CLAUDE_MODEL = "claude-opus-5-5"
CODEX_MODEL = "gpt-6.1-sol"
CODEX_EFFORT = "high"
# The one step above it on the ruled ladder; past it, stop and ask Sean. Never `ultra`, never `max`.
CODEX_ESCALATED_EFFORT = "xhigh"

# Per-pass caps, the master skill's day-one defaults; `context --cap-*` overrides them at Open.
CLAUDE_CAPS = {"minutes": 30, "budget_usd": 15}
DEFAULT_CAPS = {
    "animator": {"minutes": 60, "tool_calls": 200},
    "story-gate": {"minutes": 20, "tool_calls": 80},
    "appearance-gate": {"minutes": 20, "tool_calls": 80},
    **{s: dict(CLAUDE_CAPS) for s in ("visual-story-director", "art-pose-designer", "finishing-sound-designer", "motion-gate")},
}
# A pass that moves vendor takes the caps of the vendor and kind of pass it becomes.
MOVED_CAPS = {"claude": CLAUDE_CAPS, "codex-redraft": DEFAULT_CAPS["animator"], "codex-read-only": DEFAULT_CAPS["story-gate"]}

# Gate findings, the held checks among them, by the gate schedule's names (with a part and a round).
GATE_FINDINGS = re.compile(r"audits/(story-gate|appearance-gate|motion-gate|revision-check)(-[a-z0-9-]+?)?(-r\d+)?\.md")
LEDGER_ENTRY = re.compile(r"d\d+-[^/]+\.md")
VENDOR_RECORD_DIRS = ("artifacts",)
ISSUE_LINK = re.compile(r"https://github\.com/[\w.-]+/[\w.-]+/issues/\d+")
# The `codex exec --json` items that are tool calls; agent_message, reasoning and todo_list are not.
CODEX_TOOL_ITEMS = ("command_execution", "file_change", "mcp_tool_call", "web_search", "collab_tool_call")
# Claude's tools that start a helper agent; every seat is denied them, and a log that shows one is caught.
CLAUDE_HELPER_TOOLS = ("Task", "Agent")
KILL_GRACE_S = 10
CODEX_FEATURES_OFF = (
    "apps", "plugins", "remote_plugin", "multi_agent", "memories", "browser_use", "computer_use",
    "in_app_browser", "image_generation", "goals", "skill_mcp_dependency_install", "shell_snapshot",
)

# --- what no pass reads -------------------------------------------------------------------

CREDENTIAL_PATHS = tuple(str(HOME / p) for p in (
    ".ssh", ".aws", ".gnupg", ".config/gh", ".config/swcb/secrets", ".config/devcraft", ".config/motioncraft",
    ".config/audio-keys",
    ".codex/auth.json", ".codex-devcraft/auth.json", ".codex-motioncraft/auth.json", ".claude/.credentials.json",
    ".netrc", ".git-credentials", ".docker/config.json", ".npmrc", ".pypirc",
    ".kube/config", ".config/gcloud", ".azure", "Library/Keychains",
))
# Sean's own Codex home: never a seat's. The one opening is Codex's own install, which its sandbox re-runs.
SEAN_HOMES = (str(HOME / ".codex"),)
SEAN_HOME_OPEN = (str(HOME / ".codex" / "packages"),)
# The machine's employer folders, one per line, written by hand outside every repo. It is the
# same list Devcraft's wall reads (one list per machine); never tracked, never shown to a seat.
EMPLOYER_PATHS_FILE = Path(os.environ.get("MOTIONCRAFT_EMPLOYER_PATHS", str(HOME / ".config" / "devcraft" / "employer-paths")))
PASSES_ROOT = Path(os.path.expanduser(os.environ.get("MOTIONCRAFT_PASSES", "~/.config/motioncraft/passes")))
SCRATCH_ROOT = Path(os.path.expanduser(os.environ.get("MOTIONCRAFT_SCRATCH_ROOT", "~/.cache/motioncraft/scratch")))
# The studio folders a Claude pass is given to read beside its engagement and media project.
STUDIO_READS = ("bench", "lanes", "corpus", "templates")

# --- the plugin allowlist (bench/toolbelts.toml) ---------------------------------------

TOOLBELTS = Path(os.environ.get("MOTIONCRAFT_TOOLBELTS", str(MOTIONCRAFT / "bench" / "toolbelts.toml")))
# This machine's copies of each seat's toolbelt, outside every repo; on Claude each is the seat's plugin.
TOOLBELT_ROOT = Path(os.path.expanduser(os.environ.get("MOTIONCRAFT_TOOLBELT_ROOT", "~/.local/share/motioncraft/toolbelt")))
# The Director's and Art's one way to the Codex image path, let out of the Claude sandbox by its own rule.
IMAGE_DOOR = HERE / "image.py"
# Finishing's one way to generated sound (ElevenLabs effects, Lyria music), let out the same way.
SOUND_DOOR = HERE / "sound.py"
SOUND_SEAT = "finishing-sound-designer"
# Every other place skills live on these Macs: no pass reads them, so a pass's skills are its toolbelt's.
SKILL_ROOTS = tuple(str(HOME / p) for p in (
    ".agents/skills", ".claude/skills", ".claude/plugins", "Library/Application Support/Claude",
    ".codex-motioncraft/skills", ".codex-devcraft/skills",
))
# Commands no Claude pass runs: images come only through the doorway, and no other generator or uploader.
CLAUDE_DENIED_COMMANDS = ("codex", "higgsfield", "nlm", "hyperframes")
# Claude Code holds an ffmpeg or ffprobe call with a name=value argument (`stream=width`, `ebur128=peak=true`) for
# an approval no one is there to give (live passes, 2026-10-19). An allow rule lets them run, still sandboxed, on a
# pass with no way out of the sandbox; on a pass with a doorway (the Director's, Art's and Finishing's drafting
# passes) the same rule would let them out, so not there: those passes put a filter in a file instead.
CLAUDE_HELD_COMMANDS = ("ffmpeg", "ffprobe")
# Blender, Resolve and Krita run for a pass only through the application doorway (launcher/apps.py), on the
# launcher's side of the sandbox under a lock written from the pass's context; none works inside a vendor's sandbox.
APPS_DOOR = HERE / "apps.py"
SEAT_APPS = ("blender", "resolve", "krita")


def die(msg: str) -> None:
    sys.stderr.write(f"seat.py: {msg}\n")
    sys.exit(1)


def real(p: str) -> str:
    return os.path.realpath(os.path.expanduser(p))


def under(path: str, root: str) -> bool:
    return path == root or path.startswith(root.rstrip("/") + "/")


def toml_str(s: str) -> str:
    return json.dumps(s)  # a JSON string is a valid TOML basic string


def sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def machine() -> str:
    return socket.gethostname().split(".")[0]


def employer_paths() -> List[str]:
    """The machine's employer folders; a missing list is a gap the preflight names, never a guess."""
    if not EMPLOYER_PATHS_FILE.is_file():
        return []
    lines = [l.strip() for l in EMPLOYER_PATHS_FILE.read_text(encoding="utf-8").splitlines()]
    return [real(l) for l in lines if l and not l.startswith("#")]


def default_vendor(seat: str) -> str:
    return "codex" if seat in CODEX_DEFAULT else "claude"


# --- the toolbelts ----------------------------------------------------------------------

def toolbelts() -> Dict:
    if not TOOLBELTS.is_file():
        die(f"no plugin allowlist at {TOOLBELTS}")
    return tomllib.loads(TOOLBELTS.read_text(encoding="utf-8"))


def seat_belt(seat: str) -> Dict:
    """A seat's allowlist line: its skills as (source, name), whether it may call the image or sound path, and its apps."""
    line = toolbelts().get("seats", {}).get(seat, {})
    skills = [tuple(s.split(":", 1)) for s in line.get("skills", [])]
    apps = list(line.get("apps", []))
    bad = [x for x in apps if x not in SEAT_APPS]
    if bad:
        die(f"the allowlist gives {seat} {', '.join(bad)}; the application doorway runs only {', '.join(SEAT_APPS)}")
    if line.get("sound") and seat != SOUND_SEAT:
        die(f"the allowlist gives {seat} the sound path; Finishing alone generates sound")
    return {"skills": skills, "image": bool(line.get("image")), "sound": bool(line.get("sound")), "apps": apps}


def source_dir(source: str) -> Optional[Path]:
    """Where a source's skills are on this machine: its path, or its glob's newest match."""
    pattern = toolbelts().get("sources", {}).get(source)
    if not pattern:
        die(f"the allowlist names a source `{source}` its [sources] table does not")
    hits = [Path(p) for p in glob.glob(os.path.expanduser(pattern)) if os.path.isdir(p)]
    return max(hits, key=lambda p: p.stat().st_mtime) if hits else None


def tree_sha(root: Path) -> str:
    """One hash over a folder's files, by relative path and content, so any edit or added file changes it."""
    h = hashlib.sha256()
    for f in sorted(p for p in root.rglob("*") if p.is_file() and not ({"__pycache__", ".DS_Store"} & set(p.parts))):
        h.update(str(f.relative_to(root)).encode() + b"\0" + f.read_bytes() + b"\0")
    return h.hexdigest()


def belt_dir(seat: str) -> Path:
    return TOOLBELT_ROOT / seat


def plugin_name(seat: str) -> str:
    return f"motioncraft-{seat}"


def build_belt(seat: str) -> List[str]:
    """Copy a seat's skills into its toolbelt folder, as a Claude plugin with a manifest; the gaps."""
    belt, gaps, rows = seat_belt(seat), [], []
    if not belt["skills"]:
        shutil.rmtree(belt_dir(seat), ignore_errors=True)
        return gaps
    tmp = TOOLBELT_ROOT / f".{seat}.building"
    shutil.rmtree(tmp, ignore_errors=True)
    (tmp / ".claude-plugin").mkdir(parents=True)
    for source, name in belt["skills"]:
        root = source_dir(source)
        src = root / name if root else None
        if not src or not (src / "SKILL.md").is_file():
            gaps.append(f"{seat}: {source}:{name} is not on this machine")
            continue
        shutil.copytree(src, tmp / "skills" / name, symlinks=False, ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"))
        rows.append({"skill": name, "source": source, "from": str(src), "sha256": tree_sha(src)})
    (tmp / ".claude-plugin" / "plugin.json").write_text(json.dumps({
        "name": plugin_name(seat), "version": datetime.now().strftime("%Y.%m.%d"),
        "description": f"Motioncraft's {seat} toolbelt, copied by seat.py toolbelt from bench/toolbelts.toml"}, indent=2) + "\n")
    (tmp / "manifest.json").write_text(json.dumps({
        "seat": seat, "built": now(), "machine": machine(), "allowlist_sha256": sha256(TOOLBELTS), "skills": rows}, indent=2) + "\n")
    shutil.rmtree(belt_dir(seat), ignore_errors=True)
    os.replace(tmp, belt_dir(seat))
    return gaps


def belt_gaps(seat: str) -> List[str]:
    """Why a seat's toolbelt copy is not ready: not built, a skill missing or extra, or a source changed since."""
    want = [n for _, n in seat_belt(seat)["skills"]]
    if not want:
        return []
    man = belt_dir(seat) / "manifest.json"
    if not man.is_file():
        return [f"{seat}: no toolbelt copy (seat.py toolbelt)"]
    rows = {r["skill"]: r for r in json.loads(man.read_text())["skills"]}
    gaps = [f"{seat}: {n} is missing from its toolbelt copy (seat.py toolbelt)" for n in want if n not in rows]
    gaps += [f"{seat}: its toolbelt copy holds {n}, which the allowlist does not name (seat.py toolbelt)"
             for n in rows if n not in want]
    for n, r in rows.items():
        if Path(r["from"]).is_dir() and tree_sha(Path(r["from"])) != r["sha256"]:
            gaps.append(f"{seat}: {n} changed at {r['from']} since its copy; read the change, then seat.py toolbelt")
    return gaps


def context_belt(seat: str, vendor: str, read_only: bool) -> Dict:
    """The toolbelt a pass runs with, fixed in its context: the copy's skills by path, and its manifest's hash."""
    gaps = belt_gaps(seat)
    if gaps:
        die("; ".join(gaps))
    belt = seat_belt(seat)
    skills = [{"skill": n, "path": str(belt_dir(seat) / "skills" / n / "SKILL.md")} for _, n in belt["skills"]]
    return {"dir": str(belt_dir(seat)) if skills else "", "skills": skills,
            "manifest_sha256": sha256(belt_dir(seat) / "manifest.json") if skills else "",
            "image": belt["image"] and vendor == "claude" and not read_only,
            "sound": belt["sound"] and vendor == "claude" and not read_only,
            # Blender, Resolve and Krita, through the application doorway: a drafting pass's, on either vendor
            "apps": [] if read_only else belt["apps"]}


def app_env() -> Tuple[List[str], Dict[str, str]]:
    """What every pass's environment carries for its applications: folders for PATH, and variables."""
    env = dict(toolbelts().get("env", {}))
    path = [os.path.expanduser(p) for p in env.pop("path", [])]
    return path, {k: os.path.expanduser(str(v)) for k, v in env.items()}


def cmd_toolbelt(a) -> None:
    TOOLBELT_ROOT.mkdir(parents=True, exist_ok=True)
    gaps = []
    for s in SEATS + GATES:
        found = build_belt(s)
        gaps += found
        for source, n in seat_belt(s)["skills"]:
            if not any(f"{source}:{n} " in g for g in found):
                print(f"{s}: {n}")
    for g in gaps:
        print(f"GAP: {g}")
    print(f"toolbelts at {TOOLBELT_ROOT}: " + ("built" if not gaps else f"{len(gaps)} gap(s)"))
    sys.exit(1 if gaps else 0)


# --- the context ------------------------------------------------------------------------

def brief_media(eng: str) -> Tuple[str, str]:
    """The media project the brief names (`media: media:<film>/<project>`), and where it is on this machine."""
    brief = Path(eng) / "brief.md"
    if not brief.is_file():
        die(f"no brief at {brief}; the context reads the media project from the brief's media: line")
    m = re.match(r"---\n(.*?)\n---", brief.read_text(encoding="utf-8"), re.S)
    line = re.search(r"^media:\s*\"?([^\"#\s]+)\"?", m.group(1), re.M) if m else None
    named = split_named(line.group(1)) if line else None
    if not named:
        die("the brief's header has no media: line naming the project as media:<film>/<project>")
    folders = load_folders(STUDIOS)
    where = folders.resolve(*named)
    if where is None:
        die(f"`{named[0]}` is not set up on this machine (folders.local); no film job opens without its media folder")
    where = Path(real(str(where)).rstrip("/"))
    if not where.is_dir():
        die(f"the media project {line.group(1)} is not at {where} on this machine")
    return line.group(1), str(where)


def fence(seat: str, eng: str, project: str, read_only: bool, vendor: str, scratch: str) -> Dict:
    """What the pass may write, and what inside those folders stays as it is, as they stand now.

    A drafting pass writes new version folders in its own stage of the media project
    and, on Claude, new files in the engagement's artifacts/ (a pass on Codex files its
    one output by -o). Every version folder and artifact already there is frozen: a
    change is a new version (rule 5) and a record is written once. A gate, an audit
    and a verification pass write only their scratch folder; the launcher files their
    findings. Anything created after the context is written is outside these lists.
    """
    write, frozen = [scratch], []
    if not read_only and seat in STAGE_DIRS:
        stage = Path(project) / STAGE_DIRS[seat]
        stage.mkdir(parents=True, exist_ok=True)
        write.append(str(stage))
        frozen += sorted(str(p) for p in stage.iterdir())
        if vendor == "claude":
            arts = Path(eng) / "artifacts"
            arts.mkdir(parents=True, exist_ok=True)
            write.append(str(arts))
            frozen += sorted(str(p) for p in arts.iterdir())
    return {"write": write, "frozen": frozen}


def cmd_context(a) -> None:
    if a.seat not in SEATS + GATES:
        die(f"unknown seat {a.seat}; the seats are {', '.join(SEATS + GATES)}")
    eng = real(a.engagement)
    if not os.path.isdir(eng):
        die(f"no engagement folder at {eng}")
    out = Path(eng) / "trace" / "logs" / f"pass-{a.pass_id}.context.json"
    if out.exists():
        die(f"{out} exists; a pass's context is written once")
    media, project = brief_media(eng)
    read_only = a.seat in GATES or a.read_only or bool(a.verify)
    escalation = context_escalation(a, eng)
    vendor, basis = context_vendor(a, eng, escalation)
    if a.host and vendor != "claude":
        die("a pass on Codex runs with the network off; --host is for a pass on Claude")
    context_belt(a.seat, vendor, read_only)  # a toolbelt not ready stops here, before the scratch folder
    scratch = real(str(SCRATCH_ROOT / os.path.basename(eng) / f"pass-{a.pass_id}"))
    make_scratch(scratch)
    data = {
        "seat": a.seat, "engagement": eng, "pass": a.pass_id, "machine": machine(),
        "media": media, "media_project": project,
        "read_only": read_only, "vendor": vendor, "vendor_basis": basis,
        "caps": context_caps(a, vendor, read_only),
        "effort": a.effort or (CODEX_EFFORT if vendor == "codex" else ""), "escalation": escalation,
        "hosts": a.host, "scratch": scratch,
        "fence": fence(a.seat, eng, project, read_only, vendor, scratch),
        "toolbelt": context_belt(a.seat, vendor, read_only),
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2) + "\n")
    print(out)


def make_scratch(path: str) -> None:
    """The pass's scratch folder: new, empty, private, and inside no repo."""
    p = Path(path)
    for d in (p, *p.parents):
        if (d / ".git").exists():
            die(f"the scratch folder {p} is inside the repo at {d}; set MOTIONCRAFT_SCRATCH_ROOT outside every repo")
    if p.exists() and any(p.iterdir()):
        die(f"the scratch folder {p} is not empty; a pass starts with an empty one")
    p.mkdir(parents=True, exist_ok=True)
    for d in (p, p.parent, Path(real(str(SCRATCH_ROOT)))):
        os.chmod(d, 0o700)


def context_caps(a, vendor: str, read_only: bool) -> Dict[str, float]:
    """The pass's default caps, with any override the Open stated (it records the why in the brief).

    On its own vendor a pass takes its seat's caps; moved, it takes the caps of
    the vendor and kind of pass it becomes.
    """
    if vendor == default_vendor(a.seat):
        caps = dict(DEFAULT_CAPS[a.seat])
    elif vendor == "claude":
        caps = dict(MOVED_CAPS["claude"])
    else:
        caps = dict(MOVED_CAPS["codex-read-only" if read_only else "codex-redraft"])
    for key, val in (("minutes", a.cap_minutes), ("tool_calls", a.cap_tool_calls), ("budget_usd", a.cap_budget_usd)):
        if val is None:
            continue
        if val <= 0:
            die(f"--cap-{key.replace('_', '-')} must be positive")
        if key == "budget_usd" and vendor != "claude":
            die(f"{a.seat} runs on Codex in this pass, which has no budget flag; cap it by minutes and tool calls")
        caps[key] = val
    return caps


def engagement_record(eng: str, path: str, flag: str) -> Tuple[Path, str, str]:
    """A record a flag names: a file inside the engagement folder, with its relative path and text."""
    rec = Path(real(os.path.join(eng, path)))
    rel = os.path.relpath(rec, eng)
    if rel.startswith(".."):
        die(f"{flag} names a record in the engagement folder, not {rec}")
    if not rec.is_file():
        die(f"no record at {rel}")
    return rec, rel, rec.read_text(encoding="utf-8")


def context_escalation(a, eng: str) -> Optional[Dict[str, str]]:
    """The record that sends a redraft one tier up, or None.

    The ladder (craftwork § Model delegation) is Opus 5.5 → Codex high → Codex
    xhigh → stop and ask Sean. The Animator starts at Codex high, so its step is
    `--effort xhigh`; a Claude seat's step is onto Codex at high, and the one
    after that, at xhigh, only on a ledger entry that names it. The record is the
    gate FAIL that sent the redraft up (audits/<gate>[-<part>][-rN].md, its verdict
    a FAIL), or the ledger entry where the coordinator or Sean called the step for
    another trigger, which must name it. Its hash goes in the context.
    """
    if not a.escalation:
        if a.effort:
            die("an effort step and its record go together: --effort xhigh --escalation <gate FAIL or ledger entry>")
        return None
    if a.seat in GATES:
        die(f"{a.seat} is a gate: a FAIL sends the owning seat's redraft one tier up, and the gate re-runs at its default")
    if a.verify:
        die("a verification pass judges a repair and is never one; --verify and --escalation do not go together")
    if a.seat == "animator" and not a.effort:
        die("an effort step and its record go together: --effort xhigh --escalation <gate FAIL or ledger entry>")
    if a.effort and a.effort != CODEX_ESCALATED_EFFORT:
        die(f"--effort {a.effort}: the only step above {CODEX_EFFORT} is {CODEX_ESCALATED_EFFORT}; past it, stop and ask Sean")
    rec, rel, text = engagement_record(eng, a.escalation, "--escalation")
    step = CODEX_ESCALATED_EFFORT if a.effort else "Codex"
    if GATE_FINDINGS.fullmatch(rel):
        m = re.search(r'^verdict:\s*"?(.*?)"?\s*$', text, re.M)
        verdict = m.group(1) if m else ""
        if not re.search(r"\bFAIL\b", verdict):
            die(f"{rel} is not a gate FAIL (verdict: {verdict or 'none'}), so it sends no redraft up")
        if a.effort and a.seat != "animator":
            die(f"a gate FAIL sends {a.seat} one tier up, onto Codex {CODEX_MODEL} {CODEX_EFFORT}; "
                f"the step past it, to {CODEX_ESCALATED_EFFORT}, takes a ledger entry that names it")
    elif LEDGER_ENTRY.fullmatch(rel):
        if step.lower() not in text.lower():
            die(f"{rel} does not name the {step} step; the entry that calls an escalation says which")
    else:
        die(f"--escalation names gate findings (audits/<gate>[-rN].md) or a ledger entry (dNN-<slug>.md), not {rel}")
    return {"path": rel, "sha256": sha256(rec)}


def last_writer(text: str) -> Optional[str]:
    """The vendor that last wrote an artifact, from its header's `model:` line, or None.

    `claude-opus-5-5`, `codex gpt-6.1-sol high`, or `claude-opus-5-5 → codex
    gpt-6.1-sol high: story gate FAIL`, where the runtime after the last arrow wrote it.
    """
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    line = re.search(r"^model:\s*(.*)$", m.group(1), re.M) if m else None
    if not line:
        return None
    value = re.sub(r"\s+#.*$", "", line.group(1)).strip().strip("\"'")
    value = re.sub(r"\([^)]*\)", "", value)
    runtime = re.split(r"→|->", value)[-1].split(":")[0].strip().lower()
    if runtime.startswith("claude-"):
        return "claude"
    if runtime.startswith(("codex", "gpt-")):
        return "codex"
    return None


def context_vendor(a, eng: str, escalation: Optional[Dict[str, str]]) -> Tuple[str, Dict]:
    """The vendor this pass runs on, and the record that says so.

    A gate names its anchor and runs on the vendor that did not last write it; a
    verification pass names the repaired artifact and runs on the vendor that did
    not write the repair. `--fallback` keeps either on the writer's vendor when the
    planned one is unavailable, naming the re-run ticket. A redraft one tier up
    runs on Codex. Anything else runs on its seat's own vendor.
    """
    if a.anchor and a.seat not in GATES:
        die(f"--anchor is a gate's; {a.seat} names a repaired artifact with --verify, or a redraft's record with --escalation")
    if a.verify and a.seat in GATES:
        die(f"{a.seat} is a gate: it names the file it reviews with --anchor, not --verify")
    if a.seat in GATES and not a.anchor:
        die(f"{a.seat} names the file it reviews with --anchor (artifacts/…), so it runs on the vendor that did not last write it")
    if a.fallback and not (a.anchor or a.verify):
        die("--fallback is for a gate or a verification pass whose planned vendor is unavailable")
    if escalation:
        return "codex", {"by": "escalation", **escalation}
    if not (a.anchor or a.verify):
        return default_vendor(a.seat), {"by": "seat"}
    flag, path = ("--anchor", a.anchor) if a.anchor else ("--verify", a.verify)
    rec, rel, text = engagement_record(eng, path, flag)
    if rel.split(os.sep)[0] not in VENDOR_RECORD_DIRS or rel.count(os.sep) < 1:
        die(f"{flag} names an artifact in artifacts/, not {rel}")
    writer = last_writer(text)
    if writer is None:
        die(f"cannot tell who last wrote {rel}: its header has no model: line naming a claude-… or codex … runtime")
    basis = {"by": flag[2:], "path": rel, "sha256": sha256(rec), "last_writer": writer}
    if not a.fallback:
        return ("codex" if writer == "claude" else "claude"), basis
    if not ISSUE_LINK.fullmatch(a.fallback):
        die("--fallback names the re-run ticket filed for it, as a GitHub issue link")
    basis["fallback"] = a.fallback
    return writer, basis


def load(path: str) -> Dict:
    ctx = json.loads(Path(path).read_text())
    ctx["source"] = real(path)
    return ctx


def pass_id_of(context_path: str) -> str:
    return Path(context_path).name.split(".")[0]  # pass-NN


def passes_dir(ctx: Dict) -> Path:
    """Where a pass's wall files live: outside every repo, since they hold the employer paths."""
    d = PASSES_ROOT / os.path.basename(ctx["engagement"])
    d.mkdir(parents=True, exist_ok=True)
    for p in (PASSES_ROOT, d):
        os.chmod(p, 0o700)
    return d


def wall_file(ctx: Dict) -> Path:
    suffix = "settings.json" if ctx["vendor"] == "claude" else "codex-layer.toml"
    return passes_dir(ctx) / f"{pass_id_of(ctx['source'])}.{suffix}"


def write_once(path: Path, text: str) -> None:
    if path.exists() or path.is_symlink():
        die(f"{path} exists; a pass's wall is written once, so a changed wall is a new pass")
    path.write_text(text)
    os.chmod(path, 0o600)


def no_read(ctx: Dict) -> List[str]:
    """Credentials, Sean's own Codex home, the employer folders, every skill folder but the pass's own
    toolbelt copy, and the engagement's other scratch folders."""
    parent = Path(ctx["scratch"]).parent
    others = sorted(str(d) for d in parent.iterdir() if d.is_dir() and str(d) != ctx["scratch"]) if parent.is_dir() else []
    return list(CREDENTIAL_PATHS) + list(SEAN_HOMES) + employer_paths() + list(SKILL_ROOTS) + others


# --- a pass on Claude -------------------------------------------------------------------

def studio_reads() -> List[str]:
    return [str(MOTIONCRAFT / d) for d in STUDIO_READS if (MOTIONCRAFT / d).is_dir()]


def add_dirs(ctx: Dict) -> List[str]:
    """The folders a Claude pass is given beside its working one, the scratch folder: only the ones it writes.

    Claude's file tools write only inside its working folders (anything else would
    need an approval no one is there to give), so giving it just the fence's folders
    keeps Write from creating a file anywhere else; its Edit denies freeze what
    is already inside them. It reads the engagement, the media project and the
    studio's files from outside them.
    """
    return [w for w in ctx["fence"]["write"] if w != ctx["scratch"]]


def claude_reads(ctx: Dict) -> List[str]:
    """What a Claude pass reads from outside its working folders: the job, the studio and its law, and its toolbelt."""
    reads = [ctx["engagement"], ctx["media_project"], str(MOTIONCRAFT), str(STUDIOS / "craftwork")]
    reads += [ctx["toolbelt"]["dir"]] * bool(ctx["toolbelt"]["dir"])
    return reads + [str(STUDIOS / "AGENTS.md")] * (STUDIOS / "AGENTS.md").exists()


def image_rule(ctx: Dict) -> str:
    """The one command a Director's or Art's pass may run outside the sandbox: the image doorway, for this pass."""
    return f"Bash({IMAGE_DOOR} --context {ctx['source']}:*)"


def sound_rule(ctx: Dict) -> str:
    """The one command a Finishing pass may run outside the sandbox: the sound doorway, for this pass."""
    return f"Bash({SOUND_DOOR} --context {ctx['source']}:*)"


def door_rules(ctx: Dict) -> List[str]:
    """The doorways this pass may run outside the sandbox, each for this pass's own context; none for most."""
    return [image_rule(ctx)] * bool(ctx["toolbelt"]["image"]) + [sound_rule(ctx)] * bool(ctx["toolbelt"].get("sound"))


def claude_no_write(ctx: Dict) -> List[str]:
    """Everything in the folders a Claude pass sees that the fence does not let it write."""
    writes, frozen = ctx["fence"]["write"], ctx["fence"]["frozen"]
    out = list(frozen) + studio_reads()
    for root in (ctx["engagement"], ctx["media_project"]):
        allowed = [w for w in writes if under(w, root)]
        if not allowed:
            out.append(root)
            continue
        for child in sorted(Path(root).iterdir()):
            if not any(under(w, str(child)) for w in allowed):
                out.append(str(child))
    return out


def claude_settings(ctx: Dict) -> Dict:
    if ctx["vendor"] != "claude":
        die(f"{ctx['seat']} runs on Codex in this pass (its context); write its layer with codex-pass")
    reads, no_write = no_read(ctx), claude_no_write(ctx)

    def rule(tool: str, p: str) -> List[str]:
        return [f"{tool}(/{p})", f"{tool}(/{p}/**)"] if os.path.isdir(p) or not os.path.exists(p) else [f"{tool}(/{p})"]

    deny: List[str] = []
    for p in reads:
        deny += rule("Read", p)
    for p in no_write:
        deny += rule("Edit", p)
    deny += [f"Bash({c}:*)" for c in ("sudo", "git push", "brew", "pipx", "crontab", "launchctl load", "launchctl bootstrap",
                                       "launchctl enable", "gh", "npm publish", "security", *CLAUDE_DENIED_COMMANDS)]
    deny += ["WebFetch", "WebSearch", *CLAUDE_HELPER_TOOLS]
    # Reads outside the working folders need a rule, or headless Read, Glob and Grep are refused there.
    allow = [r for p in claude_reads(ctx) for r in rule("Read", p)]
    # A doorway (image or sound): the pass asks to run it outside the sandbox, and its rule is the only one that
    # lets a command out. Every other command asking the same needs an approval no one is there to give.
    door = bool(door_rules(ctx))
    if door:
        allow += door_rules(ctx)
    else:
        allow += [f"Bash({c}:*)" for c in CLAUDE_HELD_COMMANDS]
    return {
        "permissions": {"allow": allow, "deny": sorted(set(deny)), "defaultMode": "acceptEdits",
                        "disableBypassPermissionsMode": "disable"},
        "sandbox": {
            "enabled": True, "failIfUnavailable": True, "autoAllowBashIfSandboxed": True,
            "allowUnsandboxedCommands": door, "excludedCommands": [],
            "filesystem": {"denyRead": sorted(set(reads)), "allowWrite": list(ctx["fence"]["write"]),
                           "denyWrite": sorted(set(no_write))},
            "network": {"allowedDomains": list(ctx["hosts"]), "strictAllowlist": True},
        },
        "env": {"MOTIONCRAFT_CONTEXT": ctx["source"]},
        "disableAllHooks": True,
    }


def cmd_claude_settings(a) -> None:
    ctx = load(a.context)
    out = wall_file(ctx)
    write_once(out, json.dumps(claude_settings(ctx), indent=2) + "\n")
    print(out)


# --- a pass on Codex --------------------------------------------------------------------

def floor_profile(name: str, deny: List[str]) -> List[str]:
    lines = [f"[permissions.{name}]", 'extends = ":read-only"', f"[permissions.{name}.filesystem]"]
    lines += [f'{toml_str(p)} = "deny"' for p in deny]
    lines += [f'{toml_str(p)} = "read"' for p in SEAN_HOME_OPEN]
    lines += [f"[permissions.{name}.network]", "enabled = false", ""]
    return lines


def cmd_codex_home(a) -> None:
    home = Path(os.path.expanduser(a.home))
    if any(under(real(str(home)), real(h)) for h in SEAN_HOMES):
        die(f"{home} is inside Sean's own Codex home, which every pass is denied")
    home.mkdir(parents=True, exist_ok=True)
    os.chmod(home, 0o700)
    deny = list(CREDENTIAL_PATHS) + list(SEAN_HOMES) + employer_paths()
    lines = [
        "# Motioncraft's Codex seat home. Written by motioncraft/launcher/seat.py codex-home; rewrite it, never hand-edit.",
        "# A pass layers <eng>-pass-NN.config.toml on top with -p; with no layer a pass gets the read-only floor.",
        'default_permissions = "motioncraft-floor"', "",
        "[features]", *[f"{f} = false" for f in CODEX_FEATURES_OFF], "",
        "[skills]", "include_instructions = false", "",
        "[shell_environment_policy]", 'inherit = "all"', "ignore_default_excludes = false",
        'exclude = ["*TOKEN*", "*KEY*", "*SECRET*", "*PASSWORD*", "*CREDENTIAL*", "GH_*", "GITHUB_*", "MOTIONCRAFT_CONTEXT"]', "",
        *floor_profile("motioncraft-floor", deny),
    ]
    (home / "config.toml").write_text("\n".join(lines) + "\n")
    print(home)
    if not (home / "auth.json").exists():
        print(f"Next, Sean signs this home in once: CODEX_HOME={home} codex login")


def codex_profile(ctx: Dict) -> str:
    return f"{os.path.basename(ctx['engagement'])}-{pass_id_of(ctx['source'])}"


def codex_layer(ctx: Dict) -> List[str]:
    name = pass_id_of(ctx["source"])
    lines = [f"# Motioncraft pass layer for {ctx['source']}. Written by seat.py codex-pass; rewrite it, never hand-edit.",
             f'default_permissions = "{name}"', "",
             f"[projects.{toml_str(ctx['media_project'])}]", 'trust_level = "untrusted"', "",
             f"[permissions.{name}]", 'extends = ":read-only"', f"[permissions.{name}.filesystem]"]
    lines += [f'{toml_str(p)} = "deny"' for p in sorted(set(no_read(ctx)))]
    lines += [f'{toml_str(p)} = "read"' for p in SEAN_HOME_OPEN]
    lines += [f'{toml_str(ctx["engagement"])} = "read"']  # the coordinator's; -o files the final message
    lines += [f'{toml_str(p)} = "write"' for p in ctx["fence"]["write"]]
    lines += [f'{toml_str(p)} = "read"' for p in ctx["fence"]["frozen"]]
    lines += [f"[permissions.{name}.network]", "enabled = false", ""]
    return lines


def cmd_codex_pass(a) -> None:
    ctx = load(a.context)
    if ctx["vendor"] != "codex":
        die(f"{ctx['seat']} runs on Claude in this pass (its context); write its settings with claude-settings")
    home = Path(os.path.expanduser(a.home))
    profile = codex_profile(ctx)
    # Codex reads a profile only from $CODEX_HOME/<name>.config.toml, so the seat home
    # links to the one copy; the record hashes that copy, and launch checks the link.
    link = home / f"{profile}.config.toml"
    if link.exists() or link.is_symlink():
        die(f"{link} exists; a pass's wall is written once")
    out = wall_file(ctx)
    write_once(out, "\n".join(codex_layer(ctx)) + "\n")
    link.symlink_to(out)
    print(profile)


# --- launch -----------------------------------------------------------------------------

def files_final_message(ctx: Dict) -> bool:
    """The launcher files the final message of every Codex pass (-o) and of a read-only Claude pass."""
    return ctx["vendor"] == "codex" or ctx["read_only"]


def number(v: float) -> str:
    return str(int(v)) if float(v).is_integer() else str(v)


def launch_argv(ctx: Dict, prompt: str, profile: str = "", output: str = "") -> List[str]:
    caps = ctx["caps"]
    if ctx["vendor"] == "claude":
        # The seat's plugin is its toolbelt copy (bench/toolbelts.toml); a seat or gate with none loads no skill.
        plugin = ctx["toolbelt"]["dir"]
        # A read-only pass's Write reaches only its scratch folder: every other dir it sees is in its Edit denies.
        tools = "Read,Write,Bash,Glob,Grep,Skill" if ctx["read_only"] else "Read,Write,Edit,Bash,Glob,Grep,Skill"
        # stream-json: the live log the caps watch, and the per-message model stamps rung-0 line 11 reads
        argv = ["claude", "-p", "--output-format", "stream-json", "--verbose", "--model", CLAUDE_MODEL,
                "--permission-mode", "acceptEdits", "--setting-sources", "", "--settings", str(wall_file(ctx)),
                "--strict-mcp-config", "--tools", tools]
        if plugin:
            argv += ["--plugin-dir", plugin]
        agents = STUDIOS / "AGENTS.md"
        if agents.exists():
            argv += ["--append-system-prompt-file", str(agents)]
        for d in add_dirs(ctx):
            argv += ["--add-dir", d]
        if "budget_usd" in caps:
            argv += ["--max-budget-usd", number(caps["budget_usd"])]
        return argv + [claude_prompt(ctx, prompt)]
    return ["codex", "exec", "--json", "--model", CODEX_MODEL, "-c", f'model_reasoning_effort="{ctx["effort"]}"',
            "-p", profile, "--strict-config", "-c", 'web_search="disabled"', "--skip-git-repo-check",
            "-C", ctx["media_project"], "-o", output, codex_prompt(ctx, prompt)]


def claude_prompt(ctx: Dict, prompt: str) -> str:
    """A Claude pass's prompt: the coordinator's, its doorway (image for the Director and Art, sound for Finishing), the apps."""
    apps = [apps_note(ctx)] * bool(ctx["toolbelt"].get("apps"))
    doors = []
    if ctx["toolbelt"]["image"]:
        doors.append(f"The image path, for board roughs and style targets under the bench README's conditions: run "
                     f"`{IMAGE_DOOR} --context {ctx['source']} --out <your stage>/<version folder>/<name>.png "
                     "--prompt-file <a file you wrote> [--ref <an image in the media project>]...` with the Bash tool's "
                     "dangerouslyDisableSandbox set to true, alone, never chained. It files the image and its prompt "
                     "beside it, labelled generated.")
    if ctx["toolbelt"].get("sound"):
        doors.append(f"The sound path, for the cues on Sean's approved cue list and nothing else: run "
                     f"`{SOUND_DOOR} --context {ctx['source']} --cue <FXn or MUn> --out <your stage>/<version folder>/"
                     "<name>.mp3` with the Bash tool's dangerouslyDisableSandbox set to true, alone, never chained. It "
                     "sends the cue's approved prompt as it stands (a reworded cue goes back to Sean as a new list), makes "
                     "one take, and files it with its prompt beside it, labelled generated: up to three takes a cue, "
                     "inside the job's spend caps, and a refusal at a cap is a checkpoint for Sean. "
                     f"`{SOUND_DOOR} --context {ctx['source']} --status` lists the approved cues, the takes used and "
                     "the spend, and makes nothing.")
    if not doors:
        return "\n\n---\n\n".join([prompt] + apps)
    held = ("Those are the only commands that may run outside the sandbox. In this pass an ffmpeg or ffprobe argument "
            "shaped name=value is held for an approval no one gives: put a filter in a file and pass it with "
            "`-/vf <file>` or `-/af <file>` (a loudness check: a file holding `ebur128=peak=true`, then "
            "`ffmpeg -i <mix> -/af <file> -f null -`), and read stream facts with `-of json -show_streams`.")
    return "\n\n---\n\n".join([prompt, " ".join(doors + [held])] + apps)


def apps_note(ctx: Dict) -> str:
    """How a pass with an app reaches it: through the application doorway, never by running the app itself."""
    apps = ctx["toolbelt"].get("apps") or []
    usage = []
    if "blender" in apps:
        usage.append(f"`python3 -B {APPS_DOOR} ask blender --script <a .py you wrote> [--blend <a .blend in the media "
                     "project>] [-- <the script's arguments>]` runs `Blender -b --factory-startup --python <your script>`; "
                     "Cycles renders on the CPU or the graphics chip (Metal), but only the CPU repeats a frame exactly, so a render "
                     "kept in a version folder uses the CPU and the graphics chip is for previews in your scratch folder. "
                     "A scene holding Grease Pencil, and any Eevee or Workbench render, aborts under your own script, so "
                     f"save the scene and ask `python3 -B {APPS_DOOR} ask blender --render --blend <the saved .blend> --out "
                     "<a folder> --frames S-E [--engine cycles|eevee|workbench]`, which renders it with the launcher's own "
                     "script (Cycles on the CPU; scripts inside the file never run); a kept render is cycles into a new "
                     "version folder in your stage, and eevee or workbench render only into your scratch folder, as previews")
        if ctx["seat"] == "visual-story-director":
            usage.append("your animatic is a sequencer edit in a .blend of your own in your stage: the boards as image "
                         "strips, the scratch timing track as a sound strip whose tones and silence your script writes with "
                         "Blender's own sound module (`aud`), and the file's output set to a movie with sound (FFmpeg, H.264 "
                         "with AAC) before it is saved; it renders through the render request like any scene, cycles into a "
                         "new version folder, as one movie file")
    if "resolve" in apps:
        usage.append(f"`python3 -B {APPS_DOOR} ask resolve --script <a .py you wrote> [-- <the script's arguments>]` "
                     "runs your script with `DaVinciResolveScript` importable, connected to the Resolve already open on "
                     "this machine; render and export only into a version folder in your stage")
    if "krita" in apps:
        usage.append(f"`python3 -B {APPS_DOOR} ask krita --script <a .py you wrote> [-- <the script's arguments>]` "
                     "runs your script inside Krita with no screen (`from krita import Krita, InfoObject`; your arguments "
                     "are `sys.argv[1:]`). Krita's brush engine is not available: `Node.paintLine`, the other `paint...` "
                     "calls and `paintAbility`, and anything that opens a window or view (`openWindow`, `addView`, "
                     "`activeWindow`), crash Krita with no screen. Draw strokes with Qt's painter (`PyQt5.QtGui.QPainter` "
                     "on a `QImage` in `Format_ARGB32`, its bytes being Krita's RGBA 8-bit layer bytes) and put them on a "
                     "layer with `Node.setPixelData`. Krita gives the layers, their order, blend modes and opacity, its "
                     "filters (`Krita.filter`), the `.kra` file (`Document.saveAs`) and each layer as a PNG with "
                     "transparency (`Node.save`, which returns nothing, so check the file, and which bakes the layer's opacity "
                     "into the PNG's alpha: export at opacity 255 and restore it, so the stated opacity is applied once "
                     "downstream); `Document.exportImage` stalls with no screen, so a flattened image is "
                     "`Document.pixelData` read into a `QImage` (`Format_ARGB32`, then `.copy()`) and saved with "
                     "`QImage.save`; save only into a new version folder in your stage. A call succeeds only "
                     "if your script runs to its end; exit non-zero (`sys.exit(1)`) when it fails")
    names = " and ".join(", ".join(n.capitalize() for n in apps).rsplit(", ", 1))
    return (f"{names}: none runs inside this pass's sandbox, so never run one yourself. "
            "Ask the launcher, from your shell: " + "; ".join(usage) + ". Write the script in your scratch "
            "folder or a new version folder in your stage. The launcher runs a copy under a lock as tight as your own "
            "fence and prints the end of the application's log and a result: what it wrote in your fence, and, for "
            "Resolve, every path written elsewhere on the Mac during the call, which goes in your check record. If it "
            "says still running, run `python3 -B " + str(APPS_DOOR) + " wait <id>`. The call counts against this "
            "pass's time.")


def codex_prompt(ctx: Dict, prompt: str) -> str:
    """A Codex pass's prompt: the studios AGENTS.md and the toolbelt's skills by path, then the coordinator's.

    Codex runs from the media project, where no AGENTS.md is found, and its seat home
    lists no skill (`[skills] include_instructions = false`), so both go in here: the
    same rules a Claude pass gets by flag, and the skills its plugin would carry.
    """
    parts = []
    agents = STUDIOS / "AGENTS.md"
    if agents.exists():
        parts.append(f"The studios AGENTS.md, which binds this pass:\n\n{agents.read_text(encoding='utf-8').strip()}")
    skills = ctx["toolbelt"]["skills"]
    if skills:
        lines = "\n".join(f"- `{s['skill']}`: {s['path']}" for s in skills)
        parts.append("Your toolbelt's skills. Read a skill's SKILL.md by its path when its moment comes; "
                     f"no other skill is yours.\n\n{lines}")
    return "\n\n---\n\n".join(parts + [apps_note(ctx)] * bool(ctx["toolbelt"].get("apps")) + [prompt])


def scrubbed_env(ctx: Dict, home: Path) -> Dict[str, str]:
    env = {k: os.environ[k] for k in KEEP_ENV if k in os.environ}
    env["MOTIONCRAFT_CONTEXT"] = ctx["source"]
    env["MOTIONCRAFT_SEAT"] = ctx["seat"]
    # The applications' own folders and variables (the allowlist's [env]); the pass's PATH starts from the launcher's.
    path, apps = app_env()
    env.update(apps)
    env["PATH"] = ":".join([env.get("PATH", "")] + path).strip(":")
    # mktemp and Python's tempfile land in the one folder every pass may write
    env["TMPDIR"] = env["MOTIONCRAFT_SCRATCH"] = ctx["scratch"]
    if ctx["vendor"] == "codex":
        env["CODEX_HOME"] = str(home)
    return env


def output_path(ctx: Dict, output: str) -> str:
    """The record the launcher files the final message into: in artifacts/ or audits/, written once."""
    if not output:
        if files_final_message(ctx):
            die("the launcher files this pass's final message; name its record with --output (artifacts/… or audits/…)")
        return ""
    if not files_final_message(ctx):
        die(f"{ctx['seat']} writes its own artifact; --output is for a Codex pass or a read-only Claude pass")
    eng = ctx["engagement"]
    p = Path(real(output if os.path.isabs(output) else os.path.join(eng, output)))
    rel = os.path.relpath(p, eng)
    if rel.startswith("..") or rel.split(os.sep)[0] not in ("artifacts", "audits") or rel.count(os.sep) < 1:
        die(f"--output must sit in the engagement's artifacts/ or audits/, not {rel}")
    if p.exists():
        die(f"{rel} exists; an output is written once")
    p.parent.mkdir(parents=True, exist_ok=True)
    return str(p)


class Watch:
    """Reads the live log line by line: the tool calls so far, any helper agent, and what the meter needs."""

    def __init__(self, vendor: str):
        self.vendor = vendor
        self.tool_ids: set = set()
        self.helpers: List[str] = []
        self.stamps: set = set()
        self.thread: Optional[str] = None
        self.usage: Dict[str, int] = {}
        self.result: Optional[Dict] = None

    @property
    def calls(self) -> int:
        return len(self.tool_ids)

    def feed(self, line: str) -> None:
        try:
            e = json.loads(line)
        except ValueError:
            return
        if not isinstance(e, dict):
            return
        t = e.get("type")
        if self.vendor == "codex":
            item = e.get("item")
            if t == "thread.started":
                self.thread = e.get("thread_id")
            elif t in ("item.started", "item.completed") and isinstance(item, dict) and item.get("type") in CODEX_TOOL_ITEMS:
                self.tool_ids.add(item.get("id") or f"anon-{len(self.tool_ids)}")
            elif t == "turn.completed" and isinstance(e.get("usage"), dict):
                for k, v in e["usage"].items():
                    if isinstance(v, int):
                        self.usage[k] = self.usage.get(k, 0) + v
            return
        # A helper speaks in assistant or user messages under its parent's tool use. A long Bash call's own progress
        # lines carry the same field (`tool_progress`, a sound doorway take, live 2026-10-19), and are no helper.
        if e.get("parent_tool_use_id") and t in ("assistant", "user"):
            self.helpers.append(f"a helper agent's message (parent tool use {e['parent_tool_use_id']})")
        if t == "assistant":
            msg = e.get("message") or {}
            if msg.get("model"):
                self.stamps.add(msg["model"])
            for block in msg.get("content") or []:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    self.tool_ids.add(block.get("id") or f"anon-{len(self.tool_ids)}")
                    if block.get("name") in CLAUDE_HELPER_TOOLS:
                        self.helpers.append(f"a {block['name']} tool call ({block.get('id', '?')})")
        elif t == "result":
            self.result = e


def kill_group(proc: subprocess.Popen) -> None:
    for sig, grace in ((signal.SIGTERM, KILL_GRACE_S), (signal.SIGKILL, 5)):
        try:
            os.killpg(proc.pid, sig)
        except ProcessLookupError:
            return
        try:
            proc.wait(timeout=grace)
            return
        except subprocess.TimeoutExpired:
            continue


def supervise(argv: List[str], env: Dict[str, str], cwd: str, log: Path, err: Path,
              caps: Dict[str, float], vendor: str) -> Dict:
    """Run one pass under its caps; kill its whole process group at 100% of any of them.

    macOS has no `timeout` and Codex has no budget, turn or time flag, so this is
    the only hard stop. What the pass wrote stays on disk for the coordinator to
    file as Blocked: budget.
    """
    watch = Watch(vendor)
    trip = threading.Event()
    limit_calls = caps.get("tool_calls")
    limit_s = caps["minutes"] * 60 if "minutes" in caps else None
    launched, start = now(), time.monotonic()
    with open(log, "x", encoding="utf-8") as logf, open(err, "xb") as errf:
        proc = subprocess.Popen(argv, cwd=cwd, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                stderr=errf, start_new_session=True)

        def pump() -> None:
            for raw in proc.stdout:
                line = raw.decode("utf-8", "replace")
                logf.write(line)
                logf.flush()
                watch.feed(line)
                if limit_calls is not None and watch.calls >= limit_calls:
                    trip.set()

        reader = threading.Thread(target=pump, daemon=True)
        reader.start()
        stopped = None
        while proc.poll() is None:
            if trip.wait(0.2):
                stopped = "tool-calls"
            elif limit_s is not None and time.monotonic() - start >= limit_s:
                stopped = "wall-clock"
            if stopped:
                kill_group(proc)
                break
        proc.wait()
        reader.join(timeout=10)
    if stopped is None and watch.result and "budget" in str(watch.result.get("subtype", "")):
        stopped = "budget-usd"  # Claude stopped itself at --max-budget-usd
    return {"launched": launched, "completed": now(), "wall_clock_s": round(time.monotonic() - start),
            "exit_code": proc.returncode, "tool_calls": watch.calls, "stopped": stopped, "watch": watch}


def codex_helpers(home: Path, log: Path, thread: Optional[str], rollouts: Path) -> Dict:
    """Save the pass's session files beside its JSONL and look for a helper agent, as rung-0 line 11 does."""
    found = [f"its raw log shows {t}" for t in codexlog.jsonl_helpers(log.read_text(encoding="utf-8"))]
    files = codexlog.collect(home, thread, rollouts) if thread else []
    sessions = codexlog.read_sessions(rollouts) if files else []
    own = [s for s in sessions if not s.helper and not s.error]
    for s in sessions:
        if s.helper:
            found.append(f"helper session {s.path}")
        if s.spawn_calls:
            found.append(f"{s.spawn_calls} spawn call(s) in {s.path}")
        if s.helper_events and not s.spawn_calls:
            found.append(f"{s.helper_events} helper event(s) in {s.path}")
    stamps = sorted({f"{m} {e}".strip() for s in own for m, e in s.stamps})
    return {"session_files": len(files), "stamps": stamps, "helper": found}


def claude_dirs(roots: List[str]) -> List[str]:
    """Every `.claude` anywhere inside these folders, found without following a link or looking inside one."""
    found = []
    for root in roots:
        for here, dirs, _ in os.walk(root):
            if ".claude" in dirs:
                found.append(os.path.join(here, ".claude"))
                dirs.remove(".claude")
    return sorted(set(found))


def only_leftovers(d: str) -> bool:
    """Nothing in `d` but empty folders and Claude Code's own `.cc-writes`: nothing a seat meant to save."""
    own = os.path.join(d, ".cc-writes")
    for here, dirs, files in os.walk(d):
        if any(os.path.islink(os.path.join(here, n)) for n in dirs + files):
            return False
        if files and here != own and not here.startswith(own + os.sep):
            return False
    return True


def sweep_claude_dirs(roots: List[str], before: List[str]) -> Dict[str, List[str]]:
    """Claude Code leaves a `.claude/` in its working folders, and in any folder a pass cd's into, the
    pass's own new version folders included, where it would change a frozen version's checksums.
    Each found in the fence after the pass that was not there before it is removed if it holds only
    leftovers, and named as left if it holds anything else.
    """
    out: Dict[str, List[str]] = {"removed": [], "left": []}
    for d in claude_dirs(roots):
        if d in before:
            continue
        if not os.path.islink(d) and only_leftovers(d):
            try:
                shutil.rmtree(d)
                out["removed"].append(d)
                continue
            except OSError:
                pass
        out["left"].append(d)
    return out


def cmd_launch(a) -> None:
    ctx = load(a.context)
    home = Path(os.path.expanduser(a.home))
    vendor, eng = ctx["vendor"], Path(ctx["engagement"])
    if ctx.get("machine") != machine():
        die(f"this context was written on {ctx.get('machine')}, not {machine()}; one machine per job, "
            "so a moved job writes a new context on the machine it moved to")
    wall = wall_file(ctx)
    if not wall.exists():
        die(f"no wall file {wall}; run seat.py {'claude-settings' if vendor == 'claude' else 'codex-pass'} first")
    profile = ""
    if vendor == "codex":
        profile = codex_profile(ctx)
        link = home / f"{profile}.config.toml"
        if not link.is_symlink() or link.resolve() != wall.resolve():
            die(f"{link} does not link to {wall}; run seat.py codex-pass")
    belt = ctx["toolbelt"]
    if belt["dir"]:
        man = Path(belt["dir"]) / "manifest.json"
        if not man.is_file() or sha256(man) != belt["manifest_sha256"]:
            die(f"{ctx['seat']}'s toolbelt copy changed since the context named it; a changed toolbelt is a new pass")
    for named in (ctx.get("escalation"), ctx.get("vendor_basis")):
        if named and named.get("path"):
            rec = eng / named["path"]
            if not rec.is_file() or sha256(rec) != named["sha256"]:
                die(f"{named['path']} changed since the context named it; a changed record is a new pass")
    output = output_path(ctx, a.output)
    argv = launch_argv(ctx, Path(a.prompt_file).read_text(), profile, output)
    env = scrubbed_env(ctx, home)
    shown = argv[:-1] + ["<prompt>"]
    print(json.dumps({"argv": shown, "env": sorted(env), "caps": ctx["caps"], "fence": ctx["fence"]}, indent=1), file=sys.stderr)
    if not a.run:
        return
    pid = pass_id_of(ctx["source"])
    logs = eng / "trace" / "logs"
    log, err, rec = logs / f"{pid}.jsonl", logs / f"{pid}.stderr.log", logs / f"{pid}.launch.json"
    for p in (log, err, rec):
        if p.exists():
            die(f"{p} exists; a pass is launched once, so a re-run is a new pass")
    wall_sha = sha256(wall)  # taken at launch: the wall this pass actually ran under
    Path(ctx["scratch"]).mkdir(parents=True, exist_ok=True)
    cwd = ctx["scratch"] if vendor == "claude" else ctx["media_project"]
    swept_roots = list(dict.fromkeys(ctx["fence"]["write"] + [cwd]))
    before = claude_dirs(swept_roots) if vendor == "claude" else []
    server = None
    if ctx["toolbelt"].get("apps"):
        # The application doorway runs on this side of the sandbox for as long as the pass does, no longer.
        import apps as appdoor  # noqa: E402  launcher/apps.py, beside this file
        server = appdoor.AppServer(ctx, time.time() + ctx["caps"].get("minutes", 60) * 60)
        env.update(server.env())
        server.start()
    try:
        run = supervise(argv, env, cwd, log, err, ctx["caps"], vendor)
    finally:
        door = server.stop() if server else None
    watch: Watch = run.pop("watch")
    rel = lambda p: os.path.relpath(p, eng)  # noqa: E731
    record = {
        "pass": pid, "seat": ctx["seat"], "vendor": vendor, "vendor_basis": ctx["vendor_basis"],
        "model": CLAUDE_MODEL if vendor == "claude" else CODEX_MODEL, "effort": ctx["effort"],
        "escalation": ctx["escalation"], "machine": machine(), "media": ctx["media"],
        "argv": shown, "caps": ctx["caps"], "fence": ctx["fence"], "toolbelt": ctx["toolbelt"], **run,
        "wall_files": [{"path": str(wall), "sha256": wall_sha}],
        "raw_log": rel(log), "stderr_log": rel(err), "scratch": ctx["scratch"],
    }
    if door is not None:
        record["apps"] = door
    helpers: List[str] = []
    if vendor == "claude":
        res = watch.result or {}
        record["usage"], record["meter_source"] = res.get("usage"), ("claude -p result.usage" if res.get("usage") else "UNMEASURED")
        record["runtime_stamps"] = sorted(watch.stamps)
        helpers = watch.helpers
        if output and res.get("subtype") == "success" and isinstance(res.get("result"), str):
            Path(output).write_text(res["result"] + "\n")
        swept = sweep_claude_dirs(swept_roots, before)
        if swept["removed"] or swept["left"]:
            record["claude_dirs"] = swept
    else:
        record["usage"] = watch.usage or None
        record["meter_source"] = "codex turn.completed.usage" if watch.usage else "UNMEASURED"
        rollouts = logs / f"{pid}.rollouts"
        seen = codex_helpers(home, log, watch.thread, rollouts)
        record["rollouts"], record["runtime_stamps"] = {"path": rel(rollouts), "files": seen["session_files"]}, seen["stamps"]
        helpers = seen["helper"]
    code = 0
    if helpers:
        record["helper_agent"] = helpers
        if output and Path(output).exists():
            moved = logs / f"{pid}.discarded{Path(output).suffix}"
            os.replace(output, moved)
            record["discarded_output"] = rel(moved)
        record["outcome"] = "helper agent: output discarded; re-run once as a new pass, a second spawn stops Blocked"
        code = 3
    if output and Path(output).exists():
        record["outputs"] = [{"path": rel(output), "sha256": sha256(Path(output))}]
    # Filing (launcher/filing.py, SWCB #245): the images and sound the pass opened are stripped from its logs, and
    # the employer folders replaced by a placeholder, before anything can be committed; the launcher refuses to
    # finish if either survives.
    import filing  # noqa: E402  launcher/filing.py, beside this file
    media_root, employer = filing.setting()
    filed = filing.file_logs(logs, [pid], media_root, employer)
    record["filing"] = {"media_stripped": filed["media_stripped"], "rewritten": len(filed["rewritten"]),
                        "employer_paths_checked": bool(employer), "survivors": filed["survivors"],
                        "not_read": filed["not_read"]}
    if run["stopped"]:
        record["outcome"] = f"Blocked: budget ({run['stopped']} cap reached)"
        code = 2
    elif run["exit_code"] != 0 and not code:
        record["outcome"] = f"the vendor exited {run['exit_code']}; see {rel(err)}"
        code = 1
    if filed["survivors"] or filed["not_read"]:
        refused = ("filing refused: media or an employer path survives in " + ", ".join(
            sorted(filed["survivors"]) + filed["not_read"]) + "; nothing from this pass may be committed")
        record["outcome"] = f"{record['outcome']}; {refused}" if record.get("outcome") else refused
        code = 4
    rec.write_text(filing.redact(json.dumps(record, indent=2), filing.employer_forms(employer)) + "\n")
    print(f"{pid}: {record.get('outcome', 'returned')}; {run['tool_calls']} tool call(s), {run['wall_clock_s']}s → {rel(rec)}")
    sys.exit(code)


# --- the model check at Route -----------------------------------------------------------

PROBE_PROMPT = "Reply with your exact model id and nothing else."
CLAUDE_STAMP = re.compile(r'"model"\s*:\s*"(claude-[A-Za-z0-9.\-]+)"')  # the trace checker's own stamp


def one_line(s: str, n: int = 80) -> str:
    s = " ".join((s or "").split())
    return s if len(s) <= n else s[: n - 1] + "…"


def run_probe(argv: List[str], cwd: str, env: Dict[str, str], log: Optional[Path]) -> subprocess.CompletedProcess:
    # stdin closed: `codex exec` otherwise waits for piped input to append to the prompt
    try:
        r = subprocess.run(argv, cwd=cwd, env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
        r = subprocess.CompletedProcess(argv, 124, out, "no answer in 300 s")
    if log is not None:
        log.write_text(r.stdout)
    return r


def probe_claude(env: Dict[str, str], cwd: str, log: Optional[Path]) -> Dict:
    argv = ["claude", "-p", "--output-format", "stream-json", "--verbose", "--model", CLAUDE_MODEL,
            "--setting-sources", "", "--strict-mcp-config", "--tools", "", "--max-budget-usd", "1", PROBE_PROMPT]
    r = run_probe(argv, cwd, env, log)
    answer = ""
    for line in r.stdout.splitlines():
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if isinstance(e, dict) and e.get("type") == "result":
            answer = str(e.get("result") or "")
    stamps = sorted(set(CLAUDE_STAMP.findall(r.stdout)))
    return {"id": CLAUDE_MODEL, "on": "claude -p", "answer": answer, "stamps": stamps, "exit": r.returncode,
            "match": stamps == [CLAUDE_MODEL], "error": one_line(r.stderr) if r.returncode else ""}


def probe_codex(home: Path, env: Dict[str, str], cwd: str, log: Optional[Path]) -> Dict:
    argv = ["codex", "exec", "--json", "--model", CODEX_MODEL, "-c", f'model_reasoning_effort="{CODEX_EFFORT}"',
            "--strict-config", "-c", 'web_search="disabled"', "--skip-git-repo-check", "-C", cwd, PROBE_PROMPT]
    r = run_probe(argv, cwd, dict(env, CODEX_HOME=str(home)), log)
    answer = ""
    for line in r.stdout.splitlines():
        try:
            e = json.loads(line)
        except ValueError:
            continue
        item = e.get("item") if isinstance(e, dict) else None
        if isinstance(e, dict) and e.get("type") == "item.completed" and isinstance(item, dict) and item.get("type") == "agent_message":
            answer = str(item.get("text") or "")
    thread = codexlog.jsonl_thread(r.stdout)
    sessions = [codexlog.read_session(f.read_text(encoding="utf-8"), f.name)
                for f in (codexlog.find_sessions(home, thread) if thread else [])]
    stamps = sorted({f"{m} {e}" for s in sessions if not s.helper for m, e in s.stamps})
    return {"id": CODEX_MODEL, "on": "codex exec", "effort": CODEX_EFFORT, "answer": answer, "stamps": stamps,
            "exit": r.returncode, "match": stamps == [f"{CODEX_MODEL} {CODEX_EFFORT}"],
            "error": one_line(r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "") if r.returncode else ""}


def route_entry(results: List[Dict], when: str) -> str:
    lines = [f"**The model check** (`motioncraft/launcher/seat.py probe`, {when}, on {machine()}; outside the budget). "
             "Each pinned id was asked for its own id; the match is read from the log's model stamp, never the answer."]
    for r in results:
        what = f"`{r['id']}`" + (f" ({r['effort']})" if r.get("effort") else "") + f" on `{r['on']}`"
        stamp = ", ".join(r["stamps"]) or "none"
        verdict = "Match." if r["match"] else "**MISMATCH**: to Sean before any seat runs."
        tail = f" Exit {r['exit']}: {r['error']}" if r["exit"] else ""
        lines.append(f"- {what}: answered \"{one_line(r['answer'])}\"; stamped {stamp}. {verdict}{tail}")
    return "\n".join(lines)


def cmd_probe(a) -> None:
    home = Path(os.path.expanduser(a.home))
    env = {k: os.environ[k] for k in KEEP_ENV if k in os.environ}
    logs = Path(a.logs) if a.logs else None
    if logs is not None:
        logs.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="motioncraft-probe-") as cwd:
        results = [probe_claude(env, cwd, logs / "probe-claude.jsonl" if logs else None),
                   probe_codex(home, env, cwd, logs / "probe-codex.jsonl" if logs else None)]
    print(route_entry(results, now()))
    sys.exit(0 if all(r["match"] for r in results) else 1)


# --- the toolbelt probe: each seat loads only its toolbelt ------------------------------

# A file every pass is denied, read once to show the skill folders' wall holds live.
OUTSIDE_SKILL = HOME / ".agents" / "skills" / "animation-vocabulary" / "SKILL.md"
SEAT_PROBE_PROMPT = (
    "This is a launch-form probe: change no file, and answer in exactly three lines. "
    "Line 1: the names of every tool you can call, comma-separated. "
    "Line 2: for each skill you were given as your toolbelt (named in your prompt, or a skill you can load), read its "
    "SKILL.md and print the value of its `name:` line, comma-separated; print `none` if you were given none. "
    f"Line 3: try once to print the first line of {OUTSIDE_SKILL} with a shell command, and print READ if it worked "
    "or BLOCKED if it did not.")


def redact(text: str) -> str:
    """Probe evidence goes to the ledger: the machine's employer folders never do."""
    for p in employer_paths():
        text = text.replace(p, "<employer folder>")
    return text


def claude_builtins(env: Dict[str, str]) -> Dict:
    """Claude Code's own skills and plugins, from a bare run with nothing of the studio's or Sean's loaded.

    They stay listed under every form (Devcraft's isolation finding), and some share
    a name with one of Sean's skills, so a seat's skills are judged against this
    baseline, not by name. Haiku, since the list does not depend on the model.
    """
    with tempfile.TemporaryDirectory(prefix="motioncraft-baseline-") as cwd:
        r = run_probe(["claude", "-p", "--output-format", "stream-json", "--verbose", "--model", "claude-haiku-4-5",
                       "--setting-sources", "", "--strict-mcp-config", "--tools", "", "--max-budget-usd", "0.05",
                       "Reply ok."], cwd, env, None)
    init = next((e for e in stream_events(r.stdout) if e.get("type") == "system" and e.get("subtype") == "init"), {})
    if not init:
        die("the built-in baseline run wrote no init line; the probe cannot tell built-in skills from loaded ones")
    return {"skills": sorted(init.get("skills", [])),
            "plugins": sorted(p.get("name", "") for p in init.get("plugins", [])),
            "claude_code_version": init.get("claude_code_version")}


def never_names() -> List[str]:
    return [n.lower() for n in toolbelts().get("never", {}).get("names", [])]


def probe_job(seat: str) -> Dict:
    """A throwaway engagement and media project for one probe pass, and the context the launcher would write."""
    base = Path(real(os.path.expanduser("~/.cache/motioncraft/probe"))) / f"{seat}-{datetime.now():%Y%m%d-%H%M%S}"
    # The engagement folder's name keys its wall files and Codex profile, so each probe's is its own.
    eng, project = base / f"probe-{base.name}", base / "media" / "probe-2026-10-19"
    for d in ("artifacts", "audits", "trace/logs"):
        (eng / d).mkdir(parents=True)
    project.mkdir(parents=True)
    vendor, read_only = default_vendor(seat), seat in GATES
    scratch = real(str(SCRATCH_ROOT / f"probe-{base.name}" / "pass-00"))
    make_scratch(scratch)
    ctx = {"seat": seat, "engagement": str(eng), "pass": "00", "machine": machine(), "media": "probe",
           "media_project": str(project), "read_only": read_only, "vendor": vendor, "vendor_basis": {"by": "probe"},
           "caps": {"minutes": 10, **({"budget_usd": 1} if vendor == "claude" else {"tool_calls": 20})},
           "effort": CODEX_EFFORT if vendor == "codex" else "", "escalation": None, "hosts": [], "scratch": scratch,
           "fence": fence(seat, str(eng), str(project), read_only, vendor, scratch),
           "toolbelt": context_belt(seat, vendor, read_only)}
    src = eng / "trace" / "logs" / "pass-00.context.json"
    src.write_text(json.dumps(ctx, indent=2) + "\n")
    ctx["source"] = str(src)
    return {"base": base, "ctx": ctx}


def answer_lines(text: str) -> List[str]:
    return [l.strip() for l in (text or "").strip().splitlines() if l.strip()][:3]


def judge_claude(init: Dict, argv: List[str], seat: str, builtins: Dict) -> List[str]:
    """What a Claude seat's first log line says it loaded, against its allowlist; one line per problem."""
    bad = []
    want_tools = sorted(argv[argv.index("--tools") + 1].split(","))
    if sorted(init.get("tools", [])) != want_tools:
        bad.append(f"tools {sorted(init.get('tools', []))}, not {want_tools}")
    if init.get("mcp_servers"):
        bad.append(f"connectors loaded: {[m.get('name') for m in init['mcp_servers']]}")
    want = sorted(n for _, n in seat_belt(seat)["skills"])
    plugins = sorted(p.get("name", "") for p in init.get("plugins", [])
                     if p.get("path") != "builtin" or p.get("name") not in builtins["plugins"])
    if plugins != ([plugin_name(seat)] if want else []):
        bad.append(f"plugins {plugins}")
    mine = f"{plugin_name(seat)}:"
    skills = init.get("skills", [])
    if sorted(s[len(mine):] for s in skills if s.startswith(mine)) != want:
        bad.append(f"its toolbelt skills are {sorted(s for s in skills if s.startswith(mine))}, not {want}")
    bad += [f"another plugin's skill loaded: {s}" for s in skills if ":" in s and not s.startswith(mine)]
    bad += [f"a skill outside Claude Code's built-ins loaded: {s}" for s in skills
            if ":" not in s and s not in builtins["skills"]]
    names = init.get("tools", []) + skills + plugins + [m.get("name", "") for m in init.get("mcp_servers", [])]
    bad += [f"a never-name loaded: {n}" for n in names for v in never_names() if v in n.lower()]
    if init.get("model") != CLAUDE_MODEL:
        bad.append(f"model {init.get('model')}")
    return bad


def judge_codex(state: Dict, rendered: str, answer: str, configs: str = "") -> List[str]:
    """What a Codex pass's session file, rendered prompt and config files say was offered; one line per problem.

    Codex's three built-in readers for connector resources (`list_mcp_resources` and
    its kin) stay in every session and reach nothing when no connector is configured,
    so connectors are judged from the seat home's config and the pass layer.
    """
    bad = []
    if re.search(r"^\s*\[mcp_servers", configs, re.M):
        bad.append("a connector is configured in the seat home or the pass layer")
    for key, want in (("skills", {"includeInstructions": False}), ("host_skills", {"includeInstructions": False}),
                      ("plugins_instructions", False), ("apps_instructions", False), ("agents_md", {})):
        if state.get(key, want) != want:
            bad.append(f"session state {key} = {state.get(key)!r}, not {want!r}")
    for marker in ("Skill roots", "<skills_instructions>", "<apps_instructions>", "<plugins_instructions>"):
        if marker in rendered:
            bad.append(f"the rendered prompt carries {marker}")
    lines = answer_lines(answer)
    tools = lines[0].lower() if lines else ""
    bad += [f"it names a tool it should not have: {t}" for t in ("image_gen", "imagegen", "web_search") if t in tools]
    bad += [f"a never-name in its tools: {v}" for v in never_names() if v in tools]
    return bad


def codex_state(home: Path, thread: Optional[str]) -> Dict:
    for f in (codexlog.find_sessions(home, thread) if thread else []):
        for line in f.read_text(encoding="utf-8").splitlines():
            try:
                e = json.loads(line)
            except ValueError:
                continue
            if e.get("type") == "world_state":
                return e.get("payload", {}).get("state", {})
    return {}


def stream_events(text: str) -> List[Dict]:
    out = []
    for line in text.splitlines():
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if isinstance(e, dict):
            out.append(e)
    return out


def probe_seat(seat: str, home: Path, logs: Optional[Path], builtins: Optional[Dict]) -> Dict:
    """One probe pass on the seat's own vendor and launch form: what loaded, judged against its allowlist."""
    job = probe_job(seat)
    ctx = job["ctx"]
    env = scrubbed_env(ctx, home)
    belt = [s["skill"] for s in ctx["toolbelt"]["skills"]]
    res = {"seat": seat, "vendor": ctx["vendor"], "toolbelt": belt, "image": ctx["toolbelt"]["image"],
           "sound": ctx["toolbelt"].get("sound", False)}
    if ctx["vendor"] == "claude":
        settings = claude_settings(ctx)
        write_once(wall_file(ctx), json.dumps(settings, indent=2) + "\n")
        argv = launch_argv(ctx, SEAT_PROBE_PROMPT)
        r = run_probe(argv, ctx["scratch"], env, None)
        events = stream_events(r.stdout)
        init = next((e for e in events if e.get("type") == "system" and e.get("subtype") == "init"), {})
        answer = next((str(e.get("result") or "") for e in events if e.get("type") == "result"), "")
        res.update(tools=init.get("tools"), skills=init.get("skills"), mcp=init.get("mcp_servers"),
                   plugins=[p.get("name") for p in init.get("plugins", [])],
                   stamps=sorted(set(CLAUDE_STAMP.findall(r.stdout))),
                   image_rule=image_rule(ctx) in settings["permissions"]["allow"],
                   sound_rule=sound_rule(ctx) in settings["permissions"]["allow"],
                   unsandboxed_allowed=settings["sandbox"]["allowUnsandboxedCommands"],
                   problems=judge_claude(init, argv, seat, builtins) if init else ["no init line in the log"])
    else:
        write_once(wall_file(ctx), "\n".join(codex_layer(ctx)) + "\n")
        link = home / f"{codex_profile(ctx)}.config.toml"
        link.symlink_to(wall_file(ctx))
        try:
            argv = launch_argv(ctx, SEAT_PROBE_PROMPT, codex_profile(ctx), str(job["base"] / "answer.md"))
            r = run_probe(argv, ctx["media_project"], env, None)
            rendered = subprocess.run(["codex", "debug", "prompt-input"], cwd=ctx["media_project"], env=env,
                                      stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=120).stdout
        finally:
            link.unlink()
        events = stream_events(r.stdout)
        answer = next((str(e["item"].get("text") or "") for e in reversed(events) if e.get("type") == "item.completed"
                       and isinstance(e.get("item"), dict) and e["item"].get("type") == "agent_message"), "")
        thread = codexlog.jsonl_thread(r.stdout)
        state = codex_state(home, thread)
        sessions = [codexlog.read_session(f.read_text(encoding="utf-8"), f.name)
                    for f in (codexlog.find_sessions(home, thread) if thread else [])]
        res.update(stamps=sorted({f"{m} {e}" for s in sessions if not s.helper for m, e in s.stamps}),
                   helper_sessions=[s.path for s in sessions if s.helper],
                   session_state={k: state.get(k) for k in ("skills", "host_skills", "plugins_instructions",
                                                            "apps_instructions", "agents_md", "multi_agent_mode")},
                   toolbelt_in_prompt=all(s["path"] in argv[-1] for s in ctx["toolbelt"]["skills"]),
                   agents_md_in_prompt="The studios AGENTS.md" in argv[-1],
                   problems=judge_codex(state, rendered, answer,
                                        (home / "config.toml").read_text() + wall_file(ctx).read_text())
                   if state else ["no session file for the pass"])
    lines = answer_lines(answer)
    res.update(answer=lines, exit=r.returncode)
    if len(lines) < 3 or "BLOCKED" not in lines[2].upper():
        res["problems"].append(f"the skill folders' wall: line 3 reads {lines[2] if len(lines) > 2 else 'nothing'!r}")
    named = {n.strip().strip("`").lower() for n in lines[1].split(",")} if len(lines) > 1 else set()
    if belt and not set(belt) <= named:
        res["problems"].append(f"it could not read its own toolbelt: line 2 reads {lines[1] if len(lines) > 1 else 'nothing'!r}")
    want_stamp = [CLAUDE_MODEL] if ctx["vendor"] == "claude" else [f"{CODEX_MODEL} {CODEX_EFFORT}"]
    if res["stamps"] != want_stamp:
        res["problems"].append(f"stamped {res['stamps']}, not {want_stamp}")
    if logs is not None:
        logs.mkdir(parents=True, exist_ok=True)
        (logs / f"probe-{seat}.jsonl").write_text(redact(r.stdout))
    shutil.rmtree(job["base"], ignore_errors=True)
    shutil.rmtree(Path(ctx["scratch"]).parent, ignore_errors=True)
    return res


def cmd_seat_probe(a) -> None:
    home = Path(os.path.expanduser(a.home))
    logs = Path(a.logs) if a.logs else None
    seats = a.seat or list(SEATS)
    for s in seats:
        if s not in SEATS + GATES:
            die(f"unknown seat {s}")
    env = {k: os.environ[k] for k in KEEP_ENV if k in os.environ}
    builtins = claude_builtins(env) if any(default_vendor(s) == "claude" for s in seats) else None
    results = [probe_seat(s, home, logs, builtins) for s in seats]
    for r in results:
        print(redact(json.dumps(r, indent=1)))
    if logs is not None:
        (logs / "seat-probe.json").write_text(redact(json.dumps({"builtins": builtins, "seats": results}, indent=2)) + "\n")
    bad = [r["seat"] for r in results if r["problems"]]
    print(f"seat probe on {machine()}, {now()}: " + ("each seat loads only its toolbelt" if not bad else f"PROBLEMS: {', '.join(bad)}"))
    sys.exit(1 if bad else 0)


# --- preflight --------------------------------------------------------------------------

def cmd_check(a) -> None:
    """What the launcher needs on this machine; the Open's own preflight covers the applications."""
    gaps = []
    for tool in ("claude", "codex"):
        if not any(os.access(os.path.join(d, tool), os.X_OK) for d in os.environ.get("PATH", "").split(os.pathsep)):
            gaps.append(f"{tool} is not on PATH")
    folders = load_folders(STUDIOS)
    gaps += folders.problems
    media = folders.resolve("media", "")
    if media is None:
        gaps.append("`media` is not set up on this machine (folders.local at the top of studios)")
    elif not media.is_dir():
        gaps.append(f"the media folder {media} does not exist")
    if not EMPLOYER_PATHS_FILE.is_file():
        gaps.append(f"no employer-path list at {EMPLOYER_PATHS_FILE}, so no pass is denied those folders")
    home = Path(os.path.expanduser(a.home))
    cfg = home / "config.toml"
    if not cfg.is_file():
        gaps.append(f"no Codex seat home at {home} (seat.py codex-home)")
    else:
        text = cfg.read_text()
        gaps += [f"the seat home leaves {f} on" for f in CODEX_FEATURES_OFF if f"{f} = false" not in text]
        if not (home / "auth.json").exists():
            gaps.append(f"the Codex seat home has no sign-in (CODEX_HOME={home} codex login)")
    for s in SEATS + GATES:
        gaps += belt_gaps(s)
    path, apps = app_env()
    gaps += [f"the allowlist's application path {p} is not on this machine" for p in path + list(apps.values())
             if not os.path.exists(p)]
    # The application doorway: Seatbelt's own runner, and the programs its locks run (Resolve's broker runs on python).
    door = {k: os.path.expanduser(str(v)) for k, v in toolbelts().get("apps", {}).items()}
    listed = {x for s in SEATS for x in seat_belt(s)["apps"]}
    if listed:
        if not os.access("/usr/bin/sandbox-exec", os.X_OK):
            gaps.append("no /usr/bin/sandbox-exec, which the application doorway's locks run under")
        gaps += [f"the allowlist's [apps] has no `{k}` path" for k in sorted((listed - {"resolve"}) | {"python"})
                 if k not in door]
        gaps += [f"the doorway's {k} {p} is not on this machine" for k, p in door.items() if not os.access(p, os.X_OK)]
    # The sound doorway: the keys file it reads, and the two keys, by name only.
    if any(seat_belt(s)["sound"] for s in SEATS):
        import sound as sounddoor  # noqa: E402  launcher/sound.py, beside this file
        keys = sounddoor.KEYS
        if not keys.is_file():
            gaps.append(f"no audio keys file at {keys}, which the sound doorway reads")
        else:
            if keys.stat().st_mode & 0o077:
                gaps.append(f"{keys} is readable by others; it is mode 600")
            names = {ln.strip().removeprefix("export ").partition("=")[0].strip()
                     for ln in keys.read_text(encoding="utf-8").splitlines() if "=" in ln}
            gaps += [f"{keys} has no {k}" for k in ("ELEVENLABS_API_KEY", "GEMINI_API_KEY") if k not in names]
        if not any(under(str(keys), c) for c in CREDENTIAL_PATHS):
            gaps.append(f"{keys} is not in a folder every pass is denied")
    for g in gaps:
        print(f"GAP: {g}")
    print(f"preflight on {machine()}: " + ("clean" if not gaps else f"{len(gaps)} gap(s)"))
    sys.exit(1 if gaps else 0)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("context")
    c.add_argument("--seat", required=True)
    c.add_argument("--engagement", required=True)
    c.add_argument("--pass", dest="pass_id", required=True)
    c.add_argument("--read-only", action="store_true", help="an audit: the pass writes only its scratch folder")
    c.add_argument("--host", action="append", default=[], help="a host a pass on Claude may reach")
    c.add_argument("--cap-minutes", type=float)
    c.add_argument("--cap-tool-calls", type=int)
    c.add_argument("--cap-budget-usd", type=float)
    c.add_argument("--effort", default="", help=f"{CODEX_ESCALATED_EFFORT} only: the Animator's step up, or a Claude seat's second step on Codex")
    c.add_argument("--escalation", default="",
                   help="the record that sends a redraft one tier up: a gate FAIL in audits/, or a dNN ledger entry")
    c.add_argument("--verify", default="", help="a verification pass: the repaired artifact; it runs read-only, on the other vendor")
    c.add_argument("--anchor", default="", help="a gate's anchor; the gate runs on the vendor that did not last write it")
    c.add_argument("--fallback", default="", help="the re-run ticket, when the planned vendor is unavailable")
    c.set_defaults(fn=cmd_context)
    s = sub.add_parser("claude-settings")
    s.add_argument("context")
    s.set_defaults(fn=cmd_claude_settings)
    h = sub.add_parser("codex-home")
    h.add_argument("--home", default=str(DEFAULT_HOME))
    h.set_defaults(fn=cmd_codex_home)
    p = sub.add_parser("codex-pass")
    p.add_argument("context")
    p.add_argument("--home", default=str(DEFAULT_HOME))
    p.set_defaults(fn=cmd_codex_pass)
    l = sub.add_parser("launch")  # noqa: E741
    l.add_argument("context")
    l.add_argument("--prompt-file", required=True)
    l.add_argument("--output", default="", help="the record a Codex or read-only pass's final message is filed to")
    l.add_argument("--home", default=str(DEFAULT_HOME))
    l.add_argument("--run", action="store_true")
    l.set_defaults(fn=cmd_launch)
    r = sub.add_parser("probe")
    r.add_argument("--home", default=str(DEFAULT_HOME))
    r.add_argument("--logs", default="", help="a folder to keep each probe's raw log in, for the Route entry")
    r.set_defaults(fn=cmd_probe)
    t = sub.add_parser("toolbelt", help="copy each seat's allowlisted skills into this machine's toolbelt folder")
    t.set_defaults(fn=cmd_toolbelt)
    q = sub.add_parser("seat-probe", help="one probe pass per seat on its own launch form: only its toolbelt loads")
    q.add_argument("--seat", action="append", default=[], help="a seat or gate; repeat it; all four seats by default")
    q.add_argument("--home", default=str(DEFAULT_HOME))
    q.add_argument("--logs", default="", help="a folder for each probe's raw log (employer folders redacted)")
    q.set_defaults(fn=cmd_seat_probe)
    k = sub.add_parser("check")
    k.add_argument("--home", default=str(DEFAULT_HOME))
    k.set_defaults(fn=cmd_check)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
