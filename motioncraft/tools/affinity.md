# Affinity.

Affinity is Canva's design app: vector drawing, photo editing and page layout in one program, free to use. In Motioncraft the lead draws the vector illustration, and Affinity is where it gets cleaned up so it animates well in HyperFrames, Rive, Lottie Creator or Blender. Read this before any vector artwork leaves the drawing stage.

## What it's best at.

- **Cleaning vector paths.** Removing stray and duplicate nodes, closing open shapes, joining broken curves, evening out stroke widths and smoothing curvature, with a Pen and Node tool that can show where a curve's bend changes abruptly.
- **Preparing artwork for motion.** Splitting a drawing into the parts that will move, grouping and naming them, placing each part's pivot, and keeping one artboard per pose or state.
- **Turning a picture into vectors.** A pixel-to-vector conversion, added in March 2026, traces a raster image into editable shapes. It is a starting point, not a finish: traced shapes need heavy node reduction.
- **Moving between vector and pixel work in one file**, such as a painted texture clipped inside a vector shape.

Where another tool wins: drawing from scratch by code (the lead writes SVG directly, or GPT Image 2.6 through Higgsfield returns clean, grouped vector output); animating anything (HyperFrames, Rive, Lottie Creator, Blender); painting by hand (Krita).

## Setup.

- **Installed:** Affinity 3.3.3 at `/Applications/Affinity.app` (checked November 8, 2026). Proof it is there: `defaults read /Applications/Affinity.app/Contents/Info CFBundleShortVersionString`.
- **What it is now** (checked on the web, November 8, 2026). Canva owns Affinity, and in late 2025 it folded the three old programs into one app with Vector, Pixel and Layout studios and made it free. Version 3.1 (March 2026) brought pixel-to-vector conversion; 3.3 (September 2026) added a Blend tool, curvature display on the Pen and Node tool, and a Scripting Studio that runs JavaScript inside the app to automate repetitive work.
- **Cost.** The app is free, but downloading it needs a free Canva account. Canva's AI tools inside it need a paid Canva plan (Pro was listed at $144 a year in September 2026). Motioncraft needs none of the AI tools.
- **How the lead works it.** Affinity has no command line that was confirmed on November 8, 2026. The ways in are Sean's hands, screen control of the app (which needs Sean's grant), or a script in the Scripting Studio run from inside the app. Whether a script can be started from outside the app could not be confirmed.

## Getting the best out of it.

**Clean for the motion, not for the print.** A path that animates well has few nodes, each placed where the shape actually turns. Fewer nodes mean smoother morphs in Rive and Lottie, smaller files and cleaner bones. A good test: if a shape's outline wobbles when you drag one node, it has too many.

**One shape, one job.** Merge overlapping duplicates, remove hidden shapes beneath others, and expand a stroke into a filled shape whenever its width must scale with the object or the target ignores stroke settings. Keep strokes live only where a tool will animate them (a line drawing on, for instance).

**Build the hierarchy the animator needs.** Group by moving part, from the root out: body, then head, then face parts inside the head. Name every layer plainly (`head`, `eye-left`, `mouth`), since names travel into the SVG as ids and become what code and Rive's hierarchy refer to. Set each part so it rotates about the right point: a head turns at the neck, an arm at the shoulder.

**Use pixels and RGB.** Set the document in pixels at the frame's size (1920 by 1080 for a film, the component's real size for an app), in RGB with an sRGB profile, so coordinates and colours come out as the targets expect.

**SVG export settings that matter.** These are the export dialog's options (labels may differ slightly in version 3.3; check the dialog):

- **Rasterise: Nothing.** Otherwise anything Affinity thinks SVG can't hold, such as a live effect, is silently turned into a picture embedded in the file.
- **Flatten transforms: on.** Bakes rotations and scales into the path points, so every tool reads the same shapes. Rive does not support skew at all.
- **Export text as curves: on,** unless the text will be set live by the target (HyperFrames type should usually be real HTML text with a shipped font instead).
- **Use hex colours: on,** for plain colour values every importer reads.
- **Set viewBox: on** for screen work, so the drawing scales cleanly. The common warning against it is about physical sizes for cutting machines, which don't matter here.

**What each target needs.**

- **HyperFrames.** The SVG goes inline in the page, so ids must be unique across the whole page and every moving part must be its own group. Prefix ids per composition. Leave out filters you want animated; build them in CSS instead.
- **Rive.** Rive turns SVG into native, editable shapes (checked against Rive's SVG guide, November 8, 2026). It keeps linear and radial gradients (but ignores gradient transforms), dashed strokes, and masks (as clipping). It ignores embedded images, does not support filters or skew, and turns inherited fills and strokes white. So: flatten transforms, set fills and strokes directly on each shape, convert effects to plain paths, and bring raster parts in separately.
- **Lottie Creator.** Imports SVG directly, and LottieFiles advise importing your own SVG rather than letting the AI draw shapes from scratch. The same clean-up rules apply; effects and embedded images are the usual casualties.
- **Blender.** Its SVG importer makes curves (or Grease Pencil strokes) from paths with flat fill colours. Expect gradients, effects and stroke styling to drop out, so expand strokes and keep one flat colour per shape. This was not tested on this Mac; check one import before relying on it.

## Where it goes wrong.

- **A picture hidden in the SVG.** Rasterising left on, a blur or shadow, or a placed image, and the file carries a bitmap that Rive ignores and HyperFrames scales badly. Open the SVG in a text editor and search for `<image`.
- **Transforms that land differently in each tool.** Unflattened rotation and skew read one way in a browser and another in Rive. Flatten.
- **Missing fonts.** Text left live arrives in a substitute wherever the font isn't installed. Curves, or real text in the target with the font file shipped.
- **Traced artwork that won't animate.** Pixel-to-vector output can carry thousands of nodes. Simplify hard, or redraw the key shapes.
- **Duplicate or meaningless ids.** Affinity writes layer names as ids and adds its own attributes; two layers both called `Layer 1` collide on a web page. Name before exporting.
- **Colour shifts.** A CMYK or wide-gamut document exports colours that don't match the brand values. Keep RGB, sRGB.

## Safety.

- **Canva account.** Signing in links the app to a Canva account; the core tools work on the Mac.
- **AI tools upload.** Canva's AI tools send the picture to Canva's servers. Never use them on Sean's private material or anyone else's artwork without asking, and they cost money besides.
- **Scripts.** Run only scripts written for the job. The Scripting Studio's AI script writing would also go online.
- **Ask Sean** before buying a Canva plan or granting screen control of the app.
