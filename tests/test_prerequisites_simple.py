"""
Simple test for Storytelling Insights prerequisites.
Tests the logic without external dependencies.
"""

import sys

def check_prerequisites(session_state):
    """Check if all prerequisites are met."""
    # Check 1: 'data' key exists in session_state (even if empty)
    if "data" not in session_state:
        return False, "No script loaded"
    
    # Check 2: 'emotion_data' key exists in session_state
    if "emotion_data" not in session_state:
        return False, "No emotion data"
    
    # Check 3: character_arcs exists in emotion_data and is not empty
    emotion_data = session_state.get("emotion_data", {})
    
    # Handle both dict access and .get() method
    if hasattr(emotion_data, "get"):
        character_arcs = emotion_data.get("character_arcs", {})
    else:
        # If emotion_data is not a dict-like object, treat as empty
        character_arcs = {}
    
    if not character_arcs:
        return False, "No character arcs"
    
    return True, "All prerequisites met"

def run_tests():
    """Run all test cases."""
    test_cases = [
        # (session_state, expected_result, description)
        ({}, (False, "No script loaded"), "Empty session state"),
        ({"data": {}}, (False, "No emotion data"), "Only data present"),
        ({"data": {}, "emotion_data": {}}, (False, "No character arcs"), "No character arcs"),
        ({"data": {}, "emotion_data": {"character_arcs": {}}}, (False, "No character arcs"), "Empty character arcs"),
        ({"data": {}, "emotion_data": {"character_arcs": {"CHAR": {}}}}, (True, "All prerequisites met"), "All prerequisites met"),
    ]
    
    passed = 0
    failed = 0
    
    for session_state, expected, description in test_cases:
        result = check_prerequisites(session_state)
        if result == expected:
            print(f"✓ PASS: {description}")
            passed += 1
        else:
            print(f"✗ FAIL: {description}")
            print(f"  Expected: {expected}")
            print(f"  Got: {result}")
            failed += 1
    
    return passed, failed

if __name__ == "__main__":
    print("Running prerequisite tests...")
    print("=" * 50)
    
    passed, failed = run_tests()
    
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed")
        sys.exit(1)
