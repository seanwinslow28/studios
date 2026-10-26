#!/usr/bin/env python3
"""The Higgsfield doorway: Art's images and the Animator's video, one take of one approved entry, metered in credits.

    higgsfield.py take   --context <eng>/trace/logs/pass-NN.context.json --entry IM1
                         --out appearance/<artifact>-vNN-<date>/<name>.png      (the launcher, for a pass's request)
    higgsfield.py settle --context <eng>/trace/logs/pass-NN.context.json --job <id>
                         --out appearance/<artifact>-vNN-<date>/<name>.png      (file a job this doorway made, unfiled)
    higgsfield.py status --context <eng>/trace/logs/pass-NN.context.json       (the approved list, takes and spend)

Art operates Higgsfield's image generation and the Animator its video, each into its own
version folders; no other seat calls Higgsfield (Sean's pick at mc-eng-002's Open,
2026-10-24, "Doorway ticket (Recommended)": SWCB #271). A pass never runs this file, or the
`higgsfield` command line, itself: inside its sandbox it has no network and cannot read the
sign-in (`~/.config/higgsfield/`, on every pass's credential wall). It asks from its shell,
`apps.py ask higgsfield --entry IM1 --out <file>`, and the launcher, which supervises the pass
from outside its sandbox, runs `take` for it, as it runs Blender for it (launcher/apps.py).
That way works on either vendor, which the image and sound doorways' way does not: the
Animator runs on Codex, whose sandbox has no rule that lets one command out. So this file
holds the terms for the call, on the sound doorway's pattern (launcher/sound.py):

- the context must sit in its engagement's `trace/logs/` and say the pass may use Higgsfield:
  a drafting Art pass for images, a drafting Animator pass for video (`higgsfield` in
  bench/toolbelts.toml, which only those two seats may carry), on either vendor;
- Sean's intended-use approval (never-do 6), recorded with Higgsfield's data-use and training
  settings in the ledger's setup record for this job: `tool: higgsfield`, with the brief's id in
  its `engagements:` list. Another job's record never covers this one, and no call is made
  before the one says approved. A record that another approved record for the job names in its
  `supersedes:` is skipped (mc-setup-027 over mc-setup-025); two still standing are Sean's to
  settle;
- the entry comes from the newest list of the pass's kind that Sean approved in one decision:
  a `higgsfield.json` in the media project's `approved/<version-id>/`, named by an approvals
  entry with decision approved whose sha256 still matches the folder. The pass names an entry
  by its id and nothing else: the model, the prompt and the settings are the list's, so a
  reworded prompt is a new list for Sean, never a take;
- nothing leaves the machine but the entry's text and settings, and, only where the job's
  setup record says `uploads: approved-media`, the files its entries name. A reference is an
  earlier take of this doorway's own in this job, by its Higgsfield job id (`job:<id>`), which
  is already on Higgsfield's side, or, under that field, an image in one of this job's approved
  copies, by its path from the media project (`approved/<version-id>/<file>`). At the take each
  such file must exist, be a regular file reached through no link, sit in a copy named by an
  approvals entry with decision approved whose sha256 still matches the folder, be listed in
  that copy's `checksums.sha256`, and match its listed sha256 byte for byte. The bytes checked
  are copied to a private folder and uploaded from there (`upload create`), once each, after
  the model is known to take the field and before the take is priced. Without the field, a
  list naming a file is refused whole, as is any list naming a path outside `approved/`, a
  link, a URL or anything else;
- three takes per entry and wording, counted across the whole job from its logs;
- two caps, both in credits: the brief's `higgsfield_credits_cap` for the whole train, and the
  list's `ceiling_credits` for its test. Each take is priced first by Higgsfield's own estimate
  (`generate cost`), and refused before any call if it would take either past its cap or ask
  more than the account holds; that is a checkpoint for Sean. The take is then metered from the
  account's own balance, read before the call and again until it moves;
- the take is downloaded the moment it is ready (never-do 13) into a new file in a version
  folder the pass made in its own stage, with `<name>.higgsfield.json` beside it (the entry,
  the approval, each upload's path, sha256 and upload id, the job, the credits, the label
  "generated": never-do 8), both created
  relative to the version folder held open since the check, never through a link and never
  over a file already there. A file that came back but could not be filed is kept in the
  pass's scratch folder. Every call, refusals too, is logged to
  `trace/logs/pass-NN.higgsfield.jsonl`, and a job's line is written the moment Higgsfield
  takes it, so a call cut off mid-way still counts what it spent.

Written on SWCB #271 (2026-10-25), on the sound doorway's pattern. Uploads of approved media
added for mc-eng-003's generated route (mc-eng-003.d29, mc-setup-027, 2026-10-26).
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import seat  # noqa: E402  the launcher's own rules: the context, the stage folders, the allowlist
from image import CONTEXT_FILE, VERSION_DIR  # noqa: E402  the same names the image doorway holds
from sound import header, media_path  # noqa: E402  the same ledger readers the sound doorway uses
from tracekit.engagement import sha256_path  # noqa: E402  the approvals ledger's folder hash

KINDS = seat.HIGGSFIELD_SEATS  # art-pose-designer: image, animator: video
ENTRY_ID = {"image": re.compile(r"IM\d+"), "video": re.compile(r"VI\d+")}
SUFFIXES = {"image": (".png", ".jpg", ".webp"), "video": (".mp4",)}
TAKES_PER_ENTRY = 3
# A setup record of Higgsfield's data-use and training settings and Sean's intended-use approval (never-do 6) says
# `tool: higgsfield`, and covers only the jobs its `engagements:` names: mc-setup-023 covers mc-eng-002.
SETUP_TOOL = "higgsfield"
# A record that says `uploads: approved-media` lets its job's lists name files in the media project's approved/
# (mc-setup-027, for mc-eng-003). Without the field, no file is ever sent.
UPLOADS_FIELD, UPLOADS_ALLOWED = "uploads", "approved-media"
LIST_FILE = "higgsfield.json"
LIST_KEYS = {"test", "ceiling_credits", "entries"}
ENTRY_KEYS = {"id", "purpose", "model", "prompt", "params", "start_image", "end_image", "image_references"}
# The only media an entry may name: an earlier take of this doorway's own, by its job id, or, where the job's setup
# record allows uploads, an image in an approved copy, by its path from the media project (approved/<version>/...).
MEDIA_FLAGS = {"start_image": "--start-image", "end_image": "--end-image", "image_references": "--image-references"}
JOB_REF = re.compile(r"job:([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})")
# No part may start with a dot, so no `..`, no `.`, no hidden file; no colon, so no link and no `media:` path.
FILE_REF = re.compile(r"approved/(?:[A-Za-z0-9_-][A-Za-z0-9._-]{0,127}/){1,8}[A-Za-z0-9_-][A-Za-z0-9._-]{0,127}")
CHECKSUMS = "checksums.sha256"
MAX_UPLOAD_BYTES = 50_000_000
UPLOAD_TIMEOUT_S = 600
UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
SCALARS = {"string": (str,), "integer": (int,), "number": (int, float), "boolean": (bool,)}
# A setting's text value: a word, a ratio or a size. Nothing shaped like a path, a link or a flag goes to the CLI,
# which uploads any local file a media flag names.
SETTING = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:+-]{0,39}")
PARAM = re.compile(r"[a-z][a-z0-9_]{0,39}")
MAX_PROMPT_CHARS = 2000
MAX_REFS = 4
CLI_TIMEOUT_S = 120
WAIT_TIMEOUT_S = 1200  # a video job; the pass's own time still bounds the call
# The balance moves some seconds after a job ends, as ElevenLabs' count did (sound.py); read it until it moves.
METER_WAIT_S, METER_POLL_S = 90, 3
MAX_DOWNLOAD_BYTES = 2_000_000_000
LABEL = ("generated: Higgsfield ({model}) through motioncraft/launcher/higgsfield.py, from Sean's approved list "
         "{approval}, under {setup}")


class Refused(Exception):
    pass


def refuse(msg: str) -> None:
    sys.stderr.write(f"higgsfield.py: {msg}\n")
    sys.exit(1)


# --- the command line, from the launcher's side -----------------------------------------------

def cli_path() -> str:
    p = seat.toolbelts().get("apps", {}).get("higgsfield")
    if not p:
        raise Refused("the allowlist's [apps] names no `higgsfield`, the command line this doorway runs")
    return os.path.expanduser(str(p))


def cli(*args: str, timeout: float = CLI_TIMEOUT_S) -> Tuple[int, object, str]:
    """One call of the Higgsfield command line, its answer read as JSON. It runs from a new, empty folder, so no
    argument can name a file there, with telemetry and the update check off."""
    env = {k: os.environ[k] for k in ("HOME", "USER", "LOGNAME", "LANG") if k in os.environ}
    env.update(PATH="/usr/bin:/bin", HIGGSFIELD_DISABLE_TELEMETRY="1", HIGGSFIELD_NO_UPDATE_CHECK="1")
    with tempfile.TemporaryDirectory(prefix="mc-higgsfield-") as empty:
        try:
            r = subprocess.run([cli_path(), *args, "--json", "--no-color"], cwd=empty, env=env,
                               stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return 124, None, f"timed out after {round(timeout)} s"
    try:
        doc = json.loads(r.stdout) if r.stdout.strip() else None
    except ValueError:
        doc = None
    return r.returncode, doc, seat.one_line((r.stderr or r.stdout or "").strip(), 300)


def balance() -> Optional[float]:
    """The account's credits now, or None."""
    code, doc, _ = cli("account", "status")
    try:
        return float(doc["credits"]) if code == 0 else None  # type: ignore[index]
    except (TypeError, KeyError, ValueError):
        return None


