# Spectacle on the web: 3D, scroll motion and smooth scrolling

Three free code libraries are how Designcraft builds pages that move with the reader: one draws 3D, one ties motion to scroll and pointer, and one makes scrolling glide. The lead writes all three as code. Read this before building any scroll story, reveal or 3D moment. Sean: "I'm a sucker for scroll effects and reveals. Scrolling is a great way to tell the story."

## What each is best at

- **Three.js: 3D and shaders in the page.** It draws with the graphics chip through WebGL, the browser's way of using it. A shader is a small program that paints colour and light there. Lando Norris's 3D head, Igloo Inc's whole world, Bruno Simon's island and Raphael Segerman's planet are all Three.js.
- **GSAP with ScrollTrigger: motion tied to the reader's hand.** ScrollTrigger runs an animation by how far the reader has scrolled, so it plays forwards and backwards with them. It pins a section in place while its story plays, and with GSAP's `matchMedia` sets up different motion for phones and for people who ask for less. Lando's, Igloo's and Segerman's sites all use GSAP.
- **Lenis: the glide.** It smooths the browser's own scrolling, so a pinned scene or a camera move doesn't stutter under a mouse wheel. Lando's, Scout Motors' and Segerman's sites use it.

Where something else wins:

- **A scrubbed film with no 3D.** Scout Motors swaps still frames on a canvas as you scroll: no Three.js, but 51.7 megabytes after a full scroll.
- **Spectacle the reader moves.** Ciechanowski's watch article is 93 hand-built models the reader turns. One thing the reader moves can beat any amount they only watch.
- **A scene shaped by hand:** Unicorn Studio or Spline, both paid for commercial work. Small vector animations: Rive or Lottie, on Motioncraft's list.

## Where the line with Motioncraft sits

Designcraft takes anything that answers the reader live, written as code in the page: scroll, pointer, tap. Motioncraft takes anything that plays the same every time: a finished film, a rendered loop, a logo sting, and the 3D models themselves, built in Blender. Designcraft places Motioncraft's model or clip in the page and decides how scroll drives it.

Models come over as glTF, the web's 3D file format, saved as a single `.glb` file. Blender exports it by itself. In the test, a small model came out at 71 kilobytes, or 15 with Draco compression. Draco needs a decoder in the page that weighs about 75 kilobytes once compressed for sending, so it only pays off for models bigger than that.

## Setup

- **Nothing to sign up for.** The three are free packages added to the job's project.
- **The proof is not that it moves. It is that it runs clean four ways:** full motion, reduced motion, a phone, and a browser that can't draw 3D. A short check script loads the page each way, scrolls it with the wheel as a person would, and reports the console. In the test all four came back clean.

## Getting the best out of it

**Run one clock.** Lenis and ScrollTrigger must agree on where the page is, every frame. Drive Lenis from GSAP's clock, and tell ScrollTrigger each time Lenis moves:

```js
const lenis = new Lenis();
lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add((t) => lenis.raf(t * 1000));
gsap.ticker.lagSmoothing(0);
```

**Scrub the story, play the small things.** Scrubbing ties an animation's progress to the scroll position: stop, and it stops; scroll back, and it runs backwards. That is what makes scroll a way of telling a story, because the reader's hand sets the pace. A short catch-up, around half a second, gives the motion weight without lag. Small arrivals, like a card fading in, play once on entry.

**One timeline per scene.** Put a scene's steps on one timeline with one ScrollTrigger, not a trigger on every step. GSAP's guide warns against nesting them. Create triggers in the order they sit on the page.

**Sticky beats pinning when it will do.** The test's reveal used a tall section with a sticky stage inside, scrubbed across the section's height: no pin, no added spacing, less for GSAP to re-measure.

**Animate movement, fade and clipping, never layout.** Position, scale, rotation, opacity and clip-path stay smooth. Width, height and margins make the browser redo the whole layout every frame.

