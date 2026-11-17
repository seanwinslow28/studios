# How a screen behaves

This brief is about everything a screen does besides look good on a perfect day: its states, how it answers each thing a person does, and what happens when something goes wrong. Read it when a job reaches app screens, forms, or any page people act on, before the rough version is shown, because a design drawn only for the happy path gets drawn twice.

## A screen is a set of states, not a picture

A mock-up shows the best moment: tidy sample names, every number the right length, a fast network. A real screen spends much of its life elsewhere. A master draws each of these:

- **First use.** The person has made nothing yet. This is the feature's first impression, so design it first. Say what will appear here, why it is worth having, and give one clear way to start. Hide the tabs, filters and search box that have nothing to act on yet.
- **Empty for other reasons.** No search results needs a way out: change the words, clear the filters. "You can't see this" needs a reason and a way to get access.
- **Loading.** Something is on its way; more below.
- **Partial.** One panel failed while the rest worked. Let the failed part say so in its own place and keep the rest working. A whole page blanked because one box failed is a design fault.
- **Too full.** Two thousand items need search, paging or grouping. A 60-character name, a number in the billions, a translation a third longer than the English: each breaks a layout tried only with tidy data.
- **Error.** Something went wrong. Say what, in plain words, and what the person can do about it.
- **Success.** Most actions are expected to work, so most success needs no fanfare; the result simply appears. Save a clear confirmation for the moments that matter, like a payment going through.
- **Offline.** Say so plainly, keep what the person typed, and retry on its own when the connection returns.

The shelf's Family wallet is the model for moving between states. It keeps people oriented by never letting anything just appear or vanish: one panel changes height and swaps its contents, so you always know where you are and how you got there.

## Signifiers: telling people what they can do

What an object lets you do is its affordance. The visible cue that tells you so is a signifier. On a screen nothing can be felt, so almost everything rests on signifiers.

Good signifiers are quietly physical. GOV.UK's green button has a darker strip under it, darkens when the pointer is over it, and drops two pixels when pressed: it says "button" in three ways without a word. Duolingo's buttons have a deeper edge like the side of a real key, and the edge vanishes when pressed. Even the width of a text box is a signifier: a short box asks for a short answer, which is why stretching every field to full width throws away a free hint.

Signifiers go wrong in a few familiar ways:

- **Flattened away.** A text link on a coloured panel stops looking clickable. A master gives it a subtle button shape instead.
- **Hidden in hover.** A phone has no hover. Anything that only shows itself when a pointer rests on it is invisible to touch.
- **Ambiguous targets.** A card that looks like one object, where only its small button works, frustrates people tapping the middle. Make the whole card the target, or make the button clearly separate.
- **A label doing the work.** If a control needs a sentence to explain it, the control is placed or shaped wrongly. Put it next to what it changes, and arrange it to mirror what it changes.

## Feedback for every action, and how fast

Every press, tap and keystroke deserves an answer, and its speed decides whether the screen feels like a tool in the hand. Usability research gives three marks:

- **About a tenth of a second.** Under this, the response feels instant and the person feels they did it themselves. Press states belong here, and they should show on the press itself, not on release. Family's web panel shifts its buttons in 100 milliseconds; Linear's quick changes take 100.
- **About one second.** Under this, people notice the wait but keep their train of thought. Past it, show that work is happening.
- **About ten seconds.** Past this, attention wanders. Show real progress, and give a way to stop.

From those marks comes the craft of waiting:

- **No spinner for a short wait.** A spinner that flashes up for a fraction of a second reads as a flicker. Under about a second, just show the result.
- **Show the shape of what is coming.** Grey blocks in the shape of the content (often called a skeleton) tell people what will arrive and where.
- **Show real progress for long waits.** A bar that moves, or a running count of items done. A spinner is the last resort, because it says only "something, eventually".
- **Show the result before the server agrees, where it is safe.** Mark the task done at once, and undo it with a clear note if the save fails. This optimistic update is why the best tools feel faster than their networks.
- **Guard against the double press.** A button that stays live while its action runs gets pressed twice. Show that it is busy and ignore the second press. Family's web panel ignores taps for just over a third of a second while it changes shape.
- **Match the weight of the feedback to the news.** Status sits quietly near what it describes. A warning about losing work interrupts. Apple's guidance makes the same split.

