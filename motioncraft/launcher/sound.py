#!/usr/bin/env python3
"""Finishing's one way to generated sound: one take of one approved cue, filed in the pass's own version folder.

    sound.py --context <eng>/trace/logs/pass-NN.context.json --cue FX1
             --out finish/<artifact>-vNN-<date>/<name>.mp3
    sound.py --context <eng>/trace/logs/pass-NN.context.json --status

Finishing alone generates sound (master skill, "Generated sound"): sound effects on
ElevenLabs, music on the Gemini API's Lyria, under Sean's intended-use approval
(mc-setup-004): from a cue list he has approved, up to three takes per cue, each file
downloaded into the version folder when it is made, with its prompt beside it and
labelled generated, inside the job's spend cap, and no production material uploaded.
A Finishing pass on Claude runs this from its shell; its settings let exactly this
command, for exactly this pass's context, out of the sandbox, because inside it the
pass has no network and cannot read the keys file (`~/.config/audio-keys/keys.env`,
which every pass is denied). So this file holds the terms for the call:

- the context must sit in its engagement's `trace/logs/` and say the pass may use the
  sound path (a drafting Finishing pass on Claude);
- the cue comes from the newest approved cue list for this job: a `cues.json` in the
  media project's `approved/<version-id>/`, named by an approvals entry with decision
  approved whose sha256 still matches the folder. The pass names a cue by its id and
  nothing else: the tool, the model, the prompt and the settings are the list's, so a
  reworded prompt is a new list for Sean, never a take;
- three takes per cue and prompt, counted across the whole job from its sound logs;
- the job's caps from its brief: `spend_cap_usd` for Lyria, which bills per call, and
  `sound_credits_cap` for ElevenLabs, whose prepaid plan cannot buy more (Sean's ruling
  on the Finishing sound doorway ticket, 2026-10-19). A take that would cross either is
  refused, and that is a checkpoint for Sean. ElevenLabs credits are read from the
  account before and after each take;
- only the cue's text prompt is sent, never a file;
- the take lands as a new file in a version folder the pass made in its own `finish/`
  stage, with `<name>.sound.json` beside it (the cue, the approval, the take, the cost,
  the label "generated"), both created relative to the version folder held open since
  the check, never through a link and never over a file already there. Each call is
  logged to `trace/logs/pass-NN.sounds.jsonl`, refused calls too; audio that came back
  but could not be filed is kept in the pass's scratch folder rather than lost.

Written on the Motioncraft build map's "Finishing's sound doorway: ElevenLabs and Lyria
from a Finishing pass" ticket (2026-10-19), on the image doorway's pattern (image.py).
"""
from __future__ import annotations

import argparse
import base64
import fcntl
import hashlib
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional, Tuple

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import seat  # noqa: E402  the launcher's own rules: the context, the stage folders
from image import CONTEXT_FILE, VERSION_DIR  # noqa: E402  the same names the image doorway holds
from tracekit.engagement import sha256_path  # noqa: E402  the approvals ledger's folder hash

