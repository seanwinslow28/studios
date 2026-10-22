"""The kerning helper against HarfBuzz: glyph positions for a fixed set of pairs, then Blender's own layout.

HarfBuzz (`hb-shape`) is the reference. It shapes with every substitution and every
positioning feature but kerning switched off, since Blender draws each character's
default glyph and does nothing else. Positions are compared in font units, exactly.

Three kinds of font. Small fonts built here, one per table layout the helper reads
(pair positioning by glyph and by class, a lookup behind an extension, a single
adjustment inside the kern feature, a mark the lookup steps over, and the legacy
`kern` table with a pair listed twice), so every machine runs the same cases. The
shelf's Source Serif 4 release, read from this machine's media folder
(`folders.local`), in its static TrueType and CFF files; its variable files are
refused, since Blender sets them at another optical size. And three of the Mac's
own fonts: STIX Two Text (open licence, variable with a weight axis only) and two
that kern with the legacy table only, read for this test and never copied
anywhere. A font or tool missing on a machine skips its test.

The Blender tests set the words in Blender 5.2.2, let the helper write the spacing,
and measure where each letter lands: the AV and To probe the ticket names, at two
sizes, within half a font unit of HarfBuzz.
"""
from __future__ import annotations

import json
import os
import shutil
import struct
import subprocess
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parents[1]
STUDIOS = TOOLS.parents[1]
sys.path.insert(0, str(TOOLS))
import kerning  # noqa: E402

HB = shutil.which("hb-shape")
BLENDER = os.environ.get("MOTIONCRAFT_BLENDER", "/Applications/Blender.app/Contents/MacOS/Blender")
HAVE_BLENDER = os.access(BLENDER, os.X_OK)
need_hb = pytest.mark.skipif(not HB, reason="HarfBuzz's hb-shape is not installed on this machine")

# Everything HarfBuzz would do that Blender does not: substitutions, and positioning other than kerning.
NOT_KERNING = "-liga,-clig,-dlig,-calt,-rclt,-ccmp,-locl,-rlig,-mark,-mkmk,-curs,-dist,-abvm,-blwm"

# The fixed pairs: the classic display-type pairs, round and straight neighbours, punctuation, and a space.
PAIRS = ["AV", "VA", "To", "Ta", "Ty", "Te", "Wa", "We", "Yo", "LT", "LV", "LY", "P.", "F,", "r.", "y.", "AT",
         "AY", "AW", "Av", "Fo", "Tr", "Vo", "Ya", "Ko", "Xo", "ff", "fi", "fl", "A ", " T", "''"]
TEXT = " ".join(PAIRS)


def harfbuzz(font: Path, text: str, index: int = 0):
    """HarfBuzz's glyph and pen x for each character, in font units."""
    out = subprocess.run([HB, "--output-format=json", "--no-glyph-names", f"--face-index={index}", "--direction=ltr",
                          "--script=Latn", "--language=en", f"--features={NOT_KERNING}", str(font), text],
                         capture_output=True, text=True, check=True).stdout
    pen, got = 0, []
    for g in json.loads(out):
        got.append((g["g"], pen + g["dx"]))
        pen += g["ax"]
    return got


def helper(font: Path, text: str, index: int = 0):
    return [(g["glyph"], g["x"]) for g in kerning.Font(font, index).layout(text)]


# --- fonts built for the test -------------------------------------------------------------

CHARS = "AVToa.,'M"
GID = {c: i + 1 for i, c in enumerate(CHARS)}  # glyph 0 is .notdef
ADV = {"A": 650, "V": 640, "T": 600, "o": 520, "a": 500, ".": 250, ",": 250, "'": 220, "M": 0}


def _cmap() -> bytes:
    codes = sorted((ord(c), g) for c, g in GID.items())
    segs = [(c, c, (g - c) & 0xFFFF) for c, g in codes] + [(0xFFFF, 0xFFFF, 1)]
    n = len(segs)
    sub = struct.pack(">HHHHHHH", 4, 16 + 8 * n, 0, 2 * n, 0, 0, 0)
    sub += b"".join(struct.pack(">H", e) for _, e, _ in segs) + b"\0\0"
    sub += b"".join(struct.pack(">H", s) for s, _, _ in segs)
    sub += b"".join(struct.pack(">H", d) for _, _, d in segs) + b"\0\0" * n
    return struct.pack(">HHHHI", 0, 1, 3, 1, 12) + sub


