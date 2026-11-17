# Colour: palettes written by lightness, ready-made scales, and a contrast check

This guide is about the colour tools: writing a palette straight into the page in a colour format built on lightness, starting from a set of ready-made colour scales, giving Sean a free picker to nudge any colour, and measuring contrast with the checker. Read it before you set the colours for any job. Which colours a design should have is a craft question for the colour brief.

## What each is best at

- **OKLCH is how the colours are written.** It names a colour by three numbers: lightness, chroma (how strong the colour is) and hue (where it sits on the colour wheel). Its promise is that lightness means what it says: two colours with the same lightness number look equally light, whatever their hue. Older ways of writing colour, like hex codes or HSL, don't promise that. It means a scale, a hover state or a night version can be made by changing one number. Every major browser has read OKLCH since May 2023.
- **Radix Colors is where a palette starts.** It offers 31 colour scales, each in 12 steps, each step with a job, and each with a matching night version. The two text steps come with a contrast promise. Radix ships its scales as hex codes and in the wider P3 range, not as OKLCH; one line of code converts them.
- **The OKLCH picker is for Sean.** It is a free web page made by Evil Martians. Paste any colour and it shows the three numbers, with sliders for each. It marks the edge of what ordinary screens can show, and of the wider ranges newer screens reach, and offers the nearest colour that fits.
- **The checker measures contrast** on the finished page: axe-core, run through Playwright, is already installed for Designcraft. Contrast is how clearly text stands out from what is behind it.

Where something else wins:

- **A palette that must be built from a target contrast:** Harmonizer, from the picker's makers, or Leonardo, from Adobe. Both are free and on the runners-up list.
- **A brand that already has colours:** read them off the live site first with the InspoAI brand reader, then convert them. Don't redraw a brand from Radix.
- **Colours for charts:** the dataviz skill has its own method.

## Setup

- **Nothing to sign up for.** The palette is a few lines of CSS. Radix comes as a free package added to the job's project, or its values can be copied from its site. The free culori library does the conversions and the gamut checks.
- **The one command that proves it works** converts a Radix colour to OKLCH:

```bash
node -e "const {formatCss,oklch}=require('culori'); console.log(formatCss(oklch('#5b5bd6')))"
```

It prints `oklch(0.54 0.184 278.28)`, give or take the decimals. That is Radix's iris step 9.

- **The picker** opens in any browser at its own address. Nothing to install.

## Getting the best out of it

**Name each colour by its job, not its step.** Radix's twelve steps each have one job. Write them into the page under job names, so the code says what each colour is for:

| Steps | Job | A good name |
|---|---|---|
| 1 and 2 | The page, then cards and sidebars | `--bg`, `--surface` |
| 3, 4, 5 | A control at rest, hovered, pressed | `--ui`, `--ui-hover`, `--ui-active` |
| 6, 7, 8 | Quiet lines, then borders on controls, then hovered borders and focus rings | `--line`, `--border`, `--border-hover` |
| 9 and 10 | Solid fills, such as a main button, and their hover | `--solid`, `--solid-hover` |
| 11 and 12 | Quieter text, then main text | `--text-low`, `--text` |

Use two scales: a grey with a faint tint for the page, and one accent. Step 9 is the purest, strongest colour in each scale. Most take white text on top; Radix says sky, mint, lime, yellow and amber need dark text instead. That matters for a lime like Lando Norris's.

**Night mode is a second set of values, not a filter.** Write the night values under the dark colour scheme, and again under a manual switch, so a visitor's choice and a page toggle both work. Radix's night scales are tuned on their own, not flipped. In the test, step 9 stayed the same colour by day and night, while step 11 went from a deep violet to a pale lilac. Set `color-scheme` too, so form controls and scrollbars follow.

**Nudge by changing one number.** This is what OKLCH buys. To shift a brand colour warmer, turn the hue a few degrees and leave lightness and chroma alone; the colour keeps its weight on the page. To make a quieter version, lower the chroma. Near white and near black, ease the chroma down: a strong colour at extreme lightness looks garish or simply can't be shown. Sean can do the same in the picker and paste the result back.

**Stay inside what screens can show.** Chroma has no fixed top. How strong a colour can get depends on its hue and lightness, and some combinations don't exist on any screen. The test made the point:

- At 90% lightness, chroma 0.15 is fine for a yellow (hue 100).
- The same numbers for a blue (hue 265) can't be shown on an ordinary screen. The strongest blue that light is about 0.05.
- A green at 55% lightness and chroma 0.30 is beyond even the wider P3 range of newer Apple screens. The strongest that ordinary screens show is about 0.17.

A colour outside the range is not the colour anyone sees: the browser has to substitute one it can show. Check each colour in the picker or with culori before it goes in. Newer Apple screens do reach further than ordinary ones; Radix ships P3 versions of its scales for them, and the picker shows both edges.

