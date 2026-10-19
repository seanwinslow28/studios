#!/usr/bin/env python3
"""The Director's and Art's one way to the Codex image path: one image, filed in the pass's own version folder.

    image.py --context <eng>/trace/logs/pass-NN.context.json
             --out <stage>/<artifact>-vNN-<date>/<name>.png --prompt-file F [--ref IMAGE]...

A seat runs this from inside its own Claude pass, as the bench README's image path
("Image generation is a tool call, never a seat"). The pass's settings let exactly
this command, for exactly this pass's context, out of the Claude sandbox, because a
`codex exec` inside that sandbox could neither read the Codex seat home's sign-in nor
start its own sandbox; every other command that asks to leave is refused. So this
file holds the fence for the call: it checks the context is a Director's or Art's
pass that may call the image path (the context says so, and no seat can write a
context), that the image lands as a new file in a version folder the pass made in
its own stage, that the prompt comes from a folder the pass writes, and that every
reference image sits in the media project, never anywhere else on the machine.

Then it runs `codex exec` from the Codex seat home with image generation switched on
for this one call and its shell switched off (the call runs outside the seat's
sandbox, so a shell could read what the seat cannot), refusing to file anything if
the run's log shows a command, a file change, a connector call or a helper anyway, on the pinned id with its effort spelled out, the prompt on
standard input (`-i` takes every following argument as a file), and files the
image Codex saved under `generated_images/<thread>/` whatever the exit code (a run
can exit 1 after the image is made; mc-setup-003). Beside it goes `<name>.image.json`:
the prompt, the references and their hashes, the run, and the label "generated"
(never-do 8, 13). Both are created relative to the version folder held open since
the check, never through a link and never over a file already there. Each call is also logged to `trace/logs/pass-NN.images.jsonl`.
Written on the Motioncraft build map's "Plugin allowlist and launch form for seat
runs" ticket (2026-10-19).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import seat  # noqa: E402  the launcher's own rules: the context, the stage folders, the pinned id

VERSION_DIR = re.compile(r"[a-z0-9][a-z0-9-]*-v\d{2,}-\d{4}-\d{2}-\d{2}")
CONTEXT_FILE = re.compile(r"pass-[0-9a-z-]+\.context\.json")
MAX_REFS = 5  # the image tool takes up to five reference images (mc-setup-003)
REF_SUFFIXES = (".png", ".jpg", ".jpeg", ".webp")
MAX_PROMPT_BYTES = 32_000
TIMEOUT_S = 600
# Codex's shell and its long-running exec: off for the image call. Not the code-mode host, which the image tool runs in.
NO_SHELL = ("shell_tool", "unified_exec")
CODEX_HOME = Path(os.path.expanduser(os.environ.get("MOTIONCRAFT_CODEX_HOME", str(seat.DEFAULT_HOME))))
LABEL = ("generated: the Codex image tool on Sean's ChatGPT plan, through motioncraft/launcher/image.py; "
         "the image model is undisclosed (mc-setup-003)")


def refuse(msg: str) -> None:
    sys.stderr.write(f"image.py: {msg}\n")
    sys.exit(1)


def under(path: str, root: str) -> bool:
    return seat.under(seat.real(path), seat.real(root))


def checked(a) -> Dict:
    """The context, the output, the prompt and the references, each held to the pass's fence; or a refusal."""
    src = seat.real(a.context)
    if not CONTEXT_FILE.fullmatch(os.path.basename(src)) or not os.path.isfile(src):
        refuse(f"{a.context} is not a pass context (trace/logs/pass-NN.context.json)")
    ctx = seat.load(src)
    if os.path.dirname(src) != os.path.join(ctx["engagement"], "trace", "logs"):
        refuse("the context is not in its engagement's trace/logs/, where only the coordinator writes")
    if not ctx.get("toolbelt", {}).get("image"):
        refuse(f"{ctx['seat']}'s pass may not call the image path: only the Director's and Art's, on Claude, drafting")
    if ctx.get("machine") != seat.machine():
        refuse(f"the context was written on {ctx.get('machine')}, not {seat.machine()}")
    stage = os.path.join(ctx["media_project"], seat.STAGE_DIRS[ctx["seat"]])
    out = Path(seat.real(a.out))
    vdir = out.parent
    if out.suffix != ".png":
        refuse("--out names a .png")
    if seat.real(str(vdir.parent)) != seat.real(stage) or not VERSION_DIR.fullmatch(vdir.name):
        refuse(f"--out goes in a version folder directly in this seat's stage ({stage}/<artifact>-vNN-<date>/)")
    if not vdir.is_dir():
        refuse(f"make the version folder {vdir.name} first; the image lands in it")
    if any(under(str(vdir), f) for f in ctx["fence"]["frozen"]):
        refuse(f"{vdir.name} was saved before this pass; a saved version is never changed (rule 5)")
    sidecar = out.with_name(out.stem + ".image.json")
    if out.exists() or sidecar.exists():
        refuse(f"{out.name} exists; an image is written once")
    prompt = Path(seat.real(a.prompt_file))
    if not prompt.is_file() or not (under(str(prompt), ctx["scratch"]) or under(str(prompt), str(vdir))):
        refuse("--prompt-file is a file the pass wrote, in its scratch folder or the version folder")
    if prompt.stat().st_size > MAX_PROMPT_BYTES:
        refuse(f"the prompt is over {MAX_PROMPT_BYTES} bytes")
    if len(a.ref) > MAX_REFS:
        refuse(f"the image tool takes up to {MAX_REFS} references")
    refs: List[Path] = []
    for r in a.ref:
        p = Path(seat.real(r))
        if not p.is_file() or p.suffix.lower() not in REF_SUFFIXES or not under(str(p), ctx["media_project"]):
            refuse(f"--ref {r}: a reference is an image file in the media project, nothing else goes to the image path")
        refs.append(p)
    if not (CODEX_HOME / "auth.json").exists():
        refuse(f"the Codex seat home {CODEX_HOME} has no sign-in")
    return {"ctx": ctx, "out": out, "sidecar": sidecar, "prompt": prompt.read_text(encoding="utf-8"), "refs": refs}


