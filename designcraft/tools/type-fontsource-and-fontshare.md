# Type: Fontsource, Fontshare, and a foundry when it counts

This guide is about getting typefaces into a page well: where the files come from, how they load without the words jumping about, and what each licence allows. Read it before you load any typeface for a job. Choosing the face is a craft question for the type brief; this page starts once the face is chosen.

## What each is best at

- **Fontsource is the default.** It packages the whole Google Fonts catalogue, and other open faces, so the font files ship inside the site. To self-host is to serve the fonts from your own site, not from the maker's servers. That brings four gains: no visit is reported to Google, the font can't change under you when Google updates it, it works offline, and there is no extra server to reach before the text appears.
- **Fontshare is for more character.** It is the free library of the Indian Type Foundry: 100 families today, with faces like Satoshi, General Sans and Clash Display. Reach for it when the Google catalogue reads too familiar for the brief. Of the 100, 64 are under the foundry's own free licence and 36 are open faces, most of them also on Google Fonts.
- **A paid foundry only when a brand needs a face nobody else has.** The licence is paid once per job and depends on the face and the use. It is always Sean's call.

Where something else wins:

- **The Mac's own system fonts** beat any download for a working tool, where speed matters and character doesn't.
- **Adobe Fonts** comes with a Creative Cloud plan, but its web fonts must load from Adobe, can't be self-hosted, and stop when the plan ends. Use it only for a job that will live on Adobe's terms.

## Setup

- **Nothing to sign up for.** Fontsource is one package per face, added to the job's project and imported in the page's code. A variable face lives under its own name: the variable Fraunces is `@fontsource-variable/fraunces`, and its family name in CSS is "Fraunces Variable", not "Fraunces".
- **Fontshare has no package.** It offers a link to a stylesheet on its own server. Downloading its files by hand works too, but see Safety before you do.
- **The one check that proves it works** runs in the browser's console on the finished page:

```js
[...new Set(performance.getEntriesByType('resource').map(r => new URL(r.name).host))]
```

It lists every server the page fetched from. With the fonts self-hosted, it lists only the site's own address. In the test it returned one address, the local one, and both fonts were loaded.

## Getting the best out of it

**Pick the variable file for the axes you will use.** A variable font holds every weight in one file, and some faces carry more axes: optical size, width, softness. An axis is one dial the font can turn. Fontsource's plain import carries only weight. Fraunces shows what the others cost. Its Latin file with weight alone is 37 kilobytes. With optical size added it is 67. With every axis it is 121. Only one set of axes can be imported per face, so decide before you build.

**Use optical size when the face has it.** Optical size redraws the letters for the size they are set at. Small sizes get sturdier strokes and looser spacing; headline sizes get finer detail and tighter fit. In the test page, the same Fraunces file gave a sharp, high-contrast headline at size 144 and a plain, readable caption at size 9. That is two typefaces' worth of range from one download.

**Let the browser fetch only the alphabets the page uses.** Fontsource already cuts each face into parts by alphabet: Latin, extended Latin, Vietnamese, Cyrillic and so on. The browser downloads only the parts the page's own characters need. The test build produced ten font files; the browser fetched two. A stray character from another alphabet pulls in one more file, which is worth knowing when copy comes pasted from elsewhere.

**Show text at once, and decide what happens when the font is late.** Fontsource sets each face to "swap": the text appears straight away in a fallback face, and changes over when the real font arrives. That is right for a display face that is the brand. The other choice, "optional", uses the web font only if it arrives almost at once and otherwise keeps the fallback for that visit. It suits body text on slow phones, where a late change helps nobody. Both are settings on the font, called font-display.

**Stretch the fallback to the web font's size.** This is the move that stops the page jumping. CSS can resize a font already on the visitor's machine, such as Arial or Times, so it takes the same width and line height as the web font. Lines then break in the same places, and nothing moves when the real font lands. The free Capsize library works out the numbers from published font measurements.

The test, with the fonts held back for a second and a half:

- **Body text with no matched fallback:** the paragraph grew from 82 to 109 pixels tall when the real font arrived, and everything below it jumped 27 pixels.
- **Body text with a matched Arial fallback:** 109 pixels before and after. Nothing moved.

**Give each role its own fallback.** The same test caught a trap. One fallback for Fraunces made the headline worse, not better. The headline was set heavy, tight and at the largest optical size, which is far narrower than the font's ordinary setting that the measurements describe. Its stretched fallback wrapped onto three lines, then snapped to two when the real font arrived: a 68 pixel jump, worse than no fallback at all. A second fallback just for the headline, measured from the headline's own settings, held it still. At phone width the medium-sized lead paragraph still lost a line when the real font arrived, and everything below it moved 30 pixels. Matching works on averages; a single line break can still land differently. Measure at desk and phone widths with the fonts held back.

**Preload only the file the first screen needs.** Preloading tells the browser to fetch a file before it finds out it needs it. Preload the Latin file of the headline face, and nothing else. Fontsource's own guide warns that preloading every file slows the first view. The build tool renames font files, and in the test it rewrote the preload link to the new name by itself.

