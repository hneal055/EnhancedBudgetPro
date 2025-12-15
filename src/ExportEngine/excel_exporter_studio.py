"""
Phase 11.1 - Excel Export Standardization
Studio-ready Excel exports with zero explanation required.

Core Rule: One row = one real-world line item
No nested dicts, no JSON blobs, no developer structures.
"""

import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')


class StudioExcelExporter:
    """
    Produces 4 standardized Excel files for film/TV production:
    - PILOTFORGE_Master_Budget.xlsx
    - PILOTFORGE_Shooting_Schedule.xlsx
    - PILOTFORGE_Talent_Availability.xlsx
    - PILOTFORGE_Risk_Forecast.xlsx
    """
    
    VERSION = "1.0.0"
    
    def __init__(self, project_name: str = "Untitled_Project"):
        self.project_name = project_name.replace(" ", "_")
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def _create_metadata_sheet(self, budget_locked: bool = True, 
                               schedule_locked: bool = True) -> pd.DataFrame:
        """Hidden metadata sheet for audit trail"""
        return pd.DataFrame([
            ["Project Name", self.project_name],
            ["Export Timestamp", self.timestamp],
            ["EBP Version", self.VERSION],
            ["Budget Locked", budget_locked],
            ["Schedule Locked", schedule_locked]
        ], columns=["Key", "Value"])
    
    def _validate_export_readiness(self, session_state: Dict) -> tuple[bool, str]:
        """
        Validate data contract before export.
        Returns: (is_ready, error_message)
        """
        checks = []
        
        # Budget locked
        if not session_state.get("master_budget"):
            checks.append("❌ Budget not calculated")
        
        # Schedule valid
        if not session_state.get("schedule"):
            checks.append("❌ Schedule not created")
        
        # Risk analysis completed
        if not session_state.get("risks"):
            checks.append("❌ Risk analysis incomplete")
        
        if checks:
            return False, "\n".join(checks)
        
        return True, "✅ Export ready"
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 1️⃣ PILOTFORGE_Master_Budget.xlsx
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    def export_master_budget(self, session_state: Dict, output_dir: str) -> str:
        """
        Exports: PILOTFORGE_Master_Budget.xlsx
        Sheets: Summary, Crew, Cast, Equipment, Locations, Post, Insurance
        """
        output_path = Path(output_dir) / f"PILOTFORGE_Master_Budget_{self.timestamp}.xlsx"
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Sheet 1: Summary
            summary_df = self._build_budget_summary(session_state)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Sheet 2: Crew
            crew_df = self._build_crew_sheet(session_state)
            crew_df.to_excel(writer, sheet_name='Crew', index=False)
            
            # Sheet 3: Cast
            cast_df = self._build_cast_sheet(session_state)
            cast_df.to_excel(writer, sheet_name='Cast', index=False)
            
            # Sheet 4: Equipment
            equipment_df = self._build_equipment_sheet(session_state)
            equipment_df.to_excel(writer, sheet_name='Equipment', index=False)
            
            # Sheet 5: Locations
            locations_df = self._build_locations_sheet(session_state)
            locations_df.to_excel(writer, sheet_name='Locations', index=False)
            
            # Sheet 6: Post
            post_df = self._build_post_sheet(session_state)
            post_df.to_excel(writer, sheet_name='Post', index=False)
            
            # Sheet 7: Insurance
            insurance_df = self._build_insurance_sheet(session_state)
            insurance_df.to_excel(writer, sheet_name='Insurance', index=False)
            
            # Metadata (hidden)
            metadata_df = self._create_metadata_sheet(budget_locked=True, schedule_locked=True)
            metadata_df.to_excel(writer, sheet_name='__METADATA', index=False)
        
        return str(output_path)
    
    def _build_budget_summary(self, session_state: Dict) -> pd.DataFrame:
        """High-level budget totals"""
        master_budget = session_state.get("master_budget", {})
        
        rows = [
            ["Above-The-Line", master_budget.get("cast_total", 0)],
            ["Crew", master_budget.get("crew_total", 0)],
            ["Equipment", master_budget.get("equipment_total", 0)],
            ["Locations", master_budget.get("location_total", 0)],
            ["Post-Production", master_budget.get("post_total", 0)],
            ["Insurance & Contingency", master_budget.get("insurance_total", 0)],
            ["GRAND TOTAL", master_budget.get("total", 0)]
        ]
        
        return pd.DataFrame(rows, columns=["Category", "Total Cost"])
    
    def _build_crew_sheet(self, session_state: Dict) -> pd.DataFrame:
        """Crew line items: Department | Role | Rate | Units | Unit Type | Total Cost | Notes"""
        crew_data = session_state.get("master_budget", {}).get("crew_breakdown", [])
        
        if not crew_data:
            # Generate from schedule if available
            schedule = session_state.get("schedule", {})
            shoot_days = schedule.get("shoot_days", 15)
            
            crew_data = [
                {"Department": "Direction", "Role": "Director", "Rate": 2500, "Units": shoot_days, "Unit_Type": "days", "Notes": ""},
                {"Department": "Camera", "Role": "DP", "Rate": 1500, "Units": shoot_days, "Unit_Type": "days", "Notes": ""},
                {"Department": "Camera", "Role": "1st AC", "Rate": 600, "Units": shoot_days, "Unit_Type": "days", "Notes": ""},
                {"Department": "Sound", "Role": "Sound Mixer", "Rate": 800, "Units": shoot_days, "Unit_Type": "days", "Notes": ""},
                {"Department": "Grip", "Role": "Key Grip", "Rate": 650, "Units": shoot_days, "Unit_Type": "days", "Notes": ""},
            ]
        
        # Flatten to row-based structure
        rows = []
        for item in crew_data:
            rows.append({
                "Department": item.get("Department", ""),
                "Role": item.get("Role", ""),
                "Rate": item.get("Rate", 0),
                "Units": item.get("Units", 0),
                "Unit Type": item.get("Unit_Type", "days"),
                "Total Cost": item.get("Rate", 0) * item.get("Units", 0),
                "Notes": item.get("Notes", "")
            })
        
        return pd.DataFrame(rows)
    
    def _build_cast_sheet(self, session_state: Dict) -> pd.DataFrame:
        """Cast costs per character"""
        intel = session_state.get("intel", {})
        cost_data = session_state.get("cost", {})
        
        rows = []
        character_stats = intel.get("character_stats", {})
        if character_stats:
            for char_name, char_stats in character_stats.items():
                rows.append({
                    "Character": char_name,
                    "Scenes": char_stats.get("scenes", 0),
                    "Dialogue Lines": char_stats.get("dialogue_lines", 0),
                    "Screen Time (min)": char_stats.get("estimated_screen_time_min", 0),
                    "Daily Rate": cost_data.get(char_name, {}).get("daily_rate", 500),
                    "Days Needed": char_stats.get("scenes", 0),
                    "Total Cost": cost_data.get(char_name, {}).get("total_cost", 0),
                    "Notes": ""
                })
        
        return pd.DataFrame(rows)
    
    def _build_equipment_sheet(self, session_state: Dict) -> pd.DataFrame:
        """Equipment rentals & gear"""
        master_budget = session_state.get("master_budget", {})
        equipment = master_budget.get("equipment_breakdown", [])
        
        if not equipment:
            # Default equipment package
            schedule = session_state.get("schedule", {})
            shoot_days = schedule.get("shoot_days", 15)
            
            equipment = [
                {"Package": "Camera", "Item": "RED KOMODO 6K Package", "Rate": 800, "Units": shoot_days, "Unit_Type": "days"},
                {"Package": "Lighting", "Item": "Lighting Package", "Rate": 1200, "Units": shoot_days, "Unit_Type": "days"},
                {"Package": "Grip", "Item": "Grip Truck", "Rate": 600, "Units": shoot_days, "Unit_Type": "days"},
                {"Package": "Sound", "Item": "Sound Package", "Rate": 400, "Units": shoot_days, "Unit_Type": "days"},
            ]
        
        rows = []
        for item in equipment:
            rows.append({
                "Package": item.get("Package", ""),
                "Item": item.get("Item", ""),
                "Rate": item.get("Rate", 0),
                "Units": item.get("Units", 0),
                "Unit Type": item.get("Unit_Type", "days"),
                "Total Cost": item.get("Rate", 0) * item.get("Units", 0),
                "Notes": item.get("Notes", "")
            })
        
        return pd.DataFrame(rows)
    
    def _build_locations_sheet(self, session_state: Dict) -> pd.DataFrame:
        """Location costs"""
        scenes = session_state.get("data", {}).get("scenes", [])
        
        # Aggregate unique locations
        location_costs = {}
        for scene in scenes:
            loc = scene.get("heading", "UNKNOWN")
            if loc not in location_costs:
                location_costs[loc] = {"scenes": 0, "cost": 2000}  # Default $2k per location
            location_costs[loc]["scenes"] += 1
        
        rows = []
        for location, info in location_costs.items():
            rows.append({
                "Location": location,
                "Scenes": info["scenes"],
                "Scout Cost": 500,
                "Permit Cost": 800,
                "Location Fee": info["cost"],
                "Total Cost": info["cost"] + 1300,
                "Notes": ""
            })
        
        return pd.DataFrame(rows)
    
    def _build_post_sheet(self, session_state: Dict) -> pd.DataFrame:
        """Post-production costs"""
        master_budget = session_state.get("master_budget", {})
        post = master_budget.get("post_breakdown", [])
        
        if not post:
            post = [
                {"Category": "Editing", "Item": "Editor (4 weeks)", "Rate": 3000, "Units": 4, "Unit_Type": "weeks"},
                {"Category": "Color", "Item": "Color Grading", "Rate": 5000, "Units": 1, "Unit_Type": "flat"},
                {"Category": "Sound", "Item": "Sound Design & Mix", "Rate": 8000, "Units": 1, "Unit_Type": "flat"},
                {"Category": "VFX", "Item": "VFX (10 shots)", "Rate": 500, "Units": 10, "Unit_Type": "shots"},
                {"Category": "Music", "Item": "Original Score", "Rate": 10000, "Units": 1, "Unit_Type": "flat"},
            ]
        
        rows = []
        for item in post:
            rows.append({
                "Category": item.get("Category", ""),
                "Item": item.get("Item", ""),
                "Rate": item.get("Rate", 0),
                "Units": item.get("Units", 0),
                "Unit Type": item.get("Unit_Type", ""),
                "Total Cost": item.get("Rate", 0) * item.get("Units", 1),
                "Notes": item.get("Notes", "")
            })
        
        return pd.DataFrame(rows)
    
    def _build_insurance_sheet(self, session_state: Dict) -> pd.DataFrame:
        """Insurance & contingency"""
        master_budget = session_state.get("master_budget", {})
        subtotal = master_budget.get("subtotal_before_insurance", 100000)
        
        rows = [
            {"Category": "General Liability", "Coverage": "2M/4M", "Rate": subtotal * 0.03, "Notes": "3% of budget"},
            {"Category": "E&O Insurance", "Coverage": "1M/3M", "Rate": subtotal * 0.02, "Notes": "2% of budget"},
            {"Category": "Equipment Insurance", "Coverage": "Replacement", "Rate": subtotal * 0.015, "Notes": "1.5% of budget"},
            {"Category": "Contingency (10%)", "Coverage": "Buffer", "Rate": subtotal * 0.10, "Notes": "10% of budget"},
        ]
        
        return pd.DataFrame(rows)
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 2️⃣ PILOTFORGE_Shooting_Schedule.xlsx
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    def export_shooting_schedule(self, session_state: Dict, output_dir: str) -> str:
        """
        Exports: PILOTFORGE_Shooting_Schedule.xlsx
        Sheets: Daily Schedule, Scene Breakdown
        """
        output_path = Path(output_dir) / f"PILOTFORGE_Shooting_Schedule_{self.timestamp}.xlsx"
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Sheet 1: Daily Schedule (stripboard-style)
            daily_df = self._build_daily_schedule(session_state)
            daily_df.to_excel(writer, sheet_name='Daily Schedule', index=False)
            
            # Sheet 2: Scene Breakdown
            breakdown_df = self._build_scene_breakdown(session_state)
            breakdown_df.to_excel(writer, sheet_name='Scene Breakdown', index=False)
            
            # Metadata
            metadata_df = self._create_metadata_sheet(schedule_locked=True)
            metadata_df.to_excel(writer, sheet_name='__METADATA', index=False)
        
        return str(output_path)
    
    def _build_daily_schedule(self, session_state: Dict) -> pd.DataFrame:
        """Stripboard-style daily schedule: Shoot Day | Scene | Location | Characters | Est. Cost | Risk"""
        schedule = session_state.get("schedule", {})
        scenes = session_state.get("data", {}).get("scenes", [])
        
        rows = []
        day_assignments = schedule.get("day_assignments", {})
        
        for day_num, scene_ids in day_assignments.items():
            for scene_id in scene_ids:
                if scene_id < len(scenes):
                    scene = scenes[scene_id]
                    rows.append({
                        "Shoot Day": day_num,
                        "Scene": f"Scene {scene_id + 1}",
                        "Location": scene.get("heading", ""),
                        "Characters": ", ".join(scene.get("characters", [])),
                        "Estimated Cost": 5000,  # Default per-scene cost
                        "Risk Level": "MEDIUM",
                        "Notes": ""
                    })
        
        # If no schedule, use linear
        if not rows:
            for i, scene in enumerate(scenes):
                rows.append({
                    "Shoot Day": (i // 3) + 1,  # ~3 scenes per day
                    "Scene": f"Scene {i + 1}",
                    "Location": scene.get("heading", ""),
                    "Characters": ", ".join(scene.get("characters", [])),
                    "Estimated Cost": 5000,
                    "Risk Level": "MEDIUM",
                    "Notes": ""
                })
        
        return pd.DataFrame(rows)
    
    def _build_scene_breakdown(self, session_state: Dict) -> pd.DataFrame:
        """Scene metadata"""
        scenes = session_state.get("data", {}).get("scenes", [])
        
        rows = []
        for i, scene in enumerate(scenes):
            rows.append({
                "Scene #": i + 1,
                "Heading": scene.get("heading", ""),
                "Characters": ", ".join(scene.get("characters", [])),
                "Dialogue Lines": scene.get("dialogue_lines", 0),
                "Action Lines": scene.get("action_lines", 0),
                "Page Est": round((scene.get("dialogue_lines", 0) + scene.get("action_lines", 0)) / 55, 2),
                "Notes": ""
            })
        
        return pd.DataFrame(rows)
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 3️⃣ PILOTFORGE_Talent_Availability.xlsx
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    def export_talent_availability(self, session_state: Dict, output_dir: str) -> str:
        """
        Exports: PILOTFORGE_Talent_Availability.xlsx
        One row per character per day (CRITICAL)
        """
        output_path = Path(output_dir) / f"PILOTFORGE_Talent_Availability_{self.timestamp}.xlsx"
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            availability_df = self._build_talent_availability(session_state)
            availability_df.to_excel(writer, sheet_name='Talent Availability', index=False)
            
            # Metadata
            metadata_df = self._create_metadata_sheet()
            metadata_df.to_excel(writer, sheet_name='__METADATA', index=False)
        
        return str(output_path)
    
    def _build_talent_availability(self, session_state: Dict) -> pd.DataFrame:
        """Character | Shoot Day | Availability | Conflict | Notes"""
        intel = session_state.get("intel", {})
        schedule = session_state.get("schedule", {})
        talent_overrides = session_state.get("talent_overrides", {})
        
        shoot_days = schedule.get("shoot_days", 15)
        
        rows = []
        for character in intel.keys():
            for day in range(1, shoot_days + 1):
                conflict = talent_overrides.get(character, {}).get(f"Day {day}", "")
                availability = "Available" if not conflict else "Conflict"
                
                rows.append({
                    "Character": character,
                    "Shoot Day": day,
                    "Availability": availability,
                    "Conflict": conflict,
                    "Notes": ""
                })
        
        return pd.DataFrame(rows)
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 4️⃣ PILOTFORGE_Risk_Forecast.xlsx
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    def export_risk_forecast(self, session_state: Dict, output_dir: str) -> str:
        """
        Exports: PILOTFORGE_Risk_Forecast.xlsx
        Sheets: Risk Summary, Scene Risk, Monte Carlo
        """
        output_path = Path(output_dir) / f"PILOTFORGE_Risk_Forecast_{self.timestamp}.xlsx"
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Sheet 1: Risk Summary
            summary_df = self._build_risk_summary(session_state)
            summary_df.to_excel(writer, sheet_name='Risk Summary', index=False)
            
            # Sheet 2: Scene Risk
            scene_risk_df = self._build_scene_risk(session_state)
            scene_risk_df.to_excel(writer, sheet_name='Scene Risk', index=False)
            
            # Sheet 3: Monte Carlo
            monte_carlo_df = self._build_monte_carlo(session_state)
            monte_carlo_df.to_excel(writer, sheet_name='Monte Carlo', index=False)
            
            # Metadata
            metadata_df = self._create_metadata_sheet()
            metadata_df.to_excel(writer, sheet_name='__METADATA', index=False)
        
        return str(output_path)
    
    def _build_risk_summary(self, session_state: Dict) -> pd.DataFrame:
        """High-level risk stats"""
        risks = session_state.get("risks", [])
        
        high = sum(1 for r in risks if r.get("risk_level") == "HIGH")
        medium = sum(1 for r in risks if r.get("risk_level") == "MEDIUM")
        low = sum(1 for r in risks if r.get("risk_level") == "LOW")
        
        rows = [
            ["High Risk Scenes", high],
            ["Medium Risk Scenes", medium],
            ["Low Risk Scenes", low],
            ["Total Scenes", len(risks)],
        ]
        
        return pd.DataFrame(rows, columns=["Metric", "Count"])
    
    def _build_scene_risk(self, session_state: Dict) -> pd.DataFrame:
        """Scene-level risk breakdown"""
        risks = session_state.get("risks", [])
        
        rows = []
        for risk in risks:
            rows.append({
                "Scene": risk.get("scene", ""),
                "Risk Type": risk.get("risk_type", ""),
                "Risk Level": risk.get("risk_level", ""),
                "Mitigation": risk.get("mitigation", ""),
                "Notes": ""
            })
        
        return pd.DataFrame(rows)
    
    def _build_monte_carlo(self, session_state: Dict) -> pd.DataFrame:
        """Monte Carlo simulation results"""
        monte_carlo = session_state.get("monte_carlo", {})
        
        if not monte_carlo:
            # Generate sample data
            rows = [
                {"Percentile": "P10 (Best Case)", "Budget": 95000},
                {"Percentile": "P50 (Most Likely)", "Budget": 115000},
                {"Percentile": "P90 (Worst Case)", "Budget": 145000},
            ]
        else:
            rows = [
                {"Percentile": "P10 (Best Case)", "Budget": monte_carlo.get("p10", 0)},
                {"Percentile": "P50 (Most Likely)", "Budget": monte_carlo.get("p50", 0)},
                {"Percentile": "P90 (Worst Case)", "Budget": monte_carlo.get("p90", 0)},
            ]
        
        return pd.DataFrame(rows)
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Master Export Function
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    def export_all_studio_packages(self, session_state: Dict, output_dir: str) -> Dict[str, str]:
        """
        Export all 4 standardized Excel files.
        Returns dict of file paths.
        """
        # Validate readiness
        is_ready, message = self._validate_export_readiness(session_state)
        if not is_ready:
            raise ValueError(f"Export validation failed:\n{message}")
        
        output_paths = {}
        
        try:
            output_paths["master_budget"] = self.export_master_budget(session_state, output_dir)
            output_paths["shooting_schedule"] = self.export_shooting_schedule(session_state, output_dir)
            output_paths["talent_availability"] = self.export_talent_availability(session_state, output_dir)
            output_paths["risk_forecast"] = self.export_risk_forecast(session_state, output_dir)
        except Exception as e:
            raise RuntimeError(f"Studio Excel export failed: {e}")
        
        return output_paths