Feedback has to reach everyone: colour plus words or an icon for someone who can't tell red from green, sound plus vibration for someone looking away.

## Forms that forgive

A form is a conversation in which the person does most of the talking, so it should be patient.

- **Labels stay visible, above the field.** Grey hint text inside the box is not a label: it vanishes once someone types, some screen readers skip it, and its grey usually fails contrast. Designcraft's own checks passed such a field, so a person has to catch it.
- **A label belongs to its field.** If the gap below a field is the same as the gap above it, people type into the wrong box. More space between groups than within them.
- **Ask one thing at a time when the questions are hard.** GOV.UK's visa checker asks three questions on three pages and keeps every past answer visible with a "Change" link.
- **Accept what people mean.** A postcode with or without a space, a card number with dashes, a name with an apostrophe or an accent. Strip the stray characters; don't reject the person.
- **Check when they're done, not while they type.** Shouting "invalid" halfway through an email address is rude, and hard on slow typists. GOV.UK waits until the person presses Continue. Live checking earns its place only where people want to know as they go, like a character count.
- **Error messages say how to fix it.** Put the message next to the field and in a short summary at the top, worded the same way, using the question's own words. "Enter how many hours you work a week", never "This field is required". Never clear what they typed. Never "oops", "sorry", "you forgot" or "invalid".
- **Don't use an error for a no.** Being ineligible, or not allowed, is not a mistake the person made. It gets its own page that explains and says what to do next.

## Undo over confirm

A box that asks "Are you sure?" feels safe and isn't. Asked often, it trains people to press Yes without reading, so it fails at the one moment it was for. Better to just do the thing and offer an easy undo. Apple's guidance warns only when a loss is both unexpected and permanent: the Finder doesn't ask when you throw a file away, because that is what you meant, and the bin gives it back.

So the craft is:

- **Make it undoable, and then don't ask.** Archive instead of erase. Show the deleted item leaving, so people see where it went: Family's deleted items tumble into a bin.
- **Give the undo time.** An undo note that vanishes after four seconds fails anyone who reads slowly or uses a screen reader. Keep it until the next action, or long enough to be noticed, and pause it while the page is hidden.
- **Confirm only what truly can't come back,** like closing an account or sending money. Then name the action on the button: "Delete 14 photos", not "OK". Say what will be lost.
- **Keep destructive actions quiet until the moment.** "Delete" or "Cancel subscription" is not the page's main action, so it is not a big red button. It can be a plain link. It becomes the strong red button only inside the step that confirms it.

## Conventions, and when to break one

People arrive knowing how screens work: the logo goes home, underlined text is a link, Back takes you back. Every convention kept is something nobody has to learn. Within one product the rule holds harder: things that look the same must behave the same.

Breaking one is worth it when the new way is plainly better, findable, and the old way still works. Things 3's plus button is the shelf's best case: tap it for a new to-do, or drag it to the exact spot the to-do belongs. Nothing was taken away. The bad break is done to look different: a menu behind a mystery gesture, with nothing in its old place.

## How it goes wrong

- **The happy path only.** Every screen full, fast and correct. Fix: draw the empty, loading, error and too-full versions in the rough stage.
- **A spinner for everything.** The same wheel for a quarter-second save and a two-minute export. Fix: nothing under a second, a skeleton for content, real progress for long jobs.
- **Errors that blame.** "Invalid input", red everywhere, the form cleared. Fix: say what to do, keep what they typed.
- **A design that only works with perfect data.** Fix: design with the longest name, the biggest number and the empty list.

## What a strong designer would notice

