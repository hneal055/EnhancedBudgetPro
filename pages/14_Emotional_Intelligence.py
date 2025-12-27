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
if not st.session_state.get("data"):
    st.error("⚠️ No script data available. Please parse a script on Page 1 first.")
    st.stop()

if not st.session_state.get("emotion_data"):
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
# 2D EMOTION HEATMAP (Character × Scene)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.header("🗺️ Emotion Heatmap (Character × Scene)")

if character_arcs and scene_emotions:
    # Build heatmap data
    characters = sorted(character_arcs.keys())[:10]  # Limit to top 10 for readability
    
    if characters:
        # Map emotions to numeric values for heatmap
        emotion_to_value = {
            "joy": 5,
            "surprise": 4,
            "neutral": 3,
            "sadness": 2,
            "fear": 1,
            "anger": 0,
            "disgust": 0
        }
        
        # Build matrix: rows=characters, cols=scenes
        heatmap_data = []
        scene_labels = []
        
        for i, scene in enumerate(scene_emotions[:30], 1):  # Limit to first 30 scenes
            scene_labels.append(f"S{i}")
        
        for char in characters:
            char_arc = character_arcs[char].get("arc", [])
            char_row = []
            
            # Match character's emotions to scene numbers
            char_scene_emotions = {entry["scene"]: entry["dominant_emotion"] for entry in char_arc}
            
            for i, scene in enumerate(scene_emotions[:30], 1):
                scene_heading = scene["scene_heading"]
                
                # If character has emotion for this scene, use it
                if scene_heading in char_scene_emotions:
                    emotion = char_scene_emotions[scene_heading]
                    char_row.append(emotion_to_value.get(emotion, 3))
                else:
                    # Character not in scene
                    char_row.append(None)
            
            heatmap_data.append(char_row)
        
        # Create heatmap
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            x=scene_labels,
            y=characters,
            colorscale=[
                [0, "#d32f2f"],    # anger/disgust - red
                [0.2, "#7b1fa2"],  # fear - purple
                [0.4, "#1976d2"],  # sadness - blue
                [0.6, "#757575"],  # neutral - gray
                [0.8, "#ffa726"],  # surprise - orange
                [1, "#fdd835"]     # joy - yellow
            ],
            hovertemplate="Character: %{y}<br>Scene: %{x}<br>Emotion Value: %{z}<extra></extra>",
            zmin=0,
            zmax=5
        ))
        
        fig_heatmap.update_layout(
            title="Character Emotions Across Scenes",
            xaxis_title="Scene Number",
            yaxis_title="Character",
            height=400 + (len(characters) * 30),  # Scale height by character count
            xaxis=dict(side="bottom"),
            yaxis=dict(autorange="reversed")
        )
        
        st.plotly_chart(fig_heatmap, width='stretch')
        
        st.info("""
        **How to read this heatmap:**
        - 🟨 **Yellow**: Joy, positive emotions
        - 🟧 **Orange**: Surprise
        - ⬜ **Gray**: Neutral
        - 🟦 **Blue**: Sadness
        - 🟪 **Purple**: Fear
        - 🟥 **Red**: Anger/Disgust
        - **Blank**: Character not in scene
        """)
    else:
        st.info("No character data available for heatmap.")
else:
    st.info("Emotion heatmap requires both character arcs and scene emotions.")

st.divider()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CHARACTER EMOTIONAL ARCS

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CHARACTER RELATIONSHIP DYNAMICS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.header("🔗 Character Relationship Dynamics")

