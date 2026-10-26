"""Motioncraft's Higgsfield doorway: the approved list, the uploads, the takes, the credit caps, the fence and the filing.

The doorway runs as the launcher runs it, in its own process, calling a fake `higgsfield`
command line that the test allowlist names (the real one's answers, from `higgsfield`
1.1.23, read 2026-10-25), which keeps the account's balance and records every call it is
given. Only the download of a finished take is patched in, by a small harness. The test
world, its context and its fence are the launcher tests' own (test_seat.py).
"""
from __future__ import annotations

import contextlib
import hashlib
import json
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path

import pytest

from test_seat import LAUNCHER, context, ctx_data, world  # noqa: F401

sys.path.insert(0, str(LAUNCHER))
import apps  # noqa: E402
from tracekit.engagement import sha256_path  # noqa: E402

PNG = b"\x89PNG\r\n\x1a\n" + b"fake image"
MP4 = b"\x00\x00\x00\x18ftypmp42" + b"fake video"

# The fake command line: Higgsfield's answers in the real one's shapes, the balance moving `lag` reads after a job.
FAKE = r'''#!{python}
import json, os, sys, uuid
from pathlib import Path
state = Path({state!r})
b = json.loads((state / "behavior.json").read_text())
args = sys.argv[1:]
with open(state / "calls.jsonl", "a") as f:
    f.write(json.dumps({{"args": args, "cwd": os.getcwd(), "cwd_files": os.listdir("."),
                        "env": sorted(os.environ)}}) + "\n")
words = [a for a in args if not a.startswith("--")]
bal = state / "balance"
n = float(bal.read_text()) if bal.exists() else b.get("balance", 1000.0)
pending = state / "pending"

def out(doc, code=0):
    print(json.dumps(doc))
    sys.exit(code)

if words[:2] == ["account", "status"]:
    if pending.exists():
        left, cost = pending.read_text().split()
        if int(left) <= 0:
            n -= float(cost)
            bal.write_text(str(n))
            pending.unlink()
        else:
            pending.write_text(f"{{int(left) - 1}} {{cost}}")
    out({{"credits": n, "email": "someone", "subscription_plan_type": "ultra"}})
if words[:2] == ["model", "list"]:
    kind = "image" if "--image" in args else "video"
    out([{{"job_type": m, "type": kind}} for m in (["nano_banana_2"] if kind == "image" else ["seedance_2_0"])])
if words[:2] == ["model", "get"]:
    p = lambda name, t, enum=None: dict(name=name, type=t, **({{"enum": enum}} if enum else {{}}))
    if words[2] == "nano_banana_2":
        out({{"job_type": words[2], "params": [p("aspect_ratio", "string", ["1:1", "16:9", "9:16"]),
             p("image_references", "array"), p("prompt", "string"), p("resolution", "string", ["1k", "2k", "4k"])]}})
    out({{"job_type": words[2], "params": [p("aspect_ratio", "string", ["16:9", "9:16"]), p("duration", "integer"),
         p("generate_audio", "boolean"), p("image_references", "array"), p("start_image", "object|null"),
         p("end_image", "object|null"), p("prompt", "string")]}})
if words[:2] == ["upload", "create"]:
    # the bytes as Higgsfield would receive them, read from the path given at the moment of the upload
    import hashlib
    data = Path(words[2]).read_bytes()
    uid = str(uuid.uuid4())
    with open(state / "uploads.jsonl", "a") as f:
        f.write(json.dumps({{"path": words[2], "sha256": hashlib.sha256(data).hexdigest(), "id": uid}}) + "\n")
    if b.get("upload_fails"):
        print("Error: upload rejected", file=sys.stderr)
        sys.exit(1)
    out({{"id": uid, "type": "image", "url": "https://cdn.example/uploads/" + uid}})
if words[:2] == ["generate", "cost"]:
    out({{"credits": b.get("cost", 2)}})
if words[:2] == ["generate", "create"]:
    if b.get("create_fails"):
        print("Error: Not enough credits", file=sys.stderr)
        sys.exit(1)
    jid = str(uuid.uuid4())
    if b.get("charge", b.get("cost", 2)):
        pending.write_text(f"{{b.get('lag', 0)}} {{b.get('charge', b.get('cost', 2))}}")
    (state / "last-job").write_text(jid)
    if b.get("create_shape") == "ids":
        out([jid])
    if b.get("create_shape") == "garbled":
        out({{"message": "created " + jid}})
    out([{{"id": jid, "job_type": words[2], "status": "queued"}}])
if words[:2] == ["generate", "get"]:
    if b.get("job_fails"):
        out({{"id": words[2], "status": "failed", "result_url": None}})
    out({{"id": words[2], "status": "completed", "result_url": "https://cdn.example/" + words[2] + b.get("ext", ".png")}})
if words[:2] == ["generate", "wait"]:
    if b.get("job_fails"):
        if pending.exists():
            pending.unlink()
        out({{"id": words[2], "status": "failed", "result_url": None}})
    out({{"id": words[2], "status": "completed", "result_url": "https://cdn.example/" + words[2] + b.get("ext", ".png")}})
print("Error: unknown command " + " ".join(args), file=sys.stderr)
sys.exit(2)
'''

# Runs the doorway as the launcher does, with only the download of the finished take answered from the test's folder.
HARNESS = r'''
import os, sys
from pathlib import Path
sys.path.insert(0, os.environ["HF_LAUNCHER"])
import higgsfield
state = Path(os.environ["HF_FAKE"])
higgsfield.METER_POLL_S = 0
higgsfield.METER_WAIT_S = 0.3

def fetch(url):
    (state / "fetched").write_text(url)
    return (state / "result.bin").read_bytes()

higgsfield.fetch = fetch
sys.argv = ["higgsfield.py"] + sys.argv[1:]
higgsfield.main()
'''

IMAGES = {"test": "sold-proof", "ceiling_credits": 300, "entries": [
    {"id": "IM1", "purpose": "the house's design reference", "model": "nano_banana_2",
     "prompt": "a craftsman house with a blue front door, late afternoon, architectural visualisation",
     "params": {"aspect_ratio": "16:9", "resolution": "2k"}},
    {"id": "IM2", "model": "nano_banana_2", "prompt": "the same porch at dawn"},
]}
SETUP = """---
id: {id}
date: 2026-10-25
step: "Higgsfield's data-use and training settings, and Sean's intended-use approval (SWCB #271)"
tool: {tool}
engagements: {engagements}
{extra}intended_use_approved: {approved}
---

The record.
"""


def setup_text(approved="2026-10-25", id="mc-setup-023", tool="higgsfield", engagements="[mc-eng-900]", **fields):
    """The test world's own intended-use record: its engagement is the world's brief, mc-eng-900. Any other header
    field (uploads, supersedes) goes in as given."""
    extra = "".join(f"{k}: {v}\n" for k, v in fields.items())
    return SETUP.format(id=id, tool=tool, engagements=engagements, approved=approved, extra=extra)


