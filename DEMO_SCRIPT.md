# PILOTFORGEAI Demo Script & Presentation Guide

Complete script for demonstrating PILOTFORGEAI to stakeholders, investors, or users.

## 5-Minute Quick Demo

### Setup (30 seconds)

**What You Need**:
- PILOTFORGEAI running: `streamlit run ui_app.py`
- Sample script ready: `samples/test_script.fdx`
- Browser at http://localhost:8501

**Opening Line**:
> "I'm going to show you how PILOTFORGEAI analyzes a screenplay and generates a complete production budget in under 10 seconds."

### Part 1: Upload & Analysis (2 minutes)

**Action**: Navigate to Page 1 (Story Intelligence)

**Script**:
> "Let's start with a sample script - a 3-scene indie thriller. I'll upload it here..."

**[Upload samples/test_script.fdx]**

> "Notice the real-time progress bar. PILOTFORGEAI is now:
> 1. Parsing the script structure
> 2. Running AI emotion detection on every line
> 3. Analyzing character arcs and scene density"

**[Point to progress indicators: 10% → 30% → 50% → 100%]**

> "And we're done - 1.5 seconds for complete analysis. Now let me show you what we got..."

### Part 2: Results Tour (2 minutes)

**Navigate: Page 1 Results**

> "Here's our story intelligence:
> - **3 scenes** detected
> - **3 characters**: Marcus, Elijah, and Detective Ramirez
> - AI analyzed **7 emotions** across all dialogue"

**[Scroll to character intelligence table]**

> "Each character gets metrics:
> - Marcus appears in 2 scenes, speaks 1 line
> - Elijah in 1 scene, 1 line  
> - Emotion analysis shows Marcus has 15% positive sentiment - this is a dark thriller"

**Navigate: Page 2 (Financial Intelligence)**

> "Now the business side. Based on this 3-scene script:
> - Estimated shoot days: 1-2 days
> - Production budget: ~$12,000-$25,000
> - This accounts for crew, equipment, and locations"

**Navigate: Page 15 (Character Arc Suite)**

> "For writers and directors - here's the character arc visualization. 
> You can see emotional journey, screen time estimates, and sentiment trends."

### Part 3: Export & Close (1 minute)

**Navigate: Page 12 (Export Center)**

> "Finally, one-click export to professional formats:
> - CSV for data analysis
> - Excel for budgets
> - PDF for presentations"

**[Click "Export All CSV"]**

> "And there you have it - from script upload to production-ready reports in under 10 seconds."

**Closing**:
> "PILOTFORGEAI works with Final Draft, Fountain, Celtx, even PDFs. 
> It scales from 3-scene shorts to 150-scene features.
> Questions?"

---

## 15-Minute Deep Dive

### Setup (1 minute)

Same as 5-minute demo, plus:
- Prepare `samples/scale_tests/test_script_100scenes.fdx`
- Have Excel open for budget review
- GPU info ready if applicable

### Part 1: The Problem (2 minutes)

**Script**:
> "Traditional script breakdown takes days or weeks:
> - Manually identify scenes, characters, props
> - Estimate shoot days by gut feel
> - Build budgets from scratch in Excel
> - Hope you didn't miss anything
>
> PILOTFORGEAI automates this entire process with AI.
> Let me show you..."

### Part 2: Small Script Demo (4 minutes)

Follow 5-minute demo script above.

### Part 3: Scale Demo (5 minutes)

**Upload: test_script_100scenes.fdx**

> "Now a real-world example - a 100-scene feature film.
> Same process, just bigger scale..."

**[Upload and click Analyze]**

> "Watch the AI work:
> - Parsing 100 scenes... 
> - Analyzing 800+ lines...
> - Running emotion detection on GPU..."

**[Show device info if GPU available]**

> "We're using GPU acceleration here - that's why this completes in 5 seconds instead of 50."

**[Results appear]**

> "Here's what we got:
> - **100 scenes** across 80 pages
> - **9 primary characters** 
> - **824 lines** of dialogue analyzed
> - **Complete emotional profile** for every character"

**Navigate through key pages**:

1. **Page 2 (Financial Intelligence)**:
   > "Production budget: $235,000 for a 20-day shoot
   > That's industry-standard for an indie feature."

2. **Page 4 (Monte Carlo Simulation)**:
   > "Risk analysis ran 10,000 scenarios.
   > 50th percentile: $235k
   > 95th percentile: $295k - plan for this number"

