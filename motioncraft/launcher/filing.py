#!/usr/bin/env python3
"""Filing a pass's logs: embedded images and sound stripped, the employer folders replaced by a placeholder.

    filing.py <engagement> [--pass pass-NN]... [--check]

A pass that opens an image carries it whole in its log: Claude Code writes the
picture it read into the tool result (as a JPEG it may have shrunk, twice on the
line), and Codex writes each image it viewed into the tool's output as a data URL.
The ledger is a git repo, so nothing visual may be committed (the frame-log ruling,
SWCB #240). And the doorway's locks, and any log that echoes one, name the folders
every pass is denied, the employer's among them, which no repo but the work lane may
hold (Sean, 2026-10-20, on SWCB #245). So before a pass's logs are committed, this
step rewrites them in place:

- every embedded image or sound becomes one line: `motioncraft-stripped`, its type,
  the sha256 and size of the copy removed, the path the log shows for it, and, when
  that path is a file in the media folder, the file's own sha256 and size; a path
  outside the media folder is marked not kept, and a copy with no path shown keeps
  its sha256 alone. No unstripped copy is kept: the frames live in the media folder;
- every path on the machine's employer-path list, and its `~`, `file://` and
  percent-encoded forms, becomes `<employer folder>`, matched only as a whole path;
- a doorway lock or script copy this changes gets `filed_sha256` beside the sha256
  its call log recorded, so the record still says what ran and what was filed.

Then it reads every file again and refuses (exit 1, each survivor named) if any image,
sound or employer path is left. Motioncraft's own check: the shared trace kit is not
changed, and its rung-0 line 11 reads the stripped logs as it read the originals.
The launcher runs this at the end of every pass (`seat.py launch`); run it by hand on
logs filed before it existed. Built on the Motioncraft build map's SWCB #245.
"""
from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import json
import os
import re
import sys
import urllib.parse
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

HERE = Path(__file__).resolve().parent
STRIPPED = "motioncraft-stripped"
EMPLOYER = "<employer folder>"
DATA_URL = re.compile(r"data:((?:image|audio|video)/[\w.+-]+);base64,([A-Za-z0-9+/=\s]*)")
# Long base64 runs in a file that is not JSON (a stray log line, an HTML page), checked by what they decode to.
BASE64_RUN = re.compile(r"[A-Za-z0-9+/]{2000,}={0,2}")
MAGIC = (b"\x89PNG", b"\xff\xd8\xff", b"GIF8", b"RIFF", b"ID3", b"OggS", b"fLaC", b"\x1aE\xdf\xa3")


def _seat():
    sys.path.insert(0, str(HERE))
    import seat  # noqa: E402  the launcher's own rules: the employer-path list, the media folder
    return seat


def decode(data: str) -> bytes:
    try:
        return base64.b64decode("".join(data.split()), validate=False)
    except (binascii.Error, ValueError):
        return b""


def looks_like_media(data: str) -> bool:
    return decode(data[:64])[:4].startswith(MAGIC) or decode(data[:64])[4:8] == b"ftyp"


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


