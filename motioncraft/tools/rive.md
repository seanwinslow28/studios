# Rive.

Rive is a design and animation tool whose files run live inside apps, websites and games. A Rive file is not a video: it carries shapes, bones, animations and the logic that decides which animation plays, so it can react to a pointer, to data and to code. Sean pays for Rive and wants its full power used when a job calls for it. Read this before any interactive piece or small runtime animation.

Start from Rive's command-line tool. Sean chose it on November 19, 2026: "the Rive CLI gives Claude Code more tools to work with." The scene is a text file on the Mac that Claude writes, builds, checks and photographs itself, and the desktop editor is there for when someone wants to see or adjust the result by hand.

## What it's best at.

- **Animation that responds.** A button that squashes when pressed, a mascot that follows the cursor and blinks on its own, a progress character whose mood follows a number.
- **Characters with real rigs.** Bones, weighted skinning, meshes on images and constraints such as inverse kinematics (point the hand and the arm follows) make one drawing pose in many ways.
- **Data-driven pieces.** A chart, a scoreboard or a card whose text, colours and lists come from the app at run time.
- **Tiny, sharp files.** A `.riv` file is small and drawn by Rive's own renderer at any size.

Where another tool wins: a linear film shot with type and interface (HyperFrames); light icon animation that must ship as Lottie (Lottie Creator); painted or hand-drawn looks (Krita, Grease Pencil); 3D (Blender). Rive can render video, but it shines when the piece stays live.

## Setup.