SEAT = "finishing-sound-designer"
TAKES_PER_CUE = 3  # mc-setup-004
KEYS = Path(os.path.expanduser("~/.config/audio-keys/keys.env"))
CUE_ID = re.compile(r"(FX|MU)\d+")
# ElevenLabs, text to sound effects (SWCB #215, read 2026-10-18). mp3 at 192 kb/s is the best the Creator plan
# allows; pcm_44100 needs Pro. Its pages disagree on cost (200 credits a take, or 40 a second when a duration is
# set), so the check before a take assumes the larger; the take itself is metered from the account.
EFFECTS_URL = "https://api.elevenlabs.io/v1/sound-generation"
EFFECTS_MODEL = "eleven_text_to_sound_v2"
EFFECTS_FORMAT = "mp3_44100_192"
SUBSCRIPTION_URL = "https://api.elevenlabs.io/v1/user/subscription"
# The account's count moves some seconds after a take (live, 2026-10-19: read at once it had not moved; a minute on it
# showed the take's 15 credits). So the doorway reads it until it moves, and records the estimate if it never does.
METER_WAIT_S, METER_POLL_S = 90, 3
# Lyria on the Gemini API's Interactions endpoint, paid tier, price per call in USD (SWCB #215, pricing page
# 2026-10-16). lyria-3-pro-preview is the older song model and lyria-realtime-exp is unpriced: neither is offered.
MUSIC_URL = "https://generativelanguage.googleapis.com/v1beta/interactions"
MUSIC_PRICES_USD = {"lyria-3-clip-preview": 0.04, "lyria-3.5": 0.08}
EFFECT_KEYS = {"id", "moment", "tool", "prompt", "duration_s", "loop", "prompt_influence"}
MUSIC_KEYS = {"id", "moment", "tool", "prompt", "model"}
MAX_PROMPT_CHARS = 2000
TIMEOUT_S = 300
LABEL = ("generated: {service} ({model}) through motioncraft/launcher/sound.py, from Sean's approved cue list "
         "{approval}, under mc-setup-004")


def refuse(msg: str) -> None:
    sys.stderr.write(f"sound.py: {msg}\n")
    sys.exit(1)


def header(text: str) -> Dict[str, str]:
    """A markdown file's `---` header as plain key: value pairs, comments dropped."""
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    out = {}
    for line in (m.group(1).splitlines() if m else []):
        k, sep, v = line.partition(":")
        if sep and not line.startswith((" ", "#")):
            out[k.strip()] = v.split(" #")[0].strip().strip('"')
    return out


def brief_caps(eng: str) -> Tuple[float, int]:
    """The job's sound caps from its brief: USD for Lyria, credits for ElevenLabs. No cap, no sound."""
    h = header((Path(eng) / "brief.md").read_text(encoding="utf-8"))
    try:
        return float(h["spend_cap_usd"]), int(h["sound_credits_cap"])
    except (KeyError, ValueError):
        refuse("the brief's header needs spend_cap_usd and sound_credits_cap; no sound is made without both caps")
    raise AssertionError


def check_cue(c: Dict) -> Optional[str]:
    """Why a cue in an approved list cannot be sent as it stands, or None."""
    if not isinstance(c, dict) or not CUE_ID.fullmatch(str(c.get("id", ""))):
        return "a cue's id is FX<n> for a sound effect or MU<n> for music"
    tool = {"FX": "effect", "MU": "music"}[c["id"][:2]]
    if c.get("tool") != tool:
        return f"{c['id']}: its tool is `{tool}`"
    if not isinstance(c.get("prompt"), str) or not c["prompt"].strip() or len(c["prompt"]) > MAX_PROMPT_CHARS:
        return f"{c['id']}: a prompt is text, up to {MAX_PROMPT_CHARS} characters"
    extra = set(c) - (EFFECT_KEYS if tool == "effect" else MUSIC_KEYS)
    if extra:
        return f"{c['id']}: the list names {', '.join(sorted(extra))}, which the doorway does not send"
    if tool == "music":
        return None if c.get("model") in MUSIC_PRICES_USD else f"{c['id']}: model is one of {', '.join(MUSIC_PRICES_USD)}"
    d = c.get("duration_s")
    if d is not None and (not isinstance(d, (int, float)) or isinstance(d, bool) or not 0.5 <= d <= 30):
        return f"{c['id']}: duration_s is 0.5 to 30 seconds, or left out"
    p = c.get("prompt_influence")
    if p is not None and (not isinstance(p, (int, float)) or isinstance(p, bool) or not 0 <= p <= 1):
        return f"{c['id']}: prompt_influence is 0 to 1, or left out"
    if not isinstance(c.get("loop", False), bool):
        return f"{c['id']}: loop is true or false"
    return None


def media_path(ctx: Dict, p: str) -> str:
    """An approvals entry's version_path, absolute or as `media:<film>/<project>/...`."""
    if p.startswith("media:"):
        root = ctx["media_project"][: -len(ctx["media"][len("media:"):])]
        return os.path.join(root, p[len("media:"):])
    return os.path.expanduser(p)


