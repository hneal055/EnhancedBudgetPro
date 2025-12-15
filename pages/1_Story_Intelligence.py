import streamlit as st
import pandas as pd
import tempfile
import os
from src.ui.global_sidebar import install_global_sidebar
install_global_sidebar()

from src.ScriptIngest import parse_script, analyze_emotions
from src.AnalysisEngine.character_intelligence import CharacterIntelligenceEngine
from src.AnalysisEngine.scene_density_engine import SceneDensityEngine

st.title("🧠 Phase 1–2 — Story Intelligence")

# ---------------------------------------------
# SCRIPT INPUT
# ---------------------------------------------

# Callback to cache file immediately when uploaded
def cache_uploaded_file():
    if st.session_state.file_uploader is not None:
        file = st.session_state.file_uploader
        st.session_state.cached_file_content = file.getvalue()
        st.session_state.cached_file_name = file.name
        st.session_state.cached_file_ext = os.path.splitext(file.name)[1]

# Add file upload with callback
uploaded_file = st.file_uploader(
    "Upload Script File",
    type=["fdx", "fountain", "txt", "pdf"],
    help="Upload a Final Draft (.fdx), Fountain, plain text, or PDF script file",
    key="file_uploader",
    on_change=cache_uploaded_file
)

# Show cached file info
if st.session_state.get("cached_file_name"):
    st.info(f"📄 Ready to analyze: {st.session_state.cached_file_name}")

st.markdown("**OR**")

script_text = st.text_area(
    "Paste Script Here",
    value=st.session_state.get("raw_script", "") if not uploaded_file else "",
    height=280,
    disabled=uploaded_file is not None,
    help="Paste plain text screenplay if not uploading a file"
)

if st.button("Analyze Script", type="primary"):
    # DEBUG - show cache state    if st.session_state.get("cached_file_content"):    
    # Determine input source - check cached file first
    if st.session_state.get("cached_file_content") is not None:
        input_source = "file"
    elif script_text.strip():
        input_source = "text"
    else:
        st.warning("⚠️ Please upload a file or paste script text.")
        st.stop()
    
# Create progress indicators
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        if input_source == "file":
            # Use cached file data
            file_name = st.session_state.cached_file_name
            file_content = st.session_state.cached_file_content
            file_ext = st.session_state.cached_file_ext
            
            status_text.text(f"📄 Processing {file_name}...")
            progress_bar.progress(10)
            
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(mode='wb', suffix=file_ext, delete=False) as tmp:
                tmp.write(file_content)
                tmp_path = tmp.name
            
            # DEBUG        
        else:  # text input
            status_text.text("📝 Preparing script...")
            progress_bar.progress(10)
            
            # Create temporary file for script
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
                tmp.write(script_text)
                tmp_path = tmp.name
        
        status_text.text("🔍 Parsing script structure...")
        progress_bar.progress(30)
        
        # Parse script
        parsed = parse_script(tmp_path)
        
        if parsed["scene_count"] == 0:
            st.error("❌ No scenes detected. Please check your script format.")
            st.stop()
        
        status_text.text("🧠 Analyzing emotional intelligence...")
        progress_bar.progress(50)
        
        # Analyze emotions
        emotion_data = analyze_emotions(parsed["scenes"], parsed["characters"])
        
        status_text.text("📊 Running character intelligence analysis...")
        progress_bar.progress(70)
        
        # Run intelligence engines
        intel_engine = CharacterIntelligenceEngine()
        density_engine = SceneDensityEngine()
        
        intel = intel_engine.analyze(parsed)
        density = density_engine.analyze(parsed)
        
        status_text.text("💾 Saving results...")
        progress_bar.progress(90)
        
        # Save into session
        if input_source == "text":
            st.session_state.raw_script = script_text
        st.session_state.data = parsed
        st.session_state.intel = intel
        st.session_state.density = density
        st.session_state.emotion_data = emotion_data
        
        status_text.text("✅ Analysis complete!")
        progress_bar.progress(100)
        
        # Show success with emotion stats
        emotion_summary = emotion_data.get("summary", {})
        scenes_analyzed = emotion_summary.get("total_scenes_analyzed", 0)
        char_arcs = len(emotion_data.get("character_arcs", {}))
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        st.success(
            f"✅ Script Parsed — {parsed['scene_count']} scenes detected\n\n"
            f"🧠 Emotional Intelligence: {scenes_analyzed} scenes analyzed, {char_arcs} character arcs tracked"
        )
        
    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"❌ Analysis error: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
        
    finally:
        # Cleanup temporary files
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
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
        st.dataframe(char_df, use_container_width=True)

    st.subheader("🎬 Scene Density Breakdown")

    scene_rows = []
    for s in density.get("scene_breakdown", []):
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
        st.dataframe(scene_df, use_container_width=True)

    # Show emotion preview if available
    if st.session_state.get("emotion_data"):
        emotion_data = st.session_state.emotion_data
        st.subheader("🧠 Emotional Intelligence Preview")
        
        summary = emotion_data.get("summary", {})
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Scenes Analyzed", summary.get("total_scenes_analyzed", 0))
        with col2:
            st.metric("Character Arcs", len(emotion_data.get("character_arcs", {})))
        with col3:
            avg_intensity = summary.get("average_intensity", 0)
            st.metric("Avg Intensity", f"{avg_intensity:.1f}")
        
        st.info("💡 Visit **Emotional Intelligence Dashboard** (Page 14) or **Character Arc Suite** (Page 15) for detailed analysis")
