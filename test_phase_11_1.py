"""
Phase 11.1 Validation Test
Tests the StudioExcelExporter with mock data
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.ExportEngine.excel_exporter_studio import StudioExcelExporter

# Mock session state with minimal required data
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
    },
    "schedule": {
        "shoot_days": 15,
        "day_assignments": {
            1: [0, 1],
            2: [2],
        }
    },
    "risks": [
        {"scene": "Scene 1", "risk_type": "Weather", "risk_level": "MEDIUM", "mitigation": "Rain cover plan"},
        {"scene": "Scene 2", "risk_type": "Location", "risk_level": "HIGH", "mitigation": "Backup location secured"},
        {"scene": "Scene 3", "risk_type": "Technical", "risk_level": "LOW", "mitigation": "Standard precautions"},
    ],
    "monte_carlo": {
        "p10": 210000,
        "p50": 230000,
        "p90": 265000,
    },
    "talent_overrides": {
        "JOHN": {"Day 5": "Medical appointment"},
        "MARY": {},
        "BOSS": {},
    }
}

def test_export():
    print("🧪 Testing Phase 11.1 - Studio Excel Exporter\n")
    
    exporter = StudioExcelExporter(project_name="Test_Project")
    output_dir = "./test_exports_phase_11_1"
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    print("1️⃣ Testing validation...")
    is_ready, message = exporter._validate_export_readiness(mock_session_state)
    print(f"   {message}")
    
    if not is_ready:
        print("\n❌ Validation failed - cannot export")
        return False
    
    print("\n2️⃣ Exporting Master Budget...")
    try:
        path = exporter.export_master_budget(mock_session_state, output_dir)
        print(f"   ✅ {path}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False
    
    print("\n3️⃣ Exporting Shooting Schedule...")
    try:
        path = exporter.export_shooting_schedule(mock_session_state, output_dir)
        print(f"   ✅ {path}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False
    
    print("\n4️⃣ Exporting Talent Availability...")
    try:
        path = exporter.export_talent_availability(mock_session_state, output_dir)
        print(f"   ✅ {path}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False
    
    print("\n5️⃣ Exporting Risk Forecast...")
    try:
        path = exporter.export_risk_forecast(mock_session_state, output_dir)
        print(f"   ✅ {path}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False
    
    print("\n6️⃣ Testing complete package export...")
    try:
        paths = exporter.export_all_studio_packages(mock_session_state, output_dir)
        print("   ✅ All files exported:")
        for name, path in paths.items():
            print(f"      - {name}: {Path(path).name}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False
    
    print("\n" + "="*60)
    print("✅ Phase 11.1 Validation: PASSED")
    print(f"📁 Output directory: {Path(output_dir).absolute()}")
    print("="*60)
    
    return True

if __name__ == "__main__":
    success = test_export()
    sys.exit(0 if success else 1)
