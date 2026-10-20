"""Motioncraft's application doorway: the lock, the request checks, and Blender, Resolve and Krita run under it for real.

The lock tests read the Seatbelt text a call would run under. The doorway tests run
the launcher's side (`AppServer`) against the test world's own context, and the
seat's side (`apps.py ask`) as a pass would. Blender's and Krita's runs under the real
lock are skipped where they are not installed, and Resolve's where Resolve is not open;
both use the real `sandbox-exec`. One launch runs the whole loop through the fake
vendor: the pass asks from its shell, the launcher runs it, the record shows it.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from test_seat import (BLENDER, KRITA, LAUNCHER, behave, codex_home, codex_pass, context, ctx_data, fake,  # noqa: F401
                       launch, record, seat, world)

sys.path.insert(0, str(LAUNCHER))
import apps  # noqa: E402

APPS = LAUNCHER / "apps.py"
HAVE_BLENDER = os.access(BLENDER, os.X_OK)
HAVE_KRITA = os.access(KRITA, os.X_OK)


@pytest.fixture()
def env_of(world):
    """Point the doorway's own module at the test world (the same variables the launcher reads)."""
    old = dict(os.environ)
    os.environ.update({k: v for k, v in world["env"].items() if k.startswith(("MOTIONCRAFT_", "TRACEKIT_"))})
    os.environ["MOTIONCRAFT_APPS_CACHE"] = str(world["root"] / "appcache")
    os.environ["MOTIONCRAFT_KRITA_CACHE"] = str(world["root"] / "kritacache")
    import seat as seatmod
    import importlib
    importlib.reload(seatmod)
    yield world
    os.environ.clear()
    os.environ.update(old)
    importlib.reload(seatmod)


def ctx_of(world, s, n, *extra):
    path = context(world, s, n, *extra)
    c = ctx_data(path)
    c["source"] = path
    return c


def server(world, s, n, *extra):
    c = ctx_of(world, s, n, *extra)
    return apps.AppServer(c, time.time() + 600), c


def ask(srv, app, script, *args, blend="", timeout=300):
    """What `apps.py ask` does, without its wait: a request in the pass's folder, run by the launcher's side."""
    rid = f"{app}-{time.strftime('%H%M%S')}-{os.urandom(3).hex()}"
    (srv.requests / f"{rid}.json").write_text(json.dumps(
        {"id": rid, "app": app, "script": str(script), "args": list(args), "blend": blend, "timeout": timeout}))
    srv.handle(f"{rid}.json")
    return json.loads((srv.results / f"{rid}.result.json").read_text()), srv.calls[-1]


# --- the lock -----------------------------------------------------------------------------

def test_the_blender_lock_holds_the_pass_fence_and_opens_only_the_graphics_chip(env_of):
    c = ctx_of(env_of, "animator", "a1")
    text = apps.lock(c, "blender")
    assert text.splitlines()[0] == "(version 1)" and "(deny default)" in text
    assert "AGXDeviceUserClient" in text and "com.apple.MTLCompilerService" in text
    assert "network" not in text, "Blender's lock has no network at all"
    for w in c["fence"]["write"]:
        assert f'(subpath "{w}")' in text
    frozen = text.index("(deny file-write*")
    assert frozen > text.index("(allow file-write*"), "the frozen list comes after the allows, so it wins"
    assert f'"{env_of["project"]}/motion/motion-v01-2026-10-19"' in text[frozen:]
    assert f'(subpath "{env_of["emp"]}")' in text, "the employer folders stay unreadable"
    for never in ("windowserver", "launchservicesd", "lsd.", "pasteboard", "appleevent", "tccd"):
        assert never not in text


def test_the_render_lock_adds_launchservices_and_nothing_else(env_of):
    c = ctx_of(env_of, "animator", "r1")
    plain, render = apps.lock(c, "blender").splitlines(), apps.lock(c, "blender", render=True).splitlines()
    added = [l for l in render if l not in plain]
    assert [l for l in added if not l.startswith(";")] == [
        '(allow mach-lookup (global-name "com.apple.coreservices.launchservicesd"))']
    assert all(l in render for l in plain), "the render lock keeps every rule of the plain one"
    assert render.index(added[-1]) < render.index(next(l for l in render if l.startswith("(deny file-write*"))), \
        "the frozen versions are still refused last"
    for never in ("windowserver", "lsd.", "pasteboard", "appleevent", "tccd", "coreservicesd\""):
        assert never not in "\n".join(render)
    with pytest.raises(ValueError):
        apps.lock(c, "resolve", "", render=True)


def test_the_krita_lock_opens_only_its_own_home_and_the_fonts(env_of):
    c = ctx_of(env_of, "art-pose-designer", "k1")
    home = str(env_of["root"] / "kritacache" / "calls" / "x")
    text = apps.lock(c, "krita", home=home)
    assert "(deny default)" in text and f'(subpath "{home}")' in text and "com.apple.fonts" in text
    for shut in ("network", "AGXDeviceUserClient", "launchservicesd", "MTLCompilerService"):
        assert shut not in text, f"Krita's lock has no {shut}: no screen, no graphics chip, no network"
    for w in c["fence"]["write"]:
        assert f'(subpath "{w}")' in text
    assert text.index("(deny file-write*") > text.index("(allow file-write*"), "the frozen list comes after the allows"
    with pytest.raises(ValueError):
        apps.lock(c, "krita")  # never without a home of its own


def test_the_resolve_lock_opens_only_the_brokers_socket(env_of):
    c = ctx_of(env_of, "finishing-sound-designer", "a2")
    text = apps.lock(c, "resolve", "/private/tmp/mc-x/s")
    assert '(allow network-outbound (remote unix-socket (path-literal "/private/tmp/mc-x/s")))' in text
    assert "remote ip" not in text and "localhost" not in text, "never Resolve's own ports"
    assert "AGXDeviceUserClient" not in text and "MTLCompilerService" not in text
    assert "network-outbound" not in apps.lock(c, "resolve", "")


# --- the Resolve broker, against a fake Resolve ----------------------------------------------

class Fake:
    """A stand-in for Resolve's remote objects: methods by name, each a plain callable."""

    def __init__(self, name, **methods):
        self.name, self.methods = name, methods

    def __getattr__(self, n):
        if n in ("name", "methods"):
            raise AttributeError(n)
        return self.methods.get(n)


