#!/usr/bin/env python3
"""Size check: a studio's always-loaded pages stay within the word budget.

A studio's lead reads two pages at the start of every job: its SKILL.md (the
lead's instructions) and its taste.md. Together they must stay within the
budget, 2,000 words unless Sean raises it. Everything else loads only when a
step asks for it, so it isn't counted.

Usage:
    size_budget.py                 check every studio built from the kit
    size_budget.py NAME [NAME ...] check these studios (folder names or paths)
    size_budget.py --budget 2500   use a different budget

Exit 0 when every studio is within budget, 1 when any is over or missing.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

BUDGET = 2000
ALWAYS_LOADED = ("SKILL.md", "taste.md")
REPO = Path(__file__).resolve().parents[2]


def word_count(text: str) -> int:
    return len(re.findall(r"\S+", text))


def studios(root: Path) -> list[Path]:
    """Top-level folders built from the kit: they hold both always-loaded pages."""
    return sorted(
        p for p in root.iterdir()
        if p.is_dir() and not p.name.startswith(".") and all((p / f).is_file() for f in ALWAYS_LOADED)
    )


def measure(studio: Path) -> tuple[dict[str, int], list[str]]:
    counts, missing = {}, []
    for name in ALWAYS_LOADED:
        f = studio / name
        if f.is_file():
            counts[name] = word_count(f.read_text(encoding="utf-8"))
        else:
            missing.append(name)
    return counts, missing


def resolve(arg: str, root: Path) -> Path:
    p = Path(arg)
    return p if p.is_dir() else root / arg


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("studios", nargs="*")
    ap.add_argument("--budget", type=int, default=BUDGET)
    ap.add_argument("--root", type=Path, default=REPO, help="the studios repo's top folder")
    args = ap.parse_args(argv)

    targets = [resolve(s, args.root) for s in args.studios] or studios(args.root)
    if not targets:
        print("No studios built from the kit yet. Nothing to check.")
        return 0

    failed = False
    for studio in targets:
        counts, missing = measure(studio)
        total = sum(counts.values())
        parts = ", ".join(f"{n} {c}" for n, c in counts.items())
        if missing:
            failed = True
            print(f"MISSING  {studio.name}: no {' or '.join(missing)}")
        elif total > args.budget:
            failed = True
            print(f"OVER     {studio.name}: {total} words of {args.budget} ({parts}). "
                  "Move detail into an expertise brief or a tool guide.")
        else:
            print(f"ok       {studio.name}: {total} words of {args.budget} ({parts})")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
