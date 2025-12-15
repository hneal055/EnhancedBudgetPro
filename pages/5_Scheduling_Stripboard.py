import streamlit as st
import pandas as pd
from src.components.sidebar import render_sidebar
render_sidebar()
from src.ui.global_sidebar import install_global_sidebar
install_global_sidebar()

from src.SchedulingEngine.production_scheduler import ProductionSchedulerEngine

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Stripboard & Schedule", layout="wide")
st.title("🎬 Phase 5 — Stripboard & Shooting Schedule")

# -------------------------------
# SAFETY CHECKS
# -------------------------------
if "data" not in st.session_state or not st.session_state.data:
    st.warning("⚠️ No script data found. Please analyze a script on the main page first.")
    st.stop()

if "cost" not in st.session_state or not st.session_state.cost:
    st.warning("⚠️ No cost data found. Please run Financial Intelligence first.")
    st.stop()

if "density" not in st.session_state or not st.session_state.density:
    st.warning("⚠️ No scene density data found. Please run Story Intelligence first.")
    st.stop()

data = st.session_state.data
cost = st.session_state.cost
density = st.session_state.density

# -------------------------------
# GENERATE / CACHE SCHEDULE
# -------------------------------
if "schedule" not in st.session_state:
    scheduler = ProductionSchedulerEngine()
    st.session_state.schedule = scheduler.generate_schedule(
        data["scenes"],
        cost["character_costs"]
    )

schedule = st.session_state.schedule

# ✅ HARD SAFETY GUARD
if not schedule or "daily_schedule" not in schedule or schedule["daily_schedule"] is None:
    st.error("❌ Schedule failed to generate. Character costs or scene data may be incomplete.")
    st.stop()

st.success("✅ Shooting schedule generated successfully")

# -------------------------------
# SCENE HEADER PARSER (SAFE LOCAL)
# -------------------------------
def parse_scene_header(header: str):
    header = header.upper()

    int_ext = (
        "INT" if header.startswith("INT") 
        else "EXT" if header.startswith("EXT") 
        else "INT/EXT"
    )

    if "NIGHT" in header:
        tod = "NIGHT"
    elif "DAY" in header:
        tod = "DAY"
    elif "DAWN" in header or "DUSK" in header:
        tod = "DAWN/DUSK"
    else:
        tod = "UNKNOWN"

    loc = header
    return int_ext, tod, loc

# -----------------------------------
# FILTER CONTROLS
# -----------------------------------
st.subheader("🎛 Stripboard Filters")

fcol1, fcol2, fcol3, fcol4, fcol5 = st.columns(5)

with fcol1:
    int_ext_filter = st.selectbox("INT / EXT", ["ALL", "INT", "EXT", "INT/EXT"])

with fcol2:
    time_filter = st.selectbox("Time of Day", ["ALL", "DAY", "NIGHT", "DAWN/DUSK"])

with fcol3:
    all_characters = sorted({c for sc in data["scenes"] for c in sc.get("characters", [])})
    selected_character = st.selectbox("Character Focus", ["ALL"] + all_characters)

with fcol4:
    min_risk = st.slider("Min Risk Score", 0, 100, 0, 5)

# ✅ SAFE MAX BURN
avg_burn = schedule.get("average_daily_burn", 1000) or 1000

with fcol5:
    max_burn = st.slider(
        "Max Daily Burn",
        0,
        int(avg_burn * 3),
        int(avg_burn * 3),
        500,
    )

# -------------------------------
# FILTER SCENES
# -------------------------------
visible_scenes = []

for idx, scene in enumerate(data["scenes"], start=1):
    header = scene.get("header", f"Scene {idx}")
    characters = scene.get("characters", [])

    int_ext, tod, loc = parse_scene_header(header)

    if int_ext_filter != "ALL" and int_ext != int_ext_filter:
        continue

    if time_filter != "ALL" and tod != time_filter:
        continue

    if selected_character != "ALL" and selected_character not in characters:
        continue

    # ✅ SAFE DENSITY LOOKUP
    density_info = next(
        (d for d in density.get("scene_density", []) if d.get("header") == header),
        {"classification": "N/A"}
    )

    visible_scenes.append((idx, scene, density_info))

# -------------------------------
# FILTER SCHEDULE
# -------------------------------
filtered_days = []

for day in schedule.get("daily_schedule", []):
    if not isinstance(day, dict):
        continue

    if day.get("daily_burn", 0) > max_burn:
        continue

    if selected_character != "ALL" and selected_character not in day.get("characters", []):
        continue

    filtered_days.append(day)

# -------------------------------
# MAIN LAYOUT (45% / 35% / 20%)
# -------------------------------
scol, schedcol, riskcol = st.columns([0.45, 0.35, 0.20])

# -------------------------------
# STRIPBOARD VISUAL
# -------------------------------
with scol:
    st.subheader("🟦 Stripboard Scenes")

    for idx, scene, density_info in visible_scenes:
        header = scene.get("header", f"Scene {idx}")
        characters = ", ".join(scene.get("characters", []))

        st.markdown(
            f"""
            <div style="
                background:#1e1e1e;
                border-left:8px solid #00d4ff;
                padding:10px;
                margin-bottom:8px;
                border-radius:6px;
                color:#f0f0f0;">
                <b>{idx}. {header}</b><br>
                🎭 {characters}<br>
                🎬 Density: {density_info.get('classification', 'N/A')}
            </div>
            """,
            unsafe_allow_html=True,
        )

# -------------------------------
# DAILY SCHEDULE
# -------------------------------
with schedcol:
    st.subheader("📆 Shooting Schedule")

    sched_rows = [
        {
            "Shoot Day": d.get("shoot_day"),
            "Scene": d.get("scene"),
            "Characters": ", ".join(d.get("characters", [])),
            "Daily Burn": d.get("daily_burn", 0),
        }
        for d in filtered_days
    ]

    st.dataframe(pd.DataFrame(sched_rows), width="stretch")

# -------------------------------
# RISK + BURN METRICS
# -------------------------------
with riskcol:
    st.subheader("⚠️ Live Metrics")

    st.metric("Visible Scenes", len(visible_scenes))
    st.metric("Visible Shoot Days", len(filtered_days))

    st.metric(
        "Filtered Burn Total",
        f"${sum(d.get('daily_burn', 0) for d in filtered_days):,.2f}",
    )

    st.metric(
        "Avg Daily Burn",
        f"${schedule.get('average_daily_burn', 0):,.2f}",
    )

    st.metric(
        "Peak Burn Day",
        f"${schedule.get('peak_burn_day', {}).get('cost', 0):,.2f}",
    )
