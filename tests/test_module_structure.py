import streamlit as st
"""
Test the structure of the Storytelling Insights module.
"""

import re

def test_module_structure():
    """Test that the module has the required structure."""
    with open("pages/16_Storytelling_Insights.py", "r") as f:
        content = f.read()
    
    tests = [
        ("Module imports streamlit", lambda: "import streamlit" in content),
        ("Sets page config", lambda: "st.set_page_config" in content),
        ("Has title or header", lambda: "st.title" in content or "st.header" in content),
        ("Uses session_state", lambda: "st.session_state" in content),
        ("Checks for data", lambda: 'st.session_state.get("data")' in content or 'session_state.get("data")' in content),
        ("Checks for emotion_data", lambda: 'emotion_data' in content),
        ("Checks for character_arcs", lambda: 'character_arcs' in content),
        ("Has error handling", lambda: "st.error" in content),
        ("Has stop calls for missing data", lambda: "st.stop()" in content),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                print(f"✓ {test_name}")
                passed += 1
            else:
                print(f"✗ {test_name}")
                failed += 1
        except Exception as e:
            print(f"✗ {test_name} - Error: {e}")
            failed += 1
    
    # Additional test: Count prerequisite checks
    lines = content.split('\n')
    stop_calls = sum(1 for line in lines if 'st.stop()' in line)
    error_messages = sum(1 for line in lines if 'st.error' in line)
    
    print(f"✓ Found {stop_calls} st.stop() calls (prerequisite checks)")
    print(f"✓ Found {error_messages} error messages")
    
    return passed, failed, stop_calls, error_messages

if __name__ == "__main__":
    print("Testing module structure...")
    print("=" * 50)
    
    try:
        passed, failed, stop_calls, error_messages = test_module_structure()
        
        print("=" * 50)
        print(f"Structure tests: {passed} passed, {failed} failed")
        print(f"Prerequisite checks: {stop_calls}")
        print(f"Error messages: {error_messages}")
        
        if failed == 0 and stop_calls >= 2:  # At least 2 prerequisite checks
            print("✅ Module structure looks good!")
            exit(0)
        else:
            print("⚠ Module may need more prerequisite checks")
            exit(1)
    except FileNotFoundError:
        print("❌ Module file not found")
        exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)
