#!/usr/bin/env python3
"""Build an empty studio from the kit's template.

Usage:
    new_studio.py NAME "WHAT IT MAKES" [--title TITLE] [--root DIR]

Copies craftwork/template/ into NAME/, fills in the studio's name, makes the
private library/ folder (git ignores it), links the studio in as a skill for
Claude (.claude/skills/NAME) and Codex (.agents/skills/NAME), then runs the
size check and the old-terms scan on it. The rest of the build is in
craftwork/guides/build-a-studio.md.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
TEMPLATE = KIT / "template"
sys.path.insert(0, str(KIT / "checks"))

import old_terms  # noqa: E402
import size_budget  # noqa: E402

SKILL_LINKS = (Path(".claude/skills"), Path(".agents/skills"))


def fill(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def build(name: str, makes: str, title: str, root: Path) -> Path:
    if not re.fullmatch(r"[a-z][a-z0-9-]*", name):
        raise SystemExit(f"The name must be lower case letters, digits or dashes: {name!r}")
    studio = root / name
    if studio.exists():
        raise SystemExit(f"{studio} already exists. Pick another name, or remove it first.")
    for base in SKILL_LINKS:
        link = root / base / name
        if link.exists() or link.is_symlink():
            raise SystemExit(f"{link} already exists. Remove it before building this studio.")

    values = {"name": name, "title": title, "makes": makes}
    shutil.copytree(TEMPLATE, studio)
    for f in studio.rglob("*.md"):
        f.write_text(fill(f.read_text(encoding="utf-8"), values), encoding="utf-8")
    left = [str(f.relative_to(root)) for f in studio.rglob("*.md") if "{{" in f.read_text(encoding="utf-8")]
    if left:
        raise SystemExit(f"Unfilled placeholders left in: {', '.join(left)}")
    (studio / "library").mkdir()

    for base in SKILL_LINKS:
        (root / base).mkdir(parents=True, exist_ok=True)
        os.symlink(Path("..") / ".." / name, root / base / name)
    return studio


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("name", help="lower case, one word: what Sean types to call the studio")
    ap.add_argument("makes", help='what the studio makes, e.g. "films, animation and all motion work"')
    ap.add_argument("--title", help="the display name (default: the name, capitalised)")
    ap.add_argument("--root", type=Path, default=KIT.parent, help="the studios repo's top folder")
    args = ap.parse_args(argv)

    root = args.root.resolve()
    studio = build(args.name, args.makes, args.title or args.name.capitalize(), root)
    print(f"Built {studio.name}/ from the template, with its skill links.\n")

    size_ok = size_budget.main([str(studio), "--root", str(root)]) == 0
    terms_ok = old_terms.main([str(studio)]) == 0
    print("\nNext: fill it in with Sean, following craftwork/guides/build-a-studio.md.")
    return 0 if size_ok and terms_ok else 1


if __name__ == "__main__":
    sys.exit(main())
