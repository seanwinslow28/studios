# Raphael Segerman's portfolio (2026)

## What it is

The personal site of Raphael Segerman, a creative developer in Cape Town who builds award-winning sites for design studios. It shows five projects and very little else.

It looks like a quiet white page. Then one small button in the corner swaps it for a blue planet in space, and the same five projects are floating in front of it in full colour. The site's own line says it: "more to discover beneath the surface."

Sean added it on November 17, 2026 as the model for his own site.

See it: https://segerman.dev/

**Best moment: press the small moon in the top right corner, then click Estrela Studio.** The white page gives way to the planet. The click passes through a full-screen view of the blue planet and lands on a purple horizon with the project's name across it. The code gives each project its own colour. Runner-up: **roll the mouse wheel on the plain white page.** The column of pictures never ends. It loops round to the first project again.

## How it turned out

- **Awwwards Honorable Mention, August 2, 2026.** Awwwards is the best-known web design award site, and this is its first rung, below Site of the Day. Fifteen members scored it, from 6.30 to 9.00 out of 10. The page shows no overall jury score.
- **What the judges' page singles out,** each with a short clip: the mode change, the endless scroll of projects, the page changes in each mode, a reveal under the cursor, and the planet's surface.
- **Estrela Studio's site, one of the five projects here, won Site of the Day** on January 9, 2026, and the Developer Award. Its page credits four accounts, and Raphael Segerman is one. The judges gave it 7.24 out of 10.
- **Yucca Packaging's site, another of the five, won the same two awards** on January 31, 2026, with 7.17. That page credits the design studio and Zulik, the studio he co-founded, not him by name.
- **His own count,** from his About page: two Awwwards Sites of the Day, two Developer Awards, and one FWA Site of the Day. The first four match the two sites above. His page for Zulik's own site says the FWA one is for that site. Nobody on this job could confirm it on FWA.
- **The caution:** an Honorable Mention is a modest prize. This site is on the shelf because Sean chose it, more than for its trophies.

## What makes it good, measured

I loaded the live site on November 17, 2026 in a private test browser, at a laptop size (1440 by 900) and a phone size (390 by 844). A short script read the type, colours and downloads off the finished page. I took stills of each state. I did not watch it move, and I never put the pointer on a picture.

- **One screen, not a long page.** On a laptop the page is exactly one screen tall, 900 pixels, and ordinary scrolling is switched off. The wheel moves only the middle column.
- **Three columns that never change places:**
  - Left: the name and one line about the work.
  - Middle: the five project pictures, which the wheel moves.
  - Right: the same five projects as a list of names.
- **An endless loop.** Five projects repeat for as long as you scroll. There is no bottom to reach.
- **Two layers, and this is the idea:**
  - Plain: a white page, navy type, and pictures reduced to navy and white with a fine speckled grain.
  - Revealed: a 3D planet behind everything, the same pictures in full colour and tilted in space, and white type with a soft glow.
  - One button moves between them. Its label in the code is "Toggle mode".
- **What opening a project does, in the revealed layer.** I opened one project, Estrela Studio. About a third of a second after the click the type is dimming and the pictures are starting to break up. By about one second the screen is all planet. Then the project page arrives: the name at 100 pixels, and a row of five short clips bent along a curve. The wheel now moves that row sideways.
- **The same page in the plain layer** is a flat row of clips on white, with a navy title and no planet. I did not capture how the plain layer changes pages.
- **The clips are short,** 3 to 10 seconds across the five projects. Estrela's run 7 to 10.
- **What the pointer does.** Rest on one name in the list and the other four fade. A small colour preview of that project appears under the list. The award page also names a reveal under the cursor on the pictures. My test missed it.
- **Type, two faces:**
  - Newake, a heavy all-capitals display face, for the big headline only. 87 pixels on the laptop with lines packed tight, at 0.8 of the type size. 62 pixels on the phone.
  - Aktiv Grotesk, a plain sans in one weight, for everything else. It is small: 12 to 14 pixels on a laptop 1,440 pixels wide, and about 17 on the About page. Every size grows and shrinks with the window.