def settled(before: Optional[float]) -> Optional[float]:
    """The balance once it has moved off `before`, or its last read when it has not in METER_WAIT_S."""
    deadline = time.time() + METER_WAIT_S
    while True:
        after = balance()
        if before is None or (after is not None and after != before) or time.time() >= deadline:
            return after
        time.sleep(METER_POLL_S)


def job_id(doc: object, keys: Tuple[str, ...] = ("id", "job_id")) -> Optional[str]:
    """The first job id in an answer: the job itself, a list of jobs, or a wrapper around them. With `keys`, the
    first id under those names, as an upload's id is read from `upload create`."""
    if isinstance(doc, dict):
        for k in keys:
            if isinstance(doc.get(k), str) and UUID.fullmatch(doc[k]):
                return doc[k]
        for v in doc.values():
            found = job_id(v, keys) if isinstance(v, (dict, list)) else None
            if found:
                return found
    elif isinstance(doc, list):
        for v in doc:
            # `generate create` answers with a bare list of job ids (mc-eng-002's first live call, 2026-10-25)
            found = v if isinstance(v, str) and UUID.fullmatch(v) else job_id(v, keys)
            if found:
                return found
    return None


def job_of(doc: object) -> Dict:
    """The job in a `generate wait` or `generate get` answer."""
    if isinstance(doc, list):
        doc = doc[0] if doc else {}
    if isinstance(doc, dict) and isinstance(doc.get("jobs"), list) and doc["jobs"]:
        doc = doc["jobs"][0]
    return doc if isinstance(doc, dict) else {}


def fetch(url: str) -> bytes:
    """The finished take, downloaded; only over https, and only a GET."""
    if urllib.parse.urlsplit(url).scheme != "https":
        raise OSError(f"the result is not an https link ({seat.one_line(url, 80)})")
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=300) as r:
        data = r.read(MAX_DOWNLOAD_BYTES + 1)
    if len(data) > MAX_DOWNLOAD_BYTES:
        raise OSError(f"the result is over {MAX_DOWNLOAD_BYTES} bytes")
    return data


def sniff(data: bytes) -> Optional[str]:
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return ".png"
    if data[:3] == b"\xff\xd8\xff":
        return ".jpg"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return ".webp"
    if data[4:8] == b"ftyp":
        return ".mp4"
    return None


# --- the approved list ------------------------------------------------------------------------