**Measure contrast on the rendered page, not from the values.** The rule most of the web follows, WCAG 2, asks for 4.5 to 1 for body text and 3 to 1 for large text. Large means 24 pixels, or about 19 pixels when bold. The test built a small palette from Radix's sand and iris scales and measured eight text pairs, day and night. Every planned pair passed. Main text on the page measured about 16 to 1 in both. White on the solid button measured 5.4 to 1.

The difference between two ways of measuring showed up on a planted fault. A script that read the text and background colours from the page called the faint label a pass, at 4.6 to 1. The checker called it a fail at 2.9 to 1, because the label was set three-quarters see-through, which the colour values alone don't show. The checker found the same fault by night, at 4.3 to 1. Use the checker; a values script is a quick first look.

**APCA, a note.** APCA is a newer way of measuring contrast that weighs light-on-dark and dark-on-light differently, and Radix uses it for its own promise: step 11 text reaches at least Lc 60, and step 12 at least Lc 90, on step 2. Lc is APCA's score. WCAG 2's ratio is still the rule to meet; APCA is a second opinion. The two disagreed most at night. Quieter text by night scored a comfortable 9 to 1 on WCAG 2 but only Lc 61 on APCA, just over Radix's floor. By day the same pair scored 5.9 to 1 and Lc 79. When a night page feels harder to read than its numbers say, APCA is usually why.

## Where it goes wrong

- **A colour outside the screen's range.** Shown above. The tell is a colour that looks different on Sean's screen and on a phone.
- **Hue numbers copied from another system.** Hue 250 in HSL is not hue 250 in OKLCH; each system places hues at its own angles.
- **Chroma written as a percentage.** In OKLCH, 100% chroma means 0.4, not 1. Write plain numbers.
- **A Radix promise used off its background.** The text steps are promised on step 2. The planted fault, step 11 on step 5, barely passed even before it was made see-through.
- **See-through text, overlays and pictures.** Contrast worked out from the colour values misses all three. The checker measures what is drawn, but it can't measure text over a photo or a 3D scene; it lists those under "need a person to look".
- **Step 9 used for text.** It is a fill. Text uses 11 and 12.
- **Night mode that only answers the device setting,** or only the page's switch. Write both.

## Safety

- **Nothing is uploaded.** The palette lives in the page; Radix and culori run in the project. The picker is a public web page, so treat what you type into it as not secret. A brand's colours are public anyway.
- **Licences:** Radix Colors and culori are free and open. axe-core is open under the Mozilla Public License.
- **Cost:** nothing.

## More details

- **Tested November 17, 2026,** in a scratch project at `designcraft-jobs/tests/type-colour-spectacle/` (outside every repo):
  - `@radix-ui/colors` 3.0.0 ships hex values and `color(display-p3 …)` values, with alpha versions; no OKLCH. 31 scales.
  - `culori` 4.0.2 converted the sand and iris scales (light and dark) to OKLCH custom properties (`scripts/palette.mjs`). Chrome's computed style reported them back as `oklch(...)`.
  - Gamut checks with culori's `inGamut('rgb')` and `inGamut('p3')`, and `clampChroma` for the largest sRGB chroma: `oklch(90% 0.15 265)` out of both (largest sRGB chroma 0.048); `oklch(90% 0.15 100)` in both; `oklch(55% 0.30 145)` out of both (0.173).
  - Iris step 9 is `#5b5bd6` in both the light and dark scales; step 11 is `#5753c6` light and `#b1a9ff` dark.
  - The page viewed in the browser pane by day and night (`colour.html?theme=light` and `?theme=dark`). The contrast script (`scripts/contrast.mjs`) emulated each colour scheme in Playwright 1.65.1 and computed the WCAG 2 ratio with culori's `wcagContrast` and APCA with `apca-w3` 0.1.9.
  - Day: text on page 16.03, quieter text on page 5.94 (Lc 79), white on solid 5.37. Night: text on page 16.29, quieter text on page 9.03 (Lc 61), white on solid 5.37. The planted fault (step 11 on step 5 at `opacity: .75`): the script said 4.62 by day; axe said 2.86 by day and 4.27 by night.
  - axe-core through Designcraft's `axe_check.mjs`, desk by day, desk by night and phone by night: one serious contrast fault each time, the planted one, and nothing else.
- **The contrast thresholds** (4.5 to 1, and 3 to 1 for text at 24 px or 18.66 px bold) are WCAG 2's level AA as axe-core applies them; the checker's report gave "4.5:1" as the expected ratio for the 17 px label.
- **Sources, read November 17, 2026:** Radix on the scale's steps and contrast promises (https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale); Radix's custom palette page (https://www.radix-ui.com/colors/custom), whose copy format the page did not state; the OKLCH picker (https://oklch.com/); MDN on `oklch()` (https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/oklch), for the value ranges, the 0.4 equivalence for percentage chroma, hue angles differing between spaces, and support since May 2023. Treatment of chroma near white and black is salvaged from the Impeccable skill's colour notes, in this studio's words.
- **Not confirmed:** what Radix's custom palette page copies out, and whether the picker page sends anything it is given.
