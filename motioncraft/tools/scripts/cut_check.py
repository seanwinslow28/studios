"""Checks that each designed hard cut in a master is a single-frame change.

Reads the frame-difference CSV that motion_check.py writes (frame, diff: mean change from the previous frame on a 480 px grey copy)
and, for each cut time, the first frame after the cut (cuts sit midway between frames, so it is ceil(t * fps)): its change must be
more than four times its neighbours' and above 2. Also lists the largest changes, which should all be designed.
Usage: python3 cut_check.py <diff.csv> <fps> <cut time> [<cut time> ...]
"""
import csv
import math
import sys

if sys.argv[1:2] in (["-h"], ["--help"]) or len(sys.argv) < 4:
    sys.exit(print(__doc__) or 0)

path, fps, cuts = sys.argv[1], float(sys.argv[2]), [float(x) for x in sys.argv[3:]]
rows = [(int(r["frame"]), float(r["diff"])) for r in csv.DictReader(open(path))]
d = dict(rows)
ok_all = True
for t in cuts:
    f = math.ceil(t * fps)
    before, at, after = d.get(f - 1, 0), d.get(f, 0), d.get(f + 1, 0)
    ok = at > 4 * max(before, after) and at > 2
    ok_all &= ok
    print(f"cut at {t:.3f} s: frame {f} diff {at:.2f}; neighbours {before:.2f} and {after:.2f}; single-frame: {ok}")
print("largest changes (frame, s, diff):", [(f, round(f / fps, 3), round(v, 2)) for f, v in sorted(rows, key=lambda r: -r[1])[:12]])
sys.exit(0 if ok_all else 1)
