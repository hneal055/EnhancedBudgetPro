# Phase 7.0 Production Optimization Console - Testing Guide

## ⚠️ Prerequisites

**The Optimization Console requires these flows to run FIRST:**
1. ✅ Script Intelligence (Page 1)
2. ✅ Financial Intelligence (Page 2)
3. ✅ Production Budget (Page 3)
4. ✅ Stripboard Scheduler (Page 5)

Without these, you'll see: **"⚠️ Run Script, Financial, Budget, and Scheduler flows first."**

---

## 📝 Complete UI Testing Steps

### Step 1: Start Streamlit
```bash
streamlit run ui_app.py
```
Browser: http://localhost:8501

### Step 2: Story Intelligence (Page 1)
1. Click "📄 Story Intelligence" in sidebar
2. Upload **samples/test_script.fdx**
3. Wait for analysis to complete
4. Verify:
   - Scene count: 3
   - Characters: MARCUS, ELIJAH, RAMIREZ

### Step 3: Financial Intelligence (Page 2)
1. Click "💰 Financial Intelligence"
2. Review character cost breakdown
3. Check metrics:
   - Total Estimated Cast Cost
   - Cost per character
   - Scene frequency analysis

### Step 4: Production Budget (Page 3)
1. Click "🎬 Production Budget"
2. Review budget categories:
   - Above the Line
   - Below the Line
   - Post Production
   - Contingency & Insurance
3. Note **Final Production Budget** amount

### Step 5: Stripboard Scheduler (Page 5)
1. Click "📅 Scheduling/Stripboard"
2. Click **"Generate Schedule"** button
3. Review stripboard layout
4. Check shoot day assignments

### Step 6: Optimization Console (Page 7) ✅
1. Click "🧠 Optimization Console"
2. **All metrics should now populate:**

---

## 📊 Expected Results in Console

### Top-Level Metrics
- **Final Studio Budget**: $500,000 (varies by script)
- **Total Cast Cost**: $100,000 - $150,000
- **Avg Daily Burn**: $150,000 - $200,000

### Schedule Snapshot
- **Total Shoot Days**: 3-5 days
- **Peak Burn Day**: Highest cost day identified
- **High-Risk Scenes**: Count of complex scenes

### Combined Schedule View
| Day | Scene | Characters | Daily Burn ($) |
|-----|-------|------------|----------------|
| 1   | INT. APARTMENT | MARCUS | $15,000 |
| 2   | EXT. STREET | ELIJAH | $14,000 |
| 3   | INT. STATION | ALL | $28,000 |

### Optimization Recommendations
The console provides **automated analysis**:

1. **Burn Variance Analysis**
   - ⚠️ If peak day >50% above average: Redistribute scenes
   - ✅ If balanced: No action needed

2. **Cast Utilization**
   - 💡 Flags characters working <3 days
   - Suggests scene consolidation

3. **Risk Concentration**
   - ⚠️ If >30% high-risk: Add contingency
   - ✅ If acceptable: Proceed as planned

### Status Summary
- ✅ Script + Financial Intelligence online
- ✅ Master Studio Budget online
- ✅ Stripboard scheduling online
- ℹ️ Auto-reschedule status (if applied)

---

## 🧪 Command-Line Testing

Run automated test:
```bash
cd /workspaces/EnhancedBudgetPro
python test_phase_7_pipeline.py
```

This validates the entire pipeline without the UI.

---

## 🐛 Troubleshooting

### Issue: "Run Script, Financial, Budget flows first"
**Solution**: You skipped prerequisite pages. Go back and complete Steps 2-5 above.

### Issue: Empty schedule view
**Solution**: Click "Generate Schedule" button on Page 5 (Stripboard).

### Issue: Missing metrics
**Solution**: Ensure script was successfully uploaded on Page 1. Check for error messages.

### Issue: Peak burn day shows "N/A"
**Solution**: This is normal if burn rate data is unavailable. Other metrics still work.

---

## ✅ Success Criteria

Phase 7.0 is working correctly if you see:

1. ✅ Three metric cards at top (Budget, Cast Cost, Burn Rate)
2. ✅ Schedule snapshot with shoot day count
3. ✅ Combined schedule table with all scenes
4. ✅ Green status checkmarks for all flows
5. ✅ Optimization recommendations section (may be empty if no issues detected)

---

## 📈 Advanced Features (Phase 7.0)

### NEW: Optimization Recommendations
The console now includes **automated intelligence**:

- **Burn Rate Analysis**: Detects cost imbalances
- **Cast Efficiency**: Identifies underutilized talent
- **Risk Assessment**: Warns about high-risk concentrations

### Integration Points
Phase 7.0 integrates data from:
- Character Intelligence (scene frequency)
- Cost Impact Analysis (per-character budgets)
- Stripboard Scheduler (daily assignments)
- Burn Rate Forecasting (cost distribution)
- Risk Analysis (complexity scoring)

---

## 🚀 Next Steps

After validating Phase 7.0:
1. Test **What-If Scenarios** (Page 7b)
2. Try **Talent Availability** (Page 6)
3. Explore **Auto-Rescheduling** (Page 11)
4. Review **Advanced Visualizations** (Page 17)

---

## 📝 Notes

- **Session State**: All data persists during your Streamlit session
- **Reloading**: Refreshing browser clears session - reupload script
- **Test Data**: Use `samples/test_script.fdx` for consistent results
- **Real Scripts**: Works with any FDX, Fountain, or Celtx file

---

**Testing Status**: ✅ Phase 7.0 validated and ready for production use!

