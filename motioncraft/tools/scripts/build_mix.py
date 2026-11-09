"""Places the sound effects on the picture's cues and lays them over the locked sound (a folder holding mix.wav and voice.wav;
the first argument, or the SOUND environment variable).
1. Every variant in sfx/ is measured: where its first transient is (first 1 ms block over 8% of its peak), how fast it reaches its peak,
   its crest (peak over RMS), how long it rings (until it stays 45 dB under its peak) and how much of its energy lands in the first 0.25 s.
   Impulsive sounds (align 'onset') score on attack, crest and a short ring; swishes ('peak', 'end') on a single clear peak.
   The best two variants rotate on repeated cues; a single cue gets the best one. I can't listen, so this is measurement, not taste.
2. Each placement is trimmed (3 ms before the transient, a 25 ms fade where the ring ends), panned (constant power, at 60% of the
   object's position on screen) and placed so its onset, peak or end sits on cue + offset. Its level is ridden against the locked mix
   around it, as a mixer rides a fader: its RMS over 240 ms at its peak sits rel_db under the mix's RMS there (big transitions 3 to 6 dB
   under, small pops about 12 dB under), 3 dB lower again where the voice is speaking, never peaking above -8 dBFS. (A first pass at
   fixed peak levels left most effects 25 to 40 dB under the mix: inaudible.)
3. The locked mix itself is not changed: effects + mix, then one fixed gain so the whole sits at -16 LUFS, then a peak limiter at
   -2.5 dBFS (latency compensated) for the few effects that land on a loud music peak, keeping the true peak under -1 dBFS.
Writes sfx-stem.wav, mix.wav, placements.json (every placement, its variant and the measured peak time) and choices.json.
palette.json: {"sounds": {"<key>": {"n": takes, "prompt": "...", "dur": s, "align": "onset" | "peak" | "end", "offset": s, "rel_db": dB,
"cues": ["<cue name>[:<extra offset s>]", "arrive:<kind>"]}}}. cues.json: {"cues": [{"name": "...", "t": s, "kind": "...", "pan": -1 to 1}]},
read from the scene's cue list after any timing change.
Run from the job's sound folder (palette.json, cues.json and sfx/ inside it) with the job's .venv python:
build_mix.py <locked sound folder>"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

if sys.argv[1:2] in (["-h"], ["--help"]):
    sys.exit(print(__doc__) or 0)

HERE = Path.cwd()  # the job's sound folder: palette.json, cues.json and sfx/
SOUND = Path(sys.argv[1] if len(sys.argv) > 1 else os.environ["SOUND"])  # the locked sound: mix.wav and voice.wav
PAL = json.loads((HERE / "palette.json").read_text())["sounds"]
CUES = json.loads((HERE / "cues.json").read_text())["cues"]
SR = 48000
LEN = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(SOUND / "mix.wav")], capture_output=True, text=True).stdout)  # the film's length, from the locked mix
N = int(round(LEN * SR))


def load(p):
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(out, np.float32).reshape(-1, 2).astype(np.float64)


def env1ms(x):
    m = np.abs(x).max(axis=1)
    b = SR // 1000
    return m[: len(m) // b * b].reshape(-1, b).max(axis=1)


def measure(x):
    e = env1ms(x)
    pk = e.max() + 1e-12
    on = int(np.argmax(e > 0.08 * pk))
    peak = int(np.argmax(e))
    tail = len(e) - int(np.argmax(e[::-1] > pk * 10 ** (-45 / 20)))
    rms = np.sqrt(np.mean(x[on * 48: tail * 48] ** 2)) + 1e-12
    energy = np.cumsum(e[on:] ** 2)
    early = float(energy[min(250, len(energy) - 1)] / energy[-1]) if len(energy) else 0
    # a second peak within 6 dB of the first, 60 ms or more away, marks a swish that isn't one clean movement
    far = np.r_[e[: max(0, peak - 60)], e[peak + 60:]]
    second = float(far.max() / pk) if len(far) else 0
    return {"onset_ms": on, "peak_ms": peak, "attack_ms": peak - on, "ring_ms": tail - on, "crest_db": round(20 * np.log10(pk / rms), 1),
            "early": round(early, 2), "second_peak": round(second, 2), "lead_silence_ms": on, "peak_dbfs": round(20 * np.log10(pk), 1)}


def score(m, align):
    if align == "onset":
        return -m["attack_ms"] / 10 + m["crest_db"] / 3 + 4 * m["early"] - m["ring_ms"] / 400
    return -6 * m["second_peak"] + m["crest_db"] / 4 - abs(m["ring_ms"] - 450) / 300


# 1. Measure and choose.
choices = {}
for key, s in PAL.items():
    rows = []
    for n in range(1, s["n"] + 1):
        p = HERE / "sfx" / f"{key}-{n}.wav"
        if p.exists():
            m = measure(load(p))
            rows.append({"variant": n, **m, "score": round(score(m, s["align"]), 2)})
    rows.sort(key=lambda r: -r["score"])
    choices[key] = {"ranked": rows, "use": [r["variant"] for r in rows[:2]]}
(HERE / "choices.json").write_text(json.dumps(choices, indent=1))

# 2. Place.
cue_map = {}
for key, s in PAL.items():
    for c in s["cues"]:
        name, _, extra = c.partition(":")
        if name == "arrive":
            cue_map[("arrive", extra)] = (key, 0.0)
        else:
            cue_map[(name, None)] = (key, float(extra) if extra else 0.0)
bus = np.zeros((N, 2))
MIXM = load(SOUND / "mix.wav")[:N].mean(axis=1)
VOM = load(SOUND / "voice.wav")[:N].mean(axis=1)
places, turn = [], {}
for c in CUES:
    hit = cue_map.get((c["name"], c.get("kind"))) or cue_map.get((c["name"], None))
    if not hit:
        continue
    key, extra_off = hit
    s = PAL[key]
    use = choices[key]["use"]
    k = turn.get(key, 0)
    turn[key] = k + 1
    v = use[k % len(use)]
    x = load(HERE / "sfx" / f"{key}-{v}.wav")
    m = measure(x)
    a, b = max(0, (m["onset_ms"] - 3) * 48), min(len(x), (m["onset_ms"] + m["ring_ms"]) * 48 + 1200)
    x = x[a:b].copy()
    f_in, f_out = 144, min(1200, len(x) // 3)
    if s["align"] == "end":
        f_out = 240  # the clear cuts off abruptly, as written
    x[:f_in] *= np.linspace(0, 1, f_in)[:, None]
    x[-f_out:] *= np.linspace(1, 0, f_out)[:, None]
    x /= np.abs(x).max() + 1e-12
    if "pan" in c:
        th = (0.6 * c["pan"] + 1) * np.pi / 4
        mono = x.mean(axis=1)
        x = np.c_[mono * np.cos(th), mono * np.sin(th)] * np.sqrt(2)
    t = c["t"] + s["offset"] + extra_off
    anchor = {"onset": 3 * 48, "peak": (m["peak_ms"] - m["onset_ms"] + 3) * 48, "end": len(x)}[s["align"]]
    start = int(round(t * SR)) - anchor
    lo, hi = max(0, start), min(N, start + len(x))
    pk = start + int(np.argmax(np.abs(x).max(axis=1)))
    wa, wb = max(0, pk - 5760), min(N, pk + 5760)
    sfx_db = 20 * np.log10(np.sqrt(np.mean(np.r_[np.zeros(max(0, start - wa)), x[max(0, wa - start): wb - start].mean(axis=1)] ** 2)) + 1e-12)
    mix_db = max(-45.0, 20 * np.log10(np.sqrt(np.mean(MIXM[wa:wb] ** 2)) + 1e-12))
    speaking = 20 * np.log10(np.sqrt(np.mean(VOM[wa:wb] ** 2)) + 1e-12) > -35
    want = mix_db + s["rel_db"] - (3 if speaking else 0)
    gdb = min(want - sfx_db, -8 - 20 * np.log10(np.abs(x).max() + 1e-12))
    x *= 10 ** (gdb / 20)
    bus[lo:hi] += x[lo - start: hi - start]
    places.append({"cue": c["name"], "cue_t": c["t"], "sound": key, "variant": v, "align": s["align"], "at_s": round(t, 3), "starts_s": round(start / SR, 3),
                   "length_s": round(len(x) / SR, 3), "rel_db": s["rel_db"], "speaking": bool(speaking), "gain_db": round(float(gdb), 1), "pan": round(c.get("pan", 0), 2)})

# 3. Sum with the locked mix; one fixed gain.
mix = load(SOUND / "mix.wav")[:N]
tmp = HERE / "tmp.wav"


def write(path, y):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f64le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_s24le", str(path)], input=np.ascontiguousarray(y).tobytes(), check=True)


def lufs(path):
    o = subprocess.run(["ffmpeg", "-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True).stderr.decode()
    s = o[o.rindex("Summary"):]
    return float(re.search(r"I:\s+(-?[\d.]+) LUFS", s).group(1)), float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", s).group(1))


write(tmp, mix + bus)
li, _ = lufs(tmp)
gain = 10 ** ((-16.0 - li) / 20)
write(tmp, (mix + bus) * gain)
# A gentle peak limiter catches the few places where an effect lands on a loud music peak (latency compensated, so nothing moves).
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp), "-af", "alimiter=limit=0.75:attack=1:release=60:level=disabled:latency=1",
                "-c:a", "pcm_s24le", str(HERE / "mix.wav")], check=True)
write(HERE / "sfx-stem.wav", bus * gain)
tmp.unlink()
mi, mp = lufs(HERE / "mix.wav")
si, sp = lufs(HERE / "sfx-stem.wav")
# Where each placement actually peaks in the stem, against where it was meant to sit.
stem_env = env1ms(bus)
for p in places:
    a, b = int(p["starts_s"] * 1000), int((p["starts_s"] + p["length_s"]) * 1000)
    p["measured_peak_s"] = round((a + int(np.argmax(stem_env[a:b]))) / 1000, 3) if b > a else None
info = {"mix_lufs": mi, "mix_true_peak_dbfs": mp, "sfx_stem_lufs": si, "sfx_stem_peak_dbfs": sp, "gain_db_applied_to_sum": round(20 * np.log10(gain), 2),
        "locked_mix_lufs_before": lufs(SOUND / "mix.wav")[0], "placements": len(places), "under_voice_extra_db": 3}
(HERE / "placements.json").write_text(json.dumps({"summary": info, "placements": places}, indent=1))
print(json.dumps(info, indent=1))
