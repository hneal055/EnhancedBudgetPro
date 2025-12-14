import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from src.ui.global_sidebar import install_global_sidebar
install_global_sidebar()

st.set_page_config(page_title="Scenario Visualization", layout="wide")
st.title("📊 Phase 7.3 — Scenario Visualization Suite")

# -------------------------------------------------------------
# Safety Check: Requires What-If Results
# -------------------------------------------------------------
if "whatif_results" not in st.session_state:
    st.warning("⚠️ No scenarios available. Run Phase 7.1 What-If Scenarios first.")
    st.stop()

results = st.session_state.whatif_results

# DataFrame check (fixing ambiguous truth error)
if isinstance(results, pd.DataFrame):
    if results.empty:
        st.warning("⚠️ Scenario results are empty. Run Phase 7.1 first.")
        st.stop()
else:
    # results may be a list of dicts
    if not results:
        st.warning("⚠️ No scenario data found.")
        st.stop()
    results = pd.DataFrame(results)

df = results.copy()

# -------------------------------------------------------------
# Normalize currency fields → numeric values
# -------------------------------------------------------------
def clean_money(x):
    if isinstance(x, (float, int)):
        return float(x)
    if isinstance(x, str):
        x = x.replace("$", "").replace(",", "")
        try:
            return float(x)
        except:
            return None
    return None

for c in ["Mean", "P10", "P90", "Shift_Days"]:
    if c in df.columns:
        df[c] = df[c].apply(clean_money)

# -------------------------------------------------------------
# Validate Required Columns
# -------------------------------------------------------------
required_cols = ["Mean", "P10", "P90"]
missing_cols = [c for c in required_cols if c not in df.columns]
if missing_cols:
    st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
    st.info("💡 Tip: Go to Phase 7.1 (What-If Scenarios) and run Monte Carlo simulations first.")
    st.stop()

# -------------------------------------------------------------
# Scenario Ranking Score (Mean + Risk Spread)
# -------------------------------------------------------------
df["Risk_Spread"] = df["P90"] - df["P10"]
df["Score"] = df["Mean"] + (0.5 * df["Risk_Spread"])

df = df.sort_values("Score")

st.subheader("🏆 Scenario Ranking Overview")
st.dataframe(df, width="stretch")

# -------------------------------------------------------------
# Enhanced Visualization — Cost & Risk Bar Chart
# -------------------------------------------------------------
st.subheader("📘 Scenario Cost Comparison (Mean vs P10–P90 Range)")

fig = go.Figure()

for _, row in df.iterrows():
    scenario = row["Scenario"]
    mean = row["Mean"]
    p10 = row["P10"]
    p90 = row["P90"]

    fig.add_trace(
        go.Bar(
            x=[p90 - p10],
            y=[scenario],
            base=p10,
            orientation="h",
            name="Risk Range",
            marker=dict(color="rgba(255,165,0,0.4)"),
            hovertemplate=f"<b>{scenario}</b><br>P10: ${p10:,.0f}<br>P90: ${p90:,.0f}<extra></extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[mean],
            y=[scenario],
            mode="markers",
            marker=dict(size=14, color="red"),
            name="Mean",
            hovertemplate=f"<b>{scenario}</b><br>Mean: ${mean:,.0f}<extra></extra>",
        )
    )

fig.update_layout(
    height=500,
    barmode="overlay",
    xaxis_title="Cost (USD)",
    yaxis_title="Scenario",
    title="Mean Cost + P10–P90 Risk Range",
)

st.plotly_chart(fig, width="stretch")

# -------------------------------------------------------------
# Scenario Funnel (Uncertainty)
# -------------------------------------------------------------
st.subheader("🔻 Scenario Uncertainty Funnel")

funnel_fig = go.Figure()

for _, row in df.iterrows():
    funnel_fig.add_trace(
        go.Scatter(
            x=[row["P10"], row["Mean"], row["P90"]],
            y=[row["Scenario"]] * 3,
            mode="lines+markers",
            line=dict(color="blue"),
            marker=dict(size=10),
        )
    )

funnel_fig.update_layout(
    height=400,
    xaxis_title="Cost Range (USD)",
    title="Cost Uncertainty Funnel",
)

st.plotly_chart(funnel_fig, width="stretch")

# -------------------------------------------------------------
# Gradient Cost Meter
# -------------------------------------------------------------
st.subheader("🌡 Scenario Cost Gradient Meter")

gradient_fig = px.scatter(
    df,
    x="Scenario",
    y="Mean",
    size="Risk_Spread",
    color="Mean",
    color_continuous_scale="RdYlGn_r",
    hover_data=["P10", "P90", "Risk_Spread"],
    title="Mean Cost Gradient (Bubble size = risk spread)",
)

st.plotly_chart(gradient_fig, width="stretch")
