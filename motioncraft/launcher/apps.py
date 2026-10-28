#!/usr/bin/env python3
"""The application doorway: Blender, Resolve and Krita for a seat pass, run by the launcher outside the pass's sandbox, under a lock of its own.

    apps.py ask blender --script F [--blend B] [--timeout S] [--wait S] [-- ARG...]    (from inside a pass)
    apps.py ask blender --render --blend B --out D [--frames S-E] [--engine E] [--device cpu|gpu] [--timeout S] [--wait S]
    apps.py ask resolve --script F [--timeout S] [--wait S] [-- ARG...]
    apps.py ask krita --script F [--fonts D] [--timeout S] [--wait S] [-- ARG...]
    apps.py ask hyperframes --render --project P --out D [--fps N] [--timeout S] [--wait S]
    apps.py ask hyperframes --check --project P [--timeout S] [--wait S]
    apps.py ask higgsfield --entry IMn|VIn --out F [--timeout S] [--wait S]
    apps.py ask higgsfield --status
    apps.py ask higgsfield --settle <job id> --out F
    apps.py wait <id> [--wait S]
    apps.py lock <context> blender|resolve|krita|hyperframes                          (the coordinator: print a lock)

Neither vendor's sandbox lets Blender or Resolve work from inside a pass. Both hide
the Mac's graphics chip (no IOKit opening for `AGXDeviceUserClient`, and no setting
that adds one on Codex 0.163.0 or Claude Code 2.1.303), so Blender 5.2.2 finds no
Metal device and crashes reading its name; and Resolve's scripting is a TCP link to
the running Resolve, which a pass with the network off cannot make. So a pass never
runs either. It leaves a request in its scratch folder (`ask`), and the launcher,
which supervises the pass from outside its sandbox, checks the request against the
pass's context and runs the application under a Seatbelt lock written from the same
context: reads as the pass reads them (its denies kept), writes only where the
pass's fence lets it write (the frozen version folders and artifacts refused), no
network, and only the openings the application needs. Blender's lock adds the
graphics chip and Metal's shader compiler, and a cache folder of Blender's own.
The script that runs is the launcher's copy in `trace/logs/pass-NN.apps/`, where no
seat writes, so the record holds what ran.

Grease Pencil, Eevee and Workbench render only through the render request
(`--render`). Blender draws them with its GPU drawing engine, which registers Blender
with macOS's app registry (LaunchServices) on start, and the lock refuses that, so
the render aborts (exit -6). The render request opens that one service, and in return
runs no code of the seat's: the launcher's own render script (`RENDER_SCRIPT`), the
scene opened with Blender's auto-run of scripts in a file switched off, Cycles on the
CPU with no OSL script nodes, or on the graphics chip (Metal) when the request asks
for `--device gpu`. The GPU needs no opening the CPU's lock lacks, so both run under
the same lock; a GPU render is kept in a version folder only in a film whose brief
adopts it (`render_device: gpu`), Sean's call per film (SWCB #272). The opening lets a process see which apps are running
and which is in front, nothing more (screen, windows, clipboard, input and launching
apps stay refused; tested 2026-10-19). A kept render is Cycles into a new version
folder; Eevee and Workbench render only into the scratch folder, as previews. Ruled
on the Motioncraft build map's "Grease Pencil renders" ticket (2026-10-19).

Resolve is different: anything connected to it can make it run code in its own,
unfenced process (Fusion's `Execute` runs Lua there; tested 2026-10-19). So a
Resolve script never reaches Resolve. Its lock has no network at all, only one local
socket, to a broker the launcher starts outside the lock, which alone holds the
connection. The script imports a stand-in `DaVinciResolveScript` whose objects
forward each attribute and call to the broker. The broker allows only the methods
in Resolve's own API file (`DaVinciResolveScript.pyi`, read from the installed
version), less the ones that run code or reach Fusion at all, change Sean's
Resolve settings and presets, switch the database, delete, archive or restore
projects, touch cloud projects, or quit. It allows work only in projects whose names
start with the media project's name, refuses a path argument outside the media
project, and lets a method that writes a file (an export, the render target) write
only into the pass's fence. A project, timeline, bin, grade or LUT file in a version
folder or the fence loads only as Resolve itself exported it: the broker records the
sha256 of each file Resolve exports in this machine's export register, and checks a
load against it, in any later pass (SWCB #264). Resolve still writes its own database
and caches, so for the length of each Resolve call the doorway also records every
path written on the Mac (FSEvents) and sorts them into the fence, Resolve's own
folders, frozen paths and everything else; the check record carries anything
outside the fence, which another program on the Mac may also have written in that
window.

Krita runs with no screen: `kritarunner`, Qt's offscreen platform, the seat's script
inside Krita's own Python by the launcher's wrapper module (`KRITA_WRAPPER`). Layers,
blend modes, opacity, filters, `.kra` files and per-layer exports work there. Krita's
brush engine does not: its paint calls need a canvas view, and every way to open one
with no screen crashes (Sean chose, on the map's "Krita's doorway" ticket, 2026-10-20,
to build the doorway without it: Art draws its strokes with Qt's painter and puts them
on layers). kritarunner keeps its settings, resources and caches under its own name in
the home folder, and Python modules there are on its path, so each call gets a home of
its own (`CFFIXED_USER_HOME`): a fresh clone of a template the launcher built once with
no code of a seat's, deleted after the call, so no pass leaves anything for a later one
and Sean's own Krita is never read or written. kritarunner exits 0 when a script fails
to load, so a call succeeds only when the wrapper's closing line says the script ended.
Krita reads its font folders only at start-up and sets text in a substitute, with no
error, when the font it names is missing. So the launcher registers the version's fonts
(`--fonts`, a folder in the media project) with Krita's own Fontconfig before the
seat's script runs, and the record names each file by checksum. In every call, text
added, a document opened, or a document still open at the end that names a family no
`--fonts` registered, or names none, fails the call, even if the script catches the
refusal (Sean's call on SWCB #263, 2026-10-22).

HyperFrames is the Animator's code route (SWCB #276, Sean's pick 2026-10-28): the shot
is a composition, an HTML page whose GSAP timeline the renderer seeks frame by frame,
in a project folder the pass wrote. Headless Chrome cannot start inside either vendor's
sandbox (macOS refuses its startup rendezvous, `bootstrap_check_in`), so the launcher
runs the pinned HyperFrames command line (`[apps] hyperframes`, on `[apps] node`, with
the pinned `[apps] chrome`) and nothing else: `render` to a PNG sequence at a fixed frame
rate, software drawing, screenshot capture, `--strict`, and `check`. The pass picks no
flag and runs no code in Node; its page's scripts run only inside Chrome. HyperFrames
feeds the page to Chrome from a file server on "any free port" of this Mac's loopback,
and drives each Chrome over another. The launcher picks a handful of free loopback ports
for the call, and its own preload (`HF_PINS`, loaded into every Node process of the call)
hands each of those servers, and each Chrome's control port, one of them. The lock allows
TCP to and from exactly those ports and nothing else, so a page reaches neither the Mac's
other servers (its databases, model runners, AirPlay) nor anything off it. Allowing all
of loopback and denying the ports already in use does not hold: Seatbelt let a denied
port through for many port numbers, with a later deny not winning over the earlier
allow (tested 2026-10-28), while an allow-list held for every port tried.
It adds Chrome's own rendezvous name, the power-management client Chrome opens, and the
scheduling call HyperFrames' lint worker makes. No graphics chip, no window server, no
font server (a font is a file the page loads). Each call runs in a home of its own,
deleted after, with telemetry off, so Sean's own `~/.hyperframes` is never read or
written. Frames repeat byte for byte under the lock (tested 2026-10-28).

Higgsfield comes through the same requests (SWCB #271), for Art's images and the
Animator's video: the launcher runs its own doorway, launcher/higgsfield.py, for one
entry of Sean's approved list, with no lock, since the call needs the network and the
sign-in no pass may read. The doorway holds the terms (the approved list, the uploads,
the takes, the credit caps, the filing); this file only carries the request to it.

Every call is logged to `trace/logs/pass-NN.apps.jsonl`, and its result, log, lock
and script copy go to `trace/logs/pass-NN.apps/`, which the pass reads but cannot
write. Written on the Motioncraft build map's "Blender and Resolve inside the seat
sandboxes" ticket (2026-10-19), Krita on "Krita's doorway" (2026-10-20), HyperFrames on
SWCB #276 (2026-10-28).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import plistlib
import secrets
import shutil
import stat
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional

HERE = Path(__file__).resolve().parent
APPS = ("blender", "resolve", "krita", "hyperframes")
REQUEST = re.compile(r"(blender|resolve|krita|hyperframes|higgsfield)-[0-9]{6}-[0-9a-f]{6}\.json")
# HyperFrames: the frame rates a render may ask for, and the flags every render carries, which the pass never sets.
# A PNG sequence (the kept render crosses to Finishing as frames, as Blender's does), software drawing and screenshot
# capture (the path that repeats a frame; the fast capture needs the graphics chip), lint errors fail the render, and
# missing media fails it rather than rendering around it.
HF_FPS = (24, 25, 30, 50, 60)
HF_RENDER_FLAGS = ("--format", "png-sequence", "--no-browser-gpu", "--experimental-fast-capture=false", "--strict",
                   "--no-best-effort")
# What every HyperFrames call's environment says: no telemetry, no update checks, no skills installed, no .env read.
HF_ENV = {"HYPERFRAMES_NO_TELEMETRY": "1", "DO_NOT_TRACK": "1", "HYPERFRAMES_SKIP_SKILLS": "1",
          "HYPERFRAMES_NO_CAPTURE_DOTENV": "1", "CI": "1"}
# How many loopback ports a call gets: one file server and one control port per Chrome (the probe, the calibration,
# the workers); a call that runs out fails, closed.
HF_PORTS = 24
# The launcher's preload for every Node process of a HyperFrames call (NODE_OPTIONS=--require; written into the call's
# record). A server asked for "any port" gets the next of the launcher's ports, and so does a Chrome started with
# `--remote-debugging-port=0`. Each port is claimed by making a file in the call's home, so the call's processes never
# hand out the same one; an "any port" past the last fails.
HF_PINS = r'''"use strict";
// Motioncraft's port pins for one HyperFrames call (motioncraft/launcher/apps.py, HF_PINS). Never hand-edited.
const fs = require("fs"), path = require("path"), net = require("net"), cp = require("child_process");
const ports = (process.env.MOTIONCRAFT_HF_PORTS || "").split(",").map(Number).filter(Boolean);
const claims = process.env.MOTIONCRAFT_HF_CLAIMS;
function take() {
  for (const p of ports) {
    try { fs.closeSync(fs.openSync(path.join(claims, String(p)), "wx")); return p; }
    catch (e) { if (e.code !== "EEXIST") throw e; }
  }
  throw new Error("motioncraft: this HyperFrames call used every loopback port the launcher gave it");
}
const listen = net.Server.prototype.listen;
net.Server.prototype.listen = function (...args) {
  const a = args[0];
  if (a && typeof a === "object" && a.path === undefined && a.handle === undefined && !a.port) args[0] = { ...a, port: take() };
  else if (a === 0 || a === "0") args[0] = take();
  else if (a === undefined || typeof a === "function") args.unshift(take());
  return listen.apply(this, args);
};
for (const name of ["spawn", "execFile"]) {
  const orig = cp[name];
  cp[name] = function (file, argv, ...rest) {
    if (Array.isArray(argv)) argv = argv.map(x => x === "--remote-debugging-port=0" ? `--remote-debugging-port=${take()}` : x);
    return orig.call(this, file, argv, ...rest);
  };
}
require("module").syncBuiltinESMExports();
'''
# Higgsfield's doorway: an entry of Sean's approved list, by its id (launcher/higgsfield.py, SWCB #271).
HIGGSFIELD_ENTRY = re.compile(r"(IM|VI)\d{1,4}")
HIGGSFIELD_JOB = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
MAX_REQUEST_BYTES = 64_000
MAX_SCRIPT_BYTES = 256_000
MAX_ARGS, MAX_ARG = 32, 2048
DEFAULT_TIMEOUT_S, MAX_TIMEOUT_S = 1800, 3600
DEFAULT_WAIT_S = 540  # under Claude Code's ten-minute Bash limit; `wait` picks up a longer call
POLL_S = 0.3
# The render request: the engine names a pass may give, and Blender's own for each. Only Cycles is kept.
RENDER_ENGINES = {"cycles": "CYCLES", "eevee": "BLENDER_EEVEE", "workbench": "BLENDER_WORKBENCH"}
# Cycles' device: the CPU by default; the graphics chip (Metal) on `--device gpu`, kept only where the brief adopts it.
RENDER_DEVICES = {"cpu": "CPU", "gpu": "GPU"}
MAX_RENDER_FRAMES = 2400  # 100 s at 24 fps; a longer stretch is two requests
# The render request's script: the launcher's, never a seat's. It sets the engine, the frames and the folder, and
# renders; it reads nothing else from the request. Cycles runs on the CPU (the one path that repeats a frame
# exactly) or, asked, on the Metal device, with OSL off, since a script node is code. Cycles falls back to the CPU
# without a word when no GPU device is enabled, so a GPU render with no Metal device stops instead. `autoexec_fail`
# is set when Blender skipped a script the file carries (a driver expression, a registered text block), so the log
# says when one was there.
RENDER_SCRIPT = r'''import bpy, os, sys
out, start, end, engine, device = sys.argv[sys.argv.index("--") + 1:]
print("MOTIONCRAFT_RENDER autoexec_blocked", bool(bpy.app.autoexec_fail), repr(bpy.app.autoexec_fail_message))
s = bpy.context.scene
s.render.engine = engine
if engine == "CYCLES":
    s.cycles.device = device
    s.cycles.shading_system = False
    used = []
    if device == "GPU":
        p = bpy.context.preferences.addons["cycles"].preferences
        p.compute_device_type = "METAL"
        p.get_devices()
        for d in p.devices:
            d.use = d.type == "METAL"
        used = [d.name for d in p.devices if d.use]
        if not used:
            raise SystemExit("MOTIONCRAFT_RENDER no Metal device: Cycles would render on the CPU")
    print("MOTIONCRAFT_RENDER device", device, *([used] if used else []))
s.frame_start, s.frame_end = int(start), int(end)
os.makedirs(out, exist_ok=True)
s.render.filepath = os.path.join(out, "frame-")
s.render.use_file_extension = True
bpy.ops.render.render(animation=True)
print("MOTIONCRAFT_RENDER done", engine, start, end)
'''
# Krita: the module kritarunner imports (`-s`), from a folder of the launcher's put on Krita's Python path by
# PYTHONUSERBASE (kritarunner ignores PYTHONPATH). It runs the seat's script as `__main__` with its arguments, then
# prints how it ended and exits with that code; a call with no script (the template build) starts Krita and stops.
KRITA_MODULE = "motioncraft_krita"
KRITA_DONE = "MOTIONCRAFT_KRITA done"
KRITA_FONTS = "MOTIONCRAFT_KRITA fonts"
KRITA_FONT_FAULT = "MOTIONCRAFT_KRITA font-fault"
# The version's fonts (`--fonts`): font files only, a licence beside them left alone.
FONT_SUFFIXES = (".otf", ".ttf", ".otc", ".ttc")
MAX_FONTS, MAX_FONT_BYTES = 64, 64_000_000
# Before the script, the wrapper hands each of the call's font files to the Fontconfig configuration Krita's text
# library made and set current (`FcConfigAppFontAddFile`, the call that library makes itself; E8, SWCB #256), and
# reads back the families they hold. Then it watches every way text reaches a document: `addShapesFromSvg` refuses
# text naming a family not registered, `openDocument` refuses a document holding such text (a .kra stores the
# family's name, not the font), and at the end every document still open is read once more. A refusal is printed
# as a font-fault line and fails the call, so a script that catches it still fails.
KRITA_WRAPPER = r'''"""Motioncraft's wrapper: runs one seat script inside Krita (motioncraft/launcher/apps.py)."""
import json, os, runpy, sys, traceback

