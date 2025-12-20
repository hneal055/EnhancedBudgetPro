from unittest import mock

import pytest

from pages.storytelling_insights import (
    create_mock_streamlit,
    import_storytelling_insights,
    run_storytelling_insights_with_state,
)


def test_missing_insights_data():
    """Test SystemExit or error when insights_data is missing."""
    session_state = {
        "data": {"scenes": []},
        "emotion_data": {"character_arcs": {"CHAR": {"scenes": [1, 2, 3]}}},
        # "insights_data" is missing
    }
    result = run_storytelling_insights_with_state(session_state)
    assert (
        result is True or result == "SystemExit"
    ), "Should handle missing insights_data"


def test_empty_character_arcs():
    """Test SystemExit or error when character_arcs is empty."""
    session_state = {
        "data": {"scenes": []},
        "emotion_data": {"character_arcs": {}},
        "insights_data": {},
    }
    result = run_storytelling_insights_with_state(session_state)
    assert (
        result is True or result == "SystemExit"
    ), "Should handle empty character_arcs"


def test_missing_data_key():
    """Test SystemExit or error when 'data' key is missing."""
    session_state = {
        "emotion_data": {"character_arcs": {"CHAR": {"scenes": [1]}}},
        "insights_data": {},
    }
    result = run_storytelling_insights_with_state(session_state)
    assert result is True or result == "SystemExit", "Should handle missing 'data' key"


def test_missing_emotion_data_key():
    """Test SystemExit or error when 'emotion_data' key is missing."""
    session_state = {
        "data": {"scenes": []},
        "insights_data": {},
    }
    result = run_storytelling_insights_with_state(session_state)
    assert (
        result is True or result == "SystemExit"
    ), "Should handle missing 'emotion_data' key"


def test_columns_mock_called():
    """Test columns are created when all prerequisites are present."""
    session_state = {
        "data": {"scenes": []},
        "emotion_data": {"character_arcs": {"CHAR": {"scenes": [1, 2, 3]}}},
        "insights_data": {
            "overall_health": {
                "score": 90,
                "rating": "Good",
                "emoji": "👍",
                "breakdown": {},
                "strengths": [],
                "weaknesses": [],
            },
            "analyzed_arcs": 1,
            "recommendations": [],
            "pacing_analysis": {
                "average_scenes_per_character": 3,
                "emoji": "👍",
                "overall_assessment": "",
                "scene_distribution": {"min": 1, "avg": 2, "max": 3},
                "pacing_issues": [],
            },
            "arc_optimization": [],
            "benchmarks": {
                "overall_alignment": {
                    "score": 100,
                    "rating": "Excellent",
                    "emoji": "🏆",
                },
                "comparisons": [],
                "industry_note": "",
            },
            "export_summary": {
                "quick_stats": {
                    "characters_analyzed": 1,
                    "arc_completion_avg": 100,
                    "consistency_avg": 100,
                },
                "executive_summary": {"priority_actions": 0},
                "top_priorities": [],
            },
        },
    }
    mock_st = create_mock_streamlit(session_state)
    import sys

    original_st = sys.modules.get("streamlit")
    try:
        sys.modules["streamlit"] = mock_st
        module = import_storytelling_insights()
        if hasattr(module, "main"):
            module.main()
        assert mock_st.columns.called, "mock_st.columns should be called"
    finally:
        if original_st:
            sys.modules["streamlit"] = original_st
        else:
            sys.modules.pop("streamlit", None)
