"""Renders a Blender scene's frames to a PNG sequence, from the command line, with no window.

Run it inside Blender, with the scene's own scripts switched off so nothing the file carries runs:

    /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --disable-autoexec <scene.blend> \\
        --python-exit-code 1 --python blender_render.py -- <out dir> <first frame> <last frame> [engine] [device]

engine is cycles (the default), eevee or workbench; device is cpu (the default) or gpu, for Cycles only.
Frames land as <out dir>/frame-0001.png and on. The log's RENDER lines say whether Blender skipped a script the
file carries, which device Cycles used, and that the render finished.

Cycles on the CPU is the path that repeats a frame exactly. On the GPU it uses the Mac's Metal device, and stops
rather than fall back to the CPU without a word when no Metal device is found. OSL script nodes are switched off,
since a script node is code. Grease Pencil, Eevee and Workbench all draw through Blender's GPU drawing engine.
"""
import os
import sys

ENGINES = {"cycles": "CYCLES", "eevee": "BLENDER_EEVEE", "workbench": "BLENDER_WORKBENCH"}
DEVICES = {"cpu": "CPU", "gpu": "GPU"}


def arguments(argv):
    """The arguments after Blender's `--`, checked; None when they ask for help or are too few."""
    args = argv[argv.index("--") + 1:] if "--" in argv else argv[1:]
    if not args or args[0] in ("-h", "--help") or len(args) < 3:
        return None
    out, start, end = args[0], int(args[1]), int(args[2])
    engine = args[3].lower() if len(args) > 3 else "cycles"
    device = args[4].lower() if len(args) > 4 else "cpu"
    if engine not in ENGINES:
        raise SystemExit(f"blender_render.py: the engine is one of {', '.join(ENGINES)}, not {engine!r}")
    if device not in DEVICES:
        raise SystemExit(f"blender_render.py: the device is cpu or gpu, not {device!r}")
    if end < start:
        raise SystemExit("blender_render.py: the last frame comes before the first")
    return out, start, end, ENGINES[engine], DEVICES[device]


def render(out, start, end, engine, device):
    import bpy  # only inside Blender

    print("RENDER autoexec_blocked", bool(bpy.app.autoexec_fail), repr(bpy.app.autoexec_fail_message))
    s = bpy.context.scene
    s.render.engine = engine
    if engine == "CYCLES":
        s.cycles.device = device
        s.cycles.shading_system = False  # no OSL script nodes
        used = []
        if device == "GPU":
            p = bpy.context.preferences.addons["cycles"].preferences
            p.compute_device_type = "METAL"
            p.get_devices()
            for d in p.devices:
                d.use = d.type == "METAL"
            used = [d.name for d in p.devices if d.use]
            if not used:
                raise SystemExit("RENDER no Metal device: Cycles would render on the CPU")
        print("RENDER device", device, *([used] if used else []))
    s.frame_start, s.frame_end = start, end
    os.makedirs(out, exist_ok=True)
    s.render.filepath = os.path.join(os.path.abspath(out), "frame-")
    s.render.use_file_extension = True
    s.render.image_settings.file_format = "PNG"
    bpy.ops.render.render(animation=True)
    print("RENDER done", engine, start, end)


if __name__ == "__main__":
    picked = arguments(sys.argv)
    if picked is None:
        sys.exit(print(__doc__) or 0)
    render(*picked)
