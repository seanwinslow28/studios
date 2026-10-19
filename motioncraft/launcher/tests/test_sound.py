"""Motioncraft's sound doorway: the approved cue list, the takes, the caps, the fence and the filing.

The doorway runs as a pass would run it, in its own process, with its network calls
answered by a fake of ElevenLabs and the Gemini API (patched in by a small harness,
never by a setting a pass could change) and a test keys file. The test world, its
context and its fence are the launcher tests' own (test_seat.py).
"""
from __future__ import annotations

import base64
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from test_seat import LAUNCHER, context, ctx_data, world  # noqa: F401

sys.path.insert(0, str(LAUNCHER))
import seat as seatmod  # noqa: E402
from tracekit.engagement import sha256_path  # noqa: E402

LIST_ID = "sound-plan-v01-2026-10-19"
CUES = [
    {"id": "FX1", "moment": "SP1", "tool": "effect", "prompt": "a soft paper brush stroke", "duration_s": 1.5},
    {"id": "FX2", "moment": "SP2", "tool": "effect", "prompt": "a small wooden tap", "loop": False, "prompt_influence": 0.5},
    {"id": "MU1", "moment": "SP3", "tool": "music", "model": "lyria-3-clip-preview", "prompt": "quiet felt piano, instrumental"},
]

# The fake services: the subscription read, the sound effect and Lyria. State lives in a folder the test reads.
HARNESS = r'''
import base64, json, os, sys
from pathlib import Path
sys.path.insert(0, os.environ["SOUND_LAUNCHER"])
import sound
state = Path(os.environ["SOUND_FAKE"])
b = json.loads((state / "behavior.json").read_text())
sound.KEYS = Path(os.environ["SOUND_KEYS"])
sound.METER_POLL_S = 0
sound.METER_WAIT_S = 0.5

def http(method, url, headers, body):
    calls = state / "calls.jsonl"
    with open(calls, "a") as f:
        f.write(json.dumps({"method": method, "url": url, "headers": sorted(headers),
                            "keys": [v for k, v in headers.items() if "key" in k.lower()],
                            "body": json.loads(body) if body else None}) + "\n")
    used, pending = state / "used", state / "pending"
    n = int(used.read_text()) if used.exists() else 1000
    if url == sound.SUBSCRIPTION_URL:
        # the account's count moves only after `lag` reads following a take, as the live one did
        if pending.exists():
            left, cost = map(int, pending.read_text().split())
            if left <= 0:
                n += cost
                used.write_text(str(n))
                pending.unlink()
            else:
                pending.write_text(f"{left - 1} {cost}")
        return 200, json.dumps({"character_count": n, "character_limit": 300000}).encode()
    if url.startswith(sound.EFFECTS_URL):
        if b.get("status", 200) != 200:
            return b["status"], b'{"detail": {"message": "invalid api key"}}'
        if b.get("cost", 200):
            pending.write_text(f"{b.get('lag', 0)} {b.get('cost', 200)}")
        return 200, b.get("effect", "ID3fake effect").encode("latin-1")
    if url == sound.MUSIC_URL:
        if b.get("status", 200) != 200:
            return b["status"], b'{"error": {"message": "quota"}}'
        audio = b.get("music", "ID3fake music").encode("latin-1")
        return 200, json.dumps({"id": "i1", "steps": [{"type": "model_output", "content": [
            {"type": "text", "text": "[Instrumental]"},
            {"type": "audio", "data": base64.b64encode(audio).decode()}]}]}).encode()
    return 404, b"no such fake"

sound.http = http
sys.argv = ["sound.py"] + sys.argv[1:]
sound.main()
'''


