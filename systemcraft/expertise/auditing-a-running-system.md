# Auditing a system that is already running

Read this when the job is not a new design but a system that already exists: Sean asks whether it is working, why it feels worse, or what to fix first. An audit is a design job run backwards. It starts from what the system did, not from what it was meant to do. A good one ends in a short list: what is broken now, how that is known, and what to do first.

## Start from Sean's own audit

The studio's best example is its own. In August 2026 an earlier version of this studio audited Sean's overnight agents. Four things it did are the method:

- **It went to the running machine and measured,** before forming a view.
- **It kept "the system noticed" apart from "a person was told".**
- **It counted the work that got done,** not the green lights.
- **It tested its own first answer,** and said so when that answer was wrong.

The rest of this brief is those four, spelled out with the public cases on the shelf.

## Look first, think second

The pull is to read the design, form a theory and go looking for proof. Resist it. Go to the system and see what it has produced, run by run, for as long back as records go. Only read at this stage; change nothing.

Hamel Husain's field guide on the shelf is the same move for a product: collect real runs, read each one whole, write a note on each failure, group the notes, count the groups. By its founder's account, one team that did this found that requests involving dates were handled right only 33% of the time. They fixed that one thing and reached 95%.

The count orders the work. Without it, the fix list is ordered by whatever was most recent or most annoying.

## The questions an audit asks

In roughly this order, because each can make the later ones pointless. Each comes from a case on the shelf.

1. **Is it running at all?** Check every scheduled run across the whole period. One person's overnight agents had a nightly job break with no signal and run blind for days.
2. **Is it making anything?** Count what each stage produced. Running is not the same as producing.
3. **Is anyone using what it makes?** Follow the output to the person it is for. Honeycomb judged its assistant by whether teams kept using the product.
4. **When it fails, is a person told?** Follow each alarm to the place a person would see it. GitLab's failure emails were sent, and rejected on the way.
5. **Do its checks agree with a person?** Take a handful of what a checker flagged and a handful it passed, and judge them by hand. Shopify's grader agreed with human experts barely better than chance until it was tuned.
6. **What has changed around the model?** Settings, instructions, limits, versions. Get the dates.
7. **What can talk it into things?** Which look-ups are required, and which are left to its judgement? Is its "manager" a real check, or the same model again? These are the shop's questions.
8. **Which rules does the machinery enforce, and which are only asked for?** By its founder's account the deleted database had an instruction against it, and nothing else stood in the way.
9. **Has the undo, or the backup, ever been tried?**
10. **What does it cost for each piece of real output?**

## Two kinds of blind spot

The post-mortem on the shelf and its side-by-side give the two ways a failing system hides, and an audit should look for both.

- **The tests couldn't see it.** Claude Code got worse for weeks because of three small changes to the set-up around the model. The company's own tests said it was fine. One of the three passed human review, automated review, small tests, full tests and in-house use.
- **The alarm rang in an empty room.** GitLab's backups were failing, and the system was sending failure emails that a mail server rejected. Nobody saw one.

A green check is a claim, not proof. An alarm that fired is not a person who knows.

## The dials around the model are part of the system

When a system gets worse, the model is the first thing blamed and often the last thing at fault. In the Claude Code case the model hadn't changed. The three causes were a lower default for thinking effort, a clean-up step that ran on every turn by mistake, and a new instruction capping the length of replies.

So an audit lists every dial: how much the model is shown, what gets cleared and when, the limits, the instructions, the tool list, the model version. Then it asks which moved, and when, and sets those dates beside the dates the complaints began.

## Pinning down a cause

- **Find the first thing that went wrong,** not the last. The last failure in a chain is usually a symptom.
- **Pin each cause down alone.** The Claude Code team removed instruction lines one at a time, on a wider test, until the drop in quality showed. Undoing three changes together would have fixed the problem and taught nothing.
- **Test your own first answer.** A first explanation is a guess until something has been tried that would show it wrong. Say so plainly when it turns out wrong.
- **Say what was not checked.** Every entry on the shelf ends with what could not be confirmed. An audit should too.

