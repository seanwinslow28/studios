# Checking a design before Sean sees it

Three free checks every design gets before Sean looks at it: the house screenshot checker, the Impeccable detector, and axe-core run through Playwright. Each catches faults the other two miss, and together they still miss some. Read this before running them, and before saying a design "passed".

## Words used here

- **Contrast** is how clearly text stands out from what is behind it, written as a ratio from 1 to 1 (invisible) to 21 to 1 (black on white). The common rule asks for at least 4.5 to 1 for body text and 3 to 1 for large headings. The house pages hold every text to 4.5 to 1.
- **Accessibility** means the design works for people who see poorly, who can't use a mouse, or who listen to the page through a screen reader, which reads the page aloud from its code.
- **A pass** means a check found nothing it knows how to look for. It never means nothing is wrong.

## What each check is best at

- **The screenshot checker** shows the design as Sean will see it: at desk size and phone size, by day and by night. It lists script errors and failed loads, and any spot where the page is wider than the screen, which makes a phone scroll sideways. It is the only one of the three that produces something to look at.
- **The Impeccable detector** reads the page's code for weak contrast and for tired design habits: the overused typeface, gradient text, the coloured stripe down one side of a card, cards inside cards. It is the taste check. It also reads the night colours from the code, so it can catch a night-mode fault without a screenshot.
- **axe-core** is a widely used set of accessibility rules, run in a real browser. It catches what a picture can't show: a button with no name, a picture with no description, headings out of order, text that fails contrast once the page has drawn.

Where something else wins: Lighthouse, from Google, adds a speed score; it is on the "not now" list. The keyboard and a screen reader still need a person.

## Setup

All three are free and already on the Mac. Nothing is uploaded.

- **The screenshot checker** is a short script in the brain, built for the house pages. It needs Node and Google Chrome. Run it on any page or link, with a folder for the pictures:

```bash
node shoot.mjs page.html shots
```

It prints how many pictures it took, then any errors and any sideways scroll, and exits with a failure if it found either. It lives on the brain's main branch; a brain checkout on another branch may not have it.

- **The Impeccable detector** ships inside the Impeccable skill, not as a command on its own. Typing `impeccable` alone gives "command not found". Call it from the skill's scripts folder, and switch its usage reports off for the run:

```bash
DO_NOT_TRACK=1 ~/.claude/skills/impeccable/scripts/impeccable detect page.html
```

It lists each finding with the bit of code behind it, and exits with 2 when it finds anything.

- **axe-core** runs from Designcraft's tools folder, beside the jobs. Its script opens the page in the Chrome already on the Mac:

```bash
node axe_check.mjs page.html --phone --dark
```

It prints what it found, worst first, and exits with 1 when it finds anything. Leave out `--phone` for desk size and `--dark` for day.

## The test: one page, fifteen planted faults

On November 17, 2026 one throwaway portfolio page was built with fifteen faults planted in it, and all three checks were run on it. Axe ran twice: desk by day, and phone by night.

| Planted fault | Screenshots | Impeccable | axe |
|---|---|---|---|
| A strip 900 pixels wide | Caught: 924 wide on a 375 screen | Missed | Missed |
| A script error on load | Caught, all four runs | Missed | Missed |
| Night mode forgets the text colour | Visible in the night pictures, not reported | Caught, 1.0 to 1 | Caught, phone by night only |
| Faint grey text on a gradient | Missed | Caught, 3.0 to 1 | Unsure: left for a person |
| Text over a busy picture | Missed | Missed | Unsure: left for a person |
| Overused typeface | Missed | Caught | Missed |
| Gradient text | Missed | Caught | Missed |
| Card inside a card, with a side stripe | Missed | Caught, both | Missed |
| A 10-pixel label | Missed | A note, not a failure | Missed |
| Headings that skip levels | Missed | Caught | Caught |
| A picture with no description | Missed | Missed | Caught |
| An icon button with no name | Missed | Missed | Caught |
| A form field with only greyed hint text inside it | Missed | Missed | Passed it |
| Focus outline removed | Missed | Missed | Missed |
| Link text "click here" | Missed | Missed | Missed |

What it showed:

- **Each check earned its place.** The screenshots alone caught the layout and the script error. Impeccable alone caught the taste faults and the faint grey. Axe alone caught the missing names.
- **Two faults got past all three.** Taking away the outline that shows where the keyboard is, and a link that says "click here". Only a person tabbing through the page finds those.
- **Axe treats hint text as a label.** The field with only greyed hint text inside, and no label, passed. An earlier test caught a field with no label at all. Hint text vanishes as soon as someone types, so a real label is still needed.
- **Axe won't guess contrast over a gradient or a picture.** It put both in "needs a person to look". The script prints only how many such items there are; the lead looks at each one in the screenshots.
- **The night fault was plain to see in the pictures,** dark grey text on near-black, but the screenshot checker said nothing about it. A picture is only a check when someone looks at it.

