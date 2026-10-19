#!/usr/bin/env python3
"""Freeze the copies a handoff crosses: strip the binding's process parts, then hash (#326).

    python3 craftwork/trace/freeze.py copy --binding <binding.md> --out <handoff/outbound/artifacts> \\
        <source.md>=<source-id> [<source.md>=<source-id> ...] [--at <ISO instant>]
    python3 craftwork/trace/freeze.py verify <copy.md>[=<source.md>] [...]
    python3 craftwork/trace/freeze.py show --binding <binding.md> <source.md>   # what would be stripped; writes nothing

`copy` writes `<source-id>--<stem>.md` per source and prints the manifest table:
the source hash, the stripped copy's hash, and the names of what was stripped.
`verify` re-hashes each copy without its stamp lines; given `=<source.md>` it also
checks the source has not moved since the freeze. A source may be a named path,
`media:<path>`, read through this machine's `folders.local` (SWCB #210); a name
the machine does not map is reported as not set up here. The binding's fenced `strip`
block names every process part; a binding without one is refused. A file that
is already a frozen copy is refused too: it is forwarded byte for byte, never
re-frozen (handoff contract § 10).

Stdlib only. Exit 0 when every copy is written or verifies, 1 on hash drift or
a moved source, 2 on a usage or binding error, an already-frozen source, or a
named folder not set up on this machine.
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tracekit.freeze import (  # noqa: E402
    MANIFEST_HEADER,
    AlreadyFrozen,
    BindingError,
    freeze,
    is_frozen,
    read_rules,
    strip,
    verify,
)
from tracekit.folders import NOT_SET_UP_TEXT, load_folders, split_named  # noqa: E402

REPO = Path(__file__).resolve().parents[2]


class NotSetUp(Exception):
    pass


def _path(raw: str) -> Path:
    """A plain path as given; a named one (`media:…`) through this machine's folders.local."""
    named = split_named(raw)
    if named is None:
        return Path(raw)
    folders = load_folders(REPO)
    p = folders.resolve(*named)
    if p is None:
        where = folders.source.name if folders.source is not None else "folders.local"
        raise NotSetUp(f"{raw} is {NOT_SET_UP_TEXT}: no `{named[0]}` folder in {where}")
    return p


def _opt(argv: list[str], name: str) -> tuple[str | None, list[str]]:
    for i, a in enumerate(argv):
        if a == name and i + 1 < len(argv):
            return argv[i + 1], argv[:i] + argv[i + 2:]
        if a.startswith(name + "="):
            return a.split("=", 1)[1], argv[:i] + argv[i + 1:]
    return None, argv


def _usage() -> int:
    print(__doc__.strip(), file=sys.stderr)
    return 2


def main(argv: list[str]) -> int:
    try:
        return _main(argv)
    except NotSetUp as e:
        print(f"FAIL  {e}", file=sys.stderr)
        return 2


def _main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] not in ("copy", "verify", "show"):
        return _usage()
    cmd, rest = argv[1], argv[2:]
    binding, rest = _opt(rest, "--binding")
    out, rest = _opt(rest, "--out")
    at, rest = _opt(rest, "--at")
    if any(a.startswith("--") for a in rest):
        return _usage()

    if cmd == "verify":
        if not rest:
            return _usage()
        ok = True
        for arg in rest:
            copy_s, _, source_s = arg.partition("=")
            copy = _path(copy_s)
            if not copy.is_file():
                print(f"{copy} is not a file", file=sys.stderr)
                return 2
            source = _path(source_s) if source_s else None
            if source is not None and not source.is_file():
                print(f"{source} is not a file", file=sys.stderr)
                return 2
            v = verify(copy, source)
            ok &= v.ok
            print("\n".join(("PASS  " if v.ok else "FAIL  ") + line for line in v.lines))
        return 0 if ok else 1

    if binding is None:
        print("copy and show need --binding <file>: the binding names what is stripped", file=sys.stderr)
        return 2
    try:
        rules = read_rules(Path(binding))
    except (BindingError, OSError) as e:
        print(e, file=sys.stderr)
        return 2

    if cmd == "show":
        if len(rest) != 1 or not _path(rest[0]).is_file():
            return _usage()
        _, removed = strip(_path(rest[0]).read_text(), rules)
        print("\n".join(removed) if removed else "nothing the binding names is present")
        return 0

    if out is None or not rest:
        return _usage()
    frozen_at = at or datetime.now().astimezone().isoformat(timespec="seconds")
    pairs = []
    for arg in rest:
        src_s, sep, sid = arg.partition("=")
        src = _path(src_s)
        if not sep or not sid or not src.is_file():
            print(f"expected <source.md>=<source-id> naming a file, got {arg!r}", file=sys.stderr)
            return 2
        if is_frozen(src.read_text()):
            print(AlreadyFrozen(f"{src} is already a frozen copy: forward it byte for byte, "
                                "never re-freeze it (handoff contract § 10)"), file=sys.stderr)
            return 2
        pairs.append((src, sid))
    print(MANIFEST_HEADER)
    for src, sid in pairs:
        print(freeze(src, sid, rules, Path(out), frozen_at).manifest_row())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
