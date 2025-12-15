# PILOTFORGEAI 🎬

**AI-Powered Film & TV Production Budget Intelligence**

Transform screenplays into actionable production intelligence in seconds.

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/hneal055/EnhancedBudgetPro)
[![Python](https://img.shields.io/badge/python-3.11+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-production%20ready-brightgreen.svg)]()

---

## ✨ What Is PILOTFORGEAI?

PILOTFORGEAI analyzes screenplays using AI to deliver:

- 📝 **Multi-Format Script Parsing**: FDX, Fountain, Celtx, PDF, TXT
- 🧠 **AI Emotion Detection**: 7 emotions tracked across every line
- 🎭 **Character Intelligence**: Arcs, screen time, sentiment analysis
- 💰 **Production Budgets**: Crew, equipment, locations, post
- ⚠️ **Risk Analysis**: Monte Carlo simulation with 10,000 scenarios
- 📊 **Professional Reports**: CSV, Excel, PDF exports

**Time to Analyze**: 3-6 seconds for a 100-scene script ⚡

---

## 🚀 Quick Start

### Install

```bash
# Clone repository
git clone https://github.com/hneal055/EnhancedBudgetPro.git
cd EnhancedBudgetPro

# Install dependencies
pip install -r requirements.txt

# Verify installation
python validate_system.py
```

### Run

```bash
# Streamlit UI (recommended)
streamlit run ui_app.py

# Command Line
python -m src.cli analyze --input samples/test_script.fdx --out ./output

# Flask Web App
python web_app.py
```

**Full Guide**: [QUICKSTART.md](QUICKSTART.md)

---

## 📖 Documentation

| Guide | Description |
|-------|-------------|
| [QUICKSTART.md](QUICKSTART.md) | Installation & first analysis (5 min) |
| [USER_GUIDE.md](USER_GUIDE.md) | Complete feature documentation |
| [DEMO_SCRIPT.md](DEMO_SCRIPT.md) | Presentation & demo materials |
| [GPU_ACCELERATION.md](GPU_ACCELERATION.md) | GPU setup (5-10x faster) |
| [PERFORMANCE_OPTIMIZATION_JOURNEY.md](PERFORMANCE_OPTIMIZATION_JOURNEY.md) | Optimization deep dive |

---

## 🎯 Key Features

### Multi-Format Script Support

| Format | Status | Notes |
|--------|--------|-------|
| Final Draft (.fdx) | ✅ | Industry standard |
| Fountain (.fountain) | ✅ | Open source format |
| Celtx (.celtx) | ✅ | JSON format |
| PDF (.pdf) | ✅ | Text extraction |
| Plain Text (.txt) | ✅ | Basic parsing |

### AI-Powered Analysis

- **Emotion Detection**: HuggingFace transformer model
- **7 Emotions**: Joy, sadness, anger, fear, surprise, disgust, neutral
- **Character Arcs**: Emotional journey visualization
- **Scene Density**: Action vs dialogue classification

### Production Budgets

- **Crew**: Director, DP, AD, grips, sound, etc.
- **Equipment**: Cameras, lighting, grip packages
- **Locations**: Permits, fees, rentals
- **Post-Production**: Editing, VFX, sound design
- **Contingency**: Industry-standard 12%

**Typical Budgets** (indie feature):
- 10-day shoot: ~$125,000
- 20-day shoot: ~$235,000
- 30-day shoot: ~$345,000

### Risk & Monte Carlo

- **Scene-Level Risk**: HIGH/MEDIUM/LOW ratings
- **Monte Carlo Simulation**: 10,000 scenario runs
- **Confidence Intervals**: 5% / 50% / 95% percentiles
- **Mitigation Plans**: Automated risk recommendations

---

## 💻 Performance

### Current (CPU)

| Script Size | Scenes | Time | Throughput |
|------------|--------|------|------------|
| Short | 10-25 | 1-2s | 68-127 l/s |
| Medium | 50 | 3-4s | 145 l/s |
| Feature | 100 | 5-6s | 147 l/s |

### With GPU (Expected)

| Script Size | CPU Time | GPU Time | Speedup |
|------------|----------|----------|---------|
| 50 scenes | 3.68s | 1.5s | 2.5x |
| 100 scenes | 5.68s | 3.2s | 1.8x |

**Scaling Efficiency**: 8.24x (🟢 EXCELLENT)

**See**: [PHASE_13_COMPLETE_SUMMARY.md](PHASE_13_COMPLETE_SUMMARY.md)

---

## 🖥️ System Requirements

**Minimum**:
- Python 3.11+
- 4GB RAM
- 2GB disk space

**Recommended**:
- Python 3.12+
- 8GB+ RAM
- 10GB disk space
- NVIDIA GPU with CUDA (5-10x faster)

**GPU**: AWS g4dn.xlarge (NVIDIA T4, $0.526/hour recommended)

---

## 📊 Architecture

```
┌──────────────────────────────────────────────────────────┐
│              PILOTFORGEAI Pipeline                       │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  1. IngestEngine     → Parse FDX/Fountain/PDF/Celtx    │
│  2. AnalysisEngine   → Character + Scene Intelligence   │
│  3. EmotionEngine    → AI Emotion Detection (GPU)       │
│  4. BudgetEngine     → Production Budget Calculation    │
│  5. RiskEngine       → Monte Carlo + Risk Analysis      │
│  6. ExportEngine     → CSV / Excel / PDF Reports        │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**Modules**:
- **IngestEngine**: Multi-format parsers (FDX, Fountain, Celtx, PDF)
- **AnalysisEngine**: Character intelligence, scene density
- **EmotionEngine**: HuggingFace transformers (GPU-accelerated)
- **ProductionBudgetEngine**: Crew, equipment, locations, post
- **ExportEngine**: CSV, Excel, PDF reporters

---

## 🎨 Streamlit UI Pages

1. **Story Intelligence**: Upload & analyze scripts
2. **Financial Intelligence**: Budget overview
3. **Production Budget**: Detailed line items
4. **Risk & Monte Carlo**: Risk analysis + simulation
5. **Stripboard Scheduler**: Visual shooting schedule
6. **Talent Availability**: Actor scheduling
7. **What-If Scenarios**: Budget scenario modeling
8. **AI Scenario Designer**: Automated optimization
12. **Export Center**: One-click report downloads
14. **Emotional Intelligence**: Deep emotion analysis
15. **Character Arc Suite**: Comprehensive character breakdowns
16. **Storytelling Insights**: Story structure analysis

**16 interactive pages** with visualizations, charts, and data tables.

---

## 🔧 Customization

### Edit Crew Rates

**File**: `src/ProductionBudgetEngine/crew_budget_engine.py`

```python
crew_rates = {
    "Director": {"rate": 1200, "quantity": 1},  # $1200/day
    "DP": {"rate": 800, "quantity": 1},         # $800/day
    "1st AD": {"rate": 600, "quantity": 1},     # $600/day
}
```

### Regional Rate Adjustments

| Market | Director | DP | 1st AD |
|--------|----------|-----|--------|
| LA (union) | $1500-$2500 | $1000-$1500 | $800-$1200 |
| NY (union) | $1400-$2200 | $900-$1400 | $750-$1100 |
| Atlanta | $800-$1500 | $600-$1000 | $500-$800 |
| Indie | $500-$1000 | $400-$800 | $350-$600 |

---

## 📤 Export Formats

### CSV
- Character intelligence
- Scene analysis
- Risk assessments
- Budget line items

### Excel
- Multi-tab workbook
- Summary, Crew, Equipment, Locations, Post, Insurance
- Formulas for real-time updates

### PDF
- Professional reports
- Stripboards
- Character breakdowns
- Executive summaries

---

## 🧪 Testing

```bash
# Validate system
python validate_system.py

# Performance benchmark
python test_gpu_acceleration.py

# Scale testing
python test_scale_performance.py

# Run CLI test
python -m src.cli analyze --input samples/test_script.fdx --out ./test_output
```

**Test Suite**: 11 comprehensive test scripts

---

## 🚢 Deployment

### Local

```bash
streamlit run ui_app.py
```

### Docker

```dockerfile
FROM python:3.12
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "ui_app.py"]
```

### Docker Compose (GPU)

```yaml
version: '3.8'
services:
  pilotforgeai:
    build: .
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
    ports:
      - "8501:8501"
```

### Cloud (AWS)

**Recommended**: g4dn.xlarge (NVIDIA T4, $0.526/hour)

```bash
# Install CUDA PyTorch
pip install torch --index-url https://download.pytorch.org/whl/cu118

# Run application
streamlit run ui_app.py --server.port 8501
```

**See**: [GPU_ACCELERATION.md](GPU_ACCELERATION.md) for complete deployment guide

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

**Areas for Contribution**:
- Additional script format parsers
- Budget engine customizations
- UI/UX improvements
- Documentation & tutorials
- Performance optimizations

---

## 📝 License

MIT License - See [LICENSE](LICENSE) for details

---

## 🙏 Acknowledgments

- **HuggingFace**: Emotion detection models
- **Streamlit**: Interactive UI framework
- **PyTorch**: GPU acceleration
- **ReportLab**: PDF generation
- **OpenPyXL**: Excel export

---

## 📧 Contact & Support

- **GitHub Issues**: [Report bugs](https://github.com/hneal055/EnhancedBudgetPro/issues)
- **Discussions**: [Ask questions](https://github.com/hneal055/EnhancedBudgetPro/discussions)
- **Documentation**: [Full guides](https://github.com/hneal055/EnhancedBudgetPro#documentation)

---

## 🗺️ Roadmap

### Q1 2026
- [ ] Cloud SaaS deployment
- [ ] Team collaboration features
- [ ] Mobile app (iOS/Android)

### Q2 2026
- [ ] Real-time Final Draft plugin
- [ ] Scheduling optimization AI
- [ ] Multi-language support

### Q3 2026
- [ ] SAG rate calculator
- [ ] Union compliance checker
- [ ] Advanced VFX budgeting

---

## 🏆 Status

**Version**: 1.0.0 (Phase 14: Polish & Ship)
**Status**: 🟢 Production Ready
**Performance**: 🟢 EXCELLENT (8.24x scaling efficiency)
**Test Coverage**: ✅ Comprehensive
**Documentation**: ✅ Complete

---

**Built with ❤️ for the film industry**

**Happy Filmmaking!** 🎬

---

<p align="center">
  <a href="QUICKSTART.md">Quick Start</a> •
  <a href="USER_GUIDE.md">User Guide</a> •
  <a href="DEMO_SCRIPT.md">Demo Materials</a> •
  <a href="GPU_ACCELERATION.md">GPU Setup</a>
</p>

<p align="center">
  <sub>⭐ Star us on GitHub if PILOTFORGEAI helps your production!</sub>
</p>
