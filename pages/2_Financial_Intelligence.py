import streamlit as st
import pandas as pd
from src.ui.global_sidebar import install_global_sidebar
install_global_sidebar()

from src.AnalysisEngine.cost_impact_engine import CharacterCostImpactEngine
from src.AnalysisEngine.burn_rate_engine import BurnRateForecastEngine

st.title("Financial Intelligence")

if "data" not in st.session_state:
    st.warning("Please upload and analyze a script first.")
    st.stop()

st.info("This page is under construction. Core logic coming soon.")

# ---------------------------------------------
# PRECHECK
# ---------------------------------------------
if not st.session_state.get("data") or not st.session_state.get("intel"):
    st.warning("⚠️ Please run **Story Intelligence** (Page 1) first.")
    st.stop()

data = st.session_state.data
intel = st.session_state.intel

# ---------------------------------------------
# CHARACTER RATES
# ---------------------------------------------
st.subheader("🎭 Character Day Rates")

default_rates = {
    name: 1000 for name in intel["character_stats"].keys()
}

rate_inputs = {}
for char, rate in default_rates.items():
    rate_inputs[char] = st.number_input(
        f"{char} Daily Rate ($)",
        min_value=100,
        max_value=50000,
        value=rate,
        step=100,
        key=f"rate_{char}",
    )

# ---------------------------------------------
# COST IMPACT + BURN RATE
# ---------------------------------------------
cost_engine = CharacterCostImpactEngine()
cost = cost_engine.analyze(
    intel["character_stats"],
    rate_inputs,
    data["scene_count"],
)
st.session_state.cost = cost

burn_engine = BurnRateForecastEngine()
burn = burn_engine.analyze(
    data["scenes"],
    cost["character_costs"],
)
st.session_state.burn = burn

st.subheader("💵 Character Cost Impact")

cost_rows = []
for char, info in cost["character_costs"].items():
    cost_rows.append(
        {
            "Character": char,
            "Daily Rate": info["daily_rate"],
            "Est. Days": info["estimated_days"],
            "Total Cost": info["estimated_total_cost"],
        }
    )

if cost_rows:
    df_cost = pd.DataFrame(cost_rows)
    df_cost["Daily Rate"] = df_cost["Daily Rate"].map(lambda x: f"${x:,.2f}")
    df_cost["Total Cost"] = df_cost["Total Cost"].map(lambda x: f"${x:,.2f}")
    st.dataframe(df_cost, width="stretch")

st.metric(
    "🎯 Total Estimated Cast Cost",
    f"${cost['total_estimated_cast_cost']:,.2f}",
)

st.subheader("🔥 Daily Burn Schedule")

burn_rows = []
for day in burn["daily_schedule"]:
    burn_rows.append(
        {
            "Shoot Day": day["shoot_day"],
            "Scene": day["scene"],
            "Characters": ", ".join(day["characters"]),
            "Daily Burn ($)": day["daily_burn"],
        }
    )

if burn_rows:
    df_burn = pd.DataFrame(burn_rows)
    df_burn["Daily Burn ($)"] = df_burn["Daily Burn ($)"].map(
        lambda x: f"${x:,.2f}"
    )
    st.dataframe(df_burn, width="stretch")

colX, colY = st.columns(2)
colX.metric(
    "📈 Average Daily Burn",
    f"${burn['average_daily_burn']:,.2f}",
)
colY.metric(
    "🚨 Peak Burn Day",
    f"Day {burn['peak_burn_day']['day']} — ${burn['peak_burn_day']['cost']:,.2f}",
)
