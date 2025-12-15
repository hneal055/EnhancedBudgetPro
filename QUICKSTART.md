# PILOTFORGEAI Quick Start Guide

Welcome to **PILOTFORGEAI** - The ultimate film & TV production budget intelligence system.

## What Is PILOTFORGEAI?

PILOTFORGEAI transforms your screenplay into actionable production intelligence:

- 📝 **Script Analysis**: Parse FDX, Fountain, Celtx, PDF, and plain text
- 🧠 **AI-Powered Intelligence**: Character arcs, emotion tracking, scene density
- 💰 **Budget Calculation**: Comprehensive production budgets with crew, equipment, locations
- ⚠️ **Risk Analysis**: Monte Carlo simulations and contingency planning
- 📊 **Export Everything**: CSV, Excel, and professional PDF reports

**Time to Analyze**: 3-6 seconds for a 100-scene script ⚡

---

## Installation

### Prerequisites

- Python 3.11 or higher
- 4GB+ RAM
- (Optional) NVIDIA GPU for 5-10x faster analysis

### Step 1: Clone Repository

```bash
git clone https://github.com/hneal055/EnhancedBudgetPro.git
cd EnhancedBudgetPro
```

### Step 2: Install Dependencies

```bash
# Create virtual environment
python -m venv .venv

# Activate (Linux/Mac)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### Step 3: Verify Installation

```bash
python validate_system.py
```

You should see: **✅ SYSTEM READY FOR DEPLOYMENT**

---

## Three Ways to Use PILOTFORGEAI

### 1. Streamlit UI (Recommended) 🎨

**Best for**: Interactive analysis, visual dashboards, exploring insights

```bash
streamlit run ui_app.py
```

**Opens**: http://localhost:8501

**Features**:
- 16 interactive pages
- Real-time progress bars
- Beautiful visualizations
- Export center with one-click downloads

### 2. Command Line (CLI) ⚡

**Best for**: Automation, batch processing, CI/CD pipelines

```bash
# Analyze single script
python -m src.cli analyze --input samples/test_script.fdx --out ./output

# Batch process multiple scripts
python -m src.cli batch --input_dir ./scripts --out ./batch_results
```

**Output**: CSV, Excel, and PDF reports in specified directory

### 3. Flask Web App 🌐

**Best for**: Team collaboration, web deployment, REST API

```bash
python web_app.py
```

**Opens**: http://localhost:5000

**Features**:
- Upload scripts via web interface
- Job-based processing (unique IDs)
- Download reports via links
- REST API endpoints

---

## Your First Analysis (60 seconds)

### Using Streamlit UI

1. **Start Streamlit**:
   ```bash
   streamlit run ui_app.py
   ```

2. **Navigate to "Story Intelligence" page** (Page 1)

3. **Upload a script**:
   - Click "Upload Script File"
   - Select `samples/test_script.fdx`
   - Or paste script text directly

4. **Click "Analyze Script"**:
   - Watch progress bar (10% → 100%)
   - See device info (CPU or GPU)
   - View timing metrics

5. **Explore Results**:
   - 📊 3 scenes detected
   - 🎭 3 characters (Marcus, Elijah, Ramirez)
   - 😊 Emotion analysis complete
   - ⏱️ Total time: ~1-2 seconds

6. **Navigate Other Pages**:
   - **Character Arc Suite** (Page 15): Deep character analysis
   - **Financial Intelligence** (Page 2): Budget overview
   - **Export Center** (Page 12): Download all reports

### Using CLI

```bash
# Quick analysis
python -m src.cli analyze \
  --input samples/test_script.fdx \
  --out ./my_first_analysis

