"""Read a Codex pass's own session files: which model ran, and whether it handed work to a helper.

Ruled on SWCB #123 (2026-10-12). Codex's sub-agent tools survive every config
switch (`multi_agent = false`, `agents.max_threads = 1`; probes of 2026-10-10 on
0.146.0 and 0.160.1), so a spawn is caught from the logs, never prevented. The
`--json` stream is not enough to catch it: it shows a `collab_tool_call` item
only when the parent waits on the helper, never the spawn itself, and the
helper's tokens never reach `turn.completed.usage`. The session files Codex
writes under `$CODEX_HOME/sessions/` hold the whole truth: the parent's
`spawn_agent` call, a `sub_agent_activity` event, one file per helper whose
`session_meta` says `thread_source: subagent`, and a `turn_context` stamp of
model and effort on every turn.

The coordinator copies a pass's session files into `trace/logs/pass-NN.rollouts/`
beside its `pass-NN.jsonl` (`collect`, or `python3 -m tracekit.codexlog collect`).
Rung-0 line 11 reads them. `codex review` is not a launch form (#123): every
Codex pass runs `codex exec --json`, so no helper is ever expected.
"""
from __future__ import annotations

import json
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional

__all__ = [
    "Session", "read_session", "read_sessions", "jsonl_helpers", "jsonl_thread",
    "rollout_dir", "parse_runtime", "find_sessions", "collect",
]

SPAWN_CALLS = ("spawn_agent",)   # the function call that starts a helper


@dataclass
class Session:
    """One session file: a pass's own thread, or a helper it started."""
    path: str
    id: str = ""
    root: str = ""                       # session_meta.session_id: the thread this one belongs to
    helper: bool = False                 # started by another thread (a spawn, or codex review's reviewer)
    stamps: set[tuple[str, str]] = field(default_factory=set)   # (model, effort) from each turn_context
    spawn_calls: int = 0
    helper_events: int = 0               # sub_agent_activity events
    usage: Optional[dict[str, int]] = None   # the last token_count's total_token_usage
    error: str = ""


def read_session(text: str, path: str = "") -> Session:
    s = Session(path=path)
    for n, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            s.error = f"line {n} is not JSON"
            continue
        t, p = e.get("type"), e.get("payload")
        if not isinstance(p, dict):
            continue
        if t == "session_meta":
            s.id = str(p.get("id") or "")
            s.root = str(p.get("session_id") or s.id)
            src = p.get("source")
            s.helper = (p.get("thread_source") == "subagent" or (isinstance(src, dict) and "subagent" in src)
                        or bool(p.get("parent_thread_id")) or (bool(s.root) and s.root != s.id))
        elif t == "turn_context" and p.get("model"):
            s.stamps.add((str(p["model"]), str(p.get("effort") or "")))
        elif t == "response_item" and p.get("type") == "function_call" and p.get("name") in SPAWN_CALLS:
            s.spawn_calls += 1
        elif t == "event_msg" and p.get("type") == "sub_agent_activity":
            s.helper_events += 1
        elif t == "event_msg" and p.get("type") == "token_count":
            info = p.get("info") or {}
            if isinstance(info.get("total_token_usage"), dict):
                s.usage = info["total_token_usage"]
    if not s.id and not s.error:
        s.error = "no session_meta"
    return s


def read_sessions(folder: Path) -> list[Session]:
    return [read_session(f.read_text(encoding="utf-8"), f.name) for f in sorted(folder.glob("*.jsonl")) if f.is_file()]


def jsonl_helpers(text: str) -> list[str]:
    """The `collab_tool_call` tools a `codex exec --json` stream shows: any one means a helper was in play."""
    tools: list[str] = []
    seen: set[str] = set()
    for line in text.splitlines():
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        item = e.get("item") if isinstance(e, dict) else None
        if isinstance(item, dict) and item.get("type") == "collab_tool_call" and item.get("id") not in seen:
            seen.add(item.get("id"))
            tools.append(str(item.get("tool") or "?"))
    return tools


def jsonl_thread(text: str) -> Optional[str]:
    for line in text.splitlines():
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(e, dict) and e.get("type") == "thread.started":
            return e.get("thread_id")
    return None


def rollout_dir(raw_log: str) -> str:
    """`trace/logs/pass-07.jsonl` → `trace/logs/pass-07.rollouts`."""
    p = raw_log.strip()
    return (p[: -len(".jsonl")] if p.endswith(".jsonl") else p) + ".rollouts"


def parse_runtime(runtime: str) -> Optional[tuple[str, str]]:
    """`codex gpt-5.6-sol high` → ("gpt-5.6-sol", "high"). Row 3 only; a provider route returns None."""
    parts = runtime.split()
    if len(parts) < 2 or parts[0] != "codex":
        return None
    return parts[1], (parts[2] if len(parts) > 2 else "")


def find_sessions(codex_home: Path, thread_id: str) -> list[Path]:
    """Every session file under `$CODEX_HOME/sessions/` that belongs to this thread: its own, and its helpers'."""
    found = []
    for f in sorted((codex_home / "sessions").rglob("rollout-*.jsonl")):
        try:
            with f.open(encoding="utf-8") as fh:
                meta = json.loads(fh.readline()).get("payload") or {}
        except (OSError, json.JSONDecodeError):
            continue
        if thread_id in (meta.get("id"), meta.get("session_id"), meta.get("parent_thread_id")):
            found.append(f)
    return found


def collect(codex_home: Path, thread_id: str, dest: Path) -> list[Path]:
    """Copy a pass's session files into its `pass-NN.rollouts/` folder. Copies, never moves: the seat home keeps its own."""
    files = find_sessions(codex_home, thread_id)
    dest.mkdir(parents=True, exist_ok=True)
    out = []
    for f in files:
        shutil.copy2(f, dest / f.name)
        out.append(dest / f.name)
    return out


def _main(argv: Iterable[str]) -> int:
    args = list(argv)
    if len(args) != 4 or args[0] != "collect":
        print("usage: python3 -m tracekit.codexlog collect <CODEX_HOME> <pass-NN.jsonl> <pass-NN.rollouts/>", file=sys.stderr)
        return 2
    home, log, dest = Path(args[1]).expanduser(), Path(args[2]), Path(args[3])
    thread = jsonl_thread(log.read_text(encoding="utf-8"))
    if not thread:
        print(f"{log}: no thread.started event, so no thread to collect", file=sys.stderr)
        return 1
    files = collect(home, thread, dest)
    print(f"{len(files)} session file(s) for thread {thread} → {dest}")
    return 0 if files else 1


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
