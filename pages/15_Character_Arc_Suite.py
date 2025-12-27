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
# CHARACTER COMPARISON
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.header("📊 Character Arc Comparison")
st.markdown("Side-by-side analysis of character development and interactions")

from src.CharacterArcEngine.arc_comparator import ArcComparator

comparator = ArcComparator()

# Character selection
col_select1, col_select2 = st.columns(2)

with col_select1:
    char1 = st.selectbox(
        "Character 1",
        options=list(valid_classifications.keys()),
        key="compare_char1"
    )

with col_select2:
    # Filter out char1 from options
    char2_options = [c for c in valid_classifications.keys() if c != char1]
    char2 = st.selectbox(
        "Character 2",
        options=char2_options if char2_options else list(valid_classifications.keys()),
        key="compare_char2"
    )

if char1 and char2 and char1 != char2:
    # Perform comparison
    comparison = comparator.compare_arcs(
        char1, character_arcs[char1],
        char2, character_arcs[char2]
    )
    
    # Basic Metrics Comparison
    st.subheader("⚖️ Basic Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    basic_metrics = comparison["basic_metrics"]
    
    with col1:
        vol1 = basic_metrics["volatility"]["char1"]
        vol2 = basic_metrics["volatility"]["char2"]
        st.metric(
            f"{char1} Volatility",
            f"{vol1:.1f}",
            delta=f"{vol1-vol2:+.1f} vs {char2}",
            delta_color="off"
        )
    
    with col2:
        vol2 = basic_metrics["volatility"]["char2"]
        st.metric(
            f"{char2} Volatility",
            f"{vol2:.1f}"
        )
    
    with col3:
        scenes1 = basic_metrics["scenes"]["char1"]
        scenes2 = basic_metrics["scenes"]["char2"]
        st.metric(
            f"{char1} Scenes",
            scenes1,
            delta=f"{scenes1-scenes2:+d} vs {char2}",
            delta_color="off"
        )
    
    with col4:
        scenes2 = basic_metrics["scenes"]["char2"]
        st.metric(
            f"{char2} Scenes",
            scenes2
        )
    
    st.divider()
    
    # Emotional Range Comparison
    st.subheader("🎨 Emotional Range")
    
    col_range1, col_range2 = st.columns(2)
    
    range_data = basic_metrics["emotional_range"]
    
    with col_range1:
        st.markdown(f"**{char1}:** {', '.join(range_data['char1_emotions'])}")
        st.caption(f"{range_data['char1']} unique emotions")
    
    with col_range2:
        st.markdown(f"**{char2}:** {', '.join(range_data['char2_emotions'])}")
        st.caption(f"{range_data['char2']} unique emotions")
    
    if range_data["shared_emotions"]:
        st.info(f"**Shared Emotions:** {', '.join(range_data['shared_emotions'])}")
    
    st.divider()
    
    # Trajectory Comparison
    traj_comp = comparison["trajectory_comparison"]
    
    if traj_comp.get("available"):
        st.subheader("📈 Trajectory Comparison")
        
        col_traj1, col_traj2 = st.columns(2)
        
        with col_traj1:
            direction1 = traj_comp["arc1_direction"]
            direction_icon = {"ascending": "📈", "descending": "📉", "flat": "➡️"}
            st.markdown(f"**{char1}:** {direction_icon.get(direction1, '➡️')} {direction1.title()}")
            st.caption(f"Peak at {traj_comp['arc1_peak_location']*100:.0f}% through arc")
        
        with col_traj2:
            direction2 = traj_comp["arc2_direction"]
            st.markdown(f"**{char2}:** {direction_icon.get(direction2, '➡️')} {direction2.title()}")
            st.caption(f"Peak at {traj_comp['arc2_peak_location']*100:.0f}% through arc")
        
        if traj_comp["parallel"]:
            st.success(f"✅ **Parallel Arcs:** Both characters move in {traj_comp['arc1_direction']} direction")
        else:
            st.warning(f"⚠️ **Divergent Arcs:** Characters move in opposite emotional directions")
        
        if traj_comp["synchronized_peaks"]:
            st.info("🎯 **Synchronized Peaks:** Both characters reach emotional peaks at similar points")
        
        # Correlation score
        correlation = traj_comp.get("correlation", 0)
        if correlation != 0:
            correlation_pct = abs(correlation) * 100
            if correlation > 0.5:
                st.success(f"📊 **Strong Positive Correlation:** {correlation_pct:.1f}% - Characters develop")
            elif correlation < -0.5:
                st.error(f"📊 **Strong Negative Correlation:** {correlation_pct:.1f}% - Characters develop in opposition")
            else:
                st.info(f"📊 **Weak Correlation:** {correlation_pct:.1f}% - Independent development")
        
        # Overlay trajectories chart
        st.markdown("#### Emotional Trajectories Overlay")
        
        char1_arc_scenes = character_arcs[char1].get("arc", [])
        char2_arc_scenes = character_arcs[char2].get("arc", [])
        
        if char1_arc_scenes and char2_arc_scenes:
            char1_intensities = [s.get("intensity", 0) for s in char1_arc_scenes]
            char2_intensities = [s.get("intensity", 0) for s in char2_arc_scenes]
            
            fig_overlay = go.Figure()
            
            # Character 1 trajectory
            fig_overlay.add_trace(go.Scatter(
                x=list(range(1, len(char1_intensities) + 1)),
                y=char1_intensities,
                mode="lines+markers",
                name=char1,
                line=dict(color="#FF6B6B", width=3),
                marker=dict(size=8)
            ))
            
            # Character 2 trajectory
            fig_overlay.add_trace(go.Scatter(
                x=list(range(1, len(char2_intensities) + 1)),
                y=char2_intensities,
                mode="lines+markers",
                name=char2,
                line=dict(color="#4ECDC4", width=3),
                marker=dict(size=8)
            ))
            
            fig_overlay.update_layout(
                title="Emotional Intensity Comparison",
                xaxis_title="Scene Appearance #",
                yaxis_title="Intensity (0-100)",
                height=400,
                hovermode="x unified"
            )
            
            st.plotly_chart(fig_overlay, use_container_width=True)
    
    st.divider()
    
    # Interaction Analysis
    st.subheader("🤝 Interaction Analysis")
    
    interaction = comparison["interaction_analysis"]
    
    col_int1, col_int2, col_int3 = st.columns(3)
    
    with col_int1:
        st.metric("Shared Scenes", interaction["shared_scenes"])
    
    with col_int2:
        st.metric("Interaction Rate", f"{interaction['interaction_rate']*100:.1f}%")
    
    with col_int3:
        st.metric("Emotional Alignment", f"{interaction['emotional_alignment']*100:.1f}%")
    
    col_only1, col_only2 = st.columns(2)
    
    with col_only1:
        st.metric(f"{char1} Solo Scenes", interaction["char1_only_scenes"])
    
    with col_only2:
        st.metric(f"{char2} Solo Scenes", interaction["char2_only_scenes"])
    
    # Interaction heatmap placeholder (Venn-style)
    if interaction["shared_scenes"] > 0:
        st.markdown("**Scene Distribution:**")
        
        # Create simple bar chart showing distribution
        fig_dist = go.Figure()
        
        fig_dist.add_trace(go.Bar(
            name=char1,
            x=["Solo", "Shared"],
            y=[interaction["char1_only_scenes"], interaction["shared_scenes"]],
            marker_color="#FF6B6B"
        ))
        
        fig_dist.add_trace(go.Bar(
            name=char2,
            x=["Solo", "Shared"],
            y=[interaction["char2_only_scenes"], interaction["shared_scenes"]],
            marker_color="#4ECDC4"
        ))
        
        fig_dist.update_layout(
            barmode="group",
            height=300,
            xaxis_title="Scene Type",
            yaxis_title="Count"
        )
        
        st.plotly_chart(fig_dist, use_container_width=True)
    
    st.divider()
    
    # Development Rates
    dev_rates = comparison["development_rates"]
    
    if dev_rates.get("available"):
        st.subheader("⚡ Development Rates")
        
        col_dev1, col_dev2, col_dev3 = st.columns(3)
        
        with col_dev1:
            st.markdown("**Development Speed**")
            rate1 = dev_rates["development_rate"]["char1"]
            rate2 = dev_rates["development_rate"]["char2"]
            faster = char1 if dev_rates["development_rate"]["faster"] == "char1" else char2
            
            st.metric(f"{char1}", f"{rate1:.2f} per scene")
            st.metric(f"{char2}", f"{rate2:.2f} per scene")
            st.caption(f"🏆 **Faster:** {faster}")
        
        with col_dev2:
            st.markdown("**Arc Depth**")
            depth1 = dev_rates["arc_depth"]["char1"]
            depth2 = dev_rates["arc_depth"]["char2"]
            deeper = char1 if dev_rates["arc_depth"]["deeper"] == "char1" else char2
            
            st.metric(f"{char1}", f"{depth1:.1f}")
            st.metric(f"{char2}", f"{depth2:.1f}")
            st.caption(f"🏆 **Deeper:** {deeper}")
        
        with col_dev3:
            st.markdown("**Consistency**")
            cons1 = dev_rates["consistency"]["char1"]
            cons2 = dev_rates["consistency"]["char2"]
            more_consistent = char1 if dev_rates["consistency"]["more_consistent"] == "char1" else char2
            
            st.metric(f"{char1}", f"{cons1:.1f}%")
            st.metric(f"{char2}", f"{cons2:.1f}%")
            st.caption(f"🏆 **More Consistent:** {more_consistent}")
        
        # Spider chart for multi-metric comparison
        st.markdown("#### Multi-Metric Comparison")
        
        fig_spider = go.Figure()
        
        categories = ["Volatility", "Scenes", "Dev Rate", "Arc Depth", "Consistency"]
        
        # Normalize metrics to 0-100 scale
        vol1_norm = min(basic_metrics["volatility"]["char1"], 100)
        vol2_norm = min(basic_metrics["volatility"]["char2"], 100)
        
        scenes1_norm = min(basic_metrics["scenes"]["char1"] / max(basic_metrics["scenes"]["char2"], 1) * 50, 100)
        scenes2_norm = min(basic_metrics["scenes"]["char2"] / max(basic_metrics["scenes"]["char1"], 1) * 50, 100)
        
        rate1_norm = min(rate1 * 10, 100)
        rate2_norm = min(rate2 * 10, 100)
        
        depth1_norm = min(depth1, 100)
        depth2_norm = min(depth2, 100)
        
        fig_spider.add_trace(go.Scatterpolar(
            r=[vol1_norm, scenes1_norm, rate1_norm, depth1_norm, cons1],
            theta=categories,
            fill="toself",
            name=char1,
            line_color="#FF6B6B"
        ))
        
        fig_spider.add_trace(go.Scatterpolar(
            r=[vol2_norm, scenes2_norm, rate2_norm, depth2_norm, cons2],
            theta=categories,
            fill="toself",
            name=char2,
            line_color="#4ECDC4"
        ))
        
        fig_spider.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            height=400,
            showlegend=True
        )
        
        st.plotly_chart(fig_spider, use_container_width=True)
    
    st.divider()
    
    # Synchronization Analysis
    sync = comparison["synchronization"]
    
    st.subheader("🔄 Arc Synchronization")
    
    st.markdown(f"### {sync['relationship_type']}")
    st.markdown(f"**{sync['description']}**")
    
    col_sync1, col_sync2 = st.columns(2)
    
    with col_sync1:
        if sync["synchronized"]:
            st.success("✅ **Peaks Synchronized** - Characters reach crisis points together")
        else:
            st.info("ℹ️ **Asynchronous Peaks** - Characters develop at different paces")
    
    with col_sync2:
        if sync["parallel"]:
            st.success("✅ **Parallel Direction** - Characters move in same emotional direction")
        else:
            st.warning("⚠️ **Opposite Direction** - Characters move in contrasting directions")