def fake_resolve(prefix):
    jobs = [{"TargetDir": "/Users/x/Movies"}]
    mine = Fake("Project", GetName=lambda: f"{prefix}-cut", SaveProject=lambda: True,
                GetRenderJobList=lambda: jobs, StartRendering=lambda *a: True)
    seans = Fake("Project", GetName=lambda: "Sean's own film", SaveProject=lambda: True)
    state = {"open": seans}
    pm = Fake("ProjectManager", GetCurrentProject=lambda: state["open"],
              CreateProject=lambda n: state.update(open=mine) or mine, ExportProject=lambda n, p, s=True: True,
              SaveProject=lambda: True, DeleteProject=lambda n: True, ImportProject=lambda path, n=None: True)
    root = Fake("Resolve", GetProjectManager=lambda: pm, Fusion=lambda: Fake("Fusion"), KEYFRAME_MODE_ALL=0.0,
                GetMediaStorage=lambda: Fake("MediaStorage", AddItemListToMediaPool=lambda paths: [Fake("Item")]))
    state["jobs"] = jobs
    return root, state


def call(b, h, name, *args):
    """getattr then call, as the stand-in does; the answer, or the refusal's text."""
    got = b.answer({"op": "getattr", "h": h, "name": name})
    if "ok" not in got:
        return got
    return b.answer({"op": "call", "h": got["ok"]["__h__"], "args": list(args)})


def test_the_broker_holds_a_resolve_script_to_its_own_projects_and_the_fence(env_of):
    c = ctx_of(env_of, "finishing-sound-designer", "a20")
    prefix = os.path.basename(c["media_project"])
    root, state = fake_resolve(prefix)
    api = frozenset({"GetProjectManager", "GetCurrentProject", "CreateProject", "ExportProject", "SaveProject",
                     "GetName", "GetMediaStorage", "AddItemListToMediaPool", "ImportProject", "StartRendering"})
    b = apps.Broker(root, c, api, prefix)
    pm = call(b, 0, "GetProjectManager")["ok"]["__h__"]
    assert "not open to a pass" in call(b, 0, "Fusion")["refused"], "Fusion's object graph is closed"
    assert "not open to a pass" in call(b, pm, "DeleteProject", "x")["refused"]
    assert b.answer({"op": "getattr", "h": 0, "name": "KEYFRAME_MODE_ALL"}) == {"ok": 0.0}
    # Sean's open project: neither worked nor saved
    seans = call(b, pm, "GetCurrentProject")["ok"]["__h__"]
    assert "not this job's" in call(b, seans, "SaveProject")["refused"]
    assert "acts on the open project" in call(b, pm, "SaveProject")["refused"]
    assert "this job's projects are named" in call(b, pm, "CreateProject", "Other film")["refused"]
    mine = call(b, pm, "CreateProject", f"{prefix}-cut")["ok"]["__h__"]
    assert call(b, mine, "SaveProject") == {"ok": True} and call(b, pm, "SaveProject") == {"ok": True}
    stage = c["fence"]["write"][1]
    assert call(b, pm, "ExportProject", f"{prefix}-cut", f"{stage}/finish-v01-2026-10-19/sources/cut.drp") == {"ok": True}
    assert "outside this pass's fence" in call(b, pm, "ExportProject", f"{prefix}-cut", "/Users/x/cut.drp")["refused"]
    frozen = [f for f in c["fence"]["frozen"] if "/finish/" in f]
    if frozen:
        assert "outside this pass's fence" in call(b, pm, "ExportProject", f"{prefix}-cut", f"{frozen[0]}/x.drp")["refused"]
    # a project file the pass wrote itself never loads; one Resolve exported in this call does
    drp = f"{stage}/finish-v01-2026-10-19/sources/cut.drp"
    crafted = f"{stage}/finish-v01-2026-10-19/sources/crafted.drp"
    assert "written in this pass" in call(b, pm, "ImportProject", crafted, f"{prefix}-x")["refused"]
    assert call(b, pm, "ImportProject", drp, f"{prefix}-reopened") == {"ok": True}
    # rendering starts only when every job's target is inside the fence
    assert "outside this pass's fence" in call(b, mine, "StartRendering")["refused"]
    state["jobs"][0]["TargetDir"] = f"{stage}/finish-v01-2026-10-19/renders"
    assert call(b, mine, "StartRendering") == {"ok": True}
    media = call(b, 0, "GetMediaStorage")["ok"]["__h__"]
    assert "outside the media project" in call(b, media, "AddItemListToMediaPool", ["/Users/x/.ssh/id"])["refused"]
    assert "give paths whole" in call(b, media, "AddItemListToMediaPool", ["inputs/a.wav"])["refused"]
    assert "never handed out" in b.answer({"op": "call", "h": 999, "args": []})["refused"]
    assert all("ms" in r for r in b.calls) and any(r.get("refused") for r in b.calls)


FUSION_ON_A_TIMELINE = ("InsertFusionTitleIntoTimeline", "InsertFusionGeneratorIntoTimeline",
                       "InsertFusionCompositionIntoTimeline")


def test_fusion_never_reaches_a_timeline_through_the_broker(env_of):
    """The three calls that put a Fusion-built item on a timeline, and every other Fusion name, are refused."""
    c = ctx_of(env_of, "finishing-sound-designer", "a21")
    prefix = os.path.basename(c["media_project"])
    root, state = fake_resolve(prefix)
    ran = []
    timeline = Fake("Timeline", **{n: (lambda *a, n=n: ran.append(n) or Fake("TimelineItem"))
                                   for n in FUSION_ON_A_TIMELINE + ("CreateFusionClip", "InsertTitleIntoTimeline")})
    mine = Fake("Project", GetName=lambda: f"{prefix}-cut", GetCurrentTimeline=lambda: timeline)
    state["open"] = mine
    real = apps.resolve_api() if apps.RESOLVE_API.is_file() else frozenset()
    # the installed API's own list where Resolve is installed; else a list that wrongly opens them, which the broker still refuses
    api = (real or frozenset(FUSION_ON_A_TIMELINE + ("CreateFusionClip", "ValidateDCTL"))) | {
        "GetProjectManager", "GetCurrentProject", "GetCurrentTimeline", "GetName", "InsertTitleIntoTimeline"}
    b = apps.Broker(root, c, api, prefix)
    pm = call(b, 0, "GetProjectManager")["ok"]["__h__"]
    p = call(b, pm, "GetCurrentProject")["ok"]["__h__"]
    tl = call(b, p, "GetCurrentTimeline")["ok"]["__h__"]
    for name in FUSION_ON_A_TIMELINE + ("CreateFusionClip",):
        assert "not open to a pass" in call(b, tl, name, "Text+")["refused"], name
    assert "not open to a pass" in call(b, 0, "ValidateDCTL", "__DEVICE__ float3 transform() {}")["refused"]
    assert ran == [], "no Fusion call reached Resolve"
    assert "ok" in call(b, tl, "InsertTitleIntoTimeline", "Text") and ran == ["InsertTitleIntoTimeline"], \
        "a plain title still goes on"
    if real:
        assert not {n for n in real if "Fusion" in n} and "ValidateDCTL" not in real
        assert {"InsertTitleIntoTimeline", "SetLUT", "ApplyGradeFromDRX", "SetCDL"} <= real


