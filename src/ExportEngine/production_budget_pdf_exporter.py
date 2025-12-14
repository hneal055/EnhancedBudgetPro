# production_budget_pdf_exporter.py — Phase 3.0-G PDF Export Engine
# ---------------------------------------------------------------
# Generates a professional Production Budget PDF from Master Engine output

from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas


class ProductionBudgetPDFExporter:

    def export(self, budget_data: dict, output_path: str):
        c = canvas.Canvas(output_path, pagesize=LETTER)
        width, height = LETTER

        y = height - 40
        c.setFont("Helvetica-Bold", 16)
        c.drawString(40, y, "PRODUCTION BUDGET SUMMARY")
        y -= 40

        c.setFont("Helvetica", 11)

        def write_line(label, value):
            nonlocal y
            c.drawString(60, y, f"{label}: {value}")
            y -= 18

        write_line("CORE PRODUCTION TOTAL", f"$ {budget_data['core_production_total']:,.2f}")
        write_line("FINAL STUDIO BUDGET", f"$ {budget_data['final_production_budget']:,.2f}")

        y -= 20
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y, "DEPARTMENT BREAKDOWN")
        y -= 30

        c.setFont("Helvetica", 10)

        departments = [
            ("Crew", budget_data["crew"]["total_crew_cost"]),
            ("Equipment", budget_data["equipment"]["total_equipment_cost"]),
            ("Locations", budget_data["locations"]["total_location_cost"]),
            ("Post-Production", budget_data["post"]["total_post_cost"]),
            ("Insurance", budget_data["insurance"]["insurance_total"]),
            ("Contingency", budget_data["insurance"]["contingency_buffer"])
        ]

        for name, cost in departments:
            c.drawString(60, y, f"{name}: $ {cost:,.2f}")
            y -= 16

        c.showPage()
        c.save()
