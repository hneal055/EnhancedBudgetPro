import random
from datetime import datetime, timedelta

import streamlit as st

st.title("🎬 Producer Personalization")

# 1. Producer Avatar Selection
avatars = {
    "Classic Producer": "🧑‍💼",
    "Director": "🎬",
    "Cinematographer": "🎥",
    "Screenwriter": "✍️",
    "Studio Exec": "💼",
    "Indie Maverick": "🧢",
}
avatar_choice = st.selectbox("Choose your Producer Avatar:", list(avatars.keys()))
st.markdown(f"## Your Avatar: {avatars[avatar_choice]} {avatar_choice}")

# 2. Upload a Profile Picture
profile_pic = st.file_uploader(
    "Upload your Producer Profile Picture (optional)", type=["png", "jpg", "jpeg"]
)
if profile_pic:
    st.image(profile_pic, width=150, caption="Your Producer Profile")

# 3. Track Production Streak
if "last_analysis_date" not in st.session_state:
    st.session_state.last_analysis_date = None
if "production_streak" not in st.session_state:
    st.session_state.production_streak = 0

today = datetime.now().date()
if st.button("Log Today's Analysis"):
    if st.session_state.last_analysis_date == today:
        st.info("You've already logged an analysis today! 🎉")
    else:
        if st.session_state.last_analysis_date == today - timedelta(days=1):
            st.session_state.production_streak += 1
        else:
            st.session_state.production_streak = 1
        st.session_state.last_analysis_date = today
        st.success(
            f"Production streak updated! Current streak: {st.session_state.production_streak} days."
        )

st.markdown(
    f"### 🏆 Current Production Streak: **{st.session_state.production_streak}** days"
)

# 4. Fun personalized message
messages = [
    "Keep rolling, Producer! Every day on set counts.",
    "Lights, camera, action! Your streak is impressive.",
    "The best producers never take a day off!",
    "Your crew is lucky to have such dedication.",
    "Another day, another masterpiece in the making.",
]
st.info(random.choice(messages))
