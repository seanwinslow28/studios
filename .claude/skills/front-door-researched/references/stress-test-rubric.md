# The stress test: two passes, one verdict

The one stage of the room whose job is to verify rather than author, and the one where same-context bias bites hardest: a room red-teaming the concept it just built is reviewing its own love story. So the authority is a **fresh-context reviewer** that has never seen the sidecar. Shape from anima's good-stress-test rubric; the vendor rule from the studios' gates. Written on SWCB #267 (2026-10-23), lock 7.

## Pass 1: the in-room reflex

A short pre-mortem in place, before any file is written for the reviewer: the obvious ways this piece fails, the load-bearing assumptions named. Declared biased in its own block (`### stress-test — pass: in-room`). It warms the room and feeds the reviewer's prompt nothing: the reviewer reads the two files only.

## Pass 2: the fresh-context reviewer

**What it reads:** the draft `concept.md` and `brief-draft.md`, and nothing else. Not the sidecar, not the board, not the frames, not this conversation. It is handed the two files' paths and this rubric.

**Vendor:** the one that did not write the drafts, as the studios' gates run on the vendor that did not write the anchor. Claude writes the drafts in the room, so the reviewer runs on **Codex, read-only**, through `codex exec` from a folder holding copies of the two files alone, with the model and effort the studio's launch form pins (Motioncraft: `--model gpt-6.1-sol`, `model_reasoning_effort="high"`), its final message saved with `-o` and filed byte for byte into `Planning/<slug>/stress-test.md`. When Codex is unavailable, a **fresh Claude sub-agent** handed only the two paths, named as the substitute in the block header. The first run may move this default; it is recorded in the lens when it does.

**What it does, in order:**

1. **Extract the load-bearing assumptions**, steelman the strongest version of each, then attack that. Never a strawman, never a cosmetic nitpick.
2. **Write each surviving risk as "Fails if ___"** with its **cheapest test** this week, then rank by impact, likelihood and cheapness to test.
3. **Triage every risk**: **Tiger** (real, act), **Paper-Tiger** (overblown, document), **Elephant** (unspoken, investigate). Default to Tiger when unsure. Name which Tigers block the studio from opening cleanly, apart from the ones that follow fast or are merely tracked.
4. **Protect the fragile intuition, with substantiation.** The engine that makes the piece special is not attacked as a risk. Every such protection names three things: the protected engine; the nearest legitimate adjacent risk, which is still attacked; and why the flagged weakness is not the engine wearing a scary label. This blocks both games: manufacturing rigour by attacking the engine, and hiding a real hole behind "that's the intuition".
5. **No manufactured doubt.** A sound concept is said sound, plainly. Five real kill-assumptions beat twenty generic risks.
6. **Recommend a verdict**: `proceed` with named, correctly scoped residuals, or `revise` with at least one blocking Tiger. The verdict is a recommendation; Sean decides; the room locks.
7. **Name its own limit**: that a review of two files cannot see what the room saw, and which residuals a live eye on the frames might retire.
8. **Name problems, never shots.** Each risk points at a gap in the brief, never at a fix in staging: no shot, framing or timing is proposed. The Director decides how to solve it.

## What binds, and where it lands

A blocking Tiger, or a proceed-with-residual that changes **buildability, budget or constraints**, is production-binding and goes into `brief-draft.md`, under *What this is NOT* or the non-negotiables, as one more checkable line, because the studio reads only the brief. Non-binding residuals (fast-follow, track) go to `concept.md`'s open threads. The room folds; it never re-runs the red team while folding.

## Sean's live review of the pass

Judged by Sean against the saved findings, never by a lint and never by the reviewer's account of itself. A good pass shows all six: a real kill-assumption found; each risk a falsifiable "Fails if" with a cheapest test; triaged, default to Tiger; no manufactured doubt and the intuition protected with its three-part substantiation; an honest verdict with correctly scoped residuals; its own limit named. **One, four and five block together**: a toothless clean pass, a twenty-risk fog or an attack on the engine, and a verdict that mis-scopes the residuals are the three ways the stage becomes theatre. The calibration case: a thin concept (generic feeling, no engine, no signature move, the subject as the joke) must come back `revise` with a blocking Tiger; a strong concept with one real register gap must come back `proceed` with that gap named, never clean.

## Cost

No spend. The reviewer is a read-only pass on the subscription or a sub-agent; no image or clip is generated for it.