if character_arcs and len(character_arcs) >= 2:
    from src.EmotionEngine import ArcTracker
    tracker = ArcTracker()
    
    # Calculate relationships between all character pairs
    characters = list(character_arcs.keys())[:8]  # Limit to top 8
    relationships = []
    
    for i in range(len(characters)):
        for j in range(i + 1, len(characters)):
            char1 = characters[i]
            char2 = characters[j]
            
            dynamics = tracker.analyze_relationship_dynamics(
                character_arcs[char1],
                character_arcs[char2]
            )
            
            if dynamics["shared_scenes"] > 0:
                relationships.append({
                    "char1": char1,
                    "char2": char2,
                    "alignment": dynamics["emotional_alignment"],
                    "shared_scenes": dynamics["shared_scenes"],
                    "type": dynamics["relationship_type"]
                })
    
    if relationships:
        # Create network-style visualization
        # Use scatter plot with connection lines
        
        # Position characters in a circle
        import math
        n = len(characters)
        positions = {}
        for i, char in enumerate(characters):
            angle = 2 * math.pi * i / n
            positions[char] = (math.cos(angle), math.sin(angle))
        
        fig_relationships = go.Figure()
        
        # Draw relationship lines
        for rel in relationships:
            char1 = rel["char1"]
            char2 = rel["char2"]
            
            if char1 in positions and char2 in positions:
                x1, y1 = positions[char1]
                x2, y2 = positions[char2]
                
                # Color by relationship type
                color_map = {
                    "supportive": "green",
                    "antagonistic": "red",
                    "complex": "orange",
                    "distant": "lightgray"
                }
                color = color_map.get(rel["type"], "gray")
                
                # Line thickness by alignment strength
                width = max(1, rel["alignment"] / 20)
                
                fig_relationships.add_trace(go.Scatter(
                    x=[x1, x2],
                    y=[y1, y2],
                    mode="lines",
                    line=dict(color=color, width=width),
                    hoverinfo="skip",
                    showlegend=False
                ))
        
        # Draw character nodes
        x_pos = [positions[char][0] for char in characters if char in positions]
        y_pos = [positions[char][1] for char in characters if char in positions]
        
        fig_relationships.add_trace(go.Scatter(
            x=x_pos,
            y=y_pos,
            mode="markers+text",
            marker=dict(size=30, color="lightblue", line=dict(color="darkblue", width=2)),
            text=characters,
            textposition="top center",
            hoverinfo="text",
            hovertext=characters,
            showlegend=False
        ))
        
        fig_relationships.update_layout(
            title="Character Relationship Network",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=500,
            hovermode="closest"
        )
        
        st.plotly_chart(fig_relationships, width='stretch')
        
        # Relationship details table
        st.subheader("Relationship Details")
        rel_df = pd.DataFrame([
            {
                "Characters": f"{r['char1']} ↔ {r['char2']}",
                "Type": r['type'].title(),
                "Alignment": f"{r['alignment']:.1f}%",
                "Shared Scenes": r['shared_scenes']
            }
            for r in sorted(relationships, key=lambda x: x['alignment'], reverse=True)
        ])
        st.dataframe(rel_df, width='stretch')
        
        st.info("""
        **Relationship Types:**
        - 🟢 **Supportive**: High emotional alignment, harmonious interactions
        - 🟠 **Complex**: Mix of conflict and harmony
        - 🔴 **Antagonistic**: Low alignment, opposing emotions
        - ⚪ **Distant**: Few shared emotional moments
        """)
    else:
        st.info("No character relationships found (characters need shared scenes).")
else:
    st.info("Relationship dynamics require at least 2 characters with emotional arcs.")

st.divider()


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
# EMOTIONAL ARC TRANSFORMATION (SANKEY)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.header("🌊 Emotional Arc Transformations")
st.markdown("Visualize how characters' emotional states flow and transform throughout the script")

