Write-Host "----------------------------------------"
Write-Host "🚀 Daily Startup Routine — $(Get-Date)"
Write-Host "----------------------------------------"

$env:PYTHONPATH = "C:\Projects\FilmStudioDev\EnhancedBudgetPro;C:\Projects\FilmStudioDev\SharedLibraries"

Write-Host "`n1) Python Check"
python --version

Write-Host "`n2) Core Import Test"
python -c "from src.BudgetEngine import ProductionBudget; from src.RiskModel import RiskModel; from src.IngestEngine.fountain_loader import FountainLoader; print('✅ Core imports OK')"

Write-Host "`n3) Fountain Loader Test"
python -c "from src.IngestEngine.fountain_loader import FountainLoader; s='''INT. STUDIO - NIGHT\nJOHN\nWe begin.'''; d=FountainLoader().load(s); print('✅ Scenes:', d['scene_count'])"

Write-Host "`n4) Budget + Risk Test"
python -c "from src.BudgetEngine import ProductionBudget; from src.RiskModel import RiskModel; b=ProductionBudget(5); b.add_crew('Director',1200); b.add_crew('DP',900); b.add_equipment('Camera',650); r=RiskModel(b); print('✅ Base:', b.total_budget()); print('✅ Risk:', r.risk_adjusted_total())"

Write-Host "`n5) Plain Text + CSV Export Test"
python -c "from src.ExportEngine.csv_exporter import CSVExporter; from src.IngestEngine.plaintext_loader import PlainTextLoader; s='''INT. TEST - DAY\nALICE\nThis is a test.'''; d=PlainTextLoader().load(s); CSVExporter().export(d,'DAILY_WINDOWS_TEST.csv'); print('✅ CSV Created')"

Write-Host "`n✅ DAILY STARTUP COMPLETE"
Write-Host "----------------------------------------"

