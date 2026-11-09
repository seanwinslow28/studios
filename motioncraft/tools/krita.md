# Krita.

Krita is a free painting program with a real brush engine, layers, filters and a frame-by-frame animation timeline. In Motioncraft its job is finishing painted frames by hand: an AI image model makes the painted frame, and a hand in Krita's window turns it into something that holds up in motion. Read this before any painted look reaches a shot.

## What it's best at.

- **Painting over a frame by hand.** Brush presets that behave like gouache, oils or dry media, with pressure, texture and colour mixing on the canvas.
- **Unifying a sequence.** Giving a run of AI frames one brush language, one set of edges and one paper, so they read as one painting moving rather than a slideshow of separate pictures.
- **Texture plates.** Paper grain, pigment blooms and edge breakup painted once as their own layers, so the animation tool can carry them with the moving shape.
- **Short frame-by-frame passes.** Its timeline and onion skin (faint views of the neighbouring frames) suit a few drawn frames, such as a smear pose or a splash.

Where another tool wins: line animation with a moving camera and many drawings (Blender's Grease Pencil); clean vector shapes (Affinity); anything that moves by keyframes rather than redrawing (Blender or HyperFrames).

**No painting by script.** Sean's first painted film drew its strokes with code, and the result read as childlike: even, mechanical marks with none of the pressure and intent of a hand. So the lead does every part of the finish that isn't a brush stroke: colour, texture plates, layer blending, and unifying a run of frames into one look. Scripts may prepare and export Krita files. When a hero frame truly needs real strokes, the lead asks Sean whether he'll paint them, and never assumes he will. Steering Krita's brush by screen control would likely look as mechanical as code did, so it isn't a way around this.

## Setup.

- **Installed:** Krita 5.3.4 at `/Applications/krita.app` (checked November 8, 2026). Free and open source.
- **Which line to use.** Krita 5.3 and 6.0 were released together in March 2026 and are almost the same program; 5.3 is built on Qt 5 and is the one the Krita team recommends for production, while 6.0 is the Qt 6 port and more experimental. The newest point releases found on November 8, 2026 were 5.3.4 and 6.0.4. Stay on 5.3 for a film.
- **Proof it is there:** `defaults read /Applications/krita.app/Contents/Info CFBundleShortVersionString` prints 5.3.4. Opening Krita and painting a stroke proves the brush engine.
- **The scriptable part** is `kritarunner`, in `/Applications/krita.app/Contents/MacOS/`, which runs a Python function inside Krita without a window (below).

## Getting the best out of it.

**Know what to fix in an AI frame.** Image models paint convincingly in a still but leave the same tells every time: edges that go soft and mushy where two shapes meet, brush marks that point every which way instead of following the form, texture that is printed flat over everything like a pattern on glass, muddy darks, and small details that melt (fingers, rims, lettering). The finish is mostly these: firm up the edges that carry the silhouette, repaint the marks so they follow the form, rebuild the darks with clean colour, and fix whatever melted.

**One brush language for the whole sequence.** Pick two or three brush presets and one size range for the film, and use only those. Paint at the delivery size or twice it, never smaller, so the marks keep their scale on screen. Sample colours from a single palette for the shot rather than from each frame, or the frames drift in hue when played.

**Keep texture in its own layers.** A painted look in motion has three kinds of texture that change on different rules: the line, which may wobble slightly from drawing to drawing (line boil); the pigment inside painted areas; and the paper underneath. Paint each on its own layer. The moving tool can then carry the paper with the shape it belongs to, instead of leaving it stuck to the screen while the picture slides under it, and can let line boil while the paper stays quiet. Never let line, pigment and paper all change on the same frames: it fizzes and competes with the action.

**Hold the anchors.** Identity marks (a character's eye, a distinctive stroke on a prop) and contact points (where a foot meets the ground) stay painted the same from frame to frame. If they wander, the move loses weight and the character loses identity.

**Judge in motion, at display size.** Texture that looks lovely on a still can flicker at full speed. Play the finished frames at the film's frame rate and size before calling a pass done, and watch any loop wrap from last frame to first for a pop.

**Colour that survives the trip.** Work in an sRGB document and export PNGs tagged sRGB, which matches the Rec. 709 colour of a video master. A wide-gamut or untagged file shifts colour when Blender or Resolve reads it.

**What scripts are good for.** Through `kritarunner`, a script can place an AI frame as the base layer, build the empty layer stack a painter will work in, apply Krita's filters, save `.kra`, `.ora` and `.psd` files, and export each layer as a PNG with transparency for Blender or Resolve. That saves the painter the setup and the export, and leaves every stroke to the hand.

## Running Krita without a window.

- **The call.** `QT_QPA_PLATFORM=offscreen /Applications/krita.app/Contents/MacOS/kritarunner -s <module> -f main` imports a Python module and runs its `main` function. `kritarunner` ignores `PYTHONPATH`, so put the module in `<base>/lib/python/site-packages/` and set `PYTHONUSERBASE=<base>`.
- **Use a small wrapper module.** It turns on batch mode (`Krita.instance().setBatchmode(True)`, so no dialog waits for a person), runs the real script with `runpy.run_path`, catches every error, prints a closing line such as `done 0`, and exits with `os._exit(code)`. This matters because `kritarunner` exits 0 even when the script failed to load: the closing line is the only trustworthy signal.
- **Its own home.** `kritarunner` writes settings, a resource database of about 110 MB and caches under its own name in the home folder, and a module in its resource folder lands on its Python path. Point `HOME` and `CFFIXED_USER_HOME` at a fresh folder for each run so nothing touches Sean's own Krita, and point its swap file there too (`swaplocation=` in that home's `Library/Preferences/kritarunnerrc`). Set `LANG` and `LC_ALL` to `en_US.UTF-8`.
- **Saving.** Krita saves through a hidden temporary copy named `.XXXXXX.<ext>` in the Mac's own temporary folder; if anything blocks that folder, the save waits forever.

## Where it goes wrong.

- **The brush engine crashes without a window.** `Node.paintLine` and the other paint calls read the main window's active view without checking it exists, and every way of opening a view with no screen crashes. Without a window, Krita gives layers, blend modes, opacity, filters and files, never brushes.
- **Export stalls.** `Document.exportImage` hangs with no screen. Take a flattened image from `Document.pixelData` into a `QImage` and save that instead.
- **Layer opacity baked in.** `Node.save` bakes a layer's opacity into the PNG's transparency. Export each layer at full opacity and pass its opacity along separately.
- **Fonts silently swapped.** Krita reads its font folders only at start-up, so a font copied in later is never seen, and text falls back to a substitute with no error. Register each font file with Krita's own Fontconfig before setting text, by calling `FcConfigAppFontAddFile` through `ctypes` on `/Applications/krita.app/Contents/Frameworks/libfontconfig.1.dylib`, then list the families it now holds to confirm. A `.kra` stores a font's name, not the font, so every reopen needs the same registration.
- **Undesigned flicker.** Each AI frame arrives with its own random texture. Played in sequence that is noise, not boil. Unify the paper and the anchors first.
- **Image jitter passed off as boil.** Shaking a whole layer is not boil; boil changes the line's shape.

## Safety.

- **Everything stays on the Mac.** Krita uploads nothing.
- **Sean's own Krita.** His settings and brushes live in his Library folder. Scripted runs use their own home; never write to his.
- **Ask Sean** before buying any paid brush pack or companion painting program.
