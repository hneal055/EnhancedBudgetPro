from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from typing import Dict, List


class PDFBudgetReport:
    """
    Generates a full film/TV production budget PDF report.
    Includes scene breakdown, page & runtime estimates,
    and integrates RiskModel + BudgetEngine results.
    
    Phase 13.1 Week 3: Enhanced with Emotional Intelligence section
    """

    def __init__(self, title="Production Budget Report"):
        self.title = title

    def generate(self, data: Dict, budget_summary: Dict, output_path="ProductionBudgetReport.pdf", emotion_data: Dict = None):
        """
        Generate PDF report with optional emotional intelligence section
        
        Args:
            data: Script data (scenes, characters, etc.)
            budget_summary: Budget calculations
            output_path: Output file path
            emotion_data: Optional emotional intelligence data
        """
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
        
        # Phase 13.1: Add emotion stats to cover if available
        if emotion_data:
            summary = emotion_data.get("summary", {})
            c.drawString(50, height - 220, 
                        f"Avg Emotional Intensity: {summary.get('average_intensity', 0):.1f}/100")
            c.drawString(50, height - 240,
                        f"Character Arcs Tracked: {summary.get('characters_with_arcs', 0)}")

        c.showPage()

        # ==== EMOTIONAL INTELLIGENCE SECTION (Phase 13.1) ====
        if emotion_data:
            self._add_emotion_section(c, emotion_data, width, height)

        # ==== SCENE BREAKDOWN PAGE ====
        scenes: List[Dict] = data.get("scenes", [])
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "Scene Breakdown")

        y = height - 90
        scene_emotions = emotion_data.get("scenes", []) if emotion_data else []
        emotion_by_heading = {s.get("heading", ""): s for s in scene_emotions}
        
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
            y -= 15
            
            # Phase 13.1: Add emotion info if available
            if header in emotion_by_heading:
                emotion_info = emotion_by_heading[header]
                intensity = emotion_info.get("intensity", 0)
                tension = emotion_info.get("tension", 0)
                dominant = emotion_info.get("dominant_emotion", "neutral")
                
                c.setFont("Helvetica-Oblique", 10)
                c.setFillColorRGB(0.3, 0.3, 0.7)
                c.drawString(70, y, 
                            f"Emotion: {dominant.title()}  |  Intensity: {intensity:.1f}  |  Tension: {tension:.1f}")
                c.setFillColorRGB(0, 0, 0)
                y -= 15
            
            y -= 15

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
    
    def _add_emotion_section(self, c, emotion_data: Dict, width: float, height: float):
        """
        Phase 13.1 Week 3: Add dedicated emotional intelligence section to PDF
        
        Args:
            c: Canvas object
            emotion_data: Emotional intelligence data
            width: Page width
            height: Page height
        """
        c.setFont("Helvetica-Bold", 18)
        c.drawString(50, height - 50, "🧠 Emotional Intelligence Analysis")
        
        summary = emotion_data.get("summary", {})
        character_arcs = emotion_data.get("character_arcs", {})
        turning_points = emotion_data.get("turning_points", {})
        
        y = height - 90
        
        # Overview metrics
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Executive Summary")
        y -= 25
        
        c.setFont("Helvetica", 11)
        metrics = [
            f"Total Scenes Analyzed: {summary.get('total_scenes_analyzed', 0)}",
            f"Average Emotional Intensity: {summary.get('average_intensity', 0):.1f}/100",
            f"Average Tension Level: {summary.get('average_tension', 0):.1f}/100",
            f"Characters with Tracked Arcs: {summary.get('characters_with_arcs', 0)}",
            f"Total Turning Points: {summary.get('total_turning_points', 0)}"
        ]
        
        for metric in metrics:
            c.drawString(70, y, metric)
            y -= 18
        
        y -= 10
        
        # Emotion distribution
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Emotion Distribution")
        y -= 25
        
        emotion_dist = summary.get("emotion_distribution", {})
        c.setFont("Helvetica", 11)
        for emotion, count in sorted(emotion_dist.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / summary.get('total_scenes_analyzed', 1)) * 100
            c.drawString(70, y, f"{emotion.title()}: {count} scenes ({percentage:.1f}%)")
            y -= 18
        
        y -= 10
        
        # Character emotional complexity
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Character Emotional Complexity")
        y -= 25
        
        c.setFont("Helvetica", 11)
        # Sort characters by volatility
        char_volatility = [(char, data.get("emotional_volatility", 0)) 
                          for char, data in character_arcs.items()]
        char_volatility.sort(key=lambda x: x[1], reverse=True)
        
        for char, volatility in char_volatility[:5]:  # Top 5
            char_data = character_arcs[char]
            dominant = char_data.get("dominant_emotion", "neutral")
            scenes = char_data.get("total_scenes", 0)
            
            c.drawString(70, y, 
                        f"{char}: Volatility {volatility:.1f}/100, {scenes} scenes, Dominant: {dominant.title()}")
            y -= 18
            
            if y < 120:
                c.showPage()
                y = height - 50
        
        y -= 10
        
        # Key turning points
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Key Emotional Turning Points")
        y -= 25
        
        c.setFont("Helvetica", 11)
        all_turning_points = []
        for char, tp_list in turning_points.items():
            for tp in tp_list:
                all_turning_points.append((char, tp))
        
        # Sort by impact
        all_turning_points.sort(key=lambda x: x[1].get("impact", 0), reverse=True)
        
        for char, tp in all_turning_points[:10]:  # Top 10
            scene_idx = tp.get("scene_index", 0) + 1
            from_em = tp.get("from_emotion", "")
            to_em = tp.get("to_emotion", "")
            impact = tp.get("impact", 0)
            
            c.drawString(70, y, 
                        f"Scene {scene_idx}: {char} - {from_em.title()} → {to_em.title()} (Impact: {impact:.1f})")
            y -= 18
            
            if y < 120:
                c.showPage()
                y = height - 50
        
        y -= 20
        
        # Interpretation guide
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Understanding the Metrics")
        y -= 25
        
        c.setFont("Helvetica", 10)
        guide_text = [
            "Intensity (0-100): Energy level based on high-energy emotions (joy, anger, fear, surprise)",
            "  • 0-30: Low energy, introspective scenes",
            "  • 31-60: Moderate energy, balanced scenes",
            "  • 61-100: High energy, action or dramatic scenes",
            "",
            "Tension (0-100): Conflict level based on antagonistic emotions (anger, fear, disgust)",
            "  • 0-30: Calm, peaceful scenes",
            "  • 31-60: Building tension",
            "  • 61-100: High conflict or suspense",
            "",
            "Volatility (0-100): How much a character's emotions change scene-to-scene",
            "  • 0-30: Stable character",
            "  • 31-60: Moderate emotional range",
            "  • 61-100: Highly volatile character arc"
        ]
        
        for line in guide_text:
            if y < 100:
                c.showPage()
                y = height - 50
            c.drawString(70, y, line)
            y -= 14
        
        c.showPage()
