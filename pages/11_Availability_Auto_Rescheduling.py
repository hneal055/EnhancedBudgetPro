import copy
import streamlit as st
from src.ui.global_sidebar import install_global_sidebar
install_global_sidebar()

st.title("🔁 Phase 6.2 — Availability-Aware Auto Rescheduling")

if not (st.session_state.get("schedule") and st.session_state.get("talent_overrides")):
    st.warning(
        "⚠️ You need a schedule (Page 5) and some availability overrides (Page 6.1) first."
    )
    st.stop()

schedule = st.session_state.schedule
overrides = st.session_state.talent_overrides

daily = schedule.get("daily_schedule", []) or []

st.subheader("🎯 Auto-Adjust Proposal")

st.write(
    "This simple engine looks for **UNAVAILABLE** actors on a given day and "
    "proposes shifting those scenes by **+1 shooting day** (minimal disruption heuristic)."
)

if st.button("Generate Auto-Reschedule Proposal"):
    proposed = copy.deepcopy(daily)
    moves = []

    for entry in proposed:
        day = entry["shoot_day"]
        chars = entry.get("characters", [])
        blocked = [
            c
            for c in chars
            if overrides.get(c, {}).get(day) == "unavailable"
        ]
        if blocked:
            new_day = day + 1
            entry["shoot_day"] = new_day
            moves.append(
                {
                    "scene": entry["scene"],
                    "from": day,
                    "to": new_day,
                    "blocked_chars": blocked,
                }
            )

    if not moves:
        st.success("✅ No changes needed — no conflicts detected.")
    else:
        st.session_state["auto_reschedule_proposal"] = proposed
        st.success(f"Generated {len(moves)} proposed scene moves.")

        for m in moves:
            st.warning(
                f"Move **{m['scene']}** from Day {m['from']} → Day {m['to']} "
                f"(blocked: {', '.join(m['blocked_chars'])})"
            )

st.subheader("📋 Proposed New Stripboard (Preview)")

proposal = st.session_state.get("auto_reschedule_proposal")
if not proposal:
    st.info("Generate a proposal above to see the adjusted stripboard.")
else:
    rows = []
    for d in sorted(proposal, key=lambda e: e["shoot_day"]):
        rows.append(
            {
                "Shoot Day": d["shoot_day"],
                "Scene": d["scene"],
                "Characters": ", ".join(d["characters"]),
                "Daily Burn ($)": d["daily_burn"],
            }
        )

    import pandas as pd

    df = pd.DataFrame(rows)
    df["Daily Burn ($)"] = df["Daily Burn ($)"].map(lambda x: f"${x:,.2f}")
    st.dataframe(df, width="stretch")

    if st.button("Apply Proposal to Live Schedule"):
        # overwrite live schedule
        schedule["daily_schedule"] = proposal
        st.session_state.schedule = schedule
        st.success("✅ Proposal applied to live schedule.")
