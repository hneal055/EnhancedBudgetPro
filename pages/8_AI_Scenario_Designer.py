import streamlit as st
import pandas as pd
from src.ui.global_sidebar import install_global_sidebar
install_global_sidebar()

from src.SchedulingEngine.production_scheduler import ProductionSchedulerEngine
from src.AnalysisEngine.cost_impact_engine import CharacterCostImpactEngine
from src.AnalysisEngine.monte_carlo_engine import MonteCarloBudgetEngine

st.set_page_config(page_title="AI Scenario Designer", layout="wide")
st.title("🤖 Phase 7.2 — AI Scenario Designer (What-If Generator)")

# -----------------------------------------------------
# SAFETY CHECKS — we need the core intelligence online
# -----------------------------------------------------
data = st.session_state.get("data")
intel = st.session_state.get("intel")
cost = st.session_state.get("cost")
master = st.session_state.get("master")

if not data or not intel or not cost or not master:
    st.warning("⚠️ Run Story Intelligence + Financial Intelligence + Master Budget first.")
    st.stop()

baseline_cast_cost = cost["total_estimated_cast_cost"]
baseline_master_budget = master.get("final_production_budget", 0)
baseline_scenes = len(data["scenes"])

st.subheader("🎬 Baseline Production Snapshot")

colA, colB, colC = st.columns(3)
colA.metric("Total Scenes", baseline_scenes)
colB.metric("Baseline Cast Cost", f"${baseline_cast_cost:,.2f}")
colC.metric("Final Studio Budget", f"${baseline_master_budget:,.2f}")

st.divider()

# -----------------------------------------------------
# AI SCENARIO BLUEPRINTS
# -----------------------------------------------------
st.subheader("🤖 Auto-Generated Scenarios")

st.markdown(
    """
We’ll generate **three smart scenarios** based on your current show:

- 🟢 **Cheapest** – reduce day rates, keep schedule reasonable  
- 🔵 **Fastest** – compress schedule aggressively, accept more volatility  
- 🟣 **Balanced** – moderate savings + lighter compression + lower risk  
    """
)

scenario_configs = {
    "Cheapest": {
        "description": "Minimize above-the-line + cast cost with gentle schedule stretch.",
        "rate_factor": 0.80,       # 20% cheaper cast
        "compression_factor": 1.05,  # tiny stretch, not faster
        "volatility": 0.02,
    },
    "Fastest": {
        "description": "Crush the schedule; accept higher risk / overtime.",
        "rate_factor": 1.05,       # slightly more expensive cast (overtime, premiums)
        "compression_factor": 0.70,  # 30% faster schedule
        "volatility": 0.05,        # more cost uncertainty
    },
    "Balanced": {
        "description": "Blend cost savings and schedule compression.",
        "rate_factor": 0.95,       # light savings
        "compression_factor": 0.85, # ~15% faster schedule
        "volatility": 0.03,
    },
}

# -----------------------------------------------------
# CUSTOM SCENARIO CREATION UI
# -----------------------------------------------------
st.subheader("➕ Create a Custom Scenario")

with st.form("custom_scenario_form"):
    custom_name = st.text_input("Scenario Name", "Custom")
    custom_rate = st.number_input("Cast Rate Factor (e.g. 0.8 = 20% cheaper)", min_value=0.1, max_value=2.0, value=1.0, step=0.01)
    custom_compression = st.number_input("Schedule Compression Factor (e.g. 0.7 = 30% faster)", min_value=0.1, max_value=2.0, value=1.0, step=0.01)
    custom_volatility = st.number_input("Volatility (0.01 = low, 0.10 = high)", min_value=0.0, max_value=1.0, value=0.02, step=0.01)
    submitted = st.form_submit_button("Add Custom Scenario")

if submitted and custom_name:
    scenario_configs[custom_name] = {
        "description": "User-defined custom scenario.",
        "rate_factor": custom_rate,
        "compression_factor": custom_compression,
        "volatility": custom_volatility,
    }
    st.success(f"Custom scenario '{custom_name}' added!")

scheduler = ProductionSchedulerEngine()
mc_engine = MonteCarloBudgetEngine()

scenario_results = {}

