"""Motioncraft's application doorway: the lock, the request checks, and Blender and Resolve run under it for real.

The lock tests read the Seatbelt text a call would run under. The doorway tests run
the launcher's side (`AppServer`) against the test world's own context, and the
seat's side (`apps.py ask`) as a pass would. Blender's run under the real lock is
skipped where Blender is not installed, and Resolve's where Resolve is not open;
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

from test_seat import (BLENDER, LAUNCHER, behave, codex_home, codex_pass, context, ctx_data, fake,  # noqa: F401
                       launch, record, seat, world)

sys.path.insert(0, str(LAUNCHER))
import apps  # noqa: E402

APPS = LAUNCHER / "apps.py"
HAVE_BLENDER = os.access(BLENDER, os.X_OK)


@pytest.fixture()
def env_of(world):
    """Point the doorway's own module at the test world (the same variables the launcher reads)."""
    old = dict(os.environ)
    os.environ.update({k: v for k, v in world["env"].items() if k.startswith(("MOTIONCRAFT_", "TRACEKIT_"))})
    os.environ["MOTIONCRAFT_APPS_CACHE"] = str(world["root"] / "appcache")
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
    assert "apps.py ask blender" in seatmod.codex_prompt(c, "work") and "Eevee does not run here" in seatmod.codex_prompt(c, "work")
    f = ctx_of(env_of, "finishing-sound-designer", "a7")
    assert "apps.py ask resolve" in seatmod.claude_prompt(f, "work") and "ask blender" not in seatmod.claude_prompt(f, "work")
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
