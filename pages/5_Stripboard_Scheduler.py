import streamlit as st
import pandas as pd
from src.ui.global_sidebar import install_global_sidebar
install_global_sidebar()

from src.SchedulingEngine.production_scheduler import ProductionSchedulerEngine

st.title("🎞 Phase 5 — Scheduling & Stripboard")

if not (st.session_state.get("data") and st.session_state.get("cost")):
    st.warning("⚠️ Please run Pages 1–2 (Story + Financial) first.")
    st.stop()

data = st.session_state.data
cost = st.session_state.cost

scheduler = ProductionSchedulerEngine()
schedule = scheduler.generate_schedule(
    data["scenes"],
    cost["character_costs"],
)

st.session_state.schedule = schedule

daily_schedule = schedule.get("daily_schedule", [])

st.subheader("📅 Shooting Stripboard")

if not daily_schedule:
    st.info("No schedule data generated.")
else:
    # Filter controls
    all_chars = sorted(
        {c for d in daily_schedule for c in d.get("characters", [])}
    )
    selected_chars = st.multiselect(
        "Filter by Character",
        all_chars,
        default=all_chars,
    )

    filtered = []
    for d in daily_schedule:
        day_chars = d.get("characters", [])
        if any(c in selected_chars for c in day_chars):
            filtered.append(d)

    rows = []
    for d in filtered:
        rows.append(
            {
                "Shoot Day": d["shoot_day"],
                "Scene": d["scene"],
                "Characters": ", ".join(d["characters"]),
                "Daily Burn ($)": d["daily_burn"],
            }
        )

    if rows:
        df = pd.DataFrame(rows)
        df["Daily Burn ($)"] = df["Daily Burn ($)"].map(
            lambda x: f"${x:,.2f}"
        )
        st.dataframe(df, width="stretch")

st.subheader("📊 Schedule Metrics")

st.metric(
    "Average Daily Burn",
    f"${schedule.get('average_daily_burn', 0.0):,.2f}",
)
peak = schedule.get("peak_burn_day", {})
if peak:
    st.metric(
        "Peak Burn Day",
        f"Day {peak.get('day')} — ${peak.get('cost', 0.0):,.2f}",
    )

st.info(
    "Stripboard export to PDF for the shooting calendar can be added later as a dedicated exporter. "
    "For now, you can copy this table or export it via pandas/DataFrame from a notebook."
)

