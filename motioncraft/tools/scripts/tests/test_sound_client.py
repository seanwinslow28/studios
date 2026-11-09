"""The sound client, with the network replaced: keys, request bodies, answers and the command line."""
import base64
import json

import pytest

import sound_client as sc


def test_a_key_comes_from_the_environment_first(monkeypatch, tmp_path):
    keys = tmp_path / "keys.env"
    keys.write_text("export ELEVENLABS_API_KEY='from-file'\n")
    monkeypatch.setenv("ELEVENLABS_API_KEY", "from-env")
    assert sc.key("ELEVENLABS_API_KEY", keys) == "from-env"
    monkeypatch.delenv("ELEVENLABS_API_KEY")
    assert sc.key("ELEVENLABS_API_KEY", keys) == "from-file"
    with pytest.raises(sc.SoundError, match="no GEMINI_API_KEY"):
        sc.key("GEMINI_API_KEY", keys)


def test_an_effect_body_is_checked():
    assert sc.effect_body("door slam", 1.5, influence=0.6) == {
        "text": "door slam", "model_id": sc.EFFECTS_MODEL, "loop": False, "duration_seconds": 1.5, "prompt_influence": 0.6}
    for bad in (dict(prompt=" "), dict(prompt="x", seconds=40), dict(prompt="x", influence=2)):
        with pytest.raises(sc.SoundError):
            sc.effect_body(**bad)


def test_make_effect_sends_only_the_prompt(monkeypatch):
    seen = {}

    def fake(method, url, headers, body):
        seen.update(method=method, url=url, headers=headers, body=json.loads(body))
        return 200, b"ID3fake-mp3"
    monkeypatch.setenv("ELEVENLABS_API_KEY", "k")
    monkeypatch.setattr(sc, "http", fake)
    assert sc.make_effect("whoosh", 2.0) == b"ID3fake-mp3"
    assert seen["method"] == "POST" and seen["url"].endswith("output_format=" + sc.EFFECTS_FORMAT)
    assert seen["body"]["text"] == "whoosh" and seen["headers"]["xi-api-key"] == "k"


def test_a_failed_effect_says_why(monkeypatch):
    monkeypatch.setenv("ELEVENLABS_API_KEY", "k")
    monkeypatch.setattr(sc, "http", lambda *a: (401, b'{"detail": "bad key"}'))
    with pytest.raises(sc.SoundError, match="HTTP 401"):
        sc.make_effect("whoosh")


def test_a_lyria_answer_gives_its_audio_and_words(monkeypatch):
    wav = b"RIFF\0\0\0\0WAVEfmt "
    answer = {"outputs": [{"type": "text", "text": "Verse one."}, {"type": "audio", "data": base64.b64encode(wav).decode()}]}
    monkeypatch.setenv("GEMINI_API_KEY", "g")
    monkeypatch.setattr(sc, "http", lambda *a: (200, json.dumps(answer).encode()))
    audio, words = sc.make_music("warm piano", "lyria-3.5")
    assert audio == wav and words == ["Verse one."] and sc.sniff(audio) == "wav"
    with pytest.raises(sc.SoundError, match="music model"):
        sc.make_music("warm piano", "lyria-old")


def test_the_command_line_writes_a_take_once(monkeypatch, tmp_path, capsys):
    monkeypatch.setenv("ELEVENLABS_API_KEY", "k")
    monkeypatch.setattr(sc, "credits_used", lambda: (100, 1000))
    monkeypatch.setattr(sc, "settled", lambda before: (115, 1000))
    monkeypatch.setattr(sc, "http", lambda *a: (200, b"ID3fake"))
    out = tmp_path / "pop.mp3"
    assert sc.main(["effect", "soft pop", str(out)]) == 0
    assert out.read_bytes() == b"ID3fake" and "15 credits" in capsys.readouterr().out
    assert sc.main(["effect", "soft pop", str(out)]) == 1, "never over a file already there"
