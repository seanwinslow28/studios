# Every screen and everyone

This brief is about one design that works on every screen and for everyone: on a phone in one hand, a wide desk screen, a keyboard, a screen reader, large text, or motion turned down. Read it when a job settles its layout, and again before Sean sees anything, because the automatic checks are worst at these faults.

## Responsive means re-composing, not shrinking

The beginner's phone layout is the desk layout, squeezed: columns stack, everything shrinks, and the page becomes a long scroll past things nobody came to the phone for. The master asks what this person is here to do on a phone, and designs for that.

The shelf shows the difference. Raphael Segerman's portfolio is one fixed screen of three columns on a laptop; on a phone it becomes an ordinary scrolling page, with each project's name set under its picture. Poor Charlie's Almanack leaves its one 3D collage out on the phone and keeps the reading column whole. Lando Norris's site turns its four-column grids into two and gives the 3D head a "tap to lock" button, so one finger never has to scroll and steer at once.

What to keep differs by product. A reading page keeps its column and loses the furniture around it. A tool keeps its main action in reach and folds the rest behind a menu.

A few habits make re-composing work:

- **Big things shrink faster than small things.** A headline sized for a desk looks absurd on a phone. On a phone the gap between big and small should narrow. Poor Charlie's Almanack keeps its text at 18 pixels while its titles drop from about 140 to about 82. GOV.UK keeps body text at 19 pixels on every screen but drops its question heading from 36 to 27, and its largest spacing step from 60 to 40.
- **Give things the width they need, not the width they're offered.** Text reads best at about 45 to 75 characters a line; GOV.UK caps it at 75. A form or a card has a width that suits it; on a big screen it stays at that width rather than growing.
- **Fix what shouldn't stretch.** A sidebar sized for its contents, with the main area flexing beside it, beats a sidebar that takes a quarter of whatever screen it gets.

## Breakpoints come from the content

A breakpoint is the width at which the layout changes. The beginner copies a list of popular device widths. The master widens and narrows the window slowly and puts a breakpoint wherever the content starts to look wrong: a line too long, a row of cards too tight, a label wrapping under its icon. Devices change every year; the moment a grid gets cramped does not. The best parts change shape by the space they're given, not the screen, so a card works in a narrow sidebar and a wide column alike.

The two sizes Designcraft's checks photograph, 1440 and 375 pixels wide, are a floor, not the set. A tablet, a phone turned sideways and a half-width desk window all sit between them, and that is where layouts usually break.

## Fingers are not pointers

A mouse pointer is a single pixel. A fingertip covers a lot more and hides what it touches. So:

- **Targets big enough to hit.** Apple's default control size is 44 by 44 points, with 28 as the floor. The web standard's required minimum is 24 by 24 pixels, and its stricter level asks for 44. GOV.UK's round option buttons are 40 pixels across inside a 44 pixel tap area: the tap area can be bigger than what you see.
- **Space between them.** Apple suggests about 12 points of padding round a control with a visible edge and about 24 round one without. Two small targets close together cause the wrong tap more often than one small target alone.
- **Dense is a desk choice.** Linear's 28 pixel rows suit a mouse, not a thumb; its own site sets 44 as the smallest tap size.
- **No hover.** Anything revealed only on hover is missing on a phone.
- **Every gesture has a button too.** Swipe to delete needs an Edit button; drag to reorder needs another way. Some people can't swipe or drag, and others never find the gesture.

## Phone-first decisions

Designing the phone version first, at roughly 400 pixels wide, forces the hard choice early: what matters most. The desk version then adds room rather than removing things, and usually needs fewer changes than expected. Other decisions belong to the phone from the start: the main actions within reach of a thumb, near the bottom; text in form fields at 16 pixels or more, because iPhone's browser zooms into smaller fields and breaks the layout; and no layout that only works held one way up.

## Accessibility is craft, not a checklist

Accessibility means the design works for people who see poorly or not at all, who can't use a mouse, who need bigger text, or who get dizzy from motion. Done well, it looks like nothing special. Done late, it looks bolted on.

**Contrast.** Body text needs at least 4.5 to 1 against its background, large text and controls at least 3 to 1. Designcraft's house pages hold all text to 4.5 to 1. The craft is meeting it without going grey and dull. Coloured status labels that fail as white on bright colour pass as dark text on a pale tint of the same colour. Text on a coloured panel gains contrast by shifting its hue towards a brighter neighbour, cyan from blue, rather than fading to grey. Check night colours separately; they are added last and checked least.

