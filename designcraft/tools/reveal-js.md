# Reveal: a deck built as a web page

Reveal is a free code library that turns a web page into a slide deck. Its full name, the one to search for, ends in ".js". Every slide is ordinary web code, so a slide can do anything a web page can: 3D, shaders, live code, video, scroll. It is Designcraft's first pick for a spectacle deck. Read this before building any deck meant to make a room sit up.

## Which of the three to reach for

- **Reveal** when the deck is a live performance: motion you see between clicks, live scenes, a brand turned on its head, a PDF and a scrolling version to leave behind.
- **The HyperFrames slideshow** when the same deck must also exist as a film, or when every move has to land on an exact frame. Its own guide says where it wins.
- **Claude Slides** when the job is a clear deck, made fast, that someone will open in PowerPoint or Keynote. It is not a spectacle.

## What it's best at

- **Motion you see live.** A click plays the move in front of the room. Matching elements glide from one slide to the next by themselves.
- **Anything the web can draw.** A Three.js scene, a GSAP timeline, a shader or a live demo sits on a slide like any other element. Bret Victor's talk is the model: when the thing itself can be on screen, run it rather than describe it.
- **Four ways out of one file.** Present it with a speaker window, export a PDF, open it as one scrolling page, or send the link.
- **Small and offline.** The library has no other code it depends on and weighs about six megabytes. Nothing needs the internet once it is in the project.

Where another tool wins: the two other deck tools, as above, and Motioncraft for a finished film.

## Setup

- **Cost:** free and open source.
- **Install:** added to each deck's own folder with npm, never system-wide. It needs Node 20.19 or newer; this Mac has Node 22.
- **Serve it locally.** A deck opened straight from the file loses features, the speaker window among them. Any small local web server will do.
- **The command that proves it works,** from an empty folder:

```bash
npm init -y && npm install reveal.js && ls node_modules/reveal.js/dist/reveal.mjs
```

It adds one package and prints the path to the library.

## Getting the best out of it

**Turn the brand on its head in the theme.** A theme is one stylesheet. The built-in ones expose their colours, typefaces and heading sizes as named values, so a custom theme starts by overriding about ten of them, then goes as far as the brief allows. Shopify's Renaissance edition is the model for where the line sits: keep the skeleton familiar (one point per slide, the order of chapters, the product's own type wherever the product appears) and change everything the eye lands on. The test deck turned the plain white theme into an olive-and-cream museum look by changing nine of those values.

**Auto-animate for continuity.** Mark two neighbouring slides as auto-animated and give the element that should travel the same id on both. The library works out the move: position, size, colour and spacing. In the test, a small number in the middle of one slide grew into a huge one on the next, under a headline that named it. That is planting and paying off in one gesture. Text, pictures and video match by themselves; anything else needs the shared id.

**Fragments for reveals, with care.** A fragment is a piece of a slide that waits for its own click. The fade and rise styles hide the piece until then. The highlight styles do not: in the test, the punchline marked "highlight on click" was on screen from the start, only changing colour on its click. For a reveal, the piece must start hidden.

**Backgrounds that fill the screen.** A slide can take a colour, a gradient, a picture, a looping video or a whole web page as its background. Two catches, both found in the test:

- A slide given both a background picture and a background video shows the picture and never loads the video. The fallback still goes in through the stylesheet instead, as a picture painted under the video. The library copies a slide's style names onto its background, so one rule can do it.
- A web page used as a background can be made clickable, but then nothing on the slide itself can be clicked.

**Embed live scenes properly.** Build each Three.js or shader scene once, when the deck loads, and run its drawing loop only while its slide is showing; the library announces every slide change. Tie GSAP moves to the fragment events, and write the step back too, or going back a click leaves the move half-done. A live scene needs a picture of itself for when 3D fails, and for print (below).

**Scroll view is the leave-behind.** Any deck can open as one long scrolling page instead of slides, by adding a word to the link or a setting to the deck. On a phone-width screen it switches on by itself. Fragments and auto-animate still work as the reader scrolls, and the page snaps to each slide. For Sean's love of scroll stories, this is the version to send after the talk. Its compact layout is still marked experimental.

**The speaker window.** Pressing S opens a second window with the speaker's notes, the next slide, a clock and a pacing timer. Notes are written inside each slide and never show to the room. Give the deck its total running time and the timer says whether each slide is running long. The window is a pop-up: a browser that blocks pop-ups blocks it, as the built-in browser pane did in the test.

