# Phase 13.2 Testing Guide

## Quick Start

### 1. Start Flask Server
```bash
python web_app.py
# Flask will run on http://localhost:8000
```

### 2. Open Browser
Navigate to: **http://localhost:8000**

### 3. Upload Test Script
Choose one of the sample scripts:

- **test_comparison_simple.fdx** - Quick smoke test (3 scenes, 2 characters)
- **test_comparison.fdx** - Standard test (6 scenes, SARAH & MARK)
- **test_comparison_complex.fdx** - Multi-character (8 scenes, 4 characters)
- **test_comparison_romance.fdx** - Romance arc (7 scenes, RILEY & SAM)

### 4. Verify Dashboard Sections

After upload, you should see 12 sections:

#### Phase 13.2 Advanced Features (NEW)
1. **Storytelling Health Dashboard**
   - Overall health score (0-100)
   - 4 health metrics with progress bars
   - AI Producer recommendations table
   - Priority badges (HIGH/MEDIUM/LOW)

2. **Character Arc Classifications**
   - Each character with arc type badge
   - Confidence percentage and progress bar
   - Arc description text

3. **Emotional Intelligence Charts**
   - Plotly line charts for each character
   - Color-coded emotions (joy=yellow, sadness=blue, etc.)
   - Interactive hover tooltips
   - Scene-by-scene progression

4. **Character Interaction Heatmap**
   - NxN matrix visualization (Plotly)
   - Darker colors = more interactions
   - Shows which characters share scenes

5. **Arc Completion Predictions**
   - Completion percentage per character
   - Missing beats list
   - Actionable suggestions

6. **Relationship Evolution Tracker**
   - Character pairs with relationship types
   - Sentiment start/end states
   - Trajectory (improving/declining/stable)
   - Turning points with scene numbers

7. **Consistency Analysis**
   - Consistency score (0-100) per character
   - Out-of-character moments list
   - Severity badges (SEVERE/MODERATE/MINOR)
   - Scene references

#### Existing Features (Phase 13.1)
8. Scene Budget Breakdown
9. Scene Risk Overview
10. Character List
11. Top Stats (Scenes, Characters, Budget)
12. Export Downloads (Excel, JSON)

### 5. Test Interactivity

- **Hover over charts** - Should show tooltips with emotion names
- **Scroll tables** - Should stay within card boundaries
- **Click export buttons** - Should download Excel/JSON files
- **Resize browser** - Should be responsive (mobile-friendly)

### 6. Expected Results

#### test_comparison_simple.fdx
- 3 scenes detected
- 2 characters (ALEX, JORDAN)
- Simple emotional arc: anger → sadness → joy
- High consistency scores (simple dialogue)
- 1 character pair in heatmap (2x2 matrix)

#### test_comparison.fdx
- 6 scenes detected
- 2 characters (SARAH, MARK)
- Emotional journey: anger → sadness → hope → joy
- Multiple relationship turning points
- Health score ~70-85%

#### test_comparison_complex.fdx
- 8 scenes detected
- 4 characters (EMMA, NOAH, OLIVIA, LIAM)
- Complex heatmap (4x4 matrix)
- Multiple character pairs
- Ensemble scene analysis

#### test_comparison_romance.fdx
- 7 scenes detected
- 2 characters (RILEY, SAM)
- Romantic arc: meet-cute → crisis → love
- Strong relationship evolution
- Positive sentiment trajectory

## Validation Checklist

### Backend
- [ ] Flask starts without errors
- [ ] File upload completes successfully
- [ ] No "0 scenes detected" errors
- [ ] All 7 Phase 13.2 engines execute
- [ ] Result dict contains all 8 data structures

### Frontend
- [ ] Upload form displays
- [ ] Top stats populate correctly
- [ ] All 7 Phase 13.2 sections render
- [ ] Plotly charts display (not blank)
- [ ] Tables show data (not empty)
- [ ] Progress bars show percentage
- [ ] Badges show correct colors
- [ ] No JavaScript console errors

### Data Accuracy
- [ ] Scene count matches script
- [ ] Character count matches script
- [ ] Emotions progress logically
- [ ] Arc types seem appropriate
- [ ] Health score is reasonable (40-90%)
- [ ] Consistency scores logical
- [ ] Recommendations make sense

### Exports
- [ ] Excel download works
- [ ] JSON download works
- [ ] Files contain Phase 13.2 data
- [ ] Multi-sheet workbook structured correctly

## Troubleshooting

### Issue: Blank Plotly Charts
**Solution:** Check browser console for JavaScript errors. Ensure Plotly CDN loaded.

### Issue: "0 scenes detected"
**Solution:** This should NOT happen with Flask. If it does, check:
- File actually uploaded (check web_output/{job_id}/)
- Script format supported (FDX, Fountain, PDF, TXT)
- No parse errors in terminal logs

### Issue: Missing Phase 13.2 Sections
**Solution:** Check that web_app.py passes all data:
```python
emotion_data=emotion_data,
arc_classifications=arc_classifications,
# ... etc
```

### Issue: Template Syntax Errors
**Solution:** Check Jinja2 template syntax in dashboard.html

### Issue: Import Errors
**Solution:** Verify all CharacterArcEngine modules exist:
```bash
ls -l src/CharacterArcEngine/
# Should see: arc_classifier, arc_comparator, interaction_heatmap,
#             arc_predictor, relationship_tracker, consistency_analyzer,
#             storytelling_insights, character_analysis_exporter
```

## Performance Benchmarks

| Script | Scenes | Chars | Parse Time | Emotion Time | Total Time |
|--------|--------|-------|------------|--------------|------------|
| simple | 3      | 2     | <1s        | ~2s          | ~3s        |
| standard | 6    | 2     | <1s        | ~3s          | ~4s        |
| complex | 8     | 4     | <1s        | ~4s          | ~5s        |
| romance | 7     | 2     | <1s        | ~3s          | ~4s        |

*Note: Emotion analysis uses HuggingFace transformer model (j-hartmann/emotion-english-distilroberta-base), which takes 2-5 seconds depending on dialogue count.*

## Browser Compatibility

Tested on:
- ✅ Chrome 120+ (Recommended)
- ✅ Firefox 120+
- ✅ Edge 120+
- ⚠️ Safari 17+ (Plotly may have minor rendering differences)
- ❌ IE11 (Not supported - use modern browser)

## Mobile/Tablet Testing

- Bootstrap 5 responsive grid
- Cards stack vertically on mobile
- Tables scroll horizontally in small viewports
- Charts resize automatically (Plotly responsive mode)

## Next Steps After Testing

1. **If tests pass:** Ready for production deployment
2. **If issues found:** Report specific errors with:
   - Browser/version
   - Test script used
   - Screenshot/console errors
   - Expected vs actual behavior

3. **Future enhancements:** See FLASK_MIGRATION_COMPLETE.md for roadmap

---

**Happy Testing! 🚀**

*For issues or questions, refer to FLASK_MIGRATION_COMPLETE.md*
