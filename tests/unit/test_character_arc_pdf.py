"""
Unit tests for CharacterArcPDFExporter
"""

import pytest
import sys
import os
import tempfile
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.VisualizationEngine.character_arc_pdf import CharacterArcPDFExporter


class TestCharacterArcPDFExporter:
    """Test suite for character arc PDF export."""
    
    @pytest.fixture
    def sample_arc_data(self):
        """Sample character arc data."""
        return {
            "scenes": 5,
            "dialogue_lines": 15,
            "estimated_screen_time_min": 7.5,
            "dominant_emotion": "joy",
            "emotions": {
                "joy": 0.6,
                "neutral": 0.2,
                "sadness": 0.1,
                "fear": 0.1
            }
        }
    
    @pytest.fixture
    def sample_scenes(self):
        """Sample scenes."""
        return [
            {
                "heading": "INT. OFFICE - DAY",
                "characters": ["ALICE", "BOB"],
                "lines": [
                    {"type": "dialogue", "character": "ALICE", "text": "Hello"},
                    {"type": "dialogue", "character": "BOB", "text": "Hi"}
                ]
            },
            {
                "heading": "EXT. PARK - DAY",
                "characters": ["ALICE"],
                "lines": [
                    {"type": "dialogue", "character": "ALICE", "text": "Nice day"}
                ]
            }
        ]
    
    @pytest.fixture
    def exporter(self):
        """Create exporter instance."""
        return CharacterArcPDFExporter()
    
    def test_initialization(self, exporter):
        """Test exporter initializes correctly."""
        assert exporter.styles is not None
        assert "CustomTitle" in exporter.styles
        assert "SectionHeader" in exporter.styles
    
    def test_export_character_arc(self, exporter, sample_arc_data, sample_scenes):
        """Test single character PDF export."""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            output_path = tmp.name
        
        try:
            result = exporter.export_character_arc(
                "ALICE",
                sample_arc_data,
                sample_scenes,
                output_path
            )
            
            assert result == output_path
            assert os.path.exists(output_path)
            assert os.path.getsize(output_path) > 0
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)
    
    def test_export_all_character_arcs(self, exporter, sample_arc_data, sample_scenes):
        """Test batch PDF export."""
        character_arcs = {
            "ALICE": sample_arc_data,
            "BOB": {**sample_arc_data, "scenes": 3}
        }
        
        with tempfile.TemporaryDirectory() as tmpdir:
            pdf_files = exporter.export_all_character_arcs(
                character_arcs,
                sample_scenes,
                tmpdir
            )
            
            assert len(pdf_files) == 2
            for pdf_file in pdf_files:
                assert os.path.exists(pdf_file)
                assert os.path.getsize(pdf_file) > 0
    
    def test_empty_emotions(self, exporter, sample_scenes):
        """Test handling of missing emotion data."""
        arc_data = {
            "scenes": 1,
            "dialogue_lines": 5,
            "estimated_screen_time_min": 2.0,
            "dominant_emotion": "neutral",
            "emotions": {}  # Empty
        }
        
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            output_path = tmp.name
        
        try:
            result = exporter.export_character_arc(
                "TEST",
                arc_data,
                sample_scenes,
                output_path
            )
            
            assert os.path.exists(output_path)
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
