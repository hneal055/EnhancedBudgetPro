"""
Export Center - Central hub for all production exports
Phase 11.1 - Studio-ready Excel packages
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ExportEngine.excel_exporter_studio import StudioExcelExporter

st.set_page_config(page_title="Export Center", page_icon="📦", layout="wide")

# Global sidebar
try:
    from src.ui.global_sidebar import render_sidebar
    render_sidebar()
except ImportError:
    pass

st.title("📦 Export Center")
st.caption("Professional production documents ready for studio, accounting, and insurance")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# System Status Dashboard
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.header("🔍 System Status")

col1, col2, col3, col4 = st.columns(4)

with col1:
    script_loaded = st.session_state.get("data") is not None
    if script_loaded:
        scene_count = len(st.session_state.get("data", {}).get("scenes", []))
        st.metric("Script", f"{scene_count} scenes", delta="Loaded", delta_color="normal")
    else:
        st.metric("Script", "Not loaded", delta="Required", delta_color="off")

with col2:
    intel_ready = st.session_state.get("intel") is not None
    if intel_ready:
        char_count = len(st.session_state.get("intel", {}))
        st.metric("Intelligence", f"{char_count} chars", delta="Ready", delta_color="normal")
    else:
        st.metric("Intelligence", "Not analyzed", delta="Required", delta_color="off")

with col3:
    budget_ready = st.session_state.get("master_budget") is not None
    if budget_ready:
        total = st.session_state.get("master_budget", {}).get("total", 0)
        st.metric("Budget", f"${total:,.0f}", delta="Calculated", delta_color="normal")
    else:
        st.metric("Budget", "Not calculated", delta="Required", delta_color="off")

with col4:
    schedule_ready = st.session_state.get("schedule") is not None
    if schedule_ready:
        days = st.session_state.get("schedule", {}).get("shoot_days", 0)
        st.metric("Schedule", f"{days} days", delta="Ready", delta_color="normal")
    else:
        st.metric("Schedule", "Not created", delta="Optional", delta_color="off")

# Overall readiness
export_ready = script_loaded and intel_ready and budget_ready

if export_ready:
    st.success("✅ System ready for professional exports")
else:
    st.warning("⚠️ Complete required analysis before exporting")
    st.info("""
    **Prerequisites:**
    1. Upload and parse a script → Page 0: Command Center
    2. Run character intelligence → Page 1: Story Intelligence
    3. Calculate production budget → Page 3: Production Budget
    """)

st.divider()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Export Configuration
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.header("⚙️ Export Settings")

col_a, col_b = st.columns(2)

with col_a:
    project_name = st.text_input(
        "Project Name",
        value=st.session_state.get("script_name", "Production").replace(" ", "_"),
        help="Used in all export filenames"
    )

with col_b:
    output_dir = st.text_input(
        "Output Directory",
        value="./exports",
        help="Folder where all exports will be saved"
    )

st.divider()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Export Packages
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.header("📊 Available Exports")

# Package 1: Master Budget (WIRED UP)
with st.container():
    st.subheader("💰 Master Budget")
    
    col_info, col_action = st.columns([3, 1])
    
    with col_info:
        st.markdown("""
        **Audience:** Producer / Studio / Accounting
        
        **Includes:**
        - Summary totals (7 categories)
        - Crew breakdown (department, role, rate)
        - Cast costs (character, scenes, rates)
        - Equipment packages (camera, lighting, sound)
        - Location costs (scout, permits, fees)
        - Post-production (editing, color, sound, VFX)
        - Insurance & contingency
        
        **Format:** 7 sheets + hidden metadata  
        **File:** `EBP_Master_Budget_<timestamp>.xlsx`
        """)
    
    with col_action:
        st.write("")  # Spacing
        st.write("")
        if st.button("📥 Export", key="export_master_budget", 
                    disabled=not export_ready, width='stretch'):
            with st.spinner("Creating Master Budget..."):
                try:
                    exporter = StudioExcelExporter(project_name=project_name)
                    Path(output_dir).mkdir(parents=True, exist_ok=True)
                    
                    # Convert session_state to dict for exporter
                    session_dict = dict(st.session_state)
                    path = exporter.export_master_budget(session_dict, output_dir)
                    
                    st.success(f"✅ Exported!")
                    
                    # Download button
                    with open(path, "rb") as f:
                        st.download_button(
                            label="📥 Download",
                            data=f,
                            file_name=Path(path).name,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key="download_master_budget"
                        )
                    
                except Exception as e:
                    st.error(f"❌ Failed: {e}")
        
        st.caption("Status: Ready" if export_ready else "Status: Waiting")

st.divider()

# Package 2: Shooting Schedule (PLACEHOLDER)
with st.container():
    st.subheader("📅 Shooting Schedule")
    
    col_info, col_action = st.columns([3, 1])
    
    with col_info:
        st.markdown("""
        **Audience:** AD / Production Manager
        
        **Includes:**
        - Daily schedule (stripboard style)
        - Scene breakdown (heading, characters, pages)
        - Shoot day assignments
        - Location groupings
        - Estimated daily costs
        - Risk levels per scene
        
        **Format:** 2 sheets + metadata  
        **File:** `EBP_Shooting_Schedule_<timestamp>.xlsx`
        """)
    
    with col_action:
        st.write("")
        st.write("")
        schedule_enabled = export_ready and schedule_ready
        if st.button("📥 Export", key="export_schedule", 
                    disabled=not schedule_enabled, width='stretch'):
            with st.spinner("Creating Shooting Schedule..."):
                try:
                    exporter = StudioExcelExporter(project_name=project_name)
                    Path(output_dir).mkdir(parents=True, exist_ok=True)
                    
                    path = exporter.export_shooting_schedule(st.session_state, output_dir)
                    
                    st.success(f"✅ Exported!")
                    
                    with open(path, "rb") as f:
                        st.download_button(
                            label="📥 Download",
                            data=f,
                            file_name=Path(path).name,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key="download_schedule"
                        )
                except Exception as e:
                    st.error(f"❌ Failed: {e}")
        
        st.caption("Status: Ready" if schedule_enabled else "Status: Schedule required")


# Package 3: PDF Budget Report with Emotional Intelligence
with st.container():
    st.subheader("📄 PDF Budget Report")
    
    col_info, col_action = st.columns([3, 1])
    
    with col_info:
        st.markdown("""
        **Audience:** Executive Producers / Investors / Studio Heads
        
        **Includes:**
        - Executive summary (budget, scenes, pages)
        - **Emotional Intelligence Analysis** (NEW)
          - Emotion distribution across script
          - Character emotional complexity
          - Key turning points
          - Intensity & tension metrics
        - Scene-by-scene breakdown with emotion data
        - Budget summary with risk adjustments
        - Interpretation guide
        
        **Format:** Multi-page PDF report  
        **File:** `ProductionBudgetReport_<timestamp>.pdf`
        """)
    
    with col_action:
        st.write("")
        st.write("")
        if st.button("📥 Export PDF", key="export_pdf_report", 
                    disabled=not export_ready, use_container_width=True):
            with st.spinner("Generating PDF Report..."):
                try:
                    from src.ExportEngine.pdf_reporter import PDFBudgetReport
                    import tempfile
                    
                    # Prepare data
                    data = st.session_state.get("data", {})
                    master_budget = st.session_state.get("master_budget", {})
                    emotion_data = st.session_state.get("emotion_data")
                    
                    # Create budget summary
                    budget_summary = {
                        "base_budget": master_budget.get("total", 0),
                        "risk_delay_cost": 0,
                        "contingency_buffer": master_budget.get("total", 0) * 0.12,
                        "risk_adjusted_total": master_budget.get("total", 0) * 1.12
                    }
                    
                    # Generate PDF
                    reporter = PDFBudgetReport(title=f"{project_name} - Production Budget Report")
                    
                    # Create output path with timestamp
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_path = Path(output_dir) / f"ProductionBudgetReport_{timestamp}.pdf"
                    Path(output_dir).mkdir(parents=True, exist_ok=True)
                    
                    # Generate with emotion data
                    reporter.generate(
                        data=data,
                        budget_summary=budget_summary,
                        output_path=str(output_path),
                        emotion_data=emotion_data
                    )
                    
                    st.success(f"✅ PDF Report Generated!")
                    
                    # Download button
                    with open(output_path, "rb") as f:
                        st.download_button(
                            label="📥 Download PDF",
                            data=f,
                            file_name=output_path.name,
                            mime="application/pdf",
                            key="download_pdf_report"
                        )
                    
                except Exception as e:
                    st.error(f"❌ Failed: {e}")
                    import traceback
                    st.code(traceback.format_exc())
        
        emotion_available = st.session_state.get("emotion_data") is not None
        status = "Ready with Emotions" if (export_ready and emotion_available) else "Ready" if export_ready else "Waiting"
        st.caption(f"Status: {status}")

st.divider()


st.divider()

# Package 3: Talent Availability (PLACEHOLDER)
with st.container():
    st.subheader("🎭 Talent Availability")
    
    col_info, col_action = st.columns([3, 1])
    
    with col_info:
        st.markdown("""
        **Audience:** AD / Producer
        
        **Includes:**
        - Character × Day availability matrix
        - Conflict tracking
        - Per-day availability status
        - Scheduling notes
        - One row per character per day
        
        **Format:** 1 sheet + metadata  
        **File:** `EBP_Talent_Availability_<timestamp>.xlsx`
        """)
    
    with col_action:
        st.write("")
        st.write("")
        talent_enabled = export_ready and schedule_ready
        if st.button("📥 Export", key="export_talent", 
                    disabled=not talent_enabled, width='stretch'):
            with st.spinner("Creating Talent Availability..."):
                try:
                    exporter = StudioExcelExporter(project_name=project_name)
                    Path(output_dir).mkdir(parents=True, exist_ok=True)
                    
                    path = exporter.export_talent_availability(st.session_state, output_dir)
                    
                    st.success(f"✅ Exported!")
                    
                    with open(path, "rb") as f:
                        st.download_button(
                            label="📥 Download",
                            data=f,
                            file_name=Path(path).name,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key="download_talent"
                        )
                except Exception as e:
                    st.error(f"❌ Failed: {e}")
        
        st.caption("Status: Ready" if talent_enabled else "Status: Schedule required")

st.divider()

# Package 4: Risk Forecast (PLACEHOLDER)
with st.container():
    st.subheader("⚠️ Risk Forecast")
    
    col_info, col_action = st.columns([3, 1])
    
    with col_info:
        st.markdown("""
        **Audience:** Insurance / Studio Execs
        
        **Includes:**
        - Risk summary (high/medium/low counts)
        - Scene-level risk breakdown
        - Monte Carlo simulation results
        - Budget confidence intervals
        - Mitigation strategies
        
        **Format:** 3 sheets + metadata  
        **File:** `EBP_Risk_Forecast_<timestamp>.xlsx`
        """)
    
    with col_action:
        st.write("")
        st.write("")
        risk_enabled = export_ready and st.session_state.get("risks")
        if st.button("📥 Export", key="export_risk", 
                    disabled=not risk_enabled, width='stretch'):
            with st.spinner("Creating Risk Forecast..."):
                try:
                    exporter = StudioExcelExporter(project_name=project_name)
                    Path(output_dir).mkdir(parents=True, exist_ok=True)
                    
                    path = exporter.export_risk_forecast(st.session_state, output_dir)
                    
                    st.success(f"✅ Exported!")
                    
                    with open(path, "rb") as f:
                        st.download_button(
                            label="📥 Download",
                            data=f,
                            file_name=Path(path).name,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key="download_risk"
                        )
                except Exception as e:
                    st.error(f"❌ Failed: {e}")
        
        st.caption("Status: Ready" if risk_enabled else "Status: Risk analysis required")

st.divider()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Complete Package Export
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.header("🚀 Complete Package")

all_ready = (export_ready and schedule_ready and 
             st.session_state.get("risks") is not None)

if all_ready:
    st.success("✅ All systems ready for complete package export")
else:
    st.info("💡 Complete all analysis steps to unlock full package export")

col_pkg, col_btn = st.columns([3, 1])

with col_pkg:
    st.markdown("""
    **Export all 4 studio-ready files at once:**
    1. EBP_Master_Budget.xlsx
    2. EBP_Shooting_Schedule.xlsx
    3. EBP_Talent_Availability.xlsx
    4. EBP_Risk_Forecast.xlsx
    
    All files will be timestamped and saved to the output directory.
    """)

with col_btn:
    st.write("")
    st.write("")
    if st.button("📦 Export All", key="export_all", type="primary",
                disabled=not all_ready, width='stretch'):
        with st.spinner("Creating complete package..."):
            try:
                exporter = StudioExcelExporter(project_name=project_name)
                Path(output_dir).mkdir(parents=True, exist_ok=True)
                
                paths = exporter.export_all_studio_packages(st.session_state, output_dir)
                
                st.success("✅ Complete package exported!")
                st.balloons()
                
                for name, path in paths.items():
                    st.write(f"- {name}: `{Path(path).name}`")
                
            except Exception as e:
                st.error(f"❌ Failed: {e}")

st.divider()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Export Standards & History
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

with st.expander("📋 Export Standards (Phase 11.1)"):
    st.markdown("""
    ### Core Principles
    **One row = one real-world line item**
    - No nested dictionaries
    - No JSON blobs  
    - No developer structures
    
    ### Quality Guarantees
    - ✅ Opens cleanly in Excel, Numbers, Google Sheets
    - ✅ No formatting fixes required
    - ✅ No explanations needed
    - ✅ Studio accountant ready
    
    ### Technical Standards
    - Currency normalized to numbers (no $ in cells)
    - Dates in ISO format or shoot day integers
    - Fixed sheet names (no user input)
    - Hidden metadata for audit trail
    
    ### Data Contract
    Before any export is allowed:
    - ✅ Budget locked
    - ✅ Schedule valid (for schedule/talent exports)
    - ✅ Risk analysis completed (for risk export)
    - ✅ All validation rules passed
    """)

with st.expander("🎯 Use Cases & Workflows"):
    st.markdown("""
    ### Master Budget
    **When to use:** Budget approvals, studio greenlight, accounting imports
    **Audience:** Producers, studio execs, production accountants
    **Next step:** Submit to accounting for approval
    
    ### Shooting Schedule
    **When to use:** Pre-production planning, crew coordination
    **Audience:** Assistant Directors, production managers
    **Next step:** Distribute to department heads
    
    ### Talent Availability
    **When to use:** Scheduling conflicts, talent negotiations
    **Audience:** AD team, producers, casting
    **Next step:** Identify and resolve conflicts
    
    ### Risk Forecast
    **When to use:** Insurance applications, contingency planning
    **Audience:** Insurance underwriters, studio execs
    **Next step:** Submit with insurance application
    
    ### Complete Package
    **When to use:** Final pre-production package
    **Audience:** All stakeholders
    **Next step:** Distribute to entire production team
    """)

st.caption("Enhanced Budget Pro v1.0.0 | Phase 11.1 - Export Center")
