# Designcraft's tool list

The tools Designcraft uses, one pick per kind of work. Scouted on November 16, 2026 for today's best. Sean said yes to the list on November 17, with two changes of his own. Each tool gets a mastery guide in this folder before the lead uses it on a job.

The short version: nothing needs buying today, because almost everything is already on the Mac or is a free code library. One free thing was added on November 17: a checker that catches problems for people who see poorly or don't use a mouse. Mobbin, a library of real app screens, is covered too: Sean has it free for a year, and its connection is working.

Sean's rule from the other studios applies here: free tools now, a paid one only when a real job needs it, asked then.

## Words used here

- To **drive** a tool means the lead can work it directly, without Sean clicking for it. A tool the lead can only describe to Sean is worth much less.
- A **connection** is a plug that lets the lead drive an app from the session. Its technical name is in "More details".
- A **canvas** is a big board where many screens sit side by side, so Sean can look across them and point.
- **Design values** are the colours, type sizes and spacing of a design, kept in one file as named values and reused everywhere. Designers call them tokens.
- **OKLCH** is a way of writing a colour as lightness, strength and hue. Two colours with the same lightness number look equally light, which the older ways can't promise.
- **Contrast** is how clearly text stands out from what is behind it. The common rule asks for a ratio of at least 4.5 to 1 for body text.
- **Accessibility** means the design works for people who see poorly, or who use a keyboard or a screen reader.
- A **shader** is a small program that paints moving colour and light on the graphics chip.
- To **self-host** a typeface is to serve the font files from your own site, not from the maker's servers.

## The list

| Kind of work | The pick | Cost | Have it? | Sean's answer |
|---|---|---|---|---|
| Finding and studying great references | For websites: the Awwwards connection, which searches award-winning sites and shows them. For real app screens, user flows and website sections: Mobbin, searched by the lead through Mobbin's own connection. | Free. Sean has Mobbin free for a year. | Awwwards: yes, and search worked in a test. Mobbin: yes. Sean added its connection on November 17, and a test search returned real screens. | Mobbin: yes, November 17, 2026. "I have a subscription free for a year, so I'll add the MCP if it's not connected." The rest: yes, with the list. |
| Designing screens on a canvas Sean can react to | Claude Design: a canvas of live screens inside Claude, which the lead fills from the session. Sean opens it in the browser and points at what to change. | On the Claude plan | Yes. The lead reached it from this session. | Yes, November 17, 2026. "I also definitely want to master Claude Design, so we'll be using that over Paper." |
| Designing in real code | The lead writes the page itself, in plain web code, steered by the design skills already on the Mac, and Sean looks at it in the browser. When Devcraft will build in React, the same thing with React's common free building blocks, Tailwind and shadcn/ui. | On the Claude plan; the code libraries are free | Yes | Yes, with the list, November 17, 2026. |
| A design system | One file of design values in the standard format, turned into web code by Style Dictionary, with a plain page beside it that says how to use them. To start from an existing brand, the InspoAI connection reads that brand's live site first. | Free | The format and the brand reader: yes. Style Dictionary: no, free, added to the project that needs it. | Yes, with the list, November 17, 2026. |
| Type | Google Fonts, taken through Fontsource so the files are self-hosted, and Fontshare for more character. A paid foundry only for a brand that needs a face nobody else has. | Free. A foundry licence is paid once per job; prices not confirmed. | Yes, nothing to install | Yes, with the list, November 17, 2026. |
| Colour | Palettes written in OKLCH straight into the page, starting from the Radix Colors scales. Sean can see and nudge any colour in the free OKLCH picker. Contrast is measured by the checker below. | Free | Yes, nothing to install | Yes, with the list, November 17, 2026. |
| Pictures, illustration and icons | Borrowed from Motioncraft for pictures (GPT Image through Higgsfield) and illustration (the lead draws the vector, Affinity cleans it up). For icons: Lucide, with Iconify as the door to every other free set. | Pictures on the Higgsfield plan Sean pays for; icons free | Yes | Yes, with the list, November 17, 2026. |
| Spectacle on the web | Three.js for 3D and shaders, GSAP for motion tied to scroll and pointer, and Lenis for smooth scrolling, all written by the lead as code. Models come from Blender, which Motioncraft has. | Free | Yes. The skills for all three are on the Mac; the libraries are added per project. | Yes, with the list, November 17, 2026. |
| Presentations | Two kinds, the spectacle first. A spectacle: the deck built in code, as a web page with reveal.js or as a HyperFrames slideshow, using the same spectacle tools as the row above. A clear deck, fast: Claude Slides, which downloads as a PowerPoint or PDF file that Keynote opens. | reveal.js is free; HyperFrames is already Motioncraft's; Claude Slides is on the Claude plan | Claude Slides and HyperFrames: yes. reveal.js: free, added to the deck that needs it. | Yes, and he set the order, November 17, 2026. "I'd definitely prefer reveal.js and HyperFrames slideshows over Claude Slides. Those allow me to create spectacles and explore what's possible with presenting through code. If I need the clear deck, fast, then Claude Slides will do." |
| Checking a design before Sean sees it | Three checks, each catching what the others miss. The house screenshot checker, for desk and phone, day and night, and broken layouts. The Impeccable detector, for weak contrast and tired design habits. And axe-core, run through Playwright, for accessibility. | Free | The first two: yes, both tested. axe-core and Playwright: yes, installed and tested November 17, 2026. | "Yes, with install." November 17, 2026. |
| Showing Sean options side by side | A house Decide page with real screenshots of each option, desk and phone, and a link to each live version. | Free | Yes | Yes, with the list, November 17, 2026. |