@pytest.fixture(scope="module")
def sw(world):
    """The test world with the brief's sound caps, an approved cue list, and its approvals entry."""
    brief = world["eng"] / "brief.md"
    old_brief = brief.read_text()
    brief.write_text(old_brief.replace("media:", "spend_cap_usd: 10\nsound_credits_cap: 1000\nmedia:", 1))
    approved = world["project"] / "approved" / LIST_ID
    approved.mkdir(parents=True)
    (approved / "cues.json").write_text(json.dumps({"cues": CUES}, indent=2))
    approvals = world["root"] / "ledger" / "approvals"
    approvals.mkdir(parents=True, exist_ok=True)
    entry = approvals / "007-2026-10-19-sound-plan.md"
    entry.write_text(f"---\nid: mc-ap-007\nversion_id: {LIST_ID}\nversion_path: media:{world['project'].relative_to(world['root'] / 'media')}/approved/{LIST_ID}\n"
                     f"version_sha256: {sha256_path(approved)}\ndecision: approved\n---\n\nApproved.\n")
    keys = world["root"] / "audio-keys" / "keys.env"
    keys.parent.mkdir()
    keys.write_text("export GEMINI_API_KEY=test-gemini\nexport ELEVENLABS_API_KEY=test-eleven\n")
    state = world["root"] / "soundfake"
    state.mkdir()
    (state / "harness.py").write_text(HARNESS)
    world.update(approved=approved, entry=entry, keys=keys, state=state)
    yield world
    brief.write_text(old_brief)


@pytest.fixture()
def take(sw):
    """A drafting Finishing pass's context and a new version folder in its stage; a fresh fake and a fresh job log."""
    n = f"s{os.urandom(2).hex()}"
    ctx = context(sw, "finishing-sound-designer", n)
    vdir = sw["project"] / "finish" / f"sound{n}-v01-2026-10-19"
    vdir.mkdir()
    for f in sw["state"].glob("*"):
        if f.name != "harness.py":
            f.unlink()
    behave(sw)
    logs = sw["eng"] / "trace" / "logs"
    for f in logs.glob("*.sounds.jsonl"):
        f.unlink()
    return {"ctx": ctx, "vdir": vdir, "n": n}


def behave(w, **b):
    (w["state"] / "behavior.json").write_text(json.dumps(b))


def run(w, *args):
    env = dict(w["env"], SOUND_LAUNCHER=str(LAUNCHER), SOUND_FAKE=str(w["state"]), SOUND_KEYS=str(w["keys"]))
    return subprocess.run([sys.executable, str(w["state"] / "harness.py"), *args], env=env, capture_output=True,
                          text=True, timeout=60)


def calls(w):
    f = w["state"] / "calls.jsonl"
    return [json.loads(x) for x in f.read_text().splitlines()] if f.exists() else []


def job(w):
    return [json.loads(x) for f in sorted((w["eng"] / "trace" / "logs").glob("*.sounds.jsonl"))
            for x in f.read_text().splitlines()]


def test_an_effect_take_is_filed_with_its_approved_prompt_beside_it(sw, take):
    out = take["vdir"] / "fx1-a.mp3"
    r = run(sw, "--context", take["ctx"], "--cue", "FX1", "--out", str(out))
    assert r.returncode == 0, r.stderr
    assert out.read_bytes() == b"ID3fake effect" and "FX1 take 1 of 3" in r.stdout and "200 of 1000 credits" in r.stdout
    side = json.loads((take["vdir"] / "fx1-a.sound.json").read_text())
    assert side["label"].startswith("generated: ElevenLabs") and "mc-ap-007" in side["label"]
    assert side["approved_cue"] == CUES[0] and side["sha256"] == seatmod.sha256(out) and side["credits"] == 200
    assert side["approval"]["approval"] == "mc-ap-007" and side["take"] == 1
    sent = [c for c in calls(sw) if c["method"] == "POST"]
    assert len(sent) == 1 and sent[0]["body"] == {"text": "a soft paper brush stroke", "model_id": "eleven_text_to_sound_v2",
                                                  "loop": False, "duration_seconds": 1.5}
    assert "output_format=mp3_44100_192" in sent[0]["url"] and sent[0]["keys"] == ["test-eleven"]
    # the key went to the service and nowhere else: not the sidecar, the log or the output
    for text in ((take["vdir"] / "fx1-a.sound.json").read_text(), json.dumps(job(sw)), r.stdout, r.stderr):
        assert "test-eleven" not in text and "test-gemini" not in text
    again = run(sw, "--context", take["ctx"], "--cue", "FX1", "--out", str(out))
    assert again.returncode == 1 and "written once" in again.stderr


