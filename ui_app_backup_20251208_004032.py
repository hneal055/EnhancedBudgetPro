import streamlit as st
import pandas as pd

from src.IngestEngine.plaintext_loader import PlainTextLoader
from src.AnalysisEngine.character_intelligence import CharacterIntelligenceEngine
from src.AnalysisEngine.scene_density_engine import SceneDensityEngine
from src.AnalysisEngine.cost_impact_engine import CharacterCostImpactEngine
from src.AnalysisEngine.burn_rate_engine import BurnRateForecastEngine

from src.ProductionBudgetEngine.crew_budget_engine import CrewBudgetEngine
from src.ProductionBudgetEngine.equipment_budget_engine import EquipmentBudgetEngine
from src.ProductionBudgetEngine.location_budget_engine import LocationBudgetEngine
from src.ProductionBudgetEngine.post_budget_engine import PostProductionBudgetEngine
from src.ProductionBudgetEngine.insurance_contingency_engine import InsuranceContingencyEngine

from src.ExportEngine.production_budget_pdf_exporter import ProductionBudgetPDFExporter

st.set_page_config(page_title="Enhanced Budget Pro", layout="wide")
st.title("🎬 Enhanced Budget Pro — FULL STUDIO BUDGET SYSTEM")

# -------------------------------
# SESSION STATE INIT
# -------------------------------
for key in ["data", "intel", "density", "cost", "burn", "master"]:
    if key not in st.session_state:
        st.session_state[key] = None

# -------------------------------
# SCRIPT INGEST
# -------------------------------
script = st.text_area("Paste Script Here", height=300)

if st.button("Analyze Script"):
    if script.strip():
        loader = PlainTextLoader()
        char_engine = CharacterIntelligenceEngine()
        density_engine = SceneDensityEngine()

        st.session_state.data = loader.load(script)
        st.session_state.intel = char_engine.analyze(st.session_state.data)
        st.session_state.density = density_engine.analyze(st.session_state.data)

        st.success(
            f"✅ Script Parsed — {st.session_state.data['scene_count']} scenes detected"
        )
    else:
        st.warning("⚠️ Please paste a script first.")

# -------------------------------
# PHASE 4A — STORY INTELLIGENCE
# -------------------------------
st.header("🧠 STORY INTELLIGENCE")

if st.session_state.data and st.session_state.intel and st.session_state.density:

    st.subheader("🎭 Character Intelligence")
    char_rows = []
    for name, stats in st.session_state.intel["character_stats"].items():
        char_rows.append({
            "Character": name,
            "Scenes": stats.get("scenes", 0),
            "Dialogue Lines": stats.get("dialogue_lines", 0),
            "Est. Screen Time (min)": round(stats.get("estimated_screen_time_min", 0), 2)
        })

    st.dataframe(pd.DataFrame(char_rows), width="stretch")

    st.subheader("🎬 Scene-by-Scene Density")
    density_rows = []
    for scene in st.session_state.density["scene_density"]:
        density_rows.append({
            "Scene": scene.get("heading", scene.get("header", "<unknown>")),
            "Characters": ", ".join(scene["characters"]),
            "Dialogue": scene["dialogue_lines"],
            "Action": scene["action_lines"],
            "Ratio": round(scene["dialogue_density_ratio"], 2),
            "Type": scene["classification"]
        })

    st.dataframe(pd.DataFrame(density_rows), width="stretch")

else:
    st.info("ℹ️ Run 'Analyze Script' to view Story Intelligence.")

# -------------------------------
# PHASE 4B — FINANCIAL INTELLIGENCE
# -------------------------------
st.header("💰 FINANCIAL INTELLIGENCE")

if st.session_state.data and st.session_state.intel:

    default_rates = {}
    for name in st.session_state.intel["character_stats"].keys():
        default_rates[name] = 1000

    rate_inputs = {}
    for char, rate in default_rates.items():
        rate_inputs[char] = st.number_input(
            f"{char} Daily Rate ($)",
            min_value=100,
            max_value=50000,
            value=rate,
            step=100,
            key=f"rate_{char}"  # ✅ FIXED KEY COLLISION
        )

    cost_engine = CharacterCostImpactEngine()
    st.session_state.cost = cost_engine.analyze(
        st.session_state.intel["character_stats"],
        rate_inputs,
        st.session_state.data["scene_count"]
    )

    burn_engine = BurnRateForecastEngine()
    st.session_state.burn = burn_engine.analyze(
        st.session_state.data["scenes"],
        st.session_state.cost["character_costs"]
    )

    st.dataframe(
        pd.DataFrame([
            {
                "Character": char,
                "Rate": info["daily_rate"],
                "Days": info["estimated_days"],
                "Total": info["estimated_total_cost"]
            }
            for char, info in st.session_state.cost["character_costs"].items()
        ]),
        width="stretch"
    )

    st.metric(
        "Total Estimated Cast Cost",
        f"${st.session_state.cost['total_estimated_cast_cost']:,.2f}"
    )

else:
    st.info("ℹ️ Run 'Analyze Script' first to activate Financial Intelligence.")

# -------------------------------
# PHASE 3 — MASTER STUDIO BUDGET
# -------------------------------
st.header("🏗 MASTER STUDIO PRODUCTION BUDGET")

shoot_days = st.slider("Total Shoot Days", 5, 120, 30)

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
    crew_budget["total_crew_cost"]
    + equipment_budget["total_equipment_cost"]
    + location_budget["total_location_cost"]
    + post_budget["total_post_cost"]
)

insurance = insurance_engine.calculate(core_total)
final_budget = core_total + insurance["insurance_total"] + insurance["contingency_buffer"]

col1, col2, col3 = st.columns(3)
col1.metric("Crew", f"${crew_budget['total_crew_cost']:,.2f}")
col2.metric("Equipment", f"${equipment_budget['total_equipment_cost']:,.2f}")
col3.metric("Locations", f"${location_budget['total_location_cost']:,.2f}")

st.metric("✅ FINAL STUDIO BUDGET", f"${final_budget:,.2f}")

# -------------------------------
# PDF EXPORT
# -------------------------------
st.subheader("📄 Final Budget PDF Export")

if st.button("Generate Final Budget PDF"):
    exporter = ProductionBudgetPDFExporter()
    exporter.export(
        {
            "crew": crew_budget,
            "equipment": equipment_budget,
            "locations": location_budget,
            "post": post_budget,
            "insurance": insurance,
            "final_production_budget": final_budget
        },
        "FINAL_PRODUCTION_BUDGET_UI.pdf"
    )

    st.success("✅ FINAL_PRODUCTION_BUDGET_UI.pdf Generated Successfully")
