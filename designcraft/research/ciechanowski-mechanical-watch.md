# Bartosz Ciechanowski's "Mechanical Watch" (2022)

## What it is

A long web article by Bartosz Ciechanowski, published on May 4, 2022. It explains how a wind-up watch works, starting from a single spring and adding one part at a time until the whole mechanism is running.

Nearly every step comes with a small 3D model set into the page. The reader can turn each model by dragging it, and most have a slider that winds a spring, turns a gear or lifts a part away. It sits on his personal site under his name alone. The page asks readers who enjoy the articles to support him on Patreon, a site for paying makers directly.

It is here as the far end of "get interactive": the reader does the reveals.

See it: https://ciechanow.ski/mechanical-watch/

**Best moment: the very first model, at the top of the page.** It is the finished watch mechanism. Drag it to look around, then pull the slider to see inside. That one model is the promise the rest of the article keeps. Runner-up: the last model, under "The Size of it All", where an outline the size of a credit card shows how small everything you have just learned really is.

## How it turned out

- **Readers voted it to the top.** On Hacker News, a tech news site where readers vote stories up, it has 4,298 points and 413 comments. That is the highest score of any of his articles there. The next eight sit between about 2,100 and 3,100.
- **It keeps coming back.** It was posted again in December 2023 (954 points) and in June 2026 (745 points), four years after it came out.
- **He kept the approach.** His archive lists four more articles in the same form after this one, the latest in December 2024. Each scored between about 2,500 and 3,100 on the same site. The archive shows nothing newer as of November 16, 2026.
- **Trade notice.** A watch newsletter, Rescapement, ran a piece whose headline calls it the "coolest explainer" on the subject. I read the headline only, not the piece.
- **No award found,** and I could not read his supporter count on Patreon.

## What makes it good, measured

I fetched the page source on November 16, 2026 and counted with a short script. Colours and type come from the page's own stylesheets.

- **Length:** about 8,000 words of body text (8,031 by my count; a second count got 8,175). At an ordinary reading speed of 230 words a minute that is 35 minutes before you touch anything.
- **93 models, 74 with a slider.** That is one model for every 86 words on average. The middle gap between two models is 77 words, and the longest is 266.
- **11 chapters, then a reading list and a closing note.** Models per chapter:
  - Power, 12.
  - Gears, 5.
  - Escapement, 3.
  - Balance, 7.
  - Mainplate, 13.
  - Click, 12.
  - Motion Works, 4.
  - Date, 5.
  - Keyless Works, 22.
  - Automatic Winding, 7.
  - The Size of it All, 1.
- **The opening:** 337 words and 2 models before the first chapter heading.
- **Each model follows the same three beats.** The text says what to try. The reader tries it. The next lines name what just happened. The phrase "demonstration below" appears 18 times and the word "Notice" 25 times.
- **Problems drive it forward.** A naive first version is built, shown failing, and fixed. Early on, a watch with no gears spins its hand far too fast, and the text says there is "some work to do".
- **What the reader can touch:** the models turn when dragged. The page says so for the first one, and I did not test all 93. Of the 74 sliders, 31 put a part in or take it out, and 27 are coloured to match the part they move. The text names parts by colour too, so "the yellow gear" in a sentence is the yellow gear in the model. Yellow is named 14 times, blue 10 and red 4.
- **Colour:** the page is pale grey, #F8F8F8, with dark grey text, #444. All the strong colour sits inside the models and their sliders: a yellow, rgb(237, 194, 73), a red, rgb(243, 86, 92), and a blue, rgb(79, 162, 229).
- **Type:** IBM Plex Sans, a plain sans, for the text. Headings are in Inter, another plain sans. Chapter headings are one or two words.
- **How it is built:** the page loads only two scripts of his own, plus one that counts visitors. There is no outside animation or 3D toolkit in the source.

Against Sean's four story rules:

- **Every headline states its point: broken.** The headings are labels: "Power", "Gears", "Click". The claims live in the sentence above each model.
- **Plant something early that the close pays off: kept.** The finished mechanism is the first thing on the page. Every chapter after it earns one more part of that picture, and the closing note returns to the whole watch coming "alive".
- **One idea per slide: kept.** One model shows one behaviour.
- **The reveal happens in silence: kept, in a new form.** The reader's own hand is the click. The text sets up, stops, and only then names what they saw.

### Why it's here

It proves that spectacle does not need decoration. The page is nearly unstyled, and readers were still voting it up four years on. My read: the lesson for Designcraft is that one thing the audience can move, placed right after a plain sentence of setup, does more than any amount of motion they only watch. The caution is cost. This is 93 hand-built models by one person, and a talk can afford perhaps two or three.

## What Sean said about it

Seen on November 17, 2026, with the rest of the shelf. He said nothing about this one by itself.

Of the whole shelf: "all of the options you provided are amazing in their own way and I wouldn't want to throw those out the window." He picked no favourite. It stays on the shelf as one end of the range.

## More details

- The article (word and model counts, colours, type, scripts): https://ciechanow.ski/mechanical-watch/
- Hacker News, first post, May 4, 2022 (4,298 points, 413 comments): https://news.ycombinator.com/item?id=31261533
- Hacker News, posted again December 2023 (954 points): https://news.ycombinator.com/item?id=38591084
- Hacker News, posted again June 2026 (745 points): https://news.ycombinator.com/item?id=48553550
- His archive (the later articles and their dates): https://ciechanow.ski/archives/
- His Patreon page (count could not be read): https://www.patreon.com/ciechanowski
- Rescapement headline: https://rescapement.com/blog/this-is-the-coolest-explainer-on-how-a-mechanical-watch-works-ive-ever-seen
- My measurements: page source and two stylesheets fetched with curl on November 16, 2026. Words are the text inside paragraph tags. Models are the page's demo containers and sliders are counted from the markup. Scores for his other articles come from the Hacker News search service, read the same day.
- Not confirmed: how the models are drawn. A reader on Hacker News says they are hand-written WebGL, a way of drawing 3D in a browser. The source fits that but I did not read the script itself.
