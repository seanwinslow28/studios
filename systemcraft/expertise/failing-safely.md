# Failing safely

Read this when a design has its shape and its tools, and before anyone calls it finished. Every part of a system built around a model will fail at some point: the model returns rubbish, a tool hangs, a loop won't stop, a service it leans on is down. The design decides what happens next. In a good one a failure is small, somebody finds out, and the work stops at a person or at a safe place.

## How these systems fail differently

Ordinary software mostly fails loudly. A system built around a model has four habits that ordinary software doesn't:

- **It fails politely.** The answer is wrong and reads well. The agent says the job is done when it isn't.
- **It isn't the same twice.** A run that worked yesterday can fail today with nothing changed.
- **It can be talked into things,** by a user or by text it reads.
- **It loops.** Given a failing step and no limit, it tries again, and again, and bills for each try.

So the usual question, "did it raise an error?", is the wrong one. Most of this brief follows from that.

## Success means the work got done

A step can run, finish and report success, having made nothing. So the question for every stage is how much it made, not whether it complained.

Sean's own audit of his overnight agents turned on exactly this: it counted the work that got done, not the green lights. The post-mortem on the shelf shows the same gap from the other side. A fault passed human review, automated review, small tests, full tests and in-house use, and users still felt it for weeks. One person's overnight set-up, also on the shelf, had a nightly job break with no signal and run blind for days.

What this asks of a design:

- Every stage that makes something reports how much. Nothing made is treated as a failure, unless the design says an empty night is normal.
- "Done" comes with proof the system can't write for itself: the thing itself, run or opened, or a test it doesn't control.
- After a repair, the evidence is what the next run made, not the fact that it started.

## An alarm has to reach a person

Noticing a failure and telling someone are two separate things, and a design must cover both.

- GitLab's nightly backups had been failing. The system did send failure emails. The receiving mail server rejected them, so nobody saw one. The alarm rang in an empty room.
- Sean's audit found the same kind: the watchdog spotted the failure and wrote it to a file nobody reads.

For every alarm in a design, name the person, the place they will see it, and how the path gets tested. An alarm that has never once been received is a guess. An alarm that rings too often goes the way of an approval prompt that appears too often: people stop reading it. So a false alarm is a fault to fix, not a nuisance to live with.

## Limits on everything that can grow

Anything in the design that can repeat or pile up needs a ceiling set outside the model:

- **Time.** Every call to a model or a tool has a time limit. Without one, a hung call holds up everything behind it.
- **Tries.** A capped number of retries, with a pause between them. A blind retry hammers a service that is already struggling.
- **Rounds.** Stripe allows two rounds of the full tests, then hands over to a person. It says more rounds bring little.
- **Turns and spend.** A limit per run on both.
- **Size.** A cap on how much a tool may return, and on how long a queue may get.

When a part keeps failing, stop calling it for a while instead of trying harder. Engineers call this a circuit breaker, after the switch that cuts the power when a wire overheats. For a model-based step it means: after so many failures in a row, stop, record it, and tell someone.

## Keep a failure from spreading

- **Walls between parts.** One part failing shouldn't take the rest with it. Separate memory for each helper, separate folders, separate keys.
- **Fail fast.** A step that can tell early that it can't succeed should say so at once, not after ten minutes.
- **Check the basics first.** In Anthropic's long-job design, every new session starts by running one basic test, to catch anything the last session broke before building on top of it. Stripe runs its five-second checks before its slow ones.
- **Be suspicious of "everything is broken".** When a monitor reports that nearly the whole system is down, the monitor is the first suspect. Automation that acts on that report, by restarting or deleting, can do more harm than the fault.

## Every path ends somewhere

Follow each way a step can fail and see where it leads. It should end at a person or at a safe stop. It should never end nowhere.

