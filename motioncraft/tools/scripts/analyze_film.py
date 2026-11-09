"""Per-frame and audio measurements for a reference film.

Usage:
  python3 analyze_film.py <video.mp4> <out_dir>

Writes:
  frames.csv   per-frame: t, mad (mean abs diff vs previous), hist (HSV hist distance),
               bg (median border colour as hex), motion (mean optical-flow magnitude)
  cuts.csv     candidate hard cuts (hist spike) and soft transitions (sustained mad)
  audio.csv    20 ms windows: t, rms_db, flux (onset strength)
  onsets.csv   peak-picked onsets with strength
  summary.json tempo estimate from onset autocorrelation, loudness range, cut list

Measurements only. Interpretation (what a shot means, what easing it uses) is done
by a person looking at the contact sheets; nothing here claims to know easing curves.
"""
import csv
import json
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from scipy.signal import find_peaks


def wants_help(min_args):
    """True when the command line asks for help or gives too few arguments."""
    args = sys.argv[1:]
    return bool(args[:1] and args[0] in ("-h", "--help")) or len(args) < min_args


def frame_metrics(video: Path, out: Path):
    cap = cv2.VideoCapture(str(video))
    fps = cap.get(cv2.CAP_PROP_FPS)
    rows, prev_gray, prev_hist = [], None, None
    i = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        small = cv2.resize(frame, (320, 180), interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0, 1], None, [32, 16], [0, 180, 0, 256])
        cv2.normalize(hist, hist)
        border = np.concatenate([small[:6].reshape(-1, 3), small[-6:].reshape(-1, 3),
                                 small[:, :6].reshape(-1, 3), small[:, -6:].reshape(-1, 3)])
        b, g, r = np.median(border, axis=0).astype(int)
        mad = hd = mot = 0.0
        if prev_gray is not None:
            mad = float(np.mean(cv2.absdiff(gray, prev_gray)))
            hd = float(cv2.compareHist(prev_hist, hist, cv2.HISTCMP_BHATTACHARYYA))
            flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            mot = float(np.mean(np.linalg.norm(flow, axis=2)))
        rows.append(dict(frame=i, t=round(i / fps, 3), mad=round(mad, 3), hist=round(hd, 4),
                         bg=f"#{r:02x}{g:02x}{b:02x}", motion=round(mot, 3)))
        prev_gray, prev_hist = gray, hist
        i += 1
    with open(out / "frames.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    return rows, fps


def find_cuts(rows, fps):
    hist = np.array([r["hist"] for r in rows])
    mad = np.array([r["mad"] for r in rows])
    cuts = []
    # Hard cut: one-frame histogram spike well above its local neighbourhood.
    for i in range(1, len(rows)):
        lo, hi = max(1, i - 6), min(len(rows), i + 7)
        neigh = np.median(np.delete(hist[lo:hi], i - lo))
        if hist[i] > 0.25 and hist[i] > 4 * max(neigh, 0.01):
            cuts.append(dict(frame=i, t=rows[i]["t"], kind="hard", hist=rows[i]["hist"], mad=rows[i]["mad"],
                             bg_before=rows[i - 1]["bg"], bg_after=rows[i]["bg"]))
    return cuts


def audio_metrics(video: Path, out: Path):
    wav = out / "audio_mono_22k.f32"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-ac", "1", "-ar", "22050",
                    "-f", "f32le", str(wav)], check=True)
    x = np.fromfile(wav, dtype=np.float32)
    wav.unlink()
    sr, hop, win = 22050, 441, 1024  # 20 ms hop
    n = 1 + (len(x) - win) // hop
    frames = np.lib.stride_tricks.as_strided(x, shape=(n, win), strides=(x.strides[0] * hop, x.strides[0]))
    rms = np.sqrt(np.mean(frames ** 2, axis=1) + 1e-12)
    spec = np.abs(np.fft.rfft(frames * np.hanning(win), axis=1))
    logspec = np.log1p(spec)
    flux = np.concatenate([[0], np.maximum(0, np.diff(logspec, axis=0)).sum(axis=1)])
    flux = flux / (flux.max() + 1e-9)
    t = np.arange(n) * hop / sr
    with open(out / "audio.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t", "rms_db", "flux"])
        for ti, r, fl in zip(t, rms, flux):
            w.writerow([round(ti, 3), round(20 * np.log10(r), 2), round(float(fl), 4)])
    peaks, props = find_peaks(flux, height=0.18, distance=5)
    with open(out / "onsets.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t", "strength"])
        for p in peaks:
            w.writerow([round(t[p], 3), round(float(flux[p]), 3)])
    # Tempo: autocorrelation of onset envelope between 60 and 180 BPM.
    env = flux - flux.mean()
    ac = np.correlate(env, env, mode="full")[len(env) - 1:]
    hop_s = hop / sr
    lags = np.arange(len(ac)) * hop_s
    band = (lags >= 60 / 180) & (lags <= 60 / 60)
    best = lags[band][np.argmax(ac[band])]
    return dict(tempo_bpm_estimate=round(60 / best, 1), onset_count=int(len(peaks)),
                rms_db_p95=round(float(np.percentile(20 * np.log10(rms), 95)), 1),
                rms_db_p10=round(float(np.percentile(20 * np.log10(rms), 10)), 1))


def main():
    if wants_help(2):
        sys.exit(print(__doc__) or 0)
    video, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    rows, fps = frame_metrics(video, out)
    cuts = find_cuts(rows, fps)
    with open(out / "cuts.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["frame", "t", "kind", "hist", "mad", "bg_before", "bg_after"])
        w.writeheader()
        w.writerows(cuts)
    audio = audio_metrics(video, out)
    summary = dict(video=video.name, fps=fps, frames=len(rows), cuts=[c["t"] for c in cuts], **audio)
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
