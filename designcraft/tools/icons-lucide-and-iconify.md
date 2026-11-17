# Icons: Lucide and Iconify

Lucide is Designcraft's icon set: about two thousand free line icons drawn to one set of rules. Iconify is the door to every other free set, some 280 of them, for when Lucide lacks a shape or a job needs a different voice. Read this before putting icons on any screen. Pictures and illustration are borrowed from Motioncraft; the pointer is at the end.

## What the test showed

On November 17, 2026, Lucide and three sets from Iconify went into a scratch page, rendered in the browser pane at desk width.

- **Lucide's default line reads heavy beside ordinary text.** At its standard 2-pixel stroke and 24-pixel size the icons sat darker than body type. At a stroke of 1.5 they matched the text's weight; at 1 they looked faint.
- **Scaling an icon scales its line.** A 48-pixel calendar at the default stroke had a line twice as thick as the 24-pixel one and read clumsy. Holding the line at 2 pixels on screen kept all three sizes looking like one family.
- **Dropped into a line of text with no adjustment,** a 24-pixel icon sat on the text's baseline and rode about 5 pixels high. Sized to the text (1em) and nudged down by an eighth of that, or centred in a flex row, it lined up within a third of a pixel.
- **Mixing sets showed at once.** Lucide's house, search and calendar beside Phosphor's: Phosphor's line is lighter. Tabler's matched Lucide closely. Font Awesome's solid set is filled shapes and looked like a different product.
- **Licences vary per set, as promised.** Iconify's own list gave each set's licence, from free-for-anything to non-commercial only.

## What it's best at

- **Lucide: one consistent line voice.** Every icon is drawn on a 24-pixel square with 2-pixel round-ended strokes, 1 pixel of padding, and at least 2 pixels between parts, so any two icons sit well together. It is shadcn/ui's icon set in the look the test used, so a React build gets it for free.
- **Iconify: the rest of the world, one way in.** Each set comes as its own small package with the same format, so taking one shape from Phosphor or a logo from Simple Icons is the same move.

Where another set beats Lucide:

- **Phosphor** comes in six weights, from thin to filled, so one family can be light in a quiet page and bold in a loud one. Two of the design skills prefer it.
- **Material Symbols,** Google's own set, suits a screen that should feel like Android.
- **Brand logos** come from Simple Icons, through Iconify; Lucide has almost none.
- **The InspoAI connection** can also return icons from several sets, but its free plan's 5 calls a month were used up during testing.

## Setup

- **React:** `npm install lucide-react`, then use each icon as a part: `<Calendar size={20} strokeWidth={1.5} />`. shadcn/ui installs it already.
- **Plain web code:** `npm install lucide-static` gives one SVG file per icon to paste or load. The `lucide` package can also swap marked-up placeholders for icons in the page.
- **Iconify:** install only the set needed (`npm install @iconify-json/ph` for Phosphor) plus `@iconify/utils` to turn an icon into SVG.
- **The command that proves Lucide works:** `cat node_modules/lucide-static/icons/house.svg` prints a small SVG with a 2-pixel stroke and its licence line.
- **Cost:** free.

## Getting the best out of it

**Match the icon's line to the text beside it.** The stroke should look like the stem of the letters next to it. Light body text wants 1.5; bold labels and buttons can take 2 or a touch more. Set it once for the whole product (Lucide's React package has a provider for size, colour and stroke), not icon by icon.

**Hold the line steady across sizes.** Use the non-scaling stroke option (`nonScalingStroke` in React; the older `absoluteStrokeWidth` is on its way out) so a big icon and a small one share one weight. In plain SVG, divide the stroke by the scale.

**Size to the text, not to a round number.** An icon beside 16-pixel text is usually 16 to 20 pixels; 1em keeps it tied to the text if the size changes. Then align it by eye: a pure box-centre can still look high, because lowercase letters sit low in their box. A pixel's nudge is normal.

**The tap area is not the icon.** An icon button can be 20 pixels drawn and still needs a target about 44 pixels square on a phone.

**One ink, told apart by shape.** Icons take the text colour (`currentColor`) and differ by shape, not by a rainbow of fills. The house pages already work this way: one drafting ink, and an icon earns a colour only when its meaning does.

**An icon with a word beats an icon alone,** unless the shape is truly universal (search, close, play). A row of mystery icons is the commonest icon failure.

An example of the difference, from the test: a "Book the room" button with a 24-pixel microphone at the default stroke. The icon stood taller than the letters and its line looked thinner than the bold label. At 18 pixels with a stroke of 2.25, centred in a flex row, it matched the label and read as part of it.

## Mixing sets

Don't, if it can be helped. If Lucide lacks a shape, look first for a set drawn on the same rules: the same 24-pixel square, round stroke ends, a similar stroke. Tabler is the nearest match found in the test. Then set the borrowed icon's stroke to match and check the two side by side at the size they ship. A filled icon among line icons always shows. So does an icon whose corners are sharp where the rest are round.

