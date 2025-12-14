"""
Page 14: Emotional Intelligence Dashboard
Phase 13.1: Emotional Intelligence Layer

Visualizes emotional patterns in the script:
- Character emotional arcs
- Scene intensity heatmaps
- Tension patterns across script
- Emotional turning points
- Character relationship dynamics
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Emotional Intelligence", layout="wide")

st.title("🧠 Emotional Intelligence Dashboard")

# Check prerequisites
if not st.session_state.data:
    st.error("⚠️ No script data available. Please parse a script on Page 1 first.")
    st.stop()

if not st.session_state.emotion_data:
    st.warning("⚠️ Emotional intelligence analysis not yet run. This should happen automatically during script parsing.")
    st.info("💡 Try re-uploading your script on Page 1 to trigger emotional analysis.")
    st.stop()

emotion_data = st.session_state.emotion_data
scene_emotions = emotion_data.get("scene_emotions", [])
character_arcs = emotion_data.get("character_arcs", {})
turning_points = emotion_data.get("turning_points", {})
summary = emotion_data.get("summary", {})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# OVERVIEW METRICS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.header("📊 Emotional Overview")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Scenes Analyzed",
        summary.get("total_scenes_analyzed", 0),
        help="Total scenes with emotional analysis"
    )

with col2:
    st.metric(
        "Avg Intensity",
        f"{summary.get('average_intensity', 0):.1f}/100",
        help="Average emotional intensity across all scenes (0-100)"
    )

with col3:
    st.metric(
        "Avg Tension",
        f"{summary.get('average_tension', 0):.1f}/100",
        help="Average tension level across all scenes (0-100)"
    )

with col4:
    st.metric(
        "Character Arcs",
        summary.get("characters_with_arcs", 0),
        help="Number of characters with tracked emotional arcs"
    )

with col5:
    st.metric(
        "Turning Points",
        summary.get("total_turning_points", 0),
        help="Total emotional turning points identified"
    )

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EMOTION DISTRIBUTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.header("🎭 Emotion Distribution Across Script")

emotion_dist = summary.get("emotion_distribution", {})
if emotion_dist:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Pie chart
        fig_pie = go.Figure(data=[go.Pie(
            labels=list(emotion_dist.keys()),
            values=list(emotion_dist.values()),
            hole=0.3,
            marker=dict(colors=px.colors.qualitative.Set2)
        )])
        fig_pie.update_layout(
            title="Dominant Emotions Across All Scenes",
            height=400
        )
        st.plotly_chart(fig_pie, width='stretch')
    
    with col2:
        st.subheader("Emotion Counts")
        for emotion, count in sorted(emotion_dist.items(), key=lambda x: x[1], reverse=True):
            pct = (count / summary.get("total_scenes_analyzed", 1)) * 100
            st.write(f"**{emotion.title()}**: {count} scenes ({pct:.1f}%)")
else:
    st.info("No emotion distribution data available.")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SCENE INTENSITY & TENSION HEATMAP
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.header("🔥 Scene Intensity & Tension Analysis")

if scene_emotions:
    # Create dataframe for plotting
    scene_df = pd.DataFrame([
        {
            "Scene": i + 1,
            "Heading": se["scene_heading"][:40] + "..." if len(se["scene_heading"]) > 40 else se["scene_heading"],
            "Intensity": se["intensity"],
            "Tension": se["tension"],
            "Dominant Emotion": se["dominant_emotion"]
        }
        for i, se in enumerate(scene_emotions)
    ])
    
    # Dual-axis line chart
    fig_intensity = go.Figure()
    
    fig_intensity.add_trace(go.Scatter(
        x=scene_df["Scene"],
        y=scene_df["Intensity"],
        name="Intensity",
        mode="lines+markers",
        line=dict(color="red", width=2),
        hovertemplate="Scene %{x}<br>Intensity: %{y:.1f}<extra></extra>"
    ))
    
    fig_intensity.add_trace(go.Scatter(
        x=scene_df["Scene"],
        y=scene_df["Tension"],
        name="Tension",
        mode="lines+markers",
        line=dict(color="orange", width=2),
        hovertemplate="Scene %{x}<br>Tension: %{y:.1f}<extra></extra>"
    ))
    
    fig_intensity.update_layout(
        title="Intensity & Tension Across Script",
        xaxis_title="Scene Number",
        yaxis_title="Score (0-100)",
        height=400,
        hovermode="x unified"
    )
    
    st.plotly_chart(fig_intensity, width='stretch')
    
    # Show top 10 most intense scenes
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔥 Top 10 Most Intense Scenes")
        top_intensity = scene_df.nlargest(10, "Intensity")
        for _, row in top_intensity.iterrows():
            st.write(f"**Scene {row['Scene']}** ({row['Intensity']:.1f}): {row['Heading']}")
    
    with col2:
        st.subheader("⚡ Top 10 Highest Tension Scenes")
        top_tension = scene_df.nlargest(10, "Tension")
        for _, row in top_tension.iterrows():
            st.write(f"**Scene {row['Scene']}** ({row['Tension']:.1f}): {row['Heading']}")
else:
    st.info("No scene emotion data available.")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CHARACTER EMOTIONAL ARCS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.header("🎭 Character Emotional Arcs")

if character_arcs:
    # Character selector
    selected_char = st.selectbox(
        "Select Character",
        options=sorted(character_arcs.keys()),
        help="Choose a character to view their emotional journey"
    )
    
    if selected_char:
        char_data = character_arcs[selected_char]
        arc = char_data.get("arc", [])
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Scenes", char_data.get("total_scenes", 0))
        
        with col2:
            st.metric("Scenes with Dialogue", char_data.get("scenes_with_dialogue", 0))
        
        with col3:
            st.metric("Dominant Emotion", char_data.get("dominant_emotion", "neutral").title())
        
        with col4:
            st.metric("Emotional Volatility", f"{char_data.get('emotional_volatility', 0):.1f}/100")
        
        # Emotional range
        emotional_range = char_data.get("emotional_range", [])
        if emotional_range:
            st.write(f"**Emotional Range**: {', '.join([e.title() for e in emotional_range])}")
        
        # Arc visualization
        if arc:
            arc_df = pd.DataFrame([
                {
                    "Scene": i + 1,
                    "Heading": entry["scene"][:40] + "..." if len(entry["scene"]) > 40 else entry["scene"],
                    "Emotion": entry["dominant_emotion"],
                    "Dialogue Lines": entry["dialogue_lines"]
                }
                for i, entry in enumerate(arc)
            ])
            
            # Emotion timeline
            fig_arc = go.Figure()
            
            # Map emotions to colors
            emotion_colors = {
                "joy": "gold",
                "sadness": "blue",
                "anger": "red",
                "fear": "purple",
                "surprise": "orange",
                "disgust": "green",
                "neutral": "gray"
            }
            
            fig_arc.add_trace(go.Scatter(
                x=arc_df["Scene"],
                y=arc_df["Emotion"],
                mode="lines+markers",
                marker=dict(
                    size=arc_df["Dialogue Lines"] * 2,  # Size by dialogue
                    color=[emotion_colors.get(e, "gray") for e in arc_df["Emotion"]],
                ),
                line=dict(color="lightgray", width=1),
                hovertemplate="Scene %{x}<br>%{y}<br>Dialogue Lines: %{marker.size}<extra></extra>"
            ))
            
            fig_arc.update_layout(
                title=f"{selected_char}'s Emotional Journey",
                xaxis_title="Scene Number",
                yaxis_title="Emotion",
                height=400
            )
            
            st.plotly_chart(fig_arc, width='stretch')
            
            # Turning points
            if selected_char in turning_points:
                st.subheader(f"🔄 {selected_char}'s Emotional Turning Points")
                char_turning = turning_points[selected_char]
                
                for i, tp in enumerate(char_turning[:5], 1):  # Show top 5
                    with st.expander(f"#{i}: {tp['scene']} (Impact: {tp['impact']:.1f})"):
                        st.write(f"**From**: {tp['from_emotion'].title()}")
                        st.write(f"**To**: {tp['to_emotion'].title()}")
                        st.write(f"**Impact Score**: {tp['impact']:.1f}/100")
else:
    st.info("No character emotional arc data available.")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXPORT OPTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.header("💾 Export Emotional Intelligence Data")

col1, col2 = st.columns(2)

with col1:
    if st.button("📊 Download Scene Emotions (CSV)"):
        if scene_emotions:
            df = pd.DataFrame(scene_emotions)
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="scene_emotions.csv",
                mime="text/csv"
            )

with col2:
    if st.button("🎭 Download Character Arcs (CSV)"):
        if character_arcs:
            # Flatten character arcs into rows
            rows = []
            for char, data in character_arcs.items():
                rows.append({
                    "Character": char,
                    "Total Scenes": data.get("total_scenes", 0),
                    "Scenes with Dialogue": data.get("scenes_with_dialogue", 0),
                    "Dominant Emotion": data.get("dominant_emotion", "neutral"),
                    "Emotional Volatility": data.get("emotional_volatility", 0),
                    "Emotional Range": ", ".join(data.get("emotional_range", []))
                })
            
            df = pd.DataFrame(rows)
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="character_arcs.csv",
                mime="text/csv"
            )

st.divider()

st.markdown("""
### 💡 Understanding Emotional Intelligence Metrics

**Intensity (0-100)**: Energy level of a scene based on high-energy emotions (joy, anger, fear, surprise)
- **0-30**: Low energy, introspective scenes
- **31-60**: Moderate energy, balanced scenes
- **61-100**: High energy, action or dramatic scenes

**Tension (0-100)**: Conflict level based on antagonistic emotions (anger, fear, disgust)
- **0-30**: Calm, peaceful scenes
- **31-60**: Building tension
- **61-100**: High conflict or suspense

**Emotional Volatility (0-100)**: How much a character's emotions change scene-to-scene
- **0-30**: Stable character
- **31-60**: Moderate emotional range
- **61-100**: Highly volatile character arc
""")
