# Oktapodi, by Gobelins students (2007)

## What it is

A two-minute 3D comedy chase with no dialogue. Two octopuses in love are split up when a cook buys one for his restaurant. The other chases his delivery van through the white streets of a Greek island town to win her back. It was the graduation film of six students at Gobelins, the Paris animation school: Julien Bocabeille, François-Xavier Chanioux, Olivier Delabarre, Thierry Marchand, Quentin Marmier and Emud Mokhberi.

- **Watch:** Gobelins' free full upload, <https://www.youtube.com/watch?v=uhQu4HqT7y8> (link checked 8 November 2026).
- **Best moment:** **0:46 to 1:03**. The orange octopus gets into the van's cab and fights the driver while he is driving. He stretches across the windscreen, gets flung off and slaps back on, while the pink one wobbles on the dashboard. It is fast and rubbery, and every hit has weight.

## How it turned out

- Nominated for the Oscar for animated short at the 81st Academy Awards in 2009. That is rare for a student film (Wikipedia; Daily Bruin).
- Won Best in Show and the Audience Prize at the SIGGRAPH 2008 Electronic Theater, the main computer-graphics conference's film showcase (SIGGRAPH history archive; Short of the Week).
- Won a student-film award at Annecy 2008 (Short of the Week).
- Gobelins' official upload has about 2 million views. Several team members went on to DreamWorks and Sony Pictures Imageworks (Daily Bruin).

Why believe it: an Oscar nomination plus the top prize at the main industry graphics conference, both judged by professionals, for a film made by six students.

## What makes it good, measured

**Measured by me from the Gobelins upload (720p) on 8 November 2026:**

- **Length:** about 2 minutes 4 seconds of film (roughly 0:04 to 2:08), then credits.
- **Picture shape:** 16:9 widescreen.
- **Shots:** about **55 shots**. Automatic detection found 59 candidates, and a handful turned out to be motion blur within one shot when I checked by eye. That gives an **average shot of about 2.2 seconds**. The opening shot is long by comparison, about 13 seconds of the two octopuses together, so we care before the chase starts.
- **Pacing:** Short of the Week describes an "increasingly frantic pace," and the cut counts agree. The story is set up in the first 20 seconds, then cuts arrive faster as the van speeds up. The cab fight runs about one cut per second.
- **Frame rate and drawings:** 25 frames a second, with a new image on every frame (on ones). That is normal for 3D, where the computer renders every frame. Fast moves use motion blur and smears so they stay readable at that speed.
- **How the texture behaves:** clean, soft 3D surfaces with no painted texture. One playful exception: the van's logo, a flat 2D drawing of a cook with an octopus, comes to life as a short graphic insert at about 0:24 to 0:30.
- **Weight and timing:** the octopuses are soft bodies. They squash on landing, stretch when flung, and drag their tentacles behind the move, which is classic squash and stretch on a shape with no bones. The driver is a tall, bony human whose timing is stiffer and heavier, so the contrast is funny. Big actions get a clear wind-up, and impacts get a beat of hold before the next gag.
- **Palette:** whitewashed walls and deep sea-blue, with a bright orange octopus and a bright pink one. Orange against blue is a complementary pair (opposites on the colour wheel), so the heroes pop out of every busy street shot.
- **Camera:** low, fast and close, riding with the van down stairs and alleys, with point-of-view shots from inside the cab. The camera itself is part of the chase.
- **Sound:** wall-to-wall score (by Kenny Wood) plus slapstick sound effects. I measured no silence longer than about 0.8 seconds in the whole film. It is the opposite strategy to *Hair Love* and *When the Day Breaks*, and right for a two-minute chase.

**From the makers' accounts, not measured:**

- Gobelins capped graduation films at about two minutes so students could finish to a high standard in the time they had (Short of the Week, citing a CG Society interview).

**The takeaway for us:** this is the closest professional reference for a small, soft character with weight, the same squash, stretch and rebound problems as Sean's falling seed, solved by a team of six in under a year. It also shows how much story two minutes can hold when every shot has one job.

## How it was made

- Six final-year students made it as a class project. Each was both animator and director, and the group approved every decision (Daily Bruin; Wikipedia).
- About seven months of production during the school year (Daily Bruin). Wikipedia says less than six months. Either way, it was well under a year.
- Two of the team, Mokhberi and Marchand, had computer-science degrees, which Mokhberi said the technical side needed (Daily Bruin).
- I could not confirm which 3D software they used.

## What Sean said about it

Seen on November 8, 2026. Sean loves every piece on the shelf and wants to come back to each one down the line:

> I hope that we'd be able to achieve all of these at one point because I love all of them.

Not the first focus; The Line's Freeview Play film is.

## More details

All times in this file refer to the Gobelins YouTube upload, which runs 2:24 including credits.

Sources:

- Gobelins full upload: <https://www.youtube.com/watch?v=uhQu4HqT7y8>
- Wikipedia: <https://en.wikipedia.org/wiki/Oktapodi>
- Short of the Week, awards and the two-minute limit: <https://www.shortoftheweek.com/2009/08/10/1709/>
- Daily Bruin, interview with Emud Mokhberi (February 2009): <https://dailybruin.com/2009/02/18/four-degrees-eight-arms-one-man/>
- SIGGRAPH history archive, 2008 Electronic Theater Best in Show: <https://history.siggraph.org/award/siggraph-2008-electronic-theater-best-in-show-bocabeille-chanioux-delabarre-marchland-marmier-et-al>
- Oscars, 2009 ceremony (81st Academy Awards): <https://www.oscars.org/oscars/ceremonies/2009>

How I measured: downloaded the upload to a scratch folder outside the repo. I used ffmpeg scene detection, checked every detected cut by eye on before-and-after frame pairs, counted duplicate frames with mpdecimate over 20-second samples, and used silencedetect and cropdetect.
