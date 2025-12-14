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
emotion_data = st.session_state.get("emotion_data", {})

# Phase 13.1 Week 3: Build intensity lookup from emotion data
intensity_by_scene = {}
if emotion_data and emotion_data.get("scenes"):
    for scene_data in emotion_data["scenes"]:
        heading = scene_data.get("heading", "")
        intensity = scene_data.get("intensity", 0)
        intensity_by_scene[heading] = intensity

scheduler = ProductionSchedulerEngine()
schedule = scheduler.generate_schedule(
    data["scenes"],
    cost["character_costs"],
)

st.session_state.schedule = schedule

daily_schedule = schedule.get("daily_schedule", [])

st.subheader("📅 Shooting Stripboard")

# Phase 13.1 Week 3: Emotion-aware stripboard legend
if intensity_by_scene:
    st.info("🎨 **Emotion-Aware Stripboard:** Scenes are color-coded by emotional intensity")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("🔴 **High Intensity** (>60) — Complex emotional scenes")
    with col2:
        st.markdown("🟡 **Medium Intensity** (30-60) — Moderate emotions")
    with col3:
        st.markdown("🟢 **Low Intensity** (<30) — Calm scenes")

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
        # Phase 13.1 Week 3: Get intensity for scene
        scene_heading = d["scene"]
        intensity = intensity_by_scene.get(scene_heading, 0)
        
        rows.append(
            {
                "Shoot Day": d["shoot_day"],
                "Scene": d["scene"],
                "Characters": ", ".join(d["characters"]),
                "Daily Burn ($)": d["daily_burn"],
                "Intensity": intensity,  # Hidden column for styling
            }
        )

    if rows:
        df = pd.DataFrame(rows)
        df["Daily Burn ($)"] = df["Daily Burn ($)"].map(
            lambda x: f"${x:,.2f}"
        )
        
        # Phase 13.1 Week 3: Apply emotion-based color styling
        def style_intensity(row):
            intensity = row["Intensity"]
            if intensity > 60:
                color = "background-color: #ffcccc"  # Light red
            elif intensity >= 30:
                color = "background-color: #fff4cc"  # Light yellow
            elif intensity > 0:
                color = "background-color: #ccffcc"  # Light green
            else:
                color = ""  # No emotion data
            return [color] * len(row)
        
        # Drop intensity column before display
        display_df = df.drop(columns=["Intensity"])
        
        if intensity_by_scene:
            styled_df = df.style.apply(style_intensity, axis=1)
            # Remove intensity column from styled output
            st.dataframe(styled_df, column_config={
                "Intensity": None  # Hide intensity column
            }, width="stretch")
        else:
            st.dataframe(display_df, width="stretch")

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

# Phase 13.1 Week 3: Show emotion-based schedule insights
if intensity_by_scene:
    st.subheader("�� Emotional Scheduling Insights")
    
    # Calculate intensity distribution across shoot days
    high_intensity_days = []
    for day in filtered:
        scene_heading = day["scene"]
        intensity = intensity_by_scene.get(scene_heading, 0)
        if intensity > 60:
            high_intensity_days.append(day["shoot_day"])
    
    if high_intensity_days:
        st.warning(
            f"⚠️ **High-Intensity Days:** Days {', '.join(map(str, high_intensity_days))} "
            f"have emotionally complex scenes. Consider additional prep time and actor support."
        )
    
    # Average intensity per day
    daily_intensities = {}
    for day in filtered:
        day_num = day["shoot_day"]
        scene_heading = day["scene"]
        intensity = intensity_by_scene.get(scene_heading, 0)
        if day_num not in daily_intensities:
            daily_intensities[day_num] = []
        daily_intensities[day_num].append(intensity)
    
    avg_daily_intensity = {
        day: sum(intensities) / len(intensities)
        for day, intensities in daily_intensities.items()
    }
    
    if avg_daily_intensity:
        max_intensity_day = max(avg_daily_intensity, key=avg_daily_intensity.get)
        st.info(
            f"📊 **Peak Emotional Day:** Day {max_intensity_day} "
            f"(Avg Intensity: {avg_daily_intensity[max_intensity_day]:.1f})"
        )

st.info(
    "Stripboard export to PDF for the shooting calendar can be added later as a dedicated exporter. "
    "For now, you can copy this table or export it via pandas/DataFrame from a notebook."
)