def check_entry(e: Dict, kind: str, uploads: bool = False) -> Optional[str]:
    """Why an entry in an approved list cannot be sent as it stands, or None. The model's own settings are
    checked again at the call, against what Higgsfield says the model takes, and a named file at the take."""
    want = {"image": "IM", "video": "VI"}[kind]
    if not isinstance(e, dict) or not ENTRY_ID[kind].fullmatch(str(e.get("id", ""))):
        return f"an entry's id is {want}<n> on a list of {kind}s"
    i = e["id"]
    extra = set(e) - ENTRY_KEYS
    if extra:
        return f"{i}: the list names {', '.join(sorted(extra))}, which the doorway does not send"
    if not isinstance(e.get("model"), str) or not re.fullmatch(r"[a-z0-9_]{1,64}", e["model"]):
        return f"{i}: model is a Higgsfield job type, such as seedance_2_0"
    if not isinstance(e.get("prompt"), str) or not e["prompt"].strip() or len(e["prompt"]) > MAX_PROMPT_CHARS:
        return f"{i}: a prompt is text, up to {MAX_PROMPT_CHARS} characters"
    params = e.get("params", {})
    if not isinstance(params, dict):
        return f"{i}: params is an object of the model's settings"
    for k, v in params.items():
        if not PARAM.fullmatch(str(k)) or k == "prompt" or k in MEDIA_FLAGS:
            return f"{i}: {k} is not a setting the doorway sends"
        if isinstance(v, str) and not SETTING.fullmatch(v):
            return f"{i}: {k} is a word, a ratio or a size, never a path, a link or a flag ({seat.one_line(v, 40)})"
        if not isinstance(v, (str, int, float, bool)):
            return f"{i}: {k} is one value, never a list or an object (media go only as earlier takes, by job id)"
    refs = []
    for k in MEDIA_FLAGS:
        if k not in e:
            continue
        v = e[k]
        vals = v if k == "image_references" and isinstance(v, list) else [v]
        if k == "image_references" and not isinstance(v, list):
            return f"{i}: image_references is a list of earlier takes, each job:<id>"
        for x in vals:
            if isinstance(x, str) and (JOB_REF.fullmatch(x) or (uploads and FILE_REF.fullmatch(x))):
                continue
            if uploads:
                return (f"{i}: {k} names an earlier take of this doorway's by its job id (job:<id>), or a file in "
                        "this job's approved copies by its path (approved/<version-id>/<file>); never a link, a path "
                        "outside approved/ or anything else")
            return (f"{i}: {k} names an earlier take of this doorway's by its job id (job:<id>); this job's setup "
                    f"record allows no upload ({UPLOADS_FIELD}: {UPLOADS_ALLOWED}), so never a file, a link or an upload")
        refs += vals
    if len(refs) > MAX_REFS:
        return f"{i}: at most {MAX_REFS} references"
    return None


def file_refs(e: Dict) -> Dict[str, List[str]]:
    """The files an entry names, each with the fields that name it, in the list's order."""
    out: Dict[str, List[str]] = {}
    for k in MEDIA_FLAGS:
        for x in (e[k] if isinstance(e.get(k), list) else [e[k]]) if k in e else []:
            if FILE_REF.fullmatch(x):
                out.setdefault(x, []).append(k)
    return out


def read_list(path: str, kind: str, uploads: bool = False) -> Optional[Dict]:
    """A list file read and checked whole, or None when it is a list of the other kind."""
    try:
        doc = json.loads(Path(path, LIST_FILE).read_text(encoding="utf-8"))
    except ValueError:
        raise Refused(f"{path}/{LIST_FILE} is not JSON")
    if not isinstance(doc, dict) or set(doc) != LIST_KEYS or not isinstance(doc["entries"], list) or not doc["entries"]:
        raise Refused(f"{path}/{LIST_FILE} is {{\"test\": ..., \"ceiling_credits\": ..., \"entries\": [...]}} and nothing else")
    ids = [str(e.get("id", "")) if isinstance(e, dict) else "" for e in doc["entries"]]
    kinds = {k for k, rx in ENTRY_ID.items() for i in ids if rx.fullmatch(i)}
    if kinds and kind not in kinds:
        return None
    if not isinstance(doc["test"], str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,39}", doc["test"]):
        raise Refused(f"{path}/{LIST_FILE}: test is the part or practical test it serves, such as sold-proof")
    c = doc["ceiling_credits"]
    if isinstance(c, bool) or not isinstance(c, (int, float)) or c <= 0:
        raise Refused(f"{path}/{LIST_FILE}: ceiling_credits is the test's ceiling, a number of credits")
    bad = [w for w in (check_entry(e, kind, uploads) for e in doc["entries"]) if w]
    if bad:
        raise Refused("the approved list cannot be sent as it stands: " + "; ".join(bad))
    if len(set(ids)) != len(ids):
        raise Refused("the approved list names an entry twice")
    return doc


def approved_copies(ctx: Dict) -> List[Tuple[Path, Dict[str, str], str]]:
    """Every approvals entry with decision approved that names a copy in this job's approved/, oldest first."""
    approvals = Path(ctx["engagement"]).parents[1] / "approvals"
    approved_root = os.path.join(ctx["media_project"], "approved")
    found = []
    for f in sorted(approvals.glob("[0-9][0-9][0-9]-*.md")) if approvals.is_dir() else []:
        h = header(f.read_text(encoding="utf-8"))
        path = media_path(ctx, h.get("version_path", ""))
        if h.get("decision") == "approved" and h.get("version_path") and seat.under(seat.real(path), seat.real(approved_root)):
            found.append((f, h, path))
    return found


def approved_list(ctx: Dict, kind: str, uploads: bool = False) -> Dict:
    """The newest list of this kind Sean approved for this job, read from the approvals ledger and its locked copy."""
    approved_root = os.path.join(ctx["media_project"], "approved")
    found = [(f, h, path) for f, h, path in approved_copies(ctx) if os.path.isfile(os.path.join(path, LIST_FILE))]
    for f, h, path in reversed(found):
        if sha256_path(Path(path)) != h.get("version_sha256"):
            raise Refused(f"{path} no longer matches its approval {h.get('id', f.name)}; an approved copy is never changed")
        doc = read_list(path, kind, uploads)
        if doc is not None:
            return {"approval": h.get("id", f.stem), "entry": str(f), "path": path, "sha256": h["version_sha256"],
                    "test": doc["test"], "ceiling": float(doc["ceiling_credits"]),
                    "entries": {e["id"]: e for e in doc["entries"]}}
    raise Refused(f"no approved list of {kind}s for this job: Sean approves the seat's {LIST_FILE} in one decision, and "
                  f"its locked copy in {approved_root}/<version-id>/ is named by an approvals entry")


