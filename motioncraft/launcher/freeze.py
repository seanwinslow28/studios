#!/usr/bin/env python3
"""Freezing version folders: their state read from the mode bits, the lock, and the sweep over a media project.

    freeze.py sweep <project> [--json]                  every version folder in the project: its three files, its
                                                        checksums re-taken, and what is still writable; exit 1 on any
    freeze.py lock  <project> [--version STAGE/NAME]...  lock every writable version whose checksums verify (all of
                                                        them, or the ones named); a version refused is named and left

`<project>` is the project folder, or `media:<film>/<project>` read from this machine's named folders
(folders.local). A version folder is any folder directly inside `story/`, `appearance/`, `motion/`,
`finish/` or `approved/` (the source contract, § 1).

The source contract's § 4: when a version is finished, `checksums.sha256` is written last, then the
folder is made read-only, files and folders (`chmod -R a-w`), and a frozen version is never unfrozen.
On the first film only the approved copies were ever locked: nine superseded versions (162 folders,
3,888 files) and 40 folders inside four approved copies stayed writable, and the Close checklist,
reading only `approved/`, never saw it (mc-self-001, SC9; SWCB #258). An approved copy made with `cp`
keeps its files' read-only bits and gets fresh writable folders, which is how those 40 came about.
So the launcher now freezes every whole version a pass made when the pass ends (`seat.py launch`,
through `state`, `gaps` and `lock` below), and the Close checklist sweeps every version folder in the
project with `sweep`, approved copies and superseded versions alike.

Everything here reads `st_mode`. The Codex reviewer's note on the self-check (N1): `os.access` asks
whether this process may write, and from inside a read-only sandbox that reads zero writable paths
whatever the bits say; the mode bits are the fact. Links are never followed: a link inside a version
is named as a gap, since what it points at is not frozen with the folder.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Tuple

HERE = Path(__file__).resolve().parent
STAGES = ("story", "appearance", "motion", "finish", "approved")
VERSION_FILES = ("pointer.txt", "manifest.md", "checksums.sha256")
WRITE = 0o222
SUM_LINE = re.compile(r"^([0-9a-fA-F]{64})\s+\*?(.+?)\s*$")


def entries(folder: Path) -> Iterator[Tuple[str, Path, os.stat_result]]:
    """The folder itself (as `.`), then every folder and file under it, by relative POSIX path; links never followed."""
    yield ".", folder, os.lstat(folder)
    for here, dirs, files in os.walk(folder, followlinks=False):
        for n in sorted(dirs) + sorted(files):
            p = Path(here) / n
            yield p.relative_to(folder).as_posix(), p, os.lstat(p)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify(folder: Path, sums: Path) -> Dict:
    """`checksums.sha256` re-taken, in the form `shasum -a 256 -c` reads: what is listed, what differs, what is
    gone, and every other file in the folder the list leaves out (the list itself excepted)."""
    listed: Dict[str, str] = {}
    for line in sums.read_text(encoding="utf-8", errors="replace").splitlines():
        m = SUM_LINE.match(line.strip())
        if m:
            listed[m.group(2)] = m.group(1).lower()
    failed, missing = [], []
    for rel, want in listed.items():
        p = folder / rel
        if not p.is_file() or os.path.islink(p):
            missing.append(rel)
        elif sha256(p) != want:
            failed.append(rel)
    lowered = {rel.lower() for rel in listed}
    own = sums.relative_to(folder).as_posix()
    unlisted = sorted(rel for rel, p, st in entries(folder)
                      if stat.S_ISREG(st.st_mode) and rel != own and rel not in listed and rel.lower() not in lowered)
    return {"listed": len(listed), "failed": sorted(failed), "missing": sorted(missing), "unlisted": unlisted}


def state(folder: Path) -> Dict:
    """One version folder, read from disk: the three files it lacks, what is writable by mode bits, its links,
    and its checksums re-taken (None when it has no list)."""
    top = {n.lower(): n for n in os.listdir(folder) if (folder / n).is_file()}  # the October versions' POINTER.txt counts
    missing = [f for f in VERSION_FILES if f not in top]
    wd = wf = 0
    links: List[str] = []
    for rel, p, st in entries(folder):
        if stat.S_ISLNK(st.st_mode):
            links.append(rel)
        elif stat.S_ISDIR(st.st_mode):
            wd += bool(st.st_mode & WRITE)
        else:
            wf += bool(st.st_mode & WRITE)
    sums = folder / top["checksums.sha256"] if "checksums.sha256" in top else None
    return {"version": folder.name, "missing": missing, "writable_dirs": wd, "writable_files": wf,
            "links": links, "checksums": verify(folder, sums) if sums else None}


def gaps(st: Dict) -> List[str]:
    """Why this version is not whole, each in one sentence; empty when it may be frozen as it stands."""
    out = [f"lacks {f}" for f in st["missing"]]
    c = st["checksums"]
    if c:
        bad = [f"{f} differs" for f in c["failed"]] + [f"{f} missing" for f in c["missing"]]
        if bad:
            out.append(f"checksums.sha256 does not verify ({'; '.join(bad)})")
        if c["unlisted"]:
            out.append(f"holds files not in checksums.sha256 ({', '.join(c['unlisted'])})")
    if st["links"]:
        out.append(f"holds a link ({', '.join(st['links'])})")
    return out


def verifies(st: Dict) -> bool:
    """The checksums list is there, every file it names is there and matches, and nothing is a link."""
    c = st["checksums"]
    return bool(c) and not c["failed"] and not c["missing"] and not st["links"]


def is_locked(st: Dict) -> bool:
    return st["writable_dirs"] == 0 and st["writable_files"] == 0


def lock(folder: Path) -> Dict:
    """`chmod -R a-w`, in Python: the write bits off on the folder and everything in it, links left alone, other
    bits kept. Then read again: what is still writable, and any path the bits could not be changed on."""
    errors: List[str] = []
    for rel, p, st in entries(folder):
        if stat.S_ISLNK(st.st_mode):
            continue
        mode = stat.S_IMODE(st.st_mode)
        if mode & WRITE:
            try:
                os.chmod(p, mode & ~WRITE)
            except OSError as e:
                errors.append(f"{rel}: {e.strerror}")
    after = state(folder)
    return {"writable_dirs": after["writable_dirs"], "writable_files": after["writable_files"], "errors": errors}


def versions_in(project: Path) -> List[Path]:
    """Every version folder in a media project: each folder directly inside a stage folder, in stage order."""
    out: List[Path] = []
    for stage in STAGES:
        d = project / stage
        if d.is_dir():
            out += [p for p in sorted(d.iterdir()) if p.is_dir() and not p.is_symlink()]
    return out


def sweep(project: Path) -> List[Dict]:
    rows = []
    for v in versions_in(project):
        st = state(v)
        st["version"] = f"{v.parent.name}/{v.name}"
        st["locked"] = is_locked(st)
        st["gaps"] = gaps(st)
        rows.append(st)
    return rows


def clean(row: Dict) -> bool:
    """What the Close sweep passes: locked, and its checksums verify."""
    return row["locked"] and verifies(row)


def describe(row: Dict) -> str:
    files = f"{3 - len(row['missing'])}/3"
    where = "locked" if row["locked"] else f"{row['writable_dirs']} dirs, {row['writable_files']} files writable"
    c = row["checksums"]
    if c is None:
        sums = "no checksums.sha256"
    elif c["failed"] or c["missing"]:
        sums = "checksums fail: " + "; ".join([f"{f} differs" for f in c["failed"]] + [f"{f} missing" for f in c["missing"]])
    else:
        sums = f"{c['listed']} checksums ok" + (f", {len(c['unlisted'])} unlisted" if c["unlisted"] else "")
    notes = [g for g in row["gaps"] if not g.startswith("checksums.sha256 does not verify")]
    return f"{row['version']:<48} {files:>4}  {where:<30} {sums}" + (f"  · {'; '.join(notes)}" if notes else "")


def die(msg: str, code: int = 2) -> None:
    print(f"freeze.py: {msg}", file=sys.stderr)
    sys.exit(code)


def project_path(arg: str) -> Path:
    """A folder, or a `media:<path>` name resolved through this machine's named folders."""
    if ":" in arg and not arg.startswith(("/", ".", "~")):
        sys.path.insert(0, str(HERE))
        import seat  # noqa: E402  the launcher's own resolution of named folders

        named = seat.split_named(arg)
        if not named:
            die(f"{arg} is not a folder path or a name:<path>")
        where = seat.load_folders(seat.STUDIOS).resolve(*named)
        if where is None:
            die(f"`{named[0]}` is not set up on this machine (folders.local)")
        if not where.is_dir():
            die(f"{arg} is not a folder on this machine ({where})")
        return where
    p = Path(os.path.expanduser(arg))
    if not p.is_dir():
        die(f"{arg} is not a folder")
    return p


