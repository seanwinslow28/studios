#!/usr/bin/env python3
"""Motioncraft's kerning helper: a font's own pair kerning, written into a Blender text object.

    python3 kerning.py FONT TEXT [--json]       → the pairs, their kerning in font units, and Blender's values

    import kerning                              (inside Blender, through the application doorway)
    kerning.apply(bpy.data.objects["Title"], "<version>/assets/fonts/<file>.otf")

Blender 5.2.2's text objects never apply a font's pair kerning and do no OpenType
shaping (Sean's type ruling, SWCB #244, 2026-10-21). They do take a per-character
spacing value, `body_format[i].kerning`, which can be keyframed. This helper reads
the font's own kerning for the exact words (the GPOS `kern` feature, or the legacy
`kern` table when GPOS has none, as HarfBuzz chooses) and writes the matching values
into those slots. Art then fine-tunes by eye in the appearance packet. Built as
Devcraft's pipeline software for Motioncraft on SWCB #255.

How Blender reads the value, probed headless on Blender 5.2.2 (2026-10-21): a
character's advance becomes `advance * (1 + kerning / 40)`, times the word spacing
when the character is a space, so the value is a share of that character's own
width and the same at every text size. Character spacing (tracking) adds on top.

Scope and known limits: Latin, left to right, one font file for the whole text.
No ligatures and no other glyph substitution (Blender draws the font's default
glyph for each character, and so does this helper). Static fonts, a collection's
first font (the one Blender loads), and a variable font's default instance, which
Blender loads only when the font has no optical-size axis: given one, Blender sets
optical size 16 whatever the text's size (probed 2026-10-21: Source Serif 4's
variable widths match `opsz=16` exactly, at text sizes 1 and 3.7), so such a font
is refused, and the release's static files serve instead. OpenType (`.otf`, `.ttf`, `.ttc`) and WOFF 1; never WOFF 2, and never
Apple's own layout tables (`morx`, `kerx`, `trak`), which only Apple's fonts carry
and which are named as a limit when present. Bold, italic and small caps set per
character in Blender, and the Justify and Flush alignments of a text box, are
refused or not matched; see `apply`.

Standard library only, so it runs in Blender's own Python with nothing installed.
"""
from __future__ import annotations

import argparse
import json
import os
import struct
import sys
import zlib
from typing import Dict, List, Optional, Sequence, Tuple

# Blender's divisor: kerning 40 adds one whole advance (vfont layout, Blender 5.2.2).
BLENDER_KERN_UNIT = 40.0

# GPOS lookup flags (OpenType 1.9, Lookup table).
IGNORE_BASE, IGNORE_LIGATURES, IGNORE_MARKS, USE_MARK_FILTERING_SET = 0x2, 0x4, 0x8, 0x10
MARK_ATTACHMENT_TYPE = 0xFF00


class FontError(ValueError):
    """The file is not a font this helper can read, or the request is outside its scope."""


def _u16(d: bytes, o: int) -> int:
    return struct.unpack_from(">H", d, o)[0]


def _i16(d: bytes, o: int) -> int:
    return struct.unpack_from(">h", d, o)[0]


def _u32(d: bytes, o: int) -> int:
    return struct.unpack_from(">I", d, o)[0]


# --- the font file --------------------------------------------------------------------------

def _tables(data: bytes, index: int) -> Dict[str, bytes]:
    """The font's tables by tag: plain OpenType, a collection's `index`th font, or WOFF 1."""
    tag = data[:4]
    if tag == b"wOF2":
        raise FontError("WOFF 2 needs Brotli, which is not in the standard library; use the release's .otf or .ttf")
    if tag == b"wOFF":
        n = _u16(data, 12)
        out = {}
        for i in range(n):
            t, off, comp, orig, _ = struct.unpack_from(">4sIIII", data, 44 + 20 * i)
            raw = data[off:off + comp]
            out[t.decode("latin-1")] = zlib.decompress(raw) if comp < orig else raw
        return out
    base = 0
    if tag == b"ttcf":
        count = _u32(data, 8)
        if not 0 <= index < count:
            raise FontError(f"the collection holds {count} fonts; there is no font {index}")
        base = _u32(data, 12 + 4 * index)
    elif index:
        raise FontError("only a collection (.ttc) has more than one font")
    if data[base:base + 4] not in (b"\x00\x01\x00\x00", b"OTTO", b"true"):
        raise FontError("not an OpenType or TrueType font")
    n = _u16(data, base + 4)
    out = {}
    for i in range(n):
        t, _, off, ln = struct.unpack_from(">4sIII", data, base + 12 + 16 * i)
        out[t.decode("latin-1")] = data[off:off + ln]
    return out


