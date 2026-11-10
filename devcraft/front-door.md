# Devcraft's front door

What this studio's front door adds to the shared front-door guide in craftwork's guides folder. The shared guide sets the method; this page says only what software work needs on top.

**Where the job lives.** The code changes on a branch of the repo being changed, never on its main line. The job's own notes (the ask, the decisions, the review pages) go in a folder named `<job>-<date>` inside Sean's Devcraft jobs folder, whose path is in `devcraft/folders.local`, which git ignores. If that file is missing, ask Sean for the path. A job on anything private to the Mac Mini keeps its branch and its notes on the Mini.

## What the ask must pin down

In this order, one question each, until every answer is a named specific:

1. **The problem, and the proof it's fixed.** What goes wrong today, in one sentence, and the one thing Sean will see working when it's done: a test that fails now and passes then, or a run he can watch. "It works better" isn't an answer yet.
2. **Where it runs and what leans on it.** Which machine, what starts it (Sean by hand, a schedule overnight, an agent), and what else depends on it. What happens today when it fails: loudly, or silently.
3. **What's already there.** The code, scripts or settings it touches, any earlier attempt, and the evidence of the problem: a log, an error, the date it last broke. Look before asking; ask only for what the files can't tell you.
4. **What must keep working, and the way back.** Everything in use that the change must not break or delete, and how it gets undone if it goes wrong. A change with no way back isn't ready to plan.
5. **The limits.** Time, money, and any tool or route Sean named, which becomes a must-have. Whether anything here is private to the Mac Mini.
6. **What this is not.** The bigger rewrite it would be tempting to do, and the nearby problems left for another job, named so they're easy to rule out.

## What good looks like here

- **The shelf first:** `devcraft/research/`. uv's "upgrade without breaking" design is Sean's pick and the current focus: one small mechanism, nothing deleted that might still be in use, and honest notes on where it stops.
- **Then where well-made small changes are shown:** the change history of mature tools that solve the same kind of problem (uv, Homebrew, git, the tool being changed), public write-ups of outages and their fixes, and well-known guides to small changes and good commits.
- **Measure, don't admire:** how big the change is in lines and files, how it's tested and what the tests would catch, what it left in place, how it's undone, and how plainly it says where it doesn't help.

## What the front door leaves to the job

- **No approach chosen.** Name the options Sean raises, but pick between them in step 3, once the examples are in.
- **No code, no test list, no plan of steps.** The proof is named in words; the tests that hold it are written in step 3.
- **No new tools** beyond the ones Sean named or the studio's tool list.
