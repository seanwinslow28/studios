"""Motioncraft's Higgsfield doorway: the approved list, no upload, the takes, the credit caps, the fence and the filing.

The doorway runs as the launcher runs it, in its own process, calling a fake `higgsfield`
command line that the test allowlist names (the real one's answers, from `higgsfield`
1.1.23, read 2026-10-25), which keeps the account's balance and records every call it is
given. Only the download of a finished take is patched in, by a small harness. The test
world, its context and its fence are the launcher tests' own (test_seat.py).
"""
from __future__ import annotations

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
    out([{{"id": jid, "job_type": words[2], "status": "queued"}}])
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
id: mc-setup-023
date: 2026-10-25
step: "Higgsfield's data-use and training settings, and Sean's intended-use approval (SWCB #271)"
intended_use_approved: {approved}
---

The record.
"""


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
    setup.write_text(SETUP.format(approved="2026-10-25"))
    world.update(state=state, fake=fake, setup=setup, brief=brief)
    approve(world, "020", "higgsfield-images-v01-2026-10-25", IMAGES)
    yield world
    belts.write_text(old_belts)
    brief.write_text(old_brief)


def approve(w, n, version, doc):
    """Sean's approval of a list: its locked copy in approved/, named by an approvals entry with its folder hash."""
    approved = w["project"] / "approved" / version
    approved.mkdir(parents=True)
    (approved / "higgsfield.json").write_text(json.dumps(doc, indent=2))
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
        assert r.returncode == 1 and "no take this doorway made" in r.stderr and "nothing is uploaded" in r.stderr
        assert sent(fresh) == []
    finally:
        withdraw(fresh, "028")


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
    assert r.returncode == 1 and "no job was made" in r.stderr and "Not enough credits" in r.stderr


def test_no_call_before_seans_intended_use_approval(fresh):
    ctx, vdir = pass_of(fresh, "art-pose-designer", "appearance")
    try:
        fresh["setup"].write_text(SETUP.format(approved="pending"))
        r = take(fresh, ctx, "IM1", vdir / "x.png")
        assert r.returncode == 1 and "no intended-use approval from Sean yet" in r.stderr
        fresh["setup"].unlink()
        r = take(fresh, ctx, "IM1", vdir / "x.png")
        assert r.returncode == 1 and "no setup record mc-setup-023" in r.stderr
    finally:
        fresh["setup"].write_text(SETUP.format(approved="2026-10-25"))
    assert sent(fresh) == []


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