## What is worth paying for, and when

Nothing today. These are the only paid tools that looked truly worth it, each for a named moment:

1. **Mobbin: already covered.** Sean has it free for a year, as he said on November 17, 2026. Its list price is $45 for three months or $120 for a year, which matters again when the free year ends. It lets the lead search more than 600,000 real product screens directly.
2. **A typeface licence from a foundry, paid once.** Only for a brand job where the free faces won't do. The price depends on the face and the use; none could be confirmed today.
3. **Figma Professional, $16 a month.** Only if a job has to be handed to someone who works in Figma.

Everything else on the "not now" list below can wait until a job proves the free pick falls short.

## Runners-up and not now

- **References:** Refero is Mobbin's closest rival and also lets the lead search it on its paid plan; its price could not be read today, and it has no free trial. InspoAI, already connected, finds websites but says it has no app screens. Godly now sends visitors to a newer free gallery called Recent, which is good for browsing by hand.
- **Canvas:** Paper is the close runner-up. Its canvas is made of real web code, the lead can read and write it, and the free plan allows 100 lead actions a week; the paid plan is $20 a month. Figma is the industry's standard and the lead can now draw in it, free while that feature is in testing. It only wins when someone else needs the file. Pencil is covered under "Things to know". Penpot is free and open, and the lead can draw in it too; it is the pick if Sean ever wants no company holding the files. Sketch is $12 a month or $120 once.
- **Real code:** v0 is free for 7 messages a day, then $30 a month. Subframe is free for one project, then $20 a month. Framer is free to start, then $10 or $30 a month. Google Stitch looked free, but its own pages would not load as text, so nothing about it is confirmed. All four make a first draft fast. None beat the lead writing the page with Sean's own skills and taste, and each adds a place where the design lives outside the repo.
- **Design system:** Terrazzo does the same job as Style Dictionary and is newer. Tokens Studio is built around Figma and costs €39 a month for the useful plan. Google's DESIGN.md format is a good shape for the plain page beside the values, and its free tool checks contrast, but Google still calls it an early version.
- **Type:** Adobe Fonts comes with a Creative Cloud plan, but its web fonts must load from Adobe, can't be self-hosted, and stop working when the plan ends. Pangram Pangram lets you try its faces free for personal work; anything commercial needs a paid licence.
- **Colour:** Harmonizer, from the makers of the OKLCH picker, builds whole palettes with even contrast. Leonardo, from Adobe, builds a palette from the contrast you want. Both are free and worth a try on the first colour job.
- **Icons:** Phosphor is the usual second choice; its main package was last updated in March 2024. Material Symbols and Iconoir are free and reachable through the InspoAI connection.
- **Spectacle:** Unicorn Studio makes shader scenes by hand in the browser. Its free plan is for non-commercial work and stamps its logo; the paid plan is $20 a month or $168 a year. Spline is a 3D editor in the browser, free with a logo stamp, with code export from $25 a month on yearly billing. Both are for when Sean wants to shape a scene by hand. Rive and Lottie, for small interactive animations, are on Motioncraft's list. A finished film or a rendered moving asset is Motioncraft's work, not Designcraft's.
- **Presentations:** Keynote is on the Mac and is the deck app to finish by hand; the lead can only drive it clumsily, through the Mac's scripting. Sean chose both reveal.js and the HyperFrames slideshow for spectacles: reveal.js is older, with a speaker view and PDF export built in, and HyperFrames is the one he already knows. Slidev is aimed at programmers' talks. Pitch is free to start, then €10 a month. Gamma makes a tidy deck from a prompt and the lead can drive it, but its decks look like everyone else's; its prices could not be read today.
- **Checking:** Lighthouse, from Google, gives a second score for accessibility and speed, and is free. Google's Chrome DevTools connection lets the lead poke at a live page; it reports how it is used back to Google unless switched off.
- **Side by side:** the picker skill already on the Mac builds several live versions and lets Sean flip between them, which is better than screenshots when the options move. The Claude Design canvas also shows options side by side.

