#!/usr/bin/env python3
"""Print a pass's `## Corpus read` list, recovered from its own transcript (SWCB #169).

    python3 craftwork/trace/reads.py <eng>/trace/logs/pass-NN.jsonl
    python3 craftwork/trace/reads.py <log> --cwd <dir>     # where relative paths resolve, if the log omits it

The coordinator pastes stdout under the record's `## Corpus read` and never
types that list. stdout is one `- <path>` line per corpus file the transcript
shows the pass reading, or `none`. A Claude log (stream-json, an Agent-tool
subagent JSONL, a session file) and a Codex `--json` log are both read; a
Codex log's session files in `pass-NN.rollouts/` beside it are read too.

Calls that name a corpus path the script cannot judge (a heredoc script, an
unknown program, a failed command) go to stderr, one per line: check each
against the transcript and say what you found in `## Notes`. They are never
guessed into the list.

Stdlib only, read-only. Exit 0 when the log was read (whatever it shows), 2
when it could not be.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tracekit.reads import format_section, read_logs  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("log", help="the pass's raw log (trace/logs/pass-NN.jsonl)")
    ap.add_argument("--cwd", help="the directory relative paths in the log resolve against, when the log omits it")
    a = ap.parse_args(argv)
    r = read_logs(Path(a.log), a.cwd)
    if r.error:
        print(r.error, file=sys.stderr)
        return 2
    print(format_section(r))
    if r.unjudged:
        print(f"{len(r.unjudged)} call(s) name a corpus path the script did not judge; check each in the "
              f"transcript and say what you found in ## Notes:", file=sys.stderr)
        for u in r.unjudged:
            print(f"  {u}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