- **The command-line tool:** `rive`, version 1.10.0, at `~/.rive/bin/rive`, signed in to Sean's Rive account (checked November 19, 2026). `rive update` installs a newer version. Only Sean signs in (`rive login`); the sign-in is needed to hand work on (push, publish, list the account), not to build, preview or check.
- **The check that proves it works:** `rive doctor` reports the version, the sign-in, the preview port and the project. On November 19, 2026 everything that matters for the web came back ok (the Android and iPhone build lines warn, and don't matter here).
- **The desktop app:** Rive Early Access, version 0.9.560, at `/Applications/Rive Early Access.app` (checked November 19, 2026). Files made in the editor live in Rive's cloud; a command-line project lives on the Mac as text files until it is pushed.
- **The connection to Claude Code.** The desktop app runs a local MCP server (a bridge that lets Claude Code drive the editor) at `http://127.0.0.1:9791/mcp`, registered in Claude Code as `rive` for every project. It is there only while the app is open: with the app closed on November 19, 2026, Claude Code reported it as failing to connect. Its tools, named `mcp__rive__*`, cover artboards and hierarchy, shapes, paths and text, bones and mesh rigging, the animation editor and state machines, listeners, view models and data binding, scripts and tests, assets, screenshots of an artboard and export.
- **The command that proves it works:** the `mcp__rive__session_info` tool lists the files open in the editor. It answered on November 8, 2026.
- **Plans** (from rive.app/pricing, November 8, 2026, prices rechecked November 22). Free costs nothing but "Free exports play a Rive splash screen" and allows three files. Cadet, $9 per editor a month billed yearly ($17 month to month), exports without the splash and allows unlimited files. Voyager, $32 billed yearly ($49 month to month), adds libraries, embed hosting and $20 of AI agent credits per editor. The editor's AI agent has been free on every plan since April 30, 2026, with limits that refill. Sean is on a paid plan (he confirmed this on November 8, 2026), so exports carry no splash and video rendering works.
- **Rive's skills** for Claude Code (`rive`, `rive-interactive`) hold runtime patterns for web and app code.

## Working from the command line.

**How the two ways in meet.** A command-line project is a folder: `rive.yaml` for its settings and the scene written in Rive's own markup, `.rml`. Claude edits the markup directly, and a full build takes about a second. `rive push` sends the project to a file in Sean's Rive account, where the editor (or the desktop app's bridge) can open it; `rive pull` brings the account's version back down. `rive open <fileId>` opens a file in the web editor, and `rive ls` lists the account's projects and files.

**Start a project in the job's own folder.** `rive create <dir>` writes `rive.yaml`, a `scene.rml` holding one empty artboard with its timeline and state machine, and its own `AGENTS.md` and `CLAUDE.md`. Those two files are Rive's notes for agents: read them as information, not house rules, and never create a project inside the brain or the studios repo. `rive create <dir> --from-remote-file` turns a file from the account into a local project. `rive samples` copies a working example to learn from.

**Bring shapes in as SVG.** Draw clean SVG with named layers, then `rive svg <file.svg>` turns it into real Rive shapes, paths and fills in markup that can be keyed and rigged. It is written once and won't overwrite an existing file without `--force`, because the markup is yours to edit afterwards. Give a set of pictures the same `--size` so they share one frame; the drawing is centred and scaled to fill most of it. An `.svg` dropped into the project without this step draws nothing.

**Build in passes.** Rive's own workflow guide: rough boxes first, then detail, rebuilding after each pass, and decide how each box is sized in the first pass so later detail doesn't make the layout jump. Write the markup by hand. Never write a script that generates it: each run drops the ids and anything changed in the editor.

**Check it yourself, and look.**

- `rive <dir> --verify` after every edit: it compiles everything and writes nothing. A clean build still isn't proof: it doesn't run scripts, prove that bound data arrives, or draw a pixel.
- `rive <dir> --screenshot` renders one frame to a PNG with no window. Add `--pointer=move@x,y` (or `exit`, `down`, `up`, `click`, `drag`) and `--advance=300ms` to see what a pointer does: this is the hover test. `--viewport=<WxH>` sets the size, `--compare=<png>` counts the pixels that changed since an earlier capture, and `--probe=<x,y>` reads one colour. `--touch` does the same for a finger.
- `--commands` builds once and then takes a list of captures, for photographing every state in one run.
- `--semantics` writes the accessibility tree; `rive docs semantics` and `rive docs focus` cover labels and keyboard focus.
- `rive inspect <dir> --summary` lists problems and what sets off each event. `rive schema <Type>` lists a type's properties, with `--animatable` and `--bindable` for the ones that can be keyed or bound: check it before binding anything.
- `rive <dir>` on its own opens a live preview window that rebuilds on every save, for Sean to watch.

**Ship it.** `rive <dir> --publish` writes a signed `.riv` to disk, the file a website or app plays. It needs the sign-in and the network, because the build is signed on Rive's servers. `--publish=web` puts up a public page instead: ask Sean first.

**The docs travel with the tool.** `rive docs` lists the topics; start with `overview` and `workflow`, read `gotchas` before a first real build, and use `rive docs --search <text>`. They match the installed version, so trust them over memory.

## Getting the best out of it.

**Design the data before the drawing.** Data binding is how a Rive file talks to the world now. A view model is a named set of properties (numbers, text, colours, true-or-false values, triggers, enums and lists); an instance holds actual values; a binding ties a property to something in the scene. Write down what the app will tell the animation and what the animation will tell the app, then build the view model to match. Runtime code then just sets and watches properties. Rive Events are the older way to signal code; use a view-model trigger instead.

**Use the defaults, then add layers.** A new artboard already has one timeline and one default state machine wired to it. Rename the timeline and key it; don't create a second state machine by habit. Inside the machine, give each independent concern its own layer: the body's pose on one, the face on another, an idle blink on a third. Layers play together, so the blink never has to know what the body is doing.

**Transitions on conditions, inputs from listeners.** A listener catches pointer events (enter, exit, down, up, click, drag) on a target shape and sets a view-model property; transitions fire on conditions against those properties. A hover state is a true-or-false property set by an enter listener and cleared by an exit listener, with two transitions testing it. Every listener needs a target: an untargeted one is not exported. For pointer input across the whole artboard, add a background shape and target that.

**Verify the machine runs.** `animation_editor` with `simulateStateMachine` plays the machine headlessly with scripted inputs and reports states entered and transitions taken. An empty trace means nothing fired. Then `capture_artboard` to look at the result.

**Rig with weights, not just parents.** Parenting a shape to a bone makes it follow rigidly; binding the path's points to bones lets it bend. Blend the weights across a joint for a smooth bend, and convert rectangles and ellipses to custom paths before binding. Add a mesh to a raster image to bend it with bones.

**Converters keep logic out of the app.** A converter transforms a bound value on its way through: a number into text, a range mapped onto another, a formula, rounding. Check the existing converters before making one, because the MCP tools can't delete one made by mistake.

**Scripting for what the editor can't do.** Rive's scripts are written in Luau, a typed language derived from Lua, and run identically in the editor and the runtimes. Each script follows a protocol that limits what it can touch: custom drawing (node), layout helpers, converters, path effects, custom transition conditions, listener actions, shared helpers and unit tests. Read `get_scripting_reference` with the topic `rules` before writing one, and `viewmodel_definitions` when it touches data. Run the tests with `run_tests`.

**Bind text to the run.** When binding text, bind the text run inside the text object, not the text object itself.

**Getting Rive into a film.** Rive's editor renders video through render presets in animate mode (H.264, WebM, GIF, PNG and SVG sequences), on Rive's cloud renderer and only on paid plans. The installed HyperFrames skills have no Rive player adapter, so a live Rive file inside a HyperFrames composition is untested; bring Rive into a film as a rendered sequence.

## Morphs, hover and the web, from November 2026 research.

From Rive's own docs (the website and the ones inside the command-line tool, version 1.10.0), its runtime code and its community, all seen November 22, 2026. Lines marked "tested" were built and measured on this Mac with the command-line tool, headless; none has been tried in a real browser yet.

**How a morph really works.**

- **Rive has no "morph A into B" feature.** A morph is one custom path whose points you key: each point's position, a corner's radius, and each handle's angle and length. So the start and end share one set of points: the count and each point's type can't change. Build the path for the more complex end and park the spare points on the simple shape, stacked on a corner or spread along an edge.
- **Use one point type for everything that morphs: the detached cubic point (`CubicDetachedVertex`).** With both handle lengths at 0 it's a sharp corner; keying the lengths up rounds it. A circle of radius r is four such points at the compass points with handle length r × 0.5523 (44.18 for r = 80). Each handle's angle points from the point to its handle, so a smooth point has its in-angle equal to its out-angle plus π. Tested: a circle keyed into a rectangle this way.
- **Every point you key needs an `id`, and `rive svg` writes none.** Add them by hand.
- **Point order decides whether the shape twists.** Tested: circle points at the compass points, sent to rectangle corners, made the shape turn about 45° on the way. Put the circle's points on the diagonals, or send each point to its nearest corner. Rive has "Reverse Direction" but no "Set First Vertex".
- **Winding must be declared.** `isClockwise` defaults to true and nothing checks it; a wrong one can cut a hole or make a contour vanish. In Rive's y-down space, top, right, bottom, left is clockwise.
- **Many changes need no point work at all.** A rectangle's corner radius keyed up turns it into a pill or a circle; a star's inner radius is keyable. But converting a shape-tool shape to a path drops those settings and any keys on them.
- **Faking a morph between unrelated shapes.** A `Solo` shows one child at a time (key its `activeComponentId` with `KeyFrameId` on property 296, hold keys; a `KeyFrameDouble` there silently does nothing). Morph the simple shape toward a rough outline of the object, then swap to the detailed parts on the frame where the outlines match. Trim paths draw detail lines on afterwards; a `GroupEffect` with a `TargetEffect` lets one keyed trim reveal many strokes at once.
- **Fluid, not mushy:** one path per part of the object (board, arm, stripes), parts staggered a few frames, overshoot only on arrival, and a whole group faded with one opacity key on its wrapping node. Key only the points that move ("Key All Vertices", Shift+K, bloats the file; community).
- **A true morph between different point counts needs a script** (a path-effect script that resamples the outline, like the `wavy_effect_as` sample). Nobody has published one; and a file with scripts must be signed with `--publish` for the web.

**Keys and easing in the markup.**

- `<LinearAnimation fps="60" duration="36" loopValue="oneShot">` holds `<KeyedObject objectId=…>`, which holds `<KeyedProperty property="x">`, which holds the keys. The key element must match the property's type (`KeyFrameDouble`, `KeyFrameColor`, `KeyFrameBool`, `KeyFrameId` and so on): a mismatch builds clean and does nothing. One-shot, the default, holds its last frame.
- **A key with no easing snaps:** the default is `hold`. The ease sits on the key that starts a stretch; the last key's ease is never read. `cubic` needs a nested `<CubicEaseInterpolator x1 y1 x2 y2/>` (the same four numbers as CSS `cubic-bezier()`), or it eases nothing. `cubicValue` gives real overshoot in the property's own units; `elastic` takes amplitude and period.
- Keys are absolute and on whole frames at the animation's `fps` (default 60). Author each keyed property at its frame-0 value.
- **Units:** animation lengths are in frames, transition lengths in milliseconds, rotation in radians.

**Hover that reverses cleanly.**

- **One true-or-false property beats triggers.** An enter listener sets `hover` true, an exit listener sets it false. A missed trigger leaves a card stuck.
- **The obvious two-state machine rewinds on a quick re-hover (tested).** Idle and Morph states, a fast blend back, "Pause Source When Exiting" (`pauseOnExit`) and "Allow exit during transition" (`enableEarlyExit`): fine for a slow pointer, but pointing again during the return restarts the morph from frame 0, so the shape first slides back toward the shapes. `reset="true"` changed nothing. A negative state speed isn't a clean reverse either: it plays from the clip's start.
- **The better pattern scrubs the timeline with an eased value (tested).** A `Joystick` plays the morph timeline at whatever position its x gives (−1 the first frame, 1 the last). Bind x to `hover` through a chain of converters: to-number, then a range mapper (0..1 to −1..1), then an interpolator. Bind the interpolator's own duration (property key 756, in seconds) to `hover` too, through to-number and a range mapper (0 gives 0.25 s, 1 gives 0.6 s). Measured: 36 frames forward, 15 back, retracing the parts' stagger in reverse. It needs no transitions: the machine is one idle state. Pointing again mid-return drifts about 15% further toward the shapes before turning, but never jumps. The wiring, as it built:

```xml
<DataConverterToNumber id="0:90"/>
<DataConverterRangeMapper minInput="0" maxInput="1" minOutput="-1" maxOutput="1" id="0:91"/>
<DataConverterInterpolator interpolationType="linear" duration="0.6" id="0:92">
  <DataBindContext sourcePathIds="VM-hover" propertyKey="756" converterId="0:95"/>  <!-- duration follows hover -->
</DataConverterInterpolator>
<DataConverterGroup id="0:93">  <!-- hover to scrub position -->
  <DataConverterGroupItem converterId="0:90"/><DataConverterGroupItem converterId="0:91"/><DataConverterGroupItem converterId="0:92"/>
</DataConverterGroup>
<DataConverterRangeMapper minInput="0" maxInput="1" minOutput="0.25" maxOutput="0.6" id="0:94"/>
<DataConverterGroup id="0:95">  <!-- hover to seconds: 0.25 back, 0.6 forward -->
  <DataConverterGroupItem converterId="0:90"/><DataConverterGroupItem converterId="0:94"/>
</DataConverterGroup>
<!-- inside the artboard: -->
<Joystick posX="0" posY="0" width="100" height="100" x="-1" xId="ID-OF-MORPH-TIMELINE">
  <DataBindContext sourcePathIds="VM-hover" propertyKey="299" converterId="0:93"/>
</Joystick>
```

- **Transition flags,** if a machine does use transitions: `enableEarlyExit` ("Allow exit during transition"; without it a layer ignores conditions until the blend ends, and a trigger fired mid-blend is lost), `pauseOnExit`, `enableExitTime` with `exitTime`, `durationIsPercentage`, and `exitTimeIsPercetange`, whose misspelling is required. A transition's duration is bindable (key 158).
- **Markup traps:** states take no `name` (a build error). Declare the `StateMachine` before any `LinearAnimation`, or the editor opens on the timeline. Space states 100 to 400 apart or they stack in the editor. Bindable-property keys: true-or-false 634, number 636, text 635, colour 638, enum 637; integer and trigger share 686. A key copied from the wrong row builds clean and binds nothing.
- **1D blend states** mix poses by weight rather than scrubbing time. The axis runs 0 to 100, children in rising order, every blended property keyed in every pose. They've been linear since July 2024, so older forum advice is stale.

**Hit areas and phones.**

- A shape with no paint at all works as a hover target (tested). Transparent fills and opacity 0 are still hit-testable, so neither turns a target off; to disable one for part of a timeline, key it off the artboard with hold keys. Every listener under the pointer fires unless a shape above has `isTargetOpaque="true"`.
- **Pointer exit can be missed at the canvas's edge.** Inset the hit rectangle a few pixels (532 by 322 on a 540 by 330 artboard worked). The web runtime's `dispatchPointerExit`, on by default, sends exit when the pointer leaves the canvas.
- **On touch, a tap is enter then exit at once.** Tested: a tap twitches the morph about 15% and back. On phones set `shouldDisableRiveListeners: true` and have page code set `hover` true when the card scrolls into view (tested with `--data=hover=true`).
- If a press state exists, the exit listener must clear it too, or a pointer leaving while held strands the card.
- Rive's cursor request does nothing on the web: use CSS `cursor: pointer`.

**On the web page.**

- **Which runtime.** Rive recommends `@rive-app/webgl2` by default (about 1.05 MB compressed). `@rive-app/canvas-lite` (about 0.37 MB) drops text, layouts, audio, scripting and feathering, and anything using them silently doesn't appear; for flat filled shapes with no text it's the light choice. `@rive-app/canvas` lacks layer masks. `@rive-app/webgl` gets no updates after 2.37.0. The test file built to about 1.2 KB, so the runtime is nearly the whole cost, paid once per page. Releases come almost daily (2.54.0 on November 21, 2026): pin an exact version.
- **One engine, one file.** The runtime loads its engine once for every canvas; to self-host, call `RuntimeLoader.setWasmUrl()` before any instance, serve it as `application/wasm`, matching the package version exactly, and make any `<link rel="preload">` name that exact URL or it downloads twice. Load a file once with `new RiveFile({src}).init()` and hand it to each instance as `riveFile:`; one `.riv` with six artboards (picked with `artboard:`) is one download for all six cards. Always pass `stateMachine:`, or the runtime plays the first timeline instead.
- **Many canvases:** set `useOffscreenRenderer: true` on every webgl2 instance so they share one graphics context (false by default in plain JavaScript). Plain JavaScript doesn't pause canvases that are scrolled away, only hidden tabs: add an IntersectionObserver calling `stopRendering()` and `startRendering()`. A settled machine stops advancing until input wakes it.
- **Sharpness:** fix the canvas's CSS size, build the artboard at exactly 540 by 330 (or 1080 by 660) so `Fit.Contain` leaves no gap, and call `resizeDrawingSurfaceToCanvas()` on load and on resize. The command-line captures always render at 1×, so they can't show softness on a high-density screen: check in a browser.
- **From page code:** with `autoBind: true`, `rive.viewModelInstance.boolean('hover').value = true`. Hovering the studio's name beside the canvas is then that name's own enter and leave events setting the same property.
- **Reduced motion:** Rive doesn't detect it. Check `matchMedia('(prefers-reduced-motion: reduce)')` first and show the still picture without ever loading the engine. (Inside a file, the neat version is a `motionSeconds` number bound to every interpolator's duration, set to 0.)
- **Gotchas:** keep the still picture under the canvas and hide it on load. iOS Lockdown Mode blocks the engine, and it covers the first-frame flash. A site's content security policy needs `'wasm-unsafe-eval'`; a `.riv` from another origin needs CORS; call `cleanup()` on teardown. The web can skip an animation's first frames, and a step keyed as a one-frame ramp flashes on 120 Hz screens: use hold keys for instant changes.

**Bringing artwork in.**

- **What `rive svg` keeps:** rectangles, circles and ellipses as editable shapes; paths, lines and polygons as point paths; groups as nodes; gradients; dashes; clip paths; styles and classes; `use` inlined. An element's `id` becomes its Rive name.
- **What it drops or bends:** text, images, filters and blend modes are dropped, and skew is approximated. A mask becomes a hard clip (tested: a cut-out hole was lost); bake holes into one path with `fill-rule="evenodd"`, which survives. A stroked line or polyline without `fill="none"` gets a black fill. The output has no state machine or style.
- **Size:** `--size` fits the drawing to 90% of the frame inside a scaled wrapper, so full-bleed art gains a 5% border. For a picture that must fill 540 by 330, export the SVG with `viewBox="0 0 540 330"` and convert without `--size` (or with `--no-fit`).
- **Prepare the SVG:** text outlined, skew flattened, masks turned into compound paths, each moving part its own element with an `id`. In SVGO turn off `mergePaths` and `convertShapeToPath`, which fuse parts and lose Rive's editable shapes.
- **For flat, geometric art, rebuild rather than trace.** Primitives give exact geometry and planned point counts; use a trace only for placement. If tracing: VTracer (`--palette` snaps to the exact colours in its 1.0 version; `--mode polygon`, `--simplify`, stacked layers, `filter_speckle 4`), Potrace one colour at a time, Inkscape's Trace Bitmap (multiple scans, 5 colours, Stack on, Smooth off) or Illustrator's Image Trace (limited palette of 5, "Snap Curves To Lines", Overlapping). None is installed here.
- **`rive illustrate --image=<png>`** traces a picture through Quiver's model by way of Rive's relay and writes markup directly. It needs Sean's sign-in, spends agent credits and sends the picture to QuiverAI: ask first.

**More of the command-line tool.**

- **Flags the sections above don't cover:** `--data=<path=value>` sets a view-model property (before the run, or as a step after a gesture); `--data-dump`, `--data-dump-every=<N|ms>` print the values as JSON over time; `--key`, `--text`, `--gamepad`, `--semantic-action`; `--scale` for smaller captures; `--artboard`, `--fit`; `--window` plays a command list in the live window; `--bench=<frames>` for speed; `--format=json` for one machine-readable answer; `--test` runs scripts' tests.
- **Gestures:** `--pointer=down|up|move|exit|click@x,y`, `drag@x1,y1>x2,y2[:steps]`, `wheel@…`; `--touch=down|up|move|tap@x,y`, where a lift is also an exit. Coordinates are in artboard space. `--advance` takes frames (at 60), seconds or milliseconds, and applies where it sits in the sequence; a capture with no advance is frame 0.
- **`--commands` verbs:** `advance`, `pointer`, `touch`, `key`, `text`, `data`, `screenshot`, `semantics`, `data-dump`, `viewport`, `artboard`, `fit`, `reload`, `wait-net`, `quit`. Each answers `ok` or `err`. `screenshot /dev/null` with `--probe=x,y` gives a colour trace frame by frame without image files: that's how the hover timings above were measured.
- **The hover test:** capture at rest; capture after `--pointer=move@x,y --advance=40`; capture after moving in, advancing, `--pointer=exit@x,y` and advancing again. The second must differ from the first, the third must match it (`--compare=rest.png` prints the share of pixels that differ).
- **Traps:** a `--compare` pointing at a file that doesn't exist makes every capture fail with a misleading "could not write" error, so take the reference in a separate run first. `inspect` also reports `interpolated-step` (a one-frame ramp), `dense-keys`, `rotation-looks-like-degrees` and `states-overlap`, but never checks key types or what a frame looks like.
- **Writing a `.riv` at all takes `--publish`,** even for a file with no scripts, and every push and publish counts against the monthly allowance: 50 on Free, 500 on Cadet, 5,000 on Voyager. Past it, Voyager pays from credits and the others are refused (exit code 9).
- **Exit codes:** 0 ok, 1 fail, 2 usage, 3 not signed in, 6 tests failed, 7 service unreachable, 8 tool too old, 9 allowance used up, 10 needs a workspace.
- `rive samples --path` and `rive docs --path` show where the samples and docs sit. `pointer_reactive` is the nearest sample to a hover card. The live window takes typed commands: `data hover=true`, `s` for a screenshot, `p` to pause.

## Where it goes wrong.

- **A machine stuck at Entry.** No condition ever becomes true, often because a listener has no target or a condition tests the wrong property. Simulate before anything else.
- **Stray defaults.** A leftover "Timeline" beside named animations, or a second state machine nobody meant to make, confuses the runtime code that picks one by default.
- **Bound text not changing.** Bound to the text object instead of its run.
- **Splash on the shipped piece.** Only happens if a file is exported from an account on the free plan; Sean's is paid, so a splash means the wrong account.
- **Runtime behind the editor.** Data binding and scripting need recent runtimes. An app pinned to an old Rive runtime plays the file wrongly or not at all. Confirm the runtime version the app ships with.
- **Export needing the network.** A `.riv` export resolves hosted assets online; a `.rev` backup with embedded assets downloads them. A `.rev` backup is a paid feature and may be refused; `.riv` works on every plan.
- **Leftover converters and enums.** Converters can't be deleted through the MCP tools; deleting an enum still in use needs force. Plan before creating.
- **A clean build that is still wrong.** `--verify` and `inspect` never render anything. Take a screenshot, with the pointer moves, before calling a piece done.
- **An artboard with no state machine** is only half alive. Keep the one `rive create` makes, and give every layer an entry state.
- **Bindings that compile but do nothing.** A bind to a property the target doesn't have, or a path that points nowhere, still builds. `rive schema` and `rive inspect --json` catch them.
- **Units.** Rotation is in radians; durations are in frames or milliseconds.
- **A box that vanishes.** A box set to hug its contents, with nothing inside yet, has no size.
- **Local work lost to a pull.** `rive pull` writes the account's file over the local project. Push or save a copy first.

## Safety.

- **Everything in the editor is uploaded.** Editor files live in Rive's cloud, and the command line's `rive push` and `--publish` send the work to Rive's servers too. Ask Sean before any of them carries his private material or anyone else's artwork.
- **Ask Sean** before publishing a hosted page or embed link (public, including `--publish=web`), publishing a library (`rive library publish`), spending AI agent credits beyond a small test, changing plans, or using the command line's monthly publishes.
- **Only Sean signs in.** Never run `rive login` or `rive logout` for him.
- **Export writes locally** to a folder you name and never overwrites an existing file.
- **Simulation runs scripts.** It reverts the values it writes but runs listener actions, scripts included, as real playback would.
