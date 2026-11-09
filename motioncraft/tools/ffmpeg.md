# ffmpeg.

ffmpeg converts, measures and delivers: the ProRes master from rendered frames, the web copy from the master, and the numbers that prove both right. Read this before encoding or checking anything.

## What it's best at.

- **Exact, repeatable conversion.** Frames to movies and back, codec to codec, every setting in one command.
- **The web delivery file.** Its x264 encoder kept noticeably more grain than Resolve's own H.264 at the same bit rate (1.20 levels against 0.72), so the web copy is made here from the master.
- **Checks.** `ffprobe` reads codec, size, rate, frame count and colour tags; `ebur128` measures loudness; `psnr`, `ssim`, `framemd5` and a difference blend compare two renders frame by frame; `blackdetect`, `freezedetect` and `scdet` find black frames, frozen frames and cuts.
- **Small fixes baked into frames**, such as a fade Resolve would lose.

Where another tool beats it:

- **Editing, grading and mixing by ear** belong in Resolve.
- **Text on a frame.** This build has no `drawtext` filter. Draw labels with Python's Pillow (as `motioncraft/tools/scripts/compare_clips.py` does) or in HyperFrames.
- **Perceptual quality scores.** This build has no `libvmaf` and no `zscale`; use `ssim` and `psnr`.

## Setup.

- **What's installed.** ffmpeg 8.1 and ffprobe from Homebrew at `/opt/homebrew/bin`, on Sean's MacBook Pro (Apple M4 Pro, macOS 27.0.1), checked November 8, 2026. Free.
- **Encoders present:** `libx264`, `libx265`, `prores_ks`, `prores_videotoolbox`, `h264_videotoolbox`, `aac` and `aac_at`. **Filters present:** `ebur128`, `loudnorm`, `psnr`, `ssim`, `blend`, `colorspace`, `signalstats`, `blackdetect`, `freezedetect` and `scdet`.
- **The command that proves it works:**

```bash
ffmpeg -version | head -1
```

- **Upgrades** (`brew upgrade ffmpeg`) go between films: a new encoder version can change the bytes and the look of the same command.
- **Scripts that use it** live in `motioncraft/tools/scripts/`: `motion_blur.py` (averaged motion blur, the ProRes master and grain), `make_web_mix.py` (the web mix), `measure_colour.py`, `contact_sheet.py` and `compare_clips.py`.

## Getting the best out of it.

**Colour: BT.709 and video range, end to end.** Rendered frames are RGB; video is YUV (brightness plus two colour channels). The matrix converts between them: BT.709 is the HD formula; BT.601, the older standard-definition one, is ffmpeg's default and shifts reds and greens. Video range puts black at level 16 and white at 235, not 0 and 255. ffmpeg writes no colour tags by default, so convert with the BT.709 matrix and tag inside the filter chain. On ffmpeg 8.1 the output flags `-color_primaries` and `-color_trc` were silently dropped on an untagged source (tested November 8, 2026); `setparams` in the filter chain stuck every time. Read the tags back with `ffprobe`.

**Put complex filters in a file.** A graph with several inputs, labels and expressions breaks on the command line: the shell eats brackets, semicolons and quotes, and commas in expressions need escaping. Write it to a text file and pass it with `-/filter_complex graph.txt` (or `-/filter` for a simple chain). The older `-filter_complex_script` option still works in 8.1 but prints a warning.

**Grain costs bit rate.** Grain changes every pixel every frame. The usual 24 fps master wants about 10 to 12 Mb/s at 1080p with two-pass x264, scaled from the 20 Mb/s used at 60 fps, a rate that matters only when rendering extra frames for blur. Two-pixel grain survives; one-pixel grain vanishes.

**Loudness: measure honestly.** `ebur128` reports no true peak unless you add `peak=true`. Measure the delivered file itself, because AAC encoding can raise the true peak; targets are in the sound brief (web: about −14 LUFS, true peak at or under −1 dBTP). If you use `loudnorm`, type every target: it defaults to −24 LUFS and −2 dBTP, its linear mode silently falls back to riding the gain, and its dynamic mode resamples to 192 kHz unless told otherwise. `make_web_mix.py` avoids it: one fixed gain, a limiter run at four times the sample rate to catch peaks between samples, then it measures the AAC file and adjusts until the file itself reads the target.

