# Design and look.

Read this when a job reaches its look: before the first style frame, whenever a piece starts to drift between shots, and whenever a look feels wrong and nobody can say why.

## What good looks like.

**One world, one light.** A convincing look is a set of decisions applied everywhere: one shape vocabulary, one palette with a job for each colour, one direction of light, one way of handling texture. The viewer only feels that every frame belongs to the same place. Even a piece that changes medium on purpose, as BUCK's GitHub film does, holds one thread: a character, a palette and a motif in every chapter.

**A style frame settles the look before anything moves.** A style frame is one finished-looking still of a key moment, made to the standard of the final piece, so motion is never spent on a look nobody has agreed. A good one is built from artwork that can actually move: characters separable from backgrounds, layers that can sit at depth, nothing painted across a join that must later come apart.

**Shape language carries feeling before colour does.** Round shapes read as soft and friendly, squares as steady and dependable, sharp triangles and diagonals as danger or energy. A master picks a dominant shape family per character and per world, and sets straights against curves inside each form so nothing goes limp. The Line's blue TV is a soft rounded box with a face of two curved lines; the red TVs that bully the town are blockier. Shape alone tells you who to trust.

**Value comes first, then colour.** Value is how light or dark something is, with colour ignored. A frame that reads in greyscale survives any palette. Good frames group into three or four clear values, with the strongest contrast where the eye should land. The commonest failure is a background that outshines the moving subject in brightness or colour, which pulls the eye away.

**A colour script gives colour a story job.** A colour script is a row of small frames, one per key beat, showing how colour changes across the piece. The working pattern: one colour that belongs to the film, one accent, and at most one surprise colour saved for the moment that matters. For each beat, pick one lever: hue for danger or a turn, value for fear and loss, saturation for joy returning. The Line's town sits in dark browns and a warm cream; the heroes' screen blue and coat yellow are small in area, which is exactly why they shine, and the last fifteen seconds warm into sunrise gold. Ordinary Folk's 2019 Webflow film tells its whole arc in brightness alone: dark navy for the problem, a sudden jump to pale lilac and sky blue for the promise.

## The main looks, and what makes each convincing.

**Painted.** The Monk and the Fish is the model: each background is one rich watercolour painting that holds still, while the moving characters are simple ink outlines with flat fills. Texture lives in the still layer; the moving layer stays simple so it reads. A painted look convinces when the marks have a hierarchy: big strokes in big shapes, crisp edges where the eye should go, soft or lost edges elsewhere, colour that varies inside a shape the way real pigment pools.

**Vector.** Confident shapes from a small, consistent system: one corner radius or a deliberate few, one stroke weight or none, a fixed set of angles, a limited palette. It convinces when every shape looks drawn by one hand; a light grain keeps it from feeling sterile. It fails with mismatched radii, stray outlines from automatic tracing, or default gradients.

**Miniature set, or a stop-motion feel.** The Line built a model town inside the computer and kept the imperfections of stop motion. It convinces through materials you could touch (felt, card, painted wood, clay with fingerprints), soft light from a few believable sources, shallow focus that makes the world feel small, and motion with a slight stepped quality. The camera side of this look is in the camera and depth brief. It fails toward the slick look of a video game: perfect surfaces, even lighting, everything sharp.

**Flat graphic.** Bold shapes, no lighting, depth only from overlap, scale and value. It convinces when composition carries everything: one idea per frame, generous empty space, a recurring shape motif. BBC Two's idents push a graphic system furthest: one fixed curve every ident must hit on exact frames, made each time from a different material.

**3D.** The Apple TV glass intro sets the bar: real glass and real light, filmed, so every reflection is earned. Computer-made 3D convinces when it borrows that discipline: materials referenced from real objects, light placed with intent, focus that falls off, small imperfections. It fails as default sheen and uniform light.

## One look across AI images and video.

AI tools drift: every prompt is a fresh guess at the style, so a piece made shot by shot slides between looks unless the look is pinned down.

- **One fixed style description,** written once from the references and pasted word for word into every image and video prompt. Paraphrasing it per shot is how drift starts.
- **Each key frame from two references:** a layout image fixes the framing, and a style reference fixes the look. One image doing both jobs muddles both.
- **Characters designed by silhouette first,** with front, side and back sheets, and a fresh sheet whenever a pairing or a prop changes. Tricky props get their own stills before any video.
- **Each reference gets one labelled job in the prompt,** so the model knows which image sets the face, which the setting and which the light.

The full method is in `../tools/higgsfield.md`. A loose painted look forgives drift that a miniature-set look will not, because a model world is judged against real materials.

## Painted texture in motion.

A painted film feels hand-made partly because its texture is alive. Texture continuity means texture travels with the thing it belongs to and changes only as designed. Two opposite failures break it.

- **Sliding.** Texture stays fixed to the screen while the picture moves beneath it, as if seen through patterned glass. Attach texture to the moving surface so grain and brush marks ride along.
- **Undesigned flicker.** Texture changes at random every frame and fizzes like noise.

A master handles the tension by designing texture as separate layers, each with its own rule for change. Line boil is the small wobble of a contour from drawing to drawing, which keeps slow moments alive. Pigment variation is the change of colour and density inside painted areas. Paper grain is the texture of the surface underneath. Then:

- Keep identity marks and contact points steady while the line boils, and keep paper quiet.
- Never let line, pigment and paper all change on the same frames.
- Save strong silhouette change for designed smears, the stretched in-between drawings of fast moves.
- Watch for a loop seam, a pop where a cycle wraps from its last drawing back to its first.
- Never fake boil by shaking a whole layer rigidly; the outline must actually change shape.
- Judge boil at full speed, at the size the piece will be shown, through the camera move. Stills hide every one of these failures.

There are no universal settings; each shot earns its own.

## How it goes wrong, and the fix.

- **Painting that reads as childlike.** On Sean's first film, painting generated by script, with marks placed by code rather than by a painter's hand, came out looking like a child's picture. The cause is evenness: every stroke the same size and pressure, every edge equally hard, colour filled rather than mixed, no hierarchy telling the eye where to go. The fix is a real painter's decisions. Today that means AI-made painted frames finished by hand in Krita.
- **A gorgeous world and forgettable characters.** Quiet the world's contrast and detail around the subject.
- **Drift between shots.** Match every shot to the style frame and the fixed description, not to the shot before.
- **Too many colours doing nothing.** Cut back to one film colour, one accent and one surprise, and give each a job.
- **A look chosen for itself.** A texture, effect or 3D flourish without a story job is noise.
- **The video-game look.** Even light, perfect surfaces, nothing out of focus. Add imperfection, believable light and falling-off focus.

## Examples.

- The Line's Freeview Play film (`../research/the-line-freeview-play.md`): a colour script that argues the story, and a miniature-set look made in 3D.
- The Monk and the Fish (`../research/the-monk-and-the-fish-dudok-de-wit.md`): texture in the still layer, simplicity in the moving one.
- BBC Two's curve idents (`../research/bbc-two-curve-idents.md`): one fixed shape, endless materials.
- Apple TV's glass intro (`../research/apple-tv-glass-intro.md`): 3D where light does all the work.
- The Stranger Things title (`../research/stranger-things-main-title.md`): one colour, red glow on black, with uneven edges from light shone through real film.
