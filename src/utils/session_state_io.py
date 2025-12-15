import streamlit as st
import json
import os

SESSION_STATE_FILE = "session_state.json"

def is_json_serializable(value):
    try:
        json.dumps(value)
        return True
    except Exception:
        return False

def save_session_state():
    try:
        # Only save serializable keys
        state = {k: v for k, v in st.session_state.items() if is_json_serializable(v)}
        with open(SESSION_STATE_FILE, "w") as f:
            json.dump(state, f)
    except Exception as e:
        st.warning(f"Session state could not be saved: {e}")

def load_session_state():
    if os.path.exists(SESSION_STATE_FILE):
        try:
            with open(SESSION_STATE_FILE, "r") as f:
                state = json.load(f)
            for k, v in state.items():
                st.session_state[k] = v
        except Exception as e:
            st.warning(f"Session state could not be loaded: {e}")
