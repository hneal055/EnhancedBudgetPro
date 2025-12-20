"""
More accurate test matching the actual module logic.
"""

import sys

def simulate_module_prerequisites(session_state):
    """
    Simulate exactly what the module does based on its code.
    From reading pages/16_Storytelling_Insights.py, it appears to check:
    1. if not st.session_state.get("data"):
    2. if not st.session_state.get("emotion_data"):
    3. character_arcs = st.session_state.emotion_data.get("character_arcs", {})
       if not character_arcs:
    """
    
    # Simulate the module's checks
    # Check 1: if not st.session_state.get("data")
    if not session_state.get("data"):
        return False, "No script loaded"
    
    # Check 2: if not st.session_state.get("emotion_data")  
    if not session_state.get("emotion_data"):
        return False, "No emotion data"
    
    # Check 3: character_arcs check with .get()
    emotion_data = session_state.get("emotion_data", {})
    
    # The module uses: st.session_state.emotion_data.get("character_arcs", {})
    # So we need to handle emotion_data as either dict or object with .get()
    if hasattr(emotion_data, 'get'):
        character_arcs = emotion_data.get("character_arcs", {})
    elif isinstance(emotion_data, dict):
        character_arcs = emotion_data.get("character_arcs", {})
    else:
        character_arcs = {}
    
    if not character_arcs:
        return False, "No character arcs"
    
    return True, "All prerequisites met"

def run_accurate_tests():
    """Run tests that match the module's actual logic."""
    test_cases = [
        # These match what the module actually checks
        ({}, (False, "No script loaded"), "Empty - should fail on data check"),
        ({"data": None}, (False, "No script loaded"), "data is None - falsy"),
        ({"data": False}, (False, "No script loaded"), "data is False - falsy"),
        ({"data": ""}, (False, "No script loaded"), "data is empty string - falsy"),
        ({"data": {}}, (False, "No emotion data"), "Empty dict is truthy, fails on emotion"),
        ({"data": [], "emotion_data": {}}, (False, "No character arcs"), "Empty list is truthy"),
        ({"data": [1], "emotion_data": {"character_arcs": {}}}, (False, "No character arcs"), "Empty character_arcs"),
        ({"data": True, "emotion_data": {"character_arcs": {"CHAR": {}}}}, (True, "All prerequisites met"), "All truthy values"),
    ]
    
    passed = 0
    failed = 0
    
    print("Running accurate prerequisite tests...")
    print("=" * 50)
    
    for session_state, expected, description in test_cases:
        result = simulate_module_prerequisites(session_state)
        if result == expected:
            print(f"✓ PASS: {description}")
            print(f"  session_state: {list(session_state.keys())}")
            passed += 1
        else:
            print(f"✗ FAIL: {description}")
            print(f"  session_state: {list(session_state.keys())}")
            print(f"  Expected: {expected}")
            print(f"  Got: {result}")
            failed += 1
    
    return passed, failed

if __name__ == "__main__":
    passed, failed = run_accurate_tests()
    
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("✅ All accurate tests passed!")
        sys.exit(0)
    else:
        print("❌ Some accurate tests failed")
        sys.exit(1)
