import streamlit as st
import os
from src.ui.global_sidebar import install_global_sidebar
install_global_sidebar()

from src.VisualizationEngine.relationship_graph_engine import RelationshipGraphEngine
from src.VisualizationEngine.gantt_chart_engine import GanttChartEngine
from src.VisualizationEngine.character_arc_pdf import CharacterArcPDFExporter

st.title("📊 Advanced Visualizations")
st.markdown("**Character networks, timelines, and exportable reports**")

# Check if data is available
if not st.session_state.get("data"):
    st.warning("⚠️ Please analyze a script first on the Story Intelligence page.")
    st.stop()

data = st.session_state.data
scenes = data["scenes"]
characters = data["characters"]

# Check if character intelligence is available
if not st.session_state.get("intel"):
    st.warning("⚠️ Character intelligence not available. Please re-run analysis.")
    st.stop()

character_arcs = st.session_state.intel.get("character_arcs", {})

# Tabs for different visualizations
tab1, tab2, tab3 = st.tabs([
    "🕸️ Character Relationships",
    "📅 Scene Timeline",
    "📄 Character Arc PDFs"
])

# Tab 1: Character Relationship Graph
with tab1:
    st.header("Character Relationship Network")
    st.markdown("Interactive graph showing character interactions based on shared scenes")
    
    with st.spinner("Building relationship graph..."):
        graph_engine = RelationshipGraphEngine()
        graph = graph_engine.build_graph(scenes, characters[:20])  # Top 20 characters
        
        # Network metrics
        metrics = graph_engine.get_network_metrics()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Characters", metrics.get("nodes", 0))
        with col2:
            st.metric("Relationships", metrics.get("edges", 0))
        with col3:
            st.metric("Network Density", f"{metrics.get('density', 0):.2f}")
        with col4:
            clustering = metrics.get("average_clustering", 0)
            st.metric("Avg Clustering", f"{clustering:.2f}" if clustering else "N/A")
        
        # Centrality analysis
        st.subheader("Most Central Characters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Degree Centrality** (Most Connected)")
            top_degree = metrics.get("top_degree_centrality", [])
            for char, score in top_degree:
                st.write(f"• {char}: {score:.2f}")
        
        with col2:
            st.markdown("**Betweenness Centrality** (Story Connectors)")
            top_between = metrics.get("top_betweenness_centrality", [])
            for char, score in top_between:
                st.write(f"• {char}: {score:.2f}")
        
        # Interactive graph
        st.subheader("Interactive Network Graph")
        fig = graph_engine.create_plotly_visualization()
        st.plotly_chart(fig, use_container_width=True)
        
        # Individual character relationships
        st.subheader("Character Relationships")
        selected_char = st.selectbox(
            "Select character to view relationships:",
            options=characters[:20]
        )
        
        if selected_char:
            relationships = graph_engine.get_character_relationships(selected_char, top_n=10)
            if relationships:
                st.markdown(f"**{selected_char}'s strongest relationships:**")
                for related_char, strength in relationships:
                    st.write(f"• {related_char}: {strength} shared scenes")
            else:
                st.info(f"{selected_char} has no recorded relationships")

