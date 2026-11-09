# When the Day Breaks, by Wendy Tilby and Amanda Forbis (1999)

## What it is

A painted short of about nine and a half minutes from Canada's National Film Board (NFB), by Wendy Tilby and Amanda Forbis, 1999. A pig in a bathrobe sees a stranger, a rooster, die in the street. The rest is her day afterwards, and her growing sense that the whole city is wired together.

- **Watch:** the NFB's free full upload, <https://www.youtube.com/watch?v=_rIBbhymIzw> (link checked 8 November 2026).
- **Best moment:** **3:24 to about 4:25**. We never see the crash. We see a car grille, then black and silence, then lemons rolling across the road, the rooster's glasses, his hat spinning to a stop. The hat melts into ink cracks. One minute, told only through objects.

## How it turned out

- It won the short-film Palme d'Or at Cannes, the top short prize at Annecy (the biggest animation festival), the Grand Prix at Animafest Zagreb, and Canada's Genie award. It was nominated for the Oscar for animated short and lost to Petrov's *The Old Man and the Sea* (Wikipedia, citing the NFB's awards list).
- Short of the Week says it won more than 40 prizes and calls it one of the most revered animated shorts of the past 20 years.
- Other directors still name it as a turning point. Jérémy Clapin, who later made the Oscar-nominated feature *I Lost My Body*, told Cartoon Brew it was the film that changed him, calling it "insanely sensorial."

Why believe it: these are independent juries in three countries plus a peer director's own account, not the studio's marketing.

## What makes it good, measured

**Measured by me from the NFB's YouTube upload (720p) on 8 November 2026:**

- **Length:** about 8 minutes 40 seconds of film (roughly 0:15 to 8:55), then credits.
- **Picture shape:** close to square, about 1.34 to 1 (old TV and film shape), not widescreen.
- **Shots:** it cuts fast for a painted film. Automatic cut detection, checked by eye on before-and-after frame pairs, puts it at roughly **180 to 220 shots**, so an average shot of **about 2.5 to 3 seconds**, and many shots under 2 seconds. The painted texture flickers so much that the detector also fires on some non-cuts, so treat this as a range, not an exact count.
- **Frame rate and drawings:** the video runs at 24 frames a second (23.976). In two 20-second samples, about two thirds of new images were held for 2 frames ("on twos", 12 new paintings a second). Camera moves drop to "ones" (a new image every frame). Calm moments hold a painting for 3 or 4 frames.
- **How the paint behaves:** it **boils**, meaning the texture crawls. Every new image is a fresh painting, background included, so specks and smudges jump each time the image changes. I checked this on the rolling-lemon close-up near 3:45: the marks on the pavement move between paintings, and stay identical across the two frames each painting is held. The boil is constant, but it never looks sloppy, because the shapes underneath come from real filmed movement.
- **Weight and timing:** the movement comes from real people on video, so it carries real weight. Lemons roll and slow down like real fruit. People shift their weight before they move. Animal heads are painted onto human bodies, which is why it feels grounded rather than cartoony. Holds come from the editing, not long still drawings: the film cuts away rather than freezing.
- **Palette:** almost monochrome grey-blue and grey-green, like a faded photocopy. Colour is rationed: lemon yellow, a red cross on the ambulance, the red of a soup can, a green bowl. Your eye goes straight to whatever is in colour.
- **Camera:** mostly tight close-ups of objects and hands, often at a tilt, with a slight jitter left over from the handheld video it was traced from. A run of plain white lines on black (about 6:50 to 7:45) shows wires and pipes linking the flats of the city, a clean break from the paint.
- **Sound:** a sung title song, plus city and kitchen sounds placed very close. At the moment of the crash the soundtrack goes **silent for about 3.5 seconds** (3:28.5 to 3:32) over a black screen. I measured that silence with an audio tool. It is the loudest moment in the film.

**From the makers' accounts and press, not measured:**

- The film is the 9 to 10 minutes Wikipedia and the NFB list.
- The singing voice is Martha Wainwright's (Wikipedia; the on-screen credits list her under singers).

**The takeaway for us:** painterly texture looks adult rather than childlike when there is real, observed movement underneath it, and when colour is used sparingly. The boil is a feature here only because the shapes under it are so solid.

## How it was made

From Short of the Week and the Animation Obsessive newsletter, which draws on the directors' own accounts:

- They filmed friends and themselves on a cheap Hi-8 home-video camera.
- They printed chosen frames as small black-and-white prints with a video printer. They re-timed the action as they went: sped up, slowed down, reversed, repeated.
- They photocopied the prints onto paper and painted over each copy with pencil and oil sticks (solid oil paint in stick form), adding animal features frame by frame. They used other methods too: some scenes were drawn or painted fresh rather than traced.
- The finished paintings were shot one by one on 35mm film under a rostrum camera (a camera fixed above the artwork).
- It took about four years, starting around 1995. The core team was the two directors, with additional animation by Martin Rose (on-screen credits).

## What Sean said about it

Seen on November 8, 2026. Sean loves every piece on the shelf and wants to come back to each one down the line:

> I hope that we'd be able to achieve all of these at one point because I love all of them.

Not the first focus; The Line's Freeview Play film is.

## More details

All times in this file refer to the NFB's YouTube upload, which runs 9:37 including the NFB logo and credits.

Sources:

- NFB full upload on YouTube: <https://www.youtube.com/watch?v=_rIBbhymIzw>
- NFB film page: <https://www.nfb.ca/film/when_the_day_breaks/>
- Wikipedia, awards and technique: <https://en.wikipedia.org/wiki/When_the_Day_Breaks>
- Short of the Week, production and reception: <https://www.shortoftheweek.com/2016/01/13/when-the-day-breaks/>
- Animation Obsessive, "When Rotoscoping Goes Very, Very Right": <https://animationobsessive.substack.com/p/when-rotoscoping-goes-very-very-right>
- Cartoon Brew, Jérémy Clapin on the film: <https://www.cartoonbrew.com/the-animation-that-changed-me/the-animation-that-changed-me-jeremy-clapin-on-when-the-day-breaks-195762.html>
- Oscars, 2000 ceremony: <https://www.oscars.org/oscars/ceremonies/2000>

How I measured: downloaded the NFB upload to a scratch folder outside the repo. I used ffmpeg scene detection at several sensitivities, then checked each detected cut by eye on before-and-after frame pairs. I found duplicate frames with ffmpeg's mpdecimate filter over 20-second samples, used silencedetect for the silence, and cropdetect for the picture shape.
