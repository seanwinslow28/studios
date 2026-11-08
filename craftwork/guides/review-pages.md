# Review pages and the scorecard

Anything Sean rules on, every studio, every checkpoint, is a house review page. The house style lives in the brain, so there is one copy for every studio and every brain session; where to find it is at the bottom of this guide.

## What every page has

- A short title, then **"The simple version"**: what this is and what to decide, explained like he's five.
- What happened, in plain words.
- What to look for, with the work beside each point.
- The work itself: the real thing, rendered or run, never a description.
- **One question.**
- **The lead's pick**, marked on its answer, with one line on why. That holds for spot-checks of the fresh check too.
- "I can't tell" as an answer, always.
- A Copy my answer button, so Sean can paste his answer into the chat.
- Anything technical folded under "More details" at the bottom.

Name each page file `review-<what>.html` and keep it in the job's folder. The plain-writing check reads any page named that way before it's written.

Before Sean sees a page, run the screenshot checker on it and look at what it shows. A page that errors or shows blank on a phone isn't ready.

## The scorecard

Every job ends with one short scorecard page, after Sean approves the work. It takes him under two minutes:

1. **How good is it?** Great, good, okay, or not good.
2. **Will you use it?** Yes, maybe, or no.
3. **What would you change?** Offer three or four suggested answers drawn from this job, each a real thing that happened ("fewer review rounds before the look was right", "the front door asked too many questions", "a better tool for the sound"), plus his own words. Suggested answers make it quick; they're never the only choice.
4. **One spot-check**, now and then: one call the fresh check made during the job, for Sean to agree or disagree with.

Keep his answers in the job's decisions record. A note that keeps coming back across jobs is how a taste rule gets proposed, and how the kit learns what to change.

## Where the house style lives

- **The guide:** `~/Code-Brain/SWCB/docs/pages/DESIGN.md`, section 9 (the Decide page).
- **The template and packer:** `~/Code-Brain/SWCB/docs/prototypes/house-look/`. Write one `decide.json` for the decision, and `build_page.py` packs it into a single file that opens from disk, on a phone, or as a Claude Artifact. `--narrate` adds the Listen clip.
- **The page tools,** in that folder's `tools/`: word timing, so pictures on an Explain page move on the exact word that explains them, and the screenshot checker, which photographs every moment of a page at desk and phone size, by day and night, and reports any page errors.