3. **Page 5 (Stripboard)**:
   > "Automatically generated shooting schedule
   > Organized by location to minimize moves"

### Part 4: Custom Budgets (2 minutes)

**Open**: `src/ProductionBudgetEngine/crew_budget_engine.py` in editor

> "All budget parameters are customizable.
> Say you're shooting in Atlanta instead of LA - 
> just update the crew rates:"

```python
"Director": {"rate": 900, "quantity": 1},  # Was $1200
"DP": {"rate": 650, "quantity": 1},        # Was $800
```

> "Save and re-analyze. Budget instantly updates to your market."

### Part 5: Q&A (2 minutes)

**Common Questions**:

Q: "What about VFX costs?"
A: "Baseline included in post-production. For heavy VFX, customize `post_budget_engine.py`."

Q: "Can this replace a line producer?"
A: "No - it's a tool FOR line producers. Handles the grunt work, they focus on creative decisions."

Q: "Does it work with TV series?"
A: "Absolutely. Batch process all episodes via CLI, aggregate the results."

---

## Pitch Deck Talking Points

### Slide 1: The Problem

**Title**: "Film Budgeting is Broken"

**Talking Points**:
- Traditional breakdown: 2-4 weeks
- Error-prone manual process
- Requires expensive line producers
- No data-driven insights
- Can't model "what-if" scenarios

**Visual**: Side-by-side comparison
- Old Way: Person with spreadsheet, stressed
- PILOTFORGEAI: Computer analyzing script, 5 seconds

### Slide 2: The Solution

**Title**: "AI-Powered Production Intelligence"

**Talking Points**:
- Upload script, get budget in seconds
- AI analyzes every scene, character, line
- Comprehensive risk analysis
- Professional reports (CSV, Excel, PDF)
- Scales from shorts to features

**Visual**: Dashboard screenshot with key metrics

### Slide 3: How It Works

**Title**: "Three-Stage Pipeline"

```
1. INGEST → Parse FDX/Fountain/PDF
2. ANALYZE → AI emotion detection + character intelligence
3. CALCULATE → Production budget + risk analysis
```

**Talking Points**:
- Multi-format support (FDX, Fountain, Celtx, PDF)
- HuggingFace AI models (7 emotions tracked)
- Industry-standard budget categories
- 10,000-run Monte Carlo simulation

### Slide 4: Performance

**Title**: "Built for Production Speed"

**Metrics**:
- 100-scene script: **5.68 seconds** (CPU)
- GPU acceleration: **3.2 seconds** (1.8x faster)
- Throughput: **147 lines/sec** (CPU), 2500+ (GPU)
- Scaling efficiency: **8.24x** (EXCELLENT)

**Talking Points**:
- Batch process entire script libraries
- GPU support for high-volume users
- Caches AI models for instant re-runs
- Production-ready performance

### Slide 5: Use Cases

**Title**: "Who Uses PILOTFORGEAI?"

**Personas**:

1. **Indie Producers**
   - Fast budget estimates for pitch decks
   - Risk analysis for insurance
   - Character breakdowns for casting

2. **Line Producers**
   - Automated script breakdown
   - Quick scenario modeling
   - Export to scheduling software

3. **Studios & Production Companies**
   - Batch analyze development slate
   - Compare project budgets
   - Data-driven greenlight decisions

4. **Film Schools & Students**
   - Learn industry-standard budgeting
   - Practice with real tools
   - Build professional portfolios

### Slide 6: Competitive Advantage

**Title**: "Why PILOTFORGEAI?"

| Feature | Movie Magic | EP Budgeting | PILOTFORGEAI |
|---------|-------------|--------------|--------------|
| AI Analysis | ❌ | ❌ | ✅ |
| Speed | Hours | Hours | Seconds |
| Multi-Format | Limited | Limited | FDX/Fountain/PDF |
| Emotion Tracking | ❌ | ❌ | ✅ 7 emotions |
| Monte Carlo | ❌ | ❌ | ✅ 10k runs |
| GPU Acceleration | ❌ | ❌ | ✅ 5-10x |
| Open Source | ❌ | ❌ | ✅ MIT |

### Slide 7: Roadmap

**Title**: "What's Next"

**Q1 2026**:
- Cloud deployment (SaaS)
- Collaboration features (teams)
- Mobile app (iOS/Android)

