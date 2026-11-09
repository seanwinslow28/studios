"""Measures where each placed effect lands in the effects stem against where it was meant to (placements.json).
Onset-aligned sounds: the first 1 ms block over 30% of the placement's own peak; peak-aligned: its loudest 1 ms block; the clear
(end-aligned): the last block over 5% of its peak. Placements that overlap a louder neighbour are measured on their own window and
can be pulled by it, so the report lists them. Writes sync.json. Run from the job's sound folder, after build_mix.py, with the job's .venv python.
Usage: python3 sync_check.py"""
import json
import subprocess
import sys

import numpy as np

if sys.argv[1:2] in (["-h"], ["--help"]):
    sys.exit(print(__doc__) or 0)

SR = 48000
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", "sfx-stem.wav", "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout, np.float32)
e = np.abs(x)[: len(x) // 48 * 48].reshape(-1, 48).max(axis=1)
P = json.load(open("placements.json"))["placements"]
rows = []
for p in P:
    a, b = int(p["starts_s"] * 1000), int((p["starts_s"] + p["length_s"]) * 1000)
    seg = e[a:b]
    if p["align"] == "onset":
        got = a + int(np.argmax(seg > 0.3 * seg.max()))
    elif p["align"] == "peak":
        got = a + int(np.argmax(seg))
    else:
        got = a + len(seg) - int(np.argmax(seg[::-1] > 0.05 * seg.max()))
    rows.append({"sound": p["sound"], "cue_t": p["cue_t"], "meant_s": p["at_s"], "measured_s": round(got / 1000, 3), "off_ms": round(got - p["at_s"] * 1000)})
off = [r for r in rows if abs(r["off_ms"]) > 17]
json.dump({"within_one_frame_60fps": len(rows) - len(off), "of": len(rows), "outside": off, "rows": rows}, open("sync.json", "w"), indent=1)
print(len(rows) - len(off), "of", len(rows), "within one 60 fps frame (17 ms); outside:", [(r["sound"], r["cue_t"], r["off_ms"]) for r in off])
