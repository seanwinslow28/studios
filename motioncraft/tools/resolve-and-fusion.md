# DaVinci Resolve Studio and its Fusion page.

Resolve is where a film is put together and finished: the cut, the colour, the mix and the delivery files. Its Fusion page is a node-based compositor, the studio's choice for motion design finished by hand, instead of After Effects. Read this before opening Resolve on a job.

## What it's best at.

- **Conform and cut.** Rebuilding the agreed cut on a timeline, frame for frame, from the animatic and the rendered shots.
- **Colour.** Balancing shots so they match and sit neutral, then one look over the top, with real scopes and colour management.
- **The mix.** Fairlight, the audio page, has loudness meters and offline analysis, enough for a short film.
- **Hand-finished motion on the Fusion page.** Type, shapes, masks, tracking, particles, 3D and compositing, keyframed by hand in a node graph.

Where another tool beats it:

- **Anything animated by script** belongs in Blender or HyperFrames. The edit API sets fixed values only; Fusion scripting can keyframe, but scripted comps didn't render in testing.
- **Drawn character animation** is Blender's Grease Pencil.
- **The web delivery file** comes out better from ffmpeg's x264: on grained frames it kept 1.20 levels of grain against Resolve's 0.72 at the same bit rate.
- **After Effects** has the larger plug-in world. Sean has said no to it unless a job truly needs it, so push Fusion first.

## Setup.

- **What's installed.** DaVinci Resolve 21.2.0 on Sean's MacBook Pro (Apple M4 Pro, macOS 27.0.1), checked from the app's own version on November 8, 2026. It's the Studio edition, a one-time $295. The scripting findings below were made on 21.1.1; recheck any that matter on 21.2.
- **Scripting from outside.** Resolve's Python link needs three environment settings:

```bash
export RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
export RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
export PYTHONPATH="$RESOLVE_SCRIPT_API/Modules"
```

- **The check that proves it works, without touching anything.** With Resolve already open, read the open project's name and nothing more:

```bash
pgrep -lx Resolve && python3 -c "import DaVinciResolveScript as d; r=d.scriptapp('Resolve'); print(r.GetVersionString(), r.GetProjectManager().GetCurrentProject().GetName())"
```

- **Reference that ships with it.** The scripting API's README, changelog and type file sit in the Scripting folder above, and 21.2 added a Fusion tool reference in `Developer/Fusion/`. The user's Fusion folder (`~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/`) holds Templates, Macros, Fuses and Scripts; its Fuses and Plugins folders were empty and no Reactor was installed on November 8, 2026.

## Getting the best out of it.

**Correct, then grade.** Correction makes the shots match and sit neutral; the grade then sets one look, written as a sentence before you touch a wheel. Balance in the first node, build the look after it. Set colour management in Project Settings before any grading, so the maths and the display transform are fixed for the whole film. A grade that drifts from the approved design colours is a design change, not a finishing choice.

**Measure loudness on the delivered file, not the mix.** Use ffmpeg's `ebur128` with `peak=true` (its peak mode is off by default). Encoding to AAC can push the true peak up, so a mix that passed can fail as a file. Resolve's scripted audio normalising defaults to sample peak, not true peak, so set it explicitly if you use it.

**Let ffmpeg make the web copy.** The chain that worked: a clean 10-bit ProRes 422 HQ master tagged BT.709, with the master mix as 24-bit PCM; then the web file made by x264 from that master (see the ffmpeg guide). Never finish from an H.264 file; start every finish from the cleanest master you have.

**Grain is its own step.** Add it after any motion-blur averaging, outside Resolve: zero-mean so it never darkens a colour, monochrome, about two pixels across, around 1.6 levels of spread, new every frame. If Resolve's Film Grain is used instead, its Offset default of 0.01 brightens everything; set it to 0.

**Scripting: what it did on 21.1.1.**

- **Worked:** creating a project, project settings, importing media as a plain list of paths (the dictionary form returned nothing), timelines, appending clips, render jobs by id (add, start, poll), and saving, closing and reopening its own project.
- **Frame rate:** on 21.1.1 the playback rate had to be set separately from the timeline rate. The 21.2 changelog says setting one now sets both.
- **Copy, not render:** a ProRes 422 HQ source rendered to ProRes 422 HQ at the same size and rate is copied byte for byte, in seconds. To test a grade or grain, render to another codec so the frames are really processed.
- **Saving:** a save can quietly fail. It returned nothing, three times, until a dialog blocking the app was dismissed. Only reopening the project proves it saved.

## The Fusion page.

Fusion's core is already strong for motion design, and much of what people buy for After Effects is built in:

- **Text+ with the Follower modifier** animates text letter by letter, word by word or line by line, with delay, order and overlap: Fusion's answer to After Effects' text animators. Character Level Styling and MultiText cover per-letter looks and several text layers in one node.
- **Shape tools** (rectangles, ellipses, stars, booleans, duplicates, grids) draw resolution-free vector shapes.
- **Particles** (emitters, forces and a particle renderer), **3D**, the **planar tracker** and the **spline editor** for hand-shaped curves.
- **Version 21 additions:** Krokodove built in (over 70 tools in 21.0, about 25 more for 2D shapes and 3D forms in 21.1), Lottie and OGraf loaders, colour fonts in Text+, a Macro Editor for building your own templates, and native Affinity files (layers can be split onto the timeline).