TEXT_TAGS = ("text", "tspan", "textPath")
faults = []


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
    """What in this SVG's text Krita would set in a font this call did not register."""
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
                said.append(f"a text names the font {f!r}, which this call did not register")
    return sorted(set(said))


def register(files, lib):
    """Hand each font file to Krita's current Fontconfig configuration; the families now registered, folded."""
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
    """Refuse text, new or reopened, that names a family not registered; record each refusal as a fault."""
    from krita import Krita, VectorLayer

    def refuse(where, said):
        msg = f"{where}: " + "; ".join(said) + " (register the version's fonts with --fonts)"
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

    add, opened = VectorLayer.addShapesFromSvg, Krita.openDocument

    def addShapesFromSvg(self, svg):
        said = unregistered(svg, registered)
        if said:
            raise refuse("addShapesFromSvg", said)
        return add(self, svg)

    def openDocument(self, path):
        doc = opened(self, path)
        said = check_doc(doc) if doc is not None else []
        if said:
            raise refuse(f"openDocument {path}", said)
        return doc

    def sweep():
        for doc in Krita.instance().documents():
            said = check_doc(doc)
            if said:
                refuse(f"the open document {doc.fileName() or doc.name()}", said)

    VectorLayer.addShapesFromSvg, Krita.openDocument = addShapesFromSvg, openDocument
    return sweep


def main(_args):
    from krita import Krita
    Krita.instance().setBatchmode(True)  # no dialogs: a script's file calls never wait on a person
    script = os.environ.get("MOTIONCRAFT_KRITA_SCRIPT", "")
    sys.argv = [script] + json.loads(os.environ.get("MOTIONCRAFT_KRITA_ARGS", "[]"))
    code = 0
    try:
        fonts = json.loads(os.environ.get("MOTIONCRAFT_KRITA_FONTS", "[]"))
        registered = register(fonts, os.environ["MOTIONCRAFT_KRITA_FONTCONFIG"]) if fonts else set()
        print("MOTIONCRAFT_KRITA fonts", json.dumps(sorted(registered)), flush=True)
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
        print("MOTIONCRAFT_KRITA font-fault", f, flush=True)
    code = code or (1 if faults else 0)
    print("MOTIONCRAFT_KRITA done", code, flush=True)
    sys.stderr.flush()
    os._exit(code)  # kritarunner itself exits 0 whatever happened