@pytest.fixture(scope="module")
def hw(world):
    """The test world with Higgsfield on Art's and the Animator's lines, the brief's cap, the setup record, a fake
    command line, and Art's approved list of images."""
    root = world["root"]
    state = root / "hffake"
    state.mkdir()
    fake = state / "higgsfield"
    fake.write_text(FAKE.format(python=sys.executable, state=str(state)))
    fake.chmod(0o755)
    (state / "harness.py").write_text(HARNESS)
    belts = root / "toolbelts.toml"
    old_belts = belts.read_text()
    belts.write_text(old_belts.replace('apps = ["krita"]\n', 'apps = ["krita"]\nhiggsfield = "image"\n', 1)
                     .replace('tools = ["kerning"]\n', 'tools = ["kerning"]\nhiggsfield = "video"\n', 1)
                     .replace("[apps]\n", f'[apps]\nhiggsfield = "{fake}"\n', 1))
    brief = world["eng"] / "brief.md"
    old_brief = brief.read_text()
    brief.write_text(old_brief.replace("media:", "higgsfield_credits_cap: 2500\nmedia:", 1))
    setup = root / "ledger" / "setup" / "2026-10-25-higgsfield" / "record.md"
    setup.parent.mkdir(parents=True)
    setup.write_text(setup_text())
    world.update(state=state, fake=fake, setup=setup, brief=brief)
    approve(world, "020", "higgsfield-images-v01-2026-10-25", IMAGES)
    yield world
    belts.write_text(old_belts)
    brief.write_text(old_brief)


def approve(w, n, version, doc=None, files=None):
    """Sean's approval of a list, or of a copy of media files: its locked copy in approved/, named by an approvals
    entry with its folder hash."""
    approved = w["project"] / "approved" / version
    approved.mkdir(parents=True)
    if doc is not None:
        (approved / "higgsfield.json").write_text(json.dumps(doc, indent=2))
    for rel, data in (files or {}).items():
        (approved / rel).parent.mkdir(parents=True, exist_ok=True)
        (approved / rel).write_bytes(data)
    return record_approval(w, n, version, approved)


def record_approval(w, n, version, approved):
    approvals = w["root"] / "ledger" / "approvals"
    approvals.mkdir(parents=True, exist_ok=True)
    rel = w["project"].relative_to(w["root"] / "media")
    (approvals / f"{n}-2026-10-25-{version}.md").write_text(
        f"---\nid: mc-ap-{n}\nversion_id: {version}\nversion_path: media:{rel}/approved/{version}\n"
        f"version_sha256: {sha256_path(approved)}\ndecision: approved\n---\n\nApproved in one decision.\n")
    return approved


def withdraw(w, n):
    for f in (w["root"] / "ledger" / "approvals").glob(f"{n}-*.md"):
        f.unlink()


@pytest.fixture()
def fresh(hw):
    """A clean fake account and job log for each test: no calls, no takes, the default prices."""
    for f in hw["state"].iterdir():
        if f.name not in ("harness.py", "higgsfield"):
            f.unlink()
    for f in (hw["eng"] / "trace" / "logs").glob("*.higgsfield.jsonl"):
        f.unlink()
    behave(hw)
    result(hw, PNG)
    return hw


def behave(w, **b):
    (w["state"] / "behavior.json").write_text(json.dumps(b))


def result(w, data):
    (w["state"] / "result.bin").write_bytes(data)


def pass_of(w, seat, stage, *extra):
    """A pass's context and a new version folder in its stage."""
    n = f"h{os.urandom(2).hex()}"
    ctx = context(w, seat, n, *extra)
    vdir = w["project"] / stage / f"gen{n}-v01-2026-10-25"
    vdir.mkdir()
    return ctx, vdir


def run(w, *args):
    env = dict(w["env"], HF_LAUNCHER=str(LAUNCHER), HF_FAKE=str(w["state"]))
    return subprocess.run([sys.executable, str(w["state"] / "harness.py"), *args], env=env, capture_output=True,
                          text=True, timeout=60)


def take(w, ctx, entry, out):
    return run(w, "take", "--context", ctx, "--entry", entry, "--out", str(out))


def calls(w):
    f = w["state"] / "calls.jsonl"
    return [json.loads(x) for x in f.read_text().splitlines()] if f.exists() else []


def sent(w):
    """Every call that would have reached Higgsfield's generator or its uploads."""
    return [c["args"] for c in calls(w) if c["args"][:2] == ["generate", "create"] or c["args"][:1] == ["upload"]]


def job(w):
    return [json.loads(x) for f in sorted((w["eng"] / "trace" / "logs").glob("*.higgsfield.jsonl"))
            for x in f.read_text().splitlines()]


def art_take(w):
    ctx, vdir = pass_of(w, "art-pose-designer", "appearance")
    r = take(w, ctx, "IM1", vdir / "house.png")
    assert r.returncode == 0, r.stderr
    return ctx, vdir, (w["state"] / "last-job").read_text()


def test_an_image_take_is_filed_with_its_approved_prompt_beside_it_and_metered_from_the_account(fresh):
    behave(fresh, cost=2, lag=2)
    ctx, vdir, jid = art_take(fresh)
    assert (vdir / "house.png").read_bytes() == PNG
    side = json.loads((vdir / "house.higgsfield.json").read_text())
    assert side["label"].startswith("generated: Higgsfield (nano_banana_2)") and "mc-ap-020" in side["label"]
    assert side["approved_entry"] == IMAGES["entries"][0] and side["test"] == "sold-proof" and side["job"] == jid
    assert side["setup"] == "mc-setup-023" and side["take"] == 1
    # metered from the balance, which moved two reads after the job
    assert side["balance_before"] == 1000 and side["balance_after"] == 998
    assert side["credits"] == 2 and side["credits_source"] == "the account's balance, before and after"
    create = sent(fresh)
    assert create == [["generate", "create", "nano_banana_2", f"--prompt={IMAGES['entries'][0]['prompt']}",
                       "--aspect_ratio=16:9", "--resolution=2k", "--json", "--no-color"]]
    for c in calls(fresh):
        assert c["cwd_files"] == [] and "mc-higgsfield-" in c["cwd"], "every call runs from a new, empty folder"
        assert not [k for k in c["env"] if k.startswith(("MOTIONCRAFT", "TRACEKIT"))]
    lines = [e for e in job(fresh) if e.get("job") == jid]
    assert len(lines) == 2 and lines[0]["credits_source"].startswith("estimate") and lines[-1]["made"]


