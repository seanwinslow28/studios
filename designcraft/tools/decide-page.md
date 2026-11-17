# Showing Sean options on a Decide page

When Sean has to choose between design options, he gets a house Decide page: one page, one question, a real screenshot of each option at desk and phone size, and a link to each live version. Read this before putting options in front of him, and before choosing between a Decide page, the picker skill and the Claude Design canvas.

## What it's best at, and when something else wins

A Decide page is for a **ruling**: Sean looks, picks, and copies one plain line back into the chat. It shows the lead's pick and why, always offers "I can't tell", and packs into one file that opens from disk or on a phone. It is the house pattern for every checkpoint, so Sean already knows how to read it.

Two other ways to show options beat it in their own cases:

- **The picker skill, when the options move.** It builds three to five working versions behind a small switch, one at a time at full size, and Sean flips between them live. A screenshot can't show a scroll effect, a hover or a page change, and Sean is "a sucker for scroll effects and reveals". When the difference between options is in the motion, the picker shows it and the Decide page can only describe it. Its own rules warn that side-by-side thumbnails distort spacing and scale. It runs only when Sean calls it himself, so the lead offers it and he starts it.
- **The Claude Design canvas, when there are many screens or the direction is still loose.** A canvas puts many live screens side by side on one board, and Sean points at what to change. That wins early, when he is reacting rather than ruling, and when the options are whole sets of screens. The canvas keeps the design on Anthropic's servers and counts toward the Claude plan's usage. It was not tried for this guide.

A good rhythm is to explore on the canvas or the picker, then put the two or three survivors on a Decide page for the ruling. The ruling is what gets recorded.

## Setup

The house kit lives in the brain, on its main branch: a page template, a packer that turns one small content file into a single page, and the screenshot checker. The house page guide's section on Decide pages sets the order of everything on the page. The craftwork guide on review pages says the page is named `review-<what>.html` and kept in the job's folder.

The packer reads its content from inside the brain's own folder and writes the page into the brain's hidden runtime folder. For a Designcraft job, work from a copy of the template and the packer in the job's folder, so nothing lands in the brain. That is how the test below was run.

The command that proves it works, run beside the copied packer with a content folder named after the page:

```bash
python3 build_page.py portfolio-first-screen --out out/review-first-screen.html
```

It prints the page's path and size: 193 kilobytes for two options with their pictures. Then the screenshot checker photographs the finished page at desk and phone size, day and night, and must come back clean.

## The test: two first screens for Sean's portfolio

On November 17, 2026 two stand-in first screens were built for Sean's portfolio and put on a Decide page. One was a single still screen in three columns, after Segerman's site. The other was a long scroll with a huge name and one project per screen, after Lando Norris's. Each was photographed at desk and phone size, packed, and the page itself photographed.

**The first try broke.** Four pictures, desk and phone for each option, went into the page's picture row. The row holds at most three across, so three sat in a row and the fourth dropped alone onto a second line. The pairs came apart. Desk and phone pictures also got the same width, so the phone pictures stood more than three times taller than the desk ones. The screenshot checker passed it: the page had no errors and fit the phone. Only looking at the pictures showed it.

**The crop was wrong too.** The option pictures were full-length, and the long scroll's was three screens tall, so they were cut down to the first screen. The cropping tool took the middle of each picture, not the top. The long-scroll option showed "Project one" instead of the name.

**The fix that worked:** one picture per option, desk on the left and phone on the right, each cut from the top to its first screen. Two options then sat side by side on a laptop and one above the other on a phone, by day and by night, and the checker came back clean.

## Getting the pictures right

- **Real screenshots of the real build.** Taken by the screenshot checker from the running page, not mock-ups or generated pictures. Sean judges the thing itself.
- **One picture per option, holding both sizes.** Desk and phone side by side in one image keeps each option together and lets the page show options across. The phone half comes out small, so the link to the live version matters more.
- **The same moment in every option.** First screen against first screen, the same content, the same day or night. A full-length picture of a long page shrinks to a thin strip; show the first screen, and a second picture of the key moment if the option has one.
- **Cut from the top, and check the cut.** Look at each picture before packing.
- **Label by what each option is.** "A. One still screen", not "Option 1". The tag sits over each picture and the same words start each answer.
- **Describe each picture in its alt text,** a short plain line of what is in it, for the Listen button and for a screen reader.

