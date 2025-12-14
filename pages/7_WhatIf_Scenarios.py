import streamlit as st
import pandas as pd
from src.ui.global_sidebar import install_global_sidebar
install_global_sidebar()

from src.AnalysisEngine.cost_impact_engine import CharacterCostImpactEngine
from src.AnalysisEngine.monte_carlo_engine import MonteCarloBudgetEngine

st.set_page_config(page_title="What-If Scenario Forecasting", layout="wide")
st.title("🔮 Phase 7 — What-If Scenario Intelligence")


# -----------------------------------------------------
# SAFETY CHECKS
# -----------------------------------------------------
if "data" not in st.session_state or "cost" not in st.session_state:
    st.warning("⚠️ Run Story, Financial, and Budget phases first.")
    st.stop()

character_costs = st.session_state.cost.get("character_costs", {}) if st.session_state.cost else {}


# -----------------------------------------------------
# UTIL: SAFE NUMBER CLEANER
# -----------------------------------------------------
def to_number(val):
    """Convert strings/floats like '$12,400' → 12400.0 safely."""
    if val is None:
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    return float(str(val).replace("$", "").replace(",", "").strip())


# -----------------------------------------------------
# ENGINE SETUP
# -----------------------------------------------------
impact_engine = CharacterCostImpactEngine()
mc = MonteCarloBudgetEngine()


# -----------------------------------------------------
# SIDEBAR OPTIONS
# -----------------------------------------------------
st.sidebar.subheader("Scenario Configuration")

scenario_mode = st.sidebar.radio(
    "Scenario Type",
    [
        "Manual Scenario Input",
        "Preset Scenarios",
        "AI-Designed Scenarios (Auto-Generate)"
    ]
)

num_scenarios = st.sidebar.slider(
    "Number of Scenarios", 1, 10, 3
)

simulation_runs = st.sidebar.slider(
    "Monte Carlo Simulations per Scenario",
    200, 3000, 1000, step=100
)

volatility = st.sidebar.slider(
    "Budget Volatility (%)",
    1, 40, 12
)


# -----------------------------------------------------
# BUILD SCENARIOS
# -----------------------------------------------------
def generate_ai_scenarios(n):
    """AI-like auto-generated scenario definitions."""
    base_chars = list(character_costs.keys())[:3]
    scenarios = []

    for i in range(n):
        adjustments = {}
        for c in base_chars:
            adjustments[c] = {
                "increase_cast": (i + 1) * 5,  # % bump
                "reduce_days": (i % 2) * 1,    # toggle
            }
        scenarios.append({
            "name": f"AI Scenario {i+1}",
            "adjustments": adjustments
        })

    return scenarios


# MANUAL input mode
manual_inputs = []

if scenario_mode == "Manual Scenario Input":
    st.subheader("✏️ Manual Scenario Builder")

    for i in range(num_scenarios):
        with st.expander(f"Scenario {i+1} Options", expanded=(i==0)):
            name = st.text_input(f"Scenario {i+1} Name", f"Scenario {i+1}")

            percent_change = st.number_input(
                f"Cast Cost Adjustment % for Scenario {i+1}",
                -50.0, 100.0, 10.0
            )

            manual_inputs.append({
                "name": name,
                "percent": percent_change
            })

elif scenario_mode == "Preset Scenarios":
    st.subheader("🎛 Using Preset Scenarios")
    manual_inputs = [
        {"name": "Low Cost Variant", "percent": -10},
        {"name": "High Cost Pressure", "percent": 15},
        {"name": "Extreme Overrun", "percent": 30},
    ][:num_scenarios]

else:
    st.subheader("🤖 AI-Designed Auto Scenarios")
    auto = generate_ai_scenarios(num_scenarios)
    manual_inputs = [
        {"name": s["name"], "percent": (idx+1) * 5}
        for idx, s in enumerate(auto)
    ]


# -----------------------------------------------------
# RUN SIMULATIONS
# -----------------------------------------------------
st.divider()
st.subheader("📊 Scenario Results")

    base_cast_total = st.session_state.cost.get("total_estimated_cast_cost", 0.0) if st.session_state.cost else 0.0

results_for_table = []

for s in manual_inputs:
    adj_cost = base_cast_total * (1 + (s["percent"] / 100.0))

    sim = mc.simulate_budget(
        simulations=simulation_runs,
        base_cost=adj_cost,
        volatility=volatility
    )

    results_for_table.append({
        "Scenario": s["name"],
        "Mean": sim["mean"],
        "P10": sim["p10"],
        "P90": sim["p90"],
    })


# -----------------------------------------------------
# DISPLAY TABLE
# -----------------------------------------------------
df = pd.DataFrame(results_for_table)

# Format for user view
show_df = df.copy()
show_df["Mean"] = show_df["Mean"].apply(lambda v: f"${v:,.0f}")
show_df["P10"] = show_df["P10"].apply(lambda v: f"${v:,.0f}")
show_df["P90"] = show_df["P90"].apply(lambda v: f"${v:,.0f}")

st.dataframe(show_df, use_container_width=True)


# -----------------------------------------------------
# SAVE TO SESSION STATE FOR OTHER PAGES (Phase 7.2 / 7.3)
# -----------------------------------------------------
st.session_state["whatif_results"] = df

st.success("✅ What-If Scenarios computed and saved for visualization & comparison.")

