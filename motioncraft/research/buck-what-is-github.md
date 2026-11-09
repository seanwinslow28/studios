# BUCK's "What is GitHub?" explainer (2022)

## What it is

An explainer film by BUCK's Amsterdam studio for GitHub, the website where software developers store code and work on it together. Released November 9, 2022, 2 minutes 43.

British comedian Phil Wang plays a know-it-all host. His sidekick is a rubber duck. That's a programmer joke: developers explain their code out loud to a toy duck on the desk to find their own mistakes ("rubber duck debugging"). The film starts in live action, then moves through chapters in different animation styles: 2D, 3D and hand-drawn frame by frame (called "cel" animation).

Credits: directors Vincent Lammers and Justin Cone (as listed by a computer graphics festival archive), creative director Richard Gray, live-action director Joe Roberts (The Panics), music and sound by Antfood.

Watch: https://www.youtube.com/watch?v=pBy1zgt0XPc

**Best moment: 0:22 to 0:27.** Phil tosses the real duck into the air. It becomes an animated duck, and the camera dives with it into a bright animated world without a cut. That handoff is the hinge of the film. Runner-up: **2:13 to 2:19**, a burst of about 30 faces, each drawn in a different style, each on screen for about a sixth of a second.

## How it turned out

- **Gold award,** European Design Awards 2023, in the Animated Storytelling category.
- **SIGGRAPH 2023 Electronic Theater.** SIGGRAPH is the biggest computer graphics conference. Its Electronic Theater is a selective screening of the year's best animation craft.
- **Trade press.** Stash featured it in April 2023 and called it a "massive, multi-technique effort".
- **Audience.** About 2.5 million views and 94,000 likes on GitHub's channel. That's about 1 like for every 27 views. My read: that's unusually high for a brand video, since paid views rarely leave likes.
- **The client kept the character.** BUCK says the duck was a hard sell at first. It then became part of the look for GitHub's 2023 conference.

## What makes it good, measured

I measured these from the 1080p YouTube upload, using ffmpeg scene detection (which finds hard cuts), frame grabs and the captions for timings. Story chapters and intent come from BUCK's own case study.

- **Length and frame rate:** 162.7 seconds, 24 frames a second.
- **Two cutting speeds.** The live-action opening has about 10 shots in 24 seconds, about 2.4 seconds each. That's quick, deadpan comedy cutting, framed with black bars top and bottom like a cinema film. Once animation takes over, the bars go and shots get long: three unbroken runs of 12 to 13 seconds and one of 27 seconds. The camera flies from scene to scene instead of cutting.
- **Shot count:** outside the face montage, 23 hard cuts, so 24 shots averaging 6.8 seconds. The montage adds about 30 more cuts in 5 seconds.
- **Words:** about 300 words of dialogue in 163 seconds, about 1.9 a second. Antfood's music runs underneath throughout.
- **One question, three answers.** BUCK planned four chapters. On screen they read as:
  - What GitHub is, 0:27 to 0:53.
  - How it works, 0:53 to 1:50.
  - Who uses it, 1:50 to 2:22.
  - Where it's going, folded into the logo at 2:22.
- **Structure with timings:**
  - Cold open, 0:00 to 0:22: live action, Phil at his desk, annoyed you asked.
  - Turn, 0:22 to 0:27: the duck toss.
  - Chapter 1, 0:27 to 0:53: a fast list of what GitHub is, as the duck surfs through a toy-block city, out to a drone on Mars.
  - Chapter 2, 0:53 to 1:50: Sonal, an engineer, explains working on separate copies of the code and joining them back together. The copies are glowing lines and orbs that split and merge. A knight-armour gag at about 1:35 covers security.
  - Chapter 3, 1:50 to 2:22: a student, musicians, a company boss, the first photo of a black hole, then the face montage.
  - Logo, 2:22 to 2:35.
  - Final joke, 2:35 to 2:43: back to Phil, now beside a giant duck.
- **How UI shows up:** as a picture idea first (code versions as rails of light), and only briefly as stylised panels with labels like "Done" and "Building". No real screenshots.
- **What holds the style changes together:** the duck is in every chapter. A hot palette repeats (magenta, duck yellow, electric blue), and so do glowing orbs. Measured main colours: dark navy #131730 and #2e317e, warm duck orange #a6795a, pale sky #b0c9ef.
- **Comedy does the heavy lifting.** The dullest parts, like lists of features, are delivered as jokes. The ending makes fun of the film itself.

### Why it's here

It stretches the shelf. It isn't one polished world. It's live action, comedy and four animation styles in under three minutes. The lesson for Motioncraft: one strong character can be the thread that lets each chapter change style without the film falling apart.

## What Sean said about it

Seen on November 8, 2026. Sean loves every piece on the shelf and wants to come back to each one down the line:

> I hope that we'd be able to achieve all of these at one point because I love all of them.

Not the first focus; The Line's Freeview Play film is.

## More details

- BUCK case study (chapters, the duck, credits): https://buck.co/work/github-what-is-github
- European Design Awards, Gold, Animated Storytelling, 2023: https://awards.europeandesign.org/winner/258195
- SIGGRAPH 2023 Electronic Theater listing: https://history.siggraph.org/animation-video-pod/what-is-github-brand-film-by-lammers-and-cone
- Stash feature (April 1, 2023): https://www.stashmedia.tv/what-is-github-buck-and-a-duck-explain/
- BUCK on reusing the duck for GitHub's 2023 conference: https://buck.co/work/github-universe-2023
- View and like counts read from YouTube on November 8, 2026.
- My measurements: ffmpeg scene detection at threshold 0.3, with cuts closer than half a second merged. The animated chapters have many scene changes made by camera moves rather than cuts, which the detector doesn't count, so 24 shots understates how many places you visit.
