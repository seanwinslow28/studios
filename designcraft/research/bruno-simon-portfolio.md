# Bruno Simon's portfolio, the drive-around one (2025)

## What it is

The personal site of Bruno Simon, a developer who builds 3D for the web. It has no pages. It is a small island, and you drive a red toy car around it. His projects, his links and a few games are places on the map.

This is the second version. The first, from 2019, also had a car, and he says it went viral. He rebuilt it from scratch over a little more than a year, aiming to finish by the end of 2025. Awwwards, the best-known web design award site, made it Site of the Day on January 21, 2026. The code that runs in the browser is public and free to reuse.

It is here as the weird one that still works. The whole menu is a toy, and you can still find everything.

See it: https://bruno-simon.com/

**Best moment: click to start, hold the up arrow, and drive straight into the nearest object.** Things get knocked about. The menu even has a button to reset every object. Then look up: the hour, the season and the weather run in real time and are shared, so every visitor sees the same evening. When I loaded it, it was night, with a purple sky and the lanterns lit. Runner-up: open the menu in the top right corner. It holds plain lists of links, for anyone who does not want to drive.

## How it turned out

- **Site of the Day,** Awwwards, January 21, 2026. Eighteen judges gave it 8.11 out of 10. Design 8.05, usability 7.83, creativity 8.62, content 8.18.
- **Awwwards members gave it 9.67,** the highest public score of any site in this batch.
- **Site of the Month,** January 2026.
- **Developer Award,** 7.65 out of 10. This one is judged by engineers. Animation 8.60, speed 8.20, phone layout 8.20, accessibility 6.60.
- **The code has a following.** The public copy on GitHub, the site where developers share code, had 2,030 stars and 349 copies made on November 16, 2026. Stars work like bookmarks. The 2019 version has 4,745.
- **Not found:** I looked for an FWA award, a CSS Design Award and a Webby and could not confirm any. His write-up gives no visitor count.

## What makes it good, measured

I loaded the live site on November 16, 2026 in a private test browser at a laptop size and a phone size. A short script read the page and added up what it downloaded. I got past the start screen once and took a screenshot. The world's details come from his own case study on Awwwards.

- **One screen, no scrolling.** The page is exactly as tall as the window. One picture fills it, drawn fresh every frame like a video game.
- **Three ways to steer,** all named in the menu: mouse and keyboard, touch on a phone or tablet, and a game controller.
- **The escape hatches.** The menu offers "unstuck", a jump back to the nearest safe spot, a reset for every object, a sound switch and a quality switch. My read: these are what make a toy usable. You can never get lost for long.
- **Ordinary lists behind the toy.** The menu has headed sections for a Three.js course, his build diaries, the source code, the music and more links.
- **Type in the menus:** Amatic SC, a tall hand-drawn face, for headings at 40 to 50 pixels. Nunito, a round sans, for text at 20 pixels. On a phone, 32 and 16.
- **Small motion in the menus:** mostly two speeds, 0.15 and 0.3 seconds, with a few slower ones.
- **The world,** per his case study:
  - About 78,400 blades of grass, each a single triangle.
  - Three kinds of tree: birch, oak and cherry.
  - Wind moves the grass and leaves. Rain turns to snow when it is cold, and the water freezes.
  - A racetrack with a daily top ten, a cookie stand, bowling pins, a campfire.
  - Achievements that unlock new paint for the car. The menu shows unlocks at 8, 15, 23, 30 and 38.
- **Shared, lightly.** Visitors can leave up to 30 short "whispers" on the map, each with a country flag. A cookie counter is shared by everyone. It is not a fully shared world. He says shared physics would need heavy server work.
- **Colour:** no fixed palette. The light changes with the hour and the season. I saw it in purple night.
- **How it's built,** each part in a few words:
  - Three.js: a library for drawing 3D in the browser.
  - WebGPU: the newest way for a browser to use the graphics chip. The site uses it where it can and falls back to the older way, WebGL, where it cannot. It fell back in my test.
  - Rapier: a physics engine. It decides how the car bounces and how things fall.
  - Blender: the 3D program the island was modelled in.
- **Weight:** 7.2 megabytes in 116 downloads to reach the start screen. The physics engine alone is 1.5. The code is 1.1. The island's model is 0.6. The phone gets the same.
- **On a phone:** the same world with touch controls. By his account it switches to a lighter setting on its own, with no blur on the water, no soft focus and simpler shadows.

### Why it's here

It answers "get weird with it" and stays usable. My read: the lesson for Designcraft is that the strange part needs a plain part beside it. The toy is the front door. The menu, the reset buttons and the three ways to steer are what keep people from leaving. The caution: this is a little over a year of one person's work, plus a composer he hired for the music, and it sells nothing but its maker.

## What Sean said about it

Seen on November 17, 2026, with the rest of the shelf. He said nothing about this one by itself.

Of the whole shelf: "all of the options you provided are amazing in their own way and I wouldn't want to throw those out the window." He picked no favourite. It stays on the shelf as one end of the range.

## More details

- Awwwards site page (Site of the Day date, jury and member scores, Developer Award marks): https://www.awwwards.com/sites/brunos-portfolio
- Awwwards Sites of the Month list (January 2026): https://www.awwwards.com/websites/sites_of_the_month/
- His case study on Awwwards, March 11, 2026 (the 2019 version, the year of work, the grass count, weather, whispers, racetrack, phone settings, why no shared cars): https://www.awwwards.com/brunos-portfolio-case-study.html
- Source code for this version (stars and copies read on November 16, 2026; MIT licence): https://github.com/brunosimon/folio-2025
- Source code for the 2019 version: https://github.com/brunosimon/folio-2019
- My measurements: a private headless Chromium driven by a short script, at 1440 by 900 and 390 by 844, 20 seconds of settling. Menu wording, typefaces and timings were read from the page. The Three.js release it reports is 187. The site itself logged that WebGPU was not available and that it was using WebGL 2.
- Rapier is not named in his case study. The site's own menu names it as the physics library, and its file is about 1.5 megabytes.
- The Awwwards page-structure, scroll-map and motion tools would not run; they need a browser add-on, Playwright, that is not installed.
- The Awwwards search tool also lists the 2019 version with a Site of the Year tag. I did not confirm which year, so I left it out.