def cmd_sweep(a) -> None:
    project = project_path(a.project)
    rows = sweep(project)
    if a.json:
        print(json.dumps(rows, indent=1))
    else:
        print(f"{'version':<48} files  state{'':<26}checksums")
        for row in rows:
            print(describe(row))
        writable = sum(not r["locked"] for r in rows)
        failing = sum(not verifies(r) for r in rows)
        print(f"{writable} of {len(rows)} version folders writable; {failing} with checksums that do not verify")
    sys.exit(0 if all(clean(r) for r in rows) else 1)


def cmd_lock(a) -> None:
    project = project_path(a.project)
    chosen = versions_in(project)
    if a.versions:
        by = {f"{v.parent.name}/{v.name}": v for v in chosen}
        for name in a.versions:
            if name not in by:
                die(f"no version folder {name} in {project}")
        chosen = [by[n] for n in a.versions]
    bad = 0
    for v in chosen:
        name = f"{v.parent.name}/{v.name}"
        st = state(v)
        notes = [g for g in gaps(st) if not g.startswith("checksums.sha256 does not verify") and not g.startswith("holds a link")]
        tail = f"  · {'; '.join(notes)}" if notes else ""
        if is_locked(st):
            print(f"{name:<48} already locked{tail}")
            continue
        if not verifies(st):
            why = [g for g in gaps(st) if g.startswith(("checksums.sha256 does not verify", "holds a link"))]
            if st["checksums"] is None:
                why = ["lacks checksums.sha256"]
            print(f"{name:<48} refused: {'; '.join(why)}; left as it is{tail}")
            bad += 1
            continue
        res = lock(v)
        if res["errors"] or res["writable_dirs"] or res["writable_files"]:
            left = f"{res['writable_dirs']} dirs, {res['writable_files']} files still writable"
            print(f"{name:<48} could not lock: {left}; {'; '.join(res['errors'])}{tail}")
            bad += 1
        else:
            print(f"{name:<48} locked ({st['writable_dirs']} dirs, {st['writable_files']} files were writable; "
                  f"{st['checksums']['listed']} checksums ok){tail}")
    sys.exit(1 if bad else 0)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sweep", help="every version folder in the project, by mode bits; exit 1 on any writable or failing")
    s.add_argument("project")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_sweep)
    k = sub.add_parser("lock", help="lock every writable version whose checksums verify; refuse and name the rest")
    k.add_argument("project")
    k.add_argument("--version", dest="versions", action="append", default=[], help="STAGE/NAME; repeat it; all by default")
    k.set_defaults(fn=cmd_lock)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
