# Design systems and brands

Read this when a job spans more than one screen, borrows a brand that already exists, or sets out to turn a brand on its head for a spectacle. It covers what a design system really is, why limits make design faster, what makes a brand recognisable, and how to break a brand without losing it. How the values file is written and built into code is in the design values tool guide; this brief is the judgement behind it.

## What a design system really is

A design system has three layers, and only the third is hard.

- **Values.** The named colours, type sizes, spaces, corner sizes, shadows and timings a design is allowed to use.
- **Parts.** The button, the card, the text field, the menu: pieces built only from those values, each with every state designed (at rest, hovered, pressed, focused, switched off, in error).
- **Judgement.** When to use each part and value, and when not to. "The accent is for actions only, never headings." "One question per page." This is the layer most systems skip, and it is the one that keeps a design whole when someone new picks it up.

The UK government's design system is the clearest example on the shelf. It publishes its values (one typeface in two weights, spacing in steps of five, each colour with one job), its parts (the button with its darker strip, the error box), and its written judgement (label the button "Continue", not "Next"; never mark required fields with a star). More than 300 services build from it, and they read as one government.

Rune Madsen's free book on design systems opens with a parable worth keeping. A designer makes a lovely label for one beer, then has to make ten more, and because the first was styled only for itself, the eleven labels share nothing. The fix is to decide the range first: a family of faces and colours varied enough for each beer and recognisable as one brewery. A system is that range, decided before the first piece. Its best rules are simple to state and still make many different things. Pentagram's identity for the MIT Media Lab grew marks for all 23 of its research groups from one small grid.

One structural habit makes everything later cheap. Name values twice: once for what they look like (ember, ink, paper), then for what they are for (action background, body text, ground). Pages use only the second set. A night version, a high-contrast version or a brand turned inside out is then a change of pointers, not a rewrite. Linear rebuilt its themes this way, from 98 hand-set colours per theme to three choices: a base colour, an accent and a contrast level.

## Constraint is a speed-up

A designer choosing from every possible value agonises over 13 pixels or 14. A designer choosing from a short scale picks between a few clearly different options, and usually two of them look obviously wrong at once. A limited set of sizes, spaces, colours, corners and shadows is not a cage. It is the reason good systems move fast.

What a strong scale looks like:

- **Steps far enough apart to tell apart.** If two neighbouring sizes look the same, one of them is waste. Spacing and type scales usually grow by a ratio, so the big end has bigger jumps than the small end.
- **Each step with a meaning.** Shadows work best as a few heights, each tied to a kind of thing: slightly raised for a button, higher for a menu, highest for a dialog. Pick the height, and the shadow follows.
- **Personality set by a few dials.** Typeface, colour, corner shape and the tone of the words decide most of how a product feels. Square corners read formal, large round ones playful. Mixing square and round in one design almost always looks worse than either.
- **Repetition everywhere.** Lando Norris's site runs on one accent, two typefaces and one motion curve, shared by 118 elements. Scout Motors shares one curve across 159. Linear is one typeface, four greys, one accent and 28-pixel rows. Duolingo has one button, used everywhere, and only two weights of type.

A system grows only when the same need comes up twice. A value added for one screen is the first crack.

## What makes a brand recognisable

A brand is not its whole style guide. People recognise it by a few carriers, often only one or two:

- **A colour.** Lando's lime, Scout's orange, Spotify's green, Duolingo's owl green. Motioncraft calls these memory colours: people forgive shifts anywhere else and notice a wrong one at once.
- **A face.** Scout Motors sets everything in its own family, Scout Sans. Duolingo has two faces of its own.
- **A shape.** Duolingo's chunky round buttons and its drawing rules (round, friendly forms, features pushed toward caricature). Spotify's small round logo.
- **A voice.** The way it talks. Duolingo's characters cheer and react; the UK government speaks plainly and never more than it must.
- **A motion habit.** A press that drops four pixels; one curve on everything.

The way to find the carriers is to look at what a brand never changes across its own variations. Shopify's Editions change costume every season, yet keep the same chapters, the same card for each update, and the product's own type wherever the product itself appears. Spotify Wrapped changes its palette every December but keeps the round logo at the top of every card and one fact per card. Those are the carriers. Everything else is free to move.

A quick test: cover the logo. If you still know whose it is, the carriers are doing their work.

## Turning a brand on its head

Sean's meaning of spectacle: take a brand's design system and turn it on its head; get interactive, get creative, explore, get weird. A tidy deck with good bones is not a spectacle.

The craft is to keep the skeleton and one or two carriers fixed, and bend everything the eye lands on. Shopify's Renaissance edition is the model: shop software dressed as 500-year-old oil paintings in a 3D gallery, with museum cream, serif headlines and drop caps, while the chapters, the update cards and the product's own type stay exactly as every edition has them. It won Webbys three years running in three costumes.

The moves that turn a system over:

- **Swap the roles.** The quiet colour becomes the ground; the ink becomes the accent.
- **Push the scale to its ends.** Gentle type steps become one enormous size and one small one. Scout sets a few words at 270 pixels, as pictures more than text.
- **Borrow a world.** A gallery of paintings for shop software. A snowy mountain of ice blocks for a penguin company, as Igloo Inc does.
- **Change the medium.** Scroll drives a film: Scout's new truck drives at you and turns into the 1960s original, so the brand's past becomes the reveal.
- **Make it touchable.** Lando's 3D head follows the pointer. Wrapped's 2025 quiz asks you to guess your top song before revealing it.
- **Hide a second layer.** Shopify hid a key that unlocks a graffiti layer. Raphael Segerman's plain white portfolio flips to a planet in space.

Weird works when the strangeness answers the brand or the story. Paintings suit a release about craft; ice suits penguins; the old Scout suits a revived name. Strange for its own sake is just novelty, and novelty wears off by the third screen.

The tool guide shows how the values file makes this cheap: the brand's raw values kept whole, the meanings rewritten, the spectacle built as a second theme beside the everyday one.

## How it goes wrong

- **A system that is only a component library.** Parts with no shared values and no written judgement, so every team uses the button differently. Fix: the values underneath and a plain page of when and when not.
- **Values named by their look.** A page that asks for "ember" can't be re-themed. Fix: pages ask only for meanings.
- **Too many values.** Forty greys, a size for every screen. Fix: prune to steps that look clearly different, and add only on the second need.
- **A system that forbids surprise.** Every page looks the same and no spectacle is possible. Fix: the system says where freedom lives, such as one hero section per page.
- **A rebrand that loses the brand.** Colour, face and shape all changed at once. Fix: keep at least one carrier untouched.
- **A spectacle that is just noise.** Spotify Wrapped 2024 had loud colour and a repeated frame on most cards, and listeners still felt short-changed because favourite parts were gone. Fix: substance first, one world, one idea, every strange choice traceable to the brand or the story.
- **A spectacle that breaks the job.** Igloo Inc draws every letter inside its 3D scene, so screen readers find nothing, and its accessibility mark was among its lowest. Scout's scroll film makes its page download over 30 megabytes on a phone and over 50 on a laptop. Fix: keep the reading layer, the action and the weight inside what the audience can bear.
- **A borrowed look, not a borrowed system.** Copying a competitor's surface makes a second-rate copy of them. Fix: borrow how a system is built, never how it looks.

## What a strong designer would notice

- A button styled three ways on three pages.
- A spacing value that appears exactly once.
- Two neighbouring sizes nobody can tell apart.
- Square and round corners in one design.
- Colours named after how they look, used directly on pages.
- No written word on when not to use a part.
- A spectacle with no fixed carrier left, so the brand is gone.
- A spectacle where every section is loud, so none is.
- Strangeness with no tie to the brand or the story.
- The skeleton changed while the surface stayed timid: exactly backwards.

## More details

- **Tool guide:** `designcraft/tools/design-values-and-style-dictionary.md` covers the values file format, the build, the two naming layers in practice, the brand reader, and the second-theme approach to turning a brand over.
- **Shelf figures** come from `designcraft/research/`: `govuk-check-uk-visa.md` (published values, parts and written rules; 300 services), `linear-app.md` (98 settings to three, one typeface, four greys, 28-pixel rows), `lando-norris.md` (one curve on 118 elements, the pointer-led head), `scout-motors.md` (Scout Sans, one curve on 159 elements, 270-pixel words, the scroll film, 51.7 megabytes on a full laptop scroll and 33.5 on a phone), `duolingo-app.md` (one button, two weights, own faces, drawing rules), `shopify-editions-renaissance.md` (what was bent and what was kept, the hidden graffiti key, three years of Webbys), `spotify-wrapped-2024-and-2025.md` (what changes and what stays each December, the 2024 reception, the 2025 quiz), `igloo-inc.md` (text drawn in 3D, accessibility its lowest mark), `segerman-portfolio.md` (the second layer).
- **Fundamentals, in the studio's own words:** Adam Wathan and Steve Schoger's *Refactoring UI* (the chapters on starting from scratch, depth and finishing touches: personality dials, choosing from a short scale by comparing neighbours, shadows as heights); Rune Madsen's free book Programming Design Systems ("What is a design system?": the brewery parable, simple rules that make many outputs, the MIT Media Lab identity), read November 17, 2026. Private notes are in `designcraft/library/`.
- **Salvaged craft,** in this studio's words: the Impeccable skill (amplify what a system already owns so the bolder version looks more like the brand; tokens named by meaning; extract only what is reused) and the frontend-taste skill (keep a brand's palette and type and take only composition from elsewhere). The house style at `SWCB/docs/pages/DESIGN.md` was read; nothing in it bore on this brief beyond what the colour brief takes.
- **Motioncraft:** `motioncraft/expertise/colour-and-finish.md` (memory colours) and `design-and-look.md` (one world, one set of decisions applied everywhere) were read so nothing here contradicts them.
- Sean's words on spectacle are from the shared brief for this build and the shelf README, November 17, 2026.