def approved_list(ctx: Dict) -> Dict:
    """The newest cue list Sean approved for this job, read from the approvals ledger and its locked copy."""
    approvals = Path(ctx["engagement"]).parents[1] / "approvals"
    approved_root = os.path.join(ctx["media_project"], "approved")
    found = []
    for f in sorted(approvals.glob("[0-9][0-9][0-9]-*.md")) if approvals.is_dir() else []:
        h = header(f.read_text(encoding="utf-8"))
        path = media_path(ctx, h.get("version_path", ""))
        if (h.get("decision") == "approved" and h.get("version_path")
                and seat.under(seat.real(path), seat.real(approved_root)) and os.path.isfile(os.path.join(path, "cues.json"))):
            found.append((f, h, path))
    if not found:
        refuse(f"no approved cue list for this job: Sean approves the sound plan's cues.json, and its locked copy in "
               f"{approved_root}/<version-id>/ is named by an approvals entry")
    f, h, path = found[-1]
    if sha256_path(Path(path)) != h.get("version_sha256"):
        refuse(f"{path} no longer matches its approval {h.get('id', f.name)}; an approved copy is never changed")
    try:
        cues = json.loads(Path(path, "cues.json").read_text(encoding="utf-8"))["cues"]
    except (ValueError, KeyError, TypeError):
        refuse(f"{path}/cues.json is not a cue list ({{\"cues\": [...]}})")
    bad = [w for w in map(check_cue, cues) if w]
    if bad:
        refuse("the approved cue list cannot be sent as it stands: " + "; ".join(bad))
    ids = [c["id"] for c in cues]
    if len(set(ids)) != len(ids):
        refuse("the approved cue list names a cue twice")
    return {"approval": h.get("id", f.stem), "entry": str(f), "path": path, "sha256": h["version_sha256"],
            "cues": {c["id"]: c for c in cues}}


