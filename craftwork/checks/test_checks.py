"""Tests for the kit's checks and the studio builder. Run: uvx --from pytest pytest craftwork/checks"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

import new_studio  # noqa: E402
import old_terms  # noqa: E402
import size_budget  # noqa: E402


def first_plain_term() -> str:
    for raw in old_terms.TERMS_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith(("#", "re:")):
            return line
    raise AssertionError("the word list has no plain terms")


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    return tmp_path


def build(repo: Path, name: str = "samplecraft") -> Path:
    return new_studio.build(name, "sample pieces", name.capitalize(), repo)


# ---- the studio builder ---------------------------------------------------

def test_builds_a_studio_from_the_template(repo):
    studio = build(repo)
    for f in ("SKILL.md", "taste.md", "front-door.md", "expertise/README.md",
              "tools/README.md", "research/README.md"):
        assert (studio / f).is_file(), f
    assert (studio / "library").is_dir()
    skill = (studio / "SKILL.md").read_text()
    assert skill.startswith("---\nname: samplecraft\n")
    assert "samplecraft/taste.md" in skill
    assert not any("{{" in f.read_text() for f in studio.rglob("*.md"))


def test_links_the_studio_in_as_a_skill(repo):
    studio = build(repo)
    for base in (".claude/skills", ".agents/skills"):
        link = repo / base / "samplecraft"
        assert link.is_symlink()
        assert link.resolve() == studio.resolve()
        assert (link / "SKILL.md").is_file()


def test_refuses_a_name_that_exists(repo):
    build(repo)
    with pytest.raises(SystemExit):
        build(repo)


def test_refuses_when_a_skill_link_is_taken(repo):
    (repo / ".claude/skills/samplecraft").mkdir(parents=True)
    with pytest.raises(SystemExit):
        build(repo)
    assert not (repo / "samplecraft").exists()


def test_refuses_a_bad_name(repo):
    with pytest.raises(SystemExit):
        build(repo, "Sample Craft")


# ---- the size check -------------------------------------------------------

def test_a_new_studio_is_within_budget_with_room_for_taste(repo):
    counts, missing = size_budget.measure(build(repo))
    assert not missing
    assert sum(counts.values()) <= size_budget.BUDGET - 800


def test_over_budget_fails(repo, capsys):
    studio = build(repo)
    with (studio / "taste.md").open("a") as f:
        f.write(" word" * size_budget.BUDGET)
    assert size_budget.main([str(studio), "--root", str(repo)]) == 1
    assert "OVER" in capsys.readouterr().out


def test_finds_only_studios_built_from_the_kit(repo):
    build(repo)
    (repo / "notastudio").mkdir()
    (repo / "notastudio" / "SKILL.md").write_text("x")
    assert [p.name for p in size_budget.studios(repo)] == ["samplecraft"]


def test_missing_taste_page_fails(repo):
    studio = build(repo)
    (studio / "taste.md").unlink()
    assert size_budget.main([str(studio), "--root", str(repo)]) == 1


# ---- the old-terms scan ---------------------------------------------------

def test_the_kit_itself_is_clean():
    assert old_terms.scan(old_terms.default_targets(), old_terms.load_terms()) == []


def test_a_new_studio_is_clean(repo):
    assert old_terms.scan([build(repo)], old_terms.load_terms()) == []


def test_finds_an_old_term(repo):
    studio = build(repo)
    (studio / "expertise" / "notes.md").write_text(f"Ask the {first_plain_term()} first.\n")
    hits = old_terms.scan([studio], old_terms.load_terms())
    assert len(hits) == 1 and hits[0][1] == 1


def test_skips_the_private_library(repo):
    studio = build(repo)
    (studio / "library" / "book.md").write_text(first_plain_term())
    assert old_terms.scan([studio], old_terms.load_terms()) == []


def test_ordinary_words_that_look_close_pass(repo):
    studio = build(repo)
    (studio / "expertise" / "pricing.md").write_text(
        "Per-seat pricing, swim lanes on a diagram, and a benchmark run.\n")
    assert old_terms.scan([studio], old_terms.load_terms()) == []
