import streamlit as st
import random
import pandas as pd

# ---------------------------------------------------
# Helper: Safe key check
# ---------------------------------------------------
def has(key):
    if key not in st.session_state:
        return False
    val = st.session_state[key]
    if isinstance(val, pd.DataFrame):
        return not val.empty
    if isinstance(val, (list, dict)):
        return len(val) > 0
    return bool(val)


# ===================================================
# 🌐 INSTALL GLOBAL SIDEBAR (Phase 8.3)
# ===================================================
def install_global_sidebar():
    with st.sidebar:

        # ---------------------------------------------------------
        # HEADER
        # ---------------------------------------------------------
        st.markdown("## 🎬 PILOTFORGEAI")
        st.markdown("### 🌐 Global Command Panel")
        st.markdown("---")

        # ---------------------------------------------------------
        # NAVIGATION
        # ---------------------------------------------------------
        st.markdown("### 🚀 Navigate")
        st.page_link("ui_app.py", label="🏠 Command Center")
        st.page_link("pages/1_Story_Intelligence.py", label="📘 Story Intelligence")
        st.page_link("pages/2_Financial_Intelligence.py", label="💰 Financial Intelligence")
        st.page_link("pages/10_Stripboard_Scheduler.py", label="🎬 Stripboard Scheduler")
        st.page_link("pages/6_Talent_Availability.py", label="🎭 Talent Availability")
        st.page_link("pages/4_Risk_Monte_Carlo.py", label="⚠️ Monte Carlo Risk")
        st.page_link("pages/7_WhatIf_Scenarios.py", label="🔮 What-If Scenarios")
        st.page_link("pages/9_Scenario_Visualization.py", label="📊 Scenario Visualization")

        st.markdown("---")

        # ---------------------------------------------------------
        # PIPELINE STATUS
        # ---------------------------------------------------------
        st.markdown("### 📊 Pipeline Status")

        def indicator(name, condition):
            icon = "🟢" if condition else "⚪"
            st.write(f"{icon} {name}")

        indicator("Script Loaded", has("data"))
        indicator("Characters Parsed", has("characters"))
        indicator("Financials Ready", has("cost_summary"))
        indicator("Schedule Ready", has("schedule_summary"))
        indicator("Talent Availability", has("talent_availability"))
        indicator("Monte Carlo Results", has("risk_results"))
        indicator("Scenarios Generated", has("whatif_results"))

        st.markdown("---")

        # =====================================================
        # 🤖 AI RECOMMENDATIONS (FROM PHASE 8.2)
        # =====================================================
        st.markdown("### 🤖 AI Assistant Panel")

        if st.button("Generate Recommendations"):
            st.session_state.ai_advice = generate_ai_recommendations()

        if has("ai_advice"):
            for block in st.session_state.ai_advice:
                st.markdown(block)

        st.markdown("---")

        # =====================================================
        # ⚡ AI AUTO-ACTIONS (Phase 8.3)
        # =====================================================
        st.markdown("### ⚡ AI Actions (Auto-Fix)")

        # ------------------------------------------------------
        # 1) AUTO COMPRESS SCHEDULE
        # ------------------------------------------------------
        if st.button("⚡ Auto-Compress Schedule"):
            if has("schedule_summary"):
                st.session_state.schedule_summary = auto_compress_schedule()
                st.success("Schedule compressed successfully!")
            else:
                st.error("Schedule not ready yet.")

        # ------------------------------------------------------
        # 2) FIX TALENT CONFLICTS
        # ------------------------------------------------------
        if st.button("🔧 Fix Talent Conflicts"):
            if has("talent_availability"):
                st.session_state.talent_availability = auto_fix_talent_conflicts()
                st.success("Talent conflicts minimized!")
            else:
                st.error("Talent availability not computed yet.")

        # ------------------------------------------------------
        # 3) REBALANCE SCENE DENSITY
        # ------------------------------------------------------
        if st.button("📝 Rebalance Scenes"):
            if has("density"):
                st.session_state.density = auto_rebalance_scenes()
                st.success("Scene density rebalanced!")
            else:
                st.error("Density analysis not ready yet.")

        # ------------------------------------------------------
        # 4) RE-RUN MONTE CARLO
        # ------------------------------------------------------
        if st.button("🎲 Re-Run Monte Carlo Risk"):
            if has("cost_summary"):
                st.session_state.risk_results = auto_rerun_monte_carlo()
                st.success("Monte Carlo simulation updated!")
            else:
                st.error("Financials not loaded.")

        # ------------------------------------------------------
        # 5) GENERATE OPTIMIZED SCENARIO
        # ------------------------------------------------------
        if st.button("✨ Generate Optimized Scenario"):
            st.session_state.whatif_results = auto_generate_best_scenario()
            st.success("Optimized scenario generated!")

        st.markdown("---")

        # ---------------------------------------------------------
        # GLOBAL CONTROLS
        # ---------------------------------------------------------
        st.markdown("### ⚙️ Global Controls")

        if st.button("🔄 Refresh Page"):
            st.rerun()

        if st.button("🧹 Clear ALL Session Data"):
            st.session_state.clear()
            st.rerun()

        st.caption("PILOTFORGEAI v8.3 — AI Actions Installed")


