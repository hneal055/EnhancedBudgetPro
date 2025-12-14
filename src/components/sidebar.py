import streamlit as st

PHASES = {
    "Phase 1 — Story Intelligence": [
        ("Story Parser", "1_Story_Intelligence"),
    ],
    "Phase 2 — Financial Intelligence": [
        ("Financial Breakdown", "2_Financial_Intelligence"),
        ("Master Production Budget", "3_Production_Budget"),
    ],
    "Phase 3 — Scheduling & Stripboard": [
        ("Scheduling Overview", "5_Scheduling_Stripboard"),
        ("Stripboard Scheduler", "5_Stripboard_Scheduler"),
    ],
    "Phase 4 — Risk & Monte Carlo": [
        ("Risk Intelligence", "4_Risk_Monte_Carlo"),
    ],
    "Phase 5 — Talent Availability": [
        ("Availability Heatmap", "6_Talent_Availability"),
        ("Auto-Rescheduling", "6_Availability_Auto_Rescheduling"),
    ],
    "Phase 6 — Export & Delivery": [
        ("Export Center", "6_Export_Center"),
    ],
    "Phase 7 — Optimization Engine": [
        ("What-If Scenarios", "7_WhatIf_Scenarios"),
        ("Optimization Console", "7_Optimization_Console"),
    ]
}


def render_sidebar():
    st.sidebar.title("🎬 Enhanced Budget Pro")
    st.sidebar.caption("Enterprise Production Intelligence Suite")

    # ------------------------------
    # STATUS PANEL
    # ------------------------------
    st.sidebar.subheader("📊 System Status")

    def status(name, key):
        ok = key in st.session_state and st.session_state[key] is not None
        icon = "🟢" if ok else "⚪"
        st.sidebar.write(f"{icon} {name}")

    status("Script Loaded", "data")
    status("Budget Ready", "cost")
    status("Schedule Ready", "schedule")
    status("Talent Overrides", "talent_overrides")
    status("Risk Model", "risk")
    status("What-If Results", "whatif_results")

    st.sidebar.markdown("---")

    # ------------------------------
    # PHASE NAVIGATION SECTION
    # ------------------------------
    st.sidebar.subheader("📁 Workflow Navigation")

    for phase_title, items in PHASES.items():
        with st.sidebar.expander(phase_title, expanded=False):
            for label, page in items:
                st.page_link(f"pages/{page}.py", label=label)

    st.sidebar.markdown("---")

    # ------------------------------
    # RUN FULL PIPELINE
    # ------------------------------
    st.sidebar.subheader("⚙️ Pipeline Control")

    if st.sidebar.button("🚀 Run Full Pipeline"):
        st.session_state["trigger_full_pipeline"] = True
        st.sidebar.success("Pipeline triggered — run pages in order.")

    st.sidebar.markdown("---")
    st.sidebar.caption("© 2025 FilmStudioDev — MAX AURA Framework")
