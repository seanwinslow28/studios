"""Runs a Python script inside Krita with no screen, and fails when text would fall back to a substitute font.

    python3 krita_run.py <script.py> [--fonts <folder>] [--home <folder>] [--timeout <s>] [-- <script args>...]

Krita's headless runner (`kritarunner`) runs the script inside Krita's own Python, on Qt's offscreen platform. Layers,
blend modes, opacity, filters, .kra files and per-layer exports all work there. Krita's brush engine does not: its
paint calls need a canvas view, and none opens without a screen, so draw strokes with Qt's painter and put them on
layers. Inside the script, `from krita import Krita` works as it does in Krita's own scripter. Every document the
script creates or opens is put in batch mode, so an export never waits on an options dialog no one can see.

Why this wrapper and not kritarunner alone:
- kritarunner exits 0 even when the script fails to load, so this file runs the script itself and reports how it
  really ended: the exit code is the script's, and the log's last line is "KRITA_RUN done <code>".
- Krita reads its font folders only at start-up and sets text in a substitute, with no error, when the font it names
  is missing. --fonts registers every font file in a folder with Krita's own Fontconfig before the script runs.
  Then text added through VectorLayer.addShapesFromSvg, a document opened, or a document still open at the end that
  names a family no --fonts file holds, or names none, fails the run, even if the script catches the refusal.
- Krita keeps its settings, resources and caches in the home folder. The run uses a home of its own (--home, by
  default ~/.cache/motioncraft/krita-home), so Sean's own Krita settings are never read or changed. The first run
  there takes longer while Krita writes its starting resources.

Krita must be installed at /Applications/krita.app, or set KRITA_APP to the app's folder.
"""
import json
import os
import runpy
import sys
import traceback

TEXT_TAGS = ("text", "tspan", "textPath")
DONE = "KRITA_RUN done"
FONT_FAULT = "KRITA_RUN font-fault"
FONT_SUFFIXES = (".otf", ".ttf", ".otc", ".ttc")
faults = []


# --- inside Krita -----------------------------------------------------------------------------

def families(svg):
    """The font families each text, tspan and textPath element in an SVG names, inherited from its parents as SVG
    does; None for one that names none, which Krita sets in its default font. A ValueError if the SVG is unreadable."""
    import xml.etree.ElementTree as ET
    try:
        root = ET.fromstring(svg.encode("utf-8") if isinstance(svg, str) else svg)
    except ET.ParseError as e:
        raise ValueError(f"the SVG could not be read: {e}")
    out = []

    def own(el):
        named = el.get("font-family")
        for part in (el.get("style") or "").split(";"):
            key, _, value = part.partition(":")
            if key.strip() == "font-family":
                named = value
        if named is None:
            return None
        return [f.strip().strip("'\"").strip() for f in named.split(",") if f.strip().strip("'\"").strip()]

    def walk(el, inherited):
        named = own(el)
        named = inherited if named is None else named
        if el.tag.rsplit("}", 1)[-1] in TEXT_TAGS:
            out.append(named)
        for child in el:
            walk(child, named)

    walk(root, None)
    return out


def unregistered(svg, registered):
    """What in this SVG's text Krita would set in a font this run did not register."""
    try:
        found = families(svg)
    except ValueError as e:
        return [str(e)]
    said = []
    for named in found:
        if not named:
            said.append("a text names no font, so Krita would set it in its default font")
        for f in named or []:
            if f.casefold() not in registered:
                said.append(f"a text names the font {f!r}, which this run did not register")
    return sorted(set(said))


def register(files, lib):
    """Hand each font file to Krita's current Fontconfig configuration; the families now registered."""
    import ctypes

    class FontSet(ctypes.Structure):
        _fields_ = [("nfont", ctypes.c_int), ("sfont", ctypes.c_int), ("fonts", ctypes.POINTER(ctypes.c_void_p))]
    fc = ctypes.CDLL(lib)
    fc.FcConfigGetCurrent.restype = ctypes.c_void_p
    fc.FcConfigAppFontAddFile.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    fc.FcConfigGetFonts.restype = ctypes.POINTER(FontSet)
    fc.FcConfigGetFonts.argtypes = [ctypes.c_void_p, ctypes.c_int]
    fc.FcPatternGetString.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)]
    cfg = fc.FcConfigGetCurrent()
    for f in files:
        if not fc.FcConfigAppFontAddFile(cfg, f.encode()):
            raise RuntimeError(f"Krita's Fontconfig would not read the font {f}")
    names = set()
    fs = fc.FcConfigGetFonts(cfg, 1)  # FcSetApplication: the fonts added for this process alone
    for i in range(fs.contents.nfont if fs else 0):
        j, s = 0, ctypes.c_char_p()
        while fc.FcPatternGetString(fs.contents.fonts[i], b"family", j, ctypes.byref(s)) == 0:
            names.add(s.value.decode("utf-8", "replace"))
            j += 1
    return names