# -----------------------------------------------------
# CORE ENGINE: build all scenarios
# -----------------------------------------------------
for name, cfg in scenario_configs.items():
    rate_factor = cfg["rate_factor"]
    compression_factor = cfg["compression_factor"]
    volatility = cfg["volatility"]

    # 1) Adjust character rates
    new_rates = {}
    for char_name, info in cost["character_costs"].items():
        new_rates[char_name] = info["daily_rate"] * rate_factor

    temp_cost_engine = CharacterCostImpactEngine()
    updated_costs = temp_cost_engine.analyze(
        intel["character_stats"],
        new_rates,
        data["scene_count"],
    )
    new_cast_total = updated_costs["total_estimated_cast_cost"]

    # 2) Rebuild schedule with updated costs
    base_schedule = scheduler.generate_schedule(
        data["scenes"],
        updated_costs["character_costs"],
    )["daily_schedule"]

    original_days = len(base_schedule)
    compressed_days = max(1, int(original_days * compression_factor))

    # For simplicity, we just truncate / compress the list;
    # later you could add smarter packing logic.
    compressed_schedule = base_schedule[:compressed_days]

    # 3) Monte Carlo simulation on new cast total
    mc_results = mc_engine.simulate_budget(
        simulations=400,
        base_cost=new_cast_total,
        volatility=volatility,
    )

    scenario_results[name] = {
        "config": cfg,
        "new_cast_total": new_cast_total,
        "schedule": compressed_schedule,
        "original_days": original_days,
        "compressed_days": compressed_days,
        "mc": mc_results,
    }

# -----------------------------------------------------
# EXPORT/IMPORT CONTROLS
# -----------------------------------------------------
from src.utils.scenario_io import export_scenarios_to_json, import_scenarios_from_json
import tempfile
import os

# --- Export Button ---
if st.button("Export Scenarios (JSON)"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
        export_scenarios_to_json(scenario_results, tmp.name)
        with open(tmp.name, "rb") as f:
            st.download_button(
                label="Download Scenarios JSON",
                data=f,
                file_name="scenarios_export.json",
                mime="application/json"
            )
        os.unlink(tmp.name)

# --- Import Button ---
uploaded_file = st.file_uploader("Import Scenarios (JSON)", type=["json"])
if uploaded_file is not None:
    imported_scenarios = import_scenarios_from_json(uploaded_file)
    st.session_state["scenario_results"] = imported_scenarios
    st.success("Scenarios imported! Refresh the page to use them.")

# Use imported scenarios if present
scenario_results = st.session_state.get("scenario_results", scenario_results)

# -----------------------------------------------------
# SCENARIO COMPARISON TABLE
# -----------------------------------------------------
rows = []
for name, result in scenario_results.items():
    rows.append({
        "Scenario": name,
        "Description": result["config"]["description"],
        "Cast Cost": result["new_cast_total"],
        "Δ Cast vs Baseline": result["new_cast_total"] - baseline_cast_cost,
        "Shoot Days": result["compressed_days"],
        "Δ Days vs Original": result["compressed_days"] - baseline_scenes,
        "MC Mean Cost": result["mc"]["mean"],
        "MC P95 Cost": result["mc"]["p90"],
    })

compare_df = pd.DataFrame(rows)
compare_df["Cast Cost"] = compare_df["Cast Cost"].map(lambda x: f"${x:,.0f}")
compare_df["Δ Cast vs Baseline"] = compare_df["Δ Cast vs Baseline"].map(lambda x: f"${x:,.0f}")
compare_df["MC Mean Cost"] = compare_df["MC Mean Cost"].map(lambda x: f"${x:,.0f}")
compare_df["MC P95 Cost"] = compare_df["MC P95 Cost"].map(lambda x: f"${x:,.0f}")

st.subheader("📊 Scenario Comparison Overview")
st.dataframe(compare_df, width="stretch")

st.divider()

# -----------------------------------------------------
# FOCUSED VIEW: pick one scenario to inspect
# -----------------------------------------------------
st.subheader("🔍 Inspect a Scenario in Detail")

selected_name = st.selectbox(
    "Choose a scenario to inspect:",
    list(scenario_results.keys()),
)

selected = scenario_results[selected_name]
mc = selected["mc"]

col1, col2, col3 = st.columns(3)
col1.metric(
    f"{selected_name} Cast Cost",
    f"${selected['new_cast_total']:,.0f}",
    delta=f"${selected['new_cast_total'] - baseline_cast_cost:,.0f}",
)
col2.metric(
    "Shoot Days",
    selected["compressed_days"],
    delta=selected["compressed_days"] - baseline_scenes,
)
col3.metric(
    "MC Mean Cost",
    f"${mc['mean']:,.0f}",
    delta=f"${mc['mean'] - baseline_cast_cost:,.0f}",
)

st.markdown(f"**Scenario description:** {selected['config']['description']}")

st.subheader("�� Monte Carlo Distribution (Sample)")
st.line_chart(mc["distribution_samples"])

st.subheader("📅 Compressed Schedule Preview")
schedule_df = pd.DataFrame(selected["schedule"])
st.dataframe(schedule_df, width="stretch")

st.info(
    "These scenarios are *suggestions* — you can treat them as starting points "
    "for negotiations, re-writing, or schedule redesign."
)

st.title("Equipment Budget")

if "data" not in st.session_state:
    st.warning("Please upload and analyze a script first.")
    st.stop()

st.info("This page is under construction. Core logic coming soon.")
