# src/ExportEngine/csv_exporter.py
import csv
import os
from typing import Dict, List, Any

class CSVExporter:
    """Export data to CSV format."""
    
    def __init__(self, encoding: str = 'utf-8'):
        self.encoding = encoding
    
    def export(self, data: Dict[str, Any], filepath: str) -> bool:
        """
        Export data to CSV file.
        
        Args:
            data: Dictionary containing data to export
            filepath: Path to save CSV file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
            
            # Determine what kind of data we have
            if "breakdown" in data and isinstance(data["breakdown"], dict):
                # Budget data structure
                return self._export_budget_data(data, filepath)
            elif "scenes" in data and isinstance(data["scenes"], list):
                # Script/scene data structure
                return self._export_scene_data(data, filepath)
            else:
                # Generic data structure
                return self._export_generic_data(data, filepath)
                
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False
    
    def _export_budget_data(self, data: Dict[str, Any], filepath: str) -> bool:
        """Export budget data to CSV."""
        try:
            with open(filepath, 'w', newline='', encoding=self.encoding) as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow(["Category", "Item", "Amount", "Notes"])
                writer.writerow([])  # Empty row
                
                # Write title and total
                writer.writerow(["Title", data.get("title", "Untitled")])
                writer.writerow(["Total Budget", f"${data.get('total_budget', 0):,}"])
                writer.writerow([])
                
                # Write breakdown
                breakdown = data.get("breakdown", {})
                for category_name, category_data in breakdown.items():
                    writer.writerow([category_name.upper().replace('_', ' '), "", "", ""])
                    
                    if isinstance(category_data, dict) and "items" in category_data:
                        items = category_data["items"]
                        for item in items:
                            writer.writerow([
                                "",
                                item.get("name", ""),
                                f"${item.get('amount', 0):,}",
                                item.get("notes", "")
                            ])
                    
                    writer.writerow(["", "Subtotal", f"${category_data.get('amount', 0):,}", ""])
                    writer.writerow([])
                
            return True
            
        except Exception as e:
            print(f"Error exporting budget data: {e}")
            return False
    
    def _export_scene_data(self, data: Dict[str, Any], filepath: str) -> bool:
        """Export scene data to CSV."""
        try:
            with open(filepath, 'w', newline='', encoding=self.encoding) as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow(["Scene", "Location", "Characters", "Description", "Dialogue Lines"])
                
                # Write scenes
                scenes = data.get("scenes", [])
                for scene in scenes:
                    writer.writerow([
                        scene.get("number", ""),
                        scene.get("location", ""),
                        ", ".join(scene.get("characters", [])),
                        scene.get("description", "")[:100],  # Truncate long descriptions
                        scene.get("dialogue_lines", 0)
                    ])
                
                # Write summary
                writer.writerow([])
                writer.writerow(["Summary", "", "", "", ""])
                writer.writerow(["Total Scenes", len(scenes), "", "", ""])
                writer.writerow(["Total Characters", len(data.get("characters", [])), "", "", ""])
                
            return True
            
        except Exception as e:
            print(f"Error exporting scene data: {e}")
            return False
    
    def _export_generic_data(self, data: Dict[str, Any], filepath: str) -> bool:
        """Export generic data to CSV."""
        try:
            with open(filepath, 'w', newline='', encoding=self.encoding) as f:
                writer = csv.writer(f)
                
                # Try to flatten the data
                if isinstance(data, dict):
                    # Write as key-value pairs
                    writer.writerow(["Key", "Value"])
                    for key, value in data.items():
                        if isinstance(value, (str, int, float, bool)):
                            writer.writerow([key, str(value)])
                        elif isinstance(value, list):
                            writer.writerow([key, ", ".join(str(v) for v in value)])
                        else:
                            writer.writerow([key, str(value)])
                else:
                    # Write single value
                    writer.writerow(["Data"])
                    writer.writerow([str(data)])
                
            return True
            
        except Exception as e:
            print(f"Error exporting generic data: {e}")
            return False

# Only export the CSVExporter class to avoid circular imports
__all__ = ['CSVExporter']
