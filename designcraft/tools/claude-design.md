# Claude Design.

Claude Design is the canvas where Designcraft puts live screens in front of Sean: a board of working screens inside Claude that he opens in his browser, clicks through and points at. Sean chose it over Paper and wants to master it. Read this before the first canvas of any job, and again when a canvas starts to feel like a fight.

A **canvas** is one board of **artboards**: each artboard is one screen, page or poster, sized like the real thing and built from web code, so buttons press and trays slide.

## What it's best at.

- **Several directions side by side,** one artboard each, so Sean compares by looking.
- **Screens that work.** An artboard can hold a whole small flow. In the test, a tray stepped from amount to check to sent, changed height at each step, and its button words changed in place. Sean presses Play and tries it.
- **Pointing instead of describing.** Sean clicks the thing that is wrong and comments on it, or nudges it himself: colour, corners, spacing, text.
- **Speaking the brand's names.** With a design system installed, the colour picker names every colour by its role ("accent", "ink-muted"), so a note like "make the button the accent" means one thing.

Where another tool wins:

- **Designing in real code** wins for anything that scrolls, reveals or performs: scroll stories, smooth scrolling, 3D and shaders, anything Sean's love of scroll effects calls for. An artboard can only animate with plain CSS, and the canvas loads nothing from the web but Google Fonts and files the lead uploads. Code also wins whenever the page itself is the deliverable.
- **The design-system row** keeps the truth. A Claude Design system is a copy made for the canvas; the repo's file of design values stays the source.
- **Decks** go to reveal.js or HyperFrames for a spectacle, or Claude Slides for a clear deck fast. Anthropic's own tutorial says decks belong in Slides, not on artboards.
- **The house Decide page** is where Sean rules. The canvas is the workbench; the Decide page, with its screenshots and a link to the canvas, is the vote.

## Setup and cost.

- **Nothing to install or buy.** It comes with every Claude plan, Sean's included. It now lives inside Claude itself; the old standalone site closes on December 14, 2026.
- **How the lead reaches it.** Through the Artifact tool: a quickstart asking for a design returns the Design type, and publishing from that type makes a new canvas. On this route the lead writes every artboard itself, so the canvas is only as good as the lead's own craft; it is the place Sean sees and handles the work, not a second designer. In an interactive session Sean can also type `/design` and a brief; Anthropic's documents say that drafts the artboards on one canvas the same way. A sister command, `/design-sync`, pulls a design system in from Claude Code; Anthropic says that route works best for a team that already has a React design system.
- **Cost.** Design work spends the same usage as all of Sean's Claude work, Claude Code and the overnight agents included. There is no separate allowance any more. Bigger asks spend more, and when the limit is reached Claude Design stops until it resets, unless extra usage is switched on.
- **The one action that proves it works.** Ask the Artifact tool for a design quickstart. If the answer names the Design type, the canvas is reachable. It creates nothing and costs almost nothing.

## Getting the best out of it.

### Brief it like a director.

The canvas follows the brief closely and fills every gap with its own habits. Its built-in guidance reaches for Inter and Space Grotesk when nothing is named, and calls a cream, serif and clay look its own habit. Sean's design checker flagged Inter as overused the moment the test used it. So a brief names: the job of the screen, who lands on it, the content in real words, the screen size, which states to draw (empty, error, loading, a lot of data), whether it should click through, the type faces, and the look it is reaching for.

An example of the difference. A weak brief: "A send-money screen for a wallet app, make it look nice." It leaves every gap to the defaults: the stock faces, a look nobody chose, and one screen where Sean needed two to choose between. The brief behind the test: "A send-money flow for a phone wallet, 390 by 844. Two contrasting directions, each on its own artboard. A: one tray over a dimmed home screen, warm off-white, the amount in a big display face, a single action per tray, the tray changing height from step to step. B: full screen, dark, monospaced numbers, a working keypad, the fee as a receipt line. Real buttons. No invented fees: mark them as placeholders." That got two screens that share nothing but the job, both clickable, with an honest placeholder where the fee goes.

### Give it a design system or brand.

A **design system** in Claude is its own page: a short rule book, the design values (colours, type, spacing, corner sizes), optional real components and a cover. The lead builds one from the brand's real sources, or Claude makes a small first one when there are none. Two things a master knows:

- **Installing is a separate step.** A canvas holds its own copy of the system, recorded in the canvas. Until the copy is in, the colour pickers show bare colour codes. After it, in the test, the picker named every colour already in the artboard by its role. The copy never updates by itself: change the system, then install it again.
- **Its file of values is shaped differently from the industry standard.** It wants simple lists. Translate the repo's values into it; never the other way round.

Sean's account holds one other system, made for slides and not set as the default. A default, if one is ever set, is applied to every design, so check before a job.

### Get real contrast, not three cousins.

Options that differ only in colour are one option. Make each one differ on a named axis, and change at least three of these together: the structure (a tray over the screen against a full screen), density, type, colour stance, light or dark, and how it moves. Name each option once ("A, one tray") and keep the name. Put each option's honest case and its main cost in the chat, not on the artboard, so the favourite doesn't get a speech the others don't. Early on, a rough sketch is enough to choose by; polish only the chosen one. When Sean says "you choose" for screens, start from Family's behaviour and make the second option its opposite.

