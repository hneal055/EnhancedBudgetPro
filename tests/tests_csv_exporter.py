import csv
from ExportEngine.csv_exporter import CSVExporter


def test_csv_exporter_writes_correct_rows(tmp_path):
    exporter = CSVExporter()
    data = {
        "scenes": [
            {
                "header": "INT. ROOM",
                "characters": ["JOHN", "MARY"],
                "dialogue_lines": 2,
                "action_lines": 3,
            }
        ]
    }

    out_file = tmp_path / "out.csv"
    out_path = exporter.export(data, str(out_file))

    # exporter returns the output path
    assert out_path == str(out_file)

    # Read the CSV and validate header + first data row
    with open(out_path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    assert rows[0] == ["Scene #", "Header", "Characters", "Dialogue", "Action", "Page Est"]
    assert rows[1] == ["1", "INT. ROOM", "JOHN, MARY", "2", "3", "0.09"]