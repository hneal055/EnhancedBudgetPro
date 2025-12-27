# Creates tests/test_csv_exporter.py safely
# Usage (from repo root, in PowerShell):
#   powershell -ExecutionPolicy Bypass -File .\scripts\create_test_files.ps1
# or if already in PowerShell:
#   .\scripts\create_test_files.ps1

$testsDir = ".\tests"
New-Item -ItemType Directory -Path $testsDir -Force | Out-Null

$script = @'
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
'@

Set-Content -Path "$testsDir\test_csv_exporter.py" -Value $script -Encoding UTF8

Write-Host "Wrote $testsDir\test_csv_exporter.py"