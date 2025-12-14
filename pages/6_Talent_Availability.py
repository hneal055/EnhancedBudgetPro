import streamlit as st
from src.ui.global_sidebar import install_global_sidebar
install_global_sidebar()

from src.SchedulingEngine.talent_availability_engine import TalentAvailabilityEngine
from src.SchedulingEngine.production_scheduler import ProductionSchedulerEngine
from src.AnalysisEngine.cost_impact_engine import CharacterCostImpactEngine  # not strictly needed but kept for context

st.title("🎭 Phase 6.1 — Talent Availability")

# ---------------------------------------------
# PRECHECK
# ---------------------------------------------
if not (st.session_state.get("data") and st.session_state.get("cost")):
    st.warning("⚠️ Run Story + Financial Intelligence first.")
    st.stop()

# Ensure overrides dict exists
if "talent_overrides" not in st.session_state or st.session_state.talent_overrides is None:
    st.session_state.talent_overrides = {}

# ---------------------------------------------
# SOURCE SCHEDULE
# ---------------------------------------------
if st.session_state.get("schedule") is None:
    scheduler = ProductionSchedulerEngine()
    schedule = scheduler.generate_schedule(
        st.session_state.data["scenes"],
        st.session_state.cost["character_costs"],
    )
    st.session_state.schedule = schedule
else:
    schedule = st.session_state.schedule

engine = TalentAvailabilityEngine()
results = engine.analyze(schedule, st.session_state.talent_overrides)

availability = results.get("availability_grid", {})
conflicts = results.get("conflicts", [])

strip_col, control_col = st.columns([4, 1])

# ---------------------------------------------
# TIMELINE VIEW
# ---------------------------------------------
with strip_col:
    st.subheader("📅 Talent Availability Timeline")

    if not availability:
        st.info("No availability data yet.")
    else:
        for char in sorted(availability.keys()):
            days_map = availability[char]
            st.markdown(f"### 🎭 {char}")

            day_numbers = sorted(days_map.keys())
            cols = st.columns(len(day_numbers) or 1)

            for idx, day in enumerate(day_numbers):
                status = days_map[day]
                if status == "available":
                    marker = "🟩"
                elif status == "partial":
                    marker = "🟨"
                elif status == "unavailable":
                    marker = "🟥"
                else:
                    marker = "⬛"

                cols[idx].markdown(f"{marker}\n\nDay {day}")

            st.caption("🟩 Available | 🟨 Partial | 🟥 Blocked | ⬛ Not Required")

# ---------------------------------------------
# CONTROL PANEL
# ---------------------------------------------
with control_col:
    st.subheader("🎛 Availability Controls")

    if availability:
        selected_char = st.selectbox(
            "Select Character",
            sorted(availability.keys()),
        )

        day_keys = sorted(availability[selected_char].keys())
        selected_day = st.selectbox("Select Shoot Day", day_keys)

        new_status = st.radio(
            "Set Availability",
            ["available", "partial", "unavailable"],
        )

        if st.button("Apply Override"):
            st.session_state.talent_overrides.setdefault(selected_char, {})
            st.session_state.talent_overrides[selected_char][selected_day] = new_status
            st.success(
                f"Override applied: {selected_char} on Day {selected_day} → {new_status}"
            )
            st.rerun()
    else:
        st.info("No schedule yet — visit the Stripboard page first.")

# ---------------------------------------------
# CONFLICTS
# ---------------------------------------------
st.subheader("🚨 Hard-Block Conflicts")

if conflicts:
    for c in conflicts:
        st.error(
            f"{c['character']} is UNAVAILABLE on Day {c['shoot_day']} "
            f"for scene: {c['scene']}"
        )
else:
    st.success("✅ No hard-block conflicts detected.")