**Q2 2026**:
- Real-time editing integration
- Final Draft plugin
- Scheduling optimization AI

**Q3 2026**:
- SAG rate calculator
- Union compliance checker
- Multi-language support

### Slide 8: Call to Action

**Title**: "Get Started Today"

**Options**:
1. **Open Source**: Clone on GitHub
2. **Cloud Beta**: Request access
3. **Enterprise**: Contact for custom deployment

**Links**:
- GitHub: github.com/hneal055/EnhancedBudgetPro
- Docs: [Link to hosted docs]
- Demo: [Link to video]

---

## Video Tutorial Outline (YouTube/Vimeo)

### Video 1: "Install & First Analysis" (5 minutes)

**Chapters**:
1. 0:00 - Intro & overview
2. 0:30 - Installation (sped up)
3. 1:30 - Launch Streamlit
4. 2:00 - Upload sample script
5. 3:00 - Explore results
6. 4:30 - Export reports

**B-Roll Needed**:
- Terminal commands
- File upload
- Progress bars
- Results dashboard
- Export downloads

### Video 2: "Character Intelligence Deep Dive" (8 minutes)

**Chapters**:
1. 0:00 - What is character intelligence?
2. 1:00 - Metrics explained
3. 3:00 - Emotional arcs
4. 5:00 - Practical applications (casting)
5. 7:00 - Export & use cases

### Video 3: "Production Budget Customization" (10 minutes)

**Chapters**:
1. 0:00 - Default budgets explained
2. 2:00 - Finding budget engine files
3. 4:00 - Editing crew rates
4. 6:00 - Equipment packages
5. 8:00 - Regional adjustments
6. 9:00 - Save & re-analyze

### Video 4: "Risk Analysis & Monte Carlo" (7 minutes)

**Chapters**:
1. 0:00 - Why risk matters
2. 1:00 - Risk levels (HIGH/MED/LOW)
3. 3:00 - Monte Carlo explained
4. 5:00 - Interpreting confidence intervals
5. 6:00 - Insurance applications

### Video 5: "GPU Acceleration Setup" (6 minutes)

**Chapters**:
1. 0:00 - CPU vs GPU performance
2. 1:00 - Check CUDA availability
3. 2:00 - Install CUDA PyTorch
4. 3:30 - Test GPU detection
5. 4:30 - Benchmark comparison
6. 5:30 - Cloud deployment options

---

## Demo Day Checklist

### Before Demo

- [ ] System validated: `python validate_system.py`
- [ ] Streamlit launched: `streamlit run ui_app.py`
- [ ] Sample scripts ready in `samples/`
- [ ] Browser at http://localhost:8501
- [ ] GPU detection tested (if applicable)
- [ ] Export directory cleared
- [ ] Excel ready for budget review
- [ ] Backup: CLI demo if Streamlit fails
- [ ] Screen recording software running
- [ ] Notes printed/accessible

### During Demo

- [ ] Introduce problem (30 sec)
- [ ] Live upload & analysis (2 min)
- [ ] Tour key pages (3 min)
- [ ] Show export process (1 min)
- [ ] Answer questions (3-5 min)

### After Demo

- [ ] Share export files
- [ ] Send GitHub link
- [ ] Follow up on questions
- [ ] Collect feedback
- [ ] Schedule next steps

---

## Stakeholder-Specific Demos

### For Producers

**Focus On**:
- Speed (seconds vs days)
- Budget accuracy (±20%)
- Export to Excel (industry-standard)
- Risk analysis (insurance requirements)

**Key Pages**: 2, 3, 4, 12

### For Directors/Writers

**Focus On**:
- Character emotional arcs
- Scene density analysis
- Storytelling insights
- No budget jargon

**Key Pages**: 1, 14, 15, 16

### For Line Producers

**Focus On**:
- Customizable rates
- Stripboard generation
- Scenario modeling
- CLI batch processing

**Key Pages**: 3, 5, 7, 12 + CLI demo

### For Investors

**Focus On**:
- ROI potential (time savings)
- Market size (film industry)
- Competitive advantages
- Roadmap & vision

**Use**: Pitch deck format, not live demo

### For Film Schools

**Focus On**:
- Educational value
- Industry-standard tools
- Free & open source
- Real-world practice

**Key Pages**: All (comprehensive tour)

---

**Good luck with your demo!** 🎬🚀

**Version**: 1.0.0
**Last Updated**: December 2025