**PDF export.** Open the deck with a print word in the link, in Chrome, and print to PDF: landscape, no margins, backgrounds on. Each fragment step prints as its own page, so five slides with one three-step reveal made eight pages. Notes can print on a page after each slide. Three things don't print, and each needs a stylesheet rule for print mode:

- A live scene prints as an empty box. Swap in its still picture.
- A move made by GSAP prints at its starting point. State the end look for print.
- A background video prints as whatever sits under it, which is one more reason to put a still there.

**Present offline, with a fallback for every clip.** Keep the library, fonts, videos and scenes inside the deck's folder: no links to other sites. Self-host every typeface. Before the talk, block the network and click through the whole deck once. Every video gets a still beneath it, every live scene a picture, every live demo a recorded version on the next slide.

**Carry the story across.** Every slide's headline states its point as a sentence, not a label, because the scroll view and the PDF will be read without the speaker. One idea per slide. The reveal happens in silence: click, then let the room look. Hans Rosling is the useful exception: he explained the chart's two axes slowly, asked one question, and only then let the bubbles run, talking over the motion. Spotify Wrapped 2024 is the warning: loud colour and one stat per card still disappointed when the substance was missing.

**An example of the difference.** The test deck's first draft used a highlight fragment for its last line. The line sat on screen from the start and only turned blue on its click, so the reveal gave nothing away. As a rising fragment it arrives on its click, with the GSAP bar growing beneath it, and the PDF shows the slide in four steps.

## Where it goes wrong

- **The deck works on the desk and dies in the room.** A link to a font or library on another site fails without internet. Test with the network blocked.
- **The punchline is visible early.** A highlight fragment shows from the start. Read every slide at its first step.
- **The fallback never appears, or the PDF has blank boxes.** A still set as the background picture wins over the video rather than backing it up, and live scenes and script-driven moves don't print without print rules. Read the PDF page by page.
- **A one-line print command gets it wrong.** Chrome's command-line print came out on portrait letter paper without the deck's print layout. A short script that waits for the print layout, then prints at the deck's own page size, worked.
- **Old-style figures in a big number.** The test's 3.5M set in Georgia had a "3" and "5" that dropped below the line beside a tall M, and the system's Georgia ignored the setting for lining figures. Pick a typeface that has them for any big stat.

## Safety

- **Nothing leaves the Mac by itself.** The test deck made no request to any other site while presenting.
- **Watch what a deck links to.** A font from Google's servers, a video from another site or a web page used as a background each tells that site about every viewing.
- **The hosted editor is a different product.** Reveal's site points to an online editor run by its makers. Using it means uploading the deck: ask Sean first.
- **Cost:** nothing. The library is MIT-licensed. GSAP and Three.js keep their own terms, set out in the spectacle guide.

## More details

- **Checked November 17, 2026:** reveal.js 6.0.2 from npm (MIT; released September 10, 2026; one package, about 6 MB unpacked, no dependencies). Its notes say building the library itself needs Node 22.12 or newer; using it needs Node 20.19 or newer.
- **The test deck:** Designcraft's jobs folder, outside the repo, under `tests/reveal-js/` (`index.html`, scripts `export-pdf.mjs`, `speaker-view.mjs`, `scroll-view.mjs`, `shots.mjs`; pictures and PDFs in `out/`). Five slides: a full-bleed looping video (made locally with ffmpeg) with a still painted underneath; an auto-animated pair; a slide with three fragments and a GSAP 3.15.1 bar; a Three.js 0.187.0 scene on its own slide, run only while current.
- **What the test showed:** it rendered in the browser pane and in Chrome through Playwright 1.65.1 (Designcraft's accessibility tools folder). Auto-animate matched the number and fired its event. Fragments counted 0, 2, 3. Pulling the video's source left the still showing. The speaker view opened on S with notes, the next slide and a pacing timer, with no outside request. Scroll view turned on by link at desk size and by itself at 390 pixels wide, and snapped to whole slides. The scripted PDF export gave 8 landscape pages at 749 by 546 points; with notes on separate pages, 14. Chrome's own command-line print gave 5 portrait letter pages without the print layout.
- **Found in the library's code:** a background picture is checked before a background video, so the video is skipped (`js/controllers/slidecontent.js`); a slide's classes are copied onto its background element (`js/controllers/backgrounds.js`).
- **Not tested:** decktape, the makers' other route to PDF; the multiplex plugin; the React wrapper; lightbox; presenting on a projector.
- **Sources, read November 17, 2026:** https://revealjs.com/ and its pages on installation, backgrounds, auto-animate, speaker view, scroll view, PDF export and themes; release notes at https://github.com/hakimel/reveal.js/releases; the npm registry.
