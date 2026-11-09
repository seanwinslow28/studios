"""Colour accuracy, in CIEDE2000 (ΔE00), for a film's finish.

Decodes a frame with the BT.709 matrix and video range (as every master here is tagged) and compares mean colours, treating code
values as sRGB-encoded like the design values. Two uses:
  chart:  python3 measure_colour.py chart <palette.json> <video> [<reference video>]
          each patch of a chart made by make_chart.py against its design hex, or against the same patch in a reference video;
  fields: python3 measure_colour.py fields <video> <hex> <time s> <y0> <y1> <x0> <x1> [<hex> <time> <y0> <y1> <x0> <x1> ...]
          flat regions of the film at given instants against their design hex.
Also importable: frame, to_lab, de00.
"""
import json
import subprocess
import sys

import numpy as np


def wants_help(min_args):
    """True when the command line asks for help or gives too few arguments."""
    args = sys.argv[1:]
    return bool(args[:1] and args[0] in ("-h", "--help")) or len(args) < min_args


def frame(path, t=0.5):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", str(path), "-frames:v", "1", "-vf",
                          "scale=in_color_matrix=bt709:in_range=tv:flags=accurate_rnd+full_chroma_int", "-f", "rawvideo", "-pix_fmt", "rgb48le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint16).reshape(1080, 1920, 3).astype(np.float64) / 65535.0


def to_lab(rgb):
    rgb = np.asarray(rgb, np.float64)
    lin = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.4124564, 0.3575761, 0.1804375], [0.2126729, 0.7151522, 0.0721750], [0.0193339, 0.1191920, 0.9503041]])
    xyz = lin @ m.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > (6 / 29) ** 3, np.cbrt(xyz), xyz / (3 * (6 / 29) ** 2) + 4 / 29)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


def de00(lab1, lab2):
    L1, a1, b1 = np.moveaxis(np.asarray(lab1), -1, 0)
    L2, a2, b2 = np.moveaxis(np.asarray(lab2), -1, 0)
    C1, C2 = np.hypot(a1, b1), np.hypot(a2, b2)
    Cm = (C1 + C2) / 2
    G = 0.5 * (1 - np.sqrt(Cm ** 7 / (Cm ** 7 + 25 ** 7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = np.hypot(a1p, b1), np.hypot(a2p, b2)
    h1p, h2p = np.degrees(np.arctan2(b1, a1p)) % 360, np.degrees(np.arctan2(b2, a2p)) % 360
    dLp, dCp = L2 - L1, C2p - C1p
    dh = h2p - h1p
    dh = np.where(C1p * C2p == 0, 0, np.where(dh > 180, dh - 360, np.where(dh < -180, dh + 360, dh)))
    dHp = 2 * np.sqrt(C1p * C2p) * np.sin(np.radians(dh / 2))
    Lpm, Cpm = (L1 + L2) / 2, (C1p + C2p) / 2
    hs = h1p + h2p
    hpm = np.where(C1p * C2p == 0, hs, np.where(np.abs(h1p - h2p) > 180, np.where(hs < 360, (hs + 360) / 2, (hs - 360) / 2), hs / 2))
    T = 1 - 0.17 * np.cos(np.radians(hpm - 30)) + 0.24 * np.cos(np.radians(2 * hpm)) + 0.32 * np.cos(np.radians(3 * hpm + 6)) - 0.20 * np.cos(np.radians(4 * hpm - 63))
    dth = 30 * np.exp(-(((hpm - 275) / 25) ** 2))
    Rc = 2 * np.sqrt(Cpm ** 7 / (Cpm ** 7 + 25 ** 7))
    Sl = 1 + 0.015 * (Lpm - 50) ** 2 / np.sqrt(20 + (Lpm - 50) ** 2)
    Sc, Sh = 1 + 0.045 * Cpm, 1 + 0.015 * Cpm * T
    Rt = -np.sin(np.radians(2 * dth)) * Rc
    return np.sqrt((dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2 + Rt * (dCp / Sc) * (dHp / Sh))


def rgb(h):
    return np.array([int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)])


def main():
    if wants_help(3):
        sys.exit(print(__doc__) or 0)
    mode = sys.argv[1]
    if mode == "chart":
        pal = json.load(open(sys.argv[2]))["patches"]
        img = frame(sys.argv[3])
        ref = frame(sys.argv[4]) if len(sys.argv) > 4 else None
        for p in pal:
            x, y = p["centre"]
            got = img[y - 30:y + 30, x - 30:x + 30].reshape(-1, 3).mean(0)
            want = ref[y - 30:y + 30, x - 30:x + 30].reshape(-1, 3).mean(0) if ref is not None else rgb(p["hex"])
            print(f'{p["name"]}: {float(de00(to_lab(got), to_lab(want))):.2f}')
    else:
        video, args = sys.argv[2], sys.argv[3:]
        for i in range(0, len(args), 6):
            hx, t, y0, y1, x0, x1 = args[i], float(args[i + 1]), *map(int, args[i + 2:i + 6])
            got = frame(video, t)[y0:y1, x0:x1].reshape(-1, 3).mean(0)
            print(f"{hx} at {t} s: {float(de00(to_lab(got), to_lab(rgb(hx)))):.2f} (read {np.round(got * 255, 1).tolist()})")


if __name__ == "__main__":
    main()
