# Motioncraft's scripts.

Small command-line tools that measure reference films and our own renders, and make the pieces a job needs. Each one prints its usage with `--help`.

## Setup.

Once per job: `python3 -m venv .venv && .venv/bin/pip install -r motioncraft/tools/scripts/requirements-venv.txt`, then run the scripts with `.venv/bin/python`.

## Studying a reference film.

- `analyze_film.py` measures every frame and the soundtrack of a film: cuts, motion, background colour, loudness, sound onsets and a tempo estimate. The lead reaches for it first when studying a reference.
- `contact_sheet.py` draws a contact sheet of a stretch of video, each tile labelled with its time and frame number. For looking closely at a shot, or pointing at an exact moment.
- `compare_clips.py` lays several clips side by side under labels, in one video. For setting our take against the reference.

## Checking our own renders.

- `seq_sheet.py` draws a contact sheet from a numbered PNG sequence. For reviewing rendered frames before they are encoded.
- `motion_check.py` measures how much each frame changes from the last, lists jumps and frozen frames in the middle of a move, and saves chosen frames and phone-width copies. For checking that motion is smooth and still reads on a phone.
- `cut_check.py` confirms that each designed hard cut is a clean one-frame change, and lists the biggest changes in the film. For the last look before the picture is locked.
- `motion_blur.py` makes real motion blur by averaging four time-shifted 240 fps HyperFrames renders through a virtual shutter, with optional living grain and a clean ProRes master. For fast moves that strobe.

## Colour.

- `make_chart.py` makes a ProRes chart of the film's palette, one flat patch per colour. For testing that colour survives the finishing chain, with the next script.
- `measure_colour.py` measures colour error, in CIEDE2000 units, for a chart or for flat areas of the film against their design values. For checking that the finish keeps brand colours true.

## Sound.

- `make_sfx.py` generates several takes of each sound effect in a job's palette with ElevenLabs, keeping takes already made. For building the effects library for a film.
- `build_mix.py` picks the best takes by measurement, places each effect on its picture cue, rides its level against the locked mix, and writes the finished mix. For laying effects over a locked music and voice mix.
- `sync_check.py` measures where each placed effect really lands against its cue, and names any more than one frame off. For checking sync after every mix.
- `make_web_mix.py` makes the web version of a master mix at a set loudness, without the pumping that automatic levelling causes. For the final upload.
- `sound_client.py` makes one ElevenLabs sound effect or one Lyria music take from a prompt, and reads the ElevenLabs balance. For a single sound outside the palette, or music.

## Type, Blender and Krita.

- `kerning.py` reads a font's own pair kerning for the exact words and writes it into a Blender text object, which otherwise ignores kerning. For any title set in Blender.
- `blender_render.py` renders a Blender scene to PNG frames from the command line, with the file's own scripts switched off. For renders without opening Blender.
- `krita_run.py` runs a Python script inside Krita with no screen, and fails if any text would fall back to a substitute font. For building layered Krita files and exports by script: layers and compositing, not painting.

## The job folder.

- `new_production.py` makes a lean job folder: the media folders, a .gitignore that keeps media out of git, and the venv requirements. For the start of a job.
- `build_review.py` builds an HTML review page from a content file, and refuses missing media or any line without ending punctuation. For showing Sean a cut.

## Tests.

Run `python3 -m pytest motioncraft/tools/scripts -q` from the top of the repo, in a venv with the requirements and pytest; tests that need ffmpeg, HarfBuzz, Blender or Krita skip where those are missing.