def ask(prompt: str, refs: List[Path]) -> str:
    use = (" Pass the attached reference image" + ("s" if len(refs) > 1 else "")
           + " to the tool as its referenced images.") if refs else ""
    return ("Make one image with the image generation tool, then reply with the word done. Call the tool exactly "
            f"once. Run no shell command and change no file.{use} The image:\n\n{prompt.strip()}\n")


def run(c: Dict) -> Dict:
    ctx = c["ctx"]
    cwd = Path(ctx["scratch"]) / f"image-{time.strftime('%H%M%S')}-{os.getpid()}"
    cwd.mkdir(parents=True)
    # The call runs outside the seat's sandbox, so it gets no shell at all: it could otherwise read files the
    # seat cannot and carry them into the image prompt. The image tool is the one tool it needs.
    argv = ["codex", "exec", "--json", "--model", seat.CODEX_MODEL, "-c", f'model_reasoning_effort="{seat.CODEX_EFFORT}"',
            "--strict-config", "-c", 'web_search="disabled"', "-c", "features.image_generation=true",
            *[a for f in NO_SHELL for a in ("-c", f"features.{f}=false")],
            "--skip-git-repo-check", "-C", str(cwd)]
    for r in c["refs"]:
        argv += ["-i", str(r)]
    argv.append("-")  # the prompt on standard input
    env = {k: os.environ[k] for k in seat.KEEP_ENV if k in os.environ}
    env.update(CODEX_HOME=str(CODEX_HOME), TMPDIR=str(cwd))
    started, t0 = seat.now(), time.time()
    try:
        r = subprocess.run(argv, input=ask(c["prompt"], c["refs"]), cwd=str(cwd), env=env,
                           capture_output=True, text=True, timeout=TIMEOUT_S)
        code, out, err = r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired as e:
        code = 124
        out = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
        err = f"no answer in {TIMEOUT_S} s"
    thread = seat.codexlog.jsonl_thread(out)
    usage, acted = {}, []
    for line in out.splitlines():
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if not isinstance(e, dict):
            continue
        if e.get("type") == "turn.completed":
            usage = e.get("usage") or {}
        item = e.get("item")
        if isinstance(item, dict) and item.get("type") in seat.CODEX_TOOL_ITEMS:
            acted.append(item["type"])
    made = []
    if thread:
        folder = CODEX_HOME / "generated_images" / thread
        made = sorted((p for p in folder.glob("*") if p.is_file() and p.stat().st_mtime >= t0 - 1),
                      key=lambda p: p.stat().st_mtime) if folder.is_dir() else []
    sessions = [seat.codexlog.read_session(f.read_text(encoding="utf-8"), f.name)
                for f in (seat.codexlog.find_sessions(CODEX_HOME, thread) if thread else [])]
    stamps = sorted({f"{m} {e}" for s in sessions if not s.helper for m, e in s.stamps})
    helpers = [s.path for s in sessions if s.helper]
    last = err.strip().splitlines()[-1] if err.strip() else ""
    return {"started": started, "completed": seat.now(), "wall_clock_s": round(time.time() - t0), "exit_code": code,
            "thread": thread, "made": [str(p) for p in made], "runtime_stamps": stamps, "usage": usage or None,
            "helper_sessions": helpers, "acted": sorted(set(acted)), "stderr_last": seat.one_line(last, 200)}