def build_font(gpos: bytes = b"", kern: bytes = b"", gdef: bytes = b"") -> bytes:
    """A minimal font HarfBuzz will shape: metrics, a character map and the given layout tables."""
    n = len(CHARS) + 1
    adv = [500] + [ADV[c] for c in CHARS]
    tables = {
        "head": struct.pack(">IIIIHHqqhhhhHHhhh", 0x10000, 0x10000, 0, 0x5F0F3CF5, 0, 1000, 0, 0, 0, -200, 1000, 800,
                            0, 3, 2, 0, 0),
        "hhea": struct.pack(">IhhhHhhhhhhhhhhhH", 0x10000, 800, -200, 0, max(adv), 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, n),
        "maxp": struct.pack(">IH", 0x5000, n),
        "hmtx": b"".join(struct.pack(">Hh", a, 0) for a in adv),
        "cmap": _cmap(),
    }
    for tag, data in (("GPOS", gpos), ("kern", kern), ("GDEF", gdef)):
        if data:
            tables[tag] = data
    tags = sorted(tables)
    out = struct.pack(">IHHHH", 0x4F54544F, len(tags), 0, 0, 0)  # 'OTTO': no outlines needed to shape
    off = 12 + 16 * len(tags)
    body = b""
    for t in tags:
        data = tables[t] + b"\0" * (-len(tables[t]) % 4)
        out += struct.pack(">4sIII", t.encode(), 0, off + len(body), len(tables[t]))
        body += data
    return out + body


def coverage(chars) -> bytes:
    gids = sorted(GID[c] for c in chars)
    return struct.pack(">HH", 1, len(gids)) + b"".join(struct.pack(">H", g) for g in gids)


def classdef(classes) -> bytes:
    """Format 2: one range per glyph."""
    items = sorted((GID[c], k) for c, k in classes.items())
    return struct.pack(">HH", 2, len(items)) + b"".join(struct.pack(">HHH", g, g, k) for g, k in items)


def pair_format1(pairs, vf2=0) -> bytes:
    """`pairs`: {(first, second): (x advance of first, (x placement, x advance) of second)}."""
    firsts = sorted({a for a, _ in pairs}, key=GID.get)
    v2 = (lambda p: struct.pack(">hh", *p)) if vf2 == 5 else (lambda p: b"")
    sets = []
    for a in firsts:
        recs = sorted(((GID[b], v) for (x, b), v in pairs.items() if x == a))
        sets.append(struct.pack(">H", len(recs)) + b"".join(struct.pack(">Hh", g, v[0]) + v2(v[1]) for g, v in recs))
    head = 10 + 2 * len(firsts)
    cov = coverage(firsts)
    offs, body = [], b""
    for s in sets:
        offs.append(head + len(cov) + len(body))
        body += s
    return (struct.pack(">HHHHH", 1, head, 4, vf2, len(firsts)) + b"".join(struct.pack(">H", o) for o in offs)
            + cov + body)


def pair_format2(c1, c2, matrix) -> bytes:
    """Class kerning, x advance on the first glyph only: `matrix[class1][class2]`."""
    n1, n2 = len(matrix), len(matrix[0])
    recs = b"".join(struct.pack(">h", v) for row in matrix for v in row)
    head = 16 + len(recs)
    cov, cd1, cd2 = coverage(c1), classdef(c1), classdef(c2)
    return (struct.pack(">HHHHHHHH", 2, head, 4, 0, head + len(cov), head + len(cov) + len(cd1), n1, n2) + recs
            + cov + cd1 + cd2)


def single(chars, xadv) -> bytes:
    cov = coverage(chars)
    return struct.pack(">HHHh", 1, 8, 4, xadv) + cov


def extension(kind, sub) -> bytes:
    return struct.pack(">HHI", 1, kind, 8) + sub


