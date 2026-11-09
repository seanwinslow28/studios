"""A small client for generated sound: ElevenLabs sound effects, Lyria music on the Gemini API, and the ElevenLabs balance.

    python3 sound_client.py effect "<prompt>" <out.mp3> [--seconds S] [--loop] [--influence 0-1]
    python3 sound_client.py music "<prompt>" <out> [--model lyria-3-clip-preview | lyria-3.5]
    python3 sound_client.py credits

Also importable: make_effect, make_music, credits_used.

Keys come from the environment (ELEVENLABS_API_KEY, GEMINI_API_KEY), or else from the keys file at
~/.config/audio-keys/keys.env (KEY=value lines, `export` allowed). A key is read here and never printed, logged or
written anywhere. Only the text prompt is sent, never a file.

ElevenLabs: model eleven_text_to_sound_v2, mp3 at 192 kb/s (the best the Creator plan allows; WAV needs Pro).
Its pages disagree on cost (200 credits a take, or 40 a second when a length is set), so the effect command reads the
account's count before and after the take. The count moves some seconds after a take, so it is read until it moves.
Lyria: the Gemini API's Interactions endpoint, paid tier, billed per call (as priced in October 2026: $0.04 for
lyria-3-clip-preview, $0.08 for lyria-3.5). Lyria may answer with text too, lyrics or structure: listen for sung
words before a take goes in the cut. The music command writes the file as MP3 or WAV, whichever came back.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Dict, Optional, Tuple

KEYS_FILE = Path(os.path.expanduser("~/.config/audio-keys/keys.env"))
EFFECTS_URL = "https://api.elevenlabs.io/v1/sound-generation"
EFFECTS_MODEL = "eleven_text_to_sound_v2"
EFFECTS_FORMAT = "mp3_44100_192"
SUBSCRIPTION_URL = "https://api.elevenlabs.io/v1/user/subscription"
MUSIC_URL = "https://generativelanguage.googleapis.com/v1beta/interactions"
MUSIC_PRICES_USD = {"lyria-3-clip-preview": 0.04, "lyria-3.5": 0.08}
METER_WAIT_S, METER_POLL_S = 90, 3
TIMEOUT_S = 300


class SoundError(RuntimeError):
    """A key is missing, or the service gave no sound."""


def key(name: str, keys_file: Path = KEYS_FILE) -> str:
    """One key, from the environment or the keys file; never printed."""
    if os.environ.get(name):
        return os.environ[name]
    if keys_file.is_file():
        for line in keys_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("export "):
                line = line[len("export "):]
            k, sep, v = line.partition("=")
            if sep and k.strip() == name and v.strip():
                return v.strip().strip("'\"")
    raise SoundError(f"no {name} in the environment or in {keys_file}")


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
    return f"HTTP {status}: " + " ".join(body.decode("utf-8", "replace").split())[:300]


def credits_used() -> Optional[Tuple[int, int]]:
    """The ElevenLabs account's credits used this month and its limit, or None."""
    status, body = http("GET", SUBSCRIPTION_URL, {"xi-api-key": key("ELEVENLABS_API_KEY")}, None)
    try:
        d = json.loads(body) if status == 200 else {}
        return int(d["character_count"]), int(d["character_limit"])
    except (ValueError, KeyError, TypeError):
        return None


def settled(before: Optional[Tuple[int, int]], wait_s: float = METER_WAIT_S) -> Optional[Tuple[int, int]]:
    """The account's count once it has moved past `before`, or its last read when it has not in `wait_s`."""
    deadline = time.time() + wait_s
    while True:
        after = credits_used()
        if not before or (after and after[0] != before[0]) or time.time() >= deadline:
            return after
        time.sleep(METER_POLL_S)


def effect_body(prompt: str, seconds: Optional[float] = None, loop: bool = False,
                influence: Optional[float] = None) -> Dict:
    """The JSON ElevenLabs takes for one sound effect."""
    if not prompt.strip():
        raise SoundError("a sound effect needs a prompt")
    if seconds is not None and not 0.5 <= seconds <= 30:
        raise SoundError("a sound effect is 0.5 to 30 seconds long, or left to the model")
    if influence is not None and not 0 <= influence <= 1:
        raise SoundError("prompt influence is 0 to 1")
    body = {"text": prompt, "model_id": EFFECTS_MODEL, "loop": bool(loop)}
    if seconds is not None:
        body["duration_seconds"] = seconds
    if influence is not None:
        body["prompt_influence"] = influence
    return body