elif char1 == char2:
    st.warning("⚠️ Please select two different characters to compare.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ARC COMPLETION PREDICTOR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.divider()
st.header("🔮 Arc Completion Predictor")
st.markdown("AI-powered forecasting of missing beats and incomplete transformations")

from src.CharacterArcEngine.arc_predictor import ArcPredictor

# Character selector for prediction
pred_char = st.selectbox(
    "Select character to analyze",
    options=list(character_arcs.keys()),
    key="predictor_char"
)

if pred_char:
    # Get character's arc type from classification (arc_classifications is a dict keyed by character name)
    char_classification = arc_classifications.get(pred_char)
    
    if char_classification:
        # Run prediction
        predictor = ArcPredictor()
        prediction = predictor.predict_completion(
            pred_char,
            character_arcs[pred_char],
            char_classification["arc_type"]
        )
        
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            completion = prediction["completion_percentage"]
            st.metric(
                "Arc Completion",
                f"{completion}%",
                delta=f"{completion - 100:.0f}%" if completion < 100 else "Complete"
            )
        
        with col2:
            confidence = prediction["confidence"]
            st.metric(
                "Prediction Confidence",
                f"{confidence:.0%}",
                help="Based on scene count and arc complexity"
            )
        
        with col3:
            missing_count = len(prediction["missing_beats"])
            st.metric(
                "Missing Beats",
                missing_count,
                delta=f"-{missing_count}" if missing_count > 0 else "None",
                delta_color="inverse"
            )
        
        with col4:
            present_count = len(prediction["present_beats"])
            st.metric(
                "Present Beats",
                present_count,
                delta=f"+{present_count}"
            )
        
        # Detailed analysis
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("📊 Analysis")
            
            # Pacing assessment
            pacing = prediction["pacing_assessment"]
            if "Well Paced" in pacing or "Appropriate" in pacing:
                st.success(f"**Pacing:** {pacing}")
            elif "Too Fast" in pacing or "Too Slow" in pacing:
                st.warning(f"**Pacing:** {pacing}")
            else:
                st.info(f"**Pacing:** {pacing}")
            
            # Transformation status
            transformation = prediction["transformation_status"]
            if "Complete" in transformation:
                st.success(f"**Transformation:** {transformation}")
            elif "Incomplete" in transformation or "Divergent" in transformation:
                st.warning(f"**Transformation:** {transformation}")
            else:
                st.info(f"**Transformation:** {transformation}")
            
            # Emotional beats
            st.write("**Present Emotional Beats:**")
            if prediction["present_beats"]:
                beats_display = ", ".join([f":{beat}:" for beat in prediction["present_beats"]])
                st.write(beats_display)
            else:
                st.write("_None detected_")
            
            if prediction["missing_beats"]:
                st.write("**Missing Emotional Beats:**")
                missing_display = ", ".join([f":{beat}:" for beat in prediction["missing_beats"]])
                st.write(missing_display)
        
        with col_right:
            st.subheader("💡 Suggestions")
            
            for i, suggestion in enumerate(prediction["suggestions"], 1):
                if "well-structured" in suggestion.lower():
                    st.success(f"{i}. {suggestion}")
                elif any(word in suggestion.lower() for word in ["add", "include", "consider"]):
                    st.info(f"{i}. {suggestion}")
                else:
                    st.warning(f"{i}. {suggestion}")
        
        # Progress visualization
        st.subheader("📈 Arc Progression")
        
        # Create progress bar with color coding
        completion_pct = prediction["completion_percentage"]
        if completion_pct >= 80:
            progress_color = "🟢"
            status_msg = "Arc is nearly complete"
        elif completion_pct >= 50:
            progress_color = "🟡"
            status_msg = "Arc is developing well"
        else:
            progress_color = "🔴"
            status_msg = "Arc needs more development"
        
        st.progress(completion_pct / 100)
        st.caption(f"{progress_color} {status_msg} - {completion_pct}% complete")
    
    else:
        st.info("⚠️ Character needs arc classification first (requires 3+ scenes)")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CHARACTER INTERACTION HEATMAP
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.divider()
st.header("🔥 Character Interaction Heatmap")
st.markdown("Visualize scene-sharing patterns across all characters")

# Build interaction matrix
all_characters = sorted(list(character_arcs.keys()))
num_chars = len(all_characters)

if num_chars >= 2:
    # Calculate interaction matrix
    interaction_matrix = []
    hover_text = []
    
    for char1 in all_characters:
        row = []
        hover_row = []
        char1_arc = character_arcs[char1]
        char1_scenes = set(char1_arc.get("scenes", []))
        
        for char2 in all_characters:
            if char1 == char2:
                # Diagonal: character's own scene count
                row.append(len(char1_scenes))
                hover_row.append(f"<b>{char1}</b><br>Total Scenes: {len(char1_scenes)}")
            else:
                # Off-diagonal: shared scenes
                char2_arc = character_arcs[char2]
                char2_scenes = set(char2_arc.get("scenes", []))
                shared_scenes = char1_scenes.intersection(char2_scenes)
                shared_count = len(shared_scenes)
                
                # Calculate emotional alignment if they share scenes
                if shared_count > 0:
                    # Get emotions for shared scenes
                    char1_emotions = char1_arc.get("emotions_by_scene", {})
                    char2_emotions = char2_arc.get("emotions_by_scene", {})
                    
                    aligned_scenes = 0
                    for scene_idx in shared_scenes:
                        e1 = char1_emotions.get(scene_idx, {}).get("emotion", "")
                        e2 = char2_emotions.get(scene_idx, {}).get("emotion", "")
                        if e1 and e2 and e1 == e2:
                            aligned_scenes += 1
                    
                    alignment_pct = (aligned_scenes / shared_count * 100) if shared_count > 0 else 0
                    
                    row.append(shared_count)
                    hover_row.append(
                        f"<b>{char1} ↔ {char2}</b><br>"
                        f"Shared Scenes: {shared_count}<br>"
                        f"Emotional Alignment: {alignment_pct:.1f}%"
                    )
                else:
                    row.append(0)
                    hover_row.append(f"<b>{char1} ↔ {char2}</b><br>No shared scenes")
        
        interaction_matrix.append(row)
        hover_text.append(hover_row)
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=interaction_matrix,
        x=all_characters,
        y=all_characters,
        text=hover_text,
        hovertemplate='%{text}<extra></extra>',
        colorscale='YlOrRd',
        showscale=True,
        colorbar=dict(
            title="Shared<br>Scenes",
            titleside="right"
        )
    ))
    
    fig.update_layout(
        title=dict(
            text=f"Character Interaction Matrix ({num_chars} characters)",
            x=0.5,
            xanchor='center'
        ),
        xaxis_title="Character",
        yaxis_title="Character",
        width=800,
        height=600,
        xaxis=dict(side='bottom'),
        yaxis=dict(autorange='reversed')  # Flip y-axis so it reads top-to-bottom
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    st.subheader("💡 Interaction Insights")
    
    # Find most connected character
    total_interactions = {}
    for i, char in enumerate(all_characters):
        total = sum(interaction_matrix[i]) - interaction_matrix[i][i]  # Exclude self
        total_interactions[char] = total
    
    most_connected = max(total_interactions, key=total_interactions.get)
    least_connected = min(total_interactions, key=total_interactions.get)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Most Connected",
            most_connected,
            f"{total_interactions[most_connected]} shared scenes"
        )
    
    with col2:
        st.metric(
            "Least Connected",
            least_connected,
            f"{total_interactions[least_connected]} shared scenes"
        )
    
    with col3:
        total_shared = sum(sum(row) for row in interaction_matrix)
        total_diagonal = sum(interaction_matrix[i][i] for i in range(num_chars))
        avg_sharing = (total_shared - total_diagonal) / (num_chars * (num_chars - 1)) if num_chars > 1 else 0
        st.metric(
            "Avg. Shared Scenes",
            f"{avg_sharing:.1f}",
            "per character pair"
        )

