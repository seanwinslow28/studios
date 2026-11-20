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
- **Plans** (from rive.app/pricing, November 8, 2026). Free costs nothing but "Free exports play a Rive splash screen" and allows three files. Cadet, $9 per editor a month, exports without the splash and allows unlimited files. Voyager, $32 per editor a month, adds libraries, embed hosting and $20 of AI agent credits per editor. Sean is on a paid plan (he confirmed this on November 8, 2026), so exports carry no splash and video rendering works.
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
