"""
Test Master Budget Export Only
Focus on getting this one file perfect before expanding
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.ExportEngine.excel_exporter_studio import StudioExcelExporter
import pandas as pd

# Enhanced mock data with more realistic budget breakdown
mock_session_state = {
    "data": {
        "scenes": [
            {"heading": "INT. OFFICE - DAY", "characters": ["JOHN", "MARY"], "dialogue_lines": 15, "action_lines": 10},
            {"heading": "EXT. STREET - NIGHT", "characters": ["JOHN"], "dialogue_lines": 8, "action_lines": 5},
            {"heading": "INT. CAR - DAY", "characters": ["MARY", "BOSS"], "dialogue_lines": 12, "action_lines": 3},
        ]
    },
    "intel": {
        "JOHN": {"scenes": 2, "dialogue_lines": 23, "estimated_screen_time_min": 15},
        "MARY": {"scenes": 2, "dialogue_lines": 27, "estimated_screen_time_min": 18},
        "BOSS": {"scenes": 1, "dialogue_lines": 12, "estimated_screen_time_min": 8},
    },
    "cost": {
        "JOHN": {"daily_rate": 800, "total_cost": 8000},
        "MARY": {"daily_rate": 750, "total_cost": 7500},
        "BOSS": {"daily_rate": 500, "total_cost": 2500},
    },
    "master_budget": {
        "cast_total": 18000,
        "crew_total": 95000,
        "equipment_total": 45000,
        "location_total": 12000,
        "post_total": 35000,
        "insurance_total": 25000,
        "total": 230000,
        "subtotal_before_insurance": 205000,
        # Add detailed breakdowns
        "crew_breakdown": [
            {"Department": "Direction", "Role": "Director", "Rate": 2500, "Units": 15, "Unit_Type": "days", "Notes": "Lead creative"},
            {"Department": "Direction", "Role": "1st AD", "Rate": 1200, "Units": 15, "Unit_Type": "days", "Notes": ""},
            {"Department": "Camera", "Role": "Director of Photography", "Rate": 1500, "Units": 15, "Unit_Type": "days", "Notes": ""},
            {"Department": "Camera", "Role": "1st AC", "Rate": 600, "Units": 15, "Unit_Type": "days", "Notes": ""},
            {"Department": "Camera", "Role": "2nd AC", "Rate": 450, "Units": 15, "Unit_Type": "days", "Notes": ""},
            {"Department": "Sound", "Role": "Sound Mixer", "Rate": 800, "Units": 15, "Unit_Type": "days", "Notes": ""},
            {"Department": "Sound", "Role": "Boom Operator", "Rate": 500, "Units": 15, "Unit_Type": "days", "Notes": ""},
            {"Department": "Grip", "Role": "Key Grip", "Rate": 650, "Units": 15, "Unit_Type": "days", "Notes": ""},
            {"Department": "Electric", "Role": "Gaffer", "Rate": 700, "Units": 15, "Unit_Type": "days", "Notes": ""},
        ],
        "equipment_breakdown": [
            {"Package": "Camera", "Item": "ARRI Alexa Mini LF", "Rate": 1200, "Units": 15, "Unit_Type": "days", "Notes": ""},
            {"Package": "Camera", "Item": "Cinema Lenses", "Rate": 800, "Units": 15, "Unit_Type": "days", "Notes": ""},
            {"Package": "Lighting", "Item": "HMI Package", "Rate": 1500, "Units": 15, "Unit_Type": "days", "Notes": ""},
            {"Package": "Grip", "Item": "Grip Truck & Equipment", "Rate": 600, "Units": 15, "Unit_Type": "days", "Notes": ""},
            {"Package": "Sound", "Item": "Sound Package", "Rate": 400, "Units": 15, "Unit_Type": "days", "Notes": ""},
        ],
        "post_breakdown": [
            {"Category": "Editing", "Item": "Editor (6 weeks)", "Rate": 3000, "Units": 6, "Unit_Type": "weeks", "Notes": ""},
            {"Category": "Color", "Item": "Color Grading", "Rate": 7000, "Units": 1, "Unit_Type": "flat", "Notes": ""},
            {"Category": "Sound", "Item": "Sound Design", "Rate": 5000, "Units": 1, "Unit_Type": "flat", "Notes": ""},
            {"Category": "Sound", "Item": "Final Mix", "Rate": 8000, "Units": 1, "Unit_Type": "flat", "Notes": ""},
            {"Category": "VFX", "Item": "VFX (15 shots)", "Rate": 500, "Units": 15, "Unit_Type": "shots", "Notes": ""},
            {"Category": "Music", "Item": "Original Score", "Rate": 12000, "Units": 1, "Unit_Type": "flat", "Notes": ""},
        ]
    },
    "schedule": {
        "shoot_days": 15,
        "day_assignments": {1: [0, 1], 2: [2]}
    },
    "risks": [
        {"scene": "Scene 1", "risk_type": "Weather", "risk_level": "MEDIUM", "mitigation": "Rain cover plan"},
    ],
}

def test_master_budget():
    print("🧪 Testing Master Budget Export\n")
    print("="*60)
    
    exporter = StudioExcelExporter(project_name="Sample_Production")
    output_dir = "./exports"
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    print("\n📊 Generating EBP_Master_Budget.xlsx...")
    print("-" * 60)
    
    try:
        path = exporter.export_master_budget(mock_session_state, output_dir)
        print(f"✅ EXPORTED: {path}\n")
        
        # Validate the file
        print("🔍 Validating Excel file structure...\n")
        
        with pd.ExcelFile(path) as xls:
            sheets = xls.sheet_names
            print(f"📑 Sheets found: {len(sheets)}")
            for sheet in sheets:
                df = pd.read_excel(xls, sheet_name=sheet)
                print(f"   - {sheet:20s} ({len(df)} rows, {len(df.columns)} columns)")
                
                # Show first few rows of key sheets
                if sheet in ["Summary", "Crew", "Cast"]:
                    print(f"\n   Preview of {sheet}:")
                    print(df.head().to_string(index=False))
                    print()
        
        print("\n" + "="*60)
        print("✅ Master Budget Export: SUCCESS")
        print("="*60)
        print(f"\n📁 File location: {Path(path).absolute()}")
        print("\n📋 Next Steps:")
        print("   1. Open the Excel file and verify formatting")
        print("   2. Check all sheets for data accuracy")
        print("   3. Verify no nested structures or JSON blobs")
        print("   4. Confirm studio-ready quality")
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_master_budget()
    sys.exit(0 if success else 1)