def test_a_video_take_moves_an_earlier_take_by_its_job_id_and_nothing_is_uploaded(fresh):
    _, _, jid = art_take(fresh)
    videos = {"test": "sold-proof", "ceiling_credits": 300, "entries": [
        {"id": "VI1", "model": "seedance_2_0", "prompt": "a slow push-in on the porch", "start_image": f"job:{jid}",
         "params": {"duration": 5, "generate_audio": False, "aspect_ratio": "16:9"}}]}
    approve(fresh, "021", f"higgsfield-video-{jid[:6]}-v01-2026-10-25", videos)
    try:
        behave(fresh, cost=22.5)
        result(fresh, MP4)
        ctx, vdir = pass_of(fresh, "animator", "motion")
        r = take(fresh, ctx, "VI1", vdir / "push-in.mp4")
        assert r.returncode == 0, r.stderr
        assert (vdir / "push-in.mp4").read_bytes() == MP4
        create = sent(fresh)[-1]
        assert f"--start-image={jid}" in create and "--duration=5" in create and "--generate_audio=false" in create
        assert not any(c["args"][:1] == ["upload"] for c in calls(fresh))
        side = json.loads((vdir / "push-in.higgsfield.json").read_text())
        assert side["kind"] == "video" and side["credits"] == 22.5
    finally:
        withdraw(fresh, "021")


def test_an_upload_is_refused_whole_before_any_call(fresh):
    ctx, vdir = pass_of(fresh, "art-pose-designer", "appearance")
    for n, bad in (("022", {"start_image": "./house.png"}), ("023", {"image_references": ["/Users/someone/logo.png"]}),
                   ("024", {"image_references": [f"upload:{uuid.uuid4()}"]}),
                   ("025", {"params": {"image_references": "job:" + str(uuid.uuid4())}}),
                   ("026", {"params": {"resolution": "/Users/someone/screens/home.png"}}),
                   ("027", {"params": {"aspect_ratio": "https://example.com/a.png"}})):
        lst = {"test": "sold-proof", "ceiling_credits": 300,
               "entries": [{"id": "IM1", "model": "nano_banana_2", "prompt": "a porch", **bad}]}
        approve(fresh, n, f"higgsfield-bad{n}-v01-2026-10-25", lst)
        try:
            r = take(fresh, ctx, "IM1", vdir / f"bad{n}.png")
            assert r.returncode == 1 and "cannot be sent as it stands" in r.stderr, (bad, r.stderr)
        finally:
            withdraw(fresh, n)
    assert sent(fresh) == [], "nothing reached Higgsfield"
    assert not list(vdir.iterdir())
    assert all(e.get("refused") for e in job(fresh)), "every refusal is a line in the pass's log"


def test_a_reference_to_a_job_this_doorway_did_not_make_is_refused(fresh):
    stranger = str(uuid.uuid4())
    approve(fresh, "028", "higgsfield-video-stranger-v01-2026-10-25", {"test": "sold-proof", "ceiling_credits": 300,
            "entries": [{"id": "VI1", "model": "seedance_2_0", "prompt": "a push-in", "start_image": f"job:{stranger}"}]})
    try:
        ctx, vdir = pass_of(fresh, "animator", "motion")
        r = take(fresh, ctx, "VI1", vdir / "push-in.mp4")
        assert r.returncode == 1 and "no take this doorway made" in r.stderr and "names only the doorway's own takes" in r.stderr
        assert sent(fresh) == []
    finally:
        withdraw(fresh, "028")


RENDER = b"\x89PNG\r\n\x1a\n" + b"the real portal, on demo data"


def renders(w, n, version, files=None, listed=None):
    """An approved copy of media files with its checksums.sha256, named by Sean's approval mc-ap-<n>."""
    files = {"screens/R01.png": RENDER} if files is None else files
    listed = files if listed is None else listed
    sums = "".join(f"{hashlib.sha256(d).hexdigest()}  {rel}\n" for rel, d in listed.items())
    return approve(w, n, version, files={**files, "checksums.sha256": sums.encode()})


def video_list(ref, **more):
    return {"test": "film-test", "ceiling_credits": 300, "entries": [
        {"id": "VI1", "model": "seedance_2_0", "prompt": "the portal builds itself on the desk", "start_image": ref,
         "params": {"duration": 5, "aspect_ratio": "16:9"}, **more}]}


@contextlib.contextmanager
def uploads_allowed(w, value="approved-media"):
    """The job's setup record says its lists may name approved media files (mc-setup-027's field)."""
    w["setup"].write_text(setup_text(uploads=value))
    try:
        yield
    finally:
        w["setup"].write_text(setup_text())


def uploads(w):
    """Every file the fake command line was given to upload, with the sha256 of the bytes it read."""
    f = w["state"] / "uploads.jsonl"
    return [json.loads(x) for x in f.read_text().splitlines()] if f.exists() else []


def test_a_file_is_refused_whole_when_the_setup_record_does_not_allow_uploads(fresh):
    renders(fresh, "040", "renders40-v01-2026-10-26")
    approve(fresh, "041", "higgsfield-video-r40-v01-2026-10-26", video_list("approved/renders40-v01-2026-10-26/screens/R01.png"))
    ctx, vdir = pass_of(fresh, "animator", "motion")
    try:
        r = take(fresh, ctx, "VI1", vdir / "shot.mp4")
        assert r.returncode == 1 and "cannot be sent as it stands" in r.stderr and "never a file" in r.stderr, r.stderr
        # the field says approved-media or it says nothing: any other word is no permission
        with uploads_allowed(fresh, "yes"):
            r = take(fresh, ctx, "VI1", vdir / "shot.mp4")
            assert r.returncode == 1 and "uploads: approved-media" in r.stderr, r.stderr
    finally:
        withdraw(fresh, "041")
        withdraw(fresh, "040")
    assert sent(fresh) == [] and uploads(fresh) == [] and not list(vdir.iterdir())


def test_with_uploads_allowed_a_listed_approved_file_is_uploaded_from_a_checked_copy_and_logged(fresh):
    approved = renders(fresh, "042", "renders42-v01-2026-10-26")
    ref = "approved/renders42-v01-2026-10-26/screens/R01.png"
    approve(fresh, "043", "higgsfield-video-r42-v01-2026-10-26", video_list(ref, image_references=[ref]))
    try:
        with uploads_allowed(fresh):
            behave(fresh, cost=30)
            result(fresh, MP4)
            ctx, vdir = pass_of(fresh, "animator", "motion")
            r = take(fresh, ctx, "VI1", vdir / "shot.mp4")
            assert r.returncode == 0, r.stderr
            s = run(fresh, "status", "--context", ctx)
            assert "with uploads of approved media (uploads: approved-media)" in s.stdout, s.stderr
    finally:
        withdraw(fresh, "043")
        withdraw(fresh, "042")
    sha = hashlib.sha256(RENDER).hexdigest()
    up = uploads(fresh)
    assert len(up) == 1 and up[0]["sha256"] == sha, "one upload a file, of exactly the bytes its copy lists"
    assert not os.path.realpath(up[0]["path"]).startswith(os.path.realpath(fresh["project"])), \
        "sent from a private copy of the checked bytes, never from the approved folder"
    order = [c["args"][:2] for c in calls(fresh) if c["args"][0] in ("upload", "generate")]
    assert order[:3] == [["upload", "create"], ["generate", "cost"], ["generate", "create"]]
    for args in ([c["args"] for c in calls(fresh) if c["args"][:2] == ["generate", "cost"]][-1], sent(fresh)[-1]):
        assert f"--start-image={up[0]['id']}" in args and f"--image-references={up[0]['id']}" in args
        assert not [a for a in args if "R01" in a or "/" in a.split("=", 1)[-1]], "no path goes to the generator"
    side = json.loads((vdir / "shot.higgsfield.json").read_text())
    assert side["label"].startswith("generated: Higgsfield (seedance_2_0)") and side["made"]
    [u] = side["uploads"]
    assert u["ref"] == ref and u["fields"] == ["start_image", "image_references"] and u["sha256"] == sha
    assert u["path"] == os.path.realpath(approved / "screens" / "R01.png") and u["approval"] == "mc-ap-042"
    assert u["upload"] == up[0]["id"] and u["bytes"] == len(RENDER) and u["uploaded"]
    assert all(e["uploads"] == side["uploads"] for e in job(fresh) if e.get("job") == side["job"]), \
        "every line of the call in the pass's log names the upload"


