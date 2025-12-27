import streamlit as st

from src.SchedulingEngine.talent_availability_engine import TalentAvailabilityEngine
from src.SchedulingEngine.production_scheduler import ProductionSchedulerEngine
from src.SchedulingEngine.availability_rescheduler import AvailabilityReschedulerEngine

st.set_page_config(page_title="Talent Availability", layout="wide")
st.title("🎭 Phase 6.2 — Availability-Aware Auto Rescheduling")

# ---------------------------------------------
# SAFETY CHECK
# ---------------------------------------------
if not st.session_state.get("data") or not st.session_state.get("cost"):
    st.warning("⚠️ Run Script + Financial + Scheduler before using Talent Availability.")
    st.stop()

# ---------------------------------------------
# BASE SCHEDULE SOURCE
# ---------------------------------------------
scheduler = ProductionSchedulerEngine()
base_result = scheduler.generate_schedule(
    st.session_state.data["scenes"],
    st.session_state.cost["character_costs"]
)

original_schedule = base_result["daily_schedule"]

# ---------------------------------------------
# SESSION STATE INIT
# ---------------------------------------------
if "talent_overrides" not in st.session_state:
    st.session_state.talent_overrides = {}

if "optimized_schedule" not in st.session_state:
    st.session_state.optimized_schedule = None

# ---------------------------------------------
# TALENT AVAILABILITY ENGINE
# ---------------------------------------------
engine = TalentAvailabilityEngine()
results = engine.analyze(original_schedule, st.session_state.talent_overrides)

availability = results.get("availability_grid", {})
conflicts = results.get("conflicts", [])

# ---------------------------------------------
# LAYOUT
# ---------------------------------------------
strip_col, control_col = st.columns([4, 1])

# ---------------------------------------------
# LEFT — HEATMAP
# ---------------------------------------------
with strip_col:
    st.subheader("📅 Talent Availability Heatmap")

    if not availability:
        st.info("No availability data.")
    else:
        for char, days in availability.items():
            st.markdown(f"### 🎭 {char}")
            bar_cols = st.columns(len(days))

            for i, (day, status) in enumerate(sorted(days.items())):
                if status == "available":
                    bar_cols[i].markdown("🟩")
                elif status == "partial":
                    bar_cols[i].markdown("🟨")
                elif status == "unavailable":
                    bar_cols[i].markdown("🟥")

# ---------------------------------------------
# RIGHT — CONTROLS
# ---------------------------------------------
with control_col:
    st.subheader("🎛 Controls")

    if availability:
        selected_char = st.selectbox("Select Character", list(availability.keys()))
        selected_day = st.selectbox(
            "Select Shoot Day",
            sorted(availability[selected_char].keys())
        )

        new_status = st.radio(
            "Set Availability",
            ["available", "partial", "unavailable"]
        )

        if st.button("Apply Availability Override"):
            st.session_state.talent_overrides.setdefault(selected_char, {})
            st.session_state.talent_overrides[selected_char][selected_day] = new_status
            st.rerun()

    # ✅ AUTO RESCHEDULE BUTTON
    st.divider()
    if st.button("⚡ Auto-Optimize Schedule"):
        optimizer = AvailabilityReschedulerEngine()
        st.session_state.optimized_schedule = optimizer.optimize(
            original_schedule,
            availability
        )
        st.success("✅ Schedule Auto-Optimized")

# ---------------------------------------------
# RESULTS — OPTIMIZED OUTPUT
# ---------------------------------------------
st.divider()
st.subheader("⚡ Optimized Shooting Schedule")

if st.session_state.optimized_schedule:
    for entry in st.session_state.optimized_schedule["daily_schedule"]:
        st.write(
            f"Day {entry['shoot_day']} — {entry['scene']} "
            f"({', '.join(entry['characters'])})"
        )
else:
    st.info("Run auto-optimization to generate rescheduled output.")

# ---------------------------------------------
# CONFLICTS
# ---------------------------------------------
st.divider()
st.subheader("🚨 Hard-Block Conflicts")

if conflicts:
    for c in conflicts:
        st.error(
            f"{c['character']} is UNAVAILABLE on Day {c['shoot_day']} "
            f"for scene: {c['scene']}"
        )
else:
    st.success("✅ No hard-block conflicts detected")