## Things to know

- **Pencil is not worth reinstalling now.** It is a design canvas whose files live in the project folder beside the code, and the lead can drive it. Its leftover files on this Mac date from March and April 2026; the app is gone but its connection is still set up, so it fails at every start. It has since been renamed pen.dev. Its free plan allows 5 days a month of designing with an agent; the paid plan is $16 a month. It overlaps with Claude Design and Paper. Reinstall it only if Sean wants design files kept inside the repo. Either way, the dead connection is worth removing.
- **The Awwwards connection is not made by Awwwards.** It is a free package with no named author. Its own notes say "personal, non-commercial use". Search worked in a test today. Its page-study tools, which measure a site's colours, type and motion, failed: they needed Playwright placed beside the connection itself. That was repaired on November 17; see "More details".
- **The three checks really do catch different things.** Tested today on a throwaway page with three planted faults. The house screenshot checker took four pictures and caught the layout that was too wide for a phone. The Impeccable detector caught the faint grey text, measuring it at 1.8 to 1. Neither caught the button with no label, which is the kind of fault axe-core exists to find.
- **The house screenshot checker lives in the brain, not here.** It was built for the house pages. Designcraft needs its own copy that takes any page and any screen size. That is a small job for Devcraft.
- **axe-core, Lighthouse, Style Dictionary and reveal.js were not tested today.** Trying them means downloading them, which this scouting run was not allowed to do. The picks rest on their makers' pages and version records.
- **The Impeccable skill reports back to its maker by default.** Found today in the installed copy: its idea-dealing feature sends anonymous usage notes unless switched off. It says it never sends project names or code. The switch is in "More details".
- **Claude Design keeps the design on Anthropic's servers.** A design made there is private until Sean shares it. Design work counts toward the Claude plan's usage, and a full deck uses more of it.
- **Paper, Figma, Mobbin, InspoAI and Gamma all hold what you make or search on their own servers.** Paper's pages do not say where files are kept. Pencil and Penpot are the two canvases that can keep files on the Mac.
- **Figma's free plan allows the lead only 20 look-ups a month.** Drawing is not counted for now, but Figma says it will be charged by use later.
- **InspoAI's brand reader is a rough first pass.** Tested today on one public site: it found the logo and ranked the colours by use, but found no fonts and guessed an odd text colour. The lead checks its answer against the live site. Which InspoAI plan Sean is on, and its price, could not be confirmed.
- **Fontshare's faces are free for commercial work but are not open.** Its maker says so. That matters here: the font files should not be saved into this public repo, because that would be handing them out. The faces Fontsource packages are open-source, so those can be.
- **Loading fonts from Google tells Google about each visit.** Fontsource's own page says Google tracks the use of its fonts. Fontsource avoids that by packaging the same faces for self-hosting.
- **GSAP is free, including the parts that used to be paid, but it is not open.** Webflow owns it and can change the terms for later versions. Its licence bars using it to build a rival to Webflow's own animation tool, which does not touch this work.
- **The Rive connection only works while the Rive app is open.** It failed today, most likely because the app was closed.
- **Adobe needs a sign-in before the lead can use it.** Whether Sean's Adobe plan is active, and so whether Adobe Fonts is on hand, could not be checked.
- **Prices move monthly.** The lead reads the price page at the start of a job and never works from memory.

## Design skills already on the Mac

These steer the lead's taste. They are not tools to buy, and several overlap.

