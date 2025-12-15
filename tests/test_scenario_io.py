import os
from src.utils.scenario_io import export_scenarios_to_json, import_scenarios_from_json, export_scenarios_to_csv, import_scenarios_from_csv

def test_scenario_io():
    scenarios = {
        "Cheapest": {"cost": 1000, "days": 3},
        "Fastest": {"cost": 1200, "days": 2},
    }
    # JSON
    json_file = "test_scenarios.json"
    export_scenarios_to_json(scenarios, json_file)
    loaded_json = import_scenarios_from_json(json_file)
    assert loaded_json == scenarios
    os.remove(json_file)

    # CSV
    csv_file = "test_scenarios.csv"
    export_scenarios_to_csv(scenarios, csv_file)
    loaded_csv = import_scenarios_from_csv(csv_file)
    # CSV import returns all values as strings, so convert for comparison
    for k in loaded_csv:
        loaded_csv[k]["cost"] = int(loaded_csv[k]["cost"])
        loaded_csv[k]["days"] = int(loaded_csv[k]["days"])
    assert loaded_csv == scenarios
    os.remove(csv_file)
    print("Scenario IO test passed.")

if __name__ == "__main__":
    test_scenario_io()
