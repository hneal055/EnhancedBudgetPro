import random
from datetime import datetime

import streamlit as st

# Only show if core data is loaded
if "data" not in st.session_state:
    st.stop()

st.title("🎬 Easter Eggs & Producer Fun!")

# Secret code unlock
if "egg_unlocked" not in st.session_state:
    st.session_state.egg_unlocked = False

with st.expander("Enter Secret Producer Code"):
    code = st.text_input("Producer Code", type="password")
    if code == "ACTION!":
        st.session_state.egg_unlocked = True
        st.success("Hollywood Mode Unlocked! 🍿")

if st.session_state.egg_unlocked:
    st.balloons()
    st.markdown("## 🌟 Welcome to Hollywood Mode!")
    st.image(
        "https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif",
        caption="You're a star producer now!",
    )

    # Fun film trivia
    trivia = [
        "The first feature-length film ever made was 'The Story of the Kelly Gang' (1906).",
        "The clapperboard was invented to help sync sound and picture.",
        "The longest film ever made is 'Logistics' (2012), running 857 hours!",
        "Alfred Hitchcock never won an Oscar for Best Director.",
        "The Wilhelm Scream has been used in over 400 movies.",
        "The most expensive movie ever made (adjusted for inflation) is 'Pirates of the Caribbean: On Stranger Tides'.",
    ]
    st.info(f"🎥 Fun Fact: {random.choice(trivia)}")

    # Random producer quote
    quotes = [
        "“The most honest form of filmmaking is to make a film for yourself.” – Peter Jackson",
        "“If it can be written, or thought, it can be filmed.” – Stanley Kubrick",
        "“Movies touch our hearts and awaken our vision.” – Martin Scorsese",
        "“Cinema is a matter of what's in the frame and what's out.” – Martin Scorsese",
        "“To make a great film you need three things – the script, the script and the script.” – Alfred Hitchcock",
    ]
    st.success(f"🎬 Producer Wisdom: {random.choice(quotes)}")

    # Show a fun "award"
    now = datetime.now()
    st.markdown(
        f"🏆 **Today's Award:** Best Producer on {now.strftime('%B %d, %Y')} goes to... **YOU!**"
    )

else:
    st.warning(
        "Enter the secret code to unlock Hollywood Mode and discover some film industry fun!"
    )