'''


# --- inside the pass: ask, then wait ----------------------------------------------------

def requests_dir() -> Path:
    d = os.environ.get("MOTIONCRAFT_APPS_REQUESTS")
    if not d:
        sys.exit("apps.py: this pass has no application doorway (only a drafting pass whose seat lists an app)")
    return Path(d)


def results_dir() -> Path:
    return Path(os.environ["MOTIONCRAFT_APPS_RESULTS"])


def show(rid: str, wait_s: float) -> None:
    out = results_dir() / f"{rid}.result.json"
    end = time.time() + wait_s
    while not out.exists():
        if time.time() >= end:
            print(f"{rid}: still running; run `apps.py wait {rid}` to keep waiting")
            sys.exit(75)
        time.sleep(0.5)
    time.sleep(0.1)  # the launcher writes the result in one write; give it a moment to land
    res = json.loads(out.read_text(encoding="utf-8"))
    log = results_dir() / f"{rid}.log"
    if log.exists():
        tail = log.read_text(encoding="utf-8", errors="replace").splitlines()[-40:]
        print("\n".join(tail))
        print("---")
    print(json.dumps(res, indent=1))
    sys.exit(0 if res.get("ok") else (res.get("exit_code") or 1))


def cmd_ask(a) -> None:
    d = requests_dir()
    rid = f"{a.app}-{time.strftime('%H%M%S')}-{secrets.token_hex(3)}"
    if a.app == "higgsfield":
        one = [bool(a.status), bool(a.entry and a.out), bool(a.settle and a.out)]
        if a.script or a.render or a.blend or a.fonts or a.args or sum(one) != 1 or (a.entry and a.settle):
            sys.exit("apps.py: ask higgsfield --entry <IMn or VIn> --out <file in a new version folder>, "
                     "--settle <job id> --out <file in a new version folder>, or --status")
        h = ({"status": True} if a.status else {"settle": a.settle, "out": os.path.abspath(a.out)} if a.settle
             else {"entry": a.entry, "out": os.path.abspath(a.out)})
        req = {"id": rid, "app": a.app, "timeout": a.timeout, "higgsfield": h}
    elif a.entry or a.status or a.settle:
        sys.exit("apps.py: --entry, --settle and --status are Higgsfield's")
    elif a.app == "hyperframes":
        if a.script or a.blend or a.fonts or a.args or a.frames or a.device != "cpu" or not a.project \
                or a.render == a.check \
                or (a.render and not a.out) or (a.check and (a.out or a.fps)):
            sys.exit("apps.py: ask hyperframes --render --project <folder> --out <folder> [--fps N], or "
                     "ask hyperframes --check --project <folder>; no script")
        h = {"mode": "render" if a.render else "check", "project": os.path.abspath(a.project)}
        if a.render:
            h.update(out=os.path.abspath(a.out), fps=a.fps or 60)
        req = {"id": rid, "app": a.app, "timeout": a.timeout, "hyperframes": h}
    elif a.project or a.check or a.fps:
        sys.exit("apps.py: --project, --check and --fps are HyperFrames'")
    elif a.device != "cpu" and not a.render:
        sys.exit("apps.py: --device is the render request's: ask blender --render ... --device gpu")
    elif a.render:
        m = re.fullmatch(r"(\d+)-(\d+)", a.frames or "")
        if a.app != "blender" or a.script or a.args or not a.blend or not a.out or not m:
            sys.exit("apps.py: ask blender --render --blend <scene> --out <folder> --frames S-E [--engine E] "
                     "[--device cpu|gpu]; no --script")
        req = {"id": rid, "app": a.app, "timeout": a.timeout,
               "render": {"blend": os.path.abspath(a.blend), "out": os.path.abspath(a.out),
                          "frames": [int(m[1]), int(m[2])], "engine": a.engine, "device": a.device}}
    else:
        if not a.script:
            sys.exit("apps.py: ask needs --script, or --render for a render")
        if a.fonts and a.app != "krita":
            sys.exit("apps.py: --fonts is Krita's: the version's font folder, registered before the script runs")
        req = {"id": rid, "app": a.app, "script": os.path.abspath(a.script), "args": a.args or [],
               "timeout": a.timeout, "blend": os.path.abspath(a.blend) if a.blend else "",
               **({"fonts": os.path.abspath(a.fonts)} if a.fonts else {})}
    part = d / f".{rid}.part"
    part.write_text(json.dumps(req) + "\n", encoding="utf-8")
    os.rename(part, d / f"{rid}.json")  # whole, or not there: the launcher reads only finished requests
    print(f"{rid}: asked; the launcher runs it")
    show(rid, a.wait)


def cmd_wait(a) -> None:
    show(a.id, a.wait)


# --- the launcher's side ------------------------------------------------------------------

def _seat():
    sys.path.insert(0, str(HERE))
    import seat  # noqa: E402  the launcher's own rules: the context, the fence, the denies
    return seat


def app_paths() -> Dict[str, str]:
    """The applications' paths on this machine, from the allowlist's [apps] table."""
    seat = _seat()
    table = seat.toolbelts().get("apps", {})
    return {k: os.path.expanduser(str(v)) for k, v in table.items()}


def sb(s: str) -> str:
    return json.dumps(s)  # an SBPL string literal is a JSON one for these paths


def user_cache() -> str:
    """This user's cache folder (`/var/folders/…/C/`), where Metal keeps a per-app cache; Python's confstr lacks the name."""
    try:
        r = subprocess.run(["/usr/bin/getconf", "DARWIN_USER_CACHE_DIR"], capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return r.stdout.strip() if r.returncode == 0 else ""


def user_temp() -> str:
    """This user's temporary folder (`/var/folders/…/T/`), which Qt on the Mac uses whatever TMPDIR says."""
    try:
        r = subprocess.run(["/usr/bin/getconf", "DARWIN_USER_TEMP_DIR"], capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return r.stdout.strip() if r.returncode == 0 else ""


def sb_regex_literal(s: str) -> str:
    """A path as a literal inside a Seatbelt regex: every character but letters, digits, `/` and `_` escaped."""
    return "".join(c if c.isalnum() or c in "/_" else "\\" + c for c in s)


def blender_cache() -> str:
    seat = _seat()
    return seat.real(os.path.expanduser(os.environ.get("MOTIONCRAFT_APPS_CACHE", "~/.cache/motioncraft/apps/blender")))


def krita_cache() -> str:
    seat = _seat()
    return seat.real(os.path.expanduser(os.environ.get("MOTIONCRAFT_KRITA_CACHE", "~/.cache/motioncraft/apps/krita")))


def hyperframes_cache() -> str:
    """Where each HyperFrames call's own home goes (`calls/<id>/`, deleted when the call ends)."""
    seat = _seat()
    return seat.real(os.path.expanduser(os.environ.get("MOTIONCRAFT_HYPERFRAMES_CACHE", "~/.cache/motioncraft/apps/hyperframes")))


def free_ports(n: int = HF_PORTS) -> List[int]:
    """`n` loopback ports free now, as the system hands them out: the only ports a HyperFrames call's lock allows."""
    import socket
    held = []
    try:
        for _ in range(n):
            s = socket.socket()
            s.bind(("127.0.0.1", 0))
            held.append(s)
        return sorted(s.getsockname()[1] for s in held)
    finally:
        for s in held:
            s.close()


def resolve_cache() -> str:
    """The broker's own folder on this machine, outside every fence: each call's folder (`calls/<id>/`, deleted when the
    call ends) and the export register (`exports.jsonl`), which only the broker writes."""
    seat = _seat()
    return seat.real(os.path.expanduser(os.environ.get("MOTIONCRAFT_RESOLVE_CACHE", "~/.cache/motioncraft/apps/resolve")))


def krita_version(kritarunner: str) -> str:
    """The installed Krita's version, from its bundle; a new version gets a template of its own."""
    try:
        with open(Path(kritarunner).parents[1] / "Info.plist", "rb") as f:
            return str(plistlib.load(f).get("CFBundleShortVersionString") or "unknown")
    except (OSError, IndexError, plistlib.InvalidFileException):
        return "unknown"


def brief_render_device(eng: str) -> str:
    """The film's render device from its brief's header: `gpu` only once Sean adopts it for this film, else `cpu`."""
    _seat()
    from sound import header  # noqa: E402  the same ledger reader the sound and Higgsfield doorways use
    try:
        return header((Path(eng) / "brief.md").read_text(encoding="utf-8")).get("render_device") or "cpu"
    except OSError:
        return "cpu"


def lock(ctx: Dict, app: str, socket_path: str = "", render: bool = False, home: str = "", ports=()) -> str:
    """The Seatbelt lock for one application call, written from the pass's context.

    Deny by default, as Codex's own base policy does; read as the pass reads (its
    denies kept); write only the fence's folders, with everything frozen in them
    refused after; no network. Blender adds the graphics chip and Metal's shader
    compiler; a Resolve script adds only the broker's one local socket; Krita adds
    only the call's own home folder (`home`) and the font server. A render
    request (`render`, Blender only) adds LaunchServices, which Blender's GPU drawing
    engine registers with on start, and nothing else. A GPU render (Cycles on Metal)
    needs nothing more than Blender's graphics chip and shader compiler, so its lock is
    the CPU render's, rule for rule. HyperFrames adds its own home, TCP on this Mac's
    loopback to and from the call's own `ports` only, and the three openings Chrome
    needs to start with no screen.
    """
    seat = _seat()
    if app not in APPS:
        raise ValueError(app)
    no_read = sorted(set(seat.no_read(ctx)))
    write = list(ctx["fence"]["write"])
    frozen = list(ctx["fence"]["frozen"])
    lines = [
        "(version 1)",
        f"; Motioncraft's {app} lock for {ctx['source']}. Written by launcher/apps.py; never hand-edited.",
        "(deny default)",
        "(allow process-exec process-fork)",
        "(allow signal (target same-sandbox))",
        "(allow process-info* (target same-sandbox))",
        "(allow sysctl-read)",
        "(allow user-preference-read)",
        "(allow ipc-posix-sem)",
        "(allow ipc-posix-shm-read* (ipc-posix-name-prefix \"apple.cfprefs.\"))",
        "(allow file-read*)",
    ]
    if no_read:
        lines.append("(deny file-read* " + " ".join(f"(subpath {sb(p)})" for p in no_read) + ")")
    lines += [
        "(allow file-write* " + " ".join(f"(subpath {sb(p)})" for p in write) + ")",
        "(allow file-write-data file-ioctl (literal \"/dev/null\") (literal \"/dev/zero\"))",
        "(allow mach-lookup (global-name \"com.apple.system.opendirectoryd.libinfo\")"
        " (global-name \"com.apple.system.notification_center\") (global-name \"com.apple.bsd.dirhelper\")"
        " (global-name \"com.apple.system.logger\") (global-name \"com.apple.logd\")"
        " (global-name \"com.apple.cfprefsd.daemon\") (global-name \"com.apple.cfprefsd.agent\"))",
    ]
    if app == "blender":
        cache = blender_cache()
        own = [cache] + ([os.path.join(user_cache(), "org.blenderfoundation.blender")] if user_cache() else [])
        bundle = str(Path(app_paths().get("blender", "/Applications/Blender.app/Contents/MacOS/Blender")).parents[2])
        lines += [
            "; the graphics chip, Metal's shader compiler and the fonts Blender draws text with",
            "(allow iokit-get-properties)",
            "(allow iokit-open (iokit-user-client-class \"AGXDeviceUserClient\")"
            " (iokit-registry-entry-class \"IOSurfaceRootUserClient\") (iokit-registry-entry-class \"RootDomainUserClient\"))",
            "(allow mach-lookup (global-name \"com.apple.MTLCompilerService\") (global-name \"com.apple.fonts\")"
            " (global-name \"com.apple.FontObjectsServer\"))",
            "; Blender's own caches: Cycles' kernels (XDG_CACHE_HOME) and Metal's per-app cache",
            "(allow file-write* " + " ".join(f"(subpath {sb(seat.real(p))})" for p in own) + ")",
            "(allow file-issue-extension (require-all (extension-class \"com.apple.app-sandbox.read\")"
            f" (subpath {sb(seat.real(bundle))})))",
            "(allow file-issue-extension (require-all (extension-class \"com.apple.app-sandbox.read\" \"com.apple.app-sandbox.read-write\") "
            + " ".join(f"(subpath {sb(seat.real(p))})" for p in own[1:]) + "))" if own[1:] else "",
        ]
        if render:
            lines += [
                "; the render request only, which runs the launcher's render script and no code of the seat's: Blender's GPU",
                "; drawing engine (Grease Pencil, Eevee, Workbench) registers with LaunchServices on start, or aborts. It shows",
                "; which apps are running; the window server, clipboard and the app database stay shut (tested 2026-10-19)",
                "(allow mach-lookup (global-name \"com.apple.coreservices.launchservicesd\"))",
            ]
    elif render:
        raise ValueError("only Blender has a render request")
    elif app == "krita":
        if not home:
            raise ValueError("a Krita call runs in a home folder of its own")
        lines += [
            "; Krita's home for this call: a fresh copy of the launcher's template, its settings, resources and caches",
            f"(allow file-write* (subpath {sb(seat.real(home))}))",
            "; Krita saves a .kra through a hidden copy named .XXXXXX.<ext> in the Mac's own temporary folder, which Qt",
            "; uses whatever TMPDIR says; without it a save waits for ever (2026-10-20). That file name only, nothing else",
            "; (Seatbelt's regexes take no {n} counts, so the name is one or more letters or digits, a dot, an extension)",
            *([f'(allow file-write* (regex #"^{sb_regex_literal(seat.real(user_temp()))}/\\.[A-Za-z0-9]+\\.[A-Za-z0-9]+$"))']
              if user_temp() else []),
            "; the fonts Krita draws text with; no graphics chip, no window server (Qt's offscreen platform)",
            "(allow mach-lookup (global-name \"com.apple.fonts\") (global-name \"com.apple.FontObjectsServer\"))",
        ]
    elif app == "hyperframes":
        if not home:
            raise ValueError("a HyperFrames call runs in a home folder of its own")
        if not ports:
            raise ValueError("a HyperFrames call runs on loopback ports the launcher chose for it")
        mine = " ".join(f"(local tcp \"localhost:{int(p)}\")" for p in ports)
        theirs = " ".join(f"(remote tcp \"localhost:{int(p)}\")" for p in ports)
        lines += [
            "; HyperFrames' home for this call: its settings and caches, never Sean's own ~/.hyperframes",
            f"(allow file-write* (subpath {sb(seat.real(home))}))",
            "; the lint worker lowers its own priority (setpriority), which Seatbelt files under scheduling",
            "(allow system-sched)",
            "; HyperFrames serves the page to Chrome from a loopback port and drives each Chrome over another; the launcher's",
            "; preload gives each one of these ports. TCP on them only: no other port on the Mac, nothing off it, no UDP",
            "; (an allow for all of loopback with these denied after it did not hold in Seatbelt; tested 2026-10-28)",
            f"(allow network-bind {mine})",
            f"(allow network-inbound {mine})",
            f"(allow network-outbound {theirs})",
            "; Chrome with no screen: its own rendezvous service, which it registers and its helpers look up, and the",
            "; power-management client it opens. No graphics chip, no window server, no font server (tested 2026-10-28)",
            "(allow mach-register (global-name-prefix \"org.chromium.\"))",
            "(allow mach-lookup (global-name-prefix \"org.chromium.\"))",
            "(allow iokit-open (iokit-registry-entry-class \"RootDomainUserClient\"))",
        ]
    else:
        lines += ["; the broker's socket, and nothing else: never Resolve's own ports, which would let a script make it run code"]
        if socket_path:
            lines.append(f"(allow network-outbound (remote unix-socket (path-literal {sb(socket_path)})))")
    if frozen:
        lines.append("; saved before this pass: never changed (rule 5); after the allows, so it wins")
        lines.append("(deny file-write* " + " ".join(f"(subpath {sb(p)})" for p in frozen) + ")")
    return "\n".join(l for l in lines if l) + "\n"


def resolve_ports() -> List[int]:
    """The TCP ports the running Resolve and its fuscript server listen on, or none if Resolve is not running."""
    pids = []
    for name in ("Resolve", "fuscript"):
        r = subprocess.run(["pgrep", "-x", name], capture_output=True, text=True)
        pids += [p for p in r.stdout.split() if p.isdigit()]
    if not pids:
        return []
    r = subprocess.run(["lsof", "-nP", "-a", "-p", ",".join(pids), "-iTCP", "-sTCP:LISTEN", "-Fn"],
                       capture_output=True, text=True)
    return sorted({int(m) for m in re.findall(r"^n\S*:(\d+)$", r.stdout, re.M)})


RESOLVE_STATE = r"""
import json, DaVinciResolveScript as d
r = d.scriptapp("Resolve")
out = {"running": bool(r)}
if r:
    pm = r.GetProjectManager(); p = pm.GetCurrentProject()
    out.update(version=r.GetVersionString(), database=pm.GetCurrentDatabase(), project=p.GetName() if p else None,
               render_targets=sorted({j.get("TargetDir", "") for j in (p.GetRenderJobList() or [])}) if p else [])
print(json.dumps(out))
"""


def resolve_state(env: Dict[str, str], python: str) -> Dict:
    """What Resolve itself says after a call: its database, the open project, the render jobs' folders."""
    try:
        r = subprocess.run([python, "-c", RESOLVE_STATE], env=env, capture_output=True, text=True, timeout=60)
        return json.loads(r.stdout.strip().splitlines()[-1]) if r.stdout.strip() else {"error": r.stderr.strip()[-300:]}
    except (subprocess.TimeoutExpired, ValueError, IndexError) as e:
        return {"error": str(e)}


# --- the Resolve broker: the one holder of the connection ----------------------------------

RESOLVE_API = Path("/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/DaVinciResolveScript.pyi")
# Never through the doorway, whatever the API file lists: code run inside Resolve or Fusion's object graph, Sean's
# own settings and presets, the database, deleting, archiving or restoring projects, cloud projects, and quitting.
# Fusion is closed for every seat (ruled 2026-10-19 on "Fusion through the doorway"): beside these names, every method
# whose name holds "Fusion" is refused (`FUSION`), so the three that put a Fusion title, generator or composition on a
# timeline, `CreateFusionClip`, and any Fusion method a later Resolve adds stay shut. DCTL is code: never validated
# or encrypted for a pass. `AddTransition` is refused whole (SWCB #257, Sean's call 2026-10-21): its `category` may be
# 'fusion' or 'ofx', which reach Fusion or outside plug-in code. `SetFades` is refused too (SWCB #262): Resolve 21.1.1
# loses a clip's fade on save and reload (mc-e8.d01), so a card's fade is baked into its frames by ffmpeg instead.
RESOLVE_DENY = frozenset("""
AddTransition SetFades Fusion GetFusionCompByIndex GetFusionCompByName AddFusionComp ImportFusionComp LoadFusionCompByName EncryptDCTL
InsertFusionTitleIntoTimeline InsertFusionGeneratorIntoTimeline InsertFusionCompositionIntoTimeline ValidateDCTL
DeleteBurnInPreset DeleteKeyboardPreset DeleteLayoutPreset DeleteUserPreferencesPreset DeleteRenderPreset
DeleteProjectSettingsPreset ImportBurnInPreset ImportKeyboardPreset ImportLayoutPreset ImportUserPreferencesPreset
ImportRenderPreset ImportProjectSettingsPreset LoadKeyboardPreset LoadLayoutPreset LoadUserPreferencesPreset
SaveLayoutPreset SaveUserPreferencesPreset UpdateLayoutPreset UpdateProjectSettingsPreset UpdateRenderPreset
SaveAsNewRenderPreset SaveCurrentProjectSettingsAsNewPreset SetQuickExportEnabledForRenderPreset
DisableBackgroundTasksForCurrentResolveSession SetCurrentDatabase DeleteProject DeleteFolder ArchiveProject
RestoreProject CreateCloudProject ImportCloudProject LoadCloudProject RestoreCloudProject Quit
""".split())
FUSION = re.compile(r"Fusion")
# Methods whose path arguments name a file Resolve writes: those go only into the pass's fence.
RESOLVE_WRITES = frozenset("""
Export ExportBurnInPreset ExportCurrentFrameAsStill ExportFusionComp ExportKeyboardPreset ExportLUT ExportLayoutPreset
ExportMetadata ExportProject ExportProjectSettingsPreset ExportRenderPreset ExportStills ExportUserPreferencesPreset
SetRenderSettings RenderWithQuickExport
""".split())
# Methods that name a project by their first argument: only the job's own projects.
RESOLVE_NAMED_PROJECT = frozenset({"CreateProject", "LoadProject", "ExportProject"})
# Methods that load a project, timeline or bin file, which can carry Fusion compositions and so code, or a grade or
# LUT. A file in a version folder of any stage, or in the pass's fence, loads only when its sha256 is in the export
# register, that is, only as Resolve itself exported it through the doorway, in this pass or an earlier one; never a
# file a pass wrote, frozen since or not (SWCB #264). Resolve reads the broker's own copy of the bytes it checked. A
# file elsewhere in the media project (Sean's `inputs/`) loads as it is.
# A grade file (`.drx`, by `ApplyGradeFromDRX` or a gallery's `ImportStills`) holds the node graph as one compressed
# binary blob the doorway cannot read, naming each node's tools (LUTs and DCTLs by name, ResolveFX); a LUT may be a
# DCTL, which is code. Found 2026-10-19 on Resolve 21.1.1; see the launcher README.
RESOLVE_IMPORTS = frozenset({"ImportProject", "ImportTimelineFromFile", "ImportFolderFromFile", "ImportIntoTimeline",
                             "ApplyGradeFromDRX", "ImportStills", "SetLUT"})
# Methods that write a file a later call may load, by the index of the path they write (`ExportStills` a folder). The
# broker has Resolve write into the call's own folder, which no pass can reach, records each file's sha256 in the
# export register, then copies the file out to where the script named. A pass that rewrites the file while Resolve
# writes it changes only its own copy, never the register.
RESOLVE_EXPORTS = {"ExportProject": 1, "Export": 0, "ExportLUT": 1, "ExportStills": 1, "ExportCurrentFrameAsStill": 0}
# Calls on Resolve or the project manager that do not act on the open project, so may run whichever is open.
RESOLVE_ANY_PROJECT = frozenset({"CreateProject", "LoadProject", "ImportProject", "ExportProject", "OpenPage",
                                 "GotoRootFolder", "GotoParentFolder", "OpenFolder", "CreateFolder"})
CONSTANT = re.compile(r"[A-Z][A-Z0-9_]+")


def resolve_api(path: Path = RESOLVE_API) -> frozenset:
    """The method names Resolve documents for the installed version, less the denied ones.

    The API file holds the current forms; the README's deprecated sections still list
    the older ones Resolve answers to and its examples use (`GetSetting`, `SetSetting`).
    """
    names = set(re.findall(r"^\s+def ([A-Z][A-Za-z0-9]*)\(", path.read_text(encoding="utf-8"), re.M))
    readme = path.with_name("README.md")
    if readme.is_file():
        text = readme.read_text(encoding="utf-8")
        old = text[text.find("## Deprecated Resolve API Functions"):] if "## Deprecated Resolve API Functions" in text else ""
        names |= set(re.findall(r"^(?:[A-Z]\w*\.)?([A-Z][A-Za-z0-9]*)\(", old, re.M))
    return frozenset(n for n in names - RESOLVE_DENY if not FUSION.search(n))


class Refused(Exception):
    pass


class Broker:
    """Holds the real Resolve objects and answers the stand-in's requests, each held to the pass's fence.

    Every object the script sees is a handle into this table. A handle remembers
    the project it came from, so work in a project not named for this job is
    refused (its name aside), and the method a handle was read as, so a call can be
    checked by name before it reaches Resolve.
    """

    def __init__(self, root, ctx: Dict, allowed: frozenset, prefix: str, home: str, register: str) -> None:
        self.seat = _seat()
        import freeze  # noqa: E402  the stages a version folder sits in
        self.ctx, self.allowed, self.prefix = ctx, allowed, prefix
        self.objs: Dict[int, object] = {0: root}
        self.meta: Dict[int, Dict] = {0: {"name": "Resolve", "project": None}}
        self.calls: List[Dict] = []
        self.home, self.register = Path(home), Path(register)  # the call's own folder; the machine's export register
        project = self.seat.real(ctx["media_project"])
        # where a pass may have written a file: this pass's fence, and every version folder of every stage, any pass's
        self.pass_written = [self.seat.real(w) for w in ctx["fence"]["write"]] + \
            [os.path.join(project, s) for s in freeze.STAGES]
        self.note: Dict = {}  # what the call in hand exported or loaded, for its line in the call log

    def open(self, name: str) -> bool:
        """Listed open, and never a refused or Fusion name, whatever list the broker was given."""
        return name in self.allowed and name not in RESOLVE_DENY and not FUSION.search(name)

    def ours(self, project: Optional[str]) -> bool:
        return project is None or project.startswith(self.prefix)

    def keep(self, obj, name: str, project: Optional[str], parent: Optional[int] = None) -> Dict:
        h = len(self.objs)
        self.objs[h], self.meta[h] = obj, {"name": name, "project": project, "parent": parent}
        return {"__h__": h}

    def encode(self, v, name: str, project: Optional[str]):
        if v is None or isinstance(v, (bool, int, float, str)):
            return v
        if isinstance(v, (list, tuple)):
            return [self.encode(x, name, project) for x in v]
        if isinstance(v, dict):
            return {"__d__": [[self.encode(k, name, project), self.encode(x, name, project)] for k, x in v.items()]}
        return self.keep(v, name, project)

    def current_project(self) -> Optional[str]:
        p = self.objs[0].GetProjectManager().GetCurrentProject()
        return p.GetName() if p else None

    def decode(self, v):
        if isinstance(v, list):
            return [self.decode(x) for x in v]
        if isinstance(v, dict):
            if "__h__" in v:
                if v["__h__"] not in self.objs:
                    raise Refused("an object this call never handed out")
                if not self.ours(self.meta[v["__h__"]]["project"]):
                    raise Refused(f"an object from the project {self.meta[v['__h__']]['project']!r}, not this job's")
                return self.objs[v["__h__"]]
            if "__d__" in v:
                return {self.decode(k): self.decode(x) for k, x in v["__d__"]}
            raise Refused("a dict travels as {'__d__': [[key, value], ...]}")
        return v

    def strings(self, v) -> List[str]:
        if isinstance(v, str):
            return [v]
        if isinstance(v, (list, tuple)):
            return [s for x in v for s in self.strings(x)]
        if isinstance(v, dict):
            return [s for k, x in v.items() for s in self.strings(k) + self.strings(x)]
        return []

    def check_paths(self, name: str, args) -> None:
        seat, ctx = self.seat, self.ctx
        for s in self.strings(args):
            if "/" not in s:
                continue
            if not s.startswith("/"):
                raise Refused(f"{name}: give paths whole, from /, not {s!r}")
            p = seat.real(s)
            if name in RESOLVE_WRITES:
                if not any(seat.under(p, w) for w in ctx["fence"]["write"]) or any(seat.under(p, f) for f in ctx["fence"]["frozen"]):
                    raise Refused(f"{name} writes {s}, outside this pass's fence (a new version folder in its stage)")
            elif not (seat.under(p, ctx["media_project"]) or seat.under(p, ctx["scratch"])):
                raise Refused(f"{name}: {s} is outside the media project; Resolve reads nothing else for a pass")

    def fresh(self, kind: str) -> Path:
        return Path(tempfile.mkdtemp(prefix=f"{kind}-", dir=self.home))

    def exported_sums(self) -> set:
        try:
            lines = self.register.read_text(encoding="utf-8").splitlines()
        except FileNotFoundError:
            return set()
        return {json.loads(l)["sha256"] for l in lines if l.strip()}

    def loadable(self, name: str, args):
        """The arguments, each file a pass may have written swapped for the broker's copy of it, once its sha256 is
        found in the export register. Read without following a link, then copied, so the bytes checked are the bytes
        Resolve loads, whatever the pass does to its own file meanwhile."""
        sums = self.exported_sums()

        def swap(v):
            if isinstance(v, list):
                return [swap(x) for x in v]
            if isinstance(v, tuple):
                return tuple(swap(x) for x in v)
            if isinstance(v, dict):
                return {k: swap(x) for k, x in v.items()}
            if not isinstance(v, str) or "/" not in v:
                return v
            p = self.seat.real(v)
            # as named or as resolved: a link the pass put in its own folder is the pass's, wherever it points now
            if not any(self.seat.under(q, r) for q in (os.path.abspath(v), p) for r in self.pass_written):
                return p  # resolved, in a folder no pass writes, so nothing can be repointed before Resolve reads it
            try:
                fd = os.open(p, os.O_RDONLY | os.O_NOFOLLOW)
            except OSError:
                raise Refused(f"{name}: {v} is not a file") from None
            with os.fdopen(fd, "rb") as f:
                if not stat.S_ISREG(os.fstat(f.fileno()).st_mode):
                    raise Refused(f"{name}: {v} is not a file")
                data = f.read()
            digest = hashlib.sha256(data).hexdigest()
            if digest not in sums:
                raise Refused(f"{name}: {v} matches no export of Resolve's (its sha256 is not in the export register); a "
                              "file in a version folder or your fence loads only as Resolve exported it, never as a pass "
                              "wrote or changed it")
            copy = self.fresh("load") / os.path.basename(p)
            copy.write_bytes(data)
            self.note.setdefault("loaded", []).append({"file": p, "sha256": digest})
            return str(copy)
        return swap(args)

    def export(self, name: str, h: int, args: List):
        """Run an export with Resolve writing into the call's own folder, then record and copy out each file it wrote."""
        i = RESOLVE_EXPORTS[name]
        target = args[i] if len(args) > i else None
        if not (isinstance(target, str) and target.startswith("/")):
            raise Refused(f"{name}: name what it writes whole, from /, in a new version folder in your stage")
        out_dir, args = self.fresh("export"), list(args)
        folder = name == "ExportStills"
        args[i] = str(out_dir) if folder else str(out_dir / os.path.basename(target))
        out = self.objs[h](*args)
        if out:
            dest = self.seat.real(target if folder else os.path.dirname(target))
            self.note["exported"] = self.deliver(name, args, out_dir, dest)
        return out

    def deliver(self, name: str, args: List, out_dir: Path, dest: str) -> List[Dict]:
        seat, ctx = self.seat, self.ctx
        if not any(seat.under(dest, w) for w in ctx["fence"]["write"]) or any(seat.under(dest, f) for f in ctx["fence"]["frozen"]):
            raise Refused(f"{name}: {dest} is outside this pass's fence now")
        rows = []
        for d, _dirs, files in os.walk(out_dir):
            for f in sorted(files):
                src = Path(d) / f
                if src.is_symlink() or not src.is_file():
                    continue
                data = src.read_bytes()
                to = Path(dest) / src.relative_to(out_dir)
                to.parent.mkdir(parents=True, exist_ok=True)
                fd = os.open(to, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW, 0o644)
                with os.fdopen(fd, "wb") as fh:
                    fh.write(data)
                digest = hashlib.sha256(data).hexdigest()
                row = {"sha256": digest, "size": len(data), "file": str(to), "method": name,
                       **({"project": args[0]} if name == "ExportProject" else {}),
                       "pass": seat.pass_id_of(ctx["source"]) if ctx.get("source") else "",
                       "engagement": os.path.basename(ctx["engagement"]), "at": seat.now()}
                self.register.parent.mkdir(parents=True, exist_ok=True)
                with open(self.register, "a", encoding="utf-8") as reg:
                    reg.write(json.dumps(row) + "\n")
                rows.append({"file": str(to), "sha256": digest})
        return rows

    def serve(self, op: Dict):
        kind, h = op.get("op"), op.get("h")
        if h not in self.objs:
            raise Refused("an object this call never handed out")
        meta = self.meta[h]
        if kind == "getattr":
            name = op.get("name", "")
            if CONSTANT.fullmatch(name):
                v = getattr(self.objs[h], name)
                if not isinstance(v, (int, float, str, bool)) and v is not None:
                    raise Refused(f"{name} is not a constant")
                return v
            if not self.open(name):
                raise Refused(f"{name} is not open to a pass (Resolve's API file, less what the doorway refuses)")
            if not self.ours(meta["project"]) and name != "GetName":
                raise Refused(f"the project {meta['project']!r} is not this job's; its projects start {self.prefix!r}")
            v = getattr(self.objs[h], name)
            if v is None or isinstance(v, (bool, int, float, str, list, tuple, dict)):
                return self.encode(v, name, meta["project"])
            return self.keep(v, name, meta["project"], parent=h)  # a method, remembered with the object it belongs to
        if kind == "call":
            name = meta["name"]
            args = self.decode(op.get("args") or [])
            if not self.open(name):
                raise Refused(f"{name} is not open to a pass")
            if not self.ours(meta["project"]) and name != "GetName":
                raise Refused(f"the project {meta['project']!r} is not this job's")
            if name in RESOLVE_NAMED_PROJECT and (not args or not isinstance(args[0], str) or not args[0].startswith(self.prefix)):
                raise Refused(f"{name}: this job's projects are named {self.prefix}…")
            if name == "ImportProject" and (len(args) < 2 or not str(args[1]).startswith(self.prefix)):
                raise Refused(f"ImportProject: name the imported project {self.prefix}… (its second argument)")
            # A call on an object that belongs to no project acts on whichever is open: that one must be the job's.
            if meta["project"] is None and not name.startswith("Get") and name not in RESOLVE_ANY_PROJECT:
                open_now = self.current_project()
                if not self.ours(open_now):
                    raise Refused(f"{name} acts on the open project {open_now!r}, not this job's; load one named {self.prefix}…")
            self.check_paths(name, args)
            if name in RESOLVE_IMPORTS:
                args = self.loadable(name, args)
            if name == "RenderWithQuickExport" and not any("/" in s for s in self.strings(args)):
                raise Refused("RenderWithQuickExport: name its TargetDir, a new version folder in your stage")
            if name == "StartRendering" and meta.get("parent") is not None:
                jobs = self.objs[meta["parent"]].GetRenderJobList() or []
                self.check_paths("SetRenderSettings", [j.get("TargetDir", "") or "/(no target)" for j in jobs])
            out = self.export(name, h, args) if name in RESOLVE_EXPORTS else self.objs[h](*args)
            project = meta["project"]
            if name in ("CreateProject", "LoadProject", "GetCurrentProject") and out is not None \
                    and not isinstance(out, (bool, int, float, str)):
                project = out.GetName()  # the project a project's objects belong to, by its own name
            return self.encode(out, name, project)
        if kind == "bool":
            return bool(self.objs[h])
        if kind == "repr":
            return f"<{meta['name']} through the Motioncraft broker>"
        raise Refused(f"unknown op {kind!r}")

    def answer(self, op: Dict) -> Dict:
        t0 = time.time()
        self.note = {}
        try:
            out = {"ok": self.serve(op)}
        except Refused as e:
            out = {"refused": str(e)}
        except Exception as e:  # noqa: BLE001  Resolve's own errors go back to the script as errors
            out = {"error": f"{type(e).__name__}: {e}"}
        name = op.get("name") or self.meta.get(op.get("h"), {}).get("name")
        self.calls.append({"op": op.get("op"), "name": name, "args": op.get("args"), "ms": round((time.time() - t0) * 1000),
                           **self.note, **({k: out[k] for k in ("refused", "error") if k in out})})
        return out


SHIM = r'''"""The stand-in DaVinciResolveScript a Motioncraft pass's Resolve script imports: every object is a handle to the
launcher's broker, the only holder of the connection to Resolve (motioncraft/launcher/apps.py)."""
import json, os, socket

