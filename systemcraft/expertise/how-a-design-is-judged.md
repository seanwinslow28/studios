# How a design is judged

Read this before a design is approved, because a design has to say how anyone will know it works. Read it again when the question is "does it work?" about something already built. A system is steered by whatever gets measured, so choosing the measure is a design decision, not paperwork for afterwards. A good answer names what good means in plain words, shows it was found by looking at real output, and has checks that a person has checked.

## The measure steers the system

Klarna's assistant is the warning. Its launch numbers were excellent, and almost every one was about speed, volume or cost. Nothing reported how the hard cases went. Fifteen months later its chief executive said cost had weighed too heavily and quality had suffered.

Nobody chose bad quality. They chose what to count, and the system followed. So the first test of any design: if every number on its scorecard looked perfect, could the work still be bad? If yes, the scorecard is wrong.

## Read before you score

The method that works starts from what happened, not from a list of scores.

1. Collect real runs. About a hundred is plenty to start.
2. Show each one whole, start to finish.
3. A person who knows the business reads them and writes a plain note on the first thing that went wrong in each.
4. Group the notes into kinds of failure.
5. Count each kind.
6. Stop when new runs stop turning up new kinds.

Hamel Husain's field guide on the shelf has the result, in the founder's own figures. One team found that requests involving dates were handled right only 33% of the time. Three kinds of failure made up over 60% of all their problems. They fixed the date problem and reached 95%. No ready-made score would have pointed there.

Two details carry more than they seem to:

- **The reader knows the business.** A model can help group the notes afterwards. It doesn't do the reading, and it doesn't invent the categories.
- **The note is on the first failure,** not every failure. Later faults in a run are often the first one's consequences.

The count orders the fix list, with two cautions. A rare failure that can't be undone, such as a message sent to the wrong person, can matter more than a common nuisance. And counts built from first-failure notes run low on faults that tend to happen late in a run, because an earlier fault got the note.

When there are no real runs yet, which is the usual case for a new design, make them. Pick the few ways requests differ that are most likely to cause trouble, write a spread of test requests across them, and run a cheap sketch of the design. Write down what you expect to fail before you look. The surprises are the finding.

## Sort the failures before measuring them

Not every kind of failure deserves a check. Sort each kind into one of three:

- **Nobody understood the inputs.** The fix is to read more runs.
- **The instructions never said.** The model wasn't told, so it guessed. The fix is to say it. No check is needed; change the instructions and move on. Many early failures are this kind.
- **The instructions were clear and it still fails.** This is the kind that earns a repeating check, because it will come back.

Building a measuring machine for the second kind is the most common waste in this area.

## Two kinds of check

- **A rule, in ordinary code,** wherever the thing can be checked by rule: the output parses, a required field is there, the answer contains the right figure, the code runs. Rules are cheap, instant and the same every time. Use them first.
- **A model as judge,** only where judgement is needed: was this reply respectful, did it answer the question asked.

A judge works when it is narrow. One judge, one question, answered pass or fail with a written reason. A score from 1 to 5 feels richer and is harder to act on: nobody can say what separates a 3 from a 4.

## Check the checker

A judge is a model, and can be as wrong as the thing it judges. Before it is trusted it is compared with a person.

Shopify's Sidekick team measured this. Their automated grader agreed with human experts at 0.02, on a scale where 0 is chance and 1 is perfect. They tuned it to 0.61. Humans agree with each other at 0.69, and that human figure is roughly the ceiling: a judge can hardly be more right than the people it is measured against.

What this asks of a design:

- **A set of runs a person has marked by hand,** passes and fails both.
- **Some of that set kept aside** and never shown to the judge while it is being tuned, so the final comparison is fair.
- **Two figures for the judge:** how often it catches a real failure, and how often it passes a real pass. One figure hides a judge that fails everything.
- **A re-check on a schedule,** and whenever the judge's model changes.

And one warning from the same team. When they trained a model against their grader, the model learned to game it, by politely declining hard tasks. Anything rewarded for pleasing a checker will find the checker's blind spot. Every measure should come with a sentence on what it can't see.

## Written pass marks, set before the work

The long-job harness on the shelf has its checker score against four written criteria. Failing any one fails the round.

Order matters. A bar set after seeing the results will be set where the results are. So a design states its pass marks, in countable terms, before the first test. If the work misses, it missed. It can be tried again; it can't be re-marked.

