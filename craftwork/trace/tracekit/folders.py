"""Named folders set per machine (SWCB #210, ruled on #186 §§ 7–8).

A record's input or output path may start with a name and a colon,
`media:<path inside that folder>`. Each machine says where each name lives in
one untracked settings file at the repo root, `folders.local`:

    # this machine only, never committed
    media = ~/Movies/Animation-Studio
    target = ~/Code-Brain            # Devcraft could write target:<repo>/...

One line per name, `name = folder`, `#` starts a comment. The folder is a full
path, or one starting `~/`. `$TRACEKIT_FOLDERS` names another settings file in
its place (a repo outside `studios`, or a test). `folders.example` beside it is
tracked and holds no real path.

A name this machine does not map is **not set up on this machine**: a state of
its own beside current, changed and missing, and never a pass. Moving a folder,
or opening the ledger on another machine, changes one line; the records keep
their paths. Paths with no name resolve exactly as before.

Stdlib only.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Optional

__all__ = [
    "ENV_VAR",
    "NOT_SET_UP",
    "NOT_SET_UP_TEXT",
    "SETTINGS_FILE",
    "Folders",
    "load_folders",
    "read_folders",
    "split_named",
]

SETTINGS_FILE = "folders.local"
ENV_VAR = "TRACEKIT_FOLDERS"
NOT_SET_UP = "not-set-up"
NOT_SET_UP_TEXT = "not set up on this machine"

_NAME = r"[a-z][a-z0-9-]*"
_NAMED = re.compile(rf"^({_NAME}):(.+)$")
_LINE = re.compile(rf"^({_NAME})\s*=\s*(.+)$")


def split_named(rel: str) -> Optional[tuple[str, str]]:
    """`media:a/b.png` → ("media", "a/b.png"); anything that is not a named path → None.

    The path after the name stays inside its folder: never a full path, never `..`,
    never empty. A web address (`https://…`) is not a name.
    """
    m = _NAMED.match(rel.strip())
    if not m:
        return None
    name, inner = m.group(1), m.group(2)
    if inner.startswith(("/", "\\")):
        return None
    if ".." in PurePosixPath(inner).parts:
        return None
    return name, inner


def read_folders(path: Path) -> tuple[dict[str, Path], list[str]]:
    """Read one settings file: the names it maps, and a line for each line it could not read."""
    folders: dict[str, Path] = {}
    problems: list[str] = []
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        m = _LINE.match(line)
        if not m:
            problems.append(f"{path.name} line {n}: expected `name = folder`, got {raw.strip()!r}")
            continue
        folder = Path(os.path.expanduser(m.group(2).strip()))
        if not folder.is_absolute():
            problems.append(f"{path.name} line {n}: `{m.group(1)}` must name a full path or one starting ~/")
            continue
        folders[m.group(1)] = folder
    return folders, problems


@dataclass
class Folders:
    """This machine's named folders, and where they were read from."""
    folders: dict[str, Path] = field(default_factory=dict)
    source: Optional[Path] = None
    problems: list[str] = field(default_factory=list)

    def resolve(self, name: str, inner: str) -> Optional[Path]:
        base = self.folders.get(name)
        return base / inner if base is not None else None

    def is_set_up(self, name: str) -> bool:
        return name in self.folders


def load_folders(repo: Optional[Path]) -> Folders:
    """`$TRACEKIT_FOLDERS` if set, else `<repo>/folders.local`, else no names at all."""
    env = os.environ.get(ENV_VAR)
    path = Path(env).expanduser() if env else (repo / SETTINGS_FILE if repo is not None else None)
    if path is None or not path.is_file():
        return Folders(source=path)
    folders, problems = read_folders(path)
    return Folders(folders, path, problems)
