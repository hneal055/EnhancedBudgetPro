import pandas as pd
import streamlit as st

st.title("📊 Data-Driven Insights")

# Ensure required data is present
if "data" not in st.session_state or not st.session_state.data:
    st.warning("No script data loaded. Please analyze a script first.")
    st.stop()

scenes = st.session_state.data.get("scenes", [])
characters = st.session_state.data.get("characters", [])


# Most Talkative Character
def get_most_talkative_character(characters):
    # Only consider dicts, per data contract: character stats should be dicts
    dict_chars = [c for c in characters if isinstance(c, dict)]
    if not dict_chars:
        return None, 0
    talkative = max(dict_chars, key=lambda c: c.get("dialogue_lines", 0))
    return talkative.get("name", "Unknown"), talkative.get("dialogue_lines", 0)


# Most Expensive Scene (requires budget info)
def get_most_expensive_scene(scenes):
    # Assume each scene has a 'budget' field if budget analysis was run
    expensive = max(scenes, key=lambda s: s.get("budget", 0), default=None)
    if expensive:
        return expensive.get("heading", "Unknown"), expensive.get("budget", 0)
    return None, 0


# Risk Bingo (show detected risks)
def get_risk_types(scenes):
    risks = set()
    for scene in scenes:
        for risk in scene.get("risks", []):
            risks.add(risk.get("risk_type", "Unknown"))
    return risks


# Display insights
char_name, char_lines = get_most_talkative_character(characters)
scene_heading, scene_budget = get_most_expensive_scene(scenes)
risk_types = get_risk_types(scenes)

st.subheader("🏅 Most Talkative Character")
if char_name:
    st.info(f"**{char_name}** with **{char_lines}** lines of dialogue.")
else:
    st.info("No character dialogue data available.")

st.subheader("💸 Most Expensive Scene")
if scene_heading and scene_budget > 0:
    st.success(f"**{scene_heading}** with a budget of **${scene_budget:,.2f}**")
else:
    st.info("No scene budget data available.")

st.subheader("🎲 Production Risk Bingo")
bingo_types = [
    "Weather",
    "Location",
    "Cast Availability",
    "Equipment",
    "Stunts",
    "Crowd Scenes",
    "Night Shoots",
    "Child Actors",
    "Animals",
    "Special FX",
]
bingo_status = [f"✅ {b}" if b in risk_types else f"⬜ {b}" for b in bingo_types]
st.write(" | ".join(bingo_status))

if risk_types:
    st.markdown(f"**Risks detected:** {', '.join(sorted(risk_types))}")
else:
    st.info("No risks detected in current script data.")

st.caption(
    "These insights are generated from your current script and budget analysis. For more, check the Financial Intelligence and Risk Monte Carlo pages."
)
