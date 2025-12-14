import streamlit as st
import pandas as pd
import tempfile
import os
from src.ui.global_sidebar import install_global_sidebar
install_global_sidebar()

from src.IngestEngine.plaintext_loader import PlainTextLoader
from src.AnalysisEngine.character_intelligence import CharacterIntelligenceEngine
from src.AnalysisEngine.scene_density_engine import SceneDensityEngine
from src.validation import validate_parsed_script
from src.errors import ParseError
from src.ScriptIngest import run_full_analysis  # Phase 13.1: Use full pipeline


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
        # Create progress placeholder
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("📝 Preparing script...")
            progress_bar.progress(10)
            
            # Create temporary file for script
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
                tmp.write(script_text)
                tmp_path = tmp.name
            
            status_text.text("🔍 Parsing script structure...")
            progress_bar.progress(20)
            
            # Create temporary output directory
            output_dir = tempfile.mkdtemp()
            
            status_text.text("📊 Running analysis pipeline...")
            progress_bar.progress(40)
            
            # Use full analysis pipeline (includes emotion analysis)
            result = run_full_analysis(tmp_path, output_dir)
            
            status_text.text("🧠 Processing emotional intelligence...")
            progress_bar.progress(80)
                
                if "error" in result:
                    st.error(f"❌ Analysis error: {result['error']}")
                    st.stop()
                
                # Extract components
                parsed = {
                    "scenes": result["scenes"],
                    "characters": result["characters"],
                    "scene_count": len(result["scenes"])
                }
                
                # Run intelligence engines on parsed data
                intel_engine = CharacterIntelligenceEngine()
                density_engine = SceneDensityEngine()
                
                intel = intel_engine.analyze(parsed)
                density = density_engine.analyze(parsed)
                
                # Save into session
                st.session_state.raw_script = script_text
                st.session_state.data = parsed
                st.session_state.intel = intel
                st.session_state.density = density
                st.session_state.emotion_data = result.get("emotion_data")  # Phase 13.1: Store emotion data
                
                status_text.text("✅ Analysis complete!")
                progress_bar.progress(100)
                
                # Show success with emotion stats
                emotion_summary = result.get("emotion_data", {}).get("summary", {})
                scenes_analyzed = emotion_summary.get("total_scenes_analyzed", 0)
                char_arcs = emotion_summary.get("characters_with_arcs", 0)
                
                st.success(
                    f"✅ Script Parsed — {parsed['scene_count']} scenes detected\n\n"
                    f"🧠 Emotional Intelligence: {scenes_analyzed} scenes analyzed, {char_arcs} character arcs tracked"
                )
                
            finally:
                # Cleanup temporary files
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)

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
    
    # Phase 13.1: Show emotion preview
    if st.session_state.emotion_data:
        st.divider()
        st.subheader("🧠 Emotional Intelligence Preview")
        
        emotion_summary = st.session_state.emotion_data.get("summary", {})
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Avg Intensity", f"{emotion_summary.get('average_intensity', 0):.1f}/100")
        with col2:
            st.metric("Avg Tension", f"{emotion_summary.get('average_tension', 0):.1f}/100")
        with col3:
            st.metric("Character Arcs", emotion_summary.get("characters_with_arcs", 0))
        
        st.info("💡 Visit **Page 14: Emotional Intelligence** for detailed character arc analysis and scene intensity charts.")

else:
    st.info("ℹ️ Paste a script and click **Analyze Script** to activate Story Intelligence.")
