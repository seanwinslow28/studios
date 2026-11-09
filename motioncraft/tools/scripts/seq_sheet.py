"""Contact sheet from a numbered PNG sequence (frame_000001.png = t 0).
Usage: seq_sheet.py <frames_dir> <out.jpg> <fps> <first_frame> <last_frame> <step> <cols> <tile_w>
Frame numbers are 0-based composition frames; each tile is labelled with frame and time."""
import sys, os
from PIL import Image, ImageDraw, ImageFont

if sys.argv[1:2] in (["-h"], ["--help"]) or len(sys.argv) < 9:
    sys.exit(print(__doc__) or 0)

d, out, fps, a, b, step, cols, tw = sys.argv[1], sys.argv[2], float(sys.argv[3]), *map(int, sys.argv[4:9])
frames = list(range(a, b + 1, step))
th = round(tw * 9 / 16)
lab = 22
rows = (len(frames) + cols - 1) // cols
sheet = Image.new("RGB", (cols * tw + (cols + 1) * 6, rows * (th + lab) + (rows + 1) * 6), (24, 24, 24))
dr = ImageDraw.Draw(sheet)
try:
    font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 14)
except OSError:
    font = ImageFont.load_default()
for k, n in enumerate(frames):
    p = os.path.join(d, f"frame_{n + 1:06d}.png")
    if not os.path.exists(p):
        p = p[:-4] + ".jpg"
    if not os.path.exists(p):
        continue
    im = Image.open(p).convert("RGB").resize((tw, th), Image.LANCZOS)
    x = 6 + (k % cols) * (tw + 6)
    y = 6 + (k // cols) * (th + lab + 6)
    dr.text((x + 2, y + 3), f"f{n}  {n / fps:.3f}s", fill=(230, 230, 230), font=font)
    sheet.paste(im, (x, y + lab))
sheet.save(out, quality=88)
print(out, len(frames), "tiles")
