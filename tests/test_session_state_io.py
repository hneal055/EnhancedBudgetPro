import os
import json
import streamlit as st
from src.utils.session_state_io import save_session_state, load_session_state, SESSION_STATE_FILE

def test_save_and_load():
    # Set up mock session state
    st.session_state["foo"] = "bar"
    st.session_state["number"] = 42
    st.session_state["list"] = [1, 2, 3]

    # Save session state
    save_session_state()
    assert os.path.exists(SESSION_STATE_FILE), "Session state file was not created."

    # Clear session state and reload
    st.session_state.clear()
    load_session_state()
    assert st.session_state["foo"] == "bar"
    assert st.session_state["number"] == 42
    assert st.session_state["list"] == [1, 2, 3]

    # Clean up
    os.remove(SESSION_STATE_FILE)
    print("Session state save/load test passed.")

if __name__ == "__main__":
    test_save_and_load()