def test_with_uploads_allowed_a_path_outside_approved_a_link_or_a_url_is_refused_whole(fresh):
    renders(fresh, "044", "renders44-v01-2026-10-26")
    v = "renders44-v01-2026-10-26"
    bad = ["inputs/rendered-assets-r2-2026-10-26/R01.png", "approved/../inputs/R01.png", f"approved/{v}/../{v}/R01.png",
           f"approved/{v}/./screens/R01.png", "/Users/someone/R01.png", f"./approved/{v}/screens/R01.png",
           "https://example.com/R01.png", f"media:film/project/approved/{v}/screens/R01.png",
           f"approved\\{v}\\screens\\R01.png", f"approved/{v}/", f"approved/{v}", f"upload:{uuid.uuid4()}"]
    ctx, vdir = pass_of(fresh, "animator", "motion")
    try:
        with uploads_allowed(fresh):
            for i, ref in enumerate(bad):
                n = f"{50 + i:03d}"
                approve(fresh, n, f"higgsfield-bad{n}-v01-2026-10-26", video_list(ref))
                try:
                    r = take(fresh, ctx, "VI1", vdir / f"bad{n}.mp4")
                    assert r.returncode == 1 and "cannot be sent as it stands" in r.stderr, (ref, r.stderr)
                finally:
                    withdraw(fresh, n)
    finally:
        withdraw(fresh, "044")
    assert sent(fresh) == [] and uploads(fresh) == [] and not list(vdir.iterdir())


def test_with_uploads_allowed_a_file_is_sent_only_as_its_approved_copy_lists_it(fresh):
    """Each named file is checked at the take: the copy's approval and hash, its checksums.sha256, the file itself."""
    proj = fresh["project"] / "approved"
    outside = fresh["root"] / "outside"
    (outside / "screens").mkdir(parents=True)
    (outside / "screens" / "R01.png").write_bytes(RENDER)
    sums = f"{hashlib.sha256(RENDER).hexdigest()}  screens/R01.png\n"
    cases = []
    # a file that is a link, to the same bytes outside the copy
    a = proj / "renders70-v01-2026-10-26"
    (a / "screens").mkdir(parents=True)
    os.symlink(outside / "screens" / "R01.png", a / "screens" / "R01.png")
    (a / "checksums.sha256").write_text(sums)
    record_approval(fresh, "070", a.name, a)
    cases.append((f"approved/{a.name}/screens/R01.png", "goes through a link"))
    # a folder that is a link
    a = proj / "renders71-v01-2026-10-26"
    a.mkdir()
    os.symlink(outside / "screens", a / "screens")
    (a / "checksums.sha256").write_text(sums)
    record_approval(fresh, "071", a.name, a)
    cases.append((f"approved/{a.name}/screens/R01.png", "goes through a link"))
    # the bytes are not the ones the copy lists
    renders(fresh, "072", "renders72-v01-2026-10-26", listed={"screens/R01.png": b"another render"})
    cases.append(("approved/renders72-v01-2026-10-26/screens/R01.png", "is not the file its approved copy lists"))
    # a file the copy does not list
    renders(fresh, "073", "renders73-v01-2026-10-26", files={"screens/R01.png": RENDER, "screens/R02.png": RENDER + b"2"},
            listed={"screens/R01.png": RENDER})
    cases.append(("approved/renders73-v01-2026-10-26/screens/R02.png", "not listed in"))
    cases.append(("approved/renders73-v01-2026-10-26/screens/R09.png", "does not exist"))
    cases.append(("approved/renders73-v01-2026-10-26/screens", "is not a regular file"))
    # a copy no approval names, and one changed since its approval
    a = proj / "renders74-v01-2026-10-26"
    (a / "screens").mkdir(parents=True)
    (a / "screens" / "R01.png").write_bytes(RENDER)
    (a / "checksums.sha256").write_text(sums)
    cases.append((f"approved/{a.name}/screens/R01.png", "no approvals entry with decision approved names"))
    a = renders(fresh, "075", "renders75-v01-2026-10-26")
    (a / "screens" / "R01.png").write_bytes(RENDER + b"edited")
    (a / "checksums.sha256").write_text(f"{hashlib.sha256(RENDER + b'edited').hexdigest()}  screens/R01.png\n")
    cases.append((f"approved/{a.name}/screens/R01.png", "no longer matches its approval mc-ap-075"))
    # listed and approved, but no image
    renders(fresh, "076", "renders76-v01-2026-10-26", files={"screens/notes.png": b"not a picture"})
    cases.append(("approved/renders76-v01-2026-10-26/screens/notes.png", "is not an image"))
    ctx, vdir = pass_of(fresh, "animator", "motion")
    try:
        with uploads_allowed(fresh):
            for i, (ref, why) in enumerate(cases):
                n = f"{80 + i:03d}"
                approve(fresh, n, f"higgsfield-file{n}-v01-2026-10-26", video_list(ref))
                try:
                    r = take(fresh, ctx, "VI1", vdir / f"f{n}.mp4")
                    assert r.returncode == 1 and why in r.stderr, (ref, r.stderr)
                    assert job(fresh)[-1].get("refused"), "the refusal is a line in the pass's log"
                finally:
                    withdraw(fresh, n)
    finally:
        for n in ("070", "071", "072", "073", "075", "076"):
            withdraw(fresh, n)
    assert sent(fresh) == [] and uploads(fresh) == [], "nothing left the machine"
    assert not list(vdir.iterdir())


