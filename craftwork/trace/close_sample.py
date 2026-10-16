#!/usr/bin/env python3
"""Optional blind Close check: draw once, then compare Sean's saved answers.

    python3 craftwork/trace/close_sample.py draw <engagement>
    python3 craftwork/trace/close_sample.py compare <engagement>

Writes only trace/close-sample/. Never changes labels, records or approval.
Exit 0: draw made / sample agrees (approval still Sean's); 1: wider review;
2: incomplete answers, changed evidence or invalid input.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from tracekit.close_sample import compare, draw
from tracekit.engagement import load_engagement
from tracekit.studio import load_profile


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("draw", "compare"))
    parser.add_argument("engagement")
    parser.add_argument("--repo", help="repo root for studio-prefixed inputs")
    parser.add_argument("--studio", help="studio profile, otherwise resolved as in render.py")
    args = parser.parse_args(argv)
    try:
        path = Path(args.engagement)
        if not path.is_dir():
            raise ValueError(f"no engagement folder at {path}")
        eng = load_engagement(path, repo=Path(args.repo) if args.repo else None,
                              studio=load_profile(args.studio) if args.studio else None)
        if args.action == "draw":
            page = draw(eng)
            print(f"Open {page} before reading eval.html or the drafted labels. "
                  "Save your answers beside it as blind-labels.md, then run compare.")
            return 0
        agrees, report = compare(eng)
        print(report.read_text(encoding="utf-8"))
        return 0 if agrees else 1
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Close sample held: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