def test_a_grade_or_lut_the_pass_wrote_never_loads(env_of):
    """A .drx holds the grade as a blob the doorway cannot read, and a LUT may be a DCTL: only files saved before the pass."""
    c = ctx_of(env_of, "finishing-sound-designer", "a22")
    prefix = os.path.basename(c["media_project"])
    root, state = fake_resolve(prefix)
    graph = Fake("Graph", ApplyGradeFromDRX=lambda path, mode, layers=False: True, SetLUT=lambda i, path: True)
    album = Fake("GalleryStillAlbum", ImportStills=lambda paths: True)
    mine = Fake("Project", GetName=lambda: f"{prefix}-cut", GetNodeGraph=lambda: graph, GetCurrentStillAlbum=lambda: album)
    state["open"] = mine
    api = frozenset({"GetProjectManager", "GetCurrentProject", "GetNodeGraph", "GetCurrentStillAlbum",
                     "ApplyGradeFromDRX", "SetLUT", "ImportStills"})
    b = apps.Broker(root, c, api, prefix)
    pm = call(b, 0, "GetProjectManager")["ok"]["__h__"]
    p = call(b, pm, "GetCurrentProject")["ok"]["__h__"]
    g = call(b, p, "GetNodeGraph")["ok"]["__h__"]
    a = call(b, p, "GetCurrentStillAlbum")["ok"]["__h__"]
    new = f"{c['fence']['write'][1]}/finish-v01-2026-10-19/sources"
    scratch = c["scratch"]
    assert "written in this pass" in call(b, g, "ApplyGradeFromDRX", f"{new}/grade.drx", 0)["refused"]
    assert "written in this pass" in call(b, g, "ApplyGradeFromDRX", f"{scratch}/grade.drx", 0)["refused"]
    assert "written in this pass" in call(b, a, "ImportStills", [f"{new}/grade.drx"])["refused"]
    assert "written in this pass" in call(b, g, "SetLUT", 1, f"{scratch}/invert.dctl")["refused"]
    saved = [f for f in c["fence"]["frozen"] if "/finish/" in f] or [str(env_of["project"])]
    assert call(b, g, "ApplyGradeFromDRX", f"{saved[0]}/grade.drx", 0) == {"ok": True}, "a grade saved before the pass loads"
    assert call(b, g, "SetLUT", 1, "LMT Day for Night.xml") == {"ok": True}, "a LUT Resolve already lists, by name"


def test_the_open_api_is_resolves_documented_one_less_the_refused(tmp_path):
    (tmp_path / "DaVinciResolveScript.pyi").write_text(
        "class Project:\n\tdef GetName(self) -> str:\n\t\t...\n\tdef SetSettings(self, s) -> bool:\n\t\t...\n"
        "class Resolve:\n\tdef Fusion(self):\n\t\t...\n\tdef Quit(self) -> None:\n\t\t...\n")
    (tmp_path / "README.md").write_text(
        "## Overview\n\nGetNothing()  --> x\n\n## Deprecated Resolve API Functions\n\n```text\n"
        "GetPresets()   --> {presets...}\nProject.SetSetting(settingName, settingValue)  --> Bool\n```\n")
    api = apps.resolve_api(tmp_path / "DaVinciResolveScript.pyi")
    assert {"GetName", "SetSettings", "GetPresets", "SetSetting"} <= api
    assert not api & {"Fusion", "Quit", "GetNothing"}, "the refused never open; nothing outside the API's own sections"
    if apps.RESOLVE_API.is_file():
        real = apps.resolve_api()
        assert {"SetSetting", "GetSetting", "ExportProject", "CreateProject"} <= real and "Fusion" not in real


def test_the_stand_in_cannot_reach_resolve_without_the_broker(env_of, tmp_path):
    shim = tmp_path / "DaVinciResolveScript.py"
    shim.write_text(apps.SHIM)
    code = ("import DaVinciResolveScript as d\ntry:\n    d.scriptapp('Fusion')\nexcept d.Refused as e:\n    print('REFUSED', e)\n")
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True,
                       env={**os.environ, "PYTHONPATH": str(tmp_path), "MOTIONCRAFT_RESOLVE_SOCKET": "/nonexistent"})
    assert "ConnectionRefusedError" in r.stderr or "FileNotFoundError" in r.stderr, "no broker, no Resolve: it cannot connect"


# --- the request checks --------------------------------------------------------------------

def test_a_request_is_held_to_the_pass_fence(env_of):
    srv, c = server(env_of, "animator", "a3")
    scratch = Path(c["scratch"])
    good = scratch / "ok.py"
    good.write_text("print('hi')\n")
    frozen = env_of["project"] / "motion" / "motion-v01-2026-10-19" / "s.py"
    out = env_of["root"] / "elsewhere.py"
    for p in (out,):
        p.write_text("print(1)\n")
    refused = lambda app, script, **k: ask(srv, app, script, **k)[0]["refused"]  # noqa: E731
    assert "may not run" in ask(server(env_of, "finishing-sound-designer", "a4")[0], "blender", good)[0]["refused"]
    assert "scratch folder or a new version folder" in refused("blender", out)
    assert "scratch folder or a new version folder" in refused("blender", frozen), "a saved version is never a script's home"
    assert "a .blend file in the media project" in refused("blender", good, blend=str(out))
    assert "args are at most" in ask(srv, "blender", good, *["x"] * 40)[0]["refused"]
    assert "--timeout" in refused("blender", good, timeout=99999)
    os.close(srv.fd)
    art, a = server(env_of, "art-pose-designer", "k2")
    mine = Path(a["scratch"]) / "paint.py"
    mine.write_text("print(1)\n")
    assert "may not run blender" in ask(art, "blender", mine)[0]["refused"], "Art's app is Krita only"
    assert "a .blend file" in ask(art, "krita", mine, blend=str(out))[0]["refused"], "--blend is Blender's"
    assert "scratch folder or a new version folder" in ask(art, "krita", out)[0]["refused"]
    assert "may not run krita" in ask(server(env_of, "animator", "k3")[0], "krita", good)[0]["refused"]
    os.close(art.fd)


