from src.utils.scenario_io import export_scenarios_to_json, import_scenarios_from_json
import os
import tempfile

def test_custom_scenario_addition():
    # Simulate adding a custom scenario
    scenario_configs = {
        "Cheapest": {"rate_factor": 0.8, "compression_factor": 1.05, "volatility": 0.02},
    }
    custom_name = "MyCustom"
    custom_cfg = {
        "description": "User-defined custom scenario.",
        "rate_factor": 1.2,
        "compression_factor": 0.9,
        "volatility": 0.05,
    }
    scenario_configs[custom_name] = custom_cfg
    assert custom_name in scenario_configs
    assert scenario_configs[custom_name]["rate_factor"] == 1.2
    print("Custom scenario addition logic test passed.")

def test_custom_scenario_export_import():
    scenarios = {
        "MyCustom": {"cost": 1500, "days": 4},
    }
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
        export_scenarios_to_json(scenarios, tmp.name)
        temp_path = tmp.name
    loaded = import_scenarios_from_json(temp_path)
    assert loaded == scenarios
    os.remove(temp_path)
    print("Custom scenario export/import test passed.")

if __name__ == "__main__":
    test_custom_scenario_addition()
    test_custom_scenario_export_import()