def _coverage(d: bytes, o: int) -> Dict[int, int]:
    """Coverage table: glyph id → coverage index."""
    fmt = _u16(d, o)
    if fmt == 1:
        return {_u16(d, o + 4 + 2 * i): i for i in range(_u16(d, o + 2))}
    if fmt == 2:
        cov = {}
        for i in range(_u16(d, o + 2)):
            start, end, first = struct.unpack_from(">HHH", d, o + 4 + 6 * i)
            for g in range(start, end + 1):
                cov[g] = first + g - start
        return cov
    raise FontError(f"unknown coverage format {fmt}")


def _classdef(d: bytes, o: int) -> Dict[int, int]:
    """ClassDef table: glyph id → class; a glyph not listed is class 0."""
    fmt = _u16(d, o)
    if fmt == 1:
        start, n = _u16(d, o + 2), _u16(d, o + 4)
        return {start + i: _u16(d, o + 6 + 2 * i) for i in range(n) if _u16(d, o + 6 + 2 * i)}
    if fmt == 2:
        cls = {}
        for i in range(_u16(d, o + 2)):
            start, end, c = struct.unpack_from(">HHH", d, o + 4 + 6 * i)
            if c:
                for g in range(start, end + 1):
                    cls[g] = c
        return cls
    raise FontError(f"unknown class definition format {fmt}")


def _value(d: bytes, o: int, fmt: int) -> Tuple[Tuple[int, int], int]:
    """A ValueRecord's (x placement, x advance) and its size in bytes.

    Device and variation-index tables are left out: they change nothing at the
    default instance with no pixel size set, which is how HarfBuzz shapes too.
    """
    xp = xa = 0
    p = o
    for bit in range(8):
        if fmt & (1 << bit):
            if bit == 0:
                xp = _i16(d, p)
            elif bit == 2:
                xa = _i16(d, p)
            p += 2
    return (xp, xa), p - o


class _SingleSubtable:
    """One SinglePos subtable: a kern feature may adjust a glyph on its own, a space's width say."""

    def __init__(self, d: bytes, o: int):
        fmt, vf = _u16(d, o), _u16(d, o + 4)
        self.cov = _coverage(d, o + _u16(d, o + 2))
        if fmt == 1:
            v = _value(d, o + 6, vf)[0]
            self.values = {g: v for g in self.cov}
        elif fmt == 2:
            size = 2 * bin(vf).count("1")
            self.values = {g: _value(d, o + 8 + size * ci, vf)[0] for g, ci in self.cov.items()}
        else:
            raise FontError(f"unknown single positioning format {fmt}")

    def match(self, gid: int):
        return self.values.get(gid)


class _PairSubtable:
    """One PairPos subtable, read once."""

    def __init__(self, d: bytes, o: int):
        self.fmt = _u16(d, o)
        self.cov = _coverage(d, o + _u16(d, o + 2))
        self.vf1, self.vf2 = _u16(d, o + 4), _u16(d, o + 6)
        self.len2 = bin(self.vf2).count("1")
        if self.fmt == 1:
            self.sets: Dict[int, Dict[int, Tuple[Tuple[int, int], Tuple[int, int]]]] = {}
            offs = [_u16(d, o + 10 + 2 * i) for i in range(_u16(d, o + 8))]
            for gid, ci in self.cov.items():
                p = o + offs[ci]
                pairs = {}
                q = p + 2
                for _ in range(_u16(d, p)):
                    second = _u16(d, q)
                    v1, n1 = _value(d, q + 2, self.vf1)
                    v2, n2 = _value(d, q + 2 + n1, self.vf2)
                    pairs.setdefault(second, (v1, v2))  # the first record wins, as in HarfBuzz's search
                    q += 2 + n1 + n2
                self.sets[gid] = pairs
        elif self.fmt == 2:
            self.cd1 = _classdef(d, o + _u16(d, o + 8))
            self.cd2 = _classdef(d, o + _u16(d, o + 10))
            self.n1, self.n2 = _u16(d, o + 12), _u16(d, o + 14)
            self.base = o + 16
            self.d = d
            self.s1, self.s2 = 2 * bin(self.vf1).count("1"), 2 * self.len2
        else:
            raise FontError(f"unknown pair positioning format {self.fmt}")

    def match(self, first: int, second: int):
        """The two value records when this subtable applies to the pair, else None."""
        if first not in self.cov:
            return None
        if self.fmt == 1:
            return self.sets[first].get(second)
        c1, c2 = self.cd1.get(first, 0), self.cd2.get(second, 0)
        if c1 >= self.n1 or c2 >= self.n2:
            return None
        p = self.base + (c1 * self.n2 + c2) * (self.s1 + self.s2)
        v1 = _value(self.d, p, self.vf1)[0]
        v2 = _value(self.d, p + self.s1, self.vf2)[0]
        return v1, v2


