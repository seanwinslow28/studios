# Lando Norris's site, by Off+Brand (2025)

## What it is

The personal website of Lando Norris, the McLaren Formula 1 driver. It does ordinary jobs: who he is, his results, his race calendar, his helmets, his shop. It does them with a 3D head at the top of the page, a wall of helmets, and one loud lime green.

It was made by Off+Brand, a studio in the United Kingdom. One source places it in Glasgow and its award profile says London. Awwwards, the best-known web design award site, picked it as Site of the Day on November 17, 2025. I found no launch date.

It is here because it won the biggest prize in this field twice over, from the judges and from the public, while still being a normal site you can find things on.

See it: https://landonorris.com/

**Best moment: the top of the home page. Move the mouse slowly across the 3D head before you scroll.** The page's code shows the head responds to the pointer. One caveat: the head drew in a still picture taken for this shelf, but nobody on this job has moved a mouse over it. So this pick rests on the award and the code, not on watching it. Runner-up, which I did see: **the Helmets Hall of Fame**, about two thirds of the way down. It is a dark grid of his race helmets, each in its own cell with a name and a year.

## How it turned out

- **Site of the Year 2025,** Awwwards Annual Awards, with 43 votes. This is the top prize of the year.
- **Site of the Year Users' Choice 2025** as well, with 596 votes. One site winning both is not the norm. In 2024 the two prizes went to different sites.
- **Site of the Day,** November 17, 2025. Eighteen judges gave it 8.18 out of 10. Design 8.12, usability 7.90, creativity 8.71, content 8.18. Awwwards members gave it 8.86.
- **Site of the Month.** It sits in Awwwards' monthly list between the picks for October and December 2025.
- **Developer Award,** 7.58 out of 10. This one is judged by engineers. Its best mark was for animation, 8.60. Its worst was for accessibility, 7.00.
- **DesignRush,** a directory of agencies, named it a best website design in April 2026 with a score of 9.38. That is a smaller prize than the ones above.
- **Not found:** I looked for an FWA award, a CSS Design Award and a Webby and could not confirm any. I found no published visitor or sales numbers.

## What makes it good, measured

I loaded the live page on November 16, 2026 in a private test browser, at a laptop size (1440 by 900) and a phone size (390 by 844). A short script read the type, colours and timings off the finished page and added up everything the page downloaded. The Awwwards tools gave me the jury scores and showed which code libraries the page ships. Section names come from screenshots I took at nine points down the page.

- **Length:** 13,579 pixels tall on the laptop, about 15 screens. On the phone, 10,077 pixels, about 12 screens.
- **Twelve sections in the page's code.** The eight I could tell apart by eye, in order:
  - The 3D head.
  - A "Message from Lando" video panel on dark olive.
  - A loose wall of photos with short quotes and a signature. This is the tallest part, 3,143 pixels.
  - A split: On Track on the left, Off Track on the right.
  - The Helmets Hall of Fame grid.
  - The store, under the headline "World Drivers' Champion".
  - A fan of social posts, laid out like a hand of cards.
  - A footer with a helmeted figure, the site menu and a strip of sponsor logos.
- **Type, two faces:**
  - Mona Sans, a plain sans, carries nearly everything. Body text is 14 to 17 pixels.
  - Brier, a sharp display face with thick and thin strokes, is used for single words inside headlines. A headline reads "ON TRACK" with one word in each face.
  - Big headlines are 93 to 110 pixels with lines packed tight, at about 0.82 of the type size. On the phone they drop to about 43 pixels.
- **Colour, four values do the work:**
  - Lime, #D2FF00, for every button and accent. One review ties it to his helmet.
  - Near black, #111112.
  - Dark olive, #282C20.
  - Off-white, #F4F4ED.
- **One motion curve.** 118 elements share the same transition: 0.75 seconds, on a curve that starts slowly, moves fast, then takes a long soft landing. In code that is cubic-bezier(0.65, 0.05, 0, 1). Only 10 elements use anything else.
- **What scroll does.** The page glides instead of stepping. Some motion is tied to how far you have scrolled, not to a clock, so it runs forwards and backwards with your hand. The code shows the camera pulling back from the 3D head this way.
- **What the pointer does.** The 3D head responds to the cursor. The page's styles hold about 30 rules for what happens under the pointer. A second count got 28. Seventeen small drawn animations sit around the page as badges and icons, and some of them are driven by scroll too.
- **How it's built,** each part in a few words:
  - Webflow: a visual site builder that also hosts the site.
  - Three.js: a library for drawing 3D in the browser. It uses WebGL, the browser's way of drawing with the graphics chip.
  - GSAP with ScrollTrigger: an animation library, and its add-on that ties motion to scrolling.
  - Lenis: a small library that makes scrolling glide.
  - Rive: a tool for small interactive vector animations.
- **Weight:** 5.5 megabytes before you scroll, in 64 downloads. 7.4 megabytes after scrolling the whole page, in 121. Of that, 4.6 are pictures, 2.0 are 3D models and textures, 0.6 is code and 0.2 is fonts.
- **On a phone:** the same 12 sections in one column. Four-column grids become two. The 3D head gets a "tap to lock" button, so a finger can either scroll the page or play with the head, not both at once. The phone downloads more, 8.9 megabytes after a full scroll.

### Why it's here

It is the spectacle that still behaves like a website. My read: the lesson for Designcraft is how little holds it together. One accent colour, two typefaces and one motion curve, used everywhere. The showpieces sit in two places, the head and the helmets. The rest is a tidy magazine layout. The caution: I could not watch the head myself, so its place as best moment rests on other people's eyes.

## What Sean said about it

Seen on November 17, 2026, with the rest of the shelf. This was one of the three the lead recommended, and of those he said: "amazing and very much what I hope Designcraft can produce for me."

He would not name it the house look. Of the whole shelf: "all of the options you provided are amazing in their own way and I wouldn't want to throw those out the window."

He agreed it is the starting point for web pages when a job names no look of its own: "Those will be the starting points to look at."

## More details

- Awwwards Annual Awards winners, 2025 (Site of the Year with 43 votes, Users' Choice with 596 votes): https://www.awwwards.com/annual-awards/winners
- Awwwards hall of fame, 2024 (the two prizes went to different sites that year): https://www.awwwards.com/annual-awards/hall-of-fame/2024
- Awwwards site page (Site of the Day date, jury scores, Developer Award marks, maker credit, palette): https://www.awwwards.com/sites/lando-norris
- Awwwards Sites of the Month list (its place between October and December 2025): https://www.awwwards.com/websites/sites_of_the_month/
- DesignRush review (Glasgow studio, helmet-based colours, April 2026 award and 9.38 score): https://www.designrush.com/best-designs/websites/lando-norris-website-design
- Codrops profile of the studio, which styles its name OFF+BRAND., August 17, 2026: https://tympanus.net/codrops/2026/08/17/creativity-at-enterprise-scale-without-compromise-the-offbrand-story/ . The page refused my fetch, so I used nothing from it.
- My measurements: a private headless Chromium driven by a short script, at 1440 by 900 and 390 by 844, 12 seconds of settling, then a full scroll. Library names and the ScrollTrigger version (3.13.0) come from the Awwwards bundle tool; the Three.js release (174) from the page itself.
- The Awwwards page-structure, scroll-map and motion tools would not run. They need a browser add-on, Playwright, that is not installed. I used my own script in their place.
- The page's own 3D scene did not draw in the test browser, which has no graphics chip. Timings and sizes are unaffected. What the head looks like in motion is not something I saw.
