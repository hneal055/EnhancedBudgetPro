# src/ExportEngine/stripboard_pdf_exporter.py
# ------------------------------------------
# Dedicated exporter for shooting stripboards (NO budget keys required)

from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


class StripboardPDFExporter:
    def export(self, schedule_data: dict, filename: str):
        """
        Expects:
        {
            "daily_schedule": [
                {"shoot_day": int, "scene": str, "characters": list, "daily_burn": int}
            ],
            "average_daily_burn": float,
            "peak_burn_day": dict,
            "danger_days": list
        }
        """

        styles = getSampleStyleSheet()
        doc = SimpleDocTemplate(filename, pagesize=LETTER)
        elements = []

        elements.append(Paragraph("FINAL SHOOTING STRIPBOARD", styles["Title"]))
        elements.append(Paragraph(" ", styles["Normal"]))

        # -------- TABLE --------
        table_data = [["Day", "Scene", "Characters", "Daily Burn ($)"]]

        for day in schedule_data.get("daily_schedule", []):
            table_data.append([
                str(day.get("shoot_day", "")),
                day.get("scene", ""),
                ", ".join(day.get("characters", [])),
                f"${day.get('daily_burn', 0):,.2f}"
            ])

        table = Table(table_data, colWidths=[1*inch, 3*inch, 2.5*inch, 2*inch])

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2933")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
            ("ALIGN", (0, 1), (-1, -1), "CENTER"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ]))

        elements.append(table)
        elements.append(Paragraph(" ", styles["Normal"]))

        # -------- SUMMARY --------
        elements.append(Paragraph(
            f"Average Daily Burn: ${schedule_data.get('average_daily_burn', 0):,.2f}",
            styles["Heading3"]
        ))

        peak = schedule_data.get("peak_burn_day", {})
        elements.append(Paragraph(
            f"Peak Burn Day: Day {peak.get('day', 'N/A')} — ${peak.get('cost', 0):,.2f}",
            styles["Heading3"]
        ))

        danger_days = schedule_data.get("danger_days", [])
        elements.append(Paragraph(
            f"Danger Days Detected: {len(danger_days)}",
            styles["Heading3"]
        ))

        doc.build(elements)