_sock = socket.socket(socket.AF_UNIX)
_sock.connect(os.environ["MOTIONCRAFT_RESOLVE_SOCKET"])
_file = _sock.makefile("rw", encoding="utf-8")


class Refused(Exception):
    """The broker refused this attribute or call; the message says why."""


def _ask(op):
    _file.write(json.dumps(op) + "\n")
    _file.flush()
    line = _file.readline()
    if not line:
        raise ConnectionError("the broker closed the connection")
    out = json.loads(line)
    if "refused" in out:
        raise Refused(out["refused"])
    if "error" in out:
        raise RuntimeError(out["error"])
    return _back(out["ok"])


def _back(v):
    if isinstance(v, list):
        return [_back(x) for x in v]
    if isinstance(v, dict):
        if "__h__" in v:
            return _Handle(v["__h__"])
        return {_back(k): _back(x) for k, x in v["__d__"]}
    return v


def _out(v):
    if isinstance(v, _Handle):
        return {"__h__": v._h}
    if isinstance(v, (list, tuple)):
        return [_out(x) for x in v]
    if isinstance(v, dict):
        return {"__d__": [[_out(k), _out(x)] for k, x in v.items()]}
    return v


class _Handle:
    __slots__ = ("_h",)

    def __init__(self, h):
        object.__setattr__(self, "_h", h)

    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(name)
        return _ask({"op": "getattr", "h": self._h, "name": name})

    def __call__(self, *args):
        return _ask({"op": "call", "h": self._h, "args": _out(list(args))})

    def __bool__(self):
        return _ask({"op": "bool", "h": self._h})

    def __repr__(self):
        return _ask({"op": "repr", "h": self._h})


