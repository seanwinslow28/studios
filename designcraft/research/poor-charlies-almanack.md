# Poor Charlie's Almanack, the web edition by Stripe Press (2023)

## What it is

A whole book, free to read in the browser. Poor Charlie's Almanack collects the talks and sayings of the investor Charlie Munger. Stripe Press, the publishing arm of the payments company Stripe, brought out a new print edition in December 2023 and put the full text online beside it.

It is a reading site. Big quiet serif titles, a column of text, cut-out portraits in the margin, and almost nothing that moves. The award entry credits three people, among them Devin Jacoviello and Nick Jones. Awwwards, the best-known web design award site, made it Site of the Day on January 4, 2024.

It is here as the calm one. Next to the showpieces on this shelf it shows what excellent looks like when the page's only job is to be read.

See it: https://www.stripe.press/poor-charlies-almanack

**Best moment: open Talk One and read the first three screens.** On the contents page, click the "01" under "Eleven Talks". A title fills the left of the screen at huge size, beside a pile of cut-out portraits. Scroll once and the text begins in a single column, with a pink note card and a bust of Cicero beside it. Watch the small percentage in the top bar count up as you read. Runner-up: on the contents page, press "Berkshire mode". By one blogger's account it restyles the site to copy the plain look of Munger's own company's website.

## How it turned out

- **Site of the Day,** Awwwards, January 4, 2024, at 7.51 out of 10. Design 7.57, usability 7.20, creativity 7.77, content 7.66. Awwwards members gave it 8.24.
- **Developer Award,** 7.54 out of 10. This one is judged by engineers. Animation 8.20, accessibility 6.80.
- **Praise from a tough critic.** John Gruber, who writes the long-running Apple blog Daring Fireball, linked it on December 29, 2023 and called it beautiful and fun. His point: an e-book you only read, and this you experience.
- **The lowest jury score in this batch,** and no yearly prize. My read: award juries mark creativity, and a reading site spends little on show. That gap is the reason to put it beside the winners.
- **Not found:** I looked for an FWA award and a Webby and could not confirm either. I found no visitor numbers.

## What makes it good, measured

I loaded two live pages on November 16, 2026 in a private test browser: the contents page and Talk One. I used a laptop size (1440 by 900) and a phone size (390 by 844). A short script read the type, colours and timings off the finished page and added up everything it downloaded. Layout notes come from screenshots I took at six points down Talk One.

- **The contents page fits one screen.** On the laptop it does not scroll at all. The whole book is in view: three chapters, eleven talks, the forewords and the back matter. On the phone it is one and a half screens.
- **Numbers as the menu.** The chapters and talks are bare numerals, "01 / 02 / 03", set at 124 to 157 pixels. Talk eleven is spelled out in italics.
- **A reading page is long and plain.** Talk One is 11,438 pixels on the laptop, about 13 screens. On the phone, about 16.
- **Type, three faces:**
  - Cardinal Fruit, a light serif with thick and thin strokes, for titles. They are 137 to 146 pixels, with lines packed tight at 0.84 of the type size.
  - Ivar, a book serif, for the text. It is 18 pixels on a 23-pixel line, in a column 638 pixels wide. That gives 70 to 80 characters a line.
  - Suisse Mono, a typewriter-style face, for labels in capitals at 9 to 13 pixels.
- **The scale jump does the work.** Titles are eight times the size of the text. Pull quotes sit between, in italic, at 41 to 49 pixels.
- **On the phone the text stays 18 pixels.** Only the titles shrink, to about 82.
- **Colour:**
  - Paper grey, #EFEFEF, behind everything.
  - Soft black, #2D2D2D, for text.
  - A pale pink, #F0CDC9, for the note card that opens the talk.
  - A dark green, #434E40, and a near black, #0D0E14, for the panels that close it.
- **Layout:** hairline rules split the screen into two or three columns. Pictures sit in one, text in the next. The pictures are cut-out portraits, layered like a paper collage.
- **Reading aids, all small:**
  - A percentage in the top bar that tracks how far you have read.
  - A read time and a listen time at the head of each talk, such as 9 minutes to read and 17 to listen.
  - An audiobook player in the bottom bar, with four speeds from 1 to 2.5 times, and a fifth, faster one named after a Stripe founder.
  - Numbered footnotes, and a sidebar you can open and close.
  - At the end, two big panels: previous chapter, next talk.
- **Motion, very little:** plain fades of 0.2 to 0.5 seconds on links and panels. Text fades in over 0.7 to 2 seconds when a page opens. Apart from the progress number, I found nothing tied to scroll, and no scroll or animation library.
- **One 3D touch.** The opening collage of Talk One is drawn on a small 3D surface on the laptop. On the phone it is left out.
- **How it's built:** Next.js, a common tool for building websites, and Three.js, a 3D library, for that one collage.
- **Weight:** the contents page is 1.8 megabytes in 25 downloads. Talk One is 8.6 megabytes, 9.3 after a full scroll. Of that, 7.8 is the portraits, which are large files of up to a megabyte each. On the phone Talk One is 5.7.

### Why it's here

It is the contrast piece. My read: the lesson for Designcraft is that size and spacing can carry a page the way motion carries the others. The biggest thing on screen is always the title. The text is always the same comfortable size. Every extra is a small help to the reader. The caution: the portraits make a quiet page heavy, heavier than the Lando Norris page before you scroll it.

## What Sean said about it

Seen on November 17, 2026, with the rest of the shelf. He said nothing about this one by itself.

Of the whole shelf: "all of the options you provided are amazing in their own way and I wouldn't want to throw those out the window." He picked no favourite. It stays on the shelf as one end of the range.

## More details

- Awwwards site page (Site of the Day date, jury and member scores, Developer Award marks, the three credits, tags): https://www.awwwards.com/sites/poor-charlies-almanack
- John Gruber, Daring Fireball, December 29, 2023 (the quote and the e-book comparison): https://daringfireball.net/linked/2023/12/29/poor-charlies-almanack
- Blog post, December 7, 2023 (the free online edition came out with the new print edition; what Berkshire mode does): https://torstensson.com/2023/12/07/free-online-edition-of-poor-charlies-almanack/
- The page measured as the reading page: https://www.stripe.press/poor-charlies-almanack/talk-one
- My measurements: a private headless Chromium driven by a short script, at 1440 by 900 and 390 by 844, 10 seconds of settling, then a full scroll. The Three.js release it reports is 159. The Awwwards stack tool identified Next.js.
- I saw the Berkshire mode button on the page but did not press it.
- The Awwwards page-structure, scroll-map and motion tools would not run; they need a browser add-on, Playwright, that is not installed.
- Characters a line: one paragraph I counted ran 495 characters over 7 lines, the last of them short.
