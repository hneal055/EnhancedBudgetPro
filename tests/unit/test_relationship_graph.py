"""
Unit tests for RelationshipGraphEngine
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.VisualizationEngine.relationship_graph_engine import RelationshipGraphEngine


class TestRelationshipGraphEngine:
    """Test suite for character relationship graph analysis."""
    
    @pytest.fixture
    def sample_scenes(self):
        """Sample scene data for testing."""
        return [
            {
                "heading": "INT. OFFICE - DAY",
                "characters": ["ALICE", "BOB"],
                "lines": [
                    {"type": "dialogue", "character": "ALICE", "text": "Hello Bob"},
                    {"type": "dialogue", "character": "BOB", "text": "Hi Alice"}
                ]
            },
            {
                "heading": "EXT. PARK - DAY",
                "characters": ["ALICE", "CHARLIE"],
                "lines": [
                    {"type": "dialogue", "character": "ALICE", "text": "Hey Charlie"},
                    {"type": "action", "text": "They walk together"}
                ]
            },
            {
                "heading": "INT. COFFEE SHOP - DAY",
                "characters": ["BOB", "CHARLIE"],
                "lines": [
                    {"type": "dialogue", "character": "BOB", "text": "Nice day"},
                    {"type": "dialogue", "character": "CHARLIE", "text": "Indeed"}
                ]
            }
        ]
    
    @pytest.fixture
    def characters(self):
        """Sample character list."""
        return ["ALICE", "BOB", "CHARLIE"]
    
    @pytest.fixture
    def engine(self):
        """Create engine instance."""
        return RelationshipGraphEngine()
    
    def test_initialization(self, engine):
        """Test engine initializes correctly."""
        assert engine.graph is None
    
    def test_build_graph_nodes(self, engine, sample_scenes, characters):
        """Test graph builds with correct nodes."""
        graph = engine.build_graph(sample_scenes, characters)
        
        assert graph.number_of_nodes() == 3
        assert "ALICE" in graph.nodes
        assert "BOB" in graph.nodes
        assert "CHARLIE" in graph.nodes
    
    def test_build_graph_edges(self, engine, sample_scenes, characters):
        """Test graph builds with correct edges."""
        graph = engine.build_graph(sample_scenes, characters)
        
        # All pairs should have edges (fully connected)
        assert graph.has_edge("ALICE", "BOB")
        assert graph.has_edge("ALICE", "CHARLIE")
        assert graph.has_edge("BOB", "CHARLIE")
        
        # Edge weights should be 1 (each pair appears once together)
        assert graph["ALICE"]["BOB"]["weight"] == 1
        assert graph["ALICE"]["CHARLIE"]["weight"] == 1
        assert graph["BOB"]["CHARLIE"]["weight"] == 1
    
    def test_node_attributes(self, engine, sample_scenes, characters):
        """Test node attributes are calculated correctly."""
        graph = engine.build_graph(sample_scenes, characters)
        
        # ALICE appears in 2 scenes, has 2 dialogue lines
        assert graph.nodes["ALICE"]["scenes"] == 2
        assert graph.nodes["ALICE"]["dialogue_lines"] == 2
        
        # BOB appears in 2 scenes, has 2 dialogue lines
        assert graph.nodes["BOB"]["scenes"] == 2
        assert graph.nodes["BOB"]["dialogue_lines"] == 2
        
        # CHARLIE appears in 2 scenes, has 1 dialogue line
        assert graph.nodes["CHARLIE"]["scenes"] == 2
        assert graph.nodes["CHARLIE"]["dialogue_lines"] == 1
    
    def test_network_metrics(self, engine, sample_scenes, characters):
        """Test network metrics calculation."""
        engine.build_graph(sample_scenes, characters)
        metrics = engine.get_network_metrics()
        
        assert metrics["nodes"] == 3
        assert metrics["edges"] == 3
        assert "density" in metrics
        assert "degree_centrality" in metrics
        assert "betweenness_centrality" in metrics
    
    def test_get_character_relationships(self, engine, sample_scenes, characters):
        """Test getting character relationships."""
        engine.build_graph(sample_scenes, characters)
        
        alice_rels = engine.get_character_relationships("ALICE", top_n=5)
        assert len(alice_rels) == 2  # ALICE has 2 relationships
        
        # Check relationship format
        for char, weight in alice_rels:
            assert isinstance(char, str)
            assert isinstance(weight, int)
            assert weight > 0
    
    def test_empty_scenes(self, engine, characters):
        """Test handling of empty scenes."""
        graph = engine.build_graph([], characters)
        
        assert graph.number_of_nodes() == 3
        assert graph.number_of_edges() == 0
    
    def test_create_visualization(self, engine, sample_scenes, characters):
        """Test Plotly visualization creation."""
        engine.build_graph(sample_scenes, characters)
        fig = engine.create_plotly_visualization()
        
        assert fig is not None
        assert len(fig.data) > 0  # Should have traces
    
    def test_nonexistent_character_relationships(self, engine, sample_scenes, characters):
        """Test querying relationships for nonexistent character."""
        engine.build_graph(sample_scenes, characters)
        
        rels = engine.get_character_relationships("DAVID", top_n=5)
        assert rels == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
