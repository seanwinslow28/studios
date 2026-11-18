# Raphael Segerman's portfolio (2026)

## What it is

The personal site of Raphael Segerman, a creative developer in Cape Town who builds award-winning sites for design studios. It shows five projects and very little else.

It looks like a quiet white page. Then one small button in the corner swaps it for a blue planet in space, and the same five projects are floating in front of it in full colour. The site's own line says it: "more to discover beneath the surface."

Sean added it on November 17, 2026 as the model for his own site.

See it: https://segerman.dev/

**Best moment: press the small moon in the top right corner, then click Estrela Studio.** The white page gives way to the planet. The click passes through a full-screen view of the blue planet and lands on a purple horizon with the project's name across it. The code gives each project its own colour. Runner-up: **roll the mouse wheel on the plain white page.** The column of pictures never ends. It loops round to the first project again.

## How it turned out

- **Awwwards Honorable Mention, August 2, 2026.** Awwwards is the best-known web design award site, and this is its first rung, below Site of the Day. Fifteen members scored it, from 6.30 to 9.00 out of 10. The judges' page singles out, each with a short clip, the mode change, the endless scroll, the page changes in each mode, a reveal under the cursor, and the planet's surface.
- **Estrela Studio's site, one of the five projects here, won Site of the Day** on January 9, 2026, and the Developer Award, with a jury score of 7.24 out of 10. Its page credits four accounts, and Raphael Segerman is one.
- **Yucca Packaging's site, another of the five, won the same two awards** on January 31, 2026, with 7.17. That page credits the design studio and Zulik, the studio he co-founded, not him by name.
- **His own count,** from his About page, matches the four Awwwards awards above and adds one FWA Site of the Day, which his page for Zulik's own site says is for that site. Nobody on this job could confirm it on FWA.
- **The caution:** an Honorable Mention is a modest prize. This site is on the shelf because Sean chose it, more than for its trophies.

## What makes it good, measured

On November 17, 2026 a short script in a private test browser read the type, colours and downloads off the page, at a laptop size (1440 by 900) and a phone size (390 by 844). On November 18 I watched it move at both sizes, by wheel, pointer, keyboard and finger, and read each timing frame by frame.

- **One screen, three columns that never change places.** On a laptop the page is exactly 900 pixels tall and ordinary scrolling is off. On the left, the name and one line about the work; in the middle, the five project pictures; on the right, the same five as a list of names. The wheel moves only the middle column, and the five repeat for as long as you scroll.
- **Two layers, and this is the idea:**
  - Plain: a white page, navy type, and pictures reduced to navy and white with a fine speckled grain.
  - Revealed: a 3D planet behind everything, the same pictures in full colour and tilted in space, and white type with a soft glow.
  - One button moves between them. Its label in the code is "Toggle mode". The planet sits under the plain layer too, and on a project page it takes that project's colour.
- **A project opens onto a row of five short clips,** 3 to 10 seconds each, under its name at 100 pixels. The row is flat on white in the plain layer and curved like the inside of a drum in the revealed one. The wheel moves it sideways, and it loops too.
- **Type, two faces:** Newake, a heavy all-capitals display face, for the headline only, at 87 pixels on a laptop with lines packed at 0.8 of the size, and 62 on a phone. Aktiv Grotesk, a plain sans in one weight, for everything else, and small: 12 to 14 pixels on a laptop.
- **Colour, two values on the plain home page:** navy-black, #00031F, and white, #FFFFFF, with small labels in a paler tint. On the plain layer, colour shows up only in moving clips.
- **A loading count** comes first, and the code makes it last at least 2.4 seconds however fast the page loads.
- **Weight:** 2.2 megabytes to show the home page, and about 3.8 after pressing the button and opening one project. Lando Norris's site, also on this shelf, takes 5.5 megabytes before you scroll.
- **How it's built:** Astro for fast, mostly plain pages; Three.js for the 3D; GSAP for animation; Lenis for the glide; and Barba, which changes pages without a reload, so the planet stays on screen between pages. No element uses a stylesheet transition: every movement is driven by script or drawn by the graphics chip.

### How it moves

**The plain page never moves on its own, and each touch gets one small, quick answer.** Only the mode button gets a big move.