**Never colour alone.** Red and green look alike to many people. A rising number gets an arrow as well as a green tint. A chart with several lines does better with light and dark shades of one colour than with several colours. GOV.UK's error messages start with a hidden word, "Error:", so a screen reader announces what red only shows.

**Focus you can see.** The focus mark shows where the keyboard is. Removing it, often because someone found the browser's ring ugly, strands every keyboard user. Replace it with something better, never with nothing. GOV.UK's thick yellow focus is the shelf's model: it is the only job yellow has on the site. The web standard's strict level asks for a mark at least 2 pixels thick at 3 to 1 contrast. And a focused item must not hide under a sticky header.

**Keyboard paths.** Every action works from the keyboard, in an order that matches the page. A pop-up holds the focus while open, closes with Escape, and hands the focus back. Nothing traps the keyboard. Things 3 shows how far a master takes it: over a hundred Mac shortcuts, the commonest actions one key.

**Structure a screen reader can follow.** A screen reader reads the page aloud from its code, so the order and names in the code are the design. Headings in order, with no skipped levels, even when a heading is styled small. A page title that only screen readers hear is fine when the content speaks for itself on screen. Every icon button gets a name. Every link says where it goes: "Read the pricing guide", never "click here". When something changes without the person moving, a saved note or a new result count, the screen reader must be told.

**Motion turned down.** Some people's devices ask for less motion because movement makes them dizzy or ill. Less motion means gentler, not none: slides and springs become short fades, and changes of colour that explain something stay. Linear's site checks for this request 41 times. Nothing flashes more than three times a second. Anything that moves on its own for more than five seconds gets a pause.

This matters most for the scroll reveals Sean loves. A page that fades its sections in as you scroll must still hold all of its content, in order, when motion is off. With motion turned down, a well-built reveal page shows everything at once; a badly built one shows a blank page, or never reveals the second half.

**Text that can grow.** People enlarge text, some of them a lot. A layout must survive text at twice its size, and must fit a screen 320 pixels wide without scrolling sideways. That rules out boxes with fixed heights, buttons with fixed widths and text set in pictures. Apple asks apps to allow at least 200 percent, and uses 17 points as its default body size on iPhone.

## What only a person catches

Designcraft's three automatic checks, and what they missed in testing, are written up in the tool guide on checking a design. In those two tests, three things got past all three checks: a removed focus outline, a "click here" link, and everything below the first screen of a scroll-reveal page. The pattern behind those misses is the craft a person brings:

- **Whether the order makes sense.** A check can see that every button has a name. Only a person tabbing through notices that the focus jumps from the header to the footer and back.
- **Whether the words make sense.** A link named "click here" is technically named. Only a person hears that a list of ten of them is useless.
- **Whether everything was seen.** Hidden menus, unscrolled reveals and anything drawn in 3D are not checked at all.
- **Whether the phone version was re-composed or just squeezed.** No rule detects a phone layout that is technically fine and pointless.
- **Whether the reduced-motion version still tells the story.**
- **Whether it holds at 200 percent text**, at a tablet width, and with the phone turned sideways.
- **Whether colour is carrying meaning alone,** and whether text over a picture or a gradient can be read. The checks leave these to a person.

## How it goes wrong

- **The desk layout, squeezed.** Fix: decide what the phone is for, and design that.
- **Breakpoints copied from a device list.** Fix: put them where the content breaks.
- **Hover and swipe as the only way in.** Fix: a visible control for everything.
- **The focus outline taken out for looks.** Fix: design a better one.
- **Grey text to look refined.** Fix: hold contrast, and find elegance in type and space.
- **Reveals that hide content from everyone who turned motion off.** Fix: the content is there first; the motion is a layer on top.

## What a strong designer would notice

- A phone layout that is the desk layout stacked.
- A table that scrolls sideways on a phone with no sign that more is off-screen.
- Tap targets smaller than a fingertip, or crowded together.
- Something only reachable by hovering or swiping.
- No visible mark of where the keyboard is.
- Links that say "click here" or "learn more" with nothing else.
- Headings chosen for their size, skipping levels.
- Red and green as the only difference between two states.
- Light grey text on white, or any text over a busy picture.
- A scroll-reveal page that is blank with motion turned off.
- A button or box that cuts off its text when the text grows.

