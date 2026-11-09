"""True motion blur by temporal supersampling: average the renders of the instants inside each frame's shutter.

Four HyperFrames renders at 240 fps, the timeline of render j shifted later by j/960 s (window.TOFF), interleave into
960 samples a second: stream j's frame k shows the instant k/240 - j/960. Output frame m (time m/60) averages the
samples inside a shutter centred on m/60. At 180 degrees that is 8 samples spanning 1/120 s, as a film camera would.

It also writes, if asked, the clean average as a 10-bit ProRes 422 HQ master with no grain (--prores out.mov), so a finish starts
one lossy generation earlier, and adds living grain to the review master after the averaging (--grain sigma, in 8-bit levels):
zero-mean, so it never darkens a colour (a multiplied grain texture darkens everything about 2.5%), monochrome, about two pixels
across (a 2 x 2 box over white noise), and new on every frame.
The four sample renders must be named <renders dir>/sub-<j>-240.mp4, j = 0..3.
Usage: python3 motion_blur.py <renders dir> <out.mp4> <seconds> [shutter degrees] [--prores out.mov] [--grain 1.6]
"""
import subprocess
import sys
from pathlib import Path

import numpy as np


def wants_help(min_args):
    """True when the command line asks for help or gives too few arguments."""
    args = sys.argv[1:]
    return bool(args[:1] and args[0] in ("-h", "--help")) or len(args) < min_args

W, H, FPS, SUB = 1920, 1080, 60, 16  # 16 samples per 60 fps frame at 960 a second
TAGS = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
OUTVF = "scale=out_color_matrix=bt709:out_range=tv,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv"


class Stream:
    """Reads one 240 fps render forward, keeping the last few frames, so a frame can be asked for more than once."""

    def __init__(self, path):
        # Decoded with the BT.709 matrix the renders are tagged with, and encoded back with it below.
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(path), "-vf", "scale=in_color_matrix=bt709:in_range=tv",
                                   "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                                  stdout=subprocess.PIPE)
        self.frames, self.next, self.last = {}, 0, None

    def get(self, k):
        k = max(0, k)
        while self.next <= k:
            buf = self.p.stdout.read(W * H * 3)
            if len(buf) < W * H * 3:
                return self.frames.get(self.last)  # past the end: hold the last frame
            self.frames[self.next] = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
            self.last = self.next
            self.next += 1
            for old in [x for x in self.frames if x < self.next - 6]:
                del self.frames[old]
        return self.frames[k]


def opt(name, default=None):
    if name in sys.argv:
        return sys.argv[sys.argv.index(name) + 1]
    return default


def main():
    if wants_help(3):
        sys.exit(print(__doc__) or 0)
    pos = [a for i, a in enumerate(sys.argv[1:], 1) if not a.startswith("--") and not sys.argv[i - 1].startswith("--")]
    src, out, seconds = Path(pos[0]), pos[1], float(pos[2])
    angle = float(pos[3]) if len(pos) > 3 else 180.0
    prores, grain = opt("--prores"), float(opt("--grain", "0"))
    n_open = max(1, round(SUB * angle / 360))  # samples inside the shutter
    offsets = [d - n_open // 2 for d in range(n_open)]  # centred on the frame's instant
    streams = [Stream(src / f"sub-{j}-240.mp4") for j in range(4)]
    n_frames = round(seconds * FPS)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-vf", OUTVF, "-c:v", "libx264", "-crf", "12", "-preset", "slow",
                            "-pix_fmt", "yuv420p", *TAGS, "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    pro = None
    if prores:
        pro = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb48le", "-s", f"{W}x{H}", "-r", str(FPS),
                                "-i", "-", "-vf", OUTVF, "-c:v", "prores_ks", "-profile:v", "3", "-vendor", "apl0",
                                "-pix_fmt", "yuv422p10le", *TAGS, prores], stdin=subprocess.PIPE)
    rng = np.random.default_rng(7)
    for m in range(n_frames):
        acc = np.zeros((H, W, 3), np.float32)
        for d in offsets:
            n = SUB * m + d
            j = (-n) % 4
            k = (n + j) // 4
            acc += streams[j].get(k)
        acc /= len(offsets)
        if pro:  # the clean average at 16 bits: no grain, no dither needed at 10-bit output
            pro.stdin.write(np.clip(acc * 257.0 + 0.5, 0, 65535).astype(np.uint16).tobytes())
        if grain:
            g = rng.standard_normal((H + 1, W + 1)).astype(np.float32)
            g = (g[:-1, :-1] + g[1:, :-1] + g[:-1, 1:] + g[1:, 1:]) * (grain / 2.0)  # 2 x 2 box: grains about two pixels across
            acc += g[:, :, None]
        # Triangular dither before rounding, so the averaged soft edges don't band.
        acc += rng.random(acc.shape, np.float32) - rng.random(acc.shape, np.float32)
        enc.stdin.write(np.clip(acc + 0.5, 0, 255).astype(np.uint8).tobytes())
    enc.stdin.close()
    enc.wait()
    if pro:
        pro.stdin.close()
        pro.wait()
    print("wrote", out, (prores or ""), n_frames, "frames,", len(offsets), "samples each at", angle, "degrees; grain", grain)


if __name__ == "__main__":
    main()
