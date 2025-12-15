def test_scene_notes_storage():
    # Simulate Streamlit session state
    session_state = {}
    # Add notes for scenes
    session_state['scene_notes'] = {}
    session_state['scene_notes'][1] = "This is a note for scene 1."
    session_state['scene_notes'][2] = "Another note for scene 2."
    # Retrieve and check
    assert session_state['scene_notes'][1] == "This is a note for scene 1."
    assert session_state['scene_notes'][2] == "Another note for scene 2."
    print("Scene notes storage and retrieval test passed.")

if __name__ == "__main__":
    test_scene_notes_storage()
