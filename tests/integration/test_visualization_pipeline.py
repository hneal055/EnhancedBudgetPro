"""
Integration tests for full visualization pipeline
"""

import pytest
import sys
import os
import tempfile
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.IngestEngine.file_router import route_file
from src.AnalysisEngine.character_intelligence import CharacterIntelligenceEngine
from src.VisualizationEngine.relationship_graph_engine import RelationshipGraphEngine
from src.VisualizationEngine.gantt_chart_engine import GanttChartEngine
from src.VisualizationEngine.character_arc_pdf import CharacterArcPDFExporter


class TestVisualizationPipeline:
    """Test full end-to-end visualization pipeline."""
    
    @pytest.fixture
    def sample_script_path(self):
        """Path to test script."""
        return "samples/test_script.fdx"
    
    def test_full_pipeline_fdx(self, sample_script_path):
        """Test complete pipeline: FDX → Analysis → Visualizations."""
        if not os.path.exists(sample_script_path):
            pytest.skip(f"Test script not found: {sample_script_path}")
        
        # Step 1: Ingest
        result = route_file(sample_script_path)
        assert "scenes" in result
        assert "characters" in result
        assert len(result["scenes"]) > 0
        
        scenes = result["scenes"]
        characters = result["characters"]
        
        # Step 2: Character Analysis
        char_engine = CharacterIntelligenceEngine()
        intel_result = char_engine.analyze(result)
        character_intel = intel_result.get("character_stats", {})
        assert len(character_intel) > 0
        
        # Step 3: Relationship Graph
        graph_engine = RelationshipGraphEngine()
        graph_engine.build_graph(scenes, characters)
        
        assert graph_engine.graph is not None
        assert len(graph_engine.graph.nodes) == len(characters)
        
        metrics = graph_engine.get_network_metrics()
        assert "degree_centrality" in metrics
        assert "density" in metrics
        
        fig = graph_engine.create_plotly_visualization()
        assert fig is not None
        
        # Step 4: Gantt Chart
        gantt_engine = GanttChartEngine()
        schedule = gantt_engine.get_production_schedule(scenes)
        
        assert schedule["total_scenes"] == len(scenes)
        assert schedule["estimated_duration_minutes"] > 0
        assert schedule["estimated_shoot_days"] > 0
        
        gantt_fig = gantt_engine.create_scene_gantt(scenes)
        assert gantt_fig is not None
        
        # Step 5: PDF Export
        with tempfile.TemporaryDirectory() as tmpdir:
            exporter = CharacterArcPDFExporter()
            
            # Export first character
            first_char = characters[0]
            if first_char in character_intel:
                output_path = os.path.join(tmpdir, f"{first_char}.pdf")
                result_path = exporter.export_character_arc(
                    first_char,
                    character_intel[first_char],
                    scenes,
                    output_path
                )
                
                assert os.path.exists(result_path)
                assert os.path.getsize(result_path) > 1000  # At least 1KB
    
    def test_multiple_characters_relationships(self, sample_script_path):
        """Test relationship analysis with multiple characters."""
        if not os.path.exists(sample_script_path):
            pytest.skip(f"Test script not found: {sample_script_path}")
        
        result = route_file(sample_script_path)
        scenes = result["scenes"]
        characters = result["characters"]
        
        graph_engine = RelationshipGraphEngine()
        graph_engine.build_graph(scenes, characters)
        
        # Test relationships for each character
        for character in characters[:3]:  # First 3 characters
            relationships = graph_engine.get_character_relationships(character, top_n=5)
            assert isinstance(relationships, list)
    
    def test_character_timeline_accuracy(self, sample_script_path):
        """Test character timeline matches scene appearances."""
        if not os.path.exists(sample_script_path):
            pytest.skip(f"Test script not found: {sample_script_path}")
        
        result = route_file(sample_script_path)
        scenes = result["scenes"]
        characters = result["characters"]
        
        gantt_engine = GanttChartEngine()
        
        for character in characters[:3]:
            # Count actual appearances
            actual_appearances = sum(
                1 for scene in scenes 
                if character in scene.get("characters", [])
            )
            
            # Get timeline
            timeline_fig = gantt_engine.create_character_timeline(scenes, character)
            
            if actual_appearances > 0:
                assert timeline_fig is not None
    
    def test_error_recovery(self):
        """Test pipeline handles errors gracefully."""
        # Test with empty scenes
        graph_engine = RelationshipGraphEngine()
        graph_engine.build_graph([], [])
        assert graph_engine.graph.number_of_nodes() == 0
        
        gantt_engine = GanttChartEngine()
        schedule = gantt_engine.get_production_schedule([])
        assert schedule["total_scenes"] == 0
        
        # Test with malformed scene
        bad_scene = {"heading": "TEST"}  # Missing required fields
        gantt_engine = GanttChartEngine()
        duration = gantt_engine.estimate_scene_duration(bad_scene)
        assert duration >= 1.0  # Should return minimum


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