def gpos(lookups, script=b"latn") -> bytes:
    """One script, its default language system holding one `kern` feature over every lookup.

    `lookups`: (type, flag, [subtable bytes]); the type is the lookup's own (9 for extensions).
    """
    n = len(lookups)
    scripts = struct.pack(">H4sH", 1, script, 8) + struct.pack(">HH", 4, 0) + struct.pack(">HHHH", 0, 0xFFFF, 1, 0)
    feature = struct.pack(">HH", 0, n) + b"".join(struct.pack(">H", i) for i in range(n))
    features = struct.pack(">H4sH", 1, b"kern", 8) + feature
    tables, offs = b"", []
    head = 2 + 2 * n
    for kind, flag, subs in lookups:
        offs.append(head + len(tables))
        lh = 6 + 2 * len(subs)
        so, sb = [], b""
        for s in subs:
            so.append(lh + len(sb))
            sb += s
        tables += struct.pack(">HHH", kind, flag, len(subs)) + b"".join(struct.pack(">H", o) for o in so) + sb
    lookup_list = struct.pack(">H", n) + b"".join(struct.pack(">H", o) for o in offs) + tables
    o1 = 10
    o2 = o1 + len(scripts)
    o3 = o2 + len(features)
    return struct.pack(">HHHHH", 1, 0, o1, o2, o3) + scripts + features + lookup_list


def gdef_marks(chars) -> bytes:
    cd = classdef({c: 3 for c in chars})
    return struct.pack(">HHHHHH", 1, 0, 12, 0, 0, 0) + cd


def kern_table(pairs) -> bytes:
    """Microsoft's legacy table, format 0; `pairs` may list a pair twice."""
    body = struct.pack(">HHHH", len(pairs), 0, 0, 0)
    body += b"".join(struct.pack(">HHh", GID[a], GID[b], v) for (a, b), v in sorted(pairs, key=lambda p: (GID[p[0][0]], GID[p[0][1]])))
    return struct.pack(">HH", 0, 1) + struct.pack(">HHH", 0, 6 + len(body), 0x0001) + body


SYNTHETIC = {
    "pairs by glyph": dict(gpos=gpos([(2, 0, [pair_format1({("A", "V"): (-80, (0, 0)), ("T", "o"): (-60, (0, 0)),
                                                             ("V", "A"): (-75, (0, 0))})])])),
    "pairs by class": dict(gpos=gpos([(2, 0, [pair_format2({"A": 1, "V": 2, "T": 3}, {"V": 1, "A": 2, "o": 3, "a": 3},
                                                           [[0, 0, 0, 0], [0, -90, 0, -10], [0, 0, -70, -30],
                                                            [0, 0, -40, -55]])])])),
    "second glyph moved too": dict(gpos=gpos([(2, 0, [pair_format1({("A", "V"): (-40, (-20, -10)),
                                                                      ("V", "o"): (-30, (5, 0))}, vf2=5)])])),
    "behind an extension": dict(gpos=gpos([(9, 0, [extension(2, pair_format1({("T", "o"): (-65, (0, 0))}))])])),
    "two lookups add": dict(gpos=gpos([(2, 0, [pair_format1({("A", "V"): (-50, (0, 0))})]),
                                       (2, 0, [pair_format1({("A", "V"): (-25, (0, 0)), ("V", "A"): (-5, (0, 0))})])])),
    "first subtable wins": dict(gpos=gpos([(2, 0, [pair_format1({("A", "V"): (-50, (0, 0))}),
                                                   pair_format1({("A", "V"): (-99, (0, 0)), ("T", "o"): (-33, (0, 0))})])])),
    "single adjustment": dict(gpos=gpos([(1, 0, [single(".,", -40)]), (2, 0, [pair_format1({("o", "."): (-20, (0, 0))})])])),
    "a mark stepped over": dict(gpos=gpos([(2, 0x8, [pair_format1({("A", "V"): (-70, (0, 0))})])]), gdef=gdef_marks("M")),
    "default script": dict(gpos=gpos([(2, 0, [pair_format1({("A", "V"): (-45, (0, 0))})])], script=b"DFLT")),
    "legacy kern table": dict(kern=kern_table([(("A", "V"), -88), (("T", "o"), -66), (("A", "V"), -88), (("'", "'"), 30)])),
}
SYNTHETIC_TEXT = "AVA To Ta AMV VoAV o. o, '' TAVTo"


@need_hb
@pytest.mark.parametrize("case", sorted(SYNTHETIC))
def test_each_table_layout_matches_harfbuzz(case, tmp_path):
    path = tmp_path / "font.otf"
    path.write_bytes(build_font(**SYNTHETIC[case]))
    font = kerning.Font(path)
    assert font.source == ("kern" if case == "legacy kern table" else "GPOS")
    assert helper(path, SYNTHETIC_TEXT) == harfbuzz(path, SYNTHETIC_TEXT)
    assert any(g["advance_change"] or g["x_placement"] for g in font.layout(SYNTHETIC_TEXT)), "the case kerns something"


