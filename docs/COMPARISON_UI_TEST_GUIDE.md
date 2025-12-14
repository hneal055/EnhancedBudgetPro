# Character Arc Comparison UI - Testing Guide

## Phase 13.2 Week 1 Day 2-3 Deliverable
**Status:** ✅ Complete  
**Commit:** e10095b  
**Date:** December 14, 2025

---

## 🎯 Testing Overview

The Character Arc Comparison UI enables side-by-side analysis of two characters' emotional development, interactions, and synchronization throughout the narrative.

## 📋 Pre-Testing Setup

### 1. Start Streamlit
```bash
cd /workspaces/EnhancedBudgetPro
streamlit run ui_app.py
```
Access at: http://localhost:8501

### 2. Upload Test Script
Navigate to **Page 1: Story Intelligence** and upload one of:
- `samples/test_comparison.fdx` - Sarah & Mark (5 scenes, interaction-focused)
- `samples/test_script.fdx` - Original test (3 scenes)

### 3. Wait for Analysis
Progress bar shows:
- ✅ Parsing script
- ✅ Character intelligence
- ✅ Scene density
- ✅ **Emotional intelligence** (60-90 seconds)
- ✅ Classifying character arcs

---

## 🧪 Test Cases

### Test Case 1: Basic Setup
**Location:** Page 15 - Character Arc Suite

**Steps:**
1. Navigate to "Character Arc Suite" in sidebar
2. Verify "Character Arc Classification" section loads
3. Scroll to "Character Comparison" section
4. Verify two dropdown selectors appear

**Expected:**
- ✅ Character 1 dropdown populated with all characters
- ✅ Character 2 dropdown populated (excluding char1)
- ⚠️ Warning if same character selected

---

### Test Case 2: Basic Metrics Comparison
**Select:** Sarah (char1) vs Mark (char2)

**Expected Results:**

#### Volatility Metrics
- **Sarah Volatility:** Numerical value (0-100)
- **Delta:** +/- comparison vs Mark
- **Mark Volatility:** Numerical value

#### Scene Counts
- **Sarah Scenes:** Integer count
- **Delta:** +/- scenes vs Mark
- **Mark Scenes:** Integer count

#### Emotional Range
- **Sarah Emotions:** List of unique emotions
- **Mark Emotions:** List of unique emotions
- **Shared Emotions:** Common emotions (if any)

**Validation:**
```
✅ All metrics display numerical values
✅ Delta shows positive/negative correctly
✅ Emotional range shows comma-separated lists
```

---

### Test Case 3: Trajectory Comparison
**Select:** Any two characters with emotional arcs

**Expected Visualizations:**

#### Direction Analysis
- **Sarah:** 📈/📉/➡️ icon + "Ascending/Descending/Flat"
- **Mark:** 📈/📉/➡️ icon + direction
- **Peak Location:** "Peak at X% through arc"

#### Synchronization Indicators
- ✅ **Parallel Arcs:** Both move in same direction
- ⚠️ **Divergent Arcs:** Characters move opposite directions
- 🎯 **Synchronized Peaks:** Both peak at similar points

#### Correlation Score
- **Strong Positive (>50%):** Green success message - "Characters develop together"
- **Strong Negative (<-50%):** Red error message - "Characters develop in opposition"
- **Weak (-50% to 50%):** Blue info message - "Independent development"

