"""Colour accuracy: CIEDE2000 against published reference pairs, and a palette chart measured back."""
import json

import numpy as np
import pytest

import measure_colour as mc
from conftest import need_ffmpeg, run

# Reference pairs from Sharma, Wu and Dalal's CIEDE2000 test data (Lab, Lab, expected difference).
SHARMA = [
    ((50.0, 2.6772, -79.7751), (50.0, 0.0, -82.7485), 2.0425),
    ((50.0, 3.1571, -77.2803), (50.0, 0.0, -82.7485), 2.8615),
    ((50.0, 2.8361, -74.0200), (50.0, 0.0, -82.7485), 3.4412),
    ((50.0, 0.0, 0.0), (50.0, -1.0, 2.0), 2.3669),
    ((50.0, 2.5, 0.0), (73.0, 25.0, -18.0), 27.1492),
    ((60.2574, -34.0099, 36.2677), (60.4626, -34.1751, 39.4387), 1.2644),
]


@pytest.mark.parametrize("a,b,want", SHARMA)
def test_de00_matches_the_reference_data(a, b, want):
    assert float(mc.de00(np.array(a), np.array(b))) == pytest.approx(want, abs=1e-4)


def test_white_and_black_land_where_lab_puts_them():
    white, black = mc.to_lab([1.0, 1.0, 1.0]), mc.to_lab([0.0, 0.0, 0.0])
    assert white == pytest.approx([100.0, 0.0, 0.0], abs=0.01)
    assert black == pytest.approx([0.0, 0.0, 0.0], abs=0.01)


@need_ffmpeg
def test_a_chart_measures_back_close_to_its_design_values(tmp_path):
    pal = tmp_path / "palette.json"
    pal.write_text(json.dumps({"patches": [{"name": "warm paper", "hex": "#F2E6D0"},
                                           {"name": "deep teal", "hex": "#1E5B63"},
                                           {"name": "signal red", "hex": "#D23A2E"}]}))
    chart = tmp_path / "chart.mov"
    run("make_chart.py", pal, chart)
    assert "centre" in json.loads(pal.read_text())["patches"][0], "patch places are written back"
    out = run("measure_colour.py", "chart", pal, chart).stdout.splitlines()
    assert len(out) == 3
    for line in out:
        assert float(line.rsplit(":", 1)[1]) < 1.0, line
