# Designing in code

The lead often designs by writing the page itself: real web code that Sean opens in his browser, scrolls and resizes. This guide covers the two ways to do it, which design skills to lean on, how to stay honest to a reference, and how to hand the work on. Read it before the first coded screen of any job.

**Plain web code** is one HTML file with hand-written styles. **React** builds web apps from reusable parts. **Tailwind** styles each element with short class names. **shadcn/ui** is a set of ready-made parts (buttons, menus, switches) copied into the project as code the project owns.

## The same screen, built both ways

One small screen, built twice on November 17, 2026: a page for booking a rehearsal room, with three room choices, two drop-down menus, an on-off switch and a booking summary with a total and a button. Same words, same colours, same typeface. Both were screenshotted at desk width (1280 pixels) and phone width (375 pixels) in the browser pane.

| | Plain web code | React, Tailwind and shadcn/ui |
|---|---|---|
| Setup | One typeface package. | One command made the project in about 20 seconds; six parts added in one more. |
| What it took on disk | Under 1 megabyte. | 263 megabytes of packages, seven part files (478 lines) copied in. |
| The screen itself | One file, 106 lines. | 125 lines, plus the part files. |
| Rounds of fixes to match the intended look | None. | Three. |
| What the visitor downloads | No script at all. | 370 kilobytes of script (119 compressed). |

**What each looked like.** The plain page came out as intended on the first look, at both widths.

The shadcn version came out in the kit's own look first: neutral greys, its default typeface, and small, dense controls built for a desk app. The menus were 32 pixels tall, the switch 18, the round choice buttons 16. Wrapped description lines had no space between them. It read as a starter kit, not as anyone's product.

Swapping in the job's own colours, typeface and corner sizes took one edit to one block of values. Three things then fought back:

- **The switch kept its small size.** Changing it from outside lost to the part's own size rules. It took an edit inside the part file, which is the shadcn way: you own the file.
- **On the phone, the date menu's text ran over the menu beside it.** Its text was set never to wrap, with nothing to trim it. A plain browser menu trims itself.
- **The cramped description lines** needed their spacing set by hand.

After those fixes the two looked nearly the same, except that the shadcn cards keep a visible round button.

**What both showed on the phone.** The total and the button fell below the first screen on a phone, under the whole form. Neither route caught that; looking at phone width did. The fix is a design decision, such as a bar fixed to the bottom of the screen with the total and the button.

## What it's best at

- **Anything that behaves.** Scroll stories, reveals, real hover and focus states, a layout that reflows from desk to phone. Sean's love of scroll effects lives here.
- **Being measured.** A coded page goes through the three checkers.
- **Plain code for the look; React when Devcraft will build in React.** Plain code is faster to shape and has nothing to fight. The React route earns its weight when the design must arrive as parts a builder will keep.

Where another tool beats it: **Claude Design** wins early, when Sean needs several directions side by side to point at, or wants to nudge a colour himself. Code wins once the thing moves, scrolls or reflows, and whenever the page itself is the deliverable. A **finished film** is Motioncraft's.

## Setup

- **Plain web code:** nothing to install. Typefaces come from Fontsource as a small package, so the files are served from the project.
- **React route:** Node is on the Mac. The one command that makes the project and proves it works, from an empty test folder:

```bash
npx shadcn@latest init -t vite -n my-screen -b radix -p nova --no-monorepo
```

It ends with "Project initialization completed." Then `npx shadcn add card switch select` copies in parts, and `npm run build` must finish with no errors. Without `-p`, the command stops to ask which of nine looks to start from; Nova pairs Lucide icons with the Geist typeface.

- **Cost:** free. Each package is open source.

## Which design skill to load for what

The skills disagree with each other in places, so load the one that fits the surface, not all of them.

| The surface | Load | What it brings |
|---|---|---|
| Any screen, any stage | Impeccable | The widest craft: modes for persuading, working, reading and showing off, plus the detector that runs after each edit. |
| A public web page | Design taste for the front end | Art direction from a study of gallery sites, measured house rules, screenshots at three widths. Not for app screens. |
| A new look with no brief | Front-end design | Ground the look in the subject's own world; spend boldness in one place. |
| How it feels to touch | Emil's design engineering | Timing, easing, press feedback, interrupting an animation midway. |
| Gestures and depth | Apple design | Springs, drag and fling, see-through layers, type that changes shape with size. |
| A named house style | High-end visual design, minimalist, brutalist | Fixed looks to reach for by name only. |
| A page that already exists | Redesign existing projects | Lifts the look without breaking what works. |
| Comparing options | The picker skill | Several versions behind one switch on the real page. |