- **Impeccable:** the widest one. Designs, critiques and polishes any screen, and carries the detector used above.
- **Design taste for the front end:** art direction for websites, drawn from a study of gallery sites, with a look-and-fix loop on screenshots.
- **Front-end design:** a general skill for building polished pages, from Claude's official plugin list.
- **Emil's design engineering:** the small details and motion choices that make software feel finished.
- **Apple design:** Apple's approach to motion, touch and type, translated for the web.
- **High-end visual design, minimalist and brutalist:** three fixed house styles to reach for by name.
- **Redesign existing projects:** audits a page already built and lifts it without breaking it.
- **Image to code, and the two image-direction skills:** make a picture of the design first, then build to match it.
- **The picker skill:** builds several live versions behind a switch so Sean can flip between them.
- **Wince:** Sean's own skill for drawing his visual taste out by showing options.
- **The Three.js, shader and scroll skills:** how-to for the spectacle row.

## More details

**The technical name for a connection** is an MCP server. Connected on this Mac on November 16, 2026: Awwwards (`awwwards-mcp` 1.19.0; 1.20.0 came out the same day), InspoAI, Context7, Higgsfield. Configured but failing: Pencil (app missing), Rive (app closed). Adobe needs a sign-in.

**Checked on this Mac, November 16, 2026, read-only.** Installed: Keynote 14.5 (it has a scripting dictionary), Affinity 3.3.3, Rive Early Access 0.9.560, Google Chrome 157, Screen Studio, Blender, Node 22, Homebrew, uv, ffmpeg. The Creative Cloud launcher is installed with Photoshop support files; no Adobe app is in the Applications folder. Not installed: Figma, Paper, Pencil, Sketch, Playwright, Lighthouse, axe, Style Dictionary, Slidev, the HyperFrames command.

**Tested today, with nothing installed, signed up for or uploaded:**

- The house screenshot checker (`shoot.mjs`, taken from the brain's main branch) on a throwaway page: 4 screenshots, sideways scroll reported on the phone size, exit code 1.
- The Impeccable detector (`impeccable detect <file>`) on the same page: `low-contrast` at 1.8:1 and one style finding. `impeccable telemetry status` reported telemetry on; `impeccable telemetry off` or `DO_NOT_TRACK=1` turns it off.
- Awwwards: `get_index_stats` returned 3,023 cached sites. `export_design_tokens` failed with "Cannot find package 'playwright'".
- InspoAI: `find_website_inspiration`, `search_icons` and `extract_brand` all returned results.
- Claude's Artifact tool: the read-only quickstart for a design and for slides returned the Design, Slides and Design System types. No artifact was created.
- A test install of Playwright and axe-core into a scratch folder was refused by the session's permission rules, so it was not run.

**The install, November 17, 2026, after Sean's yes.** Playwright 1.65.1 and `@axe-core/playwright` 4.14.0 went into a tools folder beside Designcraft's jobs, outside every repo. No browser was downloaded: the checker drives the Google Chrome already on the Mac. A short script, `axe_check.mjs`, runs it on a page or a link, at desk or phone size, day or night. Tested the same day:

- A page with four planted faults: all four caught (a button with no name, a picture with no description, a form field with no label, faint grey text).
- A clean page: nothing found.
- One of Sean's own review pages, at desk size by day and phone size by night: nothing found.

**The award-site tools, repaired November 17, 2026, after a second yes.** The list said the first install would also repair the Awwwards connection's page-study tools. It did not: that connection ran from its own sealed copy, which cannot see a Playwright installed anywhere else. Sean said yes to the bigger repair, and it was done the way the connection's own instructions ask:

- The connection (version 1.19.0, the one already in use), Playwright 1.65.1 and `ffmpeg-static` 5.3.0 were installed system-wide, side by side.
- Playwright downloaded its own test browser, about 100 megabytes.
- Sean's Claude settings now start the installed copy instead of fetching one each time. A copy of the settings from before the change was kept. Sessions opened before the change keep the old copy until they are restarted.

Tested by calling the installed copy directly:

- A plain test page: measured, with a real browser.
- Lando Norris's site: the scroll tool ran and agreed with the shelf entry on the page's height and its 0.75 second motion curve. It did not find the site's scroll triggers, which are packed inside the site's code where it cannot reach.
- Raphael Segerman's site: the tools ran but saw little. The whole site is drawn on one 3D surface, so they report one band and almost no hover rules. One tool measured the loading count, not the page. Its default wait never finished, because the site keeps streaming clips; the shorter wait works.

What that means: these tools read ordinary pages well and 3D sites poorly. For a site drawn on a 3D surface, the lead's own measuring scripts still see more.

One side effect: Playwright cleared an older test browser that another Playwright tool on this Mac had downloaded. That tool will fetch its browser again the next time it runs.

**Mobbin's connection, checked November 17, 2026.** Mobbin's own page gives the address `https://api.mobbin.com/mcp`, with a sign-in in the browser, on its Pro, Team and Enterprise plans. It offers three searches: single screens, step-by-step flows, and website sections such as a hero or a pricing block. It can also read and write Sean's saved collections. Mobbin's guide says the simplest way in is to add its connector in the Claude app's own connector list, signed in to the same Claude account. Sean added it later the same day, and a test search for a wallet app's home screen returned two real screens with their pictures. An older package called `mobbin-mcp` is not Mobbin's and is no longer kept up.

**Free things that needed Sean's yes because they install something:** Playwright with `@axe-core/playwright`, and the system-wide install that repairs the Awwwards page-study tools. Both are done. Everything else in the list is either already here or a library added inside the one project that uses it: Style Dictionary, Fontsource packages, Lucide, Three.js, GSAP, Lenis, reveal.js.

**Versions and licences, from the package registry on November 16, 2026:** Playwright 1.65.1 (Apache-2.0), axe-core for Playwright 4.14.0 (MPL-2.0), Lighthouse 13.6.0 (Apache-2.0), Chrome DevTools MCP 1.13.0 (Apache-2.0), Style Dictionary 5.8.0 (Apache-2.0), Terrazzo CLI 2.10.0 (MIT), Google's DESIGN.md tool 0.4.0, Three.js 0.187.0 (MIT), React Three Fiber 9.8.2 (MIT), GSAP 3.15.1 (Webflow's no-charge licence), Lenis 1.3.27 (MIT), Motion 14.14.0 (MIT), reveal.js 6.0.2 (MIT), Slidev 53.1.0 (MIT), Lucide 1.73.0 (ISC), Phosphor core 2.1.1 (MIT), Iconify's icon data (MIT tooling; each set has its own licence), Impeccable 4.9.2 (Apache-2.0). The design values format is the Design Tokens Community Group's, first stable version 2025.10.