def ask_render(srv, blend, out, frames=(1, 3), engine="cycles", timeout=300, **extra):
    """What `apps.py ask blender --render` does, without its wait."""
    rid = f"blender-{time.strftime('%H%M%S')}-{os.urandom(3).hex()}"
    req = {"id": rid, "app": "blender", "timeout": timeout,
           "render": {"blend": str(blend), "out": str(out), "frames": list(frames), "engine": engine}, **extra}
    (srv.requests / f"{rid}.json").write_text(json.dumps(req))
    srv.handle(f"{rid}.json")
    return json.loads((srv.results / f"{rid}.result.json").read_text()), srv.calls[-1]


def test_a_render_request_carries_no_code_and_is_held_to_the_fence(env_of):
    srv, c = server(env_of, "animator", "r2")
    scratch, stage = Path(c["scratch"]), env_of["project"] / "motion"
    blend = stage / "motion-v05-2026-10-19" / "scene.blend"
    blend.parent.mkdir(exist_ok=True)
    blend.write_bytes(b"BLENDER")
    outside = env_of["root"] / "elsewhere.blend"
    outside.write_bytes(b"BLENDER")
    frozen = stage / "motion-v01-2026-10-19"
    refused = lambda *a, **k: ask_render(srv, *a, **k)[0]["refused"]  # noqa: E731
    assert "no script or arguments" in refused(blend, scratch / "f", script=str(scratch / "x.py"))
    assert "no script or arguments" in refused(blend, scratch / "f", args=["x"])
    assert "a .blend file in the media project" in refused(outside, scratch / "f")
    assert "new version folder" in refused(blend, frozen / "frames"), "a saved version never takes a render"
    assert "new version folder" in refused(blend, env_of["eng"] / "frames")
    assert "new version folder" in refused(blend, stage), "the stage itself is not a version folder"
    assert "previews" in refused(blend, stage / "motion-v05-2026-10-19" / "frames", engine="eevee")
    assert "previews" in refused(blend, stage / "motion-v05-2026-10-19" / "frames", engine="workbench")
    assert "--engine" in refused(blend, scratch / "f", engine="BLENDER_EEVEE_NEXT")
    assert "--frames" in refused(blend, scratch / "f", frames=(5, 4))
    assert "--frames" in refused(blend, scratch / "f", frames=(1, apps.MAX_RENDER_FRAMES + 1))
    assert "may not run" in ask_render(server(env_of, "finishing-sound-designer", "r3")[0], blend, scratch / "f")[0]["refused"]
    os.close(srv.fd)


def test_a_planted_link_is_never_read_as_a_request(env_of):
    srv, c = server(env_of, "animator", "a5")
    secret = env_of["root"] / "secret.json"
    secret.write_text('{"id": "blender-000000-aaaaaa"}')
    (srv.requests / "blender-000000-aaaaaa.json").symlink_to(secret)
    srv.handle("blender-000000-aaaaaa.json")
    res = json.loads((srv.results / "blender-000000-aaaaaa.result.json").read_text())
    assert res["ok"] is False and "refused" in res
    os.close(srv.fd)


def test_the_prompt_tells_a_seat_with_an_app_to_ask(env_of):
    import seat as seatmod
    c = ctx_of(env_of, "animator", "a6")
    assert "apps.py ask blender" in seatmod.codex_prompt(c, "work") and "ask blender --render" in seatmod.codex_prompt(c, "work")
    f = ctx_of(env_of, "finishing-sound-designer", "a7")
    assert "apps.py ask resolve" in seatmod.claude_prompt(f, "work") and "ask blender" not in seatmod.claude_prompt(f, "work")
    assert "ask resolve" not in seatmod.codex_prompt(c, "work") and "sequencer" not in seatmod.codex_prompt(c, "work")
    d = ctx_of(env_of, "visual-story-director", "a9b")
    prompt = seatmod.claude_prompt(d, "work")
    assert "ask blender --render" in prompt and "sequencer edit" in prompt and "`aud`" in prompt and "ask resolve" not in prompt
    a = ctx_of(env_of, "art-pose-designer", "a9c")
    prompt = seatmod.claude_prompt(a, "work")
    assert prompt.count("apps.py ask krita") == 1 and "brush engine is not available" in prompt and "QPainter" in prompt
    assert prompt.index("Krita: none runs") > 0 and "ask blender" not in prompt and "ask krita" not in seatmod.codex_prompt(c, "work")
    assert "image.py" in prompt, "Art keeps the image path beside Krita"
    g = ctx_of(env_of, "story-gate", "a8", "--anchor", "artifacts/story-packet.md")
    assert "apps.py" not in seatmod.codex_prompt(g, "work")


# --- Blender under the real lock --------------------------------------------------------------

BLENDER_SCRIPT = r'''
import bpy, os, sys, socket
out, eng, frozen = sys.argv[sys.argv.index("--") + 1:][:3]
p = bpy.context.preferences.addons["cycles"].preferences
p.compute_device_type = "METAL"; p.get_devices()
print("METAL", [d.name for d in p.devices if d.type == "METAL"])
for d in p.devices: d.use = d.type == "METAL"
s = bpy.context.scene; s.render.engine = "CYCLES"; s.cycles.device = "GPU"; s.cycles.samples = 4
s.render.resolution_x, s.render.resolution_y = 64, 36
os.makedirs(out, exist_ok=True)
s.render.filepath = os.path.join(out, "frame-0001.png"); bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, "scene.blend"))
for name, target in (("ENGAGEMENT", os.path.join(eng, "brief.md")), ("FROZEN", os.path.join(frozen, "scene.blend"))):
    try:
        open(target, "a").write("x"); print(name, "WROTE")
    except OSError as e: print(name, "REFUSED", type(e).__name__)
try:
    socket.create_connection(("1.1.1.1", 80), timeout=3); print("NET WROTE")
except OSError as e: print("NET REFUSED", type(e).__name__)
'''


