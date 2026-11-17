# Claude Slides

Claude Slides makes a clear slide deck inside Claude, fast, from notes, files or the work already in a conversation. The deck opens beside the chat, where Sean can edit it by hand, present it, and download it as PowerPoint or PDF, which Keynote opens. Read this before making a deck whose job is to be understood, not to astonish. For a spectacle, go to Reveal or the HyperFrames slideshow.

## Which of the three to reach for

- **Reveal** when the deck is a live performance: motion you see between clicks, live scenes, a brand turned on its head.
- **The HyperFrames slideshow** when the same deck must also exist as a film.
- **Claude Slides** when the job is a clear deck, made fast, that someone will open, edit or forward in PowerPoint, Keynote or Google Slides. Sean's words: "If I need the clear deck, fast, then Claude Slides will do."

## What it's best at

- **Speed to a clean first deck.** The lead writes the slides straight into the deck from the session, and Sean sees it in his browser the moment it lands.
- **Hand edits without code.** Sean can select, retype, drag and resize much as in Keynote, reorder thumbnails, skip a slide, or click an element and leave a comment for Claude to act on.
- **Leaving as an ordinary file.** PowerPoint, PDF, a single web page, a picture of one slide, or an editable copy in Google Drive.
- **Presenting inside Claude.** Present plays it full screen. Present with speaker notes adds a second window with the notes, a clock, and the current and next slides.
- **A design system.** A saved set of colours, type and rules can style every deck. One marked as the default is applied to every deck automatically.

## Where it falls short of a spectacle

Plainly: it cannot make one. The deck is a set of fixed canvases with styling, not a web page that runs code.

- **Motion is limited to arrivals.** Elements can animate when a slide arrives, reveals can wait for a click, and a slide can leave with a fade, a push or a "magic move" that glides matching elements across. Nothing reacts to the pointer, and no script runs on a slide.
- **No live scenes.** No Three.js, no shader, no scroll story. The one exception is a tiny sandboxed embed, a small web page boxed inside the slide: up to eight a slide, each 16 kilobytes at most, with no internet, and viewers can't click into it. PDF and PowerPoint flatten it into a picture.
- **No scroll view, no branching, no audience taking part.** Spotify Wrapped 2025's quiz, where the listener guesses before the reveal, has no equivalent here.
- **PowerPoint drops the motion.** Transitions and skipped slides are dropped, and charts, icons and shapes become pictures. Only the web-page download keeps the transitions.
- **Hard caps.** About 200 elements a slide, four typefaces a deck, pictures only from uploads (never a link to an image elsewhere).

Shopify's Renaissance edition could not be built here. A calm, clear deck in the spirit of Poor Charlie's Almanack can, because there size and spacing carry the page, not motion.

## Setup

- **Cost:** on every Claude plan, Free included. On Team and Enterprise plans an owner can switch it off.
- **Two ways in.** Sean asks for a deck in any conversation, or opens Artifacts and makes something new. From a Claude Code session, the lead starts a deck from the Slides type with the Artifact tool, then writes its slides as files.
- **The design-system question comes first.** A default design system is used on every deck, however short the request. Sean's account lists two systems and marks neither as default, so ask which to use, or build with a look of the deck's own.
- **The one call that proves it works:** the Artifact tool's read-only quickstart for slides. It names the Slides type and lists the design systems, and creates nothing.

## Getting the best out of it

**Write the headlines first, as the story.** Every slide's headline states its point as a sentence with a verb. Read in a row, the headlines alone should make the case. The test deck's five headlines are the story side of all three deck tools:

1. Read only the headlines, and the deck should still make its case.
2. A headline that states the point does its work before anyone speaks.
3. One idea per slide keeps the room with you.
4. The reveal lands when the speaker stops talking.
5. Every clip needs a fallback you have already tested.

**One idea per slide, and fewer bullets.** The type's own guidance is blunt: a statement beats a list. Turn lists into a table, a row of cards, one big number or a quote.

**Use the reveal sparingly.** A reveal works the way it does in Reveal: a piece of the slide waits for its click, styled one way before and another after. Put the click on the thing that moves, not on its parent or its child, or it shows from the start. Then stop talking and let the room look.

