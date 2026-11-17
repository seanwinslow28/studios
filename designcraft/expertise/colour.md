# Colour in an interface

Read this whenever a job reaches its colours: choosing a palette, setting a night version, checking that text can be read, or bending a brand's colours for a spectacle. How to write colours down, start from ready-made scales and measure contrast is in the colour tool guide; this brief is the judgement behind those tools. Colour grading of film belongs to Motioncraft.

## A colour never looks the same twice

A colour on a screen is not a fixed thing. Three forces change it, and a master judges every colour where it will live, never as a lone swatch.

- **Its neighbours.** The colours around a colour shift how light, how strong and even which hue it looks. The same grey looks pale on black and dark on white; a blue looks greener beside violet. So a palette that looked balanced as a row of chips can fall apart on a page. Judge colours in the layout, at the size they will be used.
- **Its amount.** A colour in a small area and the same colour as a whole field are different experiences. Lando Norris's lime is thrilling on a button and would be exhausting as a page. A strong colour gets stronger the rarer it is, which is why the action colour should appear in very few places.
- **Its strength.** Strong colours look lighter than they measure, and a yellow and a blue with the same lightness number in the older colour formats look nothing alike. The eye is a poor judge of lightness across hues, which is why the studio writes colour in a format built on how light a colour looks.

The room matters too: colours look less colourful in dim light, and a colour at the edge of what one screen can show may not exist on another.

## Building a palette

A working palette is mostly grey. Greys do nearly all the work: text, backgrounds, panels, lines, controls at rest. A screen needs roughly eight to ten, so text, quieter text, borders, hover states and two or three surface levels each get a step. Linear runs its whole app on a near-black ground, four greys for text by importance and one indigo.

Then one brand colour with a full ladder of shades: a pale tint for a background, a border, the solid fill for the main button, a darker fill for its hover, and a shade dark enough to be text. A five-colour palette from a generator cannot build a screen, because each of its colours is only one rung.

Then the status colours: red for danger, amber for warning, green for success, often blue for information. Each needs its own ladder, because an alert uses a pale ground, an edge, an icon and dark text, all in one hue.

What makes a palette strong rather than merely large:

- **Shades decided once, up front.** Lightening and darkening on the fly breeds dozens of near-identical blues and no system. Each colour gets a fixed set of steps, and work picks from them.
- **The same lightness at the same step, whatever the hue.** Stripe rebuilt its palette this way after finding its coloured text failed contrast: every hue followed one lightness curve, so a step number predicted contrast, and any two colours a set number of steps apart could be paired safely. Radix's scales work on the same idea.
- **Each step still looks like the same colour.** The palest and darkest steps need their strength tuned by eye, not copied from the middle, or they go chalky, muddy or out of the screen's range. Yellow is the classic trap: a dark, strong yellow barely exists on a screen, as Stripe's palette editor showed, so its darker steps need tuning by eye to stay recognisably yellow.
- **Greys with a temperature.** A touch of the brand's hue in the greys makes them sit with the brand colour instead of looking dead beside it. Linear's 2026 refresh warmed its grey. A neutral grey is still right when the content should lead, as on a photo site.
- **Proportion decided before colouring.** The ground takes most of the screen, and the accent stays under about one twentieth of any view, on the action and perhaps one other recurring thing.
- **Colours named by job.** "Action background", not "blue 600". A name that says what a colour is for stops it spreading to other jobs.

## Meaning without colour alone

About one man in twelve and one woman in two hundred sees colour differently, most often struggling to tell red from green. A red badge and a green badge can look identical to them. So colour may support a meaning but never carry it alone. Pair it with a word, an icon, a shape or a position. The UK government's visa checker shows an error four ways at once: a red-edged box at the top, a bold message beside the question, a red bar down its side, and a hidden "Error:" for screen readers. The Mechanical Watch article names its parts by colour in the text and colours the matching sliders, so the words and the colour carry the same meaning.

Give each colour one job and keep it. On the government's pages, yellow means only "this is where your keyboard is". The moment the action colour also decorates headings, it stops meaning "press here". Saturation can be a signal of its own: muted colour for everything at rest, strong colour only for what is active or needs a hand.

For charts, steps of lightness in one hue survive colour blindness better than a rainbow of hues. The chart skill has its own method.

## Contrast, and how it is measured

Contrast is how clearly a thing stands out from what is behind it. The rule most of the web meets, WCAG 2, measures it as a ratio of lightness between text and background: at least 4.5 to 1 for body text, and 3 to 1 for large text, icons, control edges and focus rings. It ignores hue entirely. A newer method, APCA, weighs light-on-dark differently from dark-on-light and accounts for thin small type; it is a second opinion, not yet the rule. The tool guide has the figures and the checker.

- **Measure what is drawn, not the values.** See-through text, overlays and text on photographs all fool a calculation made from colour codes. Text over a picture needs a calm region, or a quiet dark wash beneath it, or it moves off the picture.
- **Darken the text, not the badge.** White text on a bright badge often fails, and darkening the fill until it passes makes the badge the loudest thing on the page. Dark text in the badge's hue on a pale tint of it passes and stays calm.
- **Passing is not the same as good.** Contrast rules say nothing about whether hues can be told apart or look alive. Some people need more than the minimum and some find very high contrast painful, which is why Linear lets people choose a contrast level.

## Night mode is its own design

A night version is a second palette, designed, not the day palette flipped. Flipped colours give a harsh, glaring screen with muddy accents.