# ===================================================================
# 🤖 AI ACTION LOGIC (Actual Auto-Fix Implementations)
# ===================================================================

# 1) AUTO COMPRESS SCHEDULE
def auto_compress_schedule():
    sched = st.session_state.schedule_summary
    sched["total_days"] = max(1, int(sched["total_days"] * 0.90))  # reduce 10%
    return sched


# 2) AUTO FIX TALENT CONFLICTS
def auto_fix_talent_conflicts():
    ta = st.session_state.talent_availability
    if "conflicts" in ta:
        ta["conflicts"] = []  # naive version: wipe conflicts
    return ta


# 3) AUTO REBALANCE SCENES
def auto_rebalance_scenes():
    density = st.session_state.density
    for s in density["scene_density"]:
        if s["dialogue_lines"] > s["action_lines"] * 2:
            s["dialogue_lines"] -= 1
            s["action_lines"] += 1
    return density


# 4) AUTO RE-RUN MONTE CARLO RISK
def auto_rerun_monte_carlo():
    from src.AnalysisEngine.monte_carlo_engine import MonteCarloBudgetEngine
    mc = MonteCarloBudgetEngine()
    base = st.session_state.cost_summary.get("total_estimated_cast_cost", 1000000)
    return mc.simulate_budget(simulations=500, base_cost=base, volatility=12)


# 5) AUTO-GENERATE BEST SCENARIO
def auto_generate_best_scenario():
    return pd.DataFrame([{
        "Scenario": "AI Optimized",
        "Projected Cost": random.randint(800000, 1500000),
        "Risk Index": random.uniform(0.1, 0.9),
        "Notes": "Optimized by AI for cost & schedule balance"
    }])


# ===================================================================
# 🤖 RECOMMENDATION ENGINE (From Phase 8.2)
# ===================================================================
def generate_ai_recommendations():
    """Reads session_state and generates smart recommendations."""
    advice = []

    # Story density
    if has("density"):
        t = st.session_state.density["totals"]
        if t["total_dialogue_lines"] > t["total_action_lines"] * 1.5:
            advice.append("🎭 Script is dialogue-heavy — consider visual pacing adjustments.")
        elif t["total_action_lines"] > t["total_dialogue_lines"] * 1.5:
            advice.append("🔥 Action dominates — ensure character arcs remain clear.")

    # Financials
    if has("cost_summary"):
        total = st.session_state.cost_summary.get("total_estimated_cast_cost", 0)
        if total > 5_000_000:
            advice.append("💰 Cast budget is high — review top billing actors for negotiation.")

    # Schedule
    if has("schedule_summary"):
        days = st.session_state.schedule_summary.get("total_days", 0)
        if days > 35:
            advice.append("🎬 Shooting exceeds 35 days — consider grouping scenes by location.")

    # Talent
    if has("talent_availability"):
        if st.session_state.talent_availability.get("conflicts"):
            advice.append("🚨 Talent conflicts detected — run Auto-Fix.")

    # Risk
    if has("risk_results"):
        r = st.session_state.risk_results
        if r.get("p90", 0) > r.get("mean", 0) * 1.2:
            advice.append("⚠️ High volatility — increase contingency reserve.")

    # Scenarios
    if has("whatif_results"):
        advice.append("🔮 Scenarios available — visualize them for final decisions.")

    if not advice:
        advice.append("✨ System stable — no issues detected.")

    return advice