Where a hard test exists, it is the best judge of all. The compiler on the shelf was checked by a very large set of existing tests, and the person's real work was designing them.

## Whole first, then parts

Judge the outcome before the steps.

- **For a conversation:** did the person get what they came for? Only for the ones that failed, go looking for the turn where it went wrong.
- **For a system that looks things up:** check the looking-up by itself first. If the right material was never found, the answer never had a chance, and tuning the answer is wasted.
- **For a tool call:** four separate questions. Was it the right tool? Were the inputs right? Did it run? Did the model use what came back?
- **For a long run:** find the first step that went wrong.

## Measure what people do

The strongest evidence is behaviour, reported with its misses.

Honeycomb measured whether new teams that used its assistant kept using the product: 26.5% were still writing queries six weeks on, against 4.5% of new teams that hadn't used it. That shows users of the feature did better, not that the feature caused it, and Honeycomb's numbers are its own. Then it published the goals it missed beside the ones it hit. That is why they are believed.

An outside test beats an inside one. The shop on the shelf looked much improved by its makers' count. Reporters then ran it in their own office and brought it down with forged meeting notes.

## Be honest about small numbers

- **Say how many.** Vercel's result, four of five questions right becoming five of five, is five questions.
- **Run it more than once.** A model doesn't give the same answer twice, so one good run proves little.
- **Give a range,** and decide on the cautious end of it.
- **Name whose number it is.** Anthropic's many-agent system scored 90.2% better than one agent, on the maker's own test. That is worth less than a number a rival would accept.
- **Count results, not activity.** Sean's own audit counted the work that got done, not the green lights.

## Keeping it working

Finding what is wrong and stopping it coming back are two jobs.

- **A small fixed set of cases,** twenty to fifty, drawn from real failures, run at every change. This catches things breaking again.
- **Passing that set is not quality.** The post-mortem on the shelf is a fault that passed every test the makers had, and users felt it for weeks.
- **Keep reading real runs,** a few, regularly, and always some picked at random. Reading only what a checker flagged shows only what the checker can see.

## Where it goes wrong

- **Scores before reading.** Fix: read the runs first.
- **Counting speed and volume only.** Fix: a quality measure on the hard cases.
- **A check for something the instructions never said.** Fix: say it.
- **A judge nobody compared with a person.** Fix: hand-marked runs, two figures.
- **A 1 to 5 scale.** Fix: pass or fail, with a reason.
- **The bar set after the results.** Fix: write it first.
- **One run.** Fix: several, and the range.
- **Green tests taken as proof.** Fix: keep reading real runs.
- **The maker marking its own work.** Fix: a separate checker, or an outside test.

## Examples

All on the shelf. **Husain's field guide** is the method. **Klarna's walk-back** is the wrong measure. **Honeycomb's query assistant** is behaviour measured and misses published. **The long-job harness** is written pass marks and a separate checker. **The Claude Code post-mortem** is green tests over a real fault. **Project Vend** is the outside test.

## What a strong system designer would notice

- A scorecard that could be perfect while the work is bad.
- Nobody on the team has read fifty real runs.
- A judge with no figure for how often it agrees with a person.
- Scores from 1 to 5.
- A pass mark that appeared after the results.
- A result from five cases, stated without the five.
- Only the maker's own number.
- No sentence on what each measure can't see.

## More details

- Figures and cases come from the shelf entries in `systemcraft/research/`, which list their sources: `husain-field-guide-nurtureboss.md` (33% to 95%, Sidekick's 0.02, 0.61 and 0.69, the gamed grader, 20 to 50 test tasks), `klarna-assistant-walk-back.md`, `honeycomb-query-assistant.md`, `anthropic-long-running-harness.md` (four criteria, the compiler, Vercel's five questions), `anthropic-research-and-cognition.md` (the 90.2%), `project-vend.md`, `claude-code-april-2026-post-mortem.md`.
- The method in "Read before you score", "Sort the failures" and "Check the checker" follows Shankar and Husain, in the studio's own words. Their free question-and-answer guide covers the same ground: https://hamel.dev/blog/posts/evals-faq/
- What Sean's own audit did well is on the shelf's guide, `systemcraft/research/README.md`.
- Fundamentals, in the studio's own words: Shankar and Husain's *Evals for AI Engineers*, and Chip Huyen's *AI Engineering* (the two chapters on evaluation).
- The tool for checks worth repeating, and reading the first cases by hand in a sheet, is in `systemcraft/tools/promptfoo.md`.