@need_hb
def test_a_pair_listed_twice_in_the_legacy_table_counts_once(tmp_path):
    path = tmp_path / "font.otf"
    path.write_bytes(build_font(**SYNTHETIC["legacy kern table"]))
    assert kerning.pairs(kerning.Font(path), "AV") == [{"pair": "AV", "units": -88, "per_mille_em": -88.0}]


# --- the shelf's fonts and the Mac's own --------------------------------------------------

def shelf() -> Path:
    """This machine's font shelf, from `folders.local`'s media line."""
    local = STUDIOS / "folders.local"
    if local.is_file():
        for line in local.read_text().splitlines():
            name, _, value = line.partition("=")
            if name.strip() == "media" and value.strip():
                return Path(os.path.expanduser(value.strip())) / "fonts"
    return Path("/nonexistent")


SERIF = shelf() / "source-serif-4.005"
REAL = {
    "static TrueType": SERIF / "TTF" / "SourceSerif4-Regular.ttf",
    "static CFF": SERIF / "OTF" / "SourceSerif4Display-Bold.otf",
    "variable, default instance": Path("/System/Library/Fonts/Supplemental/STIXTwoText.ttf"),
    "legacy kern only, collection": Path("/System/Library/Fonts/Times.ttc"),
    "legacy kern only": Path("/System/Library/Fonts/Supplemental/Trebuchet MS Bold.ttf"),
}


@need_hb
@pytest.mark.parametrize("name", sorted(REAL))
def test_real_fonts_match_harfbuzz_on_the_fixed_pairs(name):
    path = REAL[name]
    if not path.is_file():
        pytest.skip(f"{path} is not on this machine")
    font = kerning.Font(path)
    assert font.source == ("kern" if name.startswith("legacy") else "GPOS")
    assert helper(path, TEXT) == harfbuzz(path, TEXT)
    kerned = {p["pair"] for p in kerning.pairs(font, TEXT)}
    assert {"AV", "To"} <= kerned, "the probe's two pairs kern in every font here"


# --- Blender's values ---------------------------------------------------------------------

def test_a_value_is_a_share_of_the_left_characters_own_width():
    class Stub(kerning.Font):
        def __init__(self):
            self.cmap = {ord("A"): 1, ord("V"): 2, ord(" "): 3}
            self.advances = [500, 600, 640, 250]
            self.apple_tables = []

        def adjustments(self, gids):
            return [(0, -60) if (a, b) == (1, 2) else (0, -25) if (a, b) == (3, 1) else (0, 0)
                    for a, b in zip(gids, gids[1:] + [None])]

    values, limits = kerning.spacing(Stub(), "AV A\nAV", space_word=2.0)
    assert values[0] == pytest.approx(40 * -60 / 600) and values[5] == pytest.approx(40 * -60 / 600)
    assert values[2] == pytest.approx(40 * -25 / (250 * 2.0)), "a space's width includes the word spacing"
    assert values[1] == values[3] == values[4] == values[6] == 0 and not limits


@need_hb
def test_a_second_glyph_moved_on_its_own_is_carried_by_both_neighbours(tmp_path):
    path = tmp_path / "font.otf"
    path.write_bytes(build_font(**SYNTHETIC["second glyph moved too"]))
    font = kerning.Font(path)
    values, _ = kerning.spacing(font, "AVo")
    pos = [0.0]
    for c, v in zip("AVo", values):
        pos.append(pos[-1] + ADV[c] * (1 + v / 40))
    assert [round(x, 6) for x in pos[:3]] == [x for _, x in harfbuzz(path, "AVo")]


def test_what_cannot_be_matched_is_said(tmp_path):
    path = tmp_path / "font.otf"
    path.write_bytes(build_font(gpos=gpos([(2, 0, [pair_format1({("M", "A"): (-30, (0, 0)),
                                                                 ("A", "V"): (0, (15, 0))}, vf2=5)])])))
    values, limits = kerning.spacing(kerning.Font(path), "MA\nAV")
    assert values[0] == 0 and [l for l in limits if "no width" in l], "a zero-width character cannot carry kerning"
    assert values[3] == pytest.approx(40 * 15 / 650), "a second glyph moved on its own is set by its left neighbour"
    assert values[4] == pytest.approx(40 * -15 / 640), "and the line's end stays put"


