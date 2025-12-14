from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from typing import Dict, List


class ExcelExporter:
    """
    Exports screenplay scene breakdown to Excel (.xlsx)
    Phase 13.1 Week 3: Enhanced with emotion data sheets
    """

    def export(self, data: Dict, output_path: str):
        scenes: List[Dict] = data.get("scenes", [])
        emotion_data = data.get("emotion_data")  # Phase 13.1: Emotion data

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

        # Phase 13.1 Week 3: Add emotion sheets if available
        if emotion_data:
            self._add_emotion_sheets(wb, emotion_data)

        wb.save(output_path)
        return output_path
    
    def _add_emotion_sheets(self, wb: Workbook, emotion_data: Dict):
        """Add emotion intelligence sheets to workbook"""
        
        # Sheet 1: Scene Emotions
        self._add_scene_emotions_sheet(wb, emotion_data)
        
        # Sheet 2: Character Arcs
        self._add_character_arcs_sheet(wb, emotion_data)
        
        # Sheet 3: Emotion Summary
        self._add_emotion_summary_sheet(wb, emotion_data)
    
    def _add_scene_emotions_sheet(self, wb: Workbook, emotion_data: Dict):
        """Scene-by-scene emotion breakdown"""
        ws = wb.create_sheet("Scene Emotions")
        
        # Header row with styling
        headers = ["Scene #", "Scene Heading", "Dominant Emotion", "Intensity (0-100)", 
                   "Tension (0-100)", "Dialogue Lines", "Action Lines"]
        ws.append(headers)
        
        # Style headers
        for cell in ws[1]:
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
            cell.font = Font(color="FFFFFF", bold=True)
        
        # Data rows
        scene_emotions = emotion_data.get("scene_emotions", [])
        for i, scene in enumerate(scene_emotions, 1):
            ws.append([
                i,
                scene.get("scene_heading", ""),
                scene.get("dominant_emotion", "").title(),
                round(scene.get("intensity", 0), 1),
                round(scene.get("tension", 0), 1),
                scene.get("dialogue_count", 0),
                scene.get("action_count", 0)
            ])
        
        # Auto-size columns
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width
    
    def _add_character_arcs_sheet(self, wb: Workbook, emotion_data: Dict):
        """Character emotional arc summary"""
        ws = wb.create_sheet("Character Arcs")
        
        # Header row
        headers = ["Character", "Total Scenes", "Scenes with Dialogue", "Dominant Emotion", 
                   "Emotional Volatility (0-100)", "Emotional Range"]
        ws.append(headers)
        
        # Style headers
        for cell in ws[1]:
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color="70AD47", end_color="70AD47", fill_type="solid")
            cell.font = Font(color="FFFFFF", bold=True)
        
        # Data rows
        character_arcs = emotion_data.get("character_arcs", {})
        for char_name, char_data in sorted(character_arcs.items()):
            emotional_range = ", ".join([e.title() for e in char_data.get("emotional_range", [])])
            
            ws.append([
                char_name,
                char_data.get("total_scenes", 0),
                char_data.get("scenes_with_dialogue", 0),
                char_data.get("dominant_emotion", "").title(),
                round(char_data.get("emotional_volatility", 0), 1),
                emotional_range
            ])
        
        # Auto-size columns
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width
    
    def _add_emotion_summary_sheet(self, wb: Workbook, emotion_data: Dict):
        """Overall emotion statistics and insights"""
        ws = wb.create_sheet("Emotion Summary")
        
        summary = emotion_data.get("summary", {})
        
        # Title
        ws.append(["EMOTIONAL INTELLIGENCE SUMMARY"])
        ws["A1"].font = Font(size=16, bold=True)
        ws.append([])
        
        # Overall metrics
        ws.append(["Overall Metrics"])
        ws["A3"].font = Font(bold=True, size=12)
        ws.append([])
        
        ws.append(["Total Scenes Analyzed:", summary.get("total_scenes_analyzed", 0)])
        ws.append(["Character Arcs Tracked:", summary.get("characters_with_arcs", 0)])
        ws.append(["Emotional Turning Points:", summary.get("total_turning_points", 0)])
        ws.append(["Average Scene Intensity:", f"{summary.get('average_intensity', 0):.1f}/100"])
        ws.append(["Average Scene Tension:", f"{summary.get('average_tension', 0):.1f}/100"])
        ws.append([])
        
        # Emotion distribution
        ws.append(["Emotion Distribution"])
        ws["A10"].font = Font(bold=True, size=12)
        ws.append([])
        
        ws.append(["Emotion", "Scene Count", "Percentage"])
        ws["A12"].font = Font(bold=True)
        ws["B12"].font = Font(bold=True)
        ws["C12"].font = Font(bold=True)
        
        emotion_dist = summary.get("emotion_distribution", {})
        total_scenes = summary.get("total_scenes_analyzed", 1)
        
        for emotion, count in sorted(emotion_dist.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_scenes * 100) if total_scenes > 0 else 0
            ws.append([emotion.title(), count, f"{percentage:.1f}%"])
        
        ws.append([])
        ws.append([])
        
        # Interpretation guide
        ws.append(["Interpretation Guide"])
        ws[f"A{ws.max_row}"].font = Font(bold=True, size=12)
        ws.append([])
        
        ws.append(["Intensity (0-100):"])
        ws.append(["  0-30: Low energy, introspective scenes"])
        ws.append(["  31-60: Moderate energy, balanced scenes"])
        ws.append(["  61-100: High energy, action or dramatic scenes"])
        ws.append([])
        
        ws.append(["Tension (0-100):"])
        ws.append(["  0-30: Calm, peaceful scenes"])
        ws.append(["  31-60: Building tension"])
        ws.append(["  61-100: High conflict or suspense"])
        ws.append([])
        
        ws.append(["Emotional Volatility (0-100):"])
        ws.append(["  0-30: Stable character"])
        ws.append(["  31-60: Moderate emotional range"])
        ws.append(["  61-100: Highly volatile character arc"])
        
        # Auto-size columns
        ws.column_dimensions["A"].width = 40
        ws.column_dimensions["B"].width = 15
        ws.column_dimensions["C"].width = 15
