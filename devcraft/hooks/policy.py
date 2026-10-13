"""Devcraft's wall, as data: who may write where, what counts as a control, a
credential or a record, and the machine-local lists. One copy, read by the
PreToolUse guard (`guard.py`), the git hooks (`gitcheck.py`), the settings
generator (`seat.py`) and the diff check (`devcraft/diffcheck/`).

Written on the Devcraft build map's "Build the never-do hooks and sandbox config"
ticket (2026-10-11), from the never-do list (`devcraft/CLAUDE.md`, rule 9) and
the never-do ticket's wall column. Stdlib only, and Python 3.9 or later, because
hooks run under `/usr/bin/python3`.

A pass's facts arrive in a **seat context**: a JSON file the coordinator writes
into the engagement's `trace/logs/` before launching the pass, named by
`$DEVCRAFT_CONTEXT`. Seats cannot write there. Everything plan-named (added test
paths, Release's ops paths, opened credential and control files, network hosts)
comes from the plan gate's frozen exceptions through that file, never from text
a seat can edit.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Iterable, List, Optional

SEATS = ("build-planner", "builder", "verifier", "release-reliability")
CLAUDE_SEATS = ("build-planner", "verifier", "release-reliability")
CODEX_SEATS = ("builder", "plan-gate", "release-gate")
GATES = ("plan-gate", "release-gate", "security-pass")
ALL_ROLES = SEATS + GATES + ("coordinator",)
VENDORS = ("claude", "codex")


def default_vendor(seat: str) -> str:
    """The vendor a seat runs on unless its context names a record that moves it (SWCB #126)."""
    return "codex" if seat in CODEX_SEATS else "claude"

HOME = Path(os.path.expanduser("~"))

# The machine-local lists live outside every repo. They name the employer, so
# they are never tracked and never shown to a seat (their folder is a
# credential-class read deny below).
LOCAL_DIR = Path(os.environ.get("DEVCRAFT_LOCAL", str(HOME / ".config" / "devcraft")))
EMPLOYER_PATHS_FILE = LOCAL_DIR / "employer-paths"
NAMES_FILE = LOCAL_DIR / "names"

# GitHub owners whose repos count as Sean's (never-do 1).
OWNERS = ("seanwinslow28",)

# --- Controls (never-do 14) -------------------------------------------------
# Relative to the target worktree, matched gitignore-style (`matches`): a name
# with no inner "/" at any depth. AGENTS.md, CLAUDE.md and skills have
# no exception, ever.
CONTROLS = (
    ".claude/", ".codex/", ".agents/", ".devcraft/", ".github/workflows/",
    ".git/", ".git", ".gitmodules", ".githooks/", ".husky/", ".pre-commit-config.yaml",
    "lefthook.yml", "lefthook.yaml", ".mcp.json",
    "AGENTS.md", "CLAUDE.md", "AGENTS.override.md",
)
NO_EXCEPTION = (".claude/skills/", ".agents/skills/", ".codex/skills/", "AGENTS.md", "CLAUDE.md", "AGENTS.override.md")
# Extra controls when the target worktree is the studios repo itself.
STUDIOS_CONTROLS = (
    "devcraft/hooks/", "devcraft/diffcheck/", "devcraft/CLAUDE.md", "craftwork/trace/check.py",
    "craftwork/trace/tracekit/checker.py", "bin/canary-check.sh",
)

# --- Credentials (never-do 6) -----------------------------------------------
CREDENTIAL_PATHS = tuple(str(HOME / p) for p in (
    ".ssh", ".aws", ".gnupg", ".config/gh", ".config/swcb/secrets", ".config/devcraft",
    ".codex/auth.json", ".codex-devcraft/auth.json", ".claude/.credentials.json",
    ".netrc", ".git-credentials", ".docker/config.json", ".npmrc", ".pypirc",
    ".kube/config", ".config/gcloud", ".azure", "Library/Keychains",
))
# `.env*` anywhere, except the two example names.
ENV_FILE = re.compile(r"(^|/)\.env[^/]*$")
ENV_OK = re.compile(r"(^|/)\.env\.(example|sample)$")
CREDENTIAL_VAR = re.compile(r"(TOKEN|SECRET|PASSWORD|PASSWD|API_?KEY|ACCESS_?KEY|PRIVATE_?KEY|CREDENTIAL|AUTH)", re.I)

# --- Records (never-do 17) ---------------------------------------------------
# Relative to the engagement folder. Seats write only `artifacts/` and new
# files in `audits/`; everything else there is the coordinator's.
SEAT_ENGAGEMENT_WRITES = ("artifacts/",)
VERIFIER_ENGAGEMENT_WRITES = ("held-out/",)  # the slice the Builder never sees
SEAT_ENGAGEMENT_CREATES = ("audits/",)

# --- Snapshot and golden-file regeneration (never-do 4) ----------------------
SNAPSHOT_FLAGS = re.compile(
    r"^(-u|--update-?snapshots?(=.*)?|--updateSnapshot|--snapshot-update|--snapshot-update=.*|"
    r"--update-goldens?|--force-regen|--inline-snapshot=(fix|create|update|trim).*|--accept)$"
)
SNAPSHOT_ENV = re.compile(r"^(UPDATE_SNAPSHOTS?|SNAPSHOT_UPDATE|UPDATE_GOLDENS?|INSTA_UPDATE|INSTA_FORCE_PASS)=")


class ContextError(Exception):
    pass


def read_list(path: Path) -> List[str]:
    """One entry per line; blank lines and `#` comments skipped."""
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(line)
    return out


def employer_paths() -> List[str]:
    """Resolved employer paths. A missing list is an error: the wall fails closed."""
    if not EMPLOYER_PATHS_FILE.is_file():
        raise ContextError(f"the employer-path list is missing ({EMPLOYER_PATHS_FILE})")
    return [real(os.path.expanduser(p)) for p in read_list(EMPLOYER_PATHS_FILE)]


def names() -> List[str]:
    if not NAMES_FILE.is_file():
        raise ContextError(f"the name list is missing ({NAMES_FILE})")
    found = read_list(NAMES_FILE)
    if not found:
        raise ContextError(f"the name list is empty ({NAMES_FILE})")
    return found


def real(path: str) -> str:
    """Absolute, `~` expanded, symlinks resolved (for every part that exists)."""
    return os.path.realpath(os.path.expanduser(path))


def under(path: str, root: str) -> bool:
    return path == root or path.startswith(root.rstrip("/") + "/")


def _pattern_regex(pattern: str) -> re.Pattern:
    out = ""
    i = 0
    while i < len(pattern):
        c = pattern[i]
        if pattern.startswith("**/", i):
            out += "(?:.*/)?"
            i += 3
            continue
        if pattern.startswith("**", i):
            out += ".*"
            i += 2
            continue
        out += {"*": "[^/]*", "?": "[^/]"}.get(c, re.escape(c))
        i += 1
    return re.compile(out)


def matches(rel: str, pattern: str) -> bool:
    """Does repo-relative `rel` fall under `pattern`? Gitignore-style.

    A match covers everything beneath it. A pattern with no "/" except a
    trailing one matches at any depth; one with a "/" inside is anchored to the
    repo root. Globs take `*`, `?` and `**`.
    """
    rel = rel.strip("/")
    pat = pattern.strip()
    if pat.startswith("./"):
        pat = pat[2:]
    pat = pat.strip("/")
    if not pat or rel.startswith(".."):
        return False
    pre = "" if "/" in pat else "(?:.*/)?"
    return re.fullmatch(pre + _pattern_regex(pat).pattern + "(?:/.*)?", rel) is not None


def any_match(rel: str, patterns: Iterable[str]) -> Optional[str]:
    for p in patterns:
        if matches(rel, p):
            return p
    return None


def is_credential(path: str, granted: Iterable[str] = ()) -> bool:
    p = real(path)
    if any(p == real(g) for g in granted):
        return False
    if ENV_FILE.search(p) and not ENV_OK.search(p):
        return True
    return any(under(p, real(c)) for c in CREDENTIAL_PATHS)


class Context:
    """One pass's facts, from the coordinator's context file."""

    def __init__(self, data: dict, source: str = ""):
        self.source = source
        self.seat = data.get("seat", "")
        if self.seat not in ALL_ROLES:
            raise ContextError(f"unknown seat {self.seat!r}")
        self.worktree = real(data["worktree"])
        self.engagement = real(data["engagement"])
        self.branch = data.get("branch", "")
        self.test_paths_add = list(data.get("test_paths_add", []))
        self.ops_paths = list(data.get("ops_paths", []))
        grants = data.get("grants", {})
        self.grant_read = [real(p) for p in grants.get("read", [])]
        self.grant_control = list(grants.get("control", []))
        bad = [c for c in self.grant_control if any_match(c, NO_EXCEPTION)]
        if bad:
            raise ContextError(f"no exception exists for {bad[0]} (never-do 14)")
        self.hosts = list(data.get("hosts", []))
        self.read_only = bool(data.get("read_only", False))
        # A context written before a pass could move vendor runs on its seat's own.
        self.vendor = data.get("vendor") or default_vendor(self.seat)
        if self.vendor not in VENDORS:
            raise ContextError(f"unknown vendor {self.vendor!r}")
        self.log = data.get("log") or os.path.join(self.engagement, "trace", "logs", "guard.jsonl")
        self.extra_read = [real(p) for p in data.get("read_dirs", [])]

    @classmethod
    def from_env(cls) -> "Context":
        path = os.environ.get("DEVCRAFT_CONTEXT", "")
        if not path:
            raise ContextError("DEVCRAFT_CONTEXT is not set")
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            raise ContextError(f"cannot read the seat context {path}: {e}")
        return cls(data, source=path)

    # -- test paths ---------------------------------------------------------
    def test_paths(self) -> List[str]:
        floor = Path(self.worktree) / ".devcraft" / "test-paths"
        if not floor.is_file():
            # The one exception: Open's one-off, where the Planner drafts the missing floor.
            # It writes only in the engagement folder, so the floor never bears on its wall.
            if self.seat == "build-planner":
                return list(self.test_paths_add)
            raise ContextError(f"the repo has no .devcraft/test-paths floor ({floor})")
        return read_list(floor) + self.test_paths_add

    def controls(self) -> List[str]:
        out = list(CONTROLS)
        if (Path(self.worktree) / "devcraft" / "CLAUDE.md").is_file():
            out += STUDIOS_CONTROLS
        return out

    # -- the one question every write asks ----------------------------------
    def write_verdict(self, path: str, creating: bool = False) -> Optional[str]:
        """None if this seat may write `path`; otherwise the reason it may not."""
        p = real(path)
        if self.read_only:
            return f"{self.seat} runs read-only"
        if under(p, self.engagement):
            rel = os.path.relpath(p, self.engagement)
            if self.vendor == "codex":
                return "the engagement folder is the coordinator's; a Codex pass's final message is filed by -o (never-do 17)"
            if any_match(rel, SEAT_ENGAGEMENT_WRITES):
                return None
            if self.seat == "verifier" and any_match(rel, VERIFIER_ENGAGEMENT_WRITES):
                return None
            if any_match(rel, SEAT_ENGAGEMENT_CREATES):
                if creating and not os.path.exists(p):
                    return None
                return f"{rel} is a record; records are append-only and a correction is a new record (never-do 17)"
            return f"{rel} in the engagement folder is the coordinator's record (never-do 17)"
        if not under(p, self.worktree):
            return f"{p} resolves outside the build's worktree (never-do 7)"
        rel = os.path.relpath(p, self.worktree)
        ctl = any_match(rel, self.controls())
        if ctl:
            granted = any(matches(rel, g) for g in self.grant_control)
            if not granted or any_match(rel, NO_EXCEPTION):
                return f"{rel} is a control ({ctl}) (never-do 14)"
        tests = self.test_paths()
        is_test = any_match(rel, tests) is not None
        is_ops = any_match(rel, self.ops_paths) is not None
        if self.seat == "builder":
            if is_test:
                return f"{rel} is a test path; the Builder never edits a test (never-do 4)"
            if is_ops:
                return f"{rel} is flagged for Release; the Builder never writes it (never-do 4)"
            return None
        if self.seat == "verifier":
            return None if is_test else f"{rel} is not a test path; the Verifier never edits source (never-do 4)"
        if self.seat == "release-reliability":
            if is_test:
                return f"{rel} is a test path; Release never edits tests (never-do 4)"
            return None if is_ops else f"{rel} is not one of Release's flagged ops paths (never-do 4)"
        return f"the {self.seat} writes only in the engagement folder"

    def read_verdict(self, path: str) -> Optional[str]:
        p = real(path)
        if self.seat == "builder" and under(p, os.path.join(self.engagement, "held-out")):
            return "held-out/ is the slice the Builder never sees (test record)"
        if is_credential(p, self.grant_read):
            return f"{p} holds a live credential and no plan line opens it to this seat (never-do 6)"
        for e in employer_paths():
            if under(p, e):
                return "that path is on the machine's employer list (never-do 2)"
        return None
