# Design values and Style Dictionary

A design system, in Designcraft, is one file of design values (the colours, type sizes, spacing and timing of a design, each with a name) plus a plain page beside it that says how to use them. Style Dictionary, a free tool, turns that file into code a web page can read. To start from a brand that already exists, the InspoAI connection reads the brand's live site first. Read this before setting up the look of any job that will span more than one screen, or before borrowing a brand.

Designers call design values tokens. The file follows a shared standard from the Design Tokens Community Group, so other tools can read it too. Its first stable version is dated October 2025.

## What the test showed

On November 17, 2026, a small values file went through Style Dictionary in a scratch project: four colours written in OKLCH (one of them deliberately brighter than ordinary screens can show), two colours that point at other colours, a typeface, four type sizes, two weights, five spacing steps, an easing curve and a duration.

- **The tool's stock web setting threw OKLCH away.** Every colour came out as an old-style hex code, and the colours that pointed at others were copied as fixed codes. So changing the accent would no longer carry through.
- **Two changes fixed both.** Swapping in Style Dictionary's own OKLCH colour step kept every colour as written, such as `oklch(0.5500 0.1700 35.00)`. Asking it to keep references made the pointing colours come out as `var(--color-ember)`, so they still follow the accent.
- **Sizes and timing came out right:** sizes in rem or pixels as written, the curve as a CSS curve, 160 milliseconds as `0.16s`.
- **A misspelt reference stopped the build** with a clear error. Good.
- **Two other mistakes did not.** A misspelt colour space (`okclh`) built "successfully" and wrote `[object Object]` into the CSS. And the standard's second way of pointing at a value, by path, built a grey: the colour lost its strength and nobody was told.
- **The built file worked in a browser.** The icon test page read its ground, ink and button colours straight from it.

Style Dictionary's own page says it does not yet fully support the October 2025 version. The test bears that out: the common parts work, the edges fail quietly.

## What it's best at

- **One source for every surface.** The same file feeds a plain page, a React build, a deck in code and a Claude Design system, so a colour changed once changes everywhere.
- **Names that carry meaning.** "Action background" says what a colour is for; Devcraft and Sean read the same word.
- **Themes from one palette.** Night mode, a print version or a spectacle edition are each a second set of meanings laid over the same raw colours.

Where another tool beats it:

- **A single page.** Write the values straight into the page's style block. A build step for one file is ceremony.
- **A React build with Tailwind.** Tailwind reads values from its own block in the stylesheet. Style Dictionary can write that block, but for one app the block itself can be the source.
- **Terrazzo** does the same job and is newer; worth a try if Style Dictionary's gaps start to bite.
- **Figma-based teams** use Tokens Studio, which is paid for the useful plan.

## Setup

- **Install into the project that needs it,** never system-wide: `npm install style-dictionary`.
- **Cost:** free and open source.
- **The command that proves it works:** `npx style-dictionary --version` prints the version. A build is proved by opening the CSS it wrote and searching it for `[object Object]`.

## Getting the best out of it

**Write colour the standard's way.** A colour is a small object: the colour space, three numbers, and optionally a hex fallback for screens that can't show it.

```json
"ember": { "$value": { "colorSpace": "oklch", "components": [0.55, 0.17, 35] } }
```

OKLCH lightness runs from 0 to 1 in the file, not as a percentage.

**Keep the OKLCH step and keep references.** In the build settings, use the OKLCH colour transform in place of the stock colour step, and set `outputReferences: true` on the CSS file. Without them the file still builds; it just quietly loses what made it worth having.

The difference in the output:

```css
--color-action-background: #c0401f;              /* stock */
--color-action-background: var(--color-ember);   /* with references */
```

**Two layers: what it is, then what it's for.** The first layer names raw values by their look (ember, ink, paper). The second names them by job (action background, body text, ground) and only points at the first. Pages use only the second layer. That split is what makes a theme, or a brand turned on its head, a change of pointers rather than a rewrite.

**Set the type once per group.** A group can declare that everything inside it is a colour or a size, so each value doesn't repeat it.

**Point with curly braces only.** `{color.ember}` works. The path form (`#/color/ember/...`) silently failed in the test.

**The plain page beside it.** Say in a few lines what each meaning is for and when not to use it: "Ember is the one accent. Actions only, never headings." The values file can't say that, and it's what stops the accent spreading to every link.

## Starting from a brand: the brand reader

The InspoAI connection's brand reader takes a web address and returns the site's logo, its colours ranked by how often the stylesheet uses them, named colour variables, suggested ground, ink and accent, and its typefaces.

Tested on the UK government's main site, then checked against the live page in the browser:

- **Right:** the brand blue (the big first block of the page), the near-black text, the link blue, the typeface and the fact that it is self-hosted, and the logo as clean, ready-to-use vector code.
- **Wrong:** it listed a named "primary button" green that no element on the page uses. The live buttons are a slightly different green. Its third-ranked colour, a bright yellow, is only the keyboard focus highlight; at rest, no element on the page shows it. Ranking by stylesheet use promoted it above the real brand blue.
- **Missing:** whether the typeface may be reused. This one is the government's own face.

So the reader is a quick first sketch. Every value it returns gets checked against the live page before it enters the values file.

**A hard limit found in testing:** the connection is on InspoAI's free plan, which allows 5 calls a month, and they ran out during this test. Use them on brand reads only, and ask Sean before a job that needs more.

## Turning a brand's system on its head

Sean's idea of spectacle is a brand's own design system turned inside out without losing the brand. Shopify's Renaissance edition, on the shelf, kept its chapters, card format and plain body type, and changed everything the eye lands on. The values file is where that becomes cheap.

- **Keep the raw layer whole.** The brand's actual colours, typeface and logo stay exactly as the brand defines them. That is what keeps it recognisable.
- **Rewrite the meanings layer.** The quiet accent becomes the ground, the ink becomes the accent, the type scale jumps from gentle steps to one huge size and one small one. Each is a changed pointer, not a new colour.
- **Build the spectacle as a second theme** from the same file, so the everyday look and the turned one sit side by side and Sean can flip between them.
- **Push the values the brand never uses.** Spacing doubled, timing slowed, an extreme weight of the same family. The brand never said these were forbidden; it just never went there.
- **Keep one anchor untouched.** The logo, the signature colour, or the typeface. Change all three and it's a different brand.

## Where it goes wrong

- **`[object Object]` in the CSS.** A misspelt colour space or an unusual value shape. The build reports success; search the output every time.
- **A colour that went grey.** A value pointed at by path, not by curly braces.
- **Hex where OKLCH should be,** and fixed codes where references should be. The stock setting; check the first few lines of output.
- **Old-style values accepted without complaint.** A plain `"#ff0000"` or `"12px"` still builds, so a file can drift from the standard unnoticed.
- **Brand values taken on trust.** The reader's unused green and focus yellow would both have gone in as brand colours.
- **Meanings used as looks.** A page that asks for "ember" instead of "action background" can't be re-themed.

## Safety

- **Style Dictionary runs on the Mac** and sends nothing out.
- **The brand reader fetches the site from InspoAI's servers.** Use it on public sites only, never on anything private of Sean's.
- **Ask Sean** before buying an InspoAI plan, and before reusing a brand's typeface: reading a font's name off a site grants no right to use it.

## More details

- **Tested November 17, 2026,** in `designcraft-jobs/tests/design-values/` (outside every repo): `tokens/values.tokens.json`, `build.mjs`, output in `build/stock.css` and `build/values.css`; failure cases in `badtest/`.
- **Versions:** Style Dictionary 5.8.0 (Apache-2.0), Node 22.22.2. Its installed code lists the October 2025 colour spaces and converts the colour object; the OKLCH transform is named `color/oklch`.
- **The working transform list:** `attribute/cti, name/kebab, time/seconds, html/icon, size/rem, color/oklch, asset/url, fontFamily/css, cubicBezier/css`, plus the shorthand transforms for stroke style, border, typography, transition and shadow. That is the stock `css` group with `color/css` swapped for `color/oklch`.
- **The standard:** Design Tokens Format Module 2025.10 and its Color Module, read November 17, 2026 at designtokens.org. Files end `.tokens` or `.tokens.json`; dimensions are a number with a unit of `px` or `rem`; colour spaces include `oklch`, `display-p3` and 12 others; `hex` is an optional fallback; tools must support both curly-brace and `$ref` path references. A schema is served at designtokens.org/schemas/2025.10/format.json, though the standard's own text still calls a schema work in progress.
- **Style Dictionary's own statement** on partial support for 2025.10: styledictionary.com/info/dtcg, read November 17, 2026.
- **Brand reader test:** `extract_brand` on gov.uk, then computed styles read in the browser pane. Live button green `#0F7A52` on 4 elements; the reported `--primary-button-color: #00703c` exists in the stylesheet but colours no element; focus yellow `#FFDD00` on 0 elements at rest. The next InspoAI call returned: free plan, 5 calls a month, all used. Other helpers may have spent some of the five.
- **Not tested:** Terrazzo, Tailwind output from Style Dictionary, and the 2025.10 group inheritance features (`$extends`, `$root`).