**Write both ends of a reveal.** The test caught this one. A panel revealed by clipping, animated "from" a clipped start, ran towards the browser's own value for the end, which was "no clipping". Halfway through the reveal its rounded corners collapsed from 16 pixels to almost square. Animating from a stated start to a stated end fixed it.

**Load 3D only when the browser can draw it, and only the parts you use.** Check for WebGL first. Import the few pieces of Three.js the scene needs, not the whole library. In the test that cut Three.js from 188 kilobytes to 131, compressed for sending.

**Show a poster until the first frame.** The first screenshot of the test page was an empty hero: the 3D code was still arriving. A still picture under the canvas, faded out once the scene draws, closes that gap. The same picture is the fallback when 3D fails.

**Spend the graphics chip only on what is seen.** Cap the sharpness at twice the screen's pixels, and one and a half on phones; beyond that the cost climbs and nobody sees the difference. Stop drawing when the scene scrolls out of view. Keep shaders cheap: fixed loop counts, few branches, lower precision on phones where the effect allows.

**Mind text over 3D.** In the test, the white headline sat on top of a bright lime shape. The checker can't measure text over a canvas. Put the words where the object isn't, or look at it on purpose.

## Performance budgets

The shelf gives the range, all measured before the first scroll:

- Segerman's portfolio: 2.2 megabytes.
- Lando Norris: 5.5.
- Igloo Inc: 14.6.
- Scout Motors: 17.7, and 51.7 after a full scroll.

A sensible default for Designcraft, offered here as a starting point, not as Sean's rule: stay under Lando's 5.5 megabytes for the first view, and spend the weight on the one moment that carries the story. The libraries are the small part. In the test, GSAP with ScrollTrigger and Lenis came to 52 kilobytes compressed for sending, and the needed parts of Three.js to 131. Models, textures, pictures and video are where pages get heavy. For smoothness, 60 frames a second leaves about 16 milliseconds to draw each one. On a phone, judge it on a phone.

## Reduced motion

Some people set their device to ask for less motion, because movement makes them dizzy or sick. Plan two versions of every scene, not one version with the motion switched off.

- **Full:** scrubbed reveals, a camera that pulls back, a shape that breathes.
- **Calm:** nothing travels. Each block fades in once as it arrives, so the order of the story is still told. The 3D scene holds still.

GSAP's `matchMedia` builds each version and swaps between them if the setting changes, tidying up after itself. Lenis turns its own smoothing off for these visitors by default. In the test, full motion set up two scrubbed triggers; calm motion set up four play-once fades and none scrubbed. Both ended in the same place. Don't erase meaning along with movement: a change of state still needs to show. Segerman's site is the caution: by its code, its calm version drops the 3D but still loops every clip.

## Phones

- **A finger can't scroll and steer at once.** Lando's site gives the 3D head a "tap to lock" button, so a finger either scrolls the page or plays with the head.
- **Leave touch scrolling native.** Lenis leaves touch to the phone unless told otherwise; its notes say the touch option can be unstable on older iPhones, and that Safari caps Lenis at 60 frames a second, or 30 in low power mode.
- **Design the phone scene, don't shrink the desk one.** Lighter detail, often less 3D and more page.

## Falling back when 3D fails

Some browsers and machines can't draw 3D, or lose the ability mid-visit. The page must still be a page. In the test, with 3D blocked, the poster showed, every scroll reveal still ran, and the console stayed clean. Bruno Simon's site goes one step further: it uses the newest way to draw, WebGPU, where it can, and falls back to WebGL. Igloo Inc is the warning at the far end. Every word is drawn inside the 3D picture, so a screen reader has nothing to read, and its accessibility mark is low. Keep real text in the page.

## Where it goes wrong

- **Two clocks.** Lenis and ScrollTrigger out of step make pinned scenes judder.
- **An animation towards the browser's own end value.** The tell is a reveal that looks wrong only halfway through.
- **Triggers measured before the page settled.** Fonts or pictures arriving late move everything below them. ScrollTrigger re-measures on resize, not on every change; refresh it once the page has settled.
- **Old Three.js habits.** The test's timing helper printed a warning: a newer one has taken its place. Read the console after every upgrade.
- **A weight that only shows on a phone.** Lando's phone download is bigger than its desk download. Measure both.