def test_an_upload_higgsfield_rejects_is_logged_and_no_job_is_made(fresh):
    renders(fresh, "045", "renders45-v01-2026-10-26")
    ref = "approved/renders45-v01-2026-10-26/screens/R01.png"
    approve(fresh, "046", "higgsfield-video-r45-v01-2026-10-26", video_list(ref))
    try:
        with uploads_allowed(fresh):
            behave(fresh, upload_fails=True)
            ctx, vdir = pass_of(fresh, "animator", "motion")
            r = take(fresh, ctx, "VI1", vdir / "shot.mp4")
    finally:
        withdraw(fresh, "046")
        withdraw(fresh, "045")
    assert r.returncode == 1 and "upload rejected" in r.stderr, r.stderr
    assert [c for c in sent(fresh) if c[:1] == ["generate"]] == [], "no job without its upload"
    last = job(fresh)[-1]
    assert last["refused"] and last["uploads"][0]["ref"] == ref and last["uploads"][0]["upload"] is None
    assert last["uploads"][0]["sha256"] == hashlib.sha256(RENDER).hexdigest()


def test_a_record_another_approved_record_supersedes_is_skipped_and_two_live_records_still_refuse(tmp_path):
    """mc-setup-027 supersedes mc-setup-025, both for mc-eng-003: the newer approved one holds, and uploads with it."""
    import higgsfield
    setup = tmp_path / "ledger" / "setup"
    eng = tmp_path / "ledger" / "engagements" / "portal-launch-film-2026-10-25"
    eng.mkdir(parents=True)
    (eng / "brief.md").write_text("---\nid: mc-eng-003\ntype: full-train\nhiggsfield_credits_cap: 1000\n---\n")

    def record(folder, **kw):
        (setup / folder).mkdir(parents=True, exist_ok=True)
        (setup / folder / "record.md").write_text(setup_text(engagements="[mc-eng-003]", **kw))

    def holds():
        return higgsfield.setup_record({"engagement": str(eng)})

    record("2026-10-25-higgsfield-portal-launch-film", id="mc-setup-025")
    assert holds()["id"] == "mc-setup-025" and holds()["uploads"] is False, "no field, no file, ever"
    record("2026-10-26-higgsfield-portal-launch-film-video", id="mc-setup-027", approved="2026-10-26",
           supersedes="mc-setup-025", uploads="approved-media")
    got = holds()
    assert got["id"] == "mc-setup-027" and got["uploads"] is True and got["supersedes"] == ["mc-setup-025"]
    record("2026-10-26-higgsfield-portal-launch-film-video", id="mc-setup-027", approved="2026-10-26",
           supersedes="[mc-setup-025]  # the plates' record")
    assert holds()["id"] == "mc-setup-027" and holds()["uploads"] is False
    # a superseding record still pending supersedes nothing yet: two live records are Sean's to settle
    record("2026-10-26-higgsfield-portal-launch-film-video", id="mc-setup-027", approved="pending",
           supersedes="mc-setup-025")
    with pytest.raises(higgsfield.Refused, match="mc-setup-025 and mc-setup-027 both cover mc-eng-003"):
        holds()
    # a third live record, superseding nothing, still refuses
    record("2026-10-26-higgsfield-portal-launch-film-video", id="mc-setup-027", approved="2026-10-26",
           supersedes="mc-setup-025")
    record("2026-10-27-higgsfield-another", id="mc-setup-028")
    with pytest.raises(higgsfield.Refused, match="mc-setup-027 and mc-setup-028 both cover mc-eng-003"):
        holds()
    # two records that supersede each other leave none standing, and say so
    record("2026-10-27-higgsfield-another", id="mc-setup-028", supersedes="mc-setup-027")
    record("2026-10-26-higgsfield-portal-launch-film-video", id="mc-setup-027", approved="2026-10-26",
           supersedes="[mc-setup-025, mc-setup-028]")
    with pytest.raises(higgsfield.Refused, match="supersede one another"):
        holds()
    # the field says approved-media, or nothing
    (setup / "2026-10-27-higgsfield-another" / "record.md").unlink()
    record("2026-10-26-higgsfield-portal-launch-film-video", id="mc-setup-027", approved="2026-10-26",
           supersedes="mc-setup-025", uploads="any")
    with pytest.raises(higgsfield.Refused, match="uploads: approved-media"):
        holds()


def test_only_an_entry_on_an_approved_list_is_sent(fresh):
    ctx, vdir = pass_of(fresh, "art-pose-designer", "appearance")
    r = take(fresh, ctx, "IM9", vdir / "x.png")
    assert r.returncode == 1 and "IM9 is not on the approved list mc-ap-020" in r.stderr
    # a list written but never approved is not sent, however it is worded
    draft = fresh["project"] / "appearance" / "higgsfield-draft-v01-2026-10-25"
    draft.mkdir()
    (draft / "higgsfield.json").write_text(json.dumps({**IMAGES, "entries": [{**IMAGES["entries"][0], "id": "IM3"}]}))
    r = take(fresh, ctx, "IM3", vdir / "y.png")
    assert r.returncode == 1 and "not on the approved list" in r.stderr
    # the Animator's newest list is of video: an image entry is never its to send
    a_ctx, a_vdir = pass_of(fresh, "animator", "motion")
    r = take(fresh, a_ctx, "IM1", a_vdir / "x.mp4")
    assert r.returncode == 1 and "no approved list of videos" in r.stderr
    assert sent(fresh) == []


def test_an_approved_copy_changed_since_is_refused(fresh):
    approved = approve(fresh, "029", "higgsfield-changed-v01-2026-10-25", IMAGES)
    try:
        (approved / "higgsfield.json").write_text(json.dumps({**IMAGES, "ceiling_credits": 2500}))
        ctx, vdir = pass_of(fresh, "art-pose-designer", "appearance")
        r = take(fresh, ctx, "IM1", vdir / "x.png")
        assert r.returncode == 1 and "no longer matches its approval mc-ap-029" in r.stderr
        assert sent(fresh) == []
    finally:
        withdraw(fresh, "029")


def test_a_take_over_the_tests_ceiling_or_the_trains_cap_is_refused_before_any_call(fresh):
    behave(fresh, cost=200)
    ctx, vdir = pass_of(fresh, "art-pose-designer", "appearance")
    assert take(fresh, ctx, "IM1", vdir / "a.png").returncode == 0
    r = take(fresh, ctx, "IM2", vdir / "b.png")
    assert r.returncode == 1 and "past its ceiling of 300 (200 spent)" in r.stderr and "checkpoint for Sean" in r.stderr
    assert len(sent(fresh)) == 1
    old = fresh["brief"].read_text()
    # the train's cap counts every test: a second test under its own ceiling still stops at the train's
    approve(fresh, "031", "higgsfield-film-v01-2026-10-25", {**IMAGES, "test": "film", "ceiling_credits": 250})
    try:
        fresh["brief"].write_text(old.replace("higgsfield_credits_cap: 2500", "higgsfield_credits_cap: 250"))
        behave(fresh, cost=60)
        r = take(fresh, ctx, "IM2", vdir / "c.png")
        assert r.returncode == 1 and "past its 250 Higgsfield credits (200 spent)" in r.stderr
        fresh["brief"].write_text(old.replace("higgsfield_credits_cap: 2500\n", ""))
        r = take(fresh, ctx, "IM2", vdir / "d.png")
        assert r.returncode == 1 and "needs higgsfield_credits_cap" in r.stderr
    finally:
        fresh["brief"].write_text(old)
        withdraw(fresh, "031")
    behave(fresh, cost=50)
    (fresh["state"] / "balance").write_text("10")
    r = take(fresh, ctx, "IM2", vdir / "e.png")
    assert r.returncode == 1 and "the account holds" in r.stderr and "never-do 7" in r.stderr
    assert len(sent(fresh)) == 1, "no refused take reached Higgsfield"