## Licences

- **Lucide is free for any use** under a short permissive licence (ISC). About 115 of its icons began in an older set, Feather, under the MIT licence; both notices travel with the package.
- **Iconify's licence covers its code, not the icons.** Its own docs say the licence is per set, and every set lists its own. Of the 280 sets listed on November 17, 2026: 148 MIT, 53 CC BY 4.0, 31 Apache, 13 OFL, 10 public domain, and a tail of share-alike, GPL and two non-commercial sets.
- **What that means in practice.** MIT, ISC, Apache and public domain: use freely. CC BY (Font Awesome's free icons among them): credit the maker on the page or in the credits. Share-alike and GPL: changes and sometimes the whole work must be shared under the same terms; avoid them in client work. Non-commercial: never for a job that sells something.
- **A logo's licence is not permission to use the brand.** Simple Icons gives its drawings away, but the marks still belong to their companies.

## When a custom icon is worth it

Worth drawing when the icon carries the brand (a mark only this product has), when the meaning is specific enough that no library shape says it, or when a whole set must share a quirk the libraries don't have. Not worth it for a single gap in an otherwise stock set: one hand-drawn icon among library icons is easy to spot.

A custom icon follows the same rules as the set it joins. For Lucide that means its 24-pixel square, 2-pixel round strokes, 1 pixel of padding, 2-pixel gaps, rounded corners, and the same visual weight as its circle and square. It goes into the project's icon library, never drawn one-off inside a page. The house rule is the same.

## Pictures and illustration

Borrowed from Motioncraft, not repeated here. For pictures, read Motioncraft's Higgsfield guide (stills from GPT Image through Higgsfield, credits and what may be uploaded). For illustration, read its Affinity guide (the lead draws the vector, Affinity cleans the paths and exports clean SVG).

## Where it goes wrong

- **Icons darker than the text.** The default 2-pixel stroke beside light type. Compare the icon's line with a letter's stem.
- **Big icons with clumsy lines.** Scaled up without holding the stroke.
- **Icons riding high.** Dropped into text with no sizing or centring.
- **Two voices on one screen.** Line and filled, round and sharp, or two stroke weights.
- **Emoji or text symbols standing in for icons.** They render differently on every device and ignore the colour.
- **A credit owed and missing.** A CC BY icon shipped without its line.

## Safety

- **Install the icons into the project.** Iconify also offers a live service that fetches icons from its servers as the page loads; that tells a third party about every visit and breaks offline. Bundle the icons instead.
- **Nothing is spent.** Every set used here is free.
- **Ask Sean** before shipping an icon from a share-alike, GPL or non-commercial set, or a company's logo in anything public.

## More details

- **Tested November 17, 2026,** in `designcraft-jobs/tests/icons/` (outside every repo): `gen.mjs` builds `index.html`; screenshots in `screenshots/`. Alignment measured in the browser pane by comparing the icon's centre with the first letter's box centre at 18-pixel text: −5.3 px with no adjustment, 0 px at 1em with a −0.125em nudge, +0.3 px in a centred flex row.
- **Versions:** `lucide` and `lucide-static` 1.74.0 (ISC), `lucide-react` 1.74.0, `@iconify/utils` 3.1.7 (MIT), `@iconify-json/ph` 1.2.2 (Phosphor, MIT, 9,072 icons), `@iconify-json/tabler` 1.2.46 (MIT, 6,545), `@iconify-json/fa6-solid` 1.2.4 (CC BY 4.0, 1,402). Lucide's package exports 2,397 names, some of them aliases; Iconify lists Lucide at 2,089 icons.
- **Lucide's rules** from its icon design guide (lucide.dev/contribute/icon-design-guide) and its stroke page, read November 17, 2026. The deprecation of `absoluteStrokeWidth` in favour of `nonScalingStroke`, and the provider, are from `lucide-react`'s own type file.
- **Licence counts** from Iconify's public list of sets (api.iconify.design/collections), read November 17, 2026: 280 sets, about 555,000 icons. "Licence is per icon set, not per icon" is from Iconify's icon-set basics page.
- **The skills' icon advice** read from their files: Impeccable bans glyphs and emoji as icons; minimalist-ui bans Lucide as a generic thin-line set and prefers Phosphor's bold or filled weights, or Radix icons; high-end-visual-design bans Lucide's default weight as too thick. So the two pull in opposite directions. The house page (SWCB's page design rules) uses one drafting ink and a single icon library.
- **Phosphor's six weights** (thin, light, regular, bold, fill, duotone) counted from its Iconify package. The 44-pixel tap target is from Impeccable's guidance on adapting to touch screens.
- **Not tested:** Material Symbols, the `lucide` package's placeholder swap, and InspoAI's icon search (out of calls).