def test_a_music_take_is_priced_and_its_words_flagged(sw, take):
    out = take["vdir"] / "mu1-a.mp3"
    r = run(sw, "--context", take["ctx"], "--cue", "MU1", "--out", str(out))
    assert r.returncode == 0, r.stderr
    assert out.read_bytes() == b"ID3fake music" and "$0.04 of $10.00" in r.stdout and "sung words" in r.stdout
    side = json.loads((take["vdir"] / "mu1-a.sound.json").read_text())
    assert side["usd"] == 0.04 and side["words"] == ["[Instrumental]"] and side["model"] == "lyria-3-clip-preview"
    post = [c for c in calls(sw) if c["method"] == "POST"][0]
    assert post["body"] == {"model": "lyria-3-clip-preview", "input": "quiet felt piano, instrumental"}
    assert post["keys"] == ["test-gemini"]


def test_a_wav_answer_is_filed_as_wav(sw, take):
    behave(sw, music="RIFF\x00\x00\x00\x00WAVEfmt ")
    r = run(sw, "--context", take["ctx"], "--cue", "MU1", "--out", str(take["vdir"] / "mu1-w.mp3"))
    assert r.returncode == 0, r.stderr
    assert (take["vdir"] / "mu1-w.wav").is_file() and not (take["vdir"] / "mu1-w.mp3").exists()


def test_three_takes_a_cue_then_a_question_for_sean(sw, take):
    for i in range(3):
        assert run(sw, "--context", take["ctx"], "--cue", "FX2", "--out", str(take["vdir"] / f"fx2-{i}.mp3")).returncode == 0
    r = run(sw, "--context", take["ctx"], "--cue", "FX2", "--out", str(take["vdir"] / "fx2-3.mp3"))
    assert r.returncode == 1 and "has had its 3 takes" in r.stderr and not (take["vdir"] / "fx2-3.mp3").exists()
    assert len([c for c in calls(sw) if c["method"] == "POST"]) == 3
    assert job(sw)[-1]["refused"].startswith("FX2 has had its 3 takes")
    status = run(sw, "--context", take["ctx"], "--status")
    assert status.returncode == 0 and "FX2 SP2 effect" in status.stdout and "3 of 3 takes used" in status.stdout


def test_the_takes_count_across_the_job_not_the_pass(sw, take):
    for i in range(2):
        assert run(sw, "--context", take["ctx"], "--cue", "FX1", "--out", str(take["vdir"] / f"a{i}.mp3")).returncode == 0
    n = f"t{os.urandom(2).hex()}"
    ctx2 = context(sw, "finishing-sound-designer", n)
    vdir2 = sw["project"] / "finish" / f"sound{n}-v01-2026-10-19"
    vdir2.mkdir()
    assert run(sw, "--context", ctx2, "--cue", "FX1", "--out", str(vdir2 / "a2.mp3")).returncode == 0
    r = run(sw, "--context", ctx2, "--cue", "FX1", "--out", str(vdir2 / "a3.mp3"))
    assert r.returncode == 1 and "has had its 3 takes" in r.stderr


def test_the_caps_stop_a_take_before_any_call(sw, take):
    logs = sw["eng"] / "trace" / "logs"
    (logs / "pass-zz.sounds.jsonl").write_text(json.dumps({"usd": 9.97, "credits": 900, "made": False}) + "\n")
    r = run(sw, "--context", take["ctx"], "--cue", "MU1", "--out", str(take["vdir"] / "m.mp3"))
    assert r.returncode == 1 and "past its $10.00 spend cap" in r.stderr and "checkpoint for Sean" in r.stderr
    r = run(sw, "--context", take["ctx"], "--cue", "FX1", "--out", str(take["vdir"] / "f.mp3"))
    assert r.returncode == 1 and "past its 1000 ElevenLabs credits" in r.stderr
    assert not [c for c in calls(sw) if c["method"] == "POST"], "no refused take reaches a service"


