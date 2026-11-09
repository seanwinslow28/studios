"""Every script loads and prints its usage on --help, without doing any work."""
import pytest

from conftest import SCRIPTS, run

SCRIPTS_WITH_HELP = sorted(p.name for p in SCRIPTS.glob("*.py"))


def test_every_script_has_a_line_in_the_guide():
    guide = (SCRIPTS / "README.md").read_text()
    assert [s for s in SCRIPTS_WITH_HELP if f"`{s}`" not in guide] == []


@pytest.mark.parametrize("script", SCRIPTS_WITH_HELP)
def test_help_loads_and_prints_usage(script, tmp_path):
    r = run(script, "--help", cwd=tmp_path)
    assert r.returncode == 0
    assert "usage" in r.stdout.lower() or script in r.stdout, r.stdout[:300]
    assert list(tmp_path.iterdir()) == [], "--help writes nothing"
