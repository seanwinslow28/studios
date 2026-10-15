#!/usr/bin/env python3
"""Set up the wall for one seat pass, on either vendor.

    seat.py context   --seat S --worktree W --engagement E --pass NN [--branch B]
                      [--test-path P]... [--ops-path P]... [--grant-read F]...
                      [--grant-control F]... [--host H]...
                      [--cap-minutes N] [--cap-tool-calls N] [--cap-budget-usd N]
                      [--effort xhigh] [--escalation R]
                      [--verify A | --anchor A [--fallback ISSUE]]
                      [--candidate REV]                             → <E>/trace/logs/pass-NN.context.json
    seat.py claude-settings <context.json>                      → <passes>/<eng>/pass-NN.settings.json
    seat.py codex-home [--home ~/.codex-devcraft]                → the Codex seat home, its hooks trusted
    seat.py codex-pass <context.json> [--home ...]              → <passes>/<eng>/pass-NN.codex-layer.toml,
                                                                  linked as <home>/<eng>-pass-NN.config.toml
    seat.py worktree <worktree> --engagement E                  → that worktree's own git hooks
    seat.py record <context.json> --check secrets|deps|drill -- TOOL ARGS...
                                                                → <E>/evidence/<check>-<candidate>.txt
    seat.py launch <context.json> --prompt-file F [--output A] [--run]
                                                                → <E>/trace/logs/pass-NN.{jsonl,stderr.log,launch.json}
    seat.py freeze-diff <context.json> --base REV [--point REV] → <E>/artifacts/pass-NN.diff.patch, and its hash
    seat.py probe [--home ...]                                  → the Route entry's model check
    seat.py check [--home ...]                                  → preflight; exit 1 on any gap

The coordinator runs these; no seat does. Every plan-named exception reaches a
pass only through `context`, whose flags the coordinator copies from the plan
gate's frozen "Exceptions on the record" table. Written on the Devcraft build
map's "Build the never-do hooks and sandbox config" ticket (2026-10-11), from
the two vendors' probes that day (see README.md). The caps, the kill switch,
the wall files' move to <passes> (~/.config/devcraft/passes/, outside every
repo, because they hold the machine's employer paths), `-o` to the artifact,
the frozen diff and the probe were added on "Launcher caps and pass-file moves
in seat.py" (2026-10-12), from the master skill design's rulings. The Builder's
one effort step, for an escalation the record names, was added on SWCB #135
(2026-10-13), after dc-eng-002 ran both of its escalations as substitutions.
A pass on the vendor its seat does not default to (a verification pass, a
Claude seat's redraft one tier up onto Codex, a gate whose anchor changed
vendor) was added on SWCB #126 (2026-10-13): the vendor is read from the record
that calls for it, never chosen, and the record's hash goes in the context.
Every pass's scratch folder (outside every repo, the one place a read-only
pass writes, and TMPDIR for the pass) was added on SWCB #148 (2026-10-14),
after dc-eng-003's read-only passes could neither run a probe nor copy the tree.
Sean's own `~/.codex` was denied to every pass, and the toolbelt's plugin skills
copied into the seat home, on SWCB #149 (2026-10-15), after a dc-eng-003 Builder
pass read a system skill there because its contract pointed at it.
The release gate's evidence check (its candidate in the context, `record`, and
`launch` refusing with exit 4) was added on SWCB #150 (2026-10-15), after two
trains spent gate rounds on the coordinator's own missing drill and check records.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
import policy  # noqa: E402

HOOKS = Path(__file__).resolve().parent
GUARD = HOOKS / "guard.py"
PYTHON = "/usr/bin/python3"
GUARD_COMMAND = f"{PYTHON} {GUARD}"
DEFAULT_HOME = Path(os.path.expanduser("~/.codex-devcraft"))
STUDIOS = HOOKS.parents[1]
sys.path.insert(0, str(STUDIOS / "craftwork" / "trace"))
from tracekit import codexlog  # noqa: E402

KEEP_ENV = ("HOME", "USER", "LOGNAME", "PATH", "LANG", "LC_ALL", "TMPDIR", "TERM", "SHELL")

# The pinned ids (bench README, "Baselines"; #99). The config default never picks a pass's model.
CLAUDE_MODEL = "claude-opus-5-5"
CODEX_MODELS = {"builder": "gpt-6.1-sol"}   # every other Codex pass takes the gate default
CODEX_GATE_MODEL = "gpt-6.1-sol"   # every studio's default gate since 2026-10-12 (Sean, SWCB #118); gpt-5.6-sol before
CODEX_EFFORT = "high"
# The one step above it on the ruled ladder (craftwork § Model delegation); past it, stop and ask Sean.
# Never `ultra` (it auto-delegates) and never `max`.
CODEX_ESCALATED_EFFORT = "xhigh"
GATE_FINDINGS = re.compile(r"audits/(plan-gate|release-gate|security-pass)(-r\d+)?\.md")
LEDGER_ENTRY = re.compile(r"d\d+-[^/]+\.md")
# The security pass is filed as a gate seat but runs on a fresh-context Opus 5.5 (bench README).
CLAUDE_LAUNCH = policy.CLAUDE_SEATS + ("security-pass",)
# Per-pass caps, the master skill's day-one defaults; `context --cap-*` overrides them at Open.
DEFAULT_CAPS = {
    "builder": {"minutes": 60, "tool_calls": 200},
    "plan-gate": {"minutes": 20, "tool_calls": 80},
    "release-gate": {"minutes": 20, "tool_calls": 80},
    **{s: {"minutes": 30, "budget_usd": 15} for s in CLAUDE_LAUNCH},
}
# A pass that moves vendor takes the caps of the vendor and kind of pass it becomes (Sean, SWCB #126).
MOVED_CAPS = {
    "claude": DEFAULT_CAPS["verifier"],
    "codex-redraft": DEFAULT_CAPS["builder"],
    "codex-read-only": DEFAULT_CAPS["plan-gate"],
}
# Where a verification pass's repaired artifact or a gate's anchor may sit in the engagement folder.
VENDOR_RECORD_DIRS = ("artifacts", "inherited")
ISSUE_LINK = re.compile(r"https://github\.com/[\w.-]+/[\w.-]+/issues/\d+")
# The `codex exec --json` items that are tool calls; agent_message, reasoning and todo_list are not.
CODEX_TOOL_ITEMS = ("command_execution", "file_change", "mcp_tool_call", "web_search", "collab_tool_call")
KILL_GRACE_S = 10
# A release gate whose evidence is missing does not launch (SWCB #150); 2 is a cap, 3 a helper agent.
EVIDENCE_EXIT = 4
RECORDED_CHECKS = {"secrets": "secret scan", "deps": "dependency check", "drill": "drill"}
# What `record` writes above a check's output, so the file alone is its execution record.
INVOCATION_FIELDS = ("check", "candidate", "cwd", "command", "tool", "interpreter", "worktree HEAD", "exit")
# What the diff check's report records of its own run since SWCB #146.
DIFFCHECK_FIELDS = ("candidate", "command", "cwd", "interpreter", "worktree HEAD", "mode", "process exit")
# The release plan's drill line: **Commands and output:** `evidence/<file>` (sha256 `<hash>`).
DRILL_DECLARED = re.compile(r"\*\*Commands and output:\*\*\s*`evidence/([^`]+)`(?:\s*\(sha256\s*`([0-9a-f]{64})`\))?")
CODEX_FEATURES_OFF = (
    "apps", "plugins", "remote_plugin", "multi_agent", "memories", "browser_use", "computer_use",
    "in_app_browser", "image_generation", "goals", "skill_mcp_dependency_install", "shell_snapshot",
)
# The toolbelt's skills that ship only in Sean's own Codex home: codex-home copies them
# into the seat home's toolbelt/, so no seat reads his (SWCB #149). The system skills
# need no copy; Codex installs them in every home's skills/.system/.
PLUGIN_CACHE = Path(os.environ.get("DEVCRAFT_PLUGIN_CACHE", str(policy.HOME / ".codex" / "plugins" / "cache" / "openai-curated")))
TOOLBELT_PLUGIN_SKILLS = {"superpowers": ("executing-plans", "verification-before-completion")}


def die(msg: str) -> None:
    sys.stderr.write(f"seat.py: {msg}\n")
    sys.exit(1)


def toml_str(s: str) -> str:
    return json.dumps(s)  # a JSON string is a valid TOML basic string


# --- the context ---------------------------------------------------------------

def cmd_context(a) -> None:
    if a.seat not in policy.ALL_ROLES:
        die(f"unknown seat {a.seat}")
    eng = policy.real(a.engagement)
    # A verification pass changes nothing (craftwork § Checks converge), so it runs read-only on either vendor.
    read_only = a.seat in policy.GATES or a.read_only or bool(a.verify)
    escalation = context_escalation(a, eng)
    vendor, basis = context_vendor(a, eng, escalation)
    candidate = context_candidate(a)
    data = {
        "seat": a.seat, "worktree": policy.real(a.worktree), "engagement": eng, "branch": a.branch or "",
        "pass": a.pass_id, "test_paths_add": a.test_path, "ops_paths": a.ops_path,
        "grants": {"read": [policy.real(p) for p in a.grant_read], "control": a.grant_control},
        "hosts": a.host, "read_only": read_only, "vendor": vendor, "vendor_basis": basis,
        "log": os.path.join(eng, "trace", "logs", "guard.jsonl"),
        "caps": context_caps(a, vendor, read_only),
        "effort": a.effort or (CODEX_EFFORT if vendor == "codex" else ""), "escalation": escalation,
        "scratch": policy.scratch_dir(eng, a.pass_id),
    }
    if candidate:
        data["candidate"] = candidate
    ctx = policy.Context(data)  # validates: no exception for AGENTS.md, CLAUDE.md or skills
    ctx.test_paths()  # a repo without the floor stops at Open, but for the Planner drafting it
    out = Path(eng) / "trace" / "logs" / f"pass-{a.pass_id}.context.json"
    if out.exists():
        die(f"{out} exists; a pass's context is written once (never-do 17)")
    make_scratch(ctx.scratch)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2) + "\n")
    print(out)


def context_candidate(a) -> str:
    """The commit a release gate reviews, in full: its drill and automatic checks are read at it (SWCB #150)."""
    if a.seat != "release-gate":
        if a.candidate:
            die("--candidate is the release gate's: the commit its evidence and its review are at")
        return ""
    if not a.candidate:
        die("release-gate names the commit it reviews with --candidate (its drill and automatic checks are read at that hash)")
    sha = git_out(policy.real(a.worktree), "rev-parse", "--verify", "--quiet", f"{a.candidate}^{{commit}}")
    if not sha:
        die(f"{a.candidate} is not a commit in {a.worktree}")
    return sha


def make_scratch(path: str) -> None:
    """The pass's scratch folder: new, empty, private, and inside no repo (SWCB #148)."""
    p = Path(path)
    for d in (p, *p.parents):
        if (d / ".git").exists():
            die(f"the scratch folder {p} is inside the repo at {d}; set DEVCRAFT_SCRATCH_ROOT outside every repo")
    if p.exists() and any(p.iterdir()):
        die(f"the scratch folder {p} is not empty; a pass starts with an empty one")
    p.mkdir(parents=True, exist_ok=True)
    for d in (p, p.parent, policy.SCRATCH_ROOT):
        os.chmod(d, 0o700)


def context_caps(a, vendor: str, read_only: bool) -> Dict[str, float]:
    """The pass's default caps, with any override the Open stated (it records the why in the brief).

    On its own vendor a pass takes its seat's caps; moved, it takes the caps of
    the vendor and kind of pass it becomes.
    """
    if vendor == policy.default_vendor(a.seat):
        caps = dict(DEFAULT_CAPS.get(a.seat, {}))
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
    rec = Path(policy.real(os.path.join(eng, path)))
    rel = os.path.relpath(rec, eng)
    if rel.startswith(".."):
        die(f"{flag} names a record in the engagement folder, not {rec}")
    if not rec.is_file():
        die(f"no record at {rel}")
    return rec, rel, rec.read_text(encoding="utf-8")


def context_escalation(a, eng: str) -> Optional[Dict[str, str]]:
    """The record that sends a redraft one tier up, or None.

    The ladder (craftwork § Model delegation) is Opus 5.5 → Codex high → Codex
    xhigh → stop and ask Sean. The Builder starts at Codex high, so its step is
    `--effort xhigh`; a Claude seat's step is onto Codex at high, and the one
    after that, at xhigh, only on a ledger entry that names it. The Verifier never
    escalates onto Codex. The record is the gate FAIL that sent the redraft up
    (audits/<gate>[-rN].md, its verdict a FAIL), or the ledger entry where the
    coordinator or Sean called the step for another trigger, which must name it.
    Its hash goes in the context, so the launch can tell the record has not moved since.
    """
    if not a.escalation:
        if a.effort:
            die("an effort step and its record go together: --effort xhigh --escalation <gate FAIL or ledger entry>")
        return None
    if a.seat in policy.GATES:
        die(f"{a.seat} is a gate: a FAIL sends the owning seat's redraft one tier up, and the gate re-runs at its default")
    if a.seat == "verifier":
        die("the Verifier never escalates onto Codex: its ladder is Opus 5.5 → stop and ask Sean (bench README)")
    if a.verify:
        die("a verification pass judges a repair and is never one; --verify and --escalation do not go together")
    if a.seat == "builder" and not a.effort:
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
        if a.effort and a.seat != "builder":
            die(f"a gate FAIL sends {a.seat} one tier up, onto Codex {codex_model(a.seat)} {CODEX_EFFORT}; "
                f"the step past it, to {CODEX_ESCALATED_EFFORT}, takes a ledger entry that names it")
    elif LEDGER_ENTRY.fullmatch(rel):
        if step.lower() not in text.lower():
            die(f"{rel} does not name the {step} step; the entry that calls an escalation says which")
    else:
        die(f"--escalation names gate findings (audits/<gate>[-rN].md) or a ledger entry (dNN-<slug>.md), not {rel}")
    return {"path": rel, "sha256": sha256(rec)}


def last_writer(text: str) -> Optional[str]:
    """The vendor that last wrote an artifact, from its header's `model:` line, or None.

    The line names the runtime that ran, plus any deviation (artifact header):
    `claude-opus-5-5`, `codex gpt-6.1-sol high`, or `claude-opus-5-5 → codex
    gpt-6.1-sol high: plan gate FAIL`, where the runtime after the last arrow wrote it.
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
    """The vendor this pass runs on, and the record that says so (SWCB #126).

    A gate names its anchor and runs on the vendor that did not last write it; a
    verification pass names the repaired artifact and runs on the vendor that did
    not write the repair (craftwork § Model delegation). `--fallback` keeps either
    on the writer's vendor when the planned one is unavailable, naming the re-run
    ticket the protocol files. A redraft one tier up runs on Codex. Anything else
    runs on its seat's own vendor.
    """
    if a.anchor and a.seat not in policy.GATES:
        die(f"--anchor is a gate's; {a.seat} names a repaired artifact with --verify, or a redraft's record with --escalation")
    if a.verify and a.seat in policy.GATES:
        die(f"{a.seat} is a gate: it names the file it reviews with --anchor, not --verify")
    if a.seat in policy.GATES and not a.anchor:
        die(f"{a.seat} names the file it reviews with --anchor (artifacts/…), so it runs on the vendor that did not last write it")
    if a.fallback and not (a.anchor or a.verify):
        die("--fallback is for a gate or a verification pass whose planned vendor is unavailable")
    if escalation:
        return "codex", {"by": "escalation", **escalation}
    if not (a.anchor or a.verify):
        return policy.default_vendor(a.seat), {"by": "seat"}
    flag, path = ("--anchor", a.anchor) if a.anchor else ("--verify", a.verify)
    rec, rel, text = engagement_record(eng, path, flag)
    if rel.split(os.sep)[0] not in VENDOR_RECORD_DIRS or rel.count(os.sep) < 1:
        die(f"{flag} names an artifact in artifacts/ or inherited/, not {rel}")
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


def load(path: str) -> policy.Context:
    return policy.Context(json.loads(Path(path).read_text()), source=policy.real(path))


def load_raw(path: str) -> Dict:
    return json.loads(Path(path).read_text())


def caps_of(path: str, seat: str) -> Dict[str, float]:
    """A context written before the caps existed falls back to the seat's defaults."""
    return load_raw(path).get("caps") or dict(DEFAULT_CAPS.get(seat, {}))


def effort_of(ctx: policy.Context) -> str:
    """A context written before the effort step existed runs at the default."""
    return load_raw(ctx.source).get("effort") or (CODEX_EFFORT if ctx.vendor == "codex" else "")


def pass_id_of(context_path: str) -> str:
    return Path(context_path).name.split(".")[0]  # pass-NN


def passes_dir(ctx: policy.Context) -> Path:
    """Where a pass's wall files live: outside every repo, since they hold the employer paths."""
    root = Path(os.path.expanduser(os.environ.get("DEVCRAFT_PASSES", "~/.config/devcraft/passes")))
    d = root / os.path.basename(ctx.engagement)
    d.mkdir(parents=True, exist_ok=True)
    for p in (root, d):
        os.chmod(p, 0o700)
    return d


def wall_file(ctx: policy.Context) -> Path:
    suffix = "settings.json" if ctx.vendor == "claude" else "codex-layer.toml"
    return passes_dir(ctx) / f"{pass_id_of(ctx.source)}.{suffix}"


def write_once(path: Path, text: str) -> None:
    if path.exists() or path.is_symlink():
        die(f"{path} exists; a pass's wall is written once, so a changed wall is a new pass (never-do 17)")
    path.write_text(text)
    os.chmod(path, 0o600)


def sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# --- shared path lists ------------------------------------------------------------

def credential_denies(ctx: policy.Context) -> List[str]:
    out = [p for p in policy.CREDENTIAL_PATHS if policy.real(p) not in ctx.grant_read]
    for root, dirs, files in os.walk(ctx.worktree):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules", ".venv")]
        for f in files:
            p = os.path.join(root, f)
            if policy.is_credential(p, ctx.grant_read):
                out.append(p)
    return out


def other_scratch(ctx: policy.Context) -> List[str]:
    """The engagement's other passes' scratch folders: a Verifier's may hold copies of held-out/ (SWCB #148)."""
    if not ctx.scratch:
        return []
    parent = Path(ctx.scratch).parent
    return sorted(str(d) for d in parent.iterdir() if d.is_dir() and str(d) != ctx.scratch) if parent.is_dir() else []


def complement(ctx: policy.Context, allowed: List[str], depth: int = 4) -> List[str]:
    """Worktree paths no `allowed` pattern can reach, as coarsely as possible.

    The sandbox cannot say "everything but the test paths", so this lists what
    lies outside them as it stands now; a file created later is the guard's.
    """
    out: List[str] = []

    def could_hold(rel_dir: str) -> bool:
        for pat in allowed:
            p = pat.strip().lstrip("./").rstrip("/")
            if "/" not in p or policy.matches(rel_dir, p):
                return True
            static = re.split(r"[*?\[]", p, 1)[0]
            if static.startswith(rel_dir + "/") or (rel_dir + "/").startswith(static.rsplit("/", 1)[0] + "/") and any(c in p for c in "*?["):
                return True
        return False

    def walk(rel: str, level: int) -> None:
        base = os.path.join(ctx.worktree, rel)
        for name in sorted(os.listdir(base)):
            r = os.path.join(rel, name) if rel else name
            if name == ".git" or policy.any_match(r, allowed):
                continue
            full = os.path.join(ctx.worktree, r)
            if os.path.isdir(full) and not os.path.islink(full):
                if could_hold(r) and level < depth:
                    walk(r, level + 1)
                elif not could_hold(r):
                    out.append(full)
            else:
                out.append(full)

    walk("", 0)
    return out


def covered(ctx: policy.Context, patterns: List[str]) -> List[str]:
    """Repo-relative paths the floor `patterns` cover, as coarsely as possible.

    Every existing match at any depth, globs included, as the worktree stands
    now (a matched folder is listed whole), plus each glob-free pattern's
    top-level path even when absent, so it cannot be created either. A match
    created later anywhere else (a new nested `tests/`, a new `test_x.py`) is
    outside the sandbox's list; the guard, the commit hook and the diff check
    still catch it.
    """
    out = set()
    for pat in patterns:
        p = pat.strip()
        p = (p[2:] if p.startswith("./") else p).strip("/")
        if p and not any(c in p for c in "*?["):
            out.add(p)
    for root, dirs, files in os.walk(ctx.worktree):
        rel = os.path.relpath(root, ctx.worktree)
        rel = "" if rel == "." else rel
        keep = []
        for name in sorted(dirs):
            r = os.path.join(rel, name)
            if name in (".git", "node_modules", ".venv"):
                continue
            if policy.any_match(r, patterns):
                out.add(r)
            else:
                keep.append(name)
        dirs[:] = keep
        out.update(r for r in (os.path.join(rel, f) for f in files) if policy.any_match(r, patterns))
    return sorted(out)


def git_out(worktree: str, *args: str) -> str:
    r = subprocess.run(["git", "-C", worktree, *args], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def common_git_dir(worktree: str) -> str:
    r = subprocess.run(["git", "-C", worktree, "rev-parse", "--path-format=absolute", "--git-common-dir"],
                       capture_output=True, text=True)
    return policy.real(r.stdout.strip()) if r.returncode == 0 else ""


def worktree_git_dir(worktree: str) -> str:
    r = subprocess.run(["git", "-C", worktree, "rev-parse", "--path-format=absolute", "--git-dir"],
                       capture_output=True, text=True)
    return policy.real(r.stdout.strip()) if r.returncode == 0 else ""


# --- Claude seats -----------------------------------------------------------------

def claude_settings(ctx: policy.Context) -> Dict:
    if ctx.vendor != "claude":
        die(f"{ctx.seat} runs on Codex in this pass (its context); write its layer with codex-pass")
    emp = policy.employer_paths()
    creds = credential_denies(ctx) + list(policy.SEAN_HOMES)
    no_read = creds + emp + [str(Path(ctx.engagement) / "held-out")] * (ctx.seat != "verifier") + other_scratch(ctx)
    no_read = [p for p in no_read if p]
    gitdir, wtgit = common_git_dir(ctx.worktree), worktree_git_dir(ctx.worktree)
    controls = [os.path.join(ctx.worktree, c.rstrip("/")) for c in ctx.controls()
                if not any(policy.matches(c, g) for g in ctx.grant_control)]
    git_controls = [os.path.join(gitdir, "hooks"), os.path.join(gitdir, "config"), os.path.join(wtgit, "config.worktree")] if gitdir else []
    eng = Path(ctx.engagement)
    records = [str(eng / "trace"), str(eng / "brief.md"), str(eng / "handoff"), str(eng / "index.md")]
    records += [str(p) for p in eng.glob("d[0-9]*.md")]
    records += [str(p) for p in (eng / "audits").glob("*")]
    refs = [str(STUDIOS / "devcraft" / "lanes"), str(STUDIOS / "devcraft" / "corpus")]
    no_write = controls + git_controls + records + refs + [str(passes_dir(ctx).parent)]
    if ctx.read_only:  # the launcher files its one output; its Write tool reaches only the scratch folder
        no_write += [ctx.worktree, ctx.engagement]
    elif ctx.seat == "build-planner":
        no_write.append(ctx.worktree)
    elif ctx.seat == "verifier":
        no_write += complement(ctx, ctx.test_paths())
    elif ctx.seat == "release-reliability":
        no_write += complement(ctx, ctx.ops_paths)
        no_write += [os.path.join(ctx.worktree, t) for t in covered(ctx, ctx.test_paths())]

    def rule(tool: str, p: str) -> List[str]:
        return [f"{tool}(/{p})", f"{tool}(/{p}/**)"] if os.path.isdir(p) or not os.path.exists(p) else [f"{tool}(/{p})"]

    deny: List[str] = []
    for p in no_read:
        deny += rule("Read", p)
    deny += [f"Read(//{ctx.worktree.lstrip('/')}/**/.env)", f"Read(//{ctx.worktree.lstrip('/')}/**/.env.local)"]
    for p in no_write:
        deny += rule("Edit", p)
    deny += [f"Edit(//{ctx.worktree.lstrip('/')}/**/{c})" for c in (".claude/**", ".codex/**", ".agents/**", "AGENTS.md", "CLAUDE.md")]
    deny += [f"Bash({c}:*)" for c in ("sudo", "git push", "brew", "pipx", "crontab", "launchctl load", "launchctl bootstrap",
                                       "launchctl enable", "gh workflow", "gh pr create", "gh issue create", "npm publish", "security")]
    deny += ["WebFetch", "WebSearch", "Task", "Agent"]
    allow_write = []
    if ctx.seat in ("verifier", "release-reliability") and gitdir:
        allow_write = [os.path.join(gitdir, "objects"), wtgit]
        branch = ctx.branch or ""
        if branch:
            allow_write += [os.path.join(gitdir, "refs", "heads", os.path.dirname(branch)) if "/" in branch else os.path.join(gitdir, "refs", "heads"),
                            os.path.join(gitdir, "logs", "refs", "heads", os.path.dirname(branch)) if "/" in branch else os.path.join(gitdir, "logs", "refs", "heads")]
    if ctx.scratch:
        allow_write.append(ctx.scratch)
    return {
        "permissions": {"deny": sorted(set(deny)), "defaultMode": "acceptEdits", "disableBypassPermissionsMode": "disable"},
        "sandbox": {
            "enabled": True, "failIfUnavailable": True, "autoAllowBashIfSandboxed": True,
            "allowUnsandboxedCommands": False, "excludedCommands": [],
            "filesystem": {"denyRead": sorted(set(no_read)), "allowWrite": allow_write,
                           "denyWrite": sorted(set(no_write + git_controls))},
            "network": {"allowedDomains": list(ctx.hosts), "strictAllowlist": True},
        },
        "hooks": {"PreToolUse": [{"matcher": "*", "hooks": [{"type": "command", "command": GUARD_COMMAND, "timeout": 15}]}],
                  "SessionStart": [{"hooks": [{"type": "command", "command": GUARD_COMMAND, "timeout": 15}]}]},
        "env": {"DEVCRAFT_CONTEXT": ctx.source},
        "disableAllHooks": False,
    }


def cmd_claude_settings(a) -> None:
    ctx = load(a.context)
    text = json.dumps(claude_settings(ctx), indent=2) + "\n"
    out = wall_file(ctx)
    write_once(out, text)
    print(out)


# --- Codex seats --------------------------------------------------------------------

def hooks_json() -> Dict:
    return {"hooks": {"PreToolUse": [{"matcher": "Bash|apply_patch", "hooks": [
        {"type": "command", "command": GUARD_COMMAND, "timeout": 15}]}]}}


def snake(event: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", event).lower()


def hook_hash(event: str, group: Dict, h: Dict) -> str:
    """Codex's trust fingerprint for one hook (codex-rs hooks discovery, 0.146)."""
    norm = {"type": "command", "command": h["command"], "timeout": max(1, int(h.get("timeout", 600))),
            "async": bool(h.get("async", False))}
    if h.get("statusMessage") is not None:
        norm["statusMessage"] = h["statusMessage"]
    ident = {"event_name": snake(event), "hooks": [norm]}
    if group.get("matcher") is not None:
        ident["matcher"] = group["matcher"]
    blob = json.dumps(ident, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(blob.encode()).hexdigest()


def floor_profile(name: str, extends: str, deny: List[str]) -> List[str]:
    lines = [f"[permissions.{name}]", f'extends = "{extends}"', f"[permissions.{name}.filesystem]"]
    lines += [f'{toml_str(p)} = "deny"' for p in deny]
    lines += [f'{toml_str(p)} = "read"' for p in policy.SEAN_HOME_OPEN]  # Codex's own install, re-run by its sandbox
    lines += [f"[permissions.{name}.network]", "enabled = false", ""]
    return lines


def copy_toolbelt(home: Path) -> List[str]:
    """Copy the toolbelt's plugin skills into the seat home, from the newest cached version; the gaps."""
    gaps = []
    for plugin, skills in TOOLBELT_PLUGIN_SKILLS.items():
        versions = sorted((d for d in (PLUGIN_CACHE / plugin).glob("*") if (d / "skills").is_dir()),
                          key=lambda d: d.stat().st_mtime) if (PLUGIN_CACHE / plugin).is_dir() else []
        for skill in skills:
            src = versions[-1] / "skills" / skill if versions else None
            if not src or not (src / "SKILL.md").is_file():
                gaps.append(f"{plugin}:{skill} is not in {PLUGIN_CACHE / plugin}")
                continue
            dest = home / "toolbelt" / plugin / skill
            shutil.rmtree(dest, ignore_errors=True)
            shutil.copytree(src, dest, symlinks=False)
    return gaps


def toolbelt_gaps(home: Path) -> List[str]:
    return [f"{p}:{s} has no copy in {home / 'toolbelt'} (seat.py codex-home)"
            for p, skills in TOOLBELT_PLUGIN_SKILLS.items() for s in skills
            if not (home / "toolbelt" / p / s / "SKILL.md").is_file()]


def skill_roots(home: Path) -> Optional[List[str]]:
    """The folders Codex finds skills in under this home, from its own rendered prompt, no model call.

    None when the prompt has no skill-roots table to read: the check then fails closed.
    """
    try:
        r = subprocess.run(["codex", "debug", "prompt-input", "-c", "skills.include_instructions=true"],
                           cwd=str(home), env=dict(os.environ, CODEX_HOME=str(home)), stdin=subprocess.DEVNULL,
                           capture_output=True, text=True, timeout=60)
        text = "\n".join(c.get("text", "") for m in json.loads(r.stdout) for c in m.get("content", []) if isinstance(c, dict))
    except (OSError, ValueError, subprocess.TimeoutExpired, AttributeError):
        return None
    table = re.search(r"### Skill roots\n((?:- `r\d+` = `[^`]+`\n?)+)", text)
    return re.findall(r"- `r\d+` = `([^`]+)`", table.group(1)) if table else None


def cmd_codex_home(a) -> None:
    home = Path(os.path.expanduser(a.home))
    if any(policy.under(policy.real(str(home)), policy.real(h)) for h in policy.SEAN_HOMES):
        die(f"{home} is inside Sean's own Codex home, which every pass is denied (SWCB #149)")
    home.mkdir(parents=True, exist_ok=True)
    os.chmod(home, 0o700)
    hj = home / "hooks.json"
    data = hooks_json()
    hj.write_text(json.dumps(data, indent=2) + "\n")
    deny = list(policy.CREDENTIAL_PATHS) + list(policy.SEAN_HOMES) + policy.employer_paths()
    lines = [
        "# Devcraft's Codex seat home. Written by devcraft/hooks/seat.py codex-home; rewrite it, never hand-edit.",
        "# A pass layers <eng>-pass-NN.config.toml on top with -p; with no layer a pass gets the read-only floor.",
        'default_permissions = "devcraft-floor"', "",
        "[features]", *[f"{f} = false" for f in CODEX_FEATURES_OFF], "",
        "[skills]", "include_instructions = false", "",
        "[shell_environment_policy]", 'inherit = "all"', "ignore_default_excludes = false",
        'exclude = ["*TOKEN*", "*KEY*", "*SECRET*", "*PASSWORD*", "*CREDENTIAL*", "GH_*", "GITHUB_*", "DEVCRAFT_CONTEXT"]', "",
        *floor_profile("devcraft-floor", ":read-only", deny),
        "[hooks.state]",
    ]
    for event, groups in data["hooks"].items():
        for gi, g in enumerate(groups):
            for hi, h in enumerate(g["hooks"]):
                lines += [f'[hooks.state.{toml_str(f"{hj}:{snake(event)}:{gi}:{hi}")}]',
                          f'trusted_hash = "{hook_hash(event, g, h)}"', "enabled = true"]
    (home / "config.toml").write_text("\n".join(lines) + "\n")
    print(home)
    for g in copy_toolbelt(home):
        print(f"GAP: {g}; the Builder's toolbelt names it")
    if not (home / "auth.json").exists():
        print(f"Next, Sean signs this home in once: CODEX_HOME={home} codex login")


def codex_layer(ctx: policy.Context) -> List[str]:
    name = f"pass-{Path(ctx.source).name.split('.')[0].split('pass-')[-1]}"
    held_out = [os.path.join(ctx.engagement, "held-out")] * (ctx.seat != "verifier")  # the Verifier's own slice
    deny = credential_denies(ctx) + list(policy.SEAN_HOMES) + policy.employer_paths() + held_out + other_scratch(ctx)
    rel_read: List[str] = []
    # Only the Builder and Release write the worktree; every other Codex pass, a
    # Planner's redraft included, files its one output by -o and reads the rest.
    writes = not ctx.read_only and ctx.seat in ("builder", "release-reliability")
    if writes:
        for c in ctx.controls():
            # listed even when absent, so the seat cannot create one either
            if not any(policy.matches(c, g) for g in ctx.grant_control):
                rel_read.append(c.rstrip("/"))
        if ctx.seat == "builder":
            rel_read += covered(ctx, ctx.test_paths() + ctx.ops_paths)
        else:  # Release's escalated redraft: its flagged ops paths and nothing else, never a test
            rel_read += covered(ctx, ctx.test_paths())
            rel_read += [os.path.relpath(p, ctx.worktree) for p in complement(ctx, ctx.ops_paths)]
        for must in (".git", ".codex"):
            if must not in rel_read and os.path.exists(os.path.join(ctx.worktree, must)):
                rel_read.append(must)
    extends = ":workspace" if writes else ":read-only"
    lines = [f"# Devcraft pass layer for {ctx.source}. Written by seat.py codex-pass; rewrite it, never hand-edit.",
             f'default_permissions = "{name}"', "",
             f"[projects.{toml_str(ctx.worktree)}]", 'trust_level = "untrusted"', ""]
    lines += [f"[permissions.{name}]", f'extends = "{extends}"', f"[permissions.{name}.filesystem]"]
    lines += [f'{toml_str(p)} = "deny"' for p in sorted(set(deny))]
    lines += [f'{toml_str(p)} = "read"' for p in policy.SEAN_HOME_OPEN]  # Codex's own install, re-run by its sandbox
    lines += [f'{toml_str(ctx.engagement)} = "read"']  # the coordinator's; -o files the final message
    if ctx.scratch:  # the one folder every pass writes, a read-only one included (SWCB #148)
        lines += [f'{toml_str(ctx.scratch)} = "write"']
    if rel_read:
        lines += [f'[permissions.{name}.filesystem.":workspace_roots"]']
        lines += [f'{toml_str(p)} = "read"' for p in sorted(set(rel_read))]
    lines += [f"[permissions.{name}.network]", "enabled = false", ""]
    return lines


def cmd_codex_pass(a) -> None:
    ctx = load(a.context)
    if ctx.vendor != "codex":
        die(f"{ctx.seat} runs on Claude in this pass (its context); write its settings with claude-settings")
    home = Path(os.path.expanduser(a.home))
    profile = codex_profile(ctx)
    # Codex reads a profile only from $CODEX_HOME/<name>.config.toml, so the seat home
    # links to the one copy; the record hashes that copy, and launch checks the link.
    link = home / f"{profile}.config.toml"
    if link.exists() or link.is_symlink():
        die(f"{link} exists; a pass's wall is written once (never-do 17)")
    out = wall_file(ctx)
    write_once(out, "\n".join(codex_layer(ctx)) + "\n")
    link.symlink_to(out)
    print(profile)


def codex_profile(ctx: policy.Context) -> str:
    return f"{os.path.basename(ctx.engagement)}-{pass_id_of(ctx.source)}"


# --- git hooks per build worktree ---------------------------------------------------

def cmd_worktree(a) -> None:
    wt = policy.real(a.worktree)
    if worktree_git_dir(wt) == common_git_dir(wt):
        die(f"{wt} is a main checkout; Devcraft's git hooks go on a build worktree only")
    run = lambda *x: subprocess.run(["git", "-C", wt, *x], check=True)  # noqa: E731
    run("config", "extensions.worktreeConfig", "true")
    run("config", "--worktree", "core.hooksPath", str(HOOKS / "git"))
    run("config", "--worktree", "devcraft.engagement", policy.real(a.engagement))
    print(f"{wt}: core.hooksPath → {HOOKS / 'git'} (this worktree only)")


# --- launch -----------------------------------------------------------------------

def codex_model(seat: str) -> str:
    """The Builder's ruled model; every other pass on Codex, moved or not, takes the gate default."""
    return CODEX_MODELS.get(seat, CODEX_GATE_MODEL)


def files_final_message(ctx: policy.Context) -> bool:
    """The launcher files the final message of every Codex pass (-o) and of a read-only Claude pass."""
    return ctx.vendor == "codex" or ctx.read_only


def number(v: float) -> str:
    return str(int(v)) if float(v).is_integer() else str(v)


def launch_argv(ctx: policy.Context, prompt: str, home: Path, profile: str = "", output: str = "",
                caps: Optional[Dict[str, float]] = None) -> List[str]:
    caps = caps if caps is not None else caps_of(ctx.source, ctx.seat)
    if ctx.vendor == "claude":
        plugin = str(STUDIOS / "devcraft" / "bench" / "plugins" / ctx.seat)
        # A read-only pass's Write reaches only its scratch folder: every other dir it sees is in its Edit denies.
        tools = ("Read,Write,Bash,Glob,Grep,Skill" if ctx.scratch else "Read,Bash,Glob,Grep,Skill") if ctx.read_only \
            else "Read,Write,Edit,Bash,Glob,Grep,Skill"
        # stream-json: the live log the caps watch, and the per-message model stamps rung-0 line 11 reads
        argv = ["claude", "-p", "--output-format", "stream-json", "--verbose", "--model", CLAUDE_MODEL,
                "--permission-mode", "acceptEdits", "--setting-sources", "", "--settings", str(wall_file(ctx)),
                "--strict-mcp-config", "--tools", tools]
        if os.path.isdir(plugin):
            argv += ["--plugin-dir", plugin]
        agents = os.path.join(ctx.worktree, "AGENTS.md")
        if os.path.exists(agents):
            argv += ["--append-system-prompt-file", agents]
        for d in (ctx.worktree, ctx.engagement, str(STUDIOS / "devcraft" / "lanes"), str(STUDIOS / "devcraft" / "corpus")):
            argv += ["--add-dir", d]
        if ctx.scratch:
            argv += ["--add-dir", ctx.scratch]
        if "budget_usd" in caps:
            argv += ["--max-budget-usd", number(caps["budget_usd"])]
        return argv + [prompt]
    effort = effort_of(ctx)
    return ["codex", "exec", "--json", "--model", codex_model(ctx.seat), "-c", f'model_reasoning_effort="{effort}"',
            "-p", profile, "--strict-config", "-c", 'web_search="disabled"', "-C", ctx.worktree,
            "-o", output, prompt]


def scrubbed_env(ctx: policy.Context, home: Path) -> Dict[str, str]:
    env = {k: os.environ[k] for k in KEEP_ENV if k in os.environ}
    env["DEVCRAFT_CONTEXT"] = ctx.source
    env["DEVCRAFT_SEAT"] = ctx.seat
    if ctx.scratch:  # mktemp and Python's tempfile land in the one folder the pass may write
        env["TMPDIR"] = env["DEVCRAFT_SCRATCH"] = ctx.scratch
    if ctx.vendor == "codex":
        env["CODEX_HOME"] = str(home)
    return env


def output_path(ctx: policy.Context, output: str) -> str:
    """The artifact the launcher files the final message into: in artifacts/ or audits/, written once."""
    if not output:
        if files_final_message(ctx):
            die("the launcher files this pass's final message; name its artifact with --output (artifacts/… or audits/…)")
        return ""
    if not files_final_message(ctx):
        die(f"{ctx.seat} writes its own artifact; --output is for a Codex pass or a read-only Claude pass")
    p = Path(output) if os.path.isabs(output) else Path(ctx.engagement) / output
    p = Path(policy.real(str(p)))
    rel = os.path.relpath(p, ctx.engagement)
    if rel.startswith("..") or rel.split(os.sep)[0] not in ("artifacts", "audits") or rel.count(os.sep) < 1:
        die(f"--output must sit in the engagement's artifacts/ or audits/, not {rel}")
    if p.exists():
        die(f"{rel} exists; an output is written once (never-do 17)")
    p.parent.mkdir(parents=True, exist_ok=True)
    return str(p)


class Watch:
    """Reads the live log line by line: the tool calls so far, and what the meter needs."""

    def __init__(self, vendor: str):
        self.vendor = vendor
        self.tool_ids: set = set()
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
        elif t == "assistant":
            for block in (e.get("message") or {}).get("content") or []:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    self.tool_ids.add(block.get("id") or f"anon-{len(self.tool_ids)}")
        elif t == "result":
            self.result = e


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


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


def helper_agent(home: Path, log: Path, thread: Optional[str], rollouts: Path) -> Dict:
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


def cmd_launch(a) -> None:
    ctx = load(a.context)
    home = Path(os.path.expanduser(a.home))
    vendor = ctx.vendor
    caps = caps_of(a.context, ctx.seat)
    wall = wall_file(ctx)
    if not wall.exists():
        die(f"no wall file {wall}; run seat.py {'claude-settings' if vendor == 'claude' else 'codex-pass'} first")
    profile = ""
    if vendor == "codex":
        profile = codex_profile(ctx)
        link = home / f"{profile}.config.toml"
        if not link.is_symlink() or link.resolve() != wall.resolve():
            die(f"{link} does not link to {wall}; run seat.py codex-pass")
    raw = load_raw(a.context)
    escalation, basis = raw.get("escalation"), raw.get("vendor_basis") or {"by": "seat"}
    for named in (escalation, basis):
        if named and named.get("path"):
            rec = Path(ctx.engagement) / named["path"]
            if not rec.is_file() or sha256(rec) != named["sha256"]:
                die(f"{named['path']} changed since the context named it; a changed record is a new pass (never-do 17)")
    evidence = None
    if ctx.seat == "release-gate":
        gaps, evidence = release_evidence(ctx, raw)
        if gaps:
            sys.stderr.write("seat.py: the release gate does not launch without its evidence (SWCB #150):\n"
                             + "".join(f"  - {g}\n" for g in gaps))
            sys.exit(EVIDENCE_EXIT)
    output = output_path(ctx, a.output)
    argv = launch_argv(ctx, Path(a.prompt_file).read_text(), home, profile, output, caps)
    env = scrubbed_env(ctx, home)
    shown = argv[:-1] + ["<prompt>"]
    print(json.dumps({"argv": shown, "env": sorted(env), "caps": caps}, indent=1), file=sys.stderr)
    if not a.run:
        return
    eng = Path(ctx.engagement)
    pid = pass_id_of(ctx.source)
    logs = eng / "trace" / "logs"
    log, err, rec = logs / f"{pid}.jsonl", logs / f"{pid}.stderr.log", logs / f"{pid}.launch.json"
    for p in (log, err, rec):
        if p.exists():
            die(f"{p} exists; a pass is launched once, so a re-run is a new pass (never-do 17)")
    wall_sha = sha256(wall)  # taken at launch: the wall this pass actually ran under
    if ctx.scratch:
        Path(ctx.scratch).mkdir(parents=True, exist_ok=True)
    run = supervise(argv, env, ctx.worktree, log, err, caps, vendor)
    watch: Watch = run.pop("watch")
    rel = lambda p: os.path.relpath(p, eng)  # noqa: E731
    record = {
        "pass": pid, "seat": ctx.seat, "vendor": vendor, "vendor_basis": basis,
        "model": CLAUDE_MODEL if vendor == "claude" else codex_model(ctx.seat),
        "effort": effort_of(ctx), "escalation": escalation,
        "argv": shown, "caps": caps, **run,
        "wall_files": [{"path": str(wall), "sha256": wall_sha}],
        "raw_log": rel(log), "stderr_log": rel(err), "scratch": ctx.scratch or None,
    }
    if evidence is not None:
        record["evidence"] = evidence
    code = 0
    if vendor == "claude":
        res = watch.result or {}
        record["usage"], record["meter_source"] = res.get("usage"), ("claude -p result.usage" if res.get("usage") else "UNMEASURED")
        if output and res.get("subtype") == "success" and isinstance(res.get("result"), str):
            Path(output).write_text(res["result"] + "\n")
    else:
        record["usage"] = watch.usage or None
        record["meter_source"] = "codex turn.completed.usage" if watch.usage else "UNMEASURED"
        rollouts = logs / f"{pid}.rollouts"
        seen = helper_agent(home, log, watch.thread, rollouts)
        record["rollouts"], record["runtime_stamps"] = {"path": rel(rollouts), "files": seen["session_files"]}, seen["stamps"]
        if seen["helper"]:
            record["helper_agent"] = seen["helper"]
            if output and Path(output).exists():
                moved = logs / f"{pid}.discarded{Path(output).suffix}"
                os.replace(output, moved)
                record["discarded_output"] = rel(moved)
            record["outcome"] = "helper agent: output discarded; re-run once as a new pass, a second spawn stops Blocked (#123)"
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


# --- the release gate's evidence (SWCB #150) ----------------------------------------------

def evidence_files(eng: Path, stem: str) -> List[Path]:
    """`<stem>.txt` and its re-runs `<stem>-2.txt`, `-3`…, oldest first: evidence is append-only."""
    found = []
    for p in (eng / "evidence").glob(f"{stem}*.txt"):
        m = re.fullmatch(re.escape(stem) + r"(?:-(\d+))?\.txt", p.name)
        if m:
            found.append((int(m.group(1) or 1), p))
    return [p for _, p in sorted(found)]


def header_fields(text: str) -> Dict[str, str]:
    """The `key: value` lines of a record, the first of each key."""
    out: Dict[str, str] = {}
    for m in re.finditer(r"^([A-Za-z][A-Za-z ]*?): (.*)$", text, re.M):
        out.setdefault(m.group(1), m.group(2).strip())
    return out


def recorded_gaps(text: str, cand: str) -> List[str]:
    """Why a check's file is not a full execution record at the candidate; empty when it is."""
    f = header_fields(text.split("\n## Output", 1)[0])
    missing = [k for k in INVOCATION_FIELDS if not f.get(k)]
    if missing:
        return [f"no full invocation (no {', '.join(missing)})"]
    gaps = []
    if f["candidate"] != cand:
        gaps.append(f"run at {f['candidate'][:12]}, not the candidate")
    if f["worktree HEAD"] != f"{cand} (the candidate)":
        gaps.append("run with the worktree off the candidate")
    return gaps


def diffcheck_gaps(text: str, cand: str) -> List[str]:
    """Why a diff-check report does not clear the gate: it must be complete, at the candidate, and exit 0."""
    f = header_fields(text)
    exits = re.findall(r"^exit: (-?\d+)\s*$", text, re.M)
    missing = [k for k in DIFFCHECK_FIELDS if not f.get(k)] + ["exit"] * (not exits)
    if missing:
        return [f"has no full invocation (no {', '.join(missing)}); re-run the diff check, whose report records its own (SWCB #146)"]
    if f["candidate"] != cand:
        return [f"is at {f['candidate'][:12]}, not the candidate"]
    if f["worktree HEAD"] != f"{cand} (the candidate)":
        return ["ran with the worktree off the candidate"]
    if f["mode"].startswith("fixture"):
        return ["ran in fixture mode, its registry lookups answered from a file"]
    if exits[-1] != "0":
        verdict = next((l for l in text.splitlines() if l.startswith("DIFF CHECK")), f"exit {exits[-1]}")
        return [f"exits {exits[-1]} ({verdict}): every hit must match a frozen exception or a dated yes from Sean"]
    return []


def release_evidence(ctx: policy.Context, raw: Dict) -> Tuple[List[str], List[Dict[str, str]]]:
    """What the release gate launches on, or what it lacks (gate schedule § The automatic checks).

    At the exact candidate the context names: the drill (`drill-<candidate>.txt`,
    or the file the release plan's "Commands and output" line declares, at the
    hash it gives); the secret scan and the dependency check, each filed by
    `record` with its full invocation; and the newest diff-check report, complete
    and clean. A scan's own findings are the gate's to judge, never a refusal.
    """
    eng = Path(ctx.engagement)
    cand = raw.get("candidate") or ""
    if not cand:
        return ["the context names no candidate; write the gate a new context with --candidate <commit>"], []
    short = cand[:7]
    gaps: List[str] = []
    files: List[Path] = []
    plan = eng / ((raw.get("vendor_basis") or {}).get("path") or "artifacts/release-plan.md")
    declared = DRILL_DECLARED.search(plan.read_text(encoding="utf-8")) if plan.is_file() else None
    if declared and "<" not in declared.group(1):
        name, want = declared.group(1), declared.group(2)
    else:
        name, want = f"drill-{short}.txt", None
    drill = eng / "evidence" / name
    if not drill.is_file():
        gaps.append(f"drill: no evidence/{name}")
    elif cand not in drill.read_text(encoding="utf-8", errors="replace"):
        gaps.append(f"drill: evidence/{name} does not name the candidate {cand}")
    elif want and sha256(drill) != want:
        gaps.append(f"drill: evidence/{name} is not the file the release plan hashed (sha256 {want[:12]}…)")
    else:
        files.append(drill)
    for check in ("secrets", "deps"):
        found = evidence_files(eng, f"{check}-{short}")
        good = [p for p in found if not recorded_gaps(p.read_text(encoding="utf-8", errors="replace"), cand)]
        if good:
            files += good
        elif found:
            why = "; ".join(recorded_gaps(found[-1].read_text(encoding="utf-8", errors="replace"), cand))
            gaps.append(f"{RECORDED_CHECKS[check]}: evidence/{found[-1].name} has {why}; file it with seat.py record --check {check}")
        else:
            gaps.append(f"{RECORDED_CHECKS[check]}: no evidence/{check}-{short}.txt; file it with seat.py record --check {check}")
    reports = evidence_files(eng, f"diff-check-{short}")
    if not reports:
        gaps.append(f"diff check: no evidence/diff-check-{short}.txt")
    else:
        why = diffcheck_gaps(reports[-1].read_text(encoding="utf-8", errors="replace"), cand)
        if why:
            gaps.append(f"diff check: evidence/{reports[-1].name} {why[0]}")
        else:
            files.append(reports[-1])
    return gaps, [{"path": os.path.relpath(p, eng), "sha256": sha256(p)} for p in files]


def tool_version(tool: str) -> str:
    """The tool's own `--version` line, or empty when it gives none (never `version`: osv-scanner reads that as a path)."""
    try:
        r = subprocess.run([tool, "--version"], stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return ""
    line = next((l.strip() for l in (r.stdout + r.stderr).splitlines() if l.strip()), "")
    return line if r.returncode == 0 else ""


def interpreter_of(tool: str) -> str:
    if re.fullmatch(r"python[\d.]*", os.path.basename(tool)):
        return f"{tool} (the tool itself)"
    with open(tool, "rb") as f:
        first = f.readline(256)
    return first[2:].decode("utf-8", "replace").strip() if first.startswith(b"#!") else "none (a native binary)"


def cmd_record(a) -> None:
    """Run one of the release gate's checks outside any sandbox and file its output with its full invocation."""
    ctx = load(a.context)
    cand = load_raw(a.context).get("candidate")
    if ctx.seat != "release-gate" or not cand:
        die("record files a release gate's evidence: name the gate's context, written with --candidate")
    argv = a.argv
    if not argv:
        die("name the check's command after --, its tool by full path")
    tool = argv[0]
    if not os.path.isabs(tool) or not os.access(tool, os.X_OK):
        die(f"each check calls its tool by its full path (gate schedule § The automatic checks), not {tool}")
    head = git_out(ctx.worktree, "rev-parse", "HEAD")
    if head != cand:
        die(f"the worktree is at {head[:12] or '?'}, not the candidate {cand[:12]}; a check at the candidate runs on it")
    version = tool_version(tool)
    if not version:
        die(f"{tool} --version gave no version, so the record would be incomplete")
    dirty = git_out(ctx.worktree, "status", "--porcelain").splitlines()
    eng = Path(ctx.engagement)
    (eng / "evidence").mkdir(parents=True, exist_ok=True)
    stem = f"{a.check}-{cand[:7]}"
    taken = evidence_files(eng, stem)
    out = eng / "evidence" / (f"{stem}.txt" if not taken else f"{stem}-{len(taken) + 1}.txt")
    while out.exists():  # a stray name in the sequence; never overwrite
        out = out.with_name(f"{out.stem}x.txt")
    started = now()
    r = subprocess.run(argv, cwd=ctx.worktree, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = [f"# {RECORDED_CHECKS[a.check]} at the candidate {cand}", "",
             f"check: {a.check}", f"candidate: {cand}", f"run: {started}", f"cwd: {ctx.worktree}",
             f"command: {shlex.join(argv)}", f"tool: {tool} ({version})", f"interpreter: {interpreter_of(tool)}",
             f"worktree HEAD: {head} (the candidate)",
             "worktree status: " + (f"{len(dirty)} uncommitted path(s): " + ", ".join(d[3:] for d in dirty[:10])
                                    + (", …" if len(dirty) > 10 else "") if dirty else "clean"),
             f"exit: {r.returncode}", "", "## Output", "", r.stdout.decode("utf-8", "replace")]
    with open(out, "x", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(json.dumps({"path": os.path.relpath(out, eng), "sha256": sha256(out), "candidate": cand, "exit": r.returncode}))


# --- the frozen diff ------------------------------------------------------------------

def cmd_freeze_diff(a) -> None:
    """Save `git diff <base>..<point>` from the target repo as this pass's output; it outlives the worktree."""
    ctx = load(a.context)
    env = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")  # no personal diff settings

    def git(*x: str) -> subprocess.CompletedProcess:
        return subprocess.run(["git", "-C", ctx.worktree, *x], capture_output=True, env=env)

    def commit(rev: str) -> str:
        r = git("rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
        if r.returncode != 0:
            die(f"{rev} is not a commit in {ctx.worktree}")
        return r.stdout.decode().strip()

    base, point = commit(a.base), commit(a.point)
    eng = Path(ctx.engagement)
    out = eng / "artifacts" / f"{a.name or pass_id_of(ctx.source)}.diff.patch"
    if out.exists():
        die(f"{out} exists; a frozen diff is written once (never-do 17)")
    r = git("diff", "--binary", "--full-index", "--no-color", "--no-ext-diff", "--no-textconv", f"{base}..{point}")
    if r.returncode != 0:
        die(f"git diff failed: {r.stderr.decode().strip()}")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(r.stdout)
    print(json.dumps({"path": os.path.relpath(out, eng), "sha256": sha256(out), "base": base, "point": point,
                      "bytes": len(r.stdout)}))


# --- the model check at Route ---------------------------------------------------------

PROBE_PROMPT = "Reply with your exact model id and nothing else."
CLAUDE_STAMP = re.compile(r'"model"\s*:\s*"(claude-[A-Za-z0-9.\-]+)"')  # the trace checker's own stamp


def one_line(s: str, n: int = 80) -> str:
    s = " ".join((s or "").split())
    return s if len(s) <= n else s[: n - 1] + "…"


def run_probe(argv: List[str], cwd: str, env: Dict[str, str]) -> subprocess.CompletedProcess:
    # stdin closed: `codex exec` otherwise waits for piped input to append to the prompt
    try:
        return subprocess.run(argv, cwd=cwd, env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
        return subprocess.CompletedProcess(argv, 124, out, "no answer in 300 s")


def probe_claude(env: Dict[str, str], cwd: str) -> Dict:
    argv = ["claude", "-p", "--output-format", "stream-json", "--verbose", "--model", CLAUDE_MODEL,
            "--setting-sources", "", "--strict-mcp-config", "--tools", "", "--max-budget-usd", "1", PROBE_PROMPT]
    r = run_probe(argv, cwd, env)
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


def probe_codex(model: str, home: Path, env: Dict[str, str], cwd: str) -> Dict:
    argv = ["codex", "exec", "--json", "--model", model, "-c", f'model_reasoning_effort="{CODEX_EFFORT}"',
            "--strict-config", "-c", 'web_search="disabled"', "--skip-git-repo-check", "-C", cwd, PROBE_PROMPT]
    r = run_probe(argv, cwd, dict(env, CODEX_HOME=str(home)))
    answer = ""
    for line in r.stdout.splitlines():
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if not isinstance(e, dict):
            continue
        item = e.get("item")
        if e.get("type") == "item.completed" and isinstance(item, dict) and item.get("type") == "agent_message":
            answer = str(item.get("text") or "")
    thread = codexlog.jsonl_thread(r.stdout)
    sessions = [codexlog.read_session(f.read_text(encoding="utf-8"), f.name)
                for f in (codexlog.find_sessions(home, thread) if thread else [])]
    stamps = sorted({f"{m} {e}" for s in sessions if not s.helper for m, e in s.stamps})
    return {"id": model, "on": "codex exec", "effort": CODEX_EFFORT, "answer": answer, "stamps": stamps,
            "exit": r.returncode, "match": stamps == [f"{model} {CODEX_EFFORT}"],
            "error": one_line(r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "") if r.returncode else ""}


def route_entry(results: List[Dict], when: str) -> str:
    lines = [f"**The model check** (`seat.py probe`, {when}; outside the budget). Each pinned id was asked for its own id; "
             "the match is read from the log's model stamp, never the answer."]
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
    with tempfile.TemporaryDirectory(prefix="devcraft-probe-") as cwd:
        results = [probe_claude(env, cwd)]
        for model in sorted(set(CODEX_MODELS.values()) | {CODEX_GATE_MODEL}):
            results.append(probe_codex(model, home, env, cwd))
    print(route_entry(results, now()))
    sys.exit(0 if all(r["match"] for r in results) else 1)


# --- preflight ----------------------------------------------------------------------

def cmd_check(a) -> None:
    gaps = []
    for label, fn in (("employer-path list", policy.employer_paths), ("name list", policy.names)):
        try:
            fn()
        except policy.ContextError as e:
            gaps.append(str(e))
    for tool in ("/opt/homebrew/bin/gitleaks", "/opt/homebrew/bin/osv-scanner", PYTHON):
        if not os.access(tool, os.X_OK):
            gaps.append(f"missing {tool}")
    if not os.access(GUARD, os.R_OK):
        gaps.append(f"the guard is not at {GUARD}")
    home = Path(os.path.expanduser(a.home))
    if not (home / "auth.json").exists():
        gaps.append(f"the Codex seat home has no sign-in (CODEX_HOME={home} codex login)")
    hj = home / "hooks.json"
    if hj.exists():
        data = json.loads(hj.read_text())
        cfg = (home / "config.toml").read_text() if (home / "config.toml").exists() else ""
        for event, groups in data["hooks"].items():
            for gi, g in enumerate(groups):
                for hi, h in enumerate(g["hooks"]):
                    if hook_hash(event, g, h) not in cfg:
                        gaps.append(f"Codex hook {event}:{gi}:{hi} is not trusted at its current hash (it would be skipped silently)")
                    if h["command"] != GUARD_COMMAND:
                        gaps.append(f"Codex hook {event}:{gi}:{hi} does not run the guard")
    else:
        gaps.append(f"no Codex seat home at {home} (seat.py codex-home)")
    if home.is_dir():
        gaps += toolbelt_gaps(home)
        # Codex finds skills by $CODEX_HOME, not by Sean's home; a release that changes that shows here (SWCB #149)
        roots = skill_roots(home)
        if roots is None:
            gaps.append("cannot read the skill roots Codex finds under the seat home (codex debug prompt-input)")
        else:
            gaps += [f"Codex finds skills in {r}, inside Sean's own Codex home" for r in roots
                     if any(policy.under(policy.real(r), policy.real(h)) for h in policy.SEAN_HOMES)]
    for g in gaps:
        print(f"GAP: {g}")
    print("preflight: " + ("clean" if not gaps else f"{len(gaps)} gap(s)"))
    sys.exit(1 if gaps else 0)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("context")
    c.add_argument("--seat", required=True)
    c.add_argument("--worktree", required=True)
    c.add_argument("--engagement", required=True)
    c.add_argument("--pass", dest="pass_id", required=True)
    c.add_argument("--branch", default="")
    for f in ("test-path", "ops-path", "grant-read", "grant-control", "host"):
        c.add_argument(f"--{f}", action="append", default=[])
    c.add_argument("--read-only", action="store_true")
    c.add_argument("--cap-minutes", type=float)
    c.add_argument("--cap-tool-calls", type=int)
    c.add_argument("--cap-budget-usd", type=float)
    c.add_argument("--effort", default="", help=f"{CODEX_ESCALATED_EFFORT} only: the Builder's step up, or a Claude seat's second step on Codex")
    c.add_argument("--escalation", default="",
                   help="the record that sends a redraft one tier up: a gate FAIL in audits/, or a dNN ledger entry")
    c.add_argument("--verify", default="", help="a verification pass: the repaired artifact; it runs read-only, on the other vendor")
    c.add_argument("--anchor", default="", help="a gate's anchor; the gate runs on the vendor that did not last write it")
    c.add_argument("--fallback", default="", help="the re-run ticket, when the planned vendor is unavailable")
    c.add_argument("--candidate", default="", help="the release gate's: the commit it reviews, where its evidence is read")
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
    w = sub.add_parser("worktree")
    w.add_argument("worktree")
    w.add_argument("--engagement", required=True)
    w.set_defaults(fn=cmd_worktree)
    e = sub.add_parser("record")
    e.add_argument("context")
    e.add_argument("--check", required=True, choices=sorted(RECORDED_CHECKS))
    e.epilog = "After --, the check's command, its tool by full path."
    e.set_defaults(fn=cmd_record)
    l = sub.add_parser("launch")  # noqa: E741
    l.add_argument("context")
    l.add_argument("--prompt-file", required=True)
    l.add_argument("--output", default="", help="the artifact a Codex or read-only pass's final message is filed to")
    l.add_argument("--home", default=str(DEFAULT_HOME))
    l.add_argument("--run", action="store_true")
    l.set_defaults(fn=cmd_launch)
    f = sub.add_parser("freeze-diff")
    f.add_argument("context")
    f.add_argument("--base", required=True)
    f.add_argument("--point", default="HEAD")
    f.add_argument("--name", default="", help="the patch's stem in artifacts/ (default pass-NN)")
    f.set_defaults(fn=cmd_freeze_diff)
    r = sub.add_parser("probe")
    r.add_argument("--home", default=str(DEFAULT_HOME))
    r.set_defaults(fn=cmd_probe)
    k = sub.add_parser("check")
    k.add_argument("--home", default=str(DEFAULT_HOME))
    k.set_defaults(fn=cmd_check)
    a, extra = ap.parse_known_args()
    if a.cmd == "record":  # everything after -- is the check's own command
        a.argv = extra[1:] if extra[:1] == ["--"] else extra
    elif extra:
        ap.error(f"unrecognized arguments: {' '.join(extra)}")
    try:
        a.fn(a)
    except policy.ContextError as e:
        die(str(e))


if __name__ == "__main__":
    main()
