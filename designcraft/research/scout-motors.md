# Scout Motors' home page, with Locomotive (2024)

## What it is

The home page of Scout Motors, an American truck brand from the 1960s that is being brought back, with the backing of Volkswagen Group. It introduces two vehicles, the Traveler and the Terra, that will not be built for a while yet. So the page has one job: get you to put down a small, refundable reservation.

It does that like a short film. As you scroll, a truck drives towards you down a dirt road at dusk, then turns into the 1960s original.

The award entry credits Locomotive, a well-known web agency, with Scout's own team. Awwwards, the best-known web design award site, made it Site of the Day on January 16, 2025. The page itself dates the trucks' reveal to October 24, 2024.

It is here as the spectacle that has to sell something.

See it: https://www.scoutmotors.com/

**Best moment: the first three screens. Scroll slowly from the top.** The two new vehicles sit in a desert. Then one drives at you along a dirt road in orange evening light. Then it becomes the old Scout, under the line "The one that started it all." The opening shot plays on its own. After that the motion follows your hand: stop scrolling and the truck stops. Runner-up: the heritage section just after, where old adverts fan out like playing cards across one giant word.

## How it turned out

- **E-commerce of the Year 2025,** Awwwards Annual Awards, with 28 votes. This is the yearly prize for sites that sell.
- **Site of the Day,** January 16, 2025, at 7.60 out of 10 from 18 judges. Design 7.73, usability 7.27, creativity 7.79, content 7.69.
- **Developer Award,** 7.36 out of 10. This one is judged by engineers.
- **The day score is modest.** It is lower than the three showpiece sites in this batch, which scored 7.92 to 8.18. It won the yearly prize anyway. My read: the jury rewarded a page that sells, not only one that dazzles.
- **Reservations.** Scout said in March 2026 that it had passed 160,000 reservations at $100 each, refundable. That is the company's own figure, reported by the car press. It reflects the trucks, the price and the news coverage, not the page alone. But the page is where the reservation is made.
- **Not found:** I looked for an FWA award, a CSS Design Award and a Webby and could not confirm any.

## What makes it good, measured

I loaded the live page on November 16, 2026 in a private test browser, at a laptop size (1440 by 900) and a phone size (390 by 844). A short script read the type, colours and timings off the finished page and added up everything it downloaded. The order of sections comes from screenshots I took at ten points down the page.

- **Length:** 17,890 pixels on the laptop, about 20 screens. It is the longest page in this batch. On the phone, 15,226 pixels, about 18 screens.
- **The order,** as I saw it:
  - The two vehicles in a desert, under "Scouts always come back."
  - The drive down the dirt road.
  - The 1960s original, "The one that started it all."
  - The brand's history on warm grey paper, with fanned-out archive cards.
  - A full-width old photo of an original Scout by a river.
  - The new truck in the dark with its lights on.
  - "Experience the reveal event," with a film of the launch.
  - The two models side by side, each with a Discover button.
  - The company's story, then a closing call to reserve.
- **Where the ask sits.** Reserve is in the top bar from the first screen. One screen down, an orange card slides in at the bottom right: "Be one of the pioneers. Reserve now."
- **Type:** the brand's own family, Scout Sans, in four cuts, plus IBM Plex Mono, a typewriter-style face, for small labels.
  - Headlines are 72 pixels in the wide cut, with lines packed tight at 0.9 of the type size.
  - A few words are set enormous, at 270 pixels, as pictures more than text.
  - Body text is 14 to 20 pixels.
  - On the phone, headlines drop to 42 pixels.
- **Colour:**
  - Warm paper grey, #EDE9E8, as the base.
  - Orange-red, #FF5432, for the things you can press.
  - Deep navy, #11232F and #0C0E1C, for the night scenes.
  - Soft black, #1C1C1A, for text.
- **One motion curve.** 159 elements share the same easing, a quick start with a long soft stop. In code that is cubic-bezier(0.38, 0.005, 0.215, 1). The most common speeds are 0.4 and 0.6 seconds, then 0.3 and 0.2.
- **How the film works.** The opening shot is a video that plays by itself. From the second screen on, the picture is tied to scroll. I stopped at eight points down the page, and each time the picture held still until I scrolled again. My read, from what the page downloads: the drive is a run of still frames, swapped as you scroll. One full scroll fetched 632 pictures. A normal video cannot stop and reverse that smoothly.
- **How it's built,** each part in a few words:
  - Astro: a tool for building fast, mostly fixed pages.
  - Lenis: a small library that makes scrolling glide.
  - Two full-screen drawing surfaces that play the frames, and two or three ordinary videos.
  - No 3D library. I found no Three.js.
- **Weight, and it is the cost of the film:** 17.7 megabytes before you scroll. 51.7 megabytes after scrolling the whole page, in 759 downloads. Pictures are 42.7 of that. One video is 7.1.
- **On a phone:** the same story in 18 screens. It downloads less, 10.9 megabytes at first and 33.5 after a full scroll. That is still more than twice the next heaviest page in this batch.
- **A rough edge:** on a first visit a cookie notice covers the lower left of the opening film.

### Why it's here

The other showpieces on this shelf sell a person or a brand mood. This one has to earn a deposit. My read: the lesson for Designcraft is the pairing. The film gives the feeling, and the ask never moves: one orange colour, one word, always in reach. The caution is the weight. Fifty megabytes is a lot to ask of a phone on a weak signal.

## What Sean said about it

Seen on November 17, 2026, with the rest of the shelf. He said nothing about this one by itself.

Of the whole shelf: "all of the options you provided are amazing in their own way and I wouldn't want to throw those out the window." He picked no favourite. It stays on the shelf as one end of the range.

## More details

- Awwwards Annual Awards winners, 2025 (E-commerce of the Year, 28 votes): https://www.awwwards.com/annual-awards/winners
- Awwwards site page (Site of the Day date, jury scores, Developer Award, Locomotive and Scout credits, palette): https://www.awwwards.com/sites/scout-motors
- Awwwards hall of fame, 2024 (Locomotive as Agency of the Year, which is why I call it well known): https://www.awwwards.com/annual-awards/hall-of-fame/2024
- Autoblog, republished by AOL, March 5, 2026 (160,000 reservations, $100 refundable, deliveries expected by 2028): https://www.aol.com/articles/scout-160-000-reservations-87-221500708.html
- The Volkswagen Group backing, the October 24, 2024 reveal and the 1961 history are stated on the page itself.
- My measurements: a private headless Chromium driven by a short script, at 1440 by 900 and 390 by 844, 12 seconds of settling, then a full scroll. The page names its own builder as Astro. It logs a "Sequence" image service three times as it starts, which supports the still-frames reading. For the hold-still test I took three captures two seconds apart at each stop and compared them.
- The Awwwards page-structure, scroll-map and motion tools would not run; they need a browser add-on, Playwright, that is not installed.
- The page may have changed since it won Site of the Day in January 2025. I measured what is live now.
