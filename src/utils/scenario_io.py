import json
import pandas as pd

def export_scenarios_to_json(scenarios, file_path):
    with open(file_path, 'w') as f:
        json.dump(scenarios, f, indent=2)

def import_scenarios_from_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def export_scenarios_to_csv(scenarios, file_path):
    # Assumes scenarios is a dict of scenario_name: scenario_data
    df = pd.DataFrame.from_dict(scenarios, orient='index')
    df.to_csv(file_path)

def import_scenarios_from_csv(file_path):
    df = pd.read_csv(file_path, index_col=0)
    return df.to_dict(orient='index')
