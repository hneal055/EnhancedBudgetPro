import streamlit as st
import pandas as pd
from src.ui.global_sidebar import install_global_sidebar
install_global_sidebar()

from src.IngestEngine.plaintext_loader import PlainTextLoader
from src.AnalysisEngine.character_intelligence import CharacterIntelligenceEngine
from src.AnalysisEngine.scene_density_engine import SceneDensityEngine
from src.validation import validate_parsed_script
from src.errors import ParseError


st.title("🧠 Phase 1–2 — Story Intelligence")

# ---------------------------------------------
# SCRIPT INPUT
# ---------------------------------------------
script_text = st.text_area(
    "Paste Script Here",
    value=st.session_state.get("raw_script", ""),
    height=280,
)

if st.button("Analyze Script"):
    if not script_text.strip():
        st.warning("⚠️ Please paste a script first.")
    else:
        loader = PlainTextLoader()
        parsed = loader.load(script_text)

        try:
            validate_parsed_script(parsed)
        except ParseError as e:
            st.error(f"❌ Validation error: {e}")
            st.stop()

        intel_engine = CharacterIntelligenceEngine()
        density_engine = SceneDensityEngine()

        intel = intel_engine.analyze(parsed)
        density = density_engine.analyze(parsed)

        # Save into session
        st.session_state.raw_script = script_text
        st.session_state.data = parsed
        st.session_state.intel = intel
        st.session_state.density = density

        st.success(f"✅ Script Parsed — {parsed['scene_count']} scenes detected")

# ---------------------------------------------
# OUTPUT PANELS
# ---------------------------------------------
if st.session_state.get("intel") and st.session_state.get("density"):
    intel = st.session_state.intel
    density = st.session_state.density

    st.subheader("🎭 Character Intelligence")

    char_rows = []
    for name, stats in intel["character_stats"].items():
        char_rows.append(
            {
                "Character": name,
                "Scenes": stats.get("scenes", 0),
                "Dialogue Lines": stats.get("dialogue_lines", 0),
                "Est. Screen Time (min)": round(
                    stats.get("estimated_screen_time_min", 0.0), 2
                ),
            }
        )

    if char_rows:
        st.dataframe(pd.DataFrame(char_rows), width="stretch")
    else:
        st.info("No character stats available.")

    st.subheader("🎬 Scene-by-Scene Density")

    density_rows = []
    for scene in density["scene_density"]:
        density_rows.append(
            {
                "Scene": scene.get("heading", scene.get("header", "<unknown>")),
                "Characters": ", ".join(scene["characters"]),
                "Dialogue Lines": scene["dialogue_lines"],
                "Action Lines": scene["action_lines"],
                "Dialogue Density": round(scene["dialogue_density_ratio"], 2),
                "Classification": scene["classification"],
            }
        )

    if density_rows:
        st.dataframe(pd.DataFrame(density_rows), width="stretch")

    totals = density["totals"]
    colA, colB = st.columns(2)
    colA.metric("Total Dialogue Lines", totals.get("total_dialogue_lines", 0))
    colB.metric("Total Action Lines", totals.get("total_action_lines", 0))

else:
    st.info("ℹ️ Paste a script and click **Analyze Script** to activate Story Intelligence.")
