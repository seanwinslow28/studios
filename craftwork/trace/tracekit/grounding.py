"""Write each artifact's `grounding:` line from the pass's reads, so no seat declares it (SWCB #260).

Ruled by Sean on SWCB #260 (2026-10-22). Two repairs on mc-eng-001 (pass-10, pass-33)
carried `grounding: full` in their header with no library file opened, the line copied
from the draft they repaired. Under SWCB #251 that `full` is right: a repair that opens
nothing keeps its draft's reads, along the artifact's own revision chain. What was wrong
is who wrote it. So the seat leaves `grounding: pending`, and after the pass the
coordinator runs this script, which writes the line from what the record shows:

- `full`: this pass's `## Corpus read` names a library file, or an earlier revision of
  the same artifact was written by a pass whose list did (the same chain rung-0 line 5
  follows, so the line and the check never disagree);
- `manifest-only`: nothing on the chain read the library, and the library is not on
  this machine;
- `none`: nothing on the chain read the library, though it was here to read.

The pass's `## Corpus read` must be what `reads.py` prints for its raw log, plus any
call it could not judge that the coordinator confirmed, or a dated correction of it:
a list that differs from the log otherwise, uncorrected, is refused, never written from. The line is written before the outputs are hashed: an output whose
recorded hash still matches the file is refused, since writing it would break the hash.
Only the `grounding:` value in the file's frontmatter changes; a comment after it stays.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .checker import _prior_reads, _same_file
from .engagement import Engagement, Record
from .reads import read_logs
from .studio import PROFILE_ENV, find_profile

__all__ = ["VALUES", "PENDING", "Stamp", "GroundingError", "library_dir", "expected", "stamp"]

VALUES = ("full", "manifest-only", "none")
PENDING = "pending"   # what a seat leaves in the header; the checker fails it if it survives the pass

_FRONTMATTER = re.compile(r"\A---\n(.*?\n)---\n", re.S)
_LINE = re.compile(r"^(grounding:[ \t]*)([^\s#]*)", re.M)
_CORRECTED = re.compile(r"^\*\*Correction, \d{4}-\d{2}-\d{2}\*\*", re.M)


class GroundingError(Exception):
    """The record cannot be written from: no such pass, a log reads.py cannot read, or a list that differs from it."""


@dataclass
class Stamp:
    path: str                 # the output, relative to the engagement folder
    was: Optional[str]        # the value the file held, or None when it has no `grounding:` line
    value: str = ""           # what the reads make it
    basis: str = ""           # why, in plain words
    written: bool = False
    refused: str = ""         # why the file was left as it is

    @property
    def line(self) -> str:
        if self.was is None:
            return f"{self.path}: no grounding: line, left as it is"
        if self.refused:
            return f"{self.path}: grounding: {self.was} left; it should read {self.value} ({self.basis}); {self.refused}"
        if self.written or self.was == self.value:
            return f"{self.path}: grounding: {self.value} ({self.basis}); {'written' if self.written else 'already so'}"
        return f"{self.path}: grounding: {self.was} should read {self.value} ({self.basis})"


def library_dir(eng: Engagement) -> Optional[Path]:
    """The studio's private library on this machine: `<team>/corpus` beside the team's trace profile."""
    profile = find_profile(eng.root) or (Path(os.environ[PROFILE_ENV]) if os.environ.get(PROFILE_ENV) else None)
    return profile.resolve().parent.parent / "corpus" if profile is not None else None


def _corpus(reads) -> list[str]:
    return sorted(x for x in reads if "corpus/" in x)


def expected(record: Record, path: str, prior: dict, prior_by: dict, library_present: bool) -> tuple[str, str]:
    """The value an output's `grounding:` line takes, and the reason in plain words."""
    if _corpus(record.corpus_read):
        return "full", "this pass's reads"
    if _corpus(prior.get(record.pass_id, {}).get(path, set())):
        by = sorted(prior_by.get(record.pass_id, {}).get(path, set()))
        return "full", f"the reads of {', '.join(by)}, an earlier revision of this artifact"
    if not library_present:
        return "manifest-only", "no library on this machine"
    return "none", "no library file read by this pass or an earlier revision of this artifact"


def _check_list(eng: Engagement, record: Record, cwd: Optional[str]) -> None:
    """Refuse a `## Corpus read` that is not reads.py's output for the pass's own log, unless corrected."""
    if _CORRECTED.search(record.file.read_text(encoding="utf-8")):
        return   # a dated correction says what the transcript shows; the checker reads it the same way
    log = eng.resolve(record.raw_log) if record.raw_log else None
    if log is None:
        raise GroundingError(f"{record.pass_id}: its raw_log {record.raw_log or '(none)'} is not on this machine, "
                             f"so its reads cannot be checked against it")
    reads = read_logs(log, cwd)
    if reads.error:
        raise GroundingError(f"{record.pass_id}: {reads.error}")
    listed, logged = _corpus(record.corpus_read), _corpus(reads.paths)
    missing = [x for x in logged if not any(_same_file(x, y) for y in listed)]
    # a call reads.py could not judge, confirmed in the transcript by the coordinator, is listed with its note
    extra = [x for x in listed if not any(_same_file(x, y) for y in logged)
             and not any(x.split("corpus/", 1)[-1] in u for u in reads.unjudged)]
    if missing or extra:
        said = "; ".join(filter(None, [f"the log shows {', '.join(missing)}" if missing else "",
                                       f"the log does not show {', '.join(extra)}" if extra else ""]))
        raise GroundingError(f"{record.pass_id}: its ## Corpus read is not what reads.py prints for "
                             f"{record.raw_log} ({said}); paste reads.py's output, or correct it under a dated "
                             f"**Correction** paragraph, before the line is written")


def stamp(eng: Engagement, pass_id: str, *, write: bool = True, library: Optional[Path] = None,
          cwd: Optional[str] = None) -> list[Stamp]:
    """Write (or, with write=False, only compute) the `grounding:` line of every file the pass output."""
    record = eng.by_id.get(pass_id)
    if record is None:
        raise GroundingError(f"no record for {pass_id} in {eng.root}")
    if not record.artifact_outputs:
        raise GroundingError(f"{pass_id}'s record lists no output paths yet; list them, then write the line, "
                             f"then take their hashes")
    _check_list(eng, record, cwd)
    lib = library if library is not None else library_dir(eng)
    present = lib is not None and lib.is_dir()
    prior, prior_by = _prior_reads(eng)
    out: list[Stamp] = []
    for o in record.artifact_outputs:
        p = eng.resolve(o.path)
        text = p.read_text(encoding="utf-8") if p is not None and p.is_file() else None
        fm = _FRONTMATTER.match(text) if text is not None else None
        m = _LINE.search(fm.group(1)) if fm else None
        if m is None:
            out.append(Stamp(o.path, None))
            continue
        s = Stamp(o.path, m.group(2))
        s.value, s.basis = expected(record, o.path, prior, prior_by, present)
        if s.was == s.value or not write:
            out.append(s)
            continue
        state = eng.output_state(o)
        if state == "current":
            s.refused = "its hash is already in the record: write the line before taking the outputs' hashes"
        elif state == "superseded":
            s.refused = "a later revision is on disk, so the file is no longer this pass's"
        else:
            start = fm.start(1) + m.start(2)
            p.write_text(text[:start] + s.value + text[fm.start(1) + m.end(2):], encoding="utf-8")
            s.written = True
        out.append(s)
    return out