def make_effect(prompt: str, seconds: Optional[float] = None, loop: bool = False,
                influence: Optional[float] = None) -> bytes:
    """One ElevenLabs sound effect, as MP3 bytes."""
    body = effect_body(prompt, seconds, loop, influence)
    status, data = http("POST", f"{EFFECTS_URL}?output_format={EFFECTS_FORMAT}",
                        {"xi-api-key": key("ELEVENLABS_API_KEY"), "Content-Type": "application/json",
                         "Accept": "audio/mpeg"}, json.dumps(body).encode())
    if status != 200 or not data:
        raise SoundError(f"no sound effect came back ({why(status, data)})")
    return data


def music_answer(doc: object) -> Tuple[Optional[bytes], list]:
    """The first audio in a Lyria answer, and any text that came with it."""
    audio, words = None, []

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
    return audio, words


def make_music(prompt: str, model: str = "lyria-3-clip-preview") -> Tuple[bytes, list]:
    """One Lyria take: its audio bytes and any text (lyrics or structure) it answered with."""
    if model not in MUSIC_PRICES_USD:
        raise SoundError(f"the music model is one of {', '.join(MUSIC_PRICES_USD)}")
    if not prompt.strip():
        raise SoundError("a music take needs a prompt")
    status, data = http("POST", MUSIC_URL, {"x-goog-api-key": key("GEMINI_API_KEY"), "Content-Type": "application/json"},
                        json.dumps({"model": model, "input": prompt}).encode())
    if status != 200:
        raise SoundError(f"no music came back ({why(status, data)})")
    try:
        doc = json.loads(data)
    except ValueError:
        doc = {}
    audio, words = music_answer(doc)
    if audio is None:
        raise SoundError("Lyria answered with no audio")
    return audio, words


def sniff(data: bytes) -> Optional[str]:
    """mp3 or wav, from the bytes, or None."""
    if data[:3] == b"ID3" or (len(data) > 1 and data[0] == 0xFF and data[1] & 0xE0 == 0xE0):
        return "mp3"
    if data[:4] == b"RIFF" and data[8:12] == b"WAVE":
        return "wav"
    return None


def write_new(path: Path, data: bytes) -> Path:
    """Write a new file, never over one already there."""
    with open(path, "xb") as f:
        f.write(data)
    return path


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    fx = sub.add_parser("effect", help="one ElevenLabs sound effect")
    fx.add_argument("prompt")
    fx.add_argument("out")
    fx.add_argument("--seconds", type=float)
    fx.add_argument("--loop", action="store_true")
    fx.add_argument("--influence", type=float)
    mu = sub.add_parser("music", help="one Lyria music take")
    mu.add_argument("prompt")
    mu.add_argument("out")
    mu.add_argument("--model", default="lyria-3-clip-preview", choices=sorted(MUSIC_PRICES_USD))
    sub.add_parser("credits", help="the ElevenLabs credits used this month, and the limit")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "credits":
            c = credits_used()
            print("could not read the account" if c is None else f"{c[0]} of {c[1]} credits used this month")
            return 0 if c else 1
        out = Path(a.out)
        if out.exists():
            raise SoundError(f"{out} exists; a take is written once")
        if a.cmd == "effect":
            before = credits_used()
            data = make_effect(a.prompt, a.seconds, a.loop, a.influence)
            write_new(out, data)
            after = settled(before)
            spent = f"{after[0] - before[0]} credits" if before and after else "credits unread"
            print(f"wrote {out} ({len(data)} bytes, {spent})")
        else:
            data, words = make_music(a.prompt, a.model)
            kind = sniff(data) or "bin"
            out = write_new(out.with_suffix("." + kind), data)
            print(f"wrote {out} ({len(data)} bytes, about ${MUSIC_PRICES_USD[a.model]:.2f})")
            if words:
                print("Lyria also answered with text; listen for sung words:", " ".join(words)[:500])
    except SoundError as e:
        print(f"sound_client.py: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
