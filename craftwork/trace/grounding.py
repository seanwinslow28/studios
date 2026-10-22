#!/usr/bin/env python3
"""Write each output's `grounding:` line from the pass's reads, so no seat declares it (SWCB #260).

    python3 craftwork/trace/grounding.py <eng> pass-NN            # write the line in every output
    python3 craftwork/trace/grounding.py <eng> pass-NN --check    # say what it should read, write nothing

The coordinator runs it on return, after pasting `## Corpus read` from reads.py
and listing the outputs' paths, and before taking their hashes. Each output
whose frontmatter has a `grounding:` line gets `full` (this pass, or the pass
that wrote an earlier revision of the same artifact, read a library file),
`manifest-only` (nothing read, and the library is not on this machine) or
`none` (nothing read, though the library was here). Seats leave `pending`.

The record's `## Corpus read` is checked against reads.py's output for its
raw log first: a list that differs, with no dated correction, is refused.

Options: --library <dir> for a library other than `<team>/corpus` beside the
team's trace profile; --cwd <dir> as for reads.py; --repo and --studio as for
check.py. Stdlib only. Exit 0 when every line is written or already right, 1
when --check finds one that is not, 2 when the record cannot be written from,
3 when a line is wrong but its output is already hashed (or superseded).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tracekit.engagement import load_engagement  # noqa: E402
from tracekit.grounding import GroundingError, stamp  # noqa: E402
from tracekit.studio import StudioNotFound, load_profile  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("engagement", help="the engagement folder")
    ap.add_argument("pass_id", help="the pass whose outputs get the line (pass-NN)")
    ap.add_argument("--check", action="store_true", help="say what each line should read; write nothing")
    ap.add_argument("--library", type=Path, help="the studio's private library, if not <team>/corpus")
    ap.add_argument("--cwd", help="the directory relative paths in the log resolve against, when the log omits it")
    ap.add_argument("--repo", type=Path, help="repo root for studio-prefixed paths")
    ap.add_argument("--studio", type=Path, help="a studio profile other than the nearest <team>/trace/studio.py")
    a = ap.parse_args(argv)
    try:
        studio = load_profile(a.studio) if a.studio else None
        eng = load_engagement(Path(a.engagement), repo=a.repo, studio=studio)
        stamps = stamp(eng, a.pass_id, write=not a.check, library=a.library, cwd=a.cwd)
    except (GroundingError, StudioNotFound) as exc:
        print(exc, file=sys.stderr)
        return 2
    for s in stamps:
        print(s.line)
    if any(s.refused for s in stamps):
        return 3
    if a.check and any(s.was is not None and s.was != s.value for s in stamps):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