else:
    st.info("⚠️ Need at least 2 characters with tracked arcs to generate interaction heatmap.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# RELATIONSHIP EVOLUTION TRACKER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.divider()
st.header("💞 Relationship Evolution Tracker")
st.markdown("Track character relationships and emotional dynamics over time")

from src.CharacterArcEngine.relationship_tracker import RelationshipTracker

# Relationship selector
rel_col1, rel_col2 = st.columns(2)

with rel_col1:
    rel_char1 = st.selectbox(
        "Character 1",
        options=list(character_arcs.keys()),
        key="rel_char1"
    )

with rel_col2:
    rel_char2_options = [c for c in character_arcs.keys() if c != rel_char1]
    rel_char2 = st.selectbox(
        "Character 2",
        options=rel_char2_options,
        key="rel_char2"
    ) if rel_char2_options else None

if rel_char1 and rel_char2 and rel_char1 != rel_char2:
    tracker = RelationshipTracker()
    relationship = tracker.track_relationship(
        rel_char1,
        character_arcs[rel_char1],
        rel_char2,
        character_arcs[rel_char2]
    )
    
    if relationship["shared_scenes"]:
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            strength = relationship["relationship_strength"]
            st.metric(
                "Relationship Strength",
                f"{strength:.0%}",
                help="Based on interaction frequency and emotional alignment"
            )
        
        with col2:
            shared_count = len(relationship["shared_scenes"])
            st.metric(
                "Shared Scenes",
                shared_count
            )
        
        with col3:
            avg_sentiment = sum(relationship["sentiment_trajectory"]) / len(relationship["sentiment_trajectory"])
            sentiment_emoji = "😊" if avg_sentiment > 0.3 else "😐" if avg_sentiment > -0.3 else "😠"
            st.metric(
                "Avg. Sentiment",
                f"{avg_sentiment:+.2f}",
                delta=sentiment_emoji
            )
        
        with col4:
            turning_points_count = len(relationship["turning_points"])
            st.metric(
                "Turning Points",
                turning_points_count,
                help="Significant shifts in relationship"
            )
        
        # Relationship type badge
        rel_type = relationship["relationship_type"]
        if "Alliance" in rel_type or "Bond" in rel_type or "Romantic" in rel_type:
            st.success(f"**Relationship Type:** {rel_type}")
        elif "Conflict" in rel_type or "Antagonistic" in rel_type or "Deteriorating" in rel_type:
            st.error(f"**Relationship Type:** {rel_type}")
        else:
            st.info(f"**Relationship Type:** {rel_type}")
        
        # Evolution summary
        st.write("**Evolution Summary:**")
        st.write(relationship["evolution_summary"])
        
        # Sentiment trajectory chart
        st.subheader("📈 Sentiment Trajectory")
        
        trajectory_data = {
            "Scene": relationship["shared_scenes"],
            "Sentiment": relationship["sentiment_trajectory"]
        }
        
        fig_trajectory = go.Figure()
        
        fig_trajectory.add_trace(go.Scatter(
            x=trajectory_data["Scene"],
            y=trajectory_data["Sentiment"],
            mode='lines+markers',
            name='Sentiment',
            line=dict(color='#8B5CF6', width=3),
            marker=dict(size=10),
            fill='tozeroy',
            fillcolor='rgba(139, 92, 246, 0.2)'
        ))
        
        # Add zero line
        fig_trajectory.add_hline(
            y=0, 
            line_dash="dash", 
            line_color="gray",
            annotation_text="Neutral"
        )
        
        # Mark turning points
        for tp in relationship["turning_points"]:
            fig_trajectory.add_annotation(
                x=tp["scene"],
                y=relationship["sentiment_trajectory"][relationship["shared_scenes"].index(tp["scene"])],
                text="⚡",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="#FF6B6B"
            )
        
        fig_trajectory.update_layout(
            title=f"{rel_char1} & {rel_char2} Relationship Evolution",
            xaxis_title="Scene Number",
            yaxis_title="Sentiment Score",
            yaxis=dict(range=[-1, 1]),
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig_trajectory, use_container_width=True)
        
        # Turning points
        if relationship["turning_points"]:
            st.subheader("⚡ Relationship Turning Points")
            
            for i, tp in enumerate(relationship["turning_points"], 1):
                shift_emoji = "📈" if tp["shift"] > 0 else "📉"
                with st.expander(f"{shift_emoji} Scene {tp['scene']}: {tp['type']} ({tp['shift']:+.2f})"):
                    st.write(f"**Description:** {tp['description']}")
                    st.write(f"**Emotions:** {tp['emotions'][0]} ({rel_char1}), {tp['emotions'][1]} ({rel_char2})")
        else:
            st.info("ℹ️ No major turning points detected - relationship remains stable")
    
    else:
        st.warning(f"⚠️ {rel_char1} and {rel_char2} do not share any scenes")

elif rel_char1 == rel_char2:
    st.warning("⚠️ Please select two different characters")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CHARACTER CONSISTENCY ANALYZER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.divider()
st.header("✅ Character Consistency Analyzer")
st.markdown("Detect out-of-character moments and behavioral deviations")

from src.CharacterArcEngine.consistency_analyzer import ConsistencyAnalyzer

# Character selector
consistency_char = st.selectbox(
    "Select character to analyze",
    options=list(character_arcs.keys()),
    key="consistency_char"
)

if consistency_char:
    analyzer = ConsistencyAnalyzer()
    analysis = analyzer.analyze_consistency(
        consistency_char,
        character_arcs[consistency_char]
    )
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        score = analysis["consistency_score"]
        if score >= 80:
            st.metric("Consistency Score", f"{score}/100", delta="Excellent", delta_color="normal")
        elif score >= 60:
            st.metric("Consistency Score", f"{score}/100", delta="Good", delta_color="normal")
        else:
            st.metric("Consistency Score", f"{score}/100", delta="Needs Review", delta_color="inverse")
    
    with col2:
        deviation_count = len(analysis["deviations"])
        st.metric(
            "Deviations Detected",
            deviation_count,
            delta=f"{deviation_count} issues" if deviation_count > 0 else "None",
            delta_color="inverse" if deviation_count > 0 else "normal"
        )
    
    with col3:
        confidence = analysis["confidence"]
        st.metric(
            "Analysis Confidence",
            f"{confidence:.0%}",
            help="Based on scene count"
        )
    
    # Pattern analysis
    st.subheader("📊 Behavior Pattern Analysis")
    st.write(analysis["pattern_analysis"])
    
    # Baseline emotions
    if analysis["baseline_emotions"]:
        st.write("**Baseline Emotions:**")
        baseline_str = ", ".join([f":{emotion}:" for emotion in analysis["baseline_emotions"]])
        st.write(baseline_str)
    
    # Warnings
    st.subheader("⚠️ Warnings & Recommendations")
    for warning in analysis["warnings"]:
        if "✅" in warning:
            st.success(warning)
        elif "⚠️" in warning:
            st.warning(warning)
        else:
            st.info(warning)
    
    # Deviations table
    if analysis["deviations"]:
        st.subheader("🚨 Out-of-Character Moments")
        
        deviation_data = []
        for dev in analysis["deviations"]:
            deviation_data.append({
                "Scene": dev["scene"],
                "Emotion": dev["emotion"],
                "Intensity": f"{dev['intensity']:.0%}",
                "Expected": dev["expected"],
                "Severity": dev["severity"].upper(),
                "Description": dev["description"]
            })
        
        df_deviations = pd.DataFrame(deviation_data)
        
        # Color code by severity
        def color_severity(val):
            if val == "SEVERE":
                return 'background-color: #ff4444; color: white'
            elif val == "MODERATE":
                return 'background-color: #ffaa00; color: white'
            else:
                return 'background-color: #ffee99'
        
        styled_df = df_deviations.style.applymap(color_severity, subset=['Severity'])
        st.dataframe(styled_df, use_container_width=True)
        
        # Deviation timeline
        st.subheader("📈 Deviation Timeline")
        
        fig_deviations = go.Figure()
        
        # Plot all emotions
        all_scenes = sorted(character_arcs[consistency_char].get("emotions_by_scene", {}).keys())
        all_emotions = [
            character_arcs[consistency_char]["emotions_by_scene"][s].get("emotion", "neutral") 
            for s in all_scenes
        ]
        
        # Convert emotions to numeric for plotting
        emotion_map = {"joy": 3, "surprise": 2, "neutral": 0, "fear": -1, "sadness": -2, "anger": -3}
        emotion_values = [emotion_map.get(e, 0) for e in all_emotions]
        
        fig_deviations.add_trace(go.Scatter(
            x=all_scenes,
            y=emotion_values,
            mode='lines+markers',
            name='Emotional State',
            line=dict(color='#6366F1', width=2),
            marker=dict(size=8)
        ))
        
        # Mark deviations
        for dev in analysis["deviations"]:
            scene_idx = dev["scene"]
            if scene_idx in all_scenes:
                idx = all_scenes.index(scene_idx)
                fig_deviations.add_annotation(
                    x=scene_idx,
                    y=emotion_values[idx],
                    text="⚠️" if dev["severity"] == "severe" else "ℹ️",
                    showarrow=True,
                    arrowhead=2,
                    arrowcolor="red" if dev["severity"] == "severe" else "orange"
                )
        
        fig_deviations.update_layout(
            title=f"{consistency_char} Emotional Consistency",
            xaxis_title="Scene Number",
            yaxis_title="Emotional State",
            yaxis=dict(
                tickvals=[-3, -2, -1, 0, 2, 3],
                ticktext=["Anger", "Sadness", "Fear", "Neutral", "Surprise", "Joy"]
            ),
            height=400
        )
        
        st.plotly_chart(fig_deviations, use_container_width=True)
    
    else:
        st.success("✅ No significant deviations detected - character behavior is consistent")


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
