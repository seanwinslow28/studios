# Planning a change.

Read this before changing anything already working: a script, a scheduled job, a settings file. A good plan is short. It says how big the change is, the order it lands in, which approach and why, what could break, and the way back.

## Sizing: small enough to read and undo.

A change is small when one reader can understand it in a sitting and undo it without dragging anything else along. Google's small-changes guide gives a rough number: about 100 changed lines is usually fine, about 1,000 is usually too many, and the same lines spread across many files count as bigger. Of its eight reasons for small changes, the last matters most here: a small change is simpler to roll back.

Lines aren't the only measure. A change is too big when its description needs "and also", when it mixes tidying with new behaviour, or when undoing one half would undo the other. Do the tidying first, as its own change, so the change that matters lands on ground already cleared (Kent Beck's well-known advice). Keep the tests in the same change as the code they prove.

How much care a change deserves depends on how long the code will live. A script run once by hand needs little. A job that runs nightly with nobody watching needs the most, because nobody notices when it breaks.

## Slicing: every step leaves things working.

Split the work into steps that each land alone, pass the tests, and could stay if the work stopped there. A step that leaves things half-broken until the next one lands is really half a step.

Three cuts cover most small software:

- **Prepare, then switch.** First teach whatever reads a file or setting to accept the new form, while everything still writes the old one. Nothing visible changes, so it's safe to undo. Then switch the writers. Undoing the switch stays safe, because the readers understand both. The AWS Builders' Library calls this a two-phase deployment.
- **Add, move, remove.** Add the new way beside the old, move each user across, then remove the old way once nothing uses it. Martin Fowler's site calls this parallel change, or expand and contract. The removal isn't optional. Skip it and you keep two ways forever.
- **Put one door in front.** When swapping out something many parts use, first route every caller through one small interface, then build the new thing behind it, then switch callers over. This is known as branch by abstraction.

Put the riskiest question first, while backing out is still cheap. For Devcraft's first job, that means proving one scheduled job runs on uv's Python before touching the rest.

## Choosing between approaches.

Sketch at least two approaches that differ in kind, not detail, before picking. Setting the first idea beside a real alternative shows what it costs, a case A Philosophy of Software Design makes well. Then prefer:

- **The simplest thing that works.** Fewer moving parts, nothing built for a need nobody has.
- **Deep modules.** A good piece of code hides a lot behind a small interface. One function that makes sure a job runs on a pinned Python beats five helpers the caller must call in the right order. When a piece's interface is about as long as the work it does, it isn't earning its place.
- **Information hiding.** Each piece of knowledge, such as a file format, a folder path or the order things must happen in, lives in one place. If two parts of the code both know where uv keeps Python, moving that folder breaks both.
- **Prevention over repair.** uv's patch upgrades are the model. A patch release is a bug-fix version, like 3.12.10 to 3.12.11. Older tools such as pipx rebuild broken project folders after the fact. uv keeps one pointer per minor version and moves only that pointer on upgrade, so the failure never happens.

A sign the approach is wrong: you can't name the new piece crisply, or describing it keeps needing "and also".

## What could break, and the way back.

Write down what could go wrong before building, not after. For each step, say:

- **What it changes:** files written, jobs loaded, settings changed.
- **What undoes it,** as a command, and whether that command has been run. An undo nobody has tried is a hope.
- **What can't be undone.** Some doors only open one way: deleting the old Python, rewriting stored data in a new format, telling another system something. Name these and put them last, after everything reversible has proved itself.

Cloudflare's 2019 outage shows the undo has to be fast as well as correct. The normal undo was too slow while sites were down, so the team used a blunter switch that turned the feature off everywhere. uv shows the other half: after an upgrade it keeps the old Python, because something might still use it. Keeping the old thing until the new one proves itself is often the whole way back.

Terraform's plan-then-apply is the model for a change to the system. A preview changes nothing and ends in a one-line summary. The apply does only what the preview showed, and refuses if things moved in between. A preview must skip the risky part entirely. Cloudflare's rule went out in a "simulate" mode that still ran the costly matching, and that's what took the servers down.

## Deciding what is a breaking change.

A change breaks someone when something they relied on behaves differently. So first decide what's public. For a script or job, that's its options, its settings and their names, its exit codes, its output files and their format, and where it puts things. An exit code is the number a program hands back when it finishes, and for a scheduled job it's often the only signal anyone reads.

Semantic versioning puts this in numbers, as major.minor.patch. A patch fixes bugs without changing anything public. A minor adds something without breaking what's there. A major is anything that breaks. uv's design leans on that promise: it moves project folders from 3.12.10 to 3.12.11 on its own, but going to 3.13 can change which add-ons work, so that stays a deliberate step.

Mind Hyrum's Law: once enough things use a tool, every behaviour they can observe gets relied on, written down or not, from log wording to the exact path of a file. When jobs and agents read each other's output, the users are scripts, and scripts don't adapt. Treat any change to visible output as possibly breaking.

## Making operations safe to run twice.

Anything a scheduled job does may run twice: after a crash, a restart, or someone rerunning it to check. An operation that's safe to repeat, called idempotent, leaves the same end state the second time. Write "make sure this is true" rather than "do this". "Make sure this folder points at Python 3.12" can run a hundred times. "Add a line to this file" adds a hundred lines.

The habits that get you there:

- **Check before acting,** and do nothing if it's already done.
- **Give each piece of work a stable name** taken from what it is, not when it ran, so a rerun finds its own earlier output.
- **Write to a temporary file, then rename it into place.** On the same disk the rename happens all at once, so a run cut off halfway never leaves a half-written file.
- **Report "nothing to do" as success,** not as an error, so the second run exits cleanly.

## Settings and their defaults.

Every setting is a question put to whoever runs the tool, and the best number of questions is zero. Work things out from the machine where you can. Where a setting must exist:

- **The default is the safe choice.** Anything destructive previews by default and acts only when told to.
- **Unknown settings are rejected,** so a misspelt name fails loudly instead of being quietly ignored.
- **Values are checked for meaning, not just shape.** Does that folder exist? Is that Python installed?
- **A setting nobody would change is a dodged decision.** Make it.

uv's `python-preference = "only-managed"` is a default worth changing on purpose. Without it, uv will use Homebrew's Python if it finds one first, which is the exact failure the first job exists to stop.

## Where it goes wrong.

- **One big change, or a step that leaves things broken.** Fix: re-cut at the cuts above until each step stands alone, tidying first.
- **The first idea, built.** Fix: sketch a different second one and compare.
- **An undo nobody ran.** Fix: run it on a throwaway copy before the real thing.
- **A one-way door in the middle.** Fix: move it to the end.
- **A preview that does the risky part.** Fix: the preview only reads.
- **Changed output nobody counted as public.** Fix: list what's public before starting.
- **A job that does damage on its second run.** Fix: "make sure", not "do", and test running it twice.

## Examples.

- **uv's patch upgrades** (`devcraft/research/uv-python-patch-upgrades.md`): one pointer, nothing deleted that might be in use, a deliberate opt-out, limits written down, and eight months behind a trial switch before becoming the default.
- **Google's small-changes guide** (`devcraft/research/google-small-changes-guide.md`): five ways to split a change.
- **Terraform's plan-then-apply** (`devcraft/research/terraform-plan-then-apply.md`): a preview with exit codes a script can read, and an honest note that a preview is not an undo.
- **Cloudflare's 2019 outage** (`devcraft/research/cloudflare-2019-outage-rollback.md`): an undo too slow to use, and a preview that wasn't safe.