# Check output
ls -lh my_first_analysis/
```

**Output Files**:
- `character_intelligence.csv` - Character metrics
- `scene_analysis.csv` - Scene-by-scene breakdown
- `risk_analysis.csv` - Production risks
- `production_budget.xlsx` - Complete budget spreadsheet
- `stripboard.pdf` - Visual stripboard

---

## Understanding the Output

### Character Intelligence

```csv
character,scenes,dialogue_lines,estimated_screen_time_min,sentiment_positive,...
MARCUS,2,1,5.0,0.15,...
ELIJAH,1,1,3.0,0.02,...
RAMIREZ,1,1,3.0,0.08,...
```

**Key Metrics**:
- **scenes**: Number of scenes character appears in
- **dialogue_lines**: Total spoken lines
- **estimated_screen_time_min**: Screen time estimate
- **sentiment_positive**: Positive emotion score (0-1)

### Scene Analysis

```csv
scene_number,heading,int_ext,location,time_of_day,dialogue_lines,action_lines,...
1,INT. APARTMENT - NIGHT,INT,APARTMENT,NIGHT,1,1,...
2,EXT. CHICAGO STREET - DAWN,EXT,CHICAGO STREET,DAWN,1,1,...
```

### Production Budget

Excel spreadsheet with tabs:
- **Summary**: Total budget breakdown
- **Crew**: Director, DP, AD, etc. with daily rates
- **Equipment**: Cameras, lighting, grip packages
- **Locations**: Scout costs, permits, fees
- **Post**: Editing, VFX, sound design
- **Insurance**: 12% contingency + liability

**Typical Budget** (indie feature):
- 10-day shoot: ~$125,000
- 20-day shoot: ~$235,000
- 30-day shoot: ~$345,000

---

## Key Features

### 1. Multi-Format Script Support

| Format | Extension | Notes |
|--------|-----------|-------|
| Final Draft | `.fdx` | ✅ Fully supported |
| Fountain | `.fountain` | ✅ Fully supported |
| Celtx | `.celtx` | ✅ JSON format |
| PDF | `.pdf` | ✅ Text extraction |
| Plain Text | `.txt` | ✅ Basic parsing |

### 2. AI Emotion Detection

**Model**: `j-hartmann/emotion-english-distilroberta-base`

**7 Emotions Tracked**:
- 😊 Joy
- 😢 Sadness
- 😠 Anger
- 😨 Fear
- 😲 Surprise
- 🤢 Disgust
- 😐 Neutral

**Performance**: 147-296 lines/sec (CPU), 2500+ lines/sec (GPU)

### 3. Production Budget Categories

**Above-the-Line** (creative team):
- Director, Producers, Writers, Lead Cast

**Below-the-Line** (production):
- Crew (DP, AD, Gaffer, Sound, etc.)
- Equipment (cameras, lighting, grip)
- Locations (permits, fees, rentals)
- Post-Production (editing, VFX, sound)

**Contingency**:
- 12% of total budget
- Covers unexpected costs
- Industry standard

### 4. Risk Analysis

**Monte Carlo Simulation**:
- Runs 10,000 scenarios
- 5% / 50% / 95% confidence intervals
- Identifies high-risk scenes

**Risk Categories**:
- **HIGH**: Complex VFX, stunts, weather-dependent
- **MEDIUM**: Multiple locations, large cast
- **LOW**: Studio interiors, small cast

### 5. Export Options

**CSV**: Character intelligence, scene analysis, risk data
**Excel**: Complete production budget (multi-tab)
**PDF**: Professional reports with charts and stripboards

---

## Advanced Usage

### GPU Acceleration (5-10x Faster)

If you have an NVIDIA GPU with CUDA:

```bash
# Install CUDA PyTorch
pip install torch --index-url https://download.pytorch.org/whl/cu118

# Run analysis (auto-detects GPU)
streamlit run ui_app.py
```

**Expected Performance**:
- 100-scene script: 5.68s → **3.2s** (1.8x faster)
- Emotion detection: 2.78s → **0.28s** (10x faster)

**Recommended GPU**: AWS g4dn.xlarge (NVIDIA T4, $0.526/hour)

### Batch Processing

Process multiple scripts at once:

```bash
# Create input directory
mkdir scripts/
cp script1.fdx script2.fountain script3.pdf scripts/

# Batch process
python -m src.cli batch --input_dir ./scripts --out ./batch_output

# Results in batch_output/ with timestamped subfolders
ls -lh batch_output/
```

### Custom Budget Parameters

Edit `src/ProductionBudgetEngine/*_budget_engine.py` to customize:
- Crew daily rates
- Equipment rental costs
- Location fees
- Post-production rates

Example:
```python
# src/ProductionBudgetEngine/crew_budget_engine.py
"Director": {"rate": 1200, "quantity": 1},  # $1200/day
"DP": {"rate": 800, "quantity": 1},         # $800/day
```

---

## Troubleshooting

### Issue: "No module named 'transformers'"

**Solution**:
```bash
pip install -r requirements.txt
```

### Issue: Slow emotion detection

**Symptoms**: >10 seconds for small scripts

**Solutions**:
1. Use Streamlit UI (caches model after first load)
2. Enable GPU acceleration
3. Reduce batch size if memory constrained

### Issue: "CUDA out of memory" (GPU)

**Solution**:
```python
# Edit src/EmotionEngine/detector.py
batch_size = 16  # Reduce from 32
```

### Issue: Script not parsing correctly

**Check**:
1. File format matches extension (.fdx for Final Draft)
2. Script has proper scene headings (INT/EXT)
3. Try different format (convert to Fountain)

**Debug**:
```bash
python -m src.cli analyze --input your_script.fdx --out ./debug
# Check debug/parsing_log.txt
```

---

## Getting Help

**Documentation**:
- [Full Architecture Guide](README.md)
- [GPU Acceleration Guide](GPU_ACCELERATION.md)
- [Performance Optimization](PERFORMANCE_OPTIMIZATION_JOURNEY.md)

**Issues**:
- GitHub Issues: https://github.com/hneal055/EnhancedBudgetPro/issues
- Check existing issues before opening new ones

**Community**:
- Discussions: https://github.com/hneal055/EnhancedBudgetPro/discussions
- Share your projects and feedback!

---

## What's Next?

Now that you've completed your first analysis:

1. **Explore All Pages**: 16 Streamlit pages with different insights
2. **Try Your Own Scripts**: Upload your screenplay
3. **Customize Budgets**: Edit engine files for your production needs
4. **Deploy with GPU**: 5-10x faster analysis on cloud GPU instances
5. **Batch Process**: Analyze entire script libraries

**Happy Filmmaking!** 🎬

---

**Version**: 1.0.0 (Phase 14: Polish & Ship)
**Last Updated**: December 2025
**License**: MIT
**Author**: PILOTFORGEAI Team