**Motion that helps, at arrival.** Write the finished look as the plain style and the starting look as the animation's first frame, so the editor, the PDF and PowerPoint all show the finished slide. Stage arrivals so the whole slide is in place within a second. Viewers who switch off motion on their computer see the finished look.

**Pick fonts that travel.** Fonts come from Google Fonts or from uploaded files. A few Google families reserve their name under their licence and stay links: offline, or in PowerPoint on a computer without them, the text falls back to the next face. The PowerPoint download comes two ways, with the deck's own fonts or with common ones every computer has. Choose common ones when a stranger will open it.

**Choose the download by what happens next.**

- Someone will edit it in PowerPoint or Keynote: PowerPoint. Keynote opens and edits PowerPoint files, by Apple's own guide.
- Someone will only read it: PDF.
- The transitions matter: the web page.
- A team works in Google: the Google Slides copy, once Google Drive is connected.

**Check every number.** Charts are built from the data Claude had when it made them and do not update. Claude may leave a visible placeholder for a missing figure. Read every slide before presenting.

**Duplicate before restructuring.** A copy of the deck keeps the working version safe while a new order is tried.

**An example of the difference.** The test deck's second slide sets a label beside a point. "Q3 results" leaves the room waiting to be told what to think. "Q3 grew because returns fell" means the room already knows before the speaker says a word. Every headline in the deck was written the second way, which is why the five can be read alone.

## Where it goes wrong

- **The brand look that wasn't asked for.** A default design system styles every deck. Check which one applies before building.
- **An ambitious slide that won't save.** Too many elements, too many pinned boxes inside one container, or unsupported styling makes a slide read-only, with the reason shown.
- **Styling that quietly disappears.** Many web styles are dropped on read, such as stacking order, some gradients and background pictures. Write the plain kind the type's format page lists.
- **The deck that changes on the way out.** PowerPoint loses the transitions and turns charts and shapes into pictures. Open the exported file before sending it.
- **A typeface swapped in someone else's copy.** A font that can't travel shows as its fallback. Pick fonts for where the deck is going.
- **A figure nobody checked.** A placeholder or a stale chart reaches the room.

## Safety

- **Private until Sean shares it.** A deck starts visible to him alone. Sharing is his choice, from the deck's Share menu, at view, comment or edit access. Anyone who can open it can read the speaker notes.
- **The deck lives on Anthropic's servers.** Ask Sean before putting anything sensitive in it.
- **Google Slides export writes to his Google Drive.** Ask first.
- **Downloads are his clicks.** The lead builds the deck; Sean downloads the file.

## More details

- **The test deck,** made November 17, 2026, private and unshared: "Designcraft test: Headlines carry the deck". Five slides, no design system, EB Garamond headings and Public Sans text from Google Fonts, one click reveal on slide four, fade transitions, notes on every slide. Its files were written in this session's scratch folder and published to the artifact in two calls; both were accepted.
- **Checked in the test:** the quickstart named the core Slides type and listed two design systems with no default. A local preview of the five slides, with scripts and the network off, showed no overflow or broken lines (fonts fell back, as expected offline).
- **Not tested:** Present, the speaker-notes window, every download, the Google Slides copy, and opening the PowerPoint file in Keynote. Each needs Sean's browser and his click. Keynote's handling of the file rests on Apple's guide alone.
- **Where the limits come from:** the Slides type's own instructions and its format and fonts references, read through the Artifact tool on November 17, 2026: the 1920 by 1080 canvas, the embed limits, 200 elements a slide, four typefaces, no image links, and which styles are dropped.
- **Sources, read November 17, 2026:** Anthropic's tutorial on Slides, https://academy.claude.com/tutorials/using-claude-design-for-presentations-and-slide-decks; Anthropic's help page on artifacts, https://support.claude.com/en/articles/17153992-what-are-artifacts-and-how-do-i-use-them; Apple's Keynote guide on opening a presentation, https://support.apple.com/guide/keynote/open-or-close-a-presentation-tan72232b56/mac.