**Getting the best from Fusion.** Build the comp by hand. Shape curves in the spline editor rather than stacking presets. Save any setup worth reusing as a macro, so the studio grows its own library instead of buying templates. Lottie files from Lottie Creator load straight into the node graph with their transparency, ready to composite and grade.

## Where it goes wrong.

- **Fades vanish.** On 21.1.1 a clip's fade was lost when the project was saved and reopened. Bake fades into the frames (ffmpeg's `fade`, or in the shot's own tool) until a reopen on 21.2 proves otherwise.
- **The edit API can't animate.** It sets fixed values only (opacity, composite mode, position, zoom, crop, rotation, the grade). Fusion scripting can keyframe, but see the next point.
- **Fusion comps built by an outside script don't render.** On 21.1.1 a scripted comp read back correctly, but the render ignored it, even a plain red background; saving first or opening the Fusion page first didn't help. Build Fusion work by hand.
- **Colour lookup files load only from Resolve's own LUT folder.** An absolute path elsewhere failed for both `.cube` and `.dctl` files; one at the top of Resolve's LUT folder worked. Put a needed LUT there by hand, through Project Settings.
- **Reopened renders can differ.** A clean project rendered identically twice, but longer studies rendered slightly differently after a reopen, cause never found. Compare decoded frames after any reopen; any differing frame is a fault until explained.
- **Effects that fight clean graphic work:** Resolve's motion blur stacked on blur already rendered into the frames; sharpening, noise reduction or blur on type the viewer reads; grain multiplied in (it darkens every colour) or frozen; bloom on white interface elements, which clips and smears.

## Fusion plug-ins and add-ons: the scout.

Checked on the web on November 8, 2026. Nothing was installed.

- **Krokodove.** Procedural nodes for shapes, patterns, warps, bevels and extrusions, pseudo-3D, beat-driven animation helpers and a text scrambler. **Cost:** included; it now ships inside Resolve 21. **To get it:** nothing; learn it. Its 35 example comps come through Reactor.
- **Reactor.** The free community package manager for Fusion tools, macros and scripts. Classic Reactor stopped running in free Resolve from 19.1, so the community built Reactor Standalone, a separate desktop app (version 4 beta, build of November 7, 2025, open source under the LGPL). **What it opens up:** Vonk Ultra (no-code data nodes that drive animation from text, numbers, spreadsheets or JSON, good for counters and charts), ShaderFuse (shader effects as Fusion nodes) and many smaller tools. **Cost:** free. **To get it:** Sean installs the app from the project's GitHub releases or its Homebrew cask. It's beta: startup can take about two minutes, and its Update button updates everything at once. Quality varies by package.
- **Puppet Pin, by Tangenten.** Puppet warp for Fusion: a mesh built from the artwork's opaque pixels, up to 48 pins over 16 layers, IK and FK chains, and automatic wiggle, spring and wind for follow-through. The nearest thing to After Effects' puppet tool, and useful for cut-out animation of painted layers. **Cost:** from $49 on Gumroad, version 1.2.2, lifetime updates, no refunds; works in free Resolve and Studio. **To get it:** Sean buys and installs it.
- **Boris FX Continuum 2027** (released October 31, 2026). Includes Particle Illusion, a fast particle system, and a new vector text tool with per-letter 3D animation, counters and countdowns; Resolve is a supported host. **Cost:** $215 to $765 a year or $365 to $2,195 to buy, depending on host; the 2026 Resolve version was $325 a year. **To get it:** a paid licence and installer; heavy for what Fusion already does.
- **Skip:** small text-animator macros (about $13 to $20; the Follower already does this) and MotionVFX template packs (Apple bought MotionVFX in March 2026, and its Resolve future is unclear).

**Recommendation.** Get nothing yet: Resolve 21 already includes Krokodove, the Follower, shapes, particles and Lottie, and the first job should push those. If a job needs a community tool, Reactor Standalone is the first install (free, Sean's yes and his hands). Puppet Pin is the first purchase worth making, at about $49, when a job needs cut-out character animation finished in Fusion rather than drawn in Grease Pencil. Continuum waits for a job that outgrows Fusion's own particles.

## Safety.

- **One driver at a time,** person or agent.
- **Read first.** Check what's running and read the open project's name. If it's one of Sean's own projects, stop and ask him before touching it: creating or loading a project closes the open one.
- **One new project, uniquely named,** checked unused first. Never load a project you didn't create; never delete, archive or quit anything you didn't start; never change preferences, presets or the database; never touch a cloud project.
- **Files that can carry code.** Never load a `.comp`, `.setting`, `.drp`, `.drx` or `.drfx` that a person didn't make or review: Fusion comps can run scripts, and colour nodes can hold code. Every plug-in, Fuse and Reactor package runs inside Resolve with full access to the Mac, so installing one is Sean's call, from a source he trusts.
- **Uploads and money.** Resolve itself uploads nothing for local projects. Media moves between Macs by rsync, never through GitHub, with checksums compared. Any purchase above is Sean's, asked when a real job needs it.
