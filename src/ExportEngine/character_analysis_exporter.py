"""
Character Analysis Exporter
Export character arc analysis data to CSV, Excel, and PDF formats
"""
import os
from typing import Dict, List, Any
import pandas as pd
from datetime import datetime


class CharacterAnalysisExporter:
    """
    Export character analysis data in multiple formats
    Supports CSV, Excel (multi-sheet), and data preparation for PDF
    """
    
    def __init__(self, output_dir: str = "./output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def export_comparison_data_csv(
        self,
        comparisons: List[Dict],
        filename: str = "character_comparisons.csv"
    ) -> str:
        """Export character comparison data to CSV"""
        
        rows = []
        for comp in comparisons:
            # Basic metrics
            row = {
                "Character_1": comp.get("characters", ["", ""])[0],
                "Character_2": comp.get("characters", ["", ""])[1],
                "Volatility_1": comp.get("basic_metrics", {}).get("volatility_1", 0),
                "Volatility_2": comp.get("basic_metrics", {}).get("volatility_2", 0),
                "Scenes_1": comp.get("basic_metrics", {}).get("scenes_1", 0),
                "Scenes_2": comp.get("basic_metrics", {}).get("scenes_2", 0),
                "Dialogue_Density_1": comp.get("basic_metrics", {}).get("dialogue_density_1", 0),
                "Dialogue_Density_2": comp.get("basic_metrics", {}).get("dialogue_density_2", 0),
                "Emotional_Range_1": comp.get("basic_metrics", {}).get("emotional_range_1", 0),
                "Emotional_Range_2": comp.get("basic_metrics", {}).get("emotional_range_2", 0),
                "Shared_Scenes": comp.get("interactions", {}).get("shared_scenes", 0),
                "Interaction_Rate": comp.get("interactions", {}).get("interaction_rate", 0),
                "Emotional_Alignment": comp.get("interactions", {}).get("emotional_alignment", 0),
                "Relationship_Type": comp.get("synchronization", {}).get("relationship_type", "Unknown")
            }
            rows.append(row)
        
        df = pd.DataFrame(rows)
        output_path = os.path.join(self.output_dir, filename)
        df.to_csv(output_path, index=False)
        
        return output_path
    
    def export_arc_progression_csv(
        self,
        character_arcs: Dict[str, Dict],
        classifications: Dict[str, Dict],
        filename: str = "arc_progressions.csv"
    ) -> str:
        """Export character arc progression data to CSV"""
        
        rows = []
        for char, arc in character_arcs.items():
            classification = classifications.get(char, {})
            
            # Get emotion progression
            emotions_by_scene = arc.get("emotions_by_scene", {})
            for scene, emotion_data in emotions_by_scene.items():
                row = {
                    "Character": char,
                    "Arc_Type": classification.get("arc_type", "Unknown"),
                    "Scene": scene,
                    "Emotion": emotion_data.get("emotion", "neutral"),
                    "Intensity": emotion_data.get("intensity", 0),
                    "Dialogue_Lines": len(emotion_data.get("dialogue", []))
                }
                rows.append(row)
        
        df = pd.DataFrame(rows)
        output_path = os.path.join(self.output_dir, filename)
        df.to_csv(output_path, index=False)
        
        return output_path
    
    def export_relationship_matrix_csv(
        self,
        relationships: List[Dict],
        filename: str = "relationship_matrix.csv"
    ) -> str:
        """Export relationship data as matrix to CSV"""
        
        # Build character list
        all_chars = set()
        for rel in relationships:
            char1, char2 = rel["characters"]
            all_chars.add(char1)
            all_chars.add(char2)
        
        all_chars = sorted(list(all_chars))
        
        # Create matrix
        matrix_data = {char: [0] * len(all_chars) for char in all_chars}
        
        for rel in relationships:
            char1, char2 = rel["characters"]
            strength = rel.get("relationship_strength", 0)
            
            idx1 = all_chars.index(char1)
            idx2 = all_chars.index(char2)
            
            matrix_data[char1][idx2] = strength
            matrix_data[char2][idx1] = strength
        
        df = pd.DataFrame(matrix_data, index=all_chars)
        df.columns = all_chars
        
        output_path = os.path.join(self.output_dir, filename)
        df.to_csv(output_path)
        
        return output_path
    
    def export_consistency_reports_csv(
        self,
        consistency_data: Dict[str, Dict],
        filename: str = "consistency_reports.csv"
    ) -> str:
        """Export character consistency analysis to CSV"""
        
        rows = []
        for char, analysis in consistency_data.items():
            # Overall row
            row = {
                "Character": char,
                "Consistency_Score": analysis.get("consistency_score", 0),
                "Baseline_Emotions": ", ".join(analysis.get("baseline_emotions", [])),
                "Total_Deviations": len(analysis.get("deviations", [])),
                "Severe_Deviations": len([d for d in analysis.get("deviations", []) if d.get("severity") == "severe"]),
                "Pattern": analysis.get("pattern_analysis", "Unknown"),
                "Confidence": analysis.get("confidence", 0)
            }
            rows.append(row)
        
        df = pd.DataFrame(rows)
        output_path = os.path.join(self.output_dir, filename)
        df.to_csv(output_path, index=False)
        
        return output_path
    
    def export_insights_summary_csv(
        self,
        insights: Dict[str, Any],
        filename: str = "storytelling_insights.csv"
    ) -> str:
        """Export storytelling insights summary to CSV"""
        
        rows = []
        
        # Overall health
        health = insights.get("overall_health", {})
        rows.append({
            "Category": "Overall Health",
            "Metric": "Score",
            "Value": health.get("score", 0),
            "Rating": health.get("rating", "Unknown")
        })
        
        # Breakdown metrics
        for key, data in health.get("breakdown", {}).items():
            rows.append({
                "Category": "Health Breakdown",
                "Metric": key.replace("_", " ").title(),
                "Value": data.get("score", 0),
                "Rating": ""
            })
        
        # Recommendations
        for rec in insights.get("recommendations", []):
            rows.append({
                "Category": "Recommendation",
                "Metric": f"{rec['character']} - {rec['category']}",
                "Value": rec["priority"],
                "Rating": rec["suggestion"]
            })
        
        df = pd.DataFrame(rows)
        output_path = os.path.join(self.output_dir, filename)
        df.to_csv(output_path, index=False)
        
        return output_path
    
    def export_all_to_excel(
        self,
        character_arcs: Dict[str, Dict],
        classifications: Dict[str, Dict],
        comparisons: List[Dict] = None,
        predictions: Dict[str, Dict] = None,
        relationships: List[Dict] = None,
        consistency: Dict[str, Dict] = None,
        insights: Dict[str, Any] = None,
        filename: str = "character_analysis_full.xlsx"
    ) -> str:
        """Export all character analysis data to multi-sheet Excel workbook"""
        
        output_path = os.path.join(self.output_dir, filename)
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            
            # Sheet 1: Summary
            summary_rows = []
            summary_rows.append({"Metric": "Total Characters", "Value": len(character_arcs)})
            summary_rows.append({"Metric": "Analyzed Characters", "Value": len(classifications)})
            if insights:
                health = insights.get("overall_health", {})
                summary_rows.append({"Metric": "Overall Health", "Value": f"{health.get('score', 0):.0f}/100"})
                summary_rows.append({"Metric": "Health Rating", "Value": health.get("rating", "Unknown")})
            
            pd.DataFrame(summary_rows).to_excel(writer, sheet_name="Summary", index=False)
            
            # Sheet 2: Arc Classifications
            if classifications:
                class_rows = []
                for char, data in classifications.items():
                    class_rows.append({
                        "Character": char,
                        "Arc_Type": data.get("arc_type", "Unknown"),
                        "Confidence": data.get("confidence", 0),
                        "Primary_Emotion": data.get("primary_emotion", "Unknown"),
                        "Scenes": len(character_arcs.get(char, {}).get("scenes", []))
                    })
                pd.DataFrame(class_rows).to_excel(writer, sheet_name="Arc Classifications", index=False)
            
            # Sheet 3: Arc Progressions
            progression_rows = []
            for char, arc in character_arcs.items():
                emotions_by_scene = arc.get("emotions_by_scene", {})
                for scene, emotion_data in emotions_by_scene.items():
                    progression_rows.append({
                        "Character": char,
                        "Scene": scene,
                        "Emotion": emotion_data.get("emotion", "neutral"),
                        "Intensity": emotion_data.get("intensity", 0)
                    })
            if progression_rows:
                pd.DataFrame(progression_rows).to_excel(writer, sheet_name="Arc Progressions", index=False)
            
            # Sheet 4: Predictions
            if predictions:
                pred_rows = []
                for char, pred in predictions.items():
                    pred_rows.append({
                        "Character": char,
                        "Completion": pred.get("completion_percentage", 0),
                        "Missing_Beats": ", ".join(pred.get("missing_beats", [])),
                        "Present_Beats": ", ".join(pred.get("present_beats", [])),
                        "Pacing": pred.get("pacing", "Unknown"),
                        "Transformation": pred.get("transformation_status", "Unknown"),
                        "Confidence": pred.get("confidence", 0)
                    })
                pd.DataFrame(pred_rows).to_excel(writer, sheet_name="Predictions", index=False)
            
            # Sheet 5: Relationships
            if relationships:
                rel_rows = []
                for rel in relationships:
                    char1, char2 = rel["characters"]
                    rel_rows.append({
                        "Character_1": char1,
                        "Character_2": char2,
                        "Shared_Scenes": rel.get("shared_scenes", 0),
                        "Relationship_Type": rel.get("relationship_type", "Unknown"),
                        "Strength": rel.get("relationship_strength", 0),
                        "Avg_Sentiment": sum(rel.get("sentiment_trajectory", [0])) / len(rel.get("sentiment_trajectory", [1])),
                        "Turning_Points": len(rel.get("turning_points", []))
                    })
                pd.DataFrame(rel_rows).to_excel(writer, sheet_name="Relationships", index=False)
            
            # Sheet 6: Consistency
            if consistency:
                cons_rows = []
                for char, cons in consistency.items():
                    cons_rows.append({
                        "Character": char,
                        "Consistency_Score": cons.get("consistency_score", 0),
                        "Baseline_Emotions": ", ".join(cons.get("baseline_emotions", [])),
                        "Total_Deviations": len(cons.get("deviations", [])),
                        "Severe_Deviations": len([d for d in cons.get("deviations", []) if d.get("severity") == "severe"]),
                        "Pattern": cons.get("pattern_analysis", "Unknown")
                    })
                pd.DataFrame(cons_rows).to_excel(writer, sheet_name="Consistency", index=False)
            
            # Sheet 7: Comparisons
            if comparisons:
                comp_rows = []
                for comp in comparisons:
                    char1, char2 = comp.get("characters", ["", ""])
                    comp_rows.append({
                        "Character_1": char1,
                        "Character_2": char2,
                        "Shared_Scenes": comp.get("interactions", {}).get("shared_scenes", 0),
                        "Emotional_Alignment": comp.get("interactions", {}).get("emotional_alignment", 0),
                        "Relationship_Type": comp.get("synchronization", {}).get("relationship_type", "Unknown")
                    })
                pd.DataFrame(comp_rows).to_excel(writer, sheet_name="Comparisons", index=False)
            
            # Sheet 8: Insights
            if insights:
                insights_rows = []
                
                # Health breakdown
                for key, data in insights.get("overall_health", {}).get("breakdown", {}).items():
                    insights_rows.append({
                        "Category": "Health",
                        "Metric": key.replace("_", " ").title(),
                        "Value": data.get("score", 0)
                    })
                
                # Recommendations
                for rec in insights.get("recommendations", [])[:10]:
                    insights_rows.append({
                        "Category": "Recommendation",
                        "Metric": f"{rec['character']} - {rec['issue']}",
                        "Value": rec["priority"]
                    })
                
                pd.DataFrame(insights_rows).to_excel(writer, sheet_name="Insights", index=False)
        
        return output_path
    
    def prepare_pdf_data(
        self,
        character_arcs: Dict[str, Dict],
        classifications: Dict[str, Dict],
        predictions: Dict[str, Dict] = None,
        relationships: List[Dict] = None,
        consistency: Dict[str, Dict] = None,
        insights: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Prepare structured data for PDF generation
        Returns organized data suitable for reportlab PDF creation
        """
        
        pdf_data = {
            "title": "Character Analysis Report",
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "summary": {
                "total_characters": len(character_arcs),
                "analyzed_characters": len(classifications),
                "overall_health": insights.get("overall_health", {}).get("score", 0) if insights else 0,
                "health_rating": insights.get("overall_health", {}).get("rating", "Unknown") if insights else "Unknown"
            },
            "characters": []
        }
        
        # Build character profiles
        for char, arc in character_arcs.items():
            classification = classifications.get(char, {})
            prediction = predictions.get(char, {}) if predictions else {}
            consistency_data = consistency.get(char, {}) if consistency else {}
            
            char_profile = {
                "name": char,
                "arc_type": classification.get("arc_type", "Unknown"),
                "scenes": len(arc.get("scenes", [])),
                "confidence": classification.get("confidence", 0),
                "completion": prediction.get("completion_percentage", 0),
                "consistency_score": consistency_data.get("consistency_score", 0),
                "emotions": []
            }
            
            # Emotion progression
            for scene, emotion_data in arc.get("emotions_by_scene", {}).items():
                char_profile["emotions"].append({
                    "scene": scene,
                    "emotion": emotion_data.get("emotion", "neutral"),
                    "intensity": emotion_data.get("intensity", 0)
                })
            
            pdf_data["characters"].append(char_profile)
        
        # Add relationships
        if relationships:
            pdf_data["relationships"] = []
            for rel in relationships:
                char1, char2 = rel["characters"]
                pdf_data["relationships"].append({
                    "characters": f"{char1} & {char2}",
                    "type": rel.get("relationship_type", "Unknown"),
                    "strength": rel.get("relationship_strength", 0),
                    "shared_scenes": rel.get("shared_scenes", 0)
                })
        
        # Add insights summary
        if insights:
            pdf_data["insights"] = {
                "strengths": insights.get("overall_health", {}).get("strengths", []),
                "weaknesses": insights.get("overall_health", {}).get("weaknesses", []),
                "top_recommendations": [
                    f"{rec['character']}: {rec['suggestion']}"
                    for rec in insights.get("recommendations", [])[:5]
                ]
            }
        
        return pdf_data
    
    def export_all_formats(
        self,
        character_arcs: Dict[str, Dict],
        classifications: Dict[str, Dict],
        comparisons: List[Dict] = None,
        predictions: Dict[str, Dict] = None,
        relationships: List[Dict] = None,
        consistency: Dict[str, Dict] = None,
        insights: Dict[str, Any] = None,
        base_filename: str = "character_analysis"
    ) -> Dict[str, str]:
        """
        Export all data in all formats
        Returns dict of format: filepath
        """
        
        exports = {}
        
        # CSV exports
        if comparisons:
            exports["csv_comparisons"] = self.export_comparison_data_csv(
                comparisons, f"{base_filename}_comparisons.csv"
            )
        
        exports["csv_progressions"] = self.export_arc_progression_csv(
            character_arcs, classifications, f"{base_filename}_progressions.csv"
        )
        
        if relationships:
            exports["csv_relationships"] = self.export_relationship_matrix_csv(
                relationships, f"{base_filename}_relationships.csv"
            )
        
        if consistency:
            exports["csv_consistency"] = self.export_consistency_reports_csv(
                consistency, f"{base_filename}_consistency.csv"
            )
        
        if insights:
            exports["csv_insights"] = self.export_insights_summary_csv(
                insights, f"{base_filename}_insights.csv"
            )
        
        # Excel export
        exports["excel"] = self.export_all_to_excel(
            character_arcs, classifications, comparisons,
            predictions, relationships, consistency, insights,
            f"{base_filename}_full.xlsx"
        )
        
        # PDF data preparation (actual PDF generation would use reportlab)
        pdf_data = self.prepare_pdf_data(
            character_arcs, classifications, predictions,
            relationships, consistency, insights
        )
        exports["pdf_data"] = pdf_data  # Return structured data for PDF generation
        
        return exports
