from openpyxl import Workbook
from typing import Dict, List


class ExcelExporter:
    """
    Exports screenplay scene breakdown to Excel (.xlsx)
    """

    def export(self, data: Dict, output_path: str):
        scenes: List[Dict] = data.get("scenes", [])

        wb = Workbook()
        ws = wb.active
        ws.title = "Scene Breakdown"

        # Header row
        ws.append(["Scene #", "Header", "Characters",
                  "Dialogue", "Action", "Page Est"])

        for i, s in enumerate(scenes, start=1):
            dialog = s.get("dialogue_lines", 0)
            action = s.get("action_lines", 0)
            page_est = round((dialog + action) / 55, 2)

            ws.append([
                i,
                s.get("header", ""),
                ", ".join(s.get("characters", [])),
                dialog,
                action,
                page_est
            ])

        wb.save(output_path)
        return output_path
