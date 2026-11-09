"""Per-frame motion check for a rendered clip.
Writes <out>/diff.csv (frame, mean abs difference to the previous frame on a 480 px grey copy) and prints:
  - spikes: a frame whose difference is > 4x the larger of its two neighbours and > 2.0 (a cut or a jump);
  - stalls: a zero-difference frame with moving frames on both sides (a duplicated frame mid-motion).
Also saves frames for the given ranges as JPEG (<out>/frames/frame_000NNN.jpg, 1-based like HyperFrames)
and phone-width (390 px) copies of the listed single frames.
Usage: motion_check.py <video> <out_dir> --ranges a-b,c-d --phone f1,f2"""
import argparse, csv, os
import cv2
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("out")
ap.add_argument("--ranges", default=""); ap.add_argument("--phone", default="")
a = ap.parse_args()
os.makedirs(os.path.join(a.out, "frames"), exist_ok=True)
os.makedirs(os.path.join(a.out, "phone"), exist_ok=True)
keep = set()
for r in filter(None, a.ranges.split(",")):
    lo, hi = map(int, r.split("-")); keep.update(range(lo, hi + 1))
phone = set(int(x) for x in filter(None, a.phone.split(",")))

cap = cv2.VideoCapture(a.video)
prev, diffs, n = None, [], 0
while True:
    ok, fr = cap.read()
    if not ok:
        break
    g = cv2.cvtColor(cv2.resize(fr, (480, 270), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY).astype(np.float32)
    diffs.append(0.0 if prev is None else float(np.mean(np.abs(g - prev))))
    prev = g
    if n in keep:
        cv2.imwrite(os.path.join(a.out, "frames", f"frame_{n + 1:06d}.jpg"), fr, [cv2.IMWRITE_JPEG_QUALITY, 92])
    if n in phone:
        w = 390; h = round(fr.shape[0] * w / fr.shape[1])
        cv2.imwrite(os.path.join(a.out, "phone", f"phone_f{n}.png"), cv2.resize(fr, (w, h), interpolation=cv2.INTER_AREA))
    n += 1
with open(os.path.join(a.out, "diff.csv"), "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["frame", "diff"]); w.writerows(enumerate(diffs))
d = np.array(diffs)
spikes = [i for i in range(1, len(d) - 1) if d[i] > 2.0 and d[i] > 4 * max(d[i - 1], d[i + 1], 0.05)]
stalls = [i for i in range(1, len(d) - 1) if d[i] < 1e-3 and d[i - 1] > 0.05 and d[i + 1] > 0.05]
print(f"frames {n}; max diff {d.max():.2f} at f{int(d.argmax())}; median moving diff {np.median(d[d > 0.01]):.3f}")
print("spikes:", spikes or "none")
print("stalls:", stalls or "none")