class Stripper:
    """Strips the media out of one log's JSON lines, knowing the paths the log names for them."""

    def __init__(self, media_root: str) -> None:
        self.media_root = os.path.realpath(media_root) if media_root else ""
        self.paths: Dict[str, str] = {}   # a Claude tool_use id -> the path its input names
        self.viewed: List[str] = []       # Codex: the paths its image views named, in order, not yet matched
        self.count = 0

    def note(self, mime: str, data: str, path: Optional[str]) -> str:
        raw = decode(data)
        bits = [STRIPPED, mime or "media", f"sha256 {sha256_bytes(raw)}", f"{len(raw)} bytes"]
        if path:
            real = os.path.realpath(path)
            bits.append(f"path {path}")
            inside = self.media_root and (real == self.media_root or real.startswith(self.media_root + "/"))
            if inside and os.path.isfile(real):
                with open(real, "rb") as f:
                    bits.append(f"file sha256 {sha256_bytes(f.read())}, {os.path.getsize(real)} bytes, in the media folder")
            elif inside:
                bits.append("in the media folder, file not found at filing")
            else:
                bits.append("not kept (outside the media folder)")
        else:
            bits.append("no path shown")
        self.count += 1
        return " · ".join(bits)

    def learn(self, obj) -> None:
        """Remember the paths a line names before the media that follows it."""
        if not isinstance(obj, dict):
            return
        msg = obj.get("message") if isinstance(obj.get("message"), dict) else None
        for block in (msg or {}).get("content") or []:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                inp = block.get("input") or {}
                path = inp.get("file_path") or inp.get("path")
                if isinstance(path, str):
                    self.paths[block.get("id", "")] = path
        payload = obj.get("payload") if isinstance(obj.get("payload"), dict) else {}
        item = payload.get("item") if isinstance(payload.get("item"), dict) else {}
        if item.get("type") == "ImageView" and isinstance(item.get("path"), str):
            p = item["path"]
            self.viewed.append(urllib.parse.unquote(p[7:]) if p.startswith("file://") else p)

    def strip(self, obj, path: Optional[str] = None):
        """The object with every embedded media string replaced by its note, in the same shape."""
        if isinstance(obj, dict):
            if obj.get("type") == "tool_result" and obj.get("tool_use_id") in self.paths:
                path = self.paths[obj["tool_use_id"]]
            out = {}
            for k, v in obj.items():
                if k == "data" and obj.get("type") == "base64" and isinstance(v, str) and not v.startswith(STRIPPED):
                    out[k] = self.note(str(obj.get("media_type", "")), v, path)
                elif k == "base64" and isinstance(v, str) and looks_like_media(v):
                    out[k] = self.note(str(obj.get("type", "")), v, path)
                else:
                    out[k] = self.strip(v, path)
            return out
        if isinstance(obj, list):
            return [self.strip(v, path) for v in obj]
        if isinstance(obj, str) and obj.startswith("data:"):
            m = DATA_URL.match(obj)
            if m:
                return self.note(m.group(1), m.group(2), path or (self.viewed.pop(0) if self.viewed else None))
        return obj

    def line(self, text: str) -> str:
        try:
            obj = json.loads(text)
        except ValueError:
            return text
        self.learn(obj)
        if "base64" not in text and "data:" not in text:
            return text
        # A Claude tool result names its tool_use; the same line's top-level copy belongs to it too.
        tid = next((b.get("tool_use_id") for b in ((obj.get("message") or {}).get("content") or [])
                    if isinstance(b, dict) and b.get("type") == "tool_result"), None) if isinstance(obj, dict) else None
        before = self.count
        new = self.strip(obj, self.paths.get(tid) if tid else None)
        return text if self.count == before else json.dumps(new, ensure_ascii=False, separators=(",", ":"))


def employer_forms(paths: Iterable[str]) -> List[re.Pattern]:
    """Each employer folder as a whole path, in the forms a log may print it."""
    home = os.path.expanduser("~")
    forms = set()
    for p in paths:
        p = p.rstrip("/")
        if not p:
            continue
        forms |= {p, urllib.parse.quote(p), json.dumps(p)[1:-1]}
        if p.startswith(home + "/"):
            forms.add("~" + p[len(home):])
    # longest first, so a folder inside another is replaced whole; a match ends the path or continues it with /
    return [re.compile(re.escape(f) + r"(?=$|[/\"'\s)\],;:<>|\\]|%2F)") for f in sorted(forms, key=len, reverse=True)]


def redact(text: str, forms: List[re.Pattern]) -> str:
    for f in forms:
        text = f.sub(EMPLOYER, text)
    return text


def is_text(p: Path) -> bool:
    """A file the step can read and rewrite: UTF-8 with no NUL byte. Anything else is refused, never committed."""
    try:
        b = p.read_bytes()
        b.decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return b"\x00" not in b


def media_in(obj) -> List[str]:
    """Embedded media still in a parsed JSON value."""
    found = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "data" and obj.get("type") == "base64" and isinstance(v, str) and not v.startswith(STRIPPED) and len(v) > 64:
                found.append("a base64 media block")
            elif k == "base64" and isinstance(v, str) and looks_like_media(v):
                found.append("a base64 media block")
            else:
                found += media_in(v)
    elif isinstance(obj, list):
        for v in obj:
            found += media_in(v)
    elif isinstance(obj, str):
        m = DATA_URL.search(obj)
        if m and len(m.group(2)) > 64:
            found.append(f"a {m.group(1)} data URL")
    return found


def survivors(p: Path, forms: List[re.Pattern]) -> List[str]:
    """What is still in a filed file that must not be: media, or an employer path."""
    found = []
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return [f"unreadable: {e}"]
    for line in (text.split("\n") if p.suffix == ".jsonl" else [text]):
        try:
            found += media_in(json.loads(line))
        except ValueError:
            m = DATA_URL.search(line)
            if m and len(m.group(2)) > 64:
                found.append(f"a {m.group(1)} data URL")
    for m in BASE64_RUN.finditer(text):
        if looks_like_media(m.group(0)):
            found.append("a long base64 run that decodes to media")
    if any(f.search(text) for f in forms):
        found.append("a path from the employer-path list")
    return found


