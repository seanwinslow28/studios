# Lottie Creator.

Lottie Creator is LottieFiles' animation editor in the browser. It makes Lottie files: small vector animations that play in apps and on websites through a Lottie player, and dotLottie files, a packaged form that can hold several animations, colour themes and interactive logic. Sean pays for it, and an MCP connection lets Claude Code build and edit animations in an open Creator tab. Read this before making an icon, a micro-animation, a loader or a small end-card mark.

## What it's best at.

- **Light vector motion for web and apps.** A tick that draws itself on, a crown that pops, a trophy that sparkles, a loader, an empty-state character that breathes.
- **One file, many looks.** Themes built from colour tokens let a single animation switch between, say, light and dark mode or brand colours at run time, without a second file.
- **Simple interactivity.** Creator's state machines (idle, hover, clicked, and the transitions between them) are packaged inside the dotLottie and run wherever a dotLottie player runs.
- **Line drawings inside a film.** A Lottie dropped into a HyperFrames composition is seeked frame by frame by the renderer, so it lines up with everything else.

Where another tool wins: rigged characters, data binding and anything with real logic (Rive, which Sean also pays for); film shots of type and interface (HyperFrames); quick blinks and glances on a character already built as SVG layers, which are cleaner moved directly on GSAP's timeline in HyperFrames than round-tripped through Lottie.

## Setup.