**Load italics on purpose.** Fontsource keeps italics in their own file and their own import. If the design uses them, import them; if it doesn't, leave them out and save the weight.

## Where it goes wrong

- **A family name that doesn't match.** Writing "Fraunces" when the package names it "Fraunces Variable" gives the fallback face everywhere, with no error. Check the loaded fonts in the browser, not the CSS.
- **One fallback stretched for the wrong setting.** Shown above. The tell is a headline that changes its line count as the page settles.
- **A Google Fonts link left in by a starter page or a skill.** It works, and it quietly reports every visit to Google. The console check above catches it.
- **Every axis loaded for one weight.** The full Fraunces file is more than three times the weight-only one. Ask which dials the design really turns.
- **Fontshare's files committed to the repo.** See Safety.
- **A face that looks right in the design but has no characters for the copy.** Accented names and other alphabets fall back mid-word. Check the face covers the real text, not just the sample sentence.

## Safety

- **What each licence allows.**
  - The faces Fontsource packages are open, most under the SIL Open Font License. Each package carries its licence file. Their files can be saved into this public repo and shipped with any site.
  - Fontshare's foundry licence is free for commercial work but is not open. Its 64 faces under that licence must never be saved into this public repo, because that would be handing the files out. Whether the licence allows serving those files from Sean's own site was not confirmed; until it is, use Fontshare's own link, and ask Sean before self-hosting one.
  - Fontshare's 36 open faces are safe, but take them from Fontsource instead, so every font in a project comes the same way.
  - A foundry licence costs money and has its own terms: ask Sean first, every time.
- **What loading from someone else's server tells them.** Fontsource's own pages say Google tracks the use of its fonts. In 2022 a court in Munich ruled that a site loading Google Fonts had passed the visitor's internet address to Google without consent, and ordered 100 euros in damages. Fontshare's link has the same shape: its server sees each visit. Self-hosted open fonts tell nobody.
- **Cost:** nothing, unless a foundry face is needed.

## More details

- **Tested November 17, 2026,** in a scratch project at `designcraft-jobs/tests/type-colour-spectacle/` (outside every repo), built with Vite 8.3.8 and served on this Mac:
  - `@fontsource-variable/fraunces` 5.3.0 (font version v38, OFL-1.1; axes opsz, wght, SOFT, WONK) and `@fontsource-variable/inter` 5.3.0.
  - Latin file sizes for Fraunces: `wght` 36,620 bytes, `opsz` 67,304, `full` 121,016.
  - The browser pane's network list showed `type.html`, its CSS and script, and two font files, all from `localhost:4317`. `document.fonts` reported both variable faces loaded. No request went to Google.
  - The build produced ten `.woff2` files (Latin, Latin Extended, Vietnamese, and Inter's Cyrillic and Greek parts); the browser fetched the two Latin ones.
  - Vite rewrote `<link rel="preload" href="/node_modules/.../fraunces-latin-opsz-normal.woff2">` to the hashed file in `dist/assets/`.
  - Fallbacks from `@capsizecss/core` 4.1.3 `createFontStack` with `@capsizecss/metrics` 4.4.0: Inter over Arial at `size-adjust: 107.1194%`; Fraunces over Times New Roman at `115.4462%`. The headline fallback, measured in the browser at `opsz 144`, weight 650 and `-0.02em` tracking against Times New Roman Bold, came to 91.9%.
  - Layout shift measured with Playwright 1.65.1 driving the Mac's Chrome, with every `.woff2` delayed 1,500 ms, at 1440 and 390 pixels wide. Scripts: `scripts/cls.mjs` and `scripts/blocks.mjs` in the scratch project.
- **Fontshare, read November 17, 2026:** its public listing at `api.fontshare.com/v2/fonts` returned 100 families, 64 with `license_type` `itf_ffl` and 36 with `sil_ofl`. Its stylesheet link (`api.fontshare.com/v2/css?f[]=satoshi@1&display=swap`) serves Satoshi as a 300 to 900 weight face from `cdn.fontshare.com` with `font-display: swap`.
- **Adobe Fonts:** the terms above are carried over from the tool list, which took them from search results quoting Adobe's help page; they were not re-read today.
- **Not confirmed:** the text of Fontshare's own licence, which neither its licence page nor its FAQ would show as text. That it is free for commercial use but closed and not to be redistributed comes from its maker's launch post (as `choices.md` records) and from secondary summaries. Whether it allows self-hosting on your own site is unknown.
- **Sources, read November 17, 2026:** Fontsource's introduction (https://fontsource.org/docs/getting-started/introduction), variable fonts guide (https://fontsource.org/docs/getting-started/variable) and preloading guide (https://fontsource.org/docs/getting-started/preload); the Fraunces package README and licence; the Munich ruling, LG München I, 20 January 2022, 3 O 17493/20, as summarised by the Bergisch chamber of commerce (https://www.ihk.de/bergische/recht-und-steuern/wettbewerbsrecht/google-fonts-5646176).
