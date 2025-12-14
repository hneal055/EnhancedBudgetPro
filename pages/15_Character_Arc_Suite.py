"""
Page 15: Character Arc Visualization Suite
Phase 13.2: Advanced character development analysis and storytelling insights
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Character Arc Suite", layout="wide")

st.title("🎭 Character Arc Visualization Suite")
st.caption("Advanced character development analysis powered by AI")

# Check prerequisites
if not st.session_state.get("data"):
    st.error("⚠️ No script data available. Please parse a script on Page 1 first.")
    st.stop()

if not st.session_state.get("emotion_data"):
    st.warning("⚠️ Emotional intelligence analysis required. This should happen automatically during script parsing.")
    st.info("💡 Try re-uploading your script on Page 1 to trigger emotional analysis.")
    st.stop()

# Import arc engines
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.CharacterArcEngine.arc_classifier import ArcClassifier

emotion_data = st.session_state.emotion_data
character_arcs = emotion_data.get("character_arcs", {})

if not character_arcs:
    st.error("⚠️ No character arcs found in emotion data.")
    st.stop()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ARC TYPE CLASSIFICATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.header("🎯 Character Arc Classification")
st.markdown("Automatically identify storytelling patterns: Hero's Journey, Redemption, Fall from Grace, and more.")

# Classify all character arcs
classifier = ArcClassifier()
arc_classifications = classifier.classify_all_characters(character_arcs)

# Filter out insufficient data
valid_classifications = {
    char: classif for char, classif in arc_classifications.items()
    if classif["arc_type"] != "insufficient_data"
}

if not valid_classifications:
    st.warning("⚠️ No characters have enough scenes for arc classification (minimum 3 scenes required).")
else:
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Characters Classified", len(valid_classifications))
    
    with col2:
        # Most common arc type
        arc_types = [c["arc_name"] for c in valid_classifications.values()]
        if arc_types:
            most_common = max(set(arc_types), key=arc_types.count)
            st.metric("Most Common Arc", most_common)
    
    with col3:
        # Average confidence
        avg_confidence = sum(c["confidence"] for c in valid_classifications.values()) / len(valid_classifications)
        st.metric("Avg Confidence", f"{avg_confidence:.1f}%")
    
    with col4:
        # High volatility count
        high_vol_count = sum(1 for c in character_arcs.values() if c.get("emotional_volatility", 0) > 60)
        st.metric("High Volatility Arcs", high_vol_count)
    
    st.divider()
    
    # Arc Type Distribution
    col_chart, col_table = st.columns([1, 1])
    
    with col_chart:
        st.subheader("📊 Arc Type Distribution")
        
        arc_type_counts = {}
        for classif in valid_classifications.values():
            arc_name = classif["arc_name"]
            arc_type_counts[arc_name] = arc_type_counts.get(arc_name, 0) + 1
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=list(arc_type_counts.keys()),
            values=list(arc_type_counts.values()),
            hole=0.4,
            marker=dict(colors=px.colors.qualitative.Set3)
        )])
        
        fig_pie.update_layout(
            title="Arc Types in Script",
            height=400
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col_table:
        st.subheader("📋 Arc Classification Summary")
        
        summary_rows = []
        for char, classif in sorted(valid_classifications.items(), key=lambda x: x[1]["confidence"], reverse=True):
            summary_rows.append({
                "Character": char,
                "Arc Type": f"{classif['emoji']} {classif['arc_name']}",
                "Confidence": f"{classif['confidence']:.1f}%",
                "Volatility": f"{character_arcs[char].get('emotional_volatility', 0):.1f}"
            })
        
        if summary_rows:
            df_summary = pd.DataFrame(summary_rows)
            st.dataframe(df_summary, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Detailed Character Arc Analysis
    st.subheader("🔍 Detailed Arc Analysis")
    
    selected_char = st.selectbox(
        "Select Character",
        options=list(valid_classifications.keys()),
        key="arc_detail_char"
    )
    
    if selected_char:
        classif = arc_classifications[selected_char]
        char_arc = character_arcs[selected_char]
        
        # Character arc card
        col_info, col_metrics = st.columns([2, 1])
        
        with col_info:
            st.markdown(f"### {classif['emoji']} {classif['arc_name']}")
            st.markdown(f"**Pattern:** {classif['pattern']}")
            st.markdown(f"**Description:** {classif['description']}")
            st.markdown(f"**Confidence:** {classif['confidence']:.1f}%")
            
            # Arc type scores (alternative classifications)
            st.markdown("**Alternative Arc Types:**")
            all_scores = classif.get("all_scores", {})
            sorted_scores = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)
            
            for arc_type, score in sorted_scores[:3]:
                arc_info = classifier.ARC_TYPES.get(arc_type, {})
                arc_name = arc_info.get("name", arc_type)
                arc_emoji = arc_info.get("emoji", "")
                
                if score > 0:
                    st.markdown(f"- {arc_emoji} {arc_name}: {score:.1f}%")
        
        with col_metrics:
            st.markdown("**Arc Metrics:**")
            metrics = classif.get("metrics", {})
            
            st.metric("Intensity Change", f"{metrics.get('intensity_delta', 0):+.1f}")
            st.metric("Tension Change", f"{metrics.get('tension_delta', 0):+.1f}")
            st.metric("Emotional Volatility", f"{metrics.get('volatility', 0):.1f}")
            st.metric("Emotional Range", f"{metrics.get('range_diversity', 0)} emotions")
        
        # Emotional trajectory with arc overlay
        st.markdown("#### Emotional Trajectory")
        
        arc_scenes = char_arc.get("arc", [])
        if arc_scenes:
            intensities = [s.get("intensity", 0) for s in arc_scenes]
            tensions = [s.get("tension", 0) for s in arc_scenes]
            scene_nums = list(range(1, len(arc_scenes) + 1))
            
            fig_traj = go.Figure()
            
            # Intensity line
            fig_traj.add_trace(go.Scatter(
                x=scene_nums,
                y=intensities,
                mode="lines+markers",
                name="Intensity",
                line=dict(color="#FF6B6B", width=3),
                marker=dict(size=8)
            ))
            
            # Tension line
            fig_traj.add_trace(go.Scatter(
                x=scene_nums,
                y=tensions,
                mode="lines+markers",
                name="Tension",
                line=dict(color="#4ECDC4", width=3, dash="dash"),
                marker=dict(size=8)
            ))
            
            # Peak marker
            peak_location = metrics.get("peak_location", 0.5)
            peak_idx = int(peak_location * len(intensities))
            if 0 <= peak_idx < len(intensities):
                fig_traj.add_trace(go.Scatter(
                    x=[peak_idx + 1],
                    y=[intensities[peak_idx]],
                    mode="markers+text",
                    name="Peak Crisis",
                    marker=dict(size=20, color="#FFD700", symbol="star"),
                    text=["Peak"],
                    textposition="top center"
                ))
            
            fig_traj.update_layout(
                title=f"{selected_char}'s Emotional Journey",
                xaxis_title="Scene Appearance #",
                yaxis_title="Score (0-100)",
                height=400,
                hovermode="x unified"
            )
            
            st.plotly_chart(fig_traj, use_container_width=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# COMING SOON
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.divider()

st.header("🚀 Coming Soon")

col1, col2 = st.columns(2)

with col1:
    st.info("""
    **📊 Character Comparison**
    - Side-by-side arc analysis
    - Interaction heatmaps
    - Development rate comparison
    """)
    
    st.info("""
    **🔮 Arc Completion Predictor**
    - Forecast arc resolution
    - Missing beats identification
    - Pacing analysis
    """)

with col2:
    st.info("""
    **💞 Relationship Evolution**
    - Animated relationship network
    - Sentiment trajectory
    - Influence analysis
    """)
    
    st.info("""
    **✅ Consistency Analyzer**
    - Out-of-character detection
    - Behavior pattern analysis
    - Deviation warnings
    """)
