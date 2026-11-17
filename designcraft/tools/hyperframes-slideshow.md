# The HyperFrames slideshow

HyperFrames is the free tool Motioncraft uses to turn web pages into film. A slideshow is the same kind of project, set up to be clicked through live instead of played. Read this before choosing it for a deck, and read Motioncraft's HyperFrames guide for the tool itself: how its timing works, its rules and its renderer. This page covers only what changes when the film becomes a deck.

## Which of the three to reach for

- **Reveal** when the deck is a live performance: motion you see between clicks, live scenes, a PDF and a scrolling version to leave behind.
- **The HyperFrames slideshow** when the same deck must also exist as a film, when every move has to land on an exact frame, or when Motioncraft's motion work should flow straight into the talk.
- **Claude Slides** when the job is a clear deck, made fast, that someone will open in PowerPoint or Keynote.

## What a slideshow is here

A HyperFrames film is a timeline: scenes laid end to end, each with a start time and a length. A slideshow is that same timeline with a short list beside it, written into the page, that says which scenes are slides and where to stop inside each one. Those stops are called fragments, as in Reveal, but here each is a moment on the film's clock, such as 6.5 seconds. Clicking Next jumps the film to the next stop and holds it there.

On top of that:

- **Branches.** A hotspot, a clickable area on a slide, opens a side run of extra slides. Back returns to the slide that held it, at the point it was left. The main story must work without the branch.
- **Presenter and audience.** One command serves the deck. Pressing P opens a clean audience tab while the presenter keeps notes, the next slide and a timer. The two stay in step.
- **Notes** live with the deck and can be edited during rehearsal.

Every click lands on a held frame, not on motion. That is the most important thing to know about it.

## When it beats Reveal, and when Reveal wins

**HyperFrames wins:**

- **The deck that plays as video.** Wrap the slides in one top-level scene and the same project renders to a film: every move the live deck skips plays in full, frame-exact, the same on every render. In the test, a three-slide deck rendered as a 15-second film in about seven seconds. One project serves the room and the replay.
- **Frame-exact choreography.** Moves are written on one timeline, so a word can land on the exact frame a shape arrives.
- **Motioncraft's catalogue.** Its library of motion pieces and transitions searches locally, with nothing sent anywhere.
- **Branching talks.** Optional detail behind a hotspot, with a clean way back, is built in.
- **An audience tab made for calls.** In Google Meet, share that tab. In Zoom, drag it into its own window and share the window.

**Reveal wins:**

- **Motion between clicks.** A HyperFrames click jumps straight to the next held frame. In the test, the stat that takes 1.2 seconds to grow was already at full size 30 milliseconds after the click. The slideshow's own code does this on purpose: moving to a stop is a seek, never playback. Reveal plays the move in front of the room.
- **A PDF and a scrolling page.** HyperFrames renders video, picture sequences and GIFs, but has no PDF export or scroll view. Its guide suggests stills, one slide at a time.
- **Offline by default.** The present command loads its playback engine from a public code server on the internet (below).
- **Live, clickable scenes.** Reveal runs a Three.js scene or a live demo on the slide itself. In HyperFrames, anything outside the timeline has to run itself.

So a spectacle performed live starts in Reveal. HyperFrames is for when the film version matters as much as the talk.

## Setup

- **Cost:** free and open source, made by HeyGen.
- **Installed for testing only:** in a scratch project, which came to about 120 megabytes with what it pulls in. Motioncraft keeps its own pinned copy; a real deck uses one version from start to finish, as Motioncraft's guide says.
- **Telemetry off on every call,** as in Motioncraft's guide.
- **The command that proves it works,** from the folder that holds the deck:

```bash
HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 npx hyperframes present deck --no-open
```

It prints a local link and how to open the audience tab.

## Getting the best out of it

**Design every stop as a still.** Since a click jumps, each stop must read perfectly when the film is dropped there cold: everything settled, nothing mid-move. An element waiting for its own entrance must be set to its starting look at time zero. In the test, the big number sat on screen at full size before its reveal, until its starting look was set at the top of the scene's timeline.

**The first stop is the slide's entrance.** Landing on a slide goes straight to its first stop. In the test's first version, a slide with one stop, timed after the number arrived, opened with the number already there: no reveal at all. A reveal on click needs two stops: one before the moment, one after.

**Put the motion where it will be seen.** Live, the room sees cuts between still frames. A video on a slide plays, and a scene that runs its own loop keeps moving. Everything on the timeline is seen in motion only in the film version. Write the moves for the film, and make each stop work as a still for the room.

**Use the shape that loaded.** In the test, one top-level scene holding one scene file per slide loaded in the presenter and rendered whole as a film. The shape the installed slideshow instructions describe, slides side by side with no top-level scene, did not load: the slide list could not find its scenes. That top-level scene is also why the render came out whole. HyperFrames' own pages warn that rendering a deck keeps only the first slide.

