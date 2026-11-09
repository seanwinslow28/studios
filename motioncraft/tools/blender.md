# Blender, with Grease Pencil.

Blender is the studio's tool for 3D, layered depth and drawn 2D character animation. Grease Pencil is its drawing system: strokes held on keyframes, layer by layer, inside a real 3D scene with a real camera. Read this before building or rendering a scene.

## What it's best at.

- **Drawn character animation.** Grease Pencil holds each drawing on a key, so exposure is set by where the keys sit: a new drawing every frame is on ones, every second frame on twos, and a drawing left alone is a hold. Onion skins show the drawings before and after, which is how you see spacing.
- **Layered depth, the miniature-set look.** Painted layers placed as flat planes at real distances under a moving camera give true parallax, and lighting and depth of field can sell a small, built world.
- **Everything that moves, by script.** Keys from a timing chart, squash and stretch that keeps its volume, fades and blends over time, all set exactly in Python and repeatable.
- **The animatic.** The sequencer lays drawn boards over a timing track and renders one movie file with its sound.

Where another tool beats it:

- **Type and interface motion** look better and come faster in HyperFrames.
- **Painting** is Krita's job; Blender places and moves the paint.
- **Grading and the mix** happen in Resolve.
- **Rigged talking characters** would suit Moho Pro, which is on hold until a job needs it.

## Setup.

- **What's installed.** Blender 5.2.2 LTS (built September 15, 2026) at `/Applications/Blender.app`, on Sean's MacBook Pro (Apple M4 Pro, macOS 27.0.1), checked November 8, 2026. Free and open source. Every scripted finding below was tested on 5.2.2.
- **Blender 5.3** is due in mid-November 2026. For Grease Pencil it brings canvas flip and roll, selection tools inside Draw mode, a Carver tool for cutting strokes, and Multi-Fill for filling several areas at once. Move to it between films, never during one.
- **Call it by its full path in scripts.** `blender` is only a shell alias on this Mac, which a script's shell may not read.
- **The command that proves it works:**

```bash
/Applications/Blender.app/Contents/MacOS/Blender --version
```

- **Rendering from the command line** uses the studio's render script, `motioncraft/tools/scripts/blender_render.py`:

```bash
/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --disable-autoexec scene.blend \
  --python-exit-code 1 --python motioncraft/tools/scripts/blender_render.py -- out/frames 1 120 cycles gpu
```

`--factory-startup` keeps Sean's own add-ons and preferences from changing the result. `--disable-autoexec` stops any script saved inside the file from running. The script sets only the engine, the frame range, the output folder and the device, so set resolution, samples, seed, colour management and file format on the scene before saving.

## Getting the best out of it.

**Start scripts from an empty file.** Reset to factory settings with `use_empty=True` so no default cube, light or camera sneaks into the shot.

**Use the 5.x names.** Blender 4.3 rebuilt Grease Pencil and its Python interface, 5.0 renamed things again, and 5.1 changed fills. Most scripts and tutorials online use names that are gone, and some old names now quietly reach the annotation tool instead. The ones that matter most:

- The object type is `GREASEPENCIL`; data comes from `bpy.data.grease_pencils.new()`.
- Strokes live at `frame.drawing.strokes`; points have `position`, `radius` (thickness, in scene units) and `opacity`.
- Keys are `layer.frames.new(n)`, moved with `layer.frames.move(old, new)` and copied forward with `layer.frames.copy(a, b)`.
- Modifiers live on `object.modifiers`, with types such as `GREASE_PENCIL_NOISE` and `GREASE_PENCIL_TIME`, filtered to a layer with `tree_node_filter`.
- Since 5.1 a fill draws only when the stroke has a non-zero `fill_id`; a script that sets only the material's fill gets an empty ring.
- Since 5.0 an action's curves sit in a channel bag for its slot, not in `action.fcurves`, and the compositor is a node group the scene points at (`scene.compositing_node_group`).

**Keep line and paint on separate layers** in one group. Then the line can boil while the paint holds still, and each takes its own modifiers.

