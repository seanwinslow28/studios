"""The job folder maker and the review page builder."""
import json

import pytest

from conftest import run


def test_new_production_makes_a_lean_job_folder(tmp_path):
    job = tmp_path / "launch-film"
    run("new_production.py", job)
    assert sorted(p.name for p in job.iterdir()) == sorted(
        [".gitignore", "requirements-venv.txt", "references", "assets", "motion-experiments", "edits", "sound"])
    assert "*.mp4" in (job / ".gitignore").read_text().splitlines()
    assert not list(job.glob("*.md")), "no record files"


def test_new_production_refuses_a_folder_with_files(tmp_path):
    (tmp_path / "keep.txt").write_text("mine")
    r = run("new_production.py", tmp_path, check=False)
    assert r.returncode != 0 and "already has files" in r.stderr


def content(**over):
    c = {"tag": "Review 1.", "h1": "The first cut.", "lead": "Here is the first cut.", "ask": "Lock it?",
         "rec": "locking it.", "rec_why": "It reads well.", "alt_cost": "Notes cost a day.",
         "sections": [{"title": "What changed.", "paragraphs": ["The ending is shorter."]}]}
    c.update(over)
    return c


def test_build_review_writes_the_page(tmp_path):
    folder = tmp_path / "edits" / "review-3"
    folder.mkdir(parents=True)
    (folder / "content.json").write_text(json.dumps(content()))
    run("build_review.py", folder / "content.json", cwd=tmp_path)
    page = (tmp_path / "REVIEW-3.html").read_text()
    assert "The ending is shorter." in page and "<title>Review 3</title>" in page


@pytest.mark.parametrize("over,said", [
    ({"lead": "No ending punctuation"}, "missing end punctuation"),
    ({"video": "nowhere.mp4", "video_note": "A note."}, "missing file"),
])
def test_build_review_refuses_bad_content(tmp_path, over, said):
    (tmp_path / "content.json").write_text(json.dumps(content(**over)))
    r = run("build_review.py", tmp_path / "content.json", cwd=tmp_path, check=False)
    assert r.returncode != 0 and said in r.stderr
