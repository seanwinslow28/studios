"""Generates the sound-effect palette (palette.json) with ElevenLabs sound effects, POST /v1/sound-generation.
Each sound is made in palette['n'] variants from its prompt and length; existing files are kept, so a re-run only fills gaps.
The key comes from the environment (source ~/.config/audio-keys/keys.env first) and is never printed or saved.
Writes sfx/<key>-<n>.wav and sfx/log.json (prompts as sent; the account's character count before and after).
Run from the job's sound folder (palette.json inside it, in the shape build_mix.py reads) with the job's .venv python:
make_sfx.py [keys…]"""
import json
import os
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

if sys.argv[1:2] in (["-h"], ["--help"]):
    sys.exit(print(__doc__) or 0)

HERE = Path.cwd()  # the job's sound folder
OUT = HERE / "sfx"
KEY = os.environ.get("ELEVENLABS_API_KEY") or sys.exit("make_sfx.py: set ELEVENLABS_API_KEY first (source ~/.config/audio-keys/keys.env)")
PAL = json.loads((HERE / "palette.json").read_text())["sounds"]


def used():
    r = urllib.request.Request("https://api.elevenlabs.io/v1/user/subscription", headers={"xi-api-key": KEY})
    with urllib.request.urlopen(r, timeout=60) as f:
        return json.loads(f.read())["character_count"]


def make(job):
    key, n, s = job
    out = OUT / f"{key}-{n}.wav"
    if out.exists():
        return key, n, "kept"
    body = {"text": s["prompt"], "duration_seconds": s["dur"], "prompt_influence": 0.6, "model_id": "eleven_text_to_sound_v2"}
    req = urllib.request.Request("https://api.elevenlabs.io/v1/sound-generation?output_format=wav_48000", method="POST",
                                 data=json.dumps(body).encode(), headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as f:
            out.write_bytes(f.read())
        return key, n, "made"
    except urllib.error.HTTPError as e:
        return key, n, f"error {e.code}: {e.read()[:300]!r}"


keys = sys.argv[1:] or list(PAL)
OUT.mkdir(exist_ok=True)
before = used()
jobs = [(k, n, PAL[k]) for k in keys for n in range(1, PAL[k]["n"] + 1)]
with ThreadPoolExecutor(4) as ex:
    for key, n, status in ex.map(make, jobs):
        print(key, n, status)
after = used()
log = json.loads((OUT / "log.json").read_text()) if (OUT / "log.json").exists() else {"runs": []}
log["runs"].append({"keys": keys, "characters_before": before, "characters_after": after, "this_run": after - before})
log["prompts"] = {k: {"prompt": v["prompt"], "duration_seconds": v["dur"], "prompt_influence": 0.6, "model_id": "eleven_text_to_sound_v2"} for k, v in PAL.items()}
(OUT / "log.json").write_text(json.dumps(log, indent=1))
print("character count moved by", after - before)
