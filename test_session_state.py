import streamlit as st

st.title("🔍 Session State Debug")

st.subheader("Current Session State:")
for key in st.session_state.keys():
    if key == "emotion_data":
        emotion_data = st.session_state[key]
        if emotion_data:
            st.write(f"**{key}:**")
            st.write(f"  - character_arcs keys: {list(emotion_data.get('character_arcs', {}).keys())}")
            st.write(f"  - summary: {emotion_data.get('summary', {})}")
    else:
        st.write(f"**{key}:** {type(st.session_state[key])}")

st.divider()

if st.button("🗑️ CLEAR ALL SESSION STATE"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.success("✅ Session state cleared! Please go to Page 1 and re-analyze your script.")
    st.rerun()
