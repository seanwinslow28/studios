# Character and acting.

Read this when a job has a character in it: designing one, posing it, writing what it does in a shot, or keeping it the same from shot to shot.

## What good looks like.

### A character that reads as a shape.

Fill the character in solid black. A good design still says who it is. The Freeview Play cast shows this at its best: a boxy TV with a screen for a face, a girl in a yellow coat, a small dog, a stooped old man. Each is a different shape at a glance, even small in a wide shot, and the yellow coat lets the girl be found in any frame.

A cast also reads by contrast. In *Hair Love* the dad is big, soft and slow, and his daughter is small and springy. In *Oktapodi* the octopuses are soft blobs and the driver is tall and bony. Size, mass, and straight lines against curves say who is who before anyone moves.

Design for the parts that will act: whatever carries the feeling (eyes, brows, hands, a tail, a screen) must be visible from the main angles and clear of the body. A simple design acts better than a detailed one, because there is less to keep consistent and every mark that remains carries more.

### A simple face that still acts.

The blue TV's whole face is two curved lines on a screen, and it reads as shy, then hopeful. That works for three reasons. The fewer the marks, the more each one means, and the viewer fills in the rest. The feeling comes from the tilt of a line and where the eyes point, not from modelling. And the body does half the acting: the TV peeks out, pulls back, leans forward.

Two working habits make a simple face act:

- **Change the expression on a hold, not in the middle of a big move.** Let the face settle into a new shape while the body is still, then move; or move, then let the face change. An expression needs about half a second (12 frames at 24 a second) to register, and longer for a strong one.
- **Use the blink as a sign of thought.** A blink placed on purpose tells the audience the character has just noticed or decided something. It also gives the edit a natural place to cut, since a cut lands best just before a new thought begins.

### A pose with force in it.

Every good pose has a line of action: one imaginary curve running through the whole body that carries its force. Bend it into a clear C or S. A straight, upright spine reads as a mannequin.

Start from a single verb. The pose is "peeks", "recoils" or "hopes", not "standing". Say it first through how the chest sits against the hips, because that relationship holds most of the action; head and limbs hang from it, and hands, feet and detail come last. Find the leading edge, the part that goes first in the move, and give it the strongest curve. Check balance against an imagined vertical through the support: mass on both sides, or a reason, such as a fall, why not. Angles near 45 degrees feel dynamic; flat horizontals and verticals feel static.

Gesture comes before detail. Get the loose, whole-body idea right first, with every line serving it, and add construction afterwards without losing the curve. The first version of a pose is nearly always too mild. Push it bigger and clearer, then pull back only if it breaks the character.

Two keys with the same silhouette are one key. If the feeling changes, the shape must change too.

### Acting written as beats by the second.

Before anything is animated or generated, write the performance as beats with times, each beat one change of thought or action. For the TV under the bridge, it might read: 0.0 to 1.2 seconds, hidden behind the boxes, only an edge of screen showing; 1.2 to 1.8, peeks out; 1.8 to 2.6, sees the girl and freezes; 2.6 to 3.4, its brows lift and it leans toward her. Writing it this way forces a decision about what the character thinks at every moment. It also gives a video model or an animator something precise to follow.

Characters think, then move. They see something, register it on a short hold, decide, and only then act. The eyes lead, then the head, then the body. Anticipation, the small opposite move before an action, is the visible part of deciding. A character who reacts on the same frame as the thing it reacts to looks like a puppet.

A performance is built from contrast. *Hair Love* cuts the hair fight every 1.8 seconds, then holds one 17-second shot of the beaten dad sliding down a door, and the stillness is where the feeling lands.

How a character stands, fidgets and waits is most of its personality. In a film with no words, as both *Hair Love* and the Freeview film are, every pose has to explain itself.

### The same character in every shot.

A character drifts unless something holds it in place. Hand-drawn studios use model sheets; for AI image and video work the method is stricter, and `motioncraft/tools/higgsfield.md` has the full image-and-video method:

- **Turnaround sheets** of each character from the front, side and back, designed silhouette first.
- **A new sheet whenever a prop or a pairing changes.** The girl holding the dog is a different picture to a model than the girl alone. Tricky props get their own stills before any video.
- **One fixed style description,** pasted word for word into every image and video prompt.
- **Each key frame built from two references,** a layout image for framing and the style reference for the look.

Write down the few things that must never change, such as proportions, the coat's colour, the number of features, the screen's blue, and compare each new shot side by side with the sheet.

For layered vector people built in code, keep the rig simple and expressive: hair behind, body, and a head group holding brows, each eye, nose and mouth, with a pivot under the chin. A blink squashes each eye nearly flat for about four frames, a glance shifts the eyes sideways, and a nod or tilt turns head and hair together about the pivot. *Hair Love* used a rig for most of its animation and adjusted the rest by hand for appeal: the rig gives consistency, the hand gives charm.

## How it goes wrong, and the fix.

- **The silhouette is muddy.** Arms sit in front of the body, a prop disappears into the torso. Fix it by changing the camera angle or moving the limbs clear of the body, not by adding detail.
- **The cast are twins.** Everyone shares one size and build. Contrast mass, proportion and the kind of line, straight or curved.
- **Poses are stiff.** The spine is straight, the limbs have parallel sides like rubber hoses. Name the verb, bend the line of action and offset the curves.
- **Everything is symmetrical.** Both arms rise together, a group moves in unison. Offset one side by a few frames and break the mirror, unless perfect unison is the joke.
- **The character moves without thinking.** It reacts instantly, or every part moves at once. Add a short hold to register, and lead with the eyes.
- **The performance is mush.** Constant, even motion with no holds. Hold the key poses long enough to read, and mix fast moves with slow ones.
- **The character drifts across shots.** The coat changes shade, the TV gains a button, the face changes shape. This is the most common failure in AI work. Make a sheet for each new state, keep the style text fixed, and drop a drifting take rather than patching it later.
- **The character is generic.** Find one specific trait, such as the old man's slump, and push it.
- **The level of detail is mixed.** Realistic hands on a simple body pull the eye. Keep every part at the same level of simplicity.

## Examples.

- **The Freeview Play film, 1:38 to 1:46.** The blue TV peeks out from behind boxes; two lines on a screen read clearly as shy, then hopeful. The whole body acts with the face.
- ***Hair Love*, 2:00 to 3:06, then the long hold after it.** The dad winds up before each comb stroke, the hair fight cuts fast, and his reactions get a beat to read. Clean, near-flat shapes are no barrier to feeling.
- ***The Monk and the Fish*.** The monk is barely more than a robe and a head, yet he crouches before every lunge, hangs at the top of a leap and flops when he misses. Gesture does it all.
- ***Oktapodi*.** Two soft characters against one bony one: casting by contrast in shape makes every gag clearer.
