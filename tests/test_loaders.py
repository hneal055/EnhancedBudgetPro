"""Unit tests for script loaders."""
import pytest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from IngestEngine.fdx_loader import load_fdx
from IngestEngine.fountain_loader import load_fountain
from IngestEngine.celtx_loader import load_celtx
from IngestEngine.plaintext_loader import load_text

SAMPLES_DIR = Path(__file__).parent.parent / 'samples'

class TestLoaderContract:
    """Test that all loaders return the correct data structure."""
    
    def test_fdx_loader_returns_correct_schema(self):
        """FDX loader should return scenes, characters, scene_count."""
        result = load_fdx(str(SAMPLES_DIR / 'test_script.fdx'))
        
        assert 'scenes' in result
        assert 'characters' in result
        assert 'scene_count' in result
        assert isinstance(result['scenes'], list)
        assert isinstance(result['characters'], list)
        assert isinstance(result['scene_count'], int)
        
    def test_fdx_scene_structure(self):
        """Each FDX scene should have required fields."""
        result = load_fdx(str(SAMPLES_DIR / 'test_script.fdx'))
        
        if result['scenes']:
            scene = result['scenes'][0]
            assert 'heading' in scene
            assert 'lines' in scene
            assert 'characters' in scene
            assert 'dialogue_lines' in scene
            assert 'action_lines' in scene
            assert isinstance(scene['lines'], list)

class TestFDXLoader:
    """Specific tests for FDX loader."""
    
    def test_fdx_extracts_scenes(self):
        """FDX should extract all Scene Heading paragraphs."""
        result = load_fdx(str(SAMPLES_DIR / 'test_script.fdx'))
        assert result['scene_count'] >= 3, "test_script.fdx should have at least 3 scenes"
        
    def test_fdx_extracts_episode1(self):
        """Test episode1.fdx parsing."""
        result = load_fdx(str(SAMPLES_DIR / 'episode1.fdx'))
        assert result['scene_count'] == 3, "episode1.fdx should have exactly 3 scenes"
        assert len(result['scenes']) == 3

class TestFountainLoader:
    """Specific tests for Fountain loader."""
    
    def test_fountain_basic_parsing(self):
        """Fountain should parse test_script.fountain."""
        result = load_fountain(str(SAMPLES_DIR / 'test_script.fountain'))
        assert 'scenes' in result
        assert isinstance(result['scenes'], list)

class TestCeltxLoader:
    """Specific tests for Celtx loader."""
    
    def test_celtx_basic_parsing(self):
        """Celtx should parse test_script.celtx.json."""
        result = load_celtx(str(SAMPLES_DIR / 'test_script.celtx.json'))
        assert 'scenes' in result
        assert isinstance(result['scenes'], list)

class TestPlaintextLoader:
    """Specific tests for plaintext loader."""
    
    def test_plaintext_fallback(self):
        """Plaintext loader should handle any text file."""
        # Create a simple test file
        test_txt = SAMPLES_DIR / 'test_temp.txt'
        test_txt.write_text("INT. TEST - DAY\n\nSome action.\n")
        
        try:
            result = load_text(str(test_txt))
            assert 'scenes' in result
            assert isinstance(result['scenes'], list)
        finally:
            if test_txt.exists():
                test_txt.unlink()

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
