import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Command Center — Enhanced Budget Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------
# SAFETY: ENSURE CORE SESSION KEYS EXIST
# ----------------------------------------------------
def ss(key, default):
    if key not in st.session_state:
        st.session_state[key] = default
    return st.session_state[key]

ss("data", None)
ss("characters", [])
ss("cost_summary", {})
ss("schedule_summary", {})
ss("talent_availability", {})
ss("whatif_results", pd.DataFrame())
ss("risk_results", {})
ss("density", None)

# ----------------------------------------------------
# HEADER
# ----------------------------------------------------
st.markdown("""
# 🎬 **Enhanced Budget Pro — Command Center**
### The unified control hub for story intelligence, budgeting, forecasting, and production readiness.
---
""")

col1, col2, col3 = st.columns([1,1,1])

# ----------------------------------------------------
# BLOCK A — SCRIPT SUMMARY
# ----------------------------------------------------
with col1:
    st.subheader("📘 Script Overview")

    data = st.session_state.data
    if data:
        scenes = data.get("scenes", [])
        st.metric("Scenes", len(scenes))

        char_count = len(st.session_state.get("characters", []))
        st.metric("Characters", char_count)

        total_lines = sum(len(s.get("lines", [])) for s in scenes)
        st.metric("Total Script Lines", total_lines)

    else:
        st.info("No script loaded yet. Import a screenplay to begin.")

# ----------------------------------------------------
# BLOCK B — FINANCIAL SUMMARY
# ----------------------------------------------------
with col2:
    st.subheader("💰 Financial Summary")

    cost = st.session_state.cost_summary
    if cost:
        st.metric("Cast Total", f"${cost.get('total_estimated_cast_cost', 0):,}")
        st.metric("Production Total", f"${cost.get('production_total', 0):,}")
        st.metric("Master Budget", f"${cost.get('final_budget', 0):,}")
    else:
        st.info("Financial intelligence has not been calculated yet.")

# ----------------------------------------------------
# BLOCK C — RISK / FORECASTING SUMMARY
# ----------------------------------------------------
with col3:
    st.subheader("⚠️ Risk Intelligence")

    risk = st.session_state.risk_results
    if risk:
        st.metric("P10", f"${risk.get('p10', 0):,}")
        st.metric("Mean", f"${risk.get('mean', 0):,}")
        st.metric("P90", f"${risk.get('p90', 0):,}")
    else:
        st.info("Run Monte Carlo to generate risk forecast.")

# ----------------------------------------------------
# STRIPBOARD / SCHEDULE SUMMARY
# ----------------------------------------------------
st.markdown("---")
st.header("📅 Production Schedule Overview")

schedule = st.session_state.schedule_summary
if schedule:
    days = schedule.get("total_days", "—")
    scenes_per_day = schedule.get("avg_scenes_per_day", "—")
    heaviest_day = schedule.get("max_load_day", "—")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Shooting Days", days)
    c2.metric("Avg Scenes / Day", scenes_per_day)
    c3.metric("Peak Load Day", heaviest_day)
else:
    st.info("Scheduling not generated yet. Run Stripboard Scheduler.")

# ----------------------------------------------------
# TALENT AVAILABILITY SUMMARY
# ----------------------------------------------------
st.markdown("---")
st.header("🎭 Talent Availability Snapshot")

tal = st.session_state.talent_availability

if tal and isinstance(tal, dict):
    st.write("Cast Availability Grid Loaded.")
else:
    st.info("Talent availability has not been processed yet.")

# ----------------------------------------------------
# WHAT-IF SCENARIOS SUMMARY
# ----------------------------------------------------
st.markdown("---")
st.header("🔮 Scenario Forecasting Summary")

results_df = st.session_state.whatif_results

if isinstance(results_df, pd.DataFrame) and not results_df.empty:
    st.dataframe(results_df.head(), width="stretch")
else:
    st.info("No scenarios generated yet.")

# ----------------------------------------------------
# NAVIGATION PANEL
# ----------------------------------------------------
st.markdown("---")
st.header("🚀 Navigation & Tools")

nav_col1, nav_col2, nav_col3 = st.columns(3)

with nav_col1:
    st.subheader("📘 Story / Script")
    st.page_link("ui_app.py", label="🏠 Main App")
    st.page_link("pages/1_Story_Intelligence.py", label="Story Intelligence")
    st.page_link("pages/2_Financial_Intelligence.py", label="Financial Intelligence")

with nav_col2:
    st.subheader("🎬 Production")
    st.page_link("pages/5_Stripboard_Scheduler.py", label="Stripboard Scheduler")
    st.page_link("pages/6_Talent_Availability.py", label="Talent Availability")
    st.page_link("pages/5_Scheduling_Stripboard.py", label="Scheduling")

with nav_col3:
    st.subheader("📊 Forecasting")
    st.page_link("pages/4_Risk_Monte_Carlo.py", label="Monte Carlo")
    st.page_link("pages/7_WhatIf_Scenarios.py", label="What-If Scenario Engine")
    st.page_link("pages/9_Scenario_Visualization.py", label="Scenario Visualization")

# ----------------------------------------------------
# FOOTER
# ----------------------------------------------------
st.markdown("""
<br><br>
---
### **Enhanced Budget Pro (v8.0) — Film Studio Intelligence Suite**  
Smarter budgeting. Smarter scheduling. Smarter storytelling.
""", unsafe_allow_html=True)
