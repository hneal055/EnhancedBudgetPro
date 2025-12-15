import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Scenario Comparison Dashboard", layout="wide")
st.title("📊 Scenario Comparison Dashboard")

# Load scenarios from session state (AI, custom, imported)
scenarios = st.session_state.get("scenario_results", {})
if not scenarios:
    st.warning("No scenarios found. Please generate or import scenarios first.")
    st.stop()

# Allow user to select scenarios to compare
scenario_names = list(scenarios.keys())
selected = st.multiselect("Select scenarios to compare:", scenario_names, default=scenario_names)

if not selected:
    st.info("Select at least one scenario to compare.")
    st.stop()

# Build comparison table
rows = []
for name in selected:
    s = scenarios[name]
    rows.append({
        "Scenario": name,
        "Cast Cost": s["new_cast_total"],
        "Shoot Days": s["compressed_days"],
        "Volatility": s["config"].get("volatility", 0),
        "MC Mean Cost": s["mc"]["mean"],
        "MC P95 Cost": s["mc"]["p90"],
    })
compare_df = pd.DataFrame(rows)

st.subheader("Comparison Table")
st.dataframe(compare_df, width="stretch")

# Bar chart: Cast Cost
fig1 = px.bar(compare_df, x="Scenario", y="Cast Cost", title="Cast Cost by Scenario")
st.plotly_chart(fig1, use_container_width=True)

# Bar chart: Shoot Days
fig2 = px.bar(compare_df, x="Scenario", y="Shoot Days", title="Shoot Days by Scenario")
st.plotly_chart(fig2, use_container_width=True)

# Line chart: MC Mean and P95 Cost
fig3 = px.line(compare_df, x="Scenario", y=["MC Mean Cost", "MC P95 Cost"], title="Monte Carlo Cost Comparison")
st.plotly_chart(fig3, use_container_width=True)
