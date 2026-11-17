# Igloo Inc's landing page, by abeto and Bureaux (2024)

## What it is

A one-page site for Igloo Inc, the parent company of Pudgy Penguins, a brand of collectible penguin characters. The whole page is a live 3D scene, drawn fresh every frame like a video game. You start outside an igloo in snowy mountains. Scrolling moves the camera on to the company's projects, shown as blocks of ice, then to a cloud of particles that forms a shape for each link.

It was built by abeto, a small team of technical artists, with Bureaux, who supplied the mood, the 3D pieces and the sound. Awwwards, the best-known web design award site, made it Site of the Day on July 23, 2024.

It is here as the far end of the scale. Even the labels and menus are drawn inside the 3D picture.

See it: https://www.igloo.inc/

**Best moment: the first scroll, from the igloo into the ice blocks.** Scroll slowly and watch the handover between the two scenes. The makers say it mixes three effects: colours splitting at the edges, a digital smear, and frost. One caveat: my test browser held the opening scene but I did not scroll it, so the handover is their account, not my viewing. Runner-up, also by the makers' account: the last section, where the particles re-form each time you pick a link.

## How it turned out

- **Site of the Year 2024,** Awwwards Annual Awards. The top prize of the year.
- **Developer Site of the Year 2024** as well. This one is judged on how well a site is engineered.
- **Site of the Day,** July 23, 2024, at 7.92 out of 10. Design 8.05, usability 7.50, creativity 8.31, content 7.91. Awwwards members gave it 8.55.
- **Site of the Month.** It sits in Awwwards' monthly list at July 2024, by its place in the order.
- **Developer Award,** 7.66 out of 10. Animation scored 9.60, the highest single mark I saw on any site in this batch. Accessibility scored 6.60 and page markup 6.40.
- **Webby Winner, 2026,** for Best Visual Design, Aesthetic, among websites. It was also a nominee for Technical Achievement. The Webbys are the long-running internet awards. Bureaux entered it.
- **Not found:** I looked for an FWA award and a CSS Design Award and could not confirm either. I found no visitor numbers.

## What makes it good, measured

I loaded the live page on November 16, 2026 in a private test browser at a laptop size and a phone size. A short script read what the page is made of and added up everything it downloaded. How it was made comes from the makers' own case study on Awwwards.

- **One screen, no page to scroll.** The page is exactly as tall as the window. The scroll wheel drives the camera, not the page.
- **Three scenes,** per the case study: the igloo, the ice blocks, the links. Before them, a short opening animation.
- **No ordinary text at all.** In my test the page held four building blocks and no words. Every letter is drawn inside the 3D picture. My read: this is why the accessibility mark is low. You cannot select the text, and a screen reader, the tool blind visitors use, has nothing to read.
- **Why the text is 3D:** for the effects. The makers wanted letters that glitch and scramble. Doing that inside the 3D picture avoids the slow work a browser does when ordinary text changes.
- **Type:** the words are part of the picture, so the page sets no type in the usual way. The page loads IBM Plex Mono, a typewriter-style face. In my screenshot the labels are small, white and blocky, like a readout on a machine. They sit in the four corners and leave the middle to the igloo.
- **Colour:** close to one colour. The page background is a cool grey, #A0A5B1. Awwwards lists the palette as #B6BAC5 and #383E4E. The ice, the snow and the sky are all in that grey-blue range, and the labels are white.
- **Each project gets its own ice block.** The makers wrote a small tool that grows ice crystals by rule, so no two blocks look alike.
- **Sound is part of the design.** Music and effects are timed to the particles as they move.
- **How it's built,** each part in a few words:
  - Three.js: a library for drawing 3D in the browser. It uses WebGL, the browser's way of drawing with the graphics chip.
  - Shaders: small programs that run on the graphics chip. Here they make the glitches, the frost and the scene changes.
  - GSAP: an animation library, for timing.
  - Svelte and Vite: tools for structuring and packaging the code.
  - Houdini and Blender: 3D programs, used to make the models.
- **Weight:** 14.6 megabytes in 94 downloads before you touch anything. 14.2 of that is 3D data: textures, models and sound. The code is 0.4. The phone gets the same 14.6.
- **On a phone:** the same scene loads at phone size. The makers say they measured speed throughout and tuned for weak devices. I did not measure how smoothly it runs.

### Why it's here

It is the purest spectacle on the shelf, and the judges called it the best site of its year. My read: the lesson for Designcraft is commitment. One world, one colour range, one way to move through it, and nothing that breaks the spell. The caution is the price. It is nearly 15 megabytes, it has no real text, and its lowest marks are for the things an ordinary site gets for free.

## What Sean said about it

Seen on November 17, 2026, with the rest of the shelf. He said nothing about this one by itself.

Of the whole shelf: "all of the options you provided are amazing in their own way and I wouldn't want to throw those out the window." He picked no favourite. It stays on the shelf as one end of the range.

## More details

- Awwwards hall of fame, 2024 (Site of the Year and Developer Site of the Year): https://www.awwwards.com/annual-awards/hall-of-fame/2024
- Awwwards site page (Site of the Day date, jury scores, Developer Award marks, makers, palette): https://www.awwwards.com/sites/igloo-inc
- Awwwards Sites of the Month list (July 2024 slot): https://www.awwwards.com/websites/sites_of_the_month/
- Makers' case study, October 31, 2024 (who did what, that Bureaux proposed the project, the three scenes, the scene-change effects, why the text is 3D, the ice tool, the sound, the tools used): https://www.awwwards.com/igloo-inc-case-study.html
- Webby category page, 2026 (Webby Winner, Best Visual Design, Aesthetic): https://winners.webbyawards.com/winners/websites-and-mobile-sites/features-design/best-visual-design-aesthetic
- Webby entry page (winner and nominee lines, Bureaux as entrant): https://winners.webbyawards.com/2026/websites-and-mobile-sites/features-design/best-visual-design-aesthetic/361001/igloo-inc
- My measurements: a private headless Chromium driven by a short script, at 1440 by 900 and 390 by 844, with 20 seconds of settling. The Three.js release it reports is 165.
- The Awwwards page-structure, scroll-map and motion tools would not run; they need a browser add-on, Playwright, that is not installed. They would have had little to read here anyway, since the page has no ordinary sections.
- A 2026 Webby for a 2024 site surprised me. Both Webby pages agree, so I kept it.
