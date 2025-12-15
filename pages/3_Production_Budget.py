import streamlit as st
from src.ui.global_sidebar import install_global_sidebar
install_global_sidebar()

from src.ProductionBudgetEngine.crew_budget_engine import CrewBudgetEngine
from src.ProductionBudgetEngine.equipment_budget_engine import (
    EquipmentBudgetEngine,
)
from src.ProductionBudgetEngine.location_budget_engine import (
    LocationBudgetEngine,
)
from src.ProductionBudgetEngine.post_budget_engine import (
    PostProductionBudgetEngine,
)
from src.ProductionBudgetEngine.insurance_contingency_engine import (
    InsuranceContingencyEngine,
)
from src.ExportEngine.production_budget_pdf_exporter import (
    ProductionBudgetPDFExporter,
)

st.title("🏗 Phase 3 — Master Studio Production Budget")

# Auto-detect shoot days from session data if available
default_days = 30
if st.session_state.get("data"):
    scene_count = st.session_state.data.get("scene_count", 0)
    if scene_count > 0:
        # Estimate: 1-2 scenes per day for small scripts
        default_days = max(1, min(scene_count, 30))

shoot_days = st.slider(
    "Total Shoot Days",
    min_value=1,
    max_value=120,
    value=default_days,
    help="Adjust based on script complexity and schedule"
)

crew_engine = CrewBudgetEngine()
equipment_engine = EquipmentBudgetEngine()
location_engine = LocationBudgetEngine()
post_engine = PostProductionBudgetEngine()
insurance_engine = InsuranceContingencyEngine()

crew_budget = crew_engine.calculate(shoot_days)
equipment_budget = equipment_engine.calculate(shoot_days)
location_budget = location_engine.calculate(shoot_days)
post_budget = post_engine.calculate()

core_total = (
    crew_budget.get("total_crew_cost", 0.0)
    + equipment_budget.get("total_equipment_cost", 0.0)
    + location_budget.get("total_location_cost", 0.0)
    + post_budget.get("total_post_cost", 0.0)
)

insurance = insurance_engine.calculate(core_total)
final_budget = (
    core_total
    + insurance.get("insurance_total", 0.0)
    + insurance.get("contingency_buffer", 0.0)
)

col1, col2, col3 = st.columns(3)
col1.metric(
    "Crew Total",
    f"${crew_budget.get('total_crew_cost', 0.0):,.2f}"
)
col2.metric(
    "Equipment Total",
    f"${equipment_budget.get('total_equipment_cost', 0.0):,.2f}"
)
col3.metric(
    "Location Total",
    f"${location_budget.get('total_location_cost', 0.0):,.2f}"
)

col4, col5, col6 = st.columns(3)
col4.metric(
    "Post Production",
    f"${post_budget.get('total_post_cost', 0.0):,.2f}"
)
col5.metric(
    "Insurance",
    f"${insurance.get('insurance_total', 0.0):,.2f}"
)
col6.metric(
    "Contingency",
    f"${insurance.get('contingency_buffer', 0.0):,.2f}"
)

st.subheader("🎯 FINAL STUDIO BUDGET")
st.metric("✅ GRAND TOTAL", f"${final_budget:,.2f}")

# Store into session for other pages + exporters
st.session_state.master = {
    "crew": crew_budget,
    "equipment": equipment_budget,
    "locations": location_budget,
    "post": post_budget,
    "insurance": insurance,
    "final_production_budget": final_budget,
    "core_production_total": core_total,
    "shoot_days": shoot_days,
}

# Legacy key for backward compatibility
st.session_state.master_budget = st.session_state.master

st.subheader("📄 Final Budget PDF Export")

if st.button("Generate Final Budget PDF"):
    try:
        exporter = ProductionBudgetPDFExporter()
        exporter.export(
            st.session_state.master,
            "FINAL_PRODUCTION_BUDGET_UI.pdf",
        )
        st.success("✅ FINAL_PRODUCTION_BUDGET_UI.pdf generated.")
    except Exception as e:
        st.error(f"❌ Error generating PDF: {e}")