def checksums(vdir: str) -> Dict[str, str]:
    """An approved copy's checksums.sha256, file by file, as `sha256sum` writes it: `<sha256>  <path>`."""
    try:
        text = Path(vdir, CHECKSUMS).read_text(encoding="utf-8")
    except (OSError, ValueError):
        return {}
    return {m[2]: m[1] for m in (re.fullmatch(r"([0-9a-f]{64}) [ *](.+)", x.rstrip("\r")) for x in text.splitlines()) if m}


def media_file(ctx: Dict, ref: str) -> Dict:
    """A file an entry names, checked to the byte against the approved copy it sits in, before anything is sent: the
    copy's approval and its folder hash, its checksums.sha256, and the file itself, a regular file reached through no
    link. The bytes returned are the ones checked, so what is uploaded is what the copy lists."""
    approved_root = seat.real(os.path.join(ctx["media_project"], "approved"))
    parts = ref.split("/")[1:]
    path, at = approved_root, None
    for p in parts:
        path = os.path.join(path, p)
        try:
            at = os.lstat(path)
        except FileNotFoundError:
            raise Refused(f"{ref} does not exist")
        if stat.S_ISLNK(at.st_mode):
            raise Refused(f"{ref} goes through a link ({p}); a file is sent only as itself, from its approved copy")
    if at is None or not stat.S_ISREG(at.st_mode):
        raise Refused(f"{ref} is not a regular file")
    vdir = os.path.join(approved_root, parts[0])
    named = [(f, h) for f, h, p in approved_copies(ctx) if seat.real(p) == vdir]
    if not named:
        raise Refused(f"{ref}: no approvals entry with decision approved names {parts[0]}; only an approved copy's "
                      "files are sent")
    folder = sha256_path(Path(vdir))
    match = [h for f, h in named if h.get("version_sha256") == folder]
    if not match:
        f, h = named[-1]
        raise Refused(f"{parts[0]} no longer matches its approval {h.get('id', f.name)}; an approved copy is never "
                      "changed")
    rel = "/".join(parts[1:])
    listed = checksums(vdir).get(rel)
    if not listed:
        raise Refused(f"{ref} is not listed in {parts[0]}/{CHECKSUMS}")
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    except OSError as err:
        raise Refused(f"{ref} could not be read ({seat.one_line(str(err), 120)})")
    with os.fdopen(fd, "rb") as fh:
        if not stat.S_ISREG(os.fstat(fh.fileno()).st_mode):
            raise Refused(f"{ref} is not a regular file")
        data = fh.read(MAX_UPLOAD_BYTES + 1)
    if len(data) > MAX_UPLOAD_BYTES:
        raise Refused(f"{ref} is over {MAX_UPLOAD_BYTES} bytes")
    sha = hashlib.sha256(data).hexdigest()
    if sha != listed:
        raise Refused(f"{ref} is not the file its approved copy lists (sha256 {sha[:12]}, listed {listed[:12]})")
    if sniff(data) not in SUFFIXES["image"]:
        raise Refused(f"{ref} is not an image (png, jpg or webp); only an image goes as a reference")
    return {"ref": ref, "path": path, "sha256": sha, "bytes": len(data), "approval": match[-1].get("id"), "data": data}


def ids(v: str) -> List[str]:
    """A header's list of ids, `[a, b]`, or one id on its own; none if unwritten."""
    v = v.strip()
    if v.startswith("[") and v.endswith("]"):
        return [x.strip() for x in v[1:-1].split(",") if x.strip()]
    return [v] if v and not v.startswith("[") else []


def engagements(h: Dict[str, str]) -> List[str]:
    """A setup record's `engagements: [mc-eng-NNN, ...]`, the jobs its intended use is written for; none if unwritten."""
    v = h.get("engagements", "")
    if not (v.startswith("[") and v.endswith("]")):
        return []
    return ids(v)


def approved_use(h: Dict[str, str]) -> bool:
    return bool(h.get("intended_use_approved")) and h["intended_use_approved"] not in ("null", "pending")


def setup_record(ctx: Dict) -> Dict:
    """The setup record of Higgsfield's settings whose intended use names this job, with Sean's approval in it; no
    call before it. Another job's approval never covers this one (never-do 6). A record that another approved record
    for this job supersedes (`supersedes: mc-setup-NNN`) is skipped; two still standing are Sean's to settle."""
    eng = header((Path(ctx["engagement"]) / "brief.md").read_text(encoding="utf-8")).get("id")
    if not eng:
        raise Refused("the brief's header names no id, so no intended-use record can be read for this job")
    setup = Path(ctx["engagement"]).parents[1] / "setup"
    found = []
    for f in sorted(setup.glob("*/record.md")) if setup.is_dir() else []:
        h = header(f.read_text(encoding="utf-8"))
        if h.get("tool") == SETUP_TOOL and eng in engagements(h):
            found.append((f, h))
    if not found:
        raise Refused(f"no Higgsfield setup record covers {eng}: its intended use is its own record in the ledger's "
                      f"setup/ (`tool: {SETUP_TOOL}`, `engagements: [{eng}]`), with Higgsfield's data-use and training "
                      "settings and Sean's approval, before the first call (never-do 6)")
    gone = {s for f, h in found if approved_use(h) for s in ids(h.get("supersedes", ""))}
    standing = [(f, h) for f, h in found if h.get("id", f.parent.name) not in gone]
    if not standing:
        raise Refused(f"{' and '.join(h.get('id', f.parent.name) for f, h in found)} supersede one another for {eng}, "
                      "so none stands; which one holds is Sean's")
    if len(standing) > 1:
        raise Refused(f"{' and '.join(h.get('id', f.parent.name) for f, h in standing)} both cover {eng}: one "
                      "intended-use record a job, so which one holds is Sean's")
    f, h = standing[0]
    sid = h.get("id", f.parent.name)
    if not approved_use(h):
        raise Refused(f"{sid} has no intended-use approval from Sean yet (never-do 6); no Higgsfield call before it")
    if h.get(UPLOADS_FIELD) not in (None, UPLOADS_ALLOWED):
        raise Refused(f"{sid} says `{UPLOADS_FIELD}: {h[UPLOADS_FIELD]}`; the field is `{UPLOADS_FIELD}: "
                      f"{UPLOADS_ALLOWED}` or absent, so no file is sent under it")
    return {"id": sid, "path": str(f), "approved": h["intended_use_approved"], "engagement": eng,
            "uploads": h.get(UPLOADS_FIELD) == UPLOADS_ALLOWED, "supersedes": ids(h.get("supersedes", ""))}