**Compare decoded frames, never file checksums.** Two files can hold identical pictures with different bytes. `framemd5` proves identity frame by frame; `ssim` and `psnr` say how close; a difference blend shows where.

## The commands a master uses most.

Each was run on ffmpeg 8.1 on November 8, 2026. `TAGS` is the tagging step from above:

```bash
TAGS="setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv"
```

**ProRes 422 HQ master from a frame sequence, with the mix as 24-bit PCM:**

```bash
ffmpeg -framerate 24 -i frames/frame-%04d.png -i mix.wav -map 0:v -map 1:a -shortest \
  -vf "scale=out_color_matrix=bt709:out_range=tv,format=yuv422p10le,$TAGS" \
  -c:v prores_ks -profile:v 3 -vendor apl0 -c:a pcm_s24le master.mov
```

**H.264 web copy from the master, two-pass, with correct colour tags:**

```bash
ffmpeg -y -i master.mov -vf "$TAGS" -c:v libx264 -preset slow -b:v 12M -pix_fmt yuv420p \
  -pass 1 -passlogfile x264 -an -f null /dev/null
ffmpeg -i master.mov -vf "$TAGS" -c:v libx264 -preset slow -b:v 12M -pix_fmt yuv420p \
  -pass 2 -passlogfile x264 -profile:v high -c:a aac -b:a 256k -movflags +faststart web.mp4
```

Give `-pix_fmt yuv420p` to both passes. From a 10-bit master, the first pass otherwise runs in 10-bit and the second refuses to start.

**Check the tags and the frame count:**

```bash
ffprobe -v error -select_streams v:0 -show_entries \
  stream=codec_name,profile,pix_fmt,color_space,color_primaries,color_transfer,color_range,nb_frames \
  -of default=nw=1 web.mp4
```

**Measure loudness and true peak:**

```bash
ffmpeg -hide_banner -nostats -i web.mp4 -af ebur128=peak=true:framelog=quiet -f null - 2>&1 | tail -12
```

**Pull out frames:** a still at a time (fast seek), or an exact frame by number:

```bash
ffmpeg -ss 2.5 -i master.mov -frames:v 1 -update 1 still.png
ffmpeg -i master.mov -vf "select='eq(n\,120)'" -frames:v 1 -update 1 frame-120.png
```

**Compare two renders frame by frame:**

```bash
ffmpeg -i a.mov -map 0:v -f framemd5 a.md5; ffmpeg -i b.mov -map 0:v -f framemd5 b.md5; diff a.md5 b.md5
ffmpeg -i a.mov -i b.mov -lavfi "[0:v][1:v]ssim=stats_file=ssim.log" -f null -
ffmpeg -i a.mov -i b.mov -lavfi "[0:v][1:v]blend=all_mode=difference,signalstats,metadata=print:key=lavfi.signalstats.YMAX:file=diff.txt" -f null -
```

The first says which frames differ, the second how much, the third the largest difference per frame.

**Bake a fade into the frames:**

```bash
ffmpeg -i shot.mov -vf "fade=t=in:st=0:d=0.5,$TAGS" -af "afade=t=in:st=0:d=0.5" \
  -c:v prores_ks -profile:v 3 -vendor apl0 -pix_fmt yuv422p10le -c:a pcm_s24le shot-faded.mov
```

## Where it goes wrong.

- **Colours shift.** A conversion without the BT.709 matrix uses BT.601: reds and greens move, most visibly in brand colours. Measure a colour chart through the pipeline.
- **Missing or wrong tags.** Without tags, players guess, and Safari and QuickTime show BT.709 lighter. Check with `ffprobe`.
- **Off-by-one frames.** A seek after `-i` decodes from the start and is slow; one before is fast and usually right on ProRes, but use `select` by frame number when the exact frame matters.
- **Variable frame rate.** Screen recordings and some phone clips vary their rate; force a constant one with the `fps` filter before comparing or editing.
- **Peaks after the encode.** The mix passed, but the AAC file reads higher. Measure the file you ship.
- **Quality you can't get back.** A master made from an H.264 file keeps its faults. Start from frames or ProRes.
- **Overwriting.** `-y` overwrites without asking. Never point an output at a source file or a delivered master.

## Safety.

ffmpeg runs entirely on the Mac: it uploads nothing and costs nothing. Write every result to a new file in the job's folder, keep sources untouched, and ask Sean before deleting outside it.
