# tests/test_imports.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

def test_import_shared_utils():
    """Test that shared_utils imports correctly"""
    from IngestEngine.shared_utils import compute_counts
    
    # Test the function
    test_content = """INT. HOUSE - DAY
    
    JOHN sits at a table.
    
    JOHN
    Hello world.
    
    MARY
    Hi John.
    """
    
    counts = compute_counts(test_content)
    assert counts is not None
    assert "character_count" in counts
    assert counts["character_count"] == 2  # JOHN and MARY
    assert "JOHN" in counts["characters"]
    assert "MARY" in counts["characters"]
    print("✓ shared_utils.compute_counts works!")

def test_import_fdx_loader():
    """Test that fdx_loader imports correctly"""
    try:
        from IngestEngine.fdx_loader import load_fdx
        print("✓ fdx_loader imports successfully!")
    except ImportError as e:
        print(f"✗ fdx_loader import failed: {e}")

def test_import_script_ingest():
    """Test that ScriptIngest imports correctly"""
    try:
        import ScriptIngest
        print("✓ ScriptIngest imports successfully!")
        print(f"  Available functions: {[x for x in dir(ScriptIngest) if not x.startswith('_')]}")
    except ImportError as e:
        print(f"✗ ScriptIngest import failed: {e}")

if __name__ == "__main__":
    test_import_shared_utils()
    test_import_fdx_loader()
    test_import_script_ingest()