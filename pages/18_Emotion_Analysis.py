import streamlit as st

st.title("Emotion Analysis")

if "data" not in st.session_state:
    st.warning("Please upload and analyze a script first.")
    st.stop()

if "emotion_data" not in st.session_state:
    st.session_state["emotion_data"] = {}

st.info("This page is under construction. Core logic coming soon.")