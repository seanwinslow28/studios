"""The kerning helper inside the Animator's Blender pass, under the application doorway's real lock.

An Animator pass asks for Blender with `apps.py ask blender --script <file>`, and the
launcher runs the script under a Seatbelt lock with no network that writes only the
pass's fence. This runs that loop with the launcher's own test world (from
`launcher/tests/`): the script imports the helper from `motioncraft/tools/` by path,
packs the font into the scene, writes the spacing, saves the scene into a new
version folder in the Animator's stage, and reopens it. Skipped where Blender is
not installed.
"""
from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS.parent / "launcher" / "tests"))
sys.path.insert(0, str(TOOLS))
import kerning  # noqa: E402
from test_apps import HAVE_BLENDER, ask, env_of, server  # noqa: E402,F401
from test_seat import world  # noqa: E402,F401
from test_kerning import REAL  # noqa: E402

# The shelf's font where the shelf is on the machine, else STIX Two Text, an open-licence font every Mac carries.
FONT = next((f for f in (REAL["static TrueType"], REAL["variable, default instance"]) if f.is_file()), REAL["static TrueType"])

SCRIPT = r'''
import bpy, json, os, sys
tools, font, out = sys.argv[sys.argv.index("--") + 1:][:3]
sys.path.insert(0, tools)
import kerning
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o)
vf = bpy.data.fonts.load(font); vf.pack()
cu = bpy.data.curves.new("Title", "FONT"); cu.body = "AVATAR To"; cu.font = vf; cu.size = 2.0
bpy.context.scene.collection.objects.link(bpy.data.objects.new("Title", cu))
report = kerning.apply(bpy.data.objects["Title"], font)
os.makedirs(out)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, "type.blend"))
bpy.ops.wm.open_mainfile(filepath=os.path.join(out, "type.blend"))
again = bpy.data.objects["Title"].data
print("KERNING " + json.dumps({"written": report["values"], "reopened": [f.kerning for f in again.body_format],
                               "packed": again.font.packed_file is not None, "limits": report["limits"]}))
'''


@pytest.mark.skipif(not HAVE_BLENDER, reason="Blender is not installed on this machine")
def test_the_helper_runs_in_an_animator_pass_under_the_blender_lock(env_of):
    if not FONT.is_file():
        pytest.skip(f"{FONT} is not on this machine")
    srv, c = server(env_of, "animator", "k1")
    fonts = env_of["project"] / "inputs" / "fonts"  # stands in for a version's assets/fonts/, copied from the shelf
    fonts.mkdir(parents=True, exist_ok=True)
    font = fonts / FONT.name
    shutil.copyfile(FONT, font)
    script = Path(c["scratch"]) / "kern.py"
    script.write_text(SCRIPT)
    out = env_of["project"] / "motion" / "motion-v03-2026-10-21"
    res, entry = ask(srv, "blender", script, str(TOOLS), str(font), str(out))
    log = Path(res["log"]).read_text()
    assert res["ok"], log[-2000:]
    got = json.loads(next(l for l in log.splitlines() if l.startswith("KERNING "))[len("KERNING "):])
    want, limits = kerning.spacing(kerning.Font(font), "AVATAR To")
    assert got["written"] == want and not got["limits"] and not limits
    assert got["reopened"] == pytest.approx(want, abs=1e-5), "the spacing survives a save and a reopen"
    assert got["packed"], "the font travels inside the scene"
    assert str(out / "type.blend") in res["new_or_changed_in_fence"]
    assert entry["argv"][0] == "sandbox-exec" and "network" not in Path(entry["lock"]["path"]).read_text(), \
        "it ran under the Blender lock, which has no network"
    os.close(srv.fd)