## More details

- **Not yet drawn on:** *The Design of Everyday Things* by Don Norman (being captured in another session) and *Don't Make Me Think* by Steve Krug (out November 30). Revisit this brief when their notes exist.
- **Book, in the studio's own words:** *Refactoring UI* by Adam Wathan and Steve Schoger, private notes in `designcraft/library/books/refactoring-ui/`: the dashboard video lesson (condense rather than stack, a cue when a table scrolls sideways), the complex-form video lesson (back to one column on a phone), the layout chapter (start at about 400 pixels, big things shrink faster, width by need, fixed sidebars, max-width over column spans), the colour chapter (dark text on a pale tint, hue rotation, never colour alone, shades of one hue for charts) and the hierarchy chapter (headings styled for their role, a title only screen readers hear).
- **Read today, November 17, 2026:**
  - WCAG 2.2 quick reference, W3C: 1.4.3 Contrast Minimum (4.5 and 3 to 1), 1.4.11 Non-text Contrast (3 to 1), 1.4.1 Use of Color, 1.4.4 Resize Text (200%), 1.4.10 Reflow (320 CSS pixels), 1.4.12 Text Spacing, 1.3.1 Info and Relationships, 1.3.4 Orientation, 2.1.1 Keyboard, 2.1.2 No Keyboard Trap, 2.2.2 Pause, Stop, Hide (5 seconds), 2.3.1 Three Flashes, 2.3.3 Animation from Interactions, 2.4.4 Link Purpose, 2.4.7 Focus Visible, 2.4.11 Focus Not Obscured, 2.4.13 Focus Appearance (2 pixels, 3 to 1, level AAA), 2.5.5 Target Size Enhanced (44 by 44, AAA), 2.5.7 Dragging Movements, 2.5.8 Target Size Minimum (24 by 24, AA), 4.1.3 Status Messages: https://www.w3.org/WAI/WCAG22/quickref/
  - Apple Human Interface Guidelines, Accessibility, read from Apple's page data; change log last entry June 9, 2025 (text to 200%, 17 point default on iPhone, contrast table, 44 by 44 default and 28 by 28 minimum controls, 12 and 24 point padding, alternatives to gestures, Reduce Motion practices, keyboard alone): https://developer.apple.com/design/human-interface-guidelines/accessibility
  - Apple Human Interface Guidelines, Feedback (feedback in more than one form so it reaches everyone): https://developer.apple.com/design/human-interface-guidelines/feedback
  - Nielsen Norman Group, ten usability heuristics (consistency, flexibility and efficiency for keyboard experts): https://www.nngroup.com/articles/ten-usability-heuristics/
  - GOV.UK Design System, text input (labels and hint text for screen readers) and error message (the hidden "Error:" word): https://design-system.service.gov.uk/components/text-input/ and https://design-system.service.gov.uk/components/error-message/
- **Shelf examples:** `designcraft/research/govuk-check-uk-visa.md` (19 pixel body on every screen, 36 to 27 pixel questions, 60 to 40 spacing, 75 characters a line, 44 pixel tap areas, yellow focus), `linear-app.md` (28 pixel rows, 44 pixel tap minimum on its site, 41 reduced-motion checks), `things-3.md` (108 Mac shortcuts), `segerman-portfolio.md` (the phone version as a scrolling page), `poor-charlies-almanack.md` (18 pixel text, titles from about 140 to 82, the collage left out on a phone), `lando-norris.md` (four columns to two, tap to lock). The book's own phone examples were swapped for these so none is retold here.
- **Craft salvaged from skills:** the Impeccable skill's adapt guidance (adapting is rethinking, not scaling; content-driven breakpoints; thumb reach; parts that respond to their container), harden guidance (16 pixel form text and iPhone zoom; 200% text; never colour alone) and audit guidance (target sizes, text scaling, reduced motion that keeps useful feedback); `emil-design-eng` and `apple-design` (reduced motion means gentler, not none; no hover on touch; scale layout with the person's text size).
- **The three checks and their misses:** Designcraft's tool guide `designcraft/tools/checking-a-design.md`, tested November 17, 2026. The 45 to 75 character line is from Refactoring UI's text chapter; GOV.UK's cap of 75 is from its own layout guide, as recorded on the shelf.