# Tab 2: Scene Timeline (Gantt Chart)
with tab2:
    st.header("Scene Timeline & Production Schedule")
    st.markdown("Visual timeline of scenes with estimated durations")
    
    gantt_engine = GanttChartEngine()
    
    # Production schedule summary
    schedule = gantt_engine.get_production_schedule(scenes)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Scenes", schedule["total_scenes"])
    with col2:
        st.metric("Est. Duration", f"{schedule['estimated_duration_minutes']} min")
    with col3:
        st.metric("Est. Shoot Days", schedule["estimated_shoot_days"])
    with col4:
        int_pct = (schedule["interior_scenes"] / schedule["total_scenes"] * 100) if schedule["total_scenes"] > 0 else 0
        st.metric("Interior Scenes", f"{int_pct:.0f}%")
    
    # Gantt chart options
    st.subheader("Timeline Visualization")
    
    viz_type = st.radio(
        "Select timeline view:",
        options=["All Scenes", "Character-Specific"],
        horizontal=True
    )
    
    if viz_type == "All Scenes":
        with st.spinner("Creating scene timeline..."):
            fig = gantt_engine.create_scene_gantt(scenes)
            st.plotly_chart(fig, use_container_width=True)
    
    else:  # Character-specific
        char_select = st.selectbox(
            "Select character:",
            options=characters[:20],
            key="gantt_char"
        )
        
        if char_select:
            with st.spinner(f"Creating timeline for {char_select}..."):
                fig = gantt_engine.create_character_timeline(scenes, char_select)
                st.plotly_chart(fig, use_container_width=True)
                
                # Character appearance stats
                char_scenes = [s for s in scenes if char_select in s.get("characters", [])]
                if char_scenes:
                    total_duration = sum(gantt_engine.estimate_scene_duration(s) for s in char_scenes)
                    st.info(f"📊 {char_select} appears in {len(char_scenes)} scenes (~{total_duration} minutes of screen time)")

# Tab 3: Character Arc PDF Exports
with tab3:
    st.header("Character Arc PDF Reports")
    st.markdown("Export individual character analysis to PDF format")
    
    # Character selection
    if character_arcs:
        st.subheader("Available Characters")
        
        # Show character list with metrics
        for char_name, arc_data in list(character_arcs.items())[:10]:
            with st.expander(f"**{char_name}** - {arc_data.get('scenes', 0)} scenes"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Dialogue Lines", arc_data.get("dialogue_lines", 0))
                with col2:
                    st.metric("Screen Time", f"{arc_data.get('estimated_screen_time_min', 0):.1f} min")
                with col3:
                    st.metric("Dominant Emotion", arc_data.get("dominant_emotion", "N/A").capitalize())
        
        st.divider()
        
        # Export options
        st.subheader("Export Options")
        
        export_option = st.radio(
            "Select export mode:",
            options=["Single Character", "All Characters"],
            horizontal=True
        )
        
        if export_option == "Single Character":
            selected_char = st.selectbox(
                "Select character to export:",
                options=list(character_arcs.keys())
            )
            
            if st.button("📄 Generate PDF Report", type="primary"):
                with st.spinner(f"Creating PDF for {selected_char}..."):
                    pdf_exporter = CharacterArcPDFExporter()
                    
                    # Create output directory
                    output_dir = "output/character_arcs"
                    os.makedirs(output_dir, exist_ok=True)
                    
                    # Sanitize filename
                    safe_name = "".join(c if c.isalnum() else "_" for c in selected_char)
                    output_path = os.path.join(output_dir, f"character_arc_{safe_name}.pdf")
                    
                    # Export
                    pdf_exporter.export_character_arc(
                        selected_char,
                        character_arcs[selected_char],
                        scenes,
                        output_path
                    )
                    
                    st.success(f"✅ PDF created: {output_path}")
                    
                    # Download button
                    with open(output_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Download PDF",
                            data=f.read(),
                            file_name=f"character_arc_{safe_name}.pdf",
                            mime="application/pdf"
                        )
        
        else:  # All Characters
            if st.button("📚 Generate All PDFs", type="primary"):
                with st.spinner("Creating PDFs for all characters..."):
                    pdf_exporter = CharacterArcPDFExporter()
                    
                    output_dir = "output/character_arcs"
                    pdf_files = pdf_exporter.export_all_character_arcs(
                        character_arcs,
                        scenes,
                        output_dir
                    )
                    
                    st.success(f"✅ Created {len(pdf_files)} PDF reports in {output_dir}")
                    
                    # Show list of created files
                    st.markdown("**Created files:**")
                    for pdf_file in pdf_files:
                        st.write(f"• {os.path.basename(pdf_file)}")
    
    else:
        st.info("No character arc data available. Please ensure emotion analysis has completed.")
