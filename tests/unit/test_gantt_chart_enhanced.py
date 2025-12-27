"""
Extended unit tests for GanttChartEngine - Enhanced Features
"""
import pytest
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.VisualizationEngine.gantt_chart_engine import GanttChartEngine


class TestGanttChartEngineEnhanced:
    """Extended test suite for enhanced Gantt chart features."""
    
    @pytest.fixture
    def engine(self):
        """Create engine instance."""
        return GanttChartEngine()
    
    @pytest.fixture
    def mixed_scenes(self):
        """Scenes with mixed INT/EXT and special characters."""
        return [
            {
                "heading": "INT. CAFE - DAY",
                "characters": ["ALICE", "BOB"],
                "dialogue_lines": 15,
                "action_lines": 5
            },
            {
                "heading": "EXT. PARK - NIGHT",
                "characters": ["ALICE"],
                "dialogue_lines": 5,
                "action_lines": 10
            },
            {
                "heading": "INT./EXT. CAR - DAY",
                "characters": ["BOB", "CHARLIE"],
                "dialogue_lines": 20,
                "action_lines": 8
            }
        ]
    
    @pytest.fixture
    def long_scenes(self):
        """Very long scenes for stress testing."""
        return [
            {
                "heading": "INT. BALLROOM - NIGHT",
                "characters": ["ENSEMBLE"],
                "dialogue_lines": 100,
                "action_lines": 50
            }
        ]
    
    def test_create_daily_schedule_basic(self, engine, mixed_scenes):
        """Test daily schedule creation."""
        schedule = engine.create_daily_schedule(mixed_scenes)
        
        assert 'days' in schedule
        assert 'total_days' in schedule
        assert schedule['total_days'] > 0
        assert len(schedule['days']) == schedule['total_days']
    
    def test_create_daily_schedule_empty(self, engine):
        """Test daily schedule with no scenes."""
        schedule = engine.create_daily_schedule([])
        
        assert schedule['total_days'] == 0
        assert len(schedule['days']) == 0
    
    def test_create_daily_schedule_with_start_date(self, engine, mixed_scenes):
        """Test daily schedule with custom start date."""
        start = datetime(2025, 6, 1)
        schedule = engine.create_daily_schedule(mixed_scenes, start_date=start)
        
        assert schedule['days'][0]['date'] == start
    
    def test_daily_schedule_respects_day_limit(self, engine):
        """Test that scenes don't exceed daily time limit."""
        # Create scenes that total more than one day
        scenes = [
            {"dialogue_lines": 500, "action_lines": 500, "heading": "INT. OFFICE"}
            for _ in range(3)
        ]
        schedule = engine.create_daily_schedule(scenes)
        
        # Should span multiple days
        assert schedule['total_days'] > 1
        
        # Each day should not exceed limit
        for day in schedule['days']:
            assert day['total_minutes'] <= engine.minutes_per_day
    
    def test_calculate_resource_needs_basic(self, engine, mixed_scenes):
        """Test resource calculation."""
        resources = engine.calculate_resource_needs(mixed_scenes)
        
        assert 'crew_size' in resources
        assert 'equipment_packages' in resources
        assert 'estimated_budget' in resources
        assert 'location_count' in resources
        assert 'character_count' in resources
        
        assert resources['crew_size'] > 0
        assert len(resources['equipment_packages']) > 0
        assert resources['estimated_budget'] > 0
    
    def test_calculate_resource_needs_empty(self, engine):
        """Test resource calculation with no scenes."""
        resources = engine.calculate_resource_needs([])
        
        assert resources['crew_size'] == 0
        assert resources['estimated_budget'] == 0
        assert resources['location_count'] == 0
    
    def test_resource_needs_detects_night_scenes(self, engine, mixed_scenes):
        """Test that night scenes are detected."""
        resources = engine.calculate_resource_needs(mixed_scenes)
        
        assert resources['night_scenes'] == 1  # One NIGHT scene in fixtures
        assert 'Night Lighting Package' in resources['equipment_packages']
    
    def test_resource_needs_scales_with_production_size(self, engine):
        """Test that crew size scales appropriately."""
        # Small production
        small_scenes = [{"dialogue_lines": 5, "action_lines": 5, "heading": f"INT. ROOM {i}"} for i in range(10)]
        small_resources = engine.calculate_resource_needs(small_scenes)
        
        # Large production
        large_scenes = [{"dialogue_lines": 5, "action_lines": 5, "heading": f"INT. ROOM {i}"} for i in range(60)]
        large_resources = engine.calculate_resource_needs(large_scenes)
        
        assert large_resources['crew_size'] > small_resources['crew_size']
    
    def test_export_schedule_to_csv(self, engine, mixed_scenes, tmp_path):
        """Test CSV export functionality."""
        csv_file = tmp_path / "test_schedule.csv"
        result = engine.export_schedule_to_csv(mixed_scenes, str(csv_file))
        
        assert os.path.exists(result)
        
        # Verify CSV content
        with open(result, 'r') as f:
            content = f.read()
            assert 'Day' in content
            assert 'Scene' in content
            assert 'ALICE' in content
    
    def test_mixed_int_ext_scenes(self, engine, mixed_scenes):
        """Test handling of mixed INT/EXT scenes."""
        schedule = engine.get_production_schedule(mixed_scenes)
        
        # Should count both INT and EXT
        assert schedule['interior_scenes'] >= 1
        assert schedule['exterior_scenes'] >= 1
    
    def test_special_characters_in_heading(self, engine):
        """Test scenes with special characters in headings."""
        scenes = [
            {
                "heading": "INT. CAFE & BAKERY - DAY (FLASHBACK)",
                "characters": ["ALICE"],
                "dialogue_lines": 10,
                "action_lines": 5
            }
        ]
        
        fig = engine.create_scene_gantt(scenes)
        assert fig is not None
    
    def test_very_long_scene(self, engine, long_scenes):
        """Test handling of very long scenes."""
        duration = engine.estimate_scene_duration(long_scenes[0])
        
        # 100 dialogue * 0.5 + 50 action * 0.3 = 50 + 15 = 65 minutes
        assert duration == 65
        
        schedule = engine.get_production_schedule(long_scenes)
        assert schedule['estimated_shoot_days'] >= 1
    
    def test_character_tracking_accuracy(self, engine, mixed_scenes):
        """Test accurate character tracking across scenes."""
        resources = engine.calculate_resource_needs(mixed_scenes)
        
        # Should find all unique characters
        expected_characters = {'ALICE', 'BOB', 'CHARLIE'}
        assert resources['character_count'] == len(expected_characters)
    
    def test_location_count_accuracy(self, engine, mixed_scenes):
        """Test accurate location counting."""
        resources = engine.calculate_resource_needs(mixed_scenes)
        
        # Each scene has unique heading
        assert resources['location_count'] == len(mixed_scenes)
    
    def test_equipment_package_completeness(self, engine, mixed_scenes):
        """Test that all necessary equipment is included."""
        resources = engine.calculate_resource_needs(mixed_scenes)
        packages = resources['equipment_packages']
        
        # Should always have camera and sound
        assert 'Camera Package' in packages
        assert 'Sound Package' in packages
        assert 'Grip & Electric' in packages


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