@pytest.mark.skipif(not HAVE_BLENDER, reason="Blender is not installed on this machine")
def test_blender_renders_on_the_graphics_chip_inside_the_fence_and_nowhere_else(env_of):
    srv, c = server(env_of, "animator", "a9")
    script = Path(c["scratch"]) / "render.py"
    script.write_text(BLENDER_SCRIPT)
    out = env_of["project"] / "motion" / "motion-v02-2026-10-19"
    frozen = env_of["project"] / "motion" / "motion-v01-2026-10-19"
    before = (frozen / "scene.blend").read_text(), (env_of["eng"] / "brief.md").read_text()
    res, entry = ask(srv, "blender", script, str(out), str(env_of["eng"]), str(frozen))
    log = Path(res["log"]).read_text()
    assert res["ok"], log[-2000:]
    assert "METAL ['" in log, "the graphics chip is visible inside the lock"
    assert (out / "frame-0001.png").stat().st_size > 0 and (out / "scene.blend").is_file()
    assert "ENGAGEMENT REFUSED" in log and "FROZEN REFUSED" in log and "NET REFUSED" in log
    assert ((frozen / "scene.blend").read_text(), (env_of["eng"] / "brief.md").read_text()) == before
    assert str(out / "frame-0001.png") in res["new_or_changed_in_fence"]
    # what ran is the launcher's copy, hashed, beside the lock it ran under
    assert Path(entry["script"]["copy"]).read_text() == BLENDER_SCRIPT and entry["lock"]["sha256"]
    assert Path(entry["script"]["copy"]).parent == env_of["eng"] / "trace" / "logs" / "pass-a9.apps"
    os.close(srv.fd)


# A Grease Pencil ball with a line and a fill, one mesh, and two scripts the file carries that must never run on a
# render: a registered text block and a driver expression, each writing a marker into the pass's scratch folder
# (inside the fence, so only auto-run being off stops them, not the lock).
GP_SCENE = r'''
import bpy, math, os, sys
out, marker = sys.argv[sys.argv.index("--") + 1:][:2]
s = bpy.context.scene
for o in list(s.objects): bpy.data.objects.remove(o)
s.frame_start, s.frame_end = 1, 3
s.render.resolution_x, s.render.resolution_y = 96, 54
s.render.engine = "CYCLES"; s.cycles.samples = 4; s.cycles.seed = 0; s.cycles.use_animated_seed = False
s.cycles.use_denoising = False; s.view_settings.view_transform = "Standard"
s.render.image_settings.file_format = "PNG"
cd = bpy.data.cameras.new("Cam"); cd.type = "ORTHO"; cd.ortho_scale = 8.0
cam = bpy.data.objects.new("Cam", cd); s.collection.objects.link(cam)
cam.location = (0, -10, 0); cam.rotation_euler = (math.radians(90), 0, 0); s.camera = cam
gp = bpy.data.grease_pencils.new("Ball"); ob = bpy.data.objects.new("Ball", gp); s.collection.objects.link(ob)
for name, line, fill in (("Ink", (0.1, 0.1, 0.1, 1), (0, 0, 0, 0)), ("Paint", (0, 0, 0, 0), (0.9, 0.4, 0.2, 1))):
    m = bpy.data.materials.new(name); bpy.data.materials.create_gpencil_data(m)
    m.grease_pencil.color, m.grease_pencil.fill_color = line, fill; gp.materials.append(m)
layer = gp.layers.new("Ball")
for f in (1, 2, 3):
    d = layer.frames.new(f).drawing
    for mat, rad, fid in ((1, 0.01, 1), (0, 0.05, 0)):
        d.add_strokes([32]); st = d.strokes[-1]; st.material_index, st.cyclic, st.fill_id = mat, True, fid
        for i, p in enumerate(st.points):
            a = 2 * math.pi * i / 32; p.position = (-3 + 2 * f + math.cos(a), 0, math.sin(a)); p.radius = rad
bpy.ops.mesh.primitive_cube_add(size=1, location=(3, 2, -2))
t = bpy.data.texts.new("autorun.py"); t.use_module = True
t.write(f"open({marker + '.text'!r}, 'w').write('ran')\n")
fc = bpy.context.object.driver_add("location", 2)
fc.driver.type = "SCRIPTED"; fc.driver.expression = f"open({marker + '.driver'!r}, 'w').write('ran') * 0 - 2"
os.makedirs(out, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, "gp.blend"))
print("SAVED")
'''

OWN_RENDER = r'''
import bpy, sys
out = sys.argv[sys.argv.index("--") + 1]
bpy.context.scene.render.filepath = out + "/own-"; bpy.ops.render.render(animation=True)
'''


def framemd5(folder: Path) -> list:
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(folder / "frame-%04d.png"), "-f", "framemd5", "-pix_fmt", "rgb24", "-"],
                       capture_output=True, text=True, check=True)
    return [l.split(",")[-1].strip() for l in r.stdout.splitlines() if not l.startswith("#")]


@pytest.mark.skipif(not HAVE_BLENDER, reason="Blender is not installed on this machine")
def test_grease_pencil_renders_only_through_the_render_request_and_repeats(env_of):
    srv, c = server(env_of, "animator", "r4")
    scratch, v06 = Path(c["scratch"]), env_of["project"] / "motion" / "motion-v06-2026-10-19"
    marker = str(scratch / "autorun-marker")
    build = scratch / "gp.py"
    build.write_text(GP_SCENE)
    res, _ = ask(srv, "blender", build, str(v06), marker)
    assert res["ok"], Path(res["log"]).read_text()[-2000:]
    blend = v06 / "gp.blend"
    # the seat's own script, under the plain lock, still cannot render Grease Pencil
    own = scratch / "own.py"
    own.write_text(OWN_RENDER)
    res, entry = ask(srv, "blender", own, str(scratch), blend=str(blend))
    assert not res["ok"] and res["exit_code"] != 0 and not list(scratch.glob("own-*"))
    assert "launchservicesd" not in Path(entry["lock"]["path"]).read_text()
    # the render request renders it, with the file's own scripts never run
    res, entry = ask_render(srv, blend, v06 / "frames")
    log = Path(res["log"]).read_text()
    assert res["ok"], log[-2000:]
    assert "MOTIONCRAFT_RENDER autoexec_blocked True" in log and "MOTIONCRAFT_RENDER done CYCLES 1 3" in log
    assert not os.path.exists(marker + ".text") and not os.path.exists(marker + ".driver"), "a script in the file ran"
    assert "--disable-autoexec" in entry["argv"] and entry["argv"].index("--disable-autoexec") < entry["argv"].index(str(blend))
    assert Path(entry["script"]["copy"]).read_text() == apps.RENDER_SCRIPT and entry["script"]["from"] == "launcher: RENDER_SCRIPT"
    assert "com.apple.coreservices.launchservicesd" in Path(entry["lock"]["path"]).read_text()
    assert sorted(p.name for p in (v06 / "frames").iterdir()) == ["frame-0001.png", "frame-0002.png", "frame-0003.png"]
    # TC5: a second render of the same file, in a fresh Blender, gives the same pixels
    res, _ = ask_render(srv, blend, scratch / "again")
    assert res["ok"]
    if subprocess.run(["which", "ffmpeg"], capture_output=True).returncode == 0:
        first, second = framemd5(v06 / "frames"), framemd5(scratch / "again")
        assert len(first) == 3 and first == second and len(set(first)) > 1, "the ball moves, and every frame repeats"
    # a preview engine renders too, into scratch only
    res, _ = ask_render(srv, blend, scratch / "preview", frames=(1, 1), engine="eevee")
    assert res["ok"], Path(res["log"]).read_text()[-2000:]
    assert (scratch / "preview" / "frame-0001.png").stat().st_size > 0
    os.close(srv.fd)


