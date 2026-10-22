# Tools

Pipeline software Devcraft built for Motioncraft's seats, under [the Devcraft binding](../templates/handoff-binding-devcraft.md). A seat runs a tool here only once its line in [`bench/toolbelts.toml`](../bench/toolbelts.toml) names it under `tools`, with Sean's yes; the launcher then names the tool's path in each drafting pass's prompt and fixes the file by hash. Each tool is standard-library Python, so it runs inside an application's own Python through the [application doorway](../launcher/README.md#the-application-doorway) with nothing installed.

| Tool | For | What it does |
|---|---|---|
| [`kerning.py`](kerning.py) | the Animator, in Blender | Reads a font's own pair kerning for the exact words and writes it into a Blender text object's per-character spacing (SWCB #255) |

## The kerning helper

Blender 5.2.2 applies none of a font's pair kerning (Sean's type ruling, SWCB #244). The helper reads it from the font file (the GPOS `kern` feature, or the legacy `kern` table when GPOS has none, which is HarfBuzz's own choice) and writes each character's `body_format[i].kerning`. Art then fine-tunes by eye in the appearance packet.

In a pass's Blender script, run through `apps.py ask blender --script <file>`:

```python
import sys
sys.path.insert(0, "<studios>/motioncraft/tools")
import kerning
report = kerning.apply(bpy.data.objects["Title"], "<version>/assets/fonts/<file>.otf")
```

`apply` refuses words that are not the object's, a font that is not the one the object is set in (Blender's built-in font included), and characters set bold, italic or in small caps. Its report lists the kerned pairs in font units and anything it could not match. From a shell, `python3 kerning.py <font> "<words>"` prints the same pairs and values without Blender, for the appearance packet.

**How Blender reads the value** (probed 2026-10-21): a character's advance becomes `advance × (1 + kerning / 40)`, and a space's is also multiplied by the word spacing. The value is a share of that character's own width, so it is the same at every text size; tracking adds on top.

**Scope.** Latin, left to right, one font file per text object. No ligatures or other glyph substitution, since Blender draws each character's default glyph. Static fonts, a collection's first font, and a variable font at its default instance. A variable font with an optical-size axis is refused: Blender 5.2.2 sets it at optical size 16 whatever the text's size, not at its default (Source Serif 4's variable widths match `opsz=16` exactly), so the release's static files serve instead. Apple's own layout tables (`morx`, `kerx`, `trak`) are not read; only Apple's fonts carry them, and films use none. WOFF 2 is refused. The Justify and Flush alignments of a text box respace each line afterwards and are named as a limit.

**Tests.** `tests/test_kerning.py` compares the helper's glyph positions with HarfBuzz's (`hb-shape`, with every substitution and every positioning feature but kerning off) on a fixed set of pairs: ten small fonts built in the test, one per table layout the helper reads; the shelf's Source Serif 4 static files; and three Mac fonts, STIX Two Text (variable, weight axis only) and two that kern with the legacy table only. Then it sets AVATAR, To, Ty and LT in Blender, lets the helper write the spacing, and measures each letter against HarfBuzz at two text sizes, within half a font unit, and sees `apply`'s refusals in Blender. `tests/test_kerning_lock.py` runs the helper in an Animator pass under the doorway's real Blender lock, packs the font, saves into a new version folder and reopens it. A font, HarfBuzz or Blender missing on a machine skips its tests.

```bash
cd ~/Code-Brain/studios && uv run --no-project --with pytest python -m pytest motioncraft/tools/tests -q
```

On the laptop, 2026-10-21: 32 passed. On the Mini, which has no `hb-shape` and no font shelf yet: 5 passed and 27 skipped, the lock test among the passes (on STIX Two Text). A sweep beyond the tests matched HarfBuzz exactly on all 120 static Source Serif 4 files (its four variable files are refused) and on 121 of the Mac's own fonts (84 kerning by GPOS, 37 by the legacy table); the 15 that differed all carry Apple's own layout tables.