def test_only_a_cue_on_the_approved_list_is_sent(sw, take):
    r = run(sw, "--context", take["ctx"], "--cue", "FX9", "--out", str(take["vdir"] / "x.mp3"))
    assert r.returncode == 1 and "not on the approved cue list mc-ap-007" in r.stderr
    r = run(sw, "--context", take["ctx"], "--cue", "FX1", "--prompt", "louder")
    assert r.returncode == 2, "a take has no prompt of its own to give"
    assert not calls(sw)


def test_an_approved_copy_changed_since_is_refused(sw, take):
    f = sw["approved"] / "cues.json"
    old = f.read_text()
    f.write_text(old.replace("soft paper", "loud paper"))
    try:
        r = run(sw, "--context", take["ctx"], "--cue", "FX1", "--out", str(take["vdir"] / "x.mp3"))
        assert r.returncode == 1 and "no longer matches its approval mc-ap-007" in r.stderr
    finally:
        f.write_text(old)
    assert not calls(sw)


def test_no_approved_list_no_sound(sw, take):
    old = sw["entry"].read_text()
    sw["entry"].write_text(old.replace("decision: approved", "decision: artistic retake"))
    try:
        r = run(sw, "--context", take["ctx"], "--cue", "FX1", "--out", str(take["vdir"] / "x.mp3"))
        assert r.returncode == 1 and "no approved cue list for this job" in r.stderr
    finally:
        sw["entry"].write_text(old)


def test_a_list_naming_a_setting_the_doorway_does_not_send_is_refused(sw, take):
    bad = sw["project"] / "approved" / "sound-plan-v02-2026-10-19"
    bad.mkdir()
    (bad / "cues.json").write_text(json.dumps({"cues": [dict(CUES[0], output_format="pcm_48000")]}))
    entry = sw["entry"].with_name("008-2026-10-19-sound-plan-v02.md")
    entry.write_text(sw["entry"].read_text().replace(LIST_ID, bad.name).replace("mc-ap-007", "mc-ap-008")
                     .replace(sha256_path(sw["approved"]), sha256_path(bad)))
    try:
        r = run(sw, "--context", take["ctx"], "--cue", "FX1", "--out", str(take["vdir"] / "x.mp3"))
        assert r.returncode == 1 and "output_format, which the doorway does not send" in r.stderr
    finally:
        entry.unlink()


@pytest.mark.parametrize("seat_name,extra", [("finishing-sound-designer", ("--read-only",)), ("visual-story-director", ()),
                                             ("animator", ())])
def test_only_a_drafting_finishing_pass_may_use_the_door(sw, take, seat_name, extra):
    ctx = context(sw, seat_name, f"j{os.urandom(2).hex()}", *extra)
    r = run(sw, "--context", ctx, "--cue", "FX1", "--out", str(take["vdir"] / "z.mp3"))
    assert r.returncode == 1 and "may not call the sound path" in r.stderr


def test_the_door_reads_only_a_context_in_trace_logs(sw, take):
    forged = Path(ctx_data(take["ctx"])["scratch"]) / "pass-99.context.json"
    forged.write_text(Path(take["ctx"]).read_text())
    r = run(sw, "--context", str(forged), "--cue", "FX1", "--out", str(take["vdir"] / "z.mp3"))
    assert r.returncode == 1 and "only the coordinator writes" in r.stderr


