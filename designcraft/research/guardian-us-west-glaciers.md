# The Guardian's vanishing glaciers of the US west (2026)

## What it is

A climate story from Guardian US, published October 23, 2026, under the headline "The US west has lost nearly 300 glaciers since the 1960s." Before the headline comes a full-screen photograph of the Hayden Glacier in Oregon, taken in 1903, in black and white. As you scroll, a thin grey line climbs the picture from the bottom. Below the line, the same mountain photographed from the same spot in 2018, in colour, takes its place.

Three short captions scroll past while it happens. Two more pairs of old and new glacier photos, further down, use the same line.

It is here as the plainest working version of a reveal line: the scroll pulls it, and the other side is the same view at another time.

See it: https://www.theguardian.com/environment/ng-interactive/2026/oct/23/glacier-loss-climate-crisis-west

**Best moment: the very first screen. Scroll slowly and watch the line rise.** The year "2018" rides just under it, while "1903" stays put in the corner of the shrinking old photo. Runner-up: **scroll back up.** The line runs backwards, exactly.

## How it turned out

- **Too new to have a track record.** It went up four weeks before this check. I found no awards and nothing public written about the graphic itself. Its standing is borrowed from the newsroom and its makers, not yet earned by this piece.
- **Who made it.** The byline reads Oliver Milman, "with data visuals by Andrew Witherspoon and Daniel Wolfe". Witherspoon is a visual journalist at Guardian US who worked at Axios before, by his own site. Wolfe's Guardian profile calls him a graphics editor of Guardian US.
- **What it stands on.** A peer-reviewed study in the Proceedings of the National Academy of Sciences, led by Andrew Fountain of Portland State University. The photos come from real archives, credited on the page: I.C. Russell's 1903 photograph from the US Geological Survey, and Hassan Basagic's 2018 photograph for the Glacier RePhoto Project.
- **Why it's still the pick.** Of about twenty-five scroll reveals checked, it is the only one I could open that does exactly this: a line pulled by the scroll, with the same view, dated, on each side. The two strongest rivals, from The New York Times and The Washington Post, block automated test browsers, so they could not be measured.

## What makes it good, measured

I loaded the live page on November 18, 2026 in a private test browser, at a laptop size (1440 by 900) and a phone size (390 by 844). A short script scrolled in 100-pixel steps and, at each step, read how much of the old photo was cut away and where the line and labels were. I closed the Guardian's fundraising banner first, with its own close button.

