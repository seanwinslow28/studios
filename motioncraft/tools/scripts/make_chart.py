"""Makes a palette chart for colour tests: one flat patch per colour of the film (up to 20, five across), 2 s at 60 fps,
ProRes 422 HQ 10-bit tagged BT.709 like the film's masters, and writes the patches' places back into the palette file.
The palette file is JSON: {"patches": [{"name": "...", "hex": "#RRGGBB"}, ...]} (design values, sRGB-encoded 8-bit).
Usage: python3 make_chart.py <palette.json> <out chart.mov>
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np


def wants_help(min_args):
    """True when the command line asks for help or gives too few arguments."""
    args = sys.argv[1:]
    return bool(args[:1] and args[0] in ("-h", "--help")) or len(args) < min_args

COLS, ROWS, W, H = 5, 4, 1920, 1080


def hexrgb(h):
    return [int(h[i:i + 2], 16) for i in (1, 3, 5)]


def main():
    if wants_help(2):
        sys.exit(print(__doc__) or 0)
    pal_path, out = Path(sys.argv[1]), Path(sys.argv[2])
    pal = json.loads(pal_path.read_text())
    img = np.full((H, W, 3), 128.0)
    pw, ph = W // COLS, H // ROWS
    for k, p in enumerate(pal["patches"][:COLS * ROWS]):
        c, r = k % COLS, k // COLS
        x0, y0 = c * pw + 12, r * ph + 12
        img[y0:y0 + ph - 24, x0:x0 + pw - 24] = hexrgb(p["hex"])
        p["centre"] = [x0 + (pw - 24) // 2, y0 + (ph - 24) // 2]
    frame = np.clip(img * 257 + 0.5, 0, 65535).astype(np.uint16).tobytes()
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb48le", "-s", f"{W}x{H}", "-r", "60", "-i", "-",
                            "-vf", "scale=out_color_matrix=bt709:out_range=tv,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv",
                            "-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le", "-colorspace", "bt709", "-color_primaries", "bt709",
                            "-color_trc", "bt709", "-color_range", "tv", str(out)], stdin=subprocess.PIPE)
    for _ in range(120):
        enc.stdin.write(frame)
    enc.stdin.close()
    enc.wait()
    pal_path.write_text(json.dumps(pal, indent=1))
    print("wrote", out, "and patch centres into", pal_path)


if __name__ == "__main__":
    main()