@pytest.mark.parametrize("name", ["SourceSerif4Variable-Roman.ttf", "SourceSerif4Variable-Italic.otf"])
def test_a_variable_font_with_an_optical_size_axis_is_refused(name):
    path = SERIF / "VAR" / name
    if not path.is_file():
        pytest.skip(f"{path} is not on this machine")
    with pytest.raises(kerning.FontError, match="optical size 16"):
        kerning.Font(path)


def test_fonts_outside_scope_are_refused_plainly(tmp_path):
    for data, words in ((b"wOF2" + b"\0" * 60, "WOFF 2"), (b"<html>", "not an OpenType")):
        (tmp_path / "f").write_bytes(data)
        with pytest.raises(kerning.FontError, match=words):
            kerning.Font(tmp_path / "f")


def test_the_command_line_prints_the_pairs_for_the_appearance_packet(tmp_path):
    path = tmp_path / "font.otf"
    path.write_bytes(build_font(**SYNTHETIC["pairs by glyph"]))
    out = subprocess.run([sys.executable, str(TOOLS / "kerning.py"), str(path), "AV To", "--json"],
                         capture_output=True, text=True, check=True).stdout
    got = json.loads(out)
    assert got["source"] == "GPOS" and [p["pair"] for p in got["pairs"]] == ["AV", "To"]
    assert got["values"][0] == pytest.approx(40 * -80 / 650)


# --- in Blender -----------------------------------------------------------------------------

# Sets the words, lets the helper write the spacing, and measures each letter's origin: its ink's left edge in
# the words, less the same glyph's left edge set alone. One material per character sorts the ink by letter.
MEASURE = r'''
import bpy, json, sys
args = sys.argv[sys.argv.index("--") + 1:]
tools, font_path, text, size, space_word, out = args[0], args[1], args[2], float(args[3]), float(args[4]), args[5]
sys.path.insert(0, tools)
import kerning
vf = bpy.data.fonts.load(font_path)
cu = bpy.data.curves.new("words", "FONT"); cu.font = vf; cu.size = size; cu.space_word = space_word
ob = bpy.data.objects.new("words", cu); bpy.context.scene.collection.objects.link(ob)
for i in range(len(text)):
    cu.materials.append(bpy.data.materials.new(f"m{i}"))

def ink_left(body):
    if cu.body != body:  # setting the words again clears every character's spacing
        cu.body = body
    for i, f in enumerate(cu.body_format):
        f.material_index = i
    bpy.context.view_layer.update()
    ev = ob.evaluated_get(bpy.context.evaluated_depsgraph_get()); m = ev.to_mesh()
    left = {}
    for p in m.polygons:
        for v in p.vertices:
            x = m.vertices[v].co.x
            left[p.material_index] = min(left.get(p.material_index, x), x)
    ev.to_mesh_clear()
    return left

alone = {c: ink_left(c).get(0) for c in set(text) if c != " "}
cu.body = text
for f in cu.body_format:
    f.kerning = 0
plain = ink_left(text)
report = kerning.apply(ob, font_path, text)
kerned = ink_left(text)
for f, v in zip(cu.body_format, report["values"]):
    assert abs(f.kerning - v) < 1e-4
print("MEASURED " + json.dumps({
    "plain": {i: plain[i] - alone[c] for i, c in enumerate(text) if i in plain},
    "kerned": {i: kerned[i] - alone[c] for i, c in enumerate(text) if i in kerned},
    "values": report["values"], "pairs": report["pairs"], "limits": report["limits"]}))
'''


def blender_measure(tmp_path, font, text, size=1.0, space_word=1.0):
    script = tmp_path / "measure.py"
    script.write_text(MEASURE)
    r = subprocess.run([BLENDER, "-b", "--factory-startup", "--python-exit-code", "1", "--python", str(script), "--",
                        str(TOOLS), str(font), text, str(size), str(space_word), str(tmp_path)],
                       capture_output=True, text=True, timeout=300)
    line = next((l for l in r.stdout.splitlines() if l.startswith("MEASURED ")), None)
    assert r.returncode == 0 and line, r.stdout[-2000:] + r.stderr[-2000:]
    got = json.loads(line[len("MEASURED "):])
    return ({int(k): v for k, v in got["plain"].items()}, {int(k): v for k, v in got["kerned"].items()}, got)


# The tolerance the ticket asks for, in font units: half a unit, 0.05% of an em at 1,000 units.
TOLERANCE = 0.5


