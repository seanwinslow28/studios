# Where a person steps in

Read this when a design decides what the system does alone, what it asks about, and what it hands back. Every system built around a model has a person in it somewhere: setting it up, reading what it made, catching what it got wrong, taking over when it can't go on. The design chooses where. A good one puts the person at the few points where they change the outcome, gives them what they need to act when they get there, and asks for nothing else.

## It is not one dial

"How much should it do by itself?" has no single answer. For each kind of action, a design picks one of five:

- **Suggest,** and the person does it.
- **Ask first,** and act on a yes.
- **Act unless stopped,** with a window to say no.
- **Act, then report.**
- **Just act.**

The choice turns on what a mistake costs and whether it can be undone, not on how capable the model is. One system can sit at "just act" for tidying its own records and "ask first" for sending anything out.

## Put the person where it counts

The shelf shows four good places, each chosen for a reason.

- **As the check, at the end.** Honeycomb's assistant writes a query the user can see, edit and undo. Nothing the model writes can break anything, so no approval step is needed at all.
- **At the one costly choice.** Uber's version of the same product stops for the user to confirm which tables to use, because the wrong table is the expensive mistake. Nowhere else.
- **At both ends, never the middle.** Stripe's coding system takes a request and returns a finished change. A person reviews every one before it is merged. Nobody steers in between.
- **First and last.** In the partner study, the person writes the first idea and the final words. The model works in between.

The weak place is everywhere: an approval prompt on every step. The authors of the safety design on the shelf say frequent requests wear people down until they approve everything. A prompt nobody reads is worse than none, because it looks like a safeguard.

## The watcher trap

The most tempting design is this one: the machine handles the work and taps a person when there is trouble. It fails for reasons that have nothing to do with the model.

- **People can't watch a thing that mostly works.** Attention to a steady, quiet task fades within about half an hour. A design that depends on a person watching continuously will fail.
- **The person who is tapped isn't ready.** They have been doing something else. They don't know what the system was in the middle of.
- **Skill fades.** A person who no longer does the task by hand takes over worse than one who never stopped. Someone who never learned it by hand is worse placed still.

So a design doesn't ask a person to watch. It makes the handover itself work.

## Handing over, and taking back

A handover that works has four parts:

- **A warning in stages,** before the point of no return. "Getting close" comes before "stopped".
- **An alarm that says something,** sent to a named person, with someone else named if they don't answer. Sean's own audit and GitLab's outage on the shelf are the same lesson: the system noticed, and nobody was told.
- **A note that lets the person act.** What the goal was, what has been done, what is half-finished, what it was looking at when it stopped. A bare "failed" hands over a puzzle.
- **Help that continues.** The system keeps doing the parts it can still do, unless it is the part that broke.

Taking the work back needs design too. The system shows it is ready, the person agrees, and for a short while afterwards both are watching, before it is left alone again.

For a one-person system the handover is usually a message on a phone and a file. The parts are the same.

## Four stages of living with a system

Christopher Noessel's book on things that act for a person splits their life into stages. Each asks something different of the design.

**Setting up.**

- Say what it can do, and say more plainly what it can't.
- It should do something sensible with no settings at all.
- Draft, and ask for corrections. People are far better at fixing a plan than at writing one from nothing.
- Offer a trial run with nothing at stake.
- Pause and resume is the first control a person learns.
- Anything that can repeat gets a cap: on count, on money, on reach. The old story of the apprentice and the brooms is a system with no cap.

**Running smoothly.**

- A person can check at a glance: is it working, how are the results, what is next.
- Notices are sized to the event. Routine success is a line in a log, not a message.
- It makes contact only when needed, and when it does, it says what it saw, what it is doing about it, and what the person should do meanwhile.
- It shows the real, measured benefit, including when the figure is unflattering.

**When something goes wrong.**

- Assume it will. A system that follows rules follows them into absurd places.
- Every correction does two things: it fixes this case, and it improves the rule so the case doesn't come back.
- It will both act when it shouldn't and miss when it should act. The misses are invisible unless the design shows some of the near-misses now and then.
- A person can switch it off without giving a reason.

**Handing over and taking back,** as above.

One thing the book could not have known in 2017: today's systems read text written by strangers, and can be steered by it. So "learn the person's preferences by watching" now means watching the owner's own material only, and showing what was inferred for a yes or no. And "done" is confirmed by a check outside the system, not by the system saying so.

## How much to trust it

Trust should follow measured reliability, not hope and not habit.