def test_a_ceiling_over_the_trains_cap_is_refused(fresh):
    approve(fresh, "030", "higgsfield-big-v01-2026-10-25", {**IMAGES, "ceiling_credits": 3000})
    try:
        ctx, vdir = pass_of(fresh, "art-pose-designer", "appearance")
        r = take(fresh, ctx, "IM1", vdir / "x.png")
        assert r.returncode == 1 and "over the train's cap" in r.stderr
    finally:
        withdraw(fresh, "030")


def test_three_takes_an_entry_counted_across_the_job_then_a_question_for_sean(fresh):
    for i in range(3):
        ctx, vdir = pass_of(fresh, "art-pose-designer", "appearance")
        assert take(fresh, ctx, "IM1", vdir / f"t{i}.png").returncode == 0
    ctx, vdir = pass_of(fresh, "art-pose-designer", "appearance")
    r = take(fresh, ctx, "IM1", vdir / "t3.png")
    assert r.returncode == 1 and "has had its 3 takes" in r.stderr
    assert take(fresh, ctx, "IM2", vdir / "other.png").returncode == 0, "another entry keeps its own takes"


def test_a_job_that_makes_nothing_and_charges_nothing_is_no_take(fresh):
    behave(fresh, job_fails=True, cost=2)
    ctx, vdir = pass_of(fresh, "art-pose-designer", "appearance")
    r = take(fresh, ctx, "IM1", vdir / "x.png")
    assert r.returncode == 1 and "no take was filed" in r.stderr
    last = job(fresh)[-1]
    assert last["credits"] == 0 and not last["made"] and not list(vdir.iterdir())
    behave(fresh, create_fails=True)
    r = take(fresh, ctx, "IM1", vdir / "y.png")
    assert r.returncode == 1 and "no job was read" in r.stderr and "Not enough credits" in r.stderr


def test_a_bare_list_of_job_ids_is_read_as_the_job(fresh):
    # `generate create` answers the real command line's way: a list of job ids (mc-eng-002's first live call)
    behave(fresh, create_shape="ids", cost=4)
    ctx, vdir, jid = art_take(fresh)
    side = json.loads((vdir / "house.higgsfield.json").read_text())
    assert side["job"] == jid and side["made"] and (vdir / "house.png").read_bytes() == PNG


def test_a_charged_call_with_no_job_read_still_counts_its_take_and_credits(fresh):
    behave(fresh, create_shape="garbled", cost=4)
    ctx, vdir = pass_of(fresh, "art-pose-designer", "appearance")
    r = take(fresh, ctx, "IM1", vdir / "house.png")
    jid = (fresh["state"] / "last-job").read_text()
    assert r.returncode == 1 and "no job was read" in r.stderr and jid in r.stderr and "settle" in r.stderr
    last = job(fresh)[-1]
    assert last["credits"] == 4 and not last["made"] and last["jobs_in_answer"] == [jid] and not list(vdir.iterdir())
    s = run(fresh, "status", "--context", ctx)
    assert "IM1 nano_banana_2: 1 of 3 takes used" in s.stdout and "sold-proof 4 of 300 credits" in s.stdout
    assert f"charged 4 credits with no job read (job ids in the answer: {jid})" in s.stdout


def test_settle_files_the_unfiled_job_as_the_same_take_with_nothing_spent_or_counted_twice(fresh):
    behave(fresh, create_shape="garbled", cost=4)
    first, vdir = pass_of(fresh, "art-pose-designer", "appearance")
    take(fresh, first, "IM1", vdir / "house.png")
    jid = (fresh["state"] / "last-job").read_text()
    creates = len(sent(fresh))
    ctx, vdir2 = pass_of(fresh, "art-pose-designer", "appearance")
    r = run(fresh, "settle", "--context", ctx, "--job", jid, "--out", str(vdir2 / "house.png"))
    assert r.returncode == 0, r.stderr
    assert "take 1 of 3, settled" in r.stdout and "4 credits, counted once" in r.stdout
    assert (vdir2 / "house.png").read_bytes() == PNG
    side = json.loads((vdir2 / "house.higgsfield.json").read_text())
    assert side["job"] == jid and side["made"] and side["take"] == 1 and side["credits"] == 4
    assert side["label"].startswith("generated: Higgsfield") and side["label"].endswith("under mc-setup-023") and side["settled_by"] and "error" not in side
    assert len(sent(fresh)) == creates, "settle reads and downloads; it never asks the generator again"
    s = run(fresh, "status", "--context", ctx)
    assert "IM1 nano_banana_2: 1 of 3 takes used" in s.stdout and "sold-proof 4 of 300 credits" in s.stdout
    # filed once: a second settle, a job the doorway never made, and the other kind's pass are each refused
    again = run(fresh, "settle", "--context", ctx, "--job", jid, "--out", str(vdir2 / "again.png"))
    assert again.returncode == 1 and "still unfiled" in again.stderr
    other = run(fresh, "settle", "--context", ctx, "--job", "00000000-0000-4000-8000-000000000000",
                "--out", str(vdir2 / "other.png"))
    assert other.returncode == 1 and "still unfiled" in other.stderr
    assert not (vdir2 / "again.png").exists() and not (vdir2 / "other.png").exists()


def test_settle_refuses_a_job_with_no_finished_result_and_writes_nothing(fresh):
    behave(fresh, create_shape="garbled", cost=4)
    first, vdir = pass_of(fresh, "art-pose-designer", "appearance")
    take(fresh, first, "IM1", vdir / "house.png")
    jid = (fresh["state"] / "last-job").read_text()
    behave(fresh, create_shape="garbled", cost=4, job_fails=True)
    ctx, vdir2 = pass_of(fresh, "art-pose-designer", "appearance")
    r = run(fresh, "settle", "--context", ctx, "--job", jid, "--out", str(vdir2 / "house.png"))
    assert r.returncode == 1 and "no finished result" in r.stderr and not list(vdir2.iterdir())


