"""
Test Phase 7.0 Production Optimization Console
Prerequisites: Script, Financial, Budget, and Scheduler flows
"""

import sys
sys.path.insert(0, '.')

from src.ScriptIngest import run_full_analysis
from src.SchedulingEngine.production_scheduler import ProductionSchedulerEngine
from src.SchedulingEngine.burn_rate_engine import BurnRateEngine
from src.AnalysisEngine.risk_analysis_engine import ScriptRiskAnalysisEngine
import json

print("=" * 70)
print("🧪 PHASE 7.0 OPTIMIZATION CONSOLE - PIPELINE TEST")
print("=" * 70)

# STEP 1: Load and analyze script
print("\n📄 STEP 1: Script Intelligence...")
script_path = "samples/test_script.fdx"
results = run_full_analysis(script_path, "test_output")

data = results.get("data")
intel = results.get("intelligence")
cost = results.get("cost_impact")
master = results.get("master_budget")

if not data:
    print("❌ Failed to load script data")
    sys.exit(1)

print(f"✅ Script loaded: {data['scene_count']} scenes")
print(f"✅ Characters: {', '.join(data['characters'][:5])}")

# STEP 2: Financial Intelligence
print("\n💰 STEP 2: Financial Intelligence...")
if cost:
    total_cast = cost.get("total_estimated_cast_cost", 0)
    print(f"✅ Total Cast Cost: ${total_cast:,.2f}")
    
    char_costs = cost.get("character_costs", {})
    print(f"✅ Character costs calculated: {len(char_costs)} characters")
    for char, cost_val in list(char_costs.items())[:3]:
        print(f"   • {char}: ${cost_val:,.2f}")
else:
    print("❌ Cost data missing")
    sys.exit(1)

# STEP 3: Production Budget
print("\n🎬 STEP 3: Production Budget...")
if master:
    final_budget = (
        master.get("final_production_budget") 
        or master.get("final_total", 0)
    )
    print(f"✅ Master Budget: ${final_budget:,.2f}")
    
    # Show budget breakdown
    if "budget_summary" in master:
        summary = master["budget_summary"]
        print(f"   • Above Line: ${summary.get('above_line', 0):,.2f}")
        print(f"   • Below Line: ${summary.get('below_line', 0):,.2f}")
        print(f"   • Post Production: ${summary.get('post', 0):,.2f}")
else:
    print("❌ Master budget missing")
    sys.exit(1)

# STEP 4: Scheduler/Stripboard
print("\n📅 STEP 4: Production Scheduler...")
scheduler = ProductionSchedulerEngine()
schedule = scheduler.generate_schedule(
    data["scenes"],
    cost.get("character_costs", {})
)

if schedule:
    daily_schedule = schedule.get("daily_schedule", [])
    num_days = len({d["shoot_day"] for d in daily_schedule})
    print(f"✅ Schedule generated: {num_days} shoot days")
    print(f"✅ Total scenes scheduled: {len(daily_schedule)}")
    
    # Show first 3 days
    for day_num in range(1, min(4, num_days + 1)):
        day_scenes = [
            s for s in daily_schedule 
            if s.get("shoot_day") == day_num
        ]
        print(f"   • Day {day_num}: {len(day_scenes)} scene(s)")
else:
    print("❌ Schedule generation failed")
    sys.exit(1)

# STEP 5: Burn Rate Analysis
print("\n🔥 STEP 5: Burn Rate Analysis...")
burn_engine = BurnRateEngine()
burn = burn_engine.calculate(schedule, master)

if burn:
    avg_burn = burn.get("average_daily_burn", 0)
    total_burn = burn.get("total_estimated_burn", 0)
    peak = burn.get("peak_burn_day")
    
    print(f"✅ Average Daily Burn: ${avg_burn:,.2f}")
    print(f"✅ Total Estimated Burn: ${total_burn:,.2f}")
    
    if peak:
        print(f"✅ Peak Burn Day: Day {peak['day']} - ${peak['cost']:,.2f}")
else:
    print("⚠️  Burn rate data not available (continuing)")
    burn = {"average_daily_burn": 0, "daily_schedule": daily_schedule}

# STEP 6: Risk Analysis
print("\n⚠️  STEP 6: Risk Analysis...")
risk_engine = ScriptRiskAnalysisEngine()
risk = risk_engine.analyze(data["scenes"])

