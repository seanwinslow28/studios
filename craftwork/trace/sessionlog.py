#!/usr/bin/env python3
"""Print the running coordinator session's transcript path, for its record's `raw_log` (SWCB #169).

    python3 craftwork/trace/sessionlog.py                 # the session this command runs in
    python3 craftwork/trace/sessionlog.py <session-id>    # another session's

Run it from the coordinator's own session at Open, Readout and Close, and
write the printed path as that record's `raw_log`. It is a pointer, never a
copy: the transcript stays where Claude Code keeps it, outside the ledger.
Rung-0 line 11 then checks the record's `runtime:` against the session's model
stamps. The meter stays `UNMEASURED`: the desktop app reports no token count
for a session.

Stdlib only, read-only. Exit 0 with the path, 2 when no transcript is found
(no session id, or none on disk under ~/.claude/projects/).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tracekit.sessionlog import session_log  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) > 1 or (args and args[0].startswith("-")):
        print(__doc__.split("\n\n")[1], file=sys.stderr)
        return 2
    path = session_log(args[0] if args else None)
    if path is None:
        print("no session transcript found: run this inside the coordinator's Claude Code session, or name the "
              "session id", file=sys.stderr)
        return 2
    print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