- A screen shown only full, with no empty or error version beside it.
- A first-use screen that is the full screen with nothing in it.
- A spinner on something that takes less than a second.
- A button that can be pressed twice while it works.
- Hint text inside a field standing in for its label.
- An error message that says what is wrong but not what to do.
- A form that clears itself after an error.
- "Are you sure?" on something that could have been undone.
- A red "Delete" button as loud as the page's main action.
- Something only discoverable by hovering, on a screen meant for phones.
- A layout that breaks on a long name or a big number.

## More details

- **Not yet drawn on:** *The Design of Everyday Things* by Don Norman (being captured in another session) and *Don't Make Me Think* by Steve Krug (out November 30). Both matter here, especially for signifiers and conventions; revisit this brief when their notes exist. The words "affordance" and "signifier" are used in their common sense, in the studio's own words.
- **Book, in the studio's own words:** *Refactoring UI* by Adam Wathan and Steve Schoger, private notes in `designcraft/library/books/refactoring-ui/`: the video lesson on a complex form (labels near their own fields, input width as a hint, ranked buttons, a quiet cancel link), the video lesson on a dashboard (subtle buttons where links stop looking clickable, the whole card as the target), the finishing-touches chapter (empty states as first impressions, hiding idle filters), and the hierarchy chapter (destructive actions stay quiet until the confirming step).
- **Read today, November 17, 2026:**
  - Nielsen Norman Group, "10 Usability Heuristics for User Interface Design", Jakob Nielsen, 1994, last reviewed January 30, 2024 (visibility of status, user control and undo, consistency, error prevention, recognising and recovering from errors): https://www.nngroup.com/articles/ten-usability-heuristics/
  - Nielsen Norman Group, "Response Times: The 3 Important Limits", Jakob Nielsen (0.1, 1 and 10 seconds; spinners as a last resort; flicker for short waits): https://www.nngroup.com/articles/response-times-3-important-limits/
  - GOV.UK Design System, error message component (two places, same words, the question's words, words to avoid, keep input, no errors for eligibility): https://design-system.service.gov.uk/components/error-message/
  - GOV.UK Design System, validation pattern (check on Continue, not on leaving a field; accept spaces and punctuation; live checking only with research behind it): https://design-system.service.gov.uk/patterns/validation/
  - GOV.UK Design System, text input component (labels above, no placeholder as label, widths that match the answer): https://design-system.service.gov.uk/components/text-input/
  - Apple Human Interface Guidelines, Feedback (passive status, alerts only for critical news, warn only for unexpected permanent loss, the Finder example), read from Apple's page data: https://developer.apple.com/design/human-interface-guidelines/feedback
  - WCAG 2.2 quick reference, W3C: 3.3.1 Error Identification, 3.3.3 Error Suggestion, 3.3.4 Error Prevention (reversible, checked or confirmed), 2.2.1 Timing Adjustable: https://www.w3.org/WAI/WCAG22/quickref/
- **Shelf examples:** `designcraft/research/govuk-check-uk-visa.md` (button signifiers, Change links, errors in two places), `family-wallet.md` (one changing panel, 100 and 200 millisecond feedback, the 360 millisecond tap guard, the bin), `things-3.md` (the plus button), `linear-app.md` (100 and 250 millisecond motion), `duolingo-app.md` (the key-like button).
- **Craft salvaged from skills:** the Impeccable skill's harden guidance (extreme inputs, translations about 30% longer, partial failure, double presses, optimistic updates) and onboard guidance (kinds of empty state, first use); `emil-design-eng` (press feedback of 100 to 160 milliseconds, pausing toast timers when the tab is hidden); `apple-design` (respond on the press, confirmation only for the truly permanent).
- **A disagreement between sources:** the `apple-design` skill says to check fields inline rather than on submit; GOV.UK says to wait until the person presses Continue and not to check on leaving a field. This brief sides with GOV.UK, which publishes the research reason (slow typists), and keeps live checking for cases like a character count.
- **The placeholder finding** is from Designcraft's own test of the three checks, written up in `designcraft/tools/checking-a-design.md`.