# The Director's animatic: two boards cut in Blender's sequencer over a scratch timing track whose clicks (frames 1, 13
# and 37) and hit (from frame 25, the cut) the seat's script writes with Blender's own sound module, `aud`; the output
# a movie with sound. Ruled on the build map's "Tool ownership" ticket (2026-10-20): the animatic stays in Blender.
ANIMATIC_SCENE = r'''
import bpy, aud, os, sys
out = sys.argv[sys.argv.index("--") + 1]
os.makedirs(os.path.join(out, "boards"), exist_ok=True)
s = bpy.context.scene
s.render.fps, s.render.fps_base, s.frame_start, s.frame_end = 24, 1, 1, 48
s.render.resolution_x, s.render.resolution_y, s.render.resolution_percentage = 160, 90, 100
boards = []
for i, rgb in enumerate(((0.9, 0.85, 0.7), (0.2, 0.3, 0.5)), 1):
    img = bpy.data.images.new(f"board-{i:02d}", 160, 90)
    px = []
    for y in range(90):
        for x in range(160):
            px += [0.05, 0.05, 0.05, 1.0] if abs(x - 80 + (i - 1) * 30) < 4 and abs(y - 45) < 20 else [*rgb, 1.0]
    img.pixels = px
    img.filepath_raw, img.file_format = os.path.join(out, "boards", f"board-{i:02d}.png"), "PNG"
    img.save()
    boards.append(img.filepath_raw)
click = aud.Sound.sine(1000, 48000).limit(0, 0.04).volume(0.5)
track = aud.Sound.silence(48000).limit(0, 2.0)
for f in (1, 13, 37):
    track = track.mix(click.delay((f - 1) / 24))
track = track.mix(aud.Sound.sine(440, 48000).limit(0, 0.25).volume(0.5).delay(24 / 24)).limit(0, 2.0)
wav = os.path.join(out, "timing-track.wav")
track.write(wav, 48000, aud.CHANNELS_MONO, aud.FORMAT_S16, aud.CONTAINER_WAV, aud.CODEC_PCM, 0, 1024)
se = s.sequence_editor_create()
se.strips.new_image("SH1", boards[0], 2, 1, fit_method="FIT").frame_final_duration = 24
se.strips.new_image("SH2", boards[1], 2, 25, fit_method="FIT").frame_final_duration = 24
se.strips.new_sound("timing track (scratch)", wav, 1, 1)
r = s.render
r.use_sequencer, r.image_settings.media_type, r.image_settings.file_format = True, "VIDEO", "FFMPEG"
r.ffmpeg.format, r.ffmpeg.codec, r.ffmpeg.constant_rate_factor = "MPEG4", "H264", "HIGH"
r.ffmpeg.audio_codec, r.ffmpeg.audio_mixrate, r.ffmpeg.audio_channels = "AAC", 48000, "MONO"
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, "animatic.blend"))
print("SAVED", [x.name for x in se.strips])
'''


def stream_md5(movie: Path, stream: str) -> list:
    """Decoded frames of one stream, `v` as RGB pixels or `a` as samples: TC5 compares these, never file checksums."""
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(movie), "-map", f"0:{stream}",
                        *(["-pix_fmt", "rgb24"] if stream == "v" else []), "-f", "framemd5", "-"],
                       capture_output=True, text=True, check=True)
    return [l.split(",")[-1].strip() for l in r.stdout.splitlines() if not l.startswith("#")]


