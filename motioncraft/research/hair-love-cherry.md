# Hair Love, by Matthew A. Cherry, Everett Downing Jr. and Bruce W. Smith (2019)

## What it is

A six-minute 2D short, 2019. A dad tries to do his young daughter's hair for a special day, following her mum's video tutorials. He loses badly, then gets it right. Only at the end do we learn where they are going. It began as Matthew A. Cherry's Kickstarter project and was finished with Sony Pictures Animation.

- **Watch:** Sony Pictures Animation's free full upload, <https://www.youtube.com/watch?v=kNw8V_Fkw28> (link checked 8 November 2026).
- **Best moment:** **2:00 to 3:06**. Dad versus the hair. The comb gets stuck, he sweats, and at about 2:40 it becomes a boxing match against a giant dark mass of hair under a spotlight. He loses, and the soundtrack goes silent as he slumps. Pure acting, no words.

## How it turned out

- Won the Oscar for animated short at the 92nd Academy Awards in 2020 (Wikipedia; Oscars).
- Its 2017 Kickstarter asked for $75,000 and raised over $300,000 (Wikipedia). Sony then picked it up and showed it in cinemas before *The Angry Birds Movie 2* in August 2019.
- The official YouTube upload has passed 121 million views (I read this from the video's own data).
- It led to a children's book and a TV spin-off series, *Young Love* (Wikipedia).

Why believe it: an Oscar win, a crowd-funded audience that existed before any studio got involved, and a huge view count on the official upload.

## What makes it good, measured

**Measured by me from the official upload (720p) on 8 November 2026:**

- **Length:** about 6 minutes 5 seconds of film (roughly 0:05 to 6:10), then credits.
- **Picture shape:** wide cinema shape, 2.39 to 1, with black bars top and bottom on YouTube.
- **Shots:** about **115 shots**. Automatic detection found 116 candidates, and almost all held up when I checked them by eye. That gives an **average shot of about 3.2 seconds** (median about 2.2).
- **Pacing changes with the story:** this is the most useful number. During the fight with the hair (2:00 to 3:00) there are 33 cuts in 60 seconds, **a new shot every 1.8 seconds**. After the fight is lost, the film holds a **single 17-second shot** (about 3:26 to 3:44) of the dad leaning on a door and sliding down to sit, and that stillness is what makes the turn land. The calmest 30-second stretches have only 4 or 5 cuts.
- **Frame rate and drawings:** 24 frames a second (23.976). In a busy sample (1:00 to 1:20), most images changed every frame (on ones). That fits fast action, hair and camera moves. In a calmer sample (4:10 to 4:30), the split was roughly half ones and half twos, with a few holds of 4 to 6 frames on poses.
- **How the texture behaves:** this isn't paint, and that's the point. Characters are clean flat colour with soft shading, and backgrounds have gentle painted texture that holds still. The hair is the one "textured" thing in motion: a dark mass with a soft, grainy edge that stays stable from frame to frame. Nothing boils.
- **Weight and timing:** the dad is big and gentle, and his weight shows in how he slumps, braces and leans back from the hair. The daughter is quick and springy. Comic beats get clear anticipation: he winds up before each comb stroke, and the rubber band stretches before it snaps. Reactions get a short hold so you can read his face.
- **Palette:** warm pastels (pinks, lilacs, teal tiles) for home. The fight drops into near-black with a single spotlight, a deliberate palette switch to show the "battle" is in his head.
- **Camera:** mostly eye-level and close. The fight breaks this rule with low angles, a boxing-ring wide shot and fast push-ins, then the film returns to calm framing.
- **Sound:** an instrumental score carries it. The only spoken lines are the mum's, on the tutorial videos. I measured a **3.7-second silence at 3:02 to 3:06**, right as the dad is beaten. It is the film's emotional floor.

**From the makers' accounts, not measured:**

- The makers deliberately left out dialogue so the story would rest on acting, "relying just on the characters' acting" (Creative Lives in Progress).

**The takeaway for us:** character performance comes from contrast (fast cutting against one long hold, a heavy dad against a light daughter, noise against silence) more than from detailed rendering. Clean, simple, near-vector shapes are no barrier to feeling. That matters for Sean's vector test.

## How it was made

- Storyboarded in Toon Boom Storyboard Pro and animated in Toon Boom Harmony, industry-standard 2D animation software (Wikipedia; Creative Lives in Progress).
- A mix of rig and hand drawing. The team built a character rig (a reusable puppet of the character seen from the front, side and three-quarter view). A lead animator drew the key poses by hand, and the rig was laid over them to keep proportions consistent. The rig covered roughly 60 to 75 percent of the animation, and the rest was adjusted by hand for appeal (Creative Lives in Progress).
- About two years overall: roughly a year on story and boards, then about six months of production (Creative Lives in Progress).
- The main production studio was 6 Point Harness. Animation Magazine reportedly put the crew at about 60 people. I couldn't open that article myself, so treat the number as second-hand.
- The acting drew on co-director Everett Downing Jr.'s own experience doing his daughter's hair, plus online videos of Black fathers doing their children's hair. The snapping rubber band came from one of those videos (Creative Lives in Progress).

## What Sean said about it

Seen on November 8, 2026. Sean loves every piece on the shelf and wants to come back to each one down the line:

> I hope that we'd be able to achieve all of these at one point because I love all of them.

Not the first focus; The Line's Freeview Play film is.

## More details

All times in this file refer to the official YouTube upload, which runs 6:48 including credits.

Sources:

- Official full upload: <https://www.youtube.com/watch?v=kNw8V_Fkw28>
- Wikipedia, credits, Kickstarter, release, software, award: <https://en.wikipedia.org/wiki/Hair_Love>
- Creative Lives in Progress, production process: <https://www.creativelivesinprogress.com/article/the-makings-of-oscar-nominated-short-film-hair-love>
- Animation Magazine, making-of (blocked to my fetch; crew size seen second-hand): <https://animationmagazine.net/shorts/hair-to-stay-making-hair-love-a-delightful-animated-trailblazer>
- Oscars, 2020 ceremony: <https://www.oscars.org/oscars/ceremonies/2020>

How I measured: downloaded the upload to a scratch folder outside the repo. I used ffmpeg scene detection, checked a full sheet of detected cuts by eye on before-and-after frame pairs, and counted cuts per 30-second window for pacing. I counted duplicate frames with mpdecimate over 20-second samples, and used silencedetect and cropdetect.