### Make it real enough to judge.

- **Phone screens are fixed at 390 by 844; pages fill the window** and must hold up at phone width. Draw no fake status bar.
- **A flow that shares state is one artboard,** with each step shown in turn. Separate artboards can link, but each forgets the last.
- **Give Sean one or two levers.** A lever is a control on the artboard's Tweaks panel, such as three accent colours to flip between. Levers are for choices that cut across the design, never for words.
- **Placeholders, not inventions.** A missing price or fee is written as one, in brackets.

### How Sean reviews and points.

He opens the link in a desktop browser. Clicking an element raises a small bar: fill colour, layout, corners, spacing, and a comment pinned to that element, with "Send to Claude" ticked. The lead reads those comments through the Artifact tool. Sean's hand edits save at once, and a publish built on an older copy is refused, so the lead re-reads before changing anything.

Two catches. The **Chat** button in the canvas's header opens a separate Claude conversation in the web app, which never reaches the lead's session. And Anthropic's help centre says inline comments sometimes vanish; the comments view finds them, or Sean pastes the note into the session.

### Move from canvas to code without losing the design.

Each artboard is plain HTML with every style written on the element, so the exact numbers are there to copy. The lead reads the artboard's own file back and carries its values into the code, never redrawing from a screenshot. The design system's values become the repo's file of design values. Claude's export menu can also hand a design to Claude Code, and the product page says `/design` can create, edit and sync designs from Claude Code. Either way, the canvas settles how it looks and behaves; Devcraft builds it.

## Where it goes wrong.

- **Default faces and colours.** A face nobody chose is the early sign. Name the faces in the brief.
- **Guessed sizes.** The test tray was given a fixed height for each step and left a blank band on the check step. The sign: empty space at the foot of a state. Let content set the size, or measure it.
- **Three cousins.** Squint at the options together; if they blur into one, the axes are too close.
- **Look-alike components.** Without the real design system, Claude draws components that resemble the product's own. Anthropic's tutorial warns of it.
- **Silent breakage.** The canvas's format fails without an error: a stray double quote inside a style, which the test hit and caught before publishing, or a calculation inside a placeholder. If part of an artboard is blank, read its file.
- **No version history yet.** Duplicate the canvas before a big change.
- **"Never check" in its own instructions.** The canvas's built-in guidance tells the lead not to open or screenshot a canvas unless asked. Designcraft's rule that done needs proof wins: the lead looks at it before Sean does.

## Safety.

- **It lives on Anthropic's servers and is private until Sean shares it.** In the test, a signed-out browser saw only a sign-in page. The lead cannot change sharing; only Sean shares.
- **It spends Sean's shared usage.** A long canvas session draws on the same budget as everything else he runs.
- **Ask Sean before uploading his own material,** such as screenshots, brand files or a code repository. Nothing from his employer goes in.
- **Opening the Chat button starts a conversation in Sean's account.** The test did this once by accident; it held no messages.

## More details.

**Sources, read November 17, 2026:**

- Launch post, April 17, 2026: https://www.anthropic.com/news/claude-design-anthropic-labs
- Product page (runs inside any conversation; `/design`, `/design-sync`): https://claude.com/product/design
- Help centre, getting started (shared usage pool, known limits): https://support.claude.com/en/articles/14604416-get-started-with-claude-design
- Help centre, the move from the standalone site (closes December 14, 2026): https://support.claude.com/en/articles/17440474-move-from-standalone-claude-design-to-claude
- The June 17, 2026 update: https://claude.com/resources/articles/claude-design-stays-on-brand-for-daily-work
- Anthropic's prototyping tutorial: https://academy.claude.com/tutorials/using-claude-design-for-prototypes-and-ux
- Claude Code's artifacts page (`/design` needs version 2.1.265 or later): https://code.claude.com/docs/en/artifacts
- Pricing (Design in every plan): https://claude.com/pricing
- The Design and Design System types' own instructions and reference pages, read through the Artifact tool.

**Tested November 17, 2026, in Sean's account, both kept private and unshared:**

- A canvas, "Designcraft test: wallet send screen, two directions". Two 390 by 844 artboards, both clickable. From the first call to both artboards live took about two minutes; one targeted revision and the design-system install took about one more. It rendered correctly in Sean's signed-in Chrome, and Play ran the tray flow.
- A design system, "Designcraft test: Tray system". Ten colours, six text styles, four spacing steps, three corner sizes, a short rule book and a cover. It was then installed on the canvas, and the picker named the colours by role.
- The house design checker flagged Inter as overused and the tray's overshooting ease as bouncy. The faces were changed; the ease was kept on purpose, after Family's tray.

**Not confirmed:**

- How the canvas viewer looks at phone width: Sean's Chrome window would not resize, and the in-app browser is not signed in. Fixed phone artboards are not affected; a page artboard needs that check.
- How `/design` behaves when typed: a helper session cannot run commands, so only the Artifact route was tested.
- How much usage a canvas spends: Anthropic publishes no figure.
- Whether the empty chat the Chat button opened is kept in Sean's list.
