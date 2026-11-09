# Checking the work with fresh eyes.

A check is most useful when a version looks finished to its maker, which is when its faults are hardest to see.

## What a fresh check is for.

The maker is the worst placed to check a piece. They know what every line says, so they can read it at any size. They watched it a hundred times in a preview, so a dropped frame in the final file never reaches them. They see what they meant, not what's there. A fresh check is a helper who didn't make the thing, working from the delivered file and the sources of truth (the script, the locked sound, the product's own copy), not from the maker's notes.

It checks truth, never taste. Truth here means:

- **Facts.** Every claim on screen traces to the product's source or its own copy, hedged the way the product hedges. Dated text is gone from a film meant to last.
- **Numbers.** Prices, counts and statistics match their source exactly.
- **Timing.** The frame count equals the locked length. Each line appears on its own beat, never before the cut into its scene.
- **Sync.** Voice, music and effects sit where they should, start to finish.
- **Technical faults.** The list below.

Whether a move feels right is Sean's call; a check that drifts into taste muddies both jobs.

## What good looks like.

- **Checked on the file Sean will see,** from the final render path. "It looked fine in the browser" isn't a check, because the render, the encode and the player each change things.
- **Looked at, not only measured.** A script can pass while a beat is plainly broken. Every number gets eyes on the frames it describes.
- **Shown, not described.** Frames around each transition, the same instant before and after a fix, and a tool's numbers as they came out. "Sync is fine" is a claim; "lag 0 samples against the source mix" can be seen. How such proof is laid out for Sean is in `craftwork/guides/review-pages.md`.
- **The check itself checked.** Some tools mislead. One common way of converting a master to RGB (the red, green and blue values a meter reads) made every colour two or three levels too dark. Converting with the settings named explicitly (BT.709 matrix, video range, accurate chroma scaling; chroma is the colour half of the picture, stored at lower resolution) showed the master was right. A clip with a fault put there on purpose shows whether a check works: if it reports exactly that fault, its silence on the real film means something.
- **A check that couldn't run tells you nothing,** so its silence is never a pass.

## The common technical faults, and how to spot and fix each.

### Dropped or duplicate frames.

A dropped frame shows as a jump in motion. A duplicate shows as a hitch, a moment where movement stalls. Spot both by scanning how much each frame differs from the one before (`motion_check.py`): a spike where no cut was designed is a drop, a near-zero dip in the middle of a move is a duplicate. Confirm with the frame count, which should equal the length times the frame rate exactly. The usual causes are a variable-rate capture, a frame-rate conversion, or a render that skipped frames under load. Fix by rendering at a constant rate, frame by frame from seeked times rather than captured live, and rendering the stretch again.

### Sync drift.

Sound that starts in sync and slides later over the film. Check sync at the start and at the end, not just once. Cross-correlating the file's audio against its source mix, sliding one against the other to find where they match best, gives an exact lag, which should be zero. A lag that grows over the length usually means a sample-rate mismatch (44.1 kilohertz audio treated as 48) or a variable-rate picture. Each effect should land within one frame of its cue. Fix by conforming everything to one sample rate and a constant frame rate before the mix, never by nudging the sound by ear.

### Banding.

Smooth gradients, such as a sky, a vignette or a soft glow, break into visible steps. It comes from too few levels: 8-bit files, heavy compression crushing dark areas, or a soft gradient pushed hard in the grade. Look at flat dark gradients on the delivered web file, at full screen. Rule out the display first, since a cheap 8-bit panel can band on its own. Fix by working at 10 bits until the end, giving the web file enough bit rate, and adding fine grain that moves every frame, about two pixels across, so it survives compression. Grain that freezes reads as dirt.

### Wrong frame rate or colour tags.

A file can carry the right pictures with the wrong labels. Read the delivered file's rate, size, frame count, duration and colour tags. For standard HD video the tags are BT.709 for primaries, transfer and matrix, at video range. An untagged or mis-tagged file looks right in one player and washed out or too dark in another; Safari and QuickTime are the usual offenders. Check brand colours by running a chart of the film's colours through the whole pipeline and measuring the difference against the design values (`make_chart.py`, `measure_colour.py`). That difference is measured in ΔE00, a unit where about 1 is the smallest change most people can see. Aim for the brand colour within 1 and flat fields within about 1.5 on the web file. Fix the tag at encode rather than shifting colours to compensate.

### Clipped audio.

Peaks hit the ceiling and crackle. Measure true peak (the waveform's real highest point, including between samples) and integrated loudness, in LUFS, the standard measure of how loud a whole mix sounds, against the target set for where the film goes: a web copy about −14 LUFS with true peak at or under −1 dBTP, broadcast −23 LUFS (the sound brief has the detail). Measure on each delivered file, not the mix. Fix with less gain or a true-peak limiter, then measure again.

### Text too small or on screen too briefly.

The maker can always read their own words. Scale frames at the smallest-text moments down to phone width, about 390 pixels across, and read them cold. Keep text inside title safe, the margin no screen crops: 5 percent of the frame's width and height in from each edge, which is 96 pixels at the sides and 54 at top and bottom of a 1920 by 1080 frame, more if the film will be cropped for phones. For time on screen, a common subtitling rule of thumb is about 15 to 17 characters a second and never much under a second for anything at all. Count the frames a line is fully readable, not the frames it exists. Fix by holding it longer, cutting words, or making it bigger.

### Jitter.

A whole layer shakes rigidly, nothing redrawn. It often comes from positions snapped to whole pixels on a slow move, or noisy tracking. Its cousins are line boil (a line wobbling frame to frame where none was designed) and texture sliding, where paint or grain stays fixed to the screen while the picture moves under it. Spot them on sheets at the film's own rate, and at full speed and viewing size, since stills hide them. Fix by moving in fractions of a pixel, smoothing the track, or pinning texture to the surface it belongs to.

### Popping.

Something appears or vanishes in a single frame with no motion, or a line of type survives one frame past its cut. Spot it on sheets at the native rate around every transition, and by checking each line's visibility one frame before and one frame after each cut. Fix by giving the element an entrance or exit, hiding the change behind something passing in front, or trimming the stray frame.

### Also worth a look.

Unplanned black or frozen frames, a file that doesn't decode cleanly end to end, artwork edges showing past the paint, and every script word heard, in order, when speech-to-text runs on the final mix.

## How it goes wrong, and the fix.

- **Checking the preview, not the deliverable.** Fix: every check runs on the file going out.
- **Describing instead of showing.** Fix: frames, clips and numbers, labelled with time and frame number; taste notes left to Sean.
- **Mastering from a compressed file.** Every later step inherits its damage. Fix: finish from a clean high-quality master, and make the web file from that.

## Examples.

- The shelf's measurements show the habit. **The Line's Freeview Play upload** (`motioncraft/research/the-line-freeview-play.md`) runs at 25 frames a second though the studio says it animated at 24, and its scene detector flagged four flicker frames at about 1:11 that had to be merged before the shot count meant anything.
- **Caption with Intention** (`motioncraft/research/caption-with-intention.md`) swells a word for only about a quarter of a second, then relaxes it over about another quarter to a third, a reminder that text timing has to be checked in frames, at viewing size.

## Tools.

`motion_check.py`, `cut_check.py`, `contact_sheet.py`, `compare_clips.py`, `measure_colour.py` and `make_chart.py` live in `motioncraft/tools/scripts/`; ffmpeg's loudness meter and ffprobe cover sound and file details.