## Where to push

Donella Meadows ranked the places to change a system from weakest to strongest. The weakest, and the one people reach for first, is the numbers: a threshold, a retry count, a limit. Stronger moves sit higher up: who can see what, what the rules are, what the system is really steered by.

For an audit this is a sorting tool. If a system's settings have been changed three times and it still misbehaves, the fault is higher up. The cheapest strong fix is very often information: put the count of real output, and the failures, where the person already looks each day.

The other warning from the same essay: people often find the right place and push it the wrong way. When something has gone wrong, the urge is to add a rule, a step or another agent. Ask first whether something should come out.

## Writing it up

- **Open with one plain page.** What is broken now, what to do first, in order. The detail sits behind it.
- **Each number says how it was counted, and whose it is.** The shelf marks a maker's own number as the maker's own. An audit holds its own numbers to the same standard.
- **One fresh check, for facts.** A reader who didn't do the audit goes through the claims against the records. When the shelf itself was checked this way, the checker found 41 problems, six of them plainly wrong.
- **Then check the repair.** After a fix goes in, look at what the next run made.

## Where it goes wrong

- **A theory before a look.** Fix: read the records first.
- **Trusting the green lights.** Fix: count what was made.
- **Stopping at "the system noticed".** Fix: follow the alarm to a person.
- **Blaming the model.** Fix: list the dials and their dates.
- **Undoing everything at once.** Fix: one change at a time.
- **Reporting the first answer untested.** Fix: try to show it wrong.
- **Numbers only the auditor has seen.** Fix: one fresh check.
- **No plain first page.** Fix: what is broken, what to do first.

## Examples

**Sean's own audit** is the method, and its records stay private. On the shelf: **the Claude Code post-mortem** is the best published audit of a running system, with **GitLab's outage** beside it. **Husain's field guide** is reading the real runs and counting. **Project Vend** is a system examined, fixed, and broken again by outsiders, with the questions to ask of anything left to run by itself. **Klarna's walk-back** is what an audit of the measures might have caught early.

## What a strong system designer would notice

- A conclusion reached before anyone looked at a real run.
- "It's running" offered as the answer to "is it working?"
- A success count that would be the same if nothing had been made.
- An alert that nobody can remember receiving.
- A checker whose findings nobody has ever checked by hand.
- "The model got worse" with no list of what else changed.
- Three fixes applied together.
- A write-up that doesn't open with what is broken now.

## More details

- What Sean's own audit did well is on the shelf's guide, `systemcraft/research/README.md`, in words safe to share. The readout and records are private; `systemcraft/folders.local`, which git ignores, says where they are on this Mac. This brief uses only those four public points.
- Figures and cases come from the shelf entries in `systemcraft/research/`, which list their sources: `claude-code-april-2026-post-mortem.md` (the three changes, the fault that passed every check, removing lines one at a time, GitLab's emails), `husain-field-guide-nurtureboss.md` (33% to 95%, Shopify's grader), `project-vend.md` (the shop, and the one-person overnight agents in its side-by-side), `honeycomb-query-assistant.md`, `nine-second-database-deletion.md`, `klarna-assistant-walk-back.md`. The fresh check of the shelf is in `systemcraft/research/README.md`.
- Donella Meadows, "Leverage Points: Places to Intervene in a System": https://donellameadows.org/archives/leverage-points-places-to-intervene-in-a-system/. All rights are reserved on it; the studio keeps only its own notes.
- How to read a saved record of a run is in `systemcraft/tools/transcripts-and-phoenix.md`.
- Fundamentals, in the studio's own words: Shankar and Husain's *Evals for AI Engineers* (reading real runs, noting the first failure, counting), and Michael Nygard's *Release It!*, borrowed from Devcraft (how running systems hide their faults).