def write_new(vdir: Path, dfd: int, name: str, data: bytes) -> None:
    """Create one new file in the version folder, never through a link, never over a file already there."""
    if seat.real(str(vdir)) != str(vdir) or os.stat(dfd).st_ino != os.stat(vdir, follow_symlinks=False).st_ino:
        refuse(f"{vdir.name} moved or became a link during the call; nothing filed")
    fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644, dir_fd=dfd)
    with os.fdopen(fd, "wb") as f:
        f.write(data)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--context", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--prompt-file", required=True)
    ap.add_argument("--ref", action="append", default=[])
    a = ap.parse_args()
    c = checked(a)
    ctx, out = c["ctx"], c["out"]
    vdir = out.parent
    # The version folder is the seat's to write, so it is held open from the check on: a folder swapped for a
    # link, or a file or link planted under either name, stops the filing.
    dfd = os.open(vdir, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    res = run(c)
    entry = {"pass": seat.pass_id_of(ctx["source"]), "seat": ctx["seat"], "out": str(out), "label": LABEL,
             "prompt": c["prompt"], "refs": [{"path": str(r), "sha256": seat.sha256(r)} for r in c["refs"]], **res}
    filed = bool(res["made"]) and not res["acted"] and not res["helper_sessions"]
    if filed:
        src = Path(res["made"][-1])
        data = src.read_bytes()
        entry.update(source=str(src), sha256=seat.hashlib.sha256(data).hexdigest(), extra_images=res["made"][:-1])
        try:
            # the label first: an image is never filed without its prompt and "generated" beside it
            write_new(vdir, dfd, c["sidecar"].name, (json.dumps(entry, indent=2) + "\n").encode())
            write_new(vdir, dfd, out.name, data)
        except FileExistsError:
            refuse(f"{out.name} or its sidecar appeared during the call; an image is written once")
    os.close(dfd)
    log = Path(ctx["engagement"]) / "trace" / "logs" / f"{entry['pass']}.images.jsonl"
    with open(log, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    if res["acted"] or res["helper_sessions"]:
        refuse(f"the image call ran more than the image tool ({', '.join(res['acted']) or 'a helper agent'}); "
               f"nothing filed; logged to {log.name}")
    if not res["made"]:
        refuse(f"no image was made (codex exit {res['exit_code']}: {res['stderr_last'] or 'no error text'}); logged to {log.name}")
    print(f"{out} sha256 {entry['sha256']}" + (f" (codex exited {res['exit_code']} after the image was made)"
                                                if res["exit_code"] else ""))


if __name__ == "__main__":
    main()
