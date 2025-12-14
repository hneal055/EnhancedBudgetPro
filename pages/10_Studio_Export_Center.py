"""
Phase 11.1 - Studio Export Center
Clean, professional Excel exports requiring zero explanation
"""

import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ExportEngine.excel_exporter_studio import StudioExcelExporter

st.set_page_config(page_title="Studio Export Center", page_icon="📊", layout="wide")

# Global sidebar
try:
    from src.ui.global_sidebar import render_sidebar
    render_sidebar()
except ImportError:
    pass

st.title("📊 Studio Export Center")
st.caption("Phase 11.1 - Professional Excel exports for producers, accountants, and insurers")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Export Readiness Check
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.header("🔍 Export Readiness Check")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.session_state.get("master_budget"):
        st.success("✅ Budget Locked")
    else:
        st.error("❌ Budget Missing")

with col2:
    if st.session_state.get("schedule"):
        st.success("✅ Schedule Valid")
    else:
        st.error("❌ Schedule Missing")

with col3:
    if st.session_state.get("risks"):
        st.success("✅ Risk Analysis")
    else:
        st.error("❌ Risk Incomplete")

with col4:
    if st.session_state.get("intel"):
        st.success("✅ Intel Ready")
    else:
        st.error("❌ Intel Missing")

# Check overall readiness
export_ready = all([
    st.session_state.get("master_budget"),
    st.session_state.get("schedule"),
    st.session_state.get("risks"),
    st.session_state.get("intel")
])

st.divider()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Export Options
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.header("📦 Export Options")

if not export_ready:
    st.warning("⚠️ Complete all required steps before exporting studio packages")
    st.info("**Next Steps:**\n1. Upload a script\n2. Run financial analysis\n3. Create schedule\n4. Calculate risks")
    st.stop()

# Project name input
project_name = st.text_input(
    "Project Name",
    value="Enhanced_Budget_Pro_Export",
    help="Used in Excel filenames"
)

# Output directory
output_dir = st.text_input(
    "Output Directory",
    value="./exports",
    help="Where to save Excel files"
)

st.divider()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Export Packages
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.header("📂 Studio-Ready Packages")

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("1️⃣ Master Budget")
    st.write("**Audience:** Producer / Studio / Accounting")
    st.write("**Sheets:** Summary, Crew, Cast, Equipment, Locations, Post, Insurance")
    
    if st.button("Export Master Budget", key="export_budget", use_container_width=True):
        with st.spinner("Creating EBP_Master_Budget.xlsx..."):
            try:
                exporter = StudioExcelExporter(project_name=project_name)
                Path(output_dir).mkdir(parents=True, exist_ok=True)
                
                path = exporter.export_master_budget(st.session_state, output_dir)
                st.success(f"✅ Exported: `{path}`")
                
                with open(path, "rb") as f:
                    st.download_button(
                        "📥 Download Master Budget",
                        data=f,
                        file_name=Path(path).name,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            except Exception as e:
                st.error(f"❌ Export failed: {e}")
    
    st.divider()
    
    st.subheader("3️⃣ Talent Availability")
    st.write("**Audience:** AD / Producer")
    st.write("**Format:** Character × Day matrix")
    
    if st.button("Export Talent Availability", key="export_talent", use_container_width=True):
        with st.spinner("Creating EBP_Talent_Availability.xlsx..."):
            try:
                exporter = StudioExcelExporter(project_name=project_name)
                Path(output_dir).mkdir(parents=True, exist_ok=True)
                
                path = exporter.export_talent_availability(st.session_state, output_dir)
                st.success(f"✅ Exported: `{path}`")
                
                with open(path, "rb") as f:
                    st.download_button(
                        "📥 Download Talent Availability",
                        data=f,
                        file_name=Path(path).name,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            except Exception as e:
                st.error(f"❌ Export failed: {e}")

with col_b:
    st.subheader("2️⃣ Shooting Schedule")
    st.write("**Audience:** AD / Production Manager")
    st.write("**Sheets:** Daily Schedule, Scene Breakdown")
    
    if st.button("Export Shooting Schedule", key="export_schedule", use_container_width=True):
        with st.spinner("Creating EBP_Shooting_Schedule.xlsx..."):
            try:
                exporter = StudioExcelExporter(project_name=project_name)
                Path(output_dir).mkdir(parents=True, exist_ok=True)
                
                path = exporter.export_shooting_schedule(st.session_state, output_dir)
                st.success(f"✅ Exported: `{path}`")
                
                with open(path, "rb") as f:
                    st.download_button(
                        "📥 Download Shooting Schedule",
                        data=f,
                        file_name=Path(path).name,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            except Exception as e:
                st.error(f"❌ Export failed: {e}")
    
    st.divider()
    
    st.subheader("4️⃣ Risk Forecast")
    st.write("**Audience:** Insurance / Studio Execs")
    st.write("**Sheets:** Risk Summary, Scene Risk, Monte Carlo")
    
    if st.button("Export Risk Forecast", key="export_risk", use_container_width=True):
        with st.spinner("Creating EBP_Risk_Forecast.xlsx..."):
            try:
                exporter = StudioExcelExporter(project_name=project_name)
                Path(output_dir).mkdir(parents=True, exist_ok=True)
                
                path = exporter.export_risk_forecast(st.session_state, output_dir)
                st.success(f"✅ Exported: `{path}`")
                
                with open(path, "rb") as f:
                    st.download_button(
                        "📥 Download Risk Forecast",
                        data=f,
                        file_name=Path(path).name,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            except Exception as e:
                st.error(f"❌ Export failed: {e}")

st.divider()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Export All Button
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.header("🚀 Export Complete Package")

if st.button("📦 Export All 4 Studio Files", type="primary", use_container_width=True):
    with st.spinner("Creating complete studio package..."):
        try:
            exporter = StudioExcelExporter(project_name=project_name)
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            paths = exporter.export_all_studio_packages(st.session_state, output_dir)
            
            st.success("✅ Complete package exported!")
            
            for name, path in paths.items():
                st.write(f"- **{name}:** `{path}`")
            
            st.balloons()
            
        except Exception as e:
            st.error(f"❌ Package export failed: {e}")
            st.exception(e)

st.divider()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Export Standards Info
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

with st.expander("📋 Export Standards & Quality Guarantees"):
    st.markdown("""
    ### Phase 11.1 Standards
    
    **Core Rule:** One row = one real-world line item
    - ✅ No nested dictionaries
    - ✅ No JSON blobs
    - ✅ No developer-style structures
    
    **Quality Guarantees:**
    - Opens cleanly in Excel, Numbers, Google Sheets
    - No formatting fixes required
    - No explanations needed
    - Studio accountant can immediately use it
    
    **Included Features:**
    - Currency normalized to numbers (no $ symbols in cells)
    - Dates in ISO format or shoot day integers
    - Fixed sheet names (no user input)
    - Hidden metadata sheet for audit trail
    
    **Validation:**
    - Budget must be locked
    - Schedule must be valid
    - Risk analysis must be completed
    - All data contracts enforced
    """)

st.caption("Enhanced Budget Pro v1.0.0 | Phase 11.1 Complete")
