import streamlit as st
import pandas as pd
from src.components.sidebar import render_sidebar
from src.ui.global_sidebar import install_global_sidebar

render_sidebar()
install_global_sidebar()

st.set_page_config(page_title="Optimization Console", layout="wide")
st.title("🧠 Phase 7.0 — Production Optimization Console")

# -------------------------------------------------
# SAFETY GUARDS
# -------------------------------------------------
data = st.session_state.get("data")
cost = st.session_state.get("cost")
burn = st.session_state.get("burn")
master = st.session_state.get("master")
risk = st.session_state.get("risk")
auto_rescheduled = st.session_state.get("auto_rescheduled")

if not data or not cost or not burn or not master:
    st.warning(
        "⚠️ Run Script, Financial, Budget, and Scheduler flows first."
    )
    st.stop()

# -------------------------------------------------
# TOP-LEVEL METRICS
# -------------------------------------------------
col1, col2, col3 = st.columns(3)

# Final studio budget
final_budget = (
    master.get("final_production_budget")
    or master.get("final_total", 0)
)
col1.metric("🎯 Final Studio Budget", f"${final_budget:,.2f}")

# Cast cost
total_cast_cost = cost.get("total_estimated_cast_cost", 0)
col2.metric("🎭 Total Cast Cost", f"${total_cast_cost:,.2f}")

# Average daily burn
avg_burn = burn.get("average_daily_burn", 0)
col3.metric("🔥 Avg Daily Burn", f"${avg_burn:,.2f}")

# -------------------------------------------------
# SCHEDULING SNAPSHOT
# -------------------------------------------------
st.subheader("🎬 Schedule Snapshot")

schedule_source = (
    auto_rescheduled or burn.get("daily_schedule", [])
)

if schedule_source:
    num_days = len({d["shoot_day"] for d in schedule_source})
else:
    num_days = 0

colA, colB, colC = st.columns(3)

colA.metric("Total Shoot Days (current)", num_days)

peak = burn.get("peak_burn_day")
if peak:
    day_num = peak.get("day")
    cost_val = peak.get("cost", 0)
    colB.metric(
        "🚨 Peak Burn Day",
        f"Day {day_num} — ${cost_val:,.2f}"
    )
else:
    colB.metric("🚨 Peak Burn Day", "N/A")

if risk and isinstance(risk, dict):
    high_risk_count = risk.get("high_risk_scene_count", 0)
    colC.metric("⚠️ High-Risk Scenes", high_risk_count)
else:
    colC.metric("⚠️ High-Risk Scenes", "N/A")

# -------------------------------------------------
# COMBINED STRIPBOARD VIEW
# -------------------------------------------------
st.subheader("📋 Combined Schedule + Burn View")

if not schedule_source:
    st.info("No schedule available yet. Run the Scheduler first.")
else:
    rows = []
    for entry in schedule_source:
        rows.append(
            {
                "Day": entry.get(
                    "rescheduled_day", entry.get("shoot_day")
                ),
                "Scene": entry.get("scene"),
                "Characters": ", ".join(
                    entry.get("characters", [])
                ),
                "Daily Burn ($)": entry.get("daily_burn", 0),
            }
        )

    df = pd.DataFrame(rows).sort_values(by=["Day"])
    st.dataframe(df, width="stretch")

# -------------------------------------------------
# STATUS SUMMARY
# -------------------------------------------------
st.subheader("✅ Optimization Stack Status")

st.success("Script + Financial Intelligence online ✅")
st.success("Master Studio Budget online ✅")
st.success("Stripboard scheduling online ✅")

if auto_rescheduled:
    st.success("Availability-aware auto-rescheduling ACTIVE ✅")
else:
    st.info(
        "Auto-reschedule not applied yet (using base schedule)."
    )

# -------------------------------------------------
# OPTIMIZATION RECOMMENDATIONS
# -------------------------------------------------
st.subheader("💡 Optimization Recommendations")

# Check for high burn variance
if peak:
    avg_burn_val = burn.get("average_daily_burn", 0)
    peak_cost = peak.get("cost", 0)
    
    if avg_burn_val > 0:
        variance_pct = (
            (peak_cost - avg_burn_val) / avg_burn_val
        ) * 100
        
        if variance_pct > 50:
            st.warning(
                f"⚠️ Peak burn day is {variance_pct:.0f}% "
                "above average. Consider redistributing scenes."
            )
        else:
            st.success("✅ Burn rate is relatively balanced.")

# Check cast utilization
if cost:
    char_costs = cost.get("character_costs", {})
    if char_costs and schedule_source:
        # Count how many days each character works
        char_days = {}
        for entry in schedule_source:
            for char in entry.get("characters", []):
                char_days[char] = char_days.get(char, 0) + 1
        
        # Check for underutilized expensive talent
        for char, days_worked in char_days.items():
            if days_worked < 3 and num_days >= 5:
                st.info(
                    f"💡 {char} works only {days_worked} day(s). "
                    "Consider consolidating scenes."
                )

# Check risk concentration
if risk and isinstance(risk, dict):
    high_count = risk.get("high_risk_scene_count", 0)
    if schedule_source:
        total_scenes = len(schedule_source)
        if total_scenes > 0:
            risk_pct = (high_count / total_scenes) * 100
            
            if risk_pct > 30:
                st.warning(
                    f"⚠️ {risk_pct:.0f}% of scenes are high-risk. "
                    "Consider additional contingency planning."
                )
