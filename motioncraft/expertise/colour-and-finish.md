# Colour and finish.

Read this when the picture is nearly locked and the job turns to correcting, grading and delivering files.

## What good looks like.

**Correct before you grade.** Correction makes every shot honest and alike: neutral things neutral, blacks and whites where they belong, shots that cut together without a jump. Grading then gives the whole piece one look. Grading uncorrected shots means each one fights its own way to the look, and they never quite match. In animation the artwork is often designed in colour from the start, so correction is mostly about keeping that design intact through the pipeline and making rendered shots agree with each other.

**Contrast first, then balance, then saturation.** Pin the darkest black and the brightest white first, then place the middle tones, which decide time of day and mood. Only then touch colour, because how bright a region is decides which colour control reaches it. To remove a colour cast, find where it sits (in the shadows, the middle tones or the highlights) and push that range toward the opposite colour until neutral things read neutral. Then set saturation, easing it off in the deepest shadows and brightest highlights.

**Memory colours.** Some colours the audience knows by heart: skin, sky, grass, a familiar brand colour. People forgive shifts elsewhere but notice a wrong one of these at once. Skin stays in a narrow band of hue across very different complexions; skies sit in a narrow band of blue that fades toward the horizon. In animation the equivalent memory colours are a character's key colours and the brand colour. Protect them first.

**A grade that serves the look.** Write the look as one sentence before touching a control, such as "warm late-afternoon light in a small handmade town". Light lives in the highlights and skin lives in the middle tones, so warm or cool the light in the highlights and push the middle tones slightly the other way, which keeps faces from turning orange or blue. When a frame wants "more colour", lift one distinct hue against the rest instead of raising saturation everywhere; colour contrast reads as richness, global saturation reads as plastic.

**Consistency shot to shot.** Pick one representative shot per sequence, set its look carefully, and match every other shot to that still. Matching each shot to its neighbour lets small errors add up, so the last shot of a sequence ends up unlike the first. When a match won't come, move on and look again later; tired eyes adapt to a cast and stop seeing it.

**Titles and type.** Text reads cleanest a little under full white and a little less saturated than the picture around it, so it sits in the frame rather than glowing on top. Never sharpen, blur or denoise type the viewer has to read.

**A master and a web copy.** A finished piece is usually delivered as two files from one finished timeline. The master is the high-quality reference every later copy is made from: lightly compressed, high bit depth, uncompressed audio. The web copy is small and plays everywhere, with its index at the front so it starts streaming at once. Every copy comes from the master, never from another compressed copy, because each lossy generation costs detail and colour.

**Frame rate and size are constant and agreed.** Pick one size and frame rate for the whole piece, keep them constant and progressive, and make the delivered frame count match the approved timing exactly. Changing between 24 and 25 frames a second shifts running time and pitch by about four percent, so convert deliberately or not at all.

**Colour tags tell players how to read the file.** A video file carries labels for its colour primaries, its transfer curve and its matrix. Most web and HD work uses the Rec.709 standard for all three. An untagged or mistagged file makes players guess, and players guess differently: Safari and QuickTime are known to show Rec.709 a little lighter than other browsers. Tag every file explicitly, and check the web copy beside known swatches in the browsers that matter.

**Fine colour survives compression only so far.** Web formats store colour at a quarter of the picture's resolution and in 8 bits, so pale near-neutral colours, like a cream background, can drift visibly, and thin coloured edges soften. Colour difference is measured as ΔE (delta E), where about 1 is the smallest difference most people can see. A brand colour within about 1 of its design, and broad fields within about 1.5, is a sound aim for the web copy.

**Loudness is checked on each file.** The target is set by where the film goes (web: about −14 LUFS, true peak at or under −1 dBTP; see the sound brief), and compression can raise peaks, so measure the master and the web copy separately.

**Fonts the piece is allowed to use.** System fonts and subscription fonts often forbid embedding the file in artwork or keep working only while a subscription lasts. Open-licence fonts, such as those under the SIL Open Font License, allow copying the file into the project and using it in video and commercial work. Copy each font file and its licence into the project so it renders the same anywhere.

**Motion blur and grain that belong.** Real motion blur averages several moments within each frame, so a fast move smears as a camera sees it. Adding an editor's blur on top of blur already in the frames doubles it into mush. Film grain, if the look wants it, should be fine, about two pixels across, monochrome, centred on zero so it never darkens colours, and new every frame. One-pixel grain doesn't survive web compression, frozen grain reads as dirt on the lens, and grain costs bit rate on every frame.

## How it goes wrong, and the fix.

- **A grade before correction.** Shots still mismatch underneath the look. Go back, correct each shot to neutral and to the reference still, then reapply the look as one shared layer.
- **Milky shadows.** Lifting the shadow control over large solid blacks turns them grey and exposes stray colour. Lower the lift and add brightness in the middle tones instead.
- **Magenta or ashen skin.** Overcorrecting a green cast swings skin to magenta; cutting shadow saturation too far makes it grey. Ease the correction back and give skin a trace of the scene's light rather than protecting it completely.
- **Drift across a sequence.** Each shot matched to the last. Re-match every shot to the one hero still.
- **Colours that shift on the web.** Missing tags, or tags the player ignores. Tag all three colour values, and compare the web copy in real browsers against swatches.
- **Blocky shadows after compression.** Crushed blacks give the encoder nothing to describe. Keep a little detail above pure black, and give grained or dark material more bit rate.
- **Finishing from a web file.** Every later copy inherits its damage. Always go back to the master.
- **Renders that don't repeat.** Save the project, close it, reopen it in a fresh session, render again and compare the two renders frame by frame, decoded to plain pixels. Any differing frame, however small the difference, means something in the project isn't saved or isn't stable. Compare lossless renders, never web copies, and decode carefully: a careless conversion from a 10-bit master to 8-bit pixels can read a few levels low and invent a difference that isn't there.

**A few Resolve lessons about colour and delivery,** with detail in the Resolve guide. Rendering a ProRes source to ProRes at the same size and rate can copy the file untouched, so a grade can seem not to apply; render to another format to force processing. In the version tested, Resolve 21.1.1, fades set in the editor were lost on save and reload, so a title's fade is safer baked into the title's own frames. Under default colour settings Resolve wrote flat colours into the master at their exact values, so a colour that reads wrong is usually in the reading, not the render.

## Examples.

- **Sean's first film** delivered at 1920 by 1080, 24 frames a second, as a ProRes 422 HQ master with uncompressed audio plus an H.264 web copy, both tagged Rec.709 and each checked separately. That is a typical delivery for a short web film, not a rule; a TV job or a 4K request changes it.
- **The Line's Freeview Play film** shows a grade serving a story. The town sits in dark browns and warm cream; the heroes get a screen blue and a coat yellow that are small in area, which is why they pop. The last fifteen seconds turn warm and golden at sunrise, so the colour itself tells you the ending is happy.
- **When the Day Breaks** keeps almost everything a faded grey-blue and rations colour to a lemon, a red cross and a green bowl, so the eye goes straight to each.
- **Hair Love** drops from warm pastels into near-black with a single spotlight for the fight, a whole-palette change that says the battle is in the dad's head.
