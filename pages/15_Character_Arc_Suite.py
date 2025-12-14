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
                st.success(f"📊 **Strong Positive Correlation:** {correlation_pct:.1f}% - Characters develop together")
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