if character_arcs:
    selected_char_sankey = st.selectbox(
        "Select Character for Transformation Flow",
        options=list(character_arcs.keys()),
        key="sankey_char"
    )
    
    if selected_char_sankey:
        char_data = character_arcs[selected_char_sankey]
        arc_scenes = char_data.get("arc", [])
        
        if len(arc_scenes) >= 2:
            # Build Sankey diagram showing emotion transitions
            sources = []
            targets = []
            values = []
            labels = set()
            
            # Create transitions between consecutive scenes
            for i in range(len(arc_scenes) - 1):
                current_scene = arc_scenes[i]
                next_scene = arc_scenes[i + 1]
                
                current_emotion = current_scene.get("dominant_emotion", "neutral")
                next_emotion = next_scene.get("dominant_emotion", "neutral")
                
                # Add labels
                labels.add(f"{current_emotion} (S{i+1})")
                labels.add(f"{next_emotion} (S{i+2})")
            
            # Convert labels to list for indexing
            labels_list = sorted(list(labels))
            label_to_idx = {label: idx for idx, label in enumerate(labels_list)}
            
            # Build connections
            for i in range(len(arc_scenes) - 1):
                current_scene = arc_scenes[i]
                next_scene = arc_scenes[i + 1]
                
                current_emotion = current_scene.get("dominant_emotion", "neutral")
                next_emotion = next_scene.get("dominant_emotion", "neutral")
                
                source_label = f"{current_emotion} (S{i+1})"
                target_label = f"{next_emotion} (S{i+2})"
                
                sources.append(label_to_idx[source_label])
                targets.append(label_to_idx[target_label])
                values.append(1)  # Weight of connection
            
            # Color mapping for emotions
            emotion_colors = {
                "joy": "#FFD700",
                "sadness": "#4682B4",
                "anger": "#DC143C",
                "fear": "#9370DB",
                "surprise": "#FF8C00",
                "disgust": "#8B4513",
                "neutral": "#A9A9A9"
            }
            
            # Assign colors to labels
            node_colors = []
            for label in labels_list:
                emotion = label.split(" (")[0]
                node_colors.append(emotion_colors.get(emotion, "#A9A9A9"))
            
            # Create Sankey diagram
            fig_sankey = go.Figure(data=[go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=labels_list,
                    color=node_colors
                ),
                link=dict(
                    source=sources,
                    target=targets,
                    value=values,
                    color="rgba(150, 150, 150, 0.3)"
                )
            )])
            
            fig_sankey.update_layout(
                title=f"Emotional Flow: {selected_char_sankey}",
                font=dict(size=12),
                height=500
            )
            
            st.plotly_chart(fig_sankey, use_container_width=True)
            
            # Interpretation
            st.markdown(f"""
            **Interpretation**: This Sankey diagram shows how **{selected_char_sankey}**'s emotions 
            transition from scene to scene. Each node represents an emotional state at a specific scene, 
            and the flows show the progression through the narrative.
            
            - **Thick flows**: Character maintains the same emotion
            - **Branching flows**: Emotional shifts and transformations
            - **Color coding**: Each emotion has a distinct color for easy tracking
            """)
            
            # Key transformations
            transformations = []
            for i in range(len(arc_scenes) - 1):
                current = arc_scenes[i].get("dominant_emotion", "neutral")
                next_em = arc_scenes[i + 1].get("dominant_emotion", "neutral")
                if current != next_em:
                    transformations.append(f"Scene {i+1}→{i+2}: **{current}** → **{next_em}**")
            
            if transformations:
                st.markdown("**Key Emotional Transformations:**")
                for trans in transformations[:5]:  # Show top 5
                    st.markdown(f"- {trans}")
        else:
            st.info(f"{selected_char_sankey} appears in too few scenes for transformation analysis.")
