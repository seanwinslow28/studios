# Building small software that stays easy to change.

Read this when a job reaches the making: writing new code, changing old code, or saving the work as commits.

## What good looks like.

Good code is cheap to change next time, by Sean in six months, the next agent, or a stranger. The enemy is complexity: anything that makes code hard to understand or change. It shows when one small change needs edits in many places, or a reader has to hold too much in their head. It rarely arrives as one big mistake. It piles up from small shortcuts, so a little design effort on every change beats a cleanup later, which almost never happens.

## Small steps, one hat at a time.

- **Refactor first, then change behaviour, never both at once.** A refactor changes the shape of code without changing what it does. When the code fights a change you want, reshape it first until the change is simple, commit that, and only then make it. Mixed together, a failing test won't say which half broke it, and a reviewer can't spot the behaviour change hiding among the moves.
- **Steps small enough to throw away.** If a test goes red mid-refactor, throw the step away, return to where everything passed, and try a smaller one.
- **Runnable at every commit.** Each saved change leaves the thing working. Then any commit can be undone on its own, or found by `git bisect` (a git command that halves through history to find the commit that broke something).
- **Change what others depend on in three moves.** Add the new form beside the old, move callers over one at a time, then remove the old. This is called expand and contract. uv's patch-upgrade design works this way: the new Python arrives, project folders move to it, and the old copy stays because something might still use it. For a scheduled job: add the new Python, point the job at it, watch it run overnight, and only then retire the old path.

## Deep modules, simple interfaces.

A module is any piece with an inside and an outside: a function, a file, a script. Its interface is what a caller must know to use it. A deep module hides a lot behind a small interface. uv's minor-version folder is a clean example: everything points at "3.12" and never learns which bug-fix release sits underneath, so an upgrade moves one pointer and nothing else notices.

A shallow module makes the caller learn almost as much as it saves them. The tells:

- **Pass-through functions** that take the same arguments as the function they call and add nothing.
- **The same knowledge in two places,** such as a file format or folder layout that two pieces both have to get right. Give it one owner.
- **Pieces named after steps in time** (fetch, parse, write) that secretly share the same knowledge. Group by what each piece knows instead.
- **Options only edge cases need** on the main call. Give sensible defaults and put rare options elsewhere.

When a hard case could be handled inside the module or by every caller, the module takes it. Before adding a setting, ask whether the person setting it really knows better than the code; if not, let the code work it out. Split a function when one part is a separate job you can name, not because it's long.

## Names and comments.

- **Names say exactly what a thing is or does.** "data", "info", "manager", "handler" and "result" say nothing. If no crisp name comes, the piece is probably doing two jobs; a name with "and" in it certainly is.
- **Comments say why,** and whatever the code can't say for itself: units, limits, who owns a file, why the odd choice was made. Wanting a comment to explain a block usually means that block wants to be a function with a good name.
- **Comments and docs change in the same commit as the code.**

## Errors.

- **Define errors out of existence where you can.** Design so the bad case can't happen, or isn't an error. Deleting a file that's already gone is a success, because the goal was "not there". Python's `Path.mkdir(parents=True, exist_ok=True)` makes sure a folder exists instead of failing when it already does. uv's pointer doesn't handle "my Python vanished"; it makes that failure impossible.
- **Fail loudly when you can't.** A rare case with no sensible recovery should stop with a clear message: what happened, what it was trying to do, which file. `except Exception: pass` is the classic way to turn a crash into silent wrong behaviour.
- **Fail closed.** If a safety check itself breaks, the action doesn't go ahead.
- **Leave nothing half done.** Write to a temporary file and rename it into place, so a crash leaves the old version whole.
- **Silence is the worst failure for a scheduled job.** A job that quietly stops is the first job's whole problem. Exit with a non-zero code on failure and log a line in a known place, so launchd (the macOS scheduler) and Sean can both see it.

## Calls that can hang.

- **Every call to another program or over the network gets a timeout.** Python's `subprocess.run` waits forever unless given `timeout=`, and so does the popular `requests` library.
- **Retries are few, spaced out and in one place.** Wait longer after each failure (exponential backoff), add a little randomness so retriers don't collide again (jitter), and cap the count. Retry at one layer only: a retry loop around a library that already retries multiplies the attempts.
- **Only retry what's safe to repeat.** A call is idempotent when running it twice does the same as running it once. Don't retry errors that will never succeed, such as bad input.
- **Put a limit on everything:** loops, queues, result sizes, log files. Release It! is the classic source on these stability habits.

## Secrets and dependencies.

- **Secrets are read by name at run time.** The code asks for `os.environ["API_TOKEN"]` or reads the macOS keychain; it never holds the value. The value never appears in code, a commit, a log, an error message or a test (tests use a fake). If a secret is missing, stop at the start and say which one, never what it holds.
- **No new dependency without a reason.** Every package is code you don't control and will have to upgrade. Check whether the standard library already does it, who maintains the package, and whether it really exists: AI tools sometimes invent package names, and attackers register them. Pin exact versions in a lockfile (`uv.lock`) so every install matches.

## Code smells and the fix for each.

A smell is a surface sign that something deeper may be wrong. The Refactoring book catalogues them; these come up most in small tools.

- **Mysterious name.** Rename it until the name says what it does.
- **The same code a third time.** Pull it into one function.
- **Long function.** Pull out the pieces and name each for what it does.
- **Shared data anything can change.** Wrap it so every change goes through one place.
- **One change touching many files.** Move the scattered pieces together.
- **`True` or `False` passed to change what a function does.** Make two functions.
- **Hooks for a future that never came.** Delete them.

Ugly code that works, doesn't need changing and sits behind a clean interface can stay as it is.

## Good commits.

- **One idea per commit, with its tests and its docs.** Simon Willison's "perfect commit" packs the change, the tests that prove it, the updated instructions and a link to the reason into one.
- **The first line says what changed,** plainly, and makes sense alone in a log. "Fix bug" and "WIP" say nothing.
- **The body says why and how you know.** Dan Carley's one-character commit puts the exact error text in the note, so anyone who hits it later finds the fix by searching. Lead with one plain sentence, though, then tell the story.
- **Tidying goes in its own commit,** before the behaviour change. Google's small-changes guide puts a reasonable change at about 100 lines and calls 1,000 usually too big.

## Where it goes wrong.

- **The smallest patch, every time.** Each quick fix is reasonable alone; the pile isn't. Fix: leave each change's surroundings a little simpler than you found them.
- **A refactor and a behaviour change in one commit.** Fix: split them, refactor first, and run the tests between.
- **A broad `except` that hides failures.** Fix: catch only what you expect and can handle; let the rest stop loudly.
- **Swapping a path the overnight job relies on in one move.** Fix: expand and contract, and watch it run before removing the old.

## Examples.

All on the shelf in `devcraft/research/`. **uv's patch upgrades** show a deep module, an error designed out instead of handled, nothing removed that might still be used, and a deliberate opt-out for anyone who asks for an exact version. **Willison's and Carley's commits** show two ways to leave a full record: the story in a linked issue, or in the commit note. **Google's small-changes guide** covers why small, how small, and five ways to split.

## Tools.

Ruff tidies Python and Pyrefly catches mistakes before it runs; ShellCheck and shfmt do the same for shell scripts; pytest runs the tests; Betterleaks scans each commit for secrets. Their guides live in `devcraft/tools/`.
