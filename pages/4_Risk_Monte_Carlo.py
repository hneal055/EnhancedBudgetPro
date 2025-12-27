import streamlit as st
import pandas as pd
from src.ui.global_sidebar import install_global_sidebar
install_global_sidebar()

from src.AnalysisEngine.risk_analysis_engine import ScriptRiskAnalysisEngine
from src.AnalysisEngine.monte_carlo_engine import MonteCarloBudgetEngine

st.title("⚠️ Phase 4C — Risk & Monte Carlo")

if not (
    st.session_state.get("data")
    and st.session_state.get("density")
    and st.session_state.get("cost")
):
    st.warning("⚠️ Please run Pages 1 and 2 (Story + Financial Intelligence) first.")
    st.stop()

data = st.session_state.data
density = st.session_state.density
cost = st.session_state.cost

# ---------------------------------------------
# RISK ANALYSIS
# ---------------------------------------------
st.subheader("🎯 Scene Risk Profiles")

risk_engine = ScriptRiskAnalysisEngine()
risk = risk_engine.analyze(
    data["scenes"],
    density["scene_density"],
    cost["character_costs"],
)
st.session_state.risk = risk

risk_rows = []
for r in risk["scene_risk_profiles"]:
    risk_rows.append(
        {
            "Scene": r["scene"],
            "Characters": ", ".join(r["characters"]),
            "Risk Score": round(r["risk_score"], 2),
            "Risk Class": r["risk_classification"],
            "Scene Cost": f"${r['scene_cost']:,.2f}",
        }
    )

if risk_rows:
    st.dataframe(pd.DataFrame(risk_rows), width="stretch")

st.metric("🚨 High-Risk Scenes", risk.get("high_risk_scene_count", 0))

# ---------------------------------------------
# MONTE CARLO BUDGET VOLATILITY
# ---------------------------------------------
st.subheader("🎲 Monte Carlo Budget Forecast")

base_cost = cost.get("total_estimated_cast_cost", 0.0)

col1, col2 = st.columns(2)
simulations = col1.slider("Simulation Runs", 100, 5000, 1000, step=100)
volatility = col2.slider("Cost Volatility (±%)", 1, 50, 10)

mc = MonteCarloBudgetEngine()
results = mc.simulate_budget(simulations, base_cost, volatility)

st.write(f"**Base Cast Cost:** ${base_cost:,.2f}")
st.write(f"**Mean Simulated Cost:** ${results['mean']:,.2f}")
st.write(
    f"**10th Percentile:** ${results['p10']:,.2f}  |  "
    f"**90th Percentile:** ${results['p90']:,.2f}"
)

# Show sample of simulation distribution
sample = results["simulations"][:50]
df_sample = pd.DataFrame({"Run #": list(range(1, len(sample) + 1)), "Cost": sample})
st.dataframe(df_sample, width="stretch")

# ---------------------------------------------
# EMOTION ANALYSIS (UNDER CONSTRUCTION)
# ---------------------------------------------
st.title("Emotion Analysis")

if "data" not in st.session_state:
    st.warning("Please upload and analyze a script first.")
    st.stop()

st.info("This page is under construction. Core logic coming soon.")
