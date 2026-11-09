"""Shared helpers for the script tests: where the scripts are, and what this machine has."""
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

FFMPEG = shutil.which("ffmpeg") and shutil.which("ffprobe")
need_ffmpeg = pytest.mark.skipif(not FFMPEG, reason="ffmpeg is not installed on this machine")
BLENDER = os.environ.get("MOTIONCRAFT_BLENDER", "/Applications/Blender.app/Contents/MacOS/Blender")
HAVE_BLENDER = os.access(BLENDER, os.X_OK)
KRITA = Path(os.environ.get("KRITA_APP", "/Applications/krita.app")) / "Contents" / "MacOS" / "kritarunner"
HAVE_KRITA = os.access(KRITA, os.X_OK)


def run(script, *args, cwd=None, check=True, env=None):
    """Run one script with this Python; its finished process."""
    return subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)], cwd=cwd, env=env,
                          capture_output=True, text=True, check=check, timeout=600)


def make_clip(path, seconds=2, cut_at=None):
    """A small 30 fps test clip: a moving pattern, with a hard cut to another at `cut_at` seconds."""
    if cut_at is None:
        src = ["-f", "lavfi", "-i", f"testsrc2=size=320x180:rate=30:duration={seconds}"]
        graph = ["-pix_fmt", "yuv420p"]
    else:
        src = ["-f", "lavfi", "-i", f"testsrc2=size=320x180:rate=30:duration={cut_at}",
               "-f", "lavfi", "-i", f"mandelbrot=size=320x180:rate=30,trim=duration={seconds - cut_at}"]
        graph = ["-filter_complex", "[0:v][1:v]concat=n=2:v=1,format=yuv420p"]
    subprocess.run(["ffmpeg", "-v", "error", "-y", *src, *graph, "-c:v", "libx264", "-crf", "18", str(path)],
                   check=True)
    return path