**Prices as read today.** Figma: Starter free, Professional $16 a month for one full licence, 3,000 AI credits a month. Paper: free, or $20 a month ($16 on yearly billing). pen.dev: free, $16 or $48 a month. Penpot: free, or $7 a month. Sketch: $12 a month on yearly billing, or $120 once for the Mac-only licence. Subframe: free, or $20 a month. v0: free, $30 or $100 a month. Framer: free, $10 or $30 a month. Mobbin: $10 a month yearly or $15 a month quarterly. Tokens Studio: free, or €39 a month on yearly billing. Spline: free, $15, $30 or $70 a month. Unicorn Studio: free, or $20 a month. Pitch: free, or €10 a month on yearly billing. Claude: Design, Slides and Docs are in every plan.

**Could not be confirmed on November 16, 2026:**

- Refero's price and library size (its pages would not load as text; its help pages confirm the lead can search it only on a paid plan).
- InspoAI's prices and Sean's plan. Its own blog gives $12 a month for the solo plan.
- Google Stitch's limits, price and connection.
- Gamma's prices. Other sites give about $12 and $25 a month.
- The exact text of Fontshare's licence, and Google Fonts' own licence page. The Fontshare claim above comes from its maker's launch post.
- Any foundry's licence price.
- Adobe's font terms at first hand. Adobe's help page refused a direct read, so the Adobe Fonts facts above come from search results quoting that page.
- Figma's free-plan limits on files and pages.
- How the `/design` command behaves inside Claude Code. It is described on Anthropic's product page; only the Artifact route was checked here.
- Whether Keynote's newer paid extras matter for decks.

**Sources:** each tool's own site, documents and pricing page, read November 16, 2026: Figma (pricing and its MCP documents), Paper, pen.dev, Claude (design and pricing pages), Penpot, Sketch, Subframe, v0, Framer, Mobbin, Refero's help pages, Recent, Tokens Studio, the Design Tokens Community Group, Google's DESIGN.md repository, Style Dictionary, Fontsource, Indian Type Foundry (Fontshare's maker), Adobe's web-font licensing help, the OKLCH picker, Radix Colors, Lucide, GSAP's licence, Spline, Unicorn Studio, reveal.js, Pitch, Gamma's developer pages, shadcn/ui, Chrome DevTools MCP, and the npm registry for versions and licences.