def scriptapp(name):
    if name != "Resolve":
        raise Refused(f"scriptapp({name!r}): a pass reaches Resolve only, never Fusion")
    return _Handle(0)
'''


def cmd_broker(a) -> None:
    """The launcher's side of one Resolve call: connect to Resolve, then answer one script on the socket."""
    import socket as sk
    seat = _seat()
    ctx = seat.load(a.context)
    import DaVinciResolveScript as dvr  # noqa: E402  the real module, from Resolve's own variables
    root = dvr.scriptapp("Resolve")
    srv = sk.socket(sk.AF_UNIX)
    srv.bind(a.socket)
    os.chmod(a.socket, 0o600)
    srv.listen(1)
    Path(a.ready).write_text("running" if root else "no-resolve")
    if not root:
        return
    broker = Broker(root, ctx, resolve_api(), a.prefix, a.home, os.path.join(resolve_cache(), "exports.jsonl"))
    srv.settimeout(a.timeout)
    try:
        conn, _ = srv.accept()
    except OSError:
        conn = None
    if conn:
        conn.settimeout(a.timeout)
        f = conn.makefile("rw", encoding="utf-8")
        try:
            for line in f:
                try:
                    op = json.loads(line)
                except ValueError:
                    break
                f.write(json.dumps(broker.answer(op)) + "\n")
                f.flush()
        except OSError:
            pass
    Path(a.calls).write_text("".join(json.dumps(c) + "\n" for c in broker.calls), encoding="utf-8")


class Writes:
    """Every path written on the Mac while it runs (FSEvents, file-level), with no process named."""

    def __init__(self) -> None:
        import ctypes
        self.c = ctypes
        cs = ctypes.cdll.LoadLibrary("/System/Library/Frameworks/CoreServices.framework/CoreServices")
        cf = ctypes.cdll.LoadLibrary("/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation")
        lib = ctypes.cdll.LoadLibrary("/usr/lib/libSystem.B.dylib")
        cf.CFStringCreateWithCString.restype = ctypes.c_void_p
        cf.CFStringCreateWithCString.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint32]
        cf.CFArrayCreate.restype = ctypes.c_void_p
        cf.CFArrayCreate.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p), ctypes.c_long, ctypes.c_void_p]
        cb_t = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_char_p),
                                ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_uint64))
        cs.FSEventStreamCreate.restype = ctypes.c_void_p
        cs.FSEventStreamCreate.argtypes = [ctypes.c_void_p, cb_t, ctypes.c_void_p, ctypes.c_void_p,
                                           ctypes.c_uint64, ctypes.c_double, ctypes.c_uint32]
        for f in ("FSEventStreamStart", "FSEventStreamFlushSync", "FSEventStreamStop", "FSEventStreamInvalidate",
                  "FSEventStreamRelease"):
            getattr(cs, f).argtypes = [ctypes.c_void_p]
        cs.FSEventStreamSetDispatchQueue.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        lib.dispatch_queue_create.restype = ctypes.c_void_p
        lib.dispatch_queue_create.argtypes = [ctypes.c_char_p, ctypes.c_void_p]
        self.cs, self.paths, self.mu = cs, set(), threading.Lock()

        def seen(_s, _i, n, paths, _flags, _ids) -> None:
            with self.mu:
                for k in range(n):
                    self.paths.add(paths[k].decode("utf-8", "replace"))
        self.cb = cb_t(seen)
        root = (ctypes.c_void_p * 1)(cf.CFStringCreateWithCString(None, b"/", 0x08000100))
        since_now, file_events, no_defer = 0xFFFFFFFFFFFFFFFF, 0x10, 0x02
        self.stream = cs.FSEventStreamCreate(None, self.cb, None, cf.CFArrayCreate(None, root, 1, None),
                                             since_now, 0.05, file_events | no_defer)
        cs.FSEventStreamSetDispatchQueue(self.stream, lib.dispatch_queue_create(b"motioncraft.apps.writes", None))
        if not cs.FSEventStreamStart(self.stream):
            raise OSError("FSEvents would not start")

    def stop(self) -> List[str]:
        time.sleep(0.3)  # the stream's latency, so the last writes land
        for f in ("FSEventStreamFlushSync", "FSEventStreamStop", "FSEventStreamInvalidate", "FSEventStreamRelease"):
            getattr(self.cs, f)(self.stream)
        with self.mu:
            return sorted(self.paths)


def resolve_own() -> List[str]:
    """Where Resolve keeps its own state: its support folders, preferences and caches, and its media storage
    (its default `~/DaVinci Resolve Media`, and `~/Movies/Davinci-Resolve`, set on these Macs)."""
    home, cache = os.path.expanduser("~"), user_cache()
    return [f"{home}/Library/Application Support/Blackmagic Design", "/Library/Application Support/Blackmagic Design",
            f"{home}/Library/Preferences/com.blackmagic-design", f"{home}/Library/Caches/com.blackmagic-design",
            f"{home}/Library/Saved Application State/com.blackmagic-design", f"{home}/Movies/CacheClip",
            f"{home}/Library/Preferences/Blackmagic Design", f"{home}/DaVinci Resolve Media",
            f"{home}/Movies/Davinci-Resolve"] + \
        ([os.path.join(seat_real(cache), "com.blackmagic-design")] if cache else [])


def other_programs() -> List[str]:
    """Places macOS and this Mac's other programs write all day (Spotlight, the scheduler, app caches): listed apart,
    since FSEvents names no process and a Resolve call cannot write there by any route the broker opens."""
    home = os.path.expanduser("~")
    return ["/private/var/db/", "/private/var/protected/", "/System/", "/Library/Caches/", "/Library/Tailscale/",
            f"{home}/Library/Metadata/",
            f"{home}/Library/Caches/com.apple.", f"{home}/Library/Preferences/com.apple.",
            f"{home}/Library/Application Support/Claude/", f"{home}/Library/Application Support/Codex/",
            f"{home}/Library/Biome/", f"{home}/Library/Logs/",
            f"{home}/Library/Application Support/com.apple.", f"{home}/Library/Group Containers/"]


def seat_real(p: str) -> str:
    return os.path.realpath(p)


def sort_writes(ctx: Dict, paths: List[str], mine: List[str]) -> Dict[str, List[str]]:
    seat = _seat()
    out: Dict[str, List[str]] = {"fence": [], "frozen": [], "resolve_own": [], "launcher": [], "other_programs": [],
                                 "outside": []}
    temp_items = re.compile(r"^/private/var/folders/[^/]+/[^/]+/T/TemporaryItems/")
    resolve_temp = re.compile(r"^/private/var/folders/[^/]+/[^/]+/T/DaVinci Resolve\.")
    for p in paths:
        rp = seat.real(p) if os.path.lexists(p) else p
        if any(seat.under(rp, f) for f in ctx["fence"]["frozen"]):
            out["frozen"].append(p)
        elif any(seat.under(rp, w) for w in ctx["fence"]["write"]):
            out["fence"].append(p)
        elif any(seat.under(rp, m) for m in mine) or re.match(r"^/private/tmp/mc-[^/]+(/s)?$", rp):
            out["launcher"].append(p)
        elif any(rp.startswith(r) for r in resolve_own()) or resolve_temp.match(rp):
            out["resolve_own"].append(p)
        elif any(rp.startswith(r) for r in other_programs()) or temp_items.match(rp):
            out["other_programs"].append(p)
        else:
            out["outside"].append(p)
    return out


def krita_swap(home: Path) -> None:
    """Point Krita's tile swap file into the call's own home. Left to itself, Krita swaps into the folder its first
    start named, or falls back to the Mac's own temporary folder; the lock refuses both, and a save then waits for
    ever (found 2026-10-20)."""
    swap = Path(home) / "swap"
    swap.mkdir(exist_ok=True)
    rc = Path(home) / "Library" / "Preferences" / "kritarunnerrc"
    rc.parent.mkdir(parents=True, exist_ok=True)
    kept = [l for l in rc.read_text(encoding="utf-8").splitlines() if not l.startswith("swaplocation=")] if rc.exists() else []
    # a key before the first [group] is in Krita's top-level settings, where it reads this one
    rc.write_text("\n".join([f"swaplocation={os.path.realpath(swap)}"] + kept) + "\n", encoding="utf-8")


def krita_finished(log: Path) -> bool:
    """Whether the wrapper's closing line is in a Krita call's log, saying the script ran to its end."""
    try:
        return any(l.startswith(KRITA_DONE) for l in Path(log).read_text(encoding="utf-8", errors="replace").splitlines())
    except OSError:
        return False


def krita_font_lines(log: Path):
    """The families the wrapper registered, and each refusal of text in a font it did not, from a Krita call's log."""
    registered: Optional[List[str]] = None
    faults: List[str] = []
    try:
        lines = Path(log).read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return [], faults
    for l in lines:
        if l.startswith(KRITA_FONT_FAULT + " "):
            faults.append(l[len(KRITA_FONT_FAULT) + 1:])
        elif l.startswith(KRITA_FONTS + " ") and registered is None:  # the wrapper's, printed before the script ran
            try:
                registered = json.loads(l[len(KRITA_FONTS) + 1:])
            except ValueError:
                registered = []
    return registered or [], faults


def tree(roots: List[str]) -> Dict[str, tuple]:
    """Every file under the fence's folders, by size and change time."""
    seen: Dict[str, tuple] = {}
    for r in roots:
        for d, _dirs, files in os.walk(r):
            for f in files:
                p = os.path.join(d, f)
                try:
                    st = os.lstat(p)
                except OSError:
                    continue
                seen[p] = (st.st_size, st.st_mtime_ns)
    return seen


class AppServer:
    """Runs on the launcher's side of one pass: picks up its requests, one at a time, until the pass ends."""

    def __init__(self, ctx: Dict, deadline: float) -> None:
        seat = _seat()
        self.seat, self.ctx, self.deadline = seat, ctx, deadline
        self.allowed = list(ctx["toolbelt"].get("apps") or []) + ["higgsfield"] * bool(ctx["toolbelt"].get("higgsfield"))
        pid = seat.pass_id_of(ctx["source"])
        logs = Path(ctx["engagement"]) / "trace" / "logs"
        self.results = logs / f"{pid}.apps"
        self.log = logs / f"{pid}.apps.jsonl"
        self.results.mkdir(exist_ok=False)
        req = Path(ctx["scratch"]) / "apps"
        req.mkdir(mode=0o700, exist_ok=False)
        # Held open from here: the folder is the seat's to write, so a link put in its place later changes nothing.
        self.fd = os.open(req, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        self.requests = req
        self.seen: set = set()
        self.calls: List[Dict] = []
        self.job: Optional[subprocess.Popen] = None
        self.halt = threading.Event()
        self.thread = threading.Thread(target=self.loop, daemon=True)

    def env(self) -> Dict[str, str]:
        """What the pass's environment carries so `ask` can find both folders."""
        return {"MOTIONCRAFT_APPS_REQUESTS": str(self.requests), "MOTIONCRAFT_APPS_RESULTS": str(self.results)}

    def start(self) -> None:
        self.thread.start()

    def stop(self) -> Dict:
        self.halt.set()
        job = self.job
        if job and job.poll() is None:
            self.seat.kill_group(job)
        self.thread.join(timeout=30)
        os.close(self.fd)
        flagged = [c["id"] for c in self.calls if c.get("written", {}).get("frozen") or c.get("written", {}).get("outside")]
        return {"calls": len(self.calls), "log": os.path.relpath(self.log, self.ctx["engagement"]),
                "refused": [c["id"] for c in self.calls if c.get("refused")], "writes_to_check": flagged}

    def loop(self) -> None:
        while not self.halt.is_set():
            try:
                names = sorted(n for n in os.listdir(self.fd) if REQUEST.fullmatch(n) and n not in self.seen)
            except OSError:
                names = []
            for n in names:
                if self.halt.is_set():
                    break
                self.seen.add(n)
                self.handle(n)
            self.halt.wait(POLL_S)

    def read_request(self, name: str) -> Dict:
        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=self.fd)
        with os.fdopen(fd, "rb") as f:
            if not stat.S_ISREG(os.fstat(f.fileno()).st_mode):
                raise ValueError("the request is not a plain file")
            data = f.read(MAX_REQUEST_BYTES + 1)
        if len(data) > MAX_REQUEST_BYTES:
            raise ValueError("the request is too large")
        req = json.loads(data)
        if not isinstance(req, dict) or req.get("id") != name[:-5]:
            raise ValueError("the request's id is not its file name")
        return req

    def check(self, req: Dict) -> Dict:
        """The request held to the pass's fence, or a ValueError naming why not."""
        seat, ctx = self.seat, self.ctx
        app = req.get("app")
        if app not in self.allowed:
            raise ValueError(f"{ctx['seat']}'s pass may not run {app}; its seat lists {', '.join(self.allowed) or 'no app'}")
        if app == "higgsfield":
            return self.check_higgsfield(req)
        if app == "hyperframes":
            return self.check_hyperframes(req)
        if "render" in req:
            return self.check_render(req)
        script = seat.real(str(req.get("script") or ""))
        stage = os.path.join(ctx["media_project"], seat.STAGE_DIRS[ctx["seat"]])
        writable = seat.under(script, ctx["scratch"]) or (
            seat.under(script, stage) and not any(seat.under(script, f) for f in ctx["fence"]["frozen"]))
        if not script.endswith(".py") or not os.path.isfile(script) or not writable:
            raise ValueError("--script is a .py file the pass wrote, in its scratch folder or a new version folder in its stage")
        with open(script, "rb") as f:
            body = f.read(MAX_SCRIPT_BYTES + 1)
        if len(body) > MAX_SCRIPT_BYTES:
            raise ValueError(f"the script is over {MAX_SCRIPT_BYTES} bytes")
        args = req.get("args") or []
        if (not isinstance(args, list) or len(args) > MAX_ARGS
                or any(not isinstance(x, str) or len(x) > MAX_ARG or "\0" in x for x in args)):
            raise ValueError(f"args are at most {MAX_ARGS} strings of at most {MAX_ARG} characters")
        blend = ""
        if req.get("blend"):
            blend = seat.real(str(req["blend"]))
            if app != "blender" or not blend.endswith(".blend") or not os.path.isfile(blend) \
                    or not seat.under(blend, ctx["media_project"]):
                raise ValueError("--blend is a .blend file in the media project, for blender")
        fonts: List[str] = []
        if req.get("fonts"):
            if app != "krita":
                raise ValueError("--fonts is Krita's: the version's font folder, registered before the script runs")
            fonts = self.check_fonts(str(req["fonts"]))
        timeout = req.get("timeout") or DEFAULT_TIMEOUT_S
        if not isinstance(timeout, int) or not 1 <= timeout <= MAX_TIMEOUT_S:
            raise ValueError(f"--timeout is whole seconds, 1 to {MAX_TIMEOUT_S}")
        return {"app": app, "script": script, "body": body, "args": args, "blend": blend, "timeout": timeout,
                "fonts": fonts, "fonts_from": seat.real(str(req["fonts"])) if fonts else ""}

    def check_fonts(self, folder: str) -> List[str]:
        """`--fonts` held to the media project: the font files in that folder and below, each a plain file there."""
        seat, project = self.seat, self.ctx["media_project"]
        d = seat.real(folder)
        if not os.path.isdir(d) or not seat.under(d, project):
            raise ValueError("--fonts is a folder in the media project: the version's assets/fonts/")
        found = []
        for top, dirs, files in os.walk(d):
            dirs.sort()
            for f in sorted(files):
                if not f.lower().endswith(FONT_SUFFIXES):
                    continue
                p = os.path.join(top, f)
                if os.path.islink(p) or not seat.under(seat.real(p), project) or not os.path.isfile(p):
                    raise ValueError(f"--fonts: {p} is a link or reaches outside the media project; copy the file in")
                if os.path.getsize(p) > MAX_FONT_BYTES:
                    raise ValueError(f"--fonts: {p} is over {MAX_FONT_BYTES} bytes")
                found.append(seat.real(p))
        if not found:
            raise ValueError(f"--fonts names no font files ({', '.join(FONT_SUFFIXES)})")
        if len(found) > MAX_FONTS:
            raise ValueError(f"--fonts names over {MAX_FONTS} font files")
        return found

    def check_higgsfield(self, req: Dict) -> Dict:
        """A Higgsfield request's shape: an entry and a file, or a status. The doorway holds the rest of the terms."""
        h = req.get("higgsfield")
        if req.get("script") or req.get("args") or req.get("render") or not isinstance(h, dict):
            raise ValueError("a Higgsfield request is an entry and a file, or a status, and no script")
        timeout = req.get("timeout") or DEFAULT_TIMEOUT_S
        if not isinstance(timeout, int) or not 1 <= timeout <= MAX_TIMEOUT_S:
            raise ValueError(f"--timeout is whole seconds, 1 to {MAX_TIMEOUT_S}")
        if h == {"status": True}:
            return {"app": "higgsfield", "argv": ["status"], "timeout": timeout}
        if set(h) == {"settle", "out"}:
            job, out = h.get("settle"), h.get("out")
            if not isinstance(job, str) or not HIGGSFIELD_JOB.fullmatch(job) \
                    or not isinstance(out, str) or not out.startswith("/") or "\0" in out or len(out) > MAX_ARG:
                raise ValueError("ask higgsfield --settle <a Higgsfield job id> --out <a file in a new version folder>")
            return {"app": "higgsfield", "argv": ["settle", "--job", job, "--out", out], "timeout": timeout}
        entry, out = h.get("entry"), h.get("out")
        if set(h) != {"entry", "out"} or not isinstance(entry, str) or not HIGGSFIELD_ENTRY.fullmatch(entry) \
                or not isinstance(out, str) or not out.startswith("/") or "\0" in out or len(out) > MAX_ARG:
            raise ValueError("ask higgsfield --entry <IMn or VIn> --out <a file in a new version folder>")
        return {"app": "higgsfield", "argv": ["take", "--entry", entry, "--out", out], "timeout": timeout}

    def check_render(self, req: Dict) -> Dict:
        """A render request held to the pass's fence: a scene, a folder, frames and an engine, and no code of the seat's."""
        seat, ctx = self.seat, self.ctx
        r = req.get("render")
        if req.get("app") != "blender" or not isinstance(r, dict) or req.get("script") or req.get("args") \
                or set(r) - {"blend", "out", "frames", "engine", "device"}:
            raise ValueError("a render request is Blender's: a scene, a folder, frames, an engine and a device, with no "
                             "script or arguments")
        blend = seat.real(str(r.get("blend") or ""))
        if not blend.endswith(".blend") or not os.path.isfile(blend) or not seat.under(blend, ctx["media_project"]):
            raise ValueError("--blend is a .blend file in the media project, for blender")
        name = r.get("engine") or "cycles"
        if name not in RENDER_ENGINES:
            raise ValueError(f"--engine is one of {', '.join(RENDER_ENGINES)}")
        out = seat.real(str(r.get("out") or ""))
        stage = os.path.join(ctx["media_project"], seat.STAGE_DIRS[ctx["seat"]])
        new_version = seat.under(out, stage) and out != stage and not any(seat.under(out, f) for f in ctx["fence"]["frozen"])
        if name == "cycles" and not (seat.under(out, ctx["scratch"]) or new_version):
            raise ValueError("--out is a folder in the scratch folder or a new version folder in the seat's stage")
        if name != "cycles" and not seat.under(out, ctx["scratch"]):
            raise ValueError(f"{name} renders are previews: --out is a folder in the scratch folder; a kept render is cycles")
        device = r.get("device") or "cpu"
        if device not in RENDER_DEVICES:
            raise ValueError(f"--device is one of {', '.join(RENDER_DEVICES)}")
        if device == "gpu" and name != "cycles":
            raise ValueError("--device gpu is cycles on the graphics chip (Metal); eevee and workbench take no device")
        if device == "gpu" and not seat.under(out, ctx["scratch"]) and brief_render_device(ctx["engagement"]) != "gpu":
            raise ValueError("a GPU render is a preview in the scratch folder until Sean adopts it for this film: the "
                             "brief's header then says render_device: gpu, and only then is it kept in a version folder")
        frames = r.get("frames")
        if (not isinstance(frames, list) or len(frames) != 2 or not all(isinstance(f, int) and f >= 0 for f in frames)
                or not 1 <= frames[1] - frames[0] + 1 <= MAX_RENDER_FRAMES):
            raise ValueError(f"--frames is S-E, whole frames from 0, at most {MAX_RENDER_FRAMES} of them")
        timeout = req.get("timeout") or DEFAULT_TIMEOUT_S
        if not isinstance(timeout, int) or not 1 <= timeout <= MAX_TIMEOUT_S:
            raise ValueError(f"--timeout is whole seconds, 1 to {MAX_TIMEOUT_S}")
        return {"app": "blender", "render": True, "script": "launcher: RENDER_SCRIPT", "body": RENDER_SCRIPT.encode(),
                "args": [out, str(frames[0]), str(frames[1]), RENDER_ENGINES[name], RENDER_DEVICES[device]],
                "device": device, "blend": blend, "timeout": timeout}

    def check_hyperframes(self, req: Dict) -> Dict:
        """A HyperFrames request held to the pass's fence: a project the pass wrote and, for a render, a new folder for its
        frames and a frame rate. The command line is the launcher's; the request names no flag and no code."""
        seat, ctx = self.seat, self.ctx
        h = req.get("hyperframes")
        if req.get("script") or req.get("args") or req.get("render") or req.get("blend") or not isinstance(h, dict) \
                or h.get("mode") not in ("render", "check") \
                or set(h) != ({"mode", "project", "out", "fps"} if h.get("mode") == "render" else {"mode", "project"}):
            raise ValueError("a HyperFrames request is a project to render (with a folder and a frame rate) or to check, "
                             "and no script")
        stage = os.path.join(ctx["media_project"], seat.STAGE_DIRS[ctx["seat"]])
        frozen = ctx["fence"]["frozen"]

        def new_in(p: str) -> bool:  # in the scratch folder, or in a new version folder in the seat's stage
            return seat.under(p, ctx["scratch"]) or (
                seat.under(p, stage) and p != stage and not any(seat.under(p, f) for f in frozen))

        project = seat.real(str(h.get("project") or ""))
        if not os.path.isfile(os.path.join(project, "index.html")) or not new_in(project):
            raise ValueError("--project is a folder holding index.html, in the scratch folder or a new version folder in "
                             "the seat's stage")
        timeout = req.get("timeout") or DEFAULT_TIMEOUT_S
        if not isinstance(timeout, int) or not 1 <= timeout <= MAX_TIMEOUT_S:
            raise ValueError(f"--timeout is whole seconds, 1 to {MAX_TIMEOUT_S}")
        c = {"app": "hyperframes", "mode": h["mode"], "project": project, "timeout": timeout,
             "script": f"launcher: hyperframes {h['mode']}"}
        if h["mode"] == "check":
            c["argv"] = ["check", project]
            return c
        out = seat.real(str(h.get("out") or ""))
        if not new_in(out) or os.path.lexists(out) or not os.path.isdir(os.path.dirname(out)) \
                or seat.under(out, project) or seat.under(project, out):
            raise ValueError("--out is a folder not made yet, in the scratch folder or a new version folder in the seat's "
                             "stage, beside the project and not inside it")
        if h.get("fps") not in HF_FPS:
            raise ValueError(f"--fps is one of {', '.join(map(str, HF_FPS))}")
        c.update(out=out, fps=h["fps"], argv=["render", project, *HF_RENDER_FLAGS, "--fps", str(h["fps"]), "-o", out])
        return c

    def write_new(self, name: str, data: bytes) -> Path:
        p = self.results / name
        with open(p, "xb") as f:
            f.write(data)
        return p

    def handle(self, name: str) -> None:
        rid = name[:-5]
        entry: Dict = {"id": rid, "pass": self.seat.pass_id_of(self.ctx["source"]), "seat": self.ctx["seat"],
                       "asked": self.seat.now()}
        try:
            req = self.read_request(name)
            entry["request"] = {k: req.get(k) for k in ("app", "script", "args", "blend", "render", "fonts", "higgsfield",
                                                        "hyperframes", "timeout") if k in req}
            c = self.check(req)
        except (ValueError, OSError) as e:
            entry["refused"] = str(e)
            self.finish(entry, {"id": rid, "ok": False, "refused": str(e)})
            return
        if c.get("render"):
            entry["device"] = c["device"]
        try:
            self.run(rid, c, entry)
        except Exception as e:  # noqa: BLE001  any failure is the seat's to read, never a dead launcher
            entry["error"] = f"{type(e).__name__}: {e}"
        written = entry.get("written", {})
        res = {"id": rid, "ok": entry.get("exit_code") == 0 and not entry.get("error") and not written.get("frozen"),
               "exit_code": entry.get("exit_code"), "log": entry.get("log"), "error": entry.get("error"),
               "new_or_changed_in_fence": written.get("fence", []), "frozen_touched": written.get("frozen", []),
               # the check record copies these: written somewhere else on the Mac during the call, by Resolve or another program
               "outside_the_fence": written.get("outside", [])[:500],
               "also_written": {k: len(written.get(k, [])) for k in ("resolve_own", "other_programs", "launcher")}}
        if c["app"] == "resolve":
            res["resolve"] = entry.get("resolve")
        if c["app"] == "krita":
            res["fonts"] = entry.get("fonts")
        if c["app"] == "hyperframes":
            res["hyperframes"] = entry.get("hyperframes")
        if c.get("render"):
            res["device"] = c["device"]
        self.finish(entry, res)

    def run(self, rid: str, c: Dict, entry: Dict) -> None:
        if c["app"] == "higgsfield":
            return self.run_higgsfield(rid, c, entry)
        seat, ctx, paths = self.seat, self.ctx, app_paths()
        if c["app"] == "hyperframes":  # no code of the seat's: the record keeps the launcher's command line
            argv = [paths["node"], paths["hyperframes"], *c["argv"]]
            copy = self.write_new(f"{rid}.argv.json", (json.dumps(argv, indent=1) + "\n").encode())
        else:
            copy = self.write_new(f"{rid}.py", c["body"])
        env = {k: os.environ[k] for k in ("HOME", "USER", "LOGNAME", "LANG", "LC_ALL") if k in os.environ}
        env.update(PATH="/usr/bin:/bin:/usr/sbin:/sbin", TMPDIR=ctx["scratch"])
        timeout = max(1, min(c["timeout"], self.deadline - time.time()))
        broker, sock, home, rhome, ports = None, "", "", "", []
        if c["app"] == "hyperframes":
            home = os.path.join(hyperframes_cache(), "calls", rid)
            os.makedirs(os.path.join(home, "claims"), mode=0o700)
            ports = free_ports()
            pins = self.write_new(f"{rid}.pins.cjs", HF_PINS.encode())
            env.update(HF_ENV, HOME=home, HYPERFRAMES_BROWSER_PATH=paths["chrome"], NODE_OPTIONS=f"--require {pins}",
                       MOTIONCRAFT_HF_PORTS=",".join(map(str, ports)), MOTIONCRAFT_HF_CLAIMS=os.path.join(home, "claims"))
            for tool in ("ffmpeg", "ffprobe"):  # for a composition's video sources; a PNG sequence needs no encoder
                found = shutil.which(tool, path=os.pathsep.join([os.environ.get("PATH", ""), "/opt/homebrew/bin"]))
                if found:
                    env[f"HYPERFRAMES_{tool.upper()}_PATH"] = found
            entry["hyperframes"] = {"mode": c["mode"], "project": c["project"], "ports": ports,
                                    **({"out": c["out"], "fps": c["fps"]} if c["mode"] == "render" else {})}
        elif c["app"] == "blender":
            Path(blender_cache()).mkdir(parents=True, exist_ok=True)
            env["XDG_CACHE_HOME"] = blender_cache()
            # a render request opens its scene with auto-run off, before the file loads: no code the file carries runs
            argv = [paths["blender"], "-b", "--factory-startup", *(["--disable-autoexec"] if c.get("render") else []),
                    *([c["blend"]] if c["blend"] else []), "--python-exit-code", "1", "--python", str(copy), "--", *c["args"]]
        elif c["app"] == "krita":
            home = self.krita_home(rid, env, entry)
            entry["fonts"], fonts = self.krita_fonts(home, c)
            env.update(self.krita_env(rid, home, env), MOTIONCRAFT_KRITA_SCRIPT=str(copy),
                       MOTIONCRAFT_KRITA_ARGS=json.dumps(c["args"]), MOTIONCRAFT_KRITA_FONTS=json.dumps(fonts),
                       MOTIONCRAFT_KRITA_FONTCONFIG=str(Path(paths["krita"]).parents[1] / "Frameworks" / "libfontconfig.1.dylib"))
            argv = [paths["krita"], "-s", KRITA_MODULE, "-f", "main"]
        else:
            # the broker's own folder for this call, where Resolve writes its exports and reads checked copies
            rhome = os.path.join(resolve_cache(), "calls", rid)
            os.makedirs(rhome, mode=0o700)
            broker, sock = self.start_broker(rid, env, timeout, rhome)
            shim = self.results / f"{rid}.shim"
            shim.mkdir()
            (shim / "DaVinciResolveScript.py").write_text(SHIM, encoding="utf-8")
            # no Resolve variables and no Resolve module: only the stand-in, and the broker's socket
            env.update(PYTHONPATH=str(shim), MOTIONCRAFT_RESOLVE_SOCKET=sock)
            argv = [paths["python"], "-s", "-B", str(copy), *c["args"]]
        rules = lock(ctx, c["app"], sock, render=bool(c.get("render")), home=home, ports=ports)
        sbf = self.write_new(f"{rid}.sb", rules.encode())
        log = self.results / f"{rid}.log"
        before = tree(ctx["fence"]["write"])
        writes = Writes() if c["app"] == "resolve" else None
        entry.update(started=seat.now(), argv=["sandbox-exec", "-f", str(sbf), *argv],
                     script={"from": c["script"], "copy": str(copy), "sha256": seat.sha256(copy)},
                     lock={"path": str(sbf), "sha256": seat.sha256(sbf)}, log=str(log))
        t0 = time.time()
        try:
            with open(log, "xb") as logf:
                self.job = subprocess.Popen(["/usr/bin/sandbox-exec", "-f", str(sbf), *argv], cwd=ctx["scratch"],
                                            env=env, stdin=subprocess.DEVNULL, stdout=logf, stderr=subprocess.STDOUT,
                                            start_new_session=True)
                try:
                    code = self.job.wait(timeout=timeout)
                except subprocess.TimeoutExpired:
                    seat.kill_group(self.job)
                    code = self.job.wait()
                    entry["stopped"] = f"timeout after {round(timeout)} s"
                self.job = None
        finally:
            if broker:
                self.stop_broker(broker, sock)
            for d in (home, rhome):
                if d:
                    shutil.rmtree(d, ignore_errors=True)  # the call's own folder: nothing in it outlives the call
        entry.update(completed=seat.now(), wall_clock_s=round(time.time() - t0), exit_code=code)
        if c["app"] == "krita" and code == 0 and not krita_finished(log):
            entry["error"] = ("Krita ended without the script finishing (kritarunner exits 0 when a script fails to "
                              "load); see the log")
        if c["app"] == "hyperframes" and c["mode"] == "render":
            frames = sorted(f for f in os.listdir(c["out"]) if f.endswith(".png")) if os.path.isdir(c["out"]) else []
            entry["hyperframes"].update(frames=len(frames), first=frames[0] if frames else "", last=frames[-1] if frames else "")
            if code == 0 and not frames:
                entry["error"] = "HyperFrames ended without writing a frame; see the log"
        if c["app"] == "krita":
            registered, faults = krita_font_lines(log)
            entry["fonts"]["families"] = registered
            if faults:
                entry["error"] = "Krita would set text in a font this call did not register: " + " | ".join(faults)
        after = tree(ctx["fence"]["write"])
        changed = sorted(p for p, v in after.items() if before.get(p) != v and not seat.under(p, str(self.requests)))
        if writes is not None:
            calls = self.results / f"{rid}.calls.jsonl"
            rows = [json.loads(l) for l in calls.read_text(encoding="utf-8").splitlines()] if calls.exists() else []
            entry["broker"] = {"calls": len(rows), "log": str(calls), "refused": [r for r in rows if "refused" in r]}
            entry["resolve"] = resolve_state(self.resolve_env(env), paths["python"])
            seen = writes.stop()
            entry["written"] = sort_writes(ctx, seen, [str(self.results), str(self.log), str(self.requests), rhome,
                                                       os.path.join(resolve_cache(), "exports.jsonl")])
            entry["written"]["fence"] = sorted(set(entry["written"]["fence"]) | set(changed))
            targets = entry["resolve"].get("render_targets") or []
            entry["resolve"]["render_targets_outside"] = [t for t in targets if t and not any(
                seat.under(seat.real(t), w) for w in ctx["fence"]["write"])]
        else:
            entry["written"] = {"fence": changed, "frozen": [p for p in changed if any(
                seat.under(p, f) for f in ctx["fence"]["frozen"])], "outside": []}

    def run_higgsfield(self, rid: str, c: Dict, entry: Dict) -> None:
        """The launcher's own Higgsfield doorway, for this pass's context, outside every lock: it needs the network and
        the sign-in no pass reads. It is the launcher's code, never the seat's, so it runs as the launcher does."""
        seat, ctx = self.seat, self.ctx
        argv = [sys.executable, "-B", str(HERE / "higgsfield.py"), c["argv"][0], "--context", ctx["source"], *c["argv"][1:]]
        env = {k: v for k, v in os.environ.items() if not k.startswith("MOTIONCRAFT_APPS_")}
        timeout = max(1, min(c["timeout"], self.deadline - time.time()))
        log = self.results / f"{rid}.log"
        before = tree(ctx["fence"]["write"])
        entry.update(started=seat.now(), argv=argv, log=str(log))
        t0 = time.time()
        with open(log, "xb") as logf:
            self.job = subprocess.Popen(argv, cwd=ctx["scratch"], env=env, stdin=subprocess.DEVNULL, stdout=logf,
                                        stderr=subprocess.STDOUT, start_new_session=True)
            try:
                code = self.job.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                seat.kill_group(self.job)
                code = self.job.wait()
                entry["stopped"] = f"timeout after {round(timeout)} s"
            self.job = None
        entry.update(completed=seat.now(), wall_clock_s=round(time.time() - t0), exit_code=code)
        after = tree(ctx["fence"]["write"])
        changed = sorted(p for p, v in after.items() if before.get(p) != v and not seat.under(p, str(self.requests)))
        entry["written"] = {"fence": changed, "frozen": [p for p in changed if any(
            seat.under(p, f) for f in ctx["fence"]["frozen"])], "outside": []}

    def krita_env(self, rid: str, home: str, env: Dict[str, str]) -> Dict[str, str]:
        """Krita's environment for one call: its own home, no screen, and the launcher's wrapper on its Python path."""
        base = self.results / f"{rid}.krita"
        site = base / "lib" / "python" / "site-packages"
        site.mkdir(parents=True)
        (site / f"{KRITA_MODULE}.py").write_text(KRITA_WRAPPER, encoding="utf-8")
        # HOME for Qt and fontconfig, CFFIXED_USER_HOME for macOS's own folder lookups (Library/...), which ignore HOME
        return {"HOME": home, "CFFIXED_USER_HOME": home, "PYTHONUSERBASE": str(base), "QT_QPA_PLATFORM": "offscreen",
                "LANG": "en_US.UTF-8", "LC_ALL": "en_US.UTF-8"}

    def krita_fonts(self, home: str, c: Dict):
        """Copy the call's fonts into its own home, so what Krita registers is what the record names by checksum."""
        own = Path(home) / "motioncraft-fonts"
        own.mkdir()
        files, copies = [], []
        for i, f in enumerate(c.get("fonts") or []):
            p = own / f"{i:02d}-{os.path.basename(f)}"
            shutil.copyfile(f, p)
            files.append({"path": f, "sha256": self.seat.sha256(p)})
            copies.append(str(p))
        return {"from": c.get("fonts_from", ""), "files": files}, copies

    def krita_home(self, rid: str, env: Dict[str, str], entry: Dict) -> str:
        """A fresh clone of this Krita version's template home, built first if this machine has none."""
        seat, paths = self.seat, app_paths()
        root = Path(krita_cache())
        template = root / f"template-{krita_version(paths['krita'])}"
        if not template.is_dir():
            entry["krita_template"] = self.build_krita_template(rid, template, env)
        home = root / "calls" / rid
        home.parent.mkdir(parents=True, exist_ok=True)
        # APFS clones: the 110 MB of resources cost nothing until Krita changes a file
        subprocess.run(["/bin/cp", "-c", "-R", str(template), str(home)], check=True, capture_output=True)
        krita_swap(home)
        return seat.real(str(home))

    def build_krita_template(self, rid: str, template: Path, env: Dict[str, str]) -> Dict:
        """Start Krita once in an empty home, under the call's lock and with no script, so it writes its first-run
        resources there; the result becomes this version's template. No code of a seat's runs in it."""
        build = template.with_name(f".{template.name}.{rid}")
        build.mkdir(parents=True)
        krita_swap(build)
        tenv = dict(env, **self.krita_env(f"{rid}.template", self.seat.real(str(build)), env), MOTIONCRAFT_KRITA_SCRIPT="")
        sbf = self.write_new(f"{rid}.template.sb", lock(self.ctx, "krita", home=str(build)).encode())
        log = self.results / f"{rid}.template.log"
        try:
            with open(log, "xb") as logf:
                r = subprocess.run(["/usr/bin/sandbox-exec", "-f", str(sbf), app_paths()["krita"], "-s", KRITA_MODULE,
                                    "-f", "main"], cwd=self.ctx["scratch"], env=tenv, stdin=subprocess.DEVNULL, stdout=logf,
                                   stderr=subprocess.STDOUT, start_new_session=True,
                                   timeout=max(1, min(600, self.deadline - time.time())))
            if r.returncode != 0 or not krita_finished(log):
                raise RuntimeError(f"Krita's first start for its template failed (exit {r.returncode}); see {log}")
            if not template.is_dir():  # another job on this machine may have built it meanwhile; theirs stands
                os.rename(build, template)
        finally:
            shutil.rmtree(build, ignore_errors=True)
        return {"built": str(template), "log": str(log), "lock": str(sbf)}

    def resolve_env(self, env: Dict[str, str]) -> Dict[str, str]:
        """The broker's environment, outside the lock: Resolve's own scripting variables (the allowlist's [env])."""
        out = {k: v for k, v in env.items() if k not in ("PYTHONPATH", "MOTIONCRAFT_RESOLVE_SOCKET")}
        out.update({k: v for k, v in self.seat.app_env()[1].items() if k.startswith("RESOLVE_") or k == "PYTHONPATH"})
        return out

    def start_broker(self, rid: str, env: Dict[str, str], timeout: float, home: str):
        """Start the broker outside the lock and wait until it holds Resolve; a short socket path (macOS caps it at 104)."""
        sockdir = tempfile.mkdtemp(prefix="mc-", dir="/private/tmp")
        sock = os.path.join(sockdir, "s")
        ready = self.results / f"{rid}.broker-ready"
        blog = open(self.results / f"{rid}.broker.log", "xb")
        proc = subprocess.Popen([app_paths()["python"], "-s", "-B", str(Path(__file__).resolve()), "broker",
                                 "--context", self.ctx["source"], "--socket", sock, "--ready", str(ready),
                                 "--calls", str(self.results / f"{rid}.calls.jsonl"), "--timeout", str(round(timeout)),
                                 "--prefix", os.path.basename(self.ctx["media_project"]), "--home", home],
                                env=self.resolve_env(env), stdin=subprocess.DEVNULL, stdout=blog, stderr=subprocess.STDOUT,
                                start_new_session=True)
        blog.close()
        end = time.time() + 30
        while not ready.exists() and proc.poll() is None and time.time() < end:
            time.sleep(0.1)
        state = ready.read_text() if ready.exists() else ""
        if state != "running":
            self.stop_broker(proc, sock)
            raise RuntimeError("Resolve is not running on this machine; the coordinator starts it, then ask again"
                               if state == "no-resolve" else "the Resolve broker did not start; see its log")
        return proc, sock

    def stop_broker(self, proc: subprocess.Popen, sock: str) -> None:
        try:
            proc.wait(timeout=5)  # a script that never connected leaves the broker waiting to accept
        except subprocess.TimeoutExpired:
            self.seat.kill_group(proc)
        for p in (sock,):
            if os.path.lexists(p):
                os.unlink(p)
        try:
            os.rmdir(os.path.dirname(sock))
        except OSError:
            pass

    def finish(self, entry: Dict, res: Dict) -> None:
        self.calls.append(entry)
        with open(self.log, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        part = self.results / f".{res['id']}.part"
        part.write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
        os.replace(part, self.results / f"{res['id']}.result.json")


def cmd_lock(a) -> None:
    seat = _seat()
    ctx = seat.load(a.context)
    home = os.path.join({"krita": krita_cache, "hyperframes": hyperframes_cache}[a.app](), "calls", "<call>") \
        if a.app in ("krita", "hyperframes") else ""
    sys.stdout.write(lock(ctx, a.app, "/private/tmp/mc-<call>/s" if a.app == "resolve" else "", home=home,
                          ports=free_ports() if a.app == "hyperframes" else ()))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    k = sub.add_parser("ask", help="from inside a pass: ask the launcher to run Blender, Resolve, Krita or HyperFrames")
    k.add_argument("app", choices=APPS + ("higgsfield",))
    k.add_argument("--script", default="", help="a .py the pass wrote, in its scratch folder or a new version folder")
    k.add_argument("--blend", default="", help="blender: a .blend in the media project to open first")
    k.add_argument("--fonts", default="",
                   help="krita: the version's font folder in the media project, registered before the script runs")
    k.add_argument("--render", action="store_true",
                   help="blender: render --blend with the launcher's own script (Grease Pencil, Eevee, Workbench render only "
                        "so); hyperframes: render --project to a PNG sequence")
    k.add_argument("--project", default="", help="hyperframes: the composition's project folder (its index.html)")
    k.add_argument("--check", action="store_true", help="hyperframes: lint and check --project in Chrome; no render")
    k.add_argument("--fps", type=int, default=0, help=f"hyperframes --render: one of {', '.join(map(str, HF_FPS))}; 60 if unset")
    k.add_argument("--out", default="", help="--render: the folder the frames go to")
    k.add_argument("--frames", default="", help="--render: S-E, the first and last frame")
    k.add_argument("--engine", default="cycles", choices=sorted(RENDER_ENGINES),
                   help="--render: cycles (the kept render), or eevee or workbench (previews, into scratch)")
    k.add_argument("--device", default="cpu", choices=sorted(RENDER_DEVICES),
                   help="--render: cycles on the cpu (the default), or gpu (Metal): a preview into scratch, kept in a "
                        "version folder only where the brief says render_device: gpu")
    k.add_argument("--entry", default="", help="higgsfield: the approved entry to take, IMn (Art) or VIn (the Animator)")
    k.add_argument("--status", action="store_true", help="higgsfield: the approved entries, takes and credits; no call")
    k.add_argument("--settle", default="", help="higgsfield: file a job the doorway started and did not file (its id), "
                                                "as the same take, into --out")
    k.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_S, help="seconds the call may run")
    k.add_argument("--wait", type=float, default=DEFAULT_WAIT_S, help="seconds to wait here for the result")
    k.add_argument("args", nargs="*", help="after --: the script's own arguments")
    k.set_defaults(fn=cmd_ask)
    w = sub.add_parser("wait", help="from inside a pass: keep waiting for a call's result")
    w.add_argument("id")
    w.add_argument("--wait", type=float, default=DEFAULT_WAIT_S)
    w.set_defaults(fn=cmd_wait)
    s = sub.add_parser("lock", help="the coordinator: print the Seatbelt lock a call would run under")
    s.add_argument("context")
    s.add_argument("app", choices=APPS)
    s.set_defaults(fn=cmd_lock)
    b = sub.add_parser("broker", help="the launcher's side of one Resolve call; never run by a seat or by hand")
    for flag in ("--context", "--socket", "--ready", "--calls", "--prefix", "--home"):
        b.add_argument(flag, required=True)
    b.add_argument("--timeout", type=float, required=True)
    b.set_defaults(fn=cmd_broker)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
