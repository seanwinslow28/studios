"""The film measurements on small generated clips: cuts found, motion checked, sheets drawn."""
import csv
import json

from conftest import make_clip, need_ffmpeg, run


def test_cut_check_passes_a_single_frame_cut_and_fails_a_soft_one(tmp_path):
    diff = tmp_path / "diff.csv"
    rows = [(f, 0.5) for f in range(60)]
    rows[30] = (30, 12.0)  # a clean cut at 1.0 s, 30 fps
    rows[45], rows[46] = (45, 6.0), (46, 5.5)  # a two-frame change, not a cut
    with open(diff, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["frame", "diff"])
        w.writerows(rows)
    assert run("cut_check.py", diff, 30, 1.0).returncode == 0
    r = run("cut_check.py", diff, 30, 1.0, 1.5, check=False)
    assert r.returncode == 1 and "single-frame: False" in r.stdout


@need_ffmpeg
def test_motion_check_finds_the_cut(tmp_path):
    clip = make_clip(tmp_path / "clip.mp4", seconds=2, cut_at=1)
    out = run("motion_check.py", clip, tmp_path / "m", "--ranges", "28-31", "--phone", "30").stdout
    assert "spikes: [30]" in out
    assert (tmp_path / "m" / "frames" / "frame_000031.jpg").is_file()
    assert (tmp_path / "m" / "phone" / "phone_f30.png").is_file()


@need_ffmpeg
def test_analyze_film_finds_the_hard_cut(tmp_path):
    clip = make_clip(tmp_path / "clip.mp4", seconds=2, cut_at=1)
    # a silent track, so the audio half has something to read
    with_audio = tmp_path / "with-audio.mp4"
    import subprocess
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(clip), "-f", "lavfi", "-i", "sine=frequency=440:duration=2",
                    "-shortest", "-c:v", "copy", "-c:a", "aac", str(with_audio)], check=True)
    run("analyze_film.py", with_audio, tmp_path / "a")
    summary = json.loads((tmp_path / "a" / "summary.json").read_text())
    assert summary["cuts"] == [1.0]
    for name in ("frames.csv", "cuts.csv", "audio.csv", "onsets.csv"):
        assert (tmp_path / "a" / name).is_file()


@need_ffmpeg
def test_contact_sheet_and_compare_clips_draw(tmp_path):
    clip = make_clip(tmp_path / "clip.mp4", seconds=2)
    run("contact_sheet.py", clip, 0, 1, 4, tmp_path / "sheet.jpg", 2, 160)
    assert (tmp_path / "sheet.jpg").stat().st_size > 1000
    run("compare_clips.py", tmp_path / "side.mp4", "A.", clip, "B.", clip)
    assert (tmp_path / "side.mp4").stat().st_size > 1000


def test_seq_sheet_draws_from_a_numbered_sequence(tmp_path):
    from PIL import Image
    frames = tmp_path / "frames"
    frames.mkdir()
    for n in range(1, 7):
        Image.new("RGB", (64, 36), (n * 40, 20, 20)).save(frames / f"frame_{n:06d}.png")
    run("seq_sheet.py", frames, tmp_path / "seq.jpg", 30, 0, 5, 1, 3, 64)
    assert Image.open(tmp_path / "seq.jpg").size == (3 * 64 + 4 * 6, 2 * (36 + 22) + 3 * 6)