- **At rest, nothing.** With no input, not one pixel of the plain page changes.
- **A wheel step glides.** One step moves the column 60 pixels on a sharp (Retina) screen and 80 on an ordinary one. It starts within 40 milliseconds, is 90% of the way there in about 0.56 seconds and rests after about 1.1: a fast start and a long, gentle stop, called an ease-out. At speed the column bends like a page curling over a drum. One lap of the loop is about 25 steps, with no seam.
- **The mode button is the one big move.** Resting on the moon opens a small round window onto the planet. On the press, everything starts within a frame or two: a wavy edge rises from the bottom, halfway in about 0.3 seconds and at the top in about 0.85, fast at first and slowing hard, while the pictures swing into 3D, 90% done in 0.36 seconds. Going back, white rises from the bottom with the same timings.
- **The pointer cuts a trail.** Moving it anywhere on the plain page opens a soft, comet-shaped hole, about 150 pixels thick, and the planet shows through. Each spot closes about half a second after the pointer leaves.
- **A name or a picture gets one small answer.** Rest on a name and the other four fade in 0.3 seconds while a small clip of that project slides up under the list. Rest on a picture and it zooms in 9% inside a frame that holds still, 90% done in about 0.6 seconds.
- **Opening a project.** In the plain layer, a white sheet rises over the dimming page and reaches the top at about 0.9 seconds, and the row slides in from the right, 90% in place at 1.45. In the planet layer, the page breaks into islands by 0.5 seconds, the screen is all planet in the project's colour by 1.0 to 1.3, and the row is still at about 2.5.
- **On a phone** it becomes an ordinary scrolling page with each picture's name underneath and no loop, in 1.8 megabytes. Tapping the moon sweeps the planet in sideways in about 0.8 seconds.
- **With less motion turned on, it is a different page.** The site checks the setting first and never loads the moving version: no planet, button, trail, loop, list of names or glide. The two-colour look goes too, because the 3D layer draws it, so the photos show in full colour in a two-column grid. Every clip still loops, including five hidden ones.
- **By keyboard, you can open a project but can't see where you are.** The Tab key reaches all 16 controls, but only the first, "Skip to content", showed a focus mark in the test browser. The five picture links all sit in one box at the top of the column. On a project page the clips can't be reached and have no text for a screen reader.

### Why it's here

Sean chose it as the bar for his own site. What makes it great, in the order he confirmed:

1. The page holds still and only the work moves.
2. The biggest move is saved for one button.
3. Every other touch gets one small, quick answer.
4. The pointer's trail gives a glimpse of the second layer before you open it.
5. The column never ends.
6. A piece opens onto a row of five short clips, which loops too.
7. Restraint and lightness: two colours, two typefaces, small text, 2.2 megabytes.

The cautions, beyond the modest prize: a full-colour page with every clip looping for visitors who ask for less motion; a keyboard that shows where you are at only one stop; and a loading count that lasts at least 2.4 seconds.

## What Sean said about it

He added it himself on November 17, 2026 and called it "the main inspiration for my website update", the site "showing what good looks like." In the same message: "I'm a sucker for scroll effects and reveals. Scrolling is a great way to tell the story."

On November 18, 2026, after watching it move on a review page beside six other examples, he confirmed the ranking above: "Yes, in this order."

## More details

- The site, its About page and a project page, read November 17 and 18, 2026: https://segerman.dev/ , https://segerman.dev/info , https://segerman.dev/work/estrela
- Awwwards page for this portfolio (15 of 16 votes, the six highlighted clips, one named "Cursor Reveal"), found by a helper after my first searches missed it: https://www.awwwards.com/sites/raphael-segerman-portfolio
- Awwwards pages for Estrela Studio (Developer Award 7.28) and Yucca Packaging (Developer Award 7.16, read by the helper): https://www.awwwards.com/sites/estrela and https://www.awwwards.com/sites/yucca-packaging
- Timings come from the site's own running values, logged once per screen redraw (good to about 17 milliseconds), and from stepping through the motion at 25 frames a second (about 40). Every planned length in the code that I checked matched. The 3.8 megabyte figure is a slight undercount.
- Wheel steps were sent as standard 100-pixel notches. The glide is counted in screen redraws, so a 120-redraw screen would settle it about twice as fast; read in the code, not measured.
- Projects opened: Estrela in the plain layer, Yucca Packaging in the planet layer.
- Typefaces, from the font files: Newake, by Indieground, and Aktiv Grotesk Medium, by Dalton Maag.
- Corrected on November 18, after watching it move. The judges' cursor reveal is the trail on the white page, not something on the pictures, which get a 9% zoom. The plain project page does have a planet underneath, in the project's colour. The row a project opens onto loops. The less-motion version is a different design, not a plain copy. And the planet page change settles at about 2.5 seconds, replacing rough readings of 0.3, 0.9 and 4.4.
- Not checked: real hardware (a real mouse, trackpad or iPhone, and Safari's own scroll settings), the changes to the next project, back to the index and to the About page, a screen reader, a focus mark in a normal browser window, and sound.