class Font:
    """The parts of one font this helper reads: units, glyph map, advances and pair kerning."""

    def __init__(self, source, index: int = 0):
        data = source if isinstance(source, (bytes, bytearray)) else open(source, "rb").read()
        self.path = None if isinstance(source, (bytes, bytearray)) else os.fspath(source)
        t = _tables(bytes(data), index)
        for need in ("head", "hhea", "hmtx", "cmap"):
            if need not in t:
                raise FontError(f"the font has no {need} table")
        if "fvar" in t:
            fvar = t["fvar"]
            axes = {fvar[_u16(fvar, 4) + 20 * i:_u16(fvar, 4) + 20 * i + 4] for i in range(_u16(fvar, 8))}
            if b"opsz" in axes:
                raise FontError("a variable font with an optical-size axis: Blender 5.2.2 sets it at optical size 16, "
                                "not at its default instance, so its widths and kerning are not the font's defaults; "
                                "use the release's static font for the size wanted")
        self.upm = _u16(t["head"], 18)
        n_metrics = _u16(t["hhea"], 34)
        hmtx = t["hmtx"]
        self.advances = [_u16(hmtx, 4 * i) for i in range(n_metrics)]
        self.cmap = self._read_cmap(t["cmap"])
        self.glyph_class: Dict[int, int] = {}
        self.mark_class: Dict[int, int] = {}
        self.mark_sets: List[Dict[int, int]] = []
        if "GDEF" in t:
            self._read_gdef(t["GDEF"])
        self.lookups: List[Tuple[int, int, int, list]] = []
        self.kern_pairs: Dict[Tuple[int, int], int] = {}
        self.source = "none"
        # Apple's own layout tables, which HarfBuzz would use instead: only Apple's fonts carry them.
        self.apple_tables = sorted(set(t) & {"morx", "mort", "kerx", "trak"})
        if "GPOS" in t:
            self._read_gpos(t["GPOS"])
        if not self.lookups and "kern" in t:
            self._read_kern(t["kern"])

    # glyph map and advances

    @staticmethod
    def _read_cmap(d: bytes) -> Dict[int, int]:
        best = None
        rank = {(3, 10): 0, (0, 6): 1, (0, 4): 2, (0, 3): 3, (3, 1): 4, (0, 2): 5, (0, 1): 6, (0, 0): 7}
        for i in range(_u16(d, 2)):
            plat, enc, off = struct.unpack_from(">HHI", d, 4 + 8 * i)
            fmt = _u16(d, off)
            if (plat, enc) in rank and fmt in (4, 12) and (best is None or rank[(plat, enc)] < best[0]):
                best = (rank[(plat, enc)], off, fmt)
        if best is None:
            raise FontError("the font has no Unicode character map")
        _, o, fmt = best
        out: Dict[int, int] = {}
        if fmt == 12:
            for i in range(_u32(d, o + 12)):
                start, end, gid = struct.unpack_from(">III", d, o + 16 + 12 * i)
                for c in range(start, end + 1):
                    out[c] = gid + c - start
            return out
        segs = _u16(d, o + 6) // 2
        ends, starts = o + 14, o + 16 + 2 * segs
        deltas, ranges = starts + 2 * segs, starts + 4 * segs
        for s in range(segs):
            end, start = _u16(d, ends + 2 * s), _u16(d, starts + 2 * s)
            delta, ro = _u16(d, deltas + 2 * s), _u16(d, ranges + 2 * s)
            for c in range(start, end + 1):
                if c == 0xFFFF:
                    continue
                if ro == 0:
                    gid = (c + delta) & 0xFFFF
                else:
                    gid = _u16(d, ranges + 2 * s + ro + 2 * (c - start))
                    gid = (gid + delta) & 0xFFFF if gid else 0
                if gid:
                    out[c] = gid
        return out

    def glyph(self, ch: str) -> int:
        """The glyph Blender draws for `ch`: the font's default one, 0 (.notdef) when missing."""
        return self.cmap.get(ord(ch), 0)

    def advance(self, gid: int) -> int:
        return self.advances[gid] if gid < len(self.advances) else self.advances[-1]

    # GDEF, for the lookup flags

    def _read_gdef(self, d: bytes) -> None:
        if _u16(d, 4):
            self.glyph_class = _classdef(d, _u16(d, 4))
        if _u16(d, 10):
            self.mark_class = _classdef(d, _u16(d, 10))
        if _u16(d, 2) >= 2 and len(d) >= 14 and _u16(d, 12):
            m = _u16(d, 12)
            self.mark_sets = [_coverage(d, m + _u32(d, m + 4 + 4 * i)) for i in range(_u16(d, m + 2))]

    def _skips(self, gid: int, flag: int, filter_set: int) -> bool:
        """Whether a lookup with `flag` steps over this glyph, as OpenType's lookup flags say."""
        cls = self.glyph_class.get(gid, 0)
        if cls == 1 and flag & IGNORE_BASE:
            return True
        if cls == 2 and flag & IGNORE_LIGATURES:
            return True
        if cls == 3:
            if flag & IGNORE_MARKS:
                return True
            if flag & USE_MARK_FILTERING_SET:
                return not (filter_set < len(self.mark_sets) and gid in self.mark_sets[filter_set])
            if flag & MARK_ATTACHMENT_TYPE:
                return self.mark_class.get(gid, 0) != (flag & MARK_ATTACHMENT_TYPE) >> 8
        return False

    # GPOS kern feature

    def _read_gpos(self, d: bytes) -> None:
        scripts, features, lookups = _u16(d, 4), _u16(d, 6), _u16(d, 8)
        # The script HarfBuzz picks for Latin text, then its default language system.
        tags = {struct.unpack_from(">4s", d, scripts + 2 + 6 * i)[0]: _u16(d, scripts + 6 + 6 * i)
                for i in range(_u16(d, scripts))}
        script = next((tags[t] for t in (b"latn", b"DFLT", b"dflt") if t in tags), None)
        if script is None:
            return
        so = scripts + script
        lang = _u16(d, so)
        if not lang:
            return
        lo = so + lang
        required = _u16(d, lo + 2)
        indices = [_u16(d, lo + 6 + 2 * i) for i in range(_u16(d, lo + 4))]
        if required != 0xFFFF:
            indices.append(required)
        chosen = set()
        for fi in indices:
            tag = struct.unpack_from(">4s", d, features + 2 + 6 * fi)[0]
            if tag == b"kern":
                fo = features + _u16(d, features + 6 + 6 * fi)
                chosen.update(_u16(d, fo + 4 + 2 * i) for i in range(_u16(d, fo + 2)))
        for li in sorted(chosen):  # HarfBuzz runs a stage's lookups in lookup-list order
            lo = lookups + _u16(d, lookups + 2 + 2 * li)
            kind, flag, n = _u16(d, lo), _u16(d, lo + 2), _u16(d, lo + 4)
            filter_set = _u16(d, lo + 6 + 2 * n) if flag & USE_MARK_FILTERING_SET else 0
            subs = []
            for si in range(n):
                so2 = lo + _u16(d, lo + 6 + 2 * si)
                k = kind
                if k == 9:  # Extension: the real subtable sits behind a 32-bit offset
                    k, so2 = _u16(d, so2 + 2), so2 + _u32(d, so2 + 4)
                if k in (1, 2):
                    subs.append((_SingleSubtable if k == 1 else _PairSubtable)(d, so2))
            if subs:
                self.lookups.append((k, flag, filter_set, subs))
        if self.lookups:
            self.source = "GPOS"

    # legacy kern table

    def _read_kern(self, d: bytes) -> None:
        pairs: Dict[Tuple[int, int], int] = {}
        if _u16(d, 0) == 0:  # Microsoft's header
            n, p, apple = _u16(d, 2), 4, False
        else:  # Apple's, version 1.0
            n, p, apple = _u32(d, 4), 8, True
        for _ in range(n):
            if apple:
                length, cov = _u32(d, p), _u16(d, p + 4)
                fmt, horizontal, cross, var = cov & 0xFF, not cov & 0x8000, cov & 0x4000, cov & 0x2000
                body, override = p + 8, False
            else:
                length, cov = _u16(d, p + 2), _u16(d, p + 4)
                fmt, horizontal, cross, var = cov >> 8, cov & 1, cov & 4, 0
                body, override = p + 6, bool(cov & 8)
                minimum = cov & 2
                if minimum:
                    horizontal = False  # a minimum-value table is not kerning
            if fmt == 0 and horizontal and not cross and not var:
                table: Dict[Tuple[int, int], int] = {}
                for i in range(_u16(d, body)):
                    left, right, v = struct.unpack_from(">HHh", d, body + 8 + 6 * i)
                    table.setdefault((left, right), v)  # a pair listed twice: one is found, never both
                for pair, v in table.items():
                    pairs[pair] = v if override else pairs.get(pair, 0) + v
            p += length
        self.kern_pairs = pairs
        if pairs:
            self.source = "kern"

    # layout

    def adjustments(self, gids: Sequence[int]) -> List[Tuple[int, int]]:
        """Each glyph's (x placement, x advance change) from the font's kerning, in font units."""
        adj = [[0, 0] for _ in gids]
        if self.source == "GPOS":
            for kind, flag, filter_set, subs in self.lookups:
                i = 0
                while i < len(gids):
                    if self._skips(gids[i], flag, filter_set):
                        i += 1
                        continue
                    if kind == 1:
                        m = next((v for v in (sub.match(gids[i]) for sub in subs) if v is not None), None)
                        if m is not None:
                            adj[i][0] += m[0]
                            adj[i][1] += m[1]
                        i += 1
                        continue
                    j = i + 1
                    while j < len(gids) and self._skips(gids[j], flag, filter_set):
                        j += 1
                    if j >= len(gids):
                        break
                    nxt = i + 1
                    for sub in subs:
                        m = sub.match(gids[i], gids[j])
                        if m is None:
                            continue
                        (p1, a1), (p2, a2) = m
                        adj[i][0] += p1
                        adj[i][1] += a1
                        adj[j][0] += p2
                        adj[j][1] += a2
                        nxt = j + 1 if sub.len2 else j  # a pair that moves its second glyph also uses it up
                        break
                    i = nxt
        elif self.source == "kern":
            for i in range(len(gids) - 1):
                adj[i][1] += self.kern_pairs.get((gids[i], gids[i + 1]), 0)
        return [(p, a) for p, a in adj]

    def layout(self, line: str) -> List[Dict]:
        """One line of text set left to right with the font's kerning: glyph, pen x and advance, in font units."""
        gids = [self.glyph(c) for c in line]
        adj = self.adjustments(gids)
        out, pen = [], 0
        for c, g, (xp, xa) in zip(line, gids, adj):
            out.append({"char": c, "glyph": g, "x": pen + xp, "advance": self.advance(g), "x_placement": xp,
                        "advance_change": xa})
            pen += self.advance(g) + xa
        return out


