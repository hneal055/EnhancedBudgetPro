#!/bin/bash
echo "----------------------------------------" >> DAILY_REPORT.log
echo "🚀 Daily Startup Routine — $(date)" >> DAILY_REPORT.log
echo "----------------------------------------" >> DAILY_REPORT.log

echo "1) Checking Python & environment..." | tee -a DAILY_REPORT.log
python --version | tee -a DAILY_REPORT.log

echo "2) Running module import validation..." | tee -a DAILY_REPORT.log
python - << 'EOF' | tee -a DAILY_REPORT.log
from shared import clean_text
from src.BudgetEngine import ProductionBudget
from src.RiskModel import RiskModel
from src.IngestEngine.fountain_loader import FountainLoader

print("\n🟢 Import validation: PASSED")

script_sample = '''
INT. STUDIO - NIGHT
JOHN
We begin.
'''

loader = FountainLoader()
data = loader.load(script_sample)

print(f"Characters found: {list(data['characters'])}")
EOF

echo "3) Running Budget Test Run..." | tee -a DAILY_REPORT.log
python - << 'EOF' | tee -a DAILY_REPORT.log
from src.BudgetEngine import ProductionBudget
from src.RiskModel import RiskModel

budget = ProductionBudget(shoot_days=5)
budget.add_crew("Director", 1200)
budget.add_crew("DP", 900)
budget.add_equipment("Camera", 650)

risk = RiskModel(budget)
print("Budget:", budget.total_budget())
print("Risk-Adjusted:", risk.risk_adjusted_total())
EOF

echo "4) Generating PDF sample..." | tee -a DAILY_REPORT.log
python - << 'EOF' | tee -a DAILY_REPORT.log
from src.ExportEngine.pdf_reporter import PDFBudgetReport
from src.BudgetEngine import ProductionBudget

proj = ProductionBudget(shoot_days=3)
proj.add_crew("Sound", 400)
proj.add_equipment("Lighting Kit", 300)

PDFBudgetReport(proj).export("DAILY_TEST_REPORT.pdf")
print("📝 PDF Generated -> DAILY_TEST_REPORT.pdf")
EOF

echo "5) Launching Streamlit UI (preview only)..." | tee -a DAILY_REPORT.log
streamlit run ui_app.py --server.headless true --server.enableCORS false --server.port 8501 &

echo "🌅 Project System Ready."
echo "🟢 DAILY STARTUP COMPLETE $(date)" | tee -a DAILY_REPORT.log
echo "----------------------------------------" >> DAILY_REPORT.log
