import streamlit as st
import pandas as pd
from src.components.sidebar import render_sidebar
render_sidebar()
from src.ui.global_sidebar import install_global_sidebar
install_global_sidebar()

from src.AnalysisEngine.monte_carlo_engine import MonteCarloBudgetEngine
from src.AnalysisEngine.cost_impact_engine import CharacterCostImpactEngine
from src.SchedulingEngine.production_scheduler import ProductionSchedulerEngine


st.set_page_config(page_title="Scenario Comparison", layout="wide")
st.title("📊 Phase 7.2 — Scenario Comparison Dashboard")


# ------------------------------------------------------
# PREREQUISITES
# ------------------------------------------------------
if not st.session_state.get("data") or not st.session_state.get("cost"):
    st.warning("⚠️ Run script + financial analysis first.")
    st.stop()


base_costs = st.session_state.cost["total_estimated_cast_cost"]
characters = list(st.session_state.cost["character_costs"].keys())


# ------------------------------------------------------
# UI LAYOUT
# ------------------------------------------------------
left, right = st.columns([2, 1])

with left:
    st.header("🎬 Define Scenarios to Compare")

    scenario_count = st.number_input(
        "How many scenarios do you want to compare?",
        min_value=2,
        max_value=6,
        value=3,
        step=1
    )

    scenario_inputs = []

    for i in range(scenario_count):
        st.subheader(f"Scenario {i+1}")

        col1, col2, col3 = st.columns(3)

        name = col1.text_input(f"Name for Scenario {i+1}", f"Scenario {i+1}")
        
        volatility = col2.slider(
            f"Volatility % (Scenario {i+1})",
            min_value=1,
            max_value=50,
            value=10
        )

        cast_multiplier = col3.slider(
            f"Cast Cost Multiplier (Scenario {i+1})",
            min_value=0.5,
            max_value=2.0,
            value=1.0
        )

        scenario_inputs.append({
            "name": name,
            "volatility": volatility,
            "cast_multiplier": cast_multiplier
        })


with right:
    st.header("⚙️ Simulation Settings")

    simulation_runs = st.number_input(
        "Simulation Runs",
        min_value=200,
        max_value=5000,
        value=1000
    )

    run_button = st.button("🚀 Run Scenario Comparison")


# ------------------------------------------------------
# RUN ENGINE
# ------------------------------------------------------
if run_button:

    mc = MonteCarloBudgetEngine()
    results = []

    for scenario in scenario_inputs:

        adjusted_cost = base_costs * scenario["cast_multiplier"]

        mc_out = mc.simulate_budget(
            simulations=simulation_runs,
            base_cost=adjusted_cost,
            volatility=scenario["volatility"]
        )

        results.append({
            "name": scenario["name"],
            "mean": mc_out["mean"],
            "p10": mc_out["p10"],
            "p90": mc_out["p90"],
            "volatility": scenario["volatility"],
            "adjusted_cast_cost": adjusted_cost
        })

    st.success("Comparison complete!")


    # ------------------------------------------------------
    # TABLE OUTPUT
    # ------------------------------------------------------
    st.header("📊 Scenario Summary Table")

    df = pd.DataFrame(results)
    st.dataframe(df, width="stretch")



    # ------------------------------------------------------
    # COMPARISON METRICS
    # ------------------------------------------------------
    st.header("📉 Risk Spread & Budget Pressure")

    for item in results:
        st.subheader(item["name"])

        st.write(f"**Mean:** ${item['mean']:,.2f}")
        st.write(f"**10th Percentile (safe):** ${item['p10']:,.2f}")
        st.write(f"**90th Percentile (danger):** ${item['p90']:,.2f}")

        spread = item["p90"] - item["p10"]
        st.metric("Risk Spread", f"${spread:,.0f}")


    # ------------------------------------------------------
    # BEST / WORST PICKER
    # ------------------------------------------------------
    st.header("🏆 Recommendations")

    best = min(results, key=lambda x: x["mean"])
    worst = max(results, key=lambda x: x["p90"])

    st.success(f"⭐ Best Overall Scenario: **{best['name']}** — Lowest mean cost")
    st.error(f"⚠️ Highest-Risk Scenario: **{worst['name']}** — Largest 90th percentile")


