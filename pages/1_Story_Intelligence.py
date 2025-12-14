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
        # Phase 13.1 Week 3: Create progress placeholder
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
            
            # Phase 13.1 Week 3: Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
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
        char_df = pd.DataFrame(char_rows)
        st.dataframe(char_df, width="stretch")

    st.subheader("🎬 Scene Density Breakdown")

    scene_rows = []
    for s in density["scene_breakdown"]:
        scene_rows.append(
            {
                "Scene": s["scene_heading"],
                "Total Lines": s.get("total_lines", 0),
                "Dialogue Lines": s.get("dialogue_lines", 0),
                "Action Lines": s.get("action_lines", 0),
                "Classification": s.get("classification", "UNKNOWN"),
            }
        )

    if scene_rows:
        scene_df = pd.DataFrame(scene_rows)
        st.dataframe(scene_df, width="stretch")

    # Phase 13.1: Show emotion preview if available
    if st.session_state.get("emotion_data"):
        emotion_data = st.session_state.emotion_data
        st.subheader("🧠 Emotional Intelligence Preview")
        
        summary = emotion_data.get("summary", {})
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Scenes Analyzed", summary.get("total_scenes_analyzed", 0))
        with col2:
            st.metric("Character Arcs", summary.get("characters_with_arcs", 0))
        with col3:
            avg_intensity = summary.get("average_intensity", 0)
            st.metric("Avg Intensity", f"{avg_intensity:.1f}")
        
        st.info("💡 Visit **Emotional Intelligence Dashboard** (Page 14) for detailed analysis")
