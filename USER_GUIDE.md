# PILOTFORGEAI User Guide

Complete guide to using PILOTFORGEAI for film & TV production budget intelligence.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Script Analysis Workflow](#script-analysis-workflow)
3. [Understanding Results](#understanding-results)
4. [Streamlit Pages Guide](#streamlit-pages-guide)
5. [Budget Customization](#budget-customization)
6. [Export & Reporting](#export--reporting)
7. [Best Practices](#best-practices)
8. [FAQ](#faq)

---

## Getting Started

### First Time Setup

1. **Install PILOTFORGEAI**: See [QUICKSTART.md](QUICKSTART.md) for installation
2. **Launch Streamlit UI**: `streamlit run ui_app.py`
3. **Prepare Your Script**: FDX, Fountain, Celtx, PDF, or TXT format
4. **Upload & Analyze**: Follow the prompts on Page 1

### System Requirements

**Minimum**:
- Python 3.11+
- 4GB RAM
- 2GB disk space
- CPU: Any modern processor

**Recommended**:
- Python 3.12+
- 8GB+ RAM
- 10GB disk space (for model cache)
- GPU: NVIDIA T4 or better (5-10x faster)

---

## Script Analysis Workflow

### Step-by-Step Process

```
1. Upload Script
   ↓
2. Parse Structure
   ├─ Extract scenes
   ├─ Identify characters
   └─ Parse dialogue/action
   ↓
3. AI Analysis
   ├─ Emotion detection (7 emotions)
   ├─ Character intelligence
   └─ Scene density
   ↓
4. Financial Intelligence
   ├─ Production budget
   ├─ Risk analysis
   └─ Monte Carlo simulation
   ↓
5. Export Results
   └─ CSV, Excel, PDF
```

### Typical Analysis Times

| Script Size | Scenes | Characters | CPU Time | GPU Time |
|------------|--------|------------|----------|----------|
| Short | 10-25 | 3-5 | 1-2s | 0.5-1s |
| Medium | 50 | 5-10 | 3-4s | 1-2s |
| Feature | 100 | 10-20 | 5-6s | 3-4s |
| Epic | 150+ | 20+ | 8-10s | 4-5s |

---

## Understanding Results

### 1. Character Intelligence

**Metrics Explained**:

```python
{
    "scenes": 15,                    # Scenes character appears in
    "dialogue_lines": 42,            # Total spoken lines
    "estimated_screen_time_min": 18, # Estimated minutes on screen
    "scenes_with_dialogue": 12,      # Scenes with speaking lines
    "dominant_emotion": "joy",       # Most frequent emotion
    "sentiment_positive": 0.65,      # Positive emotion score (0-1)
    "sentiment_negative": 0.25,      # Negative emotion score (0-1)
    "sentiment_neutral": 0.10        # Neutral emotion score (0-1)
}
```

**Interpretation**:
- **High dialogue_lines**: Major character (protagonist/antagonist)
- **Low scenes_with_dialogue**: Background/minor role
- **High sentiment_positive**: Optimistic/heroic character
- **High sentiment_negative**: Troubled/villainous character

**Example - Hero Character**:
```
Marcus: 45 scenes, 120 lines, 35 min screen time
├─ Dominant emotion: determination (joy + anger mix)
├─ Positive: 0.55 (moderate optimism)
├─ Negative: 0.35 (faces challenges)
└─ Arc: Starts neutral (0.5) → Ends positive (0.75)
```

**Example - Supporting Character**:
```
Sarah: 12 scenes, 28 lines, 8 min screen time
├─ Dominant emotion: neutral (supportive role)
├─ Positive: 0.70 (encouraging friend)
├─ Negative: 0.15 (minimal conflict)
└─ Arc: Stable positive throughout
```

### 2. Scene Density Analysis

**Density Types**:

- **DIALOGUE-HEAVY** (>70% dialogue):
  - Examples: Interrogation, confession, romantic conversation
  - Budget Impact: Lower (studio/interior common)
  - Shoot Time: 1-2 pages/day

- **ACTION-HEAVY** (>70% action):
  - Examples: Chase, fight, explosion
  - Budget Impact: Higher (VFX, stunts, safety)
  - Shoot Time: 1/4 to 1/2 page/day

- **BALANCED** (30-70% each):
  - Examples: Normal scenes with action + dialogue
  - Budget Impact: Moderate
  - Shoot Time: 3-5 pages/day

**Budget Rule of Thumb**:
- 1 DIALOGUE scene ≈ $5,000-$10,000
- 1 BALANCED scene ≈ $10,000-$25,000
- 1 ACTION scene ≈ $25,000-$100,000+

### 3. Production Budget

**Budget Breakdown** (typical indie feature, 20-day shoot):

```
Above-the-Line (30-40%): $70,000-$95,000
├─ Director: $15,000
├─ Producers: $20,000
├─ Writers: $10,000
└─ Lead Cast: $25,000-$50,000

Below-the-Line (50-60%): $120,000-$145,000
├─ Crew: $60,000
├─ Equipment: $30,000
├─ Locations: $20,000
└─ Post-Production: $10,000

Contingency (12%): $25,000

TOTAL: $215,000-$265,000
```

**Scaling by Shoot Days**:
- 10 days: ~$125,000
- 20 days: ~$235,000
- 30 days: ~$345,000
- 40 days: ~$455,000

### 4. Risk Analysis

**Risk Levels**:

**HIGH RISK** (20-30% of scenes):
- Weather-dependent exteriors
- Complex VFX/stunts
- Large crowds
- Water/fire effects
- Animals/children
- **Mitigation**: Add 20-30% contingency, backup plans

**MEDIUM RISK** (40-50% of scenes):
- Multiple locations
- Night shoots
- Period/costume complexity
- **Mitigation**: Add 10-15% contingency

**LOW RISK** (30-40% of scenes):
- Studio interiors
- Small cast
- Dialogue-heavy
- **Mitigation**: Standard 5-10% contingency

**Example Risk Report**:
```
Scene 15: EXT. HIGHWAY CHASE - DAY
├─ Risk Level: HIGH
├─ Factors:
│   ├─ Moving vehicles (safety)
│   ├─ Traffic control (permits)
│   ├─ Weather dependency
│   └─ VFX requirements (cleanup)
├─ Contingency: +25%
└─ Mitigation:
    ├─ Hire stunt coordinator
    ├─ Obtain road closure permits
    ├─ Schedule backup date
    └─ Pre-vis for VFX planning
```

### 5. Monte Carlo Simulation

**What It Does**:
Runs 10,000 scenarios with random variations in:
- Shoot days (+/- 20%)
- Crew costs (+/- 15%)
- Equipment costs (+/- 10%)
- Location costs (+/- 25%)

**Interpreting Results**:

```
Budget Confidence Intervals:
├─ 5% Percentile: $185,000  (best case - lucky)
├─ 50% Percentile: $235,000 (most likely)
└─ 95% Percentile: $295,000 (worst case - plan for this)
```

**Decision Making**:
- **Greenlight budget**: Use 50th percentile
- **Fundraising target**: Use 75th-90th percentile
- **Investor presentation**: Show range (5th-95th)

---

## Streamlit Pages Guide

### Page 0: Command Center
- **Purpose**: Quick overview dashboard
- **Use When**: First login, daily check-ins
- **Key Metrics**: Scene count, character count, budget summary

### Page 1: Story Intelligence
- **Purpose**: Upload and analyze scripts
- **Use When**: Starting new project
- **Features**:
  - File upload (FDX, Fountain, PDF, etc.)
  - Real-time progress tracking
  - Device info (CPU/GPU)
  - Timing metrics

**Pro Tip**: Use Streamlit UI for first analysis (caches model), then CLI for batch processing.

### Page 2: Financial Intelligence
- **Purpose**: Budget overview and breakdown
- **Use When**: Preparing pitch decks, investor meetings
- **Features**:
  - Total budget calculation
  - Category breakdowns
  - Cost per scene
  - Shoot day estimates

### Page 3: Production Budget
- **Purpose**: Detailed line-item budget
- **Use When**: Pre-production planning
- **Features**:
  - Crew rates (customizable)
  - Equipment packages
  - Location costs
  - Post-production breakdown

**Pro Tip**: Export to Excel, customize rates, re-import for final budget.

### Page 4: Risk & Monte Carlo
- **Purpose**: Risk assessment and simulation
- **Use When**: Risk management planning, insurance quotes
- **Features**:
  - Scene-level risk ratings
  - Monte Carlo simulation (10,000 runs)
  - Confidence intervals
  - Contingency recommendations

### Page 5-11: Scheduling & Optimization
- **Stripboard Scheduler**: Visual shooting schedule
- **Talent Availability**: Actor scheduling conflicts
- **What-If Scenarios**: Budget scenario modeling
- **AI Scenario Designer**: Automated schedule optimization

### Page 12: Export Center
- **Purpose**: One-click report generation
- **Use When**: Delivering to stakeholders
- **Formats**:
  - CSV (data analysis)
  - Excel (budgets)
  - PDF (presentations)

**Export Checklist**:
- [ ] Character intelligence CSV
- [ ] Scene analysis CSV
- [ ] Risk analysis CSV
- [ ] Production budget Excel
- [ ] Stripboard PDF
- [ ] Executive summary PDF

### Page 14: Emotional Intelligence
- **Purpose**: Deep emotion analysis
- **Use When**: Character development, story notes
- **Features**:
  - Scene-by-scene emotion flow
  - Character emotional arcs
  - Sentiment trends
  - Emotion heatmaps

### Page 15: Character Arc Suite
- **Purpose**: Comprehensive character analysis
- **Use When**: Character breakdowns, casting
- **Features**:
  - Screen time estimates
  - Dialogue analysis
  - Emotional journey visualization
  - Character relationship mapping

**Pro Tip**: Use for casting discussions and actor breakdowns.

### Page 16: Storytelling Insights
- **Purpose**: Story structure analysis
- **Use When**: Script notes, rewrites
- **Features**:
  - Three-act structure detection
  - Pacing analysis
  - Emotional beats
  - Dramatic tension curves

---

## Budget Customization

### Editing Crew Rates

**File**: `src/ProductionBudgetEngine/crew_budget_engine.py`

```python
def calculate(self, shoot_days=20):
    crew_rates = {
        # Format: "Role": {"rate": daily_rate, "quantity": num_needed}
        
        # Update these rates for your market
        "Director": {"rate": 1200, "quantity": 1},        # $1200/day
        "1st AD": {"rate": 600, "quantity": 1},           # $600/day
        "DP": {"rate": 800, "quantity": 1},               # $800/day
        
        # Add custom roles
        "VFX Supervisor": {"rate": 900, "quantity": 1},
        "Drone Operator": {"rate": 500, "quantity": 0.5}, # Half-time
    }
```

**Regional Rates**:

| Market | Director | DP | 1st AD | PA |
|--------|----------|-----|--------|-----|
| LA (union) | $1500-$2500 | $1000-$1500 | $800-$1200 | $200-$300 |
| NY (union) | $1400-$2200 | $900-$1400 | $750-$1100 | $180-$280 |
| Atlanta | $800-$1500 | $600-$1000 | $500-$800 | $150-$200 |
| Indie/Non-union | $500-$1000 | $400-$800 | $350-$600 | $100-$150 |

### Editing Equipment Costs

**File**: `src/ProductionBudgetEngine/equipment_budget_engine.py`

```python
equipment_packages = {
    # Camera Packages
    "ARRI Alexa Mini Package": {"rate": 1500, "quantity": shoot_days},
    "RED Komodo Package": {"rate": 800, "quantity": shoot_days},
    "Sony FX6 Package": {"rate": 500, "quantity": shoot_days},
    
    # Add your gear
    "DJI Ronin 2 Gimbal": {"rate": 200, "quantity": shoot_days * 0.3},
    "Teradek Bolt Wireless Video": {"rate": 150, "quantity": shoot_days},
}
```

### Custom Location Fees

**File**: `src/ProductionBudgetEngine/location_budget_engine.py`

```python
location_costs = {
    "Location Scout (per day)": {"rate": 500, "quantity": 5},
    "Permit Fees": {"rate": 300, "quantity": num_locations},
    "Location Rental (per day)": {"rate": 1500, "quantity": exterior_days},
    
    # Add specific locations
    "Warehouse Rental": {"rate": 2000, "quantity": 3},  # 3 days
    "Restaurant After-Hours": {"rate": 1000, "quantity": 2},
}
```

---

## Export & Reporting

### CSV Exports

**Use Cases**:
- Data analysis in Excel/Python
- Import into scheduling software
- Custom reporting templates

**Files Generated**:
```
output/
├─ character_intelligence.csv (character metrics)
├─ scene_analysis.csv (scene-by-scene data)
├─ risk_analysis.csv (risk assessments)
└─ budget_summary.csv (budget line items)
```

### Excel Workbooks

**Use Cases**:
- Client presentations
- Budget approvals
- Financial tracking

**Tabs Included**:
```
production_budget.xlsx
├─ Summary (total budget)
├─ Crew (detailed crew breakdown)
├─ Equipment (rental costs)
├─ Locations (permits & fees)
├─ Post (editing, VFX, sound)
└─ Insurance (contingency & liability)
```

**Pro Tip**: Share Excel with line producers for real-time budget tracking.

### PDF Reports

**Use Cases**:
- Pitch decks
- Investor presentations
- Insurance applications

**Reports Generated**:
```
output/
├─ stripboard.pdf (visual shooting schedule)
├─ character_breakdown.pdf (actor casting info)
├─ budget_summary.pdf (executive overview)
└─ risk_assessment.pdf (contingency planning)
```

---

## Best Practices

### Script Preparation

**Do**:
- ✅ Use proper scene headings (INT/EXT, Location, Time)
- ✅ Consistent character names (MARCUS not Marcus/MARC)
- ✅ Clear scene numbers
- ✅ Standard formatting (1 page ≈ 1 minute screen time)

**Avoid**:
- ❌ Missing scene headings
- ❌ Inconsistent character names
- ❌ Heavy formatting (all caps action, colored text)
- ❌ Non-standard sluglines

### Budget Planning

**Golden Rules**:
1. **Always add contingency** (minimum 10%, preferably 15-20%)
2. **Use 75th percentile** from Monte Carlo for fundraising
3. **Update crew rates** for your local market
4. **Include prep and wrap days** (typically +20% shoot days)
5. **Account for payroll taxes** (~25% on top of wages)

**Common Mistakes**:
- Forgetting location permits
- Underestimating post-production time
- Not budgeting for reshoots
- Skipping insurance (required for most productions)

### Performance Optimization

**For Faster Analysis**:
1. **Use Streamlit UI first** (caches model)
2. **Enable GPU if available** (5-10x faster)
3. **Close other applications** (free RAM)
4. **Batch process overnight** (large script libraries)

**For Large Projects** (200+ scenes):
- Increase batch size: Edit `detector.py`, set `batch_size=64`
- Use GPU with 8GB+ VRAM
- Split into acts/episodes for parallel processing

---

## FAQ

### General

**Q: What script formats are supported?**
A: Final Draft (.fdx), Fountain (.fountain), Celtx (.celtx), PDF (.pdf), plain text (.txt)

**Q: How accurate are the budgets?**
A: ±20% for indie features. Always customize crew rates for your market and add contingency.

**Q: Can I use this for TV series?**
A: Yes! Analyze each episode separately, then aggregate. Use batch processing CLI.

### Technical

**Q: Why is first analysis slow?**
A: AI model loading (~1.3s). Use Streamlit UI to cache model across analyses.

**Q: GPU vs CPU - which should I use?**
A: GPU is 5-10x faster but requires NVIDIA card + CUDA. CPU works fine for <50 scenes.

**Q: Can I run this on a server?**
A: Yes! Deploy Flask web app or Streamlit with Docker. See [GPU_ACCELERATION.md](GPU_ACCELERATION.md) for cloud deployment.

### Budgeting

**Q: Why is my budget so high/low?**
A: Check crew rates in `ProductionBudgetEngine/*.py`. Default rates are LA union scale.

**Q: How do I account for SAG rates?**
A: Edit `crew_budget_engine.py`, add SAG categories with day rates + fringes (~25%).

**Q: What about post-production?**
A: Default is $10k baseline. Customize in `post_budget_engine.py` for your VFX/sound needs.

### Troubleshooting

**Q: "No scenes detected" error?**
A: Check scene headings (must start with INT/EXT). Try converting to Fountain format.

**Q: Character names inconsistent?**
A: Ensure consistent ALL CAPS for character names throughout script.

**Q: Export files missing?**
A: Check output directory permissions. Use `--out` flag to specify writable location.

---

## Next Steps

1. **Complete Tutorial**: Work through [QUICKSTART.md](QUICKSTART.md)
2. **Analyze Sample Scripts**: Try `samples/test_script.fdx`
3. **Customize Budgets**: Edit engine files for your market
4. **Deploy Production**: See deployment guides
5. **Join Community**: Share feedback on GitHub Discussions

**Need Help?**
- Documentation: [README.md](README.md)
- Issues: [GitHub Issues](https://github.com/hneal055/EnhancedBudgetPro/issues)
- Performance: [PERFORMANCE_OPTIMIZATION_JOURNEY.md](PERFORMANCE_OPTIMIZATION_JOURNEY.md)

---

**Happy Budgeting!** 🎬💰

**Version**: 1.0.0
**Last Updated**: December 2025
**License**: MIT