## Links to the live versions

The page puts links on its "what to look for" lines, one per line, and on its text cards. The pictures themselves don't link.

- **Only web links survive.** The template keeps links that start with http or https and silently drops the rest. A link to a file on the Mac vanishes with no warning.
- **A link to this Mac works only on this Mac.** A page served from the Mac opens at his desk, not on his phone or anywhere else. To open on the phone, the live version has to be online somewhere, and putting it online, even as a private Claude page, uploads the work: ask Sean first, unless the job already agreed it.
- **Say what to do on the live page.** "Scroll slowly past the name" tells him where the difference is. A picture shows the look; the link shows the motion.

## Making options truly contrast

Options that differ only in colour or wording waste Sean's time: flipping between them teaches him nothing, and he ends up choosing a tint.

- **Give each option one axis of its own.** An axis is the single way it differs: the layout, the story the scroll tells, the density, the mood, how it moves. If two options would share the same answer on every axis, they are one option. In the test the axis was how the page tells the story: everything at once, or one project per screen.
- **Name each in a phrase that rules the other out.** "One still screen" and "a long scroll" can't both be true. "Clean" and "modern" can.
- **Keep everything else the same.** Same name, same projects, same pictures, same quality. The only thing Sean should see changing is the axis.
- **Make every option one the lead would defend.** A weak option planted to make the pick look good is a foil, and Sean will see through it.
- **Two to four options.** Two when the choice is a fork, three when the space is wide, never more than four. The page lays out three across at most.
- **Pull contrast from the shelf.** The shelf runs from pole to opposite: Segerman's quiet first layer against Lando's loud long scroll, Poor Charlie's calm against Igloo's spectacle. A job that names no look starts with two or three contrasting entries from it.
- **Tie the pick to Sean's own words.** The test page's pick, the long scroll, quoted his line about scrolling telling the story. A pick with no reason is just the lead's taste.

## Where it goes wrong

- **More than three pictures** break the row, as the test showed.
- **A clean screenshot check is not a good page.** It catches errors and sideways scroll, not pairs that came apart or a crop that missed the point.
- **Options that move, shown as stills.** If the difference is the motion, use the picker, or at least link each live version and say where to look.
- **A page that asks two things.** One question per page. A second choice gets its own page.
- **Writing the page by hand.** The page is the template plus one content file. A new layout for the template is a change to the house look and needs Sean's yes.

## Safety

- **Nothing is sent by the page.** Copy my answer puts one line on the clipboard; Sean pastes it.
- **The page loads its fonts from Google,** which tells Google about the visit; offline it falls back to the Mac's own fonts.
- **Packing it is safe; putting it online is not automatic.** Showing it as a private Claude page, or hosting a live version, uploads the work. Ask Sean first.
- **The Listen clip** is rendered on the Mac into iCloud, never into a repo.

## More details

- **Kit, read November 17, 2026, from the brain's main branch:** `docs/prototypes/house-look/decide.html`, `build_page.py` and `tools/shoot.mjs`; the house guide `docs/pages/DESIGN.md`, section 9; the craftwork guide `craftwork/guides/review-pages.md`. The brain checkout's current branch did not have the `tools/` folder.
- **Template facts, read in its code:** pictures sit in a grid of `min(count, 3)` columns and one column below 700 pixels wide; `show` items take `img`, `tag`, `label` and `alt`, with no link; links come from `look_for[].link` and `cards[].link` and must match `^https?://`; `build_page.py` reads `docs/<slug>/decide.json` beside itself and writes to `.runtime/pages/<slug>.html` unless given `--out`.
- **Test files:** `designcraft-jobs/tests/tool-guides/decide/`. Option pages in `options/`; option pictures from `shoot.mjs --theme day`; pairs made with ffmpeg (each cropped from the top, phone scaled to the desk's 900-pixel height, then joined side by side). The first crop used `sips --cropOffset`, which centred the cut here. Packed page `out/decide-test.html`; first try `shots-decide/`, fixed version `shots-decide2/`, both exit 0.
- **The picker skill** is `prototype-variants`; its facts (three variants by default, up to five, one at a time at full size, user-invoked only, prototype removed after the choice) are from its own skill file. It was not run.
- **The Claude Design facts** are from the tool list. Nothing was published or created in Sean's Claude account.
