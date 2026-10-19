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
the release gate's evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import signal
import socket
import subprocess
import sys
import tempfile
import threading
import time
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
    """Credentials, Sean's own Codex home, the employer folders and the engagement's other scratch folders."""
    parent = Path(ctx["scratch"]).parent
    others = sorted(str(d) for d in parent.iterdir() if d.is_dir() and str(d) != ctx["scratch"]) if parent.is_dir() else []
    return list(CREDENTIAL_PATHS) + list(SEAN_HOMES) + employer_paths() + others


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
    """What a Claude pass reads from outside its working folders: the job, and the studio and its law."""
    reads = [ctx["engagement"], ctx["media_project"], str(MOTIONCRAFT), str(STUDIOS / "craftwork")]
    return reads + [str(STUDIOS / "AGENTS.md")] * (STUDIOS / "AGENTS.md").exists()


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
                                       "launchctl enable", "gh", "npm publish", "security")]
    deny += ["WebFetch", "WebSearch", *CLAUDE_HELPER_TOOLS]
    # Reads outside the working folders need a rule, or headless Read, Glob and Grep are refused there.
    allow = [r for p in claude_reads(ctx) for r in rule("Read", p)]
    return {
        "permissions": {"allow": allow, "deny": sorted(set(deny)), "defaultMode": "acceptEdits",
                        "disableBypassPermissionsMode": "disable"},
        "sandbox": {
            "enabled": True, "failIfUnavailable": True, "autoAllowBashIfSandboxed": True,
            "allowUnsandboxedCommands": False, "excludedCommands": [],
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
        # #197 fills each seat's plugin with links to exactly its toolbelt; with none, no skill loads.
        plugin = MOTIONCRAFT / "bench" / "plugins" / ctx["seat"]
        # A read-only pass's Write reaches only its scratch folder: every other dir it sees is in its Edit denies.
        tools = "Read,Write,Bash,Glob,Grep,Skill" if ctx["read_only"] else "Read,Write,Edit,Bash,Glob,Grep,Skill"
        # stream-json: the live log the caps watch, and the per-message model stamps rung-0 line 11 reads
        argv = ["claude", "-p", "--output-format", "stream-json", "--verbose", "--model", CLAUDE_MODEL,
                "--permission-mode", "acceptEdits", "--setting-sources", "", "--settings", str(wall_file(ctx)),
                "--strict-mcp-config", "--tools", tools]
        if plugin.is_dir():
            argv += ["--plugin-dir", str(plugin)]
        agents = STUDIOS / "AGENTS.md"
        if agents.exists():
            argv += ["--append-system-prompt-file", str(agents)]
        for d in add_dirs(ctx):
            argv += ["--add-dir", d]
        if "budget_usd" in caps:
            argv += ["--max-budget-usd", number(caps["budget_usd"])]
        return argv + [prompt]
    return ["codex", "exec", "--json", "--model", CODEX_MODEL, "-c", f'model_reasoning_effort="{ctx["effort"]}"',
            "-p", profile, "--strict-config", "-c", 'web_search="disabled"', "--skip-git-repo-check",
            "-C", ctx["media_project"], "-o", output, prompt]


def scrubbed_env(ctx: Dict, home: Path) -> Dict[str, str]:
    env = {k: os.environ[k] for k in KEEP_ENV if k in os.environ}
    env["MOTIONCRAFT_CONTEXT"] = ctx["source"]
    env["MOTIONCRAFT_SEAT"] = ctx["seat"]
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
        if e.get("parent_tool_use_id"):
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


def sweep_claude_dirs(fresh: List[str]) -> Dict[str, List[str]]:
    """Claude Code leaves an empty `.claude/` in each --add-dir root; each absent before and empty now is removed."""
    out: Dict[str, List[str]] = {"removed": [], "left": []}
    for d in fresh:
        if os.path.islink(d) or not os.path.isdir(d):
            continue
        try:
            os.rmdir(d)
            out["removed"].append(d)
        except OSError:
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
    fresh = [d for d in (os.path.join(r, ".claude") for r in add_dirs(ctx) + [cwd]) if not os.path.lexists(d)] \
        if vendor == "claude" else []
    run = supervise(argv, env, cwd, log, err, ctx["caps"], vendor)
    watch: Watch = run.pop("watch")
    rel = lambda p: os.path.relpath(p, eng)  # noqa: E731
    record = {
        "pass": pid, "seat": ctx["seat"], "vendor": vendor, "vendor_basis": ctx["vendor_basis"],
        "model": CLAUDE_MODEL if vendor == "claude" else CODEX_MODEL, "effort": ctx["effort"],
        "escalation": ctx["escalation"], "machine": machine(), "media": ctx["media"],
        "argv": shown, "caps": ctx["caps"], "fence": ctx["fence"], **run,
        "wall_files": [{"path": str(wall), "sha256": wall_sha}],
        "raw_log": rel(log), "stderr_log": rel(err), "scratch": ctx["scratch"],
    }
    helpers: List[str] = []
    if vendor == "claude":
        res = watch.result or {}
        record["usage"], record["meter_source"] = res.get("usage"), ("claude -p result.usage" if res.get("usage") else "UNMEASURED")
        record["runtime_stamps"] = sorted(watch.stamps)
        helpers = watch.helpers
        if output and res.get("subtype") == "success" and isinstance(res.get("result"), str):
            Path(output).write_text(res["result"] + "\n")
        swept = sweep_claude_dirs(fresh)
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
    if run["stopped"]:
        record["outcome"] = f"Blocked: budget ({run['stopped']} cap reached)"
        code = 2
    elif run["exit_code"] != 0 and not code:
        record["outcome"] = f"the vendor exited {run['exit_code']}; see {rel(err)}"
        code = 1
    rec.write_text(json.dumps(record, indent=2) + "\n")
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
    k = sub.add_parser("check")
    k.add_argument("--home", default=str(DEFAULT_HOME))
    k.set_defaults(fn=cmd_check)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
