"""Integration tests for full CLI pipeline."""
import pytest
from pathlib import Path
import sys
import json
import shutil

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from ScriptIngest import run_full_analysis

SAMPLES_DIR = Path(__file__).parent.parent / 'samples'
OUTPUT_DIR = Path(__file__).parent.parent / 'test_output'

class TestCLIPipeline:
    """Test complete pipeline from script to exports."""
    
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Create and cleanup output directory."""
        OUTPUT_DIR.mkdir(exist_ok=True)
        yield
        # Cleanup after test
        if OUTPUT_DIR.exists():
            shutil.rmtree(OUTPUT_DIR)
    
    def test_fdx_end_to_end(self):
        """Test complete pipeline with FDX input."""
        result = run_full_analysis(
            str(SAMPLES_DIR / 'test_script.fdx'),
            str(OUTPUT_DIR)
        )
        
        # Check result structure
        assert 'scenes' in result
        assert 'characters' in result
        assert 'budget_summary' in result
        assert 'budget_rows' in result
        assert 'risk_rows' in result
        
        # Check outputs were created
        assert (OUTPUT_DIR / 'scenes.csv').exists()
        assert (OUTPUT_DIR / 'summary.json').exists()
        
        # Validate summary.json
        summary = json.loads((OUTPUT_DIR / 'summary.json').read_text())
        assert 'scene_count' in summary
        assert 'total_budget' in summary
        assert summary['scene_count'] > 0
        
    def test_episode1_end_to_end(self):
        """Test pipeline with episode1.fdx."""
        result = run_full_analysis(
            str(SAMPLES_DIR / 'episode1.fdx'),
            str(OUTPUT_DIR / 'ep1')
        )
        
        assert result['scenes']
        assert len(result['scenes']) == 3
        assert (OUTPUT_DIR / 'ep1' / 'summary.json').exists()

class TestMultipleFormats:
    """Test pipeline works with different script formats."""
    
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        OUTPUT_DIR.mkdir(exist_ok=True)
        yield
        if OUTPUT_DIR.exists():
            shutil.rmtree(OUTPUT_DIR)
    
    def test_fountain_format(self):
        """Test pipeline with Fountain format."""
        result = run_full_analysis(
            str(SAMPLES_DIR / 'test_script.fountain'),
            str(OUTPUT_DIR / 'fountain')
        )
        assert 'scenes' in result
        
    def test_celtx_format(self):
        """Test pipeline with Celtx format."""
        result = run_full_analysis(
            str(SAMPLES_DIR / 'test_script.celtx.json'),
            str(OUTPUT_DIR / 'celtx')
        )
        assert 'scenes' in result

if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
