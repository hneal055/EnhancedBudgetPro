import streamlit as st

# ----------------------------------------------------
# GLOBAL APP CONFIG
# ----------------------------------------------------
st.set_page_config(
    page_title="PILOTFORGEAI — Command Center",
    layout="wide",
)

# ----------------------------------------------------
# SHARED SESSION STATE BOOTSTRAP
# ----------------------------------------------------
default_keys = {
    "data": None,
    "intel": None,
    "density": None,
    "cost": None,
    "burn": None,
    "risk": None,
    "schedule": None,
    "talent_overrides": {},
    "whatif_results": {},
    "master_budget": None,
    "raw_script": "",
    "emotion_data": None,  # Phase 13.1: Emotional Intelligence
}

for k, v in default_keys.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ----------------------------------------------------
# UNIFIED SIDEBAR (STATUS + QUICK GUIDE)
# ----------------------------------------------------
with st.sidebar:
    st.header("🎛 Studio Sidebar")

    st.markdown("**Project Status**")

    def status_row(label: str, ok: bool):
        icon = "✅" if ok else "⬜"
        st.write(f"{icon} {label}")

    status_row("Script Parsed", st.session_state.data is not None)
    status_row("Story Intelligence", st.session_state.intel is not None and st.session_state.density is not None)
    status_row("Financial Intelligence", st.session_state.cost is not None)
    status_row("Scheduler / Stripboard", st.session_state.schedule is not None)
    status_row("Talent Availability", st.session_state.talent_overrides is not None and len(st.session_state.talent_overrides) > 0)
    status_row("Master Budget", st.session_state.master_budget is not None)
    status_row("What-If Scenarios", st.session_state.whatif_results is not None and (isinstance(st.session_state.whatif_results, dict) or not st.session_state.whatif_results.empty))
    status_row("Emotional Intelligence", st.session_state.emotion_data is not None)  # Phase 13.1

    st.divider()
    st.markdown("**Navigation Map**")
    st.write("1️⃣ Story Intelligence")
    st.write("2️⃣ Financial Intelligence")
    st.write("3️⃣ Master Production Budget")
    st.write("4️⃣ Risk + Monte Carlo")
    st.write("5️⃣ Scheduling / Stripboard")
    st.write("6️⃣ Talent Availability & Auto-Reschedule")
    st.write("7️⃣ What-If Scenario Lab")
    st.write("8️⃣ 🧠 Emotional Intelligence")  # Phase 13.1

    st.divider()
    st.markdown("**Quick Actions**")

    if st.button("🔁 Reset All Session Data"):
        for k in default_keys.keys():
            st.session_state[k] = default_keys[k]
        st.success("Session reset. You can re-analyze from Page 1.")

# ----------------------------------------------------
# COMMAND CENTER MAIN VIEW
# ----------------------------------------------------
st.title("🎬 PILOTFORGEAI — Studio Command Center")

st.markdown(
    """
Welcome to the **Unified Control Hub**.

Use the left page list to move between:

1. **🧠 Story Intelligence** — parse script, characters, scenes  
2. **💰 Financial Intelligence** — day rates, cast cost, burn rate  
3. **🏗 Master Production Budget** — crew, locations, insurance, final budget  
4. **⚠️ Risk & Monte Carlo** — scene risk + budget volatility forecasts  
5. **🎞 Stripboard Scheduler** — day-by-day shooting breakdown  
6. **🎭 Talent Availability** — availability grid + auto-reschedule helper  
7. **🧪 What-If Scenarios** — auto-generated scenarios for decision making
8. **�� Emotional Intelligence** — character arcs, scene intensity, turning points
"""
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📌 Pipeline Progress")

    st.write(
        "- ✅ **Step 1:** Paste script & analyze (Page 1)\n"
        "- ✅ **Step 2:** Configure day rates & burn (Page 2)\n"
        "- ✅ **Step 3:** Build master budget (Page 3)\n"
        "- ✅ **Step 4:** Run risk + Monte Carlo (Page 4)\n"
        "- ✅ **Step 5:** Generate stripboard (Page 5)\n"
        "- ✅ **Step 6:** Mark talent availability & rescheduling (Page 6)\n"
        "- ✅ **Step 7:** Explore What-If scenarios (Page 7)\n"
        "- ✅ **Step 8:** View emotional intelligence (Page 8)\n"
    )

with col2:
    st.subheader("📊 Current Snapshot")

    total_scenes = st.session_state.data["scene_count"] if st.session_state.data else 0
    total_chars = len(st.session_state.intel["character_stats"]) if st.session_state.intel else 0
    final_budget = (
        st.session_state.master_budget.get("final_production_budget", 0.0)
        if st.session_state.master_budget
        else 0.0
    )
    
    # Phase 13.1: Add emotional intelligence metrics
    emotion_summary = st.session_state.emotion_data.get("summary", {}) if st.session_state.emotion_data else {}
    avg_intensity = emotion_summary.get("average_intensity", 0.0)
    character_arcs = emotion_summary.get("characters_with_arcs", 0)

    st.metric("Scenes Parsed", total_scenes)
    st.metric("Characters Tracked", total_chars)
    st.metric("Final Studio Budget", f"${final_budget:,.2f}")
    st.metric("Avg Scene Intensity", f"{avg_intensity:.1f}/100")
    st.metric("Character Arcs", character_arcs)

st.info(
    "Tip: If anything feels out of sync, revisit pages 1–3 in order, then work forward again. "
    "All new UIs are now using a unified, stable structure. "
    "**NEW: Emotional Intelligence analysis now runs automatically on script upload!**"
)
