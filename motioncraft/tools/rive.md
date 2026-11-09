# Rive.

Rive is a design and animation tool whose files run live inside apps, websites and games. A Rive file is not a video: it carries shapes, bones, animations and the logic that decides which animation plays, so it can react to a pointer, to data and to code. Sean pays for Rive and wants its full power used when a job calls for it. Read this before any interactive piece or small runtime animation.

## What it's best at.

- **Animation that responds.** A button that squashes when pressed, a mascot that follows the cursor and blinks on its own, a progress character whose mood follows a number.
- **Characters with real rigs.** Bones, weighted skinning, meshes on images and constraints such as inverse kinematics (point the hand and the arm follows) make one drawing pose in many ways.
- **Data-driven pieces.** A chart, a scoreboard or a card whose text, colours and lists come from the app at run time.
- **Tiny, sharp files.** A `.riv` file is small and drawn by Rive's own renderer at any size.

Where another tool wins: a linear film shot with type and interface (HyperFrames); light icon animation that must ship as Lottie (Lottie Creator); painted or hand-drawn looks (Krita, Grease Pencil); 3D (Blender). Rive can render video, but it shines when the piece stays live.

## Setup.

- **Installed:** the Rive Early Access desktop app, version 0.9.560, at `/Applications/Rive Early Access.app` (checked November 8, 2026). Rive files live in Rive's cloud, not on the Mac's disk.
- **The connection to Claude Code.** The desktop app runs a local MCP server (a bridge that lets Claude Code drive the editor) at `http://127.0.0.1:9791/mcp`, registered in Claude Code as `rive`. It is there only while the app is open. Its tools, named `mcp__rive__*`, cover artboards and hierarchy, shapes, paths and text, bones and mesh rigging, the animation editor and state machines, listeners, view models and data binding, scripts and tests, assets, screenshots of an artboard and export.
- **The command that proves it works:** the `mcp__rive__session_info` tool lists the files open in the editor. It answered on November 8, 2026.
- **Plans** (from rive.app/pricing, November 8, 2026). Free costs nothing but "Free exports play a Rive splash screen" and allows three files. Cadet, $9 per editor a month, exports without the splash and allows unlimited files. Voyager, $32 per editor a month, adds libraries, embed hosting and $20 of AI agent credits per editor. Sean is on a paid plan (he confirmed this on November 8, 2026), so exports carry no splash and video rendering works.
- **Rive's skills** for Claude Code (`rive`, `rive-interactive`) hold runtime patterns for web and app code.

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

## Safety.

- **Everything in Rive is uploaded.** Files live in Rive's cloud. Ask Sean before importing his private material or anyone else's artwork.
- **Ask Sean** before publishing a hosted page or embed link (public), spending AI agent credits beyond a small test, changing plans, or using the command line's monthly publishes.
- **Export writes locally** to a folder you name and never overwrites an existing file.
- **Simulation runs scripts.** It reverts the values it writes but runs listener actions, scripts included, as real playback would.