- **The scroll drives it inch by inch.** In motion design this is called "scrubbing": the animation's progress is tied to the scroll position, the way a video's is tied to the scrubber. The old photo is cut away from the bottom up by 7.6% of its height for every 100 pixels scrolled. The steps are even, with no speeding up or slowing down, and nothing plays by itself. *Read: the cut at every 100 pixels.*
- **One crossing takes 1,320 pixels of scrolling,** about one and a half laptop screens, starting the moment the picture locks to the top of the screen. On the phone it takes 1,216 pixels, again about one and a half screens. *Read: the first and last positions where the cut changed.*
- **Scrolling back runs it backwards, exactly.** At any scroll position the cut and the line sit in the same place, going down or coming back up. *Read: sampled again on the way up; every value matched.*
- **The picture holds still while the line crosses.** It stays locked to the top of the screen for about 2,000 pixels: the crossing, then about 700 more resting on the finished 2018 view. Then it lets go and scrolls away into the headline. *Read: the picture's top edge across that range.*
- **The line is 2 pixels thick, light grey (#DCDCDC) and 650 pixels long.** The photo is only about 630 pixels wide, so the line pokes out about 10 pixels past each side. It reads as a line drawn over the photo rather than the edge of a cut. *Read: the line's measured size and colour.*
- **The new date rides the line; the old date stays put.** "2018" travels up just under the line at its right end, in white at 80% strength. "1903" stays in the top-right corner of the old photo, in near-black (#121212) against the pale sky. Both are in the Guardian's own serif, Guardian Text Egyptian, at 30 pixels. *Read: the labels' positions and styles at each step.*
- **The photograph itself says "before".** The 1903 picture is a black-and-white archive photo; the 2018 one is in colour, from the same spot, a practice called repeat photography. The page adds no tint, grain or filter of its own.
- **Almost nothing else moves.** Three white caption boxes scroll up past the photo, and a small arrow bobs until the line is under way. A blurred, darkened copy of the photo fills the rest of the screen and holds still. *Read: the script logged every element that moved.*
- **The two smaller reveals further down are easy to miss.** The Coleman and Mazama glacier pairs use the same line, but the picture doesn't lock in place. The crossing happens while the photo is still moving up the screen, in about 300 pixels of scroll for one and about 120 for the other, so a normal flick of the wheel jumps the whole change. *Read: the same sampling, every 40 pixels.*
- **On a phone it gets bigger, not squeezed.** The photo fills the screen edge to edge, with the captions laid over it. Same line, same labels.
- **For visitors who ask for less motion, nothing changes.** With the device's "reduce motion" setting on, every value matched the normal run. There is no side-by-side version for them. *Read: the same sampling with the setting on.*
- **By keyboard it works, but coarsely.** One press of the space bar scrolls 860 pixels: the first lands mid-change, at 45%, and the second lands past the end. The arrow keys move 40 pixels, so a crossing takes about 33 presses. *Read: keys pressed in the test browser, the cut read after each.*
- **A screen reader hears only "Glacier before" and "Glacier after",** with no place and no years. *Read: the pictures' descriptions in the page.*
- **How it's built:** Svelte, a tool for building web pages, and its "scroller" add-on, which holds a background still while text scrolls past. Each picture is a stack of two: the colour photo underneath, and the old photo on top, its bottom cut away by a clipping shape that the page's own script sets on every scroll step.

### Why it's here

It is the cleanest working example found of a line the scroll pulls across a still picture, with another time of the same view on the other side. My read on what it teaches: tie the line to the scroll inch by inch; hold the picture still while it crosses; give each layer its own date and let the new one ride the line; and give the crossing room, here about one and a half screens, so nobody scrolls past it by accident, the way they can past this story's two smaller reveals.

Its gaps teach too: nothing for visitors who ask for less motion, a line that pokes out past the photo, and descriptions that drop the dates. Where the old layer is drawn rather than photographed, colour has to do the archive photo's job.

## What Sean said about it

Seen November 18, 2026, as an example for his portfolio site's thin-line reveal. No comment of his own yet.

## More details

- The story, read and measured November 18, 2026: https://www.theguardian.com/environment/ng-interactive/2026/oct/23/glacier-loss-climate-crisis-west
- Coverage of the study, titles seen in search results and not read in full: https://phys.org/news/2026-10-glaciers-american-west-mid20th-century.html and https://theconversation.com/300-glaciers-have-disappeared-from-the-american-west-since-the-mid-20th-century-the-survivors-have-a-few-things-in-common-294084
- The makers, both read: https://andrewwitherspoon.com/ and https://www.theguardian.com/profile/daniel-wolfe
- The lower pairs are the Coleman Glacier (1910 and 2025) and the Mazama Glacier (1901 and 2013), credited to the National Snow and Ice Data Center and the Glacier RePhoto Project.
- Exact rates: 7.58% per 100 pixels on the laptop, 8.08% on the phone.
- Distances are counted from the moment the picture locks, because the layout above it shifts between loads: the lock came after 262 pixels of scrolling on one load and 422 on another.
- The Awwwards scroll-mapping tool found no scroll-driven animation here, because the page sets the cut with its own script, which the tool doesn't read.
- Not checked: a real trackpad's momentum or a phone flick (the scrolling was scripted and even), a real screen reader, a slow connection, and how often real visitors see the fundraising banner.
