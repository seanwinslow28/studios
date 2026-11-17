# Motion in an interface

Read this whenever something on a screen or a web page moves because a person did something: a tap, a hover, a drag, a scroll, a panel opening. It covers what interface motion is for, how fast it should be, how scroll can tell a story, and how it goes wrong. Finished films and rendered moving pictures belong to Motioncraft, and the line between the two studios comes first.

## Where Designcraft stops and Motioncraft starts

Designcraft designs motion that answers a person live: a button that gives under a finger, a panel that grows out of the thing that opened it, a page whose story moves with the reader's scroll. Motioncraft makes anything that plays the same way every time: a launch film, a rendered loop, a logo sting, a character animation, a 3D model built in Blender. When a page needs one of those, Motioncraft makes it, and Designcraft places it and decides what sets it off and how scroll drives it.

The fundamentals are shared. Motioncraft's brief on timing, spacing and weight holds here too: duration and easing are separate decisions, a curve is named by the pose it slows into, and overshoot belongs only where it means something. What changes in an interface is who is in charge. The person causes the motion, often waits on it, and may see it a hundred times a day.

## What motion is for

Interface motion has five jobs. A move that does none of them should go.

- **Showing where something came from and where it went.** Family's wallet panel changes shape instead of swapping screens, so the person never loses their place. A menu should grow out of the button that opened it, and a message that slides in from the bottom should leave the same way. A dialog in the middle of the screen is the exception: it belongs to no one button, so it grows from the centre.
- **Confirming an action.** The interface shows it heard the press, the moment the finger lands, not when it lifts. Duolingo's main button drops four pixels and loses its dark edge, so it looks pushed in.
- **Keeping place through a change.** When a list reorders or a layout reflows, motion shows what moved where. Things that simply appear or vanish feel broken.
- **Guiding attention.** The eye goes to whatever moves. That is why only one thing should move at a time when it matters.
- **Personality.** Things 3 animates almost everything; Duolingo's characters react to right and wrong answers. This is the job that has to justify itself hardest, because it is the one that turns into decoration.

## How often decides whether it moves at all

The first question is not how a thing should move but how often a person will see it.

- **Hundreds of times a day,** like a keyboard shortcut or a command menu: no animation. Anything triggered from the keyboard should respond instantly.
- **Tens of times a day,** like hover effects or moving through a list: barely any, and very fast.
- **Now and then,** like a dialog, a drawer or a message: ordinary motion.
- **Rarely,** like a first run or a finished task: room for delight. Family saves its confetti for the day you back up your wallet.

A lovely half-second move on something used all day becomes a tax by the afternoon.

## Speed and easing by job

Rough durations that hold across good products:

- Press feedback: about a tenth of a second, up to about 160 milliseconds.
- Tooltips and small pop-ups: about 125 to 200 milliseconds.
- A routine change of state: 150 to 300 milliseconds.
- Panels, sheets and moves between views: 300 to 500 milliseconds.
- One authored entrance the page has earned: up to about 800 milliseconds.

The shelf agrees. Linear runs two speeds, 100 and 250 milliseconds, and a hover highlight that appears at once and fades over 150. The panel the Family team built for websites slides in over 300 milliseconds and leaves in 130. Above about 300 milliseconds, routine motion starts to feel like waiting.

Easing, said Motioncraft's way, by the end that slows:

- **Arrivals** should be fast out of the start and slow into the rest. The person sees movement the instant they act, and the thing settles softly.
- **Anything the person asked for must never start slowly.** A move that creeps off the mark reads as lag, even at the same total length.
- **A move across the screen** slows at both ends, strongly.
- **Steady processes,** like a progress bar, run at an even speed.

The curves built into browsers are too weak to feel intentional. Pick one or two stronger curves and use them everywhere. Lando Norris's site puts 118 elements on one curve; Scout Motors puts 159 on one. That repetition is a large part of why each feels like one designed thing.

**Leave faster than you arrive.** Slow where the person is deciding, fast where the system is answering. A hold-to-delete button fills slowly while held, then snaps back in a fifth of a second when let go.

**Never grow from nothing.** Start an entrance from about 95% of full size with a fade, not from a dot. **Stagger a list** by a few hundredths of a second per item, and never block clicks while the stagger plays. **Bounce only after a throw:** overshoot feels right on a card the person flicked and wrong on a menu that simply opened.

## Motion that can be interrupted

People change their minds mid-motion. A master makes every move something a person can grab and reverse from wherever it is right now, not from where it was heading. A drawer that is closing should follow the finger the moment it is touched again, instead of finishing its close and reopening.

- **Never lock out input during a transition.** That same Family panel ignores taps for 360 milliseconds while it changes: a deliberate, short trade against accidental double taps, not a habit to copy.
- **Carry the finger's speed into the motion.** When a drag ends, the motion should continue at the speed the finger was moving, with no visible seam. A quick flick should be enough to dismiss something, however short the distance.
- **Resist softly at edges.** Past a boundary, the thing follows less and less, like a rubber band, instead of hitting an invisible wall.
- **Springs suit anything a person touches,** because they start from the current position and speed. Most should settle with no bounce.

## Scroll as a way to tell the story

Sean: "I'm a sucker for scroll effects and reveals. Scrolling is a great way to tell the story." Scroll is the one input where the reader sets the pace of a story with their own hand. It is the web's version of the presenter's click, and the same craft governs it.