- **Start narrow, widen on evidence.** A person approves everything at first; then the system serves people inside the house; then outsiders. Each step up is earned by a number, such as how often its suggestions were accepted unchanged.
- **Scope follows the cost of failure,** not only the record so far. A hundred good runs don't justify handing over an action that can't be undone.
- **One bad failure can undo the lot.** A design should know which failure that would be, and guard it hardest.
- **Friction on the high-stakes step.** Making the dangerous action slower and more deliberate is a feature.
- **An honest "I don't know"** is worth more than a confident guess. Confidence should be shown only where it has been earned.
- **Good results and low trust means it isn't showing enough.** If people can't see what it is doing and can't predict what it will do next, they won't rely on it, however well it performs.

Trust can also run too high. In the shop on the shelf, the agent was talked into giving things away, and its manager agent approved soft requests about eight times as often as it refused them. A person who assumes "the second agent is checking" has placed trust where there is no check.

## When the person is the maker

For creative and thinking work, the person is not there to approve. They are there because the work is theirs. The partner study measured four ways to set this up:

- **An open chat:** no gain in quality.
- **A partner that only offers suggestions:** no gain.
- **A partner that rewrites the idea:** the biggest jump in quality in the first experiment, but everyone's ideas became more alike and felt less their own. In a hand-read sample of 20 conversations, about nine in ten people accepted the rewrite and added nothing.
- **A partner that offers options and then asks questions:** a real gain, equal to the rewriting partner in the second experiment, and ideas stayed varied. In its sample of 20, about six in ten developed their idea a lot. People found it harder work.

So the order is: the person first, options second, questions third, and the person writes the final version. The warning sign that a design has drifted: the person is accepting the model's rewrites unchanged.

## A way to a person, always

For anything that serves other people, the route to a human is part of the product. Klarna's answer, fifteen months on, was not a better model. It said it wanted a person always on offer, and began a pilot with a human team.

And the system speaks for whoever runs it. A tribunal held Air Canada to a refund rule its chatbot got wrong. "The model said it" is no defence.

## Where it goes wrong

- **A prompt on every step.** Fix: walls for the common case, a person for the rare, costly one.
- **A person asked to watch.** Fix: staged warnings and a real handover.
- **An alarm to nobody in particular.** Fix: a named person, and a second.
- **A handover that says only "failed".** Fix: goal, done, half-done, last thing seen.
- **Trust granted by track record alone.** Fix: scope by what failure costs.
- **The person as rubber stamp.** Fix: person first and last; a partner that asks.
- **No way to pause it.** Fix: pause and resume, taught first.
- **No route to a human.** Fix: always on offer, with its own target.
- **Successes reported, misses hidden.** Fix: show some near-misses.

## Examples

All on the shelf. **The question-asking partner study** is the order of a creative session. **Honeycomb** and its side-by-side, **Uber's QueryGPT**, are two right places for a person. **Stripe's Minions** is a person at both ends. **Klarna's walk-back** is the route to a person, moved from the edge of the product to its centre. **The three-part rule and CaMeL** is why approval prompts wear out. **Project Vend** is trust placed in a check that wasn't one.

## What a strong system designer would notice

- The same level of freedom for every kind of action.
- An approval step where nothing could be harmed.
- No approval step where something could.
- A plan that relies on someone keeping an eye on it.
- An alert with no name on it.
- A handover message that doesn't say what was half-finished.
- A person whose only move is "accept".
- No pause control.
- Wider freedom granted because "it has been fine so far".

## More details

- Figures and cases come from the shelf entries in `systemcraft/research/`, which list their sources: `question-asking-partner-study.md`, `honeycomb-query-assistant.md` (with Uber's QueryGPT), `stripe-minions.md`, `klarna-assistant-walk-back.md` (with Air Canada), `lethal-trifecta-and-camel.md` (worn-down approvals), `project-vend.md`, `claude-code-april-2026-post-mortem.md` (GitLab).
- What Sean's own audit did well is on the shelf's guide, `systemcraft/research/README.md`.
- The four stages, the watcher trap and the parts of a handover follow Christopher Noessel's *Designing Agentive Technology* (2017), in the studio's own words, with the adjustments for today's models marked as the studio's.
- Starting narrow and widening on evidence follows Chip Huyen's *AI Engineering*, in the studio's own words.
- Free reading on the same ground: Google's People + AI Guidebook (https://pair.withgoogle.com/guidebook/) and Microsoft's guidelines for people working with AI.