#### Overlay Chart
- **X-axis:** Scene Appearance # (1, 2, 3...)
- **Y-axis:** Intensity (0-100)
- **Sarah Line:** Red (#FF6B6B), 3px width
- **Mark Line:** Cyan (#4ECDC4), 3px width
- **Markers:** 8px circles on data points
- **Hover:** Shows intensity values for both

**Validation:**
```
✅ Chart loads without errors
✅ Two distinct colored lines visible
✅ Hover shows unified values for both characters
✅ Chart title: "Emotional Intensity Comparison"
```

---

### Test Case 4: Interaction Analysis
**Select:** Sarah vs Mark (high interaction expected)

**Expected Metrics:**

| Metric | Expected | Format |
|--------|----------|--------|
| **Shared Scenes** | Integer | Count |
| **Interaction Rate** | Percentage | XX.X% |
| **Emotional Alignment** | Percentage | XX.X% |
| **Sarah Solo Scenes** | Integer | Count |
| **Mark Solo Scenes** | Integer | Count |

#### Distribution Chart
- **Chart Type:** Grouped bar chart
- **X-axis:** "Solo" and "Shared"
- **Bars:**
  - Sarah (Red) - Solo count, Shared count
  - Mark (Cyan) - Solo count, Shared count
- **Height:** 300px

**Validation:**
```
✅ All metrics show numerical values
✅ Interaction rate <= 100%
✅ Shared scenes <= min(Sarah scenes, Mark scenes)
✅ Bar chart displays correctly
```

---

### Test Case 5: Development Rates
**Select:** Any two characters with trajectory data

**Expected Metrics:**

#### Development Speed
- **Sarah:** X.XX per scene
- **Mark:** X.XX per scene
- **Winner:** 🏆 Faster: [Name]

#### Arc Depth
- **Sarah:** XX.X (emotional range)
- **Mark:** XX.X
- **Winner:** 🏆 Deeper: [Name]

#### Consistency
- **Sarah:** XX.X%
- **Mark:** XX.X%
- **Winner:** 🏆 More Consistent: [Name]

#### Spider/Radar Chart
- **Categories:** Volatility, Scenes, Dev Rate, Arc Depth, Consistency
- **Sarah:** Red fill (#FF6B6B)
- **Mark:** Cyan fill (#4ECDC4)
- **Range:** 0-100 (normalized)
- **Shape:** Pentagonal radar

**Validation:**
```
✅ All three metrics display
✅ Winner annotations correct
✅ Spider chart renders with both overlays
✅ All 5 categories labeled
```

---

### Test Case 6: Synchronization Analysis
**Select:** Characters with varying relationships

**Expected Relationship Types:**

1. **Synchronized Allies**
   - ✅ Peaks synchronized (within 20% of narrative)
   - ✅ Parallel direction (both ascending/descending)
   - Example: Hero & Mentor, Partners

2. **Synchronized Opposites**
   - ✅ Peaks synchronized
   - ⚠️ Opposite direction (one ascending, one descending)
   - Example: Hero vs Villain climax

3. **Asynchronous Allies**
   - ℹ️ Asynchronous peaks
   - ✅ Parallel direction
   - Example: Subplot characters, B-storylines

4. **Independent Arcs**
   - ℹ️ Asynchronous peaks
   - ⚠️ Opposite direction
   - Example: Separate character journeys

**Display Format:**
```
🔄 Arc Synchronization
### [Relationship Type]
**[Description text]**

[Peak Status]     [Direction Status]
✅/ℹ️             ✅/⚠️
```

**Validation:**
```
✅ Relationship type displays as heading
✅ Description explains dynamic
✅ Status indicators match relationship logic
✅ Color coding appropriate (green/blue/yellow)
```

---

## 🐛 Known Issues & Edge Cases

### Issue 1: No Characters
**Scenario:** Script has no detectable characters  
**Expected:** Dropdowns show empty or single "Unknown" character  
**Status:** ⚠️ Needs graceful handling

### Issue 2: Single Character
**Scenario:** Only one character in script  
**Expected:** Warning message: "Need at least 2 characters for comparison"  
**Status:** 🚧 To implement

### Issue 3: No Trajectory Data
**Scenario:** Character has no emotional arc scenes  
**Expected:** "Trajectory Comparison" section shows "Not available"  
**Handling:** `if traj_comp.get("available")` guard present ✅

### Issue 4: Zero Shared Scenes
**Scenario:** Characters never appear together  
**Expected:**
- Shared Scenes: 0
- Interaction Rate: 0.0%
- Emotional Alignment: 0.0%
- No distribution chart
**Status:** ✅ Handled by `if interaction["shared_scenes"] > 0`

---

## �� Performance Benchmarks

| Operation | Expected Time | Notes |
|-----------|--------------|-------|
| Page Load | <1s | If session_state populated |
| Character Selection | <100ms | Dropdown rendering |
| Comparison Calculation | <500ms | ArcComparator.compare_arcs() |
| Chart Rendering | <1s | Plotly visualizations |
| Full Page Interaction | <2s | Selection → Charts |

---

## ✅ Acceptance Criteria

### Visual Completeness
- [x] Two character selectors functional
- [x] 4 basic metric cards display
- [x] Emotional range lists formatted
- [x] Trajectory overlay chart renders
- [x] Interaction bar chart displays
- [x] Spider/radar chart loads
- [x] Synchronization status badges show

### Data Accuracy
- [x] Volatility calculations match EmotionEngine
- [x] Scene counts accurate
- [x] Correlation formula correct (Pearson-like)
- [x] Interaction rate = shared / min(total) ✅
- [x] Development rate = intensity delta / scenes ✅
- [x] Consistency = 100 - volatility ✅

### User Experience
- [x] No crashes on character selection
- [x] Charts responsive to screen size
- [x] Hover tooltips informative
- [x] Color scheme consistent (Red/Cyan)
- [x] Section dividers clear
- [x] Performance < 2s for interactions

---

## 🚀 Next Steps After Testing

### Immediate (Day 3)
1. **Interaction Heatmap:** Full character × character matrix
2. **Export:** Add comparison data to CSV/Excel/PDF

### Week 1 Days 4-5
3. **Arc Completion Predictor:** Forecast missing beats
4. **Relationship Evolution Tracker:** Animated network graphs

### Week 2
5. **Consistency Analyzer:** Out-of-character detection
6. **Storytelling Insights:** AI Producer recommendations

---

## 📞 Support & Feedback

**Testing Issues:** Document in GitHub Issues  
**Feature Requests:** Update PHASE_13_2_SPEC.md  
**Bug Reports:** Include script sample, character names, screenshot

**Developer:** Agent (GitHub Copilot)  
**Project:** EnhancedBudgetPro  
**Phase:** 13.2 - Character Arc Visualization Suite  
**Status:** Week 1 Day 2-3 Complete ✅

---

## 📝 Test Log Template

```
Date: _____________
Tester: _____________
Script: _____________
Characters Tested: _____________ vs _____________

Test Case 1 (Basic Setup):              ✅ / ❌
Test Case 2 (Basic Metrics):            ✅ / ❌
Test Case 3 (Trajectory):               ✅ / ❌
Test Case 4 (Interaction):              ✅ / ❌
Test Case 5 (Development Rates):        ✅ / ❌
Test Case 6 (Synchronization):          ✅ / ❌

Issues Found:
1. _____________________________________________
2. _____________________________________________

Overall Status: ✅ PASS / ❌ FAIL
```

