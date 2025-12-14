import streamlit as st
import pandas as pd
from src.ui.global_sidebar import install_global_sidebar
install_global_sidebar()

from src.SchedulingEngine.production_scheduler import ProductionSchedulerEngine

st.title("🎬 Phase 5 — Scheduling & Stripboard Visuals")

# -------------------------------------------------------
# 1. PULL SHARED DATA FROM SESSION
# -------------------------------------------------------
data = st.session_state.get("data")
cost = st.session_state.get("cost")

if not (data and cost):
    st.warning("ℹ️ Run **Story Intelligence** and **Financial Intelligence** first so we know scenes and character costs.")
    st.stop()

# -------------------------------------------------------
# 2. RUN SCHEDULER ENGINE
# -------------------------------------------------------
scheduler = ProductionSchedulerEngine()
schedule = scheduler.generate_schedule(
    data["scenes"],
    cost["character_costs"]
)

daily = schedule["daily_schedule"]
avg_burn = schedule.get("average_daily_burn", 0)
peak = schedule.get("peak_burn_day", {})

# Convert to DataFrame for visualization
df = pd.DataFrame(daily)

# Normalize fields
if "characters" in df.columns:
    df["Characters"] = df["characters"].apply(lambda c: ", ".join(c) if isinstance(c, (list, tuple)) else str(c))
if "daily_burn" in df.columns:
    df["Daily Burn ($)"] = df["daily_burn"]

df["Shoot Day"] = df["shoot_day"]

# -------------------------------------------------------
# 3. STRIPBOARD-STYLE RISK FLAGS
# -------------------------------------------------------
def classify_day(burn_value: float, avg: float) -> str:
    if avg <= 0:
        return "🟢 Normal"
    ratio = burn_value / avg
    if ratio >= 1.5:
        return "🔴 HOT DAY"
    elif ratio >= 1.1:
        return "🟡 Elevated"
    else:
        return "🟢 Normal"

df["Burn Classification"] = df["Daily Burn ($)"].apply(
    lambda v: classify_day(v, avg_burn)
)

# Try to parse basic INT/EXT + TIME OF DAY from scene header
def parse_header(header: str):
    if not isinstance(header, str):
        return "", "", header
    parts = [p.strip() for p in header.split("-")]
    int_ext = ""
    tod = ""
    location = header
    if len(parts) >= 1:
        if parts[0].upper().startswith("INT"):
            int_ext = "INT"
        elif parts[0].upper().startswith("EXT"):
            int_ext = "EXT"
    if len(parts) >= 2:
        location = parts[1].strip()
    if len(parts) >= 3:
        tod = parts[2].strip().upper()
    return int_ext, tod, location

int_ext_list = []
tod_list = []
loc_list = []

for s in df["scene"]:
    ie, tod, loc = parse_header(s)
    int_ext_list.append(ie)
    tod_list.append(tod)
    loc_list.append(loc)

df["INT/EXT"] = int_ext_list
df["Time of Day"] = tod_list
df["Location"] = loc_list

# -------------------------------------------------------
# 4. SUMMARY METRICS
# -------------------------------------------------------
st.subheader("📊 Schedule Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Total Shoot Days", len(df))
col2.metric("Average Daily Burn", f"${avg_burn:,.2f}")
if peak:
    col3.metric(
        "Peak Burn Day",
        f"Day {peak.get('day', '?')} — ${peak.get('cost', 0):,.2f}"
    )
else:
    col3.metric("Peak Burn Day", "N/A")

# -------------------------------------------------------
# 5. DAILY BURN BAR CHART
# -------------------------------------------------------
st.subheader("🔥 Daily Burn by Shoot Day")

chart_df = df[["Shoot Day", "Daily Burn ($)"]].set_index("Shoot Day")
st.bar_chart(chart_df)

# -------------------------------------------------------
# 6. STRIPBOARD TABLE VIEW
# -------------------------------------------------------
st.subheader("🎞 Stripboard View")

