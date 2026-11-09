# HyperFrames.

HyperFrames turns a web page into video. A composition is an HTML file: elements carry timing in `data-*` attributes, one paused GSAP timeline holds every move, and headless Chrome seeks to each frame and captures it. Read this before building motion design, moving type, a logo intro or a flat layer for a film.

## What it's best at.

- **Type, shapes and interface, moving precisely.** Anything drawn with HTML, CSS and SVG moves frame-exact, with real fonts and kerning, and re-renders identically.
- **Flat layers for a deeper scene.** Cards, labels, line drawings and 2.5D turns rendered with transparency, then placed over Blender or footage in Resolve.
- **Fast changes.** "Hold that word four frames longer" is a one-number edit and a minute's render.
- **Lottie inside a film.** A Lottie or dotLottie player registered with the page is seeked frame by frame like everything else.

Where another tool wins: painted or hand-drawn character acting (Krita and Blender's Grease Pencil), true 3D with light and depth of field (Blender), anything that must stay interactive in an app (Rive or Lottie), and hand-finished compositing where the eye has to steer each frame (Resolve's Fusion). Remotion does similar work, free for individuals and companies of up to three people (checked November 8, 2026).

## Setup.

- **Cost.** Free. Needs Node 22 or newer; this Mac has Node 22.22.2 and ffmpeg 8.1.
- **Versions on this Mac** (checked November 8, 2026). The command line comes through `npx`; 0.8.158 is in the npx cache, 0.8.164 is installed by hand under `~/.local/share/motioncraft/hyperframes/` with a pinned headless Chrome (150.0.7871.24), and the newest on npm is 0.9.26. There is no global `hyperframes` command or desktop app.
- **Pin one version per film.** Pixel output drifts across versions and Chrome builds, so a film keeps one version throughout. Move to a newer one between films: `npx hyperframes@latest upgrade --project . --check` reports the gap without changing anything.
- **The command that proves it works:** `HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 npx -y hyperframes@0.8.158 doctor`, which checks Node, ffmpeg, ffprobe and Chrome. If Chrome is missing, `npx hyperframes browser ensure` fetches the pinned build.
- **The skills.** Claude Code has the HyperFrames skills installed: start at `hyperframes`, then `hyperframes-core` for the composition rules, `hyperframes-animation` and `hyperframes-keyframes` for motion, `hyperframes-creative` for type and palette, and `hyperframes-cli` for commands.

## Getting the best out of it.

**Let GSAP own every transform.** A CSS `transform` on an element GSAP also moves becomes a fixed offset that fights the tween, and lint rejects it. Set start states inside `fromTo`, centre with flex or `inset`, and animate only `x`, `y`, `scale`, `rotation` and `opacity`, never `width`, `top` or `left`.

**Write for a renderer that seeks, not one that plays.** The renderer jumps to arbitrary frames with events suppressed, so `onUpdate` never fires, clocks and unseeded `Math.random` break repeatability, and `getBoundingClientRect()` at tween time reads wrong. Bake curves into keyframes, compute layout once when the page builds, and give a `fromTo` on a shared timeline `immediateRender: false`. An element waiting for its own start must already be set to its start state when the page builds.

**Real motion blur, made from sub-frames.** The usual master is 24 fps; higher rates matter only for making blur. Sub-frames are extra in-between moments rendered just to be averaged into each output frame. `motion_blur.py`, built and tested for 60 fps output, renders four passes at 240 fps, each starting a quarter of a sample later (a quarter of the gap between rendered frames): 16 moments per output frame. Averaging the 8 nearest each frame's centre gives a 180-degree shutter, open for half of each frame as a film camera usually is. At 24 fps the same scheme means passes at 96 fps (untested). Without blur a fast logo hit strobes; with it, the move reads as one gesture. Put hard cuts midway between shutters, at `(floor(t*fps)+0.5)/fps`, or the averaging makes a ghost frame.

**Preview a stretch, not the film.** A small page that scrubs the film's timeline from `a` to `b`, with the root's `data-duration` set to `b - a`, renders a four-second window in under a minute. For stills at exact instants use `snapshot --at 10.85,27.4 --describe false`.

**Measure in the browser before rendering.** A page that reads `?t=` and seeks gives any instant for measuring. Check that type sits inside title safe (5 percent in: 96 pixels at the sides, 54 top and bottom at 1920 by 1080), that no moving object crosses the band where words sit while a line is up, that a line leaves on the same frame as its picture's cut, and that small type still reads at 390 pixels wide. Seek and read the layout in the same call; with the browser pane hidden, animation frames barely run.

**Search before hand-building.** `npx hyperframes catalog --query "<the beat in plain words>"` searches a local catalogue of motion blocks, transitions and effects; nothing is sent anywhere. Port a found pattern's maths, never a recognisable sequence.

**Flat layers with transparency.** Give the page no background fill, then render a PNG sequence (`--format png-sequence`) or ProRes 4444 (`--format mov`). Check one frame's alpha before using the layer.

**Fonts are files.** A named font needs an `@font-face` pointing at a font file shipped with the project, or the browser substitutes without a word.

## Where it goes wrong.

- **Chrome dies inside a sandbox.** On macOS, a sandboxed shell (Claude Code's or Codex's) blocks the startup handshake headless Chrome needs (`bootstrap_check_in`, the Mach port rendezvous), so every Chrome exits at once. Lint and audio still work; `check`, `snapshot` and `render` do not. This is the host, not a broken install. Run those commands outside the sandbox; never build a stand-in renderer from images.
- **A clean report that checked nothing.** A lint error switches off the layout and contrast audits, and `check` then reports zero samples, which looks like a pass. Clear lint errors first, then trust the numbers.
- **Silent sound.** Every `<audio>` needs an `id`, or the mixer never finds it.
- **Black or grey frames.** Filter lists must match function for function between keyframes, and a colour tweened into a gradient goes grey.
- **Soft or wrongly placed cards in 3D.** Perspective goes on a wrapper, turning faces need `backface-visibility: hidden`, and CSS `zoom` on an absolutely placed box scales its position too, so zoom an inner wrapper.
- **Visibility fights.** Never tween `visibility`, `display` or `autoAlpha` on a timed clip; the framework hides clips itself. Animate a child.
- **A cut-off ending.** Render length is the root's `data-duration`, not the timeline's length. A clip that runs past it is cut.
- **A render killed with its terminal.** If the calling tool kills its process group on timeout, start long renders with `HYPERFRAMES_RENDER_DETACHED=1` in their own process group, or as a background command, and watch the log.
- **Stale files in preview.** A preview server caches files; reload a changed one with `fetch(url, { cache: "reload" })`.

## Safety.

- **Telemetry off on every call:** `HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1`.
- **Frames can leave the Mac by accident.** `snapshot` without `--describe false`, or `capture` without `--skip-vision`, sends frames to a vision service. Always pass both flags.
- **Ask Sean first** before `publish` (a public link), `cloud render`, Lambda or Cloud Run (each uploads the project to someone's servers), and `feedback` or `--file-issue` (each posts to a public channel).
- **Installs.** `npx hyperframes skills update` rewrites installed skills, and `npx -y` downloads an uncached version; name both when they happen.
- **Rendering outside the sandbox** means the command runs with full access to the Mac. Keep it to the render or check command, on the job's own folder.