- **Colour, two values on the plain home page:** navy-black, #00031F, and white, #FFFFFF, with small labels in a paler tint. The stylesheet puts a light grey, #EEEEEE, behind pictures. On the plain layer, colour shows up only in moving clips: the hover preview and a project's clips. The rest lives in the revealed layer.
- **No stylesheet motion at all.** Not one element uses a CSS transition, and the stylesheet declares no animations. Every movement is driven by script or drawn by the graphics chip.
- **A loading count.** It sits at 0% for about a second and a half, reaches 100% about four seconds after the page starts, and is gone by six and a half. The code makes the count last at least 2.4 seconds however fast the page loads.
- **A fallback, read in the code and not tested.** The code checks two things first: whether the visitor has asked their device for less motion, and whether the browser can draw 3D. If either fails, it removes the loading count and the 3D layer, and leaves a plain page. That page loses the button and the second layer. It also still plays every clip on a loop, which a visitor who asked for less motion may not want.
- **Weight:** 2.2 megabytes to show the home page, in 79 downloads. About 3.8 megabytes after pressing the button and opening one project. Lando Norris's site, also on this shelf, takes 5.5 megabytes before you scroll.
- **On a phone:** it turns into an ordinary scrolling page, 1,930 pixels tall. Each picture gets its project name underneath. The button and both layers are still there. It took 1.8 megabytes.
- **How it's built,** each part in a few words:
  - Astro: a tool that builds fast, mostly plain web pages.
  - Three.js: a library for drawing 3D in the browser.
  - GSAP with SplitText: an animation library, and its add-on for animating words and letters.
  - Lenis: a small library that makes scrolling glide.
  - Barba: a library that changes pages without a reload, which is what lets the planet stay on screen between pages.

### Why it's here

Sean chose it. My read on what it teaches: the reveal is the design. The first layer is restrained enough to pass for a plain page. Two colours, two typefaces, small text. That restraint is what makes the second layer land. The scroll does one job on each page, and the layout around it holds still.

It also shows a showpiece site does not have to be heavy. The cautions: its own prize is a modest one, its fallback for less motion is thin, and I saw stills, not motion.

## What Sean said about it

He added it himself on November 17, 2026 and called it "the main inspiration for my website update", the site "showing what good looks like."

In the same message: "I'm a sucker for scroll effects and reveals. Scrolling is a great way to tell the story."

## More details

- The site, its About page and its five project pages, read November 17, 2026: https://segerman.dev/ , https://segerman.dev/info , https://segerman.dev/work/estrela
- Awwwards page for this portfolio (Honorable Mention, August 2, 2026, 15 of 16 votes, the six highlighted clips): https://www.awwwards.com/sites/raphael-segerman-portfolio . My first two web searches missed this page. A helper who did not write the entry found it, and I then read it myself.
- Awwwards page for Estrela Studio's site (Site of the Day date, jury score 7.24, Developer Award 7.28, the four credited accounts): https://www.awwwards.com/sites/estrela
- Awwwards page for Yucca Packaging (Site of the Day January 31, 2026, 7.17, Developer Award 7.16, credits), read by the helper: https://www.awwwards.com/sites/yucca-packaging
- FWA: a search result pointed to an FWA page for this portfolio, but that address now says "not found", so nothing from it is used.
- Measurements: a private headless Chrome driven over its DevTools protocol by a short script, with the graphics chip on, so the 3D layer drew. Nine seconds of settling before reading the page.
- Every still of a project opening was taken after pressing the button, so those describe the revealed layer. They were taken about 0.3, 0.9 and 4.4 seconds after the click. The timings are rough.
- Only Estrela's page was opened in the browser. Clip lengths for the other four projects were read from the clip files by the helper. The site's data gives Estrela a purple planet, Yucca and PayJustNow green, Zulik blue and Vineyard teal.
- The loading count was read every quarter second on this Mac's connection. It will differ elsewhere.
- The 3.8 megabyte figure is a slight undercount: a few clips were still arriving when it was read.
- Typefaces, from the font files the page loads: Newake, by Indieground, and Aktiv Grotesk Medium, by Dalton Maag.
- Versions, from the site's own code: Astro 5.16.3, Three.js release 181, GSAP 3.13.0, SplitText 3.13.0, Barba 2.10.3, Lenis 1.3.17.
- The fallback is in the site's small start-up script. The stylesheet hides the mode button when it runs.
- The site is served through Cloudflare and loads Google Analytics.
- Not checked: the pointer over a picture, the page change in the plain layer, the fallback running for real, the keyboard, and a screen reader.