def job_log(eng: str) -> List[Dict]:
    """Every sound call this job has made, from every pass's log, in order."""
    out = []
    for f in sorted((Path(eng) / "trace" / "logs").glob("*.sounds.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            try:
                out.append(json.loads(line))
            except ValueError:
                continue
    return out


def prompt_sha(cue: Dict) -> str:
    return hashlib.sha256(json.dumps(cue, sort_keys=True).encode()).hexdigest()


def tally(log: List[Dict]) -> Dict:
    takes: Dict[str, int] = {}
    for e in log:
        if e.get("made"):
            takes[e["cue_sha256"]] = takes.get(e["cue_sha256"], 0) + 1
    return {"takes": takes, "usd": round(sum(e.get("usd") or 0 for e in log), 4),
            "credits": sum(e.get("credits") or 0 for e in log)}


def effect_estimate(cue: Dict) -> int:
    d = cue.get("duration_s")
    return max(200, math.ceil(40 * d)) if d else 200


def key(name: str) -> str:
    """One key from Sean's keys file, read here and never printed, logged or passed on."""
    if not KEYS.is_file():
        refuse(f"no keys file at {KEYS}")
    for line in KEYS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("export "):
            line = line[len("export "):]
        k, sep, v = line.partition("=")
        if sep and k.strip() == name and v.strip():
            return v.strip().strip("'\"")
    refuse(f"the keys file has no {name}")
    raise AssertionError


def http(method: str, url: str, headers: Dict[str, str], body: Optional[bytes]) -> Tuple[int, bytes]:
    """One request; the status and the body, an error's included."""
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return 0, str(e).encode()


def why(status: int, body: bytes) -> str:
    return f"HTTP {status}: " + seat.one_line(body.decode("utf-8", "replace"), 300)


def credits_used() -> Optional[Tuple[int, int]]:
    """The account's credits used this month and its limit, or None."""
    status, body = http("GET", SUBSCRIPTION_URL, {"xi-api-key": key("ELEVENLABS_API_KEY")}, None)
    try:
        d = json.loads(body) if status == 200 else {}
        return int(d["character_count"]), int(d["character_limit"])
    except (ValueError, KeyError, TypeError):
        return None


def settled(before: Optional[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
    """The account's count once it has moved past `before`, or its last read when it has not in METER_WAIT_S."""
    deadline = time.time() + METER_WAIT_S
    while True:
        after = credits_used()
        if not before or (after and after[0] != before[0]) or time.time() >= deadline:
            return after
        time.sleep(METER_POLL_S)


def make_effect(cue: Dict) -> Dict:
    body = {"text": cue["prompt"], "model_id": EFFECTS_MODEL, "loop": bool(cue.get("loop", False))}
    for k, api in (("duration_s", "duration_seconds"), ("prompt_influence", "prompt_influence")):
        if cue.get(k) is not None:
            body[api] = cue[k]
    before = credits_used()
    status, data = http("POST", f"{EFFECTS_URL}?output_format={EFFECTS_FORMAT}",
                        {"xi-api-key": key("ELEVENLABS_API_KEY"), "Content-Type": "application/json",
                         "Accept": "audio/mpeg"}, json.dumps(body).encode())
    made = data if status == 200 and data else None
    after = settled(before) if made else credits_used()
    res = {"service": "ElevenLabs text to sound effects", "model": EFFECTS_MODEL, "endpoint": EFFECTS_URL,
           "request": {**body, "output_format": EFFECTS_FORMAT}, "status": status, "usd": 0.0}
    if before and after and (after[0] > before[0] or (not made and after[0] == before[0])):
        res.update(credits=after[0] - before[0], credits_source="the account's character_count, before and after")
    else:
        res.update(credits=effect_estimate(cue) if made else 0,
                   credits_source="estimate (the account's count did not move, failed, or reset)")
    return {**res, "audio": made, "error": None if made else why(status, data)}


def make_music(cue: Dict) -> Dict:
    body = {"model": cue["model"], "input": cue["prompt"]}
    status, data = http("POST", MUSIC_URL, {"x-goog-api-key": key("GEMINI_API_KEY"), "Content-Type": "application/json"},
                        json.dumps(body).encode())
    audio, words, usage = None, [], None
    if status == 200:
        try:
            doc = json.loads(data)
        except ValueError:
            doc = {}
        usage = doc.get("usage") if isinstance(doc, dict) else None

        def walk(x):
            nonlocal audio
            if isinstance(x, dict):
                if x.get("type") == "audio" and isinstance(x.get("data"), str) and audio is None:
                    audio = base64.b64decode(x["data"])
                elif x.get("type") == "text" and isinstance(x.get("text"), str):
                    words.append(x["text"])
                for v in x.values():
                    walk(v)
            elif isinstance(x, list):
                for v in x:
                    walk(v)
        walk(doc)
    return {"service": "Gemini API Lyria", "model": cue["model"], "endpoint": MUSIC_URL, "request": body,
            "status": status, "usd": MUSIC_PRICES_USD[cue["model"]] if audio else 0.0, "credits": 0,
            "usage": usage, "words": words, "audio": audio,
            "error": None if audio else (why(status, data) if status != 200 else "HTTP 200 with no audio in the answer")}


def sniff(data: bytes) -> Optional[str]:
    if data[:3] == b"ID3" or (len(data) > 1 and data[0] == 0xFF and data[1] & 0xE0 == 0xE0):
        return "mp3"
    if data[:4] == b"RIFF" and data[8:12] == b"WAVE":
        return "wav"
    return None


def checked(a) -> Dict:
    """The context, the job's approved list and caps, and (for a take) the cue and the output; or a refusal."""
    src = seat.real(a.context)
    if not CONTEXT_FILE.fullmatch(os.path.basename(src)) or not os.path.isfile(src):
        refuse(f"{a.context} is not a pass context (trace/logs/pass-NN.context.json)")
    ctx = seat.load(src)
    if os.path.dirname(src) != os.path.join(ctx["engagement"], "trace", "logs"):
        refuse("the context is not in its engagement's trace/logs/, where only the coordinator writes")
    if ctx["seat"] != SEAT or not ctx.get("toolbelt", {}).get("sound"):
        refuse(f"{ctx['seat']}'s pass may not call the sound path: only Finishing's, on Claude, drafting")
    if ctx.get("machine") != seat.machine():
        refuse(f"the context was written on {ctx.get('machine')}, not {seat.machine()}")
    usd_cap, credits_cap = brief_caps(ctx["engagement"])
    c = {"ctx": ctx, "usd_cap": usd_cap, "credits_cap": credits_cap, "list": approved_list(ctx)}
    if a.status:
        return c
    if not a.cue or not a.out:
        refuse("a take names --cue and --out")
    cue = c["list"]["cues"].get(a.cue)
    if cue is None:
        refuse(f"{a.cue} is not on the approved cue list {c['list']['approval']}; a new or reworded cue goes to Sean first")
    stage = os.path.join(ctx["media_project"], seat.STAGE_DIRS[SEAT])
    out = Path(seat.real(a.out))
    vdir = out.parent
    if out.suffix != ".mp3":
        refuse("--out names a .mp3 (a WAV answer is filed under the same name as .wav)")
    if seat.real(str(vdir.parent)) != seat.real(stage) or not VERSION_DIR.fullmatch(vdir.name):
        refuse(f"--out goes in a version folder directly in this seat's stage ({stage}/<artifact>-vNN-<date>/)")
    if not vdir.is_dir():
        refuse(f"make the version folder {vdir.name} first; the take lands in it")
    if any(seat.under(str(vdir), seat.real(f)) for f in ctx["fence"]["frozen"]):
        refuse(f"{vdir.name} was saved before this pass; a saved version is never changed (rule 5)")
    names = [out, out.with_suffix(".wav"), out.with_name(out.stem + ".sound.json")]
    if any(os.path.lexists(p) for p in names):
        refuse(f"{out.name} or its sidecar exists; a take is written once")
    return {**c, "cue": cue, "out": out}


def write_new(vdir: Path, dfd: int, name: str, data: bytes) -> None:
    """Create one new file in the version folder, never through a link, never over a file already there."""
    if seat.real(str(vdir)) != str(vdir) or os.stat(dfd).st_ino != os.stat(vdir, follow_symlinks=False).st_ino:
        raise FileExistsError(f"{vdir.name} moved or became a link during the call")
    fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644, dir_fd=dfd)
    with os.fdopen(fd, "wb") as f:
        f.write(data)


def status(c: Dict) -> None:
    t = tally(job_log(c["ctx"]["engagement"]))
    lst = c["list"]
    print(f"approved cue list {lst['approval']} ({lst['path']})")
    for cid, cue in lst["cues"].items():
        used = t["takes"].get(prompt_sha(cue), 0)
        what = cue["model"] if cue["tool"] == "music" else f"{EFFECTS_MODEL}, {cue.get('duration_s') or 'auto'} s"
        print(f"  {cid} {cue.get('moment', '')} {cue['tool']} ({what}): {used} of {TAKES_PER_CUE} takes used")
    print(f"spend: ${t['usd']:.2f} of ${c['usd_cap']:.2f} (Lyria); {t['credits']} of {c['credits_cap']} credits (ElevenLabs)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--context", required=True)
    ap.add_argument("--cue")
    ap.add_argument("--out")
    ap.add_argument("--status", action="store_true", help="the approved cues, the takes used and the spend; no call")
    a = ap.parse_args()
    c = checked(a)
    ctx = c["ctx"]
    if a.status:
        status(c)
        return
    cue, out = c["cue"], c["out"]
    vdir = out.parent
    logs = Path(ctx["engagement"]) / "trace" / "logs"
    pid = seat.pass_id_of(ctx["source"])
    log = logs / f"{pid}.sounds.jsonl"
    # The version folder is the seat's to write, so it is held open from the check on.
    dfd = os.open(vdir, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    # One take at a time across the job, so two calls cannot both pass the count and the caps.
    with open(logs / "sounds.lock", "a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        t = tally(job_log(ctx["engagement"]))
        sha = prompt_sha(cue)
        entry = {"pass": pid, "seat": ctx["seat"], "cue": cue["id"], "cue_sha256": sha, "approved_cue": cue,
                 "approval": {k: c["list"][k] for k in ("approval", "entry", "path", "sha256")},
                 "take": t["takes"].get(sha, 0) + 1, "out": str(out), "started": seat.now(), "made": False}
        refusal = None
        if t["takes"].get(sha, 0) >= TAKES_PER_CUE:
            refusal = f"{cue['id']} has had its {TAKES_PER_CUE} takes; more is a question for Sean"
        elif cue["tool"] == "music" and t["usd"] + MUSIC_PRICES_USD[cue["model"]] > c["usd_cap"] + 1e-9:
            refusal = (f"this take (${MUSIC_PRICES_USD[cue['model']]:.2f}) would take the job past its ${c['usd_cap']:.2f} "
                       f"spend cap (${t['usd']:.2f} spent): a checkpoint for Sean")
        elif cue["tool"] == "effect" and t["credits"] + effect_estimate(cue) > c["credits_cap"]:
            refusal = (f"this take (up to {effect_estimate(cue)} credits) would take the job past its {c['credits_cap']} "
                       f"ElevenLabs credits ({t['credits']} used): a checkpoint for Sean")
        if refusal:
            entry.update(refused=refusal, completed=seat.now())
            with open(log, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
            os.close(dfd)
            refuse(refusal)
        t0 = time.time()
        res = make_music(cue) if cue["tool"] == "music" else make_effect(cue)
        audio = res.pop("audio")
        entry.update(res, completed=seat.now(), wall_clock_s=round(time.time() - t0), made=bool(audio))
        filed = None
        if audio:
            fmt = sniff(audio)
            entry.update(sha256=hashlib.sha256(audio).hexdigest(), bytes=len(audio), format=fmt)
            label = LABEL.format(service=res["service"], model=res["model"], approval=c["list"]["approval"])
            try:
                if fmt is None:
                    raise FileExistsError("the answer is neither MP3 nor WAV")
                filed = out if fmt == "mp3" else out.with_suffix(".wav")
                entry.update(filed=str(filed), label=label)
                # the label first: a take is never filed without its prompt and "generated" beside it
                write_new(vdir, dfd, out.stem + ".sound.json", (json.dumps(entry, indent=2) + "\n").encode())
                write_new(vdir, dfd, filed.name, audio)
            except (FileExistsError, OSError) as e:
                kept = Path(ctx["scratch"]) / f"sound-{cue['id']}-{time.strftime('%H%M%S')}-{os.getpid()}.{fmt or 'bin'}"
                kept.write_bytes(audio)
                entry.update(filed=None, kept_in_scratch=str(kept), filing_error=str(e))
                filed = None
        with open(log, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    os.close(dfd)
    if not audio:
        refuse(f"no sound was made ({res['error']}); logged to {log.name}")
    if filed is None:
        refuse(f"the take came back but could not be filed ({entry['filing_error']}); kept at {entry['kept_in_scratch']}, "
               f"and it counts as a take; logged to {log.name}")
    t = tally(job_log(ctx["engagement"]))
    print(f"{filed} sha256 {entry['sha256']} · {cue['id']} take {entry['take']} of {TAKES_PER_CUE} · "
          f"job spend ${t['usd']:.2f} of ${c['usd_cap']:.2f}, {t['credits']} of {c['credits_cap']} credits")
    if res.get("words"):
        print("Lyria also answered with text (lyrics or structure): listen for sung words before the take goes in the "
              "cut; words in the film are Sean's (rule 8). The text is in the sidecar.")


if __name__ == "__main__":
    main()
