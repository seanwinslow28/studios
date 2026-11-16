# Systemcraft's shelf of good work

Real examples of excellent designs for systems built around AI: the workflows, agents and tools that make an idea run, each vetted for how it turned out: who made it, how it was received, and what makes it good, measured rather than admired. Step 2 of every job starts here, then adds the examples that job needs.

One file per example or small group, holding:

- What it is, who made it, when, and a link.
- How it turned out: how it was received, and why that's believable.
- What makes it good, measured: the numbers, structure and choices behind the effect.
- What Sean said about it, in his words, if he has seen it.

Links and words only. Other people's work never goes in this repo or in a finished piece.

## Sean's own audit comes first

In August 2026 Sean's earlier Systemcraft audited a system that was already running: his own overnight agents. It is the studio's own best example, so the shelf starts from it: what it did well, and what it wasted. Its records and the readout stay private and never land in this repo. `systemcraft/folders.local`, which git ignores, says where they are on this Mac.

What it did well, in words safe to share:

- It went to the running machine and measured, before forming a view.
- It kept "the system noticed" apart from "a person was told".
- It counted the work that got done, not the green lights.
- It tested its own first answer, and said so when that answer was wrong.

## Where the shelf stands

Eleven outside examples, written up on November 15, 2026, each answering one question a design has to answer. Sean saw all of them, with his own audit, on November 16, 2026. He picked the long-job harness as the closest to what he wants Systemcraft to do; his words are on that entry. He said nothing about the others yet. A fresh checker who hadn't written them compared every entry with its sources the same day and found 41 problems, six of them plainly wrong. All are corrected, and what couldn't be confirmed is said in each entry's "More details".

| The question | The example |
|---|---|
| Does this need an agent at all? | `honeycomb-query-assistant.md`: one prompt, no agent, and the misses published. |
| How do fixed steps and an agent fit together? | `stripe-minions.md`: rails where the path is known, the model where judgement is needed. |
| When does splitting a job among agents pay? | `anthropic-research-and-cognition.md`: two rivals who ended up close together. |
| What goes around the model on a long job? | `anthropic-long-running-harness.md`: a planner, a builder and a separate checker. |
| How should a person and a model make something together? | `question-asking-partner-study.md`: a partner that asks beats a partner that rewrites. |
| How do you tell whether it works? | `husain-field-guide-nurtureboss.md`: read the real runs, count the failures, fix the biggest. |
| What happens when you measure the wrong thing? | `klarna-assistant-walk-back.md`: great launch numbers, then its chief executive says quality suffered. |
| What stops an agent doing damage? | `nine-second-database-deletion.md`: instructions are not a brake. |
| Can outside text take it over? | `lethal-trifecta-and-camel.md`: a three-part rule, and the cost of building it in. |
| How do you find what broke in a running system? | `claude-code-april-2026-post-mortem.md`: three small changes around the model, found only after users complained. |
| What happens when an agent runs something by itself? | `project-vend.md`: a shop examined, fixed, and broken again. |

Every entry also names one or two side-by-sides: another real system that solved a similar problem a different way.

## Looked at and left off

Used as side-by-sides inside the entries above: Ramp's Inspect, Spotify's Honk, Airbnb's test migration, Uber's QueryGPT, Cursor's browser experiment, Google's study of many-agent set-ups, Vercel's tool cut, Karpathy's overnight loop, Shopify's Sidekick, Dramatron, GitLab's 2017 outage, Air Canada's chatbot ruling, Replit's 2025 deletion, and one person's "Wiz" set-up.

Left off, with the reason:

- **OpenAI's "Harness engineering" post (February 2026):** the page would not open for two researchers on November 15, 2026, so nothing in it could be checked. Worth another look.
- **Manus, "Context Engineering for AI Agents" (July 2025):** strong lessons on keeping the cheap, cached part of a prompt stable, but no measured result for the system.
- **HumanLayer's "12-factor agents":** a useful checklist of twelve principles, with no measured result.
- **Geoffrey Huntley's "Ralph" loop:** the headline results are anecdotes. A team that tried it overnight spent about $800 and found some features the agent called done that didn't work.
- **Intercom's Fin:** no engineering write-up of the design could be found.
- **New York City's business chatbot:** an outside audit found it telling businesses to do illegal things, and the city took it down. No design was published. A good spare warning.
- **Rechat's "Lucy":** widely cited, but the piece gives no before-and-after number.

One gap in the published record: no careful, months-long write-up of a one-person agent system with full numbers could be found. A Systemcraft audit of Sean's own could be one.