def watch(registered):
    """Refuse text, new or reopened, that names a family not registered, recording each refusal as a fault; and put
    every document the script creates or opens in batch mode."""
    from krita import Krita, VectorLayer

    def refuse(where, said):
        msg = f"{where}: " + "; ".join(said) + " (register the job's fonts with --fonts)"
        if msg not in faults:
            faults.append(msg)
        return RuntimeError(msg)

    def check_doc(doc):
        said, stack = [], [doc.rootNode()]
        while stack:
            n = stack.pop()
            if hasattr(n, "toSvg"):
                said += unregistered(n.toSvg(), registered)
            stack += list(n.childNodes())
        return sorted(set(said))

    add, opened, created = VectorLayer.addShapesFromSvg, Krita.openDocument, Krita.createDocument

    def addShapesFromSvg(self, svg):
        said = unregistered(svg, registered)
        if said:
            raise refuse("addShapesFromSvg", said)
        return add(self, svg)

    def createDocument(self, *args):
        doc = created(self, *args)
        if doc is not None:
            doc.setBatchmode(True)  # an export never waits on an options dialog no one can see
        return doc

    def openDocument(self, path):
        doc = opened(self, path)
        if doc is not None:
            doc.setBatchmode(True)
        said = check_doc(doc) if doc is not None else []
        if said:
            raise refuse(f"openDocument {path}", said)
        return doc

    def sweep():
        for doc in Krita.instance().documents():
            said = check_doc(doc)
            if said:
                refuse(f"the open document {doc.fileName() or doc.name()}", said)

    VectorLayer.addShapesFromSvg, Krita.openDocument, Krita.createDocument = addShapesFromSvg, openDocument, createDocument
    return sweep


def main(_args):
    """kritarunner's entry point (`-s krita_run -f main`): register the fonts, run the script, report how it ended."""
    from krita import Krita
    Krita.instance().setBatchmode(True)  # no dialogs: a script's file calls never wait on a person
    script = os.environ.get("KRITA_RUN_SCRIPT", "")
    sys.argv = [script] + json.loads(os.environ.get("KRITA_RUN_ARGS", "[]"))
    code = 0
    try:
        fonts = json.loads(os.environ.get("KRITA_RUN_FONTS", "[]"))
        registered = register(fonts, os.environ["KRITA_RUN_FONTCONFIG"]) if fonts else set()
        print("KRITA_RUN fonts", json.dumps(sorted(registered)), flush=True)
        sweep = watch({f.casefold() for f in registered})
    except BaseException:
        traceback.print_exc()
        script, code, sweep = "", 1, (lambda: None)
    if script:
        try:
            runpy.run_path(script, run_name="__main__")
        except SystemExit as e:
            code = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
        except BaseException:
            traceback.print_exc()
            code = 1
    try:
        sweep()
    except BaseException:
        traceback.print_exc()
        code = code or 1
    for f in faults:
        print(FONT_FAULT, f, flush=True)
    code = code or (1 if faults else 0)
    print(DONE, code, flush=True)
    sys.stderr.flush()
    os._exit(code)  # kritarunner itself exits 0 whatever happened


# --- from the shell -----------------------------------------------------------------------------

def run(argv=None):
    import argparse
    import shutil
    import subprocess
    import tempfile
    from pathlib import Path

    argv = list(sys.argv[1:] if argv is None else argv)
    extra = []
    if "--" in argv:
        extra, argv = argv[argv.index("--") + 1:], argv[:argv.index("--")]
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("script", help="the Python script to run inside Krita")
    ap.add_argument("--fonts", help="a folder of font files to register before the script runs")
    ap.add_argument("--home", default="~/.cache/motioncraft/krita-home", help="Krita's home folder for this run")
    ap.add_argument("--timeout", type=float, default=1800, help="seconds before the run is stopped")
    a = ap.parse_args(argv)

    app = Path(os.environ.get("KRITA_APP", "/Applications/krita.app"))
    runner = app / "Contents" / "MacOS" / "kritarunner"
    if not os.access(runner, os.X_OK):
        raise SystemExit(f"krita_run.py: no kritarunner at {runner}; install Krita or set KRITA_APP")
    script = Path(a.script).resolve()
    if not script.is_file():
        raise SystemExit(f"krita_run.py: no script at {script}")
    fonts = []
    if a.fonts:
        folder = Path(a.fonts).expanduser().resolve()
        fonts = sorted(str(p) for p in folder.iterdir() if p.suffix.lower() in FONT_SUFFIXES)
        if not fonts:
            raise SystemExit(f"krita_run.py: no font files in {folder}")
    home = Path(a.home).expanduser().resolve()
    home.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="krita-run-") as base:
        # kritarunner ignores PYTHONPATH but reads the user site folder, which PYTHONUSERBASE moves.
        site = Path(base) / "lib" / "python" / "site-packages"
        site.mkdir(parents=True)
        shutil.copyfile(__file__, site / "krita_run.py")
        env = dict(os.environ)
        # HOME for Qt and Fontconfig, CFFIXED_USER_HOME for macOS's own folder lookups (Library/...), which ignore HOME.
        env.update(HOME=str(home), CFFIXED_USER_HOME=str(home), PYTHONUSERBASE=base, QT_QPA_PLATFORM="offscreen",
                   LANG="en_US.UTF-8", LC_ALL="en_US.UTF-8", KRITA_RUN_SCRIPT=str(script),
                   KRITA_RUN_ARGS=json.dumps(extra), KRITA_RUN_FONTS=json.dumps(fonts),
                   KRITA_RUN_FONTCONFIG=str(app / "Contents" / "Frameworks" / "libfontconfig.1.dylib"))
        proc = subprocess.Popen([str(runner), "-s", "krita_run", "-f", "main"], env=env, stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        try:
            out, _ = proc.communicate(timeout=a.timeout)
        except subprocess.TimeoutExpired:
            proc.kill()
            out, _ = proc.communicate()
            sys.stdout.write(out or "")
            raise SystemExit(f"krita_run.py: stopped after {a.timeout:.0f} s")
        sys.stdout.write(out or "")
        lines = (out or "").splitlines()
    done = [l for l in lines if l.startswith(DONE)]
    if not done:
        raise SystemExit(f"krita_run.py: Krita ended without the script finishing (exit {proc.returncode})")
    return int(done[-1].split()[-1])


if __name__ == "__main__":
    sys.exit(run())