@pytest.mark.skipif(not (HB and HAVE_BLENDER), reason="needs Blender and HarfBuzz")
@pytest.mark.parametrize("name", ["static TrueType", "static CFF", "variable, default instance"])
@pytest.mark.parametrize("size", [1.0, 3.7])
def test_av_and_to_land_where_harfbuzz_puts_them_in_blender(name, size, tmp_path):
    font = REAL[name]
    if not font.is_file():
        pytest.skip(f"{font} is not on this machine")
    text = "AVATAR To Ty LT"
    plain, kerned, got = blender_measure(tmp_path, font, text, size)
    ref = [x for _, x in harfbuzz(font, text)]
    pen, base = 0, []
    for g in kerning.Font(font).layout(text):
        base.append(pen)
        pen += g["advance"]
    scale = plain[len(text) - 1] / base[-1]  # Blender units per font unit at this size, from the unkerned words
    for i in plain:
        assert plain[i] / scale == pytest.approx(base[i], abs=TOLERANCE), "Blender sets no kerning of its own"
    worst = max(abs(kerned[i] / scale - ref[i]) for i in kerned)
    assert worst <= TOLERANCE, f"letters land {worst:.3f} font units from HarfBuzz"
    assert {"AV", "To"} <= {p["pair"] for p in got["pairs"]} and base != ref, "the words kern"
    assert not got["limits"]


@pytest.mark.skipif(not (HB and HAVE_BLENDER), reason="needs Blender and HarfBuzz")
def test_word_spacing_is_allowed_for(tmp_path):
    font = REAL["static TrueType"]
    if not font.is_file():
        pytest.skip(f"{font} is not on this machine")
    text = "A To"
    plain, kerned, _ = blender_measure(tmp_path, font, text, 1.0, space_word=1.5)
    f = kerning.Font(font)
    space = f.advance(f.glyph(" "))
    # HarfBuzz's positions with the space half again as wide, which moves everything after it
    ref = [x + (0.5 * space if i > 1 else 0) for i, (_, x) in enumerate(harfbuzz(font, text))]
    scale = plain[3] / (f.advance(f.glyph("A")) + 1.5 * space + f.advance(f.glyph("T")))
    assert {" T", "To"} <= {p["pair"] for p in kerning.pairs(f, text)}, "the space kerns"
    assert max(abs(kerned[i] / scale - ref[i]) for i in kerned) <= TOLERANCE


REFUSALS = r'''
import bpy, sys
args = sys.argv[sys.argv.index("--") + 1:]
sys.path.insert(0, args[0])
import kerning
cu = bpy.data.curves.new("words", "FONT"); cu.body = "AV"
ob = bpy.data.objects.new("words", cu)
def refused(**kw):
    try:
        kerning.apply(ob, args[1], **kw)
    except kerning.FontError as e:
        return str(e)
print("BUILTIN", refused())
cu.font = bpy.data.fonts.load(args[1])
print("WORDS", refused(text="VA"))
cu.body_format[1].use_bold = True
print("BOLD", refused())
cu.body_format[1].use_bold = False
cu.font = bpy.data.fonts.load(args[2])
print("OTHER", refused())
'''


@pytest.mark.skipif(not HAVE_BLENDER, reason="needs Blender")
def test_apply_refuses_what_it_cannot_kern_truly(tmp_path):
    fonts = [f for f in (REAL["static TrueType"], REAL["static CFF"], REAL["variable, default instance"]) if f.is_file()]
    if len(fonts) < 2:
        pytest.skip("needs two fonts")
    script = tmp_path / "refusals.py"
    script.write_text(REFUSALS)
    r = subprocess.run([BLENDER, "-b", "--factory-startup", "--python-exit-code", "1", "--python", str(script), "--",
                        str(TOOLS), str(fonts[0]), str(fonts[1])], capture_output=True, text=True, timeout=300)
    out = dict(l.split(" ", 1) for l in r.stdout.splitlines() if l.split(" ", 1)[0] in ("BUILTIN", "WORDS", "BOLD", "OTHER"))
    assert r.returncode == 0, r.stdout[-2000:] + r.stderr[-2000:]
    assert "built-in font" in out["BUILTIN"] and "not 'VA'" in out["WORDS"]
    assert "bold, italic or in small caps" in out["BOLD"] and "is set in" in out["OTHER"]