- **A route to a person, always.** Klarna's answer, fifteen months on, wasn't a better model. It said it wanted a person always on offer, and began a pilot with a human team.
- **An honest "I don't know".** A system that can decline is safer than one that must always answer.
- **A fallback that is decided in advance.** When the model is slow or down: a simpler model, a saved answer, a queue for later, or a plain "not now". The worst fallback is the one the system makes up.
- **A stopping place that leaves things tidy.** Work saved, a note on where it stopped, nothing half-written.

## Undo, backups and the stop switch

- **Anything that deletes can be undone** for a while. The hosting company on the shelf now holds every delete for 48 hours.
- **A backup counts only once it has been restored.** GitLab's nightly backups had been failing, and it found out on the day it needed one.
- **A stop switch counts only once it has been used.** If nobody has ever tried it, the design doesn't have one yet.

Safety parts are easy to lose. They are rarely used, so they look like waste, and they get trimmed. Donella Meadows makes the point about every kind of system: strip out the emergency mechanism and the system survives a narrower range of trouble. A design should mark these parts as not for trimming.

## How failures really happen

Richard Cook's short essay on complex systems is the best corrective to tidy thinking. In the studio's words:

- A working system is always running with some faults in it. People and safeguards cover for them.
- A big failure is several small faults lining up, never one cause.
- Looking back, the cause seems obvious. It wasn't at the time.
- The people closest to the work are what keep it safe, by noticing and adapting.

Two things follow. A design shouldn't promise that failures won't happen; it should say how they will be noticed and contained. And when something does break, "the model made a mistake" or "someone slipped" is where the looking starts, not where it ends. Ask why the set-up accepted the slip and made it bigger.

## Where it goes wrong

- **Green lights over no work.** Fix: count output.
- **An alarm nobody receives.** Fix: name the person, test the path.
- **An alarm that always rings.** Fix: treat the false alarm as a fault.
- **A loop with no ceiling.** Fix: limits on tries, rounds, turns and spend, outside the model.
- **Retrying harder.** Fix: stop, pause, tell someone.
- **A failure path that ends nowhere.** Fix: walk every path to a person or a safe stop.
- **A backup or stop switch never tried.** Fix: try it, and write down the date.
- **"The agent said it was done."** Fix: done needs proof the agent can't edit.

## Examples

All on the shelf. **The Claude Code post-mortem** is green tests over a real fault, with GitLab's unheard alarm beside it. **The nine-second deletion** is the missing undo. **Klarna's walk-back** is the route to a person, moved to the centre of the product. **Stripe's Minions** is the hard stop after two rounds. **The long-job harness** is the basic test at the start of every session.

## What a strong system designer would notice

- A health check that only asks whether an error was raised.
- An alarm with no named person on the other end.
- A retry with no cap.
- A step that can hang forever.
- A failure path that just stops.
- A backup that has never been restored.
- A safeguard described as "probably not needed".
- One cause given for a failure that needed three things to line up.

## More details

- Figures and cases come from the shelf entries in `systemcraft/research/`, which list their sources: `claude-code-april-2026-post-mortem.md` (the fault that passed every check, GitLab's backups and emails), `stripe-minions.md` (two rounds, fast checks first), `klarna-assistant-walk-back.md`, `nine-second-database-deletion.md` (the 48-hour hold), `anthropic-long-running-harness.md` (the basic test each session), `project-vend.md` (the one-person overnight set-up, in its side-by-side), `lethal-trifecta-and-camel.md` (worn-down approvals).
- What Sean's own audit did well is on the shelf's guide, `systemcraft/research/README.md`, in words safe to share. Its records stay private.
- Richard Cook, "How Complex Systems Fail": https://how.complexsystems.fail/
- Donella Meadows, "Leverage Points: Places to Intervene in a System": https://donellameadows.org/archives/leverage-points-places-to-intervene-in-a-system/
- Fundamentals, in the studio's own words: Michael Nygard's *Release It!* (second edition), borrowed from Devcraft, for time limits, capped retries, circuit breakers, walls between parts, failing fast, and doubting a monitor that says everything is down.
- What a design can count on from a scheduled overnight run is in Devcraft's guide, `devcraft/tools/launchd.md`.