def test_the_door_refuses_outside_the_pass_fence(sw, take):
    finish = sw["project"] / "finish"
    saved = finish / "saved-v01-2026-10-19"
    saved.mkdir(exist_ok=True)
    ctx = context(sw, "finishing-sound-designer", f"k{os.urandom(2).hex()}")  # written after `saved`, so it is frozen
    vdir = finish / f"new{os.urandom(2).hex()}-v01-2026-10-19"
    vdir.mkdir()
    cases = [
        (saved / "x.mp3", "saved before this pass"),
        (finish / "x.mp3", "version folder directly in this seat's stage"),
        (sw["project"] / "motion" / "m-v01-2026-10-19" / "x.mp3", "version folder directly"),
        (sw["eng"] / "artifacts" / "x.mp3", "version folder directly"),
        (vdir / "x.wav", "names a .mp3"),
        (finish / "absent-v09-2026-10-19" / "x.mp3", "make the version folder"),
    ]
    for out, why in cases:
        r = run(sw, "--context", ctx, "--cue", "FX1", "--out", str(out))
        assert r.returncode == 1 and why in r.stderr, (out, r.stderr)
    assert not calls(sw), "no refused call reaches a service"


def test_the_door_never_writes_through_a_planted_link(sw, take):
    target = sw["root"] / "outside-sound.json"
    (take["vdir"] / "linked.sound.json").symlink_to(target)  # dangling
    r = run(sw, "--context", take["ctx"], "--cue", "FX1", "--out", str(take["vdir"] / "linked.mp3"))
    assert r.returncode == 1 and not target.exists() and not (take["vdir"] / "linked.mp3").exists()
    assert not calls(sw)


def test_a_failed_call_files_nothing_and_is_no_take(sw, take):
    behave(sw, status=401)
    r = run(sw, "--context", take["ctx"], "--cue", "FX1", "--out", str(take["vdir"] / "e.mp3"))
    assert r.returncode == 1 and "no sound was made (HTTP 401" in r.stderr and not (take["vdir"] / "e.mp3").exists()
    assert job(sw)[-1]["made"] is False and job(sw)[-1]["credits"] == 0
    behave(sw)
    assert run(sw, "--context", take["ctx"], "--cue", "FX1", "--out", str(take["vdir"] / "e2.mp3")).returncode == 0
    assert job(sw)[-1]["take"] == 1


def test_audio_that_cannot_be_filed_is_kept_in_scratch_and_counts(sw, take):
    behave(sw, effect="not audio at all")
    r = run(sw, "--context", take["ctx"], "--cue", "FX1", "--out", str(take["vdir"] / "u.mp3"))
    assert r.returncode == 1 and "could not be filed" in r.stderr and not (take["vdir"] / "u.mp3").exists()
    kept = Path(job(sw)[-1]["kept_in_scratch"])
    assert kept.read_bytes() == b"not audio at all" and kept.parent == Path(ctx_data(take["ctx"])["scratch"])
    assert job(sw)[-1]["made"] is True


def test_a_brief_without_both_caps_makes_no_sound(sw, take):
    brief = sw["eng"] / "brief.md"
    old = brief.read_text()
    brief.write_text(old.replace("sound_credits_cap: 1000\n", ""))
    try:
        r = run(sw, "--context", take["ctx"], "--cue", "FX1", "--out", str(take["vdir"] / "c.mp3"))
        assert r.returncode == 1 and "needs spend_cap_usd and sound_credits_cap" in r.stderr
    finally:
        brief.write_text(old)


def test_the_meter_waits_for_the_account_to_move(sw, take):
    behave(sw, cost=15, lag=3)  # the live take: 15 credits, shown a few reads late
    r = run(sw, "--context", take["ctx"], "--cue", "FX1", "--out", str(take["vdir"] / "lag.mp3"))
    assert r.returncode == 0, r.stderr
    assert job(sw)[-1]["credits"] == 15 and job(sw)[-1]["credits_source"].startswith("the account's character_count")


def test_a_count_that_never_moves_is_charged_the_estimate(sw, take):
    behave(sw, cost=0)
    r = run(sw, "--context", take["ctx"], "--cue", "FX1", "--out", str(take["vdir"] / "still.mp3"))
    assert r.returncode == 0, r.stderr
    assert job(sw)[-1]["credits"] == 200 and job(sw)[-1]["credits_source"].startswith("estimate")