## Safety

- **GSAP's licence.** GSAP is free, including every plugin that used to be paid, and free for commercial work. It is not open: Webflow owns it, and can change the terms for later versions; older versions stay usable on the old terms. Its one bar that matters is building a visual, no-code animation tool that competes with Webflow's own. Using it on sites and apps is allowed, and GSAP code written by an AI is expressly fine.
- **Three.js and Lenis** are open, under the MIT licence.
- **Nothing is uploaded.** Bundle the libraries into the page rather than loading them from a public code server, which would see each visit.
- **Ask Sean first** before going past the weight budget, before sound that plays by itself, and before any paid tool such as Unicorn Studio or Spline.

## More details

- **Tested November 17, 2026,** in a scratch project at `designcraft-jobs/tests/type-colour-spectacle/` (outside every repo), built with Vite 8.3.8: `three` 0.187.0 (MIT), `gsap` 3.15.1 (package licence field: "Standard 'no charge' license"), `lenis` 1.3.27 (MIT).
  - The page (`spectacle.html`, `src/spectacle.js`): a scroll-scrubbed Three.js shape with a small custom shader, a sticky reveal of three lines and a clipped panel, Lenis on GSAP's ticker, `gsap.matchMedia` with full and calm branches, `WebGL.isWebGL2Available()` before the dynamic import, pixel ratio capped at 2 (1.5 under 700 px), drawing paused off screen by an `IntersectionObserver`.
  - Viewed in the browser pane at 1280 by 820: the scene drew, no errors. The first screenshot came before the dynamic import finished, which is what led to the poster.
  - `scripts/spectacle-check.mjs`, Playwright 1.65.1 driving the Mac's Chrome: full motion, `reducedMotion: 'reduce'`, iPhone 14, and WebGL blocked by overriding `getContext`. Each scrolled with 16 wheel steps of 120 px. All four consoles clean, after an empty favicon removed a 404. Full: 2 triggers, both scrubbed. Calm: 4 triggers, none scrubbed, `lenis.prefersReducedMotion` true. No WebGL: poster shown, reveals ran.
  - The clip-path fault: `.from()` ended at `inset(0px 0px 0.6523% round 0.1044px)`; `.fromTo()` with an explicit end kept `round 16px`.
  - Bundle, gzip: GSAP, ScrollTrigger, Lenis and page code 51.7 KB; all of Three.js 187.7 KB; named parts only 130.9 KB.
  - `THREE.Clock` logged a deprecation warning pointing to `THREE.Timer`.
  - Blender 5.2.2 LTS, headless with `--factory-startup --disable-autoexec`: a subdivided test model exported as GLB at 71,392 bytes, 15,252 with Draco. Three.js's Draco decoder (`draco_decoder.wasm` plus `draco_wasm_wrapper.js`) gzips to about 75 KB.
- **Shelf figures** come from the entries for Lando Norris, Igloo Inc, Bruno Simon, Scout Motors, Raphael Segerman and the Mechanical Watch in `designcraft/research/`.
- **Sources, read November 17, 2026:** GSAP's standard licence (https://gsap.com/standard-license/); ScrollTrigger's documents (https://gsap.com/docs/v3/Plugins/ScrollTrigger/); `gsap.matchMedia()` (https://gsap.com/docs/v3/GSAP/gsap.matchMedia()); Lenis's README (https://github.com/darkroomengineering/lenis) and the installed copy, which list `respectReducedMotion` (default true), `syncTouch` (default false) and the Safari frame caps. Shader habits are salvaged from the shader skill, and pixel-ratio and reduced-motion habits from the Three.js skill's optimisation notes and the Impeccable skill, in this studio's words. The GSAP and Three.js skills on the Mac use some older calls, such as `ScrollTrigger.matchMedia` in place of `gsap.matchMedia`.
- **Not measured:** real frame rates. The test browser ran without a screen, so its timings say nothing about a real phone.