# --- Blender's values -----------------------------------------------------------------------

def spacing(font: Font, text: str, space_word: float = 1.0) -> Tuple[List[float], List[str]]:
    """Blender's `body_format[i].kerning` for each character of `text`, and what could not be matched.

    The value on character i sets the gap to character i + 1, so each one is worked
    from where the two glyphs must sit: their kerned pen positions, the second's
    placement included. A line break resets the pen. The last character's value
    keeps the line's end where HarfBuzz puts it, which only an aligned line shows.
    """
    values = [0.0] * len(text)
    limits: List[str] = []
    if font.apple_tables:
        limits.append(f"the font carries Apple's {', '.join(font.apple_tables)}, which this helper does not read")
    start = 0
    for line in text.split("\n"):
        glyphs = font.layout(line)
        for i, g in enumerate(glyphs):
            if i == 0 and g["x_placement"]:
                limits.append(f"{g['char']!r} at {start}: the line's first glyph moves by "
                              f"{g['x_placement']} units, which a spacing value cannot do")
            # the last glyph's gap runs to the line's end, which its own placement does not move
            end = g["advance"] + g["advance_change"] - g["x_placement"]
            gap = (glyphs[i + 1]["x"] - g["x"]) if i + 1 < len(glyphs) else end
            change = gap - g["advance"]
            if not change:
                continue
            width = g["advance"] * (space_word if g["char"] == " " else 1.0)
            if not width:
                limits.append(f"{g['char']!r} at {start + i} has no width, so its {change}-unit kerning cannot be set")
                continue
            values[start + i] = BLENDER_KERN_UNIT * change / width
        start += len(line) + 1
    return values, limits