strip_df = df[[
    "Shoot Day",
    "scene",
    "INT/EXT",
    "Location",
    "Time of Day",
    "Characters",
    "Daily Burn ($)",
    "Burn Classification",
]]

strip_df = strip_df.sort_values("Shoot Day")

st.dataframe(strip_df, width="stretch")

# -------------------------------------------------------
# 7. PER-DAY STRIP CARDS (VISUAL BOARD)
# -------------------------------------------------------
st.subheader("📅 Day-by-Day Stripboard")

for _, row in strip_df.iterrows():
    day = row["Shoot Day"]
    header = row["scene"]
    ie = row["INT/EXT"]
    tod = row["Time of Day"]
    loc = row["Location"]
    chars = row["Characters"]
    burn = row["Daily Burn ($)"]
    flag = row["Burn Classification"]

    with st.container(border=True):
        st.markdown(
            f"**Day {day} — {flag}**  \n"
            f"**Scene:** {header}  \n"
            f"**INT/EXT:** {ie or '—'} | **Location:** {loc or '—'} | **Time:** {tod or '—'}  \n"
            f"**Characters:** {chars}  \n"
            f"**Daily Burn:** `${burn:,.2f}`"
        )

st.caption("Phase 5 Stripboard: visual foundation for future calendar + call-sheet export.")
# ===============================
# PHASE 5.2 — STRIPBOARD VISUAL
# LAYOUT RATIO: 45% | 35% | 20%
# ===============================

st.markdown("---")
st.header("🎞️ PRODUCTION STRIPBOARD — STUDIO DARK")

if st.session_state.data and st.session_state.cost and st.session_state.burn:

    strip_col, sched_col, risk_col = st.columns([4.5, 3.5, 2])

    # ===============================
    # LEFT — SCENE STRIPBOARD (45%)
    # ===============================
    with strip_col:
        st.subheader("🎬 Stripboard — Scene Cards")

        for idx, scene in enumerate(st.session_state.data["scenes"], start=1):

            scene_header = scene.get("header", "UNKNOWN")
            scene_chars = ", ".join(scene.get("characters", []))

            # Find matching burn cost
            burn_match = next(
                (d for d in st.session_state.burn["daily_schedule"] if d["scene"] == scene_header),
                None
            )

            daily_burn = burn_match["daily_burn"] if burn_match else 0

            st.markdown(
                f"""
                <div style="
                    background:#161B22;
                    padding:16px;
                    margin-bottom:10px;
                    border-radius:12px;
                    border-left:6px solid #00E5FF;
                ">
                <b>Scene {idx}:</b> {scene_header}<br>
                👥 {scene_chars}<br>
                💵 Daily Burn: ${daily_burn:,.0f}
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ===============================
    # CENTER — SHOOT SCHEDULE (35%)
    # ===============================
    with sched_col:
        st.subheader("🗓 Shoot Day Flow")

        sched_rows = []
        for day in st.session_state.burn["daily_schedule"]:
            sched_rows.append({
                "Day": day["shoot_day"],
                "Scene": day["scene"],
                "Characters": ", ".join(day["characters"]),
                "Daily Burn ($)": day["daily_burn"]
            })

        st.dataframe(pd.DataFrame(sched_rows), width="stretch")

        st.metric(
            "📈 Average Daily Burn",
            f"${st.session_state.burn['average_daily_burn']:,.2f}"
        )

    # ===============================
    # RIGHT — RISK + EXECUTIVE (20%)
    # ===============================
    with risk_col:
        st.subheader("⚠️ Executive Risk")

        peak = st.session_state.burn.get("peak_burn_day", {})
        st.metric(
            "🔥 Peak Burn",
            f"Day {peak.get('day', '-')}",
            f"${peak.get('cost', 0):,.2f}"
        )

        danger = st.session_state.burn.get("danger_days", [])
        st.metric("🚨 Danger Days", len(danger))

else:
    st.info("ℹ️ Run Script + Financial Analysis to activate Stripboard.")