**Boil the line with drawings, not only noise.** The Noise modifier only jiggles points that already exist, so the shape never truly changes. A small family of redrawn lines, looped with the Time Offset modifier, reads as hand-drawn life. Two traps: Time Offset's default offset of 1 runs the whole loop a frame early (set it to 0), and Noise's step lands on frame numbers divisible by the step, not counted from the key.

**Name easing by the pose, never by Blender's word.** Blender's `EASE_IN` slows the start of the segment leaving a key, the opposite of the animator's "slow in", where drawings bunch as they arrive. Say "speed up into the contact" or "slow into the rest", and set the curve to match.

**On twos without moving keys.** A Stepped modifier on the curve (step 2, with an offset chosen so every charted key lands on a held frame) holds each value for two frames.

**Squash and stretch that keeps its mass.** For a solid, key only the squash axis and let a Maintain Volume constraint in Strict mode solve the other two. For a flat card, drive width as one over height from a single keyed number; keying both axes separately loses area between keys, because each eases on its own.

**Painted layers at depth.** Import each painted layer as a shadeless plane, place it at its distance, and size it to fill the frame there: distance times sensor width over focal length, plus about 20% spare for the camera move. Turn off `use_lights` on Grease Pencil layers that should keep flat painted colour; left on in a scene with no lights, a bright orange rendered dull brown.

**Fades and blends over time stay in Blender.** Resolve's edit scripting can't keyframe and its scripted Fusion comps didn't render in testing, so fades are keyed here: an opacity value inside the material, or a separate view layer joined in the compositor for a blend mode.

**Choosing the render device.** Cycles on the CPU repeats a frame exactly. The graphics chip is much faster; its frames differ from the CPU's by tiny, normal amounts. Finished renders may use the graphics chip; keep one device, a fixed seed and one Blender version for the whole film. Leave hardware ray tracing on Auto; switched off, frames strayed further from the CPU's.

## Where it goes wrong.

- **Crashes inside a sandbox that hides the graphics card.** Blender 5.2.2 finds no Metal device and crashes reading its name (exit code 139). Run it where the graphics chip is visible.
- **Grease Pencil, Eevee and Workbench won't render under a locked-down launcher.** All three draw through Blender's GPU drawing engine, even inside a Cycles render, and that engine registers with macOS's app registry when it starts. Block that and the render aborts (exit code −6). Calling `gpu.init()` first doesn't help, and converting the drawing to a mesh leaves bare edges with no fill. Render from the normal app environment.
- **Silent CPU fallback.** Asked for the graphics chip with no Metal device switched on, Cycles renders on the CPU without a word. The render script enables the Metal devices and stops if there are none; check its log line naming the device.
- **Old scripts and tutorials.** Anything before 4.3 uses the old names; 4.3 and 4.4 material may use names ending `_v3`. Blender Studio's free Grease Pencil course predates the rewrite.
- **Settings on their way out.** A material's `show_stroke` and `show_fill` still work in 5.2 but warn they go in 6.0; hide a line or fill by setting its colour's alpha to 0.
- **Driver loops.** A driver on one axis that reads another axis of the same object is a loop; Blender reports it and never runs the driver. Drive both from a custom property instead.
- **Mixed versions.** A file saved in 4.3 or later never opens correctly in 4.2 or earlier, and Noise or stacked Time Offsets can look different across versions. One version per film.
- **Animation faults to look for.** Noise on contact frames or holds, so the pose shimmers when it should land; a loop that jumps at the wrap; evenly spaced interpolated in-betweens that make a fall float; line and fill on one layer, so the paint swims with the boil.
- **Comparing renders.** Two renders of a movie can match pixel for pixel while their file bytes differ. Compare decoded frames, never file checksums.

## Safety.

- **Free and local.** Blender uploads and costs nothing.
- **Files carry code.** A `.blend` can hold scripts and driver expressions. Open others' files with auto-run off, and render with `--disable-autoexec`. Simple driver expressions (like `1 / q`) still run without auto-run, so keep drivers simple.
- **Add-ons are code.** Ask Sean before installing any add-on or extension.
- **Versions and device.** Settled: the graphics chip is fine for finished renders, with one device, seed and Blender version per film.
- **Long renders** tie up the Mac for hours; tell Sean before starting one.
