"""
Test script for new visualization engines
"""

from src.IngestEngine.fdx_loader import load_fdx
from src.VisualizationEngine.relationship_graph_engine import RelationshipGraphEngine
from src.VisualizationEngine.gantt_chart_engine import GanttChartEngine
from src.VisualizationEngine.character_arc_pdf import CharacterArcPDFExporter
import os

def test_relationship_graph():
    """Test character relationship graph."""
    print("\n" + "="*60)
    print("Testing Character Relationship Graph")
    print("="*60)
    
    # Load test script
    parsed = load_fdx("samples/test_script.fdx")
    scenes = parsed["scenes"]
    characters = parsed["characters"]
    
    print(f"Loaded: {len(scenes)} scenes, {len(characters)} characters")
    
    # Build graph
    graph_engine = RelationshipGraphEngine()
    graph = graph_engine.build_graph(scenes, characters)
    
    print(f"✅ Graph built: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")
    
    # Get metrics
    metrics = graph_engine.get_network_metrics()
    print(f"   Network density: {metrics.get('density', 0):.2f}")
    print(f"   Top central character: {metrics['top_degree_centrality'][0] if metrics.get('top_degree_centrality') else 'N/A'}")
    
    # Test visualization
    fig = graph_engine.create_plotly_visualization()
    print(f"✅ Plotly visualization created ({len(fig.data)} traces)")
    
    return graph_engine


def test_gantt_chart():
    """Test scene Gantt chart."""
    print("\n" + "="*60)
    print("Testing Scene Gantt Chart")
    print("="*60)
    
    parsed = load_fdx("samples/test_script.fdx")
    scenes = parsed["scenes"]
    
    gantt_engine = GanttChartEngine()
    
    # Get production schedule
    schedule = gantt_engine.get_production_schedule(scenes)
    print(f"Total scenes: {schedule['total_scenes']}")
    print(f"Est. duration: {schedule['estimated_duration_minutes']} minutes")
    print(f"Est. shoot days: {schedule['estimated_shoot_days']}")
    print(f"Interior/Exterior: {schedule['interior_scenes']}/{schedule['exterior_scenes']}")
    
    # Create Gantt chart
    fig = gantt_engine.create_scene_gantt(scenes)
    print(f"✅ Gantt chart created ({len(fig.data)} traces)")
    
    # Create character timeline
    if parsed["characters"]:
        char = parsed["characters"][0]
        fig = gantt_engine.create_character_timeline(scenes, char)
        print(f"✅ Character timeline created for '{char}'")
    
    return gantt_engine


def test_character_arc_pdf():
    """Test character arc PDF export."""
    print("\n" + "="*60)
    print("Testing Character Arc PDF Export")
    print("="*60)
    
    parsed = load_fdx("samples/test_script.fdx")
    scenes = parsed["scenes"]
    characters = parsed["characters"]
    
    # Create mock arc data
    mock_arc = {
        "scenes": 2,
        "dialogue_lines": 5,
        "estimated_screen_time_min": 3.5,
        "dominant_emotion": "neutral",
        "emotions": {
            "neutral": 0.6,
            "joy": 0.2,
            "sadness": 0.1,
            "fear": 0.1
        }
    }
    
    pdf_exporter = CharacterArcPDFExporter()
    
    output_dir = "output/test_visualizations"
    os.makedirs(output_dir, exist_ok=True)
    
    if characters:
        char = characters[0]
        output_path = os.path.join(output_dir, f"test_arc_{char}.pdf")
        
        pdf_exporter.export_character_arc(char, mock_arc, scenes, output_path)
        print(f"✅ PDF created: {output_path}")
        
        # Verify file exists
        if os.path.exists(output_path):
            size_kb = os.path.getsize(output_path) / 1024
            print(f"   File size: {size_kb:.1f} KB")
        else:
            print("❌ PDF file not found!")
    
    return pdf_exporter


if __name__ == "__main__":
    print("\n" + "#"*60)
    print("VISUALIZATION ENGINES TEST SUITE")
    print("#"*60)
    
    try:
        # Test all engines
        graph_engine = test_relationship_graph()
        gantt_engine = test_gantt_chart()
        pdf_exporter = test_character_arc_pdf()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED")
        print("="*60)
        print("New visualization engines are ready!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