## Pages that reveal on scroll

Sean loves reveals, so a second page was tested: three screens, with the second and third fading in as you scroll, and faint grey text planted in the second.

- **The screenshots showed only the first screen.** Everything below it was blank, because the page was photographed without being scrolled. No error was reported.
- **Axe skipped the faint text,** because it was still hidden. It reported only that the page had no main region and no top-level heading.
- **Impeccable found nothing.**

So for a page built on reveals, all three checks pass a page they have not seen. Two ways round it: check the page with reduced motion switched on, where a well-built page shows everything at once (the screenshot checker has a `--reduced` setting), and look at the live page in a browser, scrolled by hand. A version of the checks that scrolls the page first was not tested.

## Getting the best out of them

- **Run all three every time.** No one of them is enough.
- **Look at every picture.** Desk and phone, day and night. The checker's silence covers errors and width, nothing else.
- **Read Impeccable's findings with judgment.** It flags habits, not laws. A gradient headline can be right for a job that asked for it. Fix it, or say why it stays.
- **Read axe's "needs a person" items.** They are usually contrast over a picture or a gradient: exactly the hero sections Designcraft makes.
- **Tab through the page once.** Every link and button should show where you are, in order, and work with the keyboard alone.
- **Check the night version on purpose.** Night colours are often added last and checked least. In the test, axe caught the night fault only when told to look at night.
- **Check the live page too.** The screenshot checker and axe both take a link to a running page.

## What a pass proves, and what it doesn't

A clean run proves the page loads without script errors, fits a phone's width, avoids the habits Impeccable knows, and breaks none of the rules axe can test. It does not prove the page is easy to read, easy to use, or beautiful. It does not prove a keyboard user or a screen-reader user can get through it, or that motion is calm enough for someone who asked their device for less. Hidden content, content below an unscrolled reveal and anything drawn on a 3D canvas are not checked at all. Say "the three checks found nothing", never "it passed accessibility".

## Where they go wrong

- **A phone picture of a page that is too wide** comes out the width of the page, not the phone. That is the fault showing; don't crop it away.
- **Hidden things are skipped.** Axe ignores what isn't showing, so a menu, a pop-up or a reveal must be opened before it is checked.
- **The screenshot checker only knows the house pages' special moments.** On any other page it takes one full-length picture per size and look.
- **Two sizes only.** Desk is 1440 wide and phone 375. A tablet, or a phone held sideways, is not covered.

## Safety

- **Nothing here uploads the page.** All three run in a browser on the Mac. A live link is fetched like any visit.
- **Impeccable reports usage to its maker by default.** Its own status line says the usage reports come from its idea-dealing feature and carry no project names or code. Set `DO_NOT_TRACK=1` on every run. Switching it off for good changes a setting, so ask Sean first.
- **No cost.** Ask Sean before installing anything new into the tools folder.

## More details

- **Tested November 17, 2026,** in `designcraft-jobs/tests/tool-guides/checks/`: `faults.html` (fifteen planted faults) and `reveal.html` (scroll reveals).
- **Screenshot checker:** `docs/prototypes/house-look/tools/shoot.mjs`, copied from the brain's `main` branch. Desk 1440 by 900; phone 375 by 812 at double density; day and night through the browser's colour-scheme setting; full-page capture without scrolling. On `faults.html`: 4 pictures, the TypeError in all four runs, sideways scroll on both phone runs, exit 1. On `reveal.html`: exit 0.
- **Impeccable:** version 4.8.0, launcher `~/.claude/skills/impeccable/scripts/impeccable`, binary for Apple silicon beside it. On `faults.html`: 13 findings and one advisory, exit 2. On `reveal.html`: exit 0. `impeccable telemetry status` printed "telemetry: on" and names three switches: `impeccable telemetry off`, `DO_NOT_TRACK=1`, `IMPECCABLE_NO_TELEMETRY=1`. The skill's hook also ran on its own when the test page was written in Claude Code, and flagged four of the same habits.
- **axe:** `designcraft-jobs/tools/a11y/axe_check.mjs`, with Playwright 1.65.1 and `@axe-core/playwright` 4.14.0; the engine reported version 4.14.1. Phone is Playwright's iPhone 14 profile. Results: `button-name`, `image-alt`, `heading-order` by day; plus `color-contrast` in 6 places by night. The `label` rule passed through `non-empty-placeholder`. The unsure items were `color-contrast` on the gradient headline, the grey line, and the text over the picture. The script's `--json` file stores only the count of unsure items.
- **Contrast rule:** the 4.5 and 3 to 1 figures are as Impeccable's own findings state them; the house rule is from the house page guide.
