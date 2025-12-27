# tests/conftest.py
import sys
import os

# Add the src directory to Python path for all tests
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_path = os.path.join(project_root, 'src')
tests_path = os.path.join(project_root, 'tests')

if src_path not in sys.path:
    sys.path.insert(0, src_path)
if tests_path not in sys.path:
    sys.path.insert(0, tests_path)

# Optional: Add any fixtures or shared test utilities here
import pytest

@pytest.fixture
def sample_script_data():
    """Fixture to provide sample script data for tests"""
    return {
        "title": "Test Movie",
        "scenes": [
            {"number": 1, "location": "INT. HOUSE - DAY", "description": "A room."},
            {"number": 2, "location": "EXT. STREET - NIGHT", "description": "Outside."}
        ],
        "characters": ["JOHN", "MARY"]
    }