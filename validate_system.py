"""
PILOTFORGEAI System Validation
Comprehensive check of all components before ship
"""

import sys
import os
from pathlib import Path

print("="*60)
print("PILOTFORGEAI SYSTEM VALIDATION")
print("="*60)

checks_passed = 0
checks_total = 0

def check(name, condition, details=""):
    global checks_passed, checks_total
    checks_total += 1
    if condition:
        print(f"✅ {name}")
        if details:
            print(f"   {details}")
        checks_passed += 1
        return True
    else:
        print(f"❌ {name}")
        if details:
            print(f"   {details}")
        return False

print("\n1. DIRECTORY STRUCTURE")
print("-"*60)
check("src/ directory exists", Path("src").exists())
check("IngestEngine exists", Path("src/IngestEngine").exists())
check("AnalysisEngine exists", Path("src/AnalysisEngine").exists())
check("EmotionEngine exists", Path("src/EmotionEngine").exists())
check("ProductionBudgetEngine exists", Path("src/ProductionBudgetEngine").exists())
check("ExportEngine exists", Path("src/ExportEngine").exists())
check("pages/ directory exists", Path("pages").exists())
check("samples/ directory exists", Path("samples").exists())

print("\n2. CORE MODULES")
print("-"*60)
try:
    from src.IngestEngine.file_router import route_file
    check("IngestEngine imports", True)
except Exception as e:
    check("IngestEngine imports", False, str(e))

try:
    from src.AnalysisEngine.character_intelligence import CharacterIntelligenceEngine
    check("AnalysisEngine imports", True)
except Exception as e:
    check("AnalysisEngine imports", False, str(e))

try:
    from src.EmotionEngine.detector import EmotionDetector
    check("EmotionEngine imports", True)
except Exception as e:
    check("EmotionEngine imports", False, str(e))

try:
    from src.ProductionBudgetEngine.master_production_budget_engine import MasterProductionBudgetEngine
    check("ProductionBudgetEngine imports", True)
except Exception as e:
    check("ProductionBudgetEngine imports", False, str(e))

try:
    from src.ExportEngine.csv_exporter import CSVExporter
    check("ExportEngine imports", True)
except Exception as e:
    check("ExportEngine imports", False, str(e))

print("\n3. SAMPLE FILES")
print("-"*60)
check("test_script.fdx exists", Path("samples/test_script.fdx").exists())
check("test_script.fountain exists", Path("samples/test_script.fountain").exists())
check("scale test scripts exist", Path("samples/scale_tests").exists())

print("\n4. STREAMLIT PAGES")
print("-"*60)
streamlit_pages = [
    "1_Story_Intelligence.py",
    "2_Character_Arcs.py",
    "3_Scene_Density.py",
    "4_Emotion_Analysis.py",
    "5_Financial_Intelligence.py",
    "6_Production_Budget.py",
    "7_Crew_Budget.py",
    "8_Equipment_Budget.py",
    "9_Location_Budget.py",
    "10_Post_Production.py",
    "11_Insurance_Contingency.py",
    "12_Risk_Analysis.py",
    "13_Monte_Carlo_Simulation.py",
    "14_Burn_Rate.py",
    "15_Export_Center.py",
    "16_Batch_Processing.py"
]

for page in streamlit_pages:
    exists = Path(f"pages/{page}").exists()
    check(f"Page: {page}", exists)

print("\n5. DOCUMENTATION")
print("-"*60)
docs = [
    "README.md",
    "requirements.txt",
    "GPU_ACCELERATION.md",
    "PERFORMANCE_OPTIMIZATION_JOURNEY.md",
    "PHASE_13_COMPLETE_SUMMARY.md"
]

for doc in docs:
    check(f"Doc: {doc}", Path(doc).exists())

print("\n6. ENTRY POINTS")
print("-"*60)
check("ui_app.py exists", Path("ui_app.py").exists())
check("web_app.py exists", Path("web_app.py").exists())
check("src/cli.py exists", Path("src/cli.py").exists())

print("\n7. TEST SUITE")
print("-"*60)
test_files = list(Path(".").glob("test_*.py"))
check(f"Test files present", len(test_files) > 0, f"{len(test_files)} test files found")

print("\n" + "="*60)
print(f"VALIDATION RESULTS: {checks_passed}/{checks_total} checks passed")
print("="*60)

if checks_passed == checks_total:
    print("✅ SYSTEM READY FOR DEPLOYMENT")
    sys.exit(0)
else:
    print("⚠️  Some checks failed - review above")
    sys.exit(1)
