import os
import tempfile
from src.utils.scenario_io import export_scenarios_to_json, import_scenarios_from_json

def test_export_import_scenarios():
    scenarios = {
        "Cheapest": {"cost": 1000, "days": 3},
        "Fastest": {"cost": 1200, "days": 2},
    }
    # Export to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
        export_scenarios_to_json(scenarios, tmp.name)
        temp_path = tmp.name
    # Import from temp file
    loaded = import_scenarios_from_json(temp_path)
    assert loaded == scenarios, f"Loaded scenarios do not match: {loaded} != {scenarios}"
    os.remove(temp_path)
    print("AI Scenario Designer export/import test passed.")

if __name__ == "__main__":
    test_export_import_scenarios()