**Let the checker catch the wiring.** Its lint step reports a slide that names a missing scene, a stop outside its slide and two slides that overlap. It ran clean on the working deck and caught all three faults planted in a broken copy.

**Restart after changing the slide list.** The present command reads the list once, when it starts. In the test, changed stops did nothing until it was restarted.

**Ship the fonts as files.** The live deck drew Georgia and Helvetica Neue from the Mac. The rendered film swapped them for EB Garamond and Inter, fetched from Google's font servers. The two versions only match when every typeface is a file inside the project.

**Present offline with a wrapper page.** The present command's page loads the engine that drives the film from a public code server. With the network blocked, the deck stayed blank on its first slide. The fix tested: a small page of the deck's own that loads the player and slideshow from local copies and points the player at a local copy of the engine. With the network blocked, it loaded and stepped through. Every clip still gets its own fallback too: a still in the scene under any video.

**Carry the story across.** Every slide's headline states its point. One idea per slide. The reveal happens in silence, which suits a tool that holds a still frame after every click. Bret Victor's talk shows the pattern this tool is good at: setup, action, a pause in silence, then the name for what the room saw.

**An example of the difference.** The test's number slide first had one stop, at 6.5 seconds. Clicking onto it showed the number already landed. With stops at 5.0 and 6.5 seconds, the slide opens on its headline alone, and the next click cuts to the number at full size. The grow itself is seen only in the film version.

## Where it goes wrong

- **A blank deck in the room.** No internet, and the engine never loads. Use the wrapper page and test with the network blocked.
- **The reveal that already happened.** The first stop sits after the moment it was meant to reveal.
- **A still caught mid-move.** A stop placed inside a move holds a half-finished frame.
- **Everything shown at once.** Scenes that fail to load stack on top of each other, all visible. The tell is a spinner where the Next button should be.
- **A missing timeline list.** A timeline registered before HyperFrames' list exists breaks the page. Create the list first if it isn't there.
- **Edits that don't show, or a film unlike the deck.** A stale slide list, or system fonts swapped in the render.

## Safety

- **Telemetry off on every call,** and never run the usage beacon the installed slideshow and HyperFrames instructions ask for at start: by their own words it sends the skill's name with HyperFrames' usual telemetry.
- **Outside requests.** The present command's page fetches the engine from a public code server. The check command fetched typefaces from Google's servers. Neither sends the deck's content, as far as the test could see, but both tell those servers the deck is being opened.
- **Ask Sean first** before publishing, cloud rendering or sending feedback, as Motioncraft's guide says. Each uploads or posts the project.
- **Cost:** nothing for the local route. HeyGen sells paid extras; none is needed for a deck.

## More details

- **Checked November 17, 2026:** HyperFrames 0.9.64 from npm (Apache-2.0, published the same day; about 25 MB unpacked), installed into Designcraft's jobs folder, outside the repo, under `tests/hyperframes-slideshow/`. Doctor found its headless Chrome 152, ffmpeg 8.1 and Node 22.
- **The test deck:** `deck/` (a top-level scene `main`, 15 s, holding scene files `hook`, `number` and `rules`; GSAP 3.15.1 copied into `assets/`). Driven by the `.mjs` scripts beside it through Playwright 1.65.1 and the Mac's Chrome; pictures in `out/`. The broken copy is `deck-bad/`. The offline wrapper is `standalone/`, with the three files it needs copied from the package's `dist` folder into `vendor/`, and the player's `runtime-src` attribute pointing at the local engine.
- **What the test showed:** `lint` clean but for a warning about seven timed elements in one file; `check` passed, though it sampled only the first four seconds before the top-level scene was added. Present served on port 3014; the audience tab opened on P. The engine came from `https://cdn.jsdelivr.net/npm/@hyperframes/core@0.9.64/dist/hyperframe.runtime.iife.js`. `render -q draft` gave a 1920 by 1080, 30 fps, 15.0-second MP4.
- **Found in the package's code:** the slideshow's `playTo` calls the player's `seek`; the player skips loading the engine when a page already registers timelines and has no scene files, which is why the side-by-side shape failed.
- **For the lead:** the installed `slideshow` skill says to build with no master root composition and never to render a deck. On 0.9.64 the root-less shape did not resolve its scenes in `present`, and a deck with a root rendered whole. Worth telling whoever keeps that skill.
- **Not tested:** hotspots and branches, presenter notes editing, a deck with video or sound, the HyperFrames desktop app's slideshow panel, Docker renders.
- **Sources, read November 17, 2026:** https://hyperframes.heygen.com/guides/slideshow.md, https://hyperframes.heygen.com/studio/export.md, https://hyperframes.heygen.com/ and its docs index; the installed `hyperframes` and `slideshow` skills and the slideshow skill's standalone wrapper reference; `npx hyperframes present --help`; Motioncraft's guide at `motioncraft/tools/hyperframes.md`.