else:
    st.info("No character arc data available for transformation analysis.")


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
""")# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ANNOTATED TIMELINE WITH TURNING POINTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.header("📈 Emotional Timeline")
st.markdown("Scene-by-scene emotional intensity with key turning points highlighted")

if scene_emotions:
    # Prepare timeline data
    timeline_data = []
    for i, scene in enumerate(scene_emotions, 1):
        timeline_data.append({
            "scene_num": i,
            "heading": scene.get("heading", f"Scene {i}"),
            "intensity": scene.get("intensity", 0),
            "tension": scene.get("tension", 0),
            "dominant_emotion": scene.get("dominant_emotion", "neutral")
        })
    
    df_timeline = pd.DataFrame(timeline_data)
    
    # Create figure with dual y-axis
    fig_timeline = go.Figure()
    
    # Intensity curve
    fig_timeline.add_trace(go.Scatter(
        x=df_timeline["scene_num"],
        y=df_timeline["intensity"],
        mode="lines+markers",
        name="Intensity",
        line=dict(color="#FF6B6B", width=3),
        marker=dict(size=6),
        hovertemplate="<b>Scene %{x}</b><br>" +
                      "Intensity: %{y:.1f}<br>" +
                      "<extra></extra>"
    ))
    
    # Tension curve
    fig_timeline.add_trace(go.Scatter(
        x=df_timeline["scene_num"],
        y=df_timeline["tension"],
        mode="lines+markers",
        name="Tension",
        line=dict(color="#4ECDC4", width=3, dash="dash"),
        marker=dict(size=6),
        hovertemplate="<b>Scene %{x}</b><br>" +
                      "Tension: %{y:.1f}<br>" +
                      "<extra></extra>"
    ))
    
    # Annotate turning points
    if turning_points:
        for char, tp_list in turning_points.items():
            for tp in tp_list[:3]:  # Top 3 per character
                scene_idx = tp.get("scene_index", 0)
                if 0 <= scene_idx < len(timeline_data):
                    scene_data = timeline_data[scene_idx]
                    
                    # Add annotation marker
                    fig_timeline.add_trace(go.Scatter(
                        x=[scene_data["scene_num"]],
                        y=[scene_data["intensity"]],
                        mode="markers+text",
                        name=f"TP: {char}",
                        marker=dict(
                            size=15,
                            color="#FFD700",
                            symbol="star",
                            line=dict(color="black", width=2)
                        ),
                        text=[f"{char}<br>{tp.get('from_emotion', '')}→{tp.get('to_emotion', '')}"],
                        textposition="top center",
                        textfont=dict(size=10, color="black"),
                        hovertemplate=f"<b>Turning Point: {char}</b><br>" +
                                      f"Scene {scene_data['scene_num']}<br>" +
                                      f"{tp.get('from_emotion', '')} → {tp.get('to_emotion', '')}<br>" +
                                      f"Impact: {tp.get('impact', 0):.1f}<br>" +
                                      "<extra></extra>",
                        showlegend=False
                    ))
    
    fig_timeline.update_layout(
        title="Emotional Intensity Timeline with Turning Points",
        xaxis_title="Scene Number",
        yaxis_title="Score (0-100)",
        height=500,
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Timeline insights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        peak_intensity_idx = df_timeline["intensity"].idxmax()
        peak_scene = df_timeline.loc[peak_intensity_idx]
        st.metric(
            "Peak Intensity Scene",
            f"Scene {peak_scene['scene_num']}",
            f"{peak_scene['intensity']:.1f}/100"
        )
    
    with col2:
        peak_tension_idx = df_timeline["tension"].idxmax()
        peak_tension_scene = df_timeline.loc[peak_tension_idx]
        st.metric(
            "Peak Tension Scene",
            f"Scene {peak_tension_scene['scene_num']}",
            f"{peak_tension_scene['tension']:.1f}/100"
        )
    
    with col3:
        avg_intensity_first_half = df_timeline[:len(df_timeline)//2]["intensity"].mean()
        avg_intensity_second_half = df_timeline[len(df_timeline)//2:]["intensity"].mean()
        intensity_delta = avg_intensity_second_half - avg_intensity_first_half
        st.metric(
            "Act 2 Intensity Change",
            f"{'+' if intensity_delta >= 0 else ''}{intensity_delta:.1f}",
            help="Difference between first half and second half average intensity"
        )
    
    st.markdown("""
    **🌟 Gold Stars** indicate emotional turning points where characters experience significant emotional shifts.
    Hover over the timeline to see detailed scene information and turning point details.
    """)
else:
    st.info("No scene emotion data available for timeline visualization.")

import streamlit as st

st.title("Burn Rate")

if "data" not in st.session_state:
    st.warning("Please upload and analyze a script first.")
    st.stop()

st.info("This page is under construction. Core logic coming soon.")