if risk:
    high_risk = risk.get("high_risk_scene_count", 0)
    medium_risk = risk.get("medium_risk_scene_count", 0)
    print(f"✅ High Risk Scenes: {high_risk}")
    print(f"✅ Medium Risk Scenes: {medium_risk}")
else:
    print("⚠️  Risk data not available (continuing)")
    risk = {"high_risk_scene_count": 0}

# STEP 7: Optimization Console Simulation
print("\n🧠 STEP 7: Optimization Console Metrics...")
print("=" * 70)

# Build session state simulation
session_state = {
    "data": data,
    "cost": cost,
    "burn": burn,
    "master": master,
    "risk": risk,
    "auto_rescheduled": None,
    "schedule": schedule
}

# Console Top Metrics
print("\n📊 TOP-LEVEL METRICS:")
print(f"   Final Studio Budget: ${final_budget:,.2f}")
print(f"   Total Cast Cost: ${total_cast:,.2f}")
print(f"   Avg Daily Burn: ${avg_burn:,.2f}")

# Schedule Snapshot
print("\n🎬 SCHEDULE SNAPSHOT:")
print(f"   Total Shoot Days: {num_days}")
if peak:
    print(f"   Peak Burn Day: Day {peak['day']} - ${peak['cost']:,.2f}")
print(f"   High-Risk Scenes: {high_risk}")

# Combined Stripboard View
print("\n📋 COMBINED SCHEDULE + BURN VIEW:")
print(f"{'Day':<6} {'Scene':<25} {'Characters':<30} {'Burn ($)':<12}")
print("-" * 73)

for entry in daily_schedule[:5]:  # Show first 5
    day = entry.get("shoot_day", "?")
    scene = entry.get("scene", "")[:23]
    chars = ", ".join(entry.get("characters", []))[:28]
    daily_burn = entry.get("daily_burn", 0)
    print(f"{day:<6} {scene:<25} {chars:<30} ${daily_burn:>10,.2f}")

if len(daily_schedule) > 5:
    print(f"... and {len(daily_schedule) - 5} more scenes")

# Optimization Recommendations
print("\n💡 OPTIMIZATION RECOMMENDATIONS:")

# Burn variance check
if peak and avg_burn > 0:
    peak_cost = peak.get("cost", 0)
    variance_pct = ((peak_cost - avg_burn) / avg_burn) * 100
    
    if variance_pct > 50:
        print(f"   ⚠️  Peak burn day is {variance_pct:.0f}% above average")
        print(f"      Consider redistributing scenes to balance costs")
    else:
        print(f"   ✅ Burn rate is relatively balanced")

# Character utilization
char_days = {}
for entry in daily_schedule:
    for char in entry.get("characters", []):
        char_days[char] = char_days.get(char, 0) + 1

underutilized = [
    f"{char} ({days} day(s))" 
    for char, days in char_days.items() 
    if days < 3 and num_days >= 5
]

if underutilized:
    print(f"   💡 Underutilized talent: {', '.join(underutilized)}")
    print(f"      Consider consolidating scenes")

# Risk concentration
if len(daily_schedule) > 0:
    risk_pct = (high_risk / len(daily_schedule)) * 100
    
    if risk_pct > 30:
        print(f"   ⚠️  {risk_pct:.0f}% of scenes are high-risk")
        print(f"      Consider additional contingency planning")
    elif risk_pct > 0:
        print(f"   ✅ Risk concentration acceptable: {risk_pct:.1f}%")

# Status Summary
print("\n✅ OPTIMIZATION STACK STATUS:")
print("   ✅ Script + Financial Intelligence online")
print("   ✅ Master Studio Budget online")
print("   ✅ Stripboard scheduling online")
print("   ℹ️  Auto-reschedule not applied (using base schedule)")

print("\n" + "=" * 70)
print("✅ PHASE 7.0 PIPELINE TEST COMPLETE!")
print("=" * 70)

print("\n📝 Next Steps:")
print("   1. Start Streamlit: streamlit run ui_app.py")
print("   2. Upload samples/test_script.fdx in Story Intelligence")
print("   3. Navigate through pages 1-6 to build session state")
print("   4. Open page 7 (Optimization Console) to view results")
print("\nAll prerequisites validated - Phase 7.0 ready for testing! 🚀")
