# Design pictures

Sean can't judge a system design by eye, and a page of prose about one is hard to rule on. So Systemcraft shows him a design as a simple drawn picture on a house review page, the page every checkpoint uses. The plain steps sit beside the picture, and a weaker version of the same design sits next to it for comparison. Read this before showing Sean any design.

## What it's best at

- **One design, seen in one glance.** A single column of boxes, read top to bottom in a few seconds.
- **Making the choice visible.** The weaker version is drawn with the same boxes, so the eye lands on the two or three that differ. That difference is the decision Sean rules on.

Where another tool beats it:

- **A bigger system,** with boxes inside boxes, goes to D2 (`d2.md`).
- **A small flow inside a markdown file** can be Mermaid, which GitHub draws on sight (Productcraft's `mermaid-and-docs.md`).
- **Comparing numbers,** such as what two designs cost to run, wants a table.

## Setup

Nothing to install or pay for. The pieces live in Sean's private brain repo:

- **The page template and its packer,** which turns one content file and its pictures into a single page file.
- **The screenshot checker,** which photographs a page at desk and phone size, by day and by night. It needs Node 22 or newer and Google Chrome; both are here.
- **The drawing script** behind the shelf page's pictures. It sits in that page's own folder, not with the shared tools.

The commands that prove it works, using any page name already in that folder's `docs/`:

```bash
cd ~/Code-Brain/SWCB/docs/prototypes/house-look
python3 build_page.py <name> --out /tmp/house-test.html
node tools/shoot.mjs /tmp/house-test.html /tmp/house-test-shots
```

The first prints the new file's path and size. The second prints "4 screenshots", and fails on a page error or sideways scroll. If `tools/` is missing, the brain's folder is on an older branch. Tell Sean; don't switch it.

## How a page gets built

A page is one folder: a content file (`decide.json`), the picture files, and the text file the pictures were drawn from.

- **The words** go in the content file, as the review-pages guide lists them. The page adds "I can't tell" by itself.
- **The pictures** go in its `show` list: a picture file, a short tag, a one-line caption, and a description in words for anyone who can't see it.
- **The plain steps** go in `cards`.

The packer reads only a folder that sits beside it. A studio-wide page such as the shelf is saved there. A job's page keeps its folder with the job and borrows a link for the build, as other studios' jobs do:

```bash
ln -s <job folder>/pages/<name> docs/<name>
python3 build_page.py <name> --narrate --out <job folder>/review-<name>.html
rm docs/<name>
```

`--narrate` adds the Listen clip. The link sits inside the brain for one command; never save it there. Then run the plain-writing check and the screenshot checker on the packed page, and look at the shots.

## Getting the best out of it

**One design per picture.** Two in one drawing is a comparison nobody can read.

**Seven to twelve boxes.** The shelf's Stripe entry has eight plain steps. Its picture has six boxes, plus two for the weaker version. Past twelve, split it or go to D2.

**The same shapes mean the same things, every time.**

| What it is | How it's drawn |
|---|---|
| A person | Amber fill. By hand, rounded ends too |
| A model step | Rounded box, blue outline |
| A fixed step of ordinary code | Grey outline, green if it's a check. By hand, square corners too |
| A file or store | Grey outline. By hand, a sheet with a folded corner |
| A wall around where something runs | By hand only: a dashed frame, named on its top edge |
| An outside source | By hand only: a slanted box, outside every wall |
| Where it goes wrong | Red dashed outline |

Colour alone fails for anyone who can't tell red from green, so by hand each kind gets its own outline too.

**Label arrows with what passes along them.** "Attachments only" on an arrow says more than the two boxes it joins. In the weaker version the same arrow reads "the whole email".

**Draw the person wherever they step in.** In the Stripe picture the amber boxes sit at the top and the bottom and nowhere between. That is the design, seen before a word is read.

**Draw the weaker version with the same boxes.** Same order, same labels, and only the changed boxes turn red. On the shelf page the weaker version was a couple of red summary boxes under each design. For a design Sean rules on, redraw it box for box.

**Title it with the point.** "A person checks the odd ones before anything is saved" beats "Receipt sorter design".

**Two to four plain words a box, taken from the design itself.** "Code checks the sums", not "Validation layer".

**Mark a guess as a guess.** A guessed number says so in its box: "a guess: about 1 in 10".

**Number the boxes, and give the plain steps the same numbers.** Sean can then point at "step 4".

**One ruling per page.** One question, the lead's pick with one line on why, and the alternative Sean might prefer with an honest line on what it buys. If he needs teaching first, that is a separate page, shown first.

## How to draw them

**The script.** The shelf page's pictures came from a short text file: for each picture, a title and a list of boxes, each with a label, a kind and an optional small line. The script stacks them in one column with arrows between, and can set boxes side by side for work done in parallel.

```bash
python3 docs/systemcraft-shelf/draw.py pictures.json <page folder>
```

It can't draw a wall, an outside source or a label on an arrow, and a file looks the same as a fixed step. Until it grows those, what passes along an arrow goes in the next box's small line.

**By hand.** When the design needs a wall or labelled arrows, write the picture by hand as SVG, a picture written as text, in the script's colours.

**Sizes.** The page squeezes each picture to fit. Measured on a test page:

- The script draws 420 wide. A phone shows that 291 wide, so type lands at about 70% of its drawn size: labels near 13 pixels, small lines near 11. Keep anything that must be read in the label. By hand, draw labels at 20 or more.
- Two pictures side by side on a desk show at drawn size. Three across shrink to 65%. One picture alone doubles, and runs about two screens tall.

So a design Sean rules on is two pictures: the design, and the weaker version. On a desk they sit side by side with the boxes lined up. On a phone the weaker one falls underneath.

**Day and night.** A picture is a sealed image. It can't follow the page's Day and Night button or borrow its font, so it carries its own paper background. On the night page it shows as a cream card, still readable. Never draw on a see-through background.

**Check the picture, not its source.** The script guesses how wide words are, so a long label can spill out of its box, and only the finished picture shows it. Two traps:

- The checker doesn't scroll. Pictures far down the long shelf page hadn't loaded when it was shot, so its shots show no pictures. On a long page, open it and scroll as well.
- The plain-writing check can't read words inside a packed picture. Run it on the pictures' text file too.

## Where it goes wrong

- **The picture that shows everything.** Every retry, log and odd case, and nobody can find the decision. Cut to the boxes the ruling turns on.
- **Decoration.** Draw only when the shape says something words don't: an order, a wall, where the person stands.
- **A guess that looks settled.** A clean box around a number nobody measured. Mark it or leave it out.
- **Teaching and asking at once.** A page that explains what an agent is and also asks for a ruling gets a tired answer.
- **Codes creeping in.** A file name as a box label, a job's code in the title. Those go under the page's "More details".
- **A weaker version nobody would build.** Draw the one a sensible person would choose to save time.

## Safety

- **Everything here runs on the Mac** and uploads nothing. An opened page asks Google for its two fonts and sends nothing about the design.
- **A page may be published only as a private page.** A packed page can go up as a Claude artifact, which is private until shared. Ask Sean before sharing it with anyone.
- **This repo is public.** Pictures and pages about Sean's own systems never go in it. They stay in the job's folder or the private brain, and day-job material stays in his private work repo.

## More details

Checked November 16, 2026, on this MacBook, with Python 3.14.8, Node 22.22.2 and Chrome 157.

- **Read:** `craftwork/guides/review-pages.md`. In the brain: `docs/pages/DESIGN.md`, and under `docs/prototypes/house-look/`: `build_page.py`, `decide.html`, `tools/`, and `docs/systemcraft-shelf/` (`draw.py`, its text file, twelve pictures).
- **The shelf page:** built November 15, 2026; Sean answered it the next day. Twelve pictures, three across on a desk.
- **Ran:** the real packer on an existing page, with `--out` to a scratch folder. The drawing script on a made-up receipt sorter. A scratch copy of the packer built three test pages: script and hand-drawn pictures together, one picture alone, and a design-and-weaker pair with step cards. The checker took 4 shots with no errors; all four were looked at.
- **Measured** in headless Chrome, desk 1440 wide and phone 375: pictures 291 wide on the phone, 425 two across, 273 three across, 880 alone.
- **The plain-writing check** passed the packed test page and caught a file name planted in a pictures file.
- **Not confirmed:** `--narrate` was not run. No artifact was published; that rests on the review-pages guide and Productcraft's `claude-artifacts.md`. Link, pack and unlink ran on the scratch copy only. The phone was emulated. The hand-drawn shapes are this guide's proposal, tested on one made-up page; Sean has not seen them.
- That day the brain's working folder had no `tools/` and no shelf folder. The copies on its main branch were used.
