"""
Unit tests for GanttChartEngine
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.VisualizationEngine.gantt_chart_engine import GanttChartEngine


class TestGanttChartEngine:
    """Test suite for Gantt chart timeline generation."""
    
    @pytest.fixture
    def sample_scenes(self):
        """Sample scene data."""
        return [
            {
                "heading": "INT. OFFICE - DAY",
                "characters": ["ALICE", "BOB"],
                "dialogue_lines": 10,
                "action_lines": 5
            },
            {
                "heading": "EXT. PARK - DAY",
                "characters": ["ALICE"],
                "dialogue_lines": 3,
                "action_lines": 2
            },
            {
                "heading": "INT. COFFEE SHOP - EVENING",
                "characters": ["BOB", "CHARLIE"],
                "dialogue_lines": 8,
                "action_lines": 3
            }
        ]
    
    @pytest.fixture
    def engine(self):
        """Create engine instance."""
        return GanttChartEngine()
    
    def test_initialization(self, engine):
        """Test engine initializes correctly."""
        assert engine is not None
    
    def test_estimate_scene_duration(self, engine):
        """Test scene duration estimation."""
        scene = {
            "dialogue_lines": 10,
            "action_lines": 5
        }
        
        duration = engine.estimate_scene_duration(scene)
        expected = int(10 * 0.5 + 5 * 0.3)  # 5 + 1.5 = 6.5 -> 6
        assert duration == expected
    
    def test_estimate_scene_duration_minimum(self, engine):
        """Test minimum duration is 1 minute."""
        scene = {
            "dialogue_lines": 0,
            "action_lines": 0
        }
        
        duration = engine.estimate_scene_duration(scene)
        assert duration == 1  # Minimum
    
    def test_get_production_schedule(self, engine, sample_scenes):
        """Test production schedule calculation."""
        schedule = engine.get_production_schedule(sample_scenes)
        
        assert schedule["total_scenes"] == 3
        assert schedule["estimated_duration_minutes"] > 0
        assert schedule["estimated_shoot_days"] >= 1
        assert schedule["interior_scenes"] == 2
        assert schedule["exterior_scenes"] == 1
    
    def test_create_scene_gantt(self, engine, sample_scenes):
        """Test Gantt chart creation."""
        fig = engine.create_scene_gantt(sample_scenes)
        
        assert fig is not None
        assert len(fig.data) > 0
    
    def test_create_character_timeline(self, engine, sample_scenes):
        """Test character-specific timeline."""
        fig = engine.create_character_timeline(sample_scenes, "ALICE")
        
        assert fig is not None
        # ALICE appears in 2 scenes
    
    def test_character_timeline_no_appearances(self, engine, sample_scenes):
        """Test timeline for character with no appearances."""
        fig = engine.create_character_timeline(sample_scenes, "DAVID")
        
        assert fig is not None
        # Should create figure with annotation
    
    def test_empty_scenes(self, engine):
        """Test handling of empty scene list."""
        fig = engine.create_scene_gantt([])
        assert fig is not None
        
        schedule = engine.get_production_schedule([])
        assert schedule["total_scenes"] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
