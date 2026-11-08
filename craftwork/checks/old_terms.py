#!/usr/bin/env python3
"""Old-terms scan: nothing from the studios' earlier setup survives in the new one.

Reads the word list in old_terms.txt beside this file and fails if any of
them appears anywhere in this repo: the kit, every studio, the front pages.

Usage:
    old_terms.py                  scan every file git tracks or would add
    old_terms.py PATH [PATH ...]  scan these files or folders instead

Each studio's private library/ folder is skipped (book notes, never tracked),
and so is anything git ignores.
Exit 0 when nothing is found, 1 when anything is.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
KIT = HERE.parent
REPO = KIT.parent
TERMS_FILE = HERE / "old_terms.txt"
KIT_PARTS = ("README.md", "new_studio.py", "template", "guides", "checks")
TEXT = {".md", ".py", ".txt", ".json", ".html", ".htm", ".sh", ".yml", ".yaml",
        ".toml", ".js", ".mjs", ".ts", ".css", ".csv"}
TEXT_NAMES = {".gitignore"}
SKIP_DIRS = {"library", "__pycache__", ".pytest_cache", "node_modules", ".git"}


def load_terms(path: Path = TERMS_FILE) -> list[tuple[str, re.Pattern]]:
    terms = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("re:"):
            pattern = line[3:]
        else:
            pattern = r"(?<![\w-])" + re.escape(line) + r"(?![\w-])"
        terms.append((line, re.compile(pattern, re.I)))
    return terms


def studios(root: Path) -> list[Path]:
    return sorted(
        p for p in root.iterdir()
        if p.is_dir() and not p.name.startswith(".")
        and (p / "SKILL.md").is_file() and (p / "taste.md").is_file()
    )


def is_text(p: Path) -> bool:
    return p.suffix.lower() in TEXT or p.name in TEXT_NAMES


def default_targets(root: Path = REPO) -> list[Path]:
    """Every text file git tracks or would add, skipping what it ignores."""
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            capture_output=True, check=True, text=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        kit = root / "craftwork"
        return [kit / part for part in KIT_PARTS if (kit / part).exists()] + studios(root)
    files = (root / name for name in out.split("\0") if name)
    return [f for f in files
            if f.is_file() and is_text(f)
            and not any(part in SKIP_DIRS for part in f.relative_to(root).parts)]


def files_in(target: Path):
    if target.is_file():
        yield target
        return
    for p in sorted(target.rglob("*")):
        if any(part in SKIP_DIRS for part in p.relative_to(target).parts):
            continue
        if p.is_file() and is_text(p):
            yield p


def scan(targets: list[Path], terms) -> list[tuple[Path, int, str, str]]:
    hits = []
    for target in targets:
        for f in files_in(target):
            if f.resolve() == TERMS_FILE:
                continue
            try:
                text = f.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for n, line in enumerate(text.splitlines(), 1):
                for term, rx in terms:
                    if rx.search(line):
                        hits.append((f, n, term, line.strip()))
    return hits


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("paths", nargs="*", type=Path)
    args = ap.parse_args(argv)

    targets = args.paths or default_targets()
    hits = scan(targets, load_terms())
    for f, n, term, line in hits:
        try:
            shown = f.resolve().relative_to(REPO)
        except ValueError:
            shown = f
        print(f"{shown}:{n}: \"{term}\" in: {line[:120]}")
    if hits:
        print(f"FOUND {len(hits)} old term(s). Rewrite them in the new setup's own words.")
        return 1
    print(f"clean: no old terms in {len(targets)} place(s) scanned.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
