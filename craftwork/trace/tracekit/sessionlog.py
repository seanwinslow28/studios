"""Find the coordinator session's own transcript, for its `open`, `readout` and `close` records (SWCB #169).

Ruled on SWCB #169 (2026-10-16), piece 2 of the coordinator's record contract.
The coordinator runs the train and writes its record, and until now its own
records said `raw_log: none`, so nothing could check them. Claude Code writes
every session to `~/.claude/projects/<project>/<session-id>.jsonl` and names the
running session in `$CLAUDE_CODE_SESSION_ID`; the record's `raw_log` points
there. It is a pointer, never a copy: the transcript holds the whole
conversation with Sean and stays on this machine, outside the ledger.

With the pointer in place, rung-0 line 11 reads the session's model stamps like
any seat's. Claude Code prunes old transcripts (`cleanupPeriodDays`, 30 days by
default), so a pointer can stop resolving; line 11 then names the pass as having
no readable log, never passes it.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

__all__ = ["session_log"]


def session_log(session_id: Optional[str] = None, home: Optional[Path] = None) -> Optional[Path]:
    """The transcript of `session_id` (default: the running session), or None when none is on disk."""
    sid = (session_id or os.environ.get("CLAUDE_CODE_SESSION_ID") or "").strip()
    if not sid or "/" in sid:
        return None
    projects = (home or Path.home()) / ".claude" / "projects"
    hits = sorted(projects.glob(f"*/{sid}.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    return hits[0] if hits else None
