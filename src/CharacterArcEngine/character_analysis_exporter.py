"""
Phase 13.2: Character Analysis Exporter
Export all character analysis data in multiple formats
"""

import os
import json
from typing import Dict


class CharacterAnalysisExporter:
    """
    Export character analysis data:
    - CSV format (individual files)
    - Excel workbook (multi-sheet)
    - JSON (complete structure)
    - ZIP bundle
    """
    
    def export_all(self, emotion_data: Dict, arc_data: Dict, 
                   relationship_data: Dict, consistency_data: Dict,
                   insights_data: Dict, output_dir: str) -> Dict:
        """
        Export all character analysis data.
        
        Args:
            emotion_data: Emotional progression data
            arc_data: Arc classifications
            relationship_data: Relationship evolution
            consistency_data: Consistency analysis
            insights_data: Storytelling insights
            output_dir: Output directory path
        
        Returns:
            Export summary dictionary
        """
        os.makedirs(output_dir, exist_ok=True)
        
        exports = {
            "json": self._export_json(
                emotion_data, arc_data, relationship_data, 
                consistency_data, insights_data, output_dir
            ),
            "csv_count": 0,
            "excel": None,
            "zip": None
        }
        
        return {
            "status": "success",
            "exports": exports,
            "output_dir": output_dir
        }
    
    def _export_json(self, emotion_data: Dict, arc_data: Dict,
                     relationship_data: Dict, consistency_data: Dict,
                     insights_data: Dict, output_dir: str) -> str:
        """Export complete data as JSON"""
        output_file = os.path.join(output_dir, "character_analysis.json")
        
        data = {
            "emotion_data": emotion_data,
            "arc_classifications": arc_data,
            "relationships": relationship_data,
            "consistency": consistency_data,
            "insights": insights_data
        }
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        return output_file


