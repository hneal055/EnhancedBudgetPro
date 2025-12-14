# Enhanced Budget Pro — User Guide

**Version:** 1.0.0  
**Last Updated:** December 13, 2025  
**Audience:** Production Managers, Budget Analysts, Producers

---

## 📚 Table of Contents

1. [Getting Started](#getting-started)
2. [Interface Selection Guide](#interface-selection-guide)
3. [CLI Usage](#cli-usage)
4. [Web App Usage](#web-app-usage)
5. [Streamlit Dashboard](#streamlit-dashboard)
6. [Workflow Examples](#workflow-examples)
7. [Understanding Reports](#understanding-reports)
8. [Best Practices](#best-practices)
9. [FAQ](#faq)
10. [Troubleshooting](#troubleshooting)

---

## 🚀 Getting Started

### Prerequisites
- **Python**: 3.12 or higher
- **Operating System**: Windows, macOS, or Linux
- **Storage**: 500MB free space (for outputs)
- **Memory**: 4GB RAM minimum (8GB recommended for large scripts)

### Installation

#### Step 1: Verify Python
```bash
python --version
# Expected: Python 3.12.x or higher
```

#### Step 2: Activate Virtual Environment
```bash
# Windows PowerShell
cd C:\Projects\FilmStudioDev\EnhancedBudgetPro
.\.venv\Scripts\Activate.ps1

# Windows CMD
.\.venv\Scripts\activate.bat

# macOS/Linux
source .venv/bin/activate
```

#### Step 3: Verify Installation
```bash
python -m pip list | Select-String "streamlit|pandas|plotly"
```

Expected output:
```
pandas         2.0.0
plotly         5.17.0
streamlit      1.28.0
```

### First Run Test
```bash
# Test CLI
python -m src.cli analyze --input samples/test_script.fdx --out ./test_output

# Expected: Creates test_output/ with 5 files
```

---

## 🎯 Interface Selection Guide

### When to Use CLI
✅ **Best for:**
- Automating budget analysis in scripts
- Batch processing multiple scripts
- CI/CD pipeline integration
- Headless server environments
- Scheduled daily/weekly reports

❌ **Not ideal for:**
- First-time users (steep learning curve)
- Interactive exploration
- Real-time collaboration

### When to Use Web App
✅ **Best for:**
- Quick one-off analyses
- Non-technical users (producers, ADs)
- Sharing with external stakeholders
- Mobile/tablet access
- Simple upload-download workflow

❌ **Not ideal for:**
- Deep analysis requiring multiple iterations
- Comparing scenarios side-by-side
- Customizing parameters extensively

### When to Use Streamlit Dashboard
✅ **Best for:**
- Power users (production managers, budget analysts)
- Interactive exploration of budget scenarios
- Real-time parameter adjustments
- Detailed what-if analysis
- Team collaboration sessions

❌ **Not ideal for:**
- Automation (no API)
- Quick one-time analyses (overhead)
- Mobile devices (desktop-optimized)

---

## 🖥️ CLI Usage

### Basic Commands

#### Analyze Single Script
```bash
python -m src.cli analyze --input <script_path> --out <output_dir>
```

**Example:**
```bash
python -m src.cli analyze --input samples/episode1.fdx --out ./analysis_ep1
```

**Output Structure:**
```
analysis_ep1/
├── scenes.csv          # Scene-by-scene breakdown
├── characters.csv      # Character intelligence metrics
├── budget.csv          # Budget line items
├── risk.csv            # Risk assessment per scene
└── summary.json        # Complete analysis (machine-readable)
```

#### Batch Process Multiple Scripts
```bash
python -m src.cli batch --input_dir <scripts_folder> --out <output_dir>
```

**Example:**
```bash
python -m src.cli batch --input_dir ./season1_scripts --out ./season1_analysis
```

**Output Structure:**
```
season1_analysis/
├── episode1_fdx_20251213_170532/
│   ├── scenes.csv
│   ├── characters.csv
│   ├── budget.csv
│   └── ...
├── episode2_fdx_20251213_170545/
│   └── ...
└── batch_summary.json  # Aggregated statistics
```

### Advanced Options

#### Custom Shoot Days
```bash
python -m src.cli analyze --input script.fdx --out ./output --shoot-days 10
# Default: 5 days
```

#### Specify Output Format
```bash
python -m src.cli analyze --input script.fdx --out ./output --formats csv,excel,pdf
# Default: all formats
```

#### Verbose Output
```bash
python -m src.cli analyze --input script.fdx --out ./output --verbose
# Shows detailed progress logs
```

### CLI Workflow Example

**Scenario:** Analyzing a weekly TV series (10 episodes)

```bash
# Step 1: Create output directory
mkdir season1_analysis
cd season1_analysis

# Step 2: Batch process all scripts
python -m src.cli batch --input_dir ../scripts/season1 --out ./weekly

# Step 3: Review batch summary
cat ./weekly/batch_summary.json

# Step 4: Compare episode budgets
python -c "
import pandas as pd
import glob

budgets = []
for file in glob.glob('weekly/*/budget.csv'):
    df = pd.read_csv(file)
    budgets.append({'episode': file.split('/')[1], 'total': df['total'].sum()})

comparison = pd.DataFrame(budgets)
print(comparison.to_string())
"
```

---

## 🌐 Web App Usage

### Starting the Web App

```bash
python web_app.py
```

**Access:** http://localhost:5000

### Step-by-Step Workflow

#### 1. Upload Script
- Click **"Choose File"** or drag-and-drop
- Supported formats: .fdx, .fountain, .celtx, .celtx.json, .pdf, .txt
- Max size: 50MB (configurable in web_app.py)

#### 2. Configure Analysis
- **Shoot Days:** Default 5 (adjustable 1-100)
- **Risk Factor:** Default 10% (adjustable 0-50%)
- **Export Formats:** Select CSV, Excel, PDF, or All

#### 3. Run Analysis
- Click **"Analyze Script"**
- Progress bar shows real-time status
- Typical processing: 5-30 seconds depending on script length

#### 4. Review Results
- **Summary Dashboard:**
  - Total budget
  - Scene count
  - Character count
  - Risk level
- **Interactive Charts:**
  - Budget breakdown by category
  - Scene density histogram
  - Risk distribution

#### 5. Download Reports
- Click **"Download All Reports"** (ZIP archive)
- Or download individual files:
  - scenes.csv
  - budget.csv
  - risk.csv
  - summary.json

### Web App Features

#### Job History
- View past 20 analyses
- Click job ID to redownload reports
- Automatic cleanup after 7 days

#### Share Analysis
- Copy shareable link: `http://localhost:5000/view/{job_id}`
- Recipients can download reports without re-running analysis

#### Mobile Support
- Responsive design works on tablets
- Upload from device camera (for photographed scripts)

---

## 🎨 Streamlit Dashboard

### Launching Dashboard

```bash
.\.venv\Scripts\streamlit.exe run ui_app.py
```

**Access:** http://localhost:8501

### Dashboard Navigation

**Multi-Page Architecture:** Enhanced Budget Pro uses Streamlit's multi-page apps feature. Navigate using the **sidebar** (click `>` in top-left if collapsed).

**15 Available Pages:**
- Page 0: Command Center (main upload & overview)
- Page 1: Story Intelligence
- Page 2: Financial Intelligence
- Page 3: Production Budget
- Page 4: Risk & Monte Carlo
- Page 5-6: Scheduling & Stripboard
- Page 6-7: Talent Availability
- Page 7-9: What-If Scenarios & Optimization
- Page 6: Export Center

**Session State:** All data persists across pages - navigate freely without losing work.

#### 🏠 Command Center (Page 0)
- Upload/paste script for analysis
- View pipeline status dashboard
- Quick navigation links to all phases
- Real-time project metrics

#### Phase 1: 📘 Story Intelligence
**Purpose:** Character and scene analysis

**Key Metrics:**
- Character frequency (scenes per character)
- Dialogue density (lines per character)
- Screen time estimation
- Scene complexity scores

**Use Case:** Identify lead roles, ensemble balance, dialogue-heavy scenes

**Actions:**
- Filter characters by scene count
- Export character matrix to CSV
- View scene sequence diagram

#### Phase 2: 💰 Financial Intelligence
**Purpose:** Cost impact analysis

**Key Metrics:**
- Character-to-cost mapping
- Scene cost estimation
- Daily burn rate
- Cost per page

**Use Case:** Understand which characters/scenes drive budget

**Actions:**
- Adjust character day rates
- Recalculate cost impact
- Export cost breakdown

#### Phase 3: 📊 Production Budget
**Purpose:** Detailed budget estimation

**Categories:**
- Crew (Director, DP, AD, etc.)
- Equipment (Camera, Lighting, Grip)
- Location (Scouts, Permits, Fees)
- Post-Production (Editing, VFX, Sound)
- Insurance & Contingency

**Actions:**
- Customize rates for each line item
- Add custom budget categories
- Export to Excel/PDF
- Compare against historical budgets

#### Phase 4: ⚠️ Risk & Monte Carlo
**Purpose:** Risk assessment and uncertainty modeling

**Features:**
- Monte Carlo simulations (1000+ runs)
- P10/P50/P90 percentile projections
- Risk distribution visualization
- Scenario probability analysis

**Use Case:** Understand budget uncertainty range, plan contingencies

**Actions:**
- Adjust volatility factor (5-20%)
- Run sensitivity analysis
- Export risk report

#### Phase 5: 🎬 Scheduling & Stripboard
**Purpose:** Shooting schedule optimization

**Features:**
- Scene sorting (by location, time, cast)
- Day breakdown
- Cast availability check
- Travel time estimation

**Use Case:** Create efficient shooting schedule, minimize company moves

**Actions:**
- Drag-and-drop scene reordering
- Color-code by location
- Export stripboard PDF
- Sync with production calendar

#### Phase 6: 🎭 Talent Availability
**Purpose:** Cast scheduling conflicts

**Features:**
- Import talent calendars
- Conflict detection
- Auto-rescheduling suggestions
- Alternate casting scenarios

**Use Case:** Avoid scheduling conflicts, plan around actor availability

**Actions:**
- Upload talent availability CSV
- Run conflict analysis
- Apply recommended changes
- Export revised schedule

#### Phase 7: 🔮 What-If Scenarios
**Purpose:** Budget optimization via scenario comparison

**Features:**
- Multi-scenario generator
- Parameter sweeps (shoot days, crew size, location)
- Cost-benefit analysis
- Optimization recommendations

**Use Case:** Find optimal budget allocation, compare production strategies

**Actions:**
- Define scenario parameters
- Run batch simulations
- Compare results side-by-side
- Export comparison table

#### Phase 8: 🤖 AI Scenario Designer
**Purpose:** AI-powered budget recommendations

**Features:**
- ML-based scenario generation
- Historical pattern analysis
- Cost reduction suggestions
- Risk mitigation strategies

**Use Case:** Leverage AI for non-obvious optimizations

**Actions:**
- Train on historical data
- Generate AI scenarios
- Review recommendations
- Apply selected changes

#### Phase 9: 📊 Scenario Visualization
**Purpose:** Visual comparison of what-if scenarios

**Charts:**
- Cost comparison bar chart (Mean + P10-P90 range)
- Uncertainty funnel
- Gradient cost meter

**Use Case:** Communicate scenarios to stakeholders, make data-driven decisions

**Actions:**
- Filter scenarios by criteria
- Export charts as PNG
- Generate presentation deck

### Dashboard Workflow Example

**Scenario:** Optimizing a 20-day shoot for a $2M indie feature

1. **Upload Script** (Command Center)
   - Upload screenplay.fdx
   - Set initial shoot days: 20

2. **Analyze Characters** (Phase 1)
   - Identify 3 leads, 5 supporting, 12 day players
   - Note: Lead #1 appears in 80% of scenes

3. **Review Base Budget** (Phase 3)
   - Initial estimate: $2.3M (over budget!)
   - Largest cost: Equipment ($450K)

4. **Run Monte Carlo** (Phase 4)
   - P50: $2.3M
   - P90: $2.6M (too risky)

5. **Create What-If Scenarios** (Phase 7)
   - Scenario A: Reduce shoot to 18 days
   - Scenario B: Use smaller camera package
   - Scenario C: Combine A + B
   - Result: Scenario C saves $400K, P90 = $2.1M ✅

6. **Visualize Options** (Phase 9)
   - Show comparison charts to director/producer
   - Decision: Proceed with Scenario C

7. **Export Final Budget** (Phase 3)
   - Download Excel file for line producer
   - Generate PDF for investors

---

## 📊 Understanding Reports

### scenes.csv
**Columns:**
- `scene_num`: Scene number (1, 2, 3...)
- `heading`: Scene heading (e.g., "INT. OFFICE - DAY")
- `characters`: List of characters in scene
- `dialogue_lines`: Number of dialogue lines
- `action_lines`: Number of action lines
- `complexity`: LOW/MEDIUM/HIGH
- `estimated_time`: Shooting time estimate (hours)

**Use Case:** Scheduling, scene prioritization

### characters.csv
**Columns:**
- `character`: Character name
- `scene_count`: Number of scenes character appears in
- `dialogue_lines`: Total dialogue lines
- `screen_time_min`: Estimated screen time (minutes)
- `role_type`: LEAD/SUPPORTING/DAY_PLAYER
- `estimated_cost`: Budget allocation for character

**Use Case:** Casting, talent budgeting

### budget.csv
**Columns:**
- `category`: Budget category (Crew, Equipment, etc.)
- `item`: Line item (Director, Camera, etc.)
- `rate`: Daily/unit rate ($)
- `quantity`: Number of units/days
- `total`: Calculated total ($)

**Use Case:** Budget review, cost tracking

### risk.csv
**Columns:**
- `scene`: Scene heading
- `risk_type`: Category (Location, Weather, Talent, Technical)
- `risk_level`: HIGH/MEDIUM/LOW
- `probability`: Likelihood (0-100%)
- `impact`: Financial impact if occurs ($)
- `mitigation`: Recommended action

**Use Case:** Risk management, contingency planning

### summary.json
**Structure:**
```json
{
  "script_info": {
    "filename": "episode1.fdx",
    "format": "FDX",
    "scene_count": 12,
    "character_count": 8,
    "page_estimate": 45
  },
  "budget_summary": {
    "total_budget": 2300000,
    "crew_cost": 850000,
    "equipment_cost": 450000,
    "location_cost": 320000,
    "post_cost": 480000,
    "insurance": 57500,
    "contingency": 142500
  },
  "risk_summary": {
    "mean_budget": 2300000,
    "p10": 2100000,
    "p50": 2300000,
    "p90": 2550000,
    "volatility": 10
  }
}
```

**Use Case:** Machine processing, dashboards, API integration

---

## 💡 Best Practices

### Script Preparation
1. **Use Standard Formatting**
   - FDX exports from Final Draft are most reliable
   - Fountain for lightweight/open-source workflows
   - Avoid heavily formatted PDFs (use OCR as last resort)

2. **Clean Character Names**
   - Consistent ALL CAPS for character names
   - Avoid parentheticals in character headers: ❌ `JOHN (V.O.)` → ✅ `JOHN`
   - Use same name throughout: ❌ `JOHN`/`JOHNNY`/`J.` → ✅ `JOHN`

3. **Structure Scenes Clearly**
   - Always start with proper scene heading: `INT./EXT. LOCATION - TIME`
   - Avoid nested scene headings
   - Use `CONTINUOUS` for running scenes

### Budget Estimation
1. **Start with Defaults**
   - Run initial analysis with default rates
   - Identify major cost drivers
   - Then customize rates based on your market

2. **Adjust for Location**
   - NYC/LA: multiply crew rates by 1.3x
   - Regional markets: multiply by 0.7-0.9x
   - International: research local union rates

3. **Factor in Scale**
   - Micro-budget (<$500K): use minimal crew package
   - Low-budget ($500K-$2M): standard indie package
   - Mid-budget ($2M-$10M): add specialists (gaffer, key grip)
   - High-budget (>$10M): full union crew

### Risk Management
1. **Run Multiple Scenarios**
   - Best case (P10)
   - Expected case (P50)
   - Worst case (P90)
   - Plan for P75 (safer than P50, not as conservative as P90)

2. **Identify Top 5 Risks**
   - Use risk.csv to prioritize
   - Develop specific mitigation plans
   - Allocate contingency funds proportionally

3. **Update Regularly**
   - Re-run analysis after script changes
   - Update actual costs as production progresses
   - Track variance: actual vs. estimated

### Collaboration
1. **Share Read-Only Reports**
   - Export PDF for executives (clean, professional)
   - Share Excel for line producers (editable)
   - Use web app links for quick sharing

2. **Version Control**
   - Name outputs with date: `budget_ep1_2025-12-13.xlsx`
   - Keep script revisions in separate folders
   - Document assumptions in notes field

3. **Integrate with Other Tools**
   - Import budget into Movie Magic Budgeting
   - Export schedule to StudioBinder
   - Sync with accounting software (QuickBooks, Xero)

---

## ❓ FAQ

### General Questions

**Q: What script formats are supported?**
A: FDX (Final Draft), Fountain, Celtx JSON, PDF (text-based), and plain text.

**Q: How accurate are the budget estimates?**
A: Within ±15% for typical indie productions when using default rates. Accuracy improves with custom rate adjustments.

**Q: Can I use this for commercials or music videos?**
A: Yes! Adjust shoot_days to 1-2 days and customize crew package.

**Q: Is my data secure?**
A: All processing is local. No data sent to external servers (unless using cloud storage).

**Q: Can multiple users access simultaneously?**
A: Yes for Web App and Streamlit (separate sessions). CLI is single-user per run.

### Technical Questions

**Q: Why is my scene count 0?**
A: Ensure script uses standard scene headings: `INT./EXT.`. Check that file isn't corrupted.

**Q: Characters not detected?**
A: Character names must be ALL CAPS and on their own line. Avoid inline names in action.

**Q: Budget seems too high/low?**
A: Check shoot_days parameter and verify regional crew rates match your market.

**Q: Can I add custom budget categories?**
A: Yes! Edit `src/ProductionBudgetEngine/master_production_budget_engine.py` or use Streamlit custom fields.

**Q: How do I export to Movie Magic?**
A: Export Excel, then import into Movie Magic using their CSV importer.

### Troubleshooting Questions

**Q: "ModuleNotFoundError: No module named 'X'"**
A: Reinstall dependencies: `.venv\Scripts\python.exe -m pip install -r requirements.txt`

**Q: Streamlit crashes on large scripts**
A: Increase memory limit: `streamlit run ui_app.py --server.maxUploadSize=200`

**Q: Web app upload fails**
A: Check file size (<50MB) and format. Try converting to FDX or Fountain first.

**Q: CLI batch mode hangs**
A: Check for permission errors in output directory. Run with `--verbose` to diagnose.

---

## 🔧 Troubleshooting

### Common Issues

#### Issue: Python version mismatch
**Symptoms:** `SyntaxError` or `ModuleNotFoundError`
**Solution:**
```bash
python --version  # Must be 3.12+
# If wrong version:
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

#### Issue: Virtual environment not activated
**Symptoms:** Missing packages, wrong Python
**Solution:**
```bash
# Windows
.venv\Scripts\Activate.ps1

# Verify activation (prompt should show (.venv))
```

#### Issue: Streamlit uses global Python
**Symptoms:** `ModuleNotFoundError` despite pip install
**Solution:**
```bash
# Always use venv streamlit executable
.venv\Scripts\streamlit.exe run ui_app.py

# NOT: streamlit run ui_app.py
```

#### Issue: Scene extraction fails
**Symptoms:** `scene_count: 0` or empty scenes array
**Solution:**
1. Verify script format (open in text editor)
2. Check for non-standard scene headings
3. Try exporting from Final Draft as FDX (not PDF)
4. Update to latest fdx_loader.py (fixed Dec 13, 2025)

#### Issue: Budget values incorrect
**Symptoms:** Total budget $0 or negative
**Solution:**
1. Verify shoot_days > 0
2. Check that budget engines return valid rates
3. Run with `--verbose` to see calculation steps

#### Issue: Reports not generating
**Symptoms:** Empty output directory
**Solution:**
1. Check write permissions on output directory
2. Verify disk space (>100MB free)
3. Look for errors in console output
4. Check `export_engine.log` if exists

### Performance Optimization

#### Slow Analysis
**For large scripts (>100 scenes):**
1. Use CLI instead of Streamlit (faster)
2. Disable PDF export (slowest format)
3. Reduce Monte Carlo simulations: edit `monte_carlo_engine.py`, change `simulations=1000` to `500`

#### Memory Issues
**For scripts >200 pages:**
1. Close other applications
2. Increase Python heap: `set PYTHONMAXMEMORY=4G`
3. Process scenes in chunks (batch mode)

#### Disk Space
**Output files add up quickly:**
1. Enable auto-cleanup in `web_app.py` (7-day retention)
2. Compress old analyses: `tar -czf archive.tar.gz output/`
3. Use CSV instead of Excel (smaller files)

### Getting Help

**Priority 1: Check Documentation**
- PROJECT_OVERVIEW.md (architecture)
- API_CHANGES.md (recent updates)
- This guide (workflows)

**Priority 2: Run Tests**
```bash
python -m pytest tests/ -v
# If tests fail, file issue with output
```

**Priority 3: Enable Verbose Logging**
```bash
python -m src.cli analyze --input script.fdx --out ./output --verbose > debug.log 2>&1
# Share debug.log when reporting issues
```

**Priority 4: Check GitHub Issues**
- Search existing issues for similar problems
- Include: Python version, OS, script format, error message

---

## 📈 Advanced Workflows

### Integrating with CI/CD

**GitHub Actions Example:**
```yaml
name: Budget Analysis
on: [push]
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: python -m src.cli analyze --input scripts/ep1.fdx --out ./output
      - uses: actions/upload-artifact@v2
        with:
          name: budget-reports
          path: output/
```

### Automating Weekly Reports

**PowerShell Script (Windows):**
```powershell
# weekly_budget_report.ps1
$date = Get-Date -Format "yyyy-MM-dd"
$scripts = Get-ChildItem C:\Scripts\Current -Filter *.fdx

foreach ($script in $scripts) {
    python -m src.cli analyze --input $script.FullName --out "C:\Reports\$date\$($script.BaseName)"
}

# Email reports
$attachment = Get-ChildItem "C:\Reports\$date" -Recurse -Include *.pdf
Send-MailMessage -To "producer@studio.com" -Subject "Weekly Budget Report" -Attachments $attachment
```

### Custom Budget Templates

**Create template in Streamlit:**
1. Go to Phase 3 (Production Budget)
2. Adjust all rates for your market
3. Click "Save as Template"
4. Future analyses use saved rates

**Export template to JSON:**
```python
import json
template = {
    "crew": {"director": 1500, "dp": 1200, "ad": 900},
    "equipment": {"camera": 800, "lighting": 600}
}
with open('my_template.json', 'w') as f:
    json.dump(template, f)
```

**Load template in analysis:**
```python
from src.ProductionBudgetEngine import ProductionBudget
with open('my_template.json') as f:
    rates = json.load(f)
budget = ProductionBudget(shoot_days=5, custom_rates=rates)
```

---

## 🎓 Training Resources

### Video Tutorials (Coming Soon)
- [ ] Quick Start (10 min)
- [ ] CLI Deep Dive (20 min)
- [ ] Streamlit Power User (30 min)
- [ ] What-If Scenarios (15 min)

### Sample Projects
- `samples/test_script.fdx` - Simple 3-scene script
- `samples/episode1.fdx` - Sci-fi episode with effects
- `samples/test_script.fountain` - Indie drama

### Recommended Reading
- Final Draft formatting guide
- Fountain syntax specification
- Industry standard budget categories (PGA)

---

## 📞 Support

### Self-Service
1. **Search this guide** (Ctrl+F)
2. **Check FAQ section**
3. **Run pytest diagnostics**

### Community Support
- GitHub Discussions (coming soon)
- Stack Overflow tag: `enhanced-budget-pro`

### Professional Support
- Email: support@enhancedbudgetpro.com
- SLA: 24-hour response for critical bugs

---

**End of User Guide**  
*For architecture and development info, see PROJECT_OVERVIEW.md*
