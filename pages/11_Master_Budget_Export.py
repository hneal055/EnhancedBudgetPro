"""
Master Budget Export (Phase 11.1 - Step 1)
Start with one perfect Excel file before expanding
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.ExportEngine.excel_exporter_studio import StudioExcelExporter

st.set_page_config(page_title="Master Budget Export", page_icon="💰", layout="wide")

# Global sidebar
try:
    from src.ui.global_sidebar import render_sidebar
    render_sidebar()
except ImportError:
    pass

st.title("💰 Master Budget Export")
st.caption("Studio-ready Excel export with zero explanation required")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Readiness Check
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.header("🔍 Export Readiness")

col1, col2, col3 = st.columns(3)

with col1:
    if st.session_state.get("master_budget"):
        st.success("✅ Budget Calculated")
        budget_ready = True
    else:
        st.error("❌ Budget Missing")
        budget_ready = False

with col2:
    if st.session_state.get("intel"):
        st.success("✅ Character Intel")
        intel_ready = True
    else:
        st.error("❌ Intel Missing")
        intel_ready = False

with col3:
    if st.session_state.get("data"):
        st.success("✅ Script Parsed")
        data_ready = True
    else:
        st.error("❌ No Script Data")
        data_ready = False

export_ready = budget_ready and intel_ready and data_ready

st.divider()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Export Settings
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.header("📊 EBP_Master_Budget.xlsx")

if not export_ready:
    st.warning("⚠️ Complete required steps before exporting")
    st.info("""
    **Required:**
    1. Upload and parse a script
    2. Calculate character intelligence
    3. Generate production budget
    """)
    st.stop()

# Project name
project_name = st.text_input(
    "Project Name",
    value=st.session_state.get("script_name", "Production").replace(" ", "_"),
    help="Used in filename: EBP_Master_Budget_<timestamp>.xlsx"
)

# Output directory
output_dir = st.text_input(
    "Output Directory",
    value="./exports",
    help="Where to save the Excel file"
)

st.divider()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# File Preview
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.subheader("📑 Included Sheets")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("""
    **Sheet 1: Summary**
    - High-level budget totals
    - Category breakdown
    - Grand total
    
    **Sheet 2: Crew**
    - Department | Role | Rate | Units
    - Daily/weekly rates
    - Total crew costs
    
    **Sheet 3: Cast**
    - Character | Scenes | Dialogue
    - Screen time estimates
    - Talent costs
    
    **Sheet 4: Equipment**
    - Package | Item | Rate | Units
    - Camera, lighting, sound packages
    - Rental costs
    """)

with col_b:
    st.markdown("""
    **Sheet 5: Locations**
    - Location | Scenes | Costs
    - Scout, permit, location fees
    - Per-location breakdown
    
    **Sheet 6: Post**
    - Category | Item | Rate | Units
    - Editing, color, sound, VFX
    - Post-production total
    
    **Sheet 7: Insurance**
    - General liability
    - E&O insurance
    - Equipment coverage
    - Contingency (10%)
    
    **Sheet 8: __METADATA** (hidden)
    - Project info, timestamp
    - Version, lock status
    """)

st.divider()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Export Button
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.subheader("🚀 Generate Export")

if st.button("💰 Export Master Budget", type="primary", use_container_width=True):
    with st.spinner("Creating EBP_Master_Budget.xlsx..."):
        try:
            exporter = StudioExcelExporter(project_name=project_name)
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            path = exporter.export_master_budget(st.session_state, output_dir)
            
            st.success(f"✅ Exported: `{Path(path).name}`")
            st.info(f"📁 Saved to: `{Path(path).absolute()}`")
            
            # Download button
            with open(path, "rb") as f:
                st.download_button(
                    label="📥 Download Master Budget",
                    data=f,
                    file_name=Path(path).name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
            st.balloons()
            
        except Exception as e:
            st.error(f"❌ Export failed: {e}")
            with st.expander("🐛 Error Details"):
                st.exception(e)

st.divider()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Quality Standards
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

with st.expander("📋 Quality Standards (Phase 11.1)"):
    st.markdown("""
    ### Core Rule
    **One row = one real-world line item**
    
    ### What You Get
    - ✅ Opens cleanly in Excel, Numbers, Google Sheets
    - ✅ No nested dictionaries or JSON blobs
    - ✅ No developer-style structures
    - ✅ Currency normalized to numbers (no $ in cells)
    - ✅ Fixed sheet names (no user input)
    - ✅ Hidden metadata for audit trail
    
    ### Studio-Ready Guarantee
    - No formatting fixes required
    - No explanations needed
    - Accountant can immediately use it
    - Professional presentation
    
    ### Validation Rules
    - No empty headers
    - No dicts/lists inside cells
    - Dates in ISO format
    - All costs in numbers
    - Standard industry format
    """)

with st.expander("🎯 Audience & Use Cases"):
    st.markdown("""
    ### Primary Audience
    - Producers
    - Studio Executives
    - Production Accountants
    - Line Producers
    
    ### Use Cases
    - Budget approvals
    - Studio greenlight presentations
    - Accounting system imports
    - Financial planning
    - Insurance underwriting
    - Funding applications
    
    ### Next Steps After Export
    1. Review all 7 sheets
    2. Verify crew/cast rates
    3. Confirm equipment packages
    4. Check location costs
    5. Validate post-production estimates
    6. Share with accounting team
    """)

st.caption("Enhanced Budget Pro v1.0.0 | Phase 11.1 - Master Budget Export")
