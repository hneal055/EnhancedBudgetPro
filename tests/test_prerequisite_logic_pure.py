"""
Pure logic test - no Streamlit, no mocking.
Tests the extracted business logic.
"""

import sys

def check_prerequisites(session_state):
    """
    Check prerequisites based on the module's logic.
    This simulates: if not st.session_state.get("key"): st.stop()
    """
    # Check for data
    if not session_state.get("data"):
        return False, "No script loaded"
    
    # Check for emotion_data
    if not session_state.get("emotion_data"):
        return False, "No emotion data"
    
    # Check for character_arcs
    emotion_data = session_state.get("emotion_data", {})
    if hasattr(emotion_data, "get"):
        character_arcs = emotion_data.get("character_arcs", {})
    else:
        character_arcs = {}
    
    if not character_arcs:
        return False, "No character arcs"
    
    return True, "All prerequisites met"

def run_pure_logic_tests():
    """Run pure logic tests without any dependencies."""
    
    print("Running PURE LOGIC prerequisite tests")
    print("=" * 60)
    print("Testing: if not session_state.get('key')")
    print("This checks for FALSY values, not just missing keys")
    print("=" * 60)
    
    test_cases = [
        # Falsy values for data
        ({}, (False, "No script loaded"), "Empty session state"),
        ({"data": None}, (False, "No script loaded"), "data = None"),
        ({"data": False}, (False, "No script loaded"), "data = False"),
        ({"data": 0}, (False, "No script loaded"), "data = 0"),
        ({"data": ""}, (False, "No script loaded"), "data = ''"),
        ({"data": {}}, (False, "No script loaded"), "data = {}"),
        ({"data": []}, (False, "No script loaded"), "data = []"),
        
        # Truthy data, falsy emotion_data
        ({"data": "some_data", "emotion_data": None}, (False, "No emotion data"), "data truthy, emotion_data = None"),
        ({"data": [1], "emotion_data": {}}, (False, "No emotion data"), "data truthy, emotion_data = {}"),
        ({"data": True, "emotion_data": False}, (False, "No emotion data"), "data truthy, emotion_data = False"),
        
        # Both truthy, missing or empty character_arcs
        ({"data": True, "emotion_data": {"other": "value"}}, (False, "No character arcs"), "No character_arcs key"),
        ({"data": True, "emotion_data": {"character_arcs": {}}}, (False, "No character arcs"), "Empty character_arcs"),
        ({"data": True, "emotion_data": {"character_arcs": []}}, (False, "No character arcs"), "Empty character_arcs list"),
        
        # Success cases
        ({"data": "script", "emotion_data": {"character_arcs": {"CHAR": {}}}}, (True, "All prerequisites met"), "Basic success"),
        ({"data": [1,2,3], "emotion_data": {"character_arcs": {"A": 1, "B": 2}}}, (True, "All prerequisites met"), "Non-empty structures"),
        ({"data": {"scenes": []}, "emotion_data": {"character_arcs": {"PROTAGONIST": {"arc": "Hero"}}}}, (True, "All prerequisites met"), "Complex structures"),
    ]
    
    passed = 0
    failed = 0
    
    for i, (session_state, expected, description) in enumerate(test_cases, 1):
        result = check_prerequisites(session_state)
        
        # Simple display
        state_desc = []
        for key in ["data", "emotion_data"]:
            if key in session_state:
                val = session_state[key]
                if isinstance(val, (dict, list)):
                    state_desc.append(f"{key}: {type(val).__name__}[{len(val)}]")
                elif val is None:
                    state_desc.append(f"{key}: None")
                else:
                    state_desc.append(f"{key}: {type(val).__name__}")
        
        if result == expected:
            print(f"{i:2d}. ✓ {description}")
            print(f"    State: {', '.join(state_desc)}")
            passed += 1
        else:
            print(f"{i:2d}. ✗ {description}")
            print(f"    State: {', '.join(state_desc)}")
            print(f"    Expected: {expected}")
            print(f"    Got: {result}")
            failed += 1
    
    return passed, failed

if __name__ == "__main__":
    passed, failed = run_pure_logic_tests()
    
    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("✅ ALL PURE LOGIC TESTS PASSED!")
        print("The prerequisite logic is working correctly.")
        sys.exit(0)
    else:
        print("❌ Some tests failed - check logic implementation")
        sys.exit(1)
