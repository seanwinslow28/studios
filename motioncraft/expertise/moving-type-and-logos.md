# Moving type and logos.

Read this when a job puts words or a logo on screen: kinetic type, title cards, captions, a logo sting, an end card, or labels inside an explainer.

## What good looks like.

**The motion means something.** Type that moves well moves the way its words feel. Caption with Intention is the clearest case: a shouted word swells to twice the line's height in a heavier weight for about a quarter second, then relaxes over another quarter to a third; a whisper shrinks and thins; each speaker has their own colour. Loudness becomes size, pitch becomes weight, and a person becomes a colour. The words around the emphasis stay calm, which is why it lands.

**The type enters as the idea arrives.** The Stranger Things title builds letter by letter, never word by word. Each letter glides in on a straight line and slows into its place with no bounce, and the logo locks exactly as the music swells. Before that, slow close-ups of letter parts let you study shapes before you can read the word: mystery first, then recognition.

**Readable at a glance, for long enough.** A line has to be large enough, high enough in contrast and still long enough to be read comfortably, ideally twice. Caption practice works at roughly 15 to 17 characters a second for adults; display type deserves more. Moving type is hardest to read, so the reading time starts when the type settles, not when it appears.

**One voice, from first card to last.** Cast type by role before the first card: main title, chapter cards, labels, captions, the end card. One family per role, and the same placement for the same role in every shot, so labels share a top edge and captions sit on one line across the film. The viewer learns where to look once.

## Readability: size, time and contrast.

- **Size.** A phone shrinks the frame to a few hundred pixels wide, so check every card at phone width. Keep important type inside title safe, the area no screen crops: 5 percent in from each edge, 96 pixels at the sides and 54 at top and bottom of a 1920 by 1080 frame.
- **Time.** A word that appears as it is spoken, keyed to the voice's word timings, reads naturally because ear and eye agree.
- **Contrast.** Light type on dark or busy ground needs a little more letter spacing and often a little more weight, because light type looks thinner and more crowded than the same type dark on light.
- **A clear band for words.** Voice lines read best at one height, in a band that no moving object crosses while a line is up. Busy action lives above and below it.
- **Leave on the cut.** A line belongs to its picture. When the picture changes, the words leave on the same frame; words that hang across a change of scene look stranded, and words that arrive before their scene feel early.

## Kerning and spacing at display sizes.

Kerning is the space between one pair of letters; tracking is the spacing of a whole word or line. At reading sizes a font's built-in kerning is fine; at display sizes the gaps grow with the type, and a master corrects by eye.

- **Tighten as type gets big.** Large titles nearly always want slightly tighter tracking than the default.
- **Kern the troublesome pairs by hand.** Pairs involving T, W, Y and V, and pairs like LA, To, Wa and Yo, open visible holes in a headline. Kern until the spaces between letters look even, which is not the same as being measurably equal.
- **Open spacing only on capitals.** Capitals and small capitals can take generous tracking; lowercase and italic letters are designed tight and come apart when spaced out.
- **Check that the tool honours the font's kerning.** Some tools ignore a font's built-in pair kerning. Blender's text objects are one, so a headline set there shows gaps after T, W and Y. The fix is to read the font's own kerning pairs for the exact words, write them in as per-character spacing, then fine-tune by eye.
- **Never stretch letters to fit.** Squeezing or stretching type thins some strokes and thickens others. Use a drawn condensed or wide style of the family instead.
- **Use the right cut for the size.** Many families have display cuts for big sizes and text cuts for small ones. A display cut used small goes frail; a text cut used huge looks heavy and blunt.

## Hierarchy.

Hierarchy is the order in which the eye reads. Build it one cue at a time: first space, then weight, then size, adding a new typeface last. Stop as soon as the parts separate. In motion, each cue can become a beat: the headline lands, a beat later the weight shifts, then the supporting line arrives. Elements moving as a unit are read as a unit, and anything that breaks the pattern, in colour, weight, size or path, draws the eye. Keep a few sizes clearly apart, on a gentle scale, rather than many that nearly match.

Variable fonts are a gift here. A variable font holds a continuous range of weights or widths in one file, so a word can swell and relax smoothly instead of jumping between styles; Caption with Intention uses one this way. When weight animates inside a held line, a uniwidth face, whose letters keep their width at every weight, stops the line from reflowing. A weight or width axis can even carry a quantity across a sequence, rising with the thing it measures.

## Logo stings, and how they land.

A sting is a logo's few seconds of motion. The best ones on the shelf share a shape.

- **Two beats: a move, then a settle.** The Apple TV intro spends a second and a half on a fast move through layers of glass, then drifts to rest. The motion drops about tenfold in a quarter of a second, keeps halving, and is completely still for the last two seconds.
- **The logo holds readable for most of the time.** About three and a quarter seconds of Apple's five; about two and a half of each seven in BBC Two's "Squish", with the wordmark readable throughout.
- **Sound lands just after the logo reads, not on the move.** Apple's chord hits about a quarter second after the logo becomes readable, like a full stop. Stranger Things saves its one big swell for the lock.
- **Restraint reads as confidence.** None of these bounce, overshoot or sparkle. The energy goes into the move; the settle is calm.
- **A system can be the logo.** BBC Two's curve is a shape every ident must hit on exact frames, made each time from a different material. The rule is strict, and everything else is free.
- **Lengths for different jobs.** Apple made one-, five- and twelve-second versions, each with its own sound. If it works at one second, the longer versions only add pleasure.

## How it goes wrong, and the fix.

- **Every word animated.** When everything moves, nothing stands out. Keep most words still and move only the ones that carry the feeling.
- **Bounce and overshoot by default.** Springy easing everywhere looks like a template. Choose the ease for the meaning.
- **Gaps in a headline.** Uncorrected kerning after T, W and Y, or a tool that dropped the font's kerning. Kern the pairs by eye at final size.
- **Unreadable on a phone.** Check at phone width and go bigger than feels necessary.
- **Words over clutter.** Clear a band for the line or give it a calm panel.
- **Fake styles.** Slanted roman passed off as italic, shrunken capitals passed off as small caps. Use the family's drawn styles, or a different family.
- **A logo that never rests.** Give the settle time and end on stillness.
- **Interface text nobody can read.** A real screenshot flashed too fast to read is noise. Either make text legible and hold it, or soften it on purpose, as Ordinary Folk's 2021 Webflow film does with blurred product panels that give the feeling of the product without its manual. Their 2019 film puts no words on screen until the closing logo and lets the voice do the explaining.

## Examples.

- Caption with Intention (`../research/caption-with-intention.md`): type mapped to how words sound, with timing tested on 125 Deaf and hard-of-hearing viewers.
- The Stranger Things title (`../research/stranger-things-main-title.md`): letter-by-letter assembly, dissolves on a steady rhythm, the lock on the swell.
- Apple TV's glass intro (`../research/apple-tv-glass-intro.md`): the move-and-settle sting, with the sound as a full stop.
- BUCK's GitHub explainer (`../research/buck-what-is-github.md`): interface shown as a picture idea first, with only brief stylised labels such as "Done" and "Building".
- Ordinary Folk's Webflow films (`../research/ordinary-folk-webflow-no-code.md`): restraint with words, and product panels softened past reading.