def brief_cap(eng: str) -> float:
    """The train's Higgsfield cap from its brief. No cap, no call."""
    h = header((Path(eng) / "brief.md").read_text(encoding="utf-8"))
    try:
        cap = float(h["higgsfield_credits_cap"])
    except (KeyError, ValueError):
        raise Refused("the brief's header needs higgsfield_credits_cap; no Higgsfield call is made without it")
    if cap <= 0:
        raise Refused("the brief's higgsfield_credits_cap is 0: this job makes no Higgsfield call")
    return cap


# --- the job's log ----------------------------------------------------------------------------

def job_log(eng: str) -> List[Dict]:
    """Every Higgsfield call this job has made, from every pass's log; a call's last line stands for it."""
    calls: Dict[str, Dict] = {}
    for f in sorted((Path(eng) / "trace" / "logs").glob("*.higgsfield.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            try:
                e = json.loads(line)
            except ValueError:
                continue
            key = e.get("call") or f"{f.name}:{len(calls)}"
            # a call's filed line stands over its unfiled one, whichever pass's log is read last (settle)
            if not (calls.get(key, {}).get("made") and not e.get("made")):
                calls[key] = e
    return list(calls.values())


def entry_sha(lst: Dict, e: Dict) -> str:
    return hashlib.sha256(json.dumps({"test": lst["test"], "entry": e}, sort_keys=True).encode()).hexdigest()


def tally(log: List[Dict]) -> Dict:
    takes: Dict[str, int] = {}
    tests: Dict[str, float] = {}
    jobs = set()
    for e in log:
        charged = float(e.get("credits") or 0)
        # a call the balance says was charged counts even when its answer named no job the doorway could read
        if e.get("job") or charged > 0:
            tests[e["test"]] = tests.get(e["test"], 0.0) + charged
            # a job that made something, or spent anything, is a take; one Higgsfield failed and charged nothing is not
            if e.get("made") or charged > 0:
                takes[e["entry_sha256"]] = takes.get(e["entry_sha256"], 0) + 1
        if e.get("made") and e.get("job"):
            jobs.add(e["job"])
    return {"takes": takes, "tests": tests, "train": round(sum(tests.values()), 3), "jobs": jobs}


# --- the call ---------------------------------------------------------------------------------

def command(e: Dict, kind: str, made: set, upload: Optional[Callable[[str], str]] = None) -> List[str]:
    """The `generate` arguments for an entry, checked against what Higgsfield says its model takes. A named file goes
    as the id `upload` returns for it, asked only once the model is known to take the field."""
    code, listed, why = cli("model", "list", f"--{kind}")
    if code != 0 or not isinstance(listed, list):
        raise Refused(f"could not list Higgsfield's {kind} models ({why})")
    if e["model"] not in {m.get("job_type") for m in listed if isinstance(m, dict)}:
        raise Refused(f"{e['id']}: {e['model']} is not one of Higgsfield's {kind} models")
    code, doc, why = cli("model", "get", e["model"])
    params = doc.get("params") if code == 0 and isinstance(doc, dict) else None
    if not isinstance(params, list):
        raise Refused(f"could not read {e['model']}'s settings ({why})")
    schema = {p["name"]: p for p in params if isinstance(p, dict) and isinstance(p.get("name"), str)}
    if "prompt" not in schema:
        raise Refused(f"{e['id']}: {e['model']} takes no prompt")
    args = [e["model"], f"--prompt={e['prompt']}"]
    for k, v in sorted((e.get("params") or {}).items()):
        p = schema.get(k)
        if p is None:
            raise Refused(f"{e['id']}: {e['model']} takes no setting {k}")
        types = SCALARS.get(str(p.get("type")))
        if types is None:
            raise Refused(f"{e['id']}: {k} is a media setting ({p.get('type')}); media go only as start_image, "
                          "end_image or image_references")
        if isinstance(v, bool) != (bool in types) or not isinstance(v, types):
            raise Refused(f"{e['id']}: {k} is {p.get('type')} for {e['model']}")
        if p.get("enum") and v not in p["enum"]:
            raise Refused(f"{e['id']}: {k} is one of {', '.join(map(str, p['enum']))} for {e['model']}")
        args.append(f"--{k}=" + (json.dumps(v) if isinstance(v, bool) else str(v)))
    media = [k for k in MEDIA_FLAGS if k in e]
    for k in media:
        if k not in schema:
            raise Refused(f"{e['id']}: {e['model']} takes no {k}")
        for ref in e[k] if isinstance(e[k], list) else [e[k]]:
            m = JOB_REF.fullmatch(ref)
            if m and m[1] not in made:
                raise Refused(f"{e['id']}: {k} names job {m[1]}, which is no take this doorway made in this job; "
                              "a job id names only the doorway's own takes")
    for k in media:
        for ref in e[k] if isinstance(e[k], list) else [e[k]]:
            m = JOB_REF.fullmatch(ref)
            if not m and upload is None:
                raise Refused(f"{e['id']}: {k} names a file, and nothing is uploaded here")
            args.append(f"{MEDIA_FLAGS[k]}={m[1] if m else upload(ref)}")
    return args


def estimate(args: List[str]) -> float:
    code, doc, why = cli("generate", "cost", *args)
    try:
        if code == 0:
            return float(doc["credits"])  # type: ignore[index]
    except (TypeError, KeyError, ValueError):
        pass
    raise Refused(f"Higgsfield gave no price for this take ({why}); nothing is sent unpriced")


def checked(a) -> Dict:
    """The context, the setup record, the job's approved list and caps, and (for a take) the entry and the output."""
    src = seat.real(a.context)
    if not CONTEXT_FILE.fullmatch(os.path.basename(src)) or not os.path.isfile(src):
        raise Refused(f"{a.context} is not a pass context (trace/logs/pass-NN.context.json)")
    ctx = seat.load(src)
    if os.path.dirname(src) != os.path.join(ctx["engagement"], "trace", "logs"):
        raise Refused("the context is not in its engagement's trace/logs/, where only the coordinator writes")
    kind = KINDS.get(ctx["seat"])
    if not kind or ctx.get("toolbelt", {}).get("higgsfield") != kind:
        raise Refused(f"{ctx['seat']}'s pass may not call Higgsfield: only Art's drafting pass, for images, and the "
                      "Animator's, for video")
    if ctx.get("machine") != seat.machine():
        raise Refused(f"the context was written on {ctx.get('machine')}, not {seat.machine()}")
    setup = setup_record(ctx)
    c = {"ctx": ctx, "kind": kind, "setup": setup, "cap": brief_cap(ctx["engagement"]),
         "list": approved_list(ctx, kind, setup["uploads"])}
    if c["list"]["ceiling"] > c["cap"]:
        raise Refused(f"the list's ceiling ({c['list']['ceiling']:g}) is over the train's cap ({c['cap']:g})")
    if getattr(a, "status", False) or getattr(a, "job", None):
        return c
    e = c["list"]["entries"].get(a.entry)
    if e is None:
        raise Refused(f"{a.entry} is not on the approved list {c['list']['approval']}; a new or reworded entry goes "
                      "to Sean first")
    return {**c, "entry": e, "out": checked_out(ctx, kind, a.out)}


def checked_out(ctx: Dict, kind: str, out_arg: str) -> Path:
    """The file a take is written to: new, in a version folder made in this pass, directly in the seat's stage."""
    stage = os.path.join(ctx["media_project"], seat.STAGE_DIRS[ctx["seat"]])
    out = Path(seat.real(out_arg))
    vdir = out.parent
    if out.suffix not in SUFFIXES[kind]:
        raise Refused(f"--out names a {' or '.join(SUFFIXES[kind])} (an answer of another type is filed under the "
                      "same name with its own suffix)")
    if seat.real(str(vdir.parent)) != seat.real(stage) or not VERSION_DIR.fullmatch(vdir.name):
        raise Refused(f"--out goes in a version folder directly in this seat's stage ({stage}/<artifact>-vNN-<date>/)")
    if not vdir.is_dir():
        raise Refused(f"make the version folder {vdir.name} first; the take lands in it")
    if any(seat.under(str(vdir), seat.real(f)) for f in ctx["fence"]["frozen"]):
        raise Refused(f"{vdir.name} was saved before this pass; a saved version is never changed (rule 5)")
    if any(os.path.lexists(out.with_suffix(s)) for s in (".png", ".jpg", ".webp", ".mp4")) \
            or os.path.lexists(out.with_name(out.stem + ".higgsfield.json")):
        raise Refused(f"{out.name} or its sidecar exists; a take is written once")
    return out


def write_new(vdir: Path, dfd: int, name: str, data: bytes) -> None:
    """Create one new file in the version folder, never through a link, never over a file already there."""
    if seat.real(str(vdir)) != str(vdir) or os.stat(dfd).st_ino != os.stat(vdir, follow_symlinks=False).st_ino:
        raise FileExistsError(f"{vdir.name} moved or became a link during the call")
    fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644, dir_fd=dfd)
    with os.fdopen(fd, "wb") as f:
        f.write(data)


def append(log: Path, entry: Dict) -> None:
    with open(log, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def refusal_line(a, msg: str) -> None:
    """A refusal before the checks passed is still a line in the pass's log, when the context says which pass."""
    try:
        src = seat.real(a.context)
        logs = Path(src).parent
        if CONTEXT_FILE.fullmatch(os.path.basename(src)) and logs.name == "logs" and logs.parent.name == "trace":
            append(logs / f"{seat.pass_id_of(src)}.higgsfield.jsonl",
                   {"call": f"refused-{time.time_ns()}", "entry": getattr(a, "entry", None), "refused": msg,
                    "completed": seat.now(), "made": False})
    except OSError:
        pass


def uploader(entry: Dict, files: Dict[str, Dict], fields: Dict[str, List[str]]) -> Callable[[str], str]:
    """Send each checked file once, from a private copy of the bytes that were checked, so the command line reads
    nothing but what the approved copy lists; each upload goes on the call's line, with its path and sha256."""
    sent_ids: Dict[str, str] = {}
    entry["uploads"] = []

    def upload(ref: str) -> str:
        if ref in sent_ids:
            return sent_ids[ref]
        f = files[ref]
        u = {"ref": ref, "fields": fields[ref], "path": f["path"], "sha256": f["sha256"], "bytes": f["bytes"],
             "approval": f["approval"], "upload": None, "uploaded": seat.now()}
        entry["uploads"].append(u)
        with tempfile.TemporaryDirectory(prefix="mc-higgsfield-upload-") as private:
            copy = os.path.join(private, os.path.basename(f["path"]))
            fd = os.open(copy, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
            with os.fdopen(fd, "wb") as fh:
                fh.write(f["data"])
            code, doc, why = cli("upload", "create", copy, timeout=UPLOAD_TIMEOUT_S)
        uid = job_id(doc, ("id", "media_id", "upload_id")) if code == 0 else None
        if not uid:
            u["error"] = f"Higgsfield gave no upload id ({why})"
            raise Refused(f"{ref} could not be uploaded ({why}); no job is made without it")
        u["upload"] = sent_ids[ref] = uid
        return uid
    return upload


def take(a) -> None:
    try:
        c = checked(a)
    except Refused as e:
        refusal_line(a, str(e))
        refuse(str(e))
    ctx, e, out, lst = c["ctx"], c["entry"], c["out"], c["list"]
    vdir = out.parent
    logs = Path(ctx["engagement"]) / "trace" / "logs"
    pid = seat.pass_id_of(ctx["source"])
    log = logs / f"{pid}.higgsfield.jsonl"
    sha = entry_sha(lst, e)
    call = f"{pid}-{e['id']}-{time.time_ns()}"
    # The version folder is the seat's to write, so it is held open from the check on.
    dfd = os.open(vdir, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    # One take at a time across the job, so two calls cannot both pass the count and the caps.
    with open(logs / "higgsfield.lock", "a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        t = tally(job_log(ctx["engagement"]))
        entry = {"call": call, "pass": pid, "seat": ctx["seat"], "kind": c["kind"], "entry": e["id"], "entry_sha256": sha,
                 "approved_entry": e, "test": lst["test"],
                 "approval": {k: lst[k] for k in ("approval", "entry", "path", "sha256")}, "setup": c["setup"]["id"],
                 "take": t["takes"].get(sha, 0) + 1, "out": str(out), "started": seat.now(), "made": False}
        try:
            if t["takes"].get(sha, 0) >= TAKES_PER_ENTRY:
                raise Refused(f"{e['id']} has had its {TAKES_PER_ENTRY} takes; more is a question for Sean")
            # every named file is checked here, on this machine, before anything is sent
            fields = file_refs(e)
            files = {ref: media_file(ctx, ref) for ref in fields}
            # the files go up once the model is known to take them, and the take is priced with them
            args = command(e, c["kind"], t["jobs"], uploader(entry, files, fields) if files else None)
            est = estimate(args)
            spent = t["tests"].get(lst["test"], 0.0)
            if t["train"] + est > c["cap"] + 1e-9:
                raise Refused(f"this take (about {est:g} credits) would take the train past its {c['cap']:g} Higgsfield "
                              f"credits ({t['train']:g} spent): a checkpoint for Sean")
            if spent + est > lst["ceiling"] + 1e-9:
                raise Refused(f"this take (about {est:g} credits) would take {lst['test']} past its ceiling of "
                              f"{lst['ceiling']:g} ({spent:g} spent): a checkpoint for Sean")
            before = balance()
            if before is None:
                raise Refused("could not read the account's balance; nothing is sent unmetered")
            if before < est:
                raise Refused(f"the account holds {before:g} credits and this take asks about {est:g}; buying more is "
                              "Sean's (never-do 7)")
        except Refused as r:
            entry.update(refused=str(r), completed=seat.now())
            append(log, entry)
            os.close(dfd)
            refuse(str(r))
        entry.update(request=["generate", "create", *args], estimate=est, balance_before=before)
        t0 = time.time()
        code, doc, why = cli("generate", "create", *args)
        jid = job_id(doc) if code == 0 else None
        if not jid:
            after = settled(before)
            # any job id the answer names, so `settle` can file a job that was made but not read as one
            seen = sorted(set(UUID.findall(json.dumps(doc) + " " + why)))
            entry.update(completed=seat.now(), balance_after=after, error=f"Higgsfield took no job ({why})",
                         credits=max(0.0, before - after) if after is not None else 0.0,
                         credits_source="the account's balance, before and after", jobs_in_answer=seen)
            append(log, entry)
            os.close(dfd)
            refuse(f"no job was read from the answer ({why}); logged to {log.name}"
                   + (f"; it names {', '.join(seen)}, which `settle` can file" if seen else ""))
        # The job's line goes in now, at the estimate, so a call cut off from here still counts what it spent.
        entry.update(job=jid, credits=est, credits_source="estimate, until the job ends", created=seat.now())
        append(log, entry)
        code, doc, why = cli("generate", "wait", jid, "--quiet", f"--timeout={WAIT_TIMEOUT_S}s",
                             timeout=WAIT_TIMEOUT_S + 60)
        job = job_of(doc)
        url = job.get("result_url") if isinstance(job.get("result_url"), str) else None
        after = settled(before)
        if after is not None and after < before:
            entry.update(credits=round(before - after, 3), credits_source="the account's balance, before and after")
        elif after is not None and code == 0 and not url:
            # the job ended with nothing and the balance never moved: Higgsfield charged nothing, or gave it back
            entry.update(credits=0.0, credits_source="the account's balance, unmoved after a job that made nothing")
        elif after is not None:
            entry.update(credits_source="estimate (the account's balance did not move)")
        entry.update(status=job.get("status"), balance_after=after, wall_clock_s=round(time.time() - t0),
                     completed=seat.now())
        filed = None
        data = b""
        if not url:
            entry["error"] = f"the job ended with no result ({job.get('status') or why})"
        else:
            entry["result_url"] = url
            try:
                data = fetch(url)
            except (OSError, urllib.error.URLError) as err:
                entry["error"] = f"the result could not be downloaded ({seat.one_line(str(err), 200)})"
        if data:
            suffix = sniff(data)
            entry.update(sha256=hashlib.sha256(data).hexdigest(), bytes=len(data), format=suffix, made=True)
            label = LABEL.format(model=e["model"], approval=lst["approval"], setup=c["setup"]["id"])
            try:
                if suffix not in SUFFIXES[c["kind"]]:
                    raise FileExistsError(f"the answer is not a {c['kind']} this doorway files ({suffix or 'unknown'})")
                filed = out.with_suffix(suffix)
                entry.update(filed=str(filed), label=label)
                # the label first: a take is never filed without its prompt and "generated" beside it
                write_new(vdir, dfd, out.stem + ".higgsfield.json", (json.dumps(entry, indent=2) + "\n").encode())
                write_new(vdir, dfd, filed.name, data)
            except (FileExistsError, OSError) as err:
                kept = Path(ctx["scratch"]) / f"higgsfield-{e['id']}-{time.strftime('%H%M%S')}-{os.getpid()}{suffix or '.bin'}"
                kept.write_bytes(data)
                entry.update(filed=None, kept_in_scratch=str(kept), filing_error=str(err))
                filed = None
        append(log, entry)
    os.close(dfd)
    t = tally(job_log(ctx["engagement"]))
    spend = (f"{lst['test']} {t['tests'].get(lst['test'], 0):g} of {lst['ceiling']:g} credits, train {t['train']:g} "
             f"of {c['cap']:g}")
    if not data:
        refuse(f"no take was filed ({entry['error']}); job {jid}, {entry['credits']:g} credits counted; {spend}; "
               f"logged to {log.name}")
    if filed is None:
        refuse(f"the take came back but could not be filed ({entry['filing_error']}); kept at {entry['kept_in_scratch']}, "
               f"and it counts as a take; {spend}; logged to {log.name}")
    print(f"{filed} sha256 {entry['sha256']} · {e['id']} take {entry['take']} of {TAKES_PER_ENTRY} · job {jid} · "
          f"{entry['credits']:g} credits ({entry['credits_source']}) · {spend}")
    print("Generated, never authored craft (never-do 8): the sidecar beside it says so, and a later entry may name "
          f"this take as job:{jid}.")


def unfiled(log: List[Dict], jid: str) -> Optional[Dict]:
    """The doorway's own call that made job `jid` and filed nothing: by the job it read, or by a job id its answer
    named when it read none (mc-eng-002's first live call). None if no call of this job made it, or it is filed."""
    for e in log:
        named = e.get("job") == jid or jid in (e.get("jobs_in_answer") or []) or jid in str(e.get("error") or "")
        if named and not e.get("refused"):
            return None if e.get("made") else e
    return None


def settle(a) -> None:
    """File a job this doorway started but did not file, into a version folder of this pass's own, as the same take:
    its credits are already counted on the call's line, which this line replaces, so nothing is spent or counted
    twice. The job is read and downloaded from Higgsfield; nothing is sent to its generator."""
    try:
        if not UUID.fullmatch(a.job or ""):
            raise Refused("--job is a Higgsfield job id")
        c = checked(a)
        ctx = c["ctx"]
        orig = unfiled(job_log(ctx["engagement"]), a.job)
        if orig is None:
            raise Refused(f"job {a.job} is no call of this doorway's in this job that is still unfiled; "
                          "settle files only a job the doorway itself started and did not file")
        if orig.get("kind") != c["kind"]:
            raise Refused(f"job {a.job} is {orig.get('kind')}, and this pass takes {c['kind']}s")
        out = checked_out(ctx, c["kind"], a.out)
    except Refused as e:
        refusal_line(a, str(e))
        refuse(str(e))
    vdir = out.parent
    logs = Path(ctx["engagement"]) / "trace" / "logs"
    pid = seat.pass_id_of(ctx["source"])
    log = logs / f"{pid}.higgsfield.jsonl"
    dfd = os.open(vdir, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    with open(logs / "higgsfield.lock", "a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        orig = unfiled(job_log(ctx["engagement"]), a.job)
        if orig is None:
            os.close(dfd)
            refuse(f"job {a.job} was filed by another call meanwhile")
        code, doc, why = cli("generate", "get", a.job)
        job = job_of(doc)
        url = job.get("result_url") if isinstance(job.get("result_url"), str) else None
        if code != 0 or job.get("status") != "completed" or not url:
            os.close(dfd)
            refuse(f"job {a.job} has no finished result to file ({job.get('status') or why}); nothing was written")
        try:
            data = fetch(url)
        except (OSError, urllib.error.URLError) as err:
            os.close(dfd)
            refuse(f"job {a.job}'s result could not be downloaded ({seat.one_line(str(err), 200)}); nothing was written")
        suffix = sniff(data)
        if suffix not in SUFFIXES[c["kind"]]:
            os.close(dfd)
            refuse(f"job {a.job}'s answer is not a {c['kind']} this doorway files ({suffix or 'unknown'})")
        e = orig["approved_entry"]
        filed = out.with_suffix(suffix)
        entry = {**orig, "job": a.job, "status": job.get("status"), "result_url": url, "made": True,
                 "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data), "format": suffix, "filed": str(filed),
                 "label": LABEL.format(model=e["model"], approval=orig["approval"]["approval"],
                                       setup=orig.get("setup") or c["setup"]["id"]),
                 "settled_by": pid, "settled": seat.now(),
                 "credits_source": f"{orig.get('credits_source')}, on the call's own line; filed later by settle"}
        entry.pop("error", None)
        write_new(vdir, dfd, out.stem + ".higgsfield.json", (json.dumps(entry, indent=2) + "\n").encode())
        write_new(vdir, dfd, filed.name, data)
        append(log, entry)
    os.close(dfd)
    t = tally(job_log(ctx["engagement"]))
    lst = c["list"]
    print(f"{filed} sha256 {entry['sha256']} · {e['id']} take {orig.get('take')} of {TAKES_PER_ENTRY}, settled · job "
          f"{a.job} · {float(orig.get('credits') or 0):g} credits, counted once · {lst['test']} "
          f"{t['tests'].get(lst['test'], 0):g} of {lst['ceiling']:g} credits, train {t['train']:g} of {c['cap']:g}")
    print("Generated, never authored craft (never-do 8): the sidecar beside it says so, and a later entry may name "
          f"this take as job:{a.job}.")


def status(a) -> None:
    try:
        c = checked(a)
    except Refused as e:
        refuse(str(e))
    t = tally(job_log(c["ctx"]["engagement"]))
    lst = c["list"]
    print(f"approved list {lst['approval']} ({lst['path']}), test {lst['test']}; intended use {c['setup']['id']} for "
          f"{c['setup']['engagement']}"
          + (f", with uploads of approved media ({UPLOADS_FIELD}: {UPLOADS_ALLOWED})" if c["setup"]["uploads"] else ""))
    for i, e in lst["entries"].items():
        used = t["takes"].get(entry_sha(lst, e), 0)
        print(f"  {i} {e['model']}: {used} of {TAKES_PER_ENTRY} takes used · {e.get('purpose', '')}")
    print(f"spend: {lst['test']} {t['tests'].get(lst['test'], 0):g} of {lst['ceiling']:g} credits; "
          f"train {t['train']:g} of {c['cap']:g}")
    for e in job_log(c["ctx"]["engagement"]):
        if e.get("refused") or e.get("made"):
            continue
        if e.get("job"):
            print(f"  job {e['job']} ({e['entry']}) made no filed take: {e.get('error') or 'cut off before it ended'}")
        elif float(e.get("credits") or 0) > 0:
            seen = ", ".join(e.get("jobs_in_answer") or sorted(set(UUID.findall(str(e.get("error") or ""))))) or "none named"
            print(f"  {e['entry']}: charged {float(e['credits']):g} credits with no job read (job ids in the answer: "
                  f"{seen}); `settle` can file one")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("take", help="the launcher, for a pass's request: one take of one approved entry")
    t.add_argument("--context", required=True)
    t.add_argument("--entry", required=True)
    t.add_argument("--out", required=True)
    t.set_defaults(fn=take)
    st = sub.add_parser("settle", help="the launcher, for a pass's request: file a job this doorway started and did "
                                       "not file, as the same take, with nothing spent or counted twice")
    st.add_argument("--context", required=True)
    st.add_argument("--job", required=True)
    st.add_argument("--out", required=True)
    st.set_defaults(fn=settle)
    s = sub.add_parser("status", help="the approved list, the takes used and the spend; no call to Higgsfield")
    s.add_argument("--context", required=True)
    s.set_defaults(fn=status, status=True)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
