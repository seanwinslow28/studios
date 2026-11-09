# Camera and depth.

Read this when a job plans its shots and camera moves, builds a layered or miniature-set world, or has to join several AI video clips into one move.

## What good looks like.

**Every move has a reason the viewer can feel.** A push in says "pay attention, something is dawning". A pull back reveals: where we are, how small the hero is, how big the idea has become. A low angle makes something loom; The Line's red TVs tower over the camera, so they feel like bullies before they do anything. A locked-off shot says "watch what happens", and The Monk and the Fish barely moves its camera at all: strong drawn perspective and wide frames do the work a move would. A move with no story reason should be a held frame.

**The camera has weight.** A real camera on a real rig has mass. It eases out of rest, travels, and eases into rest; it doesn't start or stop at full speed, and it doesn't drift at a constant rate unless drift is the point. The Apple TV intro shows the craft at its finest: a fast pull back for a second and a half, then movement drops about tenfold in a quarter of a second and keeps halving until the picture settles completely. The settle is the payoff.

**Depth is built from layers.** Even a flat 2D world can feel deep: split it into planes (foreground, subject, middle ground, far background) and let a moving camera do the rest. Near planes slide across the frame faster than far ones; that difference, called parallax, is what the eye reads as depth. In a simple test, trucking the camera sideways moved the near layer about 9 percent of the frame's width, the middle layer under 6 and the far layer under 4: depth from distance alone, with nothing animated by hand.

**Atmosphere separates the planes.** Far things are lighter, cooler, lower in contrast and softer. Near things are darker, richer and sharper, or deliberately out of focus. Value and focus do more for depth than geometry does.

**One continuous space.** Across cuts, the viewer must always know where they are and which way things are going. Screen direction holds (a character travelling left keeps travelling left), the light comes from the same side, eyelines match, and the lens and camera height stay consistent unless a change means something. Ordinary Folk's 2019 Webflow film goes further: almost no cuts at all, with the camera flying on while each shape turns into the next scene, and one small glowing ball guiding the eye the whole way.

## The miniature-set look.

The Line's Freeview Play film is the target: a model British town built inside the computer, photographed like a real miniature. What makes it convincing:

- **Shallow depth of field.** Only a thin slice of the world is sharp, and the background melts into soft blur. Real miniatures are shot close with real lenses, so focus falls off fast. That falloff is the strongest single signal that a world is small.
- **The camera at the figures' scale.** The lens sits low, near the characters' eye level, the way a small camera on a tabletop set would. Shooting from a human height above the set reads as a model being looked down on, not a world being lived in.
- **Scale cues in the materials.** Surfaces that would be smooth at full size show texture at model size: the weave of felt, the grain of card and painted wood, small dents and joins. Slight irregularity, edges not quite straight and paint not quite even, says "made by hands".
- **Lighting like a practical set.** A few believable sources, soft shadows, warm pools of light and dark corners. Even, sourceless light is the quickest way to the video-game look.
- **Motion with a trace of stop motion.** Characters moving on twos (a new pose every second frame) and small imperfections from frame to frame. The camera, by contrast, moves smoothly, the way a motion-control rig does on a real stop-motion stage.

The miniature look forgives less than a loose painted one, because the eye judges it against real objects. A painted look can wobble and still feel intended; a model world that wobbles looks broken.

## Grey-box blocking.

Grey-box blocking means roughing out the set in plain 3D boxes, placing stand-ins for the characters, and recording the camera move there first. The boxes carry no look at all; they fix only space, scale, timing and the path of the camera. A video model is then given that grey-box clip and copies its camera move, while the look comes from the style frame and the fixed style description. The video model copies the camera, never the look.

Why it works: AI video invents camera moves freely and inconsistently. Locking the move in a cheap 3D sketch turns the camera from a guess into a decision, and lets a move be judged and changed before any expensive take. It also makes continuity possible, because every shot in a scene is blocked in the same boxes with the same lens. Higgsfield's own 3D scene builder may stand in for a separate grey-box stage; that needs a test (method: `../tools/higgsfield.md`).

## Long moves stitched from several clips.

AI video clips are short, but a story often wants one long, unbroken move. The craft is hiding the joins.

- **Wipe behind something passing the camera.** A pole, a passer-by, a branch or a door crosses the lens, filling the frame for a few frames, and the next clip starts behind it. This is the method from the Higgsfield workflow and the oldest trick in long-take filmmaking.
- **Continue the motion across the seam.** The camera's speed, direction and lens must match exactly on either side. A seam where the camera slows, speeds up or changes height is a seam the viewer feels, even when they can't see it.
- **Carry one element across the seam.** BUCK's GitHub film tosses a real duck into the air, it becomes animated, and the camera dives with it into a new world without a cut. The eye follows the duck and never notices the change of world.
- **Hand over frame to frame.** Starting a clip from the previous clip's last frame keeps place and light continuous, but models still drift in colour, scale or detail at the join.

## How it goes wrong, and the fix.

- **Moves for their own sake.** Constant swooping makes everything feel equally important. Save movement for beats that earn it.
- **A camera with no weight.** Hard starts and stops, or floaty constant speed. Give every move an ease out of rest and a settle into rest, and let the settle take longer than you think.
- **Flat parallax.** Every layer moves at the same speed, so the world reads as one sliding card. Place layers at real depths and move the camera, not the layers.
- **Edges in frame.** A camera move reveals where a painted layer ends. Paint every layer wider than the frame (about a fifth extra is a sensible start) and check the extremes of every move.
- **Texture that doesn't travel.** Painted grain stays fixed to the screen while the camera moves. Texture must ride on its layer; the design and look brief covers this.
- **The miniature that reads as a game.** Everything sharp, light everywhere, the camera at human height. Narrow the focus, lower the lens, add texture and give the light a source.
- **Broken continuity.** A character flips screen direction, or the light jumps sides between shots. Block a whole scene in one grey-box set and keep one lens and camera height per scene unless a change means something.
- **Visible seams in a stitched move.** Plan the seam in the grey box, match the motion exactly, and hide it behind something passing the lens.
- **Colour shifts in flat painted layers.** A renderer that treats painted planes as a lit scene can tone-map their colours away from what was painted. Render painted layers unlit, with a view setting that keeps painted colour as painted.

## Examples.

- The Line's Freeview Play film (`../research/the-line-freeview-play.md`): low angles under looming TVs, blurred backgrounds like photographs of a model, and a single 10-second held shot under the railway bridge after a fast chase.
- Apple TV's glass intro (`../research/apple-tv-glass-intro.md`): one unbroken pull back and a settle that drifts to rest instead of stopping dead.
- Ordinary Folk's Webflow films (`../research/ordinary-folk-webflow-no-code.md`): a continuous camera flying through scenes that morph into each other, standing in for cuts.
- BUCK's GitHub explainer (`../research/buck-what-is-github.md`): a hand-off from live action to animation carried by one object, then long flying takes of 12 to 27 seconds.
- The Monk and the Fish (`../research/the-monk-and-the-fish-dudok-de-wit.md`): almost no camera movement; drawn perspective and wide, held frames do the work.