- **The ground is a deep, slightly tinted dark, and the text a soft light,** not pure white on pure black. Pure white text on black glares and seems to swell.
- **Depth comes from lightness.** Shadows barely show on dark, so a raised panel is a step lighter than the ground, and the closest thing is the lightest.
- **Light type looks heavier on dark.** Thin strokes and light text look bolder and larger than the same marks by day, so night often wants a lighter weight and a second look at fine lines.
- **Strong colours need taming.** Saturated colour glows and vibrates on a dark ground. Duolingo's night version lifts and softens its brand green, and its white becomes a deep blue-black.
- **Quieter text is where night fails.** The same contrast ratio reads harder light-on-dark; the tool guide's test found quieter night text passing WCAG comfortably but only just clearing APCA's floor.
- **Choose day or night from the scene of use,** who reads it, where and under what light, not from the category. And honour both the device setting and a switch on the page.

## Colour in a spectacle

A spectacle is allowed to let colour own whole regions. A page can be drenched in one colour, or change its entire background colour section by section, edge to edge, like chapters. Neighbouring sections should differ in lightness, not only in hue, or the join vibrates.

Bending a brand's colours is where spectacle starts. Shopify's Renaissance edition swapped software colours for a museum's cream and olive black, yet kept the product's own violet in the chapter about that product. Spotify Wrapped throws out the app's dark-and-green each December, and two years teach the edge. In 2024 every chapter got its own fully saturated colour, and loud soon became flat. In 2025 it cut back to near black and white with one accent at a time. Igloo Inc commits to one grey-blue range for the whole world. Raphael Segerman's portfolio shows the reveal version: a plain two-colour page, so the coloured second layer behind it hits hard.

Strange colour never cancels legibility. The reading layer stays readable, the action colour stays findable (Scout Motors keeps one orange for Reserve, always in reach), and a strange ground still gets text with enough contrast. A lime like Lando's takes dark text, not white.

## How it goes wrong

- **Grey text on a coloured panel.** It looks washed out and often fails contrast. Fix: take the quieter text from the panel's own hue, or use the panel's own ink.
- **Too few shades.** Five swatches and improvised tints. Fix: a full ladder for each colour, decided once.
- **Saturated everything.** Nothing leads, and the eye tires. Fix: one strong colour owns one region or one job; the rest goes quiet.
- **Pure black and pure grey.** Pure black is harsh and glares at night; untinted greys look dead beside a brand colour. Fix: a tinted near-black and greys with a trace of temperature. Duolingo sets its text in dark grey, not black.
- **Soft, see-through text.** Fading text to make it gentle quietly breaks contrast. Fix: a measured colour from the palette.
- **The generated look.** Cream with terracotta, violet everything, or neon on near-black, chosen because nothing was decided. Each is fine when the brief asks for it.

## What a strong designer would notice

- A palette judged as chips, never on the page.
- Too few greys, or untinted greys beside a warm brand.
- The action colour also on headings, icons and borders.
- A red and a green that mean opposite things with nothing else to tell them apart.
- Grey secondary text on a coloured field.
- Badges that pass contrast by shouting.
- Pure white on pure black, or a night mode that is the day mode upside down.
- A spectacle where every section is equally loud.
- Text over a photograph with no calm place to sit.

## More details

- **Tool guide:** `designcraft/tools/colour-oklch-and-radix.md` covers OKLCH, the Radix scales, the picker, the gamut checks, the contrast thresholds as the checker applies them, and the night-mode test figures this brief cites (Radix iris step 11 changing between day and night; quieter night text at Lc 61).
- **Shelf figures** come from `designcraft/research/`: `linear-app.md` (four text greys, one indigo, the contrast setting, the warmer grey), `duolingo-app.md` (dark grey text, night values for its green and white), `govuk-check-uk-visa.md` (one job per colour, the four-way error, yellow for focus), `ciechanowski-mechanical-watch.md` (parts named by colour in text and sliders), `lando-norris.md` (lime on buttons and accents, four values), `shopify-editions-renaissance.md` (cream, olive black, the kept violet), `spotify-wrapped-2024-and-2025.md` (one saturated colour per chapter in 2024, near black and white with one accent in 2025), `igloo-inc.md`, `segerman-portfolio.md`, `scout-motors.md` (the one orange).
- **Fundamentals, in the studio's own words:** Adam Wathan and Steve Schoger's *Refactoring UI* (the chapters on colour, depth, finishing touches and starting from scratch); Nate Baldwin's free guide Color and Contrast (colorandcontrast.com: context effects, why saturated colours look lighter, colour in dim light, light marks looking heavier on dark, contrast polarity, colour vision deficiency figures, APCA's status); Stripe's "Designing accessible color systems" by Daryl Koopersmith and Wilson Miner (2019: one lightness curve for every hue, pairing by steps apart, accessible is not the same as vivid); Rune Madsen's free book Programming Design Systems (the colour chapters: lightness first, then saturation, then hue; saturation as a signal of state). All read November 17, 2026; private notes are in `designcraft/library/`.
- **Salvaged craft,** in this studio's words: the Impeccable skill's colour guidance (roles over swatches, secondary text from the surface hue, night mode composed rather than inverted, strategies from restrained to drenched, choosing day or night from the scene of use); the frontend-taste skill's colour reference (ground, ink and accent proportions, section fields that differ in lightness, the generated-look families); the house style at `SWCB/docs/pages/DESIGN.md` (no pure black or white; both the device setting and a page switch).
- **Motioncraft:** `motioncraft/expertise/colour-and-finish.md` and `design-and-look.md` were read so nothing here contradicts them. Both agree that a few colours with clear jobs beat many, and that one hue lifted against the rest reads richer than raising saturation everywhere.
- **Not confirmed:** the WCAG 3 to 1 figure for icons, control edges and focus rings is from the Impeccable skill and WCAG's non-text contrast rule as commonly applied; the colour tool guide's own test measured text only.
