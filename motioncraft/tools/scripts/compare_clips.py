"""Side-by-side comparison clip with a label bar over each clip (FFmpeg here has no drawtext).

Usage: python3 compare_clips.py <out.mp4> <label1> <clip1> [<label2> <clip2> ...]
Each clip is scaled to 640×360, held on its last frame to the longest duration, and placed
in one row under a 40 px label bar. 30 fps, H.264, silent.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

if sys.argv[1:2] in (["-h"], ["--help"]) or len(sys.argv) < 4:
    sys.exit(print(__doc__) or 0)

out, pairs = sys.argv[1], sys.argv[2:]
labels, clips = pairs[0::2], pairs[1::2]
dur = max(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", c],
                               capture_output=True, text=True).stdout) for c in clips)
W, H, BAR = 640, 360, 40
with tempfile.TemporaryDirectory() as tmp:
    bar = Image.new("RGB", (W * len(clips), BAR), (24, 24, 24))
    d = ImageDraw.Draw(bar)
    font = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", 18)
    for i, lab in enumerate(labels):
        d.text((i * W + 14, 10), lab, fill=(240, 240, 240), font=font)
    bar_path = Path(tmp) / "bar.png"
    bar.save(bar_path)
    args = ["ffmpeg", "-v", "error", "-y"]
    for c in clips:
        args += ["-i", c]
    args += ["-loop", "1", "-i", str(bar_path)]
    chains = [f"[{i}:v]fps=30,scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,"
              f"tpad=stop_mode=clone:stop_duration={dur},trim=duration={dur},setpts=PTS-STARTPTS[v{i}]" for i in range(len(clips))]
    row = "".join(f"[v{i}]" for i in range(len(clips))) + f"hstack=inputs={len(clips)}[row]" if len(clips) > 1 else "[v0]copy[row]"
    graph = ";".join(chains + [row, f"[{len(clips)}:v]trim=duration={dur}[bar]", "[bar][row]vstack=inputs=2,format=yuv420p[out]"])
    args += ["-filter_complex", graph, "-map", "[out]", "-an", "-c:v", "libx264", "-crf", "18", "-movflags", "+faststart", out]
    subprocess.run(args, check=True)
print(out, f"{dur:.2f}s")
