
"""
Minimal test for Storytelling Insights prerequisites.
"""

def test_basic_prerequisites():
    """Test that the module file exists and has basic structure."""
    # Check 1: Module file exists
    import os
    assert os.path.exists('pages/16_Storytelling_Insights.py'), 'Module file should exist'
    
    # Check 2: Module has basic content
    with open('pages/16_Storytelling_Insights.py', 'r') as f:
        content = f.read()
    
    assert 'import streamlit' in content, 'Should import streamlit'
    assert 'session_state' in content, 'Should use session_state'
    
    print('✓ Basic test passed')
    return True

if __name__ == '__main__':
    try:
        test_basic_prerequisites()
        print('✅ All tests passed')
    except AssertionError as e:
        print(f'❌ Test failed: {e}')