def sounding_frames(movie: Path, fps: int = 24, rate: int = 48000) -> list:
    """The frames, from 1, whose decoded sound rises above a tenth of full scale."""
    import array
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(movie), "-map", "0:a", "-ac", "1", "-ar", str(rate),
                          "-f", "s16le", "-"], capture_output=True, check=True).stdout
    a, n = array.array("h", raw), rate // fps
    return [i // n + 1 for i in range(0, len(a), n) if max(abs(x) for x in a[i:i + n]) > 3277]


@pytest.mark.skipif(not HAVE_BLENDER, reason="Blender is not installed on this machine")
def test_the_directors_sequencer_animatic_renders_through_the_render_request_and_repeats(env_of):
    srv, c = server(env_of, "visual-story-director", "r5")
    scratch, v01 = Path(c["scratch"]), env_of["project"] / "story" / "animatic-v01-2026-10-20"
    build = scratch / "animatic.py"
    build.write_text(ANIMATIC_SCENE)
    res, _ = ask(srv, "blender", build, str(v01))
    assert res["ok"], Path(res["log"]).read_text()[-2000:]
    assert (v01 / "timing-track.wav").stat().st_size > 190_000, "two seconds of tones and silence, written by aud"
    res, entry = ask_render(srv, v01 / "animatic.blend", v01 / "render", frames=(1, 48))
    log = Path(res["log"]).read_text()
    assert res["ok"], log[-2000:]
    assert "MOTIONCRAFT_RENDER done CYCLES 1 48" in log and "--disable-autoexec" in entry["argv"]
    movie = v01 / "render" / "frame-0001-0048.mp4"
    assert [p.name for p in (v01 / "render").iterdir()] == [movie.name], "one movie file, with its sound"
    assert all(str(p).startswith(str(v01)) for p in res["new_or_changed_in_fence"]), "only the new version folder"
    if subprocess.run(["which", "ffmpeg"], capture_output=True).returncode != 0:
        os.close(srv.fd)
        return
    video, audio = stream_md5(movie, "v"), stream_md5(movie, "a")
    assert len(video) == 48 and audio, "48 frames at 24 fps, and a sound stream"
    beats = sounding_frames(movie)
    assert {1, 13, 25, 37} <= set(beats) and not set(beats) & {2, 12, 20, 36, 40}, beats
    # TC5: the same file rendered again in a fresh Blender gives the same pixels and the same samples
    res, _ = ask_render(srv, v01 / "animatic.blend", scratch / "again", frames=(1, 48))
    assert res["ok"]
    again = scratch / "again" / movie.name
    assert stream_md5(again, "v") == video and stream_md5(again, "a") == audio
    os.close(srv.fd)


# --- Resolve under the real lock ---------------------------------------------------------------

RESOLVE_SCRIPT = r'''
import DaVinciResolveScript as d, socket, sys
r = d.scriptapp("Resolve"); print("RESOLVE", r.GetVersionString())
p = r.GetProjectManager().GetCurrentProject()
for name, go in (("FUSION", lambda: r.Fusion()), ("DELETE", lambda: r.GetProjectManager().DeleteProject("x")),
                 ("FUSION-TITLE", lambda: p.InsertFusionTitleIntoTimeline("Text+")),
                 ("FUSION-GENERATOR", lambda: p.InsertFusionGeneratorIntoTimeline("Contours")),
                 ("FUSION-COMPOSITION", lambda: p.InsertFusionCompositionIntoTimeline())):
    try:
        go(); print(name, "RAN")
    except d.Refused as e: print(name, "REFUSED")
for name, port in (("RESOLVE-PORT", 15000), ("FUSCRIPT-PORT", 1144)):
    try:
        socket.create_connection(("127.0.0.1", port), timeout=3); print(name, "OPEN")
    except OSError as e: print(name, "REFUSED", type(e).__name__)
'''


def real_resolve_env(monkeypatch):
    import seat as seatmod
    real = seatmod.tomllib.loads((LAUNCHER.parent / "bench" / "toolbelts.toml").read_text())
    monkeypatch.setattr(seatmod, "app_env", lambda: ([], {k: v for k, v in real["env"].items() if k != "path"}))
    monkeypatch.setattr(apps, "app_paths", lambda: {**real["apps"], "python": real["apps"]["python"]})


@pytest.mark.skipif(not apps.resolve_ports(), reason="Resolve is not open on this machine")
def test_resolve_is_reached_only_through_the_broker_and_its_writes_are_recorded(env_of, monkeypatch):
    real_resolve_env(monkeypatch)
    srv, c = server(env_of, "finishing-sound-designer", "a10")
    script = Path(c["scratch"]) / "hello.py"
    script.write_text(RESOLVE_SCRIPT)
    res, entry = ask(srv, "resolve", script)
    log = Path(res["log"]).read_text()
    assert res["ok"], log[-2000:] + str(entry.get("error"))
    assert "RESOLVE 2" in log and "FUSION REFUSED" in log and "DELETE REFUSED" in log
    for name in ("FUSION-TITLE", "FUSION-GENERATOR", "FUSION-COMPOSITION"):
        assert f"{name} REFUSED" in log, f"{name}: a Fusion item never goes on a timeline"
    assert "RESOLVE-PORT REFUSED" in log and "FUSCRIPT-PORT REFUSED" in log, "the script never reaches Resolve itself"
    assert entry["broker"]["calls"] >= 3 and len(entry["broker"]["refused"]) == 5
    assert entry["resolve"]["running"] is True
    assert set(entry["written"]) == {"fence", "frozen", "resolve_own", "launcher", "other_programs", "outside"}
    os.close(srv.fd)


def test_without_resolve_open_the_call_says_so(env_of, monkeypatch):
    monkeypatch.setattr(apps.AppServer, "start_broker", lambda *a: (_ for _ in ()).throw(
        RuntimeError("Resolve is not running on this machine; the coordinator starts it, then ask again")))
    srv, c = server(env_of, "finishing-sound-designer", "a11")
    script = Path(c["scratch"]) / "hello.py"
    script.write_text("print(1)\n")
    res, _ = ask(srv, "resolve", script)
    assert res["ok"] is False and "Resolve is not running" in res["error"]
    os.close(srv.fd)


# --- Krita under the real lock -----------------------------------------------------------------

# Art's kind of script: Qt's painter for the strokes, Krita for the layers, a filter, the file and the exports; then
# writes that must be refused, and a module planted in the call's own Krita home for a later call to find.
KRITA_PAINT = r"""
import os, socket, sys
from krita import Krita, InfoObject
from PyQt5.QtCore import QPointF, QRect, Qt
from PyQt5.QtGui import QBrush, QColor, QImage, QPainter, QPainterPath, QPen
out, eng, frozen, sean = sys.argv[1:5]
W = H = 128
k = Krita.instance()
doc = k.createDocument(W, H, "paint", "RGBA", "U8", "", 72.0)
root = doc.rootNode()
paper = doc.createNode("paper", "paintlayer"); root.addChildNode(paper, None)
paper.setPixelData(bytes([200, 220, 230, 255]) * (W * H), 0, 0, W, H)
noise = k.filter("noise"); cfg = noise.configuration(); cfg.setProperty("level", 30); noise.setConfiguration(cfg)
noise.apply(paper, 0, 0, W, H)
img = QImage(W, H, QImage.Format_ARGB32); img.fill(Qt.transparent)
p = QPainter(img); p.setRenderHint(QPainter.Antialiasing)
path = QPainterPath(QPointF(10, 100)); path.cubicTo(40, 10, 90, 120, 118, 20)
p.setPen(QPen(QColor(150, 40, 30, 200), 9, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)); p.drawPath(path)
p.setPen(Qt.NoPen); p.setBrush(QBrush(QColor(30, 60, 140, 160))); p.drawEllipse(QPointF(64, 64), 20, 14); p.end()
bits = img.constBits(); bits.setsize(img.sizeInBytes())
ink = doc.createNode("ink", "paintlayer"); root.addChildNode(ink, paper)
ink.setPixelData(bytes(bits), 0, 0, W, H); ink.setBlendingMode("multiply"); ink.setOpacity(220)
doc.waitForDone()
os.makedirs(out, exist_ok=True)
print("SAVED", doc.saveAs(os.path.join(out, "layers.kra")))
for n in (paper, ink):
    n.save(os.path.join(out, n.name() + ".png"), 72.0, 72.0, InfoObject(), QRect(0, 0, W, H))
doc.refreshProjection(); doc.waitForDone()
flat = QImage(bytes(doc.pixelData(0, 0, W, H)), W, H, QImage.Format_ARGB32).copy()
print("FLAT", flat.save(os.path.join(out, "flat.png")))
for name, target in (("ENGAGEMENT", os.path.join(eng, "brief.md")), ("FROZEN", os.path.join(frozen, "x.kra")),
                     ("SEANS_KRITA", os.path.join(sean, "motioncraft-test-must-not-exist"))):
    try:
        open(target, "a").write("x"); print(name, "WROTE")
    except OSError as e: print(name, "REFUSED", type(e).__name__)
try:
    socket.create_connection(("1.1.1.1", 80), timeout=3); print("NET WROTE")
except OSError as e: print("NET REFUSED", type(e).__name__)
home_pykrita = os.path.join(os.environ["HOME"], "Library", "Application Support", "kritarunner")
open(os.path.join(home_pykrita, "planted.py"), "w").write("print('PLANTED RAN')\n")
print("HOME", os.environ["HOME"])
"""

KRITA_REOPEN = r"""
import os, sys
from krita import Krita, InfoObject
from PyQt5.QtCore import QRect
kra, out = sys.argv[1:3]
doc = Krita.instance().openDocument(kra)
for n in doc.rootNode().childNodes():
    if n.name() in ("paper", "ink"):
        print("LAYER", n.name(), n.blendingMode(), n.opacity())
        n.save(os.path.join(out, "reopen-" + n.name() + ".png"), 72.0, 72.0, InfoObject(), QRect(0, 0, 128, 128))
try:
    import planted
    print("PLANTED FOUND")
except ImportError:
    print("PLANTED GONE")
"""


def decoded(png: Path) -> str:
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(png), "-f", "framemd5", "-pix_fmt", "rgba", "-"],
                       capture_output=True, text=True, check=True)
    return [l for l in r.stdout.splitlines() if not l.startswith("#")][0].split(",")[-1].strip()