def pairs(font: Font, text: str) -> List[Dict]:
    """Every kerned pair in `text`, for the appearance packet: the two characters and the units between them."""
    out = []
    for line in text.split("\n"):
        g = font.layout(line)
        for a, b in zip(g, g[1:]):
            change = (b["x"] - a["x"]) - a["advance"]
            if change:
                out.append({"pair": a["char"] + b["char"], "units": change, "per_mille_em": round(1000 * change / font.upm, 1)})
    return out


def _font_bytes(vfont) -> Optional[bytes]:
    """The bytes Blender set the text with: the packed copy, or the file it points at."""
    if vfont is None:
        return None
    if vfont.packed_file is not None:
        return bytes(vfont.packed_file.data)
    if vfont.filepath == "<builtin>":
        raise FontError("the object is set in Blender's built-in font; load the shelf's font file into it first")
    import bpy  # noqa: F401  (only ever called inside Blender)
    path = bpy.path.abspath(vfont.filepath)
    return open(path, "rb").read() if os.path.isfile(path) else None


def apply(obj, font_path: str, text: Optional[str] = None) -> Dict:
    """Write `font_path`'s own kerning into a Blender text object (or its curve), and say what was written.

    Every character's spacing value is set, zero where the font has no kerning,
    so run it on the words as Art set them, then fine-tune by eye. Refused: words
    that are not the object's, a font that is not the one the object is set in,
    and characters set bold, italic or in small caps, which draw from other font
    files or at another width. Not matched: the Justify and Flush alignments of a
    text box, which spread each line after the spacing is applied.
    """
    curve = getattr(obj, "data", obj)
    if getattr(curve, "body_format", None) is None:
        raise FontError(f"{getattr(obj, 'name', obj)!r} is not a text object")
    data = open(font_path, "rb").read()
    if text is not None and text != curve.body:
        raise FontError(f"the object holds {curve.body!r}, not {text!r}")
    used = _font_bytes(curve.font)
    if used is not None and used != data:
        raise FontError(f"the object is set in {curve.font.filepath!r}, not in {font_path!r}")
    styled = [i for i, f in enumerate(curve.body_format) if f.use_bold or f.use_italic or f.use_small_caps]
    if styled:
        raise FontError(f"characters {styled} are set bold, italic or in small caps; set each style as its own object")
    font = Font(data)  # a collection's first font, the one Blender loads
    values, limits = spacing(font, curve.body, curve.space_word)
    for f, v in zip(curve.body_format, values):
        f.kerning = v
    if curve.align_x in ("JUSTIFY", "FLUSH") and any(b.width for b in curve.text_boxes):
        limits.append(f"the text box's {curve.align_x} alignment respaces each line after the kerning")
    return {"font": font_path, "source": font.source, "upm": font.upm, "values": values,
            "pairs": pairs(font, curve.body), "limits": limits}


# --- command line ---------------------------------------------------------------------------

def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="A font's own pair kerning for some words, as Blender spacing values.")
    ap.add_argument("font")
    ap.add_argument("text")
    ap.add_argument("--index", type=int, default=0, help="the font's number in a .ttc collection")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        font = Font(a.font, a.index)
    except (OSError, FontError) as e:
        print(f"kerning: {e}", file=sys.stderr)
        return 1
    values, limits = spacing(font, a.text)
    found = pairs(font, a.text)
    if a.json:
        print(json.dumps({"source": font.source, "upm": font.upm, "values": values, "pairs": found, "limits": limits}))
        return 0
    print(f"{os.path.basename(a.font)}: kerning from {font.source}, {font.upm} units to the em")
    for i, (c, v) in enumerate(zip(a.text, values)):
        if v:
            print(f"  [{i}] {c!r}  kerning {v:+.4f}")
    for p in found:
        print(f"  {p['pair']!r}: {p['units']:+d} units ({p['per_mille_em']:+} thousandths of an em)")
    for line in limits:
        print(f"  not matched: {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
