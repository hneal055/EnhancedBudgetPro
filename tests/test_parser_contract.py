import pytest

from src.IngestEngine.shared_utils import extract_characters
from src.AnalysisEngine.scene_density_engine import SceneDensityEngine
from src.validation import validate_parsed_script


# -------------------------------------------------
# FIXTURE — SAMPLE SCRIPT CONTENT
# -------------------------------------------------
@pytest.fixture
def sample_scene_data():
    return {
        "scenes": [
            {
                "heading": "INT. LAB - NIGHT",
                "lines": [
                    "JOHN",
                    "We have to move now.",
                    "SARAH",
                    "There's no time left.",
                    "CUT TO",
                    "The alarms blare."
                ],
                "characters": ["JOHN", "SARAH"]
            }
        ]
    }


# -------------------------------------------------
# TEST 1 — Character Extraction Filter
# -------------------------------------------------
def test_extract_characters_filters_noise():
    lines = [
        "INT. LAB - NIGHT",
        "JOHN",
        "We have to move.",
        "CUT TO",
        "SARAH",
        "No time left.",
        "DAY"
    ]

    chars = extract_characters(lines)

    assert "JOHN" in chars
    assert "SARAH" in chars
    assert "CUT TO" not in chars
    assert "INT. LAB - NIGHT" not in chars
    assert "DAY" not in chars
    assert len(chars) == 2


# -------------------------------------------------
# TEST 2 — Parsed Script Contract Validation
# -------------------------------------------------
def test_validate_parsed_script_contract(sample_scene_data):
    assert validate_parsed_script(sample_scene_data) is True

    scene = sample_scene_data["scenes"][0]

    assert "heading" in scene
    assert "lines" in scene
    assert "characters" in scene
    assert isinstance(scene["lines"], list)
    assert isinstance(scene["characters"], list)


# -------------------------------------------------
# TEST 3 — Scene Density Engine Stability
# -------------------------------------------------
def test_scene_density_engine_output(sample_scene_data):
    engine = SceneDensityEngine()
    result = engine.analyze(sample_scene_data)

    assert "scene_density" in result
    assert "totals" in result

    density = result["scene_density"][0]

    assert "dialogue_lines" in density
    assert "action_lines" in density
    assert "classification" in density

    assert density["dialogue_lines"] > 0
    assert density["action_lines"] >= 0
    assert density["classification"] in {
        "Dialogue-Heavy",
        "Action-Heavy",
        "Balanced"
    }


# -------------------------------------------------
# TEST 4 — Malformed Scene Fails Fast
# -------------------------------------------------
def test_invalid_scene_fails_validation():
    bad_data = {
        "scenes": [
            {
                "lines": ["JOHN", "Hello"]
            }
        ]
    }

    with pytest.raises(Exception):
        validate_parsed_script(bad_data)
