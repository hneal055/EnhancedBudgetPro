# EnhancedBudgetPro - Page Testing Checklist

## ✅ Completed Pages
- [x] Page 1: Story Intelligence (file upload + emotion analysis working)
- [x] Page 14: Emotional Intelligence (visualizations confirmed)
- [x] Page 15: Character Arc Suite (all features working)
- [x] Page 16: Storytelling Insights (confirmed working)

## 🔄 Pages to Test

### Core Analysis Pages

**Page 2: Financial Intelligence** 
- Prerequisites: Page 1 complete (data + intel in session)
- Features to verify:
  - [ ] Character daily rates input table
  - [ ] Character cost impact calculation
  - [ ] Burn rate forecast table
  - [ ] Total estimated cast cost metric
- Expected behavior: Shows cost breakdown by character

**Page 3: Production Budget**
- Prerequisites: None (standalone)
- Features to verify:
  - [ ] Shoot days slider (5-120 days)
  - [ ] Crew budget total
  - [ ] Equipment budget total
  - [ ] Location budget total
  - [ ] Post production budget
  - [ ] Insurance & contingency
  - [ ] Grand total calculation
  - [ ] "Generate Final Budget PDF" button
- Expected behavior: Independent budget calculator

**Page 4: Risk & Monte Carlo**
- Prerequisites: Pages 1 & 2 (data, density, cost)
- Features to verify:
  - [ ] Risk analysis table (scene, characters, risk score)
  - [ ] High-risk scenes count
  - [ ] Monte Carlo simulation controls (runs, volatility)
  - [ ] Budget forecast (mean, p10, p90)
  - [ ] Simulation distribution table
- Expected behavior: Shows risk scores and budget simulations

### AI Producer Mode Pages (5-13)

**Page 5: Scheduling Stripboard**
- Prerequisites: Pages 1 & 2 (data + cost)
- Features: Basic stripboard view
- [ ] Renders without errors

**Page 6: Talent Availability**
- Prerequisites: Pages 1 & 2 (data + cost)
- Features: Talent scheduling constraints
- [ ] Renders without errors

**Page 7: Optimization Console** (OR **7: WhatIf Scenarios**)
- Prerequisites: Pages 1-3 (data, cost, burn, master, risk)
- Features: Optimization controls
- [ ] Renders without errors

**Page 8: AI Scenario Designer** (OR **8: Scenario Comparison**)
- Prerequisites: Pages 1-3
- Features: Scenario generation
- [ ] Renders without errors

**Page 9: Scenario Visualization**
- Prerequisites: Page 7 scenarios completed
- Features: Visualize scenario results
- [ ] Renders without errors

**Page 10: Stripboard Scheduler**
- Prerequisites: Pages 1 & 2
- Features: Advanced stripboard
- [ ] Renders without errors

**Page 11: Availability Auto-Rescheduling**
- Prerequisites: Page 5/10 schedule + talent overrides
- Features: Automatic rescheduling
- [ ] Renders without errors

**Page 12: Export Center**
- Prerequisites: Any completed analysis
- Features: Export to CSV/Excel/PDF
- [ ] Renders without errors

**Page 13: AI Producer Mode**
- Prerequisites: May be standalone or require full pipeline
- Features: AI-powered production decisions
- [ ] Renders without errors

## Testing Workflow

1. **Upload test_script.fdx on Page 1**
   - Verify: 3 scenes, 3 character arcs tracked

2. **Navigate to Page 2: Financial Intelligence**
   - Enter daily rates for MARCUS, ELIJAH, RAMIREZ
   - Verify cost calculations appear

3. **Navigate to Page 3: Production Budget**
   - Adjust shoot days slider
   - Verify totals recalculate
   - Test PDF export button

4. **Navigate to Page 4: Risk & Monte Carlo**
   - Verify risk table shows 3 scenes
   - Run Monte Carlo simulation
   - Check distribution data

5. **Test Pages 5-13 in order**
   - Note any missing prerequisite warnings
   - Verify each page renders
   - Test key interactive features

## Known Issues

- None currently - all Phase 13.2 pages working!

## Notes

- Page 3 is standalone - doesn't need script data
- Pages 9 & 11 need data from previous wizard steps
- Session state properly guards all pages