def test_no_call_before_seans_intended_use_approval(fresh):
    ctx, vdir = pass_of(fresh, "art-pose-designer", "appearance")
    try:
        fresh["setup"].write_text(setup_text(approved="pending"))
        r = take(fresh, ctx, "IM1", vdir / "x.png")
        assert r.returncode == 1 and "no intended-use approval from Sean yet" in r.stderr
        fresh["setup"].unlink()
        r = take(fresh, ctx, "IM1", vdir / "x.png")
        assert r.returncode == 1 and "no Higgsfield setup record covers mc-eng-900" in r.stderr
    finally:
        fresh["setup"].write_text(setup_text())
    assert sent(fresh) == []


def test_a_call_for_an_engagement_no_record_covers_is_refused(fresh):
    """Never-do 6 is per engagement: another film's approval, or another tool's, never covers this one."""
    ctx, vdir = pass_of(fresh, "art-pose-designer", "appearance")
    other = fresh["setup"].parent.parent / "2026-10-26-higgsfield-second" / "record.md"
    try:
        # mc-eng-002's record, approved, names only mc-eng-002
        fresh["setup"].write_text(setup_text(engagements="[mc-eng-002]"))
        r = take(fresh, ctx, "IM1", vdir / "x.png")
        assert r.returncode == 1 and "no Higgsfield setup record covers mc-eng-900" in r.stderr, r.stderr
        assert "refused" in job(fresh)[-1]
        # a record of another tool's intended use names this job, and still does not cover Higgsfield
        fresh["setup"].write_text(setup_text(tool="elevenlabs"))
        r = take(fresh, ctx, "IM1", vdir / "x.png")
        assert r.returncode == 1 and "no Higgsfield setup record covers mc-eng-900" in r.stderr
        # a record with no engagements line covers nothing, as mc-setup-023 did before it had one
        fresh["setup"].write_text(setup_text().replace("engagements: [mc-eng-900]\n", ""))
        r = take(fresh, ctx, "IM1", vdir / "x.png")
        assert r.returncode == 1 and "no Higgsfield setup record covers mc-eng-900" in r.stderr
        # a name that only starts like this job's id is not this job
        fresh["setup"].write_text(setup_text(engagements="[mc-eng-9000, mc-eng-90]"))
        r = take(fresh, ctx, "IM1", vdir / "x.png")
        assert r.returncode == 1 and "no Higgsfield setup record covers mc-eng-900" in r.stderr
        # two records for one job is a question for Sean, never a pick
        fresh["setup"].write_text(setup_text())
        other.parent.mkdir()
        other.write_text(setup_text(id="mc-setup-099", engagements="[mc-eng-002, mc-eng-900]"))
        r = take(fresh, ctx, "IM1", vdir / "x.png")
        assert r.returncode == 1 and "mc-setup-023 and mc-setup-099 both cover mc-eng-900" in r.stderr, r.stderr
    finally:
        fresh["setup"].write_text(setup_text())
        if other.exists():
            other.unlink()
            other.parent.rmdir()
    assert sent(fresh) == []
    # the job's own record, listed among others, covers it
    fresh["setup"].write_text(setup_text(engagements="[mc-eng-002, mc-eng-900]"))
    try:
        r = take(fresh, ctx, "IM1", vdir / "x.png")
        assert r.returncode == 0, r.stderr
        assert json.loads((vdir / "x.higgsfield.json").read_text())["setup"] == "mc-setup-023"
    finally:
        fresh["setup"].write_text(setup_text())


def test_mc_eng_002_still_passes_on_mc_setup_023_and_mc_eng_003_does_not(tmp_path):
    """The ledger's own shape: mc-setup-023 names mc-eng-002, and mc-eng-003 waits on a record of its own."""
    import higgsfield
    setup = tmp_path / "ledger" / "setup"
    (setup / "2026-10-25-higgsfield-intended-use").mkdir(parents=True)
    (setup / "2026-10-25-higgsfield-intended-use" / "record.md").write_text(
        setup_text(engagements="[mc-eng-002]  # the train it covers"))
    (setup / "2026-10-25-font-poppins").mkdir()
    (setup / "2026-10-25-font-poppins" / "record.md").write_text("---\nid: mc-setup-024\nengagements: [mc-eng-003]\n---\n")
    engs = tmp_path / "ledger" / "engagements"
    for folder, eid in (("agent-portal-launch-2026-10-24", "mc-eng-002"), ("portal-launch-film-2026-10-25", "mc-eng-003")):
        (engs / folder).mkdir(parents=True)
        (engs / folder / "brief.md").write_text(f"---\nid: {eid}\ntype: full-train\nhiggsfield_credits_cap: 1000\n---\n")
    got = higgsfield.setup_record({"engagement": str(engs / "agent-portal-launch-2026-10-24")})
    assert got["id"] == "mc-setup-023" and got["approved"] == "2026-10-25" and got["engagement"] == "mc-eng-002"
    with pytest.raises(higgsfield.Refused, match="no Higgsfield setup record covers mc-eng-003"):
        higgsfield.setup_record({"engagement": str(engs / "portal-launch-film-2026-10-25")})
    # mc-eng-003's draft, pending Sean, still refuses
    (setup / "2026-10-25-higgsfield-portal-launch-film").mkdir()
    (setup / "2026-10-25-higgsfield-portal-launch-film" / "record.md").write_text(
        setup_text(id="mc-setup-025", engagements="[mc-eng-003]", approved="pending"))
    with pytest.raises(higgsfield.Refused, match="mc-setup-025 has no intended-use approval from Sean yet"):
        higgsfield.setup_record({"engagement": str(engs / "portal-launch-film-2026-10-25")})
    assert higgsfield.setup_record({"engagement": str(engs / "agent-portal-launch-2026-10-24")})["id"] == "mc-setup-023"


@pytest.mark.parametrize("seat_name,stage,extra", [("finishing-sound-designer", "finish", ()),
                                                   ("visual-story-director", "story", ()),
                                                   ("art-pose-designer", "appearance", ("--read-only",))])
def test_only_arts_and_the_animators_drafting_passes_may_call(fresh, seat_name, stage, extra):
    ctx, vdir = pass_of(fresh, seat_name, stage, *extra)
    r = take(fresh, ctx, "IM1", vdir / "x.png")
    assert r.returncode == 1 and "may not call Higgsfield" in r.stderr
    assert sent(fresh) == []


def test_the_take_lands_only_in_a_new_version_folder_in_the_seats_own_stage(fresh):
    ctx, vdir = pass_of(fresh, "art-pose-designer", "appearance")
    p = fresh["project"]
    for out, why in ((p / "motion" / "gen-v01-2026-10-25" / "x.png", "directly in this seat's stage"),
                     (p / "appearance" / "x.png", "directly in this seat's stage"),
                     (vdir / "x.mp4", "names a .png"),
                     (p / "appearance" / "not-made-v09-2026-10-25" / "x.png", "make the version folder")):
        r = take(fresh, ctx, "IM1", out)
        assert r.returncode == 1 and why in r.stderr, (out, r.stderr)
    (vdir / "x.png").write_bytes(b"mine")
    r = take(fresh, ctx, "IM1", vdir / "x.png")
    assert r.returncode == 1 and "a take is written once" in r.stderr
    saved = p / "appearance" / "saved-v01-2026-10-24"
    saved.mkdir()
    later = context(fresh, "art-pose-designer", f"h{os.urandom(2).hex()}")
    r = take(fresh, later, "IM1", saved / "x.png")
    assert r.returncode == 1 and "saved before this pass" in r.stderr
    assert sent(fresh) == []