- **Where it lives.** Creator runs in the browser at creator.lottiefiles.com, signed in to Sean's LottieFiles account. Nothing to install for the editor itself.
- **Cost** (from lottiefiles.com/pricing, November 8, 2026). The Individual plan, which lists Lottie Creator, is $19.99 a month billed yearly with 300 AI credits a month; Team is $24.99 with 600. Which plan Sean is on was not confirmed.
- **The MCP connection** (from LottieFiles' docs, November 8, 2026). The Creator MCP server is a small local program that talks to an open Creator tab. It needs Node 18 or newer (this Mac has 22), the Creator tab open for the whole session, and in Creator, Settings, then MCP Settings, then "Enable local MCP". Creator then shows "Local MCP bridge connected" and a blue MCP mark in its top bar. The command to add it to Claude Code is `claude mcp add lottiefiles-creator -- npx -y @lottiefiles/creator-mcp@latest`.
- **On this Mac** (changed November 22, 2026, on Sean's say). The server is registered for the studios folder only, pinned to version 0.2.2, which is already on the Mac (`npx -y @lottiefiles/creator-mcp@0.2.2`, Claude Code's local scope). Its registration for any other folder was removed, and an old session's bridge that had held the port since November 19 was stopped. Version 0.2.3 is out (October 29, 2026); moving to it is a download, so ask Sean first.
- **Sean connects Creator himself.** The bridge on the Mac only waits; the link is made from the Creator web page, by Sean. So before any Creator work, tell Sean you're about to use it, and wait for him to say the badge shows.
- **The check that proves it works:** `lsof -nP -iTCP:3847` shows which process holds the bridge's local port (one session at a time), and the "Local MCP bridge connected" notice in Creator confirms the link. Then make one read-only call, `read_scene`, which returns the scene's size.
- **LottieFiles changed its MCP on November 10, 2026.** Its docs now describe three ways in, compared at docs.lottiefiles.com/en/developers/which-mcp, and the local bridge above is no longer among them (its package is still published, with 0.2.3 tagged as the latest and no warning to stop using it):
  - **The hosted Creator MCP**, at `https://creator.mcp.lottiefiles.com/mcp`. Nothing to install and no Creator tab: it runs a headless Creator on LottieFiles' servers. Twelve tools, among them `creator_exec` (runs a script against the scene), `creator_preview` (filmstrips and stills Claude can see), `creator_document` (revisions and restore), `creator_account` (shows the credit balance) and `creator_download_file`. It **exports** Lottie JSON, dotLottie, MP4, WebM, GIF, AVIF, WebP and PNG. It lists markers, path keys, masks and mattes, but not state machines. Its documents stay on LottieFiles' servers, and generated or traced pictures, SVGs included, spend AI credits; saves and previews are free. Setup: `claude mcp add --transport http --scope user creator-mcp https://creator.mcp.lottiefiles.com/mcp`, then a LottieFiles sign-in in the browser, which only Sean does.
  - **WebMCP** (since September 10, 2026): edits the file open in a Creator tab from an assistant inside a browser that supports it, such as the ChatGPT desktop app's browser. It's on by default (Settings, MCP Settings, "Enable WebMCP"). Claude Code can't call it.
  - **The LottieFiles MCP**, for account data only (below).
- **Which route, for a job.** The local bridge edits the file Sean has open, so he watches it happen and can take over, but Claude can't see the canvas or export. The hosted server can see its own work and export it, which suits a test Claude must judge by eye, but it is a new sign-in, a change for every folder, and work stored on LottieFiles' servers. Put the choice to Sean, with that trade, before the first Creator step. Whether Creator still shows "Enable local MCP" for the old bridge after November 10 wasn't confirmed: check it in Creator first.
- **A different server, not to be confused with it.** LottieFiles also runs a hosted MCP server for account data (workspaces, projects, animations), signed in through the browser. It organises and changes things in Sean's workspace; it does not animate.

## Getting the best out of it.

**Bring your own shapes.** LottieFiles' own advice is that the AI is unpredictable when drawing shapes from scratch, so import clean SVG made in Affinity, or written by the lead, and let Creator animate it. Name the layers before import; the names are how you and the MCP tools find parts later. Use the strongest model available, since the result depends on it.

**What the MCP connection can do.** Grouped in LottieFiles' docs: scenes and layers (size, frame rate, duration, background); shapes, paths and text, including splitting text for per-letter motion; fills, strokes, blend modes, shadows, blur, masks and mattes; keyframes, easing, motion paths; importing SVG, Lottie files and images, and turning a raster image into vectors; theme slots and saved presets; and segments, state machines and the events that drive them. Through the local bridge, exporting is done with Creator's own controls; the hosted server (above) exports itself.

**Ease like a motion designer, not a spreadsheet.** Lottie plays the curves you give it exactly. Default ease-in-out on everything reads as generic. Give entrances a fast start and a long settle, let small parts overshoot slightly and follow the main shape a few frames late, and use the easing editor rather than presets.

**Pick the export for the destination.**

- **dotLottie** for apps and sites using the dotLottie player: smaller, and the only format that carries themes, state machines and several animations in one file.
- **Lottie JSON** for `lottie-web`, the player HyperFrames' Lottie adapter supports alongside dotLottie.
- **Video** (MP4, MOV, WebM with transparency, GIF) when the animation goes into an edit as footage.

**Lottie inside HyperFrames.** Load the file with a `lottie-web` or dotLottie player, register the player on `window.__hfLottie`, and always set `loop` explicitly: `lottie-web` treats a missing `loop` as true. A numeric loop count doesn't repeat under seeking, so bake repeats into the file. Keep the container's size fixed in CSS. Make the Lottie at the film's frame rate so its keys land on the film's frames.

**Use segments for states.** Name the stretches of the timeline (intro, idle, success) as segments; state machines and app code can then play them by name.

## Where it goes wrong.

- **It looked right in Creator and wrong in the app.** Players differ. `lottie-web`'s SVG and canvas modes and the dotLottie player (built on the ThorVG renderer) each support a slightly different set of features. Preview in the player the app will actually ship.
- **Effects that don't survive.** Blurs, glows, shadows and other effects, layer styles, 3D layers and complex expressions are the usual failures, especially in older players. Keep the animation to shapes, fills, strokes, transforms, trims and simple masks unless the target player is known to handle more.
- **Text that changes font.** Live text depends on fonts the player may not have. Convert words to shapes unless the app must swap the text.
- **Heavy files.** Embedded raster images, traced artwork with thousands of points and a key on every frame bloat the file and slow the player. Simplify paths and let easing do the in-betweens.
- **Mattes and masks that stutter.** They cost a lot to draw on phones. Use as few as the design allows.
- **The AI drew something odd.** Shapes made from scratch by the AI are the least reliable part. Import instead.
- **The bridge won't connect.** Check that "Enable local MCP" is on, the Creator tab is still open, and no other session holds the port.

## Morphs, tracing and hover, from November 2026 research.

Sources were LottieFiles' docs, help centre, release log and players' GitHub issues, all seen November 22, 2026; community tips are marked.

**Shape morphs.**

- **A path morph needs the same number of points at both ends.** LottieFiles' compatibility table says so outright. Players handle a mismatch differently (lottie-web still glitches; lottie-android draws only the shorter list), so match the counts by hand and never trust a player to fill the gap.
- **Points pair by order.** The first point of one key travels to the first point of the next. Built-in shapes start at known places: a rectangle at its top right, an ellipse at 12 o'clock, both running clockwise; a rounded rectangle has 8 points. A rectangle and an ellipse can't morph into each other as primitives at all, because they're different shape types. So convert every shape to a path, start each at the same spot (say top centre, clockwise), and run them all the same way: a path wound the other way flips inside out halfway (community, from After Effects habit). Creator's docs show no "set first vertex" or "reverse path" command; test, or rebuild the path.
- **Plan the counts.** Give every pose of a part the highest count any pose needs, and park the spare points on top of each other along a straight edge of the simpler shape. A part that appears (the clapper's hinge) starts as a collapsed sliver or a stack of points hidden inside another shape, rather than popping in. Key the fill colour on the same frames as the path, and stagger parts 2 to 4 frames.
- **Through the bridge,** morph with `animate_property` on `shape_path` (keys are `{points, closed}`); mask paths take the same form (`mask_path`). Keep the `shape_id` that `add_shape_to_layer` returns, because `read_scene` won't list it again.
- **Check the ends.** Creator 1.114 (September 24, 2026) added composition snapshots: capture a frame, then hold Option to see a Difference blend against the live canvas, where black means identical. Use it to check the first frame against the shapes picture and the last against the finished one. It doesn't work on the opt-in WebGPU renderer.
- A community plugin, "Morpher" (version 0.0.1), morphs up to six shapes with spring timing and falls back to a fade when shapes can't morph; it bakes many keys, so run its optimiser.

**Tracing a picture.**

- **For flat, geometric art, rebuild rather than trace.** Traced paths carry dozens of uneven points, which morph badly and weigh more. Put the trace, or the picture itself, on a locked layer at low opacity and draw over it with primitives and clean paths of planned point counts.
- **Creator's Vectorize** (right-click an image, or Image Options) has no settings. It "keeps the original colors" and groups layers. Raster to Vector costs 5 credits a run; whether Vectorize inside Creator, or the bridge's `vectorize_image`, bills the same isn't documented, so check the balance before and after one test image. `vectorize_image` hides the original picture rather than deleting it: delete it before export.
- **Prompt to Vector** (2 credits) has a "Vectorize" mode for clean flat output and a "Smart Grouping" mode for layers ready to animate, and takes a reference image for the colours.
- **Outside Creator, VTracer is the best free tracer for few-colour art** (version 1.0, August 2026): `--palette '#hex,…'` snaps every area to the exact studio colours, `--mode polygon` keeps edges straight, `--simplify` (1 to 2.5) means fewer curves, `--hierarchical cutout` leaves no hairline seams, `--filter-speckle` drops specks. Potrace does one colour at a time, so it needs one mask per colour.
- **What Creator's SVG import keeps:** paths, primitives, groups, fills, strokes, gradients, transforms and layer names. It drops filters, some blend modes and live text. Prepare SVG with flattened transforms and no `<use>`, text as outlines, one named `<path>` per colour area with a plain `fill` (the `id` becomes the layer name), and no embedded `<image>`.

**Hover on a web page.**

- **Plain page code is the sturdier route** for a card that answers the pointer: the card's own enter and leave events, the touch fallback and reduced motion all live in one place. Use Creator's state machine only when the file must carry its own behaviour into a host with no code.
- **If a state machine is used:** two states on the same named segment (a Lottie marker, not a frame range), one Forward and one Reverse at a higher speed, joined by immediate transitions. Leaving mid-play then reverses from the current frame, which works only from dotlottie-web 0.70.0 on. Never tweened transitions for hover: they block new changes until they finish, and since 0.83.0 events wait out the tween, so a quick in-and-out lags. Pointer events fire only over the canvas or a visible, filled layer, never over the card around it; drive the machine from the card's events instead (`stateMachineFireEvent()` or a true-or-false input). Every transition that waits for an event needs an interaction that fires it. Test rapid hover in and out in Creator's Interactivity Mode.
- **With lottie-web:** on enter `setDirection(1)` then `play()`; on leave `setDirection(-1)`, `setSpeed(1.5)`, `play()`. It carries on from the current frame. Avoid `playSegments()`: direction is ignored after it, and reversed segments flash frame 0 (both open bugs). lottie-web hasn't had a release since 5.13.0 in November 2024, and its worker mode has an open security hole, so use the non-worker light build.
- **With dotlottie-web:** `setMode('forward'|'reverse')`, `setSpeed()`, `play()`. Never `setSegment()` with the start after the end (it once froze the page). `tween(frame, ms)` goes straight from the current pose to the target without the frames between, an experimental "fast return" worth testing against plain reverse.
- **Faster on the way back.** An ease-out entrance played in reverse becomes an ease-in exit, and speed 1.4 to 1.5 makes it about two-thirds as long, which matches LottieFiles' own motion skill ("Exit = 65-75% of entrance").
- **Weight** (measured November 22, 2026, compressed as the browser downloads it): lottie-web's light SVG build is about 40 KB; dotlottie-web is about 21 KB of script plus a 476 KB engine. For a few simple shape animations lottie-web is a tenth of the weight; dotLottie earns its size only for state machines, themes, its extra effects or several animations in one file. Six small files loaded as they come near usually beat one bundle.
- **Loading dotlottie-web well:** `DotLottie.preload()` starts the engine early; a `<link rel="preload">` must name the exact, version-pinned engine file or it downloads twice; `setWasmUrl()` self-hosts it. `freezeOnOffscreen` is on by default; `destroy()` what's gone; `useFrameInterpolation: false` halves the drawing for slow art. Pin 0.83.2 or later (open bugs: search crawlers may fail to index pages that load it; the canvas can gain gaps above and below).
- **Sharpness.** dotlottie-web draws at 0.75 of the screen's pixel density by default, which softens flat edges: set `renderConfig: { devicePixelRatio: Math.min(window.devicePixelRatio, 2) }` and size the box exactly to the slot in CSS. lottie-web's SVG stays sharp; `rendererSettings: { viewBoxOnly: true }` fixes its known blur.
- **Reduced motion and phones.** No Lottie player handles reduced motion itself. Show a still picture and never load the player; listen for the setting changing too. On a device without hover (`matchMedia('(hover: hover) and (pointer: fine)')` false), play once when an IntersectionObserver sees the picture, then stop watching.
- **LottieFiles' own motion skill** (`npx skills add LottieFiles/motion-design-skill`, updated November 19, 2026) holds duration and easing tables, a hover rule ("Hover enter <100ms; hover exit 150-200ms") and a quality checklist. Installing it is a download: ask Sean.

## How the bridge really behaves.

Learned hands-on in October and November 2026, from three full builds in Creator and from reading the bridge's own code (version 0.2.2).

- **One port, one tab, one session.** The bridge is a stdio MCP server for Claude Code plus a small WebSocket server on `127.0.0.1:3847`. The Creator tab is the client: it connects to that port once "Enable local MCP" is on. Only the page `https://creator.lottiefiles.com` is accepted, and a second tab is refused ("Another tab is already connected").
- **Limited mode.** Every Claude Code session that has the server registered starts its own bridge. If the port is already taken, the newcomer logs "Starting in limited mode (MCP server only, no WebSocket)": its tools still appear, but every call answers "No Creator tab is connected", and it never retries. This is the usual reason the bridge "won't connect".
- **The handover recipe** (tested November 3, 2026). Find the holder with `lsof -nP -iTCP:3847`; stop that bridge process (not its session) with Sean's yes; stop this session's own limited-mode bridge too; then make any Creator call. Claude Code restarts the bridge, it takes the port, and an open Creator tab reconnects by itself within seconds, with no clicks in Creator.
- **Drops and timeouts.** A tab that misses a 5-second ping is dropped. Calls run one at a time; one that runs past 70 seconds times out, can leave half-made edits, and the bridge refuses new calls until it settles. Keep each call small. Switching Creator files drops the bridge; turn Local MCP on again until the badge shows.
- **It can't see or export.** About 108 tools are registered. There is no export, publish, share or upload tool, and no snapshot of the canvas. You see the result only through Sean's screenshots, a browser view of the tab, or a render of a file Sean exports (Export, Drafts, Optimized dotLottie or Lottie JSON, Download).
- **Work in a new, empty file.** The bridge can change or delete anything in the open file.
- **AI credits.** Across three full builds the bridge spent no credits (measured October 2026: the same balance before and after). Creator's own AI features are priced per run (LottieFiles' credits page, October 29, 2026): Lottie AI 5, Raster to Vector 5, Motion Copilot 3, Prompt to Keyframe 3, Prompt to State Machines 3, Prompt to Theming 2, Prompt to Vector 2. The bridge's `vectorize_image` runs Creator's vectorizer; whether it bills like Raster to Vector isn't documented, so ask first. The bridge can't read the balance; Sean checks it in the Copilot panel.

**Tools with a sting in their defaults.**

- `split_text` deletes the original text, `apply_motion_path` deletes the source path, and `bend_shape` swaps out the first shape, unless told not to.
- `animate_property`, `set_group_transform`, `apply_bounce`, `apply_squash` and `apply_coupled_shadow` clear a property's existing keys by default; `apply_keyframes` doesn't.
- `set_scene_settings` changes the whole scene's size, frame rate and length. `rename_segment` silently breaks state machines that use the old name.
- `import_asset` with a `url` makes Creator fetch from the web: pass the SVG inline as `content` instead.
- Every `delete_*`, `remove_*` and `break_scene_layer` tool is destructive.
- Easing presets (ease-in, ease-out, ease-in-out, gentle-out, snappy-out, smooth-in-out, overshoot-soft, overshoot-hard, anticipate) work only in `apply_keyframes` and `retime_keyframes`; elsewhere give a cubic bezier.

**Quirks that cost time.**

- A keyframe's easing applies to the stretch leaving that key.
- `read_keyframes` never returns easing, so restate every easing when rewriting a property.
- No bridge tool sets stroke dashes, line caps or line joins; Sean sets them in the Stroke panel. Line ends came out round by default.
- `add_shape_to_layer` takes no position: an offset sub-shape is a path drawn in the layer's own coordinates.
- `read_scene` lists no shape ids inside a layer, so a buried shape can't be reordered; build a new layer instead. Its bounds ignore fills, so its "hidden" and "clipped" warnings can be false alarms. Moving a node in Creator's own controls changes its layer id.
- A fill grouped with a Trim Path gets trimmed too; give fills their own layers.
- A mask that starts as a 1-pixel circle shows as a dot; keep the layer at 0% opacity until it grows.
- `set_scene_background` is for preview only: exports always have a transparent background.
- Chrome saves a repeat download as `name (1).lottie`.

**What Creator could and couldn't do, as tested in October 2026.**

- Masks Add and Subtract work, including an animated mask whose path morphs; it exported and played in both lottie-web and dotlottie-web. Animated shape paths morph and export too.
- Track mattes are Alpha and Inverted Alpha only, one per layer, with the matte directly above. No luma mattes.
- No boolean operations or merge paths, no expressions (After Effects expressions must be baked), no 3D layers, cameras or lights.
- Effects (drop shadow, blur, tint, tritone, colour overlay) play in dotlottie-web, but lottie-web silently drops them.
- Several scenes in one file export into one `.lottie`. A dotLottie version 2 file is a zip holding `manifest.json` plus `a/<scene>.json`, one per scene (version 1 used `animations/`); unzip it to get plain Lottie JSON.
- Line-drawing scenes built entirely through the bridge, at 300 by 300 and 60 frames a second, exported at 2.6 to 5 KB each.

**Lottie inside HyperFrames, tested.**

- HyperFrames' Lottie adapter seeks every lottie-web player on the page, registered or not, so a player meant to hold one frame gets moved too: freeze it as plain SVG or destroy it.
- It seeks to the render time minus the start of the player's nearest `[data-composition-id]` ancestor. So a player can sit inside anything that moves or turns in 3D: give its box `data-composition-id` and `data-start` (the cue in seconds) and register a stub `window.__timelines[id]`. It's blank on its cue frame and draws from the next.
- It was frame-exact (a seeked frame matched the Lottie frame pixel for pixel), gave identical frames on two renders, and moved on every frame at 60 frames a second from a 30-frame-a-second Lottie.
- Load the JSON synchronously, from a local script that sets a variable. The adapter doesn't wait for a player to be ready.
- A sub-composition must load the player inside its own `<template>`, or HyperFrames' lint fails (`missing_lottie_script`).
- One Lottie per cue, each in its own sub-composition, so retiming is an edit to `data-start`, not to Creator.
- The player used: lottie-web 5.13.0, its SVG-only build (`lottie_svg.min.js`, 243 KB), vendored into the project with its MIT licence. Adding it fresh is a download: ask Sean.

**Creator or code, by job.** Creator wins at line-drawn icons, trim-path draw-ons, mask reveals, shape morphs, and anything Sean wants to retime by hand in the graph editor. Code wins at kinetic type (real fonts, exact words; Creator splits text into one layer per letter) and at interface details that must match a real product's CSS.

## Safety.

- **Everything in Creator is in LottieFiles' cloud.** Keep confidential names, logos, client artwork and private data out of Creator unless Sean says yes.
- **Never publish** an animation or use a hosted LottieFiles link; those are public. Export files instead.
- **AI credits.** Creator's AI features spend the plan's monthly credits. Check the balance before and after a session, and ask before a large batch.
- **Tell Sean before using Creator.** He turns the connection on in the Creator web page, so say plainly that you're about to use it, and in the same message say whether the bridge's port is free.
- **Another session's bridge.** If another session holds the port, tell Sean which one and ask before stopping it. Stop only the bridge process, never the session.
- **Adding the MCP server** for another folder changes Claude Code's configuration and brings back the fight over the port; ask Sean first.
