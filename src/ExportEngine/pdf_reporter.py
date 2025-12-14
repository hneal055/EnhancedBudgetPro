from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from typing import Dict, List


class PDFBudgetReport:
    """
    Generates a full film/TV production budget PDF report.
    Includes scene breakdown, page & runtime estimates,
    and integrates RiskModel + BudgetEngine results.
    """

    def __init__(self, title="Production Budget Report"):
        self.title = title

    def generate(self, data: Dict, budget_summary: Dict, output_path="ProductionBudgetReport.pdf"):
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter

        # ==== COVER PAGE ====
        c.setFont("Helvetica-Bold", 20)
        c.drawString(50, height - 80, self.title)

        c.setFont("Helvetica", 12)
        c.drawString(50, height - 110,
                     f"Total Pages: {data.get('page_estimate', 'N/A')}")
        c.drawString(50, height - 130,
                     f"Scene Count: {data.get('scene_count', 'N/A')}")
        c.drawString(
            50, height - 150, f"Base Budget:  ${budget_summary.get('base_budget', 0):,.0f}")
        c.drawString(
            50, height - 170, f"Risk-Adjusted: ${budget_summary.get('risk_adjusted_total', 0):,.0f}")
        c.drawString(
            50, height - 190, f"Contingency Buffer: ${budget_summary.get('contingency_buffer', 0):,.0f}")

        c.showPage()

        # ==== SCENE BREAKDOWN PAGE ====
        scenes: List[Dict] = data.get("scenes", [])
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "Scene Breakdown")

        y = height - 90
        for i, s in enumerate(scenes, start=1):
            if y < 120:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica-Bold", 16)
                c.drawString(50, y, "Scene Breakdown Continued")
                y -= 40

            header = s["header"]
            chars = ", ".join(s["characters"])
            dialog = s["dialogue_lines"]
            action = s["action_lines"]
            page_est = round((dialog + action) / 55, 2)

            c.setFont("Helvetica-Bold", 13)
            c.drawString(50, y, f"Scene {i}: {header}")
            y -= 20

            c.setFont("Helvetica", 11)
            c.drawString(70, y, f"Characters: {chars}")
            y -= 15
            c.drawString(
                70, y, f"Dialogue Lines: {dialog}  |  Action Lines: {action}  |  Estimated Pages: {page_est}")
            y -= 30

        c.showPage()

        # ==== SUMMARY PAGE ====
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 60, "Budget Summary")

        c.setFont("Helvetica", 12)
        c.drawString(
            50, height - 110, f"Base Production Cost: ${budget_summary['base_budget']:,.0f}")
        c.drawString(
            50, height - 130, f"Risk Adjustment Added: ${budget_summary['risk_delay_cost']:,.0f}")
        c.drawString(
            50, height - 150, f"Contingency Reserve:  ${budget_summary['contingency_buffer']:,.0f}")
        c.drawString(50, height - 170,
                     "---------------------------------------------")
        c.drawString(
            50, height - 190, f"Final Risk-Adjusted Budget: ${budget_summary['risk_adjusted_total']:,.0f}")

        c.save()
        return output_path