@pytest.mark.skipif(not HAVE_KRITA, reason="Krita is not installed on this machine")
def test_krita_paints_layers_inside_the_fence_and_nowhere_else(env_of):
    stage = env_of["project"] / "appearance"
    frozen = stage / "appearance-v01-2026-10-20"
    frozen.mkdir(exist_ok=True)
    (frozen / "x.kra").write_text("v01")
    srv, c = server(env_of, "art-pose-designer", "k4")
    scratch, out = Path(c["scratch"]), stage / "appearance-v02-2026-10-20"
    sean = Path(os.path.expanduser("~/Library/Application Support/krita"))
    (scratch / "paint.py").write_text(KRITA_PAINT)
    before = (frozen / "x.kra").read_text(), (env_of["eng"] / "brief.md").read_text()
    try:
        res, entry = ask(srv, "krita", scratch / "paint.py", str(out), str(env_of["eng"]), str(frozen), str(sean))
        log = Path(res["log"]).read_text()
        assert res["ok"], log[-3000:]
        assert entry["krita_template"]["built"], "the first call builds this version's template"
        assert "SAVED True" in log and "FLAT True" in log and "MOTIONCRAFT_KRITA done 0" in log
        for name in ("ENGAGEMENT", "FROZEN", "SEANS_KRITA", "NET"):
            assert f"{name} REFUSED" in log, name
        assert ((frozen / "x.kra").read_text(), (env_of["eng"] / "brief.md").read_text()) == before
        assert {p.name for p in out.iterdir()} == {"layers.kra", "paper.png", "ink.png", "flat.png"}
        assert str(out / "layers.kra") in res["new_or_changed_in_fence"]
        home = [l.split(" ", 1)[1] for l in log.splitlines() if l.startswith("HOME ")][0]
        assert not os.path.exists(home), "the call's home is gone with the call"
        assert not str(home).startswith(os.path.expanduser("~/Library")), "never Sean's own Library"
        # each layer exported with its transparency: the ink is see-through where nothing was drawn
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=pix_fmt", "-of", "csv=p=0", str(out / "ink.png")],
                           capture_output=True, text=True, check=True)
        assert "a" in r.stdout.strip(), r.stdout
        # a second call reopens the file: same layers, same decoded pixels, and nothing of the first call's home
        (scratch / "reopen.py").write_text(KRITA_REOPEN)
        res2, entry2 = ask(srv, "krita", scratch / "reopen.py", str(out / "layers.kra"), str(scratch))
        log2 = Path(res2["log"]).read_text()
        assert res2["ok"], log2[-3000:]
        assert "krita_template" not in entry2, "the template is built once"
        assert "LAYER paper normal 255" in log2 and "LAYER ink multiply 220" in log2
        assert "PLANTED GONE" in log2 and "PLANTED RAN" not in log2, "a call's home never reaches a later call"
        for n in ("paper", "ink"):
            assert decoded(out / f"{n}.png") == decoded(scratch / f"reopen-{n}.png"), n
    finally:
        stray = sean / "motioncraft-test-must-not-exist"
        if stray.exists():
            stray.unlink()
        os.close(srv.fd)


@pytest.mark.skipif(not HAVE_KRITA, reason="Krita is not installed on this machine")
def test_a_krita_call_that_fails_says_so(env_of):
    srv, c = server(env_of, "art-pose-designer", "k5")
    scratch = Path(c["scratch"])
    cases = {
        "raises.py": "raise RuntimeError('no')\n",
        # the brush engine with no screen: Krita itself crashes, and the call says so
        "brush.py": ("from krita import Krita\nd = Krita.instance().createDocument(8, 8, 'b', 'RGBA', 'U8', '', 72.0)\n"
                     "print(d.rootNode().childNodes()[0].paintAbility())\n"),
        # leaving Krita before the wrapper's closing line, which kritarunner would report as exit 0
        "quits.py": "import os; os._exit(0)\n",
    }
    try:
        for name, body in cases.items():
            (scratch / name).write_text(body)
            res, entry = ask(srv, "krita", scratch / name)
            assert res["ok"] is False, name
            if name == "quits.py":
                assert res["exit_code"] == 0 and "without the script finishing" in res["error"]
            else:
                assert res["exit_code"] != 0, name
    finally:
        os.close(srv.fd)


# --- the whole loop, through a launch ------------------------------------------------------------

@pytest.mark.skipif(not HAVE_BLENDER, reason="Blender is not installed on this machine")
def test_a_pass_asks_from_its_shell_and_the_launch_record_shows_the_call(world, codex_home, fake):
    ctx = codex_pass(world, codex_home, "a12")
    scratch = ctx_data(ctx)["scratch"]
    script = Path(scratch) / "hello.py"
    script.write_text("import bpy; print('BLENDER', bpy.app.version_string)\n")
    behave(fake, calls=1, run=[[sys.executable, "-B", str(APPS), "ask", "blender", "--script", str(script), "--wait", "120"]])
    r = launch(world, ctx, "--output", "artifacts/scene-record-a12.md", "--run")
    assert r.returncode == 0, r.stderr
    seen = (fake / "seen-run-0.txt").read_text()
    assert seen.startswith("0\n") and "BLENDER 5." in seen and '"ok": true' in seen
    rec = record(world, "a12")
    assert rec["apps"]["calls"] == 1 and rec["apps"]["refused"] == [] and rec["apps"]["writes_to_check"] == []
    env = json.loads((fake / "seen-env.json").read_text())
    assert env["MOTIONCRAFT_APPS_REQUESTS"] == str(Path(scratch) / "apps")