def test_a_take_that_cannot_be_filed_is_kept_in_scratch_and_counts(fresh):
    result(fresh, b"<html>not an image</html>")
    ctx, vdir = pass_of(fresh, "art-pose-designer", "appearance")
    r = take(fresh, ctx, "IM1", vdir / "x.png")
    assert r.returncode == 1 and "could not be filed" in r.stderr
    last = job(fresh)[-1]
    assert last["made"] and Path(last["kept_in_scratch"]).read_bytes() == b"<html>not an image</html>"
    assert not list(vdir.iterdir())


def test_status_lists_the_entries_takes_and_spend_and_makes_nothing(fresh):
    art_take(fresh)
    ctx, _ = pass_of(fresh, "art-pose-designer", "appearance")
    r = run(fresh, "status", "--context", ctx)
    assert r.returncode == 0, r.stderr
    assert "IM1 nano_banana_2: 1 of 3 takes used" in r.stdout and "sold-proof 2 of 300 credits; train 2 of 2500" in r.stdout
    assert len(sent(fresh)) == 1


def test_a_pass_reaches_the_doorway_only_by_asking_the_launcher(fresh, monkeypatch):
    for k, v in fresh["env"].items():
        monkeypatch.setenv(k, v)
    ctx_path = context(fresh, "art-pose-designer", f"h{os.urandom(2).hex()}")
    c = ctx_data(ctx_path)
    c["source"] = ctx_path
    srv = apps.AppServer(c, time.time() + 600)
    try:
        def ask(h, **top):
            rid = f"higgsfield-{time.strftime('%H%M%S')}-{os.urandom(3).hex()}"
            (srv.requests / f"{rid}.json").write_text(json.dumps({"id": rid, "app": "higgsfield", "timeout": 120,
                                                                  "higgsfield": h, **top}))
            srv.handle(f"{rid}.json")
            return json.loads((srv.results / f"{rid}.result.json").read_text()), (srv.results / f"{rid}.log")
        res, log = ask({"status": True})
        assert res["ok"] and "IM1 nano_banana_2" in log.read_text()
        res, log = ask({"entry": "IM9", "out": str(fresh["project"] / "appearance" / "x-v01-2026-10-25" / "x.png")})
        assert not res["ok"] and "not on the approved list" in log.read_text()
        res, _ = ask({"entry": "rm -rf", "out": "x.png"})
        assert "ask higgsfield --entry" in res["refused"]
        res, _ = ask({"status": True}, script="x.py")
        assert "an entry and a file, or a status" in res["refused"]
    finally:
        os.close(srv.fd)
    assert sent(fresh) == []


def test_the_prompt_tells_art_and_the_animator_to_ask_on_either_vendor(fresh, monkeypatch):
    for k, v in fresh["env"].items():
        monkeypatch.setenv(k, v)
    import importlib
    import seat as seatmod
    importlib.reload(seatmod)
    try:
        art = seatmod.load(context(fresh, "art-pose-designer", f"h{os.urandom(2).hex()}"))
        animator = seatmod.load(context(fresh, "animator", f"h{os.urandom(2).hex()}"))
        assert art["vendor"] == "claude" and animator["vendor"] == "codex"
        assert art["toolbelt"]["higgsfield"] == "image" and animator["toolbelt"]["higgsfield"] == "video"
        ask = f"{seatmod.APPS_DOOR} ask higgsfield --entry"
        assert ask in seatmod.claude_prompt(art, "do the work") and "<IM<n>>" in seatmod.claude_prompt(art, "x")
        assert ask in seatmod.codex_prompt(animator, "do the work") and "<VI<n>>" in seatmod.codex_prompt(animator, "x")
        for s in ("visual-story-director", "finishing-sound-designer"):
            other = seatmod.load(context(fresh, s, f"h{os.urandom(2).hex()}"))
            assert other["toolbelt"]["higgsfield"] == "" and "ask higgsfield" not in seatmod.claude_prompt(other, "x")
        audit = seatmod.load(context(fresh, "art-pose-designer", f"h{os.urandom(2).hex()}", "--read-only"))
        assert audit["toolbelt"]["higgsfield"] == "" and "ask higgsfield" not in seatmod.claude_prompt(audit, "x")
        # the sign-in is on every pass's credential wall, and no Claude pass may run the command line itself
        assert any(seatmod.under(os.path.expanduser("~/.config/higgsfield"), p) for p in seatmod.CREDENTIAL_PATHS)
        assert "Bash(higgsfield:*)" in seatmod.claude_settings(art)["permissions"]["deny"]
    finally:
        monkeypatch.undo()  # the environment back first, so the module the later tests share reads their settings
        importlib.reload(seatmod)


def test_the_allowlist_gives_higgsfield_only_to_art_for_images_and_the_animator_for_video(fresh, monkeypatch):
    belts = fresh["root"] / "toolbelts.toml"
    old = belts.read_text()
    try:
        belts.write_text(old.replace('higgsfield = "image"', 'higgsfield = "video"'))
        r = subprocess.run([sys.executable, str(LAUNCHER / "seat.py"), "context", "--seat", "art-pose-designer",
                            "--engagement", str(fresh["eng"]), "--pass", f"h{os.urandom(2).hex()}"],
                           env=fresh["env"], capture_output=True, text=True)
        assert r.returncode == 1 and "Art alone makes images there and the Animator video" in r.stderr
    finally:
        belts.write_text(old)


def test_the_launcher_takes_a_settle_request_only_as_a_job_id_and_a_file():
    sys.path.insert(0, str(LAUNCHER))
    import apps
    check = lambda h: apps.AppServer.check_higgsfield(None, {"higgsfield": h})
    job = "be4ac502-797e-49c7-b640-206d7bb055b0"
    ok = check({"settle": job, "out": "/m/appearance/x-v01-2026-10-25/IM1-take1.png"})
    assert ok["argv"] == ["settle", "--job", job, "--out", "/m/appearance/x-v01-2026-10-25/IM1-take1.png"]
    for bad in ({"settle": "job:" + job, "out": "/m/x.png"}, {"settle": job, "out": "x.png"},
                {"settle": job, "out": "/m/x.png", "entry": "IM1"}, {"settle": "../etc", "out": "/m/x.png"}):
        with pytest.raises(ValueError):
            check(bad)
