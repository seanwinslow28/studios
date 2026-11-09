"""Timestamped contact sheet for a time range of a video.

Usage:
  python3 contact_sheet.py <video> <start_s> <end_s> <fps> <out.jpg> [cols] [tile_w]

Every tile is labelled with absolute source time (s) and frame number at the
video's native rate, so a sheet can be cited as evidence ("t=10.48 f262").
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def wants_help(min_args):
    """True when the command line asks for help or gives too few arguments."""
    args = sys.argv[1:]
    return bool(args[:1] and args[0] in ("-h", "--help")) or len(args) < min_args


def main():
    if wants_help(5):
        sys.exit(print(__doc__) or 0)
    video, start, end, fps, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), Path(sys.argv[5])
    cols = int(sys.argv[6]) if len(sys.argv) > 6 else 6
    tile_w = int(sys.argv[7]) if len(sys.argv) > 7 else 320
    native = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate",
                             "-of", "csv=p=0", video], capture_output=True, text=True).stdout.strip()
    num, den = native.split("/")
    native_fps = float(num) / float(den)
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{start:.3f}", "-to", f"{end:.3f}", "-i", video,
                        "-vf", f"fps={fps},scale={tile_w}:-2", "-start_number", "0", f"{tmp}/f_%04d.png"],
                       check=True)
        files = sorted(Path(tmp).glob("f_*.png"))
        tiles = [Image.open(p).convert("RGB") for p in files]
    if not tiles:
        sys.exit("no frames")
    tw, th = tiles[0].size
    label_h = 18
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * (th + label_h)), (24, 24, 24))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/SFNSMono.ttf", 12)
    except OSError:
        font = ImageFont.load_default()
    for i, tile in enumerate(tiles):
        x, y = (i % cols) * tw, (i // cols) * (th + label_h)
        sheet.paste(tile, (x, y + label_h))
        t = start + i / fps
        draw.text((x + 4, y + 2), f"t={t:6.2f}  f{round(t * native_fps)}", fill=(235, 235, 235), font=font)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=88)
    print(out, f"{len(tiles)} tiles", sheet.size)


if __name__ == "__main__":
    main()