- **Scrub the story, play the small things.** Scrubbed motion is tied to scroll position: stop and it stops, scroll back and it runs backwards. That is what makes scroll a storyteller. Small arrivals, like a card fading in, play once as they enter.
- **Set up before the reveal.** Ciechanowski's mechanical watch article runs on three beats, 93 times: the text says what to try, the reader moves the model, the next lines name what just happened. The reader's hand is the click, and the naming comes after.
- **One job per stretch of scroll, and a still frame around it.** On Raphael Segerman's site the scroll does one thing on each page and the layout around it holds still. Restraint in the first layer is what makes the second land.
- **Spend the show in one or two places.** Lando's site puts its spectacle in the 3D head and the helmet wall and lays the rest out like a tidy magazine. One rehearsed focal sequence beats a fade-and-rise on every section, which is the clearest sign of preset motion.
- **Keep the ask still.** Scout Motors' film plays under the reader's scroll, while one orange Reserve button never moves.
- **Leave the scroll in the reader's hands.** Smoothing it is fine. Taking over its speed is not. On a phone, leave touch scrolling to the phone, and never ask one finger to scroll and steer at once: Lando's 3D head has a "tap to lock" button for exactly that.
- **Content is visible by default.** If the script fails, nothing should stay hidden waiting for a reveal that never comes.
- **Mind the weight.** Scout Motors' scrubbed film fetches 51.7 megabytes over one full scroll.

How to build all this, with the libraries for 3D, scroll motion and smooth scrolling, is in the spectacle tool guide.

## Reduced motion

Some people set their device to ask for less motion, because movement makes them dizzy or sick. A master designs two versions of every moving scene, not one version with the motion switched off.

- **The calm version keeps the meaning.** Nothing travels across the screen. Things fade in once, in order, so the story's sequence survives. A change of state still shows, and a button press is still confirmed.
- **Remove what triggers sickness first:** large moving backgrounds, parallax (layers moving at different speeds), slow repeating swells, and sudden jumps in brightness.
- **Stop loops when they are off screen.** Segerman's calm version, as its code reads, drops its 3D layer but still loops every clip, which is the caution.
- Linear is the model: its code checks the setting 41 times.

## How it goes wrong

- **Motion on the thing used all day.** Fix: count how often it is seen, and remove the animation if the answer is hundreds.
- **A slow start on a response.** The interface feels laggy at any length. Fix: fast out of the start, slow into the rest.
- **Every section fades and rises on scroll.** Fix: one focal moment, and plain arrivals elsewhere.
- **Bounce on everything.** Fix: overshoot only after a flick or a throw.
- **Growing from the wrong place,** or from nothing. Fix: grow from the trigger, from about 95% size.
- **Hover motion on touch screens,** where a tap fires the hover by mistake. Fix: hover effects only for a real pointer.
- **Reduced motion forgotten,** or treated as all off. Fix: a calm version that keeps every state.
- **A scroll story that tails off.** Fix: decide the payoff before the reveals.

## What a strong designer would notice

- A command menu or keyboard action that animates.
- A move that starts slowly when the person asked for it.
- Every section on the page arriving with the same fade and rise.
- A pop-up that grows from its centre instead of its button.
- An exit as slow as the entrance.
- A drawer that has to finish closing before it can be reopened.
- A scrubbed scene whose layout keeps moving around it.
- A reduced-motion version that loses a state change, or still loops video.
- Text that stays invisible when the script is slow.

## More details

- **Where the line sits** follows `designcraft/tools/choices.md` (the Spectacle row and its runners-up) and `designcraft/tools/spectacle-threejs-gsap-lenis.md`, which is the tool guide named above. Motioncraft's fundamentals: `motioncraft/expertise/timing-spacing-and-weight.md`, read for this brief so nothing here contradicts it.
- **Shelf figures** come from the entries in `designcraft/research/`: `family-wallet.md` (the panel's 300 and 130 millisecond timings, the 360 millisecond tap lock, the confetti), `linear-app.md` (two speeds, the 41 reduced-motion checks), `duolingo-app.md` (the four-pixel press), `things-3.md` (the animation toolkit), `lando-norris.md` (one curve on 118 elements, the tap-to-lock head), `scout-motors.md` (one curve on 159 elements, the still Reserve button, 51.7 megabytes), `segerman-portfolio.md` (one job per scroll, the thin calm version) and `ciechanowski-mechanical-watch.md` (93 models, the three beats).
- **Durations, easing habits, frequency, interruption and reduced motion** are salvaged, in this studio's words, from three skills on the Mac: Emil Kowalski's design-engineering skill (the frequency ladder, durations, the 95% start, stagger, asymmetric timing, hold-to-delete), the Apple design skill (interruption, carrying velocity, rubber-banding, springs with no bounce by default, reduced-motion triggers) and the Impeccable skill's animate guidance (the five jobs, the 800 millisecond ceiling for one authored entrance, one focal sequence over repeated reveals, content visible by default).
- Those skills use the bare words "ease-out" and "ease-in". This brief follows Motioncraft and names each curve by the end that slows, because the bare words mean opposite things in different programs.
- Sean's words on scroll are from the shelf's README, November 17, 2026.
- Nothing here was tested today. The durations are rules of thumb from the skills and the measured shelf, not figures checked on a device.
