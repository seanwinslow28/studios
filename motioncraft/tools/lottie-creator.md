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
- **On this Mac** (checked November 8, 2026). The server, pinned to version 0.2.2, is not yet connected to the studios repo, so its tools don't appear here; connecting it is Sean's call.
- **The check that proves it works:** `lsof -nP -iTCP:3847` shows whether a session already holds the bridge's local port (one session at a time; it was held on November 8, 2026), and the "Local MCP bridge connected" notice in Creator confirms the link.
- **A different server, not to be confused with it.** LottieFiles also runs a hosted MCP server for account data (workspaces, projects, animations), signed in through the browser. It organises and changes things in Sean's workspace; it does not animate.

## Getting the best out of it.

**Bring your own shapes.** LottieFiles' own advice is that the AI is unpredictable when drawing shapes from scratch, so import clean SVG made in Affinity, or written by the lead, and let Creator animate it. Name the layers before import; the names are how you and the MCP tools find parts later. Use the strongest model available, since the result depends on it.

**What the MCP connection can do.** Grouped in LottieFiles' docs: scenes and layers (size, frame rate, duration, background); shapes, paths and text, including splitting text for per-letter motion; fills, strokes, blend modes, shadows, blur, masks and mattes; keyframes, easing, motion paths; importing SVG, Lottie files and images, and turning a raster image into vectors; theme slots and saved presets; and segments, state machines and the events that drive them. Exporting is done with Creator's own controls, not through the MCP tools.

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

## Safety.

- **Everything in Creator is in LottieFiles' cloud.** Keep confidential names, logos, client artwork and private data out of Creator unless Sean says yes.
- **Never publish** an animation or use a hosted LottieFiles link; those are public. Export files instead.
- **AI credits.** Creator's AI features spend the plan's monthly credits. Check the balance before and after a session, and ask before a large batch.
- **Another session's bridge.** If another session holds the port, ask Sean before stopping it.
- **Adding the MCP server** for a new project changes Claude Code's configuration; ask Sean first.
