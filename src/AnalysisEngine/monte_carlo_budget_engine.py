import streamlit as st

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Enhanced Budget Pro",
    layout="wide"
)

st.title("🎬 Enhanced Budget Pro — Stable Core UI")
st.info("✅ Recovery Mode Active — All advanced modules will load safely as they become available.")

# -----------------------------
# SAFE ENGINE IMPORTS
# -----------------------------

ENGINES = {}

def safe_import(name, path):
    try:
        module = __import__(path, fromlist=[name])
        ENGINES[name] = getattr(module, name)
        return True
    except Exception as e:
        ENGINES[name] = None
        st.warning(f"⚠️ Engine not loaded: {name}")
        return False


safe_import("PlainTextLoader", "src.IngestEngine.plaintext_loader")
safe_import("CharacterIntelligenceEngine", "src.AnalysisEngine.character_intelligence")
safe_import("SceneDensityEngine", "src.AnalysisEngine.scene_density_engine")
safe_import("CharacterCostImpactEngine", "src.AnalysisEngine.cost_impact_engine")
safe_import("BurnRateForecastEngine", "src.AnalysisEngine.burn_rate_engine")

# -----------------------------
# SCRIPT INPUT
# -----------------------------

st.subheader("📄 Script Input")

script_text = st.text_area(
    "Paste your script here:",
    height=300
)

run_btn = st.button("🚀 Analyze Script")

# -----------------------------
# ANALYSIS PIPELINE
# -----------------------------

if run_btn:

    if not script_text.strip():
        st.error("❌ Please paste a screenplay first.")
        st.stop()

    loader = ENGINES.get("PlainTextLoader")
    intel_engine = ENGINES.get("CharacterIntelligenceEngine")
    density_engine = ENGINES.get("SceneDensityEngine")
    cost_engine = ENGINES.get("CharacterCostImpactEngine")
    burn_engine = ENGINES.get("BurnRateForecastEngine")

    if not loader:
        st.error("❌ PlainTextLoader not available.")
        st.stop()

    data = loader().load(script_text)

    st.success("✅ Script successfully parsed.")
    st.write("Scenes Detected:", data.get("scene_count", 0))

    # -----------------------------
    # CHARACTER INTELLIGENCE
    # -----------------------------
    if intel_engine:
        st.subheader("🎭 Character Intelligence")
        intel = intel_engine().analyze(data)
        st.dataframe(intel["character_stats"])

    # -----------------------------
    # SCENE DENSITY
    # -----------------------------
    if density_engine:
        st.subheader("🎬 Scene Density")
        density = density_engine().analyze(data)
        st.dataframe(density["scene_density"])

    # -----------------------------
    # CAST COST INPUT
    # -----------------------------
    if cost_engine and intel_engine:

        st.subheader("💰 Cast Cost Estimation")

        rates = {}
        for character in intel["character_stats"].keys():
            rates[character] = st.number_input(
                f"Daily Rate for {character}",
                min_value=100,
                max_value=10000,
                value=1000,
                step=100
            )

        if st.button("📊 Calculate Cast Cost"):

            cost = cost_engine().analyze(
                intel["character_stats"],
                rates,
                data["scene_count"]
            )

            st.success("✅ Cast cost calculated.")
            st.dataframe(cost["character_costs"])
            st.write("🎯 Total Cast Cost:", cost["total_estimated_cast_cost"])

    # -----------------------------
    # BURN RATE FORECAST
    # -----------------------------
    if burn_engine and cost_engine and intel_engine:

        st.subheader("🔥 Burn Rate Forecast")

        burn = burn_engine().analyze(
            data["scenes"],
            cost["character_costs"]
        )

        st.dataframe(burn["daily_schedule"])
        st.write("📈 Average Daily Burn:", burn["average_daily_burn"])
        st.write("⚠️ Peak Burn Day:", burn["peak_burn_day"])

# -----------------------------
# FOOTER
# -----------------------------

st.divider()
st.caption("Enhanced Budget Pro — Stable UI Core | Phase 3 Ready ✅")

