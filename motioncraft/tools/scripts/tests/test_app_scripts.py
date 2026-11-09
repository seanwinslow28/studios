"""The Blender render script and the Krita runner: their own parts, then each in its application where installed."""
import subprocess
import sys

import pytest

import blender_render
import krita_run
from conftest import BLENDER, HAVE_BLENDER, HAVE_KRITA, SCRIPTS, run


def test_render_arguments_are_checked():
    assert blender_render.arguments(["blender", "--", "out", "1", "24"]) == ("out", 1, 24, "CYCLES", "CPU")
    assert blender_render.arguments(["blender", "--", "out", "1", "2", "workbench", "gpu"])[3:] == ("BLENDER_WORKBENCH", "GPU")
    assert blender_render.arguments(["blender", "--", "--help"]) is None
    for bad in (["o", "1", "2", "octane"], ["o", "1", "2", "cycles", "tpu"], ["o", "5", "2"]):
        with pytest.raises(SystemExit):
            blender_render.arguments(["blender", "--", *bad])


@pytest.mark.skipif(not HAVE_BLENDER, reason="Blender is not installed on this machine")
@pytest.mark.parametrize("engine", ["cycles", "workbench"])
def test_blender_renders_the_frames(tmp_path, engine):
    scene = tmp_path / "s.blend"
    make = ("import bpy; s = bpy.context.scene; s.render.resolution_x = 64; s.render.resolution_y = 36; "
            f"s.cycles.samples = 1; bpy.ops.wm.save_as_mainfile(filepath={str(scene)!r})")
    subprocess.run([BLENDER, "-b", "--factory-startup", "--python-expr", make], check=True, capture_output=True)
    r = subprocess.run([BLENDER, "-b", "--factory-startup", "--disable-autoexec", str(scene), "--python-exit-code", "1",
                        "--python", str(SCRIPTS / "blender_render.py"), "--", str(tmp_path / "out"), "1", "2", engine],
                       capture_output=True, text=True, timeout=600)
    assert r.returncode == 0, r.stdout[-2000:] + r.stderr[-2000:]
    assert "RENDER done" in r.stdout
    assert sorted(p.name for p in (tmp_path / "out").iterdir()) == ["frame-0001.png", "frame-0002.png"]


def test_families_follow_svg_inheritance():
    svg = ('<svg xmlns="http://www.w3.org/2000/svg"><g font-family="Inter, sans-serif">'
           '<text>a<tspan style="font-family: \'Source Serif 4\'">b</tspan></text></g><text>c</text></svg>')
    assert krita_run.families(svg) == [["Inter", "sans-serif"], ["Source Serif 4"], None]


def test_unregistered_names_each_missing_font():
    svg = '<svg xmlns="http://www.w3.org/2000/svg"><text font-family="Inter">a</text><text>b</text></svg>'
    said = krita_run.unregistered(svg, {"inter"})
    assert said == ["a text names no font, so Krita would set it in its default font"]
    assert any("'Inter'" in s for s in krita_run.unregistered(svg, set()))
    assert krita_run.unregistered("<svg", set())[0].startswith("the SVG could not be read")


EXPORT = '''
import sys
from krita import Krita, InfoObject
doc = Krita.instance().createDocument(64, 32, "t", "RGBA", "U8", "", 72.0)
print("EXPORTED", doc.exportImage(sys.argv[1], InfoObject()))
doc.close()
'''

WRONG_FONT = '''
from krita import Krita
doc = Krita.instance().createDocument(200, 100, "t", "RGBA", "U8", "", 72.0)
layer = doc.createVectorLayer("words")
doc.rootNode().addChildNode(layer, None)
try:
    layer.addShapesFromSvg('<svg xmlns="http://www.w3.org/2000/svg" width="200" height="100">'
                           '<text x="10" y="50" font-family="No Such Font Anywhere">Hi</text></svg>')
except RuntimeError:
    pass  # caught, and the run still fails
'''


@pytest.mark.skipif(not HAVE_KRITA, reason="Krita is not installed on this machine")
def test_krita_runs_a_script_and_fails_on_a_missing_font(tmp_path):
    home = tmp_path / "home"
    (tmp_path / "export.py").write_text(EXPORT)
    r = run("krita_run.py", tmp_path / "export.py", "--home", home, "--", tmp_path / "out.png")
    assert "EXPORTED True" in r.stdout and (tmp_path / "out.png").is_file()
    (tmp_path / "font.py").write_text(WRONG_FONT)
    r = run("krita_run.py", tmp_path / "font.py", "--home", home, check=False)
    assert r.returncode == 1 and "font-fault" in r.stdout and "No Such Font Anywhere" in r.stdout
