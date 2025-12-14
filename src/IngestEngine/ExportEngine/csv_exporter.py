import csv
from typing import Dict, List


class CSVExporter:
    """
    Exports parsed screenplay data to CSV.
    """

    def export(self, data: Dict, output_path: str):
        scenes: List[Dict] = data.get("scenes", [])

        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Scene #", "Header", "Characters",
                            "Dialogue", "Action", "Page Est."])

            for i, s in enumerate(scenes, start=1):
                page_est = round(
                    (s["dialogue_lines"] + s["action_lines"]) / 55, 2)
                writer.writerow([
                    i,
                    s["header"],
                    ", ".join(s["characters"]),
                    s["dialogue_lines"],
                    s["action_lines"],
                    page_est
                ])

        return output_path
