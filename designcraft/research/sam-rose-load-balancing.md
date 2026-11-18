# Sam Rose's "Load Balancing" (2023)

## What it is

A web article by Sam Rose, a software engineer who writes visual explainers about programming, published on his own site on April 10, 2023. The page says it was updated on October 25, 2026, and that version is the one measured here.

It explains a load balancer: the part of a big website that decides which of several computers, called servers, handles each incoming request. It adds one complication at a time, and each step is a simulation: a small working model that runs the real rule, drawn as plain shapes.

**Two rules matter for the best moment.** Round robin sends each request to the next server in turn, however busy it is. Least connections sends each request to the server with the least work waiting.

It is here as the plain end of drawn pictures: no characters, no decoration, and every mark stands for something.

See it: https://samwho.dev/load-balancing/

**Best moment: scroll to the end of "When round robin doesn't cut it" and press play.** Five servers of different strength take turns getting work. The weakest one piles up a queue, its waiting dots turn from green toward red, and some are dropped. Then press play on the first drawing under "Moving away from round robin": a similar set of servers, a smarter rule, and the pile-up is gone.

## How it turned out

- **Readers voted it up.** On Hacker News, a tech news site where readers vote stories up, it scored 1,143 points and 217 comments on April 16, 2023. His "Memory Allocation", in the same style, scored 1,360 a month later, and a 2025 piece on big O notation scored 691. The series kept landing.
- **It is the piece he is known for.** In a February 2025 interview with the newsletter Write That Blog, he said: "The post I hear the most about is Load Balancing."
- **His model is on this shelf.** In the same interview he says he had long admired a site he links, and wanted to bring its style to programming. The link is to Bartosz Ciechanowski's site, home of the "Mechanical Watch", though he doesn't name him.
- **He now explains for a living.** His author page at ngrok, a networking company, calls him a Senior Developer Educator, with posts there since October 27, 2025. Nothing I read says the articles got him the job.
- **The caution:** no award found, since these are personal articles, not entered for prizes. And the reception is for the 2023 version: the page has been updated since, and I could not see what changed.

## What makes it good, measured

I loaded the page on November 18, 2026 in a private test browser, at a laptop size (1440 by 900) and a phone size (390 by 844). Sizes and colours come from the running page, colour rules from its stylesheets and its one script, and timings from a short script that logged every animation the page started.

- **Flat shapes, no shading, no texture, and four parts:** servers are grey 50-pixel squares with 9-pixel rounded corners; the load balancer is the same square in near-black; requests are 20-pixel dots; and a queue is a small tube above each server, holding up to three waiting dots. The only outlines are 1-pixel borders, a shade darker than the fill.
- **Colour has three jobs, and only three:**
  - Grey is server strength, from light (weak) to dark (strong). The text says so in one line.
  - Near-black is the load balancer.
  - Green to red is how long a request has waited. Its colour mixes from green (#009E73) toward red-orange (#D55E00) over 10 seconds, in quarter-second steps. A dropped request turns fully red.
- **The colours come from the Okabe-Ito palette,** eight colours chosen to stay distinct for colour-blind readers.
- **The words are the legend.** "Request" is printed in green with a small dot beside it, "drop" in red, "server" in grey and "load balancer" in black. The sentence above a drawing tells you how to read it, with no key.
- **It waits for a press, then keeps going.** Each of the 15 simulations sits still until you press play, runs until paused, and pauses itself when scrolled out of view. A slider with a tortoise at one end and a hare at the other sets the speed.
- **How long each move takes.** In the 8 seconds after pressing play on the "before", the page started 174 animations. From that log:
  - A request travels in short legs of 0.19 to 0.35 seconds, at a steady speed.
  - It settles into a queue place in 0.16 seconds, slowing as it lands. That slowing is called easing.
  - A ring sweeps round a request while a server works on it, and each sweep lasts exactly as long as that server takes: 0.27 to 2.14 seconds in this sample.
- **The setup is written into the page in plain numbers.** Each simulation states its servers' strengths, the requests per second and their cost, the queue length and the rule. The "before": five servers of strength 1, 3, 5, 6 and 8; five requests a second, each costing 100 to 300; three queue places; round robin. The "after": strengths 2, 4, 6, 8 and 10, the same traffic, least connections. *Read from each simulation's settings in the page source.*
- **The drawing is the rule running, not a cartoon of it.** Requests go where the rule sends them, the sweep lasts as long as the work, and the colour is the wait.
- **The article is long; the labels are short.** About 3,100 words, in one column, with text above and below each drawing. A median of 138 words sits between one simulation and the next. Each drawing also carries a hidden one-sentence label for screen readers, median 14 words. The "before" label says, in 16 words, that slower servers queue work while faster ones may sit idle. *Counted from the article body in the page source.*
- **On a phone** the drawings shrink to 358 pixels wide and keep every part, with no sideways scrolling.
- **With less motion on,** the setting a visitor can turn on in their device to ask for less animation, a decorative coin machine at the top stays still. The simulations still run when pressed, because here the movement is the information. But the settles become instant, new requests appear without popping in, and each ring sweep becomes a fade of the same length. The same 8 seconds started 84 animations instead of 174.
- **Weight: 0.12 megabytes** to show the page, in 17 downloads. No pictures beyond a few tiny icons, no downloaded fonts and no animation library: the drawings are plain page elements, moved by the browser's own animation feature.

### Next to the Mechanical Watch

The same idea carried to software, with four differences: it is flat and 2D, not 3D models you turn by hand; it runs by itself after one press, instead of the reader dragging a slider; colour carries a measured value, how long a dot has waited; and each drawing has a short label written for screen readers.

### Why it's here

It is the cleanest example found of a technical record turned into a drawing that stays true to it: stated numbers in, honest motion out. My read on what it teaches a designer: let one colour carry one fact, let the words in the text double as the legend, and show a decision as the same drawing run twice with one rule changed, so the result shows without a word. When a visitor asks for less motion, keep the movement that carries information and drop the rest.

The cautions: the article around the drawings is a long read; the drawings are small on a big screen, 480 pixels wide on a 1,440-pixel screen; and the before-and-after pair is not a perfectly controlled comparison, since the servers differ (strengths 1 to 8 against 2 to 10).

## What Sean said about it

Seen November 18, 2026, as an example for his portfolio site's drawn pictures. No comment of his own yet.

## More details

- The article, with its published and updated dates: https://samwho.dev/load-balancing/
- Hacker News, first post, April 16, 2023 (1,143 points, 217 comments): https://news.ycombinator.com/item?id=35588797
- Hacker News, "Memory Allocation", May 22, 2023 (1,360 points): https://news.ycombinator.com/item?id=36029087
- Hacker News, "A visual introduction to big O notation", August 24, 2025 (691 points): https://news.ycombinator.com/item?id=45002182
- Scores read from the Hacker News search service on November 18, 2026.
- The interview, February 6, 2025 (the quote and the link to ciechanow.ski): https://writethatblog.substack.com/p/sam-rose-on-technical-blogging
- His ngrok author page: https://ngrok.com/blog/author/sam-rose
- Timings: a script logged every animation the page started for 8 seconds after pressing play, once normally and once with less motion on. Word counts: the article body, split at each simulation, over the 11 gaps before the charts begin (63 to 174 words).
- Not checked: how it feels under a real hand; the 2023 version readers voted for; the keyboard and a screen reader (the labels were read, not tested); dark mode; and the charts and playground at the end of the article.