Two disagreements met in testing. The Impeccable detector flagged the plain page for using one typeface throughout, while the gallery-site skill calls one family normal and two the limit. And the high-end skill bans Lucide's default icons outright. The brief and the reference settle such fights, not the louder skill.

## Getting the best out of it

**Values first, then layout, then everything else.** Colours, type sizes and spacing go in as named values at the top, and everything below uses only those names. That one habit made the shadcn re-theme a single edit. It also means a change of look touches one place.

**Real words at real lengths, at both widths, early.** The phone overflow only appeared with the real date text in place.

**Theme the parts nobody draws.** Text selection, focus rings, scrollbars and the numbers in a table all ship with browser defaults. Setting them from the palette is the cheapest sign a page was built, not assembled.

**One bold place.** One element carries the page; the rest stays quiet. Then remove one thing.

**Motion that answers a person.** A press that gives under the finger, a menu that opens from where it was clicked; never the same fade-in on every section.

**With shadcn, edit the part, don't fight it.** A part that resists from outside is telling you to change its file. That is what owning the code is for.

An example of the difference: the stock shadcn screen and the re-themed one have identical layout code. The stock one looks like a starter kit; the re-themed one looks like a booking page for a real room. The difference is about 20 values and three part fixes.

## Keeping a coded design honest to a reference

- **Measure the reference, then build to the numbers.** Read its type sizes, spacing, line lengths and colours off the live page, not from memory or a screenshot's impression.
- **Put the two side by side at the same width,** desk and phone, and look for the gap in scale first. Scale is what drifts most: a build usually comes out with its big things too small and its small things too big.
- **Copy the decisions, never the work.** Take the proportions and the logic; the words, pictures and drawn assets stay the job's own.
- **Check the states a screenshot never shows:** hover, focus, empty, error, a long name.

## Handing it to Devcraft

The design is the running code itself, not a picture of it. A good hand-off holds:

- **The coded screen,** running, with every state shown.
- **The file of design values** it reads from, so nothing is re-typed.
- **Screenshots at desk and phone width,** the target the build must match.
- **A short list of what must not change** and what is free: the scale and spacing, say, are fixed; the data plumbing is Devcraft's call.

If Devcraft will build in React, hand over the shadcn version, part files included, so the builder starts from the parts the design already proved.

## Where it goes wrong

- **The kit's look leaks through.** Default grey, default typeface, default dense controls. Spot it by asking whether the screen could belong to any other product.
- **Controls too small for a thumb.** The Nova look's controls suit a desk, not a phone. Measure on the phone.
- **Text that never wraps** runs over its neighbour at phone width. Test the longest real value.
- **A pile of overrides.** When the class list grows long fighting a part, change the part's file instead.

## Safety

- **Nothing is uploaded.** Both routes run on the Mac; the browser pane reads the page on this machine only.
- **Installs stay in the job's folder.** The packages go into the one project, never system-wide.
- **Fonts loaded from Google's servers** tell Google about each visit; Fontsource avoids that.
- **Ask Sean first** before a coded design of his own work is published anywhere.

## More details

- **Tested November 17, 2026,** in a scratch folder outside every repo (`designcraft-jobs/tests/designing-in-code/`): `plain/index.html` and `shadcn-screen/`, with screenshots in `screenshots/`. Served on 127.0.0.1 and captured with the browser pane at 1280 by 820 and at its 375 by 812 phone size.
- **Versions used:** shadcn CLI 4.23.0, Tailwind 4 (through `@tailwindcss/vite`), Vite 8, React 19.3, TypeScript 6.0, `radix-ui` 1.8.1, `lucide-react` 1.74.0, Bricolage Grotesque from Fontsource. Node 22.22.2.
- **Measured in the stock Nova look,** on the phone: menu triggers 32 px tall, switch 32 by 18.4 px, radio 16 px, wrapped description at 14 px size with 14 px line height. The fixes: switch size changed inside `switch.tsx`; menu text given `min-w-0` and truncation; description spacing set by hand.
- **The init command's options** (`-t`, `-b`, `-p`, `--no-monorepo`) and the nine looks (Nova, Vega, Maia, Lyra, Mira, Luma, Sera, Rhea, Custom) come from `shadcn init --help` and its own prompt. It also offers Base UI and React Aria as the base under the parts.
- **The skills** were read from their own files on this Mac: Impeccable 4.8.0 and its craft-floor page, design-taste-frontend v2, front-end design 1.1.1, emil-design-eng, apple-design, high-end-visual-design, minimalist-ui, industrial-brutalist-ui, redesign-existing-projects, prototype (the picker). The detector finding (`single-font`) came from Impeccable's hook during the test.
- **Not tested:** the shadcn MCP connection, the Base UI and React Aria bases, and Claude Design on this screen.