def pass_files(logs: Path, passes: List[str]) -> List[Path]:
    """Every file under trace/logs the step files: one pass's (pass-NN.*, its folders), or all of them."""
    out = []
    for p in sorted(logs.rglob("*")):
        if not p.is_file() or p.name.startswith("."):
            continue
        top = p.relative_to(logs).parts[0]
        if passes and not any(top == pid or top.startswith(pid + ".") for pid in passes):
            continue
        out.append(p)
    return out


def write_if_changed(p: Path, text: str, original: str) -> bool:
    if text == original:
        return False
    tmp = p.with_name(f".{p.name}.filing")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, p)
    return True


def note_filed_hashes(apps_log: Path) -> bool:
    """Beside each lock and script copy's recorded sha256, the filed copy's, where filing changed it."""
    lines, changed = apps_log.read_text(encoding="utf-8").splitlines(), False
    out = []
    for line in lines:
        try:
            entry = json.loads(line)
        except ValueError:
            out.append(line)
            continue
        for key, field in (("lock", "path"), ("script", "copy")):
            rec = entry.get(key)
            if isinstance(rec, dict) and rec.get("sha256") and os.path.isfile(str(rec.get(field, ""))):
                now = sha256_bytes(Path(rec[field]).read_bytes())
                if now != rec["sha256"] and rec.get("filed_sha256") != now:
                    rec["filed_sha256"], changed = now, True
        out.append(json.dumps(entry))
    if changed:
        apps_log.write_text("\n".join(out) + "\n", encoding="utf-8")
    return changed


def file_logs(logs: Path, passes: List[str], media_root: str, employer: List[str], check_only: bool = False) -> Dict:
    """Strip and redact the logs, then read them again. `survivors` empty means they may be committed."""
    forms = employer_forms(employer)
    files = pass_files(logs, passes)
    stripped, redacted = 0, []
    if not check_only:
        # Locks and script copies first, so a call log can then record their filed hashes; then everything else.
        apps_logs = [p for p in files if p.name.endswith(".apps.jsonl")]
        for p in [f for f in files if f not in apps_logs] + apps_logs:
            if not is_text(p):
                continue
            noted = p.name.endswith(".apps.jsonl") and note_filed_hashes(p)
            original = p.read_text(encoding="utf-8")
            text = original
            if p.suffix in (".jsonl", ".json"):
                s = Stripper(media_root)
                text = "\n".join(s.line(l) for l in text.split("\n")) if p.suffix == ".jsonl" else s.line(text)
                stripped += s.count
            text = redact(text, forms)
            if write_if_changed(p, text, original) or noted:
                redacted.append(str(p.relative_to(logs)))
    left = {str(p.relative_to(logs)): s for p in files if is_text(p) for s in [survivors(p, forms)] if s}
    binary = [str(p.relative_to(logs)) for p in files if not is_text(p)]
    return {"files": len(files), "media_stripped": stripped, "rewritten": redacted, "survivors": left,
            "not_read": binary}


def setting() -> Tuple[str, List[str]]:
    """This machine's media folder and employer-path list, from the launcher's own settings."""
    seat = _seat()
    media = seat.load_folders(seat.STUDIOS).resolve("media", "")
    return (str(media) if media else ""), seat.employer_paths()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("engagement")
    ap.add_argument("--pass", dest="passes", action="append", default=[], help="pass-NN; repeat it; every pass by default")
    ap.add_argument("--check", action="store_true", help="change nothing; report what would not be filed")
    a = ap.parse_args()
    logs = Path(a.engagement).resolve() / "trace" / "logs"
    if not logs.is_dir():
        sys.exit(f"filing.py: no trace/logs under {a.engagement}")
    media, employer = setting()
    if not employer:
        sys.exit("filing.py: this machine has no employer-path list, so no path can be checked; set it up first")
    res = file_logs(logs, a.passes, media, employer, check_only=a.check)
    print(f"{res['files']} file(s); {res['media_stripped']} embedded media stripped; {len(res['rewritten'])} rewritten")
    for p in res["rewritten"]:
        print(f"  filed: {p}")
    for p in res["not_read"]:
        print(f"  not a text file, left as it is: {p}")
    for p, why in res["survivors"].items():
        print(f"REFUSED: {p}: {'; '.join(sorted(set(why)))}")
    sys.exit(1 if res["survivors"] or res["not_read"] else 0)


if __name__ == "__main__":
    main()
