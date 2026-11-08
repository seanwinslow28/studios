# Building a studio

How to build or rebuild a studio from this kit. It's done in a live session with Sean, because two of its parts, the tools to buy and the first taste page, are his calls.

## 1. Make the empty studio

```
python3 craftwork/new_studio.py <name> "<what it makes>"
```

This copies the template into `<name>/`, fills in the name, makes the private `library/` folder, links the studio in as a skill for Claude and Codex, and runs the checks. The name is lower case, one word, and is what Sean types to call the studio.

## 2. Fill the shelf of good work

Research the best real examples of this studio's work and vet each one for how it actually turned out: who made it, how it was received, why that's believable. Measure what makes each good. Write each to `<name>/research/` as the folder's guide says. Aim for a handful of excellent examples, not a long list. Show Sean the shelf and ask which ones he loves and why; his answers go on the examples, and they seed the taste page.

## 3. Scout the tools

Find the best tools for this kind of work today, not the ones the last version used. For each serious candidate: what it's best at, what it costs, and what it would take to get. Tell Sean what's worth buying or downloading and recommend one choice per job. He decides; nothing is bought or signed up for without him. Then write a mastery guide in `<name>/tools/` for each tool the studio will use, on getting the very best out of it.

## 4. Gather the expertise

Write a brief in `<name>/expertise/` for each area a master of this craft has to know. Draw on the books (notes in `<name>/library/`, never copied into a tracked file), on good existing skills, and on anything worth salvaging from earlier work. Salvage the craft knowledge only: what good looks like, how it goes wrong, how to fix it. Leave behind every procedure, sign-off and rule about other rules.

## 5. Write the studio's front-door page

Say what a clear ask for this craft must pin down, in order; where to look for good examples; and what the front door leaves to later steps. One screen. The method itself stays in the shared guide.

## 6. Write the first taste page with Sean

Start from what he loved and disliked on the shelf, his past notes in the brain, and any taste rules an earlier skill kept. Propose each rule as one line in his words with the example behind it; he says yes, no or rewrites it. About 15 at most. Only taste goes here: truth and safety are already on the lead's page.

## 7. Fill in the lead's page

Add what's specific to this studio: the order it locks decisions in, the checks it runs before Sean sees a version, the skills to load at each step. Keep it short; detail goes in the expertise and tools folders, which load only when needed.

## 8. Check it

```
python3 craftwork/checks/size_budget.py <name>
python3 craftwork/checks/old_terms.py <name>
```

The size check fails if the lead's page and taste page together run over 2,000 words; move detail into a brief or guide. The old-terms scan fails on any word from the studios' earlier setup.

## Keeping it small

- **Size budget:** the lead's page plus the taste page stay within 2,000 words. Everything else loads only when a step needs it.
- **No rule for an incident.** When something goes wrong, fix it in the work. A new rule comes only from Sean.
- **No rule that patches another rule.** If two rules fight, rewrite or remove one.
- **Prune at every rebuild.** Anything that hasn't earned its place goes.
