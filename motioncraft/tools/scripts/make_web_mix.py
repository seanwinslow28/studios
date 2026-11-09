"""Makes the web mix from a master mix: one fixed gain, then a peak limiter run at four times the sample rate (it catches
inter-sample peaks), then AAC 256k, searching the gain and the ceiling until the AAC file itself reads the target loudness
(± 0.15 LU) with a true peak at or under the ceiling. No loudnorm: its linear mode falls back to riding the gain, which can pump.
Writes <out stem>.wav (48 kHz, 24-bit) and <out stem>.m4a, and prints the tries as JSON.
Usage: python3 make_web_mix.py <master mix.wav> <out stem> [target LUFS, default -14] [true-peak ceiling dBTP, default -1.5]
"""
import json
import re
import subprocess
import sys
from pathlib import Path


def wants_help(min_args):
    """True when the command line asks for help or gives too few arguments."""
    args = sys.argv[1:]
    return bool(args[:1] and args[0] in ("-h", "--help")) or len(args) < min_args


def measure(path):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=peak=true:framelog=quiet", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    s = err[err.rindex("Summary:"):]
    return {"lufs": float(re.search(r"I:\s+(-?[\d.]+) LUFS", s).group(1)), "lra": float(re.search(r"LRA:\s+(-?[\d.]+) LU", s).group(1)),
            "true_peak_dbtp": float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", s).group(1))}


def main():
    if wants_help(2):
        sys.exit(print(__doc__) or 0)
    src, stem = Path(sys.argv[1]), sys.argv[2]
    target = float(sys.argv[3]) if len(sys.argv) > 3 else -14.0
    tp_max = float(sys.argv[4]) if len(sys.argv) > 4 else -1.5
    wav, aac = Path(stem + ".wav"), Path(stem + ".m4a")
    s0 = measure(src)
    gain, ceiling, log = target - s0["lufs"], tp_max - 0.5, []
    for _ in range(8):
        lim = 10 ** (ceiling / 20)
        af = f"volume={gain:.2f}dB,aresample=192000,alimiter=limit={lim:.5f}:attack=2:release=60:level=disabled:latency=1,aresample=48000:filter_size=64:cutoff=0.97"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-af", af, "-c:a", "pcm_s24le", str(wav)], check=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-c:a", "aac", "-b:a", "256k", str(aac)], check=True)
        a = measure(aac)
        log.append({"gain_db": round(gain, 2), "ceiling_db": round(ceiling, 2), "aac": a})
        ok_i, ok_tp = abs(a["lufs"] - target) <= 0.15, a["true_peak_dbtp"] <= tp_max
        if ok_i and ok_tp:
            break
        if not ok_tp:
            ceiling -= a["true_peak_dbtp"] - tp_max + 0.1
        if not ok_i:
            gain += target - a["lufs"]
    print(json.dumps({"source": s0, "tries": log, "pass": abs(log[-1]["aac"]["lufs"] - target) <= 0.3 and log[-1]["aac"]["true_peak_dbtp"] <= tp_max}, indent=1))


if __name__ == "__main__":
    main()
